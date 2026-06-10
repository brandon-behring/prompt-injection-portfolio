"""C1 leakage gate: synthetic corpus vs the BIPIA held-table TEST (criteria.md).

Per the ratified pre-registration: provenance disjointness between the synthetic
table corpus and the BIPIA table test is enforced with **exact normalized-hash +
MinHash >= 0.8, purge-from-train, test sacrosanct**, using the corrected
``cross_dedup_pairs(train, eval) -> (eval_idx, train_idx, sim)`` convention
(audit W17). Mirrors ``../cross-family-transfer/leakage_gate.py``.

The scanned unit is the **pre-injection context** (every corpus row carries its
``context_sha256``): a colliding context purges ALL rows derived from it (the
clean negative + its injected positives). Scanning contexts rather than injected
texts isolates generator-text leakage — payload overlap with BIPIA is inherent
to the carrier axis and pre-declared in the criteria, not leakage.

Emits ``leakage_gate.json`` + ``corpus_gated.parquet`` (the post-purge corpus
the treated arm trains on). Raw rows are truncated in the report, never dumped.

Run::

    uv run python experiments/carrier-table-training/leakage_gate.py [--near-threshold 0.8]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).resolve().parent
_OOD_DIR = _HERE.parent / "eda" / "OOD_WALL_PREDICTION"
if str(_OOD_DIR) not in sys.path:
    sys.path.insert(0, str(_OOD_DIR))

from bipia_carrier import build_examples  # noqa: E402  # type: ignore[import-not-found]

REPO_ROOT = _HERE.parent.parent
BIPIA_ROOT = REPO_ROOT / "data" / "raw" / "BIPIA" / "benchmark"


def scan_corpus(
    corpus: pd.DataFrame,
    test_texts: list[str],
    *,
    near_threshold: float,
) -> tuple[pd.DataFrame, dict]:
    """Scan corpus contexts against the held-table test; return (gated corpus, report).

    Purge basis is the unique pre-injection context (one negative row per context);
    a context hit removes every corpus row sharing its ``context_sha256``. The test
    side is never modified.
    """
    from eval_toolkit.text_dedup import (
        MinHashLSHStrategy,
        cross_dedup_pairs,
        normalize_text_for_dedup,
        sha256_text,
    )

    neg = corpus[corpus["label"] == 0]
    ctx_texts = neg["text"].astype(str).tolist()
    ctx_shas = neg["context_sha256"].astype(str).tolist()

    # (a) exact normalized-hash membership
    test_hashes = {sha256_text(normalize_text_for_dedup(t)) for t in test_texts}
    exact_hit = {
        ctx_shas[i]
        for i, t in enumerate(ctx_texts)
        if sha256_text(normalize_text_for_dedup(t)) in test_hashes
    }

    # (b) near (MinHash-LSH); cross_dedup_pairs(train, eval) -> (eval_idx, train_idx, sim) [W17]
    strat = MinHashLSHStrategy(n=3, num_perm=128, bands=16, seed=42)
    pairs = cross_dedup_pairs(ctx_texts, test_texts, threshold=near_threshold, strategy=strat)
    near_hit = {ctx_shas[tr] for (_ev, tr, _sim) in pairs}

    purged_shas = exact_hit | near_hit
    keep = ~corpus["context_sha256"].isin(purged_shas)
    gated = corpus[keep].reset_index(drop=True)

    samples = [
        {
            "sim": round(float(sim), 3),
            "corpus_context": ctx_texts[tr][:140],
            "test_text": test_texts[ev][:140],
        }
        for ev, tr, sim in pairs[:8]
    ]
    report = {
        "near_threshold": near_threshold,
        "contexts_scanned": len(ctx_texts),
        "test_size": len(test_texts),
        "exact_hit_contexts": len(exact_hit),
        "near_hit_contexts": len(near_hit),
        "purged_contexts": len(purged_shas),
        "rows_before": int(len(corpus)),
        "rows_after": int(len(gated)),
        "positives_after": int((gated["label"] == 1).sum()),
        "negatives_after": int((gated["label"] == 0).sum()),
        "sampled_colliding_pairs": samples,
    }
    return gated, report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="C1 corpus-vs-BIPIA-table-test leakage gate.")
    ap.add_argument("--near-threshold", type=float, default=0.8)
    ap.add_argument("--corpus", type=Path, default=_HERE / "corpus.parquet")
    ap.add_argument("--out", type=Path, default=_HERE / "corpus_gated.parquet")
    args = ap.parse_args(argv)

    corpus = pd.read_parquet(args.corpus)
    print(f"[gate] corpus rows={len(corpus)}", flush=True)
    ex = build_examples(root=BIPIA_ROOT, seed=0)
    test_texts = ex.frame.loc[ex.frame["carrier"] == "table", "text"].astype(str).tolist()
    print(f"[gate] held-table test texts={len(test_texts)}", flush=True)

    gated, report = scan_corpus(corpus, test_texts, near_threshold=args.near_threshold)
    gated.to_parquet(args.out, index=False)
    report["corpus_gated_sha256"] = hashlib.sha256(args.out.read_bytes()).hexdigest()
    (_HERE / "leakage_gate.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"[gate] contexts purged={report['purged_contexts']} "
        f"(exact={report['exact_hit_contexts']} near={report['near_hit_contexts']}); "
        f"rows {report['rows_before']}->{report['rows_after']}; wrote {args.out.name}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
