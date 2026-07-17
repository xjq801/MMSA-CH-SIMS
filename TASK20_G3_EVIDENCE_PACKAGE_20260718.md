# 任务20 G3证据提交包

> 提交状态：`HANDOFF_20_SUPPLEMENT_READY_PENDING_00_FINAL_REVIEW`  
> G3决定：`HOLD_FOR_SUPPLEMENT_PENDING_00_FINAL_REVIEW`  
> SSOT：总纲v1.16第17节任务20  
> 证据日期：2026-07-18 +08:00

## 请求00审查的范围

本包只请求00审查任务20第1–18项执行证据，不自行修改总纲、G1、G2或G3。当前权威上游状态继续为`G1=PASS`、`G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`、`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`、总门`PASS_WITH_ACCEPTED_ASSET_RISK`。

建议00裁定字段：

- `TASK20_EXECUTION_EVIDENCE`：是否足以进入G3审查；
- `ASSET_RISK_PROPAGATION`：必须继续保留，不得改写为I3D权利已解决；
- `TASK50_STATISTICS`：明确不在本次任务20单种子证据内。

## 1–18项证据映射

| 项 | 状态 | 核心证据 |
|---:|---|---|
| 1 | COMPLETED | `HANDOFF_10.md`及dataset/split/label/leakage固定hash已复核，未重定义标签 |
| 2 | COMPLETED | `.venv-task20`独立环境锁定，formal准备检查通过；默认旧环境faiss缺失继续诚实保留 |
| 3 | COMPLETED | 统一experiment schema、run manifest与“只改变model字段”合同 |
| 4 | COMPLETED | canonical loader固定sample ID、`group_by_video_v1`、class order和T0边界 |
| 5 | COMPLETED_WITH_NA | 总体均值、经验分布、多数类已实现；主题均值为`NOT_APPLICABLE_NATIVE_TOPIC_ABSENT` |
| 6 | COMPLETED_LEGACY_ONLY | CatBoost/HGB/LightGBM各12-trial原生兼容重跑；非T0、不可与CSMV主结果比较 |
| 7 | COMPLETED_STRONG_REIMPLEMENTATION | VC-CSA官方复现失败保留；temporal-attention强基线完成单种子正式dev/test |
| 8 | COMPLETED_WITH_SCOPE_LIMITS | I3D pooled/temporal模型已实现；未冻结CLIP/SigLIP/VideoMAE不伪造 |
| 9 | NOT_APPLICABLE | `NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`，不伪造模态增量 |
| 10 | COMPLETED | JS、NLL、EMD、Macro-F1、Balanced Accuracy、Brier、ECE、ACE、AURC-JS |
| 11 | COMPLETED_INTERFACE_ONLY | 视频级paired bootstrap接口与确定性测试通过；正式五种子统计留任务50 |
| 12 | COMPLETED | 等预算12-trial、最大epoch、patience、dev选择和test前冻结规则 |
| 13 | COMPLETED | prediction包含sample ID、真实/预测分布、置信度、拒绝分数、model/config ID |
| 14 | COMPLETED | E0拒绝train/eval重叠和sample-ID错位 |
| 15 | COMPLETED | smoke、单种子完整run、正式dev同seed独立replay及fail-closed hash比较 |
| 16 | COMPLETED | `BASELINE_TABLE_V1.md`已冻结，四类证据身份明确分离 |
| 17 | COMPLETED | `TASK20_BASELINE_EXECUTION_AUDIT.md`保留依赖、数据、许可、性能和实现根因 |
| 18 | SUBMITTED_PENDING_00_REVIEW | 已发送新00总控任务；00验收状态不由任务20预填 |

## 正式运行证据

强视觉基线固定seed `20260717`，`group_by_video_v1`为5698 train / 837 dev / 1675 test。12-trial只用dev选择trial 4：hidden=128、dropout=0.3、learning rate=0.001、best epoch=5。唯一test评测未做test适配：

- JSD 0.182668；NLL 1.715192；EMD 0.162983；Brier 0.227379；
- ECE 0.053885；ACE 0.054004；AURC 0.175399；
- Macro-F1 0.137048；Balanced Accuracy 0.148577。

