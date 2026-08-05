# CARM可信净收益路由：系统化范围查新与closest-prior矩阵

> 版本：v1.0  
> 查询冻结：2026-08-05（Asia/Shanghai）  
> 状态：`SYSTEMATIC_SCOPING_PASS_WITH_LIMITATIONS`  
> 用途：Task40开发创建门；不支持“世界首创”或穷尽性声明

## 1. 冻结问题

查新问题不是“是否有人预测观众反应分布”，而是：是否已有工作把以下链条用于目标响应不可见的内容到群体反应分布预测：

1. train-only历史反应记忆；
2. cross-fitted/out-of-fold专家净收益标签；
3. 对有限响应计数的后验收益概率或可信下界；
4. `USE_MEMORY/FALLBACK_CONTENT/ABSTAIN`三动作；
5. 内容—反应自然错位、Oracle headroom、负迁移与matched-coverage强门控对照；
6. 群体分歧、有限响应抽样、模型/OOD三源分别验证；
7. 对经验反应分布的校准预测区域。

## 2. 来源与查询族

本轮覆盖arXiv、ACL Anthology、CVF Open Access、PMLR、IEEE/DOI出版社页面、Hugging Face官方数据卡、作者官方GitHub/项目页和项目既有冻结文献台账。核心查询族包括：

- `video audience reaction distribution comments induced emotion`；
- `historical audience reaction retrieval routing negative transfer`；
- `out-of-fold benefit prediction router retrieval utility`；
- `Dirichlet finite annotator emotion uncertainty distribution`；
- `selective prediction conformal risk control distribution prediction`；
- `content similarity reaction similarity audience affect`。

已知文献召回检查包含Video2Reaction、MVIndEmo、CSMV/VC-CSA、训练期评论知识、RAMER/RAER、SelectiveNet、负迁移、LEEP/LogME、Dirichlet情绪标签不确定性、情绪分布估计与selective conformal risk control。查询是结构化范围查新，不是带双人筛选和数据库导出存档的正式系统综述。

## 3. closest-prior矩阵

| 前作/家族 | 已覆盖部分 | 未覆盖或尚未定位部分 | 本项目必须做的差异证据 |
|---|---|---|---|
| Video2Reaction（arXiv:2607.06875） | 视频到21类观众反应分布、视频/音频/描述派生特征、电影视频数据、LLM标签与人工质检 | 未把train-only历史反应的逐样本净收益作为路由目标；当前公开材料未证明后验净收益三动作链 | CSMV公平适配；独立movie-disjoint银标外验；禁止任务首创 |
| MVIndEmo（10.1007/s00530-023-01221-8） | TikTok公众诱发情绪、评论模型聚合、点赞加权分布 | 获取入口/revision/许可当前未闭合；未形成当前OOF可信净收益链 | 只作条件银标压力测试；不把点赞写成曝光或因果极化 |
| CSMV/VC-CSA | 视频—单评论诱发情绪、目标评论参与推理的原生任务 | 不满足本项目严格T0群体分布推理 | 仅冻结I3D内容接口；原生NON_T0结果不进入正式证据 |
| Discovering Attractive Segments等训练期评论知识 | 训练评论向视频模型迁移，部署期可只见视频 | 目标常混合热度/片段吸引力；不是有限响应后验净收益路由 | Task30负结果必须公开边界；不恢复teacher/KD |
| RAMER/RAER与检索增强情感 | 历史实例、检索、缺失信息补偿 | 普通检索不等于能识别历史是否有害 | no/random/lexical/kNN、固定融合、错配邻居、Oracle与负迁移对照 |
| SelectiveNet/一般gate/MoE | 选择性预测、拒答、门控专家 | 一般门控不是群体反应专属净收益监督 | 同输入/参数/预算、matched coverage比较；ABL-01只替换benefit target |
| Characterizing and Avoiding Negative Transfer | 定义与规避负迁移、过滤不相关源 | 非观众反应分布、非train-only历史案例路由 | 把负迁移率和被避免有害检索设为必要机制证据 |
| LEEP/LogME/Example Transfer | 任务或样本可迁移性估计 | 不直接形成当前样本的历史反应专家净收益后验 | 作为transferability信号基线，不宣称迁移性估计首创 |
| Wu et al., T-AFFC 2023 Dirichlet标签不确定性 | 用Dirichlet建模有限情绪标注的不确定性 | 不决定历史反应证据是否比内容模型更有益 | Dirichlet只是计数后验工具；必须用点收益路由和固定先验敏感性对照 |
| Wu et al., ACL 2024 / DEER | 情绪分布估计、模糊/OOD、aleatoric/epistemic不确定性 | 不等于群体响应抽样、历史迁移和模型错误三源都可识别 | 三源分别绑定held-out/split-half、thinning与ensemble/OOD外部判据 |
| SCRC/SCoRE等选择性conformal | 一般选择性风险与有限样本控制 | 尚未定位观众反应分布上的同构后验历史收益路由 | 预测区域/拒答作为可靠性工具，不宣称conformal首创；严格说明交换性边界 |

## 4. 新颖性裁定

本轮没有定位到完全同构的“有限响应后验OOF历史净收益 + 三动作路由 + 群体反应专属三源验证”公开方案，但这只能支持：

> 在本次冻结的系统化范围查新覆盖内，尚未定位完全同构方法；候选差异必须由预注册实验而不是模块清单证明。

禁止使用：`first`、`novel task`、`no prior work`、`world-first`，以及“Dirichlet/gate/retrieval/conformal本身是创新”。

## 5. 创新是否足以支撑T-AFFC

裁定：`PROMISING_CONDITIONAL`。

只有同时满足以下证据链，完整方法贡献才可能成立：

1. 自然内容—反应错位在控制支持量/source/noise后仍存在；
2. Oracle在内容专家与历史专家之间有稳定headroom；
3. 后验OOF收益路由优于点收益路由和最强generic/selective gate；
4. 负迁移率或选择性风险在自然group/source-family OOD下降；
5. 三源分别预测自己的外部判据；
6. 经验分布区域达到预注册coverage并报告效率；
7. Video2Reaction得到公平对比或详细不可执行审计。

若第1—3项任一失败，论文应降级为content-only可靠性测量、数据/协议贡献或负结果，不继续叠加模块。

## 6. 查新限制与滚动更新

- 本轮没有执行双人独立筛选、正式PRISMA流程或所有付费数据库全文检索；
- 2026年新预印本变化快，Task50结果冻结前和投稿前必须各滚动更新一次；
- Video2Reaction的正式venue/proceedings状态、公开revision与许可层须分别核验；
- 任一新完全同构前作出现时，先收缩claim与基线义务，不因已投入实验而忽略。

## 7. 主要公开定位

- Video2Reaction：<https://arxiv.org/abs/2607.06875>
- Video2Reaction数据卡：<https://huggingface.co/datasets/infofusionlab/Video2Reaction>
- Dirichlet情绪标签不确定性：<https://arxiv.org/abs/2203.04443>
- 情绪分布与模糊性：<https://aclanthology.org/2024.acl-long.114/>
- Deep evidential emotion regression：<https://aclanthology.org/2023.acl-long.873/>
- Negative transfer：<https://arxiv.org/abs/1811.09751>
- Selective conformal risk control：<https://arxiv.org/abs/2512.12844>
- SCoRE：<https://arxiv.org/abs/2603.24704>
