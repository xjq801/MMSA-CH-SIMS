# T-AFFC任务登记表

> 版本：v1.2  
> 更新：2026-07-27  
> 上位SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.20（第17节收益感知路由执行规格补强；v1.17数值门未恢复）  
> 规则：本表登记任务状态与退出门；科学事实以各任务HANDOFF、G门审查和专用台账为准。

| 任务 | 状态 | 任务/线程 | 权威输入 | 退出门与当前结论 | 交接 |
|---|---|---|---|---|---|
| 00 总控 | ACTIVE | `019f6e64-0635-7ac0-a70a-65445b0fc1d1` | 总纲v1.20、G门、决策/风险/claim台账 | 持续维护SSOT；最终T-AFFC Go/No-Go | `.light/handoff/S23-video2reaction-direct-prior-v119.md`及后续链 |
| 10 数据与协议 | COMPLETED_WITH_LIMITATIONS | 历史线程ID未在本表补录 | 总纲、T0政策、公开数据与lineage | G1 PASS；G2协议/数据PASS_WITH_LIMITATIONS；资产风险延期接受 | `HANDOFF_10.md` |
| 20 基线与统一评测 | FORMAL_CORE_COMPLETED_EXPLORATION_RESUME_BLOCKED_CHECKPOINT_CROSS_REGION | `019f6e2e-f781-7270-bb45-af8272ff5a5c` | HANDOFF_10、冻结数据/split/评测协议 | G3 PASS_WITH_LIMITATIONS；13区8210项I3D已复核，冻结环境正在恢复，但精确断点仍只在亚太2区，跨区复制完成且SHA-256匹配前不得续训；恢复锚为Epoch 4 step 220，永久NON_T0/INELIGIBLE | `HANDOFF_20.md`、`TASK00_G3_FINAL_REVIEW_20260718.md`、最新Task20线程/`WORK_LOG.md` |
| 30 评论teacher/student | NOT_CREATED_BLOCKED_TASK20_CLOSEOUT | 未创建 | G3、evaluation-kit、H1预注册 | v1.20门：普通KD、错配评论、teacher-only上界与content-only公平比较；teacher/蒸馏不作模块首创 | 未来`HANDOFF_30.md` |
| 40 反应记忆与路由 | NOT_CREATED | 未创建 | HANDOFF_30、冻结student与H1决策 | v1.20门：train内部OOF效用标签；learned retrieval强对照；收益感知router与固定融合/相似度/熵/SelectiveNet式拒绝公平比较；减少负迁移或改善选择性风险 | 未来`HANDOFF_40.md` |
| 50 正式实验 | NOT_CREATED | 未创建 | 冻结CARM/降级方法、正式预注册 | G4—G6；两主集、Video2Reaction式强基线、五种子、严格OOD、E0—E9、统计冻结 | 未来`HANDOFF_50.md` |
| 60 论文与投稿 | NOT_CREATED | 未创建 | G6、results-freeze、claim-evidence | submission-ready与00最终Go | 未来`HANDOFF_60.md` |

## 不属于本项目的任务

IJCV的J0—J2、JH1—JH3、任务25和65已迁至`D:\MMSA-CH-SIMS - IJCV方向`，不得在本表创建或执行。
