# Internal results analysis -- 2026-06-08

Audience: internal critique. Scope: canonical merged metrics plus final untracked RunPod LoRA provenance folders. This is a table-first data review; interpretation follows the raw tables.

## Short version

The project did not find one simple OOD wall. It found three different unlike-training tests with different outcomes: attack-type transfer inside BIPIA is solved by the small fine-tune, carrier transfer inside BIPIA is partly solved with a table residual, and cross-family transfer remains the hard failure.

| Area | Plain-English result |
| --- | --- |
| Attack type inside BIPIA | Small fine-tune solved this; held-out attack types scored near ceiling. |
| Carrier inside BIPIA | Small fine-tune helped, but table-formatted inputs still dropped. |
| Cross-family transfer | Small fine-tune did not solve this; direct data did not bridge to indirect dialects. |

## How to read the tables

| Term | Plain meaning |
| --- | --- |
| OOD / unlike-training data | Test data that differs from the data used for training. |
| Leave-one-out test | Hide one group during training, then test on that hidden group. |
| tfidf | Simple word-count detector. |
| frozen | Pretrained encoder used as fixed features; it does not learn end-to-end. |
| lora | Small end-to-end fine-tune of the detector. |
| AUPRC | Precision-recall score; can be inflated when positives are common. |
| ROC-AUC | Ranking score; 0.5 is chance and below 0.5 points the wrong way. |
| Gap score | Validation score minus held-out test score; larger positive values mean worse transfer. |
| CI-low | Lower end of a confidence interval. |
| TPR @ FPR | Attack catch rate at a fixed benign false-positive rate. |

## Raw results inventory

| Source directory | Metrics files included | Role |
| --- | --- | --- |
| attack-type-lodo/results | 63 | canonical merged BIPIA attack/carrier results |
| cross-family/B2_3_results | 60 | canonical B- dialect results |
| cross-family/B2_3_results_Bplus | 36 | canonical B+ dialect results |
| cross-family/B2_4_results | 12 | canonical Arm A capped/uncapped results |
| runpod/B3_results_runpod_all27_lora | 16 | untracked H100 LoRA provenance/final coverage |
| runpod/B3_results_runpod_bplus_cheap_lora | 12 | untracked cheap-card B+ LoRA provenance/final coverage |

Included model/rung labels: `tfidf`, `frozen`, `lora`, `reference_prompt_guard_1`, `reference_prompt_guard_2`, `reference_protectai_v2`.

Additional off-the-shelf comparison rows are stored inside cross-family `summary.json` files rather than per-run `.metrics.json` files: B2.3 E8 has 12 rows, B2.4 E8 has 12 rows, and B2.3 B+ has no separate E8 block. They are included below as reference-comparison tables.

Excluded duplicate/provenance artifacts from the raw tables: `experiments/attack-type-lodo/results_dressrehearsal_frozen/`, `experiments/attack-type-lodo/results_dressrehearsal_tfidf/`, `experiments/attack-type-lodo/results_runpod_lora/`, and `experiments/attack-type-lodo/results_runpod_carrier_lora/`. The final cross-family RunPod folders are included in a separate provenance table because they document final LoRA coverage and cross-card reconciliation.

## Canonical headline verdict check

| Axis | Statistic | Value | p-value | CI | Verdict |
| --- | --- | --- | --- | --- | --- |
| Attack-type | LoRA T | -0.003 | p=0.900 | CI-low=-0.007 | FALSIFIED |
| Carrier | LoRA G | 0.067 |  | CI-low=0.064 | SMALL-THROUGHOUT |
| Cross-family Arm A | LoRA Gx | 0.365 |  | CI-low=0.284 | SURVIVES |

## Raw table 1 -- BIPIA leave-one-out trained runs

Rows are one seed/fold/model each, excluding carrier-specific folds and off-the-shelf reference probes, which have their own tables below.

| Fold | Seed | Model | n_train | n_val | n_test | Val score | Test AUPRC | Test ROC-AUC | Brier | ECE | TPR@1% | TPR@0.5% | TPR@0.1% | NotInject FPR | Recipe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| carrier_plus_attack_external | 0 | frozen | 1494 | 404 | 890 | 0.960 | 0.983 | 0.780 | 0.056 | 0.056 | 0.332 | 0.332 | 0.332 | 0.982 | C=10.0 |
| carrier_plus_attack_external | 0 | lora | 1494 | 404 | 890 | 0.995 | 0.999 | 0.976 | 0.035 | 0.082 | 0.794 | 0.794 | 0.794 | 0.106 | r=16, lr=0.0001, epochs=3 |
| carrier_plus_attack_external | 0 | tfidf | 1494 | 404 | 890 | 0.913 | 0.991 | 0.858 | 0.049 | 0.028 | 0.427 | 0.427 | 0.427 | 0.212 | C=10.0 |
| core_attack_type | 0 | frozen | 2038 | 557 | 2720 | 0.978 | 0.984 | 0.852 | 0.125 | 0.170 | 0.321 | 0.204 | 0.080 | 0.814 | C=1.0 |
| core_attack_type | 0 | lora | 2038 | 557 | 2720 | 0.997 | 0.998 | 0.981 | 0.050 | 0.061 | 0.861 | 0.852 | 0.784 | 0.044 | r=16, lr=0.0001, epochs=3 |
| core_attack_type | 0 | tfidf | 2038 | 557 | 2720 | 0.945 | 0.979 | 0.795 | 0.122 | 0.204 | 0.229 | 0.200 | 0.111 | 0.398 | C=10.0 |
| obfuscation_technique | 0 | frozen | 876 | 218 | 920 | 0.949 | 0.962 | 0.879 | 0.150 | 0.153 | 0.310 | 0.293 | 0.279 | 0.381 | C=1.0 |
| obfuscation_technique | 0 | lora | 876 | 218 | 920 | 0.981 | 0.989 | 0.958 | 0.069 | 0.049 | 0.883 | 0.861 | 0.861 | 0.106 | r=16, lr=0.0001, epochs=3 |
| obfuscation_technique | 0 | tfidf | 876 | 218 | 920 | 0.957 | 0.956 | 0.866 | 0.158 | 0.191 | 0.233 | 0.221 | 0.158 | 0.080 | C=10.0 |
| carrier_plus_attack_external | 1 | frozen | 1494 | 404 | 890 | 0.969 | 0.986 | 0.808 | 0.056 | 0.056 | 0.349 | 0.349 | 0.349 | 0.982 | C=1.0 |
| carrier_plus_attack_external | 1 | lora | 1494 | 404 | 890 | 0.996 | 0.997 | 0.953 | 0.044 | 0.087 | 0.612 | 0.612 | 0.612 | 0.788 | r=16, lr=0.0001, epochs=3 |
| carrier_plus_attack_external | 1 | tfidf | 1494 | 404 | 890 | 0.916 | 0.975 | 0.686 | 0.201 | 0.386 | 0.132 | 0.132 | 0.132 | 0.000 | C=0.1 |
| core_attack_type | 1 | frozen | 2039 | 555 | 2720 | 0.981 | 0.985 | 0.862 | 0.147 | 0.202 | 0.254 | 0.217 | 0.200 | 0.850 | C=1.0 |
| core_attack_type | 1 | lora | 2039 | 555 | 2720 | 0.997 | 0.997 | 0.965 | 0.078 | 0.086 | 0.864 | 0.863 | 0.795 | 0.372 | r=16, lr=0.0001, epochs=3 |
| core_attack_type | 1 | tfidf | 2039 | 555 | 2720 | 0.935 | 0.961 | 0.669 | 0.219 | 0.390 | 0.079 | 0.059 | 0.045 | 0.000 | C=0.1 |
| obfuscation_technique | 1 | frozen | 876 | 219 | 920 | 0.968 | 0.962 | 0.883 | 0.145 | 0.153 | 0.286 | 0.274 | 0.263 | 0.558 | C=1.0 |
| obfuscation_technique | 1 | lora | 876 | 219 | 920 | 0.994 | 0.992 | 0.970 | 0.063 | 0.050 | 0.881 | 0.871 | 0.775 | 0.150 | r=16, lr=0.0001, epochs=3 |
| obfuscation_technique | 1 | tfidf | 876 | 219 | 920 | 0.951 | 0.938 | 0.840 | 0.169 | 0.202 | 0.090 | 0.017 | 0.017 | 0.088 | C=10.0 |
| carrier_plus_attack_external | 2 | frozen | 1494 | 404 | 890 | 0.962 | 0.990 | 0.859 | 0.055 | 0.051 | 0.371 | 0.371 | 0.371 | 0.991 | C=0.1 |
| carrier_plus_attack_external | 2 | lora | 1494 | 404 | 890 | 0.991 | 0.999 | 0.985 | 0.059 | 0.157 | 0.880 | 0.880 | 0.880 | 0.062 | r=16, lr=0.0001, epochs=3 |
| carrier_plus_attack_external | 2 | tfidf | 1494 | 404 | 890 | 0.922 | 0.974 | 0.673 | 0.205 | 0.390 | 0.148 | 0.148 | 0.148 | 0.000 | C=0.1 |
| core_attack_type | 2 | frozen | 2039 | 552 | 2720 | 0.983 | 0.985 | 0.858 | 0.159 | 0.187 | 0.196 | 0.177 | 0.123 | 0.885 | C=10.0 |
| core_attack_type | 2 | lora | 2039 | 552 | 2720 | 0.995 | 0.998 | 0.976 | 0.074 | 0.083 | 0.885 | 0.877 | 0.792 | 0.053 | r=8, lr=0.0001, epochs=3 |
| core_attack_type | 2 | tfidf | 2039 | 552 | 2720 | 0.936 | 0.961 | 0.674 | 0.223 | 0.395 | 0.068 | 0.050 | 0.043 | 0.000 | C=0.1 |
| obfuscation_technique | 2 | frozen | 869 | 217 | 920 | 0.952 | 0.966 | 0.896 | 0.165 | 0.195 | 0.311 | 0.225 | 0.151 | 0.743 | C=1.0 |
| obfuscation_technique | 2 | lora | 869 | 217 | 920 | 0.985 | 0.987 | 0.949 | 0.080 | 0.077 | 0.883 | 0.878 | 0.790 | 0.080 | r=16, lr=0.0001, epochs=3 |
| obfuscation_technique | 2 | tfidf | 869 | 217 | 920 | 0.924 | 0.950 | 0.844 | 0.175 | 0.215 | 0.256 | 0.201 | 0.190 | 0.035 | C=10.0 |

## Raw table 2 -- Carrier leave-one-out trained runs

| Carrier | Seed | Model | n_train | n_val | n_test | Val score | Test AUPRC | Test ROC-AUC | Brier | ECE | TPR@1% | TPR@0.5% | TPR@0.1% | NotInject FPR | Recipe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code | 0 | frozen | 2982 | 746 | 1780 | 0.987 | 0.975 | 0.728 | 0.056 | 0.056 | 0.056 | 0.048 | 0.048 | 0.947 | C=1.0 |
| code | 0 | lora | 2982 | 746 | 1780 | 0.998 | 0.998 | 0.960 | 0.044 | 0.054 | 0.886 | 0.668 | 0.668 | 0.336 | r=8, lr=0.0001, epochs=3 |
| code | 0 | tfidf | 2982 | 746 | 1780 | 0.976 | 0.989 | 0.862 | 0.051 | 0.049 | 0.232 | 0.176 | 0.176 | 0.540 | C=10.0 |
| email | 0 | frozen | 2982 | 746 | 1780 | 0.980 | 0.991 | 0.870 | 0.056 | 0.056 | 0.502 | 0.435 | 0.435 | 0.991 | C=1.0 |
| email | 0 | lora | 2982 | 746 | 1780 | 0.998 | 0.998 | 0.969 | 0.024 | 0.019 | 0.742 | 0.573 | 0.573 | 0.611 | r=8, lr=0.0001, epochs=3 |
| email | 0 | tfidf | 2982 | 746 | 1780 | 0.950 | 0.997 | 0.961 | 0.045 | 0.042 | 0.482 | 0.137 | 0.137 | 0.310 | C=10.0 |
| table | 0 | frozen | 2848 | 712 | 1948 | 0.999 | 0.904 | 0.605 | 0.639 | 0.659 | 0.049 | 0.031 | 0.024 | 0.920 | C=10.0 |
| table | 0 | lora | 2848 | 712 | 1948 | 1.000 | 0.973 | 0.837 | 0.184 | 0.194 | 0.642 | 0.638 | 0.628 | 0.637 | r=16, lr=0.0001, epochs=3 |
| table | 0 | tfidf | 2848 | 712 | 1948 | 0.987 | 0.984 | 0.939 | 0.048 | 0.050 | 0.088 | 0.045 | 0.045 | 0.558 | C=10.0 |
| code | 1 | frozen | 2982 | 746 | 1780 | 0.991 | 0.979 | 0.752 | 0.061 | 0.063 | 0.127 | 0.076 | 0.076 | 0.973 | C=10.0 |
| code | 1 | lora | 2982 | 746 | 1780 | 0.997 | 0.998 | 0.970 | 0.041 | 0.051 | 0.904 | 0.884 | 0.884 | 0.389 | r=16, lr=0.0001, epochs=3 |
| code | 1 | tfidf | 2982 | 746 | 1780 | 0.979 | 0.989 | 0.862 | 0.052 | 0.053 | 0.260 | 0.159 | 0.159 | 0.611 | C=10.0 |
| email | 1 | frozen | 2982 | 746 | 1780 | 0.977 | 0.991 | 0.863 | 0.056 | 0.056 | 0.519 | 0.501 | 0.501 | 0.982 | C=1.0 |
| email | 1 | lora | 2982 | 746 | 1780 | 0.996 | 0.999 | 0.981 | 0.030 | 0.032 | 0.835 | 0.327 | 0.327 | 0.027 | r=16, lr=0.0001, epochs=3 |
| email | 1 | tfidf | 2982 | 746 | 1780 | 0.953 | 0.997 | 0.961 | 0.050 | 0.049 | 0.802 | 0.337 | 0.337 | 0.363 | C=10.0 |
| table | 1 | frozen | 2848 | 712 | 1948 | 0.995 | 0.909 | 0.635 | 0.670 | 0.695 | 0.045 | 0.041 | 0.000 | 0.894 | C=10.0 |
| table | 1 | lora | 2848 | 712 | 1948 | 1.000 | 0.962 | 0.773 | 0.349 | 0.416 | 0.586 | 0.579 | 0.578 | 0.779 | r=16, lr=0.0001, epochs=3 |
| table | 1 | tfidf | 2848 | 712 | 1948 | 0.982 | 0.979 | 0.921 | 0.051 | 0.053 | 0.065 | 0.050 | 0.050 | 0.558 | C=10.0 |
| code | 2 | frozen | 2982 | 746 | 1780 | 0.983 | 0.977 | 0.725 | 0.057 | 0.050 | 0.194 | 0.115 | 0.115 | 0.965 | C=0.1 |
| code | 2 | lora | 2982 | 746 | 1780 | 0.995 | 0.998 | 0.969 | 0.044 | 0.054 | 0.910 | 0.864 | 0.864 | 0.717 | r=8, lr=0.0001, epochs=3 |
| code | 2 | tfidf | 2982 | 746 | 1780 | 0.975 | 0.990 | 0.869 | 0.051 | 0.050 | 0.246 | 0.238 | 0.238 | 0.619 | C=10.0 |
| email | 2 | frozen | 2982 | 746 | 1780 | 0.978 | 0.991 | 0.869 | 0.056 | 0.056 | 0.415 | 0.415 | 0.415 | 1.000 | C=0.1 |
| email | 2 | lora | 2982 | 746 | 1780 | 0.994 | 0.999 | 0.981 | 0.020 | 0.049 | 0.510 | 0.429 | 0.429 | 0.124 | r=8, lr=0.0001, epochs=3 |
| email | 2 | tfidf | 2982 | 746 | 1780 | 0.957 | 0.998 | 0.966 | 0.048 | 0.048 | 0.794 | 0.345 | 0.345 | 0.425 | C=10.0 |
| table | 2 | frozen | 2848 | 712 | 1948 | 0.992 | 0.907 | 0.635 | 0.686 | 0.712 | 0.054 | 0.014 | 0.002 | 0.805 | C=1.0 |
| table | 2 | lora | 2848 | 712 | 1948 | 1.000 | 0.961 | 0.769 | 0.215 | 0.211 | 0.595 | 0.575 | 0.326 | 0.770 | r=16, lr=0.0001, epochs=3 |
| table | 2 | tfidf | 2848 | 712 | 1948 | 0.973 | 0.981 | 0.923 | 0.051 | 0.049 | 0.055 | 0.053 | 0.053 | 0.354 | C=10.0 |

## Raw table 3 -- BIPIA per-type detail

This expands every metrics file that contains `per_type`. The `drop` column is validation AUPRC minus that type's test AUPRC inside the source metric file.

