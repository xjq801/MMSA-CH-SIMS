---
session_no: S10
contract_version: 2
suggested_title: "[T-AFFC] S11 监督VC-CSA隔离探索执行与删除核验"
parent_session: S09
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-18
---

# S10 VC-CSA泄漏接受型探索合同hash验收交接卡

## 当前状态

- 任务20提交`4ebcb260dfccf357e9cfb9c7a92c9d348a1b28d9`已由00独立验收。
- 接受合同：`TASK20_VCCSA_LEAKAGE_ACCEPTED_EXPLORATORY_EXECUTION_CONTRACT_20260718.md`。
- 精确SHA-256=`77b0a93003d265aae6215caca3ef53fbef4624bd24cf3dfabf46df3978cdaed4`；当前文件物理行数为100，不是任务20回传的48。
- `EFFECTIVE_I3D_TRANSFER_PERMISSION=APPROVED_FOR_BOUND_EXPLORATORY_CONTRACT`。
- 唯一身份：`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`；`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`。
- 任务20可按合同依次执行实例三元绑定、固定8210传前fixity、SFTP暂存、远端fixity、一次seed=3407诊断和删除核验。
- 本批准不等于传输或训练已发生；验收时真实I3D仍0上传、真实训练0次。
- 旧NO_TRANSFER合同保持历史不变；新合同字节或任何实例/资产绑定漂移都会使批准失效。
- I3D许可、官方revision、权利方包身份/fixity继续UNKNOWN；`ASSET_INVALIDATED_DO_NOT_REPORT`止损不变。
- `G3=PASS_WITH_LIMITATIONS`、任务50未完成、任务30冻结、T-AFFC CARM单路线不变。

## 监督硬门

1. 先验证SSH host-key SHA-256、GPU UUID和endpoint digest三元绑定；失败即不传输。
2. 传前和传后都必须恰好8210项且missing/extra/size/hash mismatch全空；失败即删除并止损。
3. 只允许一次seed=3407工程诊断，不允许新增种子、调参、bootstrap或选择性重跑。
4. 结果只作受污染探索诊断，不进入T0/G3/统一baseline/任务50/论文claim，不做正式排名。
5. 任务结束或任一失败后，必须核验受限根目录、I3D、runtime、权重、预测、缓存和相关进程均按合同清除。
6. 不创建任务30或IJCV任务，不并发修改任务20实验核心。

## 接续提示词

你是新的“00-T-AFFC总控”，接替S10。先读取`AGENTS.md`、`WORK_RECORD_POLICY.md`、`WORK_LOG.md`末条、总纲v1.16、`TASK00_VCCSA_EXPLORATORY_CONTRACT_HASH_ACCEPTANCE_20260718.md`、`TASK00_VCCSA_LEAKAGE_ACCEPTED_EXPLORATORY_AUTHORIZATION_20260718.md`、任务20新探索合同、旧NO_TRANSFER合同、`.light/decision_log.md`和本卡，并刷新`origin/main`与任务20实时状态。当前获接受合同SHA-256为`77b0a93003d265aae6215caca3ef53fbef4624bd24cf3dfabf46df3978cdaed4`、物理100行；`EFFECTIVE_I3D_TRANSFER_PERMISSION=APPROVED_FOR_BOUND_EXPLORATORY_CONTRACT`。任务20只可按顺序执行实例三元绑定、固定8210传前fixity、SFTP、远端fixity、一次seed=3407诊断和删除核验；任一漂移立即停止。实验身份永久为`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`且正式证据资格INELIGIBLE，不得进入T0、G3、统一baseline、任务50或论文claim。继续传播I3D许可/revision/权利方身份/fixity UNKNOWN和`ASSET_INVALIDATED_DO_NOT_REPORT`止损。项目只执行T-AFFC CARM，不创建IJCV J0—J2、JH1—JH3、任务25或65，不得创建任务30。每次会话收尾继续新建下一张`.light/handoff/S<NN>-*.md`并打印接续提示词。
