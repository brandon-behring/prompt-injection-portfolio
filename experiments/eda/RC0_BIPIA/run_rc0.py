#!/usr/bin/env python3
"""RC0 — measure BIPIA attack-type-split adequacy against the PRE-REGISTERED criteria
(experiments/eda/RC0_BIPIA/criteria.md). Reproducible; writes results.json + figures.

Also dogfoods the merged eval_toolkit.eda layer (audit_dataset) on real data.
Run: uv run --no-project python experiments/eda/RC0_BIPIA/run_rc0.py
"""
from __future__ import annotations
import json, itertools, pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
BIPIA = pathlib.Path("data/raw/BIPIA/benchmark")
OVERLAP_TYPE = "Language Translation"  # the known cross-split overlap (criterion i)
NEAR_DUP_HARD = 0.95   # pre-registered iii PASS floor (mean within-type cosine < this)
NEAR_DUP_REF = 0.80    # MiniLM canonical dedup ref (context only; NOT the gate)


def load_text_attacks():
    train = json.loads((BIPIA / "text_attack_train.json").read_text())
    test = json.loads((BIPIA / "text_attack_test.json").read_text())
    return train, test


def mean_pairwise_cosine(vecs: np.ndarray) -> float:
    """Mean off-diagonal cosine of L2-normalized row vectors."""
    if len(vecs) < 2:
        return float("nan")
    n = vecs / (np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-12)
    sims = n @ n.T
    iu = np.triu_indices(len(n), k=1)
    return float(sims[iu].mean())


