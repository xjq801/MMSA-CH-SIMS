# 术语表 — MMSA-CH-SIMS T-AFFC 总控

| 类别 | 标准叫法 | 缩写 | 英文 | 备注 |
|---|---|---|---|---|
| 构念 | 公众诱发受众情绪 | — | public-induced audience affect | 不是说话者情绪、画面群体情绪或传播链 |
| 构念观测边界 | 评论者公开表达的诱发反应分布 | — | publicly expressed induced-reaction distribution among commenters | 不代表所有观看者内在心理状态或总体人口参数 |
| 方法工作代号 | 受众反应记忆 | CARM | Audience-Response Memory | 仅历史工作包代号；完整方法尚未验证，且CARM重名，不得作为正式标题或首创标识 |
| C1贡献边界 | 严格T0受众反应分布预测协议与证据 | — | strict-T0 audience-reaction distribution protocol and evidence | Video2Reaction已覆盖任务层目标；禁止“首次video-to-reaction-distribution” |
| C2候选差异 | train-only历史反应后验效用与风险约束选择 | — | train-only posterior utility of historical reactions and risk-controlled selection | Task30/40/45负边界保持；一般utility/selective routing各有前作，只有领域测量、有效负控和实际策略证据链通过才可作完整方法claim |
| C2核心候选机制 | OOF后验效用分布学习与风险预算策略 | — | out-of-fold posterior utility-distribution learning with a risk-budget policy | 先学习`p(tau)/mu/m+/m-/Q05或CVaR`，再由expected-regret/risk budget映射三动作；推理只看T0查询与train-only邻居诊断；须通过有效跨组负控并优于固定融合、content-entropy/generic gate和SelectiveNet |
| 三源不确定性 | 群体分歧、有限响应抽样与模型/OOD不确定性 | — | group disagreement, finite-response sampling, and epistemic/OOD uncertainty | 三源必须各有held-out、重采样或自然OOD判据；不得由单一浓度参数自证 |
| 预测区域 | 经验反应分布预测区域 | — | prediction region for the empirical reaction distribution | 报告80/90/95% coverage；不保证沉默观看者或总体人口潜在情绪；集合大小不直接等同群体分歧 |
| 路由动作 | 使用历史/纯内容回退/拒答 | — | use memory / fall back to content / abstain | 阈值仅在dev预注册规则下选择，formal test不可用于选择 |
| Task45主目标 | 后验获益概率 | b | posterior probability of positive historical benefit | `P(Delta>0)`；是训练target，不是T0输入 |
| Task45主目标 | 后验正收益幅度 | m | posterior expected positive-benefit magnitude | `E[max(Delta,0)]`；与概率组成AND诊断门 |
| Task45角色 | 诊断拟合/诊断确认/路由确认 | — | TRAIN_DIAG_FIT / TRAIN_DIAG_CONFIRM / TRAIN_ROUTER_CONFIRM | Task45只可用前两者；最后一者完全封存 |
| Task45结果边界 | 探索性弱效用信号、可学习性未通过 | — | exploratory weak utility signal; learnability not passed | Brier/MAE/Spearman因shuffled-target负控失效不能支持正式可学习性；Task45不得改判或补跑 |
| Task46候选目标 | 后验历史效用分布 | — | posterior distribution of historical-reaction utility | `Delta=JSD(content)-JSD(memory)`；估计`p(tau)/mu/m+/m-/Q05或CVaR`，label不是T0输入 |
| Task46候选策略 | 期望后悔与风险预算选择 | — | expected-regret and risk-budget selection | `USE_MEMORY/FALLBACK_CONTENT/ABSTAIN`由冻结策略产生；Q05只作风险约束，不作为唯一动作监督 |
| 可发表性边界 | 有限受众响应噪声下的T0历史效用测量与选择性利用 | — | strict-T0 historical-utility measurement and selective use under finite-response noise | 一般utility prediction/selection不是方法首创；Task45结果不升级正式claim，Task46仍未创建 |
| 论文定位 | 分布偏移与目标响应不可用下的可靠内容到受众反应分布预测 | — | reliable content-to-audience affect distribution forecasting under distribution shift and unavailable target responses | Video2Reaction为closest/direct prior |
| 直接前作 | Video2Reaction | V2R | Video2Reaction | 共同任务必须承认；workshop展示确认、归档状态待核；ECCV为作者报告待正式条目 |
| V2R标签层级 | LLM生成且人工核验银标 | SILVER_LLM_HUMAN_VERIFIED | LLM-derived, human-verified silver labels | 不是逐样本HUMAN_GOLD，不替代CSMV/LAI-GAI主测试 |
| V2R对比A轨 | CSMV公平适配 | V2R-A | CSMV fair adaptation | 同split、T0输入、评测、种子与预算；服务主对比 |
| V2R对比B轨 | Video2Reaction原生外部验证 | V2R-B | Video2Reaction-native external validation | 公开特征复现、movie-disjoint和适用CARM组件；独立分表 |
| 预测时点 | T0内容预测 | T0 | content-only prediction at publication time | 禁止未来评论/互动/推荐结果 |
| 数据层级 | 人工金标 | HUMAN_GOLD | human-annotated gold labels | CSMV与LAI-GAI |
| 数据层级 | 银标 | SILVER | automatically derived labels | 不进入人工test |
| 主指标 | Jensen–Shannon散度 | JS divergence | Jensen–Shannon divergence | 越低越好；正式统计按内容项 |
| 门 | 协议/数据G2 | G2_PROTOCOL_DATA | protocol/data G2 | 当前PASS_WITH_LIMITATIONS |
| 风险状态 | 资产准入延期接受风险 | ASSET_ADMISSIBILITY | deferred accepted asset risk | 不是许可证据 |
| 输入边界 | 实际可得全部输入 | ALL_AVAILABLE_INPUTS | all legally frozen available inputs | 不含理论上可能的音频 |
| 音频状态 | 结构性不可得且不插补 | — | STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED | 不得伪造缺失鲁棒性 |
| I3D主协议 | 完整序列动态padding与mask | — | FULL_SEQUENCE_DYNAMIC_PADDING_MASK | `True=observed` |
| I3D敏感性 | 首尾覆盖均匀180步 | — | UNIFORM_180_ENDPOINT_INCLUSIVE | 前180仅补充 |
