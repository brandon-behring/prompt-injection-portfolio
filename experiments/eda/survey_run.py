#!/usr/bin/env python3
"""Phase 2 — broad dataset survey. For each candidate: load_dataset() for real,
discover the actual schema, map (text,label), run eval_toolkit.eda.audit_dataset
(ModernBERT tokenizer, context_window=8192, obfuscation), write per-dataset audit.json,
and record measured-vs-ledger discrepancies. The usable working set is the set that
survives (loads + sound + mappable). No silent caps: large sets are sampled with a logged note.

Usage: uv run --no-project python experiments/eda/survey_run.py [bibkey ...]
       (no args = full batch; one arg = dogfood that single dataset)
       --out PATH selects the output file (default experiments/eda/survey_summary.json),
       enabling collision-free parallel per-dataset runs (one --out each).
"""
from __future__ import annotations
import json, sys, pathlib, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

OUT = pathlib.Path("experiments/eda")
CAP = 40_000  # rows above this are sampled (seeded) for the audit; logged, not silent

# bibkey -> hf id  (protectai pointer = a MODEL repo, not a dataset -> excluded)
CANDIDATES = {
    "deepset2023promptinjections": "deepset/prompt-injections",
    "jackhhao2023jailbreakclassification": "jackhhao/jailbreak-classification",
    "xtram12024safeguardpromptinjection": "xTRam1/safe-guard-prompt-injection",
    "jayavibhav2024promptinjection": "jayavibhav/prompt-injection",
    "jayavibhav2024promptinjectionsafety": "jayavibhav/prompt-injection-safety",
    "gentellab2024gentelbench": "GenTelLab/gentelbench-v1",
    "hendzh2025promptshield": "hendzh/PromptShield",
    "guychuk2024benignmalicious": "guychuk/benign-malicious-prompt-classification",
    "harelix2024mixedtechniques": "Harelix/Prompt-Injection-Mixed-Techniques-2024",
    "lin2023toxicchat": "lmsys/toxic-chat",
    "reshabhs2024spmlchatbotpromptinjection": "reshabhs/SPML_Chatbot_Prompt_Injection",
    "shen2023inthewild": "TrustAIRLab/in-the-wild-jailbreak-prompts",
    "han2024wildguard": "allenai/wildguardmix",
    "leolee2024notinject": "leolee99/NotInject",
    "rottger2024xstest": "natolambert/xstest-v2-copy",
    "cui2024orbench": "bench-llm/or-bench",
    "hackaprompt2023emnlp": "hackaprompt/hackaprompt-dataset",
    "llmailinject2025microsoft": "microsoft/llmail-inject-challenge",
}

TEXT_COLS = ["text", "prompt", "sentence", "input", "query", "message", "content",
             "user_input", "question", "jailbreak_query", "goal", "Prompt", "user_prompt",
             "instruction", "turns", "vanilla"]
LABEL_COLS = ["label", "labels", "is_injection", "injection", "jailbreak", "toxicity",
              "malicious", "is_jailbreak", "type", "category", "class", "target",
              "ground_truth_label", "jailbreaking", "prompt_injection", "is_safe", "safe"]


def pick(cols, cands):
    low = {c.lower(): c for c in cols}
    for c in cands:
        if c.lower() in low:
            return low[c.lower()]
    return None


def to_binary(series):
    """Return (mapped int series or None, semantics-note)."""
    vals = series.dropna().unique()
    s = set(map(lambda x: str(x).strip().lower(), vals))
    if s <= {"0", "1"} or s <= {"0.0", "1.0"}:
        return series.astype(float).astype(int), f"numeric {sorted(s)}"
    if s <= {"true", "false"}:
        return series.astype(str).str.lower().map({"true": 1, "false": 0}), "bool"
    pos = {"injection", "malicious", "jailbreak", "unsafe", "attack", "1", "yes", "harmful"}
    neg = {"benign", "safe", "legitimate", "clean", "0", "no", "normal"}
    if s <= (pos | neg):
        return series.astype(str).str.lower().map(lambda x: 1 if x in pos else 0), f"string {sorted(s)}"
    return None, f"non-binary ({len(vals)} vals: {list(vals)[:6]})"


