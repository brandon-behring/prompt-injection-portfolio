"""Arm-A direct→indirect cross-family assembly (criteria.md Revision 3 + 4, B2.4).

Builds the Arm-A study pools, rebuilt from our audited ``data/raw/`` (we do NOT consume the
prototype's processed folds — "trust no prototype result", criteria §i):

* **Train** = a capped-balanced direct-injection positive pool (deepset / Gandalf / Mosscap /
  HackAPrompt) + a 3-source negative pool (deepset native neg + neuralchemy hard-negatives +
  guychuk diversity top-up), benign-heavy ≈3:1 (criteria §ii / §iv).
* **Test** = the pooled cross-family OOD slate over the **4 two-class slices** (BIPIA, InjecAgent,
  JBB, XSTest), each carrying a slice-prefixed natural ``cluster_id`` (criteria §v).
* **Over-defense** = NotInject (single-class benign-with-trigger; non-gating FPR column, §v).

Quality discipline (criteria §i "our own dedup/leakage discipline"; finalized in Revision 4):

* **exact-dedup per direct corpus before capping** (EDA: hackaprompt 33% / mosscap 22% duplicate);
* a **light game-artifact filter** (denylist + length floor) on the direct positives — a *deviation*
  from §iii's cap-only bounding, recorded in Revision 4, with every dropped string LOGGED;
* the cap then draws from the deduped/filtered/(leakage-)clean rows (``load_direct_base`` consumes
  the :mod:`leakage_gate_arm_a` clean-manifest; pipeline order dedup → gate → cap).

Library-first (ADR-026): reuses ``assemble.load_bipia`` / ``assemble.load_injecagent`` for the two
indirect test slices and ``eval_toolkit.text_dedup`` for normalization. No silent fallback — every
load failure raises with context.

Run a standalone shape check (the Phase-A gate input)::

    uv run python experiments/cross-family-transfer/assemble_arm_a.py
"""

from __future__ import annotations

import sys
from collections.abc import Iterable
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import assemble as asm  # noqa: E402  # reuse load_bipia / load_injecagent for the test slices

# --------------------------------------------------------------------------------------
# Paths (audited 2026-06-04 against data/raw/MANIFEST.json)
# --------------------------------------------------------------------------------------
RAW = REPO_ROOT / "data" / "raw"
DEEPSET_GLOB = "deepset/**/*.parquet"
GANDALF_GLOB = "gandalf_ignore/**/*.parquet"
MOSSCAP_GLOB = "mosscap/**/*.parquet"
HACKAPROMPT_GLOB = "hackaprompt/*.parquet"
NEURALCHEMY_FULL_GLOB = "neuralchemy/full/*.parquet"  # `full`-only (the F1 dedup; core ⊂ full)
GUYCHUK_GLOB = "guychuk/**/*.parquet"
JBB_DIR = RAW / "jbb" / "data"
XSTEST_GLOB = "xstest/**/*.parquet"
NOTINJECT_SPLITS = (
    "NotInject_one",
    "NotInject_two",
    "NotInject_three",
)  # canonical 339 (decision 4)

# Fixed assembly knobs (criteria §ii/§iv; logged in Revision 4)
CAP = 3000  # per-corpus positive cap (criteria §ii — FIXED)
BENIGN_POS_RATIO = 3.0  # benign:positive (inside §iv's "≈3–4:1"); decision F2
DIRECT_DIALECT = "direct_base"

# Game-target artifacts that hackaprompt/mosscap relabel as positive but are NOT injections
# (decision 8; EDA: "I have been PWNED"×2098, "(key)"×1227, "key:"×1061). The filter drops ONLY
# unambiguous non-injections and must NOT nuke real attacks — neither terse real injections (gandalf
# "ignore rules", deepset "generate c++") nor LONG injections whose *payload* instructs the model to
# output the win-string (the whole hackaprompt game is "make it say I have been PWNED"). Three rules
# on the normalized text:
#   (1) no alphanumeric chars  — degenerate junk (control chars "\x02", pure whitespace/punct);
#   (2) bare target-fragment   — exact match in _ARTIFACT_DENYLIST (bare key/password words);
#   (3) SHORT win-string       — contains "pwned" AND ≤ _WINSTRING_MAX_TOKENS tokens (the bare
#                                "i have been pwned", NOT a long attack embedding it).
# Every dropped string is LOGGED (no silent truncation; the user reviews it before ratifying Rev 4).
_ARTIFACT_DENYLIST: frozenset[str] = frozenset(
    {"(key)", "key:", "key", "key.", "password", "password.", "the key", "the password", "sekey"}
)
_WINSTRING_MAX_TOKENS = (
    5  # "say i have been pwned" = 5 tokens; a real attack embedding it is longer
)


