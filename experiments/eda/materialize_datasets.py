"""Materialize the in-scope dataset universe to ``data/raw/`` as a reproducible local corpus.

The "full materialize" round (2026-06-02): persist every accessible dataset to the **gitignored**
``data/raw/`` (HF snapshot / git clone / Tier-3 derivation), quarantine the unlicensed sets under
``_eda_only_unlicensed/``, and emit ``data/raw/MANIFEST.json``. Tier-4 (execution-only) and Tier-5
(unavailable) datasets are recorded as manifest rows but not fetched.

Library-first (ADR-026): reuses ``configs/data/dataset_specs.yml`` (the verified spec list) +
``huggingface_hub.snapshot_download`` (raw parquet/csv — smallest + reproducible) — no bespoke download
logic. License/tier facts are the 2026-06-02 acquisition re-verify (HackAPrompt=MIT; Gandalf/Mosscap
unlicensed; InjecAgent ships static test cases). See ``docs/planning/dataset-acquisition-deep-dive-2026-06.md``.

Run (local; GBs + LLMail derivation ⇒ background)::

    uv run python experiments/eda/materialize_datasets.py --out data/raw          # core
    uv run python experiments/eda/materialize_datasets.py --out data/raw --build-bipia   # + BIPIA qa/abstract
"""

from __future__ import annotations

import argparse
import json
import subprocess
import urllib.request
from pathlib import Path

REPO = Path.cwd()