| Fold | Seed | Model | Type | Test AUPRC | Drop | n_pos | n_total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| carrier_lodo_code | 0 | frozen | Alphanumeric Substitution | 0.553 | 0.434 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Anagramming | 0.611 | 0.376 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Base Encoding | 0.509 | 0.478 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Business Intelligence | 0.606 | 0.381 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Clickbait | 0.622 | 0.365 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Content Creation | 0.585 | 0.402 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Conversational Agent | 0.507 | 0.480 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Emoji Substitution | 0.637 | 0.350 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Entertainment | 0.653 | 0.334 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Homophonic Substitution | 0.624 | 0.363 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Information Dissemination | 0.650 | 0.337 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Information Retrieval | 0.547 | 0.440 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Instruction | 0.624 | 0.363 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Learning and Tutoring | 0.563 | 0.424 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Malware Distribution | 0.689 | 0.298 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Marketing & Advertising | 0.667 | 0.320 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Misinformation & Propaganda | 0.653 | 0.334 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Misspelling Intentionally | 0.592 | 0.395 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Persuasion | 0.657 | 0.330 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Programming Help | 0.643 | 0.344 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Research Assistance | 0.618 | 0.369 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Reverse Text | 0.586 | 0.401 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Scams & Fraud | 0.631 | 0.356 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Sentiment Analysis | 0.626 | 0.361 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Social Interaction | 0.631 | 0.356 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Space Removal & Grouping | 0.553 | 0.434 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Substitution Ciphers | 0.571 | 0.416 | 60 | 160 |
| carrier_lodo_code | 0 | frozen | Task Automation | 0.599 | 0.388 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Alphanumeric Substitution | 0.930 | 0.068 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Anagramming | 0.913 | 0.085 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Base Encoding | 0.982 | 0.016 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Business Intelligence | 0.992 | 0.006 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Clickbait | 0.935 | 0.064 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Content Creation | 0.954 | 0.044 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Conversational Agent | 0.994 | 0.004 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Emoji Substitution | 0.992 | 0.007 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Entertainment | 0.999 | -0.001 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Homophonic Substitution | 0.923 | 0.075 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Information Dissemination | 0.997 | 0.001 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Information Retrieval | 0.919 | 0.079 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Instruction | 0.923 | 0.075 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Learning and Tutoring | 0.910 | 0.088 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Malware Distribution | 0.940 | 0.058 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Marketing & Advertising | 0.997 | 0.001 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Misinformation & Propaganda | 0.997 | 0.001 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Misspelling Intentionally | 0.952 | 0.046 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Persuasion | 0.918 | 0.080 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Programming Help | 0.922 | 0.076 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Research Assistance | 0.995 | 0.003 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Reverse Text | 0.976 | 0.023 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Scams & Fraud | 0.985 | 0.013 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Sentiment Analysis | 0.970 | 0.028 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Social Interaction | 0.921 | 0.078 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Space Removal & Grouping | 0.911 | 0.087 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Substitution Ciphers | 0.995 | 0.003 | 60 | 160 |
| carrier_lodo_code | 0 | lora | Task Automation | 0.996 | 0.002 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Alphanumeric Substitution | 0.783 | 0.194 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Anagramming | 0.803 | 0.173 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Base Encoding | 0.766 | 0.211 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Business Intelligence | 0.744 | 0.232 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Clickbait | 0.821 | 0.155 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Content Creation | 0.682 | 0.294 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Conversational Agent | 0.711 | 0.266 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Emoji Substitution | 0.840 | 0.136 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Entertainment | 0.872 | 0.105 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Homophonic Substitution | 0.821 | 0.156 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Information Dissemination | 0.867 | 0.110 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Information Retrieval | 0.719 | 0.258 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Instruction | 0.825 | 0.152 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Learning and Tutoring | 0.677 | 0.300 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Malware Distribution | 0.798 | 0.178 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Marketing & Advertising | 0.893 | 0.084 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Misinformation & Propaganda | 0.842 | 0.134 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Misspelling Intentionally | 0.781 | 0.196 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Persuasion | 0.847 | 0.129 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Programming Help | 0.767 | 0.209 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Research Assistance | 0.753 | 0.223 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Reverse Text | 0.740 | 0.236 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Scams & Fraud | 0.854 | 0.122 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Sentiment Analysis | 0.763 | 0.213 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Social Interaction | 0.808 | 0.169 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Space Removal & Grouping | 0.752 | 0.225 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Substitution Ciphers | 0.791 | 0.185 | 60 | 160 |
| carrier_lodo_code | 0 | tfidf | Task Automation | 0.786 | 0.190 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Alphanumeric Substitution | 0.899 | 0.081 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Anagramming | 0.909 | 0.071 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Base Encoding | 0.825 | 0.155 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Business Intelligence | 0.712 | 0.268 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Clickbait | 0.872 | 0.108 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Content Creation | 0.837 | 0.143 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Conversational Agent | 0.743 | 0.237 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Emoji Substitution | 0.910 | 0.070 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Entertainment | 0.880 | 0.100 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Homophonic Substitution | 0.931 | 0.049 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Information Dissemination | 0.835 | 0.145 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Information Retrieval | 0.759 | 0.221 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Instruction | 0.857 | 0.123 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Learning and Tutoring | 0.754 | 0.226 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Malware Distribution | 0.895 | 0.085 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Marketing & Advertising | 0.813 | 0.167 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Misinformation & Propaganda | 0.857 | 0.123 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Misspelling Intentionally | 0.901 | 0.079 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Persuasion | 0.883 | 0.097 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Programming Help | 0.889 | 0.091 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Research Assistance | 0.689 | 0.291 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Reverse Text | 0.801 | 0.179 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Scams & Fraud | 0.921 | 0.059 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Sentiment Analysis | 0.709 | 0.271 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Social Interaction | 0.861 | 0.119 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Space Removal & Grouping | 0.852 | 0.128 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Substitution Ciphers | 0.929 | 0.051 | 60 | 160 |
| carrier_lodo_email | 0 | frozen | Task Automation | 0.745 | 0.235 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Alphanumeric Substitution | 0.940 | 0.057 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Anagramming | 0.973 | 0.025 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Base Encoding | 0.964 | 0.034 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Business Intelligence | 0.939 | 0.058 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Clickbait | 0.976 | 0.022 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Content Creation | 0.982 | 0.016 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Conversational Agent | 0.972 | 0.026 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Emoji Substitution | 0.977 | 0.021 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Entertainment | 0.972 | 0.025 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Homophonic Substitution | 0.950 | 0.047 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Information Dissemination | 0.972 | 0.026 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Information Retrieval | 0.914 | 0.084 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Instruction | 0.985 | 0.013 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Learning and Tutoring | 0.915 | 0.083 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Malware Distribution | 0.902 | 0.095 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Marketing & Advertising | 0.963 | 0.035 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Misinformation & Propaganda | 0.985 | 0.013 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Misspelling Intentionally | 0.961 | 0.037 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Persuasion | 0.973 | 0.025 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Programming Help | 0.942 | 0.055 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Research Assistance | 0.951 | 0.047 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Reverse Text | 0.981 | 0.017 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Scams & Fraud | 0.946 | 0.052 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Sentiment Analysis | 0.765 | 0.233 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Social Interaction | 0.951 | 0.047 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Space Removal & Grouping | 0.966 | 0.032 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Substitution Ciphers | 0.987 | 0.011 | 60 | 160 |
| carrier_lodo_email | 0 | lora | Task Automation | 0.954 | 0.044 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Alphanumeric Substitution | 0.929 | 0.021 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Anagramming | 0.937 | 0.013 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Base Encoding | 0.913 | 0.037 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Business Intelligence | 0.927 | 0.023 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Clickbait | 0.940 | 0.010 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Content Creation | 0.858 | 0.092 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Conversational Agent | 0.887 | 0.063 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Emoji Substitution | 0.961 | -0.011 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Entertainment | 0.974 | -0.024 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Homophonic Substitution | 0.928 | 0.022 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Information Dissemination | 0.972 | -0.022 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Information Retrieval | 0.828 | 0.122 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Instruction | 0.954 | -0.004 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Learning and Tutoring | 0.780 | 0.170 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Malware Distribution | 0.962 | -0.012 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Marketing & Advertising | 0.977 | -0.027 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Misinformation & Propaganda | 0.942 | 0.008 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Misspelling Intentionally | 0.928 | 0.022 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Persuasion | 0.965 | -0.015 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Programming Help | 0.854 | 0.096 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Research Assistance | 0.921 | 0.029 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Reverse Text | 0.887 | 0.063 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Scams & Fraud | 0.969 | -0.019 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Sentiment Analysis | 0.949 | 0.001 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Social Interaction | 0.945 | 0.005 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Space Removal & Grouping | 0.909 | 0.041 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Substitution Ciphers | 0.952 | -0.002 | 60 | 160 |
| carrier_lodo_email | 0 | tfidf | Task Automation | 0.903 | 0.047 | 60 | 160 |
| carrier_lodo_table | 0 | frozen | Alphanumeric Substitution | 0.256 | 0.743 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Anagramming | 0.298 | 0.701 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Base Encoding | 0.250 | 0.749 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Business Intelligence | 0.283 | 0.717 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Clickbait | 0.274 | 0.725 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Content Creation | 0.273 | 0.726 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Conversational Agent | 0.238 | 0.761 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Emoji Substitution | 0.271 | 0.728 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Entertainment | 0.229 | 0.771 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Homophonic Substitution | 0.274 | 0.726 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Information Dissemination | 0.263 | 0.737 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Information Retrieval | 0.270 | 0.729 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Instruction | 0.257 | 0.742 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Learning and Tutoring | 0.386 | 0.613 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Malware Distribution | 0.296 | 0.704 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Marketing & Advertising | 0.306 | 0.693 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Misinformation & Propaganda | 0.230 | 0.769 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Misspelling Intentionally | 0.298 | 0.702 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Persuasion | 0.357 | 0.643 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Programming Help | 0.289 | 0.711 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Research Assistance | 0.347 | 0.652 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Reverse Text | 0.205 | 0.794 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Scams & Fraud | 0.249 | 0.750 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Sentiment Analysis | 0.289 | 0.710 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Social Interaction | 0.319 | 0.680 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Space Removal & Grouping | 0.329 | 0.670 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Substitution Ciphers | 0.228 | 0.771 | 60 | 328 |
| carrier_lodo_table | 0 | frozen | Task Automation | 0.368 | 0.631 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Alphanumeric Substitution | 0.796 | 0.204 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Anagramming | 0.795 | 0.205 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Base Encoding | 0.845 | 0.155 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Business Intelligence | 0.792 | 0.208 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Clickbait | 0.696 | 0.304 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Content Creation | 0.815 | 0.185 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Conversational Agent | 0.731 | 0.269 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Emoji Substitution | 0.740 | 0.260 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Entertainment | 0.794 | 0.206 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Homophonic Substitution | 0.796 | 0.204 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Information Dissemination | 0.783 | 0.217 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Information Retrieval | 0.758 | 0.242 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Instruction | 0.718 | 0.282 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Learning and Tutoring | 0.793 | 0.206 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Malware Distribution | 0.832 | 0.168 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Marketing & Advertising | 0.733 | 0.267 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Misinformation & Propaganda | 0.679 | 0.321 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Misspelling Intentionally | 0.807 | 0.193 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Persuasion | 0.745 | 0.255 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Programming Help | 0.809 | 0.191 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Research Assistance | 0.777 | 0.223 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Reverse Text | 0.722 | 0.277 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Scams & Fraud | 0.784 | 0.216 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Sentiment Analysis | 0.768 | 0.232 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Social Interaction | 0.794 | 0.205 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Space Removal & Grouping | 0.811 | 0.189 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Substitution Ciphers | 0.752 | 0.248 | 60 | 328 |
| carrier_lodo_table | 0 | lora | Task Automation | 0.821 | 0.179 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Alphanumeric Substitution | 0.711 | 0.277 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Anagramming | 0.771 | 0.216 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Base Encoding | 0.685 | 0.302 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Business Intelligence | 0.674 | 0.313 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Clickbait | 0.708 | 0.279 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Content Creation | 0.617 | 0.370 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Conversational Agent | 0.574 | 0.413 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Emoji Substitution | 0.723 | 0.264 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Entertainment | 0.739 | 0.248 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Homophonic Substitution | 0.715 | 0.272 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Information Dissemination | 0.737 | 0.251 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Information Retrieval | 0.648 | 0.339 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Instruction | 0.709 | 0.278 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Learning and Tutoring | 0.654 | 0.333 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Malware Distribution | 0.746 | 0.241 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Marketing & Advertising | 0.750 | 0.237 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Misinformation & Propaganda | 0.753 | 0.234 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Misspelling Intentionally | 0.723 | 0.264 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Persuasion | 0.752 | 0.235 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Programming Help | 0.643 | 0.344 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Research Assistance | 0.698 | 0.289 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Reverse Text | 0.652 | 0.335 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Scams & Fraud | 0.768 | 0.219 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Sentiment Analysis | 0.647 | 0.340 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Social Interaction | 0.735 | 0.252 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Space Removal & Grouping | 0.770 | 0.217 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Substitution Ciphers | 0.717 | 0.270 | 60 | 328 |
| carrier_lodo_table | 0 | tfidf | Task Automation | 0.717 | 0.270 | 60 | 328 |
| carrier_plus_attack_external | 0 | frozen | Base Encoding | 0.826 | 0.134 | 60 | 110 |
| carrier_plus_attack_external | 0 | frozen | Business Intelligence | 0.690 | 0.270 | 60 | 110 |
| carrier_plus_attack_external | 0 | frozen | Conversational Agent | 0.807 | 0.154 | 60 | 110 |
| carrier_plus_attack_external | 0 | frozen | Emoji Substitution | 0.907 | 0.054 | 60 | 110 |
| carrier_plus_attack_external | 0 | frozen | Entertainment | 0.837 | 0.123 | 60 | 110 |
| carrier_plus_attack_external | 0 | frozen | Information Dissemination | 0.845 | 0.115 | 60 | 110 |
| carrier_plus_attack_external | 0 | frozen | Marketing & Advertising | 0.845 | 0.115 | 60 | 110 |
| carrier_plus_attack_external | 0 | frozen | Misinformation & Propaganda | 0.854 | 0.106 | 60 | 110 |
| carrier_plus_attack_external | 0 | frozen | Research Assistance | 0.723 | 0.238 | 60 | 110 |
| carrier_plus_attack_external | 0 | frozen | Reverse Text | 0.842 | 0.119 | 60 | 110 |
| carrier_plus_attack_external | 0 | frozen | Scams & Fraud | 0.919 | 0.041 | 60 | 110 |
| carrier_plus_attack_external | 0 | frozen | Sentiment Analysis | 0.809 | 0.152 | 60 | 110 |
| carrier_plus_attack_external | 0 | frozen | Substitution Ciphers | 0.901 | 0.060 | 60 | 110 |
| carrier_plus_attack_external | 0 | frozen | Task Automation | 0.780 | 0.181 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Base Encoding | 0.998 | -0.002 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Business Intelligence | 0.988 | 0.008 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Conversational Agent | 0.998 | -0.003 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Emoji Substitution | 0.998 | -0.003 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Entertainment | 0.996 | -0.001 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Information Dissemination | 0.995 | 0.001 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Marketing & Advertising | 0.992 | 0.003 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Misinformation & Propaganda | 0.998 | -0.003 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Research Assistance | 0.984 | 0.011 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Reverse Text | 0.996 | -0.000 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Scams & Fraud | 0.968 | 0.027 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Sentiment Analysis | 0.759 | 0.236 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Substitution Ciphers | 0.998 | -0.002 | 60 | 110 |
| carrier_plus_attack_external | 0 | lora | Task Automation | 0.988 | 0.008 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Base Encoding | 0.937 | -0.025 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Business Intelligence | 0.811 | 0.101 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Conversational Agent | 0.675 | 0.237 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Emoji Substitution | 0.971 | -0.059 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Entertainment | 0.980 | -0.068 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Information Dissemination | 0.980 | -0.067 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Marketing & Advertising | 0.980 | -0.068 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Misinformation & Propaganda | 0.967 | -0.055 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Research Assistance | 0.798 | 0.115 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Reverse Text | 0.912 | 0.001 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Scams & Fraud | 0.980 | -0.067 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Sentiment Analysis | 0.736 | 0.177 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Substitution Ciphers | 0.960 | -0.048 | 60 | 110 |
| carrier_plus_attack_external | 0 | tfidf | Task Automation | 0.704 | 0.209 | 60 | 110 |
| core_attack_type | 0 | frozen | Base Encoding | 0.837 | 0.141 | 180 | 380 |
| core_attack_type | 0 | frozen | Business Intelligence | 0.755 | 0.223 | 180 | 380 |
| core_attack_type | 0 | frozen | Conversational Agent | 0.761 | 0.217 | 180 | 380 |
| core_attack_type | 0 | frozen | Emoji Substitution | 0.892 | 0.086 | 180 | 380 |
| core_attack_type | 0 | frozen | Entertainment | 0.863 | 0.114 | 180 | 380 |
| core_attack_type | 0 | frozen | Information Dissemination | 0.848 | 0.130 | 180 | 380 |
| core_attack_type | 0 | frozen | Marketing & Advertising | 0.834 | 0.143 | 180 | 380 |
| core_attack_type | 0 | frozen | Misinformation & Propaganda | 0.869 | 0.108 | 180 | 380 |
| core_attack_type | 0 | frozen | Research Assistance | 0.779 | 0.199 | 180 | 380 |
| core_attack_type | 0 | frozen | Reverse Text | 0.822 | 0.156 | 180 | 380 |
| core_attack_type | 0 | frozen | Scams & Fraud | 0.882 | 0.095 | 180 | 380 |
| core_attack_type | 0 | frozen | Sentiment Analysis | 0.800 | 0.178 | 180 | 380 |
| core_attack_type | 0 | frozen | Substitution Ciphers | 0.864 | 0.113 | 180 | 380 |
| core_attack_type | 0 | frozen | Task Automation | 0.799 | 0.179 | 180 | 380 |
| core_attack_type | 0 | lora | Base Encoding | 0.990 | 0.007 | 180 | 380 |
| core_attack_type | 0 | lora | Business Intelligence | 0.987 | 0.010 | 180 | 380 |
| core_attack_type | 0 | lora | Conversational Agent | 0.984 | 0.013 | 180 | 380 |
| core_attack_type | 0 | lora | Emoji Substitution | 0.983 | 0.014 | 180 | 380 |
| core_attack_type | 0 | lora | Entertainment | 0.985 | 0.012 | 180 | 380 |
| core_attack_type | 0 | lora | Information Dissemination | 0.988 | 0.009 | 180 | 380 |
| core_attack_type | 0 | lora | Marketing & Advertising | 0.984 | 0.013 | 180 | 380 |
| core_attack_type | 0 | lora | Misinformation & Propaganda | 0.982 | 0.015 | 180 | 380 |
| core_attack_type | 0 | lora | Research Assistance | 0.985 | 0.012 | 180 | 380 |
| core_attack_type | 0 | lora | Reverse Text | 0.985 | 0.012 | 180 | 380 |
| core_attack_type | 0 | lora | Scams & Fraud | 0.976 | 0.021 | 180 | 380 |
| core_attack_type | 0 | lora | Sentiment Analysis | 0.951 | 0.046 | 180 | 380 |
| core_attack_type | 0 | lora | Substitution Ciphers | 0.981 | 0.016 | 180 | 380 |
| core_attack_type | 0 | lora | Task Automation | 0.987 | 0.010 | 180 | 380 |
| core_attack_type | 0 | tfidf | Base Encoding | 0.779 | 0.166 | 180 | 380 |
| core_attack_type | 0 | tfidf | Business Intelligence | 0.665 | 0.280 | 180 | 380 |
| core_attack_type | 0 | tfidf | Conversational Agent | 0.574 | 0.372 | 180 | 380 |
| core_attack_type | 0 | tfidf | Emoji Substitution | 0.868 | 0.077 | 180 | 380 |
| core_attack_type | 0 | tfidf | Entertainment | 0.898 | 0.048 | 180 | 380 |
| core_attack_type | 0 | tfidf | Information Dissemination | 0.911 | 0.034 | 180 | 380 |
| core_attack_type | 0 | tfidf | Marketing & Advertising | 0.905 | 0.040 | 180 | 380 |
| core_attack_type | 0 | tfidf | Misinformation & Propaganda | 0.881 | 0.064 | 180 | 380 |
| core_attack_type | 0 | tfidf | Research Assistance | 0.665 | 0.280 | 180 | 380 |
| core_attack_type | 0 | tfidf | Reverse Text | 0.771 | 0.174 | 180 | 380 |
| core_attack_type | 0 | tfidf | Scams & Fraud | 0.876 | 0.070 | 180 | 380 |
| core_attack_type | 0 | tfidf | Sentiment Analysis | 0.612 | 0.333 | 180 | 380 |
| core_attack_type | 0 | tfidf | Substitution Ciphers | 0.840 | 0.106 | 180 | 380 |
| core_attack_type | 0 | tfidf | Task Automation | 0.635 | 0.311 | 180 | 380 |
| obfuscation_technique | 0 | frozen | Base Encoding | 0.877 | 0.072 | 180 | 380 |
| obfuscation_technique | 0 | frozen | Emoji Substitution | 0.895 | 0.055 | 180 | 380 |
| obfuscation_technique | 0 | frozen | Reverse Text | 0.847 | 0.102 | 180 | 380 |
| obfuscation_technique | 0 | frozen | Substitution Ciphers | 0.892 | 0.057 | 180 | 380 |
| obfuscation_technique | 0 | lora | Base Encoding | 0.979 | 0.002 | 180 | 380 |
| obfuscation_technique | 0 | lora | Emoji Substitution | 0.967 | 0.014 | 180 | 380 |
| obfuscation_technique | 0 | lora | Reverse Text | 0.965 | 0.016 | 180 | 380 |
| obfuscation_technique | 0 | lora | Substitution Ciphers | 0.965 | 0.016 | 180 | 380 |
| obfuscation_technique | 0 | tfidf | Base Encoding | 0.846 | 0.111 | 180 | 380 |
| obfuscation_technique | 0 | tfidf | Emoji Substitution | 0.898 | 0.060 | 180 | 380 |
| obfuscation_technique | 0 | tfidf | Reverse Text | 0.818 | 0.140 | 180 | 380 |
| obfuscation_technique | 0 | tfidf | Substitution Ciphers | 0.874 | 0.083 | 180 | 380 |
| carrier_lodo_code | 1 | frozen | Alphanumeric Substitution | 0.684 | 0.307 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Anagramming | 0.698 | 0.293 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Base Encoding | 0.638 | 0.353 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Business Intelligence | 0.590 | 0.401 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Clickbait | 0.649 | 0.342 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Content Creation | 0.635 | 0.356 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Conversational Agent | 0.617 | 0.375 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Emoji Substitution | 0.719 | 0.273 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Entertainment | 0.707 | 0.284 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Homophonic Substitution | 0.667 | 0.325 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Information Dissemination | 0.729 | 0.263 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Information Retrieval | 0.523 | 0.468 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Instruction | 0.692 | 0.299 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Learning and Tutoring | 0.655 | 0.336 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Malware Distribution | 0.674 | 0.317 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Marketing & Advertising | 0.686 | 0.306 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Misinformation & Propaganda | 0.609 | 0.383 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Misspelling Intentionally | 0.706 | 0.285 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Persuasion | 0.714 | 0.278 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Programming Help | 0.628 | 0.364 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Research Assistance | 0.653 | 0.338 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Reverse Text | 0.628 | 0.363 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Scams & Fraud | 0.645 | 0.346 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Sentiment Analysis | 0.582 | 0.409 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Social Interaction | 0.715 | 0.276 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Space Removal & Grouping | 0.670 | 0.322 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Substitution Ciphers | 0.699 | 0.292 | 60 | 160 |
| carrier_lodo_code | 1 | frozen | Task Automation | 0.594 | 0.397 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Alphanumeric Substitution | 0.942 | 0.055 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Anagramming | 0.953 | 0.044 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Base Encoding | 0.999 | -0.002 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Business Intelligence | 1.000 | -0.003 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Clickbait | 0.942 | 0.055 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Content Creation | 0.972 | 0.025 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Conversational Agent | 1.000 | -0.003 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Emoji Substitution | 1.000 | -0.003 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Entertainment | 1.000 | -0.003 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Homophonic Substitution | 0.890 | 0.107 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Information Dissemination | 1.000 | -0.003 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Information Retrieval | 0.933 | 0.064 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Instruction | 0.944 | 0.053 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Learning and Tutoring | 0.935 | 0.062 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Malware Distribution | 0.918 | 0.079 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Marketing & Advertising | 1.000 | -0.003 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Misinformation & Propaganda | 1.000 | -0.003 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Misspelling Intentionally | 0.966 | 0.031 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Persuasion | 0.972 | 0.025 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Programming Help | 0.919 | 0.078 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Research Assistance | 1.000 | -0.003 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Reverse Text | 1.000 | -0.003 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Scams & Fraud | 0.989 | 0.008 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Sentiment Analysis | 0.986 | 0.011 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Social Interaction | 0.944 | 0.053 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Space Removal & Grouping | 0.949 | 0.048 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Substitution Ciphers | 0.999 | -0.002 | 60 | 160 |
| carrier_lodo_code | 1 | lora | Task Automation | 1.000 | -0.003 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Alphanumeric Substitution | 0.769 | 0.210 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Anagramming | 0.811 | 0.168 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Base Encoding | 0.767 | 0.212 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Business Intelligence | 0.733 | 0.245 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Clickbait | 0.772 | 0.206 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Content Creation | 0.594 | 0.385 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Conversational Agent | 0.719 | 0.260 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Emoji Substitution | 0.798 | 0.180 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Entertainment | 0.911 | 0.068 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Homophonic Substitution | 0.811 | 0.168 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Information Dissemination | 0.906 | 0.073 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Information Retrieval | 0.653 | 0.325 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Instruction | 0.773 | 0.206 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Learning and Tutoring | 0.649 | 0.329 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Malware Distribution | 0.807 | 0.171 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Marketing & Advertising | 0.921 | 0.057 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Misinformation & Propaganda | 0.856 | 0.122 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Misspelling Intentionally | 0.823 | 0.155 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Persuasion | 0.862 | 0.116 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Programming Help | 0.713 | 0.265 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Research Assistance | 0.822 | 0.157 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Reverse Text | 0.773 | 0.205 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Scams & Fraud | 0.856 | 0.122 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Sentiment Analysis | 0.793 | 0.185 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Social Interaction | 0.826 | 0.152 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Space Removal & Grouping | 0.798 | 0.181 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Substitution Ciphers | 0.821 | 0.158 | 60 | 160 |
| carrier_lodo_code | 1 | tfidf | Task Automation | 0.745 | 0.233 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Alphanumeric Substitution | 0.875 | 0.103 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Anagramming | 0.917 | 0.060 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Base Encoding | 0.834 | 0.143 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Business Intelligence | 0.720 | 0.258 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Clickbait | 0.913 | 0.064 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Content Creation | 0.850 | 0.127 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Conversational Agent | 0.790 | 0.187 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Emoji Substitution | 0.931 | 0.046 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Entertainment | 0.878 | 0.099 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Homophonic Substitution | 0.856 | 0.121 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Information Dissemination | 0.854 | 0.123 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Information Retrieval | 0.816 | 0.162 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Instruction | 0.904 | 0.073 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Learning and Tutoring | 0.855 | 0.122 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Malware Distribution | 0.945 | 0.033 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Marketing & Advertising | 0.807 | 0.171 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Misinformation & Propaganda | 0.885 | 0.092 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Misspelling Intentionally | 0.872 | 0.105 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Persuasion | 0.885 | 0.093 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Programming Help | 0.864 | 0.114 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Research Assistance | 0.730 | 0.248 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Reverse Text | 0.824 | 0.154 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Scams & Fraud | 0.881 | 0.096 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Sentiment Analysis | 0.700 | 0.278 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Social Interaction | 0.917 | 0.060 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Space Removal & Grouping | 0.846 | 0.132 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Substitution Ciphers | 0.948 | 0.029 | 60 | 160 |
| carrier_lodo_email | 1 | frozen | Task Automation | 0.840 | 0.137 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Alphanumeric Substitution | 0.958 | 0.037 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Anagramming | 0.974 | 0.022 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Base Encoding | 0.971 | 0.025 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Business Intelligence | 0.981 | 0.015 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Clickbait | 0.974 | 0.022 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Content Creation | 0.978 | 0.018 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Conversational Agent | 0.971 | 0.024 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Emoji Substitution | 0.979 | 0.017 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Entertainment | 0.983 | 0.013 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Homophonic Substitution | 0.966 | 0.029 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Information Dissemination | 0.987 | 0.008 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Information Retrieval | 0.940 | 0.055 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Instruction | 0.982 | 0.014 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Learning and Tutoring | 0.953 | 0.042 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Malware Distribution | 0.946 | 0.050 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Marketing & Advertising | 0.983 | 0.013 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Misinformation & Propaganda | 0.990 | 0.006 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Misspelling Intentionally | 0.977 | 0.019 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Persuasion | 0.979 | 0.016 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Programming Help | 0.949 | 0.046 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Research Assistance | 0.965 | 0.030 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Reverse Text | 0.979 | 0.016 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Scams & Fraud | 0.978 | 0.017 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Sentiment Analysis | 0.764 | 0.232 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Social Interaction | 0.962 | 0.033 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Space Removal & Grouping | 0.972 | 0.024 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Substitution Ciphers | 0.987 | 0.009 | 60 | 160 |
| carrier_lodo_email | 1 | lora | Task Automation | 0.960 | 0.036 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Alphanumeric Substitution | 0.949 | 0.004 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Anagramming | 0.983 | -0.030 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Base Encoding | 0.934 | 0.019 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Business Intelligence | 0.916 | 0.037 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Clickbait | 0.974 | -0.021 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Content Creation | 0.845 | 0.108 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Conversational Agent | 0.927 | 0.026 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Emoji Substitution | 0.971 | -0.018 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Entertainment | 0.991 | -0.038 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Homophonic Substitution | 0.928 | 0.025 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Information Dissemination | 0.988 | -0.035 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Information Retrieval | 0.860 | 0.093 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Instruction | 0.966 | -0.013 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Learning and Tutoring | 0.871 | 0.082 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Malware Distribution | 0.982 | -0.029 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Marketing & Advertising | 0.992 | -0.039 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Misinformation & Propaganda | 0.977 | -0.024 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Misspelling Intentionally | 0.944 | 0.009 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Persuasion | 0.971 | -0.018 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Programming Help | 0.888 | 0.065 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Research Assistance | 0.944 | 0.009 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Reverse Text | 0.920 | 0.033 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Scams & Fraud | 0.985 | -0.032 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Sentiment Analysis | 0.957 | -0.004 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Social Interaction | 0.977 | -0.024 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Space Removal & Grouping | 0.965 | -0.012 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Substitution Ciphers | 0.973 | -0.020 | 60 | 160 |
| carrier_lodo_email | 1 | tfidf | Task Automation | 0.922 | 0.031 | 60 | 160 |
| carrier_lodo_table | 1 | frozen | Alphanumeric Substitution | 0.365 | 0.630 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Anagramming | 0.386 | 0.609 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Base Encoding | 0.216 | 0.778 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Business Intelligence | 0.322 | 0.673 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Clickbait | 0.279 | 0.715 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Content Creation | 0.266 | 0.729 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Conversational Agent | 0.207 | 0.787 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Emoji Substitution | 0.283 | 0.712 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Entertainment | 0.303 | 0.691 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Homophonic Substitution | 0.281 | 0.713 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Information Dissemination | 0.287 | 0.707 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Information Retrieval | 0.271 | 0.724 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Instruction | 0.288 | 0.707 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Learning and Tutoring | 0.316 | 0.679 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Malware Distribution | 0.336 | 0.659 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Marketing & Advertising | 0.288 | 0.707 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Misinformation & Propaganda | 0.336 | 0.659 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Misspelling Intentionally | 0.266 | 0.728 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Persuasion | 0.354 | 0.640 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Programming Help | 0.328 | 0.667 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Research Assistance | 0.231 | 0.763 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Reverse Text | 0.204 | 0.791 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Scams & Fraud | 0.246 | 0.748 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Sentiment Analysis | 0.239 | 0.755 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Social Interaction | 0.282 | 0.713 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Space Removal & Grouping | 0.333 | 0.661 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Substitution Ciphers | 0.304 | 0.690 | 60 | 328 |
| carrier_lodo_table | 1 | frozen | Task Automation | 0.306 | 0.688 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Alphanumeric Substitution | 0.768 | 0.232 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Anagramming | 0.805 | 0.194 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Base Encoding | 0.650 | 0.350 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Business Intelligence | 0.729 | 0.271 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Clickbait | 0.650 | 0.350 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Content Creation | 0.749 | 0.251 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Conversational Agent | 0.722 | 0.278 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Emoji Substitution | 0.819 | 0.181 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Entertainment | 0.732 | 0.268 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Homophonic Substitution | 0.706 | 0.294 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Information Dissemination | 0.732 | 0.268 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Information Retrieval | 0.741 | 0.259 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Instruction | 0.715 | 0.285 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Learning and Tutoring | 0.669 | 0.331 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Malware Distribution | 0.747 | 0.253 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Marketing & Advertising | 0.754 | 0.246 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Misinformation & Propaganda | 0.728 | 0.271 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Misspelling Intentionally | 0.745 | 0.255 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Persuasion | 0.825 | 0.175 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Programming Help | 0.718 | 0.281 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Research Assistance | 0.633 | 0.367 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Reverse Text | 0.654 | 0.346 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Scams & Fraud | 0.630 | 0.369 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Sentiment Analysis | 0.567 | 0.433 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Social Interaction | 0.673 | 0.327 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Space Removal & Grouping | 0.784 | 0.216 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Substitution Ciphers | 0.727 | 0.273 | 60 | 328 |
| carrier_lodo_table | 1 | lora | Task Automation | 0.681 | 0.319 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Alphanumeric Substitution | 0.725 | 0.257 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Anagramming | 0.745 | 0.237 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Base Encoding | 0.587 | 0.395 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Business Intelligence | 0.590 | 0.392 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Clickbait | 0.606 | 0.377 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Content Creation | 0.508 | 0.475 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Conversational Agent | 0.528 | 0.454 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Emoji Substitution | 0.675 | 0.307 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Entertainment | 0.725 | 0.257 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Homophonic Substitution | 0.681 | 0.301 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Information Dissemination | 0.709 | 0.273 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Information Retrieval | 0.524 | 0.458 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Instruction | 0.657 | 0.325 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Learning and Tutoring | 0.552 | 0.430 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Malware Distribution | 0.676 | 0.306 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Marketing & Advertising | 0.648 | 0.334 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Misinformation & Propaganda | 0.697 | 0.285 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Misspelling Intentionally | 0.708 | 0.274 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Persuasion | 0.764 | 0.218 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Programming Help | 0.572 | 0.410 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Research Assistance | 0.588 | 0.395 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Reverse Text | 0.618 | 0.364 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Scams & Fraud | 0.624 | 0.359 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Sentiment Analysis | 0.614 | 0.369 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Social Interaction | 0.685 | 0.298 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Space Removal & Grouping | 0.668 | 0.314 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Substitution Ciphers | 0.646 | 0.336 | 60 | 328 |
| carrier_lodo_table | 1 | tfidf | Task Automation | 0.599 | 0.383 | 60 | 328 |
| carrier_plus_attack_external | 1 | frozen | Base Encoding | 0.896 | 0.073 | 60 | 110 |
| carrier_plus_attack_external | 1 | frozen | Business Intelligence | 0.741 | 0.228 | 60 | 110 |
| carrier_plus_attack_external | 1 | frozen | Conversational Agent | 0.819 | 0.150 | 60 | 110 |
| carrier_plus_attack_external | 1 | frozen | Emoji Substitution | 0.927 | 0.042 | 60 | 110 |
| carrier_plus_attack_external | 1 | frozen | Entertainment | 0.893 | 0.076 | 60 | 110 |
| carrier_plus_attack_external | 1 | frozen | Information Dissemination | 0.879 | 0.089 | 60 | 110 |
| carrier_plus_attack_external | 1 | frozen | Marketing & Advertising | 0.813 | 0.156 | 60 | 110 |
| carrier_plus_attack_external | 1 | frozen | Misinformation & Propaganda | 0.863 | 0.105 | 60 | 110 |
| carrier_plus_attack_external | 1 | frozen | Research Assistance | 0.795 | 0.174 | 60 | 110 |
| carrier_plus_attack_external | 1 | frozen | Reverse Text | 0.871 | 0.098 | 60 | 110 |
| carrier_plus_attack_external | 1 | frozen | Scams & Fraud | 0.891 | 0.078 | 60 | 110 |
| carrier_plus_attack_external | 1 | frozen | Sentiment Analysis | 0.757 | 0.212 | 60 | 110 |
| carrier_plus_attack_external | 1 | frozen | Substitution Ciphers | 0.922 | 0.047 | 60 | 110 |
| carrier_plus_attack_external | 1 | frozen | Task Automation | 0.809 | 0.160 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Base Encoding | 0.992 | 0.003 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Business Intelligence | 0.989 | 0.006 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Conversational Agent | 0.985 | 0.011 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Emoji Substitution | 0.994 | 0.002 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Entertainment | 0.980 | 0.016 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Information Dissemination | 0.976 | 0.020 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Marketing & Advertising | 0.981 | 0.015 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Misinformation & Propaganda | 0.987 | 0.009 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Research Assistance | 0.955 | 0.041 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Reverse Text | 0.995 | 0.000 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Scams & Fraud | 0.971 | 0.025 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Sentiment Analysis | 0.647 | 0.348 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Substitution Ciphers | 0.997 | -0.001 | 60 | 110 |
| carrier_plus_attack_external | 1 | lora | Task Automation | 0.952 | 0.043 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Base Encoding | 0.768 | 0.148 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Business Intelligence | 0.650 | 0.266 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Conversational Agent | 0.647 | 0.269 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Emoji Substitution | 0.850 | 0.066 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Entertainment | 0.850 | 0.066 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Information Dissemination | 0.837 | 0.079 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Marketing & Advertising | 0.797 | 0.119 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Misinformation & Propaganda | 0.803 | 0.113 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Research Assistance | 0.702 | 0.214 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Reverse Text | 0.737 | 0.178 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Scams & Fraud | 0.787 | 0.128 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Sentiment Analysis | 0.700 | 0.216 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Substitution Ciphers | 0.782 | 0.134 | 60 | 110 |
| carrier_plus_attack_external | 1 | tfidf | Task Automation | 0.645 | 0.271 | 60 | 110 |
| core_attack_type | 1 | frozen | Base Encoding | 0.845 | 0.136 | 180 | 380 |
| core_attack_type | 1 | frozen | Business Intelligence | 0.784 | 0.196 | 180 | 380 |
| core_attack_type | 1 | frozen | Conversational Agent | 0.774 | 0.207 | 180 | 380 |
| core_attack_type | 1 | frozen | Emoji Substitution | 0.911 | 0.070 | 180 | 380 |
| core_attack_type | 1 | frozen | Entertainment | 0.894 | 0.086 | 180 | 380 |
| core_attack_type | 1 | frozen | Information Dissemination | 0.877 | 0.104 | 180 | 380 |
| core_attack_type | 1 | frozen | Marketing & Advertising | 0.843 | 0.137 | 180 | 380 |
| core_attack_type | 1 | frozen | Misinformation & Propaganda | 0.883 | 0.098 | 180 | 380 |
| core_attack_type | 1 | frozen | Research Assistance | 0.789 | 0.191 | 180 | 380 |
| core_attack_type | 1 | frozen | Reverse Text | 0.846 | 0.134 | 180 | 380 |
| core_attack_type | 1 | frozen | Scams & Fraud | 0.854 | 0.126 | 180 | 380 |
| core_attack_type | 1 | frozen | Sentiment Analysis | 0.809 | 0.171 | 180 | 380 |
| core_attack_type | 1 | frozen | Substitution Ciphers | 0.899 | 0.082 | 180 | 380 |
| core_attack_type | 1 | frozen | Task Automation | 0.775 | 0.205 | 180 | 380 |
| core_attack_type | 1 | lora | Base Encoding | 0.966 | 0.031 | 180 | 380 |
| core_attack_type | 1 | lora | Business Intelligence | 0.977 | 0.019 | 180 | 380 |
| core_attack_type | 1 | lora | Conversational Agent | 0.976 | 0.021 | 180 | 380 |
| core_attack_type | 1 | lora | Emoji Substitution | 0.984 | 0.013 | 180 | 380 |
| core_attack_type | 1 | lora | Entertainment | 0.978 | 0.019 | 180 | 380 |
| core_attack_type | 1 | lora | Information Dissemination | 0.978 | 0.018 | 180 | 380 |
| core_attack_type | 1 | lora | Marketing & Advertising | 0.977 | 0.020 | 180 | 380 |
| core_attack_type | 1 | lora | Misinformation & Propaganda | 0.974 | 0.023 | 180 | 380 |
| core_attack_type | 1 | lora | Research Assistance | 0.963 | 0.034 | 180 | 380 |
| core_attack_type | 1 | lora | Reverse Text | 0.970 | 0.027 | 180 | 380 |
| core_attack_type | 1 | lora | Scams & Fraud | 0.958 | 0.039 | 180 | 380 |
| core_attack_type | 1 | lora | Sentiment Analysis | 0.943 | 0.053 | 180 | 380 |
| core_attack_type | 1 | lora | Substitution Ciphers | 0.973 | 0.024 | 180 | 380 |
| core_attack_type | 1 | lora | Task Automation | 0.973 | 0.024 | 180 | 380 |
| core_attack_type | 1 | tfidf | Base Encoding | 0.647 | 0.288 | 180 | 380 |
| core_attack_type | 1 | tfidf | Business Intelligence | 0.585 | 0.351 | 180 | 380 |
| core_attack_type | 1 | tfidf | Conversational Agent | 0.558 | 0.378 | 180 | 380 |
| core_attack_type | 1 | tfidf | Emoji Substitution | 0.684 | 0.251 | 180 | 380 |
| core_attack_type | 1 | tfidf | Entertainment | 0.700 | 0.235 | 180 | 380 |
| core_attack_type | 1 | tfidf | Information Dissemination | 0.717 | 0.219 | 180 | 380 |
| core_attack_type | 1 | tfidf | Marketing & Advertising | 0.700 | 0.235 | 180 | 380 |
| core_attack_type | 1 | tfidf | Misinformation & Propaganda | 0.698 | 0.238 | 180 | 380 |
| core_attack_type | 1 | tfidf | Research Assistance | 0.621 | 0.314 | 180 | 380 |
| core_attack_type | 1 | tfidf | Reverse Text | 0.648 | 0.287 | 180 | 380 |
| core_attack_type | 1 | tfidf | Scams & Fraud | 0.696 | 0.239 | 180 | 380 |
| core_attack_type | 1 | tfidf | Sentiment Analysis | 0.632 | 0.303 | 180 | 380 |
| core_attack_type | 1 | tfidf | Substitution Ciphers | 0.672 | 0.263 | 180 | 380 |
| core_attack_type | 1 | tfidf | Task Automation | 0.578 | 0.358 | 180 | 380 |
| obfuscation_technique | 1 | frozen | Base Encoding | 0.831 | 0.137 | 180 | 380 |
| obfuscation_technique | 1 | frozen | Emoji Substitution | 0.913 | 0.055 | 180 | 380 |
| obfuscation_technique | 1 | frozen | Reverse Text | 0.852 | 0.116 | 180 | 380 |
| obfuscation_technique | 1 | frozen | Substitution Ciphers | 0.908 | 0.060 | 180 | 380 |
| obfuscation_technique | 1 | lora | Base Encoding | 0.966 | 0.028 | 180 | 380 |
| obfuscation_technique | 1 | lora | Emoji Substitution | 0.986 | 0.008 | 180 | 380 |
| obfuscation_technique | 1 | lora | Reverse Text | 0.972 | 0.022 | 180 | 380 |
| obfuscation_technique | 1 | lora | Substitution Ciphers | 0.978 | 0.016 | 180 | 380 |
| obfuscation_technique | 1 | tfidf | Base Encoding | 0.755 | 0.197 | 180 | 380 |
| obfuscation_technique | 1 | tfidf | Emoji Substitution | 0.852 | 0.099 | 180 | 380 |
| obfuscation_technique | 1 | tfidf | Reverse Text | 0.780 | 0.171 | 180 | 380 |
| obfuscation_technique | 1 | tfidf | Substitution Ciphers | 0.814 | 0.138 | 180 | 380 |
| carrier_lodo_code | 2 | frozen | Alphanumeric Substitution | 0.664 | 0.319 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Anagramming | 0.708 | 0.274 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Base Encoding | 0.585 | 0.398 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Business Intelligence | 0.515 | 0.468 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Clickbait | 0.695 | 0.288 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Content Creation | 0.618 | 0.365 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Conversational Agent | 0.570 | 0.413 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Emoji Substitution | 0.718 | 0.265 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Entertainment | 0.680 | 0.302 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Homophonic Substitution | 0.710 | 0.273 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Information Dissemination | 0.676 | 0.306 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Information Retrieval | 0.557 | 0.425 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Instruction | 0.603 | 0.379 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Learning and Tutoring | 0.600 | 0.382 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Malware Distribution | 0.698 | 0.284 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Marketing & Advertising | 0.637 | 0.345 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Misinformation & Propaganda | 0.692 | 0.290 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Misspelling Intentionally | 0.663 | 0.319 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Persuasion | 0.665 | 0.317 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Programming Help | 0.686 | 0.297 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Research Assistance | 0.553 | 0.429 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Reverse Text | 0.617 | 0.365 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Scams & Fraud | 0.664 | 0.319 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Sentiment Analysis | 0.689 | 0.293 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Social Interaction | 0.647 | 0.336 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Space Removal & Grouping | 0.663 | 0.319 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Substitution Ciphers | 0.626 | 0.356 | 60 | 160 |
| carrier_lodo_code | 2 | frozen | Task Automation | 0.553 | 0.430 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Alphanumeric Substitution | 0.911 | 0.084 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Anagramming | 0.935 | 0.061 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Base Encoding | 0.999 | -0.004 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Business Intelligence | 0.999 | -0.004 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Clickbait | 0.914 | 0.081 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Content Creation | 0.921 | 0.075 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Conversational Agent | 1.000 | -0.004 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Emoji Substitution | 1.000 | -0.005 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Entertainment | 1.000 | -0.004 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Homophonic Substitution | 0.960 | 0.036 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Information Dissemination | 1.000 | -0.004 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Information Retrieval | 0.945 | 0.050 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Instruction | 0.937 | 0.058 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Learning and Tutoring | 0.939 | 0.056 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Malware Distribution | 0.938 | 0.057 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Marketing & Advertising | 1.000 | -0.004 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Misinformation & Propaganda | 0.999 | -0.004 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Misspelling Intentionally | 0.933 | 0.062 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Persuasion | 0.925 | 0.070 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Programming Help | 0.959 | 0.036 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Research Assistance | 0.999 | -0.004 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Reverse Text | 0.999 | -0.004 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Scams & Fraud | 0.996 | -0.001 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Sentiment Analysis | 0.993 | 0.002 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Social Interaction | 0.918 | 0.077 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Space Removal & Grouping | 0.944 | 0.052 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Substitution Ciphers | 1.000 | -0.005 | 60 | 160 |
| carrier_lodo_code | 2 | lora | Task Automation | 1.000 | -0.004 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Alphanumeric Substitution | 0.834 | 0.141 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Anagramming | 0.857 | 0.117 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Base Encoding | 0.763 | 0.211 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Business Intelligence | 0.741 | 0.233 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Clickbait | 0.844 | 0.131 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Content Creation | 0.722 | 0.252 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Conversational Agent | 0.713 | 0.262 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Emoji Substitution | 0.867 | 0.107 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Entertainment | 0.867 | 0.107 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Homophonic Substitution | 0.852 | 0.123 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Information Dissemination | 0.870 | 0.105 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Information Retrieval | 0.677 | 0.298 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Instruction | 0.812 | 0.163 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Learning and Tutoring | 0.734 | 0.241 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Malware Distribution | 0.830 | 0.145 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Marketing & Advertising | 0.919 | 0.056 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Misinformation & Propaganda | 0.846 | 0.128 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Misspelling Intentionally | 0.813 | 0.162 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Persuasion | 0.857 | 0.118 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Programming Help | 0.765 | 0.210 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Research Assistance | 0.720 | 0.255 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Reverse Text | 0.787 | 0.188 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Scams & Fraud | 0.832 | 0.142 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Sentiment Analysis | 0.800 | 0.175 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Social Interaction | 0.855 | 0.119 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Space Removal & Grouping | 0.841 | 0.134 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Substitution Ciphers | 0.829 | 0.146 | 60 | 160 |
| carrier_lodo_code | 2 | tfidf | Task Automation | 0.735 | 0.239 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Alphanumeric Substitution | 0.877 | 0.101 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Anagramming | 0.940 | 0.038 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Base Encoding | 0.867 | 0.111 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Business Intelligence | 0.748 | 0.230 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Clickbait | 0.930 | 0.048 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Content Creation | 0.859 | 0.119 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Conversational Agent | 0.710 | 0.268 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Emoji Substitution | 0.907 | 0.072 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Entertainment | 0.855 | 0.124 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Homophonic Substitution | 0.885 | 0.094 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Information Dissemination | 0.797 | 0.181 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Information Retrieval | 0.709 | 0.269 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Instruction | 0.885 | 0.093 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Learning and Tutoring | 0.830 | 0.149 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Malware Distribution | 0.935 | 0.043 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Marketing & Advertising | 0.771 | 0.207 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Misinformation & Propaganda | 0.838 | 0.140 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Misspelling Intentionally | 0.864 | 0.114 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Persuasion | 0.852 | 0.126 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Programming Help | 0.881 | 0.097 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Research Assistance | 0.732 | 0.246 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Reverse Text | 0.786 | 0.192 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Scams & Fraud | 0.854 | 0.124 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Sentiment Analysis | 0.722 | 0.256 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Social Interaction | 0.881 | 0.097 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Space Removal & Grouping | 0.894 | 0.084 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Substitution Ciphers | 0.903 | 0.075 | 60 | 160 |
| carrier_lodo_email | 2 | frozen | Task Automation | 0.852 | 0.126 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Alphanumeric Substitution | 0.949 | 0.045 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Anagramming | 0.976 | 0.018 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Base Encoding | 0.951 | 0.044 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Business Intelligence | 0.977 | 0.018 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Clickbait | 0.970 | 0.025 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Content Creation | 0.971 | 0.023 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Conversational Agent | 0.977 | 0.017 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Emoji Substitution | 0.975 | 0.020 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Entertainment | 0.987 | 0.008 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Homophonic Substitution | 0.962 | 0.033 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Information Dissemination | 0.988 | 0.006 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Information Retrieval | 0.950 | 0.045 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Instruction | 0.981 | 0.013 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Learning and Tutoring | 0.962 | 0.033 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Malware Distribution | 0.891 | 0.104 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Marketing & Advertising | 0.968 | 0.026 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Misinformation & Propaganda | 0.986 | 0.008 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Misspelling Intentionally | 0.966 | 0.028 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Persuasion | 0.961 | 0.033 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Programming Help | 0.947 | 0.047 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Research Assistance | 0.960 | 0.034 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Reverse Text | 0.977 | 0.017 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Scams & Fraud | 0.957 | 0.037 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Sentiment Analysis | 0.784 | 0.210 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Social Interaction | 0.950 | 0.045 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Space Removal & Grouping | 0.977 | 0.018 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Substitution Ciphers | 0.983 | 0.011 | 60 | 160 |
| carrier_lodo_email | 2 | lora | Task Automation | 0.961 | 0.033 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Alphanumeric Substitution | 0.952 | 0.005 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Anagramming | 0.974 | -0.017 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Base Encoding | 0.945 | 0.013 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Business Intelligence | 0.936 | 0.021 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Clickbait | 0.973 | -0.016 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Content Creation | 0.862 | 0.095 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Conversational Agent | 0.885 | 0.072 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Emoji Substitution | 0.985 | -0.028 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Entertainment | 0.988 | -0.031 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Homophonic Substitution | 0.929 | 0.028 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Information Dissemination | 0.990 | -0.033 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Information Retrieval | 0.874 | 0.083 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Instruction | 0.976 | -0.019 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Learning and Tutoring | 0.872 | 0.085 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Malware Distribution | 0.981 | -0.023 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Marketing & Advertising | 0.989 | -0.032 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Misinformation & Propaganda | 0.976 | -0.019 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Misspelling Intentionally | 0.967 | -0.010 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Persuasion | 0.986 | -0.029 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Programming Help | 0.908 | 0.049 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Research Assistance | 0.953 | 0.004 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Reverse Text | 0.950 | 0.008 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Scams & Fraud | 0.981 | -0.024 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Sentiment Analysis | 0.980 | -0.023 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Social Interaction | 0.964 | -0.007 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Space Removal & Grouping | 0.972 | -0.015 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Substitution Ciphers | 0.974 | -0.017 | 60 | 160 |
| carrier_lodo_email | 2 | tfidf | Task Automation | 0.941 | 0.016 | 60 | 160 |
| carrier_lodo_table | 2 | frozen | Alphanumeric Substitution | 0.246 | 0.746 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Anagramming | 0.329 | 0.663 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Base Encoding | 0.232 | 0.760 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Business Intelligence | 0.290 | 0.702 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Clickbait | 0.326 | 0.666 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Content Creation | 0.270 | 0.722 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Conversational Agent | 0.283 | 0.710 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Emoji Substitution | 0.281 | 0.711 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Entertainment | 0.295 | 0.698 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Homophonic Substitution | 0.328 | 0.664 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Information Dissemination | 0.283 | 0.709 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Information Retrieval | 0.255 | 0.737 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Instruction | 0.285 | 0.708 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Learning and Tutoring | 0.249 | 0.743 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Malware Distribution | 0.364 | 0.628 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Marketing & Advertising | 0.244 | 0.748 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Misinformation & Propaganda | 0.333 | 0.660 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Misspelling Intentionally | 0.283 | 0.710 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Persuasion | 0.322 | 0.670 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Programming Help | 0.239 | 0.753 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Research Assistance | 0.250 | 0.742 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Reverse Text | 0.248 | 0.744 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Scams & Fraud | 0.304 | 0.688 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Sentiment Analysis | 0.263 | 0.729 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Social Interaction | 0.271 | 0.721 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Space Removal & Grouping | 0.241 | 0.751 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Substitution Ciphers | 0.262 | 0.730 | 60 | 328 |
| carrier_lodo_table | 2 | frozen | Task Automation | 0.265 | 0.727 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Alphanumeric Substitution | 0.576 | 0.424 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Anagramming | 0.780 | 0.220 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Base Encoding | 0.773 | 0.227 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Business Intelligence | 0.657 | 0.343 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Clickbait | 0.635 | 0.365 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Content Creation | 0.601 | 0.399 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Conversational Agent | 0.756 | 0.244 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Emoji Substitution | 0.735 | 0.265 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Entertainment | 0.790 | 0.210 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Homophonic Substitution | 0.686 | 0.314 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Information Dissemination | 0.821 | 0.179 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Information Retrieval | 0.660 | 0.340 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Instruction | 0.765 | 0.235 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Learning and Tutoring | 0.681 | 0.319 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Malware Distribution | 0.794 | 0.206 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Marketing & Advertising | 0.743 | 0.257 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Misinformation & Propaganda | 0.761 | 0.239 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Misspelling Intentionally | 0.735 | 0.265 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Persuasion | 0.735 | 0.265 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Programming Help | 0.711 | 0.289 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Research Assistance | 0.674 | 0.326 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Reverse Text | 0.729 | 0.271 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Scams & Fraud | 0.665 | 0.335 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Sentiment Analysis | 0.529 | 0.471 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Social Interaction | 0.767 | 0.233 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Space Removal & Grouping | 0.814 | 0.186 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Substitution Ciphers | 0.664 | 0.336 | 60 | 328 |
| carrier_lodo_table | 2 | lora | Task Automation | 0.716 | 0.284 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Alphanumeric Substitution | 0.698 | 0.275 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Anagramming | 0.695 | 0.278 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Base Encoding | 0.600 | 0.374 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Business Intelligence | 0.630 | 0.343 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Clickbait | 0.671 | 0.302 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Content Creation | 0.596 | 0.377 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Conversational Agent | 0.637 | 0.336 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Emoji Substitution | 0.706 | 0.267 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Entertainment | 0.691 | 0.282 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Homophonic Substitution | 0.709 | 0.264 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Information Dissemination | 0.721 | 0.252 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Information Retrieval | 0.586 | 0.387 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Instruction | 0.705 | 0.268 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Learning and Tutoring | 0.604 | 0.369 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Malware Distribution | 0.711 | 0.262 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Marketing & Advertising | 0.709 | 0.264 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Misinformation & Propaganda | 0.693 | 0.280 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Misspelling Intentionally | 0.656 | 0.317 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Persuasion | 0.679 | 0.294 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Programming Help | 0.557 | 0.416 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Research Assistance | 0.583 | 0.390 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Reverse Text | 0.600 | 0.373 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Scams & Fraud | 0.765 | 0.208 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Sentiment Analysis | 0.655 | 0.318 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Social Interaction | 0.730 | 0.244 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Space Removal & Grouping | 0.672 | 0.301 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Substitution Ciphers | 0.691 | 0.282 | 60 | 328 |
| carrier_lodo_table | 2 | tfidf | Task Automation | 0.620 | 0.354 | 60 | 328 |
| carrier_plus_attack_external | 2 | frozen | Base Encoding | 0.928 | 0.034 | 60 | 110 |
| carrier_plus_attack_external | 2 | frozen | Business Intelligence | 0.840 | 0.122 | 60 | 110 |
| carrier_plus_attack_external | 2 | frozen | Conversational Agent | 0.838 | 0.124 | 60 | 110 |
| carrier_plus_attack_external | 2 | frozen | Emoji Substitution | 0.955 | 0.007 | 60 | 110 |
| carrier_plus_attack_external | 2 | frozen | Entertainment | 0.912 | 0.050 | 60 | 110 |
| carrier_plus_attack_external | 2 | frozen | Information Dissemination | 0.897 | 0.066 | 60 | 110 |
| carrier_plus_attack_external | 2 | frozen | Marketing & Advertising | 0.898 | 0.065 | 60 | 110 |
| carrier_plus_attack_external | 2 | frozen | Misinformation & Propaganda | 0.916 | 0.046 | 60 | 110 |
| carrier_plus_attack_external | 2 | frozen | Research Assistance | 0.866 | 0.096 | 60 | 110 |
| carrier_plus_attack_external | 2 | frozen | Reverse Text | 0.914 | 0.048 | 60 | 110 |
| carrier_plus_attack_external | 2 | frozen | Scams & Fraud | 0.931 | 0.031 | 60 | 110 |
| carrier_plus_attack_external | 2 | frozen | Sentiment Analysis | 0.819 | 0.143 | 60 | 110 |
| carrier_plus_attack_external | 2 | frozen | Substitution Ciphers | 0.942 | 0.021 | 60 | 110 |
| carrier_plus_attack_external | 2 | frozen | Task Automation | 0.903 | 0.060 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Base Encoding | 0.995 | -0.005 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Business Intelligence | 0.999 | -0.009 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Conversational Agent | 0.998 | -0.008 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Emoji Substitution | 0.998 | -0.007 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Entertainment | 0.999 | -0.009 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Information Dissemination | 0.999 | -0.008 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Marketing & Advertising | 0.999 | -0.008 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Misinformation & Propaganda | 0.997 | -0.007 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Research Assistance | 0.993 | -0.002 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Reverse Text | 0.997 | -0.006 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Scams & Fraud | 0.987 | 0.003 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Sentiment Analysis | 0.846 | 0.145 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Substitution Ciphers | 1.000 | -0.009 | 60 | 110 |
| carrier_plus_attack_external | 2 | lora | Task Automation | 0.992 | -0.001 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Base Encoding | 0.743 | 0.179 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Business Intelligence | 0.680 | 0.242 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Conversational Agent | 0.592 | 0.330 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Emoji Substitution | 0.829 | 0.092 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Entertainment | 0.794 | 0.128 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Information Dissemination | 0.828 | 0.094 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Marketing & Advertising | 0.788 | 0.134 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Misinformation & Propaganda | 0.786 | 0.136 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Research Assistance | 0.730 | 0.192 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Reverse Text | 0.719 | 0.203 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Scams & Fraud | 0.822 | 0.100 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Sentiment Analysis | 0.718 | 0.204 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Substitution Ciphers | 0.763 | 0.158 | 60 | 110 |
| carrier_plus_attack_external | 2 | tfidf | Task Automation | 0.681 | 0.240 | 60 | 110 |
| core_attack_type | 2 | frozen | Base Encoding | 0.845 | 0.137 | 180 | 380 |
| core_attack_type | 2 | frozen | Business Intelligence | 0.777 | 0.206 | 180 | 380 |
| core_attack_type | 2 | frozen | Conversational Agent | 0.774 | 0.209 | 180 | 380 |
| core_attack_type | 2 | frozen | Emoji Substitution | 0.892 | 0.091 | 180 | 380 |
| core_attack_type | 2 | frozen | Entertainment | 0.863 | 0.120 | 180 | 380 |
| core_attack_type | 2 | frozen | Information Dissemination | 0.848 | 0.135 | 180 | 380 |
| core_attack_type | 2 | frozen | Marketing & Advertising | 0.825 | 0.158 | 180 | 380 |
| core_attack_type | 2 | frozen | Misinformation & Propaganda | 0.878 | 0.105 | 180 | 380 |
| core_attack_type | 2 | frozen | Research Assistance | 0.788 | 0.195 | 180 | 380 |
| core_attack_type | 2 | frozen | Reverse Text | 0.824 | 0.159 | 180 | 380 |
| core_attack_type | 2 | frozen | Scams & Fraud | 0.869 | 0.114 | 180 | 380 |
| core_attack_type | 2 | frozen | Sentiment Analysis | 0.824 | 0.158 | 180 | 380 |
| core_attack_type | 2 | frozen | Substitution Ciphers | 0.864 | 0.119 | 180 | 380 |
| core_attack_type | 2 | frozen | Task Automation | 0.816 | 0.167 | 180 | 380 |
| core_attack_type | 2 | lora | Base Encoding | 0.980 | 0.015 | 180 | 380 |
| core_attack_type | 2 | lora | Business Intelligence | 0.974 | 0.021 | 180 | 380 |
| core_attack_type | 2 | lora | Conversational Agent | 0.984 | 0.011 | 180 | 380 |
| core_attack_type | 2 | lora | Emoji Substitution | 0.978 | 0.017 | 180 | 380 |
| core_attack_type | 2 | lora | Entertainment | 0.985 | 0.010 | 180 | 380 |
| core_attack_type | 2 | lora | Information Dissemination | 0.985 | 0.011 | 180 | 380 |
| core_attack_type | 2 | lora | Marketing & Advertising | 0.981 | 0.014 | 180 | 380 |
| core_attack_type | 2 | lora | Misinformation & Propaganda | 0.979 | 0.016 | 180 | 380 |
| core_attack_type | 2 | lora | Research Assistance | 0.973 | 0.022 | 180 | 380 |
| core_attack_type | 2 | lora | Reverse Text | 0.975 | 0.020 | 180 | 380 |
| core_attack_type | 2 | lora | Scams & Fraud | 0.980 | 0.015 | 180 | 380 |
| core_attack_type | 2 | lora | Sentiment Analysis | 0.974 | 0.022 | 180 | 380 |
| core_attack_type | 2 | lora | Substitution Ciphers | 0.972 | 0.024 | 180 | 380 |
| core_attack_type | 2 | lora | Task Automation | 0.976 | 0.020 | 180 | 380 |
| core_attack_type | 2 | tfidf | Base Encoding | 0.624 | 0.313 | 180 | 380 |
| core_attack_type | 2 | tfidf | Business Intelligence | 0.600 | 0.336 | 180 | 380 |
| core_attack_type | 2 | tfidf | Conversational Agent | 0.550 | 0.386 | 180 | 380 |
| core_attack_type | 2 | tfidf | Emoji Substitution | 0.676 | 0.260 | 180 | 380 |
| core_attack_type | 2 | tfidf | Entertainment | 0.723 | 0.214 | 180 | 380 |
| core_attack_type | 2 | tfidf | Information Dissemination | 0.705 | 0.231 | 180 | 380 |
| core_attack_type | 2 | tfidf | Marketing & Advertising | 0.711 | 0.226 | 180 | 380 |
| core_attack_type | 2 | tfidf | Misinformation & Propaganda | 0.703 | 0.234 | 180 | 380 |
| core_attack_type | 2 | tfidf | Research Assistance | 0.593 | 0.344 | 180 | 380 |
| core_attack_type | 2 | tfidf | Reverse Text | 0.646 | 0.291 | 180 | 380 |
| core_attack_type | 2 | tfidf | Scams & Fraud | 0.731 | 0.206 | 180 | 380 |
| core_attack_type | 2 | tfidf | Sentiment Analysis | 0.602 | 0.335 | 180 | 380 |
| core_attack_type | 2 | tfidf | Substitution Ciphers | 0.658 | 0.278 | 180 | 380 |
| core_attack_type | 2 | tfidf | Task Automation | 0.575 | 0.362 | 180 | 380 |
| obfuscation_technique | 2 | frozen | Base Encoding | 0.863 | 0.089 | 180 | 380 |
| obfuscation_technique | 2 | frozen | Emoji Substitution | 0.924 | 0.028 | 180 | 380 |
| obfuscation_technique | 2 | frozen | Reverse Text | 0.859 | 0.093 | 180 | 380 |
| obfuscation_technique | 2 | frozen | Substitution Ciphers | 0.900 | 0.052 | 180 | 380 |
| obfuscation_technique | 2 | lora | Base Encoding | 0.968 | 0.017 | 180 | 380 |
| obfuscation_technique | 2 | lora | Emoji Substitution | 0.967 | 0.018 | 180 | 380 |
| obfuscation_technique | 2 | lora | Reverse Text | 0.963 | 0.022 | 180 | 380 |
| obfuscation_technique | 2 | lora | Substitution Ciphers | 0.956 | 0.029 | 180 | 380 |
| obfuscation_technique | 2 | tfidf | Base Encoding | 0.809 | 0.115 | 180 | 380 |
| obfuscation_technique | 2 | tfidf | Emoji Substitution | 0.898 | 0.026 | 180 | 380 |
| obfuscation_technique | 2 | tfidf | Reverse Text | 0.812 | 0.112 | 180 | 380 |
| obfuscation_technique | 2 | tfidf | Substitution Ciphers | 0.851 | 0.073 | 180 | 380 |

