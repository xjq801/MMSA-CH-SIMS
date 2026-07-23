---
session_no: S20
contract_version: 2
suggested_title: "[T-AFFC] S21 close Task20 and freeze Task30 H1 preregistration"
parent_session: S19
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-23
---

# S20 master plan v1.17 consolidation handoff

## 当前阶段

- 活动SSOT已升级为总纲v1.17；当前仍处于Task20探索收尾与Task30预注册准备，未创建任务30、未运行新实验。

## 已完成

- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.17 — 验证：活动总纲由1299行压缩为476行，集中保留项目边界、G1—G6、C1—C3、H1—H4、3%/5%/8%效应门、E0—E9、任务树、预算和T-AFFC Go标准。
- `AGENTS.md` — 验证：当前执行版本和任务10定位已更新为v1.17/第7.3节。
- `.light/project_card.md`、`.light/terminology.md`、`.light/decision_log.md`、`.light/version_history.md` — 验证：方法标准词固定为“收益感知可靠性路由”，方法状态仍PLANNED/TO_VERIFY。
- `CLAIM_EVIDENCE_MATRIX.md` v1.1 — 验证：C3加入cross-fitting效用、固定融合/简单拒绝和错误邻居对照；C1—C4状态未升级。
- `RISK_REGISTER.md` — 验证：新增新颖性、单seed证据和Task20运维收尾风险。
- `TASK_REGISTRY.md` v1.0 — 验证：登记00—60状态、任务ID、退出门和交接；任务30仍冻结。
- 一致性部分回扫 — 验证：Markdown权威源扫描8份材料，术语/数值/claim强度硬冲突0；因技能安装缺`_shared/findings_schema`，机读报告生成失败，结论只能是PARTIAL，未冒充完整一致性门PASS。

## 工作区状态

- 开工时`main=origin/main=d45338eafb8da2bdfe09e55121e9810c5244348f`，仅Task20所有的`tmp/`未跟踪。
- 本批修改总纲及其版本/claim/风险/任务登记/交接文件，当前worktree为dirty/unpushed；提交前门禁结果以本批实际输出为准。
- `tmp/`未被00读取、暂存、移动或删除。

## 待用户回答

- none — 用户已明确授权把创新与实验目标整合进总纲并精简；本批未启动付费、远程、投稿或删除动作。

## 核心决策

1. 总纲v1.17正式采用“评论特权学习 + train-only受众反应记忆 + 收益感知可靠性路由”的计划方法，但实现和有效性仍是PLANNED/TO_VERIFY。
2. 开发趋势固定为JSD相对改善至少3%；论文最低门为至少5%且原生单位paired bootstrap 95% CI优于0；强结果为至少8%；可靠性替代门为JSD绝对+0.003内非劣、AURC至少改善10%、负迁移率至少下降20%。
3. 当前正式协议没有同一样本多T0模态，H3/E5保持N/A；H4保持条件性NEmo+增强。
4. 精简没有改变G1—G3、I3D风险、formal split、T0边界、Task20 NON_T0/INELIGIBLE身份或任务依赖。

## 阻塞/风险

- Task20 VC-CSA探索、运行时快照和受限存储生命周期仍未闭环，阻止Task30创建。
- `.light/passport.yaml`仍是旧PLANNED账本；底层validate为WARN且无inputs_fingerprint，不能自动证明新总纲的stale传播。未获专门台账迁移/修复批次前不冒充passport已同步。
- 一致性技能因缺`_shared/findings_schema`只能完成文本回扫，完整机读findings不可用。
- I3D许可、稳定revision和权利方包身份/fixity继续UNKNOWN；资产止损不变。

## 必读文件

- `.light/handoff/S20-master-plan-v117-consolidation.md`
- `.light/passport.yaml`
- `.light/project_card.md`
- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.17
- `TAFFC_PAPER_INNOVATION_AND_EXPERIMENT_TARGETS_20260723.md`
- `TASK_REGISTRY.md`
- `CLAIM_EVIDENCE_MATRIX.md`
- `RISK_REGISTER.md`
- `TASK00_G3_FINAL_REVIEW_20260718.md`
- 最新`WORK_LOG.md`与Task20实时任务

## 下一步

- 跑Task20实时状态复核，要求其形成完成、失败或不可用收尾以及快照/受限存储生命周期证据。
- 验证共享实验核心停止修改或运行后，按总纲v1.17起草Task30 H1预注册与创建提示。
- 写Task30目标链和失败树，冻结3%开发门、5%论文门、ECE guardrail和错配评论负对照。

## 禁止

- 不得把本卡当作当前事实或凭记忆执行；必须先运行`git status --short --branch`和`git log`，再刷新Task20。
- 不得把3%/5%/8%计划门写成已取得结果或录用保证。
- 不得在Task20未闭环时创建任务30或并发修改共享实验核心。
- 不得把收益感知可靠性路由写成已实现、已验证或模块级首创。
- 不得把H3/E5的N/A写成通过，不得制造伪模态。
- 不得更新旧IJCV任务或触碰Task20所有的`tmp/`。

## Continuation prompt

You are the 00-T-AFFC total controller taking over S20. Read AGENTS.md and perform startup checks, then read S20, passport, project_card, master plan v1.17, TASK_REGISTRY, CLAIM_EVIDENCE_MATRIX, RISK_REGISTER and the latest WORK_LOG. Refresh origin/main, git status/log and Task20 thread; this handoff is not current fact. The active SSOT is master plan v1.17. It adopts the PLANNED benefit-aware reliability router and the preregistration gates of 3% relative JSD for development, 5% plus native-unit paired 95% CI for the paper minimum, 8% for a strong result, or absolute JSD noninferiority +0.003 with at least 10% AURC improvement and 20% negative-transfer reduction. These are targets, not results. H3/E5 remain N/A under current single-T0-modality protocols. Formal gates remain G1 PASS, G2 protocol/data PASS_WITH_LIMITATIONS, asset admissibility DEFERRED_ACCEPTED_RISK and G3 PASS_WITH_LIMITATIONS. First close Task20’s NON_T0/INELIGIBLE exploration and storage lifecycle; only after the shared core is inactive may you draft and create Task30. Do not touch tmp/. At session close create S21 and print the next continuation prompt.
