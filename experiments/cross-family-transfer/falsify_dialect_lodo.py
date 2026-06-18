"""Dialect-LODO ROC-AUC transfer-gap estimator — cross-family-transfer/criteria.md Rev 1/2.

The within-indirect (Arm B) sibling of ``attack-type-lodo/falsify_carrier_lodo.py``. Mirrors that
module's seed-aggregation, permutation construction, and ≥10 000-iter bootstrap, with the **one
pre-registered change** of criteria Rev 2 (b): the resampling unit is a **label-stratified cluster
bootstrap** — within each held-out dialect's test set, positive-clusters and negative-clusters are
resampled **separately** (by ``cluster_id``), preserving prevalence and never collapsing to a single
class. (Carrier-LODO resamples *only* the positive payload-clusters with negatives held fixed; here
both class-sides are resampled by cluster.)

``Gx(rung, dialect) = val_roc_auc − test_roc_auc(held-out dialect)`` (criteria §Statistics 2), on a
ROC-AUC basis (prevalence-invariant). ``val_roc`` is read from the harness ``metrics.json`` (the
predictions parquet holds only test rows) and **held fixed** in the bootstrap, as carrier-LODO does.

This module is B2.3 (cheap rungs): it produces the **directional per-dialect × per-rung table**
only, **NOT a verdict** (the verdict is lora-gated at B3). It therefore reports the per-dialect Gx,
the one-sided 95 % label-stratified-cluster bootstrap CI, and the per-fold permutation p — but
computes no SURVIVES/FALSIFIED/SMALL-THROUGHOUT label.

Seed-aggregation (mirrors ``falsify_carrier_lodo._rung_gap``): ``val_roc`` and the point
``test_roc`` are each averaged over seeds; in the bootstrap each iteration draws one resampled
``test_roc`` per seed and averages them, then forms ``Gx = mean_seed(val_roc) −
mean_seed(test_roc_b)`` (val held fixed). The permutation is a **presence-of-transfer** diagnostic:
it permutes the held-out test labels (within each seed), recomputes the null ``test_roc``, and
reports ``perm_p`` = fraction of null ``test_roc`` ≥ the observed (does the detector beat chance on
the held-out dialect?). Bootstrap iteration count ``_N_BOOT = 10_000``. (Carrier-LODO has no
permutation test — only the bootstrap CI + verdict; this presence-of-transfer diagnostic is the
dialect-axis addition the pre-reg's "per-fold permutation, presence-of-effect" calls for.)
"""

from __future__ import annotations

import json
import sys
from collections.abc import Hashable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from eval_toolkit.bootstrap import stratified_cluster_bootstrap_ci
from scipy.stats import rankdata  # type: ignore[import-untyped]

