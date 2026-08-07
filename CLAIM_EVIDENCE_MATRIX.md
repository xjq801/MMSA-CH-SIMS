# Claim—Evidence矩阵

> 版本：v1.7；日期：2026-08-06  
> 原则：没有证据的主张保持`TO_VERIFY`，不得写成论文结论；`TO_VERIFY`不等于仍有实验授权。

| Claim ID | 核心主张 | 所需证据 | 对应实验/材料 | 当前状态 | 允许措辞 |
|---|---|---|---|---|---|
| C1 | 无泄漏T0协议能形成可审计的公众公开表达诱发反应分布预测证据 | 两个公开人工标注集、内容单元划分、物理泄漏隔离、Data Card | G1/G2、E0、`T0_INPUT_POLICY.md` | TO_VERIFY | 仅可描述协议/证据贡献；任务与分布输出均不称首创 |
| C2 | train-only历史反应的后验效用分布能否在严格T0被学习，并经风险预算选择在匹配coverage下减少错误历史证据负迁移 | Task45 not-passed包只提供探索性Brier/MAE/排序信号；未来Task46须先通过有效跨组负控和FIT nested-OOF概率/幅度/均值/风险学习，再一次性比较content-entropy/point/generic/SelectiveNet/fixed fusion与matched-coverage主JSD及负迁移 | H2a/H2b、E2/E4/E4b/E4c/E7、Task40关闭证据、Task45关闭包、总纲v1.25 | TO_VERIFY | Task40/45候选均已关闭或待行政终审；探索性ranking不是动作证据。一般utility/selective router不是方法首创；Task46/50均未创建 |
| C3 | 群体分歧、有限反应抽样和模型/迁移不确定性能被分别验证，并支持校准的经验反应分布预测区域与选择性可靠性 | held-out/split-half反应；2/4/8/all与8/16/32/all thinning；ensemble/自然group-OOD；单源消融；80/90/95% coverage+width；严格分组与外部边界 | H2c、E4/E5/E6、CAL-01；Task40 P5未执行报告 | TO_VERIFY | 固定顺序阻断后只能写“未检验”；不得宣称三源无效、区域未校准、区域保证、所有观众或因果效应 |
| H1-R | Task30评论特权teacher开发假设 | 冻结Task30开发包；未触及formal test | Task30 | RETIRED_FROM_ACTIVE_CLAIM_SET_DEVELOPMENT_NOT_PASSED | 不得写为正式H1被反驳；不得恢复主方法或进入正式表 |

状态只能是`TO_VERIFY`、`SUPPORTED_LIMITED`、`SUPPORTED`、`REFUTED`。任何状态变更必须填写结果文件、统计证据和复核日期。

## 2026-08-05 Task40开发关闭边界

- Task40只使用train/DEV_SELECT/DEV_CALIBRATE，formal-test access/label/feature/prediction/IDs均为0；其结果不能升级为正式论文结果。
- P1受控错位与P2 Oracle headroom通过，只支持开发机制链前两段，不支持C2路由有效性。
- P3/P4可信router相对最强control主JSD门0/5，五个观察差均为正且95% CI均跨0；活动可信净收益router候选以`CLOSED_NOT_PASSED_ROUTER_MAIN_JSD`关闭，C2不升级。
- 可信负迁移按固定顺序未检验，P5 thinning、三源与预测区域未执行；C3保持无支持证据，正确边界是“未检验”而不是“被反驳”。
- Task50未创建且当前无授权；任何替代路线必须重新冻结计划并由用户明确授权。证据：`TASK00_TASK40_FINAL_INDEPENDENT_REVIEW_20260805.md`。

## 2026-08-06 Task45诊断边界

- 用户批准重新规划，不等于恢复Task40。Task40状态与旧主JSD失败永久保留。
- Task45只在CSMV原train三角色中使用FIT与DIAG_CONFIRM；`TRAIN_ROUTER_CONFIRM`、旧DEV和formal test事件必须为0。
- 两条primary相对同容量content-only的Brier/MAE均表面改善且5/5方向为负，但两条shuffled-target阴性对照也异常优于constant；Task45须保持`CLOSED_NOT_PASSED_T0_BENEFIT_LEARNABILITY`，等待00独立行政终审。
- Spearman约0.247—0.291、top-decile enrichment、支持量、Q05和逐组消融只允许写成`EXPLORATORY_SUGGESTIVE_SIGNAL`，不能支持“收益可预测”、路由有效、负迁移、P5、C2或C3升级。
- 增量closest-prior已阻断“一般两阶段utility router为新算法”的措辞；允许上限是受众响应有限样本下的领域诊断贡献。

