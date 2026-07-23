# T-AFFC任务登记表

> 版本：v1.0  
> 更新：2026-07-23  
> 上位SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.16（2026-07-23由v1.17回退）  
> 规则：本表登记任务状态与退出门；科学事实以各任务HANDOFF、G门审查和专用台账为准。

| 任务 | 状态 | 任务/线程 | 权威输入 | 退出门与当前结论 | 交接 |
|---|---|---|---|---|---|
| 00 总控 | ACTIVE | `019f6e64-0635-7ac0-a70a-65445b0fc1d1` | 总纲v1.16、G门、决策/风险/claim台账 | 持续维护SSOT；最终T-AFFC Go/No-Go | `.light/handoff/S21-master-plan-rollback-to-v116.md`及后续链 |
| 10 数据与协议 | COMPLETED_WITH_LIMITATIONS | 历史线程ID未在本表补录 | 总纲、T0政策、公开数据与lineage | G1 PASS；G2协议/数据PASS_WITH_LIMITATIONS；资产风险延期接受 | `HANDOFF_10.md` |
| 20 基线与统一评测 | FORMAL_CORE_COMPLETED_EXPLORATION_OPEN | `019f6e2e-f781-7270-bb45-af8272ff5a5c` | HANDOFF_10、冻结数据/split/评测协议 | G3 PASS_WITH_LIMITATIONS；VC-CSA探索永久NON_T0/INELIGIBLE且未闭环 | `HANDOFF_20.md`、`TASK00_G3_FINAL_REVIEW_20260718.md` |
| 30 评论teacher/student | NOT_CREATED_BLOCKED_TASK20_CLOSEOUT | 未创建 | G3、evaluation-kit、H1预注册 | v1.16门：相对最强content-only呈稳定趋势，校准无不可接受恶化，E3隔离特权监督贡献 | 未来`HANDOFF_30.md` |
| 40 反应记忆与路由 | NOT_CREATED | 未创建 | HANDOFF_30、冻结student与H1决策 | v1.16门：有效检索明显优于随机检索，低质量/OOD邻居下减少负迁移或改善选择性风险 | 未来`HANDOFF_40.md` |
| 50 正式实验 | NOT_CREATED | 未创建 | 冻结CARM/降级方法、正式预注册 | G4—G6；两主集、五种子、E0—E9、统计冻结 | 未来`HANDOFF_50.md` |
| 60 论文与投稿 | NOT_CREATED | 未创建 | G6、results-freeze、claim-evidence | submission-ready与00最终Go | 未来`HANDOFF_60.md` |

## 不属于本项目的任务

IJCV的J0—J2、JH1—JH3、任务25和65已迁至`D:\MMSA-CH-SIMS - IJCV方向`，不得在本表创建或执行。