# --- HF snapshot sets (Tier 1 permissive + Tier 2 unlicensed). rev pins the HF SHA where known. ---
HF_SNAPSHOT: list[dict] = [
    # Tier 1 — permissive, → data/raw/<key>/
    dict(
        key="deepset",
        hf_id="deepset/prompt-injections",
        rev="4f61ecb038e9",
        tier=1,
        license="Apache-2.0",
        eda_only=False,
    ),
    dict(
        key="jackhhao",
        hf_id="jackhhao/jailbreak-classification",
        rev="2f2ceeb39658",
        tier=1,
        license="Apache-2.0",
        eda_only=False,
    ),
    dict(
        key="promptshield",
        hf_id="hendzh/PromptShield",
        rev="a5234cb1f5cd",
        tier=1,
        license="Apache-2.0",
        eda_only=False,
    ),
    dict(
        key="guychuk",
        hf_id="guychuk/benign-malicious-prompt-classification",
        rev="e13090643e6f",
        tier=1,
        license="Apache-2.0",
        eda_only=False,
    ),
    dict(
        key="toxicchat",
        hf_id="lmsys/toxic-chat",
        rev="29df8e4dba60",
        tier=1,
        license="CC-BY-NC-4.0",
        eda_only=False,
        note="non-commercial",
    ),
    dict(
        key="spml",
        hf_id="reshabhs/SPML_Chatbot_Prompt_Injection",
        rev="02ce8084e979",
        tier=1,
        license="MIT",
        eda_only=False,
    ),
    dict(
        key="shen_dan",
        hf_id="TrustAIRLab/in-the-wild-jailbreak-prompts",
        rev="a10aab8eff1c",
        tier=1,
        license="MIT",
        eda_only=False,
    ),
    dict(
        key="notinject",
        hf_id="leolee99/NotInject",
        rev="847ae76cf8fe",
        tier=1,
        license="MIT",
        eda_only=False,
    ),
    dict(
        key="xstest",
        hf_id="walledai/XSTest",
        rev=None,
        tier=1,
        license="CC-BY-4.0",
        eda_only=False,
        note="canonical (replaced natolambert/xstest-v2-copy mirror 2026-06-03; gate accepted)",
    ),
    dict(
        key="orbench",
        hf_id="bench-llm/or-bench",
        rev=None,
        tier=1,
        license="CC-BY-4.0",
        eda_only=False,
    ),
    dict(
        key="gentelbench",
        hf_id="GenTelLab/gentelbench-v1",
        rev="bf27033065d7",
        tier=1,
        license="Apache-2.0",
        eda_only=False,
    ),
    dict(
        key="hackaprompt",
        hf_id="hackaprompt/hackaprompt-dataset",
        rev="25b87fbedfb8",
        tier=1,
        license="MIT",
        eda_only=False,
        note="label=attack-success (different task)",
    ),
    dict(
        key="wildguardmix",
        hf_id="allenai/wildguardmix",
        rev=None,
        tier=1,
        license="ODC-By",
        eda_only=False,
        note="gated — gate cleared 2026-06; spec marked it excluded (stale)",
    ),
    dict(
        key="jbb",
        hf_id="JailbreakBench/JBB-Behaviors",
        rev=None,
        tier=1,
        license="MIT",
        eda_only=False,
        note="cross-family TEST anchor; was cached-unanalyzed",
    ),
    # Phase-2 expansion (2026-06-03) — live-verified keepers; roles PENDING_EDA (no spec/role until EDA gate).
    dict(
        key="neuralchemy",
        hf_id="neuralchemy/Prompt-injection-dataset",
        rev=None,
        tier=1,
        license="Apache-2.0",
        eda_only=False,
        note="cfg 'core' (4.4K) for EDA / full=14K; binary text/label; has source+group_id (leakage-checkable). rev unpinned for EDA gate.",
    ),
    dict(
        key="aegis2",
        hf_id="nvidia/Aegis-AI-Content-Safety-Dataset-2.0",
        rev=None,
        tier=1,
        license="CC-BY-4.0",
        eda_only=False,
        note="corrected id 2026-06-03 (handoff 'nvidia/Aegis-2.0' 404s); 33.4K; feature prompt → prompt_label(str→map).",
    ),
    dict(
        key="falsereject",
        hf_id="AmazonScience/FalseReject",
        rev=None,
        tier=1,
        license="CC-BY-NC-4.0",
        eda_only=False,
        note="non-commercial (like toxicchat); benign over-refusal control (all-benign, no binary label); feature prompt; 15.8K.",
    ),
    dict(
        key="browsesafe",
        hf_id="perplexity-ai/browsesafe-bench",
        rev=None,
        tier=1,
        license="MIT",
        eda_only=False,
        note="indirect-HTML carrier axis; content(full HTML ~190MB) → label(str→map); 14.7K; dual-rep at EDA (raw E2 / stripped E4).",
    ),
    dict(
        key="jailbreakdb",
        hf_id="youbin2014/JailbreakDB",
        rev=None,
        tier=1,
        license="CC-BY-4.0",
        eda_only=False,
        note="14-source aggregate; 2 raw CSVs ~12.3M rows (Viewer 500s; snapshot pulls files directly); user_prompt+jailbreak(0/1); source col=provenance. LARGE.",
    ),
    dict(
        key="fujitsu_arag",
        hf_id="Fujitsu/agentic-rag-redteam-bench",
        rev=None,
        tier=1,
        license="CC-BY-4.0",
        eda_only=False,
        note="ART-SafeBench v2.0.0 (gate GRANTED 2026-06-03; handoff id 'Fujitsu/agentic-rag' 404s). RAG-injection/"
        "poisoning: B1 poison_content/benign_content + B4 malicious/benign + B3 PI queries; multimodal (B2 image). "
        "source_datasets ⊃ jbb/gandalf/injecagent/tensortrust/harmbench → LEAKAGE-GATE before any role.",
    ),
    # Tier 2 — UNLICENSED, → data/raw/_eda_only_unlicensed/<key>/  (loadable != licensed)
    dict(
        key="xtram1",
        hf_id="xTRam1/safe-guard-prompt-injection",
        rev="a3a877d608f3",
        tier=2,
        license="none",
        eda_only=True,
    ),
    dict(
        key="jayavibhav",
        hf_id="jayavibhav/prompt-injection",
        rev="a5bd9869c16d",
        tier=2,
        license="none",
        eda_only=True,
    ),
    dict(
        key="jayavibhav_safety",
        hf_id="jayavibhav/prompt-injection-safety",
        rev=None,
        tier=2,
        license="none",
        eda_only=True,
        note="3-class",
    ),
    dict(
        key="mosscap",
        hf_id="Lakera/mosscap_prompt_injection",
        rev=None,
        tier=1,
        license="MIT",
        eda_only=False,
        note="MIT (corrected 2026-06-03; a probe-bug had read None); cross-family TRAIN anchor",
    ),
    dict(
        key="gandalf_ignore",
        hf_id="Lakera/gandalf_ignore_instructions",
        rev=None,
        tier=1,
        license="MIT",
        eda_only=False,
        note="MIT (corrected 2026-06-03); cross-family TRAIN anchor",
    ),
    dict(
        key="gandalf_summ",
        hf_id="Lakera/gandalf_summarization",
        rev=None,
        tier=1,
        license="MIT",
        eda_only=False,
        note="MIT (corrected 2026-06-03)",
    ),
    dict(
        key="tensortrust",
        hf_id="qxcv/tensor-trust",
        alt_ids=["ai-ml-ops-eng/tensortrust-datasets"],
        rev=None,
        tier=2,
        license="none",
        eda_only=True,
    ),
]

