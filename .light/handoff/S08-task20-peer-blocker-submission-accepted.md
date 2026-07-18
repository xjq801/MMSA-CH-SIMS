---
session_no: S08
contract_version: 2
suggested_title: "[T-AFFC] S09 监督任务树与非faithful替代方案边界"
parent_session: S07
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-18
---

# S08 任务20 peer阻断提交验收交接卡

## 当前状态

- 主仓库与远端审查锚点：`main@baaac078add841bb40fa6be1b44fa202c60f6e2b`；审查前工作区clean。
- `TASK20_PEER_BLOCKER_SUBMISSION=ACCEPTED`。
- `AUTHOR_ORIGINAL_FULL_REPRODUCTION=LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`。
- `EFFECTIVE_I3D_TRANSFER_PERMISSION=BLOCKED_DO_NOT_TRANSFER`；真实I3D 0上传，未连接远端、未启动真实smoke或全量训练。
- 最终合同SHA-256=`5dbf891d1fcd6307ee19f98dc46c8e3f7c35a712c167a5b258c4c10b79d28d3c`，120行。
- 00独立复跑67/67；真实聚合为7,854个跨split视频，train/dev/test singleton与cross-split-only peer均122/2,750/1,573，`no_global_peer=0`。
- 默认`.venv`仍为faiss缺失/`formal_model_work_ready=false`；正式`.venv-task20`为faiss可用/`formal_model_work_ready=true`。二者不得混写。
- G3仍`PASS_WITH_LIMITATIONS`；temporal-attention仍为`REIMPLEMENTATION_STRONG_BASELINE`；任务50未完成。
- I3D许可、官方revision、权利方包身份/fixity继续UNKNOWN；权利否认或8210 hash/覆盖漂移仍触发`ASSET_INVALIDATED_DO_NOT_REPORT`。

## 监督边界

1. faithful作者全量路径以结构性peer泄漏阻断收尾，不得因A6000可用或用户曾接受实例风险而恢复传输/训练。
2. 任何peer适配只能另建`REIMPLEMENTATION_NON_FAITHFUL_PEER_ADAPTATION`，独立冻结estimand、split、peer规则、对照、claim和资产边界，并重新申请00审批。
3. peer适配不得进入作者faithful复现列，不得自动进入T0统一主表，也不得回写G3冻结证据包。
4. 本验收不创建任务30或任何新任务；用户若明确要求创建Codex任务，再按总纲和当前任务树处理。
5. 不创建或执行IJCV J0—J2、JH1—JH3、任务25或65，不并发修改实验核心。
6. `light-consistency`仍只有PARTIAL回扫，不能冒充完整一致性门。

## 接续提示词

你是新的“00-T-AFFC总控”，接替S08。先读取`AGENTS.md`、`WORK_RECORD_POLICY.md`、`WORK_LOG.md`末条、总纲v1.16、`TASK00_TASK20_PEER_BLOCKER_SUBMISSION_ACCEPTANCE_20260718.md`、`TASK00_VCCSA_AUTHOR_PEER_ISOLATION_REVIEW_20260718.md`、任务20最终NO_TRANSFER合同、`TASK20_BASELINE_EXECUTION_AUDIT.md`和本卡，并刷新`origin/main`与任务20实时状态。当前任务20提交`baaac078`已由00独立验收；faithful作者全量路径因同video peer与随机comment split的结构性冲突被`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`阻断，真实I3D 0上传且`EFFECTIVE_I3D_TRANSFER_PERMISSION=BLOCKED_DO_NOT_TRANSFER`。任何peer改法只能另建`REIMPLEMENTATION_NON_FAITHFUL_PEER_ADAPTATION`并重新预注册/审批，不得冒充faithful或自动进入T0主表。继续传播G3=PASS_WITH_LIMITATIONS、任务50未完成、I3D许可/revision/权利方fixity UNKNOWN及止损条件。项目只执行T-AFFC CARM，不得创建IJCV任务。每次会话收尾继续新建下一张`.light/handoff/S<NN>-*.md`并打印接续提示词。
