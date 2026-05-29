"""BIPIA carrier-preserving loader for the pre-modeling OOD-wall prediction.

Portfolio-specific glue (per `docs/planning/eda-design.md`: "portfolio-specific =
BIPIA carrier/taxonomy views"). Constructs the `(text, label)` rows a content
classifier would see — a scenario context with one BIPIA attack string injected
(positive) vs the clean context (negative) — while **preserving** the
`attack_type` / `subfamily` / `carrier` / `position` metadata the attack-type-LODO
folds + the A1 cube need.

Data is local at `data/raw/BIPIA/benchmark/` (verified in RC0):
- `text_attack_{train,test}.json` — `{attack_type: [5 strings]}`, 15 types each.
- `{email,code,table}/{train,test}.jsonl` — lines with a `context` field.
- `qa/`, `abstract/` carriers are license-gated (newsqa / XSum) → excluded.

The "Language Translation" attack-type is the only train/test overlap → dropped
(RC0 criterion i), yielding the 14v14 disjoint split.

Injection is a documented, consistent **suffix** injection (`context\\n\\nattack`);
the predicted collapse *ranking* is robust to the template so long as it is held
fixed (the absolute scores are not the deliverable — the rank is).
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

# The single train/test overlapping attack-type (RC0 criterion i) — dropped so
# train and test attack-type sets are disjoint.
OVERLAP_DROP: frozenset[str] = frozenset({"Language Translation"})

# Obfuscation-subfamily attack types (harness-spec §2 obfuscation sub-split). The
# train side mutates surface form by substitution/spacing; the test side by
# encoding/transformation — the cleanest *technique*-generalization slice.
OBFUSCATION_TRAIN: frozenset[str] = frozenset(
    {
        "Alphanumeric Substitution",
        "Homophonic Substitution",
        "Misspelling Intentionally",
        "Anagramming",
        "Space Removal & Grouping",
    }
)
OBFUSCATION_TEST: frozenset[str] = frozenset(
    {
        "Substitution Ciphers",
        "Base Encoding",
        "Reverse Text",
        "Emoji Substitution",
    }
)
_OBFUSCATION_ALL: frozenset[str] = OBFUSCATION_TRAIN | OBFUSCATION_TEST

# Carriers with redistributable context data (email/code/table). qa + abstract
# need license-gated context generation → excluded (honest ceiling).
CARRIERS: tuple[str, ...] = ("email", "code", "table")


def subfamily(attack_type: str) -> str:
    """Return ``"obfuscation"`` for technique-mutation types, else ``"task-intent"``."""
    return "obfuscation" if attack_type in _OBFUSCATION_ALL else "task-intent"


def load_attack_pools(split: str, *, root: Path) -> dict[str, list[str]]:
    """Load ``{attack_type: [strings]}`` for a split, dropping the overlap type.

    Parameters
    ----------
    split : str
        ``"train"`` or ``"test"``.
    root : Path
        BIPIA benchmark root (``data/raw/BIPIA/benchmark``).

    Returns
    -------
    dict[str, list[str]]
    """
    path = root / f"text_attack_{split}.json"
    raw: dict[str, list[str]] = json.loads(path.read_text(encoding="utf-8"))
    return {atype: strings for atype, strings in raw.items() if atype not in OVERLAP_DROP}


def load_contexts(carrier: str, split: str, *, root: Path) -> list[str]:
    """Load the ``context`` strings for one carrier + split from its ``.jsonl``."""
    path = root / carrier / f"{split}.jsonl"
    contexts: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        contexts.append(json.loads(line)["context"])
    return contexts


def inject(context: str, attack: str) -> str:
    """Suffix-inject ``attack`` into ``context`` (the fixed injection template)."""
    return f"{context}\n\n{attack}"


@dataclass(frozen=True, slots=True)
class CarrierExamples:
    """The constructed BIPIA rows + the disjoint attack-type sets.

    Attributes
    ----------
    frame : pandas.DataFrame
        Columns: ``text``, ``label`` (1 positive / 0 clean-negative), ``attack_type``
        (``""`` for negatives), ``subfamily``, ``carrier``, ``position``, ``role``
        (``"train"`` / ``"test"``), ``source`` (``"inject"`` / ``"clean"``).
    train_types, test_types : tuple[str, ...]
        The disjoint attack-type sets (14 each after the overlap drop).
    """

    frame: pd.DataFrame
    train_types: tuple[str, ...]
    test_types: tuple[str, ...]


def build_examples(
    *,
    root: Path,
    contexts_per_attack: int = 12,
    carriers: Sequence[str] = CARRIERS,
    seed: int = 0,
) -> CarrierExamples:
    """Build the carrier-injected `(text, label)` rows with preserved metadata.

    For each carrier + split, every attack string is injected into a deterministic
    sample of ``contexts_per_attack`` contexts (positives); the sampled clean
    contexts are emitted once per split as negatives. Sampling keeps the pools
    bounded (BIPIA's signal is the ~5 payloads/type, not context volume).

    Parameters
    ----------
    root : Path
        BIPIA benchmark root.
    contexts_per_attack : int, optional
        Contexts each attack string is injected into (per carrier/split).
    carriers : sequence of str, optional
        Which carriers to use. Default :data:`CARRIERS` (email/code/table).
    seed : int, optional
        Deterministic context-sampling seed.

    Returns
    -------
    CarrierExamples
    """
    import numpy as np  # local import: keep module import torch/np-light for tests

    rng = np.random.default_rng(seed)
    rows: list[dict[str, object]] = []
    train_types: set[str] = set()
    test_types: set[str] = set()

    for split, type_acc in (("train", train_types), ("test", test_types)):
        pools = load_attack_pools(split, root=root)
        type_acc.update(pools)
        for carrier in carriers:
            contexts = load_contexts(carrier, split, root=root)
            if not contexts:
                continue
            ctx_arr = np.asarray(contexts, dtype=object)
            # Negatives: clean contexts (deduped sample, once per carrier/split).
            # Scaled by the type count so carriers with many contexts (table ~900)
            # contribute more balance; email/code are context-limited (~50) so they
            # cap out — the residual imbalance is handled by the driver (balanced
            # C2 fit + NotInject hard negatives).
            n_clean = min(len(contexts), contexts_per_attack * 14)
            clean_idx = rng.choice(len(contexts), size=n_clean, replace=False)
            for ci in clean_idx:
                rows.append(
                    {
                        "text": str(ctx_arr[ci]),
                        "label": 0,
                        "attack_type": "",
                        "subfamily": "benign",
                        "carrier": carrier,
                        "position": "none",
                        "role": split,
                        "source": "clean",
                    }
                )
            # Positives: each attack string injected into a context sample.
            for atype, strings in pools.items():
                fam = subfamily(atype)
                for attack in strings:
                    k = min(len(contexts), contexts_per_attack)
                    idx = rng.choice(len(contexts), size=k, replace=False)
                    for ci in idx:
                        rows.append(
                            {
                                "text": inject(str(ctx_arr[ci]), attack),
                                "label": 1,
                                "attack_type": atype,
                                "subfamily": fam,
                                "carrier": carrier,
                                "position": "suffix",
                                "role": split,
                                "source": "inject",
                            }
                        )

    frame = pd.DataFrame(rows)
    return CarrierExamples(
        frame=frame,
        train_types=tuple(sorted(train_types)),
        test_types=tuple(sorted(test_types)),
    )
