# 20-M3 progress

## 2026-07-17

- 完成审计、计划隔离与第一批实现。
- 新增 `scripts/task20_baseline.py`、`tests/test_task20_baseline.py`、`configs/task20-baseline-v1.yaml`、`requirements-task20-lock.txt`。
- 已通过：`python -m unittest -v tests.test_task20_baseline`（3/3）；`python -m compileall -q scripts tests`；`scripts/run_preparation_checks.py` 返回无 blocking checks，但 formal 环境仍 BLOCKED_M1。
- 已记录失败：独立环境 pip 安装因代理不可连接失败；不得写成 faiss 已解决。
