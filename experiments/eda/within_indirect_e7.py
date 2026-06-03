"""E7 within-indirect embedding geometry: is BIPIA representative of the indirect family?

The main E2 run (``cross_dataset_geometry.py``) found that BIPIA — an *indirect*-injection corpus —
sits PAD 1.86–2.0 from every *direct* source, i.e. the cross-family wall is geometrically real
pre-modeling. That used BIPIA as the *single* indirect anchor. E7 asks a follow-up: is BIPIA
*representative of the indirect-injection family*, or just one indirect "dialect"?

We answer by measuring the MiniLM embedding geometry among **three** indirect-attack corpora —
**BIPIA**, **LLMail-Inject** (``microsoft/llmail-inject-challenge``), and **WAInjectBench** (text
modality, malicious rows) — using the *same* PAD / silhouette machinery and the *same* MiniLM
embedder as the main run, so the numbers are directly comparable to that ~1.9 indirect↔direct
baseline.

* If indirect↔indirect PAD is much LOWER than ~1.9 ⇒ the indirect corpora cluster together (apart
  from the direct cloud) ⇒ BIPIA is representative.
* If indirect↔indirect PAD is ALSO ~1.9 ⇒ the indirect family is internally fragmented ⇒ BIPIA is
  just one indirect dialect, which weakens BIPIA-as-the-cross-family-test-anchor.

This is local, free, read-only exploratory geometry — NOT a modeling result. It imports and reuses
``pad``, ``_load_bipia``, ``_sample_texts`` and the MiniLM embedder from ``cross_dataset_geometry``;
it does not modify that module or any canonical record.

Run (local, free, CPU):
    uv run python experiments/eda/within_indirect_e7.py
"""

from __future__ import annotations

import json
import sys
import warnings
from itertools import islice
from pathlib import Path

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score

# --- library-first: reuse the E2 geometry primitives verbatim (do NOT reimplement) -----------
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cross_dataset_geometry import (  # noqa: E402
    SEED,
    _load_bipia,
    _sample_texts,
    pad,
)

PER_CORPUS = 250
LLMAIL_STREAM_ROWS = 1500  # cap streamed rows; we only need PER_CORPUS after sampling
WAINJECT_DIR = Path("/tmp/wainjectbench")  # cloned OUTSIDE the repo tree (unlicensed → EDA-only)
OUT_DIR = Path("experiments/eda/CROSS_DATASET")


def _load_llmail(n_stream: int) -> list[str]:
    """Stream LLMail-Inject attack emails (every row is an attack) and join ``subject`` + ``body``.

    The corpus is 461,640 rows (MIT); we *stream* it and take only the first ``n_stream`` rows
    rather than downloading the whole thing. Labels are irrelevant for geometry (all rows are
    attacks ⇒ one "llmail" indirect group), so the nested ``objectives`` JSON is ignored.

    Parameters
    ----------
    n_stream:
        Number of rows to pull from the stream before sampling.

    Returns
    -------
    list[str]
        ``subject`` + "\\n\\n" + ``body`` for each streamed row (empty/missing fields tolerated).

    Raises
    ------
    RuntimeError
        If the dataset yields no usable rows.
    """
    from datasets import load_dataset

    ds = load_dataset("microsoft/llmail-inject-challenge", streaming=True)
    split = "Phase1" if "Phase1" in ds else next(iter(ds))
    texts: list[str] = []
    for row in islice(ds[split], n_stream):
        subject = str(row.get("subject") or "").strip()
        body = str(row.get("body") or "").strip()
        joined = f"{subject}\n\n{body}".strip()
        if joined:
            texts.append(joined)
    if not texts:
        raise RuntimeError("LLMail-Inject stream produced no usable rows")
    return texts


def _load_wainject(root: Path) -> tuple[list[str], int]:
    """Load WAInjectBench *text*-modality malicious rows; also count benign rows for the report.

    NOTE on layout (adapted per the inspect-and-adapt bounding rule): the live repo encodes the
    label **by directory**, not by an in-row ``label`` field. Text JSONL lines are ``{"id","text"}``;
    the malicious/benign split is ``data/text/malicious/*.jsonl`` vs ``data/text/benign/*.jsonl``.
    The ``data/image/*`` modality (``{"path","label"}``) is ignored. So malicious == label-1.

    Parameters
    ----------
    root:
        Cloned WAInjectBench repo root (a scratch dir outside this repo).

    Returns
    -------
    tuple[list[str], int]
        (malicious texts, benign row count seen).

    Raises
    ------
    FileNotFoundError
        If the expected ``data/text/{malicious,benign}`` directories are absent.
    RuntimeError
        If no malicious text rows can be parsed.
    """
    text_root = root / "data" / "text"
    mal_dir, ben_dir = text_root / "malicious", text_root / "benign"
    if not mal_dir.is_dir():
        raise FileNotFoundError(f"WAInjectBench malicious text dir not found: {mal_dir}")

    def _read_text_field(d: Path) -> list[str]:
        out: list[str] = []
        for fp in sorted(d.glob("*.jsonl")):
            for line in fp.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                txt = str(rec.get("text") or "").strip()
                if txt:
                    out.append(txt)
        return out

    malicious = _read_text_field(mal_dir)
    benign_count = len(_read_text_field(ben_dir)) if ben_dir.is_dir() else 0
    if not malicious:
        raise RuntimeError(f"no malicious WAInjectBench text rows parsed under {mal_dir}")
    return malicious, benign_count


