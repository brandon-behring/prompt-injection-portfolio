"""Cross-dataset contamination + shift AUDIT matrix (D2/D3 — descriptive only).

Per the Q2 decision, this is the **audit artifact**, NOT the OOD-wall prediction
(that is BIPIA-internal). It profiles the certified Phase-2 working set:
- **D2 contamination** — does BIPIA (the study anchor) share near-duplicate
  examples with the other datasets? (cross-dataset TF-IDF cosine >= 0.90).
- **Shift landscape** — pairwise proxy-A-distance between dataset positives, with
  the **within-dataset random-split PAD floor** (should be ~0) as a sanity check.

Pre-registered caveats (criteria.md): cross-dataset distance conflates covariate
with **label-semantics** shift and is largely a **dataset fingerprint** (length /
vocabulary / formatting) — it is read **ordinally**, never as a calibrated
covariate distance. The research shows datasets are near-trivially separable
(PAD ~ 2 everywhere), so the *informative* signal here is the contamination
overlap + the within-dataset floor, not the (saturated) PAD landscape.

Per-dataset loads are best-effort: a gated/missing/format-broken dataset is
skipped (logged), never fatal. Samples are capped for tractability.

Run:  uv run python experiments/eda/OOD_WALL_PREDICTION/run_audit_matrix.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from eval_toolkit.eda import proxy_a_distance
from eval_toolkit.embeddings import make_minilm_embedder

HERE = Path(__file__).resolve().parent
ROOT = Path.cwd()
BIPIA_ROOT = ROOT / "data" / "raw" / "BIPIA" / "benchmark"
SEED = 0
CAP = 250  # positive-text samples per dataset
NEAR_DUP_THRESHOLD = 0.90
sys.path.insert(0, str(HERE))
from bipia_carrier import build_examples  # noqa: E402


def load_positive_sample(spec: dict, rng: np.random.Generator) -> list[str] | None:
    """Best-effort: load a capped sample of a dataset's positive-class texts."""
    try:
        from datasets import load_dataset

        hf_id = spec["hf_id"]
        rev = spec.get("revision")
        ds = load_dataset(hf_id, revision=rev, split="train")
        feat = spec.get("feature_col")
        if feat is None:  # multi-column (e.g. reshabhs System+User) — join
            cols = spec["feature_cols"]
            join = spec.get("feature_join", "\n\n")
            texts_all = [join.join(str(r[c]) for c in cols) for r in ds]
        else:
            texts_all = [str(x) for x in ds[feat]]
        label_col = spec.get("label_col")
        labels_raw = list(ds[label_col])
        lmap = spec.get("label_map")
        labels = [lmap.get(v, v) if lmap else v for v in labels_raw]
        pos = [t for t, y in zip(texts_all, labels, strict=True) if int(y) == 1]
        if len(pos) < 20:
            return None
        idx = rng.choice(len(pos), size=min(CAP, len(pos)), replace=False)
        return [pos[i] for i in idx]
    except Exception as exc:  # noqa: BLE001 — best-effort cross-dataset load
        print(f"  [skip] {spec.get('hf_id','?')}: {type(exc).__name__}: {str(exc).splitlines()[0][:90]}")
        return None


