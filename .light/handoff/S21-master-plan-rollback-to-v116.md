---
session_no: S21
contract_version: 2
suggested_title: "[T-AFFC] S22 close Task20 under restored master plan v1.16"
parent_session: S20
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-23
---

# S21 master plan rollback to v1.16 handoff

## 当前阶段

- 用户已撤回v1.17活动总纲，当前SSOT恢复为`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.16；项目仍处于Task20探索收尾，Task30未创建。

## 已完成

- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` — 验证：正文已恢复为`d45338e`中的v1.16字节版本。
- `AGENTS.md`、`.light/terminology.md`、`CLAIM_EVIDENCE_MATRIX.md`、`TAFFC_PAPER_INNOVATION_AND_EXPERIMENT_TARGETS_20260723.md` — 验证：活动版本与主张边界恢复到v1.16；详细创新档案重新标为非权威建议。
- `.light/decision_log.md`与`.light/version_history.md` — 验证：保留v1.17历史并追加用户撤回记录，没有删除既有决策。
- `.light/project_card.md`、`TASK_REGISTRY.md`与`RISK_REGISTER.md` — 验证：保留当前G门和Task20事实，同时把活动SSOT改回v1.16。
- Task20实时任务 — 验证：统一基线/G3主体已完成；VC-CSA全量探索、运行时快照和受限存储生命周期仍未闭环，远端SSH状态最近不可用。

## 工作区状态

- 回退前`HEAD=origin/main=47e9338cdf06f120f99e819f74ef19f1aa9eda3d`；用户回退动作形成11项精确逆向改动，总纲正文尚未回退，另有Task20所有的`tmp/`。
- 本批采用审计式回退：补齐v1.16正文，保留WORK_LOG、S20和TASK_REGISTRY的历史连续性，并新增本卡；最终提交与推送状态须先刷新Git。
- 当前worktree为`dirty/unpushed`，提交前工作日志门与diff检查已通过；S21合同和准备检查以本批最终复跑结果为准。
- `tmp/`未被00读取、暂存、移动或删除。

## 待用户回答

- none — 用户已明确选择恢复上一步总纲v1.16；未授权或执行实验、付费、远程存储、投稿或删除动作。

## 核心决策

1. 活动SSOT为v1.16；v1.17不再约束任务30—60。
2. 收益感知可靠性路由、3%/5%/8%效应门与新增Pareto门只保留在历史Git和建议档案，不得写成当前预注册要求。
3. 回退不撤销G1、G2、G3、formal split、I3D资产风险或Task20的NON_T0/INELIGIBLE边界。
4. WORK_LOG与handoff只追加；不得为“看起来像没发生过”而删除v1.17历史。

## 阻塞/风险

- Task20 VC-CSA探索、运行时快照和受限存储生命周期未闭环，继续阻止Task30创建。
- `.light/passport.yaml`仍是陈旧PLANNED账本且无inputs fingerprint；本批未迁移或伪造其状态。
- I3D许可、稳定revision和权利方包身份/fixity继续UNKNOWN；资产止损条件不变。
- 若未来重新采用v1.17候选机制或数值门，必须由用户重新批准并在查看test前完成预注册。

## 必读文件

- `.light/handoff/S21-master-plan-rollback-to-v116.md`
- `.light/passport.yaml`
- `.light/project_card.md`
- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.16
- `TASK_REGISTRY.md`
- `TASK00_G3_FINAL_REVIEW_20260718.md`
- `RISK_REGISTER.md`
- 最新`WORK_LOG.md`与Task20实时任务

## 下一步

- 读取Task20实时状态，要求其形成训练完成、失败或不可用收尾以及快照/受限存储生命周期证据。
- 检查共享实验核心停止修改后，严格按v1.16复核Task30创建条件。
- 编写Task30创建前的H1目标链、公平对照、校准边界、错配评论负对照和失败降级路径。

## 禁止

- 不得把本卡当作当前事实；必须先运行`git status --short --branch`和`git log`并刷新Task20。
- 不得把v1.17的收益感知路由、3%/5%/8%或新增Pareto门当作当前SSOT要求。
- 不得在Task20未闭环时创建Task30或并发修改共享实验核心。
- 不得删除v1.17历史决策、WORK_LOG或S20交接卡。
- 不得改变I3D风险、NON_T0/INELIGIBLE边界或触碰Task20所有的`tmp/`。

## Continuation prompt

You are the 00-T-AFFC total controller taking over S21. Read AGENTS.md and perform startup checks, then read S21, passport, project_card, master plan v1.16, TASK_REGISTRY, RISK_REGISTER and the latest WORK_LOG. Refresh origin/main, git status/log and Task20 thread; this handoff is not current fact. The active SSOT was restored from v1.17 to v1.16 by explicit user instruction. Treat the benefit-aware router and 3%/5%/8% thresholds as historical non-authoritative proposals unless the user reauthorizes them. Formal gates remain G1 PASS, G2 protocol/data PASS_WITH_LIMITATIONS, asset admissibility DEFERRED_ACCEPTED_RISK and G3 PASS_WITH_LIMITATIONS. First close Task20’s NON_T0/INELIGIBLE exploration, runtime snapshot and restricted-storage lifecycle; only after the shared core is inactive may you review Task30 creation under v1.16. Do not touch tmp/. At session close create S22 and print the next continuation prompt.