## Raw table 4 -- Cross-family Arm A direct-to-indirect runs

| Pool | Seed | Model | Val ROC-AUC | Test ROC-AUC | Gap | n_train | n_val | n_test | Over-defense FPR | Threshold | Recipe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| capped | 0 | frozen | 0.998 | 0.689 | 0.309 | 23239 | 5809 | 8283 |  |  | C=0.1 |
| capped | 0 | lora | 0.999 | 0.615 | 0.384 | 23239 | 5809 | 8283 | 0.339 | 0.264 | r=16, lr=0.0001, epochs=3 |
| capped | 0 | tfidf | 0.997 | 0.527 | 0.471 | 23239 | 5809 | 8283 |  |  | C=10.0 |
| capped | 1 | frozen | 0.998 | 0.685 | 0.312 | 23239 | 5809 | 8283 |  |  | C=0.1 |
| capped | 1 | lora | 0.999 | 0.627 | 0.373 | 23239 | 5809 | 8283 | 0.425 | 0.160 | r=16, lr=0.0001, epochs=3 |
| capped | 1 | tfidf | 0.997 | 0.540 | 0.457 | 23239 | 5809 | 8283 |  |  | C=10.0 |
| capped | 2 | frozen | 0.998 | 0.681 | 0.317 | 23239 | 5809 | 8283 |  |  | C=0.1 |
| capped | 2 | lora | 0.999 | 0.663 | 0.337 | 23239 | 5809 | 8283 | 0.392 | 0.186 | r=16, lr=0.0001, epochs=3 |
| capped | 2 | tfidf | 0.997 | 0.508 | 0.490 | 23239 | 5809 | 8283 |  |  | C=10.0 |
| uncapped | 0 | tfidf | 0.999 | 0.501 | 0.499 | 633529 | 158382 | 8283 |  |  | C=10.0 |
| uncapped | 1 | tfidf | 0.999 | 0.509 | 0.490 | 633529 | 158382 | 8283 |  |  | C=1.0 |
| uncapped | 2 | tfidf | 0.999 | 0.527 | 0.472 | 633529 | 158382 | 8283 |  |  | C=1.0 |

