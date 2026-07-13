# 第二版模型消融实验

## 实验设置

- 数据集：CH-SIMS
- 主干：Self-MM
- 随机种子：1111、1112、1113
- 汇总方式：三个随机种子的均值 ± 总体标准差
- TG：带温度与熵下限约束的模态自适应门控
- MP：覆盖 `[-1, -0.5, 0, 0.5, 1]` 的五区间情绪原型

## 消融结果

| 模型 | Acc-2 ↑ | Acc-3 ↑ | Acc-5 ↑ | F1 ↑ | MAE ↓ | Corr ↑ | Loss ↓ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Self-MM | 76.95 ± 0.27 | 64.11 ± 0.71 | 43.76 ± 0.64 | 76.98 ± 0.26 | 41.98 ± 0.92 | 58.11 ± 1.11 | 42.26 ± 1.43 |
| Self-MM + TG | 78.12 ± 1.79 | **66.01 ± 0.55** | **43.91 ± 1.56** | 78.15 ± 1.49 | 42.13 ± 0.09 | 57.90 ± 0.31 | 42.65 ± 0.20 |
| Self-MM + MP | 79.21 ± 1.72 | 65.06 ± 1.09 | 42.38 ± 0.63 | 78.69 ± 1.36 | **41.87 ± 0.14** | 58.70 ± 0.59 | **41.97 ± 0.81** |
| Self-MM + TG + MP | **80.23 ± 0.45** | **66.01 ± 0.68** | 43.62 ± 2.03 | **80.06 ± 0.53** | 42.15 ± 0.93 | **58.73 ± 1.24** | 42.11 ± 0.87 |

## 分析

仅加入 TG 后，Acc-2、Acc-3、Acc-5 和 F1 分别较基线提高 1.17、1.90、0.15 和 1.17 个百分点，说明受约束的动态门控主要增强分类能力。其 Corr 略降 0.21 个百分点，MAE 和 Loss 也未改善，因此门控并不是回归性能提升的来源。

仅加入 MP 后，Acc-2、Acc-3、F1 和 Corr 分别提高 2.26、0.95、1.71 和 0.59 个百分点，同时 MAE 与 Loss 分别降低 0.11 和 0.29 个百分点。这说明五区间原型能够提供有效的情绪结构先验，但 Acc-5 下降 1.38 个百分点，尚未稳定提高离散的五分类结果。

完整模型取得最高 Acc-2、F1 和 Corr。与基线相比，Acc-2、Acc-3、F1 和 Corr 分别提高 3.28、1.90、3.08 和 0.62 个百分点；相较两个单模块版本，完整模型的 Acc-2 与 F1 也更高，说明 TG 与 MP 在情绪极性识别上具有互补作用。完整模型的 Acc-2 和 F1 标准差仅为 0.45 和 0.53，低于两个单模块版本，组合后分类稳定性更好。

需要如实说明：完整模型的 Acc-5 比基线低 0.14 个百分点，MAE 高 0.17 个百分点。因此当前证据支持“提升情绪极性分类及相关性”，不支持“全面提升所有细粒度回归指标”。

## 复现命令

```powershell
& D:\MMSA-CH-SIMS\.venv\Scripts\python.exe D:\MMSA-CH-SIMS\run_self_mm_aegm_sims.py --variant refined_gate --seeds 1111 1112 1113 --gpu 0
& D:\MMSA-CH-SIMS\.venv\Scripts\python.exe D:\MMSA-CH-SIMS\run_self_mm_aegm_sims.py --variant refined_prototype --seeds 1111 1112 1113 --gpu 0
& D:\MMSA-CH-SIMS\.venv\Scripts\python.exe D:\MMSA-CH-SIMS\run_self_mm_aegm_sims.py --variant refined --seeds 1111 1112 1113 --gpu 0
```

结果目录依次为 `experiments/self_mm_refined_gate`、`experiments/self_mm_refined_prototype` 和 `experiments/self_mm_refined`。
