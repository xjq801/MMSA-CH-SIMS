# HANDOFF_30 — M4评论教师与内容学生最终回交

## 1. 回交身份

- 状态：`SUBMITTED_H1_DEVELOPMENT_GATE_NOT_PASSED_AWAITING_00_REVIEW`
- 实际任务ID：`019fbdaa-01aa-7f60-9828-920d4a397ba5`
- 分支：`codex/task30-h1`
- 最新上游锚点：`origin/main@540c8d3a883d61e51b59d7d1a9937f06ec0f99db`
- Task30补缺实现提交：`9adcc0a59d31d16c86e50891ff53fad916130f95`
- Task30非敏感冻结与报告提交：`0665682281ae435c2e021d2c8722a6ec9b75a97b`
- Git同步：以上提交只在本地分支，尚未推送
- Task30自报开发门：`NOT_PASSED_MECHANISM_NOT_STABLE`
- Task40：`NOT_CREATED/BLOCKED_NOT_AUTHORIZED`

本回交只请求00独立复核Task30 H1开发门；不改写G1—G3，不进入Task40/50。

## 2. 完成范围与泄漏控制

- CSMV保持Task20冻结split：5,698 train / 837 dev / 1,675 test。
- teacher只聚合5,698个train视频的74,727条合法反应；dev/test评论正文未提供给teacher或写入产物。
- student训练和推理只读取T0合法内容特征；正式test行未materialize，未参与模型、温度、权重、阈值、早停、校准或超参选择。
- Task20冻结评测核心未修改；未引入memory、retrieval、router、GNN、生成模块、闭源/付费LLM、远程GPU、对象存储或数据外传。
- 未提交或再分发I3D数组、评论正文、模型权重、逐样本隐私预测、凭据或本机绝对路径。
- I3D许可、官方revision、权利方包身份与fixity仍为`UNKNOWN`，只按既有`DEFERRED_ACCEPTED_RISK`做内部开发研究。

## 3. 已交付实现

- 配置驱动的`DatasetRuntimeSpec`提供动态类别顺序、split、item、target、response-count字段与数据集特定head；CSMV运行入口不再硬编码八类或目标字段。
- train-only评论级反应编码与视频级分布聚合，冻结类别质量、稀疏性、评论数、缺失标签、经验teacher置信度与异常审计。
- 最小content-only student、softmax/Dirichlet head、ordinary teacher、comment-privileged teacher与确定性错配teacher。
- 公平比较hard label、soft distribution、ordinary KD、comment-privileged KD、mismatch control和Dirichlet；每行相同12-trial student预算。
- 完整数值/归一化/梯度fail-closed检查，2473行student/teacher epoch历史，6个本地私有入选model states及规范张量hash。
- 评论数、目标熵、标签噪声代理和train teacher置信度机制诊断；不打开dev评论制造讽刺案例。
- run bundle v2记录时间、argv、exit code、矩阵行、seed角色、输入/代码hash、clean/dirty与diff hash。
- tracked非敏感冻结：`experiments/task30-h1-development-v1/`；专用门：`scripts/validate_task30_completion.py`。

## 4. 真实CSMV开发结果

seed 20260802在干净代码提交上完成72个student trials：

| 方法 | JSD ↓ | NLL ↓ | Brier ↓ | ECE ↓ | ACE ↓ |
|---|---:|---:|---:|---:|---:|
| hard label | 0.180825 | 1.790076 | 0.239266 | 0.041093 | 0.045672 |
| soft distribution | 0.172843 | **1.703714** | 0.218402 | 0.048944 | 0.061966 |
| ordinary KD | 0.171793 | 1.712183 | 0.219297 | 0.041235 | 0.060414 |
| comment-privileged KD | **0.169667** | 1.723492 | 0.220087 | **0.028594** | **0.052400** |
| mismatch control | 0.171766 | 1.714517 | 0.218371 | 0.044501 | 0.064686 |
| Dirichlet | 0.172688 | 1.706831 | **0.213503** | 0.072300 | 0.067911 |

teacher-only为train diagnostic（JSD 0.014677、ECE 0.347062），固定`NOT_COMPARABLE_DEV_RESPONSES_PROHIBITED`，不是可部署或可比dev上界。

