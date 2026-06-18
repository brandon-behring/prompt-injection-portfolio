#!/usr/bin/env python3
"""Phase 2 survey, v2 — heuristic-robust. Consumes the VERIFIED specs in
configs/data/dataset_specs.yml (no column guessing) and audits each via the
extended eval_toolkit.loaders.HFDatasetsLoader (feature_cols/label_map/revision)
or a documented custom adapter. Every verdict traces to a verified spec.

Run: uv run --no-project python experiments/eda/survey_v2.py [bibkey ...]
"""
from __future__ import annotations
import json, sys, pathlib, warnings
warnings.filterwarnings("ignore")
import pandas as pd
import yaml

OUT = pathlib.Path("experiments/eda")
SPECS = yaml.safe_load(pathlib.Path("configs/data/dataset_specs.yml").read_text())["datasets"]
AUDIT_ROLES = {"binary_detection", "positive_pool", "benign_control"}
CAP = 15_000  # rows above this are seeded-sampled before the O(n^2) near-dup/leakage checks


def custom_parquet_loader(spec):
    """gentellab-style: read per-file parquets, harmonize columns, concat -> DataFrameLoader."""
    from eval_toolkit.loaders import DataFrameLoader
    hid, rev = spec["hf_id"], spec.get("revision")
    renames = spec.get("column_renames", {})
    frames = []
    for f in spec["parquet_files"]:
        url = f"https://huggingface.co/datasets/{hid}/resolve/{rev or 'main'}/{f}"
        df = pd.read_parquet(url).rename(columns=renames)
        df["__split__"] = "train"
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    return DataFrameLoader(df, split_col="__split__", feature_col=spec["feature_col"],
                           label_col=spec["label_col"], name=spec["hf_id"]), len(df)


def custom_csv_loader(spec):
    """JailbreakDB-style: read raw CSV(s) the HF Viewer can't serve, from the local materialized
    snapshot (falls back to the HF resolve URL), memory-bounded via per-chunk Bernoulli sampling to
    ``sample_rows`` (the full corpus is scanned only by the separate leakage gate). -> DataFrameLoader."""
    import pathlib as _pl
    from eval_toolkit.loaders import DataFrameLoader
    hid, rev = spec["hf_id"], spec.get("revision")
    feat, lab = spec["feature_col"], spec["label_col"]
    cap = int(spec.get("sample_rows", 30_000))
    approx = max(int(spec.get("approx_rows", cap)), 1)
    keep = list(dict.fromkeys([feat, lab, *spec.get("keep_cols", [])]))
    local = _pl.Path("data/raw") / spec.get("local_dir", "")
    p = min(1.0, (3 * cap) / approx)  # Bernoulli keep-prob → ~3*cap rows uniformly across the full stream
    frames = []
    for f in spec["csv_files"]:
        path = local / f
        src = str(path) if path.exists() else f"https://huggingface.co/datasets/{hid}/resolve/{rev or 'main'}/{f}"
        for chunk in pd.read_csv(src, usecols=lambda c: c in keep, chunksize=200_000):
            frames.append(chunk if p >= 1.0 else chunk.sample(frac=p, random_state=42))
    df = pd.concat(frames, ignore_index=True)
    if len(df) > cap:
        df = df.sample(cap, random_state=42).reset_index(drop=True)
    df["__split__"] = "train"
    return DataFrameLoader(df, split_col="__split__", feature_col=feat, label_col=lab, name=hid), len(df)


def hf_loader(spec):
    from eval_toolkit.loaders import HFDatasetsLoader
    kw = dict(repo_id=spec["hf_id"], revision=spec.get("revision"), config_name=spec.get("config"),
              label_col=spec.get("label_col", "label"))
    if spec.get("feature_cols"):
        kw.update(feature_cols=spec["feature_cols"], feature_join=spec.get("feature_join", "\n\n"))
    else:
        kw.update(feature_col=spec.get("feature_col", "text"))
    if spec.get("label_map"):
        kw["label_map"] = spec["label_map"]
    return HFDatasetsLoader(**{k: v for k, v in kw.items() if v is not None})


