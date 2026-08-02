# HANDOFF_30 — M4 评论教师与内容学生最终回交

## 1. 回交身份

- 状态：`SUBMITTED_H1_DEVELOPMENT_GATE_NOT_PASSED_AWAITING_00_REVIEW`
- 实际任务 ID：`019fbdaa-01aa-7f60-9828-920d4a397ba5`
- 分支：`codex/task30-h1`
- 当前上游锚点：`origin/main@349be41c34db5082cb238350956799acb478faef`
- Task30 完整实现与开发证据提交：`923dc1553f11f7b35a0e64d1caa2814215296042`
- 上游合并提交：`459ebe9fba57d3c65cdf4e40410f38e326030b64`
- Git 状态：提交仅在本地分支，尚未推送。
- 开发门裁定：`NOT_PASSED_MECHANISM_NOT_STABLE`
- Task40：`NOT_CREATED/BLOCKED_NOT_AUTHORIZED`

本回交只请求 00 独立复核 Task30 H1 开发门，不改写 G1—G3，不进入 Task40/50。

## 2. 执行范围与泄漏控制

- CSMV 保持 Task20 冻结 split：5,698 train / 837 dev / 1,675 test。
- teacher 只聚合 5,698 个 train 视频的 74,727 条合法反应；dev/test 评论正文从未提供给 teacher 或写入产物。
- student 在训练和推理均只读取 T0 冻结内容特征；正式 test 行未 materialize，未参与模型、温度、权重、早停、校准或超参选择。
- Task20 冻结评测核心未修改；没有 memory、retrieval、router、GNN、生成模块、闭源 LLM、远程 GPU、对象存储或数据外传。
- 没有保存或提交 I3D 数组、评论正文、模型权重、逐样本隐私预测、凭据或本机绝对路径。
- I3D 许可、官方 revision、权利方包身份/fixity 仍为 `UNKNOWN`；仅按既有 `DEFERRED_ACCEPTED_RISK` 做内部开发研究。

## 3. 已实现与验证的比较

以 TDD 先红后绿实现并测试：dev/test 评论不可达、错配 teacher、缺字段 fail-closed、非法/非有限/未归一化分布拒绝、动态数据集 head、train-only 聚合和确定性复跑。

公平开发矩阵包括 hard label、soft distribution、ordinary KD、comment-privileged KD、mismatched-comment control、soft Dirichlet，以及不可部署的 teacher-only train diagnostic。每个可部署 CSMV 行使用相同的 12-trial student 预算；温度和 KD 权重只在 train/dev 开发合同内选择。

实现文件与完整数值见 `TASK30_H1_DEVELOPMENT_REPORT_20260801.md`。主要代码入口为：

- `scripts/task30_data.py`
- `scripts/task30_models.py`
- `scripts/task30_teacher.py`
- `scripts/task30_training.py`
- `scripts/run_task30_h1_development.py`
- `scripts/task30_analysis.py`
- `scripts/task30_lai_gai.py`

## 4. CSMV 开发结果

seed 20260802 完成 72 个 student trials；837 条 dev 私有预测未纳入 Git。选中指标如下：

| 方法 | JSD ↓ | NLL ↓ | Brier ↓ | ECE ↓ | ACE ↓ |
|---|---:|---:|---:|---:|---:|
| hard | 0.180825 | 1.790076 | 0.239266 | 0.041093 | 0.045672 |
| soft | 0.172843 | **1.703714** | 0.218402 | 0.048944 | 0.061966 |
| ordinary KD | 0.171793 | 1.712183 | 0.219297 | 0.041235 | 0.060414 |
| privileged KD | **0.169667** | 1.723492 | 0.220087 | **0.028594** | **0.052400** |
| mismatch | 0.171766 | 1.714517 | 0.218371 | 0.044501 | 0.064686 |
| Dirichlet | 0.172688 | 1.706831 | **0.213503** | 0.072300 | 0.067911 |

