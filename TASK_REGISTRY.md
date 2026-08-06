# T-AFFC任务登记表

> 版本：v1.20  
> 更新：2026-08-06  
> 上位SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.25（Task40/45负结果不变；Task46重构为后验效用分布学习与风险约束选择但仍未创建；Task50与formal test仍阻断）  
> 规则：本表登记任务状态与退出门；科学事实以各任务HANDOFF、G门审查和专用台账为准。

| 任务 | 状态 | 任务/线程 | 权威输入 | 退出门与当前结论 | 交接 |
|---|---|---|---|---|---|
| 00 总控 | ACTIVE_TOTAL_CONTROL_04 | `019fd19d-b8ef-71f2-82b3-433168211358`（总控04；移交方总控03=`019fbdab-9037-7320-9fda-9000c58a5c4b`） | 总纲v1.25、G门、决策/风险/claim台账、S41—S44 | 已独立关闭Task40；Task45已回交not-passed包待独立终审；按用户决定冻结v1.25效用分布/risk-budget方向但不创建Task46，不代跑实验核心 | S44 |
| 10 数据与协议 | CLOSED_MANUSCRIPT_DATA_SECTIONS_ACCEPTED_WITH_LIMITATIONS | `019f5cf3-1810-7cd2-95bb-ff603551571b` | 总纲v1.23、论文SSOT v0.1.3、T0政策、公开数据与lineage | `main@1d2018c`数据/协议/构念/许可/隐私/泄漏段落已被00以`ACCEPTED_WITH_LIMITATIONS`验收；有限反应补充绑定CSMV有效情绪响应107266与LAI-GAI边际重抽样边界；不升级C1—C3 | `HANDOFF_10.md`、`TASK10_CARM_RESPONSE_SUPPORT_DATA_FITNESS_ADDENDUM_20260805.md` |
| 20 基线与统一评测 | FORMAL_CORE_CLOSED_RECOVERY_ATTEMPT2_SUPPLEMENT_REQUIRED | `019f6e2e-f781-7270-bb45-af8272ff5a5c` | Task20冻结G3证据、2026-08-02恢复复跑合同与`TASK00_TASK20_EPOCH1_3_RECOVERY_REVIEW_20260802.md` | Attempt2已完成并提交，但00尚未接受：须追加未来时间戳勘误、修正实验登记状态、披露逐step时间戳缺口并补充私有证据非秘密hash索引；不授权复跑，NON_T0/INELIGIBLE及原缺口不变 | `HANDOFF_20.md`、Task20最终closeout、2026-08-02恢复复跑审查 |
| 30 评论teacher/student | CLOSED_NOT_PASSED | `019fbdaa-01aa-7f60-9828-920d4a397ba5` | G3、evaluation-kit、`TASK00_TASK30_CREATION_AUTHORIZATION_20260801.md`、冻结ref `9086bd537b36cad5635eaa9db81aaeb6756b4088` | 00已接受可审计的开发负结果包并裁定H1=`NOT_PASSED_MECHANISM_NOT_STABLE`；formal test未materialize，正式H1未裁定；不授权修复，开发数值不得进入论文正式claim | `TASK00_TASK30_H1_FINAL_INDEPENDENT_REVIEW_20260804.md`、`HANDOFF_30.md` |
| 40 可信净收益反应记忆与三源可靠性 | CLOSED_NOT_PASSED_ROUTER_MAIN_JSD | `019fd19c-abf3-7bf0-8530-759e38c3a6ab`（独立worktree；tag `task40-carm-cnbr-development-20260805`） | `SC-20260805-01/02`、v1.23、`AUTH-00-TASK40-CNBR-DEVELOPMENT-20260805`、Task30负结果边界 | P0/P1/P2通过；P3/P4可信router相对最强control主JSD门0/5，差值均为正且CI跨0；负迁移按固定顺序未检验，P5未执行，formal test为0；不授权修复或新实验 | `HANDOFF_40.md`；`TASK00_TASK40_FINAL_INDEPENDENT_REVIEW_20260805.md`；S42 |
| 45 T0历史收益可学习性诊断 | DELIVERED_CLOSED_NOT_PASSED_AWAITING_00_REVIEW | `019fd586-628b-74f0-85ae-b44fa60968ff`（tag `task45-t0-benefit-learnability-development-20260806`） | `SC-20260806-01`、v1.24冻结合同、`HANDOFF_45.md`与P0—P2交付包 | 两条primary表面改善，但两条shuffled-target阴性对照异常通过；代理按预注册关闭。旧DEV、TRAIN_ROUTER_CONFIRM、formal test零事件；禁止补跑/改判，等待00独立hash/validator/one-shot终审 | `HANDOFF_45.md`；S44 |
| 46 后验效用分布与风险约束选择（候选） | PLANNED_NOT_CREATED_PENDING_TASK45_REVIEW_AND_V125_PREREGISTRATION | 未创建 | `SC-20260806-02`、总纲v1.25；未来须Task45独立关闭审核、跨组负控/target/failure/公平基线/访问边界/预注册、用户执行授权和00精确创建合同 | 当前不得训练或打开`TRAIN_ROUTER_CONFIRM`；未来先效用学习，再冻结risk-budget三动作；matched-coverage主JSD通过前不得检验负迁移/P5 | S44；未创建 |
| 50 正式实验 | NOT_CREATED_FIXED_ORDER_BLOCKED | 未创建 | 仅在未来另有用户明确授权和新冻结计划时才可改变 | Task40主JSD开发门未通过；当前不得materialize formal test，不得执行H2b/H2c正式统计或Video2Reaction外验 | `.light/handoff/S42-task40-closed-not-passed.md` |
| 60 论文与投稿 | NOT_CREATED | 未创建 | G6、results-freeze、claim-evidence | submission-ready与00最终Go | 未来`HANDOFF_60.md` |

## 不属于本项目的任务

IJCV的J0—J2、JH1—JH3、任务25和65已迁至`D:\MMSA-CH-SIMS - IJCV方向`，不得在本表创建或执行。
