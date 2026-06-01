"""Off-the-shelf reference scorers for the attack-type-LODO comparison (ADR-054).

Scores frozen, **untrained** prompt-injection guards on each LODO fold's *test set* as a
reference column alongside the trained rungs (the "off-the-shelf vs trained" comparison).
These are **not** detector rungs: their artifacts are named ``reference_{probe}.test_scores.parquet``
(not ``{rung}.predictions.parquet``), so :func:`harness._scan_artifacts` /
``detectors.REQUIRED_RUNGS`` never see them — they can never affect ``complete_headline_sweep``
or the §6.5 write-gate.

Gated probes (Meta PG1/PG2) **skip-gracefully** on a 403/unavailable — exactly as
``experiments/eda/OOD_WALL_PREDICTION/run_v10_probes.py`` does — so the run itself is the
per-account grant check (issue #1). ProtectAI is ungated and always scores.

Scoring recipe (mirrors ``run_v10_probes.score_texts``): malicious = ``1 − P(benign)``,
512-token chunk + max-pool (a late-positioned payload is not truncated away), benign class
resolved from ``id2label``. The probes are untrained, so a probe's score for a given text is
deterministic; we score the **seed-0 test set** as the representative reference column.

Run::

    python experiments/attack-type-lodo/reference_scorers.py --out experiments/attack-type-lodo/results
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
import pandas as pd
from eval_toolkit.artifacts import write_json_strict

_HERE = Path(__file__).resolve().parent
_OOD_DIR = _HERE.parent / "eda" / "OOD_WALL_PREDICTION"
for _p in (_HERE, _OOD_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import folds  # noqa: E402
import metrics  # noqa: E402
from bipia_carrier import build_examples  # noqa: E402  # type: ignore[import-not-found]

REPO_ROOT = _HERE.parent.parent
BIPIA_ROOT = REPO_ROOT / "data" / "raw" / "BIPIA" / "benchmark"
_MAX_TOK = 512

# Off-the-shelf guards (frozen, inference-only). ProtectAI is ungated; the Meta guards are
# gated (per-account license) and skip-gracefully on 403. Scope notes: run_v10_probes.VALIDITY.
REFERENCE_PROBES: dict[str, str] = {
    "protectai_v2": "protectai/deberta-v3-base-prompt-injection-v2",
    "prompt_guard_2": "meta-llama/Llama-Prompt-Guard-2-86M",
    "prompt_guard_1": "meta-llama/Prompt-Guard-86M",
}


def _benign_index(config: Any) -> int:
    """Resolve the benign class index from a model's ``id2label`` (convention: index 0)."""
    for idx, name in config.id2label.items():
        if str(name).upper() in {"BENIGN", "SAFE", "LABEL_0", "0", "NEGATIVE"}:
            return int(idx)
    return 0


def score_texts(texts: Sequence[str], model_id: str) -> npt.NDArray[np.float64]:
    """Malicious score ``1 − P(benign)`` per text; 512-tok chunk + max-pool. Inference-only.

    Mirrors ``run_v10_probes.score_texts``. ``torch`` / ``transformers`` are imported lazily
    (as in :mod:`detectors`) so importing this module stays light. Propagates a load error
    (e.g. a gated 403) to the caller, which skips that probe.
    """
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSequenceClassification.from_pretrained(model_id).to(device).eval()
    benign = _benign_index(model.config)
    out = np.empty(len(texts), dtype=np.float64)
    with torch.no_grad():
        for i, text in enumerate(texts):
            ids = tok(text, truncation=False, return_tensors="pt")["input_ids"][0]
            chunks = [ids[j : j + _MAX_TOK] for j in range(0, max(len(ids), 1), _MAX_TOK)] or [ids]
            best = 0.0
            for chunk in chunks:
                logits = model(input_ids=chunk.unsqueeze(0).to(device)).logits
                probs = torch.softmax(logits, dim=-1)[0]
                best = max(best, float(1.0 - probs[benign].item()))
            out[i] = best
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return out


def score_fold(
    frame: pd.DataFrame,
    fold_name: str,
    *,
    seed: int,
    probes: dict[str, str],
    out_dir: Path,
) -> dict[str, dict[str, object]]:
    """Score every accessible reference probe on one fold's test set; persist + return records.

    Writes, per accessible probe, ``{out}/seed={seed}/{fold}/reference_{probe}.test_scores.parquet``
    + ``reference_{probe}.metrics.json``. A gated/unavailable probe is recorded as ``skipped``
    (never raises) so the run is the per-account grant check.
    """
    fold = folds.make_fold(frame, fold_name, seed=seed)
    test = fold.test
    labels = test["label"].tolist()
    fold_dir = out_dir / f"seed={seed}" / fold_name
    fold_dir.mkdir(parents=True, exist_ok=True)
    records: dict[str, dict[str, object]] = {}
    for pname, model_id in probes.items():
        try:
            scores = score_texts(test["text"].tolist(), model_id)
        except Exception as exc:  # noqa: BLE001 — gated/unavailable probe → skip, never block
            reason = f"{type(exc).__name__}: {str(exc).splitlines()[0][:140]}"
            print(f"  [skip] reference {pname} ({model_id}): {reason}")
            records[pname] = {"status": "skipped", "reason": reason, "model_id": model_id}
            continue
        record: dict[str, object] = {
            "reference_probe": pname,
            "model_id": model_id,
            "fold": fold_name,
            "seed": seed,
            "status": "ok",
            "headline": metrics.compute_fold_metrics(labels, scores, n_bootstrap=0, seed=seed),
            "n_test": int(len(test)),
            "note": "off-the-shelf reference (untrained); NOT a rung; non-gating (ADR-054)",
        }
        pred = test.loc[:, ["text", "label", "attack_type", "carrier"]].copy()
        pred["y_score"] = scores
        pred.to_parquet(fold_dir / f"reference_{pname}.test_scores.parquet", index=False)
        write_json_strict(record, fold_dir / f"reference_{pname}.metrics.json")
        records[pname] = record
        print(f"  [ok] reference {pname} on {fold_name} (seed={seed}, n_test={len(test)})")
    return records


def main(argv: Sequence[str] | None = None) -> int:
    """Score the reference probes on the LODO fold test sets (seed-0 representative)."""
    p = argparse.ArgumentParser(description="Off-the-shelf reference scorers (ADR-054; non-gating).")
    p.add_argument("--out", type=Path, default=_HERE / "results")
    p.add_argument("--folds", nargs="+", default=list(folds.FOLD_NAMES), choices=folds.FOLD_NAMES)
    p.add_argument("--seed", type=int, default=0, help="fold-carve seed (probes untrained)")
    p.add_argument("--contexts-per-attack", type=int, default=12)
    args = p.parse_args(argv)
    if not BIPIA_ROOT.exists():
        raise FileNotFoundError(f"BIPIA benchmark not found at {BIPIA_ROOT}.")
    frame = build_examples(
        root=BIPIA_ROOT, contexts_per_attack=args.contexts_per_attack, seed=args.seed
    ).frame
    any_ok = False
    for fold_name in args.folds:
        res = score_fold(frame, fold_name, seed=args.seed, probes=REFERENCE_PROBES, out_dir=args.out)
        any_ok = any_ok or any(r.get("status") == "ok" for r in res.values())
    if not any_ok:
        print(
            "[reference] no probe accessible — ProtectAI is ungated; Meta PG1/PG2 need the "
            "gate GRANTED (issue #1)."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
