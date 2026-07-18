# 实验登记表

正式运行前先登记；每个实验只能由一个版本化配置启动。

| experiment_id | 日期 | 配置 | 数据版本 | split | T0/T+Δ | 唯一变化 | seed | 主指标 | 停止条件 | 状态 | 输出/日志 |
|---|---|---|---|---|---|---|---:|---|---|---|---|
| bootstrap-config-validation | 2026-07-14 | `configs/experiment.bootstrap.yaml` | pending_m1 | pending_m2 | T0 | 验证配置契约，不训练 | 20260714 | JSD | 泄漏检查失败 | VALIDATION_ONLY | 无模型输出 |
| task20-minimum-baselines-dev-smoke | 2026-07-17 | `configs/task20/baseline-common.json` | dataset-v1 | group_by_video_v1 train/dev | T0 | 最低基线统一评测smoke | 20260717 | JSD | E0或合同失败 | VALIDATION_ONLY | `results/task20-minimum-baselines-smoke-20260717-b/` |
| task20-legacy48-formal-rerun | 2026-07-17 | `configs/task20/tuning-plan-v1.json` | CUC-IGPE-v2 legacy | formal split未分配 | 非T0 | CatBoost/HGB/LightGBM | 20260717 | JSD | 数据协议不匹配 | FAILED | `TASK20_BASELINE_EXECUTION_AUDIT.md` |
| task20-vccsa-official-reproduction | 2026-07-17 | fixed official revision audit | CSMV official revision | official comment split | 非T0目标评论 | VC-CSA | 20260717 | JSD | 官方代码或T0合同不满足 | FAILED | `TASK20_BASELINE_EXECUTION_AUDIT.md` |
| task20-pooled-mlp-local-cpu-smoke-a | 2026-07-17 | `configs/task20/tuning-plan-v1.json` | dataset-v1 + pooled-i3d-v1 | group_by_video_v1 train/dev | T0 | 1 trial / 2 epochs / CPU | 20260717 | JSD | schema或E0失败 | VALIDATION_ONLY | `results/task20-pooled-mlp-smoke-local-cpu-v2/` |
| task20-pooled-mlp-local-cpu-smoke-b | 2026-07-17 | `configs/task20/tuning-plan-v1.json` | dataset-v1 + pooled-i3d-v1 | group_by_video_v1 train/dev | T0 | 同seed独立复跑 | 20260717 | JSD | 预测hash不一致 | VALIDATION_ONLY | `results/task20-pooled-mlp-smoke-local-cpu-v3/` |
| task20-remote-a30-runtime-preflight | 2026-07-17 | environment preflight | 无数据输入 | 不适用 | 不适用 | CUDA最小矩阵运算 | 20260717 | 不适用 | 30秒未完成 | FAILED | `TASK20_BASELINE_EXECUTION_AUDIT.md` |
| task20-temporal-attention-local-cpu-smoke-a | 2026-07-17 | `configs/task20/tuning-plan-v1.json` | dataset-v1 + restricted I3D local read-only | group_by_video_v1 train/dev smoke subset | T0 | 32 train / 16 dev / 1 trial / 2 epochs / CPU | 20260717 | JSD | schema、E0或合同失败 | VALIDATION_ONLY | `results/task20-temporal-attention-smoke-local-cpu-v1/` |
| task20-temporal-attention-local-cpu-smoke-b | 2026-07-17 | `configs/task20/tuning-plan-v1.json` | dataset-v1 + restricted I3D local read-only | group_by_video_v1 train/dev smoke subset | T0 | 同seed独立复跑 | 20260717 | JSD | 预测/指标/选择hash不一致 | VALIDATION_ONLY | `results/task20-temporal-attention-smoke-local-cpu-v2/` |
| task20-remote-a30-runtime-remediation | 2026-07-17 | isolated Python 3.8 execution environment | 无数据输入 | 不适用 | 不适用 | 校验公开CUDA wheel并安装后执行最小矩阵 | 20260717 | 不适用 | 实例失联前未完成CUDA smoke | FAILED | `TASK20_BASELINE_EXECUTION_AUDIT.md` |
| task20-legacy48-native-rerun-v1 | 2026-07-17 | `configs/task20/legacy-48-native-rerun-v1.json` | CUC-IGPE-v2@legacy-local，2787条 | legacy48_publisher_hash_v1 train/dev/test | LEGACY_POST_HOC_NON_T0 | CatBoost/HGB/LightGBM各12-trial原生二分类兼容重跑 | 20260717 | Macro-F1 | dev选择后test每模型一次 | COMPLETED | `results/task20/legacy48-native-rerun-v1/`（本机忽略）/ `TASK20_BASELINE_EXECUTION_AUDIT.md` |
| task20-temporal-attention-formal-dev-v1 | 2026-07-17 | `configs/task20/tuning-plan-v1.json` | dataset-v1 + restricted I3D local read-only | group_by_video_v1 train/dev=5698/837 | T0 | 12-trial frozen full-sequence temporal attention dev选择 | 20260717 | JSD | patience 20 / max 200 epoch | COMPLETED | `results/task20/temporal-attention-formal-dev-task7-v1/`（本机忽略） |
| task20-temporal-attention-formal-test-v1 | 2026-07-17 | frozen dev selection SHA256 `dce53eeb...c97dfbf` | dataset-v1 + restricted I3D local read-only | group_by_video_v1 test=1675 | T0 | 选中配置一次性test前向，无test适配 | 20260717 | JSD | frozen config；test一次 | COMPLETED | `results/task20/temporal-attention-formal-test-task7-v1/`（本机忽略）/ `TASK20_BASELINE_EXECUTION_AUDIT.md` |
| task20-temporal-attention-formal-dev-replay-v1 | 2026-07-17 | `configs/task20/tuning-plan-v1.json` | dataset-v1 + restricted I3D local read-only | group_by_video_v1 train/dev=5698/837 | T0 | 与正式dev同环境同seed独立12-trial replay，不读取test | 20260717 | JSD | 四项核心产物hash不一致即失败 | COMPLETED | run id `temporal-attention-formal-dev-task15-replay-v1`（本机忽略）/ `TASK20_BASELINE_EXECUTION_AUDIT.md` |
| task20-vccsa-author-source-preflight-20260718 | 2026-07-18 | author fork `3e8c42608f4e89bc2082c55760aa63535e8e276a` | 未读取数据 | 作者原comment split待复现 | NON_T0_TARGET_COMMENT | 代码身份、语法与入口依赖预检，不训练 | 3407（作者默认，未运行） | 不适用 | 入口依赖或路径合同失败即停 | FAILED | compileall通过；`main.py --help`/`main_eval.py --help`因`en_vectors_web_lg`缺失exit 1；`TASK20_BASELINE_EXECUTION_AUDIT.md` |

允许状态：`PLANNED`、`RUNNING`、`COMPLETED`、`FAILED`、`LEAKAGE_BLOCKED`、`VALIDATION_ONLY`。失败和被阻断的运行不得删除记录。

历史实验不因本表建立而被追认成正式运行。既有代码与结果的证据资格统一见`legacy-experiment-classification.md`；其中目标评论、未来互动、全量图或随机split不合格结果不得补登记为`COMPLETED`。
