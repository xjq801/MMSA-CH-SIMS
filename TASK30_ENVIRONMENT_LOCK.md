# Task30 independent environment lock

> Environment: `.venv-task30` (ignored local directory)  
> Created: 2026-08-01  
> Evidence scope: local Task30 TDD and development execution only  
> Readiness: `LOCAL_DEVELOPMENT_EXECUTION_READY_AND_USED`

## Locked runtime

| Component | Locked or observed value |
|---|---|
| Python | CPython 3.8.9 |
| PyTorch | 2.4.1+cu121 |
| CUDA runtime reported by PyTorch | 12.1 |
| cuDNN | 90100 |
| NumPy | 1.24.4 |
| jsonschema | 4.23.0 |
| PyYAML | 6.0.3 |
| scikit-learn | 1.3.2 (Task20 frozen regression compatibility) |
| Pillow | 10.4.0 (LAI-GAI T0 image boundary only) |
| GPU | NVIDIA GeForce RTX 3070 Ti Laptop GPU, 8192 MiB |
| Driver | 610.62 |
| OS observation | PowerShell `10.0.26200.0`; Python platform `Windows-10-10.0.26100-SP0` |
| dtype / AMP | float32 development default; AMP disabled until explicitly configured and tested |

The exact package snapshot is `requirements-task30-lock.txt`. `pip check` returned `No broken requirements found.` CUDA availability was true and the GPU name matched the table. Full CSMV development and LAI-GAI boundary runs completed on this local GPU; observed peak memory remained below 2.2 GiB, so no rented or remote compute was required.

## Rebuild

```powershell
py -3.8 -m venv .venv-task30
.\.venv-task30\Scripts\python.exe -m pip install --upgrade pip==25.0.1
.\.venv-task30\Scripts\python.exe -m pip install --index-url https://download.pytorch.org/whl/cu121 torch==2.4.1+cu121
.\.venv-task30\Scripts\python.exe -m pip install -r requirements-task30-lock.txt
```

Because the lock includes the CUDA-tagged torch package, the official PyTorch CUDA 12.1 index is required for that package. No remote GPU, paid service, external tracker or credential is part of this environment.

## Reproducibility boundary

- Unit tests use CPU tensors unless a test explicitly says otherwise.
- A real run must set the process-level hash seed before Python starts and record Python, NumPy, PyTorch, CUDA, cuDNN, DataLoader and deterministic-algorithm settings.
- Same-seed same-environment replay was executed and produced byte-identical private predictions (`SHA-256 195e60290d867ca2ce75be75830bffb4bd808228f0786b9f65deb019e5ade53a`). This supports only that environment identity and does not prove cross-platform or cross-release bitwise reproducibility.
- `.venv-task30` is independent. It does not inherit or assert readiness from the missing main `.venv` or the absent Task20 local environment.

## Asset and input boundary

I3D licence, official revision, rightsholder package identity and fixity remain `UNKNOWN` under `DEFERRED_ACCEPTED_RISK`. The environment itself contains no I3D array, comment body, model weight, credential or private path. An approved local main-workspace binding was consumed read-only; generated predictions remain in Git-ignored local results and are prohibited from redistribution. No model weights were saved.
