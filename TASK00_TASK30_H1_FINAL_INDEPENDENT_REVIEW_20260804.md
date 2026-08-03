# Task30 H1 最终独立审核裁定

> 版本：v1.0  
> 日期：2026-08-04（Asia/Shanghai）  
> 审核方：00-T-AFFC总控03  
> 对象：Task30 `019fbdaa-01aa-7f60-9828-920d4a397ba5`  
> 科学总纲：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.21，第5节H1开发门  
> 最终裁定：`CLOSED_NOT_PASSED`

## 1. 裁定摘要

00接受Task30冻结开发包作为可审计的**开发阶段负结果证据**，但不接受H1为已通过。精确状态如下：

- Task30任务状态：`CLOSED_NOT_PASSED`；
- H1开发门状态：`NOT_PASSED_MECHANISM_NOT_STABLE`；
- 正式H1状态：`NOT_ADJUDICATED_ON_FORMAL_TEST`；
- 证据身份：永久为`DEVELOPMENT_EVIDENCE_ONLY`；
- Task30修复批次：`NOT_AUTHORIZED`；
- Task40：`NOT_CREATED_BLOCKED_H1_NOT_PASSED`。

本次“关闭”仅表示实现、证据包、失败边界和交接义务已达到可审计收口标准，不表示评论特权监督机制得到科学支持。正式test未materialize，Task50的五种子正式推断未执行，故不得把本裁定写成正式假设拒绝，也不得把开发指标写入论文正式结果。

## 2. 审核对象与Git边界

独立`git fetch origin`后核验：

- 基线：`origin/main@540c8d3a883d61e51b59d7d1a9937f06ec0f99db`；
- 冻结ref：`task30-h1-final-20260803`；
- 冻结commit：`9086bd537b36cad5635eaa9db81aaeb6756b4088`；
- 冻结范围：相对基线ahead 13，33个文件，4815行新增、25行删除；
- 00导入：只以冻结ref执行`--no-ff`合并，合并commit为`26df7c6fc305d5d57dbff3bfc107dadcc3f33185`。

Task30实时worktree分支在冻结后又前进到`9c606a5149a783bb408e6bc20f62955a28111f3f`（ahead 14）。该额外commit只追加审核请求日志，但不属于冻结ref，未进入本次审核或合并。由此，用户回交的`9086bd...`是正确的冻结对象，但不是审核时worktree分支的实时HEAD；两者不得混写。

冻结差异只包含Task30代码、配置、测试、环境锁、非秘密冻结摘要、报告和交接材料。未发现评论正文、逐样本私有预测、模型字节、I3D资产、凭据、秘密链接或私有绝对路径进入Git。`git diff --check origin/main...9086bd...`通过。

## 3. 独立fixity核验

| 对象 | 独立复算SHA-256 | 结果 |
|---|---|---|
| `HANDOFF_30.md` | `4b755d16e6773854a4efdd1fd8bec2b1e3dc8b30f27be8a9b91b45173c23113c` | MATCH |
| `TASK30_DATA_FLOW.md` | `c51360cec948b162620fbbaf8eceaac63f7d566cfa6dab377c93c99d93e30c86` | MATCH |
| `completion-freeze.json` | `a286ac7ecda26b368cd0284e0b187957f28aef02225164011e3a77b24b08078f` | MATCH |
| `nonsecret-freeze.json` | `53064d09f8f728a6b4cff31aa45efc35583d31e65f50054d1b1cd5d80df8debf` | MATCH |
| `TASK30_H1_DEVELOPMENT_REPORT_20260801.md` | `e5c4c21f972c7a812411d642fc7b90b1b8e13f654c4287fae83c299d7ac73f2c` | MATCH |
| development matrix | `cd8b42add73c5984e396ae6eb597cf89439b8f420799ad0dd9fe253bf84acc02` | MATCH |
| dataset contract | `3df6b0e148ed4317c68ed3c6cd1ac3222ee783da1d1968c943b347493b169abd` | MATCH |

数据流审查确认：train评论只进入teacher；dev只用于开发选择且dev评论被阻断；formal test行未materialize；student推断只使用T0内容。该设计边界支持“未发现本批开发流程的评论特权泄漏”，但不能替代H1有效性证据。

