---
session_no: S40
contract_version: 2
suggested_title: "[TAFFC-CARM] S41 Task40创建后Oracle门监督"
parent_session: S39
project: mmsa-ch-sims-taffc-carm
date: 2026-08-05
source_context: total-control-03-carm-v123-preregistration-and-task40-authorization
target_thread: total-control-03
---

## 当前阶段

总纲已升为v1.23、第17节规格v1.7、论文SSOT v0.1.3、claim矩阵v1.4。`SC-20260805-02`已闭合有限反应数据适配、closest-prior查新、target chain、failure tree、五种子、主终点、多重比较和formal-test禁令。`AUTH-00-TASK40-CNBR-DEVELOPMENT-20260805`已签发，Task40状态为`AUTHORIZED_TO_CREATE_DEVELOPMENT_ONLY_NOT_YET_CREATED`，须由用户新建独立Task40任务。

Task30仍`CLOSED_NOT_PASSED`，formal H1未裁定；Task20 Attempt2仍`SUPPLEMENT_REQUIRED_NO_ACCEPTANCE_YET`、NON_T0/INELIGIBLE；G1—G3、I3D UNKNOWN/accepted-risk与2026-08-31 23:59:59 +08:00受限存储删除截止不变。formal test未materialize，Task50未创建，C1—C3仍`TO_VERIFY`。

## 已完成

- `scripts/audit_carm_response_support.py` — 命令`.\.venv\Scripts\python.exe scripts\audit_carm_response_support.py`返回exit 0，确认CSMV 8210视频、107266有效情绪响应、计数精确可恢复；LAI-GAI只允许维度边际重抽样。
- `TASK10_CARM_RESPONSE_SUPPORT_DATA_FITNESS_ADDENDUM_20260805.md` — 00独立人工确认Task10 `main@1d2018c`后以`ACCEPTED_WITH_LIMITATIONS`接受数据/协议段落。
- `TASK00_CARM_ROUTE_CLOSEST_PRIOR_SEARCH_20260805.md` — 00人工确认检索证据后裁定`SYSTEMATIC_SCOPING_PASS_WITH_LIMITATIONS`；尚未定位完全同构方法，但禁止世界首创措辞。
- `TASK00_CARM_CREDIBLE_NET_BENEFIT_PREREGISTRATION_20260805.md` — 四个`.light/carm-v123-*.json`经Python JSON解析为PASS，并冻结点/后验净收益、response thinning、OOF、五种子、串行门、公平对照与test禁令。
- `TASK00_TASK40_CREATION_AUTHORIZATION_20260805.md` — SHA-256 `9089a8302e09fbdbb6910cf4bbfe5a35dc964c8b61cd21160042709a10c2c14a`绑定9项预注册hash，准许创建Task40开发任务，不允许总控代理或Task30直接执行。
- `DATA_SOURCE_LEDGER.md` — 人工确认Video2Reaction远端身份为HF revision `75278468c91c51ff54cf709d61ee881ca5c37c9b`与GitHub commit `0da6060445782128f503cd19d157f6a5922d107a`；许可表述差异未闭合，保持条件外验且未下载。

## 工作区状态

- 本卡创建时内容仍处于待最终验证/提交/推送状态；最终main commit必须以Git刷新为准，不可从本卡猜测。
- 用户自有未跟踪目录`NEmoP/`、`__MACOSX/`、`tmp/`未被读取、修改、暂存或删除。

## 待用户回答

- decision_id=CARM_TASK40_CREATION_20260805_RESOLVED | question=Task40是否已获准创建？ | option_a=已授权且保持未创建；影响：用户可新建独立Task40，00只做监督审核 | option_b=撤回授权；影响：Task40保持未创建且不得执行（当前未选择）

## Task40执行合同

1. 新Task40首先校验授权文件和9个绑定hash，使用独立worktree/branch，不与00同时修改SSOT。
2. 只允许train/DEV_SELECT/DEV_CALIBRATE；test loader必须fail-closed，Task40的test access event必须为0。
3. 串行顺序：泄漏审计→自然错位→Oracle headroom→point router→credible router→三源/区域。Oracle无headroom即关闭，不训练router。
4. 点/credible router的唯一机制变化是监督目标；共享同架构、输入、候选池、预算、early stopping、种子和coverage。
5. 开发种子固定`1364847620/426925854/1839464886/1138176833/484191872`；CSMV执行2/4/8/all×200 thinning；主比较在90% coverage下检验JSD与负迁移率。
6. 任何泄漏、预算不公平、稀释/先验翻转、三源不可辨识或区域失配都必须忠实降级，不增加模块追分。

