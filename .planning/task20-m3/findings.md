# 20-M3 findings

- 旧 `.venv` 为 Python 3.8.9，numpy 1.24.4、scikit-learn 1.3.2 可用，faiss 不可用。
- 独立 `.venv-task20` 已创建；pip 25.0.1 升级成功，但安装 `pytest`/`faiss-cpu` 因代理不可连接失败，环境保持未就绪。
- 任务20最小基线测试使用标准库 unittest，3/3 通过；compileall 通过。
- `run_preparation_checks.py` 真实结果：`blocking_checks=[]`，但 `formal_carm_environment.classification=BLOCKED_M1`、`faiss_available=false`、`formal_model_work_ready=false`。
