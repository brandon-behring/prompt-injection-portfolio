"""neuralchemy (core) ⟶ our-universe leakage scan — to settle dedup-vs-park (G-EDA-1).

neuralchemy declares a `source` column showing ~38% of its core rows are drawn from corpora we already
have (hackaprompt 1984, wildguard 300, harmbench 100). This quantifies the ACTUAL overlap (exact + MinHash
near-dup, library-first via eval_toolkit.text_dedup) so we can decide: dedup-and-use the clean remainder,
or park. In-memory (neuralchemy core ≈ 6.3K; probe sampled where huge).

Output: experiments/eda/NEW_SETS_AUDIT/neuralchemy_leakage.json.
Run:    uv run python experiments/eda/neuralchemy_leakage_scan.py
"""

from __future__ import annotations

import json
import textwrap
import warnings
from collections import Counter
from pathlib import Path

warnings.filterwarnings("ignore")
import pandas as pd

RAW = Path("data/raw")
OUT = Path("experiments/eda/NEW_SETS_AUDIT")
OUT.mkdir(parents=True, exist_ok=True)
# our universe (candidate text columns); cap big corpora for the in-memory probe.
UNIVERSE: dict[str, list[str]] = {
    "hackaprompt": ["prompt", "user_input", "text"],
    "wildguardmix": ["prompt"],
    "guychuk": ["prompt", "text"],
    "promptshield": ["prompt", "text"],
    "deepset": ["text"],
    "spml": ["User Prompt", "user_prompt", "text"],
    "jackhhao": ["prompt", "text"],
    "shen_dan": ["prompt", "text"],
    "jbb": ["Goal", "goal", "prompt"],
}
PROBE_CAP = 250_000  # per-corpus cap for the in-memory probe (random sample if larger)
NEAR_PROBE_CAP = 25_000  # smaller cap for the MinHash near-dup pass


def _clip(t: object, n: int = 140) -> str:
    return textwrap.shorten(" ".join(str(t).split()), width=n, placeholder=" …")


def _load_universe_texts(corpus: str, cols: list[str], cap: int) -> list[str]:
    d = RAW / corpus
    if not d.exists():
        d = RAW / "_eda_only_unlicensed" / corpus
    texts: list[str] = []
    for p in (list(d.rglob("*.parquet")) + list(d.rglob("*.csv")) + list(d.rglob("*.jsonl"))
              + list(d.rglob("*.json"))):
        try:
            if p.suffix == ".parquet":
                df = pd.read_parquet(p)
            elif p.suffix == ".csv":
                df = pd.read_csv(p)
            else:
                df = pd.read_json(p, lines=(p.suffix == ".jsonl"))
        except Exception:  # noqa: BLE001
            continue
        c = next((x for x in cols if x in df.columns), None)
        if c:
            texts.extend(df[c].dropna().astype(str).tolist())
    if len(texts) > cap:
        texts = pd.Series(texts).sample(cap, random_state=42).tolist()
    return texts


def main() -> None:
    from datasets import load_dataset
    from eval_toolkit.text_dedup import MinHashLSHStrategy, cross_dedup_pairs, normalize_text_for_dedup

    nc = load_dataset("neuralchemy/Prompt-injection-dataset", "core")
    df = pd.concat([nc[s].to_pandas() for s in nc], ignore_index=True)
    nc_texts = df["text"].astype(str).tolist()
    nc_source = df["source"].astype(str).tolist() if "source" in df else ["?"] * len(df)
    nc_norm = [normalize_text_for_dedup(t) for t in nc_texts]
    OUR_SOURCES = {"hackaprompt", "wildguard_judgecomp", "harmbench", "harmbench_benign"}  # declared-from-us

    # exact membership: probe normalized -> corpus
    probe_norm: dict[str, str] = {}
    probe_counts: dict[str, int] = {}
    for corpus, cols in UNIVERSE.items():
        t = _load_universe_texts(corpus, cols, PROBE_CAP)
        probe_counts[corpus] = len(t)
        for x in t:
            probe_norm.setdefault(normalize_text_for_dedup(x), corpus)
        print(f"[probe] {corpus:14s} {len(t)} rows", flush=True)

    exact_hit_corpus: list[str | None] = [probe_norm.get(n) for n in nc_norm]
    exact_by_corpus = Counter(c for c in exact_hit_corpus if c)
    exact_by_source = Counter(nc_source[i] for i, c in enumerate(exact_hit_corpus) if c)
    n_exact = sum(1 for c in exact_hit_corpus if c)

    # near-dup (MinHash) vs a capped probe
    near_probe: list[str] = []
    for corpus, cols in UNIVERSE.items():
        near_probe += [(t) for t in _load_universe_texts(corpus, cols, NEAR_PROBE_CAP)]
    strat = MinHashLSHStrategy(n=3, num_perm=128, bands=16, seed=42)
    pairs = cross_dedup_pairs(near_probe, nc_texts, threshold=0.8, strategy=strat)
    near_hit_idx = {e for (e, _t, _s) in pairs}
    # rows that are NEITHER exact nor near, AND not declared-from-our-sources -> the clean novel remainder
    clean = [
        i for i in range(len(df))
        if exact_hit_corpus[i] is None and i not in near_hit_idx and nc_source[i] not in OUR_SOURCES
    ]
    source_dist = Counter(nc_source)

    report = {
        "n_neuralchemy_core": len(df),
        "source_distribution": dict(source_dist.most_common()),
        "declared_from_our_corpora": {s: source_dist[s] for s in OUR_SOURCES if s in source_dist},
        "exact_overlap": {
            "total": n_exact, "rate": round(n_exact / max(len(df), 1), 4),
            "by_universe_corpus": dict(exact_by_corpus), "by_neuralchemy_source": dict(exact_by_source),
            "samples": [{"src": nc_source[i], "hit": exact_hit_corpus[i], "text": _clip(nc_texts[i])}
                        for i in range(len(df)) if exact_hit_corpus[i]][:15],
        },
        "near_overlap": {"near_probe_n": len(near_probe), "threshold": 0.8,
                         "neuralchemy_rows_hit": len(near_hit_idx),
                         "rate": round(len(near_hit_idx) / max(len(df), 1), 4)},
        "clean_remainder": {
            "n": len(clean), "rate": round(len(clean) / max(len(df), 1), 4),
            "definition": "not exact-dup, not near-dup(>=0.8), and source NOT in {hackaprompt,wildguard,harmbench}",
            "source_dist": dict(Counter(nc_source[i] for i in clean).most_common()),
        },
        "probe_corpora_counts": probe_counts,
        "verdict_input": (
            "dedup-and-use is viable iff the clean_remainder is large + genuinely novel; park if overlap is "
            "pervasive or the remainder is too small/low-value. (user leans park.)"
        ),
    }
    (OUT / "neuralchemy_leakage.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\n[done] n={len(df)} | exact={n_exact} ({report['exact_overlap']['rate']}) "
          f"by_corpus={dict(exact_by_corpus)} | near={len(near_hit_idx)} | CLEAN remainder={len(clean)} "
          f"({report['clean_remainder']['rate']})", flush=True)
    print(f"[done] wrote {OUT}/neuralchemy_leakage.json", flush=True)


if __name__ == "__main__":
    main()
