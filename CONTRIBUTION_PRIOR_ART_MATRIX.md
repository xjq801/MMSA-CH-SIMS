# 步骤20：最相近前作—相同点—不同点—必须对比实验矩阵

> 状态：FROZEN_v5
> 日期：2026-07-28
> 用途：限制贡献表述与后续实验矩阵；不是新颖性法律意见，也不是“没有更近前作”的保证。

| 拟检验主张 | 最相近前作 | 相同点 | 本项目允许声称的不同点 | 后续必须对比实验 | 失败/降级触发 |
|---|---|---|---|---|---|
| C1：严格T0公众诱发反应分布协议与证据 | Video2Reaction（closest/direct prior）；NEmo+；CSMV/MSA-CRVI；MVIndEmo | 从内容预测完整受众诱发反应分布；使用多人/评论反应 | 只允许声称HUMAN_GOLD、target评论推理不可见、video/post-group与topic held-out、未来信息物理隔离和系统审计；不再允许任务首创或“分布输出即创新” | V2R-A：CSMV同split/T0/评测/预算的直接内容模型与LDL；V2R-B：原生公开特征复现、movie-disjoint及适用memory/router；内容先验；冻结视频特征+MLP；VC-CSA仅作NON_T0诊断 | 若主要差异只剩数据集/划分、V2R-A未处理或把V2R-B银标冒充人工金标，C1只能作为协议/证据贡献；目标评论或未来互动进入输入则C1失败 |
| H1/C2前半：评论特权教师改善content-only学生 | LUPI；generalized distillation；M2PKD | 训练期额外信息；teacher/student；测试期学生不依赖特权模态 | 特权信息是train评论；目标是视频级公开表达反应分布；test评论只在隔离评测端构标签 | content-only hard/soft；普通KD；M2PKD式特权蒸馏；teacher upper bound；随机/错配评论负对照 | CSMV最强content-only无稳定改善；校准明显恶化；提升只来自随机split或软标签/参数量 |
| H2/C2后半：train-only受众反应记忆、收益感知router与rejection | RAMER；SelectiveNet | 从外部相似情绪样本检索信息；处理信息不足并允许拒绝 | 检索对象是历史受众反应案例；index严格train-only/earlier-only；用train内部cross-fitting/OOF误差差构造检索效用，router仅凭T0查询与相似度、邻居分歧、域/时间距离和模态质量预测检索是否有益 | 去memory；no/random/BM25/CLIP-kNN/learned；RAMER式适配；固定融合、相似度阈值、预测熵、SelectiveNet式拒绝；去router/去rejection；coverage匹配；错域/低质邻居；效用与index泄漏测试 | 学习检索不优于普通近邻；效用标签in-sample/test污染；router在匹配coverage后不优于强路由对照；OOD误差/校准更差且不能减少负迁移，则撤掉收益感知/完整检索创新 |
| H3/C3：合格多输入协议的完整/缺失/OOD可靠性 | MissModal；IMDer；HRLF；Selective Classification；SelectiveNet | 缺失模态鲁棒；不确定性或拒绝；risk-coverage | public-induced distribution目标；仅在同一样本至少两个实际T0输入模态时并报随机/自然缺失；跨话题/平台；分布误差、校准与选择性风险联合 | late fusion；zero-fill；modality dropout；MissModal式表征；IMDer/HRLF近期强基线；最大概率/熵拒绝；SelectiveNet式拒绝 | 不优于late fusion、zero-fill或近期缺失模态基线；校准恶化；只在人工随机缺失有效；无合格协议则`NOT_APPLICABLE` |
| H4增强：配对模态对反应分布变化的贡献 | BU-NEmo/NEmo+ | 同一新闻在T、I、TI条件下采集人类反应 | 直接预测`p_TI-p_T`与`p_TI-p_I`，且仅在配对条件合法可复现时启用 | 独立预测两分布后相减；T-only；I-only；TI joint；共享/不共享参数 | 不超过“独立预测后相减”；NEmo+许可/媒体门不过则H4保持关闭 |

## 表述红线

- 禁止：见`TAFFC_CLAIM_BLACKLIST_20260724.md`；尤其禁止任务首创、把既有工作概括成“从未预测受众诱发反应”、以分布输出本身或模块拼接宣称创新，以及把评论者公开表达外推为所有观众内在情绪。
- 允许的候选表述：在严格T0与group-held-out协议下，检验评论特权监督和train-only受众反应记忆是否能改善公众诱发情绪分布预测，并量化OOD/缺失条件下的校准与选择性风险。
- 所有“优于”表述必须等待两个人工公开主集、五种子和视频/帖子级paired bootstrap 95% CI；本文件不预判结果。
- Video2Reaction原生标签固定为`SILVER_LLM_HUMAN_VERIFIED`；其原生结果与CSMV公平适配结果必须分表，原论文Top-3 F1不得与CSMV绝对值横比。