def main() -> int:
    from eval_toolkit.embeddings import make_minilm_embedder

    train, test = load_text_attacks()
    tr_types, te_types = set(train), set(test)
    overlap = sorted(tr_types & te_types)

    # criterion i — drop the overlap type from BOTH for the disjoint analysis
    tr = {k: v for k, v in train.items() if k != OVERLAP_TYPE}
    te = {k: v for k, v in test.items() if k != OVERLAP_TYPE}

    res: dict = {"dataset": "BIPIA text attacks", "source": "microsoft/BIPIA@benchmark"}

    # ---- Criterion i: disjoint split ----
    res["criterion_i_disjoint_split"] = {
        "n_train_types": len(tr_types), "n_test_types": len(te_types),
        "overlap_types": overlap, "n_overlap": len(overlap),
        "after_drop_overlap": {"n_train": len(tr), "n_test": len(te)},
        "PASS": len(overlap) <= 1 and len(tr) >= 10 and len(te) >= 10,
    }

    # ---- Criterion ii: per-type N ----
    tr_counts = {k: len(v) for k, v in tr.items()}
    te_counts = {k: len(v) for k, v in te.items()}
    allc = list(tr_counts.values()) + list(te_counts.values())
    res["criterion_ii_per_type_N"] = {
        "train_min": min(tr_counts.values()), "train_median": int(np.median(list(tr_counts.values()))),
        "test_min": min(te_counts.values()), "test_median": int(np.median(list(te_counts.values()))),
        "total_train_strings": sum(tr_counts.values()), "total_test_strings": sum(te_counts.values()),
        "PASS": int(np.median(allc)) >= 5 and min(allc) >= 3,
    }

    # ---- Embeddings (MiniLM, GPU) ----
    embed = make_minilm_embedder(device="cuda")
    tr_vecs = {k: embed(v) for k, v in tr.items()}
    te_vecs = {k: embed(v) for k, v in te.items()}

    # ---- Criterion iii: within-type diversity ----
    per_type = {}
    for split, vecs in (("train", tr_vecs), ("test", te_vecs)):
        for k, v in vecs.items():
            per_type[f"{split}:{k}"] = round(mean_pairwise_cosine(v), 4)
    finite = [c for c in per_type.values() if not np.isnan(c)]
    agg_mean = float(np.mean(finite))
    flagged_hard = {k: c for k, c in per_type.items() if c >= NEAR_DUP_HARD}
    flagged_ref = {k: c for k, c in per_type.items() if c >= NEAR_DUP_REF}
    res["criterion_iii_within_type_diversity"] = {
        "metric": "mean pairwise within-type MiniLM cosine",
        "aggregate_mean": round(agg_mean, 4),
        "per_type": per_type,
        "hard_threshold_0.95": {"n_flagged": len(flagged_hard), "flagged": flagged_hard},
        "ref_threshold_0.80_context_only": {"n_at_or_above": len(flagged_ref)},
        "PASS": agg_mean < NEAR_DUP_HARD and len(flagged_hard) == 0,
    }

    # ---- Criterion iv: train-vs-test population separation (descriptive) ----
    tr_all = np.vstack(list(tr_vecs.values())); te_all = np.vstack(list(te_vecs.values()))
    c_tr = tr_all.mean(0); c_te = te_all.mean(0)
    centroid_cos = float((c_tr @ c_te) / (np.linalg.norm(c_tr) * np.linalg.norm(c_te) + 1e-12))
    res["criterion_iv_train_test_separation"] = {
        "centroid_cosine": round(centroid_cos, 4),
        "note": "descriptive (split is by type); near-1.0 would be a red flag",
    }

    # ---- Criterion v: benign-FPR control (NotInject) loads + auditable ----
    from datasets import load_dataset
    from eval_toolkit.eda import audit_dataset
    from eval_toolkit.loaders import DataFrameLoader
    import pandas as pd
    crit_v = {"dataset": "leolee99/NotInject"}
    try:
        ni = load_dataset("leolee99/NotInject")
        split0 = list(ni.keys())[0]
        df = ni[split0].to_pandas()
        crit_v.update({"loaded": True, "split": split0, "rows": len(df), "columns": list(df.columns)})
        crit_v["PASS"] = len(df) >= 1
    except Exception as e:
        crit_v.update({"loaded": False, "error": str(e)[:200], "PASS": False})
    res["criterion_v_benign_control"] = crit_v

    # ---- Dogfood: audit_dataset on BIPIA attacks (text, label=1, strata=type, split) ----
    rows = ([{"text": s, "label": 1, "attack_type": k, "split": "train"} for k, v in tr.items() for s in v]
            + [{"text": s, "label": 1, "attack_type": k, "split": "test"} for k, v in te.items() for s in v])
    bdf = __import__("pandas").DataFrame(rows)
    loader = DataFrameLoader(bdf, split_col="split", feature_col="text", label_col="label",
                             strata_col="attack_type", name="BIPIA-text-attacks")
    try:
        # single positive class is expected (all attacks) -> class_balance gate will flag; that's fine for a dogfood
        audit = audit_dataset(loader, obfuscation=True, near=True, cross_split=True)
        res["eda_layer_dogfood"] = {
            "gate_summary": audit.gate_summary,
            "splits": {s: {"n_rows": ss.n_rows, "char_p95": ss.char_lengths.get("p95"),
                            "obfuscation_invisible_rate": (ss.obfuscation.invisible_char_rate if ss.obfuscation else None)}
                       for s, ss in audit.split_summaries.items()},
            "cross_split_attack_string_leakage": "no train/test attack-string overlap" if "cross_split" not in audit.leakage_reports or not audit.leakage_reports["cross_split"].has_errors() else "LEAK",
        }
    except Exception as e:
        res["eda_layer_dogfood"] = {"error": str(e)[:300]}

    # ---- Verdict ----
    gates = {"i": res["criterion_i_disjoint_split"]["PASS"],
             "ii": res["criterion_ii_per_type_N"]["PASS"],
             "iii": res["criterion_iii_within_type_diversity"]["PASS"],
             "v": res["criterion_v_benign_control"]["PASS"]}
    res["VERDICT"] = {"gates": gates, "GO": all(gates.values()),
                      "rule": "GO iff i & ii & iii & v all PASS (iv descriptive)"}

    (HERE / "results.json").write_text(json.dumps(res, indent=2))

    # ---- Figure: per-type within-type diversity ----
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        items = sorted(per_type.items(), key=lambda kv: kv[1])
        labels = [k for k, _ in items]; vals = [v for _, v in items]
        fig, ax = plt.subplots(figsize=(8, 9))
        colors = ["#c0392b" if v >= NEAR_DUP_HARD else ("#e67e22" if v >= NEAR_DUP_REF else "#27ae60") for v in vals]
        ax.barh(range(len(labels)), vals, color=colors)
        ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels, fontsize=7)
        ax.axvline(NEAR_DUP_HARD, color="#c0392b", ls="--", lw=1, label="0.95 hard floor (memorization)")
        ax.axvline(NEAR_DUP_REF, color="#e67e22", ls=":", lw=1, label="0.80 MiniLM dedup ref")
        ax.set_xlabel("mean pairwise within-type cosine (lower = more diverse)")
        ax.set_title("BIPIA RC0 — within-type semantic diversity (criterion iii)")
        ax.legend(fontsize=7, loc="lower right"); fig.tight_layout()
        fig.savefig(HERE / "within_type_diversity.png", dpi=120)
    except Exception as e:
        print("figure error:", e)

    print(json.dumps(res["VERDICT"], indent=2))
    print(f"aggregate within-type cosine={agg_mean:.3f}  centroid_cos={centroid_cos:.3f}")
    print(f"per-type ≥0.95(hard)={len(flagged_hard)}  ≥0.80(ref)={len(flagged_ref)}/{len(per_type)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
