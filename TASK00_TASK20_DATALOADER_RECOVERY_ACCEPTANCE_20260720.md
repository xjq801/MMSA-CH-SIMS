# 00 Task20 DataLoader 恢复状态验收

日期：2026-07-20  
审查对象：`main@7d686dd2497b90099ac63596f531d3e8ef7286f9`  
审查来源：`WORK_LOG.md` WR-20260720-002、任务20实时任务状态、Git提交边界

## 裁定

`TASK20_DATALOADER_RECOVERY=ACCEPTED_RUNNING_NOT_COMPLETED`

00接受任务20对这次工程恢复的记录：保留原失败尝试，将远端作者启动器的 `num_workers` 从8降至0，并以同一唯一种子 `seed=3407` 重新启动。该裁定只确认恢复动作和当时的存活状态，不确认首个epoch、checkpoint、最终输出或实验结果。

## 独立复核到的证据

- `git fetch origin` 后，`main=origin/main=7d686dd2497b90099ac63596f531d3e8ef7286f9`。
- `7d686dd` 相对总控父提交 `48201e979eb5c96355a6e621fc9cedb9adb4a857` 只修改 `WORK_LOG.md`，新增WR-20260720-002；未修改复盘、S15、总纲、门报告或实验核心的tracked文件。
- 原失败保留为：epoch 1运行至step 4269/4692后，DataLoader worker被信号 `Killed` 终止；失败时远端RAM可用约85 GB。现有证据不支持把它写成GPU OOM。
- 恢复后任务20报告进程使用 `--num_workers 0` 并存活至约step 126/4692；当时GPU利用率约82%、显存约14518 MiB、RAM可用约82 GB。
- 原失败中的 `Loss_sum=0.1785` 和恢复运行中的约 `Loss_sum=0.3637` 都只是中途诊断值。首个epoch尚未完成，二者均不得进入结果表、claim或模型比较。
- 任务20报告bundled Python的工作日志校验通过：136条、latest=`WR-20260720-002`。准备检查仍因本地旧虚拟环境不可用、bundled Python缺PyYAML而不可完整复跑；本裁定不将其冒充为当前准备门通过。

00未直接登录远端实例，因此GPU、RAM、step和进程存活属于任务20报告并由tracked日志固定的运行时证据，不是00远端重跑结果。

## 身份、门与claim边界

- 实验身份继续永久为 `AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`。
- `FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`；不得进入T0、统一baseline、G3主证据、任务50或论文主张。
- 正式门不变：G1=`PASS`；G2协议/数据=`PASS_WITH_LIMITATIONS`；资产准入=`DEFERRED_ACCEPTED_RISK`；G3=`PASS_WITH_LIMITATIONS`。
- I3D许可、官方revision、权利方包身份/fixity仍为UNKNOWN；权利方否认或固定8210项hash/覆盖漂移仍触发 `ASSET_INVALIDATED_DO_NOT_REPORT`。
- `RUNTIME_SNAPSHOT=DEFERRED_NOT_STARTED`，只能在安全暂停或完成后按S13另行记录和验收。

## 后续验收条件

任务20可继续监控同一 `seed=3407` 恢复运行。下一次只在以下任一事件发生时追加证据：

1. 首个epoch真实完成并形成可核验checkpoint；
2. 训练完整完成并形成最小输出证据；
3. 进程再次失败、中断或资源状态显著变化。

在这些事件发生前，状态保持 `RUNNING_NOT_COMPLETED`。不得仅凭进程存活、部分step或中途loss升级为完成。