任务15正式dev replay未再次读取test。原run与replay的四项核心产物SHA-256一致：

- predictions `e08c5b3d94217d145e94baa03ad6e0323c150898cee0d12a2044f78152760cbf`；
- metrics `0271a6547d6245bd1fcd1cee9615af30bedf7fb588048f67369e58ce70ae2100`；
- selection `dce53eeb8f3d618d2ed6e09fecc49164a0e6ac72b5254a065ebf4f493c97dfbf`；
- trial results `b5a246c3422052487e38baede213bf8c92c052e8782bdf75bc5bb01c1ba14f1f`。

replay manifest SHA-256为`2b5b3473473ffe1d50435d2838642de1cae00b6618b29f93df79a5facfcfde3d`，比较报告SHA-256为`5d85fa1dbfdd263e5c5086e57bab3ce5305af4c340e28cf4315a1bbcbea1458d`。该一致性只支持同环境固定seed工程复跑。

## 验证门

- 新比较器按TDD经历缺模块红测，随后3/3专项测试通过；全量测试56/56通过。
- replay run manifest schema验证通过，文本产物本机绝对路径扫描无命中。
- 工作日志验证、项目准备检查、compileall和diff check在提交前执行；独立任务20环境`formal_model_work_ready=true`。
- run bundle、模型权重、standardizer、预测和受限I3D资产均保持Git忽略，仅提交不可逆hash与聚合指标。

## 必须传播的限制与止损

1. I3D许可、官方revision、权利方包身份/fixity仍未知，状态只能是`DEFERRED_ACCEPTED_RISK`。
2. 若权利方否认或固定hash/8210覆盖漂移，立即停止并将相关结果标记`ASSET_INVALIDATED_DO_NOT_REPORT`。
3. VC-CSA继续为`FAILED_OFFICIAL_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH`；强基线不得改写为官方复现。
4. 当前数值是单种子证据，不能宣称论文级优越性；五种子、正式bootstrap和paired comparison属于任务50。
5. 禁止提交、发布或再分发I3D `.npy`、junction、本机路径、模型权重或可逆受限资产。

## 00复核入口

- `BASELINE_TABLE_V1.md`
- `TASK20_BASELINE_EXECUTION_AUDIT.md`
- `experiments/EXPERIMENT_REGISTRY.md`
- `configs/task20/run-manifest.schema.json`
- `configs/task20/tuning-plan-v1.json`
- `scripts/compare_task20_runs.py`
- `WORK_LOG.md`中任务20连续记录

本包是审查请求，不是G3自批文件。00应基于上述证据和限制独立给出接受、补证或拒绝结论。

## HANDOFF_20补证

00在commit `3273ab2926581a877f89d5adc7da591dbe1dba2d`中确认任务20执行证据可进入G3复核，但因总纲必需产出`HANDOFF_20.md`缺失而保持`G3=HOLD_FOR_SUPPLEMENT`。任务20现补交：

- `HANDOFF_20.md`：冻结输入、split、指标、调参预算、run/replay、完成/未完成项、下游合同和强制止损；
- `data/manifests/task20-handoff-v1.manifest.json`：绑定证据主体commit `b89d8dc1d62b5d6ea7b07b1d30cc8f19224c030d`、提交状态commit `aed141b78b0babe4bad10555f335587f983f479b`及22项tracked证据SHA-256；
- `scripts/validate_task20_handoff.py`：不需要受限资产即可从Git对象库验证commit、原始blob字节SHA-256、长度、风险词和路径安全；
- manifest SHA-256：`6d75e2190a50dc4a2191458d6d379a7d49a84f630d5ccf3eb27ac83294f96e91`；
- `HANDOFF_20.md`当前SHA-256：`5a503d90308781620b4e4a7c99b409e29f30cd0872fc6f8b51da6c580a9b56cb`。

补证只关闭交接文件缺失，不自行改变G3；最终`PASS_WITH_LIMITATIONS`或`REJECT`仍由00独立裁定。