## 2026-08-06 v1.25候选Task46边界

- 用户批准把未来科学问题改写为“估计历史受众反应知识的后验可迁移效用，再在风险预算下选择性利用”，但这只是路线决定和预注册准备，不是Task46创建/训练授权。
- source-group singleton只使旧组内shuffle失效，不支持video-level随机split；主身份继续source-group-disjoint，未来负控必须跨组有效置换并满足预冻结改变率/相关/constant门。
- U1效用学习证据至少需要相对G0 content-only的预注册proper-loss改善、五seed方向稳定、有效shuffled/random-neighbor负控及排序/校准全报告。Spearman>0或top-k富集不能单独升级C2。
- U3策略证据仍需一次性`TRAIN_ROUTER_CONFIRM`、同预算同90% coverage、相对每seed最强control的视频级paired JSD主门；该门通过前负迁移/P5固定`NOT_TESTED`。
- 任何Task46成功仍是development evidence；formal test和Task50另需用户授权，C1—C3继续`TO_VERIFY`。

## 2026-08-07 Task45独立关闭与Task46执行边界

- 总控04已从 `task45-t0-benefit-learnability-development-20260806` 独立复核 P0/P1/P2、CRLF归一化hash、one-shot marker、异常shuffled-target、线程数偏差和零访问账；Task45正式登记为`CLOSED_NOT_PASSED_T0_BENEFIT_LEARNABILITY`。
- Task45的Brier/MAE/Spearman/top-decile只保留`EXPLORATORY_SUGGESTIVE_SIGNAL`，不支持“T0收益已被证明可学习”、动作routing、负迁移改善、P5或C2/C3升级。
- 用户明确要求执行共享对话与《任务安排.docx》中的下一步方案后，00只冻结v1.25 Task46 P0/P1/P2/P3合同；旧文档的复用DIAG_CONFIRM、固定10% memory和无ABSTAIN规则被当前SSOT的重建角色、跨组有效负控、0.90 non-abstain coverage和三动作risk-budget规则替代。
- Task46未创建前不产生任何确认集或formal证据；`TRAIN_ROUTER_CONFIRM`只有在U0—U2与策略hash全部冻结后才可一次性打开，主JSD通过前负迁移/P5固定`NOT_TESTED`，Task50仍未创建。

## 2026-07-14 前作约束（不改变实验支持状态）

| Claim/边界 | 已核前作 | 对允许措辞的限制 | 证据文件 |
|---|---|---|---|
| C1任务定位 | NEmo+、CSMV/MSA-CRVI、MVIndEmo、iNews | 不得声称首次提出公众诱发情绪或分布预测；只可强调严格T0与group-held-out协议 | `LITERATURE_SEARCH_REPORT.md`、`CONTRIBUTION_PRIOR_ART_MATRIX.md` |
| 历史H1-R机制 | LUPI、generalized distillation、M2PKD | teacher/student和训练期特权信息不是贡献；Task30已退出活动claim集 | 同上 |
| C2历史记忆机制 | RAMER | 检索增强缺失模态情绪识别已有直接前作；必须做no/random/BM25/CLIP-kNN和RAMER式对照 | 同上 |
| C3可靠性 | Selective Classification、SelectiveNet、MissModal、IMDer、HRLF | 拒绝和缺失模态鲁棒不是模块级首创；只检验其在public-induced distribution、OOD和选择性风险下的证据 | 同上 |

上述查新只冻结主张上限，不把C1—C3从`TO_VERIFY`升级为`SUPPORTED`；任何有效性表述仍须等待预注册实验与统计证据。

## 2026-07-23 Video2Reaction增量约束

