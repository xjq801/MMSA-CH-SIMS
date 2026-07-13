# 自建数据集复跑结果

数据集：论文自建“极端群体情绪预测数据集”  
可用样本：2787 条  
标签分布：0 类 1444 条，1 类 1343 条  
测试集：随机分层 80/20，测试样本 558 条  

## 1. 原论文 CatBoost 复现结果

| 模型 | Accuracy | Precision | Recall | F1 Score |
|---|---:|---:|---:|---:|
| CatBoost（原论文代码） | 82.26% | 84.55% | 77.32% | 80.78% |

混淆矩阵：

```text
[[251,  38],
 [ 61, 208]]
```

结果文件：

- `D:\MMSA-CH-SIMS\experiments\self_built_dataset\catboost_original\artifacts\train_metrics.json`
- `D:\MMSA-CH-SIMS\experiments\self_built_dataset\catboost_original\artifacts\test_metrics.json`

## 2. MW+EP 在自建数据集上的表格迁移版结果

说明：自建数据集没有 CH-SIMS 那种文本、音频、视觉序列特征，不能直接运行原始 Self-MM。因此这里做的是一个最小迁移实验：把 48 维人工特征按“标题 / 标签 / 简介 / 封面”拆成 4 个伪模态，加入模态权重门控（MW）和情绪原型（EP）。

该模型不能严格称为 Self-MM，只能作为“MW+EP 模块迁移到自建表格数据”的补充实验。

3 seeds：1111、1112、1113。

| 模型 | Accuracy | Precision | Recall | F1 Score |
|---|---:|---:|---:|---:|
| Tabular MW+EP | 72.64% ± 0.08 | 80.11% ± 1.52 | 57.62% ± 1.82 | 66.99% ± 0.70 |

结果文件：

- `D:\MMSA-CH-SIMS\experiments\self_built_dataset\tabular_mw_ep\results.json`

## 3. 结论

在自建数据集上，原论文 CatBoost 明显优于表格迁移版 MW+EP。主要原因是：

1. 自建数据集是 48 维人工统计特征，不是原始文本、音频、视觉多模态序列。
2. CatBoost 对这种小样本结构化表格数据非常强。
3. Self-MM+MW+EP 的优势场景是 CH-SIMS 这类公开多模态 benchmark，而不是只有人工特征的表格分类任务。

因此，论文里不建议写“Self-MM+MW+EP 在自建数据集上超过原论文 CatBoost”。更稳妥的写法是：

> 在公开 CH-SIMS benchmark 上，本文方法相较 Self-MM baseline 取得提升；在自建群体情绪数据集上，原论文 CatBoost 仍作为强表格基线保留，用于证明自建数据集上的传统机器学习有效性。
