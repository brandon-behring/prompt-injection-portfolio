# B3 RunPod provenance manifest (generated mechanically 2026-06-10)
#
# Source pods: all-27 concurrent H100 sweep (~$16; recovered A+B− lora + Arm A + B+ pilot)
#              + cheap Ada RTX-4090 B+ run (~$3-5; criteria.md Rev 9 gpu_order fix).
# Reconciliation (audit 2026-06-10, consolidated-audit-2026-06-09.md §5): every metrics.json
# below is byte-identical (sha256) to its canonical merged-tree counterpart; the single expected
# cross-arch pair is browsesafe-s0 B+ (H100 0.5928 vs 4090 0.5999, Δroc 0.0072 ≪ 0.05 SESOI).
# Canonical B+ tree comes from the 4090 run. Parquets are local-only (gitignored), inventoried below.
#
# sha256  bytes  path
32a4fb86ed871ba82bb4bc1437cf0a92190b8814fef914b8f55d49cffe30abf3  1032  B3_results_runpod_all27_lora/B2_3_results_Bplus/natural/seed=0/dialect_lodo_browsesafe/lora.metrics.json
b423ecdfad3b1d16799e1ba0b9f96fcda19bc21ac76b67c43d267dbcd9b4f98f  1027  B3_results_runpod_all27_lora/B2_3_results/natural/seed=0/dialect_lodo_bipia/lora.metrics.json
f128e42432410583e139e44fd7eeec4c236bf962a62d6aa4f3aaeee6bdcedc5c  1035  B3_results_runpod_all27_lora/B2_3_results/natural/seed=0/dialect_lodo_browsesafe/lora.metrics.json
8486a6f0ed91cef092870d5cdbe18b1348f9679ac831c7c33ed8f6024e4e9496  1012  B3_results_runpod_all27_lora/B2_3_results/natural/seed=0/dialect_lodo_fujitsu/lora.metrics.json
6a0f5d957f34aafffd29a76331d3824985139e809c831456ce41e4849c5a89b9  940  B3_results_runpod_all27_lora/B2_3_results/natural/seed=0/dialect_lodo_injecagent/lora.metrics.json
34ccdf8ab7a8e3940c029b78d843368513613f55ba12b6cc3ba66949a2a5040a  1027  B3_results_runpod_all27_lora/B2_3_results/natural/seed=1/dialect_lodo_bipia/lora.metrics.json
df251c99d04e137a7f4bbc2cbbbbcd88f2cf2d1b501c0595c4378087ddd8e393  1034  B3_results_runpod_all27_lora/B2_3_results/natural/seed=1/dialect_lodo_browsesafe/lora.metrics.json
34cbde30a38c8f16d2e42025a0e4600b71ecfeb55c61c3997309ba459adc5370  1009  B3_results_runpod_all27_lora/B2_3_results/natural/seed=1/dialect_lodo_fujitsu/lora.metrics.json
25f874a3c4541f270f6833d0ddd8204748b1083446ec759a235347020781a6be  942  B3_results_runpod_all27_lora/B2_3_results/natural/seed=1/dialect_lodo_injecagent/lora.metrics.json
590d3223fb80d388e4223258fe41032f2d636e13b1bbd1685207014d55bd104a  1027  B3_results_runpod_all27_lora/B2_3_results/natural/seed=2/dialect_lodo_bipia/lora.metrics.json
ff096b4cd26a2253dce7bc194f2bbe9a059b695dca3919a3b48b9b9dca752728  1031  B3_results_runpod_all27_lora/B2_3_results/natural/seed=2/dialect_lodo_browsesafe/lora.metrics.json
cb7d68ad6edc3a5df52d89d143d89e05d421fa8519a3c1326db0863cc370e773  1010  B3_results_runpod_all27_lora/B2_3_results/natural/seed=2/dialect_lodo_fujitsu/lora.metrics.json
c4eca5ada01c2cf137a490c0c8db0ae6ef61c5bb819f5dc36d81da150567ca3c  942  B3_results_runpod_all27_lora/B2_3_results/natural/seed=2/dialect_lodo_injecagent/lora.metrics.json
36309f8e2623b23b383149d39ba5075cdf4d35e78a079728df7eae23dbaa93a2  470  B3_results_runpod_all27_lora/B2_4_results/capped/seed=0/arm_a_pooled/lora.metrics.json
b789f8f676c6d8abd3a0168d1c9f6bf5ade6e1e54126e8edb3ebfb482f085185  468  B3_results_runpod_all27_lora/B2_4_results/capped/seed=1/arm_a_pooled/lora.metrics.json
6d9f83e39a110cda1d177d3a3da2569460457d318c991266d9ae20142f387c18  472  B3_results_runpod_all27_lora/B2_4_results/capped/seed=2/arm_a_pooled/lora.metrics.json
6cc0c52927818acf672194b846608cccb9792f1b37f1e9741a66c533e3751d89  1023  B3_results_runpod_bplus_cheap_lora/B3_lora_bplus_cheap/B2_3_results_Bplus/natural/seed=0/dialect_lodo_bipia/lora.metrics.json
e82ce9c4e01875e8498aff5f87bede03df60bcc903992ef6eb7f5ae127ee82bf  1033  B3_results_runpod_bplus_cheap_lora/B3_lora_bplus_cheap/B2_3_results_Bplus/natural/seed=0/dialect_lodo_browsesafe/lora.metrics.json
6769494166b5df00be2e06a20b29df94d0957382c78706d3b419a067d6254bc4  965  B3_results_runpod_bplus_cheap_lora/B3_lora_bplus_cheap/B2_3_results_Bplus/natural/seed=0/dialect_lodo_fujitsu/lora.metrics.json
dc1cd3af1a4481acbc87ec3d24d2697bc1b281f0fe24c8d93d7ab35d5001308f  1015  B3_results_runpod_bplus_cheap_lora/B3_lora_bplus_cheap/B2_3_results_Bplus/natural/seed=0/dialect_lodo_injecagent/lora.metrics.json
91aad6a7a4bb9ff427e90d3fa5b60924584884f1e9ea5f63c44d79e5e92f6d49  1024  B3_results_runpod_bplus_cheap_lora/B3_lora_bplus_cheap/B2_3_results_Bplus/natural/seed=1/dialect_lodo_bipia/lora.metrics.json
c991549c8596a75d820af81d7c9ac085b55109eb9eb0e4ce8c6029ef87fbeabc  1028  B3_results_runpod_bplus_cheap_lora/B3_lora_bplus_cheap/B2_3_results_Bplus/natural/seed=1/dialect_lodo_browsesafe/lora.metrics.json
e6a902f3f757b1cc5323ae2b700870e960ed174980f1095f267b4e47e3714b4e  996  B3_results_runpod_bplus_cheap_lora/B3_lora_bplus_cheap/B2_3_results_Bplus/natural/seed=1/dialect_lodo_fujitsu/lora.metrics.json
4b76b9deb00c4f7bc76bae499a7d0577be55b695697e5db72a8ae5d9cc10ad07  942  B3_results_runpod_bplus_cheap_lora/B3_lora_bplus_cheap/B2_3_results_Bplus/natural/seed=1/dialect_lodo_injecagent/lora.metrics.json
3c8e27ec6603c4785583bb8e2f1acbcaa8f4a2cd552f9207543b758b25c28d6e  976  B3_results_runpod_bplus_cheap_lora/B3_lora_bplus_cheap/B2_3_results_Bplus/natural/seed=2/dialect_lodo_bipia/lora.metrics.json
78ee709a7ad97f99292fb3b570f069f2066ec2f5a68c2a431e44823e109447d7  1029  B3_results_runpod_bplus_cheap_lora/B3_lora_bplus_cheap/B2_3_results_Bplus/natural/seed=2/dialect_lodo_browsesafe/lora.metrics.json
ba9d402a5ffa1689f16b306ce87964dcb9a05becd98d7a97753a6685f033864d  979  B3_results_runpod_bplus_cheap_lora/B3_lora_bplus_cheap/B2_3_results_Bplus/natural/seed=2/dialect_lodo_fujitsu/lora.metrics.json
a05ac7fde7f7c3244b3732ca6b0b1915117661e490c7277d15752451caf515fe  1016  B3_results_runpod_bplus_cheap_lora/B3_lora_bplus_cheap/B2_3_results_Bplus/natural/seed=2/dialect_lodo_injecagent/lora.metrics.json
#
# Parquet inventory (local-only):
#   B3_results_runpod_all27_lora: 19 parquets, 421M total
#   B3_results_runpod_bplus_cheap_lora: 12 parquets, 324M total
