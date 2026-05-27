# Citation Audit Report — rag-injection-defenses

Generated: 2026-05-26

## Summary

- Total support links: 32
- Strongly grounded (verbatim_match + user_asserted): 28/32 (88%)
- Partially grounded (paraphrase + manual_override): 2/32 (6%)
- Weakly grounded (llm_inferred + propagated_from_child): 2/32 (6%)
- Substring check pass rate: 8/28 (29%)

## Per-method breakdown

| extraction_method | count | avg link_confidence |
|---|---|---|
| llm_inferred | 2 | 0.55 |
| paraphrase | 2 | 0.7 |
| verbatim_match | 28 | 0.914 |

## Per-claim grounding strength

| claim_id | strongest_method_bucket |
|---|---|
| claim_rag_bipia_capability_vulnerability_correlation | strong |
| claim_rag_bipia_introduction | strong |
| claim_rag_bipia_universal_vulnerability | strong |
| claim_rag_c2pa_consortium | strong |
| claim_rag_chatgpt_markdown_exfil | strong |
| claim_rag_comet_indirect_injection | strong |
| claim_rag_comet_ocr_screenshot_inject | strong |
| claim_rag_drag_blockchain_provenance | strong |
| claim_rag_echoleak_vulnerability_class | strong |
| claim_rag_echoleak_zeroclick | strong |
| claim_rag_gemini_memory_poison | strong |
| claim_rag_greshake_bing_advisory | strong |
| claim_rag_llatrieval_method | strong |
| claim_rag_llmail_dataset_scale | strong |
| claim_rag_promptshields_announcement | strong |
| claim_rag_promptshields_user_doc_split | strong |
| claim_rag_provenance_nli_factcheck | strong |
| claim_rag_retrieval_provenance_nascent_2026 | weak |
| claim_rag_sag_encryption_method | strong |
| claim_rag_sag_first_provably_secure | strong |
| claim_rag_slackai_crosschannel | strong |
| claim_rag_spotlighting_asr_reduction | strong |
| claim_rag_spotlighting_foundry_integration | strong |
| claim_rag_spotlighting_method | strong |
| claim_rag_spotlighting_variant_utility_tradeoff | weak |

## Substring check failures

- ev_rag_injection_defenses_0001.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/2d58408c3b4f8e5df2be287f08a82e90c321323ff9955814bab02aac08bda878.txt
- ev_rag_injection_defenses_0003.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/70d4cfd50519178f534c15b1a27c3b97e19f145ee1f1ad3f270b1f74f1384713.txt
- ev_rag_injection_defenses_0004.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/70d4cfd50519178f534c15b1a27c3b97e19f145ee1f1ad3f270b1f74f1384713.txt
- ev_rag_injection_defenses_0005.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/8e0c41db3ea23938d570d96d89c8ca7e3701ef605ee22081d03db4280b4ddda6.txt
- ev_rag_injection_defenses_0007.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/511632eb78fd27aaf3f54b96d7aefa6d29bc4a8d040380ef7667c9260a8738d3.txt
- ev_rag_injection_defenses_0008.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/f8a5917cbb6f90f31cd050d0b1c6c8773d99450847ef8d7fb95f46c813bacc0a.txt
- ev_rag_injection_defenses_0009.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/2cd488ed531263180448699d4750808704f4561ab3d392de40765cf93e43ce20.txt
- ev_rag_injection_defenses_0010.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/0ff0ef0921c091ce46e8ac77f504a1ed408db29a1e1941190790233492af3c9f.txt
- ev_rag_injection_defenses_0011.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/0791dc731c58273802528f8231c54391aa52f54626d788415be95f6f6c330377.txt
- ev_rag_injection_defenses_0012.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/67bd28229d9c5dbbac2b2d45146344546a1679187b87cb400b23ee969bdae8e0.txt
- ev_rag_injection_defenses_0013.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/253cee74d309b716350579cc4b1bfe1b5c904cb0bb78dce5fcf2b19fa16c3526.txt
- ev_rag_injection_defenses_0014.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/08a2701d30db2ed863233a99d9c974354fda515407208b0306aded1769a5b23c.txt
- ev_rag_injection_defenses_0015.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/d6c4a8f317e625aaee774f12eb80d39e6267613a2e3bd8dd5528b409fda85596.txt
- ev_rag_injection_defenses_0016.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/d6f1a60278136697a2a9f63d778931843376b364df993d46b5637ac40d10146b.txt
- ev_rag_injection_defenses_0017.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/b36fa9cd293f76e9da6dd4810d64fe5dc766a55d27fe58d3737ba5730a8284aa.txt
- ev_rag_injection_defenses_0018.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/176f4d1b387fbc02d1a42b4cb952441431ffdd1412403ccf3002bb9f2d6468cc.txt
- ev_rag_injection_defenses_0019.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/d63581ef546db4629722f6e9b3ab6e872f8d8f182661f89f0d6ba07c5da4e89e.txt
- ev_rag_injection_defenses_0020.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/1a53a472fdf9260736f62e03eaa6328279e8f497ed6fc95c27b4e2e5c90c9f3f.txt
- ev_rag_injection_defenses_0021.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/504ad53d8af02e6d7a20a88dceea775dad424d433ff03bd03b3643ccc406b1aa.txt
- ev_rag_injection_defenses_0022.supports[?].excerpt_anchor: text_path file does not exist: /Users/brandonbehring/Claude/prompt-injection-portfolio/docs/research/rag-injection-defenses/text/sha256/504ad53d8af02e6d7a20a88dceea775dad424d433ff03bd03b3643ccc406b1aa.txt
