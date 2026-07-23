---
session_no: S18
contract_version: 2
suggested_title: "[T-AFFC] S19 calibrate Task30 runtime and authorize staged GPU budget"
parent_session: S17
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-23
---

# S18 compute budget estimate handoff

## 当前阶段

- G1—G3正式地基已完成；总纲v1.16剩余GPU主线为任务30、40和50。基于A30 24GB、¥2.20/GPU·小时形成G6预算估算；尚未授权新的租卡或付费执行。

## 已完成

- `COMPUTE_BUDGET_ESTIMATE_20260723.md` — 验证：逐段读取总纲第5—11节及任务30—50规格，并用Task20实测13.5分钟/12-trial基线和VC-CSA已知规模校准，给出470—755 GPU小时、¥1,034—1,661的正式主线区间。
- `WORK_LOG.md` WR-20260723-002 — 验证：记录估算假设、分项成本、并行策略和未包含费用，提交前运行工作日志校验。
- `.light/handoff/S18-compute-budget-estimate.md` — 验证：运行`handoff_contract.py --as-of 2026-07-23`并要求PASS。
- `origin/main` — 验证：`git fetch origin`、`git status --short --branch`和`git log`确认估算输入commit=`e2ab6e26f35a8726e4376b6060eb8f9d6d96cffb`，仅任务20所有的`tmp/`未跟踪。

## 工作区状态

- 写卡前`main=origin/main=e2ab6e26f35a8726e4376b6060eb8f9d6d96cffb`；新增预算报告、WR-20260723-002和本S18后工作区dirty/unpushed，待显式提交。
- `tmp/`仍为任务20所有，00未读取、暂存、移动或删除；本次没有租卡、创建实例或发生外部付费动作。

## 待用户回答

- none — 当前只是预算评估，没有发起付费动作；后续若要真正租卡，应按分阶段上限另行确认。

## 阻塞/风险

- 任务30/40尚未实现，1—2 A30小时/训练等价运行是基于冻结特征路线的规划假设，必须由首批3—5个smoke重新校准。
- 图片只给出GPU单价，存储、快照、流量和税费未知；报告金额仅为GPU小时，另建议10%—15%现金余量。
- 任务30→40→50存在硬依赖，不能用6卡长期并行消除开发和门审查时间；空闲开机将直接扩大费用。
- VC-CSA作者探索永久NON_T0/INELIGIBLE，90—180 GPU小时为可选额外成本，不得挤占正式主线或冒充G6证据。

## 必读文件

- `.light/handoff/S18-compute-budget-estimate.md`；
- `.light/passport.yaml`、`.light/project_card.md`；
- `COMPUTE_BUDGET_ESTIMATE_20260723.md`；
- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.16；
- `TASK20_BASELINE_EXECUTION_AUDIT.md`、`BASELINE_TABLE_V1.md`；
- `PROJECT_STATUS_RETROSPECTIVE_20260720.md`；
- 最新`WORK_LOG.md`和任务20实时任务。

## 下一步

1. 读任务20实时状态并完成其探索收尾，确认共享实验核心不再被修改或运行。
2. 验任务30创建条件并冻结首批3—5个A30 smoke的资源测量协议，用实测更新预算区间。
3. 写分阶段付费授权：开发阶段1卡、任务50三卡、最终独立矩阵短时六卡，并设置20%超支暂停门。

## 禁止

- 本卡不是当前事实；接续时必须先运行`git status --short --branch`、`git log`并读取任务20实时状态。
- 不得把预算估算写成已产生费用或已完成实验，不得在未授权前创建付费实例。
- 不得把GPU数量当作可以跳过任务30→40→50硬依赖的理由，不得长期空闲占用6卡。
- 不得把VC-CSA可选探索并入正式G6主线或论文claim，不得触碰任务20的`tmp/`或受限资产。
- 不创建IJCV J0—J2/JH1—JH3、任务25/65；任务20未收尾前不得创建任务30。

## Continuation prompt

You are the 00-T-AFFC total controller taking over S18. Read AGENTS.md and perform startup checks, then read the must-read files above. Refresh origin/main, git status, git log and task20 thread; this handoff is not current fact. Formal gates remain G1 PASS, G2 protocol/data PASS_WITH_LIMITATIONS, ASSET_ADMISSIBILITY DEFERRED_ACCEPTED_RISK and G3 PASS_WITH_LIMITATIONS. The current formal remaining GPU scope is Task30, Task40 and Task50. The planning estimate at A30 ¥2.20/GPU-hour is 470–755 GPU-hours and ¥1,034–1,661 for G6, with a recommended ¥1,700 cap; VC-CSA is an optional NON_T0/INELIGIBLE add-on of roughly 90–180 GPU-hours, not formal evidence. Do not create paid instances without a scoped authorization. First close Task20, then calibrate 3–5 Task30 smoke runs on one A30 before revising the budget; use three GPUs for frozen five-seed runs and six only for short independent final matrices. At session close create S19 and print the next continuation prompt.