## Raw table 5 -- Cross-family Arm B dialect-transfer runs

| Condition | Variant | Held-out dialect | Seed | Model | Val ROC-AUC | Test ROC-AUC | Gap | Test AUPRC | Brier | ECE | TPR@1% | TPR@0.5% | TPR@0.1% | n_train | n_val | n_test | Recipe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dialect_balanced | B- | dialect_lodo_bipia | 0 | frozen | 0.963 | 0.639 | 0.324 | 0.944 | 0.167 | 0.177 | 0.018 | 0.014 | 0.001 | 5100 | 1275 | 5508 | C=1.0 |
| dialect_balanced | B- | dialect_lodo_bipia | 0 | tfidf | 0.935 | 0.583 | 0.353 | 0.934 | 0.177 | 0.283 | 0.017 | 0.009 | 0.002 | 5100 | 1275 | 5508 | C=10.0 |
| dialect_balanced | B- | dialect_lodo_browsesafe | 0 | frozen | 0.981 | 0.534 | 0.448 | 0.532 | 0.376 | 0.341 | 0.019 | 0.010 | 0.002 | 5100 | 1275 | 14719 | C=0.1 |
| dialect_balanced | B- | dialect_lodo_browsesafe | 0 | tfidf | 0.974 | 0.534 | 0.441 | 0.530 | 0.274 | 0.144 | 0.018 | 0.008 | 0.002 | 5100 | 1275 | 14719 | C=10.0 |
| dialect_balanced | B- | dialect_lodo_fujitsu | 0 | frozen | 0.906 | 0.311 | 0.595 | 0.385 | 0.503 | 0.499 | 0.003 | 0.002 | 0.001 | 5100 | 1275 | 21886 | C=1.0 |
| dialect_balanced | B- | dialect_lodo_fujitsu | 0 | tfidf | 0.865 | 0.707 | 0.158 | 0.747 | 0.349 | 0.345 | 0.151 | 0.111 | 0.049 | 5100 | 1275 | 21886 | C=10.0 |
| dialect_balanced | B- | dialect_lodo_injecagent | 0 | frozen | 0.942 | 0.973 | -0.030 | 1.000 | 0.245 | 0.376 | 0.728 | 0.728 | 0.728 | 13219 | 3305 | 2125 | C=1.0 |
| dialect_balanced | B- | dialect_lodo_injecagent | 0 | tfidf | 0.929 | 0.967 | -0.038 | 1.000 | 0.010 | 0.060 | 0.625 | 0.625 | 0.625 | 13219 | 3305 | 2125 | C=10.0 |
| dialect_balanced | B- | dialect_lodo_bipia | 1 | frozen | 0.966 | 0.576 | 0.390 | 0.928 | 0.086 | 0.076 | 0.011 | 0.001 | 0.000 | 5100 | 1275 | 5508 | C=1.0 |
| dialect_balanced | B- | dialect_lodo_bipia | 1 | tfidf | 0.936 | 0.627 | 0.309 | 0.943 | 0.171 | 0.268 | 0.038 | 0.032 | 0.005 | 5100 | 1275 | 5508 | C=10.0 |
| dialect_balanced | B- | dialect_lodo_browsesafe | 1 | frozen | 0.983 | 0.535 | 0.449 | 0.529 | 0.362 | 0.309 | 0.019 | 0.011 | 0.002 | 5100 | 1275 | 14719 | C=1.0 |
| dialect_balanced | B- | dialect_lodo_browsesafe | 1 | tfidf | 0.970 | 0.528 | 0.441 | 0.524 | 0.265 | 0.098 | 0.014 | 0.005 | 0.002 | 5100 | 1275 | 14719 | C=10.0 |
| dialect_balanced | B- | dialect_lodo_fujitsu | 1 | frozen | 0.910 | 0.303 | 0.607 | 0.385 | 0.512 | 0.512 | 0.001 | 0.001 | 0.000 | 5100 | 1275 | 21886 | C=1.0 |
| dialect_balanced | B- | dialect_lodo_fujitsu | 1 | tfidf | 0.874 | 0.695 | 0.180 | 0.729 | 0.386 | 0.390 | 0.138 | 0.102 | 0.033 | 5100 | 1275 | 21886 | C=10.0 |
| dialect_balanced | B- | dialect_lodo_injecagent | 1 | frozen | 0.940 | 0.994 | -0.053 | 1.000 | 0.381 | 0.519 | 0.934 | 0.934 | 0.934 | 13219 | 3305 | 2125 | C=1.0 |
| dialect_balanced | B- | dialect_lodo_injecagent | 1 | tfidf | 0.927 | 0.969 | -0.042 | 1.000 | 0.013 | 0.065 | 0.865 | 0.865 | 0.865 | 13219 | 3305 | 2125 | C=10.0 |
| dialect_balanced | B- | dialect_lodo_bipia | 2 | frozen | 0.961 | 0.633 | 0.328 | 0.942 | 0.198 | 0.207 | 0.016 | 0.006 | 0.000 | 5100 | 1275 | 5508 | C=1.0 |
| dialect_balanced | B- | dialect_lodo_bipia | 2 | tfidf | 0.925 | 0.584 | 0.342 | 0.935 | 0.186 | 0.297 | 0.021 | 0.013 | 0.005 | 5100 | 1275 | 5508 | C=10.0 |
| dialect_balanced | B- | dialect_lodo_browsesafe | 2 | frozen | 0.983 | 0.549 | 0.433 | 0.540 | 0.359 | 0.306 | 0.017 | 0.011 | 0.004 | 5100 | 1275 | 14719 | C=1.0 |
| dialect_balanced | B- | dialect_lodo_browsesafe | 2 | tfidf | 0.973 | 0.538 | 0.435 | 0.532 | 0.257 | 0.065 | 0.020 | 0.008 | 0.002 | 5100 | 1275 | 14719 | C=10.0 |
| dialect_balanced | B- | dialect_lodo_fujitsu | 2 | frozen | 0.923 | 0.460 | 0.463 | 0.474 | 0.477 | 0.463 | 0.007 | 0.004 | 0.001 | 5100 | 1275 | 21886 | C=1.0 |
| dialect_balanced | B- | dialect_lodo_fujitsu | 2 | tfidf | 0.892 | 0.689 | 0.203 | 0.729 | 0.358 | 0.353 | 0.138 | 0.110 | 0.047 | 5100 | 1275 | 21886 | C=10.0 |
| dialect_balanced | B- | dialect_lodo_injecagent | 2 | frozen | 0.943 | 0.997 | -0.054 | 1.000 | 0.452 | 0.576 | 0.982 | 0.982 | 0.982 | 13219 | 3305 | 2125 | C=1.0 |
| dialect_balanced | B- | dialect_lodo_injecagent | 2 | tfidf | 0.926 | 0.984 | -0.058 | 1.000 | 0.011 | 0.062 | 0.917 | 0.917 | 0.917 | 13219 | 3305 | 2125 | C=10.0 |
| natural | B- | dialect_lodo_bipia | 0 | frozen | 0.963 | 0.612 | 0.351 | 0.935 | 0.182 | 0.193 | 0.015 | 0.005 | 0.000 | 30984 | 7746 | 5508 | C=1.0 |
| natural | B- | dialect_lodo_bipia | 0 | lora | 0.984 | 0.684 | 0.300 | 0.954 | 0.204 | 0.240 | 0.032 | 0.024 | 0.012 | 30984 | 7746 | 5508 | r=16, lr=0.0001, epochs=3 |
| natural | B- | dialect_lodo_bipia | 0 | tfidf | 0.952 | 0.603 | 0.349 | 0.938 | 0.228 | 0.327 | 0.023 | 0.011 | 0.002 | 30984 | 7746 | 5508 | C=10.0 |
| natural | B- | dialect_lodo_browsesafe | 0 | frozen | 0.997 | 0.541 | 0.456 | 0.531 | 0.466 | 0.460 | 0.016 | 0.009 | 0.002 | 23615 | 5904 | 14719 | C=1.0 |
| natural | B- | dialect_lodo_browsesafe | 0 | lora | 1.000 | 0.539 | 0.461 | 0.541 | 0.476 | 0.473 | 0.020 | 0.009 | 0.002 | 23615 | 5904 | 14719 | r=16, lr=0.0001, epochs=3 |
| natural | B- | dialect_lodo_browsesafe | 0 | tfidf | 0.995 | 0.533 | 0.462 | 0.530 | 0.270 | 0.111 | 0.018 | 0.007 | 0.002 | 23615 | 5904 | 14719 | C=10.0 |
| natural | B- | dialect_lodo_fujitsu | 0 | frozen | 0.890 | 0.546 | 0.344 | 0.538 | 0.404 | 0.376 | 0.016 | 0.007 | 0.001 | 17882 | 4470 | 21886 | C=1.0 |
| natural | B- | dialect_lodo_fujitsu | 0 | lora | 0.949 | 0.755 | 0.193 | 0.780 | 0.229 | 0.156 | 0.198 | 0.159 | 0.087 | 17882 | 4470 | 21886 | r=16, lr=0.0001, epochs=3 |
| natural | B- | dialect_lodo_fujitsu | 0 | tfidf | 0.837 | 0.696 | 0.141 | 0.737 | 0.312 | 0.284 | 0.171 | 0.141 | 0.080 | 17882 | 4470 | 21886 | C=10.0 |
| natural | B- | dialect_lodo_injecagent | 0 | frozen | 0.958 | 0.991 | -0.033 | 1.000 | 0.217 | 0.349 | 0.957 | 0.957 | 0.957 | 33690 | 8423 | 2125 | C=1.0 |
| natural | B- | dialect_lodo_injecagent | 0 | lora | 0.986 | 1.000 | -0.014 | 1.000 | 0.000 | 0.001 | 1.000 | 1.000 | 1.000 | 33690 | 8423 | 2125 | r=16, lr=0.0001, epochs=3 |
| natural | B- | dialect_lodo_injecagent | 0 | tfidf | 0.952 | 0.983 | -0.031 | 1.000 | 0.004 | 0.012 | 0.829 | 0.829 | 0.829 | 33690 | 8423 | 2125 | C=10.0 |
| natural | B- | dialect_lodo_bipia | 1 | frozen | 0.965 | 0.610 | 0.355 | 0.936 | 0.161 | 0.172 | 0.017 | 0.005 | 0.000 | 30984 | 7746 | 5508 | C=1.0 |
| natural | B- | dialect_lodo_bipia | 1 | lora | 0.985 | 0.702 | 0.283 | 0.955 | 0.193 | 0.228 | 0.021 | 0.008 | 0.003 | 30984 | 7746 | 5508 | r=16, lr=0.0001, epochs=3 |
| natural | B- | dialect_lodo_bipia | 1 | tfidf | 0.955 | 0.607 | 0.347 | 0.940 | 0.217 | 0.300 | 0.029 | 0.013 | 0.002 | 30984 | 7746 | 5508 | C=10.0 |
| natural | B- | dialect_lodo_browsesafe | 1 | frozen | 0.997 | 0.536 | 0.461 | 0.525 | 0.404 | 0.372 | 0.015 | 0.008 | 0.002 | 23615 | 5904 | 14719 | C=1.0 |
| natural | B- | dialect_lodo_browsesafe | 1 | lora | 1.000 | 0.576 | 0.424 | 0.599 | 0.483 | 0.483 | 0.029 | 0.008 | 0.003 | 23615 | 5904 | 14719 | r=16, lr=0.0001, epochs=3 |
| natural | B- | dialect_lodo_browsesafe | 1 | tfidf | 0.995 | 0.533 | 0.462 | 0.532 | 0.268 | 0.108 | 0.021 | 0.010 | 0.002 | 23615 | 5904 | 14719 | C=10.0 |
| natural | B- | dialect_lodo_fujitsu | 1 | frozen | 0.884 | 0.543 | 0.341 | 0.537 | 0.414 | 0.388 | 0.016 | 0.007 | 0.002 | 17882 | 4470 | 21886 | C=1.0 |
| natural | B- | dialect_lodo_fujitsu | 1 | lora | 0.945 | 0.730 | 0.216 | 0.764 | 0.261 | 0.220 | 0.170 | 0.120 | 0.069 | 17882 | 4470 | 21886 | r=16, lr=0.0001, epochs=3 |
| natural | B- | dialect_lodo_fujitsu | 1 | tfidf | 0.831 | 0.677 | 0.154 | 0.724 | 0.317 | 0.285 | 0.167 | 0.136 | 0.076 | 17882 | 4470 | 21886 | C=10.0 |
| natural | B- | dialect_lodo_injecagent | 1 | frozen | 0.961 | 0.997 | -0.036 | 1.000 | 0.211 | 0.335 | 0.970 | 0.970 | 0.970 | 33690 | 8423 | 2125 | C=10.0 |
| natural | B- | dialect_lodo_injecagent | 1 | lora | 0.987 | 1.000 | -0.013 | 1.000 | 0.001 | 0.007 | 1.000 | 1.000 | 1.000 | 33690 | 8423 | 2125 | r=16, lr=0.0001, epochs=3 |
| natural | B- | dialect_lodo_injecagent | 1 | tfidf | 0.953 | 0.988 | -0.035 | 1.000 | 0.004 | 0.014 | 0.862 | 0.862 | 0.862 | 33690 | 8423 | 2125 | C=10.0 |
| natural | B- | dialect_lodo_bipia | 2 | frozen | 0.965 | 0.605 | 0.361 | 0.935 | 0.170 | 0.180 | 0.019 | 0.010 | 0.000 | 30984 | 7746 | 5508 | C=1.0 |
| natural | B- | dialect_lodo_bipia | 2 | lora | 0.985 | 0.695 | 0.290 | 0.953 | 0.279 | 0.292 | 0.024 | 0.022 | 0.007 | 30984 | 7746 | 5508 | r=16, lr=0.0001, epochs=3 |
| natural | B- | dialect_lodo_bipia | 2 | tfidf | 0.955 | 0.591 | 0.364 | 0.936 | 0.236 | 0.330 | 0.027 | 0.013 | 0.002 | 30984 | 7746 | 5508 | C=10.0 |
| natural | B- | dialect_lodo_browsesafe | 2 | frozen | 0.998 | 0.538 | 0.460 | 0.530 | 0.473 | 0.469 | 0.018 | 0.011 | 0.001 | 23615 | 5904 | 14719 | C=1.0 |
| natural | B- | dialect_lodo_browsesafe | 2 | lora | 1.000 | 0.549 | 0.451 | 0.557 | 0.286 | 0.190 | 0.017 | 0.003 | 0.001 | 23615 | 5904 | 14719 | r=8, lr=0.0001, epochs=3 |
| natural | B- | dialect_lodo_browsesafe | 2 | tfidf | 0.996 | 0.538 | 0.458 | 0.535 | 0.269 | 0.111 | 0.021 | 0.010 | 0.002 | 23615 | 5904 | 14719 | C=10.0 |
| natural | B- | dialect_lodo_fujitsu | 2 | frozen | 0.877 | 0.499 | 0.378 | 0.504 | 0.439 | 0.413 | 0.010 | 0.005 | 0.001 | 17882 | 4470 | 21886 | C=1.0 |
| natural | B- | dialect_lodo_fujitsu | 2 | lora | 0.942 | 0.669 | 0.274 | 0.736 | 0.302 | 0.254 | 0.257 | 0.231 | 0.135 | 17882 | 4470 | 21886 | r=16, lr=0.0001, epochs=3 |
| natural | B- | dialect_lodo_fujitsu | 2 | tfidf | 0.834 | 0.674 | 0.160 | 0.722 | 0.315 | 0.281 | 0.163 | 0.134 | 0.082 | 17882 | 4470 | 21886 | C=10.0 |
| natural | B- | dialect_lodo_injecagent | 2 | frozen | 0.960 | 0.994 | -0.034 | 1.000 | 0.128 | 0.230 | 0.943 | 0.943 | 0.943 | 33690 | 8423 | 2125 | C=10.0 |
| natural | B- | dialect_lodo_injecagent | 2 | lora | 0.986 | 1.000 | -0.014 | 1.000 | 0.001 | 0.004 | 1.000 | 1.000 | 1.000 | 33690 | 8423 | 2125 | r=8, lr=0.0001, epochs=3 |
| natural | B- | dialect_lodo_injecagent | 2 | tfidf | 0.952 | 0.993 | -0.041 | 1.000 | 0.004 | 0.015 | 0.941 | 0.941 | 0.941 | 33690 | 8423 | 2125 | C=10.0 |
| natural | B+ | dialect_lodo_bipia | 0 | frozen | 0.971 | 0.626 | 0.345 | 0.941 | 0.119 | 0.120 | 0.009 | 0.005 | 0.000 | 36794 | 9198 | 5508 | C=1.0 |
| natural | B+ | dialect_lodo_bipia | 0 | lora | 0.989 | 0.711 | 0.278 | 0.960 | 0.172 | 0.188 | 0.058 | 0.058 | 0.003 | 36794 | 9198 | 5508 | r=8, lr=0.0001, epochs=3 |
| natural | B+ | dialect_lodo_bipia | 0 | tfidf | 0.961 | 0.598 | 0.362 | 0.938 | 0.089 | 0.059 | 0.025 | 0.013 | 0.003 | 36794 | 9198 | 5508 | C=10.0 |
| natural | B+ | dialect_lodo_browsesafe | 0 | frozen | 0.998 | 0.543 | 0.454 | 0.531 | 0.491 | 0.491 | 0.016 | 0.008 | 0.001 | 29424 | 7357 | 14719 | C=1.0 |
| natural | B+ | dialect_lodo_browsesafe | 0 | lora | 1.000 | 0.600 | 0.400 | 0.590 | 0.480 | 0.481 | 0.023 | 0.003 | 0.000 | 29424 | 7357 | 14719 | r=8, lr=0.0001, epochs=3 |
| natural | B+ | dialect_lodo_browsesafe | 0 | tfidf | 0.994 | 0.536 | 0.458 | 0.532 | 0.311 | 0.238 | 0.016 | 0.011 | 0.003 | 29424 | 7357 | 14719 | C=10.0 |
| natural | B+ | dialect_lodo_fujitsu | 0 | frozen | 0.919 | 0.442 | 0.478 | 0.461 | 0.478 | 0.464 | 0.009 | 0.004 | 0.002 | 23692 | 5922 | 21886 | C=1.0 |
| natural | B+ | dialect_lodo_fujitsu | 0 | lora | 0.964 | 0.424 | 0.540 | 0.486 | 0.505 | 0.504 | 0.000 | 0.000 | 0.000 | 23692 | 5922 | 21886 | r=16, lr=0.0001, epochs=3 |
| natural | B+ | dialect_lodo_fujitsu | 0 | tfidf | 0.881 | 0.671 | 0.210 | 0.714 | 0.426 | 0.428 | 0.153 | 0.127 | 0.081 | 23692 | 5922 | 21886 | C=10.0 |
| natural | B+ | dialect_lodo_injecagent | 0 | frozen | 0.966 | 0.879 | 0.088 | 0.998 | 0.409 | 0.522 | 0.137 | 0.137 | 0.137 | 39500 | 9875 | 2125 | C=1.0 |
| natural | B+ | dialect_lodo_injecagent | 0 | lora | 0.990 | 0.997 | -0.008 | 1.000 | 0.001 | 0.002 | 0.955 | 0.955 | 0.955 | 39500 | 9875 | 2125 | r=8, lr=0.0001, epochs=3 |
| natural | B+ | dialect_lodo_injecagent | 0 | tfidf | 0.960 | 0.979 | -0.019 | 1.000 | 0.006 | 0.004 | 0.877 | 0.877 | 0.877 | 39500 | 9875 | 2125 | C=10.0 |
| natural | B+ | dialect_lodo_bipia | 1 | frozen | 0.972 | 0.625 | 0.346 | 0.941 | 0.109 | 0.104 | 0.013 | 0.007 | 0.002 | 36794 | 9198 | 5508 | C=1.0 |
| natural | B+ | dialect_lodo_bipia | 1 | lora | 0.989 | 0.696 | 0.293 | 0.957 | 0.174 | 0.188 | 0.076 | 0.068 | 0.003 | 36794 | 9198 | 5508 | r=8, lr=0.0001, epochs=3 |
| natural | B+ | dialect_lodo_bipia | 1 | tfidf | 0.963 | 0.592 | 0.371 | 0.936 | 0.088 | 0.055 | 0.026 | 0.012 | 0.002 | 36794 | 9198 | 5508 | C=10.0 |
| natural | B+ | dialect_lodo_browsesafe | 1 | frozen | 0.998 | 0.538 | 0.460 | 0.523 | 0.451 | 0.438 | 0.011 | 0.007 | 0.001 | 29424 | 7357 | 14719 | C=10.0 |
| natural | B+ | dialect_lodo_browsesafe | 1 | lora | 1.000 | 0.599 | 0.401 | 0.606 | 0.501 | 0.501 | 0.030 | 0.012 | 0.001 | 29424 | 7357 | 14719 | r=8, lr=0.0001, epochs=3 |
| natural | B+ | dialect_lodo_browsesafe | 1 | tfidf | 0.994 | 0.537 | 0.457 | 0.536 | 0.399 | 0.387 | 0.020 | 0.012 | 0.004 | 29424 | 7357 | 14719 | C=10.0 |
| natural | B+ | dialect_lodo_fujitsu | 1 | frozen | 0.917 | 0.447 | 0.469 | 0.466 | 0.475 | 0.461 | 0.009 | 0.005 | 0.002 | 23692 | 5922 | 21886 | C=1.0 |
| natural | B+ | dialect_lodo_fujitsu | 1 | lora | 0.963 | 0.504 | 0.459 | 0.541 | 0.477 | 0.465 | 0.026 | 0.008 | 0.000 | 23692 | 5922 | 21886 | r=8, lr=0.0001, epochs=3 |
| natural | B+ | dialect_lodo_fujitsu | 1 | tfidf | 0.884 | 0.650 | 0.234 | 0.699 | 0.429 | 0.427 | 0.142 | 0.116 | 0.071 | 23692 | 5922 | 21886 | C=10.0 |
| natural | B+ | dialect_lodo_injecagent | 1 | frozen | 0.967 | 0.866 | 0.101 | 0.998 | 0.323 | 0.446 | 0.069 | 0.069 | 0.069 | 39500 | 9875 | 2125 | C=1.0 |
| natural | B+ | dialect_lodo_injecagent | 1 | lora | 0.989 | 1.000 | -0.011 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 39500 | 9875 | 2125 | r=8, lr=0.0001, epochs=3 |
| natural | B+ | dialect_lodo_injecagent | 1 | tfidf | 0.960 | 0.981 | -0.021 | 1.000 | 0.006 | 0.004 | 0.879 | 0.879 | 0.879 | 39500 | 9875 | 2125 | C=10.0 |
| natural | B+ | dialect_lodo_bipia | 2 | frozen | 0.975 | 0.617 | 0.358 | 0.939 | 0.102 | 0.100 | 0.017 | 0.004 | 0.000 | 36794 | 9198 | 5508 | C=1.0 |
| natural | B+ | dialect_lodo_bipia | 2 | lora | 0.988 | 0.685 | 0.303 | 0.952 | 0.194 | 0.208 | 0.000 | 0.000 | 0.000 | 36794 | 9198 | 5508 | r=16, lr=0.0001, epochs=3 |
| natural | B+ | dialect_lodo_bipia | 2 | tfidf | 0.963 | 0.580 | 0.384 | 0.933 | 0.088 | 0.057 | 0.010 | 0.009 | 0.002 | 36794 | 9198 | 5508 | C=10.0 |
| natural | B+ | dialect_lodo_browsesafe | 2 | frozen | 0.998 | 0.544 | 0.455 | 0.533 | 0.491 | 0.491 | 0.018 | 0.010 | 0.002 | 29424 | 7357 | 14719 | C=1.0 |
| natural | B+ | dialect_lodo_browsesafe | 2 | lora | 1.000 | 0.627 | 0.373 | 0.644 | 0.422 | 0.422 | 0.065 | 0.038 | 0.002 | 29424 | 7357 | 14719 | r=8, lr=0.0001, epochs=3 |
| natural | B+ | dialect_lodo_browsesafe | 2 | tfidf | 0.996 | 0.534 | 0.462 | 0.533 | 0.335 | 0.288 | 0.019 | 0.011 | 0.002 | 29424 | 7357 | 14719 | C=10.0 |
| natural | B+ | dialect_lodo_fujitsu | 2 | frozen | 0.921 | 0.386 | 0.535 | 0.428 | 0.492 | 0.481 | 0.006 | 0.005 | 0.002 | 23692 | 5922 | 21886 | C=1.0 |
| natural | B+ | dialect_lodo_fujitsu | 2 | lora | 0.962 | 0.553 | 0.410 | 0.605 | 0.487 | 0.476 | 0.054 | 0.000 | 0.000 | 23692 | 5922 | 21886 | r=8, lr=0.0001, epochs=3 |
| natural | B+ | dialect_lodo_fujitsu | 2 | tfidf | 0.883 | 0.645 | 0.239 | 0.696 | 0.428 | 0.425 | 0.142 | 0.119 | 0.075 | 23692 | 5922 | 21886 | C=10.0 |
| natural | B+ | dialect_lodo_injecagent | 2 | frozen | 0.969 | 0.892 | 0.077 | 0.999 | 0.297 | 0.404 | 0.260 | 0.260 | 0.260 | 39500 | 9875 | 2125 | C=10.0 |
| natural | B+ | dialect_lodo_injecagent | 2 | lora | 0.989 | 0.999 | -0.010 | 1.000 | 0.001 | 0.007 | 0.978 | 0.978 | 0.978 | 39500 | 9875 | 2125 | r=16, lr=0.0001, epochs=3 |
| natural | B+ | dialect_lodo_injecagent | 2 | tfidf | 0.960 | 0.982 | -0.023 | 1.000 | 0.006 | 0.007 | 0.895 | 0.895 | 0.895 | 39500 | 9875 | 2125 | C=10.0 |

