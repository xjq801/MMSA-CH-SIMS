---
session_no: S12
contract_version: 2
suggested_title: "[T-AFFC] S13 监督任务20新实例完整探索执行"
parent_session: S11
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-19
---

# S12 任务20新实例完整探索执行授权交接卡

## 当前状态

- 用户明确要求以跑完任务20实验为核心，并授权任务20为完成探索诊断执行所需请求。
- `TASK20_OPERATIONAL_REQUEST_AUTHORITY=APPROVED_WITHIN_TASK20_EXPLORATORY_SCOPE`。
- 当前目标endpoint digest=`4af92a8622db78ce968bdb49b98f06ef26d4151a943c885ad03de5548eb32cdc`；端点原文和凭据不得入Git/日志。
- 任务20可完成三元绑定后直接执行8210 fixity→SFTP→远端fixity→唯一seed=3407→最小证据→删除核验，无需00二次签字。
- 当前实例失败时，任务20可自主排障、工程重试或切换替代实例；每个实际实例仍须先完成新的非秘密三元绑定。
- 用户扩权取消额外审批门，不取消凭据保护、8210严格集合、失败实录、删除要求或结果身份边界。
- 实验永久`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`且`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`。
- G3限制、任务50未完成、任务30冻结、I3D UNKNOWN项与资产止损均不变。

## 监督边界

1. 00持续监督而不逐步卡签；任务20可自主完成本次探索所需环境、传输、训练和清理。
2. 三元绑定、8210前后fixity、单完成seed=3407和删除核验仍须留下非秘密证据；失败不得删除。
3. 可做工程故障重试，不得基于dev/test指标选择性调参、挑结果或扩成多种子。
4. 凭据、端点原文、I3D、评论正文、标签明细、权重和逐样本预测不得进入Git或公开材料。
5. 不创建任务30、任务50执行或IJCV任务，不并发修改正式T0实验核心。

## 接续提示词

你是新的“00-T-AFFC总控”，接替S12。先读取`AGENTS.md`、`WORK_RECORD_POLICY.md`、`WORK_LOG.md`末条、总纲v1.16、`TASK00_VCCSA_NEW_INSTANCE_FULL_EXECUTION_AUTHORIZATION_20260719.md`、S11失败验收、探索合同hash验收单、任务20探索合同、`.light/decision_log.md`和本卡，并刷新`origin/main`与任务20实时状态。用户已把核心优先级设为跑完任务20探索诊断；任务20对endpoint digest `4af92a8622db78ce968bdb49b98f06ef26d4151a943c885ad03de5548eb32cdc`完成三元绑定后可直接执行8210 fixity、SFTP、远端fixity、唯一seed=3407、最小证据和删除核验，无需00逐步签字；实例失败可自主排障或换实例重绑定。00只监督证据和范围，不制造额外审批等待。端点原文/凭据不入Git，冻结8210不公开，失败与清理如实记录。实验永久NON_T0、正式证据资格INELIGIBLE，不得进入T0/G3/统一baseline/任务50/论文claim。继续传播I3D许可/revision/权利方身份/fixity UNKNOWN。项目只执行T-AFFC CARM，不创建IJCV J0—J2、JH1—JH3、任务25或65，不创建任务30。每次会话收尾继续新建下一张`.light/handoff/S<NN>-*.md`并打印接续提示词。