def main() -> None:
    """Load the three indirect corpora, embed once, compute pairwise PAD + silhouette, write JSON."""
    out = OUT_DIR
    out.mkdir(parents=True, exist_ok=True)
    blockers: list[str] = []

    # --- per-corpus loaders, each independently bounded (record blocker + proceed on failure) ---
    corpora: dict[str, list[str]] = {}
    wainject_benign = None

    # BIPIA (the indirect anchor) — reuse the E2 loader verbatim.
    try:
        bipia_texts = _sample_texts(_load_bipia(PER_CORPUS), PER_CORPUS, SEED)
        corpora["bipia"] = bipia_texts
    except Exception as exc:  # noqa: BLE001 — record + proceed (bounding rule)
        blockers.append(f"bipia: {type(exc).__name__}: {str(exc)[:160]}")

    # LLMail-Inject (streamed).
    try:
        llmail_texts = _sample_texts(_load_llmail(LLMAIL_STREAM_ROWS), PER_CORPUS, SEED)
        corpora["llmail"] = llmail_texts
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"llmail: {type(exc).__name__}: {str(exc)[:160]}")

    # WAInjectBench (text malicious; benign counted).
    try:
        wain_texts, wainject_benign = _load_wainject(WAINJECT_DIR)
        corpora["wainject"] = _sample_texts(wain_texts, PER_CORPUS, SEED)
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"wainject: {type(exc).__name__}: {str(exc)[:160]}")

    if not corpora:
        raise RuntimeError(f"no indirect corpus loaded; blockers={blockers}")

    # --- build the (text, corpus) frame and embed ALL groups in ONE MiniLM call ---------------
    rows = [{"text": t, "corpus": name} for name, texts in corpora.items() for t in texts]
    df = pd.DataFrame(rows)

    from eval_toolkit.embeddings import make_minilm_embedder

    emb = np.asarray(make_minilm_embedder()(df["text"].tolist()), dtype=float)
    codes = df["corpus"].astype("category").cat.codes.to_numpy()
    names = list(df["corpus"].astype("category").cat.categories)

    # --- pairwise PAD among the loaded corpora -------------------------------------------------
    n = len(names)
    pad_mat = np.full((n, n), np.nan)
    for i in range(n):
        for j in range(i + 1, n):
            p = pad(emb, codes, i, j)
            pad_mat[i, j] = pad_mat[j, i] = p

    pad_matrix = {
        names[i]: {
            names[j]: (round(float(pad_mat[i, j]), 3) if not np.isnan(pad_mat[i, j]) else None)
            for j in range(n)
        }
        for i in range(n)
    }

    # --- within-indirect silhouette (only meaningful with >= 2 corpora) ------------------------
    within_indirect_silhouette = (
        round(float(silhouette_score(emb, codes)), 4) if n >= 2 else None
    )

    metrics = {
        "question": (
            "Is BIPIA representative of the indirect-injection family, or one indirect dialect? "
            "Compare within-indirect PAD (BIPIA/llmail/wainject) against the ~1.9 indirect-vs-direct "
            "baseline from cross_dataset_geometry.json (BIPIA-vs-direct PAD 1.86-2.0)."
        ),
        "per_corpus_n": {name: len(texts) for name, texts in corpora.items()},
        "wainject_benign_count_seen": wainject_benign,
        "pad_matrix": pad_matrix,
        "within_indirect_silhouette": within_indirect_silhouette,
        "indirect_vs_direct_baseline_pad_range": [1.864, 2.0],
        "blockers": blockers,
        "interpretation": (
            "within-indirect PAD much LOWER than ~1.9 => indirect corpora cluster together apart "
            "from the direct cloud => BIPIA is representative. within-indirect PAD comparably high "
            "(~1.9) => the indirect family is internally fragmented => BIPIA is one dialect, which "
            "weakens BIPIA-as-the-cross-family-test-anchor."
        ),
    }
    (out / "within_indirect_e7.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print(f"[done] per_corpus_n={metrics['per_corpus_n']}", flush=True)
    print(f"[done] wainject_benign_count_seen={wainject_benign}", flush=True)
    print(f"[done] pad_matrix={pad_matrix}", flush=True)
    print(f"[done] within_indirect_silhouette={within_indirect_silhouette}", flush=True)
    print(f"[done] blockers={blockers}", flush=True)
    print(f"[done] wrote {out}/within_indirect_e7.json", flush=True)


if __name__ == "__main__":
    main()
