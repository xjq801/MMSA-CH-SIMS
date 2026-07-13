# CH-SIMS 上 CatBoost 与 Self-MM+MW+EP 对比

实验日期：2026-07-07  
数据集：CH-SIMS benchmark  
统计方式：3 seeds，均值 ± 标准差，单位为 %

## 重要说明

这里的 CatBoost 不是原论文自建数据集上的 48 维 M-DRGE 特征原样复刻。原因是 CH-SIMS 不包含原论文的传播、检索、粉丝数、播放量、热度等人工特征。

因此本实验采用“CatBoost 适配 CH-SIMS”方案：

1. 使用 CH-SIMS 官方 train / valid / test 划分。
2. 分别对文本、音频、视觉序列做均值和标准差池化。
3. 每个模态用 PCA 压缩到 16 维。
4. 拼接得到 48 维特征。
5. 使用 CatBoostRegressor 预测连续情感分数，再按 CH-SIMS 规则计算二分类、三分类、五分类指标。

Self-MM+MW+EP 使用此前最终模型结果。

## 1. 原论文 CatBoost 适配到 CH-SIMS

结果文件：

- `D:\MMSA-CH-SIMS\results\catboost_adapted\catboost_sims_report.json`
- `D:\MMSA-CH-SIMS\results\catboost_adapted\catboost_sims_runs.csv`
- `D:\MMSA-CH-SIMS\run_my_catboost_on_sims.py`

| 模型 | Accuracy | Precision | Recall | F1 Score | Acc-3 | Acc-5 | MAE | Corr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| CatBoost adapted | 81.25 ± 0.27 | 81.61 ± 0.36 | 81.25 ± 0.27 | 81.40 ± 0.30 | 63.46 ± 0.64 | 32.31 ± 0.27 | 44.16 ± 0.49 | 62.96 ± 0.91 |

## 2. Self-MM+MW+EP

结果文件：

- `D:\MMSA-CH-SIMS\experiments\final_classic_metrics\self_mm_mw_ep\results\normal\sims.csv`
- `D:\MMSA-CH-SIMS\final_self_mm_mw_ep_classic_ablation_results.md`

| 模型 | Accuracy | Precision | Recall | F1 Score | Acc-3 | Acc-5 | MAE | Corr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Self-MM+MW+EP | 80.23 ± 0.45 | 80.00 ± 0.60 | 80.23 ± 0.45 | 80.06 ± 0.53 | 66.01 ± 0.68 | 43.62 ± 2.03 | 42.15 ± 0.93 | 58.73 ± 1.24 |

## 3. 直接对比

| 指标 | 更优模型 | 说明 |
|---|---|---|
| Accuracy（二分类） | CatBoost adapted | 81.25% vs 80.23% |
| Precision（二分类） | CatBoost adapted | 81.61% vs 80.00% |
| Recall（二分类） | CatBoost adapted | 81.25% vs 80.23% |
| F1（二分类） | CatBoost adapted | 81.40% vs 80.06% |
| Acc-3 | Self-MM+MW+EP | 66.01% vs 63.46% |
| Acc-5 | Self-MM+MW+EP | 43.62% vs 32.31% |
| MAE | Self-MM+MW+EP | 42.15% vs 44.16%，越低越好 |
| Corr | CatBoost adapted | 62.96% vs 58.73% |

## 4. 结论

在 CH-SIMS benchmark 上，CatBoost 适配版在二分类 Accuracy / Precision / Recall / F1 和 Corr 上略优于 Self-MM+MW+EP。

但 Self-MM+MW+EP 在更细粒度的 Acc-3、Acc-5 和 MAE 上更好，说明它对连续情绪强度和细粒度情绪区间的建模更有优势。

因此论文中不建议写“Self-MM+MW+EP 全面超过 CatBoost”。更稳妥的写法是：

> 在 CH-SIMS benchmark 上，CatBoost 适配版在二分类指标上表现较强，而本文提出的 Self-MM+MW+EP 在三分类、五分类以及 MAE 上表现更优，说明该模型更适合细粒度多模态情绪建模。考虑到 CatBoost 使用的是池化后的统计特征，而 Self-MM+MW+EP 直接建模文本、音频、视觉序列，两者从不同角度验证了 CH-SIMS 上多模态情绪预测的有效性。
