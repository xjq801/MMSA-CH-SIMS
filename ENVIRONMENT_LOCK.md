# 当前环境锁定记录

> 快照日期：2026-07-14  
> 用途：保存现有历史实验环境，确保当前脚本和结果可追溯。此文件不代表后续 CARM 正式环境已冻结。

## 1. 操作系统与解释器

- 平台：Windows 10 build 26100，64 位
- Python：3.8.9
- Python 路径：`D:\MMSA-CH-SIMS\.venv\Scripts\python.exe`
- pip：25.0.1
- 完整包版本：`requirements-lock.txt`

## 2. 深度学习与 GPU

- PyTorch：2.4.1+cu121
- PyTorch CUDA：12.1
- cuDNN：90100
- CUDA 可用：是
- GPU：NVIDIA GeForce RTX 3070 Ti Laptop GPU
- 显存：8192 MiB
- NVIDIA 驱动：610.62

## 3. 关键研究依赖

- MMSA：2.2.1
- CatBoost：1.2.10
- transformers：4.30.2
- scikit-learn：1.3.2
- numpy：1.24.4
- pandas：1.5.3
- scipy：1.10.1
- matplotlib：3.7.5

## 4. 重建命令

```powershell
py -3.8 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip==25.0.1
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

PyTorch 的 CUDA wheel 在不同平台可能需要使用 PyTorch 官方索引单独安装。重建后必须运行下列验证：

```powershell
.\.venv\Scripts\python.exe -c "import torch, catboost, transformers, sklearn, MMSA; print(torch.__version__); print(torch.cuda.is_available())"
```

## 5. 环境边界

- 当前 Python 3.8 环境用于保存和复现现有 MMSA/历史基线，不直接作为十个月新主线的永久环境承诺。
- CSMV、iNews/NEmo+ 和 CARM 正式开发环境应在 M1 数据可行性门通过后另建环境并独立锁定，避免破坏历史基线。
- 新环境不得原地升级本 `.venv`；建议使用新的虚拟环境名，并保存 Python、CUDA、依赖、硬件和安装来源。
- `requirements-lock.txt` 是包版本快照，不包含操作系统驱动、外部二进制、数据文件或模型权重。

## 6. 2026-07-14 验收状态

- `python -m pip check`：通过，无破损依赖。
- 历史环境最小导入：torch、CatBoost、transformers、scikit-learn、MMSA通过；CUDA可用。
- faiss：未安装。因此正式CARM环境仍为`BLOCKED_M1`，不得宣称已经冻结或可复现。
- 空环境重建：尚未执行。原因是正式数据/检索方案未通过M1门，且当前锁文件仅代表历史环境；M1通过后应新建独立环境、安装冻结的faiss后端并在空环境运行相同smoke check。
- 可重复检查：`python scripts/environment_smoke.py --profile historical`；正式环境使用`--profile formal-carm`。
