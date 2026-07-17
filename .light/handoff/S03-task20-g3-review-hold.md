---
session_no: S03
contract_version: 2
suggested_title: "[T-AFFC] S04 复核任务20补交HANDOFF_20并裁定G3"
parent_session: S02
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-18
---

# S03 任务20 G3独立审查交接卡

## 当前裁定

- 主仓库现实：`origin/main@b89d8dc1d62b5d6ea7b07b1d30cc8f19224c030d`，工作区审查前clean。
- 机器证据已独立复核：task20环境56/56测试通过，`validate_work_log.py`通过，`run_preparation_checks.py`无blocking checks且`formal_model_work_ready=true`，compileall和diff check通过。
- `TASK20_EXECUTION_EVIDENCE=ACCEPTED_FOR_G3_REVIEW`。
- `G3=HOLD_FOR_SUPPLEMENT`，尚未PASS或REJECT。
- 阻塞项：总纲任务20必需产出`HANDOFF_20.md`在`b89d8dc`中缺失；强基线是项目重实现，不得写成VC-CSA官方复现。
- 任务30冻结；任务50五种子/bootstrap仍未完成。
- I3D许可、官方revision、权利方身份/fixity仍未知，`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`持续传播。

## 已审查证据

- `TASK20_G3_EVIDENCE_PACKAGE_20260718.md`
- `BASELINE_TABLE_V1.md`
- `TASK20_BASELINE_EXECUTION_AUDIT.md`
- `experiments/EXPERIMENT_REGISTRY.md`
- `configs/task20/run-manifest.schema.json`
- `configs/task20/tuning-plan-v1.json`
- 总纲v1.16任务20/G3条款

## 下一轮必须完成

1. 任务20补交与`b89d8dc`及证据hash绑定的`HANDOFF_20.md`，包含冻结输入、split、指标、调参预算、run/replay范围、已完成/未完成项、VC-CSA失败状态和资产风险。
2. 00独立复核补交文件与主仓库新commit，确认没有提交run bundle、I3D `.npy`、模型权重、本机路径或可逆受限资产。
3. 补证闭合后，再裁定`G3=PASS_WITH_LIMITATIONS`或`G3=REJECT`；此前不得创建任务30。

## 接续提示词

你是新的“00-T-AFFC总控”项目，接替S03。先读取`AGENTS.md`、`WORK_RECORD_POLICY.md`、`WORK_LOG.md`末条和本卡；刷新`origin/main`与任务20线程实时状态。当前不要把任务20自报READY当成G3 PASS：G3处于`HOLD_FOR_SUPPLEMENT`，因为`HANDOFF_20.md`缺失。仅在补交文件与提交hash核对通过后独立作最终G3裁定。继续保留I3D资产未知许可/revision/fixity、VC-CSA官方复现失败、单种子边界和任务50未完成；G3前不得创建任务30。会话收尾继续新建下一张`.light/handoff/S<NN>-*.md`并打印接续提示词。
