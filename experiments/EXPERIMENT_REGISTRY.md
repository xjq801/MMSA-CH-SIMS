# 实验登记表

正式运行前先登记；每个实验只能由一个版本化配置启动。

| experiment_id | 日期 | 配置 | 数据版本 | split | T0/T+Δ | 唯一变化 | seed | 主指标 | 停止条件 | 状态 | 输出/日志 |
|---|---|---|---|---|---|---|---:|---|---|---|---|
| bootstrap-config-validation | 2026-07-14 | `configs/experiment.bootstrap.yaml` | pending_m1 | pending_m2 | T0 | 验证配置契约，不训练 | 20260714 | JSD | 泄漏检查失败 | VALIDATION_ONLY | 无模型输出 |

允许状态：`PLANNED`、`RUNNING`、`COMPLETED`、`FAILED`、`LEAKAGE_BLOCKED`、`VALIDATION_ONLY`。失败和被阻断的运行不得删除记录。
