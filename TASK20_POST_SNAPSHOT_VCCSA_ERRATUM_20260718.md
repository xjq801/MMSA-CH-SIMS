# Task20 post-snapshot VC-CSA erratum

> 日期：2026-07-18  
> 类型：hash-bound G3快照后的状态勘误与补充说明  
> 当前VC-CSA状态：`AUTHOR_ORIGINAL_PATH_SMOKE_EXECUTABLE_FULL_REPRODUCTION_BLOCKED_COMPUTE`  
> 协议身份：`AUTHOR_ORIGINAL_SETTING_NON_T0`

## 1. 适用范围与优先级

本勘误只覆盖VC-CSA“当前代码可得性、运行状态和输入隔离证据”的解释，不修改G3裁定、既有T0强基线数值、split、评测器或资产风险。

发生冲突时，下列优先级仅对VC-CSA当前状态生效：

1. 本勘误及`TASK20_BASELINE_EXECUTION_AUDIT.md`第8—9节；
2. 00更正后的`TASK00_G3_FINAL_REVIEW_20260718.md`；
3. 以下hash-bound或冻结历史快照中的旧状态文字。

历史快照保持字节不变，不静默改写：

| 文件 | 冻结SHA-256 | 旧文字定位 | 当前解释 |
|---|---|---|---|
| `TASK20_G3_EVIDENCE_PACKAGE_20260718.md` | `cf906a93c9cd1c8ad6c022d7bfe019d323ba19d0f6aa4bd7786a338c152248c6` | 第69行 | 只表示当时官方main `99d1424`审计状态 |
| `BASELINE_TABLE_V1.md` | `7a2b612c16ebe8110a67a4108877ae0aca4082d8b7ab7d87897dc48f6c651f44` | 第19行 | 冻结v1历史行，不表示当前作者fork运行状态 |
| `HANDOFF_20.md` | `5a503d90308781620b4e4a7c99b409e29f30cd0872fc6f8b51da6c580a9b56cb` | 第96行 | hash-bound交接快照历史状态 |

除VC-CSA状态解释外，上述文件的其他内容和绑定关系继续有效。`scripts/validate_task20_handoff.py`仍应按原snapshot commit校验22项证据；本勘误不冒充重新绑定旧handoff。

## 2. 状态时间线

1. **历史官方main尝试**：`IEIT-AGI/MSA-CRVI@99d1424`当时无模型代码，且目标评论/comment split不符合T0。该状态现写为`HISTORICAL_OFFICIAL_MAIN_99D1424_ATTEMPT_FAILED_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH`。
2. **作者实现定位**：定位`JackySnake/MSA-CRVI@3e8c426`及上游open PR #3，代码缺失不再是当前阻塞；PR未合并事实不变。
3. **兼容与首次smoke**：修复依赖、死导入、路径和launcher后，本地GPU入口成功运行。训练入口未迭代test split，但旧smoke构建器仍复制了总标注字典和完整video映射，因此当时“物理无test”证据不足。
4. **输入隔离修复与重跑**：TDD修复后，runtime标注和video映射ID严格等于8个train与4个dev的并集，`test_set=[]`，不存在额外ID；新run完成训练/dev smoke。当前状态为`AUTHOR_ORIGINAL_PATH_SMOKE_EXECUTABLE_FULL_REPRODUCTION_BLOCKED_COMPUTE`。

## 3. 当前允许与禁止表述

允许：

- 作者原设定路径已在固定作者fork和锁定环境中完成输入隔离后的本地GPU smoke；
- smoke只证明可执行性和资源估算；
- 全量复现因租用A30不可达和本地预计耗时过长尚未启动；
- 作者原任务读取目标评论并使用comment split，属于NON_T0。

禁止：

- “VC-CSA作者代码当前缺失”；
- “已完成VC-CSA全量/官方main/T0复现”；
- 把smoke指标写入冻结baseline表或论文结论；
- 把“入口未迭代test”混写为旧runtime“物理不含test记录”。

## 4. 不变边界

- `G3=PASS_WITH_LIMITATIONS`不变；
- temporal-attention仍为`REIMPLEMENTATION_STRONG_BASELINE`；
- T0适配必须另建`REIMPLEMENTATION`实验；
- I3D许可、官方revision、权利方包身份/fixity仍未知，`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`不变；
- 权利否认或8210 hash/覆盖漂移仍触发`ASSET_INVALIDATED_DO_NOT_REPORT`；
- 本勘误不包含或再分发作者评论、I3D `.npy`、权重、预测或本机路径。
