# Portfolio Experiment Record Template Schema

**Companion to** `~/.claude/plans/i-want-to-consider-merry-milner.md` §17.
Produced during 2026-05-19 round-7 holistic review (focus area #2: experiment record templates).

---

## Design principles

1. **Skeleton-first**: lanes open with `hypothesis.md` + `protocol.md` pre-committed at M0-M1; `results.md` + `decisions.md` written retrospectively at lane close.
2. **ADR-grounded**: each lane references the ADRs it depends on; reverse-linkage in ADRs (claim_family pointers) connects to lane outcomes.
3. **Dossier-anchored**: hypothesis.md cites prior evidence from docs/research/ MANIFEST.json `claim_family` entries.
4. **Freshness-badge-aware**: lane state transitions drive chapter freshness badges (per scaffold's 7-state machine, Round 5 Q2'''').
5. **Cost-transparent**: budget envelopes pre-committed in hypothesis.md; cost_ledger.csv reconciliation in results.md; contingency-unlock gates explicit.

---

## 4-file schema

### `hypothesis.md` (written at lane START)

YAML frontmatter:
```yaml
---
lane_id: N
lane_slug: <kebab-case-slug>
hypothesis_id: HYP-NNN
date_opened: YYYY-MM-DD
estimated_duration_weeks: N
gpu_budget_usd: NN.NN
contingency_budget_usd: NN.NN
---
```

Required sections:
- **Question being asked** (1-2 paragraphs)
- **Expected outcomes (3-way pre-commitment)**: Positive (H1) / Negative (H0) / Null (H∅) with quantitative thresholds
- **Prior evidence references**: links to submission ADRs, dossier `claim_family` keys, compass artifacts
- **Success criteria**: bulleted gate conditions
- **Bail-out criteria**: cost/time/signal triggers for lane abort or pivot
- **Cost envelope**: table with GPU + API + contingency line items
- **ADR pointers**: submission ADRs the lane relies on + portfolio ADRs to be filed at close

### `protocol.md` (written at lane START)

YAML frontmatter:
```yaml
---
lane_id: N
lane_slug: <kebab-case-slug>
protocol_id: PROTO-NNN
date_finalized: YYYY-MM-DD
---
```

Required sections:
- **Eval slate specification**: data sources × sample sizes × SHA pins; train-test disjoint verification
- **Checkpoint specification**: model IDs + revisions + fold/seed assignments
- **Eval-toolkit + RunPod command sequence**: phase-by-phase exact commands with expected wall-clock + cost per phase
- **Contingency-unlock-gate signal thresholds**: table of signal → threshold → action → lock status
- **Test-contract attestations**: list of `tests/contracts/test_lane_N_*.py` assertions
- **Single-class slice handling**: convention per Round 4 ADR-027 carry-over (val-fixed TPR only on single-class slices)
- **Metric reporting deliverables**: Tier A (headline) + Tier B (spoke); include TPR@LowFPR per ADR-036 + APR per ADR-037

### `results.md` (written at lane CLOSE, retrospective)

YAML frontmatter:
```yaml
---
lane_id: N
lane_slug: <kebab-case-slug>
results_id: RES-NNN
date_closed: YYYY-MM-DD
outcome_branch: H1 | H0 | H∅
---
```

Required sections:
- **Which hypothesis branch fired** (1-2 sentence headline)
- **Per-cell metrics with bootstrap CIs**: full table with AUPRC + AUROC + TPR@LowFPR + CI widths
- **Paired-bootstrap Delta CIs vs submission baseline**: cross-zero status
- **Figure references**: paths to rendered PNG/SVG outputs in `docs/plots/lane-N/`
- **Predictions parquet pointers**: per-row prediction file paths
- **Cost realized vs envelope**: table; contingency-overage flag if applicable
- **Deviations from protocol**: any protocol changes during execution
- **Cross-references to book chapters**: which chapter sections consume this lane's results

### `decisions.md` (written at lane CLOSE)

YAML frontmatter:
```yaml
---
lane_id: N
lane_slug: <kebab-case-slug>
decisions_id: DEC-NNN
date_closed: YYYY-MM-DD
---
```

Required sections:
- **Lane-internal decisions** (not promoted to ADR level): table of decision × options × lock × rationale
- **Decisions promoted to portfolio-level ADRs**: ADR IDs + titles + status
- **Contingency-unlock entries**: trigger × status × ADR pointer × resolution
- **Follow-on work flagged for v0.8+**: items deferred to NEXT_SESSION.md
- **Book chapter intake status**: which chapters accept which results + freshness-badge transition
- **Freshness-badge state machine transition**: SKELETON → IN_PROGRESS → RESULTS_LOCKED → CHAPTER_INTEGRATED → FINAL

---

## Cross-reference matrix (`experiments/MANIFEST.json`)

```json
{
  "lanes": {
    "lane-1-deferred-loaders": {
      "hypothesis_id": "HYP-001",
      "adr_references": ["ADR-016", "ADR-006", "ADR-027", "ADR-036"],
      "dossier_families": ["ood_shift", "lora_training", "bootstrap_ci_methodology"],
      "chapters": {
        "08_reading_the_ood_wall": {"status": "INTEGRATED", "sections": ["§8.2"]},
        "appendix_a_full_results": {"status": "LIVE", "badge_state": "LOCKED"}
      },
      "hf_hub_artifacts": {
        "dataset_card": "prompt-injection-ood-test-v1",
        "model_cards": ["prompt-injection-direct-v2-reference-scorers"]
      }
    }
  }
}
```

Authority graph maintained as single source of truth for:
- lane → ADRs (reverse-linkage for decision audits)
- lane → chapters (intake status; content-freeze gates)
- lane → dossier families (literature anchors)
- lane → HF Hub artifacts (dataset/model cards produced by lane)

---

## Test-contract attestation

`tests/contracts/test_experiment_records_complete.py`:

```python
@pytest.mark.parametrize("lane_id", ["lane-1", "lane-1b", "lane-2", "lane-3", "lane-4", "lane-5"])
def test_experiment_record_files_exist_at_milestone(lane_id):
    """Verify lane has all 4 files populated (vs skeleton) at lane close."""
    lane_path = Path("experiments") / lane_id
    for fname in ["hypothesis", "protocol", "results", "decisions"]:
        f = lane_path / f"{fname}.md"
        assert f.exists(), f"{lane_id} missing {fname}.md"
        content = f.read_text()
        assert "---" in content, f"{lane_id}/{fname}.md missing YAML frontmatter"
    results = (lane_path / "results.md").read_text()
    assert "outcome_branch:" in results, f"{lane_id}/results.md missing outcome_branch"

@pytest.mark.parametrize("lane_id", ["lane-1", "lane-1b", "lane-2", "lane-3", "lane-4", "lane-5"])
def test_experiment_manifest_lane_entry(lane_id):
    """Verify MANIFEST.json carries lane and cross-reference data."""
    manifest = Path("experiments/MANIFEST.json")
    data = json.loads(manifest.read_text())
    assert lane_id in data["lanes"], f"{lane_id} missing from MANIFEST.json"
    lane_entry = data["lanes"][lane_id]
    assert "hypothesis_id" in lane_entry
    assert "adr_references" in lane_entry and len(lane_entry["adr_references"]) > 0
    assert "chapters" in lane_entry
```

---

## Worked example: Lane 1 (deferred OOD loaders + Tier B reference scorers)

### `experiments/lane-1-deferred-loaders/hypothesis.md`

```markdown
---
lane_id: 1
lane_slug: deferred-loaders
hypothesis_id: HYP-001
date_opened: 2026-05-20
estimated_duration_weeks: 2
gpu_budget_usd: 10.00
contingency_budget_usd: 2.00
---

# Lane 1 Hypothesis: Direct-injection baseline + Tier B reference scorers

## Question being asked

Does the submission's frozen-probe + LoRA baseline AUPRC on direct-injection
slices remain competitive when compared to contemporary SOTA encoders
(Meta Prompt Guard 2 86M; optionally PromptShield Llama-3.1-8B if Tier C
unlocks)? Per submission ADR-052 + v1.1.2 DeBERTa null result, this lane
tests the backbone-invariance hypothesis: *ModernBERT-base advantage holds
across modern encoder detectors, not just within submission's training pool.*

## Expected outcomes (3-way pre-commitment)

1. **Positive (H1)**: Meta PG2 86M AUPRC ≥ 0.35 on BIPIA direct-only;
   frozen-probe within 0.02 of PG2; backbone-invariance confirmed.
2. **Negative (H0)**: Meta PG2 86M outperforms frozen-probe by >0.05 AUPRC;
   ModernBERT advantage is architecture-specific not data-driven.
3. **Null (H∅)**: All three encoders cluster within 0.30-0.37 AUPRC; no
   meaningful differentiation; the field has saturated direct-injection
   detection.

## Prior evidence references

- Submission ADR-052 (LoRA active-harm reframing): claim_family=lora_overhead
- Submission v1.1.2 DeBERTa null result (backbone-invariance evidence)
- Compass §2 (Detector Landscape): Meta PG2 86M as best-in-class encoder

## Success criteria

- All 4 experiment record files populated.
- Per-slice + pooled metrics computed with 95% bootstrap CIs (n=10,000).
- TPR@LowFPR reported per ADR-036 (1%, 0.5%, 0.1%, 0.05% FPR).
- Cost ≤ $12 (budget + contingency).
- Test-contracts pass: predictions_persisted + leakage_scan_present.

## Bail-out criteria

- GPU cost > $15 cumulative → suspend + file contingency unlock.
- Meta PG2 86M HF Hub download fails (>10 min latency) → defer to v0.8.
- Frozen-probe baseline AUPRC < 0.25 on direct-injection (signal loss) →
  switch to Appendix-B null-framing prose.

## Cost envelope

| Component | Qty | Rate | Subtotal |
|---|---:|---:|---:|
| ProtectAI v1/v2 inference (CPU) | 2 scorers | $0 | $0 |
| Meta PG2 86M inference (GPU L4) | ~2h wall | $0.40/h | ~$1 |
| HF Hub bandwidth + cached downloads | — | — | ~$1 |
| Contingency buffer | 1 | — | $8 |
| **Total** | | | **$10** |

## ADR pointers

- ADR-016 (OOD slate composition; carried from submission)
- ADR-027 (single-class slice convention; submission-enforced)
- ADR-036 (TPR@LowFPR reporting requirement; Round 7 Tier A)
- ADR-038 (benchmark integrity audit; Round 7 Tier A)
```

### `experiments/lane-1-deferred-loaders/protocol.md` (header skeleton)

Sections per schema above; key fields populated:
- Eval slate: BIPIA-direct-only (subset to direct-user-input ~500 rows) + AgentDojo + InjecAgent + NotInject + LLMail-Inject 5K stratified + PINT-EN 3016
- Checkpoints: submission's `BBehring/prompt-injection-{frozen-probe,lora}` + ProtectAI v1/v2 + Meta PG2 86M
- Command sequence: T0 portfolio-clean eval-from-hub (Phase 1) + reference scorer batch (Phase 2) + metrics battery (Phase 3) + bootstrap CI (Phase 4) + figures (Phase 5)
- Contingency unlock gate: PromptShield Llama-3.1-8B Tier C #1 if Meta PG2 86M results show base detectors fall below 0.40 AUPRC pooled OOD
- Test-contracts: `test_lane_1_predictions_persisted` + `test_lane_1_leakage_scan_present`
- Metric reporting: Tier A (pooled OOD AUPRC + TPR@LowFPR + paired-bootstrap Delta CI vs frozen-probe) + Tier B (per-slice 6×6 grid)

---

## Bootstrap effort

- M0 (skeleton): write hypothesis.md + protocol.md for all 6 lanes (~2-3 days; ~150-300 lines each)
- Per-lane close (M1-M6): write results.md + decisions.md (~1 day each; templated from this schema)

Total per-lane authoring: ~3-4 days across the lane's lifecycle.
