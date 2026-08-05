# CARM 三 idea 统一路线实验矩阵

> 版本：v1.1（2026-08-05）  
> 状态：`PREREGISTRATION_GATES_CLOSED_AWAITING_EXACT_TASK40_CREATION_AUTHORIZATION`  
> 决策：`SC-20260805-01`  
> 上位文件：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.23  
> 详细方案：`TASK00_CARM_UNIFIED_ROUTE_RESEARCH_PLAN_20260805.md`

## 1. 冻结问题与估计量

- 目标任务：视频刚发布、目标评论尚不可见时，仅凭 T0 内容预测评论者公开表达的诱发反应分布。
- 核心问题：历史反应记忆何时有净收益，模型能否在使用记忆、退回内容模型和拒答之间作出可校准决策。
- 主要估计量：在相同评测单位和 coverage 下，统一路线相对内容模型的成对 JSD 差；负值表示改善。
- 路由监督：训练折内 OOF 生成 `Delta_i = JSD(y_i,f0)-JSD(y_i,fH)`；禁止用同一样本的拟合内预测生成收益标签。
- 实验单位：CSMV 以冻结 source-family/video 单位为主；LAI-GAI 以冻结 group/sample 单位为主；Video2Reaction 以其冻结 movie-disjoint 单位为主。
- 选择动作：`USE_MEMORY`、`FALLBACK_CONTENT`、`ABSTAIN`。
- 正式 test：在模型、路由、阈值、coverage 网格和随机种子全部冻结后只 materialize 一次；本矩阵本身不构成执行授权。

## 2. 数据角色

| 数据集 | 角色 | 当前可用范围 | 必过准入门 | 禁止外推 |
|---|---|---|---|---|
| CSMV | 主机制与主 HUMAN_GOLD 评测 | 8210 视频；冻结 split 5698/837/1675；107267 条人工反应标签 | 既有 G1/G2、source-family 隔离、I3D 风险披露、T0 输入审计 | 不代表所有观看者；I3D 许可/官方 revision/权利方身份-fixity 仍 UNKNOWN |
| LAI-GAI | 跨域、校准和小样本稳健性 | 847 图；冻结 split 594/127/126；63682 条人工评分 | 既有资产/分组审计；视频、评论历史和原生检索项记 N/A | 不称第二视频复现，不用于证明视频时序机制 |
| Video2Reaction | closest/direct prior 与外部 SILVER 验证 | 仅在 revision、文件树、hash、许可边界和 movie split 冻结后使用 | source manifest、恢复率、movie-disjoint、银标隔离、公平适配 | 不冒充 HUMAN_GOLD；不与 CSMV 绝对指标横比；缺原始评论时相关机制 N/A |
| MVIndEmo | 候选补充，不在当前正式矩阵 | 当前未形成可审计资产闭环 | 可访问性、许可、标签构念、split 与 fixity 全部重审 | 未过门前不得列为正式数据证据 |

NEmoP 与任何本地临时目录均不属于本路线的已批准数据；不得因文件存在而自动纳入实验。

## 3. 主实验矩阵