# --- Tier 4 (execution/environment only) + Tier 5 (unavailable, double-checked 2026-06-02): record, do NOT fetch. ---
RECORD_ONLY: list[dict] = [
    dict(
        key="open_prompt_injection",
        source="github.com/liu00222/Open-Prompt-Injection",
        tier=4,
        license="MIT",
        status="needs_execution",
        note="toolkit: system-prompt templates only; rows generated at runtime",
    ),
    dict(
        key="agentdojo",
        source="pip/github AgentDojo",
        tier=4,
        license="MIT",
        status="needs_execution",
        note="agent environment, not (text,label)",
    ),
    dict(
        key="agent_security_bench",
        source="github Agent-Security-Bench",
        tier=4,
        license="MIT",
        status="needs_execution",
        note="ASR framework; outputs metrics not rows",
    ),
    dict(
        key="wasp",
        source="github.com/facebookresearch/wasp",
        tier=4,
        license="CC-BY-NC-4.0",
        status="needs_execution",
        note="Docker web-agent sandbox; non-commercial",
    ),
    dict(
        key="piguard",
        source="leolee99/PIGuard",
        tier=1,
        license="MIT",
        status="available_not_fetched",
        note="MIT but BUNDLES BIPIA_text/code.json → LEAKAGE vs any BIPIA test; fetch only with explicit exclude",
    ),
    dict(
        key="harelix",
        source="Harelix/Prompt-Injection-Mixed-Techniques-2024",
        tier=5,
        license="-",
        status="unavailable_404",
        note="404 re-confirmed live 2026-06-02 (a web-cache snapshot misreports it live)",
    ),
    dict(
        key="pint",
        source="github.com/lakeraai/pint-benchmark",
        tier=5,
        license="harness MIT",
        status="unavailable_withheld",
        note="ships only example-dataset.yaml; data request-only via opensource@lakera.ai",
    ),
    dict(
        key="indirect_in_the_wild",
        source="arXiv:2604.27202 (+ confusable 2601.07072)",
        tier=5,
        license="none stated",
        status="unavailable_no_release",
        note="no public data, no stated release plan (re-checked 2026-06-02); author contact only",
    ),
]

_README = """# UNLICENSED datasets — INTERNAL EDA ONLY

These load but carry NO license artifact (all-rights-reserved by default). **Loadable != licensed.**
Use ONLY for internal exploratory analysis. Do NOT redistribute, and CLEAR the license (author contact)
before any published benchmark/model/artifact.

Members (re-verified 2026-06-03): xTRam1/safe-guard, jayavibhav/prompt-injection,
jayavibhav/prompt-injection-safety, Tensor Trust, WAInjectBench. (The Lakera sets gandalf_ignore /
gandalf_summarization / mosscap were briefly here but are MIT → relocated to data/raw/.)

See docs/planning/dataset-acquisition-deep-dive-2026-06.md (bucket B).
"""