def audit_one(bibkey, spec, tok):
    from eval_toolkit.eda import audit_dataset
    from eval_toolkit.loaders import DataFrameLoader
    rec = {"bibkey": bibkey, "hf_id": spec["hf_id"], "role": spec["role"], "revision": spec.get("revision")}
    is_control = spec["role"] == "benign_control"
    try:
        if is_control:
            # benign-only controls have no binary label column -> load raw, label all 0
            from datasets import load_dataset
            args = [spec["config"]] if spec.get("config") else []
            dd = load_dataset(spec["hf_id"], *args, revision=spec.get("revision"))
            fc = spec.get("feature_col", "prompt")
            frames = [pd.DataFrame({"text": dd[s].to_pandas()[fc].astype(str), "label": 0, "__sp__": s})
                      for s in dd]
        else:
            lm = spec.get("load_method")
            if lm == "custom_parquet":
                slices = custom_parquet_loader(spec)[0].load_splits()
            elif lm == "custom_csv":
                slices = custom_csv_loader(spec)[0].load_splits()
            else:
                slices = hf_loader(spec).load_splits()
            frames = []
            for s, sl in slices.items():
                d = sl.df.copy().rename(columns={sl.feature_col: "text"})
                d["label"] = d[sl.label_col]
                d["__sp__"] = s
                frames.append(d[["text", "label", "__sp__"]])
        df = pd.concat(frames, ignore_index=True)
        total = len(df)
        near = total <= CAP  # skip the expensive within-split near-dup on sampled large sets
        if total > CAP:
            df = df.sample(CAP, random_state=42).reset_index(drop=True)
            rec["sampled"] = f"{CAP}-row seeded sample of {total} (near-dup skipped; dedup/leakage partial)"
        loader = DataFrameLoader(df, split_col="__sp__", feature_col="text", label_col="label", name=bibkey)
        audit = audit_dataset(loader, tokenizer=tok, context_window=8192, obfuscation=True,
                              near=near, cross_split=True)
        d = OUT / bibkey; d.mkdir(parents=True, exist_ok=True)
        audit.write(d / "audit.json")
        rec.update(status="AUDITED", rows=total, gate_passed=bool(audit.gate_passed),
                   gate_summary=audit.gate_summary,
                   splits={s: {"n": ss.n_rows, "pos": ss.n_positive, "neg": ss.n_negative,
                               "tok_p95": (ss.token_lengths or {}).get("p95"),
                               "pct_over_8192": ss.pct_over_context_window,
                               "obf_invisible": round(ss.obfuscation.invisible_char_rate, 4) if ss.obfuscation else None}
                          for s, ss in audit.split_summaries.items()},
                   failed_gates=[g.name for g in audit.gates if not g.passed])
    except Exception as e:
        rec.update(status="AUDIT-ERROR", error=str(e)[:240])
    return rec


def main(argv):
    from transformers import AutoTokenizer
    hf_tok = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
    tok = lambda s: hf_tok(s, truncation=False, add_special_tokens=True)["input_ids"]
    keys = [k for k in argv if k in SPECS] if argv else list(SPECS)
    records = []
    for bibkey in keys:
        spec = SPECS[bibkey]
        if spec["role"] not in AUDIT_ROLES:
            records.append({"bibkey": bibkey, "hf_id": spec["hf_id"], "role": spec["role"],
                            "status": "NOT-AUDITED", "reason": spec["role"], "evidence": spec.get("evidence")})
            print(f"--- {bibkey}: {spec['role']} (not audited) ---", flush=True)
            continue
        print(f"--- {bibkey} ({spec['hf_id']}) [{spec['role']}] ---", flush=True)
        r = audit_one(bibkey, spec, tok)
        print(f"    {r.get('status')}  gate={'PASS' if r.get('gate_passed') else r.get('failed_gates', r.get('error',''))}", flush=True)
        records.append(r)
    (OUT / "survey_v2_summary.json").write_text(json.dumps(records, indent=2))
    aud = [r for r in records if r.get("status") == "AUDITED"]
    print(f"\n=== {len(aud)} audited; {len([r for r in records if r['role'] in AUDIT_ROLES])} audit-role specs ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