def _is_game_artifact(norm: str) -> bool:
    """True iff a normalized direct positive is an unambiguous non-injection game artifact."""
    if not any(c.isalnum() for c in norm):
        return True  # degenerate (control chars, pure whitespace/punctuation)
    if norm in _ARTIFACT_DENYLIST:
        return True  # bare key/password target fragment
    return "pwned" in norm and len(norm.split()) <= _WINSTRING_MAX_TOKENS  # short win-string only


# --------------------------------------------------------------------------------------
# Shared helpers
# --------------------------------------------------------------------------------------
def _read_glob(glob: str) -> pd.DataFrame:
    """Concatenate every parquet matching ``glob`` under ``data/raw/`` (raises if none)."""
    files = sorted(RAW.glob(glob))
    if not files:
        raise FileNotFoundError(f"no parquet under data/raw/ for glob {glob!r}")
    return pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)


def _norm(text: str) -> str:
    """Normalized text for exact-dedup / artifact matching (library-first ``text_dedup``)."""
    from eval_toolkit.text_dedup import normalize_text_for_dedup

    return normalize_text_for_dedup(str(text))


def _cap_by_level(texts: pd.Series, levels: pd.Series | None, *, cap: int, seed: int) -> pd.Series:
    """Deterministic level-stratified-proportional cap to exactly ``cap`` rows (seeded).

    With no ``levels`` (or already ≤ cap), a plain seeded sample / pass-through. Otherwise
    allocate ``cap`` across levels proportional to their size (largest-remainder to hit exactly
    ``cap``), then sample within each level. Mirrors criteria §ii.
    """
    rng = np.random.default_rng(seed)
    n = len(texts)
    if n <= cap:
        return texts.reset_index(drop=True)
    if levels is None:
        idx = rng.choice(n, size=cap, replace=False)
        return texts.iloc[np.sort(idx)].reset_index(drop=True)

    df = pd.DataFrame({"text": texts.to_numpy(), "level": levels.astype(str).to_numpy()})
    counts = df["level"].value_counts()
    frac = cap / n
    alloc = {lv: int(np.floor(c * frac)) for lv, c in counts.items()}
    # largest-remainder: hand out the leftover one at a time, deterministically by level name
    while sum(alloc.values()) < cap:
        for lv in sorted(alloc, key=str):
            if alloc[lv] < counts[lv]:
                alloc[lv] += 1
            if sum(alloc.values()) == cap:
                break
    parts: list[pd.Series] = []
    for lv in sorted(counts.index, key=str):
        sub = df.loc[df["level"] == lv, "text"]
        take = rng.choice(len(sub), size=min(alloc[lv], len(sub)), replace=False)
        parts.append(sub.iloc[np.sort(take)])
    return pd.concat(parts).reset_index(drop=True)


def _apply_manifest(frame: pd.DataFrame, manifest: frozenset[str] | None) -> pd.DataFrame:
    """Drop rows whose normalized text is in the leakage ``manifest`` (purge-from-train, §vi)."""
    if not manifest:
        return frame
    keep = ~frame["text"].map(_norm).isin(manifest)
    return frame[keep].reset_index(drop=True)


def _direct_frame(texts: Iterable[str], *, label: int) -> pd.DataFrame:
    """A direct-pool frame with unified columns (no cluster_id — resampling unit is the slice)."""
    t = pd.Series(list(texts), dtype=str)
    return pd.DataFrame(
        {
            "text": t,
            "label": label,
            "dialect": DIRECT_DIALECT,
            "cluster_id": "",
            "attack_type": "",  # required by carve_val_from_train's (disabled) type-holdout branch
        }
    )


