# 研究问题、贡献边界与实验接口冻结审计 v2

> 日期：2026-07-24  
> 决策：`POSITIONING_AMENDMENT_FROZEN_V2`  
> 上位SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.19  
> 历史审计：`RESEARCH_PROTOCOL_FREEZE_AUDIT.md`保留v1追溯，不再覆盖本文件。

## 1. 研究问题

核心问题重定位为：在目标评论不可用且测试内容偏离训练域时，能否可靠预测社交媒体评论者公开表达的诱发反应分布。

- RQ1/C1：严格T0、group-safe协议能否形成可审计的内容到受众反应分布预测证据；不主张任务首创。
- RQ2/H1：训练期评论特权教师能否改善T0 content-only学生，且收益不来自软标签、参数量或目标评论捷径。
- RQ3/H2：train-only反应记忆是否提供随机/普通近邻没有的有效证据，router/rejection能否识别错误检索与OOD负迁移。
- RQ4/C3：movie/group、topic、time、platform和跨数据域偏移下，分布误差、校准和选择性风险是否形成可解释的Pareto证据。
- H3/H4继续按v1的条件性/增强边界保留；无合格协议时记`NOT_APPLICABLE`，不虚构实验。

## 2. 接口影响

- 数据、split、标签、评测器、G1—G3和Task20冻结核心不变。
- 任务30新增普通KD、错配评论和teacher-only上界。
- 任务40分别消融memory、router、rejection，并增加错域/低质邻居和目标/未来候选fail-closed负对照。
- 任务50新增Video2Reaction式VLM直接微调/LDL强基线、movie/group OOD和完整五种子/paired bootstrap。
- 任务60执行claim blacklist和Video2Reaction closest-prior叙事。

## 3. 证据强度

C1—C4均保持`TO_VERIFY`。只有H1/H2至少一条在CSMV得到五种子、原生内容单元置信区间与强基线支持，且OOD/校准/选择性证据不过度恶化，才能保留完整方法主张。
