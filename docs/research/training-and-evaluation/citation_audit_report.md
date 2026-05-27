# Citation Audit Report — training-and-evaluation

Generated: 2026-05-26

## Summary

- Total support links: 163
- Strongly grounded (verbatim_match + user_asserted): 13/163 (8%)
- Partially grounded (paraphrase + manual_override): 141/163 (87%)
- Weakly grounded (llm_inferred + propagated_from_child): 9/163 (6%)
- Substring check pass rate: 13/13 (100%)

## Per-method breakdown

| extraction_method | count | avg link_confidence |
|---|---|---|
| llm_inferred | 9 | 0.561 |
| paraphrase | 141 | 0.803 |
| verbatim_match | 13 | 0.954 |

## Per-claim grounding strength

| claim_id | strongest_method_bucket |
|---|---|
| claim_synthesis_training_and_evaluation_four_benchmarks_saturated | weak |
| claim_synthesis_training_and_evaluation_license_red_flags | weak |
| claim_synthesis_training_and_evaluation_ood_collapse_at_low_fpr | weak |
| claim_training_and_evaluation_abdelnabi2025llmailinject_a1_headline | partial |
| claim_training_and_evaluation_abdelnabi2025llmailinject_a2_methodology | partial |
| claim_training_and_evaluation_abdelnabi2025llmailinject_a3_contribution | partial |
| claim_training_and_evaluation_bhagwatkar2025firewalls_a1_abstract | partial |
| claim_training_and_evaluation_bhagwatkar2025firewalls_a2_saturation | strong |
| claim_training_and_evaluation_bhagwatkar2025firewalls_a3_weak_attacks | strong |
| claim_training_and_evaluation_bhagwatkar2025firewalls_body_four_benchmarks_saturated | strong |
| claim_training_and_evaluation_bhagwatkar2025firewalls_body_weak_attacks_critique | strong |
| claim_training_and_evaluation_carlini2023aligned_a1_headline | partial |
| claim_training_and_evaluation_carlini2023aligned_a2_methodology | partial |
| claim_training_and_evaluation_carlini2023aligned_a3_contribution | partial |
| claim_training_and_evaluation_chao2024jailbreakbench_a1_headline | partial |
| claim_training_and_evaluation_chao2024jailbreakbench_a2_methodology | partial |
| claim_training_and_evaluation_chao2024jailbreakbench_a3_contribution | partial |
| claim_training_and_evaluation_choudhary2025detect_a1_headline | partial |
| claim_training_and_evaluation_choudhary2025detect_a2_methodology | partial |
| claim_training_and_evaluation_choudhary2025detect_a3_contribution | partial |
| claim_training_and_evaluation_cui2025orbench_a1_abstract | partial |
| claim_training_and_evaluation_cui2025orbench_a2_pairs_with_notinject | weak |
| claim_training_and_evaluation_debenedetti2024agentdojo_a1_headline | partial |
| claim_training_and_evaluation_debenedetti2024agentdojo_a2_methodology | partial |
| claim_training_and_evaluation_debenedetti2024agentdojo_a3_contribution | partial |
| claim_training_and_evaluation_deepset2024promptinjections_a1_existence | partial |
| claim_training_and_evaluation_deepset2024promptinjections_a2_provenance | partial |
| claim_training_and_evaluation_deng2024contamination_a1_abstract | partial |
| claim_training_and_evaluation_deng2024contamination_a2_slot_guessing | partial |
| claim_training_and_evaluation_fomin2026benchmarkslie_a1_headline | partial |
| claim_training_and_evaluation_fomin2026benchmarkslie_a2_methodology | partial |
| claim_training_and_evaluation_fomin2026benchmarkslie_a3_contribution | partial |
| claim_training_and_evaluation_geekyrakshit2024promptinjectiondataset_a1_existence | partial |
| claim_training_and_evaluation_geekyrakshit2024promptinjectiondataset_a2_provenance | partial |
| claim_training_and_evaluation_gulrajani2021domainbed_a1_dg_definition | strong |
| claim_training_and_evaluation_gulrajani2021domainbed_a2_model_selection | strong |
| claim_training_and_evaluation_gulrajani2021domainbed_a3_erm_baseline | strong |
| claim_training_and_evaluation_gulrajani2021domainbed_body_lodo_methodology_foundation | strong |
| claim_training_and_evaluation_hackett2025bypassing_a1_headline | partial |
| claim_training_and_evaluation_hackett2025bypassing_a2_methodology | partial |
| claim_training_and_evaluation_hackett2025bypassing_a3_contribution | partial |
| claim_training_and_evaluation_hackett2025bypassing_body_character_injection_100pct | strong |
| claim_training_and_evaluation_han2024wildguard_a1_headline | partial |
| claim_training_and_evaluation_han2024wildguard_a2_methodology | partial |
| claim_training_and_evaluation_han2024wildguard_a3_contribution | partial |
| claim_training_and_evaluation_harelix2024_mixed_a1_existence | partial |
| claim_training_and_evaluation_hendzh2025promptshielddataset_a1_existence | partial |
| claim_training_and_evaluation_hendzh2025promptshielddataset_a2_provenance | partial |
| claim_training_and_evaluation_hu2021lora_a1_headline | partial |
| claim_training_and_evaluation_hu2021lora_a2_methodology | partial |
| claim_training_and_evaluation_hu2021lora_a3_contribution | partial |
| claim_training_and_evaluation_ivry2025sentinel_a1_headline | partial |
| claim_training_and_evaluation_ivry2025sentinel_a2_methodology | partial |
| claim_training_and_evaluation_ivry2025sentinel_a3_contribution | partial |
| claim_training_and_evaluation_jackhhao2023jailbreakclassification_a1_existence | partial |
| claim_training_and_evaluation_jackhhao2023jailbreakclassification_a2_provenance | partial |
| claim_training_and_evaluation_jacob2025promptshield_a1_headline | partial |
| claim_training_and_evaluation_jacob2025promptshield_a2_methodology | partial |
| claim_training_and_evaluation_jacob2025promptshield_a3_contribution | partial |
| claim_training_and_evaluation_jacob2025promptshield_body_protectai_v2_table4_collapse | strong |
| claim_training_and_evaluation_jiang2024wildjailbreak_a1_headline | partial |
| claim_training_and_evaluation_jiang2024wildjailbreak_a2_methodology | partial |
| claim_training_and_evaluation_jiang2024wildjailbreak_a3_contribution | partial |
| claim_training_and_evaluation_jung2026postmortem_a1_summary | partial |
| claim_training_and_evaluation_jung2026postmortem_a2_saxe_fscore | strong |
| claim_training_and_evaluation_jung2026postmortem_a3_speed_bump | strong |
| claim_training_and_evaluation_kopf2023oasst1_a1_abstract | partial |
| claim_training_and_evaluation_kopf2023oasst1_a2_benign_pool_role | weak |
| claim_training_and_evaluation_lakera2023gandalfignore_a1_existence | partial |
| claim_training_and_evaluation_lakera2023gandalfignore_a2_provenance | partial |
| claim_training_and_evaluation_lakera2024pint_a1_announcement | partial |
| claim_training_and_evaluation_lakera2024pint_a2_contribution | partial |
| claim_training_and_evaluation_li2024injecguard_a1_headline | partial |
| claim_training_and_evaluation_li2024injecguard_a2_methodology | partial |
| claim_training_and_evaluation_li2024injecguard_a3_contribution | partial |
| claim_training_and_evaluation_li2024saladbench_a1_headline | partial |
| claim_training_and_evaluation_li2024saladbench_a2_methodology | partial |
| claim_training_and_evaluation_li2024saladbench_a3_contribution | partial |
| claim_training_and_evaluation_lin2023toxicchat_a1_headline | partial |
| claim_training_and_evaluation_lin2023toxicchat_a2_methodology | partial |
| claim_training_and_evaluation_lin2023toxicchat_a3_contribution | partial |
| claim_training_and_evaluation_liu2020energyood_a1_headline | partial |
| claim_training_and_evaluation_liu2020energyood_a2_methodology | partial |
| claim_training_and_evaluation_liu2020energyood_a3_contribution | partial |
| claim_training_and_evaluation_liu2024dora_a1_headline | partial |
| claim_training_and_evaluation_liu2024dora_a2_methodology | partial |
| claim_training_and_evaluation_liu2024dora_a3_contribution | partial |
| claim_training_and_evaluation_liu2025datasentinel_a1_headline | partial |
| claim_training_and_evaluation_liu2025datasentinel_a2_methodology | partial |
| claim_training_and_evaluation_liu2025datasentinel_a3_contribution | partial |
| claim_training_and_evaluation_luo2024jailbreakv28k_a1_headline | partial |
| claim_training_and_evaluation_luo2024jailbreakv28k_a2_methodology | partial |
| claim_training_and_evaluation_luo2024jailbreakv28k_a3_contribution | partial |
| claim_training_and_evaluation_m2026sixfrontier_a1_abstract | partial |
| claim_training_and_evaluation_m2026sixfrontier_a2_field_skew | partial |
| claim_training_and_evaluation_mazeika2024harmbench_a1_headline | partial |
| claim_training_and_evaluation_mazeika2024harmbench_a2_methodology | partial |
| claim_training_and_evaluation_mazeika2024harmbench_a3_contribution | partial |
| claim_training_and_evaluation_meta2025promptguard2_a1_existence | partial |
| claim_training_and_evaluation_meta2025promptguard2_a2_provenance | partial |
| claim_training_and_evaluation_microsoft2024orcaagentinstruct_a1_existence | partial |
| claim_training_and_evaluation_microsoft2024orcaagentinstruct_a2_provenance | partial |
| claim_training_and_evaluation_nasr2025attackersecond_a1_headline | partial |
| claim_training_and_evaluation_nasr2025attackersecond_a2_methodology | partial |
| claim_training_and_evaluation_nasr2025attackersecond_a3_contribution | partial |
| claim_training_and_evaluation_neuralchemy2026dataset_a1_size_license | partial |
| claim_training_and_evaluation_neuralchemy2026dataset_a2_zero_leakage_splits | partial |
| claim_training_and_evaluation_oren2023provetestcontam_a1_abstract | partial |
| claim_training_and_evaluation_oren2023provetestcontam_a2_exchangeability | partial |
| claim_training_and_evaluation_protectai2024_validation_dataset_a1_existence | partial |
| claim_training_and_evaluation_protectai2024deberta_a1_existence | partial |
| claim_training_and_evaluation_protectai2024deberta_a2_provenance | partial |
| claim_training_and_evaluation_reshabh2024spml_a1_existence | partial |
| claim_training_and_evaluation_reshabh2024spml_a2_provenance | partial |
| claim_training_and_evaluation_rogue2025promptinjectionsbenchmark_a1_existence | partial |
| claim_training_and_evaluation_rogue2025promptinjectionsbenchmark_a2_provenance | partial |
| claim_training_and_evaluation_sainz2023nlpeval_a1_abstract | partial |
| claim_training_and_evaluation_sainz2023nlpeval_a2_disclosure_norm | partial |
| claim_training_and_evaluation_schulhoff2023hackaprompt_a1_headline | partial |
| claim_training_and_evaluation_schulhoff2023hackaprompt_a2_methodology | partial |
| claim_training_and_evaluation_schulhoff2023hackaprompt_a3_contribution | partial |
| claim_training_and_evaluation_sensoy2018evidential_a1_headline | partial |
| claim_training_and_evaluation_sensoy2018evidential_a2_methodology | partial |
| claim_training_and_evaluation_sensoy2018evidential_a3_contribution | partial |
| claim_training_and_evaluation_shen2023doanythingnow_a1_headline | partial |
| claim_training_and_evaluation_shen2023doanythingnow_a2_methodology | partial |
| claim_training_and_evaluation_shen2023doanythingnow_a3_contribution | partial |
| claim_training_and_evaluation_shi2023minkprob_a1_abstract | partial |
| claim_training_and_evaluation_shi2023minkprob_a2_methodology | partial |
| claim_training_and_evaluation_toyer2023tensortrust_a1_headline | partial |
| claim_training_and_evaluation_toyer2023tensortrust_a2_methodology | partial |
| claim_training_and_evaluation_toyer2023tensortrust_a3_contribution | partial |
| claim_training_and_evaluation_wallace2024instructionhierarchy_a1_headline | partial |
| claim_training_and_evaluation_wallace2024instructionhierarchy_a2_methodology | partial |
| claim_training_and_evaluation_wallace2024instructionhierarchy_a3_contribution | partial |
| claim_training_and_evaluation_wallace2024instructionhierarchy_body_priority_ordering | strong |
| claim_training_and_evaluation_white2024livebench_a1_abstract | partial |
| claim_training_and_evaluation_white2024livebench_a2_methodology | partial |
| claim_training_and_evaluation_xtram2024safeguard_a1_existence | partial |
| claim_training_and_evaluation_xtram2024safeguard_a2_provenance | partial |
| claim_training_and_evaluation_xu2024contamination_a1_abstract | partial |
| claim_training_and_evaluation_xu2024contamination_a2_ood_wall_link | weak |
| claim_training_and_evaluation_yang2024rephrased_a1_abstract | partial |
| claim_training_and_evaluation_yang2024rephrased_a2_dossier_implication | weak |
| claim_training_and_evaluation_yao2024taubench_a1_headline | partial |
| claim_training_and_evaluation_yao2024taubench_a2_methodology | partial |
| claim_training_and_evaluation_yao2024taubench_a3_contribution | partial |
| claim_training_and_evaluation_yi2023bipia_a1_headline | partial |
| claim_training_and_evaluation_yi2023bipia_a2_methodology | partial |
| claim_training_and_evaluation_yi2023bipia_a3_contribution | partial |
| claim_training_and_evaluation_zawalski2025codec_a1_abstract | partial |
| claim_training_and_evaluation_zawalski2025codec_a2_icl_signal | partial |
| claim_training_and_evaluation_zhan2024injecagent_a1_headline | partial |
| claim_training_and_evaluation_zhan2024injecagent_a2_methodology | partial |
| claim_training_and_evaluation_zhan2024injecagent_a3_contribution | partial |
| claim_training_and_evaluation_zhang2025asb_a1_headline | partial |
| claim_training_and_evaluation_zhang2025asb_a2_methodology | partial |
| claim_training_and_evaluation_zhang2025asb_a3_contribution | partial |
| claim_training_and_evaluation_zou2023universal_a1_headline | partial |
| claim_training_and_evaluation_zou2023universal_a2_methodology | partial |
| claim_training_and_evaluation_zou2023universal_a3_contribution | partial |
| claim_training_eval_synth_underdisclosed_training_data | weak |
| claim_training_eval_synth_vendor_self_comparison | weak |
