"""Unit tests for the attack-type-LODO fold construction.

Target: ``experiments/attack-type-lodo/folds.py``. Covers the spec-§2/§3/§6
contract: the three LODO folds build with disjoint train/test attack-types, the
source-disjointness assertion fires on a planted overlap, the
train-context-overlap purge removes leaked contexts, and the validation carve
yields two-class splits.

The experiment dir name is hyphenated (not an importable package), so the module
is loaded via ``sys.path`` injection — the same pattern ``harness.py`` uses.
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


def _toy_frame() -> pd.DataFrame:
    """A minimal carrier frame with disjoint train/test attack-types + one shared context.

    ``ctxShared`` appears as a clean negative on both sides (a planted leak the purge
    must remove); ``a1/a2`` are train attack-types, ``b1/b2`` test attack-types.
    """
    rows: list[dict[str, object]] = []
    # Train negatives (clean contexts), incl. the shared one.
    for c in ("ctxTrainA", "ctxTrainB", "ctxShared"):
        rows.append(
            {
                "text": c,
                "label": 0,
                "attack_type": "",
                "subfamily": "benign",
                "carrier": "email",
                "position": "none",
                "role": "train",
                "source": "clean",
            }
        )
    # Test negatives, incl. the shared one.
    for c in ("ctxTestA", "ctxTestB", "ctxShared"):
        rows.append(
            {
                "text": c,
                "label": 1 - 1,
                "attack_type": "",
                "subfamily": "benign",
                "carrier": "email",
                "position": "none",
                "role": "test",
                "source": "clean",
            }
        )
    # Train positives: attack-types a1/a2 over train contexts.
    for atype in ("a1", "a2"):
        for c in ("ctxTrainA", "ctxTrainB"):
            for k in range(4):
                rows.append(
                    {
                        "text": f"{c}\n\natk-{atype}-{k}",
                        "label": 1,
                        "attack_type": atype,
                        "subfamily": "task-intent",
                        "carrier": "email",
                        "position": "suffix",
                        "role": "train",
                        "source": "inject",
                    }
                )
    # Test positives: attack-types b1/b2 over test contexts.
    for atype in ("b1", "b2"):
        for c in ("ctxTestA", "ctxTestB"):
            for k in range(4):
                rows.append(
                    {
                        "text": f"{c}\n\natk-{atype}-{k}",
                        "label": 1,
                        "attack_type": atype,
                        "subfamily": "task-intent",
                        "carrier": "email",
                        "position": "suffix",
                        "role": "test",
                        "source": "inject",
                    }
                )
    return pd.DataFrame(rows)


@pytest.mark.unit
def test_core_fold_builds_with_disjoint_types() -> None:
    """The core fold builds; train/test attack-types are disjoint; test_types is populated."""
    fold = folds.make_fold(_toy_frame(), "core_attack_type", seed=0, min_types_for_typeholdout=99)
    train_types = {t for t in fold.train["attack_type"].unique() if t}
    test_types = {t for t in fold.test["attack_type"].unique() if t}
    assert train_types == {"a1", "a2"}
    assert test_types == {"b1", "b2"}
    assert not (train_types & test_types)
    assert set(fold.test_types) == {"b1", "b2"}


@pytest.mark.unit
def test_purge_removes_shared_context_from_train_only() -> None:
    """The shared clean context is dropped from train; the test side keeps it intact."""
    frame = _toy_frame()
    train = frame[frame["role"] == "train"].reset_index(drop=True)
    test = frame[frame["role"] == "test"].reset_index(drop=True)
    purged = folds.purge_train_context_overlap(train, test)
    assert "ctxShared" in set(test["text"])  # test untouched
    assert "ctxShared" not in set(purged.loc[purged["label"] == 0, "text"])  # purged from train
    # No surviving train row (pos or neg) sits on a test context.
    test_ctx = folds._underlying_contexts(test)
    surviving = folds._underlying_contexts(purged)
    assert not (surviving & test_ctx)


@pytest.mark.unit
def test_assert_source_disjoint_fires_on_attack_type_overlap() -> None:
    """A shared attack-type across the split boundary raises ValueError."""
    train = pd.DataFrame({"text": ["c1\n\nx"], "label": [1], "attack_type": ["shared"]})
    test = pd.DataFrame({"text": ["c2\n\ny"], "label": [1], "attack_type": ["shared"]})
    with pytest.raises(ValueError, match="attack-type overlap"):
        folds.assert_source_disjoint(train, test)


@pytest.mark.unit
def test_assert_source_disjoint_fires_on_context_overlap() -> None:
    """A shared underlying context (cross-class) raises ValueError."""
    # Train negative is the bare context; test positive injects an attack onto the same context.
    train = pd.DataFrame({"text": ["sharedCtx"], "label": [0], "attack_type": [""]})
    test = pd.DataFrame({"text": ["sharedCtx\n\nattack"], "label": [1], "attack_type": ["b1"]})
    with pytest.raises(ValueError, match="context overlap"):
        folds.assert_source_disjoint(train, test)


@pytest.mark.unit
def test_carve_val_yields_two_class_splits() -> None:
    """The val carve produces inner-train + val splits that each contain both classes."""
    frame = _toy_frame()
    train = frame[frame["role"] == "train"].reset_index(drop=True)
    inner, val = folds.carve_val_from_train(train, seed=0, min_types_for_typeholdout=99)
    assert set(inner["label"].unique()) == {0, 1}
    assert set(val["label"].unique()) == {0, 1}
    assert len(inner) + len(val) == len(train)


@pytest.mark.unit
def test_make_fold_rejects_unknown_name() -> None:
    """An unknown fold name raises KeyError naming the valid set."""
    with pytest.raises(KeyError, match="unknown fold"):
        folds.make_fold(_toy_frame(), "not_a_fold", seed=0)


def _rich_frame() -> pd.DataFrame:
    """A multi-carrier, obfuscation-aware frame where all three folds are non-degenerate.

    Each ``(role, carrier)`` gets its own unique contexts (so train/test never overlap),
    a task-intent positive type and an obfuscation positive type drawn from the real
    taxonomy, plus clean negatives — enough that every fold builder yields a two-class
    train+test and the val carve succeeds.
    """
    obf_train = sorted(folds.OBFUSCATION_TRAIN)[0]  # e.g. "Alphanumeric Substitution"
    obf_test = sorted(folds.OBFUSCATION_TEST)[0]  # e.g. "Base Encoding"
    rows: list[dict[str, object]] = []
    plan = {
        "train": (("TaskTrain", "task-intent"), (obf_train, "obfuscation")),
        "test": (("TaskTest", "task-intent"), (obf_test, "obfuscation")),
    }
    for role, types in plan.items():
        for carrier in ("code", "table", "email"):
            for i in range(6):  # clean negatives (unique per role+carrier)
                rows.append(
                    {
                        "text": f"{role}-{carrier}-neg{i}",
                        "label": 0,
                        "attack_type": "",
                        "subfamily": "benign",
                        "carrier": carrier,
                        "position": "none",
                        "role": role,
                        "source": "clean",
                    }
                )
            for atype, fam in types:
                for i in range(6):  # positives: inject onto unique contexts
                    rows.append(
                        {
                            "text": f"{role}-{carrier}-pos{i}\n\natk-{atype}",
                            "label": 1,
                            "attack_type": atype,
                            "subfamily": fam,
                            "carrier": carrier,
                            "position": "suffix",
                            "role": role,
                            "source": "inject",
                        }
                    )
    return pd.DataFrame(rows)


@pytest.mark.unit
def test_all_three_folds_build() -> None:
    """Each declared fold constructs a two-class train/val/test on a realistic frame."""
    frame = _rich_frame()
    for name in folds.FOLD_NAMES:
        fold = folds.make_fold(frame, name, seed=0)
        assert fold.name == name
        for split_name, split in (("train", fold.train), ("val", fold.val), ("test", fold.test)):
            assert set(split["label"].unique()) == {0, 1}, f"{name}/{split_name} not two-class"
        # The disjointness guarantee holds for every fold (no train↔test context/type leak).
        folds.assert_source_disjoint(fold.train, fold.test)
        folds.assert_source_disjoint(fold.val, fold.test)