## Raw table 6 -- BIPIA off-the-shelf reference detectors

These are untrained public detectors scored on the BIPIA leave-one-out test folds. They are comparison probes, not trained rungs, and they are seed-0 only.

| Source | Fold/dialect | Seed | Probe | Model id | n_test | AUPRC | ROC-AUC | Brier | ECE | TPR@1% | TPR@0.5% | TPR@0.1% | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BIPIA reference | carrier_plus_attack_external | 0 | prompt_guard_1 | meta-llama/Prompt-Guard-86M | 890 | 0.998 | 0.959 | 0.197 | 0.220 | 0.812 | 0.812 | 0.812 | ok |
| BIPIA reference | carrier_plus_attack_external | 0 | prompt_guard_2 | meta-llama/Llama-Prompt-Guard-2-86M | 890 | 0.984 | 0.788 | 0.916 | 0.922 | 0.232 | 0.232 | 0.232 | ok |
| BIPIA reference | carrier_plus_attack_external | 0 | protectai_v2 | protectai/deberta-v3-base-prompt-injection-v2 | 890 | 0.940 | 0.485 | 0.382 | 0.403 | 0.014 | 0.014 | 0.014 | ok |
| BIPIA reference | core_attack_type | 0 | prompt_guard_1 | meta-llama/Prompt-Guard-86M | 2720 | 0.998 | 0.972 | 0.124 | 0.142 | 0.806 | 0.776 | 0.662 | ok |
| BIPIA reference | core_attack_type | 0 | prompt_guard_2 | meta-llama/Llama-Prompt-Guard-2-86M | 2720 | 0.958 | 0.661 | 0.879 | 0.891 | 0.108 | 0.091 | 0.033 | ok |
| BIPIA reference | core_attack_type | 0 | protectai_v2 | protectai/deberta-v3-base-prompt-injection-v2 | 2720 | 0.922 | 0.444 | 0.678 | 0.692 | 0.009 | 0.008 | 0.005 | ok |
| BIPIA reference | obfuscation_technique | 0 | prompt_guard_1 | meta-llama/Prompt-Guard-86M | 920 | 0.991 | 0.969 | 0.118 | 0.128 | 0.782 | 0.746 | 0.571 | ok |
| BIPIA reference | obfuscation_technique | 0 | prompt_guard_2 | meta-llama/Llama-Prompt-Guard-2-86M | 920 | 0.868 | 0.677 | 0.755 | 0.765 | 0.083 | 0.068 | 0.018 | ok |
| BIPIA reference | obfuscation_technique | 0 | protectai_v2 | protectai/deberta-v3-base-prompt-injection-v2 | 920 | 0.813 | 0.530 | 0.542 | 0.548 | 0.024 | 0.022 | 0.013 | ok |

