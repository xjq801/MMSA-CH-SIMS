# Self-MM + MW + EP 消融实验结果（Accuracy / Precision / Recall / F1）

数据集：CH-SIMS  
实验设置：3 seeds（1111、1112、1113）  
分类口径：二分类，负向/非正向 `[-1, 0]` vs 正向 `(0, 1]`  
统计方式：均值 ± 标准差，单位为 %

| 模型 | Accuracy | Precision | Recall | F1 Score |
|---|---:|---:|---:|---:|
| Self-MM | 76.95 ± 0.27 | 77.02 ± 0.25 | 76.95 ± 0.27 | 76.98 ± 0.26 |
| Self-MM + MW | 78.12 ± 1.79 | 78.38 ± 1.27 | 78.12 ± 1.79 | 78.15 ± 1.49 |
| Self-MM + EP | 79.21 ± 1.72 | 78.78 ± 1.43 | 79.21 ± 1.72 | 78.69 ± 1.36 |
| Self-MM + MW + EP | **80.23 ± 0.45** | **80.00 ± 0.60** | **80.23 ± 0.45** | **80.06 ± 0.53** |

## 结论

1. 相比原始 Self-MM，加入模态自适应权重（MW）后，Accuracy 从 76.95% 提升到 78.12%，F1 从 76.98% 提升到 78.15%。
2. 单独加入情绪原型引导（EP）后，Accuracy 达到 79.21%，提升幅度高于单独 MW。
3. 同时加入 MW 和 EP 后效果最好，Accuracy 达到 80.23%，F1 Score 达到 80.06%，说明两个模块存在互补作用。

## 结果文件

- 原始 Self-MM：`D:\MMSA-CH-SIMS\experiments\final_classic_metrics\self_mm\results\normal\sims.csv`
- Self-MM + MW：`D:\MMSA-CH-SIMS\experiments\final_classic_metrics\self_mm_mw\results\normal\sims.csv`
- Self-MM + EP：`D:\MMSA-CH-SIMS\experiments\final_classic_metrics\self_mm_ep\results\normal\sims.csv`
- Self-MM + MW + EP：`D:\MMSA-CH-SIMS\experiments\final_classic_metrics\self_mm_mw_ep\results\normal\sims.csv`

## 代码改动

- 在 `D:\MMSA-CH-SIMS\MMSA\src\MMSA\utils\metricsTop.py` 中补充了 Precision 和 Recall。
- 新增运行脚本：`D:\MMSA-CH-SIMS\run_final_self_mm_mw_ep_ablation.py`。