| Claim/边界 | 新近前作 | 对允许措辞的限制 | 强制证据动作 |
|---|---|---|---|
| C1任务定位 | Video2Reaction，arXiv:2607.06875 v1；workshop展示已确认；ECCV为作者报告待正式条目 | C1只能称严格T0、HUMAN_GOLD、group-held-out和future-comment isolation的协议/证据贡献；禁止任务首创与“分布输出即创新” | 任务50执行其VLM直接微调/LDL公平适配，或提交输入/标签/split/许可/资源/预算不可比审计 |
| 历史H1-R评论教师 | Video2Reaction未覆盖已定位的训练期评论特权链，但LUPI/M2PKD/评论增强已覆盖组件 | Task30开发未通过且已退出活动claim集 | 归档负边界；不进入正式实验 |
| C2反应记忆 | Video2Reaction未覆盖已定位的train-only反应记忆与负迁移拒绝；RAMER/SelectiveNet覆盖相邻组件 | 不得以模块组合证明创新；必须证明可信净收益路由优于随机/普通近邻/点路由/generic gate且识别有害邻居 | E2/E4/E7、MEAS-01、错误邻居、OOD、负迁移率和risk-coverage |

本节不改变当前C1—C3的`TO_VERIFY`状态，不追溯改变G1—G3；Task30的H1自2026-08-04起只作归档负边界。

## 2026-07-28 Video2Reaction双轨证据合同

| 轨道 | 证据角色 | 必须保持一致/必须审计 | 可支持的主张 | 不可支持的主张 |
|---|---|---|---|---|
| A：CSMV公平适配 | closest prior在本项目证据地基上的最强直接基线 | 同CSMV split、T0输入、标签、评测器、五种子、模型选择与调参预算；VLM输入不可得项显式登记 | CARM相对最近直接方法在同协议下的分布、校准或选择性差异 | 用Video2Reaction论文原生Top-3 F1代替公平对比；虚构CSMV音频/文本 |
| B：Video2Reaction原生外部验证 | 银标电影视频域上的复现、movie-disjoint和适用机制外部效度 | HF revision/许可/fixity；官方split与movie identity；train-only memory；原始评论不可得；作者指标与本项目指标分栏 | C2/C3在另一视频域的有限外部支持，或清晰失败边界 | 第三HUMAN_GOLD主集；H1评论teacher证据；与CSMV绝对指标横比 |

- B轨标签固定为`SILVER_LLM_HUMAN_VERIFIED`；双盲人工核验质量不能把逐样本分布升级为人工金标。
- A轨优先级高于B轨原始VLM恢复；B轨媒体恢复受阻时，先完成公开派生特征基线与不可执行审计。
- 两轨所需档案固定为`VIDEO2REACTION_DATA_INTAKE.md`、`video2reaction-source-v1.manifest.json`、`VIDEO2REACTION_REPRODUCTION_REPORT.md`、`VIDEO2REACTION_MOVIE_SPLIT_AUDIT.md`和`V2R_BASELINE_ADAPTATION_REPORT.md`。
- 本合同不升级C1—C3，不改变G1—G3；任何“优于Video2Reaction式方法”仍须等待任务50五种子与原生内容单位统计。

## 2026-07-27 第17节收益感知路由执行合同

- 收益感知router不是通过改名获得创新资格：任务40必须用train内部cross-fitting/out-of-fold预测构造检索效用标签，路由推理不得读取真实标签、目标响应或评测后误差。
- 强对照至少包括固定融合、相似度阈值、预测熵阈值和SelectiveNet式拒绝；选择性方法必须匹配coverage或风险预算。
- 正式证据必须覆盖五种子、按原生内容单元paired bootstrap、检索效用、负迁移率、被避免负迁移比例、AURC/risk-coverage和OOD/污染负对照。
- 若上述机制链不成立，C2降级为普通检索融合或负结果；不得用平均分小幅改善替代路由机制证据。

## 2026-07-24 Claim blacklist与构念边界

- `TAFFC_CLAIM_BLACKLIST_20260724.md`是活动主张禁用表，覆盖标题、摘要、引言、贡献、相关工作、结论、PPT和答辩材料。
- 社媒评论标签只支持“评论者公开表达的诱发反应分布”，不支持“所有观看者真实内在情绪”。
- Video2Reaction必须称`closest/direct prior`；“尚未定位完全同构方法”只允许写成scoping未检出，不得写世界首创。
- 本节不升级任何有效性状态。

