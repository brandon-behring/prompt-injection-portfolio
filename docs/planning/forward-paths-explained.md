# Forward paths, explained (plain-language)

A reader-friendly companion to the dense `PORTFOLIO_PLAN.md`: where the project
stands and the four things it could do next, in plain terms. Jargon is *italicised*
on first use and defined in [`docs/glossary.md`](../glossary.md).

> **Audience note.** This is the "explain it to me clearly" view. The authoritative
> status lives in `PORTFOLIO_PLAN.md` (§5/§9/§16) and `SESSION-HANDOFF.md`; the
> numbers trace to `experiments/{eda/OOD_WALL_PREDICTION,carrier-lodo,AUDIT_2026-06}/`.

---

## Where we are (the one-paragraph version)

The project set out to test whether prompt-injection *detectors* hit an "*OOD wall*"
— work in training, fail on inputs unlike training. The answer is now in, on **two
axes**, and independently re-checked five times, for **~$2 of a $250 budget**:

- **Attack-type axis** (does the detector generalise to a *kind* of attack it never
  saw?): the wall is **real for weak detectors but disappears once you fine-tune**
  (*capacity-dependent*). A small fine-tune (*LoRA*) catches every attack-type
  near-perfectly.
- **Carrier axis** (does it generalise to a new *container* — email vs code vs
  table?): the wall is **partly real even after fine-tuning** — it shrinks ~60% but
  leaves a **stubborn gap on table-formatted inputs** (*capacity-attenuated*, with a
  *residual wall* at the table carrier).

Milestone-wise: **M0** (planning + analysis) is done and ratified; **M1**
(attack-type study) is done; the **carrier pre-flight** is done; **M2–M7 have not
started.** So the *science question* is answered; the *build-out* (more lanes, the
book) is almost entirely ahead — and mostly a choice.

---

## The four things we could do next

### ① Consolidate — *write up and ship what's already proven* · $0
Turn the finished result into finished outputs: update the decision record so it
stops calling the carrier wall a "standing wall" (the data says *partial*), write
the two book chapters whose results are ready (the OOD-wall story + the baseline),
and tag a public release. **Costs nothing, risks nothing — it banks value.**
*Needs:* a ratify + a public release (your calls).

### ② Cheap-advance — *run a small cheap experiment while the big one is stuck* · ~$1, 2–3 days
Two side-experiments can run today, nothing blocking them:
- **Lane 3 (spotlighting):** does *marking* untrusted text — wrapping it in
  delimiters, or base64-encoding it — make our **detectors** better (it's known to
  make the LLM itself safer)?
- **Lane 1b (character-injection):** do invisible characters / look-alike letters
  fool our detectors? (A 2025 paper fools *older* detectors ~100% of the time.)

These add **breadth** (defence + robustness findings), not the core carrier story.

### ③ Lane 2 — *the main event: can we TRAIN past the wall?* · $156–230, 4–5 weeks
The richest and heaviest next step. We found a stubborn gap on **table** inputs;
Lane 2 asks whether generating a big, carrier-diverse synthetic training set and
retraining **closes** it. It's **currently blocked**: the tool that generates the
synthetic data has a bug that could *silently corrupt* the training set
(research_toolkit **#22** — see `PORTFOLIO_PLAN`/`upstream_issues.md`), so we either
fix that upstream first or fall back to using only existing data (cheaper, narrower).
It's the **gateway** — its training data is also what Lanes 4 and 5 need later.

### ④ Carrier-settle — *make the carrier finding rock-solid* · $0–2, 2–3 days once licensed
Our carrier result rests on **3** container types; **2 more** sit behind a dataset
license we don't have. Get the license, add them, re-run → a *"settled, 5-point"*
finding instead of *"directional, 3-point."* Cheap and quick **once licensed**, but
the license is external and may not come. It's **optional polish** — the current
finding is already honestly flagged *provisional*, with a scheduled "re-test when the
license arrives" trigger.

---

## How they fit together

```
Consolidate ─ (anytime, $0)
Cheap-advance ─ Lane 3 ──────────────┐
                                     ├─► Lane 4 (fusion)
Lane 2 (gateway) ─ corpus ───────────┘
              └─ corpus ─► Lane 5 (probe)
Carrier-settle ─ (parallel, needs a license)
```

- **Lane 2 is the gate to the back half:** its training data feeds Lanes 4 and 5, so
  little downstream runs without it.
- **Independent / runnable now:** Consolidate, Lane 3, Lane 1b.
- **Total if you do everything:** ~$190–272 — still inside the $250 base budget.
- **A sensible order:** **Consolidate** (bank it) → **Lane 3** (cheap, feeds Lane 4)
  *while* pushing to unblock Lane 2 → **Lane 2** → **Lanes 4/5** → **carrier-settle**
  if the license shows up. Unblocking Lane 2 early has leverage, because the path to
  the *full* program runs through it.

---

*Last updated 2026-06-02. Terms: see [`docs/glossary.md`](../glossary.md). Decisions:
`decisions/ADR-05{2,4,5}-*.md`. Costs/gates: `portfolio-lane-execution-playbooks.md`,
`PORTFOLIO_PLAN.md` §16.*
