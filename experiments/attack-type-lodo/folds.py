"""Attack-type-LODO fold construction (ADR-052 harness, spec §2/§3/§6).

Builds the three pre-registered leave-one-distribution-out (LODO) folds over the
BIPIA carrier-injected rows from
:func:`experiments.eda.OOD_WALL_PREDICTION.bipia_carrier.build_examples`, carves a
train-internal validation split (spec §3, never touching the test attack-types or
contexts), and asserts train/test source-disjointness (spec §6 pre-run check).

Fold geometry mirrors the pre-modeling prediction's fold definitions
(``run_prediction.py:202-213``) so the harness scores exactly the distributions the
OOD-wall prediction was registered against.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

# Reuse the EDA loader + the frozen obfuscation/carrier taxonomy (single source of
# truth). The loader lives in the OOD_WALL_PREDICTION sibling directory.
_OOD_DIR = Path(__file__).resolve().parents[1] / "eda" / "OOD_WALL_PREDICTION"
if str(_OOD_DIR) not in sys.path:
    sys.path.insert(0, str(_OOD_DIR))

from bipia_carrier import OBFUSCATION_TEST, OBFUSCATION_TRAIN  # noqa: E402

__all__ = [
    "Fold",
    "FOLD_NAMES",
    "CARRIER_LODO_FOLDS",
    "make_fold",
    "assert_source_disjoint",
    "assert_carrier_disjoint",
    "purge_train_context_overlap",
    "carve_val_from_train",
]

# Leave-one-carrier-out folds (carrier-lodo/criteria.md Revision 1): hold out each available
# BIPIA carrier in turn; the carrier is the ONLY shifted axis (attack types are shared).
_LODO_CARRIERS: tuple[str, ...] = ("email", "code", "table")
CARRIER_LODO_FOLDS: tuple[str, ...] = tuple(f"carrier_lodo_{c}" for c in _LODO_CARRIERS)

FOLD_NAMES: tuple[str, ...] = (
    "core_attack_type",
    "obfuscation_technique",
    "carrier_plus_attack_external",
    *CARRIER_LODO_FOLDS,
)

_EXTERNAL_TRAIN_CARRIERS = ("code", "table")
_EXTERNAL_TEST_CARRIER = "email"


@dataclass(frozen=True, slots=True)
class Fold:
    """A train/val/test split for one LODO fold.

    Attributes
    ----------
    name : str
        Fold identifier (one of :data:`FOLD_NAMES`).
    train, val, test : pandas.DataFrame
        Row subsets of the ``build_examples`` frame. ``val`` is carved from the
        fold's training rows only (spec §3) and shares no test attack-type/context.
    test_types : tuple[str, ...]
        The held-out test attack-types scored per-type (the §6.5 diagnostic axis).
    """

    name: str
    train: pd.DataFrame
    val: pd.DataFrame
    test: pd.DataFrame
    test_types: tuple[str, ...]


def _test_types(test: pd.DataFrame) -> tuple[str, ...]:
    """Sorted unique positive attack-types present in a test split."""
    types = test.loc[test["label"] == 1, "attack_type"].unique().tolist()
    return tuple(sorted(t for t in types if t))


def _build_core(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Core attack-type-LODO (carrier constant): split by BIPIA's role column.

    Train rows carry train-attack-types, test rows carry the disjoint test-attack-
    types (``build_examples`` loads disjoint train/test attack pools), so the only
    shift is attack type. This is the headline fold (spec §2).
    """
    train = frame[frame["role"] == "train"].reset_index(drop=True)
    test = frame[frame["role"] == "test"].reset_index(drop=True)
    return train, test


