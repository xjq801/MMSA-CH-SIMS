---
session_no: S39
contract_version: 2
suggested_title: "[TAFFC-CARM] S40 v1.22数据门与预注册合同"
parent_session: S38
project: mmsa-ch-sims-taffc-carm
date: 2026-08-05
source_context: total-control-03-unified-route-master-v122
target_thread: total-control-03
---

## 当前阶段

用户已明确授权把三个idea的具体实验方案、步骤和数据集并入唯一总纲。总纲现为v1.22、第17节规格为v1.6；路线状态是`ROUTE_APPROVED_PLAN_FROZEN_EXECUTION_NOT_YET_AUTHORIZED`。内容提交锚点为`83283b22b0edb834f733a0c946188889b4ca21e9`，下次会话必须刷新Git以取得包含本卡的最终closure commit。

Task30仍为`CLOSED_NOT_PASSED`，H1开发门仍为`NOT_PASSED_MECHANISM_NOT_STABLE`，formal test未materialize。v1.22没有恢复评论teacher/KD；Task40状态为`NOT_CREATED_PLAN_AUTHORIZED_AWAITING_PREREGISTRATION_GATES`，Task50未创建。G1—G3、I3D UNKNOWN、Task20 NON_T0/INELIGIBLE与2026-08-31受限存储删除截止均未改变。

## 已完成

- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.22 — 人工确认已写入`SC-20260805-01`、H2a—H2c、P0—P6、Task30历史负结果、第5月无teacher路线、G4和Task40/50创建顺序；Git验证内容提交为`83283b22b0edb834f733a0c946188889b4ca21e9`。
- `TASK00_CARM_UNIFIED_ROUTE_RESEARCH_PLAN_20260805.md` — 人工确认question/estimand、训练折内OOF `Delta_i`、三动作、数据角色、主要终点、停止规则和Task40创建门已冻结，且没有写入新实验结果。
- `experiments/CARM_UNIFIED_ROUTE_EXPERIMENT_MATRIX_20260805.md` — `plan_lint.py`验证10个实验/消融行四要素齐全，严谨性计数评分100/100、exit 0。
- 控制面传播 — 人工确认AGENTS、Registry、passport、project card、terminology、两份decision log、version history、risk register和WORK_LOG均已吸收v1.22；passport底层validator仅保留历史stage 10缺hash/timestamp的WARN。
- 仓库综合门 — `scripts/validate_work_log.py`验证262条、0错误；`scripts/run_preparation_checks.py` exit 0、`blocking_checks=[]`；`git diff --check`通过，同时确认`formal_model_work_ready=false`、`faiss_available=false`与`g2_asset_ready=false`未被改写。

## 工作区状态

- 本卡创建前工作树相对内容commit为`clean`但仍存在用户自有未跟踪目录`NEmoP/`、`__MACOSX/`、`tmp/`；这些目录未被读取、修改、暂存或删除。
- 本地`main`在内容commit `83283b22b0edb834f733a0c946188889b4ca21e9`处相对`origin/main@e51621a18f87b2648d8b1a6f8770d5a41d98e74f`为ahead 1；本卡与最终追加日志处于`dirty/unpushed`状态，尚待closure commit和push。

## 待用户回答

- decision_id=CARM_IDEA_20260805_UNIFIED_ROUTE_RESOLVED | question=三个idea的方案是否已获用户授权合入总纲？ | option_a=已授权并已落入v1.22；影响：继续数据与预注册准备但不自动创建Task40或运行实验 | option_b=未授权；影响：不适用，保留此字段仅为交接合同记录，不覆盖用户在本会话的明确授权

## 路线合同

1. 测试时只见T0视频内容；目标评论不可见。训练评论只可构造标签、计数和历史反应分布，不可恢复Task30评论teacher/KD。
2. 历史收益标签只能由训练折内OOF预测生成：`Delta_i=JSD(y_i,f0)-JSD(y_i,fH)`；拟合内收益只能作泄漏诊断，不能训练正式router。
3. 路由动作固定为`USE_MEMORY`、`FALLBACK_CONTENT`、`ABSTAIN`；所有路由器必须在相同coverage、候选池、输入、预算和种子下与固定融合、相似度、熵、OOD/generic gate及SelectiveNet式拒答比较。
4. 先证明自然内容—反应错位与Oracle headroom，再训练路由；Oracle无headroom即停止，不得追加模块。
5. aleatoric/group、有限响应sample、epistemic与transfer/retrieval源须各自绑定外部/重采样判据；不可辨识时只报告总不确定性。经验分布预测区域必须同时报告coverage与width，禁止外推总体人口保证。