def dir_bytes(d: Path) -> int:
    """Total bytes of all files under ``d`` (0 if absent)."""
    return sum(f.stat().st_size for f in d.rglob("*") if f.is_file()) if d.exists() else 0


def count_rows(d: Path) -> int | None:
    """Best-effort row count: parquet footer metadata, else line/array count. None on failure."""
    pqs = list(d.rglob("*.parquet"))
    if pqs:
        try:
            import pyarrow.parquet as pq

            return int(sum(pq.ParquetFile(p).metadata.num_rows for p in pqs))
        except Exception:  # noqa: BLE001 — counting is advisory; never abort the batch
            return None
    total, found = 0, False
    for ext in ("*.csv", "*.jsonl", "*.json"):
        for p in d.rglob(ext):
            found = True
            try:
                if p.suffix == ".json":
                    obj = json.loads(p.read_text(encoding="utf-8"))
                    total += len(obj) if isinstance(obj, list) else 1
                else:
                    n = sum(1 for _ in p.open("r", encoding="utf-8", errors="ignore"))
                    total += max(0, n - 1) if p.suffix == ".csv" else n
            except Exception:  # noqa: BLE001
                return None
    return total if found else None


def snapshot_one(desc: dict, out_root: Path) -> dict:
    """Snapshot-download one HF dataset (trying ``alt_ids`` on failure); record a manifest row."""
    from huggingface_hub import snapshot_download

    sub = "_eda_only_unlicensed" if desc["eda_only"] else ""
    dest = out_root / sub / desc["key"]
    rec = dict(
        key=desc["key"],
        source=desc["hf_id"],
        tier=desc["tier"],
        license=desc["license"],
        eda_only=desc["eda_only"],
        note=desc.get("note", ""),
        local_path=str(dest.relative_to(REPO)),
    )
    if dest.exists() and any(dest.iterdir()):  # idempotent: skip re-download
        rec.update(status="ok_cached", n_rows=count_rows(dest), bytes=dir_bytes(dest))
        return rec
    for hf_id in [desc["hf_id"], *desc.get("alt_ids", [])]:
        try:
            snapshot_download(
                repo_id=hf_id, repo_type="dataset", revision=desc.get("rev"), local_dir=str(dest)
            )
            rec.update(source=hf_id, status="ok", n_rows=count_rows(dest), bytes=dir_bytes(dest))
            return rec
        except Exception as exc:  # noqa: BLE001 — try alts, then record the failure (no silent drop)
            last = f"{type(exc).__name__}: {str(exc)[:120]}"
    rec.update(status=f"FAIL: {last}", n_rows=None, bytes=dir_bytes(dest))
    return rec


