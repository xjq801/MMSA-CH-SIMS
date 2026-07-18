---
session_no: S09
contract_version: 2
suggested_title: "[T-AFFC] S10 复核VC-CSA泄漏接受型探索合同"
parent_session: S08
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-18
---

# S09 VC-CSA泄漏风险接受型探索授权交接卡

## 当前状态

- `SC-20260718-04`已裁定：用户接受跨split peer泄漏仅用于隔离探索。
- 唯一实验身份是`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`。
- `FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`；不得进入T0、统一baseline、G3主证据、任务50、论文主表或泛化/无泄漏claim。
- `REMOTE_I3D_TRANSFER_AUTHORIZATION=APPROVED_IN_PRINCIPLE_FOR_THIS_INSTANCE_AND_THIS_EXPLORATORY_RUN_ONLY`。
- `EFFECTIVE_I3D_TRANSFER_PERMISSION=PENDING_EXPLORATORY_CONTRACT_HASH_REVIEW`；任务20在新合同精确hash获00接受前必须保持真实I3D 0上传、0真实训练。
- 旧NO_TRANSFER合同SHA-256=`5dbf891d1fcd6307ee19f98dc46c8e3f7c35a712c167a5b258c4c10b79d28d3c`仅为历史证据，不得原地改写。
- formal/clean路径的`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`仍成立；用户风险接受不等于泄漏消失。
- I3D许可、官方revision、权利方包身份/fixity继续UNKNOWN；权利方否认、8210 hash/覆盖或实例绑定漂移仍触发`ASSET_INVALIDATED_DO_NOT_REPORT`。
- `G3=PASS_WITH_LIMITATIONS`、temporal-attention=`REIMPLEMENTATION_STRONG_BASELINE`、任务50未完成、任务30冻结均不变。

## 下一步硬门

1. 任务20应新建其所有权的独立探索合同，明确NON_T0、泄漏披露、单种子诊断、正式证据禁入、8210严格集合、实例三元绑定、传输/权限/删除和止损条款。
2. 00只读复核合同及工作区，计算并记录精确SHA-256；合同未接受前不得传输第一字节。
3. 若合同通过，00另行把有效权限改为`APPROVED_FOR_BOUND_EXPLORATORY_CONTRACT`；任务20才可按合同执行。
4. 结果必须显式披露train可读取dev/test peer评论与标签，dev/test指标受污染；不得做正式比较或claim升级。
5. 不创建任务30或任何IJCV任务，不与任务20并发修改实验核心。

## 接续提示词

你是新的“00-T-AFFC总控”，接替S09。先读取`AGENTS.md`、`WORK_RECORD_POLICY.md`、`WORK_LOG.md`末条、总纲v1.16、`TASK00_VCCSA_LEAKAGE_ACCEPTED_EXPLORATORY_AUTHORIZATION_20260718.md`、`TASK00_TASK20_PEER_BLOCKER_SUBMISSION_ACCEPTANCE_20260718.md`、任务20旧NO_TRANSFER合同、`.light/decision_log.md`和本卡，并刷新`origin/main`与任务20实时状态。当前用户已明确接受跨split peer泄漏，但仅授权身份`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`的隔离探索；正式证据资格永久为INELIGIBLE。当前实例8210项I3D临时传输仅原则批准，`EFFECTIVE_I3D_TRANSFER_PERMISSION=PENDING_EXPLORATORY_CONTRACT_HASH_REVIEW`，任务20必须先提交新的独立探索合同供00绑定精确SHA-256，合同接受前保持0上传/0真实训练。旧NO_TRANSFER合同hash `5dbf891d...28d3c`不得改写。继续传播G3=PASS_WITH_LIMITATIONS、任务50未完成、I3D许可/revision/权利方身份/fixity UNKNOWN及资产止损条件。项目只执行T-AFFC CARM，不创建IJCV J0—J2、JH1—JH3、任务25或65，不得在未过门时创建任务30。每次会话收尾继续新建下一张`.light/handoff/S<NN>-*.md`并打印接续提示词。
