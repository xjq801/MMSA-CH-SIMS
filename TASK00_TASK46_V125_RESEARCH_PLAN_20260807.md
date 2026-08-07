# Task46 v1.25 研究计划（P0冻结包，未创建任务）

## 定位

工作标题：`Learning When Historical Audience Reactions Are Trustworthy for Affect Distribution Forecasting`。这不是 Task40/Task45 修复，也不是把普通 utility routing 写成方法首创。Task40 和 Task45 的失败边界保留；本计划只把共享回答/《任务安排.docx》中的可用思想迁移到当前 v1.25 合同。

核心问题：在目标评论不可见的严格 T0 条件下，能否从当前内容、train-only 历史邻居几何/反应证据和专家交互估计历史反应知识的后验效用分布，并在冻结的 expected-regret/risk budget 下选择 `USE_MEMORY`、`FALLBACK_CONTENT` 或 `ABSTAIN`。

数据继续使用 CSMV；source-group 仍是主身份、OOF 隔离和 cluster-bootstrap 单位。不得用 video-level random split 替换它。已看过的 `TRAIN_DIAG_CONFIRM`、旧 `DEV_SELECT`、旧 `DEV_CALIBRATE` 不得重新成为确认集；`TRAIN_ROUTER_CONFIRM` 仍封存，formal test 永久封存。

## 串行阶段

### P0：身份与有效负控门

只读重算原始 train 角色、FIT folds、ROUTER_CONFIRM 零访问、source-group/fold 零重叠。实现跨 source-group、按 response-support 分层的 constrained derangement；预注册硬门为 target 改变率 ≥0.95、`|rho|≤0.10`、零 role collision、层内边际保持且 shuffled 模型不得优于 constant。synthetic 与 FIT 验证未全部通过时停止，不消费确认角色。

### P1：OOF 后验效用 target

在 FIT 的 source-group nested OOF 专家预测上构造 `Delta=JSD(theta,f0)-JSD(theta,fH)`，主 posterior 为 `theta|c~Dirichlet(c+0.5)`、200 个确定性 draws，`c+1` 仅敏感性。冻结并输出 `p_tau=P(Delta>tau)`、`mu=E[Delta]`、`m+`、`m-`、`Q05/CVaR`、support strata 与 posterior calibration。查询响应数、查询评论、真实 Delta 和任何 confirmation 派生量不得进入特征。

### P2：nested-OOF 可学习性

固定五个 seed，在 FIT 内比较 constant、G0 content-only、相似度/邻居一致性启发式、G1/G2/G3 逐组消融、完整 G0—G3、diagnostics-only 和有效 shuffled/random-neighbor null。主门同时要求概率与幅度 proper loss 相对 G0 的预注册 CI 改善、5 seed 方向稳定和负控合格；Spearman、Pearson、top-10/20% gain、uplift 与校准只作排序/解释证据。

### P3：策略冻结

只在 FIT nested OOF 内冻结校准器、`tau=0` 与 `tau_h=0` 的主方向定义、SESOI 规则、expected-regret、LCB/CVaR 风险预算、coverage=0.90（90% 样本有动作，10% 允许 ABSTAIN）和三动作映射。阈值、coverage、lambda、模型、baseline 和指标不得从 ROUTER_CONFIRM 反推。

### P4：一次性确认主门

所有代码、配置、环境、seed、feature schema、target manifest、负控报告、策略、baseline、hash 和成功/失败规则冻结后，才允许一次性打开 `TRAIN_ROUTER_CONFIRM`。在同数据、同五 seed、同 90% coverage 下比较 always-content、always-memory、fixed fusion、content-entropy selective、Task40 point router、generic gate、SelectiveNet 与新策略。主终点仍是相对每 seed 最强 control 的视频级 paired JSD；不得以 Spearman、top-k 或固定 10% memory 选择替代主门。

### P5：固定顺序的后续证据

只有 P4 主 JSD 通过才检验负迁移、routing regret、risk-coverage/AURC、错误邻居/OOD；只有这些通过才允许 response thinning、三源不确定性、预测区域和条件性 Video2Reaction 外验。任一前门失败均关闭后续，不创建 Task50。

## 成功/失败/无效

- `P2_PASS_UTILITY_LEARNABILITY`：只说明合法 T0 诊断有有限效用预测/排序信息，不等于动作有效。
- `P4_PASS_POLICY_MAIN_JSD`：策略在匹配 coverage 下相对最强 control 通过预注册 JSD CI 与 seed 一致性，才可进入 P5。
- P2 通过而 P4 失败：仅报告 utility measurement/negative policy result。
- P2 失败或负控失败：关闭 Task46，不加 seed、不换指标、不改数据、不调 confirmation 阈值。
- 任意确认集提前访问、角色碰撞、特征泄漏、配置未冻结或 formal-test 事件：`INVALID_LEAKAGE_BLOCKED`，不产生科学结论。

## 论文边界

候选叙事是“learning the transferable utility of historical audience reactions under risk”。普通 utility prediction、selective prediction、learning-to-defer、三动作或 probability-plus-magnitude 分解均已有近邻，不得写成首创。C1—C3 继续 `TO_VERIFY`，直到正式证据另行验收。