## Raw table 7 -- Cross-family Arm B off-the-shelf reference detectors

These are the E8 deployed-baseline comparison rows from `experiments/cross-family-transfer/B2_3_results/summary.json`. They use chunk scoring plus max pooling, with a label-stratified cap of 2,000 documents per dialect where needed. They are non-gating and seed-0 only.

| Source | Slice/dialect | Seed | Probe | Model id | AUROC | Mean attack score | Mean benign score | n_scored | n_full | Capped | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B2.3 | bipia | 0 | protectai_v2 | protectai/deberta-v3-base-prompt-injection-v2 | 0.470 | 0.287 | 0.256 | 2000 | 5508 | yes | ok |
| B2.3 | bipia | 0 | prompt_guard_2 | meta-llama/Llama-Prompt-Guard-2-86M | 0.671 | 0.044 | 0.010 | 2000 | 5508 | yes | ok |
| B2.3 | bipia | 0 | prompt_guard_1 | meta-llama/Prompt-Guard-86M | 0.973 | 0.866 | 0.048 | 2000 | 5508 | yes | ok |
| B2.3 | browsesafe | 0 | protectai_v2 | protectai/deberta-v3-base-prompt-injection-v2 | 0.591 | 0.999 | 0.998 | 2000 | 14719 | yes | ok |
| B2.3 | browsesafe | 0 | prompt_guard_2 | meta-llama/Llama-Prompt-Guard-2-86M | 0.670 | 0.393 | 0.121 | 2000 | 14719 | yes | ok |
| B2.3 | browsesafe | 0 | prompt_guard_1 | meta-llama/Prompt-Guard-86M | 0.635 | 0.395 | 0.158 | 2000 | 14719 | yes | ok |
| B2.3 | fujitsu | 0 | protectai_v2 | protectai/deberta-v3-base-prompt-injection-v2 | 0.693 | 0.166 | 0.030 | 2000 | 21886 | yes | ok |
| B2.3 | fujitsu | 0 | prompt_guard_2 | meta-llama/Llama-Prompt-Guard-2-86M | 0.889 | 0.063 | 0.001 | 2000 | 21886 | yes | ok |
| B2.3 | fujitsu | 0 | prompt_guard_1 | meta-llama/Prompt-Guard-86M | 0.502 | 0.147 | 0.059 | 2000 | 21886 | yes | ok |
| B2.3 | injecagent | 0 | protectai_v2 | protectai/deberta-v3-base-prompt-injection-v2 | 0.608 | 0.660 | 0.583 | 2000 | 2125 | yes | ok |
| B2.3 | injecagent | 0 | prompt_guard_2 | meta-llama/Llama-Prompt-Guard-2-86M | 0.915 | 0.221 | 0.013 | 2000 | 2125 | yes | ok |
| B2.3 | injecagent | 0 | prompt_guard_1 | meta-llama/Prompt-Guard-86M | 0.917 | 0.687 | 0.064 | 2000 | 2125 | yes | ok |

