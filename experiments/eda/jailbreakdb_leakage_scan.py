"""JailbreakDB ⟶ {jackhhao, shen_dan, jbb} leakage scan (D5 — the authoritative gate).

The default 250-row geometry E4 cannot validate a 12.2M-row, ~14-source aggregate, so this is the
load-bearing leakage gate for JailbreakDB. Three passes, **library-first** (ADR-026; eval_toolkit.text_dedup):

  (a) PROVENANCE  full ``source``-column tabulation (the free prior — JailbreakDB self-declares its sources).
  (b) EXACT       normalized-text membership over the FULL ~12.2M stream vs the ~68K probe rows (definitive).
  (c) NEAR        MinHash-LSH ``cross_dedup_pairs`` on a representative JailbreakDB sample vs the probe
                  (the paraphrase tail beyond exact matches).

Output: ``experiments/eda/NEW_SETS_AUDIT/jailbreakdb_leakage.json`` (compact verdict; raw rows never printed).
Run:    uv run python experiments/eda/jailbreakdb_leakage_scan.py [--near-sample 60000] [--near-threshold 0.8]
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path

import pandas as pd

REPO = Path.cwd()
RAW = REPO / "data" / "raw"
OUT = REPO / "experiments" / "eda" / "NEW_SETS_AUDIT"
JDB = RAW / "jailbreakdb"
JDB_FILES = ["text_jailbreak_unique.csv", "text_regular_unique.csv"]
# existing corpora JailbreakDB might contaminate -> candidate text columns (first present wins).
PROBES: dict[str, list[str]] = {
    "jackhhao": ["prompt", "text"],
    "shen_dan": ["prompt", "text"],
    "jbb": ["Goal", "goal", "prompt", "Behavior", "behavior", "query", "target", "text"],
}
CHUNK = 500_000
APPROX_ROWS = 12_200_000


def _norm_series(s: pd.Series) -> pd.Series:
    """Vectorized mirror of eval_toolkit.text_dedup.normalize_text_for_dedup (NFC + lower + collapse-ws)."""
    return s.astype(str).str.normalize("NFC").str.lower().str.split().str.join(" ")


def _load_probe_texts(dirname: str, cols: list[str]) -> list[str]:
    """Load a probe corpus's text column from its materialized files (parquet / csv / json[l])."""
    d = RAW / dirname
    files = sorted(
        list(d.rglob("*.parquet")) + list(d.rglob("*.csv"))
        + list(d.rglob("*.jsonl")) + list(d.rglob("*.json"))
    )
    texts: list[str] = []
    for p in files:
        try:
            if p.suffix == ".parquet":
                df = pd.read_parquet(p)
            elif p.suffix == ".csv":
                df = pd.read_csv(p)
            else:
                df = pd.read_json(p, lines=(p.suffix == ".jsonl"))
        except Exception:  # noqa: BLE001 — an unparseable probe file is skipped, not fatal
            continue
        col = next((c for c in cols if c in df.columns), None)
        if col is None:  # fallback: the longest-mean-length object column
            obj = [c for c in df.columns if df[c].dtype == object]
            if not obj:
                continue
            col = max(obj, key=lambda c: df[c].astype(str).str.len().mean())
        texts.extend(df[col].dropna().astype(str).tolist())
    return texts


