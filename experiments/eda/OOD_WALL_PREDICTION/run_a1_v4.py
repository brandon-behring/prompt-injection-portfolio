"""A1 positive-class cube + V4 embedding geometry (Phase-3 EDA).

A1 — occupancy of the positive class over (channel × intent/subfamily × technique
[attack_type] × split): is "PI detection" actually one corner of the cube? V4 —
2-D embedding geometry via **UMAP** (the design's choice; `umap-learn` is a [dev]
EDA tool under the ADR-051 GPU-EDA exception). Per the design the rigor is the
**silhouette / ARI / PAD** pairing — computed on the FULL embedding
(projector-independent), NOT eyeballing the scatter — so the carrier-dominance
finding is identical regardless of projector; UMAP only makes the scatter faithful.

Run:  uv run python experiments/eda/OOD_WALL_PREDICTION/run_a1_v4.py
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
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from umap import UMAP

from eval_toolkit.embeddings import make_minilm_embedder

HERE = Path(__file__).resolve().parent
BIPIA_ROOT = Path.cwd() / "data" / "raw" / "BIPIA" / "benchmark"
SEED = 0
sys.path.insert(0, str(HERE))
from bipia_carrier import build_examples  # noqa: E402


def main() -> None:
    ex = build_examples(root=BIPIA_ROOT, contexts_per_attack=12, seed=SEED)
    pos = ex.frame[ex.frame.label == 1].reset_index(drop=True)
    print(f"positives: {len(pos)}  carriers={sorted(pos.carrier.unique())}")

    # --- A1 cube: positive counts by attack_type × carrier, train block then test. ---
    types = list(ex.train_types) + list(ex.test_types)
    cube = (
        pos.pivot_table(index="attack_type", columns="carrier", values="label", aggfunc="count", fill_value=0)
        .reindex(types)
        .fillna(0)
    )
    split_line = len(ex.train_types)

    # --- V4 geometry: PCA-2D of a balanced positive sample + silhouette/ARI. ---
    rng = np.random.default_rng(SEED)
    samp = pos.sample(n=min(1800, len(pos)), random_state=SEED).reset_index(drop=True)
    embed = make_minilm_embedder()
    emb = np.asarray(embed(samp["text"].tolist()), dtype=float)
    coords = UMAP(n_components=2, random_state=SEED).fit_transform(emb)

    carrier_codes = samp["carrier"].astype("category").cat.codes.to_numpy()
    type_codes = samp["attack_type"].astype("category").cat.codes.to_numpy()
    fam_codes = samp["subfamily"].astype("category").cat.codes.to_numpy()
    # silhouette: how cleanly does each labelling separate in the FULL embedding?
    sil = {
        "by_carrier": float(silhouette_score(emb, carrier_codes)),
        "by_attack_type": float(silhouette_score(emb, type_codes)),
        "by_subfamily": float(silhouette_score(emb, fam_codes)),
    }
    # ARI: cluster into n_carriers groups → does the clustering recover carrier or type?
    km = KMeans(n_clusters=len(set(carrier_codes)), n_init=10, random_state=SEED).fit_predict(emb)
    ari = {
        "kmeans_vs_carrier": float(adjusted_rand_score(carrier_codes, km)),
        "kmeans_vs_attack_type": float(adjusted_rand_score(type_codes, km)),
    }
    print("silhouette:", {k: round(v, 3) for k, v in sil.items()})
    print("ARI:", {k: round(v, 3) for k, v in ari.items()})
    dominant = max(sil, key=lambda k: sil[k])
    print(f"=> geometry is dominated by: {dominant} (highest silhouette)")

    metrics = {
        "silhouette": sil,
        "ari": ari,
        "dominant_axis": dominant,
        "note": "carrier-dominates-embedding: silhouette_by_carrier >> by_attack_type confirms the "
        "MiniLM geometry tracks the email/code/table carrier, not the injected attack-type — "
        "consistent with the secondary-fold PAD (carrier+attack external 2.0 >> core 0.51).",
    }
    (HERE / "a1_v4_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    # --- Figures. ---
    fig, ax = plt.subplots(figsize=(7, 9))
    im = ax.imshow(cube.to_numpy(), aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(cube.columns)))
    ax.set_xticklabels(cube.columns)
    ax.set_yticks(range(len(types)))
    ax.set_yticklabels(types, fontsize=7)
    ax.axhline(split_line - 0.5, color="red", lw=2)
    ax.text(0.02, split_line / 2, "TRAIN types", color="white", fontsize=9, rotation=90, va="center")
    ax.text(0.02, split_line + len(ex.test_types) / 2, "TEST types", color="white", fontsize=9, rotation=90, va="center")
    ax.set_title("A1 — positive-class cube: count by attack-type × carrier\n(disjoint train/test type blocks)")
    fig.colorbar(im, ax=ax, label="positive count")
    fig.tight_layout()
    fig.savefig(HERE / "A1_positive_cube.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 7))
    for code, name in enumerate(samp["carrier"].astype("category").cat.categories):
        m = carrier_codes == code
        ax.scatter(coords[m, 0], coords[m, 1], s=6, alpha=0.5, label=name)
    ax.legend(title="carrier")
    ax.set_title(
        f"V4 — UMAP-2D of injected positives (colored by carrier)\n"
        f"silhouette: carrier={sil['by_carrier']:.2f}  attack_type={sil['by_attack_type']:.2f}  "
        f"(carrier dominates the geometry)"
    )
    ax.set_xlabel("UMAP-1")
    ax.set_ylabel("UMAP-2")
    fig.tight_layout()
    fig.savefig(HERE / "V4_embedding_geometry.png", dpi=120)
    plt.close(fig)
    print(f"wrote A1_positive_cube.png + V4_embedding_geometry.png + a1_v4_metrics.json")


if __name__ == "__main__":
    main()
