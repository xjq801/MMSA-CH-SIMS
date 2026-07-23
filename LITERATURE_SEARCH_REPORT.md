# M1 步骤19：四路贡献级查新报告

> 状态：SCOPING_COMPLETE_v3
> 截止日期：2026-07-24
> 范围事实源：`references/search/step19-23/scope-decision.txt`
> 诚实边界：本报告是中等范围 scoping 查新，不是系统综述，不声称穷尽召回，不据“未检出”判定首创。

## 1. 检索与核验方法

四条检索分别运行，不合并成单一宽查询。每条均执行近期前沿、经典奠基和跨领域方法三层召回；自动召回使用 OpenAlex、Crossref 与 DOAJ，原始结果保存在 `references/search/step19-23/raw/`。核心条目随后回到论文页、会议/出版方页面、预印本或作者官方仓库核验。

自动召回共形成四个行内去重候选池：124、138、124、114 条；合计500条，跨行按 DOI、否则按规范化标题+年份去重后为488条。该数字只表示候选召回，不表示488条均为相关研究。宽查询存在明显噪声，因此自动相似度与被引排序不进入贡献判断。

## 2. 检索线A：评论特权监督

### 核心前作

| 层级 | 前作 | 经核验的相关点 | 对本项目的约束 |
|---|---|---|---|
| 经典 | Vapnik & Vashist, *A New Learning Paradigm: Learning Using Privileged Information* (Neural Networks, 2009), DOI `10.1016/j.neunet.2009.06.042` | 训练期使用额外信息、测试期不需要该信息的LUPI范式 | 不得把“训练期额外信息、测试期缺席”写成首创 |
| 经典/跨域 | Lopez-Paz et al., *Unifying Distillation and Privileged Information* (ICLR 2016), [arXiv](https://arxiv.org/abs/1511.03643) | 将蒸馏与特权信息统一为generalized distillation | teacher/student与软目标本身不是贡献 |
| 前沿直接邻近 | Aslam et al., *Privileged Knowledge Distillation for Dimensional Emotion Recognition in the Wild* (CVPR Workshops 2023), [CVF](https://openaccess.thecvf.com/content/CVPR2023W/FGAHI/html/Aslam_Privileged_Knowledge_Distillation_for_Dimensional_Emotion_Recognition_in_the_Wild_CVPRW_2023_paper.html) | 以训练期音频为特权模态，将多模态教师蒸馏到视觉学生 | H1必须与标准content-only、硬标签、软分布和privileged distillation适配版比较 |

### 边界结论

- 当前核验未发现“目标视频受众评论作为训练期特权信息、推理期严格content-only、预测群体反应分布”的完全同构前作；这只是当前scoping范围内的未检出信号，不是新颖性判决。
- 可检验的差异仅限：特权信息是受众响应评论；目标是视频/帖子级经验分布；test评论不可达；按视频/帖子group split。
- 若评论teacher的提升只在旧随机split成立，或测试期直接/间接读取目标评论，则H1失败。

## 3. 检索线B：公众诱发情绪分布

### 核心前作

| 前作 | 经核验的任务位置 | 与本项目的关键差别 |
|---|---|---|
| Guo et al., *MVIndEmo: a dataset for micro video public-induced emotion prediction on social media* (Multimedia Systems, 2024), DOI `10.1007/s00530-023-01221-8` | 微视频公众诱发情绪预测；标签由多个评论情感模型和点赞加权聚合生成 | 属银标数据源，不是人工金标；不能承担主测试真值 |
| Jia et al., *Infer Induced Sentiment of Comment Response to Video: A New Task, Dataset and Baseline* (NeurIPS D&B 2024), [OpenReview](https://openreview.net/forum?id=EEwb201bnO) | CSMV含人工标注评论，VC-CSA将视频与目标评论共同输入以预测评论意见/情绪 | 本项目聚合为视频级经验分布，T0推理不得读取目标评论，且必须video-group split |
| Gao et al., *Prediction of People’s Emotional Response towards Multi-modal News* (AACL-IJCNLP 2022), [ACL Anthology](https://aclanthology.org/2022.aacl-main.29/) | NEmo+直接预测多模态新闻诱发的人类情绪分布 | 构念高度相近，是最直接的分布预测前作；当前本地审计因许可文件和媒体可复现性未过主集门 |
| Zhang et al., *iNews: A Multimodal Dataset for Modeling Personalized Affective Responses to News* (ACL 2025), [ACL Anthology](https://aclanthology.org/2025.acl-long.1217/) | 多人、个性化的新闻情感响应，含VAD与离散情绪 | 当前公开包无可复现媒体，且截图保留互动量，不满足本项目T0主输入门 |

### 边界结论

- “公众诱发情绪”与“诱发情绪分布预测”已有直接前作，C1不得写成首次提出任务。
- 本项目可成立的贡献上限是：严格T0输入边界、视频/帖子级无泄漏划分、评论只作标签/训练期特权监督，以及跨话题/缺失条件下的可靠性证据。
- NEmo+与iNews当前均未过第二人工多模态主集可复现门，因此检索结论不能替代G1数据门。

## 4. 检索线C：检索增强情绪预测

### 核心前作

| 前作 | 经核验的相关点 | 必须处理的差异 |
|---|---|---|
| Fan et al., *Leveraging Retrieval Augment Approach for Multimodal Emotion Recognition Under Missing Modalities* (arXiv:2410.02804), [论文](https://arxiv.org/abs/2410.02804)、[官方代码](https://github.com/WooyoohL/Retrieval_Augment_MER) | RAMER以FAISS检索相似多模态情绪样本补充缺失模态；官方代码Apache-2.0 | 本项目检索的是train-only历史受众反应案例，不把邻居当目标媒体重建；必须审计index时间和split边界 |
| Zhu et al., *Fast Retrieval and Slow Reasoning for Explainable Multimodal Sentiment Analysis* (Findings of ACL 2026), [ACL Anthology](https://aclanthology.org/2026.findings-acl.1519/) | 从当前样本内部检索Top-K情感相关线索再推理 | 不是外部历史反应记忆，但说明“检索+情感预测”表述已过宽，不可作为名称创新 |

### 边界结论

- 检索增强缺失模态情绪识别已有直接方法，后续必须比较RAMER式检索思想。
- H2的最小公平对照固定为：no retrieval、random retrieval、BM25、CLIP-kNN、learned retrieval；所有索引只含train，若有可靠时间还须满足`candidate_time < query_time`。
- 随机检索同样好，或OOD上分布误差/校准持续恶化且可靠性路由不能识别时，撤销检索创新。

## 5. 检索线D：可靠性拒绝与缺失模态

### 核心前作

| 子方向 | 前作 | 经核验的相关点 |
|---|---|---|
| 后验拒绝 | Geifman & El-Yaniv, *Selective Classification for Deep Neural Networks* (NeurIPS 2017), [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html) | 以风险—覆盖权衡构造拒绝机制 |
| 端到端拒绝 | Geifman & El-Yaniv, *SelectiveNet* (ICML 2019), [PMLR](https://proceedings.mlr.press/v97/geifman19a) | 联合优化预测和拒绝，直接比较risk-coverage |
| 选择性评估 | Traub et al., *Overcoming Common Flaws in the Evaluation of Selective Classification Systems* (NeurIPS 2024), [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2024/hash/047c84ec50bd8ea29349b996fc64af4b-Abstract-Conference.html) | 指出常见选择性评估缺陷并提出AUGRC；AURC结果应辅以定义和敏感性检查 |
| 缺失模态表征 | Lin & Hu, *MissModal* (TACL 2023), [ACL Anthology](https://aclanthology.org/2023.tacl-1.94/) | 用表示学习提高多模态情感分析的缺失模态鲁棒性 |
| 缺失模态重建 | Wang et al., *IMDer* (NeurIPS 2023), [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2023/hash/372cb7805eaccb2b7eed641271a30eec-Abstract-Conference.html)、[官方代码](https://github.com/mdswyz/IMDer) | 条件扩散恢复缺失模态；官方代码MIT，依赖较旧PyTorch/CUDA和预训练权重 |
| 不确定缺失 | Li et al., *HRLF* (NeurIPS 2024), [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2024/hash/3209cf3312b2cbb68e33644362ddc2bd-Abstract-Conference.html) | 分层表示、互信息和对抗学习处理不确定模态缺失 |

### 边界结论

- 缺失模态鲁棒性和拒绝机制均已有成熟前作；本项目不得把mask、zero-fill、重建、蒸馏或selective head本身写成创新。
- H3的可检验差异是同一模型在完整、单模态、随机缺失与自然缺失下平稳退化，并在public-induced distribution目标上同时报告分布误差与校准/选择性风险。
- 可靠性评价至少保留Brier、ECE/ACE、risk-coverage与AURC；若采用AUGRC，必须作为预注册补充指标，不替换主指标JS。

## 6. 覆盖缺口与后续限制

- 当前没有做付费数据库或付费全文检索，也没有调用付费LLM。
- 中国知网等受限来源未纳入，因此中文覆盖不完整；不得据此作中文首创判断。
- 自动召回对精确术语和缩写敏感，且四条宽查询噪声高；核心矩阵只使用人工回到主要来源核验的条目。
- 文献查新可冻结贡献上限，但不能解除第二人工多模态主集缺失、媒体许可、标签映射或物理泄漏隔离等G1/G2阻塞。

## 7. 2026-07-24前沿增量核验：Video2Reaction

### 来源与状态

- Nguyen et al., *Video2Reaction: Mapping Video to Audience Reaction Distribution in the Wild*, arXiv:2607.06875 v1，2026-07-08提交：[arXiv](https://arxiv.org/abs/2607.06875)。
- [CVPR 2026 DataMFM官方页面](https://datamfm.github.io/)确认同题工作进入accepted papers；该页面把条目置于`Proceedings Track`标题下，但[CVF公开workshop论文集](https://openaccess.thecvf.com/CVPR2026_workshops)尚未检出对应条目，故记`WORKSHOP_APPEARANCE_CONFIRMED_ARCHIVAL_STATUS_UNRESOLVED`。
- [合作者出版页](https://gaurijagatap.github.io/publications/)与团队公开帖将Video2Reaction列为ECCV 2026录用；截至2026-07-24未检出ECCV/ECVA正式论文集条目，故记`AUTHOR_REPORTED_ECCV_2026_ACCEPTANCE_PENDING_OFFICIAL_PROCEEDINGS`。这比“仅孤立预印本”更强，但仍不等于正式论文集闭合。
- 论文公开表述为从多模态视频内容直接预测受众诱发情绪分布；数据规模为10,348段电影视频，反应标签由社交媒体评论经开源LLM多代理流水线构造，并报告盲测人工核验。

### 对本项目的碰撞判定

| 层级 | 判定 | 说明 |
|---|---|---|
| C1任务目标 | `DIRECT_NEAR_COLLISION` | “视频内容→完整受众反应分布”与本项目T0核心目标在target层高度等价，不能再声称任务首创 |
| 数据/协议 | `RELATED_NOT_IDENTICAL` | Video2Reaction是电影视频与LLM评论标签；本项目以CSMV人工标注评论聚合HUMAN_GOLD，并要求video-group、future-comment isolation和审计链 |
| H1评论特权教师 | `NOT_COVERED_BY_LOCATED_METHOD` | 已核论文方法主要是LDL/VLM benchmark，未定位到“评论只在训练期作为特权teacher”的同构实现；仍受LUPI/M2PKD/评论增强前作约束 |
| H2历史反应记忆与拒绝 | `NOT_COVERED_BY_LOCATED_METHOD` | 未定位到train-only历史反应分布记忆、错误邻居负对照和负迁移拒绝链；仍受RAMER与SelectiveNet等组件前作约束 |

### 强制影响

- C1固定降为协议/证据贡献，禁止“首次从视频预测受众反应分布”“首次video-to-reaction-distribution”。
- Video2Reaction进入相关工作和最相近前作矩阵；任务50须执行其可比适配基线，或形成输入、标签、许可、资源不匹配的书面不可执行审计。
- 完整方法的新颖性不能来自模块数量，只能来自可证伪差异：严格train-only历史反应案例是否提供随机/普通近邻没有的有效信息，以及可靠性机制是否能识别并减少检索负迁移。
- “尚未定位到完全同构前作”只表示当前scoping范围内未检出，不是穷尽检索或世界首创证明；投稿前须再次做滚动查新。

### 论文重定位

Video2Reaction是`closest/direct prior`，双方共享内容到受众诱发反应分布任务。本项目不能通过强调数据来源差异来淡化碰撞，必须把问题收紧为：目标响应不可用且测试分布偏移时，评论特权监督、train-only历史反应记忆、可靠性路由与选择性拒绝能否维持可信预测。

正式论文须删除“任务首创”“此前只研究内容表达情感”“分布输出本身创新”等叙事；社媒评论标签只能解释为公开表达的诱发反应，不能代表所有观众的内在心理状态。
