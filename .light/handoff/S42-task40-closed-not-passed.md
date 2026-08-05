# S42 — Task40主JSD开发门关闭与总控04接续

## 1. 接续身份与Git锚点

- 当前总控：00-T-AFFC总控04，task/thread `019fd19d-b8ef-71f2-82b3-433168211358`。
- 项目只执行IEEE T-AFFC CARM路线；不得创建或执行IJCV J0—J2、JH1—JH3、任务25或65。
- 本次独立审核起点：`origin/main@6b4015e16aca6b6cd5a41540255e0f977413632e`。
- Task40审计tag：`refs/tags/task40-carm-cnbr-development-20260805`，解引用到`c0fe21dc472b508e52ff6c29b8ea54afd7322e0e`。
- 总控04审核与SSOT裁定commit：`ce147280d4cbaec6b7d1f4dfa2f72956ff5f0653`。
- 独立审核文件：`TASK00_TASK40_FINAL_INDEPENDENT_REVIEW_20260805.md`，SHA-256=`ae1f890fbbeb1625fdbaf4e95b3998d46bc715e8d3416daa21b36f3f0d27f42e`。

## 2. 当前门与任务状态

- G1=`PASS`。
- G2协议/数据=`PASS_WITH_LIMITATIONS`；I3D资产风险=`DEFERRED_ACCEPTED_RISK`；总G2=`PASS_WITH_ACCEPTED_ASSET_RISK`；`formal_split=true`。
- G3=`PASS_WITH_LIMITATIONS`。
- Task10：数据/协议论文段落`ACCEPTED_WITH_LIMITATIONS`。
- Task20：Attempt2仍`SUPPLEMENT_REQUIRED_NO_ACCEPTANCE_YET`，永久`NON_T0/INELIGIBLE`；受限存储可见层删除截止`2026-08-31 23:59:59 +08:00`不变，平台控制面仍UNKNOWN。
- Task30：永久`CLOSED_NOT_PASSED`，不得恢复teacher/KD。
- Task40：`CLOSED_NOT_PASSED_ROUTER_MAIN_JSD`。
- Task50：`NOT_CREATED_FIXED_ORDER_BLOCKED`；不得materialize formal test。
- 论文：`MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS`；C1不升级，C2开发候选关闭且不得升级，C3因固定顺序未检验而非被反驳。

## 3. Task40独立审核结论

- P0 PASS：train=5698、DEV_SELECT=393、DEV_CALIBRATE=444，正式test五类事件为0。
- P1 PASS：高相似受控错位6/570，95% CI下界大于0。
- P2 PASS：Oracle headroom 5/5 seed稳定为正。
- P3/P4 FAIL：credible相对每seed最强control的主JSD差为`+0.003044/+0.004890/+0.004964/+0.006216/+0.005152`，五个95% CI均跨0，主门0/5。
- credible五seed均0次`USE_MEMORY`；不能声称优于point/generic control。
- 可信负迁移=`NOT_TESTED_FIXED_ORDER_MAIN_JSD_FAILED`；P5=`NOT_EXECUTED_FIXED_ORDER_ROUTER_MAIN_JSD_FAILED`。
- 25/25 Task40测试与P0/P1/P2/P3-P4四个validator均PASS；Task40 WORK_LOG 285条0错误。
- 通用准备门只因data-free Task40 worktree缺少相对`HUMAN_GOLD`而`FileNotFoundError`/exit 1；未绕过。
- 两次失败运行commit均在tag祖先链且保留；Task40分支未push、未merge main。

## 4. 不可改变的边界

1. 不创建Task50，不新增seed/trial/module/coverage，不用P5或Video2Reaction挽救失败主门。
2. 不把P1/P2开发证据写成正式论文结果，不把C2写成已验证或把C3写成被反驳。
3. 不恢复Task30 teacher/KD，不接受Task20 Attempt2为T0，不改受限存储截止。
4. I3D license、官方revision、权利方包身份/fixity仍UNKNOWN；仅内部研究，禁止确认或再分发。
5. 任何替代研究路线、新实验或Task50创建都须用户另行明确授权，并先完成新查新、数据适配、预注册与总控审核。

## 5. 最近行动与下一动作

最近三项行动：

1. 从annotated tag重算全部交付hash、两份配对JSD差、coverage/action及零test事件。
2. 独立运行25项测试、四个阶段validator、WORK_LOG validator和通用准备门，保留后者data-free失败。
3. 发布Task40最终独立审核，更新总纲当前态、Task Registry v1.16、Claim矩阵 v1.5、决策/风险/项目卡。

下一项总控动作：在不授权任何新实验的前提下，完成当前CARM论文路线的可发表性/降级选项审计，并继续监督Task20最小补证与2026-08-31受限存储删除验收。

## 6. 接续提示词

```text
你是00-T-AFFC总控04的接续会话。项目根目录D:\MMSA-CH-SIMS，只执行IEEE T-AFFC CARM路线；IJCV位于另一项目，禁止创建或执行J0—J2、JH1—JH3、任务25或65。先fetch并核对origin/main包含总控04审核commit ce147280d4cbaec6b7d1f4dfa2f72956ff5f0653，再完整读取AGENTS.md、WORK_RECORD_POLICY.md、WORK_LOG末条、.light/passport.yaml、.light/project_card.md、TASK_REGISTRY.md v1.16、总纲v1.23当前态、DECISION_LOG末条、RISK_REGISTER、CLAIM_EVIDENCE_MATRIX.md v1.5、TASK00_TASK40_FINAL_INDEPENDENT_REVIEW_20260805.md及本S42。Task40已以CLOSED_NOT_PASSED_ROUTER_MAIN_JSD关闭：P0/P1/P2通过，P3/P4主JSD 0/5；负迁移未检验，P5未执行，formal test五类事件全0。不得创建Task50、补跑实验、恢复teacher/KD或把P5未执行写成阴性结果。论文继续MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS；C2不得升级，C3只能写未检验。继续维护G1—G3、I3D UNKNOWN/禁止再分发、Task20 NON_T0/INELIGIBLE及2026-08-31受限存储截止。下一动作仅做路线可发表性/降级选项审计和既有风险监督，任何新实验须用户明确授权。
```
