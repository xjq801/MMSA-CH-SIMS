# 00对任务20 VC-CSA peer阻断提交的独立验收

> 日期：2026-07-18  
> 审查提交：`baaac078add841bb40fa6be1b44fa202c60f6e2b`  
> 父状态：`c7edb5499a908541ae24646e76ca03f0b4472274`

## 裁定

`TASK20_PEER_BLOCKER_SUBMISSION=ACCEPTED`

`AUTHOR_ORIGINAL_FULL_REPRODUCTION=LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`

`EFFECTIVE_I3D_TRANSFER_PERMISSION=BLOCKED_DO_NOT_TRANSFER`

本验收接受任务20对结构性阻断的代码化、测试化和审计化提交，不把该状态写成作者全量复现成功、远端运行成功、T0复现或I3D资产许可闭合。

## 提交范围

`baaac078`相对父提交严格包含五项：

1. `TASK20_REMOTE_A6000_I3D_STAGING_EXECUTION_CONTRACT_20260718.md`；
2. `TASK20_BASELINE_EXECUTION_AUDIT.md`；
3. `scripts/prepare_vccsa_author_reproduction.py`；
4. `tests/test_vccsa_author_reproduction.py`；
5. `WORK_LOG.md`中的`WR-20260718-028`。

提交未修改00裁定、S07、总纲、G门、冻结G3 package/HANDOFF、T0协议或任务50状态。

## 00独立验证

- Git：`HEAD=origin/main=baaac078add841bb40fa6be1b44fa202c60f6e2b`，工作区clean，任务20线程idle。
- 合同：SHA-256=`5dbf891d1fcd6307ee19f98dc46c8e3f7c35a712c167a5b258c4c10b79d28d3c`，120行，状态`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY_NO_TRANSFER`。
- `git diff --check c7edb54..baaac078`：exit 0。
- `.venv-task20`全量unittest：67/67通过，exit 0。
- 真实`audit_peer_isolation()`：跨split视频7,854；train/dev/test singleton和cross-split-only peer均为122/2,750/1,573；三split`no_global_peer_ids=0`；报告不含comment IDs/text；exit 0。
- 默认`.venv`：`validate_work_log.py`为118条、latest=`WR-20260718-028`、`passed=true`；`run_preparation_checks.py` exit 0、`blocking_checks=[]`，同时如实保留`faiss_available=false`、`formal_model_work_ready=false`。
- 正式`.venv-task20`：`run_preparation_checks.py` exit 0、`blocking_checks=[]`、`faiss_available=true`、`formal_model_work_ready=true`。
- `validate_task20_handoff.py`：22项冻结证据通过、`restricted_assets_required=false`；G3冻结handoff字节未漂移。

## 影响与边界

任务20已把“作者完整comment split无法同时满足faithful peer采样与物理无泄漏”固化为可重复fail-closed门。此前peer-safe 8 train/4 dev smoke仍只证明筛选子集入口可执行，不能支持完整作者split复现。

用户对当前A6000实例残余风险的接受仍是历史事实，但本实验的数据/泄漏门更早失败，因此真实I3D保持0上传，远端未连接，真实smoke和全量训练均不得启动。增加算力不能解除该阻断。

任何删除singleton、self-peer、固定/合成peer、取消peer分支、允许跨split peer或视频级重分割都会改变作者合同，只能另建`REIMPLEMENTATION_NON_FAITHFUL_PEER_ADAPTATION`；须重新预注册和单独申请00审批，不得继承faithful作者复现或当前资产传输资格。

`G3=PASS_WITH_LIMITATIONS`、temporal-attention的`REIMPLEMENTATION_STRONG_BASELINE`、任务50未完成及I3D许可/revision/权利方fixity UNKNOWN均不变。

## 结论

任务20本轮可按“faithful作者全量复现因结构性peer泄漏冲突止损，NO_TRANSFER证据已接受”收尾。若用户不另行授权非faithful REIMPLEMENTATION，则无需继续为该路径占用租用GPU。

