# Citation Audit Report — direct-vs-indirect

Generated: 2026-05-26

## Summary

- Total support links: 63
- Strongly grounded (verbatim_match + user_asserted): 51/63 (81%)
- Partially grounded (paraphrase + manual_override): 8/63 (13%)
- Weakly grounded (llm_inferred + propagated_from_child): 4/63 (6%)
- Substring check pass rate: 4/51 (8%)

## Per-method breakdown

| extraction_method | count | avg link_confidence |
|---|---|---|
| llm_inferred | 4 | 0.557 |
| paraphrase | 8 | 0.8 |
| verbatim_match | 51 | 0.942 |

## Per-claim grounding strength

| claim_id | strongest_method_bucket |
|---|---|
| claim_agentdojo_dynamic_environment | strong |
| claim_agentdojo_extensible_environment | strong |
| claim_asb_10_scenarios_400_tools | strong |
| claim_asb_formalize_benchmark | strong |
| claim_attacker_moves_second_adaptive | strong |
| claim_bipia_first_indirect_benchmark | strong |
| claim_camel_agentdojo_provable_security_77pct | strong |
| claim_camel_capability_isolation | strong |
| claim_camel_control_data_flow | strong |
| claim_chatgpt_markdown_image_exfil | strong |
| claim_comet_indirect_injection | strong |
| claim_cve_2025_32711_record | strong |
| claim_designpatterns_provable_resistance | strong |
| claim_direct_vs_indirect_greshake_taxonomy | strong |
| claim_direct_vs_indirect_greshake_taxonomy_impacts | strong |
| claim_echoleak_aim_labs_disclosure | partial |
| claim_echoleak_zero_click_xpia | strong |
| claim_firewalls_benchmark_saturation | partial |
| claim_formalize_5_attacks_10_defenses | strong |
| claim_gemini_trifecta_three_vulns | strong |
| claim_goal_hijacking_prompt_leaking | strong |
| claim_guardrail_evasion_100pct | partial |
| claim_hines_spotlighting_method | strong |
| claim_houyi_36_apps_31_vulnerable | strong |
| claim_houyi_blackbox_attack | strong |
| claim_injecagent_ipi_definition | strong |
| claim_injecagent_tool_integrated_benchmark | strong |
| claim_instruction_hierarchy_priority | strong |
| claim_isolategpt_execution_isolation | strong |
| claim_jailbreak_failure_modes | strong |
| claim_jailbreak_universal_success | strong |
| claim_jatmo_task_specific_distillation | strong |
| claim_judgedeceiver_attack_mechanism | strong |
| claim_judgedeceiver_optimization_attack | strong |
| claim_kad_structural_vulnerability | partial |
| claim_llamafirewall_open_guardrail | strong |
| claim_llmail_inject_adaptive_dataset | strong |
| claim_meta_secalign_open_model | strong |
| claim_mitre_atlas_taxonomy | partial |
| claim_month_of_ai_bugs_announcement | partial |
| claim_month_of_ai_bugs_wrapup | partial |
| claim_neural_exec_differentiable_search | strong |
| claim_neural_exec_family | strong |
| claim_owasp_llm01_direct_indirect_split | strong |
| claim_production_incidents_share_data_channel_vector_class | weak |
| claim_prompt_injection_definition_llm_integrated | strong |
| claim_promptinject_framework | strong |
| claim_rossi_categorization_overview | strong |
| claim_secalign_dpo_defense | strong |
| claim_secalign_llama3_8b_8pct_asr | strong |
| claim_shadowprompt_claude_chrome | strong |
| claim_slack_ai_cross_channel_exfil | partial |
| claim_struq_structured_queries | strong |
| claim_wasp_web_agent_benchmark | strong |
| claim_whispers_agent_evaluation | strong |
| claim_whispers_tooling_amplifies_leakage | strong |
| claim_willison_dual_llm_pattern | strong |
| claim_willison_lethal_trifecta | strong |

