# baseline-table-v1

> 状态：`TASK16_FROZEN_BASELINE_TABLE_V1_SINGLE_SEED_NOT_TASK50_FINAL`  
> 冻结时间：2026-07-18 00:00 +08:00  
> 数据：CSMV HUMAN_GOLD，`group_by_video_v1`；明确标注的legacy原生兼容行除外  
> 主指标：CSMV为Jensen–Shannon divergence；强视觉基线test已按冻结selection评测一次，其余CSMV基线尚未正式评测；legacy原生二分类test已按独立冻结规则各评测一次

分类合同：`OFFICIAL_REPRODUCTION_ATTEMPT`只用于固定官方材料的复现尝试；`REIMPLEMENTATION`/`REIMPLEMENTATION_STRONG_BASELINE`是本项目重实现；`LEGACY_NATIVE_COMPATIBILITY`只保留原任务兼容结果；`REFERENCE_MODEL`只列参考资格，不伪造未冻结输入或数值。

| baseline | 分类 | 输入 | 当前状态 | 数值资格 | 说明 |
|---|---|---|---|---|---|
| 总体均值 | REIMPLEMENTATION | 无内容输入，train标签统计 | DEV_SMOKE_COMPLETED | 验证实现，不进论文表 | train-only |
| 主题均值 | REIMPLEMENTATION | 原生topic | NOT_APPLICABLE_NATIVE_TOPIC_ABSENT | 无 | 8210条均无原生topic |
| 经验分布 | REIMPLEMENTATION | 无内容输入，train argmax经验分布 | DEV_SMOKE_COMPLETED | 验证实现，不进论文表 | train-only |
| 多数类 | REIMPLEMENTATION | 无内容输入，train多数类 | DEV_SMOKE_COMPLETED | 验证实现，不进论文表 | train-only |
| 原48维+CatBoost | LEGACY_NATIVE_COMPATIBILITY | CUC legacy 48维 | COMPLETED_LEGACY_NATIVE_NON_T0_NON_COMPARABLE | 仅legacy附表 | test Macro-F1=0.5346，Balanced Acc=0.6006，AUPRC=0.6884，Recall=0.2183；不复用旧数值 |
| 原48维+HGB | LEGACY_NATIVE_COMPATIBILITY | CUC legacy 48维 | COMPLETED_LEGACY_NATIVE_NON_T0_NON_COMPARABLE | 仅legacy附表 | test Macro-F1=0.4591，Balanced Acc=0.5514，AUPRC=0.5989，Recall=0.1338；不复用旧数值 |
| 原48维+LightGBM | LEGACY_NATIVE_COMPATIBILITY | CUC legacy 48维 | COMPLETED_LEGACY_NATIVE_NON_T0_NON_COMPARABLE | 仅legacy附表 | test Macro-F1=0.3645，Balanced Acc=0.4766，AUPRC=0.4581，Recall=0.0528；不复用旧数值 |
| VC-CSA | OFFICIAL_REPRODUCTION_ATTEMPT | 视频+目标评论 | FAILED_OFFICIAL_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH | 无 | 官方revision无模型代码；输入非T0 |
| 冻结I3D pooled MLP | REIMPLEMENTATION | I3D mean/std | CPU_SMOKE_COMPLETED_FORMAL_RUN_BLOCKED | 验证实现，不进论文表 | 同seed两次预测hash一致 |
| 冻结I3D temporal attention | REIMPLEMENTATION_STRONG_BASELINE | 完整I3D序列+mask | SINGLE_SEED_FORMAL_TEST_AND_DEV_REPLAY_COMPLETED_ACCEPTED_ASSET_RISK | 单种子正式值；待任务50五种子统计 | test JSD=0.182668，NLL=1.715192，EMD=0.162983，Brier=0.227379，ECE=0.053885，ACE=0.054004，AURC=0.175399，Macro-F1=0.137048，Balanced Acc=0.148577；正式dev同seed独立replay四项核心产物hash一致；非VC-CSA官方复现 |
| CLIP/SigLIP/VideoMAE+MLP | REFERENCE_MODEL | 未冻结特征 | NOT_AVAILABLE_IN_FROZEN_T0_PROTOCOL | 无 | 不另行下载或伪造 |
| late fusion | REIMPLEMENTATION | 多模态 | NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY | 无 | CSMV仅一个T0模态 |
| multimodal cross-attention | REIMPLEMENTATION | 多模态 | NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY | 无 | 不把时间处理冒充模态融合 |

temporal-attention数值来自冻结12-trial dev选择后的单种子test一次性评测，在内部研究授权和`DEFERRED_ACCEPTED_RISK`下成立；同seed正式dev replay只证明同环境工程复跑。尚未完成任务50五种子统计与正式bootstrap，不能作为最终论文比较结论。上列legacy数值来自独立原生二分类兼容重跑，只能用于失败/历史对照附表，不能与CSMV八类分布结果比较，也不能承担T0或主结论证据。
