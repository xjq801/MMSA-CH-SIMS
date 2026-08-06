# CARM v1.24 可发表性与closest-prior增量审计

> 审计日期：2026-08-06（Asia/Shanghai）  
> 裁定：`CONDITIONAL_GO_DIAGNOSTIC_ONLY_METHOD_NOVELTY_BLOCKED`  
> 适用范围：Task40关闭后的替代路线规划；不授权恢复Task40、创建Task50或访问formal test

## 1. 审计问题与程序限制

本轮问题是：在Task40已证明Oracle存在、但五个seed的可信router均零次`USE_MEMORY`且主JSD门0/5之后，能否把“先学习历史记忆的获益概率与幅度，再按期望遗憾/风险预算执行三动作”作为足以支撑IEEE T-AFFC的方法贡献。

用户已在审计前明确给出该方向，因此无法满足idea-critique技能的blind-then-open盲审顺序。本审计不伪称盲审；它以v1.23已冻结的反证门、Task40负结果和新增closest-prior为ex ante边界，并把程序限制记为保守降级理由。

## 2. 增量closest-prior

| 前作 | 已覆盖的核心思想 | 对本路线的约束 |
|---|---|---|
| SelectiveNet（PMLR 2019） | 联合优化预测与拒绝、按目标coverage工作 | 拒答、risk-coverage和matched coverage不是创新 |
| Learning to Defer（NeurIPS 2018） | 在模型与外部决策者之间学习延迟/转交 | 三动作或专家路由不是创新 |
| Adaptive-RAG（ICLR 2024） | 预测查询复杂度并选择不同检索动作 | “先判断是否需要检索”不是创新 |
| Expected Reward Prediction for Model Routing（ICLR 2025 OpenReview） | 在生成前预测不同系统的期望reward并按成本路由 | 预响应效用预测和成本约束路由已有直接家族 |
| Predicting Retrieval Utility and Answer Quality in RAG（arXiv:2601.14546） | 把有/无上下文的性能增益定义为retrieval utility，并用检索器、读者和文档特征预测 | “预测历史/检索是否有益”与本提议高度碰撞 |
| R3AG（arXiv:2604.22849） | 区分retrieval quality与generation utility | 两阶段质量/效用分解不是模块级新颖性 |
| Modality Relevance is not Modality Utility（arXiv:2607.05438） | 先测Oracle headroom，再估计value-of-escalation并受成本约束 | Oracle→效用预测→升级动作的通用链条高度相近 |

公开定位：

- <https://proceedings.mlr.press/v97/geifman19a.html>
- <https://proceedings.neurips.cc/paper/2018/hash/09d37c08f7b129e96277388757530c72-Abstract.html>
- <https://openreview.net/forum?id=eqlRvIeOyYzc>
- <https://openreview.net/forum?id=87JyHeA8f6>
- <https://arxiv.org/abs/2601.14546>
- <https://arxiv.org/abs/2604.22849>
- <https://arxiv.org/abs/2607.05438>

这些工作不是都与受众情绪分布同构，但足以否决“概率+幅度两阶段效用路由本身是新算法”的表述。投稿前仍需滚动查新；本轮不是PRISMA系统综述，也不能支持穷尽性或首创性措辞。

## 3. fatal-flaw与可发表性裁定

### 3.1 方法新颖性：阻断

一般效用预测、选择性路由、拒答、风险预算和两阶段效用分解均已有强近邻。若只把Task40的`Q05(Delta)`单头改为`P(Delta>0)+magnitude`双头，将被合理评价为结果驱动的模块替换，不能单独支撑T-AFFC方法贡献。

### 3.2 测量问题：条件可发表

尚有一条更窄、可证伪且与T-AFFC读者相关的科学问题：在目标响应不可见、响应支持量有限且历史证据可能负迁移时，T0可得诊断是否真的含有可泛化的历史收益信息；Task40的Oracle headroom与零`USE_MEMORY`退化之间为何断裂。只有独立确认集上同时证明获益概率和获益幅度可学习，才能继续讨论路由器；否则应把它写成严格边界下的负结果/测量研究，而不是继续追分。

### 3.3 数据身份：条件可用

Task45只需要既有CSMV原始train角色，不需要新数据。I3D license、官方revision、权利方包身份/fixity仍为`UNKNOWN`，仅允许内部研究且禁止再分发。评论者公开表达不代表所有观看者内在情绪。原DEV_SELECT、DEV_CALIBRATE和formal test全部排除。

## 4. 允许的claim上限

- 允许：研究“有限响应噪声下，train-only历史收益在T0是否可学习”，并报告通过、失败或不确定。
- 条件允许：若Task45通过，可把两阶段效用模型作为后续候选实现，而不是方法首创。
- 禁止：`first`、`novel utility router`、`new selective learning paradigm`、`verified robust memory routing`、`formal improvement`。
- Task45结果只属于开发诊断，不进入正式有效性主表，不升级C1—C3。

## 5. 决定

1. Task40保持`CLOSED_NOT_PASSED_ROUTER_MAIN_JSD`，不修复、不重开。
2. Task50保持`NOT_CREATED_FIXED_ORDER_BLOCKED`。
3. 创建独立Task45是必要的，但只授权train-only可学习性诊断，不授权两阶段路由训练。
4. Task45通过后也必须停止并回交；由总控另写Task46预注册、复核查新和预算，才可决定是否创建Task46。
5. Task45失败或不确定时关闭该替代路线，不增加seed、不放宽门、不改主指标、不借P5或外部数据挽救。

