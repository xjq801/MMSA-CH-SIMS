---
session_no: S13
contract_version: 2
suggested_title: "[T-AFFC] S14 监督任务20存储、训练与删除证据"
parent_session: S12
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-19
---

# S13 任务20受限存储与镜像补充授权交接卡

## 当前状态

- `SC-20260719-02`已批准受限存储补充，旧NO_TRANSFER/探索合同历史字节不改写。
- `RESTRICTED_STORAGE_SUPPLEMENT=APPROVED_EXECUTABLE`；用户接受私有MatBox、私有对象存储、私有环境/卷快照和配置镜像的残余平台控制面风险。
- 允许区域为逻辑前缀`matbox-private/task20-vccsa-exploratory-20260719/`、`object-private/task20-vccsa-exploratory-20260719/`、`snapshot-private/task20-vccsa-exploratory-20260719-*`和`config-mirror/task20-vccsa-exploratory-20260719/`。
- 任务20可直接创建和使用私有区域，绑定每个实际目标的非秘密digest/ACL/加密摘要，核验固定8210项后备份、快照、恢复或继续当前A30 `seed=3407`探索训练。
- 受限I3D/运行材料保留至最小证据验收后30日；非敏感配置镜像可保留至项目归档。删除记录只证明可见层，平台控制面仍UNKNOWN。
- Git仍不得承载I3D、评论正文、标签明细、权重、逐样本预测、凭据或端点原文。
- 实验身份永久NON_T0/INELIGIBLE；G3限制、任务50未完成、任务30冻结和I3D未知项不变。

## 监督边界

1. 每个实际MatBox/object/snapshot目标必须有私有目标digest、区域类别、ACL摘要、加密状态、对象计数和前后fixity非秘密记录。
2. I3D严格为8210项；missing/extra/size/hash mismatch任一非空不得称fixity一致。
3. 可自主备份、恢复、排障和继续训练；00不再逐步卡签，但需监督失败、快照/恢复与删除证据。
4. 配置镜像不得含凭据、端点原文或可逆受限内容；运行快照可含受限材料但仅限私有区域和30日策略。
5. 不创建任务30、任务50执行或IJCV任务，不将结果升级为正式证据。

## 接续提示词

你是新的“00-T-AFFC总控”，接替S13。先读取`AGENTS.md`、`WORK_RECORD_POLICY.md`、`WORK_LOG.md`末条、总纲v1.16、`TASK00_VCCSA_RESTRICTED_STORAGE_AND_IMAGE_SUPPLEMENT_AUTHORIZATION_20260719.md`、探索合同hash验收单、完整执行授权、任务20探索合同、`.light/decision_log.md`和本卡，并刷新`origin/main`与任务20实时状态。当前用户已授权固定8210项I3D及运行环境进入私有MatBox、私有对象存储、私有快照和配置镜像；旧合同历史字节不改写。任务20可直接备份、恢复和继续A30 seed=3407训练，绑定每个实际目标的非秘密digest/ACL/加密摘要并记录前后fixity。受限材料保留至最小证据验收后30日，配置镜像仅在非敏感时可长期保留；删除只证明可见层。实验永久NON_T0/INELIGIBLE，不得进入T0/G3/统一baseline/任务50/论文claim。继续传播I3D许可/revision/权利方身份/fixity UNKNOWN和资产止损。项目只执行T-AFFC CARM，不创建IJCV J0—J2、JH1—JH3、任务25或65，不得创建任务30。每次会话收尾继续新建下一张`.light/handoff/S<NN>-*.md`并打印接续提示词。