def main() -> None:
    ap = argparse.ArgumentParser(description="JailbreakDB leakage scan (D5)")
    ap.add_argument("--near-sample", type=int, default=60_000)
    ap.add_argument("--near-threshold", type=float, default=0.8)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    from eval_toolkit.text_dedup import (
        MinHashLSHStrategy,
        cross_dedup_pairs,
        normalize_text_for_dedup,
    )

    # --- probe set + exact-membership index (normalized text -> corpus) ---
    probe_texts: list[str] = []
    probe_corpus: list[str] = []
    probe_counts: dict[str, int] = {}
    for corpus, cols in PROBES.items():
        t = _load_probe_texts(corpus, cols)
        probe_texts += t
        probe_corpus += [corpus] * len(t)
        probe_counts[corpus] = len(t)
        print(f"[probe] {corpus:10s} {len(t)} rows", flush=True)
    if not probe_texts:
        raise RuntimeError("no probe texts loaded — check data/raw/{jackhhao,shen_dan,jbb}")

    probe_norm = _norm_series(pd.Series(probe_texts))
    # consistency guard: the vectorized normalize MUST match the library scalar fn (no silent divergence)
    for t in probe_texts[:200]:
        if _norm_series(pd.Series([t])).iloc[0] != normalize_text_for_dedup(t):
            raise AssertionError("vectorized normalize diverges from eval_toolkit.normalize_text_for_dedup")
    norm_to_corpus: dict[str, str] = {}
    for nt, c in zip(probe_norm.tolist(), probe_corpus):
        norm_to_corpus.setdefault(nt, c)
    probe_norm_set = set(norm_to_corpus)
    print(f"[probe] total {len(probe_texts)} rows, {len(probe_norm_set)} unique normalized", flush=True)

    # --- (a) provenance + (b) exact, FULL stream + a per-chunk fraction into the near pool ---
    src_counter: Counter = Counter()
    exact_by_probe: Counter = Counter()
    exact_by_route: Counter = Counter()  # "jdb_source → probe_corpus"
    exact_samples: list[dict] = []
    near_pool: list[str] = []
    n_total = 0
    frac = min(1.0, (args.near_sample * 1.5) / APPROX_ROWS)
    for f in JDB_FILES:
        path = JDB / f
        for chunk in pd.read_csv(path, usecols=["user_prompt", "source"], chunksize=CHUNK):
            ups = chunk["user_prompt"].astype(str)
            srcs = chunk["source"].astype(str)
            n_total += len(chunk)
            src_counter.update(srcs.value_counts().to_dict())
            norm = _norm_series(ups)
            hit = norm.isin(probe_norm_set)
            if hit.any():
                for u, s, nt in zip(ups[hit].tolist(), srcs[hit].tolist(), norm[hit].tolist()):
                    c = norm_to_corpus.get(nt, "?")
                    exact_by_probe[c] += 1
                    exact_by_route[f"{s} -> {c}"] += 1
                    if len(exact_samples) < 30:
                        exact_samples.append({"jdb_source": s, "probe": c, "text": u[:140]})
            near_pool.extend(
                ups.sample(frac=frac, random_state=42).tolist() if frac < 1.0 else ups.tolist()
            )
            print(
                f"  [{f[:18]:18s}] scanned={n_total:>9d} exact_hits={sum(exact_by_probe.values()):>6d}",
                flush=True,
            )
    if len(near_pool) > args.near_sample:
        near_pool = random.Random(42).sample(near_pool, args.near_sample)

    # --- (c) near-dup (MinHash-LSH) on the sample vs the probe ---
    strat = MinHashLSHStrategy(n=3, num_perm=128, bands=16, seed=42)
    pairs = cross_dedup_pairs(probe_texts, near_pool, threshold=args.near_threshold, strategy=strat)
    near_eval_hits = {e for (e, _t, _s) in pairs}
    near_by_probe: Counter = Counter()
    near_samples: list[dict] = []
    for e, tr, sim in pairs:
        c = probe_corpus[tr] if tr < len(probe_corpus) else "?"
        near_by_probe[c] += 1
        if len(near_samples) < 20:
            near_samples.append(
                {"probe": c, "sim": round(sim, 3), "jdb_text": near_pool[e][:120],
                 "probe_text": probe_texts[tr][:120]}
            )

    exact_total = sum(exact_by_probe.values())
    verdict = {
        "n_jailbreakdb_rows": n_total,
        "probe_corpora": probe_counts,
        "provenance_top_sources": dict(src_counter.most_common(40)),
        "exact_overlap": {
            "total_rows": exact_total,
            "rate": round(exact_total / max(n_total, 1), 6),
            "by_probe_corpus": dict(exact_by_probe),
            "by_route_top": dict(exact_by_route.most_common(20)),
            "samples": exact_samples,
        },
        "near_overlap_estimate": {
            "near_sample_n": len(near_pool),
            "threshold": args.near_threshold,
            "pairs": len(pairs),
            "unique_jdb_rows_hit": len(near_eval_hits),
            "rate_in_sample": round(len(near_eval_hits) / max(len(near_pool), 1), 6),
            "by_probe_corpus": dict(near_by_probe),
            "samples": near_samples,
        },
        "interpretation": (
            "exact_overlap = JailbreakDB rows byte-identical (after NFC+lower+ws normalization) to an existing "
            "jackhhao/shen_dan/jbb row -> definitive contamination. near_overlap_estimate extrapolates the "
            "paraphrase tail from a representative sample. provenance_top_sources self-declares JailbreakDB's "
            "component corpora; any JBB-Behaviors / in-the-wild / jailbreak-classification entry is prima-facie "
            "overlap with our universe."
        ),
    }
    (OUT / "jailbreakdb_leakage.json").write_text(json.dumps(verdict, indent=2), encoding="utf-8")
    print(
        f"\n[done] scanned {n_total} rows | exact={exact_total} (rate {verdict['exact_overlap']['rate']}) "
        f"by={dict(exact_by_probe)} | near_sample={len(near_pool)} near_hits={len(near_eval_hits)}",
        flush=True,
    )
    print(f"[done] wrote {OUT}/jailbreakdb_leakage.json", flush=True)


if __name__ == "__main__":
    main()