def main() -> None:
    rng = np.random.default_rng(SEED)
    specs = yaml.safe_load((ROOT / "configs/data/dataset_specs.yml").read_text())["datasets"]

    pools: dict[str, list[str]] = {}
    # BIPIA anchor (positives across carriers).
    ex = build_examples(root=BIPIA_ROOT, contexts_per_attack=12, seed=SEED)
    bipia_pos = ex.frame[ex.frame.label == 1]["text"].tolist()
    pools["BIPIA"] = list(rng.choice(bipia_pos, size=min(CAP, len(bipia_pos)), replace=False))

    print("=== loading certified binary_detection datasets ===")
    for bibkey, spec in specs.items():
        if spec.get("role") != "binary_detection":
            continue
        sample = load_positive_sample(spec, rng)
        if sample is not None:
            pools[bibkey.split("20")[0]] = sample  # short label
            print(f"  loaded {bibkey}: {len(sample)} positives")
    names = list(pools)
    print(f"datasets in matrix: {names}")

    # --- Embed all pools (MiniLM). ---
    embed = make_minilm_embedder()
    emb: dict[str, np.ndarray] = {n: np.asarray(embed(pools[n]), dtype=float) for n in names}

    # --- Pairwise PAD landscape + within-dataset floor (diagonal). ---
    n = len(names)
    pad_mat = np.zeros((n, n))
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if i == j:
                half = len(emb[a]) // 2
                pad_mat[i, j] = proxy_a_distance(emb[a][:half], emb[a][half:], random_state=SEED).pad
            elif i < j:
                p = proxy_a_distance(emb[a], emb[b], random_state=SEED).pad
                pad_mat[i, j] = pad_mat[j, i] = p

    # --- D2 contamination: BIPIA near-dup overlap with each dataset (TF-IDF cosine). ---
    contamination: dict[str, float] = {}
    tfidf = TfidfVectorizer(min_df=1).fit([t for n in names for t in pools[n]])
    bipia_vec = tfidf.transform(pools["BIPIA"])
    for nm in names:
        if nm == "BIPIA":
            continue
        sims = cosine_similarity(bipia_vec, tfidf.transform(pools[nm]))
        frac = float((sims.max(axis=1) >= NEAR_DUP_THRESHOLD).mean())
        contamination[nm] = round(frac, 4)

    diag_floor = {names[i]: round(float(pad_mat[i, i]), 3) for i in range(n)}
    summary = {
        "datasets": names,
        "cap_per_dataset": CAP,
        "pad_matrix": [[round(float(x), 3) for x in row] for row in pad_mat],
        "within_dataset_pad_floor": diag_floor,
        "bipia_near_dup_contamination": contamination,
        "near_dup_threshold": NEAR_DUP_THRESHOLD,
        "caveat": "cross-dataset PAD conflates covariate + label-semantics shift and is a dataset "
        "fingerprint (length/vocab/format) — ordinal only. Informative signal = contamination "
        "overlap + the within-dataset floor (should be ~0), not the (saturated) off-diagonal PAD.",
    }
    (HERE / "audit_matrix.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # --- Heatmap. ---
    fig, ax = plt.subplots(figsize=(1.2 * n + 3, 1.0 * n + 2))
    im = ax.imshow(pad_mat, cmap="magma", vmin=0, vmax=2)
    ax.set_xticks(range(n)); ax.set_yticks(range(n))
    ax.set_xticklabels(names, rotation=90, fontsize=8); ax.set_yticklabels(names, fontsize=8)
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{pad_mat[i, j]:.1f}", ha="center", va="center",
                    color="w" if pad_mat[i, j] < 1.4 else "k", fontsize=7)
    ax.set_title("D2 audit — cross-dataset proxy-A-distance (diag = within-dataset floor)\n"
                 "ordinal only; off-diagonal ~2.0 = trivially separable (dataset fingerprint)")
    fig.colorbar(im, ax=ax, label="PAD")
    fig.tight_layout()
    fig.savefig(HERE / "D2_audit_matrix.png", dpi=120)
    plt.close(fig)

    print("\nwithin-dataset PAD floor (sanity; should be ~0):")
    for nm, v in diag_floor.items():
        print(f"  {nm:14s} {v}")
    print("\nBIPIA near-dup contamination (frac BIPIA with cosine>=0.9 to dataset):")
    for nm, v in sorted(contamination.items(), key=lambda kv: -kv[1]):
        print(f"  {nm:14s} {v}")
    print(f"\nwrote D2_audit_matrix.png + audit_matrix.json")


if __name__ == "__main__":
    main()
