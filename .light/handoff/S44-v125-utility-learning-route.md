---
session_no: S44
contract_version: 2
suggested_title: "[TAFFC] S45 Task45独立关闭审核与Task46预注册"
parent_session: S43
project: MMSA-CH-SIMS-TAFFC-CARM
date: 2026-08-06
---
# S44 — v1.25后验效用学习路线与Task45负控失效边界

## 当前阶段

总控04已把Task40/45失败分析转化为总纲v1.25的“后验效用分布学习→风险预算选择性利用”候选路线。Task45执行代理已交付失败关闭包但尚待总控最终tag审核；Task46只在计划层存在，未创建、未授权、未训练。

## 已完成

- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` — 已由人工diff复核加入v1.25、SC-20260806-02、U0—U5顺序、有效负控、source-group主身份与Task46创建前提；`git diff --check` exit 0。
- `TASK_REGISTRY.md`、`CLAIM_EVIDENCE_MATRIX.md`、`RISK_REGISTER.md`、`DECISION_LOG.md`及`.light/`台账 — 已同步Task45探索性边界与Task46未创建状态；`light-consistency`验证结果为扫描8份材料、0项硬冲突、1项事实源部分覆盖WARN与11项INFO。
- `.light/passport.yaml` revision 24 — 已用底层`passport.py validate`核验，verdict WARN/exit 0；唯一警告是既有stage10 PASS占位缺hash/timestamp，不是本批新实验门。

## 工作区状态

当前分支`codex/total-control04-task45-plan`，本批基线`HEAD=origin/main=fdaaf117e67eb442c412303969d33dd31ce09b01`。总纲v1.25、Registry/claim/risk/decision/passport/project card/terminology/version history、WORK_LOG与本S44构成待提交dirty批次；尚未commit或push。

## 待用户回答

- none — 当前没有待用户回答的问题；用户已明确批准把该方向合并进总纲，但这不等于Task46执行授权，下一步可直接做Task45独立关闭审核与Task46预注册冻结。

## 下一步

1. 验证annotated tag `task45-t0-benefit-learnability-development-20260806`中的Task45 hash、validators、失败run、线程偏差与零访问账，并签发最终关闭裁定。
2. 写入并验证v1.25完整数据身份、target chain、failure tree、公平基线、访问边界、有效跨组负控与machine-readable preregistration，全程不创建Task46。
3. 检查是否已有新的用户执行授权与总控hash-bound创建锚点；两者齐备后才可创建独立Task46，期间继续封存Task50与formal test。

## 阻塞/风险

- Task45两个shuffle负控异常通过，真实标签弱信号只能标记为`EXPLORATORY_SUGGESTIVE_SIGNAL`。
- 正Spearman/top-k enrichment不保证matched-coverage JSD净收益，排序到策略仍受不对称损失与fallback退化约束。
- 旧DEV和DIAG_CONFIRM已看过，重新调阈值或改用video random split作主证据会造成不可修复的确认污染。

## 必读文件

1. `.light/handoff/S44-v125-utility-learning-route.md`
2. `.light/passport.yaml`
3. `.light/project_card.md`
4. `AGENTS.md`、`WORK_RECORD_POLICY.md`与`WORK_LOG.md`末条
5. `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.25、`TASK_REGISTRY.md` v1.20、`CLAIM_EVIDENCE_MATRIX.md` v1.7、`RISK_REGISTER.md`与`DECISION_LOG.md`末条

## 禁止

- 不得把本卡当作当前事实；接手后先运行`git status --short --branch`、`git log -3`及`git rev-parse HEAD/origin/main`刷新现实。
- 不得重做已完成清单中的工作或凭记忆补写未验证结论；不得把Task45探索信号写成正式证明。
- 不得重跑Task45、创建/训练Task46、创建Task50、读取旧DEV/`TRAIN_ROUTER_CONFIRM`/formal test，除非存在新的精确用户授权与总控hash-bound合同。

## 1. 接续身份与Git锚点

- 当前总控：00-T-AFFC总控04，task/thread `019fd19d-b8ef-71f2-82b3-433168211358`；不是Task45或未来Task46执行代理。
- 项目只执行IEEE T-AFFC CARM路线；不得创建或执行IJCV J0—J2、JH1—JH3、任务25或65。
- 本批开始时实际`HEAD=origin/main=fdaaf117e67eb442c412303969d33dd31ce09b01`，分支为`codex/total-control04-task45-plan`。
- 本S44记录总纲v1.25路线冻结批次；写入时变更尚未提交或推送，不得把本卡本身当成远端同步证明。
- 父交接：`.light/handoff/S43-task45-diagnostic-authorization.md`。

