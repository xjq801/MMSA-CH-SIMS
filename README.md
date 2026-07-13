# CH-SIMS / Self-MM 基线复现

## 环境

- Python 3.8
- PyTorch 2.4.1 + CUDA 12.1
- MMSA 2.2.1（官方仓库）
- GPU：NVIDIA GeForce RTX 3070 Ti Laptop GPU

## 目录

```text
D:\MMSA-CH-SIMS
├─ .venv\
├─ MMSA\
├─ data\SIMS\Processed\unaligned_39.pkl
├─ models\bert-base-chinese\
├─ run_self_mm_sims.py
├─ saved_models\
├─ results\
└─ logs\
```

## 运行

```powershell
cd D:\MMSA-CH-SIMS
.\.venv\Scripts\python.exe .\run_self_mm_sims.py
```

脚本使用官方CH-SIMS训练、验证和测试划分，运行Self-MM，随机种子为1111、1112和1113。

## 数据校验

`unaligned_39.pkl` 的SHA-256应为：

```text
c9e20c13ec0454d98bb9c1e520e490c75146bfa2dfeeea78d84de047dbdd442f
```

样本数：训练1368、验证456、测试457。

## 本机复现结果

测试集包含457条样本。三个随机种子的结果如下：

| Seed | Acc-2 | Acc-3 | Acc-5 | F1 | MAE | Corr |
|---:|---:|---:|---:|---:|---:|---:|
| 1111 | 77.24% | 64.99% | 44.64% | 77.29% | 0.4085 | 0.5944 |
| 1112 | 76.59% | 64.11% | 43.54% | 76.65% | 0.4310 | 0.5672 |
| 1113 | 77.02% | 63.24% | 43.11% | 77.00% | 0.4200 | 0.5818 |
| 均值±标准差 | 76.95±0.27% | 64.11±0.71% | 43.76±0.64% | 76.98±0.26% | 0.4198±0.0092 | 0.5811±0.0111 |

MMSA仓库公开表格中的Self-MM参考值为Acc-2 80.04%、Acc-3 65.47%、Acc-5
41.53%、F1 80.44%、MAE 0.4250、Corr 0.5952。本机结果与其处于同一量级：
Acc-2和F1分别低3.09、3.46个百分点，Acc-5高2.23个百分点，MAE低0.0052
（MAE越低越好）。差异可能来自PyTorch、CUDA、Transformers版本、官方汇总随机种子
数量以及仓库代码更新。

模型保存在：

```text
D:\MMSA-CH-SIMS\saved_models\self_mm-sims.pth
```

结果和完整日志保存在：

```text
D:\MMSA-CH-SIMS\results\normal\sims.csv
D:\MMSA-CH-SIMS\logs\self_mm-sims.log
```

## 兼容性说明

官方MMSA 2.2.1的最新版源码在一个函数注解中使用了Python 3.10的联合类型写法，
但项目元数据声明支持Python 3.8。本项目仅将该注解改写为等价的`typing.Union`，没有
修改模型、损失函数、数据处理或训练逻辑。