def derive_llmail(out_root: Path) -> dict:
    """Tier-3: stream microsoft/llmail-inject-challenge; persist (text, objectives, defense_undetected)."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    from datasets import get_dataset_config_names, load_dataset

    repo = "microsoft/llmail-inject-challenge"
    dest = out_root / "llmailinject2025microsoft"
    dest.mkdir(parents=True, exist_ok=True)
    rec = dict(
        key="llmail",
        source=repo,
        tier=3,
        license="MIT",
        eda_only=False,
        note="text=subject+body; label=defense.undetected (parsed); all rows are attacks",
        local_path=str(dest.relative_to(REPO)),
    )
    if (dest / "llmail_derived.parquet").exists():  # idempotent: skip re-derive
        rec.update(status="ok_cached", n_rows=count_rows(dest), bytes=dir_bytes(dest))
        return rec
    try:
        configs = get_dataset_config_names(repo) or [None]
        path = dest / "llmail_derived.parquet"
        writer, n = None, 0
        buf: dict[str, list] = {
            "text": [],
            "objectives": [],
            "defense_undetected": [],
            "is_attack": [],
        }

        def flush() -> None:
            nonlocal writer
            tbl = pa.table(buf)
            if writer is None:
                writer = pq.ParquetWriter(path, tbl.schema)
            writer.write_table(tbl)
            for v in buf.values():
                v.clear()

        for cfg in configs:
            dd = load_dataset(repo, cfg, streaming=True)
            for _split, it in dd.items():
                for row in it:
                    obj = row.get("objectives")
                    try:
                        parsed = json.loads(obj) if isinstance(obj, str) else (obj or {})
                        und = (
                            bool(parsed.get("defense.undetected"))
                            if isinstance(parsed, dict)
                            else None
                        )
                    except Exception:  # noqa: BLE001
                        und = None
                    text = f"{row.get('subject') or ''}\n\n{row.get('body') or ''}".strip()
                    buf["text"].append(text)
                    buf["objectives"].append(str(obj))
                    buf["defense_undetected"].append(und)
                    buf["is_attack"].append(1)
                    n += 1
                    if n % 50000 == 0:
                        flush()
        if buf["text"]:
            flush()
        if writer is not None:
            writer.close()
        rec.update(status="ok", n_rows=n, bytes=dir_bytes(dest))
    except Exception as exc:  # noqa: BLE001
        rec.update(
            status=f"FAIL: {type(exc).__name__}: {str(exc)[:140]}",
            n_rows=None,
            bytes=dir_bytes(dest),
        )
    return rec


def fetch_injecagent(out_root: Path) -> dict:
    """Tier-3: pull InjecAgent's STATIC test/attacker case files (no agent run) → (text, attack_type)."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    dest = out_root / "injecagent"
    dest.mkdir(parents=True, exist_ok=True)
    base = "https://raw.githubusercontent.com/uiuc-kang-lab/InjecAgent/main/data/"
    files = [
        "test_cases_dh_base.json",
        "test_cases_dh_enhanced.json",
        "test_cases_ds_base.json",
        "test_cases_ds_enhanced.json",
        "attacker_cases_dh.jsonl",
        "attacker_cases_ds.jsonl",
        "user_cases.jsonl",
    ]
    rec = dict(
        key="injecagent",
        source="uiuc-kang-lab/InjecAgent",
        tier=3,
        license="MIT",
        eda_only=False,
        note="static test cases (full ASR still needs execution)",
        local_path=str(dest.relative_to(REPO)),
    )
    if (dest / "injecagent_derived.parquet").exists():  # idempotent: skip re-fetch
        rec.update(status="ok_cached", n_rows=count_rows(dest), bytes=dir_bytes(dest))
        return rec
    try:
        for f in files:
            urllib.request.urlretrieve(base + f, dest / f)  # noqa: S310 — fixed trusted GitHub raw URL
        rows: list[dict] = []
        for f in files:
            if not f.startswith("test_cases"):
                continue
            for r in json.loads((dest / f).read_text(encoding="utf-8")):
                tool_resp = r.get("Tool Response Template", r.get("Tool Response", ""))
                instr = r.get("Attacker Instruction", "")
                # W2 fix (2026-06-10): the template embeds the attack at an
                # `<Attacker Instruction>` placeholder — substitute it there. The prior
                # concatenation left the literal placeholder in every positive
                # (consolidated-audit-2026-06-09.md W2); ratified runs used the old
                # parquet and the slice is retired as uninformative, so this fix is
                # forward-only.
                if "<Attacker Instruction>" in tool_resp:
                    text = tool_resp.replace("<Attacker Instruction>", instr).strip()
                else:
                    text = f"{instr}\n\n{tool_resp}".strip()
                rows.append(
                    dict(text=text, attack_type=r.get("Attack Type", ""), setting=f, label=1)
                )
        if rows:
            pq.write_table(pa.Table.from_pylist(rows), dest / "injecagent_derived.parquet")
        rec.update(status="ok", n_rows=len(rows), bytes=dir_bytes(dest))
    except Exception as exc:  # noqa: BLE001
        rec.update(
            status=f"FAIL: {type(exc).__name__}: {str(exc)[:140]}",
            n_rows=None,
            bytes=dir_bytes(dest),
        )
    return rec


