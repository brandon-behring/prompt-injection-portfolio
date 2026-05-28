# Dataset candidate universe — unsafe-input / guardrail detection (working scope-map)

> **Status:** WORKING DRAFT, pre-verification (2026-05-27). The saturation-checked landscape for **broad unsafe-input/guardrail detection** (injection-direct/indirect · jailbreak · toxicity-safety-guard · over-defense · agentic-trajectory · aggregated-recipe · helper). Text-input focus; multimodal = `pointer`. Feeds the `dataset_ledger.yml` expansion — entries **graduate** into the ledger as each is per-entry verified (`status: verified`). **Relevance is a SOFT tag; dataset *selection* is deferred to the EDA.** Gitignored `_`-prefix = scratch/working.

**Soft tags.** `family`: inj-direct / inj-indirect / jailbreak / tox-safety-guard / over-defense / agentic-traj / aggregated-recipe / helper. `encoder_readiness`: drop-in / derivable / eval-only / adaptation-heavy / pointer. `study_relevance` (soft, for an injection-detection + attack-type-generalization study): high / medium / low.

## Saturation statement
Cross-checked to convergence against: Joe-B-Security/awesome-prompt-injection; ucsb-mlsec/Awesome-Agent-Security; yueliu1999/Awesome-Jailbreak-on-LLMs; Awesome-AI-Security-Benchmarks; tldrsec/prompt-injection-defenses; **safetyprompts.com** (richest); the **InjecGuard ~20-set composition** (resolved: 14 benign + 12 malicious sources) and **ProtectAI-v2** (7/22 named) + **Meta PromptGuard/Llama-Guard** (undisclosed) mixture source-lists; HF `prompt-injection` tag (137; page-1 reviewed). **Converged:** last passes added only out-of-scope multimodal/domain-safety (ChemSafety/MedSafety/MM-SafetyBench) or low-signal mirrors. Residual long tail = HF tag pages 2–5 (~107, low-yield derivative mirrors) — not enumerated.

## Already in `dataset_ledger.yml` (20, verified)
`bipia2023microsoft` · `injecagent2024uiuc` · `agentdojo2024ethz` · `llmailinject2025microsoft` · `asb2024agiresearch` · `deepset2023promptinjections` · `jackhhao2023jailbreakclassification` · `xtram12024safeguardpromptinjection`(⚠ bad-citation) · `reshabhs2024spmlchatbotpromptinjection` · `jayavibhav2024promptinjection` · `jayavibhav2024promptinjectionsafety` · `gentellab2024gentelbench` · `leolee2024notinject` · `lakera2024pintbenchmark`(withheld) · `hackaprompt2023emnlp` · `tensortrust2023arxiv` · `wainjectbench2025arxiv` · `injecguard2024arxiv` · `protectai2024debertav2mix` · `ipiwild2026arxiv`(unreleased)

## NET-NEW candidates (~65) — `name | bibkey | url | family | readiness | relevance | license | ~size | note`