## 2. 当前门、SSOT与任务状态

- 当前SSOT：总纲v1.25（第17节任务规范v1.9）、Task Registry v1.20、Claim—Evidence Matrix v1.7、passport revision 24、本S44。
- G1=`PASS`。
- G2协议/数据=`PASS_WITH_LIMITATIONS`；I3D资产=`DEFERRED_ACCEPTED_RISK`；总G2=`PASS_WITH_ACCEPTED_ASSET_RISK`；`formal_split=true`。
- G3=`PASS_WITH_LIMITATIONS`。
- Task10=`CLOSED_MANUSCRIPT_DATA_SECTIONS_ACCEPTED_WITH_LIMITATIONS`。
- Task20=`FORMAL_CORE_CLOSED_RECOVERY_ATTEMPT2_SUPPLEMENT_REQUIRED`；Attempt2永久`NON_T0/INELIGIBLE`且补证未验收；受限存储可见层删除截止`2026-08-31 23:59:59 +08:00`不变。
- Task30永久`CLOSED_NOT_PASSED`，不恢复teacher/KD。
- Task40永久`CLOSED_NOT_PASSED_ROUTER_MAIN_JSD`；P0/P1/P2通过不覆盖P3/P4主JSD 0/5失败，不授权修复。
- Task45执行代理已交付annotated tag `task45-t0-benefit-learnability-development-20260806`，报告状态为`CLOSED_NOT_PASSED_T0_BENEFIT_LEARNABILITY_AWAITING_00_REVIEW`；总控04最终tag/hash/validator独立审核尚未完成。
- Task46=`PLANNED_NOT_CREATED_PENDING_TASK45_REVIEW_AND_V125_PREREGISTRATION`；Task50=`NOT_CREATED`。
- `TRAIN_ROUTER_CONFIRM`与formal test均封存，formal-test访问事件必须为0；论文继续`MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS`，C1—C3=`TO_VERIFY`。

## 3. Task45证据的精确解释

- 实标签诊断出现弱信号：full-G0 PROB Brier差`-0.003122656`、95%CI `[-0.005103636,-0.001159598]`、5/5；MAG MAE差`-0.0000674363`、95%CI `[-0.000110523,-0.0000239202]`、5/5；Spearman约`0.247—0.291`。
- 但两个预注册负控都异常优于constant：PROB shuffle差`-0.003992584`且CI全小于0；MAG shuffle差`-0.003506802`且CI全小于0。因此Task45主可学习性门失败。
- source group近乎全为单例，使“组内shuffle”没有有效改变绝大多数标签；该根因只否定该负控，不授权改成video-level随机划分，也不允许重跑Task45或用同一DIAG_CONFIRM修补。
- 结论边界固定为`EXPLORATORY_SUGGESTIVE_SIGNAL`：可提出“严格T0可能含弱收益排序信号”的待检验假设，不得写成“Task45已经证明收益可预测”、正式结果或C2证据。

## 4. v1.25新科学路线

- 问题从“直接分类是否使用memory”改为“先估计历史受众反应的后验效用分布，再按风险预算决策”。
- 候选目标包括`p_tau=P(Delta>tau|T0)`、`mu_Delta=E[Delta|T0]`、正/负尾幅度、`Q05(Delta)`或预注册CVaR；`Delta=JSD(theta,f0)-JSD(theta,fH)`，`theta|c~Dirichlet(c+0.5)`。
- 决策层与估值层分离：只有估值层通过有效负控、校准与排序门后，才可按expected regret/risk budget输出`USE_MEMORY/FALLBACK_CONTENT/ABSTAIN`。
- 主数据继续CSMV，不因source-group单例而降级为video random split。主身份仍为source-group-disjoint；新负控应使用跨source-group derangement/permutation，并在执行前冻结至少95% target改变且`|rho|<=0.10`的有效性门。
- topic或CLIP embedding cluster只能在FIT内完成无泄漏构造与稳定性审计后作secondary robustness，不得替代主source-group身份。
- 诊断序列冻结为U0身份/泄漏/负控有效性，U1后验utility targets，U2简单基线与T0特征组，U3连续估值/校准/排序，U4固定top-k与risk-budget selective policy，U5仅在主matched-coverage JSD通过后检查负迁移/P5。
- 简单公平基线至少包括constant、similarity heuristic、content entropy、Task40 point router、generic gate、SelectiveNet、fixed fusion；同预算、同coverage、同T0边界。
- Spearman、MAE/Brier、top-k真实收益与uplift曲线只能证明可学习性/排序性；最终自动使用claim仍必须通过预注册的matched-coverage主JSD与风险门，不得用容易通过的诊断指标替换旧失败门。