def survey_one(bibkey, hf_id, tok):
    from datasets import load_dataset, get_dataset_config_names
    from eval_toolkit.eda import audit_dataset
    from eval_toolkit.loaders import DataFrameLoader
    rec = {"bibkey": bibkey, "hf_id": hf_id}
    try:
        try:
            dd = load_dataset(hf_id)
        except Exception:
            cfgs = get_dataset_config_names(hf_id)
            dd = load_dataset(hf_id, cfgs[0]); rec["config"] = cfgs[0]
        frames = []
        for split, d in dd.items():
            df = d.to_pandas(); df["__split__"] = split; frames.append(df)
        raw = pd.concat(frames, ignore_index=True)
        rec["measured_rows"] = int(len(raw))
        rec["measured_splits"] = {s: int((raw["__split__"] == s).sum()) for s in raw["__split__"].unique()}
        rec["measured_columns"] = list(c for c in raw.columns if c != "__split__")
    except Exception as e:
        rec["status"] = "LOAD-FAILED"; rec["error"] = str(e)[:240]
        return rec

    tcol = pick(rec["measured_columns"], TEXT_COLS)
    lcol = pick(rec["measured_columns"], LABEL_COLS)
    rec["mapped_text_col"], rec["mapped_label_col"] = tcol, lcol
    if tcol is None or lcol is None:
        rec["status"] = "NEEDS-MANUAL-MAPPING"
        rec["note"] = f"no clear {'text' if not tcol else ''}{'+' if not tcol and not lcol else ''}{'label' if not lcol else ''} column"
        return rec

    df = raw[[tcol, lcol, "__split__"]].copy()
    df[tcol] = df[tcol].astype(str)
    lab, sem = to_binary(df[lcol])
    rec["label_semantics"] = sem
    if lab is None:
        rec["status"] = "NON-BINARY-LABEL"
        return rec
    df["label"] = lab.values
    if len(df) > CAP:
        df = df.sample(CAP, random_state=42).reset_index(drop=True)
        rec["sampled"] = f"audited on {CAP}-row seeded sample of {rec['measured_rows']} (dedup/leakage partial)"

    loader = DataFrameLoader(df, split_col="__split__", feature_col=tcol, label_col="label",
                             name=bibkey)
    try:
        audit = audit_dataset(loader, tokenizer=tok, context_window=8192, obfuscation=True,
                              near=(len(df) <= CAP), cross_split=True)
        d = OUT / bibkey; d.mkdir(parents=True, exist_ok=True)
        audit.write(d / "audit.json")
        rec["status"] = "AUDITED"
        rec["gate_passed"] = bool(audit.gate_passed)
        rec["gate_summary"] = audit.gate_summary
        rec["label_distribution"] = {s: {"pos": ss.n_positive, "neg": ss.n_negative, "pos_pct": round(ss.pos_pct, 1)}
                                     for s, ss in audit.split_summaries.items()}
        rec["pct_over_8192"] = {s: ss.pct_over_context_window for s, ss in audit.split_summaries.items()}
        rec["obfuscation_invisible_rate"] = {s: round(ss.obfuscation.invisible_char_rate, 4)
                                             for s, ss in audit.split_summaries.items() if ss.obfuscation}
    except Exception as e:
        rec["status"] = "AUDIT-ERROR"; rec["error"] = str(e)[:240]
    return rec


def main(argv: list[str] | None = None) -> int:
    """Run the dataset survey and persist the records to a JSON file.

    Parameters
    ----------
    argv : list[str] | None
        CLI tokens. Zero positional bibkeys = the full ``CANDIDATES`` batch;
        one or more = dogfood just those keys. ``--out PATH`` selects the output
        file (default ``experiments/eda/survey_summary.json``), enabling
        collision-free parallel per-dataset runs (one ``--out`` each).

    Returns
    -------
    int
        Process exit code (``0`` on success).

    Raises
    ------
    ValueError
        If ``--out`` points at an existing directory rather than a file path.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Phase-2 broad dataset survey.")
    parser.add_argument("bibkeys", nargs="*", help="bibkeys to survey (default: all CANDIDATES)")
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        default=OUT / "survey_summary.json",
        help="output JSON path (default: experiments/eda/survey_summary.json)",
    )
    args = parser.parse_args(argv)

    out_path: pathlib.Path = args.out
    if out_path.exists() and out_path.is_dir():
        raise ValueError(f"--out must be a file path, not a directory: {out_path}")

    targets = (
        {k: CANDIDATES[k] for k in args.bibkeys if k in CANDIDATES}
        if args.bibkeys
        else dict(CANDIDATES)
    )

    records = []
    if targets:  # only pay the tokenizer/model load when there is work to do
        from transformers import AutoTokenizer

        hf_tok = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
        tok = lambda s: hf_tok(s, truncation=False, add_special_tokens=True)["input_ids"]
        for bibkey, hf_id in targets.items():
            print(f"--- {bibkey} ({hf_id}) ---", flush=True)
            r = survey_one(bibkey, hf_id, tok)
            print(
                f"    {r.get('status')}  rows={r.get('measured_rows')}  "
                f"text={r.get('mapped_text_col')} label={r.get('mapped_label_col')} "
                f"({r.get('label_semantics', '')})",
                flush=True,
            )
            records.append(r)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(records, indent=2))
    print(f"wrote {len(records)} record(s) -> {out_path}", file=sys.stderr)

    audited = [r for r in records if r.get("status") == "AUDITED"]
    print(f"\n=== {len(audited)}/{len(records)} AUDITED ===")
    for r in records:
        if r.get("status") != "AUDITED":
            print(f"  {r['status']:20} {r['bibkey']}  {r.get('note', '') or r.get('error', '')[:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