## 数据角色

| 数据集 | 冻结角色 | 未闭合事项 |
|---|---|---|
| CSMV | 8210视频、107267人工反应标签；H2a/H2b主机制与HUMAN_GOLD主表 | I3D许可、官方revision、权利方身份/fixity仍UNKNOWN；禁止再分发 |
| LAI-GAI | 847图、63682人工评分；H2c中可同构的有限样本、校准/OOD与预测区域外验 | 无视频/历史评论机制；相关项必须N/A |
| Video2Reaction | closest/direct prior与movie-disjoint SILVER外部表候选 | revision、fixity、许可、恢复率和movie split未冻结；不得冒充HUMAN_GOLD |
| MVIndEmo | 候选补充，当前不在正式矩阵 | 合法入口、许可、媒体、标签构念和split未闭合 |

`NEmoP/`只是用户自有未跟踪目录，不是v1.22已批准数据或本次交付物。

## 阻塞/风险

- 尚无EXP-00自然错位、EXP-01 Oracle headroom、EXP-02路由或三源可识别性的实验结果；全部方法claim仍是计划/TO_VERIFY。
- `.light/consistency`四份结构化事实源不存在。Markdown审计未见术语、数值或claim强度冲突，但标准findings导出因`_shared/findings_schema`不可导入而失败，只能记部分覆盖。
- `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md`仍为v0.1.2无正式结果脚手架，尚未吸收v1.22；未经数据/预注册门和受控论文升版不得把计划写成贡献已验证。
- Task10论文数据/协议段落、Task20最小补证及2026-08-31受限存储删除验收仍是并行总控义务。

## 下一步

1. 读取并验证S39、passport、project card、Registry、总纲v1.22、研究方案、实验矩阵与论文SSOT，刷新Task10/20/30实时状态。
2. 验证P0数据identity/fitness并完成版本化系统查新，优先冻结Video2Reaction revision/fixity/许可/movie-disjoint准入；不得下载或执行未授权资产。
3. 检查target chain、failure tree、具体五种子、co-primary reliability终点、多重比较家族和formal-test materialization合同并冻结结果；形成精确`AUTH-00-TASK40-*`前保持Task40未创建。

## 必读文件

1. `.light/handoff/S39-unified-route-master-v122.md`
2. `.light/passport.yaml`
3. `.light/project_card.md`
4. `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.22，重点0.12、6、7、10、11、17节
5. `TASK00_CARM_UNIFIED_ROUTE_RESEARCH_PLAN_20260805.md`
6. `experiments/CARM_UNIFIED_ROUTE_EXPERIMENT_MATRIX_20260805.md`
7. `TASK_REGISTRY.md`
8. `TASK00_TASK30_H1_FINAL_INDEPENDENT_REVIEW_20260804.md`
9. `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md`
10. `WORK_LOG.md`末条与Task10/20/30实时状态

## 禁止

- 不得把本卡当作实时事实；必须先运行`git status --short --branch`、`git log -3`和`git rev-parse HEAD/origin/main`刷新现实，禁止凭卡片猜当前commit或任务状态。
- 不得恢复Task30评论特权teacher/KD、继续调参、materialize其formal test，或把`CLOSED_NOT_PASSED`改写为通过/正式H1拒绝。
- 不得创建Task40/50、运行实验或触碰实验核心，除非00先形成版本化预注册与精确创建/执行授权。
- 不得把Video2Reaction写成HUMAN_GOLD，把LAI-GAI写成视频历史记忆证据，把评论者分布外推为所有观众，或把经验coverage写成无条件总体保证。
- 不得改写G1—G3、I3D UNKNOWN、Task20 NON_T0/INELIGIBLE、论文`TO_VERIFY`或受限存储删除截止；不得读取、提交或删除用户自有未跟踪目录。

## 接续提示词

你是“00-T-AFFC总控03”，不是Task30或未来Task40执行代理。先读AGENTS.md与WORK_RECORD_POLICY.md，刷新Git、WORK_LOG末条和Task10/20/30实时状态；再读S39、passport、project card、Registry、总纲v1.22、统一路线研究方案、实验矩阵与论文SSOT。v1.22只冻结无teacher的历史净收益OOF路由与三源不确定性方案，Task40仍未创建。下一步先完成数据identity/fitness、系统查新、target chain、failure tree、具体五种子、主终点和formal-test禁令；未形成精确`AUTH-00-TASK40-*`前不运行模型、不materialize test、不恢复Task30，不改变G1—G3、I3D UNKNOWN、Task20 NON_T0/INELIGIBLE或论文TO_VERIFY边界。