## Raw table 8 -- Cross-family Arm A/off-task off-the-shelf reference detectors

These are the E8 deployed-baseline comparison rows from `experiments/cross-family-transfer/B2_4_results/capped/summary.json`. BIPIA and InjecAgent overlap with the Arm B E8 comparison; JBB and XSTest show the off-task harmful-content slices.

| Source | Slice/dialect | Seed | Probe | Model id | AUROC | Mean attack score | Mean benign score | n_scored | n_full | Capped | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B2.4 | BIPIA | 0 | protectai_v2 | protectai/deberta-v3-base-prompt-injection-v2 | 0.470 | 0.287 | 0.256 | 2000 | 5508 | yes | ok |
| B2.4 | BIPIA | 0 | prompt_guard_2 | meta-llama/Llama-Prompt-Guard-2-86M | 0.671 | 0.044 | 0.010 | 2000 | 5508 | yes | ok |
| B2.4 | BIPIA | 0 | prompt_guard_1 | meta-llama/Prompt-Guard-86M | 0.973 | 0.866 | 0.048 | 2000 | 5508 | yes | ok |
| B2.4 | InjecAgent | 0 | protectai_v2 | protectai/deberta-v3-base-prompt-injection-v2 | 0.608 | 0.660 | 0.583 | 2000 | 2125 | yes | ok |
| B2.4 | InjecAgent | 0 | prompt_guard_2 | meta-llama/Llama-Prompt-Guard-2-86M | 0.915 | 0.221 | 0.013 | 2000 | 2125 | yes | ok |
| B2.4 | InjecAgent | 0 | prompt_guard_1 | meta-llama/Prompt-Guard-86M | 0.917 | 0.687 | 0.064 | 2000 | 2125 | yes | ok |
| B2.4 | JBB | 0 | protectai_v2 | protectai/deberta-v3-base-prompt-injection-v2 | 0.600 | 0.000 | 0.010 | 200 | 200 | no | ok |
| B2.4 | JBB | 0 | prompt_guard_2 | meta-llama/Llama-Prompt-Guard-2-86M | 0.754 | 0.303 | 0.054 | 200 | 200 | no | ok |
| B2.4 | JBB | 0 | prompt_guard_1 | meta-llama/Prompt-Guard-86M | 0.332 | 1.000 | 1.000 | 200 | 200 | no | ok |
| B2.4 | XSTest | 0 | protectai_v2 | protectai/deberta-v3-base-prompt-injection-v2 | 0.411 | 0.000 | 0.000 | 450 | 450 | no | ok |
| B2.4 | XSTest | 0 | prompt_guard_2 | meta-llama/Llama-Prompt-Guard-2-86M | 0.638 | 0.001 | 0.001 | 450 | 450 | no | ok |
| B2.4 | XSTest | 0 | prompt_guard_1 | meta-llama/Prompt-Guard-86M | 0.644 | 1.000 | 1.000 | 450 | 450 | no | ok |

