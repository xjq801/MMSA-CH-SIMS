# 术语表 — MMSA-CH-SIMS T-AFFC 总控

| 类别 | 标准叫法 | 缩写 | 英文 | 备注 |
|---|---|---|---|---|
| 构念 | 公众诱发受众情绪 | — | public-induced audience affect | 不是说话者情绪、画面群体情绪或传播链 |
| 方法 | 上下文感知受众反应记忆 | CARM | Context-Aware Audience Reaction Memory | 标题方法；完整方法尚未实现，当前为PLANNED/TO_VERIFY |
| 核心机制 | 收益感知可靠性路由 | — | benefit-aware reliability routing | 预测检索相对content-only的正/负收益，决定融合、降权或拒绝；须train内cross-fitting |
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
| 开发效应门 | JSD相对改善至少3% | — | development effect gate | 只允许进入下一开发阶段，不等于论文结论 |
| 论文效应门 | JSD相对改善至少5% | — | paper minimum effect gate | 还须原生单位paired bootstrap 95% CI优于0、校准不恶化 |
| 强结果门 | JSD相对改善至少8% | — | strong-result effect gate | NLL/EMD方向一致且校准改善 |
| 可靠性Pareto门 | JSD绝对非劣界+0.003、AURC改善至少10%、负迁移率下降至少20% | — | reliability Pareto gate | 作为平均误差不大幅改善时的预注册替代成功门 |
