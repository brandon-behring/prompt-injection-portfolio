"""Phase-3 pre-modeling OOD-wall prediction (BIPIA-internal core).

Runs the pre-registered analysis (`criteria.md`) AFTER the method was locked:
fuses E1 distribution-shift with C1/C2 shortcut-exposure into a per-test-attack-type
**collapse RANK**, and records it + its components in `results.json` (+ figures
V5, V9). The falsification test (top-k vs bottom-k permutation contrast vs the
eventual Lane-1 LODO gaps) runs later — the gaps do not exist pre-modeling.

Honors the locked knobs: MiniLM embeddings (primary) + TF-IDF PAD (alongside);
unbiased RBF MMD with a **frozen** median-heuristic bandwidth (comparable across
type-folds), B=1000 permutations; linear-CV PAD; C2 fit on a **balanced** train
pool, evaluated per test-type. Per-type MMD subsamples the train pool to a fixed
cap for tractability (the rank, not the absolute MMD, is the deliverable).

Run:  uv run python experiments/eda/OOD_WALL_PREDICTION/run_prediction.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from eval_toolkit.eda import (
    class_lexical_association,
    competency_baselines,
    knn_purity,
    maximum_mean_discrepancy,
    median_bandwidth,
    proxy_a_distance,
)
from eval_toolkit.embeddings import make_minilm_embedder

HERE = Path(__file__).resolve().parent
ROOT = Path.cwd()
BIPIA_ROOT = ROOT / "data" / "raw" / "BIPIA" / "benchmark"
SEED = 0
PER_TYPE_MMD_CAP = 200  # train-pool subsample size per per-type MMD/PAD comparison
N_PERMUTATIONS = 1000
N_BOOTSTRAP_BARS = 50  # descriptive per-type MMD CI bars for V9 (not the falsification stat)
TOP_K = 4

sys.path.insert(0, str(HERE))
from bipia_carrier import OBFUSCATION_TEST, OBFUSCATION_TRAIN, build_examples  # noqa: E402


def load_notinject_negatives(rng: np.random.Generator) -> list[str]:
    """Load NotInject benign-with-trigger prompts as hard negatives (best-effort)."""
    try:
        from datasets import load_dataset

        ds = load_dataset("leolee99/NotInject", split="NotInject_one")
        prompts = [str(p) for p in ds["prompt"]]
        rng.shuffle(prompts)
        return prompts
    except Exception as exc:  # noqa: BLE001 — optional hard-negative augmentation
        print(f"[warn] NotInject unavailable ({type(exc).__name__}): {exc}; proceeding without it")
        return []


def zscore(x: np.ndarray) -> np.ndarray:
    """Z-score; returns zeros if degenerate (zero variance)."""
    sd = x.std()
    return (x - x.mean()) / sd if sd > 0 else np.zeros_like(x)


def main() -> None:
    rng = np.random.default_rng(SEED)
    print("=== Loading BIPIA carrier examples ===")
    ex = build_examples(root=BIPIA_ROOT, contexts_per_attack=12, seed=SEED)
    df = ex.frame
    test_types = list(ex.test_types)
    print(f"train_types={len(ex.train_types)} test_types={len(test_types)} rows={len(df)}")

    # --- Negatives: clean carrier contexts (in df) + NotInject hard negatives. ---
    notinject = load_notinject_negatives(rng)
    half = len(notinject) // 2
    ni_train, ni_test = notinject[:half], notinject[half:]

    train_pos = df[(df.role == "train") & (df.label == 1)]
    train_neg_texts = (
        df[(df.role == "train") & (df.label == 0)]["text"].tolist() + ni_train
    )
    test_neg_texts = df[(df.role == "test") & (df.label == 0)]["text"].tolist() + ni_test
    print(f"train_pos={len(train_pos)} train_neg={len(train_neg_texts)} test_neg={len(test_neg_texts)}")

    # --- Embed everything once (MiniLM, GPU if available). ---
    print("=== Embedding (MiniLM all-MiniLM-L6-v2) ===")
    embed = make_minilm_embedder()
    train_pos_texts = train_pos["text"].tolist()
    train_pos_emb = np.asarray(embed(train_pos_texts), dtype=float)
    type_pos_emb: dict[str, np.ndarray] = {}
    type_pos_texts: dict[str, list[str]] = {}
    for t in test_types:
        txt = df[(df.role == "test") & (df.label == 1) & (df.attack_type == t)]["text"].tolist()
        type_pos_texts[t] = txt
        type_pos_emb[t] = np.asarray(embed(txt), dtype=float)

    # Frozen bandwidth: median heuristic on a pooled reference (train + all test pos).
    pooled_ref = np.vstack([train_pos_emb] + [type_pos_emb[t] for t in test_types])
    frozen_sigma = median_bandwidth(pooled_ref, random_state=SEED)
    print(f"frozen MMD bandwidth sigma = {frozen_sigma:.4f}")

    # --- TF-IDF features (for the alongside TF-IDF PAD). ---
    tfidf = TfidfVectorizer(min_df=2)
    tfidf.fit(train_pos_texts + train_neg_texts)
    train_pos_tfidf = tfidf.transform(train_pos_texts).toarray()

    # --- C1: log-odds of injected (pos) vs clean+NotInject (neg) on the train pool. ---
    print("=== C1 log-odds (V5) ===")
    c1_texts = train_pos_texts + train_neg_texts
    c1_labels = [1] * len(train_pos_texts) + [0] * len(train_neg_texts)
    c1 = class_lexical_association(c1_texts, c1_labels, min_count=5)
    top_pos = c1.top_a(20)
    top_neg = c1.top_b(20)

    # --- C2: balanced baseline fit on train, evaluated per test-type. ---
    print("=== C2 competency baselines per test-type ===")
    n_bal = min(len(train_pos_texts), len(train_neg_texts))
    bal_idx = rng.choice(len(train_pos_texts), size=n_bal, replace=False)
    c2_train_texts = [train_pos_texts[i] for i in bal_idx] + train_neg_texts[:n_bal]
    c2_train_labels = [1] * n_bal + [0] * n_bal

    per_type: dict[str, dict[str, float]] = {}
    for t in test_types:
        te_texts = type_pos_texts[t] + test_neg_texts
        te_labels = [1] * len(type_pos_texts[t]) + [0] * len(test_neg_texts)
        comp = competency_baselines(c2_train_texts, c2_train_labels, te_texts, te_labels)
        per_type[t] = {"competency_auprc": comp.best().average_precision,
                       "competency_baseline": comp.best().name,
                       "competency_floor": comp.test_positive_prevalence}

    # --- E1: per-type shift (embedding PAD+MMD+kNN, frozen bandwidth) + TF-IDF PAD. ---
    print("=== E1 distribution shift per test-type (V9) ===")
    for t in test_types:
        tp = type_pos_emb[t]
        cap = min(PER_TYPE_MMD_CAP, len(train_pos_emb))
        ref_idx = rng.choice(len(train_pos_emb), size=cap, replace=False)
        ref_emb = train_pos_emb[ref_idx]
        pad = proxy_a_distance(ref_emb, tp, n_bootstrap=0, random_state=SEED)
        mmd = maximum_mean_discrepancy(
            ref_emb, tp, bandwidth=frozen_sigma, n_permutations=N_PERMUTATIONS,
            n_bootstrap=N_BOOTSTRAP_BARS, random_state=SEED,
        )
        purity = knn_purity(ref_emb, tp, k=5)
        # TF-IDF PAD alongside.
        tp_tfidf = tfidf.transform(type_pos_texts[t]).toarray()
        ref_tfidf = train_pos_tfidf[ref_idx]
        pad_tfidf = proxy_a_distance(ref_tfidf, tp_tfidf, random_state=SEED)
        per_type[t].update(
            pad_emb=pad.pad, pad_emb_ci_low=pad.ci_low, pad_emb_ci_high=pad.ci_high,
            mmd_emb=mmd.mmd_squared, mmd_p=mmd.p_value,
            mmd_ci_low=mmd.ci_low, mmd_ci_high=mmd.ci_high,
            knn_purity=purity.mean_purity, pad_tfidf=pad_tfidf.pad,
        )

    # --- Fuse: weighted rank-average of E1-shift rank + C2-shortcut-failure rank. ---
    types_arr = np.array(test_types)
    shift_z = zscore(np.array([per_type[t]["pad_emb"] for t in test_types])) + zscore(
        np.array([per_type[t]["mmd_emb"] for t in test_types])
    )
    auprc = np.array([per_type[t]["competency_auprc"] for t in test_types])
    # rank 1 = most collapse: highest shift, lowest competency-transfer.
    e1_rank = (-shift_z).argsort().argsort() + 1  # 1 = most shift
    c2_rank = auprc.argsort().argsort() + 1  # 1 = lowest AUPRC (worst transfer)
    fused = (e1_rank + c2_rank) / 2.0
    # tie-break by c2_rank (the mechanism the hypothesis privileges).
    order = sorted(range(len(test_types)), key=lambda i: (fused[i], c2_rank[i]))
    for i, t in enumerate(test_types):
        per_type[t].update(
            shift_z=float(shift_z[i]), e1_rank=int(e1_rank[i]),
            c2_rank=int(c2_rank[i]), fused_rank=float(fused[i]),
        )
    predicted_order = [test_types[i] for i in order]
    top_k = predicted_order[:TOP_K]  # predicted to collapse MOST
    bottom_k = predicted_order[-TOP_K:]  # predicted to collapse LEAST

    # --- Secondary: coarse 3-fold-structure shift ordering. ---
    print("=== Secondary: 3 fold-structure shifts ===")

    def _emb(texts: list[str]) -> np.ndarray:
        return np.asarray(embed(texts), dtype=float)

    def _shift(a: np.ndarray, b: np.ndarray) -> dict[str, float]:
        ca = min(PER_TYPE_MMD_CAP, len(a))
        cb = min(PER_TYPE_MMD_CAP, len(b))
        a2 = a[rng.choice(len(a), ca, replace=False)]
        b2 = b[rng.choice(len(b), cb, replace=False)]
        p = proxy_a_distance(a2, b2, random_state=SEED)
        m = maximum_mean_discrepancy(a2, b2, bandwidth=frozen_sigma, n_permutations=N_PERMUTATIONS, random_state=SEED)
        return {"pad": p.pad, "mmd": m.mmd_squared, "mmd_p": m.p_value}

    all_test_pos = np.vstack([type_pos_emb[t] for t in test_types])
    obf_train_mask = (df.role == "train") & (df.label == 1) & (df.attack_type.isin(OBFUSCATION_TRAIN))
    obf_test_mask = (df.role == "test") & (df.label == 1) & (df.attack_type.isin(OBFUSCATION_TEST))
    obf_train_emb = _emb(df[obf_train_mask]["text"].tolist())
    obf_test_emb = _emb(df[obf_test_mask]["text"].tolist())
    # carrier+attack external: train {code,table} train-pos vs test {email} test-pos.
    ext_tr = df[(df.role == "train") & (df.label == 1) & (df.carrier.isin(["code", "table"]))]
    ext_te = df[(df.role == "test") & (df.label == 1) & (df.carrier == "email")]
    fold_structures = {
        "core_attack_type": _shift(train_pos_emb, all_test_pos),
        "obfuscation_technique": _shift(obf_train_emb, obf_test_emb),
        "carrier_plus_attack_external": _shift(_emb(ext_tr["text"].tolist()), _emb(ext_te["text"].tolist())),
    }
    fold_order = sorted(fold_structures, key=lambda k: fold_structures[k]["pad"], reverse=True)

    # --- Persist results.json (predicted ranking, pre-modeling). ---
    results = {
        "pre_registration": "experiments/eda/OOD_WALL_PREDICTION/criteria.md",
        "recorded": "pre-modeling (Lane-1 LODO gaps do not yet exist)",
        "fold_set": "14 per-test-attack-type, carrier-pooled (email/code/table)",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "frozen_mmd_bandwidth": float(frozen_sigma),
        "n_permutations": N_PERMUTATIONS,
        "per_type_mmd_cap": PER_TYPE_MMD_CAP,
        "fusion_rule": "weighted rank-average(E1 shift-rank, C2 shortcut-failure-rank); tie-break C2",
        "predicted_collapse_order": predicted_order,
        "top_k_predicted_worst": top_k,
        "bottom_k_predicted_best": bottom_k,
        "k": TOP_K,
        "per_type": per_type,
        "secondary_fold_structures": fold_structures,
        "secondary_fold_collapse_order": fold_order,
        "c1_top_positive_tokens": top_pos,
        "c1_top_negative_tokens": top_neg,
        "falsification": "top-k vs bottom-k one-sided permutation contrast on the eventual "
        "per-test-type diagnostic LODO AUPRC drops; dual rule p<0.05 AND bootstrap-CI>0 "
        "(run at verification time, not now).",
    }
    out = HERE / "results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nwrote {out}")
    print("PREDICTED collapse order (most→least):")
    for i, t in enumerate(predicted_order, 1):
        pt = per_type[t]
        print(f"  {i:2d}. {t:32s} shift_z={pt['shift_z']:+.2f} pad={pt['pad_emb']:.2f} "
              f"comp_auprc={pt['competency_auprc']:.3f}")
    print(f"\ntop-{TOP_K} predicted-worst: {top_k}")
    print(f"bottom-{TOP_K} predicted-best: {bottom_k}")
    print(f"fold-structure collapse order (by PAD): {fold_order}")

    _make_figures(per_type, test_types, top_pos, top_neg)


def _make_figures(
    per_type: dict[str, dict[str, float]],
    test_types: list[str],
    top_pos: list,
    top_neg: list,
) -> None:
    """V5 (log-odds + competency floor) + V9 (per-type PAD/MMD)."""
    # V5: top log-odds tokens (positive vs negative) + per-type competency AUPRC.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    toks = [t for t, _ in top_pos[:12]][::-1] + [t for t, _ in top_neg[:12]]
    zs = [z for _, z in top_pos[:12]][::-1] + [z for _, z in top_neg[:12]]
    colors = ["#c44"] * 12 + ["#48c"] * 12
    ax1.barh(range(len(toks)), zs, color=colors)
    ax1.set_yticks(range(len(toks)))
    ax1.set_yticklabels(toks, fontsize=7)
    ax1.set_title("V5 — C1 log-odds z (red=injected-leaning, blue=clean)")
    ax1.axvline(0, color="k", lw=0.5)
    order = sorted(test_types, key=lambda t: per_type[t]["competency_auprc"])
    ax2.barh(range(len(order)), [per_type[t]["competency_auprc"] for t in order], color="#7a3")
    ax2.set_yticks(range(len(order)))
    ax2.set_yticklabels(order, fontsize=7)
    ax2.set_xlabel("best competency-baseline AUPRC (C2 shortcut transfer)")
    ax2.set_title("V5 — C2 per-test-type shortcut floor (low = worse transfer)")
    fig.tight_layout()
    fig.savefig(HERE / "V5_lexical_association.png", dpi=120)
    plt.close(fig)

    # V9: per-type PAD + MMD bars with CI whiskers.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    order = sorted(test_types, key=lambda t: per_type[t]["pad_emb"], reverse=True)
    pads = [per_type[t]["pad_emb"] for t in order]
    pad_lo = [per_type[t]["pad_emb"] - (per_type[t]["pad_emb_ci_low"] or per_type[t]["pad_emb"]) for t in order]
    pad_hi = [(per_type[t]["pad_emb_ci_high"] or per_type[t]["pad_emb"]) - per_type[t]["pad_emb"] for t in order]
    ax1.barh(range(len(order)), pads, xerr=[pad_lo, pad_hi], color="#c66", capsize=2)
    ax1.set_yticks(range(len(order)))
    ax1.set_yticklabels(order, fontsize=7)
    ax1.set_xlabel("proxy-A-distance (embedding)")
    ax1.set_title("V9 — E1 per-test-type PAD (train-pos vs type-pos)")
    mmds = [per_type[t]["mmd_emb"] for t in order]
    ax2.barh(range(len(order)), mmds, color="#66c")
    ax2.set_yticks(range(len(order)))
    ax2.set_yticklabels(order, fontsize=7)
    ax2.set_xlabel("unbiased MMD² (embedding, frozen bandwidth)")
    ax2.set_title("V9 — E1 per-test-type MMD")
    fig.tight_layout()
    fig.savefig(HERE / "V9_distribution_shift.png", dpi=120)
    plt.close(fig)
    print(f"wrote {HERE / 'V5_lexical_association.png'} + {HERE / 'V9_distribution_shift.png'}")


if __name__ == "__main__":
    main()
