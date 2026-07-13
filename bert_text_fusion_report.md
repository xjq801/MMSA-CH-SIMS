# BERT文本深度表示融合实验报告

更新时间：2026-07-10

## 1. 实验目的

本次实验验证“标题 + 标签 + 简介 + 代表评论”的中文深度文本表示是否能补充当前自建数据集上的特征体系。

文本构造方式：

- 标题
- 视频标签
- 视频简介
- 评论点赞数最高的前 20 条代表评论

文本编码器：

- 本地 `bert-base-chinese`
- 冻结 BERT，不微调
- mean pooling 得到 768 维文本向量
- 在每次 train/test split 内，只用训练集 fit PCA，将文本向量降到 32 维，避免小样本高维过拟合和数据泄漏

## 2. 运行说明

第一次运行时，本机 CatBoost 包不可用，原因是 Windows 用户代理指向 `127.0.0.1:7890`，但该本地代理服务不可用，导致 pip 下载失败。随后临时关闭代理、使用清华 PyPI 镜像安装了 `catboost==1.2.10`，并恢复了原代理设置。

因此本报告同时保留：

- sklearn `HistGradientBoostingClassifier` fallback 结果；
- CatBoost 正式复跑结果。

## 3. 实验设置

- 样本：195 个已有 StepFun LLM 缓存视频
- 标签分布：0 类 96，1 类 99
- 划分：70% train / 30% test，`random_state=42`，stratify
- 随机种子：1111、1112、1113
- 指标：Accuracy、Precision、Recall、F1

## 4. HGB fallback 实验结果

| 模型 | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| HGB 48维 | 89.83 ± 0.00 | 85.29 ± 0.00 | 96.67 ± 0.00 | 90.63 ± 0.00 |
| HGB BERT文本 | 81.36 ± 0.00 | 82.76 ± 0.00 | 80.00 ± 0.00 | 81.36 ± 0.00 |
| HGB 48维 + BERT文本 | 93.22 ± 0.00 | 90.63 ± 0.00 | 96.67 ± 0.00 | 93.55 ± 0.00 |
| HGB 48维 + LLM情绪元 + Temporal | 93.22 ± 0.00 | 90.63 ± 0.00 | 96.67 ± 0.00 | 93.55 ± 0.00 |
| HGB 48维 + LLM情绪元 + Temporal + BERT文本 | **96.61 ± 0.00** | **96.67 ± 0.00** | **96.67 ± 0.00** | **96.67 ± 0.00** |

## 5. 结论

1. BERT文本单独预测不够强，说明“只看语义文本”还不足以替代原论文的传播和检索特征。
2. BERT文本与48维特征融合有效：Accuracy 从 89.83% 提升到 93.22%，F1 从 90.63% 提升到 93.55%。
3. 在 `48维 + LLM情绪元 + Temporal` 的基础上继续加入 BERT文本，Accuracy/F1 进一步提升到 96.61%/96.67%。
4. 这说明在 HGB fallback 模型中，BERT 文本表示有增益。

## 6. CatBoost正式复跑结果

在 CatBoost 中，旧口径 `48维 + LLM情绪元 + Temporal` 结果已复现：

| CatBoost模型 | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| CatBoost 48维 | 93.79 ± 0.80 | 91.60 ± 1.38 | 96.67 ± 0.00 | 94.06 ± 0.72 |
| CatBoost BERT文本 | 82.49 ± 2.88 | 79.20 ± 2.42 | 88.89 ± 3.14 | 83.76 ± 2.69 |
| CatBoost 48维 + BERT文本 | 93.79 ± 0.80 | 91.60 ± 1.38 | 96.67 ± 0.00 | 94.06 ± 0.72 |
| CatBoost 48维 + LLM情绪元 + Temporal | **96.05 ± 0.80** | **95.63 ± 1.47** | **96.67 ± 0.00** | **96.14 ± 0.75** |
| CatBoost 48维 + LLM情绪元 + Temporal + BERT文本 | 94.35 ± 0.80 | 92.57 ± 1.38 | 96.67 ± 0.00 | 94.57 ± 0.72 |

同时扫了 BERT 文本 PCA 维度：

| BERT PCA维度 | Accuracy | Precision | Recall | F1 |
|---:|---:|---:|---:|---:|
| 4 | 94.92 | 93.55 | 96.67 | 95.08 |
| 8 | 95.48 | 94.59 | 96.67 | 95.61 |
| 16 | 93.79 | 91.60 | 96.67 | 94.06 |
| 32 | 94.35 | 92.57 | 96.67 | 94.57 |
| 64 | 94.92 | 93.61 | 96.67 | 95.10 |

结论：在 CatBoost 正式模型中，BERT 文本特征暂时没有超过 `48维 + LLM情绪元 + Temporal`，最佳 PCA=8 时 F1=95.61%，仍低于不加 BERT 的 F1=96.14%。

因此当前论文主模型仍建议保留：

> CatBoost + 48维原始特征 + LLM情绪元 + Temporal时间传播聚合

BERT 文本深度表示可以作为“已探索但未提升”的消融实验，或后续改用更适合语义检索的 BGE/Qwen embedding 再评估。

## 7. 注意事项

- 当前样本仍是 195 条 LLM 缓存子集，正式论文需要扩大样本。
- 当前仍是随机划分探索结果，需要补充 time split 和 publisher group split。
- 旧 CatBoost+Temporal 脚本与本脚本的时间字段读取方式不同，本脚本补充了从评论表读取标题、标签、简介和发布时间的 fallback，因此后续应统一数据加载逻辑后再做正式大表。

## 8. 相关文件

- 运行脚本：`D:\MMSA-CH-SIMS\run_bert_text_fusion_experiment.py`
- 原始结果：`D:\MMSA-CH-SIMS\experiments\bert_text_fusion\bert_text_fusion_results.json`
- CatBoost文本PCA维度扫描：`D:\MMSA-CH-SIMS\experiments\bert_text_fusion\catboost_text_pca_sweep.json`
- BERT文本向量缓存：`D:\MMSA-CH-SIMS\experiments\bert_text_fusion\bert_text_embeddings.npz`
- 本报告：`D:\MMSA-CH-SIMS\bert_text_fusion_report.md`