## 2026-07-16 CSMV输入与主张上限

| 边界 | 冻结证据 | 允许措辞 | 禁止措辞 |
|---|---|---|---|
| CSMV内容输入 | `csmv-i3d-sequence-protocol-v1.manifest.json`；8210/8210 shape/fixity | “冻结I3D视觉表征上的公众诱发受众情绪分布预测” | 端到端视频编码、原始帧学习 |
| 序列处理 | 完整序列主协议；确定性均匀180步主敏感性；前180补充 | 视觉序列处理消融/敏感性 | 多模态增量、看到test后选择规则 |
| 音频与评论 | `experiment-protocol-v2.md`；00音频复审 | 评论特权监督；音频结构性不可得 | 音视频融合、音频增益、评论文本T0输入 |
| 资产准入 | 本地fixity已闭合；维护者证明延期；`SC-20260717-01` | “内部研究使用，资产外部证明为已接受延期风险” | “官方资产已确认”“权利方已授权”“官方checksum已闭合” |

本节只收紧未来论文措辞，不把当前C1—C3的有效性状态升级为`SUPPORTED`。

## 2026-07-16 IJCV独立claim合同（已迁出归档）

> 下列J-claims是总纲v1.14时期的历史快照，已随`SC-20260716-03`迁至独立IJCV项目。本项目不得执行、更新或把它们计入当前claim集合；T-AFFC当前活动claim集合只有C1—C3。表内`TO_VERIFY`仅记录迁出时状态，不代表本项目仍有对应待办。

| Claim ID | 核心主张 | 所需证据 | 对应实验/材料 | 当前状态 | 允许措辞 |
|---|---|---|---|---|---|
| J-C1 | 响应分布几何监督能学习更适合主观情绪分布的视觉表征 | 至少两个像素人工分布集；PC/SAMNet/MFRN及强ViT/CLIP公平基线；JSD/EMD/NLL、5种子、按图像CI | JH1、J1—J3、任务25 | TO_VERIFY | 仅可描述假设与方法动机 |
| J-C2 | 显式分歧建模能改善区间/选择性可靠性且分布误差非劣 | 可识别的观察者分歧estimand、coverage/NLL/Brier/AURC、softmax/Dirichlet/ensemble对照 | JH2、J4—J5、任务25 | TO_VERIFY | 不得把预测熵等同观察者分歧或认知不确定性 |
| J-C3 | 分布几何保持能在标签空间不完全同构时支持跨域视觉迁移 | 预注册跨域estimand、数据集特定head、source-only/fine-tune/域适配对照 | JH3、J6/J8、任务25 | TO_VERIFY | 不得声称统一标签空间或跨域有效 |

迁出边界：J-C1—J-C3及其后续证据只在`D:\MMSA-CH-SIMS - IJCV方向`维护；本项目不得把其主实验、主表或方法改名复用。历史方案文件仅用于解释范围变化，当前执行事实源为T-AFFC总纲v1.15。

## Task46 P0 独立复核（2026-08-07）

| Claim/证据 | 当前状态 | 边界 |
|---|---|---|
| Task46 FIT 身份、跨 source-group 有效负控与零访问门 | `P0_ACCEPTED` | 仅证明角色重建、置换算法和访问控制可审计；不证明 utility 可学习或 policy 有效 |
| 后验 utility prediction / nested OOF / risk-budget policy | `BLOCKED_P1_CONTENT_ASSET_ADMISSIBILITY` | 没有第二个 hash-bound、许可/revision/fixity 已闭合的 T0 内容表示；P1/P2/P3 未执行 |
| Task46 P0 伪特征 null sanity | `IMPLEMENTATION_SANITY_ONLY` | identity-hash pseudo-feature 不是 scientific T0 feature，不得写入论文结果或 claim |
| I3D/VideoMAE 内容资产 | `UNKNOWN_NOT_ADMISSIBLE` | 本次真实读取为0；不确认、不再分发、不以其支撑任何结果 |
| Task40/Task45、formal test、Task50 | `CLOSED_OR_SEALED` | Task40/45关闭结论不变；formal test零 materialization；Task50不创建 |
