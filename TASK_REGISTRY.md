# T-AFFC任务登记表

> 版本：v1.14  
> 更新：2026-08-05  
> 上位SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.23（无teacher的OOF点/后验净收益路由、response thinning、三源不确定性与经验分布预测区域；Task30负结果和Video2Reaction双轨边界不变）  
> 规则：本表登记任务状态与退出门；科学事实以各任务HANDOFF、G门审查和专用台账为准。

| 任务 | 状态 | 任务/线程 | 权威输入 | 退出门与当前结论 | 交接 |
|---|---|---|---|---|---|
| 00 总控 | ACTIVE_TOTAL_CONTROL_03 | `019fbdab-9037-7320-9fda-9000c58a5c4b`（总控03；前任总控02=`019f6e64-0635-7ac0-a70a-65445b0fc1d1`） | 总纲v1.23、G门、决策/风险/claim台账 | 已闭合`SC-20260805-02`数据/查新/预注册门，独立受限验收Task10段落，并签发`AUTH-00-TASK40-CNBR-DEVELOPMENT-20260805`；Task40尚未创建，Task20受限存储截止监督继续 | `.light/handoff/S40-carm-v123-task40-authorization.md` |
| 10 数据与协议 | CLOSED_MANUSCRIPT_DATA_SECTIONS_ACCEPTED_WITH_LIMITATIONS | `019f5cf3-1810-7cd2-95bb-ff603551571b` | 总纲v1.23、论文SSOT v0.1.3、T0政策、公开数据与lineage | `main@1d2018c`数据/协议/构念/许可/隐私/泄漏段落已被00以`ACCEPTED_WITH_LIMITATIONS`验收；有限反应补充绑定CSMV有效情绪响应107266与LAI-GAI边际重抽样边界；不升级C1—C3 | `HANDOFF_10.md`、`TASK10_CARM_RESPONSE_SUPPORT_DATA_FITNESS_ADDENDUM_20260805.md` |
| 20 基线与统一评测 | FORMAL_CORE_CLOSED_RECOVERY_ATTEMPT2_SUPPLEMENT_REQUIRED | `019f6e2e-f781-7270-bb45-af8272ff5a5c` | Task20冻结G3证据、2026-08-02恢复复跑合同与`TASK00_TASK20_EPOCH1_3_RECOVERY_REVIEW_20260802.md` | Attempt2已完成并提交，但00尚未接受：须追加未来时间戳勘误、修正实验登记状态、披露逐step时间戳缺口并补充私有证据非秘密hash索引；不授权复跑，NON_T0/INELIGIBLE及原缺口不变 | `HANDOFF_20.md`、Task20最终closeout、2026-08-02恢复复跑审查 |
| 30 评论teacher/student | CLOSED_NOT_PASSED | `019fbdaa-01aa-7f60-9828-920d4a397ba5` | G3、evaluation-kit、`TASK00_TASK30_CREATION_AUTHORIZATION_20260801.md`、冻结ref `9086bd537b36cad5635eaa9db81aaeb6756b4088` | 00已接受可审计的开发负结果包并裁定H1=`NOT_PASSED_MECHANISM_NOT_STABLE`；formal test未materialize，正式H1未裁定；不授权修复，开发数值不得进入论文正式claim | `TASK00_TASK30_H1_FINAL_INDEPENDENT_REVIEW_20260804.md`、`HANDOFF_30.md` |
| 40 可信净收益反应记忆与三源可靠性 | AUTHORIZED_TO_CREATE_DEVELOPMENT_ONLY_NOT_YET_CREATED | 未创建；须由用户创建新Task40 | `SC-20260805-01/02`、v1.23、`AUTH-00-TASK40-CNBR-DEVELOPMENT-20260805`、Task30负结果边界 | 文档/数据/统计门已闭合；创建后串行执行泄漏门→错位→Oracle→point/credible router→三源/区域；Oracle无headroom立即关闭；formal test禁止，不得恢复teacher | 未来`HANDOFF_40.md` |
| 50 正式实验 | NOT_CREATED | 未创建 | 冻结无teacher CARM/降级方法、正式预注册 | G4—G6；H2a现象/Oracle、H2b OOF路由、H2c三源/预测区域；两个HUMAN_GOLD主集；Video2Reaction双轨；五种子、严格OOD、E0—E9、统计冻结 | 未来`HANDOFF_50.md` |
| 60 论文与投稿 | NOT_CREATED | 未创建 | G6、results-freeze、claim-evidence | submission-ready与00最终Go | 未来`HANDOFF_60.md` |

## 不属于本项目的任务

IJCV的J0—J2、JH1—JH3、任务25和65已迁至`D:\MMSA-CH-SIMS - IJCV方向`，不得在本表创建或执行。
