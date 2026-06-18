"""Unit tests for the C1 carrier/table-training arc (criteria.md, ratified 2026-06-10).

Targets ``experiments/carrier-table-training/{build_corpus,leakage_gate,run_c1,c1_verdict}.py``.
Verifies the corpus construction invariants (fence stripping, format sanity, dedup, balanced
mechanical injection with the fold's own suffix template), the leakage gate's purge-by-context
semantics under the corrected W17 pair convention, the treated-arm augmentation guards, the
pre-registered CLOSED/REDUCED/NOT-CLOSED rule arithmetic, and — the W3 safety property —
that the verdict overwrite-gate refuses to clobber an existing record.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import cast

import numpy as np
import pandas as pd
import pytest

_C1_DIR = Path(__file__).resolve().parent.parent.parent / "experiments" / "carrier-table-training"
if str(_C1_DIR) not in sys.path:
    sys.path.insert(0, str(_C1_DIR))

import build_corpus as bc  # noqa: E402
import c1_verdict as cv  # noqa: E402

# generate_openai imports dataset_synthesize from the gitignored .tooling/ tree, which is absent
# in CI; skip this experiment-scaffold module cleanly when that local-only dependency is missing.
go = pytest.importorskip("generate_openai")  # noqa: E402
import leakage_gate as lg  # noqa: E402
import run_c1 as rc  # noqa: E402

# ---------- build_corpus ----------


def test_strip_fences_removes_wrapping_fence_with_language_tag() -> None:
    fenced = "```csv\na,b\n1,2\n```"
    assert bc._strip_fences(fenced) == "a,b\n1,2"
    bare = "| a | b |\n|---|---|\n| 1 | 2 |"
    assert bc._strip_fences(bare) == bare


def test_format_ok_per_format() -> None:
    md = "| a | b |\n|---|---|\n| 1 | 2 |"
    csv = "a,b,c\n1,2,3\n4,5,6"
    html = "<table><tr><td>x</td></tr></table>"
    assert bc._format_ok(md, "markdown")
    assert bc._format_ok(csv, "csv")
    assert bc._format_ok(html, "html")
    assert not bc._format_ok("just prose, with a comma", "markdown")
    assert not bc._format_ok("no commas here at all", "csv")
    assert not bc._format_ok("<div>no table</div>", "html")


def _toy_pool() -> list[tuple[str, str]]:
    return [(f"Type {i}", f"attack payload {i} variant {j}") for i in range(4) for j in range(2)]


def test_build_rows_schema_injection_and_determinism() -> None:
    contexts = [{"text": f"| h |\n|---|\n| row {i} |", "format": "markdown"} for i in range(5)]
    pool = _toy_pool()
    frame = bc.build_rows(contexts, pool, payloads_per_context=3, seed=0)
    again = bc.build_rows(contexts, pool, payloads_per_context=3, seed=0)
    pd.testing.assert_frame_equal(frame, again)  # deterministic given seed

    neg = frame[frame["label"] == 0]
    pos = frame[frame["label"] == 1]
    assert len(neg) == 5 and len(pos) == 15
    # Positives use the fold's exact suffix template: context + "\n\n" + payload.
    for _, row in pos.iterrows():
        ctx, payload = row["text"].rsplit("\n\n", 1)
        assert payload.startswith("attack payload")
        assert ctx in {c["text"] for c in contexts}
    # Negatives are the clean contexts; positives share their context_sha256.
    assert set(pos["context_sha256"]) == set(neg["context_sha256"])
    assert set(frame["role"]) == {"train"} and set(frame["carrier"]) == {"table"}
    assert set(pos["source"]) == {"synthetic_inject"}
    assert set(neg["source"]) == {"synthetic_clean"}
    # Balanced round-robin: with 15 draws over an 8-payload pool, every type appears.
    assert pos["attack_type"].nunique() == 4


def test_load_contexts_from_raw_drops_and_dedups(tmp_path: Path) -> None:
    rows = [
        {"content": "| a | b |\n|---|---|\n| 1 | 2 |", "metadata": {"format": "markdown"}},
        {"content": "| a | b |\n|---|---|\n| 1 | 2 |", "metadata": {"format": "markdown"}},  # dup
        {"content": "", "metadata": {"format": "markdown"}},  # empty
        {"content": "no pipes here", "metadata": {"format": "markdown"}},  # bad format
        {"content": "```\nx,y,z\n1,2,3\n4,5,6\n```", "metadata": {"format": "csv"}},  # fenced
    ]
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "samples.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    kept, drops = bc.load_contexts_from_raw(raw)
    assert [k["format"] for k in kept] == ["markdown", "csv"]
    assert kept[1]["text"] == "x,y,z\n1,2,3\n4,5,6"  # fence stripped
    assert drops == {"empty": 1, "format": 1, "exact_dup": 1}


# ---------- leakage_gate ----------


def _toy_corpus() -> pd.DataFrame:
    # Genuinely distinct contexts (different vocabulary), so the MinHash near-scan
    # only fires on the planted collision, not on fixture self-similarity.
    html_ctx = "<table><tr><th>Speaker</th></tr><tr><td>R. Imai</td></tr></table>"
    contexts = [
        {"text": "| invoice | total |\n|---|---|\n| 1042 | 311.40 |", "format": "markdown"},
        {"text": "station,temp,wind\nKX21,12.4,18\nKX09,14.1,9", "format": "csv"},
        {"text": html_ctx, "format": "html"},
        {"text": "| player | goals |\n|---|---|\n| Santos | 17 |", "format": "markdown"},
    ]
    return cast(pd.DataFrame, bc.build_rows(contexts, _toy_pool(), payloads_per_context=2, seed=1))


def test_leakage_gate_purges_colliding_context_and_its_positives() -> None:
    corpus = _toy_corpus()
    leaked_ctx = corpus.loc[corpus["label"] == 0, "text"].iloc[0]
    test_texts = [leaked_ctx, "completely unrelated test text about email threads"]
    gated, report = lg.scan_corpus(corpus, test_texts, near_threshold=0.8)
    assert report["exact_hit_contexts"] == 1
    assert report["purged_contexts"] == 1
    # ALL rows sharing the leaked context (1 neg + 2 pos) are gone.
    assert report["rows_before"] - report["rows_after"] == 3
    assert leaked_ctx not in set(gated["text"])
    assert not any(t.startswith(leaked_ctx + "\n\n") for t in gated["text"])


def test_leakage_gate_clean_corpus_passes_untouched() -> None:
    corpus = _toy_corpus()
    gated, report = lg.scan_corpus(
        corpus, ["entirely different held-out table text"], near_threshold=0.8
    )
    assert report["purged_contexts"] == 0
    assert report["rows_after"] == len(corpus)
    pd.testing.assert_frame_equal(gated, corpus.reset_index(drop=True))


# ---------- run_c1 augmentation guards ----------


def _fold_train_like() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "text": ["bipia train row"],
            "label": [1],
            "attack_type": ["Type 0"],
            "subfamily": ["task-intent"],
            "carrier": ["email"],
            "position": ["suffix"],
            "role": ["train"],
            "source": ["inject"],
        }
    )


def test_augment_train_appends_and_projects_columns() -> None:
    corpus = _toy_corpus()
    train = _fold_train_like()
    out = rc.augment_train(train, corpus)
    assert len(out) == len(train) + len(corpus)
    assert list(out.columns) == list(train.columns)  # corpus extras dropped
    assert (out["role"] == "train").all()


def test_augment_train_rejects_nontrain_and_single_class() -> None:
    corpus = _toy_corpus()
    bad_role = corpus.copy()
    bad_role.loc[bad_role.index[0], "role"] = "test"
    with pytest.raises(ValueError, match="role"):
        rc.augment_train(_fold_train_like(), bad_role)
    single = corpus[corpus["label"] == 1].copy()
    with pytest.raises(ValueError, match="both classes"):
        rc.augment_train(_fold_train_like(), single)


# ---------- c1_verdict rule + gates ----------


def test_decide_rule_branches() -> None:
    assert cv.decide(0.02, 0.01) == "CLOSED"  # wall under SESOI, real improvement
    assert cv.decide(0.10, 0.01) == "REDUCED"  # improvement, wall remains
    assert cv.decide(0.02, 0.0) == "NOT-CLOSED"  # CI-low <= 0 dominates everything
    assert cv.decide(0.30, -0.05) == "NOT-CLOSED"


def test_dual_reading_w10() -> None:
    r = cv.dual_reading({"lora": 0.067, "frozen": 0.167})
    assert "attenuated" in r["half_frozen_knob"]
    assert "persists" in r["sign_only"]
    r2 = cv.dual_reading({"lora": -0.01, "frozen": 0.1})
    assert "no residual wall" in r2["sign_only"]


def _carrier_fold(seed_scores: dict[int, tuple[float, float]]) -> cv.fcl.CarrierFold:
    """Tiny CarrierFold: per seed, 4 payload clusters at (pos_level) + negatives at (neg_level).

    Score noise (sigma 0.1) is wide enough that a small pos-neg gap yields a genuinely
    imperfect ROC (a real val->test gap), while a large gap separates cleanly.
    """
    payload_pos = {}
    neg = {}
    val_roc = {}
    rng = np.random.default_rng(0)
    for s, (pos_level, neg_level) in seed_scores.items():
        payload_pos[s] = [np.clip(rng.normal(pos_level, 0.1, size=6), 0, 1) for _ in range(4)]
        neg[s] = np.clip(rng.normal(neg_level, 0.1, size=30), 0, 1)
        val_roc[s] = 0.99
    return cv.fcl.CarrierFold(payload_pos, neg, val_roc, sorted(seed_scores))


def test_paired_delta_g_detects_treated_improvement() -> None:
    # Control barely separates (pos ~ neg); treated separates well -> ΔG > 0 with CI-low > 0.
    ctrl = _carrier_fold({0: (0.55, 0.5), 1: (0.55, 0.5), 2: (0.55, 0.5)})
    treat = _carrier_fold({0: (0.9, 0.1), 1: (0.9, 0.1), 2: (0.9, 0.1)})
    r = cv.paired_delta_g(ctrl, treat, n_boot=300, rng=np.random.default_rng(7))
    assert r["G_treated"] < r["G_control"]
    assert r["delta_G"] > 0
    assert r["ci_low_delta"] > 0


def test_verdict_overwrite_gate_refuses_existing(tmp_path: Path) -> None:
    existing = tmp_path / "c1_verdict.json"
    existing.write_text("{}")
    path, allowed, reason = cv.resolve_verdict_path(existing, force=False)
    assert path == existing and not allowed and "refusing to overwrite" in reason
    _, allowed_force, _ = cv.resolve_verdict_path(existing, force=True)
    assert allowed_force
    fresh = tmp_path / "scratch.json"
    _, allowed_fresh, _ = cv.resolve_verdict_path(fresh, force=False)
    assert allowed_fresh


def test_verdict_default_path_is_canonical() -> None:
    path, _, _ = cv.resolve_verdict_path(None, force=False)
    assert path == cv._HERE / "c1_verdict.json"


# ---------- generate_openai adapter (criteria Revision 1) ----------


class _FakeOAIChoice:
    def __init__(self, content: str | None, finish_reason: str = "stop") -> None:
        self.message = type("M", (), {"content": content})()
        self.finish_reason = finish_reason


class _FakeOAIResponse:
    def __init__(self, content: str | None, prompt: int = 100, completion: int = 50) -> None:
        self.choices = [_FakeOAIChoice(content)]
        self.usage = type("U", (), {"prompt_tokens": prompt, "completion_tokens": completion})()


class _FakeOAIClient:
    """Hand-rolled OpenAI double recording the mapped chat-completions kwargs."""

    def __init__(self, content: str | None) -> None:
        outer = self

        class _Completions:
            def create(self, **kwargs: object) -> _FakeOAIResponse:
                outer.last_kwargs = kwargs
                return _FakeOAIResponse(content)

        self.chat = type("C", (), {"completions": _Completions()})()
        self.last_kwargs: dict[str, object] = {}


def _anthropic_call_args() -> dict[str, object]:
    return {
        "model": "gpt-4.1-mini",
        "system": [{"type": "text", "text": "sys prompt"}],
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": "few-shot q"}]},
            {"role": "assistant", "content": [{"type": "text", "text": "few-shot a"}]},
            {"role": "user", "content": [{"type": "text", "text": "Generate one table."}]},
        ],
        "max_tokens": 500,
        "temperature": 1.0,
    }


def test_openai_adapter_maps_messages_and_usage() -> None:
    fake = _FakeOAIClient("| a |\n|---|\n| 1 |")
    adapter = go.OpenAIAnthropicAdapter(fake)
    resp = adapter.messages.create(**_anthropic_call_args())
    # OpenAI-side mapping: system first, then flattened few-shot + final user turn.
    sent = cast(list[dict[str, str]], fake.last_kwargs["messages"])
    assert sent[0] == {"role": "system", "content": "sys prompt"}
    assert [m["role"] for m in sent[1:]] == ["user", "assistant", "user"]
    assert fake.last_kwargs["max_completion_tokens"] == 500
    # Anthropic-shaped response: the orchestrator's extractors work unchanged.
    assert go.ds._extract_text(resp) == "| a |\n|---|\n| 1 |"
    usage = go.ds._extract_usage(resp)
    assert usage == {
        "input_tokens": 100,
        "output_tokens": 50,
        "cache_read_tokens": 0,
        "cache_creation_tokens": 0,
    }


def test_openai_adapter_empty_content_triggers_empty_response_gate() -> None:
    fake = _FakeOAIClient(None)  # refusal / tool-call style: message.content is None
    adapter = go.OpenAIAnthropicAdapter(fake)
    resp = adapter.messages.create(**_anthropic_call_args())
    assert resp.content == []  # -> _extract_text "" -> the PR #38 EmptyResponse gate fires
    assert go.ds._extract_text(resp) == ""


def test_load_env_key_reads_only_named_key(tmp_path: Path) -> None:
    env = tmp_path / ".env.local"
    env.write_text('OTHER=zzz\nexport OPENAI_API_KEY="sk-test-123"\n')
    assert go.load_env_key(env) == "sk-test-123"
    env_missing = tmp_path / "empty.env"
    env_missing.write_text("OTHER=zzz\n")
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        go.load_env_key(env_missing)
