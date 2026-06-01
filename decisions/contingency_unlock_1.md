# Contingency unlock 1 — cloud GPU for the M1 Lane-1 attack-type-LODO headline sweep

**Filed:** 2026-05-30 · **Status:** Budget **RESOLVED → base-budget** (2026-05-30 spend tally below:
$0.00 realized, $1–5 « $250 base) ⇒ **no contingency draw; ADR-014 stays Reserved.** The spend itself
still awaits the user's launch go-ahead (the launch glue is now wired — ADR-053, `4862e21`).
Routed via the cost-driven slot ([ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md)), **not** the
ADR-039 method-expansion.

> **Why ADR-014, not ADR-039.** ADR-039 is the Lane-1 PromptShield SOTA-anchor *method-expansion*,
> gated on a **research signal** (all base detectors cluster <0.40 AUPRC). This unlock is **not** a
> method expansion — it is the *same* pre-registered headline sweep relocated for an **infrastructure**
> reason (local VRAM), so per ADR-013 §Consequences ("method-expansions … separate from cost-driven
> unlocks ADR-014/015") it routes through the cost-driven slot. The Lane-1 `hypothesis.md` bail-out that
> names this file ("Local GPU sweep infeasible within budget → run the feasibility probe, then escalate
> to gated cloud GPU (`decisions/contingency_unlock_N.md`)") points here.

## Triggering condition (the signal that justifies the unlock)

The local-feasibility probe (2026-05-30, `docs/plans/active/lane1-attack-type-lodo_2026-05-29.md`
§"GPU LoRA feasibility probe") proved the local RTX 2070 SUPER (8 GB, shared with the GNOME desktop)
**cannot run the headline sweep at spec config**:

- The **real** `LoRADetector` runs correctly on GPU — minimal config (r=8, batch 2, max_len 256,
  1 epoch) measured **t_fit 118.9 s/model/epoch, predict 39.9 s, peak VRAM 1.37 GB, val AUPRC 0.958**.
  So this is **not** a code defect — the path is correct and learns signal.
- But **spec config (batch 16 / max_len 512) OOMs**: the desktop reclaims ~4 GB of the 8 GB card; at
  the failure point only ~32 MiB was free. `full_ft` at spec config needs *more* memory than the LoRA
  that already OOM'd → not locally runnable at spec.
- A forced-batch-2 local run would be ≈ **6–8 h** GPU wall-clock for `(lora+full_ft) × 3 folds × 3
  seeds`, with live OOM risk from desktop VRAM reclamation (already observed killing the batch-8 probe).

This is a **capability** limit (VRAM), not a budget limit — the bail-out's "infeasible within budget"
clause is met by infeasibility, independent of remaining $.

## Amount requested

**~$1–5 envelope** — a few hours on a single **24 GB+ cloud GPU** (e.g. A5000 / A40 / L4 / A100 via
the `runpod-deploy` orchestrator already pinned in `decisions/library_imports.md`). At 24 GB+ the spec
config (batch 16 / max_len 512, **native bf16** on Ampere+) runs with no desktop contention at ~3–5×
local throughput → the full sweep completes reliably in **~1.5–3 h**.

> ✅ **Budget classification RESOLVED → BASE-BUDGET (2026-05-30).** A manual spend tally (substituting for
> the absent `make cost-report`; see *Spend tally* below) confirms **$0.00 realized cumulative spend** —
> all compute to date is local (CPU + the owned RTX 2070 probe), no cloud GPU rented, no paid API. The
> $1–5 sweep therefore sits **inside the base $250**: a normal **base-budget GPU spend, NOT a contingency
> draw**. ADR-014 stays **Reserved**. *(The spend itself still awaits the user's launch go-ahead; the launch
> glue is wired — ADR-053.)*

### Spend tally (manual attestation — 2026-05-30; substitutes for `make cost-report`)

| line | $ |
|------|---|
| **Realized cumulative spend to date** | **$0.00** |
| — EDA Phases 0–3, dataset survey, harness build, cheap-rung rehearsals (all CPU) | $0 |
| — local RTX 2070 SUPER GPU feasibility probe (owned hardware) | $0 |
| — cloud GPU rented (`runpod-deploy` is a dependency pin, not usage) | $0 |
| — paid API (PG2 / CourtGuard not yet run; PG1 Meta-gated/not-run; V10 used local HF models) | $0 |
| **This sweep** — LoRA-only on RunPod (~0.75–1.5 h, 24 GB+; tfidf+frozen+falsify+baselines now local) | **$1–5** |
| **Projected realized cumulative after sweep** | **$1–5** |
| *context:* full-project base forecast if all lanes complete (ADR-002) | ~$187–267 |
| *context:* full-project forecast **incl.** this sweep | ~$188–272 |
| Base cap (ADR-002) | $250 |
| Hard cap (ADR-002) | $350 |

**Method:** no spend-ledger file exists (the repo's `*_ledger.yml` are bibliography / evidence / dataset
ledgers, not cost), so this enumerates realized spend from the project record. **Classification:** against
**$0 realized**, the $1–5 sweep is **BASE-BUDGET** — no contingency draw, ADR-014 stays Reserved.
**Hard-cap check:** even the full-project forecast (~$188–272, incl. this sweep) stays **< $350** ✓; the
$1–5 realized add is « the $250 base ✓.

**Revision (2026-06-01, ADR-054 — LoRA-only hybrid).** The sweep was re-scoped from the 4-rung
(`tfidf+frozen+lora+full_ft`) cloud run to **LoRA-only on RunPod**: `tfidf`, `frozen`, the §6.5
falsification, and the off-the-shelf reference baselines now run **locally** (free; only transformer
training at spec batch needs the 24 GB card). This *lowers* the cloud estimate (4-rung $5–15 →
LoRA-only **$1–5**) and only strengthens the base-budget classification. `full_ft` is deferred to a
conditional trigger-gate (PORTFOLIO §16); **if that trigger later fires**, a `full_ft × 3 folds × 3
seeds` pass is a separate **~$2–6** (LoRA-class card) increment to re-tally then. Realized cumulative
spend is still **$0.00**.

## Expected outcome / hypothesis being tested

Run the full pre-registered headline sweep → produce the **write-gate-OPEN** §6.5 OOD-wall
falsification verdict (the deferred deliverable):

- **Local** `harness.py --rungs tfidf frozen --folds <all 3> --seeds 0 1 2` + **RunPod** `--rungs lora`,
  merged into one tree and re-stamped via `harness.py --finalize-manifest` (ADR-054 hybrid) →
  per-`(rung,fold,seed)` predictions parquet + metrics JSON (with per-type drops) + a complete
  `MANIFEST.yml` (`complete_headline_sweep: true`).
- `falsify_ood_wall.py` then **writes** the SURVIVES/FALSIFIED verdict into
  `experiments/eda/OOD_WALL_PREDICTION/` (the write-gate opens only on a complete ≥3-seed × 3-rung
  `tfidf+frozen+lora` sweep — `full_ft` deferred, ADR-054; verified CLOSED on partial runs). Tests H1
  (shortcut-mediated collapse ordering); a null
  result is publishable.

## Bail-out criteria (when to stop drawing further)

- **Cost overrun:** if measured cloud spend projects past the ~$15 envelope (e.g. a 24 GB card is
  unavailable and only pricier instances remain), halt + re-quote before continuing.
- **Cloud OOM/instability:** unexpected OOM even at 24 GB, or >2× the ~3 h wall-clock estimate → stop,
  capture the partial MANIFEST (write-gate stays CLOSED, no verdict written), reassess.
- **API/data drift:** eval-toolkit breaking change or a BIPIA load failure on the cloud image → halt
  (the harness is pinned `[probes,losses]>=1.6`; mirror the local env).
- **Hard cap:** projected total spend must stay **< $350** (ADR-002 hard cap) — non-negotiable.

## Pre-spend checklist (per ADR-013, to complete at ratification)

- [x] Confirm base-vs-contingency from the spend ledger → **BASE-BUDGET** ($0.00 realized; see *Spend tally*).
- [ ] If contingency: advance [ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) `Reserved → Accepted`
      — **N/A** (base-budget, not a contingency draw; ADR-014 stays Reserved).
- [x] Cost attestation (manual ledger tally — `make cost-report` absent) showing projected **$1–5 < $350**.
- [x] Correct the spec/plan's "Turing → fp16" note already applied (`_select_device_dtype` gates on
      native bf16) — the cloud Ampere+ card will select **bf16** as intended.
- [x] `runpod_deploy.Session` wiring → **resolved** (there is no `Session`; wired via `scripts/runpod_sweep.py`
      → `load_job_spec→run_job`, ADR-053, `4862e21`).
- [ ] **User launch go-ahead at spend time** (the spend itself stays user-led) — still open.

## Cross-references

- [ADR-013](ADR-013-cost-contingency-unlock-policy.md) (gating policy this file enforces)
- [ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) (cost slot — ratifies this unlock if contingency)
- [ADR-002](ADR-002-cost-cap-250-base-100-contingency.md) ($250 base + $100 contingency; $350 hard cap)
- [ADR-052](ADR-052-attack-type-generalization-study-design.md) (the study design this sweep executes)
- `experiments/lane-1/hypothesis.md` (bail-out criterion that names this file)
- `docs/plans/active/lane1-attack-type-lodo_2026-05-29.md` (feasibility-probe evidence + verdict)