### B. Injection-specific detection corpora
- PromptShield | `hendzh2025promptshield` | hf:hendzh/PromptShield | inj-direct+indirect | drop-in | **high** | apache-2.0 | 43,425 | {prompt,label,lang}; clean splits; arXiv:2501.15145.
- guychuk benign-malicious | `guychuk2024benignmalicious` | hf:guychuk/benign-malicious-prompt-classification | inj-direct | drop-in | **high** | apache-2.0 | 464,470 | "manipulation-only" labels; largest clean binary.
- Harelix Mixed-Techniques-2024 | `harelix2024mixedtechniques` | hf:Harelix/Prompt-Injection-Mixed-Techniques-2024 | inj-direct | drop-in | **high** | apache-2.0 | mid(verify) | named in ProtectAI-v2 + InjecGuard mixes.
- Open-Prompt-Injection | `liu2024openpromptinjection` | gh:liu00222/Open-Prompt-Injection | inj-direct/indirect | derivable | **high** | MIT(verify) | 7 NLP-task sets | Liu et al. arXiv:2310.12815; combinable attack×target.
- neuralchemy | `neuralchemy2024promptinjection` | hf:neuralchemy/Prompt-injection-dataset | inj-direct | drop-in | medium | unknown | 22,200 | verify license/schema.
- qualifire benchmark | `qualifire2024pibenchmark` | hf:qualifire/prompt-injections-benchmark | jailbreak/inj | drop-in | medium | unknown | 5,000 | vendor eval set.
- Octavio multilingual PI | `octavio2024multilingualpi` | hf:Octavio-Santana/prompt-injection-attack-detection-multilingual | inj-direct | drop-in | medium | unknown | 7,920 | non-EN coverage.
- ScaleAI/aspi | `scaleai2026aspi` | hf:ScaleAI/aspi | agentic/inj-indirect | adaptation-heavy | medium | cc-by-4.0 | 728 | AgentDojo-derived; recent.
- Mindgard evaded-samples | `mindgard2025evaded` | hf:Mindgard/evaded-prompt-injection-and-jailbreak-samples | inj/jailbreak | derivable | medium | verify | paired orig/modified | arXiv:2504.11168; char-evasion robustness pairs.
- budecosystem guardrail-training | `budecosystem2024guardrail` | hf:budecosystem/guardrail-training-data | aggregated-recipe | drop-in | medium | verify | mid(verify) | injection+malware+privacy w/ benign.
- StruQ aug data | `chen2024struq` | gh:Sizhe-Chen/StruQ | inj-direct | derivable | medium | verify | IT-augmentation | USENIX'25; InjecGuard source.
- imoxto cleaned | `imoxto2023cleaned` | hf:imoxto/prompt_injection_cleaned_dataset | inj-direct | adaptation-heavy | **low** | unknown | 535,105 | ⚠ HackAPrompt repackage w/ label noise (lvl 8-10) — avoid for eval.
- PIArena | `piarena2025` | hf:sleeepeer/PIArena | inj-direct | derivable | low | unknown | 2,000 | unverified provenance.
- ARPIbench | `arpibench2025` | hf:alexcbecker/ARPIbench | inj-direct | derivable | low | unknown | 7,560 | unverified.
- Necent | `necent2024pijb` | hf:Necent/llm-jailbreak-prompt-injection-dataset | inj/jailbreak | derivable | low | unknown | 1.18M | empty-card risk; flag.
- VPI-Bench | `vpibench2025` | hf:VPI-Bench/vpi-bench | inj-indirect | pointer | low | unknown | 306 | multimodal pointer.
- vigil-jailbreak-ada-002 | `deadbits2023vigil` | hf:deadbits/vigil-jailbreak-ada-002 | jailbreak | derivable | medium | verify | embeddings+prompts | InjecGuard malicious source.
- TaskTracker | `abdelnabi2024tasktracker` | gh:microsoft/TaskTracker | helper | adaptation-heavy | medium | MIT-likely | >500k activations | arXiv:2406.00799; probe/activation data, not (text,label).

### C. Jailbreak benchmarks / behavior sources
- In-the-Wild Jailbreak (DAN) | `shen2023inthewild` | hf:TrustAIRLab/in-the-wild-jailbreak-prompts | jailbreak | drop-in | **high** | MIT | 21,527 | CCS'24 "Do Anything Now"; benign+JB → balanced binary.
- AdvBench | `zou2023advbench` | gh:llm-attacks/llm-attacks | jailbreak | derivable | medium | MIT | 1,000+500 | GCG source.
- HarmBench | `mazeika2024harmbench` | gh:centerforaisafety/HarmBench | jailbreak | eval-only | medium | MIT | 400 | std red-team eval + classifier.
- JailbreakBench (JBB) | `chao2024jailbreakbench` | hf:JailbreakBench/JBB-Behaviors | jailbreak | eval-only | medium | MIT | 100+100 | std JB harness.
- StrongREJECT | `souly2024strongreject` | gh:alexandrasouly/strongreject | jailbreak | eval-only | medium | MIT | 313 | forbidden-prompt eval + grader.
- SALAD-Bench/Salad-Data | `li2024saladbench` | hf:OpenSafetyLab/Salad-Data | tox-safety-guard | derivable | medium | apache-2.0 | ~21,000 | ProtectAI-v2 source.
- (low) JailbreakV-28K `luo2024jailbreakv28k` (multimodal); MHJ `li2024mhj`; MaliciousInstruct `huang2023maliciousinstruct`; Forbidden-Questions `verazuo2023forbidden`; GPTFuzzer seeds `yu2023gptfuzzer`; SORRY-Bench `xie2024sorrybench`; S-Eval `yuan2024seval`; LatentJailbreak `qiu2023latentjailbreak`; GA_Jailbreak `ga2025jbbench`.