冻结选中配置后，privileged KD 相对 soft 的 JSD 收益在 3/3 development seeds 为正，均值 `0.0030668`；但相对 ordinary KD 和 mismatch 均仅 2/3 为正。NLL 相对 soft 在 3/3 seeds 变差，均值 `+0.0179915`。高目标熵和高标签噪声代理组中 privileged KD 也在 3/3 seeds 变差。因此无法稳定隔离“正确 train 评论”带来的特异机制收益。

teacher-only 仅为 train diagnostic（JSD 0.014677，ECE 0.347062），不是可部署或可比的 dev 上界。

## 5. 其他数据集边界

- LAI-GAI：无评论字段，H1=`NOT_APPLICABLE_COMMENT_FIELD_UNAVAILABLE`。仅运行真实支持的图像内容/校准开发边界：594 train / 127 dev，softmax JSD 0.054140，Dirichlet 0.054456，ECE 分别约 0.233/0.254；不能用作 H1 复刻。
- Video2Reaction 原生分支：H1=`NOT_APPLICABLE_DATA_NOT_RELEASED`；未从派生分布反推或伪造评论 teacher。
- 只有一个 comment-bearing H1 开发集；正式五种子、正式 test、paired bootstrap 与论文级推断均未运行。

## 6. 可复现身份

- CSMV full manifest：`330c9de88918a9cea5293ebf7c721d9f3c6738a9e7142c3a8fdff18cb86e3fa7`
- CSMV aggregate：`17f23df0b6d883fc01b7c6e35b2dd06930adad1d761064f13ac750c8f21a3e4d`
- same-seed 私有预测 SHA-256：`195e60290d867ca2ce75be75830bffb4bd808228f0786b9f65deb019e5ade53a`
- replay / seed03 / seed04 manifests：`7c37a51234051bb02bcb51fb18d3bf6b17b098e1bf5e1021870c8fe6e0c141b1` / `8d241df7dc1a04e04111de140f077d9c934a0a3434ecd80fc35c8f9c7a57e56d` / `c0c97dfe760e2a089c8235591e9af123f60d31031268a24336e62176ebed1e8b`
- LAI-GAI aggregate：`a972278f1b2101bc1a776d4cf9ae5049c25326a556290e487532c46fc8ed97a6`

同 seed replay 的预测逐字节一致；所有声明的 manifest artifact hash 均复核通过。运行使用本地 RTX 3070 Ti，观察显存低于 2.2 GiB，完整搜索约 18.5 分钟；不需要租赁或远程大算力。

## 7. 最终门禁

- Task30 专项：46/46 通过。
- 全仓回归：120/120 通过。
- `compileall`、Task30 matrix schema、Task20 handoff 22 项证据、`pip check`、`git diff --check`：通过。
- Light review gate：通过，0 findings。
- 同 seed replay：逐字节一致；workspace Python seed audit 六项机制齐全。
- `.venv-task30` 的 `validate_work_log.py`：通过。
- `.venv-task30` 的 `run_preparation_checks.py`：诚实失败，原因是本 worktree 不承载冻结相对路径 `data/processed/HUMAN_GOLD/csmv/video_labels.v1.jsonl`；真实开发只读绑定来自授权主工作区，未复制入 Git worktree。
- AGENTS 指定的主 `.venv` 两个入口：主 `.venv` 不存在，均在脚本启动前失败；未冒充主环境 ready。
- Python 3.8 下 Light seed 工具因 AST 兼容边界误报缺少 `PYTHONHASHSEED`；同一代码由 workspace Python 复核通过，且固定 seed replay 提供实际确定性证据。失败与通过均保留。

## 8. 向 00 请求的独立裁定

请 00 在以下开发证据身份下独立复核：

1. 接受 `NOT_PASSED_MECHANISM_NOT_STABLE`，关闭 Task30 H1 开发门且不创建 Task40；或
2. 在不接触 formal test 的前提下，书面授权一个预声明的 H1 范围内机制修复批次。

本结果不是 `H1_SUCCESS`，也不是正式 test 上的 `H1_REJECTED`。在 00 新授权前，Task30 不继续调参、不查看 test、不创建 Task40。