# --------------------------------------------------------------------------------------
# Direct positive corpora (dedup → filter → [manifest] → cap)
# --------------------------------------------------------------------------------------
def _load_direct_corpus(corpus: str) -> pd.DataFrame:
    """Load one direct corpus's positives as a ``(text, level)`` frame (level None where absent)."""
    if corpus == "deepset":
        df = _read_glob(DEEPSET_GLOB)
        return pd.DataFrame({"text": df.loc[df["label"] == 1, "text"].astype(str), "level": None})
    if corpus == "gandalf":  # all-positive, no label column
        return pd.DataFrame({"text": _read_glob(GANDALF_GLOB)["text"].astype(str), "level": None})
    if corpus == "mosscap":  # all-positive; text=prompt, level="Level n"
        df = _read_glob(MOSSCAP_GLOB)
        return pd.DataFrame({"text": df["prompt"].astype(str), "level": df["level"].astype(str)})
    if corpus == "hackaprompt":  # all relabeled positive; text=user_input, level=int
        df = _read_glob(HACKAPROMPT_GLOB)
        df = df[df["user_input"].notna()]
        return pd.DataFrame(
            {"text": df["user_input"].astype(str), "level": df["level"].astype(str)}
        )
    raise KeyError(f"unknown direct corpus {corpus!r}")


def _clean_positive_texts(
    corpus: str, *, purged: frozenset[str] | None, drop_log: dict
) -> tuple[pd.Series, pd.Series | None]:
    """Dedup + artifact-filter (+ optional leakage purge) one direct corpus, text/level aligned.

    Operates on a ``(text, level)`` frame so the level stratification column stays aligned through
    every drop. Records per-corpus drop counts into ``drop_log`` (surfaced at the Phase-A gate).
    Returns ``(texts, levels)`` (``levels`` None for the unleveled deepset/gandalf corpora).
    """
    df = _load_direct_corpus(corpus).reset_index(drop=True)
    norm = df["text"].map(_norm)

    # (a) exact-dedup (decision 7): keep first per normalized key
    keep = ~norm.duplicated()
    n_dedup = int((~keep).sum())
    print(f"  [dedup] {corpus}: {len(df)} → {int(keep.sum())} (exact-dropped {n_dedup})")
    df, norm = df[keep].reset_index(drop=True), norm[keep].reset_index(drop=True)

    # (b) game-artifact filter (decision 8): pwned ∪ degenerate ∪ bare-fragment; log every drop
    drop = norm.map(_is_game_artifact)
    dropped = sorted(set(df.loc[drop, "text"].astype(str)))
    print(
        f"  [artifact-filter] {corpus}: dropped {int(drop.sum())} rows "
        f"({len(dropped)} distinct); samples={dropped[:8]}"
    )
    df, norm = df[~drop].reset_index(drop=True), norm[~drop].reset_index(drop=True)

    # (c) leakage purge (decision 9): drop rows whose normalized text was purged by the §vi gate
    if purged:
        keep = ~norm.isin(purged)
        n_purged = int((~keep).sum())
        if n_purged:
            print(f"  [leakage-purge] {corpus}: dropped {n_purged} leakage-matched rows")
        df = df[keep].reset_index(drop=True)
        drop_log.setdefault("leakage_purged", {})[corpus] = n_purged

    drop_log.setdefault("exact_dedup", {})[corpus] = n_dedup
    drop_log.setdefault("artifact_dropped", {})[corpus] = dropped
    levels = df["level"] if df["level"].notna().any() else None
    return df["text"].reset_index(drop=True), levels


def load_direct_base(
    *, cap: int | None = CAP, seed: int = 0, clean_manifest: frozenset[str] | None = None
) -> pd.DataFrame:
    """The Arm-A direct-injection positive pool (criteria §i/§ii; decisions 1/5/7/8/9).

    Pipeline per corpus: load → exact-dedup → artifact-filter → (leakage clean-manifest purge) →
    level-stratified cap. ``cap=CAP`` (default) → the capped-balanced primary pool (≈7,262 pos,
    each ≤41%); ``cap=None`` → the uncapped natural-mix robustness pool (≈881k, decision 5).

    Re-exported by ``folds_dialect.load_direct_base`` (called with the persisted manifest) to
    unblock the Arm-B **B+** variant.

    Parameters
    ----------
    cap : int or None
        Per-corpus positive cap; ``None`` disables capping (uncapped robustness pool).
    seed : int
        Cap-sampling seed.
    clean_manifest : frozenset[str] or None
        Normalized texts purged by :mod:`leakage_gate_arm_a` (dropped pre-cap); ``None`` = no purge
        (first build, before the gate runs).

    Returns
    -------
    pandas.DataFrame
        Columns ``text, label=1, dialect="direct_base", cluster_id="", attack_type=""``.
    """
    drop_log: dict = {}
    parts: list[pd.DataFrame] = []
    for corpus in ("deepset", "gandalf", "mosscap", "hackaprompt"):
        texts, levels = _clean_positive_texts(corpus, purged=clean_manifest, drop_log=drop_log)
        if cap is not None:
            texts = _cap_by_level(texts, levels, cap=cap, seed=seed)
        parts.append(_direct_frame(texts, label=1))
        print(f"  [direct] {corpus}: {len(parts[-1])} positives kept")
    frame = pd.concat(parts, ignore_index=True)
    # cross-corpus dedup (the §vi direct⊗direct dups): keep ONE copy of a prompt appearing in 2+
    # corpora (a train↔train dedup, NOT a train↔test leakage purge — so it is handled here, not via
    # the leakage manifest, which would drop both copies).
    keep = ~frame["text"].map(_norm).duplicated()
    n_xcorpus = int((~keep).sum())
    if n_xcorpus:
        print(f"  [cross-corpus-dedup] dropped {n_xcorpus} duplicate positives (kept first)")
    frame = frame[keep].reset_index(drop=True)
    drop_log["cross_corpus_dedup"] = n_xcorpus
    frame.attrs["drop_log"] = drop_log
    return frame


