"""Dialect-LODO fold construction for Arm B (within-indirect dialect transfer).

The cross-family / dialect-transfer sibling of ``attack-type-lodo/folds.py`` — it **imports**
the shared ``Fold`` dataclass + ``carve_val_from_train`` helper from that module rather than
copying them (ADR-026, library-first; the hyphenated experiment dirs resolve via sys.path).

Per the pre-registration (``criteria.md`` §Design / §Fold construction):

* hold out one indirect **dialect** at a time over {bipia, browsesafe, fujitsu, injecagent};
* **two training compositions** per fold:
    - **B+** = (the other 3 indirect dialects) ∪ (the direct base pool from Arm A);
    - **B−** = (the other 3 indirect dialects) only;
* the held-out **dialect** is the only shifted axis → :func:`assert_dialect_disjoint`;
* val is carved **in-(train-)distribution** with the attack-type mini-LODO **disabled**
  (``min_types_for_typeholdout = 10**9``; carrier-LODO Rev 2), so ``val_roc`` does not inherit
  the attack-type collapse and ``Gx = val_roc − test_roc`` isolates the dialect shift.

B2.0 status: **B− is fully working now.** B+ wires the variant switch but leaves the direct-base
loading as a clearly-marked TODO (Arm A's direct pool is built later, at B2.4).
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path
from typing import Literal

import pandas as pd

_HERE = Path(__file__).resolve().parent
_ATTACK_LODO_DIR = _HERE.parent / "attack-type-lodo"
if str(_ATTACK_LODO_DIR) not in sys.path:
    sys.path.insert(0, str(_ATTACK_LODO_DIR))

# Shared primitives reused from the attack-type-LODO harness (single source of truth).
from folds import Fold, carve_val_from_train  # noqa: E402

__all__ = [
    "Fold",
    "Variant",
    "LODO_DIALECTS",
    "DIALECT_LODO_FOLDS",
    "assert_dialect_disjoint",
    "make_dialect_fold",
    "load_direct_base",
]

Variant = Literal["B+", "B-"]

_LODO_DIALECTS: tuple[str, ...] = ("bipia", "browsesafe", "fujitsu", "injecagent")
LODO_DIALECTS: tuple[str, ...] = _LODO_DIALECTS
DIALECT_LODO_FOLDS: tuple[str, ...] = tuple(f"dialect_lodo_{d}" for d in _LODO_DIALECTS)


def _dialect_lodo_builder(
    held_out: str,
) -> Callable[[pd.DataFrame], tuple[pd.DataFrame, pd.DataFrame]]:
    """Factory: a leave-one-dialect-out builder holding out ``held_out``.

    Train = all rows with ``dialect != held_out``; test = all rows with ``dialect == held_out``.
    The dialect is the only held-out axis.
    """
    if held_out not in _LODO_DIALECTS:
        raise KeyError(f"unknown dialect {held_out!r}; expected one of {_LODO_DIALECTS}")

    def build(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        train = frame[frame["dialect"] != held_out].reset_index(drop=True)
        test = frame[frame["dialect"] == held_out].reset_index(drop=True)
        return train, test

    return build


def assert_dialect_disjoint(train: pd.DataFrame, test: pd.DataFrame) -> None:
    """Raise ``ValueError`` if train and test share a dialect or an exact text.

    The dialect-LODO sibling of ``folds.assert_carrier_disjoint``: the claim is void if the
    held-out dialect also appears in training. Attack types / carriers are **not** the held-out
    axis here, so they may overlap. Cross-corpus exact-text overlap is nil by construction and
    kept as a defensive guard (the fuzzy near-dup purge is the separate :mod:`leakage_gate`).

    Parameters
    ----------
    train, test : pandas.DataFrame
        Fold splits with ``dialect`` / ``text`` columns.

    Raises
    ------
    ValueError
        If a dialect or an exact text is shared across the split boundary.
    """
    train_dialects = {str(d) for d in train["dialect"].unique()}
    test_dialects = {str(d) for d in test["dialect"].unique()}
    overlap = train_dialects & test_dialects
    if overlap:
        raise ValueError(f"train↔test dialect overlap: {sorted(overlap)}")

    text_overlap = set(train["text"].astype(str)) & set(test["text"].astype(str))
    if text_overlap:
        raise ValueError(f"train↔test exact-text overlap: {len(text_overlap)} shared texts")


_ARM_A_LEAKAGE_MANIFEST = _HERE / "B2_leakage" / "leakage_gate_armA.json"


def _load_leakage_manifest() -> frozenset[str] | None:
    """Normalized texts purged by the Arm-A leakage gate (B2.4 §vi), or None if it has not run.

    The cap in :func:`assemble_arm_a.load_direct_base` consumes this so B+ draws the direct base
    from leakage-free rows (pipeline order dedup → gate → cap; decision 9). Absent manifest ⇒ no
    purge (the gate is a Phase-A precondition; on the first build it simply has not run yet).
    """
    if not _ARM_A_LEAKAGE_MANIFEST.exists():
        return None
    import json

    data = json.loads(_ARM_A_LEAKAGE_MANIFEST.read_text(encoding="utf-8"))
    purged = data.get("purged_normalized_texts", [])
    return frozenset(str(t) for t in purged)


def load_direct_base() -> pd.DataFrame:
    """Load the Arm-A direct-injection base pool (criteria.md B2.4 — re-export; unblocks B+).

    Thin wrapper over :func:`assemble_arm_a.load_direct_base` (the capped-balanced direct pool,
    rebuilt from our audited ``data/raw/``). Passes the persisted leakage clean-manifest so the
    cap draws from leakage-free rows.

    Returns
    -------
    pandas.DataFrame
        Columns ``text, label, dialect, cluster_id`` with ``dialect == "direct_base"``.
    """
    from assemble_arm_a import load_direct_base as _load

    return _load(clean_manifest=_load_leakage_manifest())


def make_dialect_fold(
    frame: pd.DataFrame,
    held_out: str,
    *,
    variant: Variant = "B-",
    seed: int = 0,
    **carve_kwargs: object,
) -> Fold:
    """Build one dialect-LODO :class:`Fold`: split → (B+ augment) → assert disjoint → carve val.

    Parameters
    ----------
    frame : pandas.DataFrame
        The unified Arm-B frame (``assemble.assemble`` output) — needs ``text, label, dialect``.
    held_out : str
        One of :data:`LODO_DIALECTS`.
    variant : {"B+", "B-"}
        ``"B-"`` → train = the other 3 indirect dialects only (fully working).
        ``"B+"`` → train = the other 3 indirect dialects ∪ the direct base pool (TODO B2.4).
    seed : int
        Validation-carve seed.
    **carve_kwargs
        Forwarded to ``folds.carve_val_from_train``. ``min_types_for_typeholdout`` is forced to
        ``10**9`` (Rev-2 in-distribution carve) unless explicitly overridden.

    Raises
    ------
    KeyError
        If ``held_out`` is not a known dialect.
    ValueError
        Propagated from :func:`assert_dialect_disjoint` / ``carve_val_from_train``.
    NotImplementedError
        If ``variant == "B+"`` (the direct base pool is not built yet).
    """
    if held_out not in _LODO_DIALECTS:
        raise KeyError(f"unknown dialect {held_out!r}; expected one of {_LODO_DIALECTS}")
    if variant not in ("B+", "B-"):
        raise ValueError(f"unknown variant {variant!r}; expected 'B+' or 'B-'")

    train_full, test = _dialect_lodo_builder(held_out)(frame)

    if variant == "B+":
        direct = load_direct_base()  # raises NotImplementedError until B2.4
        train_full = pd.concat([train_full, direct], ignore_index=True)

    assert_dialect_disjoint(train_full, test)

    # In-distribution val reference (criteria.md §Shared, mirroring carrier-LODO Rev 2): disable
    # the attack-type mini-LODO so the carve is a label-stratified row-holdout with attack type
    # held fixed — never a type-holdout — so val_roc stays in-(train-)distribution.
    carve: dict[str, object] = dict(carve_kwargs)
    carve.setdefault("min_types_for_typeholdout", 10**9)

    # The unified frame has no single shared attack_type axis across dialects; carve_val_from_train
    # reads "attack_type" for the (now-disabled) type-holdout branch, so guarantee the column.
    if "attack_type" not in train_full.columns:
        train_full = train_full.assign(attack_type="")
    else:
        train_full = train_full.assign(attack_type=train_full["attack_type"].fillna(""))

    inner, val = carve_val_from_train(train_full, seed=seed, **carve)  # type: ignore[arg-type]

    # test_types: the held-out dialect carries no shared attack-type axis → report its dialect tag.
    return Fold(
        name=f"dialect_lodo_{held_out}", train=inner, val=val, test=test, test_types=(held_out,)
    )