### D. Toxicity / safety-guard moderation (helper / co-training)
- ToxicChat | `lin2023toxicchat` | hf:lmsys/toxic-chat | tox-safety-guard | derivable | **high** | cc-by-nc-4.0 | 10,165 | has `toxicity` AND `jailbreaking` columns.
- WildGuardMix | `han2024wildguard` | hf:allenai/wildguardmix | tox-safety-guard | derivable | **high** | odc-by | 86,759/1,725 | prompt-harm+refusal+`adversarial`; Wildguard-Benign is a SOTA-mix source.
- BeaverTails | `ji2023beavertails` | hf:PKU-Alignment/BeaverTails | tox-safety-guard | derivable | medium | cc-by-nc-4.0 | ~333,963 | safety-annotated QA.
- Aegis 1.0/2.0 | `ghosh2024aegis` | hf:nvidia/Aegis-AI-Content-Safety-Dataset-1.0 | tox-safety-guard | derivable | medium | cc-by-4.0 | ~11k | NVIDIA taxonomy.
- WildJailbreak | `jiang2024wildjailbreak` | hf:allenai/wildjailbreak | jailbreak/tox | derivable | medium | verify | 261,534 | synthetic safety-training.
- (low) GuardBench `dubois2024guardbench` (meta, 40+ sets); ALERT `tedeschi2024alert`; RealToxicityPrompts `gehman2020rtp`; ToxiGen `hartvigsen2022toxigen`; Do-Not-Answer `wang2023donotanswer`.

### E. Over-defense / false-refusal controls
- XSTest | `rottger2024xstest` | hf:natolambert/xstest-v2-copy | over-defense | eval-only | **high** | cc-by-4.0 | 450 | ProtectAI-v2 source; pairs w/ NotInject.
- OR-Bench | `cui2024orbench` | hf:bench-llm/or-bench | over-defense | eval-only | **high** | verify | 80,000 | largest over-refusal eval.
- PHTest | `an2024phtest` | hf:furonghuang-lab/PHTest | over-defense | eval-only | medium | verify | 3,260 | pseudo-harmful false-refusal.
- (low) OKTest/OverKill `shi2024oktest`; CoCoNot `brahman2024coconot`.

### F. Agentic-trajectory / web-agent injection
- WASP | `liao2025wasp` | gh:facebookresearch/wasp | inj-indirect/agentic | adaptation-heavy | **high** | CC-BY-NC-4.0 | web envs | Meta/UCSD indirect web-agent PI; arXiv:2504.18575.
- (low/specialized) AgentHarm `andriushchenko2024agentharm`; Agent-SafetyBench `zhang2024agentsafetybench`; OS-Harm `kuntz2025osharm`; RedTeamCUA `wu2025redteamcua`; RAS-Eval; RiOSWorld (multimodal); CyberSecEval2/3 `bhatt2024cyberseceval`; τ-bench `yao2024taubench`.
- AgentPI (SoK) | `wang2026agentpi` | arXiv:2602.10453 | agentic | pointer | medium | unknown | n/a | ⚠ no released data link found.

### G. Aggregated / recipe / benign-carrier (meta — name components)
- Meta PromptGuard/Llama-Guard mix | `meta2024promptguard` | gh:meta-llama/PurpleLlama | aggregated-recipe | pointer | medium | llama-license | recipe | mostly undisclosed.
- LMSYS-Chat-1M | `zheng2023lmsyschat1m` | hf:lmsys/lmsys-chat-1m | helper | derivable | medium | custom | 1M | benign-carrier source.
- Benign-carrier pool (Alpaca / no_robots / ultrachat_200k / chatbot_instruction_prompts / VMware-open-instruct / grok-conversation-harmless) | helper | drop-in | medium | mixed | — | benign half of InjecGuard + ProtectAI-v2 mixes.

## Could-not-verify (flagged, not dropped)
- **AgentPI** (no data link); **ProtectAI-v2** 15/22 sources unnamed; **PromptGuard/Llama-Guard** mix undisclosed.
- License "unknown/verify": jayavibhav×2, xTRam1, Tensor Trust, WAInjectBench, neuralchemy, qualifire, Necent, PIArena, ARPIbench, Octavio + most C/D/E "verify" rows.
- **imoxto** label-noise (lvl 8-10); HF tag pages 2-5 (~107) low-yield, not enumerated.

## Next (verify → graduate → index → audit)
Verify per-entry in `study_relevance` priority order → graduate to `dataset_ledger.yml` with `status: verified` + `family`/`encoder_readiness`/`study_relevance` fields. **High-relevance first:** PromptShield, guychuk, Harelix, In-the-Wild-Jailbreak, ToxicChat, WildGuardMix, XSTest, OR-Bench, WASP, Open-Prompt-Injection. Then `/dataset-index` (re-render agent_index + rubric) → `/dossier-audit --focus "license + access + metadata correctness"` (first audit round; fix xTRam1, GenTel count).
