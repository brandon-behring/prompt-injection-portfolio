"""E8 off-the-shelf detector reference column for the dialect-transfer study (criteria §E8).

Scores the three wired frozen guards — ProtectAI-v2, Prompt-Guard-2-86M, Prompt-Guard-1-86M — on
each held-out dialect's test set as a **non-gating deployed-baseline contrast** (criteria §E8).
Tests: *do deployed guards generalize to HTML / RAG / tool-output indirect carriers, or blind too?*

Library-first (ADR-026): reuses ``attack-type-lodo/reference_scorers.score_texts`` (chunk +
max-pool; ``reference_scorers.py:74``) — its recipe already splits each doc into ≤512-token windows
with the detector's own tokenizer, scores every chunk, and takes the **max** chunk score as the doc
score (the steel-man "is the guard blind?" test). Gated probes (Meta PG1/PG2) skip on a 403.

Reporting discipline (criteria §E8 + the AUDIT_2026-06 lesson): report **AUROC + per-class score
means** per dialect per detector — blind accuracy / AUPRC at high prevalence hides the blindness.

Long-document cap (criteria Rev 2 (c) deviation guard): chunk-scoring the full browsesafe (14.7k) /
fujitsu (21.9k) test sets is impractically slow on the local RTX 2070S. We cap each dialect test set
to ``_MAX_DOCS_PER_DIALECT`` docs (label-stratified, seeded) and **log the cap explicitly** in the
emitted record (``capped`` / ``n_scored`` / ``n_full``) — no silent truncation.
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ATTACK_LODO_DIR = _HERE.parent / "attack-type-lodo"
for _p in (_HERE, _ATTACK_LODO_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import metrics  # noqa: E402
from reference_scorers import REFERENCE_PROBES, score_texts  # noqa: E402

# Cap on docs scored per dialect (cap-and-log, criteria Rev 2 (c)); 0 = no cap.
_MAX_DOCS_PER_DIALECT = 2_000


def _cap_test(test: pd.DataFrame, *, max_docs: int, seed: int) -> tuple[pd.DataFrame, bool]:
    """Label-stratified seeded down-sample of a dialect test set to ``max_docs`` (cap-and-log).

    Preserves class prevalence; returns ``(capped_frame, was_capped)``. ``max_docs <= 0`` or a
    set already at/under the cap passes through untouched.
    """
    if max_docs <= 0 or len(test) <= max_docs:
        return test.reset_index(drop=True), False
    frac = max_docs / len(test)
    rng = np.random.default_rng(seed)
    parts = []
    for _, grp in test.groupby("label"):
        n = max(1, int(round(len(grp) * frac)))
        take = rng.choice(len(grp), size=min(n, len(grp)), replace=False)
        parts.append(grp.iloc[take])
    capped = pd.concat(parts, ignore_index=True)
    return capped.reset_index(drop=True), True


def score_dialect(
    test: pd.DataFrame,
    dialect: str,
    *,
    probes: dict[str, str] = REFERENCE_PROBES,
    max_docs: int = _MAX_DOCS_PER_DIALECT,
    seed: int = 0,
) -> dict[str, dict[str, Any]]:
    """Score every accessible reference probe on one held-out dialect's test set.

    Returns AUROC + per-class score means per probe (criteria §E8 reporting discipline). A
    gated/unavailable probe is recorded ``skipped`` (never raises). The long-doc cap is logged in
    every record.

    Parameters
    ----------
    test : pandas.DataFrame
        The held-out dialect's test rows (needs ``text`` / ``label``).
    dialect : str
        Held-out dialect name (for the record).
    probes : dict[str, str]
        ``{probe_name: model_id}`` (default = the 3 wired guards).
    max_docs : int
        Per-dialect cap (cap-and-log); 0 disables.
    seed : int
        Down-sample seed.

    Returns
    -------
    dict
        ``{probe_name: {status, auroc, mean_attack, mean_benign, n_scored, n_full, capped, ...}}``.
    """
    n_full = int(len(test))
    scored, capped = _cap_test(test, max_docs=max_docs, seed=seed)
    labels = scored["label"].to_numpy()
    texts = scored["text"].astype(str).tolist()
    records: dict[str, dict[str, Any]] = {}
    for pname, model_id in probes.items():
        try:
            s = score_texts(texts, model_id)
        except Exception as exc:  # noqa: BLE001 — gated/unavailable probe → skip, never block
            reason = f"{type(exc).__name__}: {str(exc).splitlines()[0][:140]}"
            print(f"  [skip] E8 {pname} on {dialect} ({model_id}): {reason}")
            records[pname] = {
                "status": "skipped",
                "reason": reason,
                "model_id": model_id,
                "dialect": dialect,
            }
            continue
        records[pname] = {
            "status": "ok",
            "model_id": model_id,
            "dialect": dialect,
            "auroc": metrics.roc_auc_point(labels, s),
            "mean_attack": float(s[labels == 1].mean()) if (labels == 1).any() else None,
            "mean_benign": float(s[labels == 0].mean()) if (labels == 0).any() else None,
            "n_scored": int(len(texts)),
            "n_full": n_full,
            "capped": capped,
            "max_docs": max_docs,
        }
        if capped:
            print(
                f"  [cap] E8 {pname} on {dialect}: scored {len(texts)}/{n_full} "
                f"(label-stratified cap={max_docs}, seed={seed}) — LOGGED"
            )
        print(
            f"  [ok] E8 {pname} on {dialect}: AUROC={records[pname]['auroc']:.3f} "
            f"mean_atk={records[pname]['mean_attack']} mean_ben={records[pname]['mean_benign']}"
        )
    return records


def score_all_dialects(
    dialect_tests: dict[str, pd.DataFrame],
    *,
    probes: dict[str, str] = REFERENCE_PROBES,
    max_docs: int = _MAX_DOCS_PER_DIALECT,
    seed: int = 0,
) -> dict[str, dict[str, dict[str, Any]]]:
    """Run :func:`score_dialect` over each held-out dialect → ``{dialect: {probe: record}}``."""
    out: dict[str, dict[str, dict[str, Any]]] = {}
    for dialect, test in dialect_tests.items():
        print(f"[E8] dialect={dialect} (n_test={len(test)})")
        out[dialect] = score_dialect(test, dialect, probes=probes, max_docs=max_docs, seed=seed)
    return out


def _probe_names(_argv: Sequence[str] | None = None) -> list[str]:
    """Names of the wired probes (exposed for orchestrator logging)."""
    return list(REFERENCE_PROBES)