def clone_wainjectbench(out_root: Path) -> dict:
    """Tier-3 (unlicensed): shallow-clone WAInjectBench; the text JSONL is directory-label-encoded."""
    dest = out_root / "_eda_only_unlicensed" / "wainjectbench"
    rec = dict(
        key="wainjectbench",
        source="github.com/Norrrrrrr-lyn/WAInjectBench",
        tier=3,
        license="none",
        eda_only=True,
        note="data/text/{malicious,benign}/*.jsonl (label by directory)",
        local_path=str(dest.relative_to(REPO)),
    )
    try:
        if dest.exists() and any(dest.iterdir()):  # idempotent: keep pruned clone, don't re-fetch 4 GB
            txt = dest / "data" / "text"
            n = (
                sum(sum(1 for _ in p.open(encoding="utf-8", errors="ignore")) for p in txt.rglob("*.jsonl"))
                if txt.exists()
                else None
            )
            rec.update(status="ok_cached", n_rows=n, bytes=dir_bytes(dest))
            return rec
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "https://github.com/Norrrrrrr-lyn/WAInjectBench",
                str(dest),
            ],
            check=True,
            capture_output=True,
            timeout=240,
        )
        txt = dest / "data" / "text"
        n = (
            sum(
                sum(1 for _ in p.open(encoding="utf-8", errors="ignore"))
                for p in txt.rglob("*.jsonl")
            )
            if txt.exists()
            else None
        )
        rec.update(status="ok", n_rows=n, bytes=dir_bytes(dest))
    except Exception as exc:  # noqa: BLE001
        rec.update(
            status=f"FAIL: {type(exc).__name__}: {str(exc)[:140]}",
            n_rows=None,
            bytes=dir_bytes(dest),
        )
    return rec


def _clone_inspect(
    out_root: Path,
    *,
    key: str,
    url: str,
    sub: str,
    tier: int,
    license: str,
    eda_only: bool,
    note: str,
) -> dict:
    """Shallow git-clone a GitHub repo into ``data/raw/<sub>/<key>`` for inspection/derivation.

    Records a manifest row with ``n_rows=None`` — these are agent/env repos, not ``(text, label)``
    until an explicit derivation earns them a role (decided at the EDA gate). Idempotent + fail-loud.
    """
    dest = out_root / sub / key
    rec = dict(
        key=key,
        source=url,
        tier=tier,
        license=license,
        eda_only=eda_only,
        note=note,
        local_path=str(dest.relative_to(REPO)),
    )
    try:
        if dest.exists() and any(dest.iterdir()):  # idempotent: keep clone, don't re-fetch
            rec.update(status="ok_cached", n_rows=None, bytes=dir_bytes(dest))
            return rec
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "1", url, str(dest)],
            check=True,
            capture_output=True,
            timeout=300,
        )
        rec.update(status="ok", n_rows=None, bytes=dir_bytes(dest))
    except Exception as exc:  # noqa: BLE001 — record the failure, never silently drop
        rec.update(
            status=f"FAIL: {type(exc).__name__}: {str(exc)[:140]}", n_rows=None, bytes=dir_bytes(dest)
        )
    return rec


def clone_agentdyn(out_root: Path) -> dict:
    """T4 agentic: SaFo-Lab/AgentDyn (an AgentDojo-based dynamic security benchmark).

    Inspect-only; a ``(text, label)`` derivation (its 560 injection cases + benign tasks) is decided at
    the EDA gate — it overlaps the already-recorded ``agentdojo`` lineage (atlas family 05).
    """
    return _clone_inspect(
        out_root,
        key="agentdyn",
        url="https://github.com/SaFo-Lab/AgentDyn",
        sub="_derive",
        tier=4,
        license="confirm-on-clone",
        eda_only=False,
        note="agentic/execution axis; overlaps agentdojo lineage; 60 tasks + 560 injection cases; derive only if it earns a role",
    )


