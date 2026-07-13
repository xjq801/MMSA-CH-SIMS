# CatBoost + LLM情绪元 + Temporal时间聚合特征实验报告

更新时间：2026-07-09

## 1. 实验目的

本次实验验证一个更适合当前自建数据集形态的混合模型：

> CatBoost + StepFun LLM情绪元 + Temporal时间聚合特征

原因是：自建数据集原始输入本质上是 48 维表格特征，CatBoost 对这种表格数据非常强；而 LLM 情绪元和 Temporal GNN 已经分别证明有额外信息，因此本次把它们转成 CatBoost 可直接使用的特征。

## 2. 特征设计

### 2.1 原始特征

- 原论文自建数据集中的 48 维人工特征。

### 2.2 LLM情绪元

使用 StepFun LLM 已缓存的 7 维情绪元：

- 正向情绪强度
- 负向情绪强度
- 情绪强度
- 攻击性
- 讽刺性
- 争议度
- 置信度

### 2.3 Temporal时间聚合特征

对同一发布者下的历史视频构造 causal temporal aggregation：

- 当前视频只使用发布时间之前的视频；
- 历史窗口为 previous 10；
- 不使用历史标签，避免标签泄漏；
- 构造历史特征均值；
- 构造当前特征与历史均值的差；
- 加入历史视频数量比例、是否存在历史视频、与上一个视频的时间间隔。

## 3. 实验设置

- 样本：已有 StepFun LLM 缓存的 195 个视频
- 标签分布：
  - 0 类：96
  - 1 类：99
- 数据划分：
  - 70% train
  - 30% test
  - 与前一版 CatBoost + LLM 实验保持一致：按 BV 排序后，使用相同 random_state 划分
- 随机种子：
  - 1111
  - 1112
  - 1113
- 模型：
  - CatBoostClassifier
  - iterations=300
  - loss_function=Logloss

## 4. 实验结果

| 模型 | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| CatBoost 48维 | 93.79 ± 0.80 | 91.60 ± 1.38 | 96.67 ± 0.00 | 94.06 ± 0.72 |
| CatBoost 48维 + LLM情绪元 | 94.92 ± 1.38 | 93.61 ± 2.47 | 96.67 ± 0.00 | 95.10 ± 1.27 |
| CatBoost 48维 + Temporal时间聚合 | 94.35 ± 1.60 | 92.64 ± 2.85 | 96.67 ± 0.00 | 94.59 ± 1.47 |
| CatBoost 48维 + LLM情绪元 + Temporal时间聚合 | **96.05 ± 0.80** | **95.63 ± 1.47** | **96.67 ± 0.00** | **96.14 ± 0.75** |

## 5. 关键结论

### 5.1 LLM情绪元有效

相比原始 48 维：

- Accuracy：93.79 → 94.92
- F1：94.06 → 95.10

说明评论中的情绪极性、攻击性、争议度等 LLM 情绪元能够补充原始人工特征。

### 5.2 Temporal时间聚合有效

相比原始 48 维：

- Accuracy：93.79 → 94.35
- F1：94.06 → 94.59

说明同一发布者历史视频的传播上下文确实有用。

### 5.3 三者组合最佳

最终组合：

> CatBoost 48维 + LLM情绪元 + Temporal时间聚合

达到：

- Accuracy：96.05%
- Precision：95.63%
- Recall：96.67%
- F1：96.14%

这是当前 195 条 StepFun LLM 缓存样本上的最佳结果。

## 6. 与深度学习 TemporalSAGE 的关系

上一版深度学习组合模型：

- TemporalSAGE 48维 + LLM情绪元
- Accuracy：87.01
- F1：86.21

本次 CatBoost 混合模型明显更高：

- Accuracy：96.05
- F1：96.14

这说明当前自建数据集仍然更适合表格学习器，但 Temporal 传播思想仍然有效。最合理的论文写法不是“深度学习全面替代 CatBoost”，而是：

> 使用大模型增强情绪语义表示，并引入因果时间传播聚合特征，最终由强表格学习器 CatBoost 进行群体情绪预测。

## 7. 当前论文方法命名建议

可以暂时命名为：

> LLM-Temporal CatBoost for Group Emotion Prediction

中文可以叫：

> 融合大模型情绪元与时间传播聚合的群体情绪预测方法

## 8. 局限性

这组结果只基于已有 195 条 StepFun LLM 缓存视频，还不是全量自建数据集结果。正式论文中需要继续扩大 LLM 标注样本，并补充：

1. 全量或更大规模样本实验；
2. 多随机划分或交叉验证；
3. topic/publisher group split；
4. LLM情绪元人工抽检；
5. 不同 temporal window 的消融。

## 9. 相关文件

- 运行脚本：`D:\MMSA-CH-SIMS\run_catboost_llm_temporal.py`
- 原始结果：`D:\MMSA-CH-SIMS\experiments\catboost_llm_temporal\catboost_llm_temporal_results.json`
- 本报告：`D:\MMSA-CH-SIMS\catboost_llm_temporal_report.md`
