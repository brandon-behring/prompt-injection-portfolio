"""Arm-B dialect-LODO leakage gate (criteria.md Q2: exact + MinHash≥0.8, PURGE-FROM-TRAIN).

For each held-out-dialect fold, scan the **train** dialects' texts against the **held-out test**
dialect's texts and purge matching TRAIN rows (the held-out test is sacrosanct). Two passes,
library-first (ADR-026; ``eval_toolkit.text_dedup``), mirroring ``jailbreakdb_leakage_scan.py``:

  (a) EXACT  normalized-text membership (``ExactNormalizedHashStrategy`` semantics via
             ``normalize_text_for_dedup`` + ``sha256_text``).
  (b) NEAR   ``MinHashLSHStrategy`` ``cross_dedup_pairs(train, test, threshold=0.8)`` — the
             paraphrase tail beyond exact matches.

CRITICAL in-Arm-B case (verified ``data/raw/MANIFEST.json:242``): **fujitsu B1 aggregates
InjecAgent** (the fujitsu adapters cite injecagent/jbb/gandalf/harmbench/tensortrust), so when
InjecAgent ∈ train and fujitsu is held out (and vice-versa) we expect real overlap — scan + purge.

Emits ``experiments/cross-family-transfer/B2_leakage/leakage_gate.json`` (per-fold before/after
sizes, #exact + #near purged, sampled colliding pairs). Raw rows are truncated, never dumped whole.

Run::

    uv run python experiments/cross-family-transfer/leakage_gate.py [--near-threshold 0.8]
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

from assemble import assemble  # noqa: E402
from folds_dialect import LODO_DIALECTS, _dialect_lodo_builder  # noqa: E402

OUT_DIR = _HERE / "B2_leakage"


def _exact_purge_mask(
    train_texts: list[str], test_texts: list[str], normalize, sha256
) -> list[bool]:
    """Return a keep-mask over train: False where a train hash matches a test text's hash.

    Uses the library ``normalize_text_for_dedup`` + ``sha256_text`` (the ExactNormalizedHash
    semantics) for a hash-set membership test — definitive exact-dup detection.
    """
    test_hashes = {sha256(normalize(t)) for t in test_texts}
    return [sha256(normalize(t)) not in test_hashes for t in train_texts]


def scan_fold(
    held_out: str,
    frame: pd.DataFrame,
    *,
    near_threshold: float,
) -> dict:
    """Run the exact+near leakage scan for one held-out-dialect fold; return the report dict.

    Scans train (dialect≠held_out) against the held-out test (dialect==held_out); records which
    TRAIN rows would be purged (exact-hash match OR MinHash≥threshold near-dup) and the resulting
    sizes. The test split is never modified.
    """
    from eval_toolkit.text_dedup import (
        MinHashLSHStrategy,
        cross_dedup_pairs,
        normalize_text_for_dedup,
        sha256_text,
    )

    train, test = _dialect_lodo_builder(held_out)(frame)
    train_texts = train["text"].astype(str).tolist()
    test_texts = test["text"].astype(str).tolist()

    # (a) exact
    exact_keep = _exact_purge_mask(train_texts, test_texts, normalize_text_for_dedup, sha256_text)
    exact_purged_idx = {i for i, keep in enumerate(exact_keep) if not keep}

    # (b) near (MinHash-LSH); cross_dedup_pairs(train, eval) → (train_idx, eval_idx, sim)
    strat = MinHashLSHStrategy(n=3, num_perm=128, bands=16, seed=42)
    pairs = cross_dedup_pairs(train_texts, test_texts, threshold=near_threshold, strategy=strat)
    near_purged_idx = {tr for (tr, _ev, _sim) in pairs}

    purged_idx = exact_purged_idx | near_purged_idx
    near_only = near_purged_idx - exact_purged_idx

    samples: list[dict] = []
    for tr, ev, sim in pairs[:8]:
        samples.append(
            {
                "sim": round(float(sim), 3),
                "train_dialect": str(train.iloc[tr]["dialect"]),
                "train_text": train_texts[tr][:140],
                "test_text": test_texts[ev][:140],
            }
        )

    train_after = len(train_texts) - len(purged_idx)
    purged_by_dialect: dict[str, int] = {}
    for i in purged_idx:
        d = str(train.iloc[i]["dialect"])
        purged_by_dialect[d] = purged_by_dialect.get(d, 0) + 1

    return {
        "held_out": held_out,
        "train_dialects": sorted({str(d) for d in train["dialect"].unique()}),
        "train_size_before": len(train_texts),
        "test_size": len(test_texts),
        "exact_purged": len(exact_purged_idx),
        "near_purged_total": len(near_purged_idx),
        "near_only_purged": len(near_only),
        "total_purged": len(purged_idx),
        "train_size_after": train_after,
        "purged_by_train_dialect": purged_by_dialect,
        "near_threshold": near_threshold,
        "sampled_colliding_pairs": samples,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Arm-B dialect-LODO leakage gate (exact + MinHash≥0.8)."
    )
    ap.add_argument("--near-threshold", type=float, default=0.8)
    ap.add_argument("--out", default=str(OUT_DIR))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    print("[assemble] loading the 4 Arm-B dialects ...", flush=True)
    frame = assemble()
    print(f"[assemble] rows={len(frame)} dialects={sorted(frame['dialect'].unique())}", flush=True)

    folds = []
    for held_out in LODO_DIALECTS:
        print(f"[scan] held_out={held_out} ...", flush=True)
        rep = scan_fold(held_out, frame, near_threshold=args.near_threshold)
        folds.append(rep)
        print(
            f"  train {rep['train_size_before']}→{rep['train_size_after']} "
            f"(exact={rep['exact_purged']} near-only={rep['near_only_purged']}) "
            f"test={rep['test_size']} purged-by={rep['purged_by_train_dialect']}",
            flush=True,
        )

    report = {"near_threshold": args.near_threshold, "folds": folds}
    (out / "leakage_gate.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"[done] wrote {out}/leakage_gate.json", flush=True)


if __name__ == "__main__":
    main()