def clone_agentdam(out_root: Path) -> dict:
    """T4 (CC-BY-NC + Llama): facebookresearch/ai-agent-privacy (= AgentDAM).

    OFF-AXIS — privacy-leakage / data-minimization on VisualWebArena, NOT injection detection.
    Inspect-only; likely catalogue-only-with-reason.
    """
    return _clone_inspect(
        out_root,
        key="agentdam",
        url="https://github.com/facebookresearch/ai-agent-privacy",
        sub="_derive",
        tier=4,
        license="CC-BY-NC-4.0 + Llama-3.1",
        eda_only=False,
        note="OFF-AXIS: privacy/data-minimization, not injection; VisualWebArena trajectories; clone+confirm only",
    )


def build_bipia_qa_abstract(out_root: Path, do_build: bool) -> dict:
    """Tier-3 bucket-C: BIPIA qa/abstract (← NewsQA + XSum, run BIPIA process.py). Opt-in (heavy)."""
    rec = dict(
        key="bipia_qa_abstract",
        source="BIPIA process.py (NewsQA MIT + XSum)",
        tier=3,
        license="MIT/derived CC-BY-SA",
        eda_only=False,
        local_path="data/raw/BIPIA",
        note="email/code/table already on disk; qa/abstract need NewsQA+XSum build",
    )
    if not do_build:
        rec.update(
            status="deferred_optin",
            n_rows=None,
            bytes=0,
            note=rec["note"] + " — re-run with --build-bipia (needs NewsQA stories + XSum)",
        )
        return rec
    rec.update(
        status="not_implemented_inline",
        note="--build-bipia requested: run BIPIA's own process.py per its README (NewsQA requires "
        "the CNN-stories manual step); not auto-run here to avoid a partial corpus.",
    )
    return rec


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Materialize the dataset universe to data/raw/ + MANIFEST.json"
    )
    ap.add_argument("--out", default="data/raw")
    ap.add_argument(
        "--build-bipia", action="store_true", help="also build BIPIA qa/abstract (heavy, opt-in)"
    )
    args = ap.parse_args()
    out = REPO / args.out
    (out / "_eda_only_unlicensed").mkdir(parents=True, exist_ok=True)
    (out / "_eda_only_unlicensed" / "README.md").write_text(_README, encoding="utf-8")

    rows: list[dict] = []
    for desc in HF_SNAPSHOT:
        r = snapshot_one(desc, out)
        rows.append(r)
        print(
            f"  [{r['status'][:24]:24s}] {r['key']:18s} rows={r.get('n_rows')} bytes={r.get('bytes')}",
            flush=True,
        )

    for fn in (derive_llmail, fetch_injecagent, clone_wainjectbench, clone_agentdyn, clone_agentdam):
        r = fn(out)
        rows.append(r)
        print(
            f"  [{r['status'][:24]:24s}] {r['key']:18s} rows={r.get('n_rows')} bytes={r.get('bytes')}",
            flush=True,
        )

    rows.append(build_bipia_qa_abstract(out, args.build_bipia))
    for ro in RECORD_ONLY:
        rows.append(
            {**ro, "eda_only": ro.get("tier") == 2, "n_rows": None, "bytes": 0, "local_path": None}
        )

    ok = [r for r in rows if r.get("status") in ("ok", "ok_cached")]
    manifest = dict(
        generated="2026-06-03",
        out_root=str(out.relative_to(REPO)),
        n_materialized=len(ok),
        total_rows=sum(r["n_rows"] for r in ok if r.get("n_rows")),
        total_bytes=sum(r.get("bytes") or 0 for r in rows),
        datasets=rows,
    )
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(
        f"\n[done] materialized={len(ok)}/{len(HF_SNAPSHOT) + 5}  total_rows={manifest['total_rows']:,}  "
        f"total_bytes={manifest['total_bytes'] / 1e9:.2f} GB  → {out}/MANIFEST.json",
        flush=True,
    )
    fails = [r["key"] for r in rows if str(r.get("status", "")).startswith("FAIL")]
    if fails:
        print(f"[done] FAILURES (recorded in manifest): {fails}", flush=True)


if __name__ == "__main__":
    main()
