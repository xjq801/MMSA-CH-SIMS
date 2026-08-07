---
session_no: S45
contract_version: 2
suggested_title: "[TAFFC] Task45独立关闭与Task46 v1.25执行冻结"
parent_session: S44
project: MMSA-CH-SIMS-TAFFC-CARM
date: 2026-08-07
---
# S45 — Task45独立关闭与Task46 v1.25执行冻结

## 本批裁定

总控04从 annotated tag `task45-t0-benefit-learnability-development-20260806` 独立复核 Task45 的 P0/P1/P2 身份、CRLF归一化 hash、one-shot marker、异常 shuffled-target、实际 torch 线程数和零访问账。Task45 正式关闭为 `CLOSED_NOT_PASSED_T0_BENEFIT_LEARNABILITY`；弱 Brier/MAE/Spearman/top-decile 仅为 `EXPLORATORY_SUGGESTIVE_SIGNAL`。Task40 仍 `CLOSED_NOT_PASSED_ROUTER_MAIN_JSD`，Task50 未创建，formal test 零事件。

## 本批新增冻结材料

- `TASK00_TASK45_FINAL_INDEPENDENT_REVIEW_20260807.md`
- `TASK00_TASK46_V125_RESEARCH_PLAN_20260807.md`
- `TASK00_TASK46_V125_PREREGISTRATION_20260807.md`
- `TASK00_TASK46_CREATION_AUTHORIZATION_20260807.md`
- `.light/carm-v125-data-identity-fitness.json`
- `.light/carm-v125-target-chain.json`
- `.light/carm-v125-failure-tree.json`
- `.light/carm-v125-fair-baselines.json`
- `.light/carm-v125-access-boundary.json`

《任务安排.docx》已只读解析，SHA-256=`FE28A804C4656E0F57916256C3C84953AC21217945C6F2DA9BD3A5906920513E`。共享回答中“复用 DIAG_CONFIRM、固定10% memory、主实验无 ABSTAIN”的旧约束与当前 v1.25 冲突，已按 v1.25 修正为新角色重建、跨组有效负控、FIT nested OOF、0.90 non-abstain coverage 和 `USE_MEMORY/FALLBACK_CONTENT/ABSTAIN` 三动作；没有打开任何确认集。

## 下一步授权边界

用户的直接执行请求记录为 `USER-20260807-EXECUTE-SHARED-TASK46-PLAN`。允许创建独立 Task46 worktree 并执行 P0→P3；P4 只有在全部代码/config/manifest/hash/负控/公平基线/策略冻结且自动 validator 通过后，才可一次性打开 `TRAIN_ROUTER_CONFIRM`。不得访问旧 DEV、DIAG_CONFIRM、formal test，不得修复或重跑 Task45/40，不得创建 Task50。P4 主 JSD 未通过时，U4 负迁移和 U5/P5 固定为 `NOT_TESTED/NOT_EXECUTED`。

## 主要风险

1. Task45 的弱信号可能来自无效负控、身份或目标结构，而不是合法 T0 可学习性。
2. 排序/效用学习可能不能转化为 matched-coverage 主 JSD 改善，且错误使用 memory 的损失不对称。
3. 已看角色和一次性确认角色污染会使任何越界访问不可修复；所有 hash 和 zero-event ledger 必须先冻结。

## 接续提示词

```text
你是00-T-AFFC总控04的后续会话。先fetch并确认HEAD=origin/main，读取AGENTS.md、WORK_RECORD_POLICY.md、WORK_LOG末条、总纲v1.25第17节、TASK_REGISTRY v1.21、passport、project_card、TASK00_TASK45_FINAL_INDEPENDENT_REVIEW_20260807.md及本S45。Task45已CLOSED_NOT_PASSED_T0_BENEFIT_LEARNABILITY，Task40已CLOSED_NOT_PASSED_ROUTER_MAIN_JSD；只按TASK00_TASK46_V125_RESEARCH_PLAN_20260807.md与PREREGISTRATION执行，先创建独立Task46 worktree并从P0身份/跨组负控门开始。旧DEV/DIAG_CONFIRM/formal test保持零访问，TRAIN_ROUTER_CONFIRM只在全部P0-P3 hash冻结后一次性打开，formal test和Task50禁止。每次行为追加WORK_LOG，收尾写下一张handoff。
```
