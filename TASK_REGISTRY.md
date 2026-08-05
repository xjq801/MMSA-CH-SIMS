# T-AFFC任务登记表

> 版本：v1.13  
> 更新：2026-08-05  
> 上位SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.22（Task30负结果后的无teacher净效用路由、三源不确定性与经验分布预测区域；Video2Reaction双轨不变；v1.17数值门未恢复）  
> 规则：本表登记任务状态与退出门；科学事实以各任务HANDOFF、G门审查和专用台账为准。

| 任务 | 状态 | 任务/线程 | 权威输入 | 退出门与当前结论 | 交接 |
|---|---|---|---|---|---|
| 00 总控 | ACTIVE_TOTAL_CONTROL_03 | `019fbdab-9037-7320-9fda-9000c58a5c4b`（总控03；前任总控02=`019f6e64-0635-7ac0-a70a-65445b0fc1d1`） | 总纲v1.22、G门、决策/风险/claim台账 | 已保持Task30=`CLOSED_NOT_PASSED`并发布`SC-20260805-01`统一路线计划；下一步闭合系统查新、数据fitness、目标链/失败树与公平基线门，再决定是否另行授权创建Task40；Task10/20审核和受限存储截止监督继续 | `.light/handoff/S39-unified-route-master-v122.md` |
| 10 数据与协议 | MANUSCRIPT_DATA_SECTIONS_SUBMITTED_AWAITING_00_REVIEW | `019f5cf3-1810-7cd2-95bb-ff603551571b` | 总纲v1.21、论文SSOT v0.1.2、T0政策、公开数据与lineage | 原G1/G2结论不变；数据/协议/构念/许可/隐私/泄漏段落已由`main@1d2018c`提交，Task10实时任务已完成并请求00审核；尚未获得00接受 | `HANDOFF_10.md`、`TASK10_MANUSCRIPT_SECTION_COMPLETION_20260801.md`；待00审查 |
| 20 基线与统一评测 | FORMAL_CORE_CLOSED_RECOVERY_ATTEMPT2_SUPPLEMENT_REQUIRED | `019f6e2e-f781-7270-bb45-af8272ff5a5c` | Task20冻结G3证据、2026-08-02恢复复跑合同与`TASK00_TASK20_EPOCH1_3_RECOVERY_REVIEW_20260802.md` | Attempt2已完成并提交，但00尚未接受：须追加未来时间戳勘误、修正实验登记状态、披露逐step时间戳缺口并补充私有证据非秘密hash索引；不授权复跑，NON_T0/INELIGIBLE及原缺口不变 | `HANDOFF_20.md`、Task20最终closeout、2026-08-02恢复复跑审查 |
| 30 评论teacher/student | CLOSED_NOT_PASSED | `019fbdaa-01aa-7f60-9828-920d4a397ba5` | G3、evaluation-kit、`TASK00_TASK30_CREATION_AUTHORIZATION_20260801.md`、冻结ref `9086bd537b36cad5635eaa9db81aaeb6756b4088` | 00已接受可审计的开发负结果包并裁定H1=`NOT_PASSED_MECHANISM_NOT_STABLE`；formal test未materialize，正式H1未裁定；不授权修复，开发数值不得进入论文正式claim | `TASK00_TASK30_H1_FINAL_INDEPENDENT_REVIEW_20260804.md`、`HANDOFF_30.md` |
| 40 净效用反应记忆与三源可靠性 | NOT_CREATED_PLAN_AUTHORIZED_AWAITING_PREREGISTRATION_GATES | 未创建 | `SC-20260805-01`、v1.22、统一路线计划、Task30负结果边界、冻结content-only接口 | 用户已批准路线但未自动授权创建；须先通过系统查新、CSMV/LAI-GAI identity/fitness、目标链、失败树、公平baseline、OOF/正式test禁令和00独立创建合同；不得恢复teacher | 未来精确授权后方可产生`HANDOFF_40.md` |
| 50 正式实验 | NOT_CREATED | 未创建 | 冻结无teacher CARM/降级方法、正式预注册 | G4—G6；H2a现象/Oracle、H2b OOF路由、H2c三源/预测区域；两个HUMAN_GOLD主集；Video2Reaction双轨；五种子、严格OOD、E0—E9、统计冻结 | 未来`HANDOFF_50.md` |
| 60 论文与投稿 | NOT_CREATED | 未创建 | G6、results-freeze、claim-evidence | submission-ready与00最终Go | 未来`HANDOFF_60.md` |

## 不属于本项目的任务

IJCV的J0—J2、JH1—JH3、任务25和65已迁至`D:\MMSA-CH-SIMS - IJCV方向`，不得在本表创建或执行。
