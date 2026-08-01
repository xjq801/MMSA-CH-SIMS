# Task20 论文基线与评测章节完成说明（2026-08-01）

## 1. 交付状态

- 状态：`REQUEST_00_TASK20_MANUSCRIPT_REVIEW`
- 输入父提交：`9a1612fa81e2a3be0173c91fde8e5ce237e7083d`
- Task10 内容提交：`1d2018ceb833376112174e7eb4d6e7528305d856`
- 修改目标：`paper/TAFFC_CARM_MANUSCRIPT_SSOT.md` v0.1.2
- 稿件状态保持：`MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS`
- 结果冻结保持：`NOT_AVAILABLE`
- C1--C4：仍为 `TO_VERIFY`，本批不升级任何 claim。

本批仅填写 Task20 拥有的基线、指标、实现复现、协议可信性和相应限制/补充材料文字。Task10 拥有的 Sec.1.1、Sec.3、Sec.5.2/5.3/5.7、Data Availability、Ethics/Privacy、S1/S2 未改写；`TASK10_MANUSCRIPT_SECTION_COMPLETION_20260801.md` 未修改，其内容仍等待 00 独立验收。

## 2. 新增文字与精确证据

| 稿件位置 | 本批新增内容 | 精确证据 | 仍保留的缺口 |
|---|---|---|---|
| Sec.5.4 Baselines | 区分 `OFFICIAL_REPRODUCTION_ATTEMPT`、`REIMPLEMENTATION_STRONG_BASELINE`、`LEGACY_NATIVE_COMPATIBILITY` 与 `REFERENCE_MODEL`；传播 VC-CSA post-snapshot erratum；固定 unavailable/N/A 边界 | `TASK20_BASELINE_EXECUTION_AUDIT.md` SHA-256 `a4a6687f8dfcd7553e9f14d18c2eb1c668e2fa53750054ed9d6c11fe5b96dfa5`；`BASELINE_TABLE_V1.md` SHA-256 `7a2b612c16ebe8110a67a4108877ae0aca4082d8b7ab7d87897dc48f6c651f44`；`TASK20_POST_SNAPSHOT_VCCSA_ERRATUM_20260718.md` SHA-256 `a02870b82853ff4e14c1a00af6b786fc7329a88bfdd048335a08eb7895575f2e`；`TASK00_TASK20_FINAL_CLOSEOUT_REVIEW_20260801.md` SHA-256 `935641c7cad38f63871102c189e5b3e5ad13d14e160d662841193cc83490baf4` | `[RESULT-GAP:FORMAL_BASELINE_TABLE_WITH_FIVE_SEED_UNCERTAINTY]`；Task50 五种子与配对统计；不得使用 VC-CSA 探索数值 |
| Sec.5.6 Metrics | 定义 JS、NLL、EMD、Macro-F1、Balanced Accuracy、Brier、ECE、ACE、AURC-JS 的方向、聚合和语义；明确 AURC-JS 非 AUROC | `scripts/task20_metrics.py` SHA-256 `45844dc47959206b92972c16ebec46efa3c233271f5d148c4e94e0096de744c0`；`scripts/task20_evaluation.py` SHA-256 `ce6f00b810b4a582b048c78beffa531dec9478d13d48a039d8a7e282bcace323`；`TASK20_G3_EVIDENCE_PACKAGE_20260718.md` SHA-256 `cf906a93c9cd1c8ad6c022d7bfe019d323ba19d0f6aa4bd7786a338c152248c6` | `[RESULT-GAP:FINAL_METRIC_VALUES_AND_NATIVE_UNIT_UNCERTAINTY]`；正式 bootstrap/paired comparison 归 Task50 |
| Sec.5.8 Implementation and reproducibility | 独立环境、统一 schema/loader/evaluator、train-only 拟合、dev 选择、test 一次、12-trial 预算、同环境同 seed replay、hash-bound 证据 | `TASK20_ENVIRONMENT_LOCK.md` SHA-256 `5c46550d5d932054fdd9ed1216ba2d0285c66e4f5640501418c3e7ee47d0d684`；`requirements-task20-lock.txt` SHA-256 `51e986891ba1ed64cebee6503fc820adc67c8b0dcfe5b7ef0bf8f78a1e3c3b6d`；`configs/task20/tuning-plan-v1.json` SHA-256 `01878e74f6f9c150d583ad591b0b7b5fb662208119076aef51ccb237ab741cf9`；`configs/task20/run-manifest.schema.json` SHA-256 `7c14ba2c8155e16a8afa11608476ba6f697eb42326103d598b66125401b03546`；`configs/task20/prediction.schema.json` SHA-256 `fadc6ff7571241bedec48e94f69082d1f6273fa627c610c7f479572e16b19d6e`；`HANDOFF_20.md` SHA-256 `5a503d90308781620b4e4a7c99b409e29f30cd0872fc6f8b51da6c580a9b56cb` | `[RESULT-GAP:FINAL_REPRODUCIBILITY_TABLE]`；最终方法环境、运行代价与可公开定位符待结果冻结 |
| Sec.6.1 Protocol validity and baseline credibility | 仅写 G3 协议可信性、E0 fail-closed 范围、22 项 hash-bound handoff 和单 seed 工程复现边界；不写性能优越性 | `TASK00_G3_FINAL_REVIEW_20260718.md` SHA-256 `cbf7a64e2e78d6eb5ad6c7b24b013ff1ad26ea290ce6a2940b030f22223f43e0`；`TASK20_G3_EVIDENCE_PACKAGE_20260718.md` SHA-256 `cf906a93c9cd1c8ad6c022d7bfe019d323ba19d0f6aa4bd7786a338c152248c6`；`HANDOFF_20.md` SHA-256 `5a503d90308781620b4e4a7c99b409e29f30cd0872fc6f8b51da6c580a9b56cb` | `[RESULT-GAP:C1_G1_G2_G3_AND_E0_EVIDENCE]` 保留；正式 dataset counts、性能表、五种子与配对区间待 Task50 |
| Sec.8 与 Supplement S3/S4/S9 | 增补单 seed、比较器可用性、VC-CSA NON_T0、指标操作化与确定性范围；给出调参和复现清单 | 同上 Task20 baseline、metric、environment、tuning、G3 与 closeout 证据 | Task30/40 的 teacher/memory/router 和 Task50 的正式统计、Video2Reaction 双轨不在本批 |

