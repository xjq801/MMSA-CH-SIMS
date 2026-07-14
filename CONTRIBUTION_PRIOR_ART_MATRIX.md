# 步骤20：最相近前作—相同点—不同点—必须对比实验矩阵

> 状态：FROZEN_v1
> 日期：2026-07-14
> 用途：限制贡献表述与后续实验矩阵；不是新颖性法律意见，也不是“没有更近前作”的保证。

| 拟检验主张 | 最相近前作 | 相同点 | 本项目允许声称的不同点 | 后续必须对比实验 | 失败/降级触发 |
|---|---|---|---|---|---|
| C1：严格T0公众诱发情绪分布预测 | NEmo+；CSMV/MSA-CRVI；MVIndEmo | 从内容预测受众诱发情绪；使用多人/评论反应 | target评论在推理时不可见；视频/帖子级经验分布；video/post-group与topic held-out；银标不作金标 | 内容先验；文本/图像/视频单模态；简单late fusion；NEmo+论文分布baseline；VC-CSA仅作“泄漏/非T0诊断上界” | 仅随机comment split有效；目标评论或未来互动进入输入；第二人工主集缺失则C1证据不完整 |
| H1/C2前半：评论特权教师改善content-only学生 | LUPI；generalized distillation；M2PKD | 训练期额外信息；teacher/student；测试期学生不依赖特权模态 | 特权信息是训练视频的受众评论；目标是视频级反应分布；test评论在隔离评测端构标签 | content-only hard label；content-only soft distribution；普通KD；M2PKD式特权蒸馏；teacher upper bound；随机/错配评论负对照 | 对两主集最强content-only均无稳定改善；校准明显恶化；提升只来自随机split |
| H2/C2后半：train-only受众反应记忆和可拒绝检索 | RAMER | 从外部相似情绪样本检索信息；处理信息不足或缺失 | 检索对象是历史受众反应案例而非伪造目标缺失媒体；index严格train-only/earlier-only；显式拒绝负迁移 | no retrieval；random；BM25；CLIP-kNN；learned retrieval；RAMER式检索适配；错邻居；top-k；index泄漏测试 | 随机检索同样好；OOD误差/校准更差；拒绝器不能识别有害邻居则撤掉检索创新 |
| H3/C3：完整/缺失/OOD下可靠性 | MissModal；IMDer；HRLF；Selective Classification；SelectiveNet | 缺失模态鲁棒；不确定性或拒绝；risk-coverage | public-induced distribution目标；随机缺失与自然缺失并报；跨话题/平台；分布误差、校准与选择性风险联合 | late fusion；zero-fill；modality dropout；MissModal式表征；IMDer/HRLF近期强基线；最大概率/熵拒绝；SelectiveNet式拒绝 | 不优于late fusion、zero-fill或近期缺失模态基线；校准恶化；只在人工随机缺失有效 |
| H4增强：配对模态对反应分布变化的贡献 | BU-NEmo/NEmo+ | 同一新闻在T、I、TI条件下采集人类反应 | 直接预测`p_TI-p_T`与`p_TI-p_I`，且仅在配对条件合法可复现时启用 | 独立预测两分布后相减；T-only；I-only；TI joint；共享/不共享参数 | 不超过“独立预测后相减”；NEmo+许可/媒体门不过则H4保持关闭 |

## 表述红线

- 禁止：首次提出公众诱发情绪、首次做情绪分布预测、首次将特权信息用于情感识别、首次做检索增强缺失模态情绪识别、首次做缺失模态拒绝。
- 允许的候选表述：在严格T0与group-held-out协议下，检验评论特权监督和train-only受众反应记忆是否能改善公众诱发情绪分布预测，并量化OOD/缺失条件下的校准与选择性风险。
- 所有“优于”表述必须等待两个人工公开主集、五种子和视频/帖子级paired bootstrap 95% CI；本文件不预判结果。