# --------------------------------------------------------------------------------------
# Negative sources (3-source, benign-heavy; criteria §iv)
# --------------------------------------------------------------------------------------
def _verify_negative_provenance(df: pd.DataFrame, *, corpus: str, label_col: str = "label") -> None:
    """Build-time fail-loud check that ``label=0 ⟺ benign`` is structurally sound (criteria §iv)."""
    if label_col not in df.columns:
        raise ValueError(f"{corpus}: missing label column {label_col!r}")
    vals = set(pd.unique(df[label_col]))
    if not vals <= {0, 1}:
        raise ValueError(f"{corpus}: label not ⊆ {{0,1}} (got {sorted(vals)})")
    if vals != {0, 1}:
        raise ValueError(
            f"{corpus}: not two-class (got {sorted(vals)}) — wrong corpus/relabel risk"
        )
    if int((df[label_col] == 0).sum()) == 0:
        raise ValueError(f"{corpus}: no label=0 rows to draw negatives from")


def load_neuralchemy_negs() -> pd.DataFrame:
    """neuralchemy `full`-only distinct ``label=0`` negatives (F1 dedup; ~3.5k realized, §iv)."""
    df = _read_glob(NEURALCHEMY_FULL_GLOB)
    _verify_negative_provenance(df, corpus="neuralchemy/full")
    neg = df.loc[df["label"] == 0, "text"].astype(str)
    neg = neg[~neg.map(_norm).duplicated()].reset_index(drop=True)  # within-source exact-dedup
    return _direct_frame(neg, label=0)


def load_guychuk_negs(
    *, n: int, seed: int = 0, clean_manifest: frozenset[str] | None = None
) -> pd.DataFrame:
    """guychuk benign top-up: a seeded sample of ``n`` distinct leakage-clean ``label=0`` (§iv)."""
    frame = _apply_manifest(_all_guychuk_negs(), clean_manifest)
    if n > len(frame):
        raise ValueError(f"guychuk: requested {n} negs but only {len(frame)} clean available")
    take = np.random.default_rng(seed).choice(len(frame), size=n, replace=False)
    return frame.iloc[np.sort(take)].reset_index(drop=True)


