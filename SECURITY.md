# Security Policy

This repository is a **methodology case study** in prompt-injection detection.
It publishes research artifacts (model checkpoints, evaluation datasets, code)
that are **dual-use**. Please read this policy in conjunction with
[`ETHICS.md`](ETHICS.md) for the full responsible-use context.

---

## 1. Status

**Pre-alpha** (v0.1.0-pre at time of writing). The repository is under active
development. ADRs are not yet locked. APIs may break. Reproducibility tiers
T0 / T1 / T2 / T3 will stabilize at v0.7.0 (M7) per the project plan.

---

## 2. What this policy covers

Use **GitHub Security Advisories** as the disclosure channel for:

- **Code vulnerabilities** in `src/`, `scripts/`, `tests/`, or build infrastructure
- **Model checkpoint integrity issues** (e.g., backdoored or poisoned weights
  uploaded to HF Hub under the `BBehring/prompt-injection-*` namespace)
- **Dataset integrity issues** (e.g., labels leaking eval slates into training
  pools, or training-pool contamination with adversarial test cases)
- **Methodology-specific security findings** — e.g., a previously undocumented
  attack vector that bypasses portfolio's published detectors at meaningfully
  higher rates than the Lane 1b 12-technique adversarial-bypass matrix
  documents (per `eval_toolkit.adversarial.ALL_TECHNIQUES`)
- **Supply-chain concerns** in any of the 4 load-bearing libraries
  (eval-toolkit / runpod-deploy / research_toolkit / book-scaffold-astro) when
  they intersect with portfolio's consumer surface
- **CI / publishing pipeline** vulnerabilities that could allow unintended
  changes to public artifacts

Use the email channel from `ETHICS.md` §6.2 for:

- Dataset misuse reports
- Citation / attribution questions
- Content concerns (book chapters, ADRs, HF Hub model cards)
- AI-disclosure questions
- Anthropic ToS compliance questions

---

## 3. Reporting a vulnerability

**Preferred channel**: <https://github.com/brandon-behring/prompt-injection-portfolio/security/advisories/new>

Submit a private security advisory there. GitHub Security Advisories supports:

- Private discussion with the maintainer
- Coordinated embargo if needed
- CVE assignment if applicable
- Tracking of the fix from disclosure → remediation → publication

**Acknowledgment SLA**: within **3 business days** of submission (mirroring
Anthropic's Responsible Disclosure Policy).

**Remediation SLA**: not committed. Depending on severity, the maintainer may:

- Issue a patch in the next portfolio release (v0.X.Y)
- Publish a CVE
- Document the finding as an `experimental-result` book chapter addition
- Reframe a project methodology decision through a new ADR

---

## 4. Responsible disclosure principles

We follow norms from:

- [Anthropic Responsible Disclosure Policy](https://www.anthropic.com/responsible-disclosure-policy)
- [AllenAI WildJailbreak / WildGuardMix](https://allenai.org/) responsible-use guidelines
- [HarmBench](https://www.harmbench.org/) (Center for AI Safety 2024) disclosure norms
- [ACL Policy on Publication Ethics](https://www.aclweb.org/portal/) (effective April 2025)

We **do not punish** good-faith reports. We do not threaten legal action against
researchers who disclose responsibly per the norms above.

---

## 5. What this policy does NOT cover

- **Detector bypass demonstrations on portfolio's published checkpoints** are
  EXPECTED research output — they are not vulnerabilities; they are findings.
  Open a regular GitHub Issue with the `research-discussion` label instead.
- **Dataset content concerns** (e.g., a single synthetic example you believe
  is over-broad or under-broad) — use the email channel in `ETHICS.md` §6.2
  rather than GitHub Security Advisories.
- **Theoretical attack categories** not demonstrated against portfolio's
  checkpoints — open a `research-discussion` issue.

---

## 6. Cross-references

- [`ETHICS.md`](ETHICS.md) — dual-use disclosure, intended use, responsible-use
  norms, citation guidance
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — community participation norms
- [`README.md`](README.md) — project overview + 3-guide entry-points
- [Anthropic Commercial Service Agreement](https://www.anthropic.com/legal/commercial-terms)
  — for questions about Claude-Sonnet-generated synthetic data

---

## 7. Version history

- **v0.1.0-pre** (M0 Day 15, 2026-05-22): initial security policy.
