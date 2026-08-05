# 术语表 — MMSA-CH-SIMS T-AFFC 总控

| 类别 | 标准叫法 | 缩写 | 英文 | 备注 |
|---|---|---|---|---|
| 构念 | 公众诱发受众情绪 | — | public-induced audience affect | 不是说话者情绪、画面群体情绪或传播链 |
| 构念观测边界 | 评论者公开表达的诱发反应分布 | — | publicly expressed induced-reaction distribution among commenters | 不代表所有观看者内在心理状态或总体人口参数 |
| 方法工作代号 | 受众反应记忆 | CARM | Audience-Response Memory | 仅历史工作包代号；完整方法尚未验证，且CARM重名，不得作为正式标题或首创标识 |
| C1贡献边界 | 严格T0受众反应分布预测协议与证据 | — | strict-T0 audience-reaction distribution protocol and evidence | Video2Reaction已覆盖任务层目标；禁止“首次video-to-reaction-distribution” |
| C2候选差异 | train-only历史反应净效用与三源可靠性 | — | train-only historical-reaction utility and tri-source reliability | Task30评论teacher保持关闭；组件各有前作，只有统一判别实验通过才可作完整方法claim |
| C2核心候选机制 | OOF收益感知可靠性路由 | — | out-of-fold benefit-aware reliability routing | 用train内部OOF误差差学习历史相对content-only是否有益；推理只看T0查询与邻居诊断；须优于固定融合、相似度/熵/OOD/generic gate和SelectiveNet并减少自然负迁移 |
| 三源不确定性 | 群体分歧、有限响应抽样与模型/OOD不确定性 | — | group disagreement, finite-response sampling, and epistemic/OOD uncertainty | 三源必须各有held-out、重采样或自然OOD判据；不得由单一浓度参数自证 |
| 预测区域 | 经验反应分布预测区域 | — | prediction region for the empirical reaction distribution | 报告80/90/95% coverage；不保证沉默观看者或总体人口潜在情绪；集合大小不直接等同群体分歧 |
| 路由动作 | 使用历史/纯内容回退/拒答 | — | use memory / fall back to content / abstain | 阈值仅在dev预注册规则下选择，formal test不可用于选择 |
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