## 5. 创建与执行边界

- 本批只合并路线与治理边界，没有创建Task46、没有训练、没有读取旧DEV、没有打开`TRAIN_ROUTER_CONFIRM`或formal test，也没有创建Task50。
- Task46创建前必须完成：Task45 annotated-tag独立审核；v1.25数据身份、target chain、failure tree、公平基线、访问边界、有效负控、estimand/指标/停止规则、预算与machine-readable preregistration；用户明确执行授权；hash-bound创建锚点。
- 已看过的旧`DEV_SELECT/DEV_CALIBRATE/DIAG_CONFIRM`不得再次作为确认集。Task46若获批，只能从原train内部重新建立冻结FIT开发与一次性新确认角色；具体角色身份必须在创建前单独冻结。
- 禁止增加seed碰运气、放宽旧门、事后换指标、在旧DEV调阈值、堆模块追分或以Task45探索信号预先宣告Task46会成功。

## 6. 最近行动、最高风险与下一项总控动作

最近三项行动：

1. 独立读取Task40/45 tag交付证据，确认Task40主JSD关闭与Task45负控异常的claim边界。
2. 把“utility distribution estimation → risk-budget policy”写入总纲v1.25，并同步Registry、claim、risk、decision、terminology、project card和passport。
3. 运行底层passport schema/hash校验与`light-consistency`跨材料审计；未把Markdown部分覆盖警告写成完整一致性证明。

三个最高风险：

1. **负控失效/伪可学习性**：Task45真实标签与shuffle都优于constant，弱信号可能来自身份、折分或目标结构而非可迁移效用。
2. **排序到策略的断裂**：正Spearman或top-k enrichment不保证matched-coverage JSD净收益；错误使用memory的损失明显不对称。
3. **确认集耗尽与范围漂移**：旧DEV和DIAG_CONFIRM已看过，若再次调阈值或把topic/video随机切分当主证据，将造成不可修复的确认污染。

下一项总控动作：先从Task45 annotated tag完成独立hash、validator、failed-run、thread-count deviation与零访问账审核并签发关闭裁定；随后只冻结完整Task46预注册包，仍不创建或执行Task46，除非用户另行明确授权。

## 7. 接续提示词

```text
你是00-T-AFFC总控04的接续会话，不是Task45/46执行代理。项目只执行IEEE T-AFFC CARM路线；禁止IJCV J0—J2、JH1—JH3、任务25/65。先fetch并确认origin/main包含S44，再完整读取AGENTS.md、WORK_RECORD_POLICY.md、WORK_LOG末条、.light/passport.yaml revision 24、.light/project_card.md、TASK_REGISTRY.md v1.20、TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md v1.25（第17节v1.9）、DECISION_LOG.md末条、RISK_REGISTER.md、CLAIM_EVIDENCE_MATRIX.md v1.7、.light/terminology.md与本S44。Task40保持CLOSED_NOT_PASSED_ROUTER_MAIN_JSD。Task45 annotated tag=task45-t0-benefit-learnability-development-20260806，报告为CLOSED_NOT_PASSED且仅有EXPLORATORY_SUGGESTIVE_SIGNAL；先独立复核tag/hash/validators/失败run/线程偏差/零访问账，不得重跑Task45。Task46仅PLANNED_NOT_CREATED；在Task45审核和完整v1.25数据身份、target chain、failure tree、公平基线、访问边界、有效跨组负控与machine-readable preregistration冻结前不得创建或训练。旧DEV、TRAIN_ROUTER_CONFIRM和formal test继续封存，Task50不创建。继续监督Task20 2026-08-31受限存储删除截止与I3D UNKNOWN/禁止再分发边界。
```