| 实验ID | 对应假设 | 数据集 | 目的与T0输入 | baseline | 指标 | 已控混淆/负对照 | 随机种子 | 完成判定 | 状态 |
|---|---|---|---|---|---|---|---|---|---|
| EXP-00 | H2（H2a） | CSMV | 测量连续内容相似度与反应距离；T0只含视频内容 | shuffled reaction、source/support controls | 相关/分层效应、JSD、错位率 | 控制支持量、source family与抽样不稳定性；随机反应负对照 | 1364847620/426925854/1839464886/1138176833/484191872 | 控制混杂后错位率/相关效应的paired-bootstrap 95% CI仍支持自然错位；否则停止历史路由路线 | 未开始 |
| EXP-01 | H2（H2a） | CSMV | 测量Oracle在内容模型与历史模型间选择的headroom；T0只含视频内容 | content-only、memory-only、fixed fusion | Oracle JSD差、负迁移率、动作上界 | 随机/错配邻居；同split、输入、候选池、评测器和预算 | 同EXP-00 | Oracle相对最强单专家/固定融合的JSD改善paired-bootstrap 95% CI下界>0；否则删除路由主张 | 未开始 |
| EXP-02 | H2（H2b） | CSMV | 验证OOF点收益与可信净收益三动作路由；T0无目标评论 | 固定融合、相似度门、熵门、OOD/generic gate、SelectiveNet式拒答门、点收益路由 | coverage-matched JSD差、负迁移率（主可靠性）、AURC、动作比例 | 点与后验收益标签仅由训练折内OOF生成；错配历史；同候选池和预算 | 1364847620/426925854/1839464886/1138176833/484191872 | 90% coverage下相对最强点收益/generic gate的JSD差95% CI上界<0，且负迁移率不劣；否则降级 | 未开始 |
| MEAS-01 | H2（H2a/H2b/H2c） | CSMV、LAI-GAI | CSMV `k=2/4/8/all`、LAI-GAI `k=8/16/32/all`反应稀释；Dirichlet(0.5/1)与bootstrap后验敏感性 | all-response target | 收益符号稳定性、后验概率/下分位、coverage/width | CSMV跨k主比较用n>=8共同样本；LAI-GAI无联合12D受试者向量，只做维度边际重抽样 | 同上 | 负迁移判断不能只在all-response或单一先验下成立；否则删除可信净收益强claim | 未开始 |
| EXP-03 | H2（H2b） | CSMV自然group/OOD | 检查邻居质量下降时路由能否阻断负迁移 | random、wrong-domain、low-sim neighbors与最强简单gate | 负迁移率、AURC、routing regret、JSD | 自然group/OOD和人工污染分开报告；相同coverage与候选池 | 同EXP-00 | 负迁移率差或AURC差的paired-bootstrap 95% CI优于最强简单gate；否则删除OOD机制claim | 未开始 |
| ABL-01 | H2（H2b） | CSMV | 只移除benefit target，保留同架构 | 完整OOF收益路由、generic gate | JSD、AURC、负迁移率 | 相同参数量、训练预算与输入 | 同EXP-00 | 完整模型相对消融的JSD/AURC/负迁移率预注册主指标95% CI支持净效用监督；否则删除该归因 | 未开始 |
| ABL-02 | H2（H2c） | CSMV、LAI-GAI | 只移除group/aleatoric源 | 完整三源模型 | 区域coverage/width、ECE、JSD | 其余两源、校准集和预算固定 | 同EXP-00 | held-out/split-half判据与coverage/width预注册指标95% CI支持独立价值；否则删除该源claim | 未开始 |
| ABL-03 | H2（H2c） | CSMV、LAI-GAI | 只移除sample源 | 完整三源模型 | 区域coverage/width、ECE、JSD | 评论/评分下采样负对照；其余两源固定 | 同EXP-00 | 下采样判据与coverage/width预注册指标95% CI支持独立价值；否则删除该源claim | 未开始 |
| ABL-04 | H2（H2c） | CSMV、LAI-GAI | 只移除epistemic或transfer/retrieval源 | 完整三源模型 | 选择风险、AURC、区域coverage/width | ensemble、group-OOD与无历史数据集N/A边界 | 同EXP-00 | ensemble/OOD判据与选择风险/AURC预注册指标95% CI支持独立价值；否则只报告总不确定性 | 未开始 |
| CAL-01 | H2（H2c） | CSMV、LAI-GAI | 固定模型，只在dev校准80/90/95%经验分布预测区域 | global radius、entropy-only | 经验coverage、区域width、ECE | test不可见；阈值与coverage网格预先冻结 | 同EXP-00 | 每个目标coverage的95% CI达到预注册容差并同时报告有限width；否则删除预测区域claim | 未开始 |
| GEN-01 | H2（H2b/H2c） | Video2Reaction | revision、fixity、许可与movie-disjoint准入后做独立SILVER外部验证 | direct/LDL、fixed memory/gate | JSD、AURC、区域coverage/width | 禁止目标test调参；HUMAN_GOLD与SILVER分表 | 同EXP-00 | 独立报告JSD/AURC/coverage/width的paired-bootstrap 95% CI；不可同构项记N/A，不作跨数据横比 | 未开始 |

## 4. 消融与负对照

| ID | 唯一变化 | 要回答的问题 | 预注册判据 |
|---|---|---|---|
| `DIAG-01` | OOF 收益标签改为拟合内标签（仅诊断，不进正式主表） | OOF 是否真正阻断收益标签乐观偏差 | 若拟合内显著更好但 OOF 消失，判为标签泄漏风险，不支持路由 |
| `DIAG-02` | 移除历史记忆 | 改善是否来自历史反应而非路由容量 | 与 `EXP-02` coverage 匹配比较 |
| `DIAG-03` | 移除收益路由，固定融合 | 路由是否优于无条件参考历史 | 比较 JSD、负迁移率与 risk-coverage |
| `DIAG-04` | 错配历史反应/随机邻居 | 模型是否只是利用额外容量或先验 | 错配不应产生与正确历史相同的稳定收益 |

## 5. 公平性与统计合同

- 所有路由对照共享同一内容编码器、历史候选池、训练预算、split、seed 集和评测实现；差异只在路由/选择规则。
- Task40开发种子冻结为`[1364847620, 426925854, 1839464886, 1138176833, 484191872]`；Task50若沿用必须在formal-test合同中再绑定，不得根据dev结果替换。
- 主比较使用原生实验单位的 paired bootstrap 置信区间；多项主张按预注册家族进行校正。
- 选择性模型必须在相同 coverage 上比较；禁止以更低 coverage 换取更好风险后直接宣称优越。
- 分布预测区域必须同时报告经验 coverage 与区域宽度；禁止只报 coverage。
- test 只作冻结后的最终估计，不用于选择模型、阈值、邻居数、记忆容量或不确定性组合。

## 6. 顺序与停止规则

1. `P0`：完成数据 identity/许可/构念/split/fixity 准入，特别是 Video2Reaction。
2. `P1`：冻结 target chain、failure tree、主/次估计量、五种子和 test materialization 合同；由00签发Task40创建授权。
3. `P2`（Task40首门）：只在 train/dev 复现内容强基线并运行 `EXP-00`。
4. `P3`（Task40止损门）：运行 `EXP-01`；Oracle 无 headroom 即停止历史路由路线。
5. `P4`：仅在Oracle通过后运行 `EXP-02`、`EXP-03`、`ABL-01`、`MEAS-01`与诊断负对照；不胜强通用门即降级。
6. `P5`：仅在 P4 通过后运行 `ABL-02`至`ABL-04`与`CAL-01`。
7. `P6`：Task40完成开发冻结后才可申请Task50与formal test；本矩阵永不授权formal test materialization。

Task40创建的前置条件是文档/数据身份/泄漏/统计合同闭合及精确授权。Oracle headroom、OOF标签实现和强通用门结果是Task40内的串行开发门，不得再循环写成Task40创建前提。