def assemble_arm_a_train(
    *,
    cap: int | None = CAP,
    ratio: float = BENIGN_POS_RATIO,
    seed: int = 0,
    clean_manifest: frozenset[str] | None = None,
) -> pd.DataFrame:
    """Arm-A train pool: capped direct positives + 3-source benign-heavy negatives (§ii/§iv).

    Negatives are filled in fixed priority — deepset native (399, style-matched) → neuralchemy
    hard-negatives (≈6,005) → guychuk diversity top-up — to ``ratio`` × positives. For ``cap=None``
    (uncapped robustness), ``ratio`` is logged-not-enforced (only ~235k negatives exist against
    ≈881k positives; the pool is deliberately positive-heavy, decision 5).

    Returns
    -------
    pandas.DataFrame
        Columns ``text, label, dialect, cluster_id="", attack_type=""`` (shuffled, seeded).
    """
    pos = load_direct_base(cap=cap, seed=seed, clean_manifest=clean_manifest)
    drop_log = pos.attrs.get("drop_log", {})
    n_pos = len(pos)

    # negatives, leakage-purged by the same manifest (the §vi negative⊗test scan; decision 9)
    deepset_neg = _apply_manifest(
        _direct_frame(_read_glob(DEEPSET_GLOB).query("label == 0")["text"].astype(str), label=0),
        clean_manifest,
    )
    neuralchemy_neg = _apply_manifest(load_neuralchemy_negs(), clean_manifest)
    n_target = int(round(ratio * n_pos))
    have = len(deepset_neg) + len(neuralchemy_neg)

    if cap is None:
        guychuk_neg = _apply_manifest(_all_guychuk_negs(), clean_manifest)  # uncapped (decision 5)
    else:
        guychuk_neg = load_guychuk_negs(
            n=max(0, n_target - have), seed=seed, clean_manifest=clean_manifest
        )

    neg = pd.concat([deepset_neg, neuralchemy_neg, guychuk_neg], ignore_index=True)
    frame = pd.concat([pos, neg], ignore_index=True)
    frame = frame.sample(frac=1.0, random_state=seed).reset_index(drop=True)

    # Trim the drop_log for serialization: COUNTS + a 10-sample per corpus, NOT the full dropped
    # lists (28,994 hackaprompt strings → a 15 MB summary.json otherwise; the full lists are in the
    # _summary stdout log for review).
    art = drop_log.get("artifact_dropped", {})
    drop_log_summary = {
        "exact_dedup": drop_log.get("exact_dedup", {}),
        "cross_corpus_dedup": drop_log.get("cross_corpus_dedup", 0),
        "leakage_purged": drop_log.get("leakage_purged", {}),
        "artifact_dropped_counts": {c: len(v) for c, v in art.items()},
        "artifact_dropped_sample": {c: list(v[:10]) for c, v in art.items()},
    }
    frame.attrs["realized"] = {
        "n_pos": n_pos,
        "n_neg": int(len(neg)),
        "neg_composition": {
            "deepset": int(len(deepset_neg)),
            "neuralchemy_full": int(len(neuralchemy_neg)),
            "guychuk": int(len(guychuk_neg)),
        },
        "ratio_target": ratio,
        "ratio_realized": round(len(neg) / max(1, n_pos), 3),
        "cap": cap,
        "drop_log": drop_log_summary,
    }
    return frame


def _all_guychuk_negs() -> pd.DataFrame:
    """Every distinct guychuk ``label=0`` (for the uncapped robustness pool, decision 5)."""
    df = _read_glob(GUYCHUK_GLOB)
    _verify_negative_provenance(df, corpus="guychuk")
    neg = df.loc[df["label"] == 0, "prompt"].astype(str)
    neg = neg[~neg.map(_norm).duplicated()].reset_index(drop=True)
    return _direct_frame(neg, label=0)


# --------------------------------------------------------------------------------------
# Test slices (pooled cross-family OOD slate; criteria §v)
# --------------------------------------------------------------------------------------
def load_jbb() -> pd.DataFrame:
    """JBB slice: harmful-behaviors (pos) vs benign-behaviors (neg); cluster_id = Category (10)."""
    rows = []
    for which, label in (("harmful", 1), ("benign", 0)):
        path = JBB_DIR / f"{which}-behaviors.csv"
        if not path.exists():
            raise FileNotFoundError(f"JBB csv missing: {path}")
        df = pd.read_csv(path)
        for goal, cat in zip(df["Goal"].astype(str), df["Category"].astype(str), strict=True):
            rows.append({"text": goal, "label": label, "slice": "JBB", "cluster_id": f"JBB::{cat}"})
    return pd.DataFrame(rows)


def load_xstest() -> pd.DataFrame:
    """XSTest slice: unsafe (pos, 200) vs safe (neg, 250); cluster_id = type (18)."""
    df = _read_glob(XSTEST_GLOB)
    label_map = {"unsafe": 1, "safe": 0}
    bad = set(df["label"].astype(str)) - set(label_map)
    if bad:
        raise ValueError(f"XSTest: unexpected label values {bad}")
    return pd.DataFrame(
        {
            "text": df["prompt"].astype(str),
            "label": df["label"].astype(str).map(label_map).astype(int),
            "slice": "XSTest",
            "cluster_id": "XSTest::" + df["type"].astype(str),
        }
    )


