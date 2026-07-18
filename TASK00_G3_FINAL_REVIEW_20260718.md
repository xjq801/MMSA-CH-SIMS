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

1. temporal-attention只能标为`REIMPLEMENTATION_STRONG_BASELINE`，不能标为VC-CSA官方复现。后续证据已定位作者释放实现：`JackySnake/MSA-CRVI@3e8c42608f4e89bc2082c55760aa63535e8e276a`是`IEIT-AGI/MSA-CRVI`的fork，并对应上游仍open、未合并的PR #3 `add source code`；因此当前状态更正为`AUTHOR_RELEASED_IMPLEMENTATION_LOCATED_PR3_OPEN_NOT_YET_REPRODUCED`。上游官方`main@99d1424`在原审计时无源代码只作为历史事实保留，不再表述为当前“作者代码缺失”。
2. 已定位实现尚未构成官方复现成功：静态`compileall`通过，但`main.py --help`与`main_eval.py --help`均在CUDA前因未声明的`en_vectors_web_lg`依赖退出，`train.sh`另有变量名与续行问题，本轮未运行GPU。原实现读取目标评论、采用随机comment split并预测评论级opinion/emotion，与T0禁用目标评论及`group_by_video_v1`视频级分布任务不匹配；不能直接进入T0统一主表。若后续执行，faithful作者任务复现与T0适配重实现必须分开配置、命名和报告。
3. 当前正式数值是单seed证据；五种子、正式bootstrap和paired comparison属于任务50，状态为`TASK50_NOT_COMPLETED`。
4. I3D许可、官方revision、权利方包身份/fixity仍未知；`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`不变。禁止提交、发布或再分发I3D特征、模型权重、预测、run bundle、本机路径或可逆受限资产。
5. 若权利方否认研究使用，或8210 hash/覆盖漂移，立即标记`ASSET_INVALIDATED_DO_NOT_REPORT`并停止依赖该资产的正式结果。
6. 任务30现在可按总纲启动条件进入后续流程，但必须读取本交接、manifest和冻结协议；不得修改任务20冻结评测器、split、class order或test规则。

## 00结论

接受任务20 G3证据，状态为`PASS_WITH_LIMITATIONS`；作者实现定位只更正证据身份和限制措辞，不使既有强基线依据失效，也不把该结论扩展为VC-CSA官方复现、最终论文优越性、跨硬件bitwise复现或任务50完成。