## Raw table 9 -- Final RunPod LoRA provenance

These rows are separated from the canonical raw tables to avoid silently mixing source/provenance paths with merged result trees. They are included because the final cross-family LoRA evidence lives on disk in these untracked folders.

| Source | Condition/pool | Variant | Fold | Seed | Model | Val score | Test ROC-AUC | Gap | Test AUPRC | n_train | n_val | n_test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| runpod/B3_all27_lora | natural | B- | dialect_lodo_bipia | 0 | lora | 0.984 | 0.684 | 0.300 | 0.954 | 30984 | 7746 | 5508 |
| runpod/B3_all27_lora | natural | B- | dialect_lodo_browsesafe | 0 | lora | 1.000 | 0.539 | 0.461 | 0.541 | 23615 | 5904 | 14719 |
| runpod/B3_all27_lora | natural | B- | dialect_lodo_fujitsu | 0 | lora | 0.949 | 0.755 | 0.193 | 0.780 | 17882 | 4470 | 21886 |
| runpod/B3_all27_lora | natural | B- | dialect_lodo_injecagent | 0 | lora | 0.986 | 1.000 | -0.014 | 1.000 | 33690 | 8423 | 2125 |
| runpod/B3_all27_lora | natural | B- | dialect_lodo_bipia | 1 | lora | 0.985 | 0.702 | 0.283 | 0.955 | 30984 | 7746 | 5508 |
| runpod/B3_all27_lora | natural | B- | dialect_lodo_browsesafe | 1 | lora | 1.000 | 0.576 | 0.424 | 0.599 | 23615 | 5904 | 14719 |
| runpod/B3_all27_lora | natural | B- | dialect_lodo_fujitsu | 1 | lora | 0.945 | 0.730 | 0.216 | 0.764 | 17882 | 4470 | 21886 |
| runpod/B3_all27_lora | natural | B- | dialect_lodo_injecagent | 1 | lora | 0.987 | 1.000 | -0.013 | 1.000 | 33690 | 8423 | 2125 |
| runpod/B3_all27_lora | natural | B- | dialect_lodo_bipia | 2 | lora | 0.985 | 0.695 | 0.290 | 0.953 | 30984 | 7746 | 5508 |
| runpod/B3_all27_lora | natural | B- | dialect_lodo_browsesafe | 2 | lora | 1.000 | 0.549 | 0.451 | 0.557 | 23615 | 5904 | 14719 |
| runpod/B3_all27_lora | natural | B- | dialect_lodo_fujitsu | 2 | lora | 0.942 | 0.669 | 0.274 | 0.736 | 17882 | 4470 | 21886 |
| runpod/B3_all27_lora | natural | B- | dialect_lodo_injecagent | 2 | lora | 0.986 | 1.000 | -0.014 | 1.000 | 33690 | 8423 | 2125 |
| runpod/B3_all27_lora | natural | B+ | dialect_lodo_browsesafe | 0 | lora | 1.000 | 0.593 | 0.407 | 0.599 | 29424 | 7357 | 14719 |
| runpod/B3_all27_lora | capped |  | arm_a_pooled | 0 | lora | 0.999 | 0.615 | 0.384 |  | 23239 | 5809 | 8283 |
| runpod/B3_all27_lora | capped |  | arm_a_pooled | 1 | lora | 0.999 | 0.627 | 0.373 |  | 23239 | 5809 | 8283 |
| runpod/B3_all27_lora | capped |  | arm_a_pooled | 2 | lora | 0.999 | 0.663 | 0.337 |  | 23239 | 5809 | 8283 |
| runpod/B3_bplus_cheap_lora | natural | B+ | dialect_lodo_bipia | 0 | lora | 0.989 | 0.711 | 0.278 | 0.960 | 36794 | 9198 | 5508 |
| runpod/B3_bplus_cheap_lora | natural | B+ | dialect_lodo_browsesafe | 0 | lora | 1.000 | 0.600 | 0.400 | 0.590 | 29424 | 7357 | 14719 |
| runpod/B3_bplus_cheap_lora | natural | B+ | dialect_lodo_fujitsu | 0 | lora | 0.964 | 0.424 | 0.540 | 0.486 | 23692 | 5922 | 21886 |
| runpod/B3_bplus_cheap_lora | natural | B+ | dialect_lodo_injecagent | 0 | lora | 0.990 | 0.997 | -0.008 | 1.000 | 39500 | 9875 | 2125 |
| runpod/B3_bplus_cheap_lora | natural | B+ | dialect_lodo_bipia | 1 | lora | 0.989 | 0.696 | 0.293 | 0.957 | 36794 | 9198 | 5508 |
| runpod/B3_bplus_cheap_lora | natural | B+ | dialect_lodo_browsesafe | 1 | lora | 1.000 | 0.599 | 0.401 | 0.606 | 29424 | 7357 | 14719 |
| runpod/B3_bplus_cheap_lora | natural | B+ | dialect_lodo_fujitsu | 1 | lora | 0.963 | 0.504 | 0.459 | 0.541 | 23692 | 5922 | 21886 |
| runpod/B3_bplus_cheap_lora | natural | B+ | dialect_lodo_injecagent | 1 | lora | 0.989 | 1.000 | -0.011 | 1.000 | 39500 | 9875 | 2125 |
| runpod/B3_bplus_cheap_lora | natural | B+ | dialect_lodo_bipia | 2 | lora | 0.988 | 0.685 | 0.303 | 0.952 | 36794 | 9198 | 5508 |
| runpod/B3_bplus_cheap_lora | natural | B+ | dialect_lodo_browsesafe | 2 | lora | 1.000 | 0.627 | 0.373 | 0.644 | 29424 | 7357 | 14719 |
| runpod/B3_bplus_cheap_lora | natural | B+ | dialect_lodo_fujitsu | 2 | lora | 0.962 | 0.553 | 0.410 | 0.605 | 23692 | 5922 | 21886 |
| runpod/B3_bplus_cheap_lora | natural | B+ | dialect_lodo_injecagent | 2 | lora | 0.989 | 0.999 | -0.010 | 1.000 | 39500 | 9875 | 2125 |

## Pivot summaries

### BIPIA trained runs: mean test AUPRC by fold/model

| Fold | Model | n | Mean test AUPRC | SD |
| --- | --- | --- | --- | --- |
| carrier_plus_attack_external | frozen | 3 | 0.986 | 0.004 |
| carrier_plus_attack_external | lora | 3 | 0.998 | 0.001 |
| carrier_plus_attack_external | tfidf | 3 | 0.980 | 0.010 |
| core_attack_type | frozen | 3 | 0.985 | 0.001 |
| core_attack_type | lora | 3 | 0.998 | 0.001 |
| core_attack_type | tfidf | 3 | 0.967 | 0.010 |
| obfuscation_technique | frozen | 3 | 0.963 | 0.002 |
| obfuscation_technique | lora | 3 | 0.989 | 0.003 |
| obfuscation_technique | tfidf | 3 | 0.948 | 0.009 |

### Carrier runs: mean test AUPRC by carrier/model

| Carrier | Model | n | Mean test AUPRC | SD |
| --- | --- | --- | --- | --- |
| code | frozen | 3 | 0.977 | 0.002 |
| code | lora | 3 | 0.998 | 0.000 |
| code | tfidf | 3 | 0.989 | 0.001 |
| email | frozen | 3 | 0.991 | 0.000 |
| email | lora | 3 | 0.999 | 0.001 |
| email | tfidf | 3 | 0.997 | 0.001 |
| table | frozen | 3 | 0.907 | 0.003 |
| table | lora | 3 | 0.965 | 0.007 |
| table | tfidf | 3 | 0.981 | 0.003 |

### Cross-family Arm A: mean gap by pool/model

| Pool | Model | n | Mean gap | SD |
| --- | --- | --- | --- | --- |
| capped | frozen | 3 | 0.313 | 0.004 |
| capped | lora | 3 | 0.365 | 0.025 |
| capped | tfidf | 3 | 0.473 | 0.017 |
| uncapped | tfidf | 3 | 0.487 | 0.014 |

### Cross-family Arm B: mean gap by condition/variant/dialect/model

| Condition | Variant | Held-out dialect | Model | n | Mean gap | SD |
| --- | --- | --- | --- | --- | --- | --- |
| dialect_balanced | B- | dialect_lodo_bipia | frozen | 3 | 0.347 | 0.037 |
| dialect_balanced | B- | dialect_lodo_bipia | tfidf | 3 | 0.335 | 0.023 |
| dialect_balanced | B- | dialect_lodo_browsesafe | frozen | 3 | 0.443 | 0.009 |
| dialect_balanced | B- | dialect_lodo_browsesafe | tfidf | 3 | 0.439 | 0.003 |
| dialect_balanced | B- | dialect_lodo_fujitsu | frozen | 3 | 0.555 | 0.080 |
| dialect_balanced | B- | dialect_lodo_fujitsu | tfidf | 3 | 0.180 | 0.023 |
| dialect_balanced | B- | dialect_lodo_injecagent | frozen | 3 | -0.046 | 0.014 |
| dialect_balanced | B- | dialect_lodo_injecagent | tfidf | 3 | -0.046 | 0.011 |
| natural | B+ | dialect_lodo_bipia | frozen | 3 | 0.350 | 0.007 |
| natural | B+ | dialect_lodo_bipia | lora | 3 | 0.291 | 0.013 |
| natural | B+ | dialect_lodo_bipia | tfidf | 3 | 0.372 | 0.011 |
| natural | B+ | dialect_lodo_browsesafe | frozen | 3 | 0.456 | 0.003 |
| natural | B+ | dialect_lodo_browsesafe | lora | 3 | 0.391 | 0.016 |
| natural | B+ | dialect_lodo_browsesafe | tfidf | 3 | 0.459 | 0.003 |
| natural | B+ | dialect_lodo_fujitsu | frozen | 3 | 0.494 | 0.036 |
| natural | B+ | dialect_lodo_fujitsu | lora | 3 | 0.470 | 0.066 |
| natural | B+ | dialect_lodo_fujitsu | tfidf | 3 | 0.228 | 0.016 |
| natural | B+ | dialect_lodo_injecagent | frozen | 3 | 0.089 | 0.012 |
| natural | B+ | dialect_lodo_injecagent | lora | 3 | -0.010 | 0.002 |
| natural | B+ | dialect_lodo_injecagent | tfidf | 3 | -0.021 | 0.002 |
| natural | B- | dialect_lodo_bipia | frozen | 3 | 0.356 | 0.005 |
| natural | B- | dialect_lodo_bipia | lora | 3 | 0.291 | 0.009 |
| natural | B- | dialect_lodo_bipia | tfidf | 3 | 0.353 | 0.009 |
| natural | B- | dialect_lodo_browsesafe | frozen | 3 | 0.459 | 0.003 |
| natural | B- | dialect_lodo_browsesafe | lora | 3 | 0.445 | 0.019 |
| natural | B- | dialect_lodo_browsesafe | tfidf | 3 | 0.461 | 0.002 |
| natural | B- | dialect_lodo_fujitsu | frozen | 3 | 0.354 | 0.021 |
| natural | B- | dialect_lodo_fujitsu | lora | 3 | 0.228 | 0.042 |
| natural | B- | dialect_lodo_fujitsu | tfidf | 3 | 0.152 | 0.010 |
| natural | B- | dialect_lodo_injecagent | frozen | 3 | -0.034 | 0.002 |
| natural | B- | dialect_lodo_injecagent | lora | 3 | -0.014 | 0.001 |
| natural | B- | dialect_lodo_injecagent | tfidf | 3 | -0.036 | 0.005 |

### B+ minus B- bridge deltas from canonical verdict

| Dialect | B+ minus B- gap delta | Plain meaning |
| --- | --- | --- |
| bipia | 0.000 | unchanged |
| browsesafe | -0.054 | better |
| fujitsu | 0.242 | worse |
| injecagent | 0.005 | worse |

## What the tables say

1. Attack-type transfer inside BIPIA is the easy axis once `lora` is used. The raw BIPIA tables show high LoRA test AUPRC and the canonical verdict shows the pre-registered attack-type contrast collapsing to T = -0.003.
2. Carrier transfer is mixed. Email and code close under LoRA, while table keeps the residual wall. This is why the carrier result should be described as capacity-attenuated, not fully solved and not fully standing.
3. Cross-family transfer is the hard axis. Arm A LoRA gaps remain large, Arm B has three genuine held-out dialects with surviving gaps, and B+ does not bridge the dialect gap.
4. Public reference detectors are scope-specific. They are useful baselines but should not be read as universal guards.

## What looks off or fragile

| Issue | Evidence in tables | Why it matters | Practical fix |
| --- | --- | --- | --- |
| Frozen embedding scope | EDA geometry is separate from LoRA tables | Do not infer LoRA representation shape from MiniLM geometry | Say frozen MiniLM geometry. |
| AUPRC inflation | Carrier/public-reference rows can have high prevalence floors | High AUPRC can be misleading when positives are common | Lead with ROC-AUC and class means. |
| InjecAgent low power | Arm B rows show mechanical FALSIFIED despite only 17 negatives in canonical notes | This is not transfer success | Always mark uninformative. |
| Mechanism overclaim | Arm A over-defense is visible but not causal | Tables show a symptom, not why it happens | Pre-register a focused mechanism test. |
| Artifact provenance | RunPod rows are untracked and separated | Future readers need to know what is canonical vs source evidence | Add a run manifest or committed provenance note. |

## Paths forward

| When | Path | Pros | Cons | Recommendation |
| --- | --- | --- | --- | --- |
| Do now | Consolidate record surfaces | Prevents stale two-axis claims and makes the raw results inspectable | No new science | Do first. |
| Do now | Add artifact provenance | Prevents unnecessary reruns and explains RunPod sources | Administrative work | Add compact manifest/summary. |
| Do next | Mechanism test for cross-family failure | Explains whether calibration, lexical shortcuts, or corpus mismatch drives failure | Can sprawl if not pre-registered | Worth doing before causal claims. |
| Do next | Lane 2 carrier/table training | Targets the residual table wall | Synthetic-data path has blockers | Proceed only with narrow carrier/table framing. |
| When unblocked | Carrier n=5 re-test | Strengthens provisional n=3 result | License-gated | Queue; do not block consolidation. |

## Bottom line

The raw tables make the result clearer than the narrative alone: small fine-tuning solves attack-type transfer inside BIPIA, partly solves carrier transfer but leaves table, and does not solve cross-family transfer. The numbers are strong enough to support the axis-dependent story, but the repo still needs provenance cleanup and careful wording around low-unit-count and mechanism claims.