## 3. 强制边界复核

1. temporal-attention 仅写为 `REIMPLEMENTATION_STRONG_BASELINE` 且仅具单 seed 工程证据。
2. VC-CSA 120 epoch 运行仅为 `AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`，`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`；稿件未写入其性能数值。
3. CLIP/SigLIP/VideoMAE 保持 `NOT_AVAILABLE_IN_FROZEN_T0_PROTOCOL`；late fusion/cross-attention/E1 保持 `NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`。
4. I3D 许可、官方 revision、权利方包身份/fixity 继续为 UNKNOWN；稿件不承诺再分发。
5. Abstract 最终结果、Sec.6.2--6.7、Sec.7、Sec.9 未填写；未新增引用或编造结果。
6. 五种子、正式 bootstrap/paired comparison 与 Video2Reaction 双轨归 Task50；teacher/memory 归 Task30/40。

## 4. 待 00 审查事项

- **RESULT gaps**：本文所列全部 `RESULT-GAP` 只能由 Task50 冻结结果消解。
- **CITATION gaps**：本批没有引入新的文献事实；正式 baseline 文献引用仍须通过引用核验后填写。
- **DECISION gaps**：最终公开仓库、可公开 artifact locator、I3D 长期处置及投稿披露仍由 00/后续任务裁定。
- **措辞审查**：请 00 复核内部 G3 术语在最终论文版本中是否保留，或在结果冻结后改写为外部可读的协议验证措辞。

## 5. 验证与提交

验证命令和真实结果在同批 `WORK_LOG.md` 记录。提交与推送完成后，本节由精确 commit 与文件 SHA-256 补充绑定。
