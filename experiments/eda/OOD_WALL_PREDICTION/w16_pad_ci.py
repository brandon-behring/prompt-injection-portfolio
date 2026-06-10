"""W16 re-check — the promised per-type PAD bootstrap CI (audit 2026-06-10).

``criteria.md`` (Locked metric knobs) promised PAD "with CV/bootstrap CI", but
``run_prediction.py:148`` computed the per-type embedding PAD with ``n_bootstrap=0``
(``pad_emb_ci_low/high`` are ``null`` in the committed ``results.json``; V9's PAD bars
carry zero-width whiskers). This re-check computes the CI the criteria promised.

Faithful-but-not-bit-identical: the train-pool reference subsample (cap 200/type) is
REDRAWN with a documented fresh ``default_rng(SEED)`` — the original draw's RNG state
depended on prior in-script consumption (NotInject shuffle, C2 balance) and is not
replayable in isolation. The recomputed PAD point therefore differs slightly from the
committed one; both are reported with their delta, so the CI brackets can be read
against the committed points honestly.

Writes a NEW dated artifact ``w16_pad_ci.json``; touches no committed file
(``results.json`` is read for contrast only — never rewritten; audit W3 discipline).

Run:  uv run python experiments/eda/OOD_WALL_PREDICTION/w16_pad_ci.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

from eval_toolkit.eda import proxy_a_distance
from eval_toolkit.embeddings import make_minilm_embedder

HERE = Path(__file__).resolve().parent
BIPIA_ROOT = Path.cwd() / "data" / "raw" / "BIPIA" / "benchmark"
SEED = 0
PER_TYPE_CAP = 200  # mirrors run_prediction.PER_TYPE_MMD_CAP
N_BOOTSTRAP = 1000
sys.path.insert(0, str(HERE))
from bipia_carrier import build_examples  # noqa: E402


def main() -> None:
    rng = np.random.default_rng(SEED)
    committed = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    per_type_committed = committed["per_type"]

    ex = build_examples(root=BIPIA_ROOT, contexts_per_attack=12, seed=SEED)
    df = ex.frame
    test_types = list(ex.test_types)
    embed = make_minilm_embedder()
    train_pos = df[(df.role == "train") & (df.label == 1)]
    train_pos_emb = np.asarray(embed(train_pos["text"].tolist()), dtype=float)

    out: dict[str, Any] = {
        "finding": "W16 (consolidated-audit-2026-06-09.md) — per-type PAD bootstrap CI",
        "n_bootstrap": N_BOOTSTRAP,
        "ref_subsample": f"cap {PER_TYPE_CAP}/type, fresh default_rng({SEED}) redraw (see docstring)",
        "per_type": {},
    }
    deltas: list[float] = []
    for t in test_types:
        txt = df[(df.role == "test") & (df.label == 1) & (df.attack_type == t)]["text"].tolist()
        tp = np.asarray(embed(txt), dtype=float)
        cap = min(PER_TYPE_CAP, len(train_pos_emb))
        ref_idx = rng.choice(len(train_pos_emb), size=cap, replace=False)
        pad = proxy_a_distance(
            train_pos_emb[ref_idx], tp, n_bootstrap=N_BOOTSTRAP, random_state=SEED
        )
        committed_pad = float(per_type_committed[t]["pad_emb"])
        delta = float(pad.pad) - committed_pad
        deltas.append(abs(delta))
        out["per_type"][t] = {
            "committed_pad_emb": committed_pad,
            "recomputed_pad_emb": float(pad.pad),
            "delta_vs_committed": round(delta, 4),
            "ci_low": float(pad.ci_low) if pad.ci_low is not None else None,
            "ci_high": float(pad.ci_high) if pad.ci_high is not None else None,
        }
        print(
            f"[{t:32s}] committed={committed_pad:.3f} recomputed={pad.pad:.3f} "
            f"CI=[{pad.ci_low:.3f},{pad.ci_high:.3f}]",
            flush=True,
        )

    out["max_abs_delta_vs_committed"] = round(max(deltas), 4)
    (HERE / "w16_pad_ci.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"max |Δ| vs committed point estimates: {max(deltas):.4f}")
    print("wrote w16_pad_ci.json")


if __name__ == "__main__":
    main()
