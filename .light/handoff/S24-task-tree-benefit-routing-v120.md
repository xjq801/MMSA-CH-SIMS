---
session_no: S24
contract_version: 2
suggested_title: "[T-AFFC] S25 close Task20 resume blocker and freeze H1/H2 preregistration"
parent_session: S23
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-27
---

# S24 Task-tree benefit-aware routing amendment and v1.20 handoff

## 当前阶段

- 当前SSOT为`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.20，第17节规格为v1.4；本版把收益感知历史反应路由落实为任务40/50执行合同。
- G1=`PASS`、`G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`、`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`、G3=`PASS_WITH_LIMITATIONS`；Task30仍未创建。
- Task20正式核心已完成。NON_T0探索有3个完整epoch和Epoch 4 step 220精确恢复锚；2026-07-27新4090位于13区，I3D已复核、环境恢复中，但精确断点仍在亚太2区，跨区复制与SHA-256闭合前不得训练。

## 已完成

- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md`第17节任务40 — 新增train内部cross-fitting/out-of-fold效用标签、T0-only路由输入、效用manifest、强路由对照、coverage匹配、负迁移机制链与止损；验证：`scripts/validate_taffc_v120_task_tree.py`输出`passed=true`。
- 同文件第17节任务50 — 新增content-only/memory/router/强基线同一五种子、效用与负迁移paired bootstrap、success/failure/inconclusive分支；验证：v1.20专项validator检查13个master contract令牌且`errors=[]`。
- `CONTRIBUTION_PRIOR_ART_MATRIX.md`、`CLAIM_EVIDENCE_MATRIX.md`、`RISK_REGISTER.md`、`TASK_REGISTRY.md`、`TAFFC_PAPER_INNOVATION_AND_EXPERIMENT_TARGETS_20260723.md`与`.light/*` — 已同步收益感知机制、强对照、证据边界和当前Task20跨区断点阻塞；验证：专项validator检查7个活动文件且`errors=[]`。
- `scripts/validate_literature_freeze.py` — 文献冻结合同升级为`FROZEN_v4`并要求OOF效用与coverage匹配；验证：专项结果`passed=true`、documents=6、queries=4、identified=500。
- v1.20明确不恢复v1.17的3%/5%/8%硬效应门，不改变G1—G3、Task20评测核心、I3D风险或Task30创建状态；验证：v1.20专项validator同时检查“不恢复”令牌和Task20段无`收益感知`扩写，`errors=[]`。

## 工作区状态

- 本批开始时共享主仓库`main=origin/main=67aa0ff`，tracked clean，仅Task20所有的`tmp/`未跟踪。
- 造卡时00的v1.20文档、台账、validator、工作日志与本卡待有意提交；`tmp/`未读取、未暂存。
- Task20已收到00文档所有权暂停并确认不写`WORK_LOG.md`/SSOT；远端预检继续，不与本批修改实验核心冲突。
- 一次递归PowerShell文本扫描因遍历过宽长期无新增输出；核对命令行后仅终止对应只读进程，后续使用定向文件列表，未改文件。
- `light-memory-pm pm.py`既知缺`_shared/passport`未重试；使用底层passport重算state hash，validate仅保留历史stage10缺内部hash/timestamp的WARN。

## 待用户回答

- none — 用户已授权“适度改进完善第17节”；本版只把已认可的收益感知创新判断变成非数值执行合同，没有新增付费、数据、远程训练或投稿授权。

## 核心决策

1. 第17节原有Video2Reaction强基线、teacher/memory/router/rejection消融、五种子、bootstrap和严格OOD条款保留。
2. C2后半的候选方法核心收紧为：只用train内部OOF效用标签学习“检索相对content-only是否有益”，推理只读T0查询和邻居诊断。
3. router必须与固定融合、相似度阈值、预测熵阈值和SelectiveNet式拒绝公平比较，选择性比较匹配coverage或风险预算。
4. 平均指标提升不足以证明router；必须报告效用识别、负迁移率、被避免负迁移、AURC/risk-coverage及OOD/污染机制链。
5. 若机制链失败，删除收益感知/完整检索创新claim；不以新模块或撤回过的数值硬门补救。

## 阻塞/风险

- Task20续训当前被精确断点跨区不可见阻塞；必须取得SHA-256=`f51e249890e2320995fe6513562010982171c3d7c16b7a1c08a008d7e1bea632`的文件，不能用Epoch 3 best模型冒充。
- Task20探索与受限存储生命周期仍未闭环，继续阻止Task30创建。
- 收益感知router仍是`TO_VERIFY`；文档合同通过不等于方法有效或可发表。
- I3D许可、稳定revision和权利方包身份/fixity仍为UNKNOWN；资产止损条件不变。

## 必读文件

- `.light/handoff/S24-task-tree-benefit-routing-v120.md`
- `.light/passport.yaml`
- `.light/project_card.md`
- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.20，尤其第17节任务40/50
- `CONTRIBUTION_PRIOR_ART_MATRIX.md`
- `CLAIM_EVIDENCE_MATRIX.md`
- `RISK_REGISTER.md`
- `TASK_REGISTRY.md`
- 最新`WORK_LOG.md`与Task20实时线程

## 下一步

- 读取Task20实时线程并核验跨区断点复制、SHA-256和续训状态；不得把环境恢复或best模型写成精确续训已开始。
- 生成H1/H2 target chain、实验矩阵、failure tree和公平baseline预算，但仅在Task20共享核心与存储生命周期闭环后提交00复核，不提前创建Task30。
- 验收v1.20前置条件并由00另行裁定Task30；若收益感知效用标签不可无泄漏构造，则回退普通融合并降低claim。

## 禁止

- 本卡不是当前事实；接手时必须先运行`git status --short --branch`、`git log`并刷新Task20线程。
- 不得把v1.20文本门通过写成收益感知router已有效、论文已可发表或G4已通过。
- 不得恢复v1.17的3%/5%/8%硬门，不得根据test选择效用、阈值、coverage或路由对照。
- 不得在Task20未闭环时创建Task30或并发修改共享实验核心。
- 不得用Epoch 3 best模型替代精确续训断点，不得触碰或提交Task20所有的`tmp/`。

## Continuation prompt

You are the 00-T-AFFC total controller taking over S24. Read AGENTS.md and perform startup checks, then read S24, passport, project_card, master plan v1.20 section 17 tasks 40/50, CONTRIBUTION_PRIOR_ART_MATRIX.md, CLAIM_EVIDENCE_MATRIX.md, RISK_REGISTER.md, TASK_REGISTRY.md and the latest WORK_LOG. Refresh origin/main, git status/log and the live Task20 thread; this handoff is not current fact. Keep G1 PASS, G2 protocol/data PASS_WITH_LIMITATIONS, asset admissibility DEFERRED_ACCEPTED_RISK and G3 PASS_WITH_LIMITATIONS. Treat Video2Reaction as the closest/direct prior and benefit-aware routing as TO_VERIFY. The router contract requires train-only cross-fitted/OOF utility labels, T0-only inference inputs, fair fixed-fusion/similarity/entropy/SelectiveNet-style controls, matched coverage, five-seed formal confirmation, native-unit paired bootstrap, negative-transfer and OOD evidence, with explicit failure/inconclusive branches. Do not restore the withdrawn 3%/5%/8% hard thresholds. First refresh whether the exact Epoch 4 step 220 checkpoint has been copied from AP2 to region 13 and SHA-256 verified; do not accept an Epoch 3 best model as a resume checkpoint. Close Task20 and its restricted-storage lifecycle before authorizing Task30. Do not touch tmp/. At session close create S25 and print the next continuation prompt.
