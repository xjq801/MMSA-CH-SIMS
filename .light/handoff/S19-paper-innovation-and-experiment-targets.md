---
session_no: S19
contract_version: 2
suggested_title: "[T-AFFC] S20 close Task20 and preregister Task30 H1"
parent_session: S18
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-23
---

# S19 paper innovation and experiment targets handoff

## 当前阶段

- 总纲v1.16、G1/G2/G3状态未变；本会话只形成论文创新性、方法新颖性和E0—E9预期性能的独立评估档案，没有启动任务30、修改实验核心或执行新训练。

## 已完成

- `TAFFC_PAPER_INNOVATION_AND_EXPERIMENT_TARGETS_20260723.md` — 验证：逐项映射C1—C3、H1—H4、E0—E9和任务30/40/50，明确当前只有候选方法框架、尚无H1/H2有效性证据。
- 性能目标 — 验证：以当前单种子temporal-attention JSD=0.182668为规划锚点，区分3%开发趋势、5%论文最低目标、8%强结果目标，并冻结可靠性Pareto建议门。
- 新颖性边界 — 验证：回扫`CONTRIBUTION_PRIOR_ART_MATRIX.md`、`LITERATURE_SEARCH_REPORT.md`和最新近邻研究，确认蒸馏、评论增强、反应分布预测、检索和选择性拒绝均不能单独称首创。
- Task20实时状态 — 验证：读取任务20任务，最新可核状态仍为基线/G3主体完成；VC-CSA探索训练未有完整结果，远端SSH不可达，永久NON_T0/INELIGIBLE。

## 工作区状态

- 写卡前`main=origin/main=5371992d04eb7981ccd0237408e8a1e4ba765ba2`，仅Task20所有的`tmp/`未跟踪；00未读取、暂存、移动或删除`tmp/`。
- 本会话新增论文创新/实验目标档案、本S19和一条WORK_LOG，当前worktree为dirty/unpushed；待门禁、提交和推送。提交前CI证据以本批实际校验输出为准。

## 待用户回答

- none — 本批只形成研究评估档案，不启动新实验或产生付费动作。

## 核心裁定

1. 当前不能宣称已经形成或验证新方法；CARM仍为待实现候选。
2. C1是中等强度的问题/协议贡献；H1单独新颖性中低；H2的“收益感知可靠性路由”最有机会成为核心方法，但属于建议收紧，尚未升级为执行事实。
3. 当前正式协议没有合格的同一样本多T0模态，H3/E5应为N/A；H4仍是NEmo+条件性增强。
4. 论文最低建议门为：相对最终最强公平基线JSD改善至少5%且paired 95% CI优于0、校准不恶化；或JSD绝对+0.003内非劣、AURC改善至少10%、负迁移率下降至少20%的Pareto优势。

## 阻塞/风险

- 任务30/40尚未实现，性能目标必须先在dev和资源smoke上校准，但不得在test后改线。
- 近邻工作已覆盖评论增强社会情绪预测和伪/生成评论路线，方法若只做模块组合会遭遇新颖性Critical。
- I3D许可、官方revision和权利方包身份/fixity仍为UNKNOWN；资产止损条件不变。
- Task20 VC-CSA探索尚未闭环，且正在/曾经使用共享实验核心；收尾前不得创建任务30。

## 必读文件

- `.light/handoff/S19-paper-innovation-and-experiment-targets.md`
- `.light/passport.yaml`
- `.light/project_card.md`
- `TAFFC_PAPER_INNOVATION_AND_EXPERIMENT_TARGETS_20260723.md`
- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.16
- `research-question-v1.md`
- `experiment-protocol-v2.md`
- `CONTRIBUTION_PRIOR_ART_MATRIX.md`
- `CLAIM_EVIDENCE_MATRIX.md`
- `TASK00_G3_FINAL_REVIEW_20260718.md`
- `BASELINE_TABLE_V1.md`
- 最新`WORK_LOG.md`与Task20实时任务

## 下一步

- 跑Task20实时状态复核，形成完成、失败或不可用的正式探索收尾，并完成运行时快照/受限存储生命周期记录。
- 验证任务30创建条件；将H1的3%开发门、5%论文目标、校准非恶化界和错配评论负对照写入正式预注册。
- 写入用户批准后的任务40候选规格；若批准收益感知路由，要求cross-fitting防泄漏并与固定权重、相似度阈值和熵拒绝比较。

## 禁止

- 不得把本卡当作当前事实或凭记忆执行；必须先运行`git status --short --branch`和`git log`，再刷新Task20。
- 不得把本档案的建议性能目标写成已取得结果或录用保证。
- 不得在Task20未收尾时创建任务30或并发修改实验核心。
- 不得把teacher/student、RAG、动态权重、拒绝或模块拼接本身写成首创。
- 不得把H3/E5的N/A改写为通过，不得制造伪模态。
- 不得升级C1—C4的`TO_VERIFY`状态，除非任务50冻结统计证据。
- 不得读取、暂存、移动或删除Task20所有的`tmp/`。

## Continuation prompt

You are the 00-T-AFFC total controller taking over S19. Read AGENTS.md and perform startup checks, then read the must-read files above. Refresh origin/main, git status, git log and Task20 thread; this handoff is not current fact. Formal gates remain G1 PASS, G2 protocol/data PASS_WITH_LIMITATIONS, ASSET_ADMISSIBILITY DEFERRED_ACCEPTED_RISK and G3 PASS_WITH_LIMITATIONS. The paper innovation assessment is in TAFFC_PAPER_INNOVATION_AND_EXPERIMENT_TARGETS_20260723.md: C1 is primarily a strict T0/no-leakage protocol contribution, H1 teacher/student is not novel alone, and the strongest candidate method is a benefit-aware reliability router over train-only audience-response memory. All effectiveness claims remain TO_VERIFY. Proposed preregistration targets are 3% relative JSD for a development trend, 5% with paired 95% CI for the paper minimum, 8% for a strong result, or JSD noninferiority within absolute +0.003 plus at least 10% AURC improvement and 20% negative-transfer reduction. H3/E5 are currently N/A because no formal protocol has at least two real T0 modalities; H4 remains optional. First close Task20, then preregister Task30 H1 without modifying frozen Task20 evaluation artifacts. Do not touch tmp/. At session close create S20 and print the next continuation prompt.
