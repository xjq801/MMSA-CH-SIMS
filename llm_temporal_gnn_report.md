# LLM情绪元 + Temporal GNN 组合实验报告

更新时间：2026-07-09

## 1. 实验目的

本次实验验证一个新的组合方向：

> 48维原始人工特征 + StepFun LLM情绪元 + Temporal GNN时间传播结构

也就是把前面已经验证过的两条有效线索合起来：

1. LLM情绪元：评论中的情绪极性、强度、攻击性、讽刺、争议度、置信度等；
2. Temporal GNN：同一发布者历史视频对当前视频群体情绪的影响。

## 2. 实验设置

- 样本：已有 StepFun LLM 缓存的 195 个视频
- 标签分布：
  - 0 类：96
  - 1 类：99
- 图结构：
  - 节点：视频
  - 边：同一发布者下，当前视频指向之前的历史视频
  - 历史窗口：previous 10
  - 有向边数：1731
  - 没有历史邻居的节点：4
- 模型：
  - MLP 48维
  - MLP 48维 + LLM情绪元
  - TemporalSAGE 48维
  - TemporalSAGE 48维 + LLM情绪元

## 3. 实验结果

| 模型 | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| MLP 48维 | 84.18 ± 0.80 | 88.89 ± 2.38 | 78.89 ± 3.14 | 83.51 ± 1.07 |
| MLP 48维 + LLM情绪元 | 85.88 ± 5.59 | 88.95 ± 3.56 | 82.22 ± 8.31 | 85.37 ± 6.08 |
| TemporalSAGE 48维 | 85.88 ± 0.80 | 93.38 ± 1.74 | 77.78 ± 1.57 | 84.85 ± 0.88 |
| TemporalSAGE 48维 + LLM情绪元 | **87.01 ± 2.11** | **93.49 ± 1.89** | **80.00 ± 2.72** | **86.21 ± 2.33** |

## 4. 关键结论

### 4.1 Temporal GNN 有效

在同一批 195 个视频上：

- MLP 48维：F1 83.51
- TemporalSAGE 48维：F1 84.85

加入时间传播结构后，F1 提升约 1.34 个百分点。

### 4.2 LLM情绪元有效

在 MLP 上：

- MLP 48维：F1 83.51
- MLP 48维 + LLM情绪元：F1 85.37

加入 LLM 情绪元后，F1 提升约 1.86 个百分点。

### 4.3 二者组合最好

最终组合模型：

- TemporalSAGE 48维 + LLM情绪元
- Accuracy：87.01
- F1：86.21

它是本组神经网络实验中最好的版本。

## 5. 与上一轮 CatBoost + LLM 的关系

需要诚实说明：这个轻量 TemporalSAGE 组合模型没有超过之前的 CatBoost + LLM 特征实验。

之前 195 条样本上的 CatBoost 结果约为：

- 原始48维：Accuracy 93.79，F1 94.06
- 原始48维 + StepFun LLM情绪元：Accuracy 94.92，F1 95.10

这说明当前数据规模较小、特征偏表格化时，CatBoost 仍然非常强。Temporal GNN 的价值不在于立刻超过 CatBoost，而在于证明“时间传播结构”本身能提供额外信息。

## 6. 当前论文判断

这条路线可以继续，但叙述要谨慎：

可以说：

> LLM情绪元与因果时间传播结构均能为群体情绪预测提供增益，二者结合在轻量神经模型中取得最佳表现。

暂时不要说：

> 深度学习模型全面超过 CatBoost。

更合理的下一步是做一个混合模型：

> CatBoost strong tabular learner + LLM情绪元 + Temporal aggregation features

也就是把 Temporal GNN 学到的历史传播信息变成可解释的时间聚合特征，再交给 CatBoost。这样更可能冲高指标，也更适合当前自建数据集的 48 维表格特征形态。

## 7. 相关文件

- 运行脚本：`D:\MMSA-CH-SIMS\run_llm_temporal_gnn.py`
- 原始结果：`D:\MMSA-CH-SIMS\experiments\llm_temporal_gnn\llm_temporal_gnn_results.json`
- 本报告：`D:\MMSA-CH-SIMS\llm_temporal_gnn_report.md`