冻结配置三development seeds的privileged JSD为0.169667/0.169030/0.170083，均值0.169593。相对soft的JSD收益3/3为正；相对ordinary KD和mismatch只在2/3为正，seed 20260804分别为-0.000003与-0.000304。平均ECE 0.036872未恶化，但正确评论的特异机制优势不稳定，因此不能标记H1成功。

teacher经验置信度均值0.49583；低/中/高三分位的train teacher拟合JSD收益为0.04253/0.04797/0.05415，Pearson相关0.16516。该分析只属于train teacher拟合诊断，不是dev student置信度分层收益。

## 5. 其他数据集与不可伪造边界

- LAI-GAI无评论字段，H1=`NOT_APPLICABLE_COMMENT_FIELD_UNAVAILABLE`；只保留真实内容/校准边界，不能用作H1复刻。
- Video2Reaction原生H1=`NOT_APPLICABLE_DATA_NOT_RELEASED`；未从派生分布反推或伪造评论teacher。
- 第二comment-bearing公开集=`NOT_EVALUABLE_DATA_NOT_RELEASED`。
- 讽刺=`NOT_EVALUABLE_DEV_RESPONSE_TEXT_UNREACHABLE`。
- 跨域H1=`NOT_APPLICABLE_NO_SECOND_COMMENT_BEARING_DATASET`。
- 00独立审核=`EXTERNAL_REVIEW_REQUIRED_NOT_SELF_APPROVABLE`。

这些是政策、数据发布与职责边界，不得伪写为已完成实验。

## 6. 复现身份

| 证据 | SHA-256 |
|---|---|
| full manifest | `97d50c320eda6eec6c6bf8fa44d36b17b0fe3d64dd444fee43fed0ee930b6ce0` |
| full aggregate | `70c6275693ced69f9955e370e2af9a3b87497358ec781487998628a659e5d1f8` |
| replay manifest | `145b7a222d4158a402ddc7499a9137fa7785225b1221f03b9ab95843d81f20bc` |
| seed-20260803 manifest | `41295136f5e890a4adce2353e5e4dbd763f53c6e42104b4853ea311378a3ff6b` |
| seed-20260804 manifest | `53ad21a9c2fb3173f70520e210632a0b1aaa4207719ae7aaecca16c5eb115a4b` |
| same-seed私有预测 | `195e60290d867ca2ce75be75830bffb4bd808228f0786b9f65deb019e5ade53a` |
| model hash index | `7bd83b2b4bfba03f3d8b42eaf85c3bf44aa631e1e84480e074cf9a8e184d5085` |
| full训练历史 | `cdb09668b0587a9069e81963cd07f3e289b305dc79f34e111735ef4d28db0ade` |

full/replay预测逐字节一致，六个模型文件与canonical tensor hash全部一致，六行dev指标一致。四个run均`dirty=false`、exit 0、`test_adaptation=false`。全部使用本地RTX 3070 Ti；完整搜索约32分40秒，不需要租赁或远程大算力。

## 7. 最终门禁

- Task30专项：50/50通过。
- 全仓回归：130/130通过。
- `compileall`、Task30 matrix schema、Task20 handoff 22项、`pip check`、`git diff --check`：通过。
- Task30非敏感完成门：通过。
- Light review：0 findings；Python 3.13 seed audit七项机制齐全、0 missing。Python 3.8静态工具曾误报缺`PYTHONHASHSEED`，实际代码有显式赋值；失败保留。
- `.venv-task30`的`validate_work_log.py`：253条、0 errors、通过。
- `.venv-task30`的通用`run_preparation_checks.py`：失败，因为本worktree不承载冻结相对HUMAN_GOLD输入；真实run使用hash绑定的授权主工作区只读输入，未复制受限数据。
- AGENTS指定主`.venv`的两个入口：主`.venv`不存在，均在脚本启动前exit 127；未冒充主环境ready。

## 8. 向00请求的独立裁定

请00在development-only身份下独立选择：

1. 接受`NOT_PASSED_MECHANISM_NOT_STABLE`，关闭Task30 H1开发门且不创建Task40；或
2. 在不接触formal test的前提下，书面授权一个预声明、仍属于H1范围的机制修复批次。

本结果不是`H1_SUCCESS`，也不是formal test上的`H1_REJECTED`。在00新授权前，Task30停止调参、不查看test、不创建Task40。
