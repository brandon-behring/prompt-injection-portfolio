"""C1 corpus generation via OpenAI credits — same orchestrator, swapped transport.

criteria.md **Revision 1** (2026-06-10, pre-datum): Anthropic API credits were
unavailable, so generation runs on OpenAI — through the SAME research_toolkit
``dataset_synthesize.synthesize()`` orchestrator (its ``client`` parameter takes
any object with the Anthropic ``messages.create`` interface), preserving the
``--bail-at-cost`` cap, JSONL resume, the manifest, and the PR #38 EmptyResponse
gate. The templates are the byte-identical ``recipe_table_corpus.yaml`` (still
benign-only generation, ADR-022/041); only the model is overridden — loudly, and
recorded in the manifest's ``model`` field (the manifest's ``recipe_sha256``
remains that of the base YAML; this override is the Revision-1 disclosure).

Cost accounting is **conservative toward the cap**: all prompt tokens are billed
at the full input price (OpenAI's automatic prompt-cache discount is ignored),
so the manifest can only overstate spend, never understate it.

The key is read from the repo-local ``.env.local`` (gitignored); it is never
printed or persisted anywhere else.

Run::

    uv run python experiments/carrier-table-training/generate_openai.py \
        [--model gpt-4.1-mini] [--bail-at-cost 5.00]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

_HERE = Path(__file__).resolve().parent
REPO_ROOT = _HERE.parent.parent
_RT_SCRIPTS = REPO_ROOT / ".tooling" / "research_toolkit" / "scripts"
if str(_RT_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_RT_SCRIPTS))

import dataset_synthesize as ds  # noqa: E402  # type: ignore[import-not-found]

DEFAULT_MODEL = "gpt-4.1-mini"
# USD per MTok (OpenAI list price; registered into ds.PRICING_PER_MTOK so
# compute_call_cost / --bail-at-cost stay honest for the overridden model).
OPENAI_PRICING: dict[str, dict[str, float]] = {
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
}


def load_env_key(env_path: Path, name: str = "OPENAI_API_KEY") -> str:
    """Read one key from a dotenv-style file without exposing other entries."""
    if not env_path.exists():
        raise FileNotFoundError(f"{env_path} not found")
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith(f"{name}=") or line.startswith(f"export {name}="):
            value = line.split("=", 1)[1].strip().strip('"').strip("'")
            if value:
                return value
    raise ValueError(f"{name} not found (or empty) in {env_path}")


class _Block:
    """Anthropic-shaped text content block."""

    type = "text"

    def __init__(self, text: str) -> None:
        self.text = text


class _Usage:
    """Anthropic-shaped usage; cache fields zero (conservative full-price accounting)."""

    def __init__(self, input_tokens: int, output_tokens: int) -> None:
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_read_input_tokens = 0
        self.cache_creation_input_tokens = 0


class _Response:
    """Anthropic-shaped Message: empty ``content`` triggers the EmptyResponse gate."""

    def __init__(self, text: str, usage: _Usage, stop_reason: str | None) -> None:
        self.content = [_Block(text)] if text else []
        self.usage = usage
        self.stop_reason = stop_reason


class _Messages:
    def __init__(self, oai_client: Any) -> None:
        self._client = oai_client

    def create(
        self,
        *,
        model: str,
        system: list[dict[str, Any]],
        messages: list[dict[str, Any]],
        max_tokens: int,
        temperature: float,
    ) -> _Response:
        """Map Anthropic block-format messages onto one OpenAI chat completion."""
        oai_messages: list[dict[str, str]] = [
            {"role": "system", "content": "".join(b.get("text", "") for b in system)}
        ]
        for m in messages:
            content = "".join(blk.get("text", "") for blk in m["content"])
            oai_messages.append({"role": str(m["role"]), "content": content})
        resp = self._client.chat.completions.create(
            model=model,
            messages=oai_messages,
            max_completion_tokens=max_tokens,
            temperature=temperature,
        )
        choice = resp.choices[0]
        text = choice.message.content or ""
        usage = _Usage(
            int(getattr(resp.usage, "prompt_tokens", 0) or 0),
            int(getattr(resp.usage, "completion_tokens", 0) or 0),
        )
        return _Response(text, usage, getattr(choice, "finish_reason", None))


class OpenAIAnthropicAdapter:
    """Duck-typed Anthropic client backed by OpenAI chat completions."""

    def __init__(self, oai_client: Any) -> None:
        self.messages = _Messages(oai_client)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="C1 corpus generation on OpenAI (Revision 1).")
    ap.add_argument("--recipe", type=Path, default=_HERE / "recipe_table_corpus.yaml")
    ap.add_argument("--output", type=Path, default=_HERE / "corpus_raw")
    ap.add_argument("--bail-at-cost", type=float, default=5.00)
    ap.add_argument("--model", default=DEFAULT_MODEL, choices=sorted(OPENAI_PRICING))
    ap.add_argument("--env-file", type=Path, default=REPO_ROOT / ".env.local")
    args = ap.parse_args(argv)

    key = load_env_key(args.env_file)
    import openai  # local import: only needed for live generation

    client = openai.OpenAI(api_key=key)

    raw = yaml.safe_load(args.recipe.read_text(encoding="utf-8"))
    recipe, errors = ds.validate_recipe(raw)
    if errors:
        for err in errors:
            print(f"recipe error: {err}", file=sys.stderr)
        return 1
    assert recipe is not None
    recipe.sha256 = ds.recipe_sha256(args.recipe)

    ds.PRICING_PER_MTOK[args.model] = OPENAI_PRICING[args.model]
    print(
        f"generate_openai: MODEL OVERRIDE {recipe.model} -> {args.model} "
        f"(criteria.md Revision 1; templates unchanged, sha {recipe.sha256[:12]}...)",
        file=sys.stderr,
    )
    recipe.model = args.model

    exit_code, manifest = ds.synthesize(
        recipe=recipe,
        output_dir=args.output,
        bail_at_cost=args.bail_at_cost,
        client=OpenAIAnthropicAdapter(client),
    )
    print(
        f"generate_openai: samples={manifest['total_samples']} "
        f"cost=${manifest['total_cost_usd']:.4f} bail={manifest['bail_fired']} "
        f"api_error={manifest['api_error']}",
        file=sys.stderr,
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
