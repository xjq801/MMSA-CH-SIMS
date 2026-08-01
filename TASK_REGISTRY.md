# T-AFFC任务登记表

> 版本：v1.9  
> 更新：2026-08-01  
> 上位SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.21（第17节Video2Reaction双轨强基线合同；v1.17数值门未恢复）  
> 规则：本表登记任务状态与退出门；科学事实以各任务HANDOFF、G门审查和专用台账为准。

| 任务 | 状态 | 任务/线程 | 权威输入 | 退出门与当前结论 | 交接 |
|---|---|---|---|---|---|
| 00 总控 | ACTIVE_TRANSFERRED_TO_03 | `019fbdab-9037-7320-9fda-9000c58a5c4b`（总控03；前任总控02=`019f6e64-0635-7ac0-a70a-65445b0fc1d1`） | 总纲v1.21、G门、决策/风险/claim台账 | 总控03接管SSOT与独立审核；下一步监督Task30并审核Task10论文数据段落 | `.light/handoff/S32-total-control-03-migration.md` |
| 10 数据与协议 | MANUSCRIPT_DATA_SECTIONS_SUBMITTED_AWAITING_00_REVIEW | `019f5cf3-1810-7cd2-95bb-ff603551571b` | 总纲v1.21、论文SSOT v0.1.2、T0政策、公开数据与lineage | 原G1/G2结论不变；数据/协议/构念/许可/隐私/泄漏段落已由`main@1d2018c`提交，Task10实时任务已完成并请求00审核；尚未获得00接受 | `HANDOFF_10.md`、`TASK10_MANUSCRIPT_SECTION_COMPLETION_20260801.md`；待00审查 |
| 20 基线与统一评测 | FORMAL_CORE_CLOSED_MANUSCRIPT_SECTIONS_ACCEPTED_WITH_LIMITATIONS | `019f6e2e-f781-7270-bb45-af8272ff5a5c` | `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md` v0.1.2、Task20冻结G3证据 | `main@5e1386d`的Sec.5.4/5.6/5.8、受限Sec.6.1、Sec.8和Task20 supplement已由00验收；无正式结果、五种子或claim升级；受限存储删除截止仍为2026-08-31 | `HANDOFF_20.md`、`TASK00_TASK20_FINAL_CLOSEOUT_REVIEW_20260801.md`、`TASK00_TASK20_MANUSCRIPT_SECTION_REVIEW_20260801.md` |
| 30 评论teacher/student | CREATED_STARTUP_AUDIT_IN_PROGRESS | `019fbdaa-01aa-7f60-9828-920d4a397ba5` | `main@32e8967`、G3、evaluation-kit、`TASK00_TASK30_CREATION_AUTHORIZATION_20260801.md`、`HANDOFF_30.md` | 只验证H1评论特权监督；train评论、dev选择、正式test禁用；不引入memory/router；完成后由00独立裁定H1门 | `HANDOFF_30.md` |
| 40 反应记忆与路由 | NOT_CREATED | 未创建 | HANDOFF_30、冻结student与H1决策 | v1.21门：train内部OOF效用标签；learned retrieval强对照；收益感知router与固定融合/相似度/熵/SelectiveNet式拒绝公平比较；接口支持V2R-B的train-only分布记忆 | 未来`HANDOFF_40.md` |
| 50 正式实验 | NOT_CREATED | 未创建 | 冻结CARM/降级方法、正式预注册 | G4—G6；两个HUMAN_GOLD主集；Video2Reaction A轨CSMV公平适配+B轨原生银标外部验证；五种子、严格OOD、E0—E9、统计冻结 | 未来`HANDOFF_50.md` |
| 60 论文与投稿 | NOT_CREATED | 未创建 | G6、results-freeze、claim-evidence | submission-ready与00最终Go | 未来`HANDOFF_60.md` |

## 不属于本项目的任务

IJCV的J0—J2、JH1—JH3、任务25和65已迁至`D:\MMSA-CH-SIMS - IJCV方向`，不得在本表创建或执行。
