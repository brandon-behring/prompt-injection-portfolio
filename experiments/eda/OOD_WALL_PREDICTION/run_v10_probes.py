"""V10 — reference-scorer score-distributions per slice (the missing §9.5 figure).

Runs three FROZEN off-the-shelf probes over BIPIA slices and plots their
malicious-score distributions per attack-type vs benign — the diagnostic the
prompt-injection post-mortem said was missing. Probes (pre-registered):

- ``meta-llama/Prompt-Guard-86M`` (PG1) — the only probe with an explicit
  indirect-injection objective → **valid** on BIPIA's indirect attacks.
- ``protectai/deberta-v3-base-prompt-injection-v2`` — direct-injection scope →
  a low score on BIPIA-indirect partly reflects **probe scope-blindness**, not data.
- ``meta-llama/Llama-Prompt-Guard-2-86M`` (PG2) — deliberate scope-contrast
  (PG2 narrowed to explicit-override; the PG1↔PG2 gap is itself informative).

Malicious score = ``1 − P(benign)`` (benign label resolved per model config).
Long inputs are 512-token chunked + **max-pooled** so a late-positioned payload
is not truncated away. Subsamples per slice for tractability (a distribution, not
a metric). Contamination/over-defense caveats are recorded in the validity map.

Run:  uv run python experiments/eda/OOD_WALL_PREDICTION/run_v10_probes.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

HERE = Path(__file__).resolve().parent
BIPIA_ROOT = Path.cwd() / "data" / "raw" / "BIPIA" / "benchmark"
SEED = 0
PER_TYPE = 40
MAX_TOK = 512
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
sys.path.insert(0, str(HERE))
from bipia_carrier import build_examples  # noqa: E402

PROBES = {
    "prompt_guard_1": "meta-llama/Prompt-Guard-86M",
    "protectai_v2": "protectai/deberta-v3-base-prompt-injection-v2",
    "prompt_guard_2": "meta-llama/Llama-Prompt-Guard-2-86M",
}
# Pre-registered per-probe validity on BIPIA (indirect injection).
VALIDITY = {
    "prompt_guard_1": "VALID — explicit indirect-injection objective; over-triggers benign (read relatively)",
    "protectai_v2": "SCOPE-CAVEAT — direct-injection probe; low BIPIA score may be scope-blindness, not data",
    "prompt_guard_2": "SCOPE-CONTRAST — narrowed to explicit-override; under-scores indirect by design",
}


def benign_index(model: AutoModelForSequenceClassification) -> int:
    """Resolve the benign class index from the model's id2label."""
    id2label = model.config.id2label
    for idx, name in id2label.items():
        if str(name).upper() in {"BENIGN", "SAFE", "LABEL_0", "0", "NEGATIVE"}:
            return int(idx)
    return 0  # convention: index 0 is the benign/negative class


@torch.no_grad()
def score_texts(texts: list[str], model_id: str) -> np.ndarray:
    """Malicious score (1 − P(benign)) per text, 512-token chunk + max-pool."""
    tok = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSequenceClassification.from_pretrained(model_id).to(DEVICE).eval()
    b_idx = benign_index(model)
    out = np.empty(len(texts), dtype=float)
    for i, text in enumerate(texts):
        ids = tok(text, truncation=False, return_tensors="pt")["input_ids"][0]
        # 512-token chunks (max-pool the malicious score across chunks).
        chunks = [ids[j : j + MAX_TOK] for j in range(0, max(len(ids), 1), MAX_TOK)] or [ids]
        best = 0.0
        for ch in chunks:
            batch = ch.unsqueeze(0).to(DEVICE)
            logits = model(input_ids=batch).logits
            probs = torch.softmax(logits, dim=-1)[0]
            mal = float(1.0 - probs[b_idx].item())
            best = max(best, mal)
        out[i] = best
    del model
    if DEVICE == "cuda":
        torch.cuda.empty_cache()
    return out


