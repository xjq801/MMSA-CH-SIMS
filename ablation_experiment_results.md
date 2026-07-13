# Self-MM 改进模型消融实验

## 实验设置

- 数据集：CH-SIMS
- 主干模型：Self-MM
- 随机种子：1111、1112、1113
- 结果形式：三个随机种子的均值 ± 总体标准差
- `Acc-2`、`Acc-3`、`Acc-5`、`F1`、`Corr` 越大越好；`MAE`、`Loss` 越小越好。

四种模型设置如下：

1. Self-MM：原始基线。
2. Self-MM + MW：仅加入模态自适应权重机制。
3. Self-MM + EP：仅加入情绪原型引导机制。
4. Self-MM + MW + EP：同时加入两个模块，即完整模型。
5. Refined：为门控加入温度和熵下限约束，并将正负二原型扩展为五个情绪强度原型。

## 三种子实验结果

| 模型 | Acc-2 ↑ | Acc-3 ↑ | Acc-5 ↑ | F1 ↑ | MAE ↓ | Corr ↑ | Loss ↓ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Self-MM | 76.95 ± 0.27 | 64.11 ± 0.71 | **43.76 ± 0.64** | 76.98 ± 0.26 | **41.98 ± 0.92** | 58.11 ± 1.11 | 42.26 ± 1.43 |
| Self-MM + MW | 77.90 ± 0.36 | 65.57 ± 0.20 | 42.16 ± 0.85 | 78.02 ± 0.48 | 42.85 ± 1.13 | 58.10 ± 0.77 | 42.84 ± 1.37 |
| Self-MM + EP | 77.68 ± 1.35 | 65.43 ± 0.18 | 42.67 ± 0.36 | 77.73 ± 1.27 | 42.56 ± 1.14 | 58.57 ± 1.36 | 43.56 ± 2.38 |
| Self-MM + MW + EP | 78.41 ± 1.29 | 64.92 ± 1.32 | 43.33 ± 1.17 | 78.48 ± 1.15 | 42.03 ± 1.02 | 58.30 ± 2.09 | **41.95 ± 1.13** |
| Refined | **80.23 ± 0.45** | **66.01 ± 0.68** | 43.62 ± 2.03 | **80.06 ± 0.53** | 42.15 ± 0.93 | **58.73 ± 1.24** | 42.11 ± 0.87 |

## 结果分析

与原始 Self-MM 相比，完整模型的 Acc-2 和 F1 分别提升 1.46 和 1.50 个百分点，说明两个模块联合使用能够增强模型对情绪极性的区分能力。完整模型还取得了最低 Loss，但 Acc-5 下降 0.43 个百分点，MAE 增加 0.05 个百分点，表明其对细粒度情绪强度的回归能力尚未稳定提升。

仅使用 MW 时，Acc-3 达到最高值 65.57，且 Acc-2 和 F1 均优于基线，说明自适应模态加权是分类性能提升的重要来源。仅使用 EP 时，Corr 达到最高值 58.57，但 MAE 和 Loss 没有改善，说明当前二原型约束能够帮助预测趋势，却可能对连续情绪强度施加了过强的离散化偏置。

两个模块联合后 Acc-2 和 F1 最优，说明 MW 与 EP 在情绪极性分类上具有一定互补性；但三次运行的标准差增大，因此后续应优先改善训练稳定性，并考虑将正、负二原型扩展为多个情绪强度原型。

精炼版完成上述改进后，Acc-2、Acc-3 和 F1 分别达到 80.23、66.01 和 80.06，相比原始 Self-MM 提升 3.28、1.90 和 3.08 个百分点；Corr 提升 0.62 个百分点。Acc-2 与 F1 的标准差也分别由上一完整模型的 1.29、1.15 降至 0.45、0.53，说明门控温度和熵约束提高了分类稳定性。Acc-5 较基线低 0.14 个百分点，MAE 高 0.17 个百分点，因此多原型尚未在三种子平均意义上显著改善细粒度回归；其 Acc-5 标准差为 2.03，仍需进一步优化原型监督或原型数量。

## 复现实验命令

```powershell
& D:\MMSA-CH-SIMS\.venv\Scripts\python.exe D:\MMSA-CH-SIMS\run_self_mm_aegm_sims.py --variant gate --seeds 1111 1112 1113 --gpu 0
& D:\MMSA-CH-SIMS\.venv\Scripts\python.exe D:\MMSA-CH-SIMS\run_self_mm_aegm_sims.py --variant prototype --seeds 1111 1112 1113 --gpu 0
& D:\MMSA-CH-SIMS\.venv\Scripts\python.exe D:\MMSA-CH-SIMS\run_self_mm_aegm_sims.py --variant both --seeds 1111 1112 1113 --gpu 0
& D:\MMSA-CH-SIMS\.venv\Scripts\python.exe D:\MMSA-CH-SIMS\run_self_mm_aegm_sims.py --variant refined --seeds 1111 1112 1113 --gpu 0
```

对应结果目录分别为 `experiments/self_mm_gate`、`experiments/self_mm_prototype`、`experiments/self_mm_aegm` 和 `experiments/self_mm_refined`。
