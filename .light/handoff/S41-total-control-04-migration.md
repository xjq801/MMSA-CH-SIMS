---
session_no: S41
contract_version: 2
suggested_title: "[TAFFC-CARM] 总控04接管并监督Task40"
parent_session: S40
project: mmsa-ch-sims-taffc-carm
date: 2026-08-05
source_context: total-control-03-task40-creation-and-control04-migration
target_thread: total-control-04
---

## 当前阶段

用户已明确要求创建Task40并创建总控04完成交接。Task40 `019fd19c-abf3-7bf0-8530-759e38c3a6ab`与总控04 `019fd19d-b8ef-71f2-82b3-433168211358`均已在独立Codex worktree创建。两者创建起点为`origin/main@51686ee5fe1f46b13745820840666ac3ccb3d853`，在收到总控03的对应FINAL_ANCHOR前只读。

总纲仍为v1.23、第17节规格v1.7、论文SSOT v0.1.3、claim矩阵v1.4。Task40只执行无teacher可信净收益路线的development-only串行门；Task30继续`CLOSED_NOT_PASSED`，formal test未materialize，Task50未创建，C1—C3仍`TO_VERIFY`。

## 已完成

- `TASK00_TASK40_CREATION_AND_CONTROL04_MIGRATION_20260805.md` — Codex任务列表人工确认Task40与总控04均取得稳定40位任务ID并运行在独立worktree。
- `TASK_REGISTRY.md` — 人工确认登记Task40=`CREATED_DEVELOPMENT_ONLY_READONLY_PENDING_FINAL_ANCHOR`与总控04接管关系。
- `.light/passport.yaml` — Python YAML解析验证stage 40状态改为created_readonly_pending_final_anchor，formal test继续禁止。
- `TASK00_TASK40_CREATION_AUTHORIZATION_20260805.md` — 9个绑定文件SHA-256在创建前经`Get-FileHash -Algorithm SHA256`逐项验证一致。
- `.light/handoff/S41-total-control-04-migration.md` — 直接运行`handoff_contract.py --as-of 2026-08-05`验证本卡合同。

## 工作区状态

- 本卡形成时Task40与总控04已创建但均被FINAL_ANCHOR只读门约束；迁移记录尚待最终验证、提交和推送，最终main须以Git刷新为准。
- 主工作区仅允许本批控制/交接文件变更；用户未跟踪`NEmoP/`、`__MACOSX/`、`tmp/`未被读取、修改、暂存或删除。

## 待用户回答

- decision_id=TOTAL_CONTROL_04_MIGRATION_20260805_RESOLVED | question=由谁接替总控03并监督新Task40？ | option_a=总控04接管；影响：总控03完成迁移后停止SSOT写入，Task40只向总控04回交（用户已选择） | option_b=总控03继续；影响：撤销本次迁移并保持旧控制链（当前未选择）

## Task40执行合同

1. Task40先核对授权及9个绑定hash，只使用train/DEV_SELECT/DEV_CALIBRATE；test loader fail-closed且test access event=0。
2. 串行执行P0泄漏→P1自然错位→P2 Oracle→P3 point→P4 credible→P5三源/区域；Oracle无稳定headroom即以`CLOSED_NOT_PASSED_NO_ORACLE_HEADROOM`关闭。
3. 点/credible router只允许监督目标不同；同架构、输入、候选池、预算、early stopping、五种子和coverage。
4. Task40不得直接合入main；回交`HANDOFF_40.md`、精确commit/ref、测试、结果与失败hash，由总控04独立裁定。

## 总控04职责

- 维护SSOT、passport/Registry、决策/风险/claim/论文边界及交接链，不代跑Task40。
- 使用Codex任务读取/等待工具刷新Task10/20/30/40实时状态，不把本卡或执行任务自报当成当前事实。
- Task40未过开发门不得创建Task50；任何主终点、种子、比较族、formal-test或资产边界变更必须先形成版本化书面裁定。
- 继续监督Task20补证边界和2026-08-31 23:59:59 +08:00受限存储删除验收。

## 阻塞/风险

- Task40尚无泄漏、错位、Oracle、router、三源或区域实验结果，C1—C3不得升级。
- I3D许可、稳定官方revision、权利方包身份/fixity仍UNKNOWN，禁止再分发。
- Video2Reaction许可差异、本地fixity与movie-disjoint未闭合，原生B轨不得执行。
- Task20 Attempt2仍补证未验收且永久NON_T0/INELIGIBLE；受限存储截止不因任务迁移延长。

## 下一步

1. 读取Git、WORK_LOG末条、passport/Registry和Task10/20/30/40实时状态，确认FINAL_ANCHOR后的实际main。
2. 验证Task40已核对9个授权hash并仅执行P0泄漏门，不允许越级训练router。
3. 验证Task20受限存储删除日历与Task40回交请求，按总控04职责独立裁定。

## 必读文件

1. `.light/handoff/S41-total-control-04-migration.md`
2. `.light/passport.yaml`
3. `.light/project_card.md`
4. `TASK00_TASK40_CREATION_AND_CONTROL04_MIGRATION_20260805.md`
5. `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.23，重点0.13、6、7、17节Task40
6. `TASK_REGISTRY.md`
7. `TASK00_TASK40_CREATION_AUTHORIZATION_20260805.md`
8. `TASK00_CARM_CREDIBLE_NET_BENEFIT_PREREGISTRATION_20260805.md`
9. `TASK10_CARM_RESPONSE_SUPPORT_DATA_FITNESS_ADDENDUM_20260805.md`
10. `TASK00_CARM_ROUTE_CLOSEST_PRIOR_SEARCH_20260805.md`
11. `experiments/CARM_UNIFIED_ROUTE_EXPERIMENT_MATRIX_20260805.md`
12. `RISK_REGISTER.md`、`CLAIM_EVIDENCE_MATRIX.md`与`paper/TAFFC_CARM_MANUSCRIPT_SSOT.md`
13. `WORK_LOG.md`末条

## 禁止

- 不得把本卡当作当前事实；必须先运行`git status --short --branch`、`git log -3`和`git rev-parse HEAD/origin/main`刷新现实。
- 总控04不得代跑Task40或与其并发修改实验核心；Task40不得修改总控SSOT后自行合入main。
- 不得materialize formal test、创建Task50、恢复Task30 teacher/KD或修改冻结统计合同。
- 不得改写G1—G3、I3D UNKNOWN、Task20 NON_T0/INELIGIBLE、Task30 `CLOSED_NOT_PASSED`、C1—C3 `TO_VERIFY`或受限存储删除截止。
- 不得读取、修改、提交或删除用户未跟踪目录。

## 接续提示词

你是“00-T-AFFC总控04”，不是Task40执行代理。先读AGENTS.md与WORK_RECORD_POLICY.md，刷新Git、WORK_LOG末条、passport/Registry及Task10/20/30/40实时状态；再读S41、创建迁移记录、总纲v1.23、Task40授权、可信净收益预注册、数据适配、查新与实验矩阵。Task40为`019fd19c-abf3-7bf0-8530-759e38c3a6ab`，只允许development-only串行执行P0泄漏→P1错位→P2 Oracle→P3 point→P4 credible→P5三源/区域；Oracle无headroom即关闭。总控04只做独立监督，不materialize formal test、不创建Task50、不恢复Task30，不改变G1—G3、I3D UNKNOWN、Task20 NON_T0/INELIGIBLE、C1—C3 TO_VERIFY或受限存储删除截止。
