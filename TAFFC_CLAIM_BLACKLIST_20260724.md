# T-AFFC Claim Blacklist

> 版本：v1.0  
> 日期：2026-07-24  
> 上位SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.19  
> 适用范围：总纲、摘要、引言、贡献、相关工作、结论、图注、补充材料、PPT、答辩稿、项目报告与对外说明。

## 1. 禁止主张

| ID | 禁止表述及同义改写 | 原因 | 允许替代 |
|---|---|---|---|
| BL-01 | 首次从多模态/视频内容预测观众情感反应 | Video2Reaction已直接覆盖 | 研究无目标响应且分布偏移时的可靠预测 |
| BL-02 | 首次研究内容到群体情感分布映射 | Video2Reaction、NEmo+等已覆盖任务家族 | 强调严格T0、train-only证据与OOD可靠性 |
| BL-03 | 首次构建视频诱发情感分布预测任务或benchmark | Video2Reaction已建立直接benchmark | C1仅称协议/证据贡献 |
| BL-04 | 现有工作只识别内容表达情感，从未预测观众诱发情感 | 与直接前作事实冲突 | 承认共享任务，说明尚未解决的可靠性问题 |
| BL-05 | 输出分布而非单标签本身就是创新 | LDL与诱发分布预测已有成熟前作 | 只把分布作为estimand与评测对象 |
| BL-06 | 评论标签代表所有观众的真实内在情绪 | 评论者有选择偏差且只能观察公开表达 | “社媒评论者公开表达的诱发反应分布” |
| BL-07 | teacher/student、蒸馏、memory、router、拒绝或其组合是模块级首创 | 各组件均有直接或相邻前作 | 以可测失败机制和单变量证据界定候选贡献 |
| BL-08 | 未完成五种子/CI/OOD前称SOTA、显著优越、稳健泛化或可靠 | 当前只有单seed基线与计划性假设 | 使用`TO_VERIFY`、开发趋势或限定性观察 |

## 2. Video2Reaction关系锁

Video2Reaction必须称为`closest/direct prior`。双方共享“内容→受众诱发反应分布”任务；差异只能落在研究目标和证据机制：本项目研究目标响应不可用和测试分布偏移时，评论特权教师、train-only反应记忆、可靠性路由、校准与选择性拒绝能否提供可审计收益。

建议引言关系句：

> Concurrent Video2Reaction research establishes the feasibility of directly predicting induced audience-reaction distributions from video. Our work instead investigates whether such predictions remain reliable when target responses are unavailable and test content deviates from training domains.

## 3. 回扫与放行合同

1. 任务30—50每次改变贡献定义后，回扫总纲、claim矩阵、实验登记和结果说明。
2. 任务60必须回扫标题、摘要、引言、贡献、相关工作、结论、图注和补充材料。
3. 命中仅作为历史引用、否定句或本blacklist定义时可保留；活动正向主张命中必须阻断写作交付。
4. “未命中关键词”不等于语义全覆盖；最终仍需人工审查同义改写与构念外推。
5. 本清单不改变G1—G3，不把C1—C4从`TO_VERIFY`升级为`SUPPORTED`。
