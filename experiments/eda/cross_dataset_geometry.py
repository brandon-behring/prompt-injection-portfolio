"""E2 cross-dataset embedding geometry + E4 cross-dataset leakage matrix.

The restored *explore-first* EDA (see `docs/planning/dataset-utilization-and-eda-plan-2026-06.md`):
the cross-family analog of `OOD_WALL_PREDICTION/run_a1_v4.py`, which measured the embedding geometry
*within BIPIA carriers*. Here the grouping variable is the **dataset / family** — i.e. the pre-modeling
geometry of the **cross-family wall** that ADR-052 pivoted away from before it was ever characterized.

For every acquirable dataset (verified loaders in `configs/data/dataset_specs.yml`, plus on-disk BIPIA
and the now-ungated WildGuardMix), we embed a balanced sample with the same MiniLM embedder used by the
BIPIA EDA, then measure:

* **silhouette** by dataset / family / coarse(direct·indirect·benign) — does the embedding cluster by
  *source*?
* **ARI** of KMeans(n=families) vs the family and dataset labels — does unsupervised clustering recover
  source family?
* a pairwise **PAD** (proxy-A-distance) matrix — how separable is each dataset *pair* (PAD≈2 ⇒ trivially
  separable ⇒ a real cross-family gap); the off-diagonal mean is the headline "how high is the wall".
* a light TF-IDF **cross-dataset near-duplicate** scan (**E4 leakage**) — flags train↔test contamination
  (e.g. the known InjecGuard⊃BIPIA bundling, or shared upstream components).

Run (local, free, CPU):
    uv run python experiments/eda/cross_dataset_geometry.py --out experiments/eda/CROSS_DATASET \\
        --per-dataset 250
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import yaml
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

REPO = Path.cwd()
SPECS_PATH = REPO / "configs" / "data" / "dataset_specs.yml"
BIPIA_ROOT = REPO / "data" / "raw" / "BIPIA" / "benchmark"
SEED = 0

# dataset bibkey / handle -> (short name, family). Families per the atlas
# (docs/planning/dataset-utilization-and-eda-plan-2026-06.md). "coarse" axis groups the
# user-turn families together so the headline contrast is indirect (BIPIA) vs the direct cloud vs benign.
FAMILY: dict[str, tuple[str, str]] = {
    "deepset2023promptinjections": ("deepset", "direct"),
    "jackhhao2023jailbreakclassification": ("jackhhao", "jailbreak"),
    "xtram12024safeguardpromptinjection": ("xtram1", "direct"),
    "jayavibhav2024promptinjection": ("jayavibhav", "direct"),
    "hendzh2025promptshield": ("promptshield", "direct"),
    "guychuk2024benignmalicious": ("guychuk", "direct"),
    "lin2023toxicchat": ("toxicchat", "toxicity"),
    "reshabhs2024spmlchatbotpromptinjection": ("spml", "direct"),
    "shen2023inthewild": ("shen_dan", "jailbreak"),
    "leolee2024notinject": ("notinject", "over_defense"),
    "rottger2024xstest": ("xstest", "over_defense"),
    "cui2024orbench": ("orbench", "over_defense"),
    "gentellab2024gentelbench": ("gentelbench", "aggregated"),
    # Phase-2 expansion (2026-06-03). PROVISIONAL families (D4) — re-examined vs where each set
    # actually lands (silhouette / nearest-family) after this run. neuralchemy wasn't in the Q4 four;
    # it is a multi-source binary injection set → 'aggregated' (confirm vs 'direct' in the re-exam).
    "nvidia2025aegis2": ("aegis2", "toxicity"),
    "amazonscience2025falsereject": ("falsereject", "over_defense"),
    "youbin2025jailbreakdb": ("jailbreakdb", "jailbreak"),
    "perplexityai2025browsesafe": ("browsesafe", "indirect_html"),
    "neuralchemy2026promptinjection": ("neuralchemy", "aggregated"),
}
COARSE = {  # family -> coarse axis label
    "direct": "direct_family",
    "jailbreak": "direct_family",
    "toxicity": "direct_family",
    "aggregated": "direct_family",
    "indirect": "indirect",
    "indirect_html": "indirect",  # browsesafe — a 2nd indirect dialect (cf. E7 "BIPIA is one dialect")
    "indirect_rag": "indirect",   # fujitsu B1 — RAG-document poisoning dialect
    "indirect_tool": "indirect",  # injecagent — tool-output dialect
    "over_defense": "benign_control",
}


def _sample_texts(texts: list[str], n: int, seed: int) -> list[str]:
    """Deterministically down-sample a text list to <= n non-empty entries."""
    clean = [t for t in (str(x).strip() for x in texts) if t]
    if len(clean) <= n:
        return clean
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(clean), size=n, replace=False)
    return [clean[i] for i in idx]


def _strip_html(text: str) -> str:
    """Strip HTML tags + collapse whitespace → a visible-text proxy for the E4 leakage near-dup (D3).

    The raw HTML is kept for the E2 carrier geometry (the markup IS the carrier signal); only the
    cross-dataset near-dup uses this stripped form, so shared ``<html>``/``<head>`` boilerplate cannot
    manufacture (or mask) cross-corpus duplicates. Regex-based — no bs4 dependency.
    """
    import html as _html
    import re

    no_tags = re.sub(r"<[^>]+>", " ", str(text))
    return re.sub(r"\s+", " ", _html.unescape(no_tags)).strip()


def _load_spec_texts(spec: dict, n: int) -> list[str]:
    """Load up to ~3n raw texts for a verified spec, reusing the survey_v2 loader logic.

    Mirrors `survey_v2.audit_one`: benign controls load raw + a single feature column; binary /
    positive-pool roles go through the eval_toolkit loaders. Raises on any load failure (no silent
    empties — the caller records the skip).
    """
    role = spec["role"]
    if role == "benign_control":
        from datasets import load_dataset

        args = [spec["config"]] if spec.get("config") else []
        dd = load_dataset(spec["hf_id"], *args, revision=spec.get("revision"))
        fc = spec.get("feature_col", "prompt")
        texts: list[str] = []
        for split in dd:
            texts.extend(dd[split].to_pandas()[fc].astype(str).tolist())
            if len(texts) >= 3 * n:
                break
        return texts

    if spec.get("load_method") == "custom_parquet":
        from eval_toolkit.loaders import DataFrameLoader

        renames = spec.get("column_renames", {})
        rev = spec.get("revision")
        frames = []
        for f in spec["parquet_files"]:
            url = f"https://huggingface.co/datasets/{spec['hf_id']}/resolve/{rev or 'main'}/{f}"
            frames.append(pd.read_parquet(url).rename(columns=renames))
        df = pd.concat(frames, ignore_index=True)
        return df[spec["feature_col"]].astype(str).tolist()

    if spec.get("load_method") == "custom_csv":
        import pathlib as _pl

        feat = spec["feature_col"]
        approx = max(int(spec.get("approx_rows", 3 * n)), 1)
        prob = min(1.0, (3 * n) / approx)  # uniform Bernoulli sample → ~3n texts across the full stream
        local = _pl.Path("data/raw") / spec.get("local_dir", "")
        texts: list[str] = []
        for f in spec["csv_files"]:
            path = local / f
            src = (
                str(path)
                if path.exists()
                else f"https://huggingface.co/datasets/{spec['hf_id']}/resolve/{spec.get('revision') or 'main'}/{f}"
            )
            for chunk in pd.read_csv(src, usecols=[feat], chunksize=200_000):
                col = chunk[feat].dropna().astype(str)
                texts.extend((col.sample(frac=prob, random_state=SEED) if prob < 1.0 else col).tolist())
        return texts

    from eval_toolkit.loaders import HFDatasetsLoader

    kw: dict = dict(
        repo_id=spec["hf_id"], revision=spec.get("revision"), config_name=spec.get("config")
    )
    if spec.get("feature_cols"):
        kw.update(feature_cols=spec["feature_cols"], feature_join=spec.get("feature_join", "\n\n"))
    else:
        kw.update(feature_col=spec.get("feature_col", "text"))
    # label_col/label_map are required by the loader even though geometry only needs text
    # (it validates the label column on load) — pass them so non-default-label specs don't skip.
    kw["label_col"] = spec.get("label_col", "label")
    if spec.get("label_map"):
        kw["label_map"] = spec["label_map"]
    loader = HFDatasetsLoader(**{k: v for k, v in kw.items() if v is not None})
    texts = []
    for _split, sl in loader.load_splits().items():
        texts.extend(sl.df[sl.feature_col].astype(str).tolist())
    return texts


def _load_wildguard(n: int) -> list[str]:
    """WildGuardMix prompts (gate now accepted by the user)."""
    from datasets import load_dataset

    dd = load_dataset("allenai/wildguardmix", "wildguardtrain")
    return dd["train"].to_pandas()["prompt"].astype(str).tolist()


def _load_bipia(n: int) -> list[str]:
    """BIPIA injected positives (the indirect anchor), via the on-disk carrier loader."""
    sys.path.insert(0, str(REPO / "experiments" / "eda" / "OOD_WALL_PREDICTION"))
    from bipia_carrier import build_examples  # noqa: E402

    ex = build_examples(root=BIPIA_ROOT, contexts_per_attack=4, seed=SEED)
    pos = ex.frame[ex.frame.label == 1]
    return pos["text"].astype(str).tolist()


def _load_fujitsu(n: int) -> list[str]:
    """fujitsu B1 RAG-document poison_content (the indirect-RAG dialect; gate granted)."""
    from datasets import load_dataset

    ds = load_dataset("Fujitsu/agentic-rag-redteam-bench", "B1_rag_text_poisoning", split="train")
    return [t for t in ds["poison_content"] if t and str(t).strip()]


def _load_injecagent(n: int) -> list[str]:
    """InjecAgent attacker-instruction-in-tool-response (the indirect-tool dialect), from disk."""
    df = pd.read_parquet(REPO / "data" / "raw" / "injecagent" / "injecagent_derived.parquet")
    return df["text"].dropna().astype(str).tolist()


def collect(per_dataset: int) -> pd.DataFrame:
    """Build the (text, dataset, family, coarse) frame across all acquirable datasets."""
    specs = yaml.safe_load(SPECS_PATH.read_text())["datasets"]
    rows: list[dict] = []
    skipped: list[str] = []

    plan: list[tuple[str, str, str]] = []  # (handle, name, family)
    for bibkey, (name, fam) in FAMILY.items():
        plan.append((bibkey, name, fam))
    specials = {"wildguardmix": ("wildguardmix", "toxicity", _load_wildguard),
                "bipia": ("bipia", "indirect", _load_bipia),
                "fujitsu": ("fujitsu", "indirect_rag", _load_fujitsu),
                "injecagent": ("injecagent", "indirect_tool", _load_injecagent)}

    for bibkey, name, fam in plan:
        spec = specs.get(bibkey)
        if spec is None:
            skipped.append(f"{name}: no spec")
            continue
        try:
            texts = _sample_texts(_load_spec_texts(spec, per_dataset), per_dataset, SEED)
            for t in texts:
                tl = _strip_html(t) if fam == "indirect_html" else t  # D3: stripped text for E4 leakage only
                rows.append({"text": t, "text_leak": tl, "dataset": name, "family": fam, "coarse": COARSE[fam]})
            print(f"  loaded {name:14s} n={len(texts):4d} family={fam}", flush=True)
        except Exception as exc:  # noqa: BLE001 — record the skip, never silently drop
            skipped.append(f"{name}: {type(exc).__name__}: {str(exc)[:100]}")
            print(f"  SKIP   {name:14s} {type(exc).__name__}: {str(exc)[:100]}", flush=True)

    for handle, (name, fam, fn) in specials.items():
        try:
            texts = _sample_texts(fn(per_dataset), per_dataset, SEED)
            for t in texts:
                tl = _strip_html(t) if fam == "indirect_html" else t  # D3: stripped text for E4 leakage only
                rows.append({"text": t, "text_leak": tl, "dataset": name, "family": fam, "coarse": COARSE[fam]})
            print(f"  loaded {name:14s} n={len(texts):4d} family={fam}", flush=True)
        except Exception as exc:  # noqa: BLE001
            skipped.append(f"{name}: {type(exc).__name__}: {str(exc)[:100]}")
            print(f"  SKIP   {name:14s} {type(exc).__name__}: {str(exc)[:100]}", flush=True)

    df = pd.DataFrame(rows)
    df.attrs["skipped"] = skipped
    return df


def pad(emb: np.ndarray, codes: np.ndarray, a: int, b: int) -> float:
    """Proxy-A-distance between two dataset groups, via ``eval_toolkit.eda.proxy_a_distance`` (Ben-David
    2010). ADR-026: consume the upstream primitive rather than a local 5-fold-LR reimplementation."""
    from eval_toolkit.eda import proxy_a_distance

    x_a, x_b = emb[codes == a], emb[codes == b]
    if len(x_a) < 5 or len(x_b) < 5:
        return float("nan")
    return float(proxy_a_distance(x_a, x_b, n_folds=5, random_state=SEED).pad)


def cross_dataset_neardup(df: pd.DataFrame) -> dict:
    """E4: cross-dataset near-duplicate pairs via ``eval_toolkit.text_dedup.audit_source_label_similarity``
    (cross-source high-similarity, default TF-IDF cosine >= 0.9). ADR-026: consume the upstream primitive
    rather than a local TF-IDF-NN reimplementation.

    Uses ``text_leak`` (HTML-stripped for the indirect_html carrier, identical to ``text`` elsewhere) so
    shared markup boilerplate can't manufacture or mask cross-corpus near-duplicates (D3). Counts pairs per
    dataset-pair (k_neighbors=20 default → more thorough than the prior k=1 row scan)."""
    from eval_toolkit.text_dedup import audit_source_label_similarity

    leak_text = df["text_leak"] if "text_leak" in df else df["text"]
    report = audit_source_label_similarity(
        leak_text.tolist(), sources=df["dataset"].tolist(), threshold=0.9,
        include_within_source=False, include_cross_source=True,
    )
    pairs: dict[str, int] = {}
    for f in report.findings:
        key = " | ".join(sorted((str(f.left_source), str(f.right_source))))
        pairs[key] = pairs.get(key, 0) + 1
    n_cross = sum(pairs.values())
    return {"cross_dataset_neardup_pairs": n_cross, "rate": round(n_cross / len(df), 4),
            "top_pairs": dict(sorted(pairs.items(), key=lambda kv: -kv[1])[:12])}


def main() -> None:
    ap = argparse.ArgumentParser(description="Cross-dataset embedding geometry (E2) + leakage (E4).")
    ap.add_argument("--out", default="experiments/eda/CROSS_DATASET")
    ap.add_argument("--per-dataset", type=int, default=250)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    print("[collect] loading acquirable datasets ...", flush=True)
    df = collect(args.per_dataset)
    if df.empty:
        raise RuntimeError("no datasets loaded — check HF auth / network")
    print(f"[collect] total rows={len(df)} datasets={df.dataset.nunique()}", flush=True)

    from eval_toolkit.embeddings import make_minilm_embedder

    print("[embed] MiniLM ...", flush=True)
    emb = np.asarray(make_minilm_embedder()(df["text"].tolist()), dtype=float)

    ds_codes = df["dataset"].astype("category").cat.codes.to_numpy()
    fam_codes = df["family"].astype("category").cat.codes.to_numpy()
    coarse_codes = df["coarse"].astype("category").cat.codes.to_numpy()
    sil = {
        "by_dataset": float(silhouette_score(emb, ds_codes)),
        "by_family": float(silhouette_score(emb, fam_codes)),
        "by_coarse": float(silhouette_score(emb, coarse_codes)),
    }
    km = KMeans(n_clusters=df["family"].nunique(), n_init=10, random_state=SEED).fit_predict(emb)
    ari = {
        "kmeans_vs_family": float(adjusted_rand_score(fam_codes, km)),
        "kmeans_vs_dataset": float(adjusted_rand_score(ds_codes, km)),
        "kmeans_vs_coarse": float(adjusted_rand_score(coarse_codes, km)),
    }

    names = list(df["dataset"].astype("category").cat.categories)
    n = len(names)
    pad_mat = np.full((n, n), np.nan)
    for i in range(n):
        for j in range(i + 1, n):
            p = pad(emb, ds_codes, i, j)
            pad_mat[i, j] = pad_mat[j, i] = p
    off = pad_mat[~np.isnan(pad_mat)]
    # BIPIA-vs-direct: the cross-family-wall slice that matters most
    bipia_pads = {}
    if "bipia" in names:
        bi = names.index("bipia")
        for j, nm in enumerate(names):
            if j != bi and not np.isnan(pad_mat[bi, j]):
                bipia_pads[nm] = round(float(pad_mat[bi, j]), 3)

    leak = cross_dataset_neardup(df)

    metrics = {
        "n_rows": int(len(df)),
        "datasets": names,
        "per_dataset_counts": df["dataset"].value_counts().to_dict(),
        "silhouette": {k: round(v, 4) for k, v in sil.items()},
        "ari": {k: round(v, 4) for k, v in ari.items()},
        "pad_offdiag_mean": round(float(off.mean()), 3) if off.size else None,
        "pad_offdiag_min": round(float(off.min()), 3) if off.size else None,
        "pad_bipia_vs_each": dict(sorted(bipia_pads.items(), key=lambda kv: kv[1])),
        "pad_matrix": {names[i]: {names[j]: (round(float(pad_mat[i, j]), 3)
                                             if not np.isnan(pad_mat[i, j]) else None)
                                  for j in range(n)} for i in range(n)},
        "leakage_E4": leak,
        "skipped": df.attrs.get("skipped", []),
        "interpretation": (
            "silhouette_by_dataset / high off-diagonal PAD ⇒ the embedding separates by SOURCE — the "
            "cross-family wall is geometrically real pre-modeling (the analog of carrier-dominance "
            "within BIPIA). pad_bipia_vs_each sizes how far indirect (BIPIA) sits from each direct "
            "source. leakage_E4 flags cross-dataset contamination for the LODO design."
        ),
    }
    (out / "cross_dataset_geometry.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    # UMAP figure (projector-independent metrics above are the rigor; UMAP just visualizes).
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from umap import UMAP

        coords = UMAP(n_components=2, random_state=SEED).fit_transform(emb)
        fig, ax = plt.subplots(figsize=(9, 7))
        for fam in sorted(df["family"].unique()):
            m = df["family"].to_numpy() == fam
            ax.scatter(coords[m, 0], coords[m, 1], s=6, alpha=0.5, label=fam)
        ax.legend(title="family")
        ax.set_title(
            f"E2 — cross-dataset MiniLM geometry (colored by family)\n"
            f"silhouette by_dataset={sil['by_dataset']:.2f} by_coarse={sil['by_coarse']:.2f}  "
            f"PAD off-diag mean={metrics['pad_offdiag_mean']}"
        )
        fig.tight_layout()
        fig.savefig(out / "cross_dataset_geometry.png", dpi=120)
        plt.close(fig)
    except Exception as exc:  # noqa: BLE001 — figure is optional; metrics already written
        print(f"[umap] skipped figure: {type(exc).__name__}: {str(exc)[:80]}", flush=True)

    print(f"[done] silhouette={metrics['silhouette']}  ari={metrics['ari']}", flush=True)
    print(f"[done] PAD off-diag mean={metrics['pad_offdiag_mean']} min={metrics['pad_offdiag_min']}", flush=True)
    print(f"[done] BIPIA-vs-each PAD={metrics['pad_bipia_vs_each']}", flush=True)
    print(f"[done] E4 leakage={leak}", flush=True)
    print(f"[done] wrote {out}/cross_dataset_geometry.json", flush=True)
    if metrics["skipped"]:
        print(f"[done] skipped: {metrics['skipped']}", flush=True)


if __name__ == "__main__":
    main()