def main() -> None:
    rng = np.random.default_rng(SEED)
    ex = build_examples(root=BIPIA_ROOT, contexts_per_attack=12, seed=SEED)
    df = ex.frame
    test_types = list(ex.test_types)

    # Build slices: per test-attack-type positives + a benign negative pool.
    slices: dict[str, list[str]] = {}
    for t in test_types:
        pool = df[(df.role == "test") & (df.label == 1) & (df.attack_type == t)]["text"].tolist()
        slices[t] = list(rng.choice(pool, size=min(PER_TYPE, len(pool)), replace=False))
    neg_pool = df[(df.role == "test") & (df.label == 0)]["text"].tolist()
    slices["[benign clean]"] = list(rng.choice(neg_pool, size=min(120, len(neg_pool)), replace=False))

    flat_texts: list[str] = []
    flat_slice: list[str] = []
    for sname, txts in slices.items():
        flat_texts.extend(txts)
        flat_slice.extend([sname] * len(txts))
    flat_slice_arr = np.array(flat_slice)

    print(f"=== V10: scoring {len(flat_texts)} texts × {len(PROBES)} probes on {DEVICE} ===")
    scores: dict[str, dict[str, list[float]]] = {}
    skipped: dict[str, str] = {}
    for pname, mid in PROBES.items():
        print(f"  scoring {pname} ({mid}) ...")
        try:
            s = score_texts(flat_texts, mid)
        except Exception as exc:  # noqa: BLE001 — gated/unavailable probe → skip gracefully
            msg = f"{type(exc).__name__}: {str(exc).splitlines()[0][:140]}"
            print(f"  [SKIP] {pname}: {msg}")
            skipped[pname] = msg
            continue
        scores[pname] = {
            sname: [float(x) for x in s[flat_slice_arr == sname]] for sname in slices
        }
    if not scores:
        raise SystemExit(
            "V10: no probes accessible. protectai-v2 is ungated; PG1/PG2 need the Meta "
            "Llama gate GRANTED (not just requested). Accept at the HF model pages, then rerun."
        )
    if skipped:
        print(f"  [note] {len(skipped)} probe(s) skipped (access pending): {list(skipped)}")

    # Persist per-probe per-slice mean malicious score + validity map.
    summary = {
        "probes": PROBES,
        "scored_probes": list(scores),
        "skipped_probes": skipped,
        "validity_map": VALIDITY,
        "per_probe_slice_mean": {
            p: {sn: round(float(np.mean(v)), 4) for sn, v in sl.items()} for p, sl in scores.items()
        },
        "benign_overtrigger_mean": {
            p: round(float(np.mean(sl["[benign clean]"])), 4) for p, sl in scores.items()
        },
        "note": "Score = 1 - P(benign), 512-tok chunk + max-pool. Read PG1 relatively (over-triggers "
        "benign); protectai/PG2 are direct-scope → low BIPIA-indirect scores are partly scope-blindness.",
    }
    (HERE / "v10_scores.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Figure: one row per probe, box-by-slice (test-types + benign).
    order = test_types + ["[benign clean]"]
    fig, axes = plt.subplots(len(scores), 1, figsize=(13, 3.7 * len(scores)), sharex=True)
    axes = np.atleast_1d(axes)
    for ax, (pname, sl) in zip(axes, scores.items(), strict=True):
        data = [sl[s] for s in order]
        bp = ax.boxplot(data, vert=True, showfliers=False, patch_artist=True)
        for patch, s in zip(bp["boxes"], order, strict=True):
            patch.set_facecolor("#bbb" if s == "[benign clean]" else "#e88")
        ax.set_ylabel("malicious\nscore", fontsize=8)
        ax.set_ylim(-0.02, 1.02)
        ax.set_title(f"{pname} — {VALIDITY[pname]}", fontsize=9, loc="left")
    axes[-1].set_xticks(range(1, len(order) + 1))
    axes[-1].set_xticklabels(order, rotation=90, fontsize=7)
    fig.suptitle("V10 — reference-scorer malicious-score distribution per BIPIA slice (test-attack-types + benign)")
    fig.tight_layout()
    fig.savefig(HERE / "V10_refscorer_distributions.png", dpi=120)
    plt.close(fig)
    print("\nper-probe benign-clean mean (over-trigger floor):")
    for p in scores:
        print(f"  {p:16s} benign={summary['benign_overtrigger_mean'][p]:.3f}  "
              f"mean-test-type={np.mean([summary['per_probe_slice_mean'][p][t] for t in test_types]):.3f}")
    print(f"wrote V10_refscorer_distributions.png + v10_scores.json")


if __name__ == "__main__":
    main()