def load_notinject_overdefense() -> pd.DataFrame:
    """NotInject over-defense set: canonical one+two+three (339), all benign (decision 4, §v)."""
    parts = []
    for split in NOTINJECT_SPLITS:
        files = sorted(RAW.glob(f"notinject/**/{split}-*.parquet"))
        if not files:
            raise FileNotFoundError(f"NotInject split missing: {split}")
        parts.append(pd.read_parquet(files[0]))
    df = pd.concat(parts, ignore_index=True)
    return pd.DataFrame(
        {
            "text": df["prompt"].astype(str),
            "label": 0,
            "slice": "NotInject",
            "cluster_id": "NotInject",
        }
    )


def assemble_arm_a_test(*, contexts_per_attack: int = 12, seed: int = 0) -> pd.DataFrame:
    """The pooled cross-family OOD test slate over the 4 two-class slices (criteria §v).

    Reuses ``assemble.load_bipia`` / ``assemble.load_injecagent`` (library-first) for the two
    indirect slices and the new ``load_jbb`` / ``load_xstest`` for the cross-family slices. Every
    slice's ``cluster_id`` is slice-prefixed for global bootstrap uniqueness (criteria §Statistics
    line 170 — "resample slices' within-slice cluster").

    Returns
    -------
    pandas.DataFrame
        Columns ``text, label, slice, cluster_id`` (NotInject NOT pooled here — over-defense only).
    """
    bipia = asm.load_bipia(contexts_per_attack=contexts_per_attack, seed=seed)
    bipia = pd.DataFrame(
        {
            "text": bipia["text"].astype(str),
            "label": bipia["label"].astype(int),
            "slice": "BIPIA",
            "cluster_id": "BIPIA::" + bipia["cluster_id"].astype(str),
        }
    )
    inj = asm.load_injecagent()
    inj = pd.DataFrame(
        {
            "text": inj["text"].astype(str),
            "label": inj["label"].astype(int),
            "slice": "InjecAgent",
            "cluster_id": "InjecAgent::" + inj["cluster_id"].astype(str),
        }
    )
    frame = pd.concat([bipia, inj, load_jbb(), load_xstest()], ignore_index=True)
    frame["label"] = frame["label"].astype(int)
    frame["cluster_id"] = frame["cluster_id"].astype(str)
    return frame


# --------------------------------------------------------------------------------------
# Standalone shape check (the Phase-A gate input)
# --------------------------------------------------------------------------------------
def _summary() -> None:
    """Print realized train composition + per-slice test counts + drop logs; assert tripwires."""
    print("=== Arm-A TRAIN (capped primary) ===")
    train = assemble_arm_a_train(cap=CAP, seed=0)
    real = train.attrs["realized"]
    n_pos, n_neg = real["n_pos"], real["n_neg"]
    print(f"pos={n_pos}  neg={n_neg}  ratio={real['ratio_realized']}:1  total={len(train)}")
    print(f"neg composition: {real['neg_composition']}")
    print(f"dedup drops: {real['drop_log'].get('exact_dedup')}")
    print(f"artifact-filter distinct drops: {real['drop_log'].get('artifact_dropped_counts')}")
    for corpus, samples in real["drop_log"].get("artifact_dropped_sample", {}).items():
        if samples:
            print(f"  {corpus} artifact samples (review!): {samples}")

    print("\n=== Arm-A TEST (pooled cross-family slate) ===")
    test = assemble_arm_a_test()
    for sl, sub in test.groupby("slice"):
        print(
            f"  {sl}: {len(sub)} rows ({int((sub.label == 1).sum())} pos / "
            f"{int((sub.label == 0).sum())} neg), {sub.cluster_id.nunique()} clusters"
        )
    od = load_notinject_overdefense()
    print(f"  over-defense NotInject: {len(od)} benign rows")

    # tripwires (dedup/filter shift the count off the pre-dedup 7,263 estimate; assert sane bounds +
    # per-corpus caps, and LOG the exact realized count for Revision 4)
    assert 7200 <= n_pos <= 7263, f"capped positives {n_pos} outside the sane [7200,7263] band"
    assert set(test["label"].unique()) == {0, 1}, "pooled test must be two-class"
    assert len(od) == 339, f"expected NotInject 339, got {len(od)}"
    print(
        f"\n✓ tripwires passed (positives={n_pos} ∈ [7200,7263]; pooled test two-class; "
        f"NotInject==339) — exact realized positives = {n_pos} (→ Revision 4)"
    )


if __name__ == "__main__":
    _summary()
