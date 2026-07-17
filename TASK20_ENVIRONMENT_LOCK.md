# Task 20 formal environment lock

Snapshot: 2026-07-17, independent environment `.venv-task20`.

| Component | Locked value |
|---|---|
| OS | Windows 10 build 26100, 64-bit |
| Python | 3.8.9 |
| GPU | NVIDIA GeForce RTX 3070 Ti Laptop GPU, 8192 MiB |
| Driver | 610.62 |
| CUDA runtime reported by PyTorch | 12.1 |
| cuDNN | 90100 |
| PyTorch | 2.4.1+cu121 |
| transformers | 4.30.2 |
| faiss | 1.7.4 |
| scikit-learn | 1.3.2 |
| CatBoost | 1.2.10 |
| LightGBM | 4.5.0 |
| MMSA | 2.2.1 |
| NumPy | 1.24.4 |

`pip check` returned `No broken requirements found.` CUDA availability and GPU import checks passed. `scripts/environment_smoke.py --profile formal-carm` returned `passed=true` with MMSA, CatBoost, faiss, sklearn, PyTorch and Transformers imports all true. The initial faiss import after installing only `faiss-cpu` failed with `ModuleNotFoundError: numpy`; the root cause was the intentionally empty independent environment. Installing the complete direct dependency set resolved the import.

Rebuild order:

```powershell
py -3.8 -m venv .venv-task20
.\.venv-task20\Scripts\python.exe -m pip install --upgrade pip==25.0.1
.\.venv-task20\Scripts\python.exe -m pip install --index-url https://download.pytorch.org/whl/cu121 torch==2.4.1+cu121
.\.venv-task20\Scripts\python.exe -m pip install -r requirements-task20-lock.txt
```

The I3D asset remains `DEFERRED_ACCEPTED_RISK`; environment readiness does not establish asset license, official revision, package identity, or rightsholder fixity.
