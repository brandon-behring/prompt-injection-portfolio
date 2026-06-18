"""Unit tests for the carrier-LODO fold construction (carrier-lodo/criteria.md Revision 1).

Target: ``experiments/attack-type-lodo/folds.py`` carrier-LODO additions. Covers: the 3
leave-one-carrier-out folds build two-class train/val/test, the held-out carrier is the ONLY
shifted axis (attack types are *shared* across the split — the opposite of attack-type LODO),
``assert_carrier_disjoint`` fires on a planted carrier overlap, and the folds are registered.

The experiment dir is hyphenated (not an importable package), so the module loads via ``sys.path``
injection — the same pattern ``harness.py`` uses.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

_LODO_DIR = Path(__file__).resolve().parent.parent.parent / "experiments" / "attack-type-lodo"
if str(_LODO_DIR) not in sys.path:
    sys.path.insert(0, str(_LODO_DIR))

import folds  # noqa: E402


def _carrier_frame() -> pd.DataFrame:
    """A 3-carrier frame where attack types are shared across carriers (carrier is the only shift).

    Each ``(carrier, role)`` gets unique contexts; the same two attack types (``TaskA`` from the
    train role, ``TaskB`` from the test role) appear under every carrier, so a leave-one-carrier-out
    split has shared attack types and disjoint carriers/contexts.
    """
    rows: list[dict[str, object]] = []
    role_type = {"train": "TaskA", "test": "TaskB"}
    for carrier in ("email", "code", "table"):
        for role, atype in role_type.items():
            for i in range(8):  # clean negatives, unique per carrier+role
                rows.append(
                    {
                        "text": f"{carrier}-{role}-neg{i}",
                        "label": 0,
                        "attack_type": "",
                        "subfamily": "benign",
                        "carrier": carrier,
                        "position": "none",
                        "role": role,
                        "source": "clean",
                    }
                )
            for i in range(8):  # positives over unique contexts
                rows.append(
                    {
                        "text": f"{carrier}-{role}-pos{i}\n\natk-{atype}",
                        "label": 1,
                        "attack_type": atype,
                        "subfamily": "task-intent",
                        "carrier": carrier,
                        "position": "suffix",
                        "role": role,
                        "source": "inject",
                    }
                )
    return pd.DataFrame(rows)


@pytest.mark.unit
def test_carrier_lodo_folds_registered() -> None:
    """The 3 carrier-LODO folds are declared and present in FOLD_NAMES."""
    assert folds.CARRIER_LODO_FOLDS == (
        "carrier_lodo_email",
        "carrier_lodo_code",
        "carrier_lodo_table",
    )
    assert set(folds.CARRIER_LODO_FOLDS) <= set(folds.FOLD_NAMES)


@pytest.mark.unit
def test_carrier_lodo_holds_out_one_carrier() -> None:
    """carrier_lodo_email trains on {code,table}, tests on {email}; both splits are two-class."""
    fold = folds.make_fold(_carrier_frame(), "carrier_lodo_email", seed=0)
    assert set(fold.train["carrier"].unique()) == {"code", "table"}
    assert set(fold.test["carrier"].unique()) == {"email"}
    for split in (fold.train, fold.val, fold.test):
        assert set(split["label"].unique()) == {0, 1}


@pytest.mark.unit
def test_carrier_lodo_shares_attack_types() -> None:
    """The carrier is the ONLY shifted axis — train and test share attack types (not disjoint)."""
    fold = folds.make_fold(_carrier_frame(), "carrier_lodo_table", seed=0)
    train_types = {t for t in fold.train["attack_type"].unique() if t}
    test_types = {t for t in fold.test["attack_type"].unique() if t}
    assert train_types & test_types  # SHARED (the opposite of attack-type LODO)
    assert train_types == test_types == {"TaskA", "TaskB"}


@pytest.mark.unit
def test_all_carrier_lodo_folds_build_and_assert_carrier_disjoint() -> None:
    """Each carrier-LODO fold builds two-class splits and passes the carrier-disjoint assertion."""
    frame = _carrier_frame()
    for name in folds.CARRIER_LODO_FOLDS:
        fold = folds.make_fold(frame, name, seed=0)
        assert fold.name == name
        folds.assert_carrier_disjoint(fold.train, fold.test)
        folds.assert_carrier_disjoint(fold.val, fold.test)


@pytest.mark.unit
def test_assert_carrier_disjoint_fires_on_carrier_overlap() -> None:
    """A carrier shared across the split boundary raises ValueError (the LODO unit leaked)."""
    train = pd.DataFrame(
        {"text": ["c1\n\nx"], "label": [1], "attack_type": ["a"], "carrier": ["email"]}
    )
    test = pd.DataFrame(
        {"text": ["c2\n\ny"], "label": [1], "attack_type": ["a"], "carrier": ["email"]}
    )
    with pytest.raises(ValueError, match="carrier overlap"):
        folds.assert_carrier_disjoint(train, test)


@pytest.mark.unit
def test_carrier_lodo_allows_shared_attack_types_through_make_fold() -> None:
    """make_fold does not raise on shared attack types for a carrier-LODO fold (carrier check)."""
    # Would raise under assert_source_disjoint (shared types); must pass under the carrier path.
    fold = folds.make_fold(_carrier_frame(), "carrier_lodo_code", seed=0)
    assert set(fold.test["carrier"].unique()) == {"code"}


def _many_type_carrier_frame() -> pd.DataFrame:
    """A 3-carrier frame with 8 shared attack types (the default carve would hold out types)."""
    rows: list[dict[str, object]] = []
    types = [f"Type{i}" for i in range(8)]
    for carrier in ("email", "code", "table"):
        for i in range(12):
            rows.append(
                {
                    "text": f"{carrier}-neg{i}",
                    "label": 0,
                    "attack_type": "",
                    "subfamily": "benign",
                    "carrier": carrier,
                    "position": "none",
                    "role": "train",
                    "source": "clean",
                }
            )
        for atype in types:
            for i in range(4):
                rows.append(
                    {
                        "text": f"{carrier}-{atype}-pos{i}\n\natk-{atype}",
                        "label": 1,
                        "attack_type": atype,
                        "subfamily": "task-intent",
                        "carrier": carrier,
                        "position": "suffix",
                        "role": "train",
                        "source": "inject",
                    }
                )
    return pd.DataFrame(rows)


@pytest.mark.unit
def test_carrier_lodo_val_is_in_distribution_on_attack_type() -> None:
    """Rev 2: carrier-LODO val holds attack type FIXED (row-holdout) → no val-exclusive type.

    With ≥6 attack types the default carve holds out val-exclusive types; the Rev-2 fix forces a
    row-holdout so ``val_roc`` is an in-(train-carrier-)distribution reference.
    """
    fold = folds.make_fold(_many_type_carrier_frame(), "carrier_lodo_email", seed=0)
    train_types = {t for t in fold.train["attack_type"].unique() if t}
    val_types = {t for t in fold.val["attack_type"].unique() if t}
    assert val_types <= train_types  # no val-exclusive held-out type → in-distribution
    assert len(train_types) == 8  # no attack type fully diverted out of inner-train