## 数据裁定

| 数据集 | 当前裁定 | Task40角色 |
|---|---|---|
| CSMV | `FIT_WITH_ACCEPTED_ASSET_RISK` | 核心错位、Oracle、OOF后验路由和thinning；无需新数据 |
| LAI-GAI | `FIT_WITH_LIMITATIONS` | 边际有限响应、校准/区域；无视频记忆H2a/H2b |
| Video2Reaction | `CONDITIONAL_EXTERNAL_VALIDATION_NOT_CORE_REQUIRED` | 不阻断核心开发；许可/fixity/movie split闭合前不运行B轨 |
| 第二comment-bearing HUMAN_GOLD视频集 | 不存在/只建议 | 可加强H2a/H2b外验，但当前不必需、不阻断 |

## 阻塞/风险

- 尚无自然错位、Oracle、point/credible router、三源或预测区域实验结果；全部方法claim仍`TO_VERIFY`。
- CSMV I3D许可/revision/权利方包身份/fixity仍UNKNOWN，禁止再分发。
- Video2Reaction许可差异与底层媒体权利未闭合；不得把公开访问写成无限许可。
- Task20私有补证当前因无资产/连接而停止，不授权复跑；受限存储截止仍需总控监督。

## 下一步

1. 读取Git、WORK_LOG末条、passport/Registry和Task10/20/30/40实时状态，不把本卡当当前事实。
2. 检查用户新建的Task40是否绑定`AUTH-00-TASK40-CNBR-DEVELOPMENT-20260805`与预注册hash；总控只做独立审核。
3. 验证Task40严格执行泄漏→错位→Oracle串行门；未过Oracle不训练router，不创建Task50。

## 必读文件

1. `.light/handoff/S40-carm-v123-task40-authorization.md`
2. `.light/passport.yaml`
3. `.light/project_card.md`
4. `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.23，重点0.13、6、7、17节Task40
5. `TASK00_TASK40_CREATION_AUTHORIZATION_20260805.md`
6. `TASK00_CARM_CREDIBLE_NET_BENEFIT_PREREGISTRATION_20260805.md`
7. `TASK10_CARM_RESPONSE_SUPPORT_DATA_FITNESS_ADDENDUM_20260805.md`
8. `TASK00_CARM_ROUTE_CLOSEST_PRIOR_SEARCH_20260805.md`
9. `experiments/CARM_UNIFIED_ROUTE_EXPERIMENT_MATRIX_20260805.md`
10. `TASK_REGISTRY.md`
11. `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md`
12. `WORK_LOG.md`末条

## 禁止

- 不得把本卡当作当前事实；必须先运行`git status --short --branch`、`git log -3`和`git rev-parse HEAD/origin/main`刷新现实。
- 不得由00总控直接运行Task40实验核心，不得恢复Task30 teacher/KD。
- 不得materialize formal test、创建Task50、修改主终点/种子/比较族或不报失败运行。
- 不得改写G1—G3、I3D UNKNOWN、Task20 NON_T0/INELIGIBLE、Task30 `CLOSED_NOT_PASSED`、C1—C3 `TO_VERIFY`或受限存储删除截止。
- 不得读取、修改、提交或删除用户未跟踪目录。

## 接续提示词

你是“00-T-AFFC总控03”，不是Task40执行代理。先读AGENTS.md与WORK_RECORD_POLICY.md，刷新Git、WORK_LOG末条、passport/Registry和Task10/20/30/40实时状态；再读S40、总纲v1.23、`TASK00_TASK40_CREATION_AUTHORIZATION_20260805.md`、可信净收益预注册、数据适配补充、查新和实验矩阵。Task40已获准创建但未创建；若用户创建新Task40，只做独立监督，检查其串行执行泄漏→错位→Oracle门，无headroom即关闭且不训练router。不materialize formal test、不创建Task50、不恢复Task30，不改变G1—G3、I3D UNKNOWN、Task20 NON_T0/INELIGIBLE、C1—C3 TO_VERIFY或受限存储删除截止。
