# 00独立G3最终审查

## 裁定

`G3=PASS_WITH_LIMITATIONS`

本裁定由00总控基于远端提交`e49ef9e57cac2b072d638811e68b621ec254e6d2`独立作出，不是任务20自批。

## 核验结果

- 主仓库：`main`与`origin/main`均为`e49ef9e57cac2b072d638811e68b621ec254e6d2`，审查前工作区clean。
- `scripts/validate_task20_handoff.py`：exit 0，`passed=true`，`tracked_evidence_checked=22`，`restricted_assets_required=false`。
- `HANDOFF_20.md` SHA-256：`5a503d90308781620b4e4a7c99b409e29f30cd0872fc6f8b51da6c580a9b56cb`。
- `data/manifests/task20-handoff-v1.manifest.json` SHA-256：`6d75e2190a50dc4a2191458d6d379a7d49a84f630d5ccf3eb27ac83294f96e91`。
- 证据快照绑定：`b89d8dc1d62b5d6ea7b07b1d30cc8f19224c030d`；提交状态绑定：`aed141b78b0babe4bad10555f335587f983f479b`。
- `.venv-task20` 全量测试：60/60通过；`validate_work_log.py`通过；`run_preparation_checks.py`为`blocking_checks=[]`、`formal_model_work_ready=true`；compileall通过。

## G3依据与限制

任务20满足总纲G3/L2的最低证据条件：统一`group_by_video_v1` split、统一输入/评测器、冻结调参预算、train-only拟合、dev选择、test一次性评估、无泄漏合同，以及至少一个可审计的强视觉重实现和同环境同seed dev replay。

限制必须继续传播：

1. temporal-attention只能标为`REIMPLEMENTATION_STRONG_BASELINE`，不能标为VC-CSA官方复现；VC-CSA保持`FAILED_OFFICIAL_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH`。
2. 当前正式数值是单seed证据；五种子、正式bootstrap和paired comparison属于任务50，状态为`TASK50_NOT_COMPLETED`。
3. I3D许可、官方revision、权利方包身份/fixity仍未知；`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`不变。禁止提交、发布或再分发I3D特征、模型权重、预测、run bundle、本机路径或可逆受限资产。
4. 若权利方否认研究使用，或8210 hash/覆盖漂移，立即标记`ASSET_INVALIDATED_DO_NOT_REPORT`并停止依赖该资产的正式结果。
5. 任务30现在可按总纲启动条件进入后续流程，但必须读取本交接、manifest和冻结协议；不得修改任务20冻结评测器、split、class order或test规则。

## 00结论

接受任务20 G3证据，状态为`PASS_WITH_LIMITATIONS`；不把该结论扩展为最终论文优越性、官方复现、跨硬件bitwise复现或任务50完成。