_HERE = Path(__file__).resolve().parent
_ATTACK_LODO_DIR = _HERE.parent / "attack-type-lodo"
for _p in (_HERE, _ATTACK_LODO_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import metrics  # noqa: E402  # attack-type-lodo/metrics.py (roc_auc_point)

_N_BOOT = 10_000
_N_PERM = 10_000
RUNGS_CHEAP: tuple[str, ...] = ("tfidf", "frozen")

_SeedFloat = dict[int, float]


def _roc_auc_fast(y: np.ndarray, s: np.ndarray) -> float:
    """Tie-corrected AUROC via the Mann-Whitney rank-sum (the fast bootstrap inner loop).

    Equivalent to ``sklearn.roc_auc_score`` including ties (average ranks); identical to
    ``falsify_carrier_lodo._roc_auc_fast``. Used only inside the bootstrap / permutation loops; the
    point estimate uses ``eval_toolkit`` via :func:`metrics.roc_auc_point`.
    """
    n_pos = int((y == 1).sum())
    n_neg = int((y == 0).sum())
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    ranks = np.asarray(rankdata(s), dtype=float)
    sum_pos = float(ranks[y == 1].sum())
    return (sum_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


@dataclass(frozen=True)
class DialectFold:
    """Per-seed label-stratified test clusters + ``val_roc`` for one (dialect, rung).

    Attributes
    ----------
    pos_clusters, neg_clusters : dict[int, list[np.ndarray]]
        Per-seed lists of per-cluster score arrays, split by label (the label-stratified
        cluster-bootstrap units; criteria Rev 2 (b)).
    val_roc : dict[int, float]
        Per-seed in-distribution val ROC-AUC (held fixed in the bootstrap).
    seeds : list[int]
        Sorted seeds present on disk for this fold/rung.
    """

    pos_clusters: dict[int, list[np.ndarray]]
    neg_clusters: dict[int, list[np.ndarray]]
    val_roc: _SeedFloat
    seeds: list[int]


def load_dialect_fold(results_dir: Path, fold_name: str, rung: str) -> DialectFold:
    """Build the per-seed label-stratified cluster structure for one dialect-LODO fold + rung.

    Reads each seed's ``{rung}.predictions.parquet`` (test rows carry ``cluster_id`` + ``label`` +
    ``y_score``) and its sibling ``{rung}.metrics.json`` for ``val_roc_auc`` (held fixed in the
    bootstrap). Positive and negative score arrays are grouped by ``cluster_id`` **separately**.
    """
    paths = sorted(results_dir.glob(f"seed=*/{fold_name}/{rung}.predictions.parquet"))
    if not paths:
        raise FileNotFoundError(f"no {rung} predictions for {fold_name} under {results_dir}")
    pos_clusters: dict[int, list[np.ndarray]] = {}
    neg_clusters: dict[int, list[np.ndarray]] = {}
    val_roc: _SeedFloat = {}
    seeds: list[int] = []
    for p in paths:
        seed = int(p.parent.parent.name.split("=")[1])
        seeds.append(seed)
        df = pd.read_parquet(p)
        if "cluster_id" not in df.columns:
            raise KeyError(f"{p} lacks cluster_id — re-run the dialect harness (run_b2_3.py)")
        pdf = df.loc[df["label"] == 1]
        ndf = df.loc[df["label"] == 0]
        pos_clusters[seed] = [
            grp["y_score"].to_numpy(dtype=float) for _, grp in pdf.groupby("cluster_id")
        ]
        neg_clusters[seed] = [
            grp["y_score"].to_numpy(dtype=float) for _, grp in ndf.groupby("cluster_id")
        ]
        meta_path = p.with_name(f"{rung}.metrics.json")
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("val_roc_auc") is None:
            raise KeyError(f"{meta_path} lacks val_roc_auc — re-run run_b2_3.py")
        val_roc[seed] = float(meta["val_roc_auc"])
    return DialectFold(pos_clusters, neg_clusters, val_roc, sorted(seeds))


def _point_test_roc(fold: DialectFold, seed: int) -> float:
    """Pooled test ROC-AUC for one seed via ``eval_toolkit`` (comparable to the headline)."""
    pos = np.concatenate(fold.pos_clusters[seed])
    neg = np.concatenate(fold.neg_clusters[seed])
    y = np.concatenate([np.ones(pos.size), np.zeros(neg.size)])
    s = np.concatenate([pos, neg])
    return float(metrics.roc_auc_point(y, s))


def _permuted_test_roc(fold: DialectFold, seed: int, rng: np.random.Generator) -> float:
    """One label-permutation null draw of the test ROC-AUC for one seed (presence-of-effect).

    Mirrors the §6.5 / carrier-LODO permutation construction: pool the seed's row scores, permute
    the labels (keeping the prevalence fixed), recompute the AUROC.
    """
    pos = np.concatenate(fold.pos_clusters[seed])
    neg = np.concatenate(fold.neg_clusters[seed])
    s = np.concatenate([pos, neg])
    y = np.concatenate([np.ones(pos.size), np.zeros(neg.size)])
    y_perm = rng.permutation(y)
    return _roc_auc_fast(y_perm, s)


def per_dialect_gap(
    fold: DialectFold, *, n_boot: int, n_perm: int, rng: np.random.Generator
) -> dict[str, Any]:
    """Point Gx + label-stratified-cluster bootstrap CI + per-fold permutation p for one dialect.

    Seed-aggregation mirrors ``falsify_carrier_lodo._rung_gap``: ``val_roc`` and point ``test_roc``
    are averaged over seeds; each bootstrap iteration averages one resampled ``test_roc`` per seed,
    holding the (fixed) mean ``val_roc``. ``Gx = mean_seed(val_roc) − mean_seed(test_roc)``.

    The permutation diagnostic is presence-of-transfer: permute the test labels per seed, recompute
    the null ``test_roc``; ``perm_p`` (one-sided) = fraction of null ``test_roc`` ≥ the observed
    ``test_roc`` (low ⇒ the detector transfers to the held-out dialect; high ⇒ a wall at chance).

    Returns
    -------
    dict
        ``val_roc, test_roc, Gx, ci_low, ci_high, perm_p, n_pos, n_neg, n_pos_clusters,
        n_neg_clusters``.
    """
    seeds = fold.seeds
    val_roc = float(np.mean([fold.val_roc[s] for s in seeds]))
    test_roc = float(np.mean([_point_test_roc(fold, s) for s in seeds]))
    gx_point = val_roc - test_roc

    # Label-stratified cluster bootstrap of the CI via the upstream primitive (library-first,
    # ADR-026/051): strata = ``{seed: (y, score, cluster_id)}``; positive- and negative-clusters
    # resampled separately (``resample_labels=(0, 1)``; criteria Rev 2 (b)); per-stratum metric =
    # the fast tie-corrected AUROC; ``combine`` = ``val_roc − mean over seeds of test_roc`` (val
    # held fixed). ``confidence=0.90`` ⇒ the 5th/95th-percentile bounds (one-sided 95%).
    strata: dict[Hashable, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    for s in seeds:
        pos = np.concatenate(fold.pos_clusters[s])
        neg = np.concatenate(fold.neg_clusters[s])
        score = np.concatenate([pos, neg])
        y = np.concatenate([np.ones(pos.size), np.zeros(neg.size)])
        pos_groups = np.concatenate(
            [np.full(c.size, f"p{i}", dtype=object) for i, c in enumerate(fold.pos_clusters[s])]
        )
        neg_groups = np.concatenate(
            [np.full(c.size, f"n{i}", dtype=object) for i, c in enumerate(fold.neg_clusters[s])]
        )
        groups = np.concatenate([pos_groups, neg_groups])
        strata[s] = (y, score, groups)

    def _combine(m: Mapping[Hashable, float]) -> float:
        return val_roc - float(np.mean(list(m.values())))

    ci = stratified_cluster_bootstrap_ci(
        strata,
        _roc_auc_fast,
        _combine,
        resample_labels=(0, 1),
        n_resamples=n_boot,
        confidence=0.90,
        rng=rng,
        n_jobs=1,
    )

    # Presence-of-transfer diagnostic (criteria Rev 2 (b), "presence-of-effect"): does the held-out
    # test_roc beat chance? Permute the test labels per seed, recompute the null test_roc; perm_p =
    # fraction of null test_roc >= the observed test_roc (one-sided upper). Low p => the detector
    # transfers to the held-out dialect; high p => a wall indistinguishable from chance. (NOT a gap
    # permutation: permuting labels drives test_roc to chance, which would trivially inflate a
    # val-test_null gap and make every perm_p ~= 1; the meaningful effect is transfer-vs-chance.)
    null_test_roc = np.empty(n_perm, dtype=float)
    for k in range(n_perm):
        null_test_roc[k] = float(np.mean([_permuted_test_roc(fold, s, rng) for s in seeds]))
    perm_p = float(np.mean(null_test_roc >= test_roc))

    s0 = seeds[0]
    n_pos = int(sum(c.size for c in fold.pos_clusters[s0]))
    n_neg = int(sum(c.size for c in fold.neg_clusters[s0]))
    return {
        "val_roc": val_roc,
        "test_roc": test_roc,
        "Gx": gx_point,
        "ci_low": float(ci.ci_low),
        "ci_high": float(ci.ci_high),
        "perm_p": perm_p,
        "n_pos": n_pos,
        "n_neg": n_neg,
        "n_pos_clusters": len(fold.pos_clusters[s0]),
        "n_neg_clusters": len(fold.neg_clusters[s0]),
        "n_seeds": len(seeds),
    }


def directional_table(
    results_dir: Path,
    dialect_folds: Sequence[str],
    *,
    rungs: Sequence[str] = RUNGS_CHEAP,
    n_boot: int = _N_BOOT,
    n_perm: int = _N_PERM,
    seed: int = 0,
) -> dict[str, Any]:
    """Per-dialect × per-rung directional Gx table (B2.3 — NO verdict, lora-gated at B3).

    Returns
    -------
    dict
        ``{"estimator","metric","note","n_boot","n_perm","rungs","per_rung":{rung:{fold:{...}}}}``.
    """
    rng = np.random.default_rng(seed)
    per_rung: dict[str, dict[str, Any]] = {}
    for rung in rungs:
        per_fold: dict[str, Any] = {}
        for fold_name in dialect_folds:
            fold = load_dialect_fold(results_dir, fold_name, rung)
            per_fold[fold_name] = per_dialect_gap(fold, n_boot=n_boot, n_perm=n_perm, rng=rng)
        per_rung[rung] = per_fold
    return {
        "estimator": (
            "dialect-LODO ROC-AUC gap Gx=val_roc-test_roc; label-stratified cluster bootstrap "
            "(positive- and negative-clusters resampled separately; criteria Rev 2 (b))"
        ),
        "metric": "roc_auc (prevalence-invariant)",
        "note": (
            "B2.3 directional read (cheap rungs tfidf+frozen only); NO verdict — the "
            "SURVIVES/FALSIFIED/SMALL-THROUGHOUT verdict is lora-gated (B3). Per-dialect "
            "permutation p is an uncorrected diagnostic (criteria Rev 2 (b))."
        ),
        "n_boot": n_boot,
        "n_perm": n_perm,
        "rungs": list(rungs),
        "per_rung": per_rung,
    }