## 4. 独立验证

在Task30 worktree使用其冻结专用Python 3.8.9环境重跑：

- Task30专项：53/53通过；
- 全仓单元测试：133/133通过；
- `scripts/validate_task30_completion.py`：PASS；
- `scripts/validate_work_log.py`：258条、0错误（258包含冻结ref之后、未合并的审核请求日志；冻结包自身为257条）；
- `git diff --check`：PASS。

通用`run_preparation_checks.py`返回exit 1，原因是该data-free worktree缺少相对路径`data/processed/HUMAN_GOLD/csmv/video_labels.v1.jsonl`；AGENTS指定主`.venv`也不存在。本审核不复制受限数据、不建立junction、不修改冻结validator，也不把该环境限制改写为通过。

敏感模式扫描首次因PowerShell正则转义错误而失败；改用正确的literal/regex模式后，冻结变更中的唯一盘符命中来自刻意检查不得出现`D:\\`的负向测试断言，未发现实际私有绝对路径。`rg`在当前控制器上返回Access denied，后续文本核验使用PowerShell `Select-String`完成。

冻结ref导入主工作区后再次验证：主`.venv`运行Task30专项53/53与completion validator均通过；同一主`.venv`运行全仓133项时有3项Task20 contract测试因环境缺少`jsonschema`而报错，未改写为通过。改用Task30冻结专用环境在主工作区重跑，全仓133/133通过。AGENTS规定的主工作区`run_preparation_checks.py`最终exit 0、`blocking_checks=[]`，同时诚实保留`formal_model_work_ready=false`和`faiss_available=false`；首次短窗口调用超时后已终止遗留进程并在独立长窗口复跑成功。

## 5. H1证据与反证

冻结开发结果中，privileged KD的JSD分别为：

- seed 20260802：0.1696667746299664；
- seed 20260803：0.1690302845140116；
- seed 20260804：0.17008342441104918；
- 三种子均值：0.16959349451834238。

相对soft distribution基线为3/3种子改善；但相对ordinary KD和错配teacher均只有2/3种子改善。seed 20260804相对ordinary KD为`-0.000003467921386557382`，相对错配teacher为`-0.00030376752502317417`。冻结报告还披露NLL/Brier并非一致改善，且高分歧/高噪声组存在弱点。ECE均值边界未恶化不足以消除上述机制稳定性反证。

总纲v1.21的H1开发门要求评论特权teacher相对最强content-only基线产生稳定改善。对ordinary KD和错配teacher的跨种子反证说明“特权评论信息被稳定、可隔离地蒸馏”没有得到支持。因此，本门不能以平均值、单一校准指标或相对较弱soft基线的3/3改善替代通过条件。

## 6. 后续约束

1. 不授权Task30继续调参或新增H1修复attempt；任何未来重开都必须由用户另行选择战略回路，并由00事前形成版本化预注册合同。
2. 不创建Task40；Task40依赖的teacher/student-v1与H1门未满足。
3. 不创建或启动Task50；本批没有formal test权限，也没有正式五种子推断。
4. `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md`继续保持v0.1.2、`MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS`、C1—C4=`TO_VERIFY`。Task30开发数值不得进入正式claim、结果表、排名或摘要/结论。
5. G1=`PASS`、G2=`PASS_WITH_ACCEPTED_ASSET_RISK`、G3=`PASS_WITH_LIMITATIONS`均不改变。I3D许可、官方revision、权利方包身份/fixity继续为`UNKNOWN/DEFERRED_ACCEPTED_RISK`，禁止确认式表述或再分发。
6. Task20 VC-CSA探索仍永久`NON_T0/INELIGIBLE`；本裁定不提升、连接或复用其证据，也不改变2026-08-31 23:59:59 +08:00受限存储可见层删除截止。

## 7. 最终结论

Task30以`CLOSED_NOT_PASSED`关闭。工程交付与失败证据可追溯，H1开发门未通过，正式H1未裁定；不授权修复，不允许Task40下游启动。该负结果必须作为方法降级与论文claim边界，而不是被隐藏、平均化或改写为成功。
