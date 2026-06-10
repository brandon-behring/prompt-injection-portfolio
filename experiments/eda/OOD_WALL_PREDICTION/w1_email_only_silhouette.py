"""W1 re-check — per-carrier (email-only headline) attack-type silhouette (audit 2026-06-10).

The full re-audit (consolidated-audit-2026-06-09.md, finding **W1**) showed the V4/A1
geometry is partly a literal truncation artifact: MiniLM's ``max_seq_length=256`` +
BIPIA's suffix injection mean most **table** and many **code** positives carry ZERO
attack tokens into the embedder, so "attack-type is embedding-invisible" was measured
on inputs that often did not contain the attack. The pre-registered re-check: recompute
the by-attack-type silhouette **within the email carrier** (whose texts fit in 256
tokens), where the attack tokens are actually visible to the embedder.

Reads nothing from and writes nothing to the committed V4 artifacts
(``a1_v4_metrics.json`` is quoted for contrast only); emits a NEW dated artifact
``w1_email_only_recheck.json``.

Run:  uv run python experiments/eda/OOD_WALL_PREDICTION/w1_email_only_silhouette.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

from eval_toolkit.embeddings import make_minilm_embedder

HERE = Path(__file__).resolve().parent
BIPIA_ROOT = Path.cwd() / "data" / "raw" / "BIPIA" / "benchmark"
SEED = 0
MAX_TOKENS = 256  # MiniLM sentence_bert_config.json max_seq_length
sys.path.insert(0, str(HERE))
from bipia_carrier import build_examples  # noqa: E402


def truncation_fraction(texts: list[str]) -> float:
    """Fraction of rows whose attack suffix is entirely beyond the 256-token window.

    Every positive is suffix-injected (``position="suffix"`` in ``bipia_carrier``), so
    the attack tokens are the text's tail. Tokenizes with the MiniLM tokenizer, decodes
    the first ``MAX_TOKENS`` tokens, and checks whether the text's last ~40 characters
    survive in the decoded prefix; a truncated row keeps none of its attack tokens.
    """
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    lost = 0
    for text in texts:
        ids = tok(text, add_special_tokens=False)["input_ids"]
        if len(ids) <= MAX_TOKENS:
            continue
        prefix = tok.decode(ids[:MAX_TOKENS])
        probe = text.strip()[-40:].strip().lower()
        if probe and probe not in prefix.lower():
            lost += 1
    return lost / max(1, len(texts))


def carrier_geometry(samp: Any, embed: Any) -> dict[str, float | int]:
    """Silhouette/ARI of the attack-type labelling within one carrier's positives."""
    emb = np.asarray(embed(samp["text"].tolist()), dtype=float)
    type_codes = samp["attack_type"].astype("category").cat.codes.to_numpy()
    n_types = len(set(type_codes))
    km = KMeans(n_clusters=n_types, n_init=10, random_state=SEED).fit_predict(emb)
    return {
        "n": int(len(samp)),
        "n_attack_types": n_types,
        "silhouette_by_attack_type": float(silhouette_score(emb, type_codes)),
        "ari_kmeans_vs_attack_type": float(adjusted_rand_score(type_codes, km)),
    }


def main() -> None:
    ex = build_examples(root=BIPIA_ROOT, contexts_per_attack=12, seed=SEED)
    pos = ex.frame[ex.frame.label == 1].reset_index(drop=True)
    embed = make_minilm_embedder()
    committed = json.loads((HERE / "a1_v4_metrics.json").read_text(encoding="utf-8"))

    out: dict[str, Any] = {
        "finding": "W1 (consolidated-audit-2026-06-09.md) — MiniLM-256 truncation re-check",
        "committed_pooled_silhouette": committed["silhouette"],
        "per_carrier": {},
        "truncation_fraction_no_attack_tokens": {},
    }
    for carrier in sorted(pos.carrier.unique()):
        sub = pos[pos.carrier == carrier].reset_index(drop=True)
        geo = carrier_geometry(sub, embed)
        frac = truncation_fraction(sub["text"].tolist())
        out["per_carrier"][carrier] = geo
        out["truncation_fraction_no_attack_tokens"][carrier] = round(frac, 4)
        print(
            f"[{carrier}] n={geo['n']} sil(by_attack_type)={geo['silhouette_by_attack_type']:+.4f} "
            f"ARI={geo['ari_kmeans_vs_attack_type']:+.4f} trunc_frac={frac:.3f}",
            flush=True,
        )

    email_sil = out["per_carrier"]["email"]["silhouette_by_attack_type"]
    out["verdict"] = (
        "CONCLUSION SURVIVES — attack-type stays embedding-invisible on the untruncated "
        "email carrier"
        if abs(email_sil) < 0.05
        else "CONCLUSION WEAKENED — attack-type separates within email; the pooled headline "
        "was partly truncation-driven"
    )
    (HERE / "w1_email_only_recheck.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"verdict: {out['verdict']}")
    print("wrote w1_email_only_recheck.json")


if __name__ == "__main__":
    main()
