"""C1 corpus builder: benign synthetic tables -> injected train-augmentation rows.

Consumes the ``dataset_synthesize`` output (``corpus_raw/samples.jsonl`` — BENIGN
table contexts only) and mechanically constructs the C1 treated-arm corpus per the
ratified ``criteria.md``:

- **Positives** = each kept context suffix-injected (``bipia_carrier.inject``,
  the fold's own ``f"{context}\\n\\n{attack}"`` template) with payloads from the
  SAME BIPIA pool the carrier-LODO fold already uses (train+test splits,
  ``load_attack_pools``; payloads are NOT held out on the carrier axis) —
  balanced across attack types via a seeded shuffled round-robin.
- **Negatives** = every kept context once, clean (the Mirror lesson, audit W12:
  same generator, same formats, same volume order).

Rows carry the ``bipia_carrier`` frame schema (text/label/attack_type/subfamily/
carrier/position/role/source) plus ``format``; ``source`` is ``synthetic_inject``
/ ``synthetic_clean`` so fold construction can never misroute them (augmentation
happens AFTER the fold builder; these rows join ``fold.train`` only).

Hygiene before injection: strip accidental code fences, per-format sanity checks
(markdown ``|`` / csv comma+rows / html ``<table``), exact-normalized dedup
(library ``normalize_text_for_dedup`` + ``sha256_text``).

Writes ``corpus.parquet`` + ``corpus_build.json`` (machine record: counts, drops,
sha256s, recipe/jsonl provenance). Deterministic given (samples.jsonl, --seed).

Run::

    uv run python experiments/carrier-table-training/build_corpus.py \
        [--raw corpus_raw/] [--seed 0] [--payloads-per-context 3]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_OOD_DIR = _HERE.parent / "eda" / "OOD_WALL_PREDICTION"
if str(_OOD_DIR) not in sys.path:
    sys.path.insert(0, str(_OOD_DIR))

from bipia_carrier import (  # noqa: E402  # type: ignore[import-not-found]
    inject,
    load_attack_pools,
    subfamily,
)

REPO_ROOT = _HERE.parent.parent
BIPIA_ROOT = REPO_ROOT / "data" / "raw" / "BIPIA" / "benchmark"


def _strip_fences(text: str) -> str:
    """Remove a single wrapping ``` code fence (with optional language tag) if present."""
    t = text.strip()
    if t.startswith("```") and t.endswith("```"):
        body = t[3:-3]
        first_nl = body.find("\n")
        if first_nl != -1 and " " not in body[:first_nl].strip():
            body = body[first_nl + 1 :]
        return body.strip()
    return t


def _format_ok(text: str, fmt: str) -> bool:
    """Cheap per-format sanity check on a generated context."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if fmt == "markdown":
        return text.count("|") >= 6 and len(lines) >= 3
    if fmt == "csv":
        return text.count(",") >= 4 and len(lines) >= 3
    if fmt == "html":
        return "<table" in text.lower() and "</table>" in text.lower()
    return False


def load_contexts_from_raw(raw_dir: Path) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Read samples.jsonl -> kept context dicts + drop accounting.

    Returns (contexts, drops) where each context dict has ``text`` (cleaned) and
    ``format``; ``drops`` counts rows removed per reason.
    """
    from eval_toolkit.text_dedup import normalize_text_for_dedup, sha256_text

    jsonl_path = raw_dir / "samples.jsonl"
    if not jsonl_path.exists():
        raise FileNotFoundError(f"no samples.jsonl under {raw_dir} — run dataset_synthesize first")

    drops = {"empty": 0, "format": 0, "exact_dup": 0}
    kept: list[dict[str, Any]] = []
    seen: set[str] = set()
    for line in jsonl_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        fmt = str(row.get("metadata", {}).get("format", ""))
        text = _strip_fences(str(row.get("content", "")))
        if not text:
            drops["empty"] += 1
            continue
        if not _format_ok(text, fmt):
            drops["format"] += 1
            continue
        h = sha256_text(normalize_text_for_dedup(text))
        if h in seen:
            drops["exact_dup"] += 1
            continue
        seen.add(h)
        kept.append({"text": text, "format": fmt})
    return kept, drops


def payload_pool(root: Path) -> list[tuple[str, str]]:
    """The fold's full payload pool: (attack_type, attack_string), both splits, sorted."""
    pool: list[tuple[str, str]] = []
    for split in ("train", "test"):
        for atype, strings in load_attack_pools(split, root=root).items():
            pool.extend((atype, s) for s in strings)
    return sorted(set(pool))


def build_rows(
    contexts: list[dict[str, Any]],
    pool: list[tuple[str, str]],
    *,
    payloads_per_context: int,
    seed: int,
) -> pd.DataFrame:
    """Construct the corpus frame: 1 clean negative + k injected positives per context.

    Payload assignment is a seeded shuffled round-robin over the full pool so
    attack types stay balanced; re-shuffles each cycle if the pool is exhausted.
    """
    from eval_toolkit.text_dedup import normalize_text_for_dedup, sha256_text

    rng = np.random.default_rng(seed)
    order = rng.permutation(len(pool))
    cursor = 0

    def _next_payload() -> tuple[str, str]:
        nonlocal cursor, order
        if cursor >= len(order):
            order = rng.permutation(len(pool))
            cursor = 0
        atype, attack = pool[int(order[cursor])]
        cursor += 1
        return atype, attack

    rows: list[dict[str, Any]] = []
    for ctx in contexts:
        ctx_sha = sha256_text(normalize_text_for_dedup(str(ctx["text"])))
        rows.append(
            {
                "text": ctx["text"],
                "context_sha256": ctx_sha,
                "label": 0,
                "attack_type": "",
                "subfamily": "benign",
                "carrier": "table",
                "position": "none",
                "role": "train",
                "source": "synthetic_clean",
                "format": ctx["format"],
            }
        )
        for _ in range(payloads_per_context):
            atype, attack = _next_payload()
            rows.append(
                {
                    "text": inject(ctx["text"], attack),
                    "context_sha256": ctx_sha,
                    "label": 1,
                    "attack_type": atype,
                    "subfamily": subfamily(atype),
                    "carrier": "table",
                    "position": "suffix",
                    "role": "train",
                    "source": "synthetic_inject",
                    "format": ctx["format"],
                }
            )
    return pd.DataFrame(rows)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build the C1 treated-arm corpus parquet.")
    ap.add_argument("--raw", type=Path, default=_HERE / "corpus_raw")
    ap.add_argument("--out", type=Path, default=_HERE / "corpus.parquet")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--payloads-per-context", type=int, default=3)
    args = ap.parse_args(argv)

    contexts, drops = load_contexts_from_raw(args.raw)
    if not contexts:
        print("build_corpus: 0 usable contexts — nothing to build", file=sys.stderr)
        return 1
    pool = payload_pool(BIPIA_ROOT)
    frame = build_rows(
        contexts, pool, payloads_per_context=args.payloads_per_context, seed=args.seed
    )
    frame.to_parquet(args.out, index=False)

    jsonl_path = args.raw / "samples.jsonl"
    record = {
        "version": "1",
        "seed": args.seed,
        "payloads_per_context": args.payloads_per_context,
        "contexts_kept": len(contexts),
        "contexts_by_format": frame.loc[frame["label"] == 0, "format"]
        .value_counts()
        .to_dict(),
        "drops": drops,
        "positives": int((frame["label"] == 1).sum()),
        "negatives": int((frame["label"] == 0).sum()),
        "attack_types_used": int(frame.loc[frame["label"] == 1, "attack_type"].nunique()),
        "payload_pool_size": len(pool),
        "samples_jsonl_sha256": hashlib.sha256(jsonl_path.read_bytes()).hexdigest(),
        "corpus_parquet_sha256": hashlib.sha256(args.out.read_bytes()).hexdigest(),
    }
    (_HERE / "corpus_build.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"build_corpus: kept {len(contexts)} contexts "
        f"(drops {drops}) -> {record['positives']} pos + {record['negatives']} neg; "
        f"{record['attack_types_used']} attack types; wrote {args.out.name}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
