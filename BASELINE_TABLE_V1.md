# baseline-table-v1

> 状态：`VALIDATION_TABLE_NOT_PAPER_RESULTS`  
> 数据：CSMV HUMAN_GOLD，`group_by_video_v1`；明确标注的legacy原生兼容行除外  
> 主指标：CSMV为Jensen–Shannon divergence且test尚未查看；legacy原生二分类test已按独立冻结规则各评测一次

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
| 冻结I3D temporal attention | REIMPLEMENTATION_STRONG_BASELINE | 完整I3D序列+mask | CPU_SMOKE_COMPLETED_FORMAL_RUN_BLOCKED | 验证实现，不进论文表 | 同seed两次预测/指标/选择hash一致；非VC-CSA官方复现 |
| CLIP/SigLIP/VideoMAE+MLP | REFERENCE_MODEL | 未冻结特征 | NOT_AVAILABLE_IN_FROZEN_T0_PROTOCOL | 无 | 不另行下载或伪造 |
| late fusion | REIMPLEMENTATION | 多模态 | NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY | 无 | CSMV仅一个T0模态 |
| multimodal cross-attention | REIMPLEMENTATION | 多模态 | NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY | 无 | 不把时间处理冒充模态融合 |

CSMV正式表格数值仍须在合格环境中完成预注册dev选择、单种子完整run与test一次性评测后另行填入。上列legacy数值来自独立原生二分类兼容重跑，只能用于失败/历史对照附表，不能与CSMV八类分布结果比较，也不能承担T0或主结论证据。
