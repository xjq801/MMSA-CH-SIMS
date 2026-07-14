# 步骤21：CARM 工作名重名审计

> 审计日期：2026-07-14
> 决策：`NAME_BLOCKED`
> 适用范围：论文标题、摘要、图表、代码包、模型卡和正式实验注册。

## 结论

`CARM`已在机器学习、推荐、检索、持续学习、可靠机器学习、优化和系统性能领域被多次使用，且至少一个既有用法就是“Constraint-Aware Retrieval Module”。因此它不具备足够区分度，当前不得作为正式方法名或标题缩写。

## 已核同名/近同名

| 既有名称 | 领域/年份 | 冲突强度 | 来源 |
|---|---|---|---|
| Confidence-aware Recommender Model (CARM) | 推荐系统，2021 | 高：同为用户反应/评论相关模型 | [Neurocomputing页面](https://www.sciencedirect.com/science/article/pii/S0925231221005142) |
| Constraint-Aware Retrieval Module (CARM) | 神经符号约束建模，2025 | 极高：同为retrieval module | [arXiv](https://arxiv.org/abs/2510.05774) |
| Conformal Association Rule Mining (CARM) | 可靠机器学习，2023 | 高：与可靠性/置信度语境重叠 | [PMLR](https://proceedings.mlr.press/v204/nouretdinov23a.html) |
| CarM: Hierarchical Episodic Memory for Continual Learning | 持续学习记忆，2022 | 极高：同为memory模型，大小写差异不足 | [论文PDF](https://snumprlab.github.io/research/papers/dac2022-carm.pdf) |
| Cache-Aware Roofline Model (CARM) | 高性能计算 | 中：广泛使用的系统性能缩写 | [arXiv检索例](https://arxiv.org/abs/2605.29740) |
| Constraint-Aware Residual Modulation (CARM) | 神经路径规划，2026 | 高：AI模型模块同名 | [arXiv](https://arxiv.org/abs/2605.10122) |
| Compression Artifact Removal Module (CARM) | 图像超分辨率，2023 | 中：视觉模块同名 | [论文页](https://www.mdpi.com/2079-9292/12/5/1209) |
| Coordinate Attention Recalibration Mechanism (CARM) | 图像去雨，2022 | 中：视觉模块同名 | [论文PDF](https://openreview.net/pdf?id=MVhqwigaZyg) |

## 执行规则

1. 现有总纲中的`CARM-v1`只按历史工作包代号理解，不得扩展为正式英文全称。
2. 配置、注册表和新文档若必须引用，写作`reaction-memory prototype (working package; NAME_BLOCKED)`，避免制造新正式名。
3. 在另行完成候选名生成、论文/代码/商标式检索和用户批准前，不替换为另一个未经审计的缩写。
4. 名称阻塞不影响M1/M2数据与协议工作，也不授权提前开发M5检索模型。
