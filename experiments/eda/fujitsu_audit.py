"""Fujitsu/agentic-rag-redteam-bench (ART-SafeBench v2.0.0) EDA gate — gate granted 2026-06-03.

A multi-config RAG-injection / poisoning red-team benchmark. Audits the TEXT configs: derives the
B1 poison/benign and B4 malicious/benign binaries, tabulates the ``source_dataset`` provenance (the leakage
prior — it aggregates jbb/gandalf/injecagent/tensortrust/raguard/harmbench), and exact-checks its text vs our
existing universe. Output: ``experiments/eda/NEW_SETS_AUDIT/fujitsu_audit.json``. Read-only.
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
HF = "Fujitsu/agentic-rag-redteam-bench"
# our universe sets that Fujitsu declares as source_datasets -> candidate text columns
UNIVERSE = {
    "jbb": ["Goal", "goal", "prompt", "Behavior"],
    "gandalf_ignore": ["prompt", "text"],
    "gandalf_summ": ["prompt", "text"],
    "injecagent": ["text", "attacker_instruction"],
}


def _clip(t: object, n: int = 180) -> str:
    return textwrap.shorten(" ".join(str(t).split()), width=n, placeholder=" …")


def _load_cfg(cfg: str) -> pd.DataFrame:
    from datasets import load_dataset

    return load_dataset(HF, cfg, split="train").to_pandas()


def _charlen(s: pd.Series) -> tuple[int, int]:
    x = s.dropna().astype(str).str.len()
    return (int(x.quantile(0.5)), int(x.quantile(0.95))) if len(x) else (0, 0)


def _load_universe_texts(corpus: str, cols: list[str]) -> list[str]:
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
    return texts


def main() -> None:
    from datasets import get_dataset_config_names
    from eval_toolkit.text_dedup import normalize_text_for_dedup as norm

    cfgs = get_dataset_config_names(HF)
    report: dict = {"configs": {}, "derived_binaries": {}, "provenance_source_dataset": {},
                    "leakage_vs_universe": {}, "samples": {}}
    src_counter: Counter = Counter()
    fuj_texts: list[str] = []
    for cfg in cfgs:
        try:
            df = _load_cfg(cfg)
        except Exception as e:  # noqa: BLE001 — failed-parquet configs are recorded, not fatal
            report["configs"][cfg] = {"status": f"LOAD-FAIL: {str(e)[:80]}"}
            continue
        report["configs"][cfg] = {"rows": len(df), "cols": list(df.columns)}
        if "source_dataset" in df:
            src_counter.update(df["source_dataset"].dropna().astype(str).tolist())
        for col in ("poison_content", "user_query", "malicious_injection"):
            if col in df:
                fuj_texts += [t for t in df[col].dropna().astype(str).tolist() if t and t != "None"]

    # B1 poison vs benign
    try:
        b1 = _load_cfg("B1_rag_text_poisoning")
        pos = b1["poison_content"].dropna().astype(str)
        pos = pos[pos.str.len() > 0]
        neg = b1["benign_content"].dropna().astype(str)
        neg = neg[(neg.str.len() > 0) & (neg != "None")]
        report["derived_binaries"]["B1_poison_vs_benign"] = {
            "pos_poison": len(pos), "neg_benign": len(neg),
            "poison_charlen_p50_p95": _charlen(pos), "benign_charlen_p50_p95": _charlen(neg)}
        report["samples"]["B1_poison"] = [_clip(t, 200) for t in pos.head(3)]
        report["samples"]["B1_benign"] = [_clip(t, 200) for t in neg.head(2)]
    except Exception as e:  # noqa: BLE001
        report["derived_binaries"]["B1_poison_vs_benign"] = {"err": str(e)[:100]}

    # B4 malicious vs benign
    try:
        b4 = _load_cfg("B4_orchestrator")
        report["derived_binaries"]["B4_malicious_vs_benign"] = {
            "malicious_injection_n": int(b4["malicious_injection"].astype(str).str.len().gt(0).sum()),
            "benign_query_n": int(b4["benign_query"].astype(str).str.len().gt(0).sum()),
            "success_vc": (b4["success"].value_counts().head(5).to_dict() if "success" in b4 else None)}
        report["samples"]["B4_malicious"] = [_clip(t, 200) for t in b4["malicious_injection"].dropna().astype(str).head(3)]
    except Exception as e:  # noqa: BLE001
        report["derived_binaries"]["B4_malicious_vs_benign"] = {"err": str(e)[:100]}

    report["provenance_source_dataset"] = dict(src_counter.most_common(25))

    # leakage vs our universe (exact normalized membership)
    probe: dict[str, str] = {}
    probe_counts: dict[str, int] = {}
    for corpus, cols in UNIVERSE.items():
        t = _load_universe_texts(corpus, cols)
        probe_counts[corpus] = len(t)
        for x in t:
            probe.setdefault(norm(x), corpus)
    hits: Counter = Counter()
    for t in fuj_texts:
        c = probe.get(norm(t))
        if c:
            hits[c] += 1
    report["leakage_vs_universe"] = {
        "probe_corpora": probe_counts, "fujitsu_texts_checked": len(fuj_texts),
        "exact_hits_by_universe_corpus": dict(hits),
        "note": "exact normalized matches of Fujitsu poison/query/injection text to our jbb/gandalf/injecagent"}

    (OUT / "fujitsu_audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({
        "configs": {k: v.get("rows", v.get("status")) for k, v in report["configs"].items()},
        "derived": report["derived_binaries"],
        "provenance_top": dict(list(report["provenance_source_dataset"].items())[:12]),
        "leakage": report["leakage_vs_universe"]}, indent=2))
    print(f"[done] wrote {OUT}/fujitsu_audit.json")


if __name__ == "__main__":
    main()
