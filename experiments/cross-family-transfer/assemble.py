"""Arm-B multi-corpus assembly for the cross-family / within-indirect dialect-transfer study.

Loads the four Arm-B indirect dialects — **BIPIA** (email/code/table carriers pooled),
**browsesafe** (HTML pages), **fujitsu B1** (RAG-document poisoning), **InjecAgent**
(tool-output) — into ONE unified frame with the columns the dialect-LODO harness needs:

    text:str · label:int(0/1) · dialect:str · cluster_id:str

plus useful per-dialect metadata. Each dialect contributes a *natural cluster* id (the
pre-registered resampling unit, ``criteria.md`` §Resampling unit):

    bipia      → payload identity   (attack_type + payload-string index; ~70 clusters)
    browsesafe → per-page row id    (each row = one HTML page)
    fujitsu    → document id         (the B1 ``id`` GUID per document)
    injecagent → attacker-tool id    (the attacker tool the injected instruction calls)

Library-first (ADR-026): reuses the existing dialect loaders
(``experiments/eda/OOD_WALL_PREDICTION/bipia_carrier.build_examples`` and the on-disk
fujitsu/injecagent/browsesafe corpora under ``data/raw/``). No silent fallback — every
load failure raises with context.

Run a standalone shape check::

    uv run python experiments/cross-family-transfer/assemble.py
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
_OOD_DIR = REPO_ROOT / "experiments" / "eda" / "OOD_WALL_PREDICTION"
if str(_OOD_DIR) not in sys.path:
    sys.path.insert(0, str(_OOD_DIR))

from bipia_carrier import CARRIERS, build_examples  # noqa: E402

BIPIA_ROOT = REPO_ROOT / "data" / "raw" / "BIPIA" / "benchmark"
BROWSESAFE_DIR = REPO_ROOT / "data" / "raw" / "browsesafe"
FUJITSU_B1_JSONL = (
    REPO_ROOT
    / "data"
    / "raw"
    / "fujitsu_arag"
    / "data"
    / "attack_types"
    / "rag_poisoning_benchmark_combined_deduplicated.jsonl"
)
INJECAGENT_DIR = REPO_ROOT / "data" / "raw" / "injecagent"

# browsesafe head+tail truncation (criteria.md §Dialect units / E4): injections cluster at
# the page top/bottom (Sun et al. 2019), so keep ~6K head + 2K tail tokens. We approximate a
# token by ~4 characters (the load-shape is the registered knob, not an exact tokenizer).
_HEAD_TOKENS = 6_000
_TAIL_TOKENS = 2_000
_CHARS_PER_TOKEN = 4
_HEAD_CHARS = _HEAD_TOKENS * _CHARS_PER_TOKEN
_TAIL_CHARS = _TAIL_TOKENS * _CHARS_PER_TOKEN

_DIALECTS: tuple[str, ...] = ("bipia", "browsesafe", "fujitsu", "injecagent")

UNIFIED_COLUMNS: tuple[str, ...] = ("text", "label", "dialect", "cluster_id")


# --------------------------------------------------------------------------------------
# BIPIA
# --------------------------------------------------------------------------------------
def load_bipia(*, contexts_per_attack: int = 12, seed: int = 0) -> pd.DataFrame:
    """Load the BIPIA dialect (email/code/table carriers pooled).

    Reuses :func:`bipia_carrier.build_examples`. ``cluster_id`` is the *payload identity*
    (criteria.md: ~70 payloads = ~5 strings × 14 attack-types) — for a positive,
    ``attack_type::<payload-index>``; for a clean negative, ``clean::<carrier>`` (the
    negative's natural unit is its carrier-clean pool, not an attack payload).

    Returns
    -------
    pandas.DataFrame
        Columns ``text, label, dialect, cluster_id`` (+ ``attack_type, carrier, role``).
    """
    ex = build_examples(
        root=BIPIA_ROOT, contexts_per_attack=contexts_per_attack, carriers=CARRIERS, seed=seed
    )
    frame = ex.frame.copy()

    # payload index: deterministic per (attack_type, payload-string). The payload string is
    # the suffix after the final "\n\n" of a positive (bipia_carrier.inject template).
    payload_of = frame["text"].where(frame["label"] == 1).str.rsplit("\n\n", n=1).str[-1]
    payload_index: dict[tuple[str, str], int] = {}
    cluster_ids: list[str] = []
    for label, atype, carrier, payload in zip(
        frame["label"], frame["attack_type"], frame["carrier"], payload_of, strict=True
    ):
        if label == 1:
            key = (str(atype), str(payload))
            idx = payload_index.setdefault(key, len(payload_index))
            cluster_ids.append(f"{atype}::{idx}")
        else:
            cluster_ids.append(f"clean::{carrier}")
    frame["dialect"] = "bipia"
    frame["cluster_id"] = cluster_ids
    return frame[
        ["text", "label", "dialect", "cluster_id", "attack_type", "carrier", "role"]
    ].reset_index(drop=True)


# --------------------------------------------------------------------------------------
# browsesafe
# --------------------------------------------------------------------------------------
def _truncate_head_tail(text: str) -> str:
    """Head+tail truncation of a long HTML page (criteria.md §browsesafe).

    Keeps the first ``_HEAD_CHARS`` and last ``_TAIL_CHARS`` characters (a ~6K-head +
    2K-tail-token proxy at ~4 chars/token); short pages pass through unchanged.
    """
    s = str(text)
    if len(s) <= _HEAD_CHARS + _TAIL_CHARS:
        return s
    return s[:_HEAD_CHARS] + "\n…\n" + s[-_TAIL_CHARS:]


def load_browsesafe() -> pd.DataFrame:
    """Load the browsesafe dialect (HTML pages; label {no→0, yes→1}).

    Each row is one page → ``cluster_id`` = a per-page row id. The full HTML (``content``)
    is head+tail truncated. Reads the on-disk ``{train,test}.parquet``.

    Returns
    -------
    pandas.DataFrame
        Columns ``text, label, dialect, cluster_id``.
    """
    frames = []
    for split in ("train", "test"):
        path = BROWSESAFE_DIR / f"{split}.parquet"
        if not path.exists():
            raise FileNotFoundError(f"browsesafe parquet missing: {path}")
        df = pd.read_parquet(path)
        if not {"content", "label"} <= set(df.columns):
            raise ValueError(f"browsesafe {split}: expected content/label, got {list(df.columns)}")
        df = df.copy()
        df["_split"] = split
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)

    label_map = {"no": 0, "yes": 1}
    bad = set(df["label"].astype(str).unique()) - set(label_map)
    if bad:
        raise ValueError(f"browsesafe: unexpected label values {bad}")
    out = pd.DataFrame(
        {
            "text": df["content"].astype(str).map(_truncate_head_tail),
            "label": df["label"].astype(str).map(label_map).astype(int),
            "dialect": "browsesafe",
            "cluster_id": [f"page::{s}::{i}" for i, s in enumerate(df["_split"])],
        }
    )
    return out.reset_index(drop=True)


# --------------------------------------------------------------------------------------
# fujitsu B1
# --------------------------------------------------------------------------------------
def _first_benign(raw: object) -> str | None:
    """Recover a single benign-document string from a B1 ``benign_content`` field.

    The local jsonl persists ``benign_content`` as a Python list-repr string
    (``"['doc1', 'doc2']"``); take the first non-empty element. Plain strings pass through.
    """
    if raw is None:
        return None
    if isinstance(raw, list):
        items = raw
    elif isinstance(raw, str):
        s = raw.strip()
        if s.startswith("["):
            try:
                items = ast.literal_eval(s)
            except (ValueError, SyntaxError):
                return s or None
        else:
            return s or None
    else:
        return None
    for it in items:
        if it and str(it).strip():
            return str(it)
    return None


def load_fujitsu() -> pd.DataFrame:
    """Load the fujitsu B1 RAG-document dialect (poison_content=1 / benign_content=0).

    Reads the on-disk ``rag_poisoning_benchmark_combined_deduplicated.jsonl`` (the
    materialized B1 config), which natively carries the per-document ``id`` GUID — so
    ``source_id`` is **already present** (used as ``cluster_id``; no re-persist needed; see
    the deviations note). EXCLUDES the augmented configs (in ``external_augmented/``, never
    read here) and SKIPS the B2 image modality. Each document contributes one positive
    (``poison_content``) and, when present, one matched negative (``benign_content``).

    Returns
    -------
    pandas.DataFrame
        Columns ``text, label, dialect, cluster_id`` (+ ``attack_category``).
    """
    if not FUJITSU_B1_JSONL.exists():
        raise FileNotFoundError(f"fujitsu B1 jsonl missing: {FUJITSU_B1_JSONL}")
    rows: list[dict[str, object]] = []
    with FUJITSU_B1_JSONL.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            doc_id = d.get("id")
            if not doc_id:
                raise ValueError("fujitsu B1 row missing 'id' (the document/source id)")
            cid = f"doc::{doc_id}"
            cat = d.get("attack_category", "")
            poison = d.get("poison_content")
            if poison and str(poison).strip():
                rows.append(
                    {
                        "text": str(poison),
                        "label": 1,
                        "dialect": "fujitsu",
                        "cluster_id": cid,
                        "attack_category": cat,
                    }
                )
            benign = _first_benign(d.get("benign_content"))
            if benign and benign.strip():
                rows.append(
                    {
                        "text": benign,
                        "label": 0,
                        "dialect": "fujitsu",
                        "cluster_id": cid,
                        "attack_category": cat,
                    }
                )
    if not rows:
        raise ValueError("fujitsu B1: no rows assembled")
    return pd.DataFrame(rows).reset_index(drop=True)


# --------------------------------------------------------------------------------------
# InjecAgent
# --------------------------------------------------------------------------------------
def _load_attacker_tool_map() -> dict[str, str]:
    """Map each attacker *instruction* → its attacker tool id (first tool in the case).

    Parsed from ``attacker_cases_{dh,ds}.jsonl`` (criteria.md: tool-output / attack-id is
    the cluster). The derived rows embed the instruction as a prefix, so the join is by
    instruction substring.
    """
    mapping: dict[str, str] = {}
    for fn in ("attacker_cases_dh.jsonl", "attacker_cases_ds.jsonl"):
        path = INJECAGENT_DIR / fn
        if not path.exists():
            raise FileNotFoundError(f"injecagent attacker cases missing: {path}")
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            instr = str(d["Attacker Instruction"]).strip()
            tools = d.get("Attacker Tools") or []
            if isinstance(tools, str):
                try:
                    tools = ast.literal_eval(tools)
                except (ValueError, SyntaxError):
                    tools = [tools]
            tool_id = str(tools[0]) if tools else "UNKNOWN_TOOL"
            mapping[instr] = tool_id
    if not mapping:
        raise ValueError("injecagent: no attacker instructions parsed")
    return mapping


def _tool_for_text(text: str, instr_to_tool: dict[str, str]) -> str:
    """Tool id for a derived InjecAgent row by matching its embedded attacker instruction.

    The derived ``text`` is ``"<attacker instruction>\\n\\n<tool response>"``; match by the
    instruction prefix (longest matching instruction wins to avoid short-prefix collisions).
    """
    head = text.split("\n\n", 1)[0].strip()
    if head in instr_to_tool:
        return instr_to_tool[head]
    best = ""
    for instr in instr_to_tool:
        if instr and text.startswith(instr) and len(instr) > len(best):
            best = instr
    if best:
        return instr_to_tool[best]
    raise ValueError(f"injecagent: no attacker tool matched for text prefix {head[:60]!r}")


def _benign_user_cases() -> list[tuple[str, str]]:
    """Real benign tool-output negatives, one per InjecAgent user-case (criteria.md Revision 2).

    InjecAgent ships 17 canonical benign user scenarios in ``user_cases.jsonl`` (distinct
    ``User Tool``s). Each ``Tool Response Template`` carries an ``<Attacker Instruction>``
    placeholder; removing it yields the clean tool output a benign agent would observe. These 17
    real responses are the negatives, **each its own per-``User Tool`` cluster** (17 negative
    clusters, not one) so the label-stratified cluster bootstrap can represent negative-side
    variability. (Revision 2 supersedes the earlier reconstruct-from-test-cases approach, which
    collapsed all negatives into a single degenerate cluster.)

    Returns
    -------
    list[tuple[str, str]]
        ``(benign_text, user_tool)`` pairs, one per user-case.
    """
    path = INJECAGENT_DIR / "user_cases.jsonl"
    if not path.exists():
        raise FileNotFoundError(f"injecagent user cases missing: {path}")
    out: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        c = json.loads(line)
        tool = str(c.get("User Tool", "")).strip()
        tmpl = str(c.get("Tool Response Template", ""))
        clean = tmpl.replace("<Attacker Instruction>", "").strip()
        if not tool or not clean:
            raise ValueError(f"injecagent user-case missing User Tool / benign response: {c!r}")
        out.append((clean, tool))
    if not out:
        raise ValueError("injecagent: no benign user-cases parsed")
    return out


def load_injecagent() -> pd.DataFrame:
    """Load the InjecAgent tool-output dialect.

    Positives: the on-disk ``injecagent_derived.parquet`` (the canonical static text slate,
    all label=1). ``cluster_id`` = the attacker tool id, derived by joining each row's
    embedded attacker instruction to ``attacker_cases_{dh,ds}.jsonl``. Negatives: the 17 real
    benign user-cases (``user_cases.jsonl``), each its clean ``Tool Response Template`` with the
    attacker placeholder removed; ``cluster_id`` = ``clean::<User Tool>`` (17 per-tool negative
    clusters; criteria.md Revision 2).

    Returns
    -------
    pandas.DataFrame
        Columns ``text, label, dialect, cluster_id`` (+ ``attack_type``).
    """
    pos_path = INJECAGENT_DIR / "injecagent_derived.parquet"
    if not pos_path.exists():
        raise FileNotFoundError(f"injecagent derived parquet missing: {pos_path}")
    df = pd.read_parquet(pos_path)
    if "text" not in df.columns:
        raise ValueError(f"injecagent derived: expected 'text', got {list(df.columns)}")

    instr_to_tool = _load_attacker_tool_map()
    pos = pd.DataFrame(
        {
            "text": df["text"].astype(str),
            "label": 1,
            "dialect": "injecagent",
            "cluster_id": [
                f"tool::{_tool_for_text(t, instr_to_tool)}" for t in df["text"].astype(str)
            ],
            "attack_type": df.get("attack_type", pd.Series([""] * len(df))).astype(str),
        }
    )
    benign = _benign_user_cases()
    neg = pd.DataFrame(
        {
            "text": [t for t, _ in benign],
            "label": 0,
            "dialect": "injecagent",
            "cluster_id": [f"clean::{tool}" for _, tool in benign],
            "attack_type": "",
        }
    )
    return pd.concat([pos, neg], ignore_index=True)


# --------------------------------------------------------------------------------------
# unified assembly
# --------------------------------------------------------------------------------------
def assemble(*, contexts_per_attack: int = 12, seed: int = 0) -> pd.DataFrame:
    """Assemble all four Arm-B dialects into one unified frame.

    Returns
    -------
    pandas.DataFrame
        Columns include :data:`UNIFIED_COLUMNS` plus per-dialect metadata (NaN where a
        dialect does not carry a given column).
    """
    parts = [
        load_bipia(contexts_per_attack=contexts_per_attack, seed=seed),
        load_browsesafe(),
        load_fujitsu(),
        load_injecagent(),
    ]
    frame = pd.concat(parts, ignore_index=True)
    for col in UNIFIED_COLUMNS:
        if col not in frame.columns:
            raise ValueError(f"unified frame missing required column {col!r}")
    frame["label"] = frame["label"].astype(int)
    frame["cluster_id"] = frame["cluster_id"].astype(str)
    missing_dialects = set(_DIALECTS) - set(frame["dialect"].unique())
    if missing_dialects:
        raise ValueError(f"assembled frame missing dialects: {sorted(missing_dialects)}")
    return frame


def _summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Per-dialect rows / label balance / cluster count summary."""
    rows = []
    for d, sub in frame.groupby("dialect"):
        rows.append(
            {
                "dialect": d,
                "rows": len(sub),
                "pos": int((sub["label"] == 1).sum()),
                "neg": int((sub["label"] == 0).sum()),
                "clusters": sub["cluster_id"].nunique(),
            }
        )
    return pd.DataFrame(rows).set_index("dialect")


if __name__ == "__main__":
    fr = assemble()
    print(_summary(fr).to_string())
    print(f"\ntotal rows={len(fr)} dialects={sorted(fr['dialect'].unique())}")
