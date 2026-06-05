"""Arm-A leakage gate (criteria.md B2.4 §vi): exact + near-dup, PURGE-FROM-TRAIN.

Four scans, train rows purged where they match a TEST / held-out text (the test is sacrosanct):

  direct⊗direct   — cross-corpus exact dups within the direct positive pool;
  direct⊗test     — direct positives vs the 4 pooled test slices (BIPIA/InjecAgent/JBB/XSTest);
  direct⊗indirect — direct positives vs the indirect dialects (the Arm-B **B+** held-out superset);
  negative⊗test   — neuralchemy / guychuk negatives vs the benign test slices (NotInject / XSTest).

Emits ``B2_leakage/leakage_gate_armA.json``: per-scan before/after + sampled colliding pairs + the
``purged_normalized_texts`` MANIFEST that ``assemble_arm_a`` / ``folds_dialect.load_direct_base``
consume pre-cap (decision 9; pipeline order dedup → gate → cap).

Library-first (ADR-026): the same ``eval_toolkit.text_dedup`` primitives as the Arm-B
``leakage_gate.py`` (``normalize_text_for_dedup`` + ``sha256_text`` exact; ``MinHashLSHStrategy`` +
``cross_dedup_pairs`` near≥0.8). The **exact** scan (normalized-hash membership, O(n)) runs on the
FULL deduped pools — comprehensive + fast. The **near-dup** MinHash scan runs on the CAPPED
assembled train (≈29k) — the plan's documented compute fallback (exact-on-full + near-on-capped),
since near-dup on the full 562k pool is impractical. Both exact + near matches join the manifest
(purge-from-train). Note: ``cross_dedup_pairs(train, eval)`` returns ``(eval_idx, train_idx, sim)``;
the Arm-B ``leakage_gate.py`` reads the first element as the train index (a latent bug, harmless
there since it found zero pairs) — this module uses the correct second-element train index.

Run (Phase A precondition; CPU)::

    uv run python experiments/cross-family-transfer/leakage_gate_arm_a.py [--near-threshold 0.8]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import assemble as asm  # noqa: E402  # the 4 Arm-B indirect dialects (direct⊗indirect scan)
import assemble_arm_a as aa  # noqa: E402

OUT_DIR = _HERE / "B2_leakage"


def _exact_purge(train_texts: list[str], ref_texts: list[str], normalize, sha256) -> set[int]:
    """Indices of ``train_texts`` whose normalized hash matches any ``ref_texts`` hash."""
    ref_hashes = {sha256(normalize(t)) for t in ref_texts}
    return {i for i, t in enumerate(train_texts) if sha256(normalize(t)) in ref_hashes}


def _scan_exact(name: str, train: pd.Series, ref_texts: list[str], *, normalize, sha256) -> dict:
    """One exact purge-from-train scan; returns a report dict + the purged normalized texts."""
    train_texts = train.astype(str).tolist()
    purged_idx = _exact_purge(train_texts, ref_texts, normalize, sha256)
    purged_norm = sorted({normalize(train_texts[i]) for i in purged_idx})
    print(
        f"  [exact] {name}: train={len(train_texts)} ref={len(ref_texts)} purged={len(purged_idx)}"
    )
    return {
        "scan": name,
        "train_size": len(train_texts),
        "ref_size": len(ref_texts),
        "exact_purged": len(purged_idx),
        "sample_purged": [train_texts[i][:140] for i in list(purged_idx)[:8]],
        "_purged_norm": purged_norm,
    }


def _near_dup_scan(train: pd.Series, ref_texts: list[str], *, threshold: float, normalize) -> dict:
    """Near-dup MinHash purge-from-train scan on the capped train vs a reference (criteria §vi).

    ``cross_dedup_pairs(train, eval)`` returns ``(eval_idx, train_idx, sim)`` (per source),
    so the TRAIN-side index is the **second** element. Returns the count, correct sample pairs, and
    the set of near-matched **train** normalized texts (merged into the purge manifest).
    """
    from eval_toolkit.text_dedup import MinHashLSHStrategy, cross_dedup_pairs

    train_texts = train.astype(str).tolist()
    strat = MinHashLSHStrategy(n=3, num_perm=128, bands=16, seed=42)
    pairs = cross_dedup_pairs(train_texts, ref_texts, threshold=threshold, strategy=strat)
    matched_train = {tr for _ev, tr, _s in pairs if 0 <= tr < len(train_texts)}
    samples = [
        {
            "sim": round(float(sim), 3),
            "train": train_texts[tr][:110],
            "ref": ref_texts[ev][:110],
        }
        for ev, tr, sim in pairs[:8]
        if 0 <= tr < len(train_texts) and 0 <= ev < len(ref_texts)
    ]
    purged_norm = sorted({normalize(train_texts[i]) for i in matched_train})
    print(f"  [near≥{threshold}] train={len(train_texts)} matched={len(matched_train)}")
    return {
        "near_threshold": threshold,
        "near_matched_train": len(matched_train),
        "sample_pairs": samples,
        "_purged_norm": purged_norm,
    }


def run_gate(*, near_threshold: float, seed: int = 0) -> dict:
    """Run all four §vi scans; return the full report (incl. the purge manifest)."""
    from eval_toolkit.text_dedup import normalize_text_for_dedup as normalize
    from eval_toolkit.text_dedup import sha256_text as sha256

    print("[build] direct positives (full deduped, no cap) ...", flush=True)
    direct_pos = aa.load_direct_base(cap=None)  # full deduped+filtered direct positives
    print("[build] negatives (neuralchemy + all guychuk) ...", flush=True)
    neuralchemy = aa.load_neuralchemy_negs()
    guychuk = aa._all_guychuk_negs()  # noqa: SLF001 — the full benign pool the cap draws from
    negatives = pd.concat([neuralchemy, guychuk], ignore_index=True)
    print("[build] pooled test slate + indirect dialects ...", flush=True)
    test = aa.assemble_arm_a_test(seed=seed)
    notinject = aa.load_notinject_overdefense()
    indirect = asm.assemble()  # the 4 Arm-B indirect dialects (direct⊗indirect superset)

    test_texts = test["text"].astype(str).tolist()
    # benign test = every benign test row (incl. XSTest-safe) ∪ NotInject (§vi negative⊗test)
    benign_test = pd.concat(
        [test.loc[test["label"] == 0, "text"], notinject["text"]], ignore_index=True
    ).astype(str)
    benign_test_texts = sorted(set(benign_test.tolist()))
    indirect_texts = indirect["text"].astype(str).tolist()

    scans: list[dict] = []
    # (1) direct⊗direct — cross-corpus exact dups within the direct positive pool
    dp = direct_pos["text"].astype(str)
    dp_keys = dp.map(normalize)
    dup_mask = dp_keys.duplicated()
    scans.append(
        {
            "scan": "direct⊗direct",
            "train_size": len(dp),
            "exact_purged": int(dup_mask.sum()),
            # NOT in the manifest: cross-corpus dups are a train↔train dedup (keep-first), handled
            # in assemble_arm_a.load_direct_base — putting them in the manifest drops BOTH copies.
            "note": "cross-corpus dedup handled in load_direct_base (keep-first), not the manifest",
            "sample_purged": dp[dup_mask].head(8).str.slice(0, 140).tolist(),
        }
    )
    print(f"  [exact] direct⊗direct: train={len(dp)} cross-corpus-dups={int(dup_mask.sum())}")
    # (2) direct⊗test, (3) direct⊗indirect
    scans.append(_scan_exact("direct⊗test", dp, test_texts, normalize=normalize, sha256=sha256))
    scans.append(
        _scan_exact("direct⊗indirect", dp, indirect_texts, normalize=normalize, sha256=sha256)
    )
    # (4) negative⊗test (vs the benign test slices)
    scans.append(
        _scan_exact(
            "negative⊗test",
            negatives["text"],
            benign_test_texts,
            normalize=normalize,
            sha256=sha256,
        )
    )

    # near-dup purge-from-train scan on the CAPPED assembled train vs the full test slate (criteria
    # §vi exact+near; the plan's documented compute fallback — exact-on-full + near-on-capped). The
    # near-matched train texts join the manifest (purge-from-train); near-dup on the full 562k pool
    # is impractical, so the capped pool (what actually trains) is scanned.
    print("[build] capped assembled train (near-dup purge scan) ...", flush=True)
    capped_train = aa.assemble_arm_a_train(seed=seed)
    near = _near_dup_scan(
        capped_train["text"], test_texts, threshold=near_threshold, normalize=normalize
    )

    near_norm = near.pop("_purged_norm")
    # manifest = real train↔test leakage only (direct⊗direct has no _purged_norm — it is a
    # train↔train cross-corpus dedup handled in load_direct_base, not a leakage purge).
    manifest = sorted({t for s in scans for t in s.pop("_purged_norm", [])} | set(near_norm))
    return {
        "criteria": "experiments/cross-family-transfer/criteria.md §vi (B2.4)",
        "near_threshold": near_threshold,
        "scans": scans,
        "near_dup_scan": near,
        "total_exact_purged_leakage": int(
            sum(s["exact_purged"] for s in scans if s["scan"] != "direct⊗direct")
        ),
        "cross_corpus_dups": int(
            next(s["exact_purged"] for s in scans if s["scan"] == "direct⊗direct")
        ),
        "near_purged": len(near_norm),
        "purged_normalized_texts": manifest,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Arm-A leakage gate (exact + near-dup; §vi).")
    ap.add_argument("--near-threshold", type=float, default=0.8)
    ap.add_argument("--out", default=str(OUT_DIR))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    report = run_gate(near_threshold=args.near_threshold)
    (out / "leakage_gate_armA.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(
        f"\n[done] exact-leakage-purged={report['total_exact_purged_leakage']} "
        f"near-purged={report['near_purged']} cross-corpus-dups={report['cross_corpus_dups']} "
        f"manifest={len(report['purged_normalized_texts'])} → {out}/leakage_gate_armA.json"
    )


if __name__ == "__main__":
    main()