def _build_obfuscation(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Obfuscation technique-LODO: train surface-mutation types → test encoding types.

    Positives restricted to the obfuscation subfamily; negatives are the role-matched
    clean contexts (spec §2 obfuscation sub-split).
    """
    pos = frame["label"] == 1
    neg = frame["label"] == 0
    is_train = frame["role"] == "train"
    is_test = frame["role"] == "test"
    train_pos = pos & is_train & frame["attack_type"].isin(OBFUSCATION_TRAIN)
    test_pos = pos & is_test & frame["attack_type"].isin(OBFUSCATION_TEST)
    train = frame[train_pos | (neg & is_train)].reset_index(drop=True)
    test = frame[test_pos | (neg & is_test)].reset_index(drop=True)
    return train, test


def _build_carrier_external(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Joint carrier+attack external shift: train {code,table} → test {email} (spec §2)."""
    is_train = frame["role"] == "train"
    is_test = frame["role"] == "test"
    train = frame[is_train & frame["carrier"].isin(_EXTERNAL_TRAIN_CARRIERS)].reset_index(drop=True)
    test = frame[is_test & (frame["carrier"] == _EXTERNAL_TEST_CARRIER)].reset_index(drop=True)
    return train, test


def _carrier_lodo_builder(
    held_out: str,
) -> Callable[[pd.DataFrame], tuple[pd.DataFrame, pd.DataFrame]]:
    """Factory: a leave-one-carrier-out builder holding out ``held_out`` (criteria.md Rev 1).

    Train = all rows with ``carrier != held_out`` (both BIPIA roles, all attack types); test = all
    rows with ``carrier == held_out``. The carrier is the ONLY held-out axis — attack types are
    shared across the split — so carrier-LODO folds assert :func:`assert_carrier_disjoint`, not the
    attack-type :func:`assert_source_disjoint`.
    """

    def build(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        train = frame[frame["carrier"] != held_out].reset_index(drop=True)
        test = frame[frame["carrier"] == held_out].reset_index(drop=True)
        return train, test

    return build


_BUILDERS: dict[str, Callable[[pd.DataFrame], tuple[pd.DataFrame, pd.DataFrame]]] = {
    "core_attack_type": _build_core,
    "obfuscation_technique": _build_obfuscation,
    "carrier_plus_attack_external": _build_carrier_external,
    **{
        name: _carrier_lodo_builder(carrier)
        for name, carrier in zip(CARRIER_LODO_FOLDS, _LODO_CARRIERS, strict=True)
    },
}


def _row_context(text: str, label: int) -> str:
    """The underlying clean context of a row.

    For a negative the context **is** the text; for a positive it is the prefix before
    the final ``"\\n\\n"`` — the inverse of the fixed suffix-injection template
    ``f"{context}\\n\\n{attack}"`` (``bipia_carrier.inject``). BIPIA attack payloads are
    single-segment, so ``rsplit(maxsplit=1)`` recovers the context even when the context
    itself contains blank lines.
    """
    return text if label == 0 else text.rsplit("\n\n", 1)[0]


def _underlying_contexts(df: pd.DataFrame) -> set[str]:
    """Set of underlying clean contexts across **both** classes of a split."""
    return {_row_context(t, lab) for t, lab in zip(df["text"], df["label"], strict=True)}


def purge_train_context_overlap(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    """Drop train rows whose underlying context also appears in test (leakage hygiene).

    BIPIA's ``email`` train/test splits share 11 identical clean contexts (``code`` /
    ``table``: none), so the spec §1 assumption that BIPIA's own split keeps contexts
    disjoint does **not** hold. Per the resolved dedup policy (2026-05-29): purge from
    the **train** side — any train row (positive or negative) built on a context that
    also appears on the test side is removed, so the test split stays exactly BIPIA's
    designated eval target while training never sees a test context (the
    context-memorization confound the §6 assertion guards against).

    Parameters
    ----------
    train, test : pandas.DataFrame
        Fold splits with ``label`` / ``text`` columns.

    Returns
    -------
    pandas.DataFrame
        ``train`` with context-overlapping rows removed, index reset.
    """
    test_contexts = _underlying_contexts(test)
    keep = [
        _row_context(t, lab) not in test_contexts
        for t, lab in zip(train["text"], train["label"], strict=True)
    ]
    return train[pd.Series(keep, index=train.index)].reset_index(drop=True)


def assert_source_disjoint(train: pd.DataFrame, test: pd.DataFrame) -> None:
    """Raise ``ValueError`` if train and test share an attack-type or an underlying context.

    The spec §6 pre-run check: the LODO claim is void if any test attack-type was seen
    in training, or if any context appears on both sides (context-memorization confound).
    The context check compares **underlying** contexts across both classes (a positive's
    context is its pre-injection prefix) — the spec's original "BIPIA's split is disjoint"
    premise proved false for ``email`` (11 shared contexts), so the check no longer trusts
    it; :func:`purge_train_context_overlap` is the paired remediation run before this gate.

    Parameters
    ----------
    train, test : pandas.DataFrame
        Fold splits with ``label`` / ``attack_type`` / ``text`` columns.

    Raises
    ------
    ValueError
        If an attack-type or an underlying context is shared across the split boundary.
    """
    train_types = {t for t in train.loc[train["label"] == 1, "attack_type"].unique() if t}
    test_types = {t for t in test.loc[test["label"] == 1, "attack_type"].unique() if t}
    type_overlap = train_types & test_types
    if type_overlap:
        raise ValueError(f"train↔test attack-type overlap: {sorted(type_overlap)}")

    ctx_overlap = _underlying_contexts(train) & _underlying_contexts(test)
    if ctx_overlap:
        raise ValueError(f"train↔test context overlap: {len(ctx_overlap)} shared contexts")


def assert_carrier_disjoint(train: pd.DataFrame, test: pd.DataFrame) -> None:
    """Raise ``ValueError`` if train and test share a carrier or an underlying context.

    The carrier-LODO sibling of :func:`assert_source_disjoint` (carrier-lodo/criteria.md Rev 1):
    the carrier-LODO claim is void if the held-out carrier also appears in training. Attack types
    are **shared** across the split by design (the carrier is the only shifted axis), so attack-type
    overlap is **not** an error here. Cross-carrier contexts are disjoint by construction (each
    carrier owns its context pool); the context check is kept as a defensive guard.

    Parameters
    ----------
    train, test : pandas.DataFrame
        Fold splits with ``carrier`` / ``label`` / ``text`` columns.

    Raises
    ------
    ValueError
        If a carrier or an underlying context is shared across the split boundary.
    """
    train_carriers = {str(c) for c in train["carrier"].unique()}
    test_carriers = {str(c) for c in test["carrier"].unique()}
    carrier_overlap = train_carriers & test_carriers
    if carrier_overlap:
        raise ValueError(f"train↔test carrier overlap: {sorted(carrier_overlap)}")

    ctx_overlap = _underlying_contexts(train) & _underlying_contexts(test)
    if ctx_overlap:
        raise ValueError(f"train↔test context overlap: {len(ctx_overlap)} shared contexts")


def carve_val_from_train(
    train: pd.DataFrame,
    *,
    seed: int = 0,
    n_val_types: int = 3,
    min_types_for_typeholdout: int = 6,
    val_frac: float = 0.2,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carve a validation split from training rows only (spec §3).

    When the fold has enough train attack-types (``>= min_types_for_typeholdout``),
    hold out ``n_val_types`` of them as a **mini-LODO** validation set (the recipe is
    then selected for generalization, not in-distribution fit) plus a ``val_frac``
    share of clean negatives. Otherwise fall back to a label-stratified ``val_frac``
    row holdout. Never touches test attack-types/contexts.

    Returns
    -------
    (inner_train, val) : tuple[pandas.DataFrame, pandas.DataFrame]

    Raises
    ------
    ValueError
        If either resulting split lacks both classes (val/inner must be scorable).
    """
    t = train.reset_index(drop=True)
    labels = t["label"].to_numpy()
    rng = np.random.default_rng(seed)
    in_val = np.zeros(len(t), dtype=bool)

    train_types = sorted({a for a in t.loc[t["label"] == 1, "attack_type"].unique() if a})
    if len(train_types) >= min_types_for_typeholdout:
        k = min(n_val_types, len(train_types) - 1)  # keep ≥1 positive type for inner
        val_types = set(rng.choice(np.asarray(train_types, dtype=object), size=k, replace=False))
        in_val |= (labels == 1) & t["attack_type"].isin(val_types).to_numpy()
        neg_pos = np.flatnonzero(labels == 0)
        n_neg = max(1, int(round(len(neg_pos) * val_frac)))
        if len(neg_pos):
            in_val[rng.choice(neg_pos, size=min(n_neg, len(neg_pos)), replace=False)] = True
    else:
        for lab in (0, 1):
            idx = np.flatnonzero(labels == lab)
            if not len(idx):
                continue
            n = max(1, int(round(len(idx) * val_frac)))
            in_val[rng.choice(idx, size=min(n, len(idx)), replace=False)] = True

    inner = t[~in_val].reset_index(drop=True)
    val = t[in_val].reset_index(drop=True)
    for name, split in (("inner-train", inner), ("val", val)):
        classes = set(split["label"].unique().tolist())
        if classes != {0, 1}:
            raise ValueError(
                f"{name} split is single-class ({classes}); cannot score — adjust val_frac/seed"
            )
    return inner, val


def make_fold(frame: pd.DataFrame, name: str, *, seed: int = 0, **carve_kwargs: object) -> Fold:
    """Build one LODO :class:`Fold`: split → assert disjoint → carve val.

    Parameters
    ----------
    frame : pandas.DataFrame
        The ``build_examples`` output frame.
    name : str
        One of :data:`FOLD_NAMES`.
    seed : int
        Validation-carve seed.
    **carve_kwargs
        Forwarded to :func:`carve_val_from_train`.

    Raises
    ------
    KeyError
        If ``name`` is not a known fold.
    ValueError
        Propagated from :func:`assert_source_disjoint` / :func:`carve_val_from_train`.
    """
    if name not in _BUILDERS:
        raise KeyError(f"unknown fold {name!r}; expected one of {FOLD_NAMES}")
    train_full, test = _BUILDERS[name](frame)
    train_full = purge_train_context_overlap(train_full, test)  # leakage hygiene (spec §6)
    carve: dict[str, object] = dict(carve_kwargs)
    if name in CARRIER_LODO_FOLDS:
        assert_carrier_disjoint(train_full, test)  # carrier-LODO: the carrier is the held-out axis
        # In-distribution val reference (carrier-lodo/criteria.md Rev 2): carrier-LODO must carve val
        # as a row-holdout with attack type HELD FIXED (not the attack-type mini-LODO), so val_roc is an
        # in-(train-carrier-)distribution reference — else G = val_roc − test_roc conflates the carrier
        # shift with the attack-type axis (which §6.5 showed collapses with capacity), biasing the verdict.
        carve.setdefault("min_types_for_typeholdout", 10**9)
    else:
        assert_source_disjoint(train_full, test)
    inner, val = carve_val_from_train(train_full, seed=seed, **carve)  # type: ignore[arg-type]
    return Fold(name=name, train=inner, val=val, test=test, test_types=_test_types(test))
