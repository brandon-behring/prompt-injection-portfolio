"""Stage C — per-set content deep-dive for the Phase-2 new datasets.

Reads a small stratified sample of REAL rows per set so mislabeling / junk / off-axis content that the
aggregate stats miss is caught before any role is proposed. HF-native sets load via ``load_dataset``
(format-agnostic, already cached by the survey); JailbreakDB reads its raw CSVs directly (Viewer broken).
Output: ``experiments/eda/NEW_SETS_AUDIT/content_samples.json`` (+ compact stdout). Read-only.
"""

from __future__ import annotations

import json
import re
import textwrap
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
import pandas as pd

RAW = Path("data/raw")
OUT = Path("experiments/eda/NEW_SETS_AUDIT")
OUT.mkdir(parents=True, exist_ok=True)
PER = 4  # samples per label stratum


def _clip(t: object, n: int = 200) -> str:
    return textwrap.shorten(" ".join(str(t).split()), width=n, placeholder=" …")


def _py(v: object) -> object:
    return v.item() if hasattr(v, "item") else v


def _ld(hf_id: str, config: str | None = None) -> pd.DataFrame:
    """Load all splits of an HF dataset into one DataFrame (format-agnostic)."""
    from datasets import load_dataset

    dd = load_dataset(hf_id, config) if config else load_dataset(hf_id)
    return pd.concat([dd[s].to_pandas() for s in dd], ignore_index=True)


def _strat(df: pd.DataFrame, label_col: str, feat_col: str, extra: tuple[str, ...] = ()) -> list[dict]:
    out: list[dict] = []
    for lab, g in df.groupby(label_col):
        for _, r in g.sample(min(PER, len(g)), random_state=42).iterrows():
            row = {"label": _py(lab), "text": _clip(r[feat_col])}
            for e in extra:
                if e in r:
                    row[e] = _py(r[e])
            out.append(row)
    return out


def main() -> None:
    samples: dict[str, list[dict]] = {}

    samples["neuralchemy"] = _strat(
        _ld("neuralchemy/Prompt-injection-dataset", "core"), "label", "text",
        extra=("category", "source", "severity"),
    )
    samples["aegis2"] = _strat(
        _ld("nvidia/Aegis-AI-Content-Safety-Dataset-2.0"), "prompt_label", "prompt",
        extra=("violated_categories",),
    )
    fr = _ld("AmazonScience/FalseReject")
    samples["falsereject"] = [
        {"text": _clip(r["prompt"]), "category_text": _py(r.get("category_text"))}
        for _, r in fr.sample(min(8, len(fr)), random_state=42).iterrows()
    ]
    bs = _ld("perplexity-ai/browsesafe-bench")
    bs["stripped"] = bs["content"].astype(str).map(lambda t: _clip(re.sub(r"<[^>]+>", " ", t), 240))
    samples["browsesafe"] = _strat(bs, "label", "stripped")

    jb: list[dict] = []
    for f in ["text_jailbreak_unique.csv", "text_regular_unique.csv"]:
        df = pd.read_csv(RAW / "jailbreakdb" / f, nrows=3000)
        for _, r in df.sample(min(PER, len(df)), random_state=42).iterrows():
            jb.append(
                {"file": f, "jailbreak": int(r["jailbreak"]), "source": r.get("source"),
                 "text": _clip(r["user_prompt"])}
            )
    samples["jailbreakdb"] = jb  # NOTE: nrows=3000 head per file → source-biased qualitative peek

    (OUT / "content_samples.json").write_text(json.dumps(samples, indent=2), encoding="utf-8")
    for k, v in samples.items():
        print(f"\n=== {k} ({len(v)} samples) ===")
        for r in v:
            print("  ", {kk: (_clip(vv, 90) if kk == "text" else vv) for kk, vv in r.items()})
    print(f"\n[done] wrote {OUT}/content_samples.json")


if __name__ == "__main__":
    main()