## Substring check failures

- ev_direct_vs_indirect_0001.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/03106dd1038645558b64199e64bb5d51cd0f3b381e32bd10cf62e42c300d52c6.txt
- ev_direct_vs_indirect_0002.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/03106dd1038645558b64199e64bb5d51cd0f3b381e32bd10cf62e42c300d52c6.txt
- ev_direct_vs_indirect_0003.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/13d91c957b4f3993065bf10604ee70570eb4cf6d7361b26fff77407bb3a21817.txt
- ev_direct_vs_indirect_0004.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/7d31fd1b044f4cdd133fffe4f1b2a16c2b957b41b0456d762d0dcc66a5ec695c.txt
- ev_direct_vs_indirect_0005.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/8f8e4bafcb839e1d01078e3795f4e9fab7c160539227f6ff702ab9f34d3c0884.txt
- ev_direct_vs_indirect_0006.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/2d58408c3b4f8e5df2be287f08a82e90c321323ff9955814bab02aac08bda878.txt
- ev_direct_vs_indirect_0007.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/c3439daa681bdac9b7569b9f43daafc4afd6605f4918291523208543ac6ec13d.txt
- ev_direct_vs_indirect_0008.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/8f562c950ef155e32624dd7815eb35a5043e5bfe9f83d8be734eff73fbd8407f.txt
- ev_direct_vs_indirect_0009.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/74a75f6036e89f8d3f2a9a2207db150232e70af123a909c1ff05dd6f4ecc5a82.txt
- ev_direct_vs_indirect_0010.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/cfffce6b1f23371d6c485fbcc35fd180004724472403adccdb68eec7f46d9c79.txt
- ev_direct_vs_indirect_0011.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/cfffce6b1f23371d6c485fbcc35fd180004724472403adccdb68eec7f46d9c79.txt
- ev_direct_vs_indirect_0012.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/c8697d3c88066297e2240046b4611a40bc370c361f70b0f2d994bec7f689dfbb.txt
- ev_direct_vs_indirect_0013.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/937568d9c8dbd86d2e37fd8fa5a2d088301bbe86566e21461765ff88d2bda29b.txt
- ev_direct_vs_indirect_0014.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/da4a859c554697e444dc260deddbbddf0957fefb09f6e1ea816f8b7d4a1aa76d.txt
- ev_direct_vs_indirect_0015.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/5575144bb9ad0eb71882db08490e75c42907ce250947476b6e70c2c0e3e07ad8.txt
- ev_direct_vs_indirect_0016.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/4397426179bea9472eb3fc7324b9d111e666c7bf5cf966f6bbf1c03bfa3f9193.txt
- ev_direct_vs_indirect_0017.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/21bc6b48049c707854b42bb3635e72ee49e8dba27bf0e2e7e18d51c0ea0e5047.txt
- ev_direct_vs_indirect_0019.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/ae0e116f2132ca5c13a02336505228f5115b99a914ff019d0ea3ce13ea12e7d8.txt
- ev_direct_vs_indirect_0022.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/d63581ef546db4629722f6e9b3ab6e872f8d8f182661f89f0d6ba07c5da4e89e.txt
- ev_direct_vs_indirect_0024.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/a72899f0e7d759999cc699457d2e6e0826624628f8ed98d9b1ce429996f540c1.txt
- ev_direct_vs_indirect_0025.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/55ce86a9fb6b737fc3c33097d04570eae642c821bccc99f3aa64fcbea5532e93.txt
- ev_direct_vs_indirect_0026.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/be5c19d4fd1c88649c17cb2568329ae63b7cee86702ec808447163733cfe7dfd.txt
- ev_direct_vs_indirect_0029.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/51e92f7784dddb6e1814cd8087ca52719275ffc0e6a0130ef457b4ebf1ad4794.txt
- ev_direct_vs_indirect_0031.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/70d4cfd50519178f534c15b1a27c3b97e19f145ee1f1ad3f270b1f74f1384713.txt
- ev_direct_vs_indirect_0032.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/4493644eb2e357a86a9b9e8cc1b5bcba133daf9eaefce404ef4e5567aa966290.txt
- ev_direct_vs_indirect_0033.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/4493644eb2e357a86a9b9e8cc1b5bcba133daf9eaefce404ef4e5567aa966290.txt
- ev_direct_vs_indirect_0034.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/28b49b68f7f9500ed49d987dbb0db7e3e2ddc907157c2990d4d0b2a037dccd08.txt
- ev_direct_vs_indirect_0035.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/28b49b68f7f9500ed49d987dbb0db7e3e2ddc907157c2990d4d0b2a037dccd08.txt
- ev_direct_vs_indirect_0036.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/8e0c41db3ea23938d570d96d89c8ca7e3701ef605ee22081d03db4280b4ddda6.txt
- ev_direct_vs_indirect_0037.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/bb37ba552eb103f6b28424a6db5382c4abe43acc16b6c383b2ed28efe8b5e911.txt
- ev_direct_vs_indirect_0038.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/bb37ba552eb103f6b28424a6db5382c4abe43acc16b6c383b2ed28efe8b5e911.txt
- ev_direct_vs_indirect_0039.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/88cbfa5775742af0fba145f2a2f59bc94299a51e0f744de781c6e4f97ff1793b.txt
- ev_direct_vs_indirect_0040.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/136e3a977e2cf0cd4c20c3d4d26943ea5b4813ed9637bd4dfedc56d683ff59e8.txt
- ev_direct_vs_indirect_0041.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/136e3a977e2cf0cd4c20c3d4d26943ea5b4813ed9637bd4dfedc56d683ff59e8.txt
- ev_direct_vs_indirect_0042.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/be3cad02dec84695b257ede7d00d128b01be3ece91abba6bbca4a06c5dcb2091.txt
- ev_direct_vs_indirect_0043.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/be3cad02dec84695b257ede7d00d128b01be3ece91abba6bbca4a06c5dcb2091.txt
- ev_direct_vs_indirect_0044.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/4d1feb00a8004deb964b6a6e2b1de95090f2134e8eae1055be91f584e7fc017d.txt
- ev_direct_vs_indirect_0045.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/4d1feb00a8004deb964b6a6e2b1de95090f2134e8eae1055be91f584e7fc017d.txt
- ev_direct_vs_indirect_0046.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/890998cb61c4094a50b5b282f79b02718d6436856e8367b51f7e37d0b51d82bd.txt
- ev_direct_vs_indirect_0047.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/890998cb61c4094a50b5b282f79b02718d6436856e8367b51f7e37d0b51d82bd.txt
- ev_direct_vs_indirect_0048.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/5e3b0b4ef4b819de27ee791b52d10c2224df113d1c5748ee514c107194d3bb2e.txt
- ev_direct_vs_indirect_0049.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/5e3b0b4ef4b819de27ee791b52d10c2224df113d1c5748ee514c107194d3bb2e.txt
- ev_direct_vs_indirect_0050.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/d4a8943b9a8e23919d21371805deb09902d96242467ec316d159d54dc2f2bdab.txt
- ev_direct_vs_indirect_0051.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/d4a8943b9a8e23919d21371805deb09902d96242467ec316d159d54dc2f2bdab.txt
- ev_direct_vs_indirect_0052.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/3fda0c48b45e0464eebe9e41326f43645578850119d0306f521acb419cb4e803.txt
- ev_direct_vs_indirect_0053.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/3fda0c48b45e0464eebe9e41326f43645578850119d0306f521acb419cb4e803.txt
- ev_direct_vs_indirect_0054.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/direct-vs-indirect/text/sha256/d0278e5b95e2b0456e2e576d46364bde365092f916b5b277ee64fd0543634947.txt
