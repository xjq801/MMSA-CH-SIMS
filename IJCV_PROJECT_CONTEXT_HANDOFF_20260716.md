# IJCV方向新项目上下文交接

> 生成日期：2026-07-16  
> 来源项目：`D:\MMSA-CH-SIMS`，Codex任务“总纲”与“10-M1–M2 数据与协议”  
> 新项目：`D:\MMSA-CH-SIMS - IJCV方向`  
> 基线提交：`0d779d6`（`origin/main`）  
> 当前分支：`codex/ijcv-j0`  
> 交接方法：锚定式结构化摘要；数字、状态、文件名和门结论均以本地SSOT复核，不代替原始聊天与台账。

## 1. 新项目的身份与当前任务

你是 **00-IJCV总控与J0启动任务**，不是T-AFFC任务20，也不是尚未获准创建的IJCV任务25。

当前唯一主目标：在 **2026-08-12** 前完成IJCV专线的 **J0数据/新颖性/预注册门**，为是否创建`25-IJCV视觉表征与实验`提供书面Go/No-Go证据。

J0必须同时闭合：

1. 在已冻结LAI-GAI之外，再冻结至少一个“像素可得、人工主观情绪分布、许可明确、版本/hash固定、group-safe split”的图像数据集；
2. 完成PC Loss、SAMNet、MFRN及2024—2026近邻的贡献/代码/数据可复现矩阵；
3. 冻结JH1—JH3、estimand、主/次指标、SESOI、非劣界、种子、调参预算、多重比较族和失败门；
4. 明确两稿的不可共享边界，并证明IJCV视觉方法不是CARM换名。

J0未通过：输出`NO_GO_IJCV_SPECIAL_ISSUE_DATA_OR_NOVELTY`，停止专刊冲刺；不得用银标、生成标签、小样本偶然高分或削弱公平基线挽救。

**硬边界：J0未通过不得创建任务25。**

## 2. 用户真实目标与关键纠错

- 项目业务始终是 **群体情绪预测/公众诱发情绪分布预测**。早期聊天中曾把“圣遗物的重塑”误解为《原神》系统，用户已明确纠正，该游戏业务必须永久忽略。
- 用户起初只瞄准IEEE T-AFFC，后根据IJCV专刊征稿，要求同时考虑IJCV。已裁定不是同稿双投，而是一个共享科学基础上的两篇实质独立论文。
- 用户要求只做可能影响论文发表的任务；维护者尚未回复的事项可暂时跳过。IJCV路线因此不等待CSMV资产维护者。
- 用户允许为效率使用本机代理、官方直连、可信第三方镜像和公开API下载公开资产到Git忽略隔离区；法律许可不能由项目自行扩大，未知许可不得用于正式训练/发布。

## 3. 对话与项目演进摘要

### 3.1 从原论文复现到新研究问题

原仓库来自毕业论文第四章“基于多模态感知与检索的群体情绪预测”。早期已完成CatBoost/HGB、CH-SIMS/Self-MM、BERT融合、LLM/Temporal/GNN等多轮探索，但旧证据存在随机划分、标签依赖、未来评论风险和构念错位，均不得直接作为新论文核心证据。

最终冻结的科学对象是：

> 对尚未获得未来评论的新内容，在T0只使用合法、实际可得的内容证据，预测随后公众评论所体现的诱发情绪分布、分歧和不确定性。

评论只可作为标签来源、训练期特权监督或train-only历史反应记忆，不得进入T0学生推理输入。统计/split/bootstrap单位是独立内容项，不是评论、fold或种子。

### 3.2 总纲与任务树

- 总纲从v1.4逐步升级到v1.14，当前唯一SSOT为`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md`。
- 原任务树：00总控 → 10数据/协议 → 20基线 → 30评论teacher → 40反应memory → 50正式实验 → 60 T-AFFC写作。
- v1.14新增IJCV条件链：J0通过 → 25视觉表征/实验；J2通过 → 65 IJCV写作/投稿。
- 任务25/65尚未创建。当前新项目只做J0，不能提前训练或把任务25写成已启动。

### 3.3 数据与协议已完成进展

**LAI-GAI（IJCV可直接继承的主资产）**

- 已冻结`LAI-GAI@v05-2026-03-11`；847张AI生成图像、63,682条合规HUMAN_GOLD响应、12维分布；
- 379个严格source/prompt/exact/dHash组，split=`594/127/126`，组/精确/近重复跨split均0；
- canonical SHA-256=`ad58c268e34adf02bd8e639338069d34576e1d9602f819a2cc6fa89be6836818`；
- prompt、目标生成情绪和模型标签只作provenance，不是真值，也不进入主输入；
- 适合IJCV的像素级人工主观分布学习，但样本仅847且为AI生成图像，不能单独支撑广泛视觉方法主张。

**CSMV（主要属于T-AFFC；IJCV仅可选外验）**

- 8,210个微视频、107,267条人工评论，修复后8,008个平台源视频族；202个重复族/404条记录；
- 正式source-family split：video=`5698/837/1675`，hashtag=`7211/327/672`，同源族跨split为0；
- 本地隔离I3D包命中8,210/8,210，另有1,732个非当前标签集文件；全部`float32[T,1024]`，`T=6—1719`；
- 主序列协议=`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`；主敏感性=`UNIFORM_180_ENDPOINT_INCLUSIVE`；531个`T>180`；不得test自适应；
- G1=`PASS`；G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；全局`formal_split=false`；
- GitHub官方Issue #5仍在等待资产级许可/revision/manifest/覆盖证明。按用户要求不等待、不催促；IJCV J0不依赖它。

**其他资产**

- CUC canonical为2,787条，存在221条标签冲突；只作T-AFFC中文无标签/银标压力测试，不是IJCV主集。
- MVIndEmo为模型聚合银标，不得替代人工金标。
- NEmo+有1,297个新闻图文对和38,910条众包反应，是IJCV第二主集候选之一，但许可、像素、固定版本和配对条件必须重新准入。
- Emotion6、OASIS、Flickr_LDL、Twitter_LDL均只是J0候选；历史聊天中的论文描述不等于资产许可或可复现准入。

### 3.4 音频和缺失模态边界

- CSMV音频=`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`，不是IJCV或T-AFFC的独立硬门。
- 不得声称音视频融合、音频增益、随机音频缺失鲁棒性或用LLM伪造音频。
- 图像/视频跨数据差异不是同一样本缺失模态实验。

## 4. IJCV专刊官方事实与适配判断

- 官方专刊：[Social, Emotional, and Cognitive Visual Intelligence](https://link.springer.com/collections/fdhgfjgaae)；状态为Open，截稿 **2026-12-15**。
- 范围直接包含主观视觉理解、情感、概率/不确定性、观察者差异、多模态/跨模态、迁移/泛化、benchmark与负责任视觉。
- 专刊特别鼓励新的计算机视觉方法或显著技术洞见。冻结I3D后接普通分布头，即使scope匹配，也不足以达到方法门。
- [IJCV投稿指南](https://link.springer.com/journal/11263/submission-guidelines)禁止稿件同时在其他地方审议。截图中的2027年通知/修回/出版日期未由本轮官方正文核实，不得当硬门。

适配裁定：`CONDITIONAL_GO_TWO_DISTINCT_PAPERS`。方向有真实希望，但当前尚不具备提交资格，不提供虚假录用概率。

## 5. 两篇论文的冻结分界

| 维度 | IJCV候选论文 | T-AFFC候选论文 |
|---|---|---|
| 问题 | 视觉表征如何保持人工响应分布的几何与分歧结构 | 评论特权监督/历史反应能否改善T0公众诱发情绪预测与可靠拒绝 |
| 方法 | 响应几何对齐、分歧/不确定性建模、跨域几何保持 | teacher—student、train-only受众记忆、可靠性路由 |
| 核心数据 | LAI-GAI + 至少一个新冻结的像素人工分布集 | CSMV + LAI-GAI + CUC压力测试 |
| 禁止混入 | 评论teacher、CARM memory/router、舆情应用 | 将IJCV几何模块及其主结果改名复用 |

通用数据读取、泄漏测试和基础指标可共享；主问题、主方法、主表、关键消融、claim-evidence和正文必须物理隔离。不得切香肠式重复发表。

## 6. IJCV候选方法与可证伪假设

工作问题：

> How can visual representations preserve the geometry and disagreement structure of human affective response distributions across images and domains?

内部工作名`Response-Geometry-Aware Visual Representation Learning`尚未查重，不得作为正式名称。

最小方法核：

1. 用人工分布间JS/Wasserstein距离定义域内目标几何，使视觉嵌入保持成对距离或局部排序，同时保留proper distribution loss；
2. 基于逐人响应/计数拟合分布均值与浓度/区间，区分观察者分歧与模型/域外不确定性；
3. 标签空间不一致时使用共享视觉编码器 + 数据集特定head，只检验预注册的几何保持/迁移estimand，不事后强行合并类别。

JH1：响应几何改善至少两个主集的JSD/EMD/NLL；两集均无达到SESOI的稳定改善则失败。  
JH2：分歧建模改善coverage/NLL/Brier/AURC且分布精度非劣；无改善或JSD超非劣界则失败。  
JH3：几何保持改善跨域迁移且不依赖事后标签映射；不优于普通fine-tune/强foundation baseline则失败。

## 7. J0必须核验的近邻与公平基线

- PC Loss / A Circular-Structured Representation for VEDL（CVPR 2021）；
- SAMNet / Seeking Subjectivity in VEDL（TIP 2022）；
- MFRN / Multiple Feature Refining Network（AAAI 2025）；
- MART等情感视觉表征、2024—2026 VEDL/主观视觉学习、跨域视觉情感与不确定性近邻；
- 强foundation基线：ViT/CLIP/SigLIP + KL/JSD/softmax/Dirichlet；
- 不确定性：temperature scaling、deep ensemble和一个预注册的Dirichlet/evidential实现；
- 跨域：source-only、普通fine-tune、线性探测及一个公平域适配基线。

“分布预测”“主观性”“affective memory”“特征精炼”均已有前作，不能单独声称首创。

## 8. IJCV阶段门与日历

| 门 | 最迟日期 | 核心条件 |
|---|---|---|
| J0 | 2026-08-12 | 两个像素人工集；近邻差异矩阵；JH/指标/SESOI预注册 |
| J1 | 2026-09-12 | 两集强基线可信复现；评测/预算冻结 |
| J2 | 2026-11-15 | JH1成立，JH2/JH3至少一条独立成立；完整统计与单变量消融 |
| IJCV投稿Go | 2026-12-11—12-15 | 十项Go标准全部满足、模拟审稿无Critical、与T-AFFC重叠审计通过 |

J0通过才创建任务25；J2通过才创建任务65。若未通过，不赶稿。

## 9. 当前机器与证据状态

- 源项目最终基线commit=`0d779d6`，已与`origin/main`同步；新项目从该状态创建分支`codex/ijcv-j0`。
- 源项目最近综合准备为`blocking_checks=[]`、`m1_read_only_work_ready=true`、`formal_model_work_ready=false`。
- 新项目是独立克隆，未复制源项目Git忽略区的9,942个I3D `.npy`。因此本地默认`run_preparation_checks.py`会诚实报告`csmv_feature_preflight/m2_release`失败；这表示“本克隆不能复现CSMV全量资产门”，不推翻源项目已审核的G1，也不阻塞不使用CSMV的只读IJCV J0。不得把该失败改写成PASS或复制大包来美化检查。
- 新项目的交接/J0专用门为`scripts/validate_ijcv_project_handoff.py`；它只验证SSOT、关键数字、任务边界、敏感片段和科学状态，不声称验证CSMV本地资产。
- 19项公共核心隔离重放零漂移；泄漏live门Critical=0，负面夹具正确输出`LEAKAGE_BLOCKED`。
- 原始数据、I3D `.npy`、模型、索引、密钥、Cookie和`.env`不得入Git。

## 10. 必读文件顺序

1. `IJCV_PROJECT_CONTEXT_HANDOFF_20260716.md`（本文件）
2. `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md`第0.6与18节
3. `IJCV_TAFFC_DUAL_TRACK_FEASIBILITY_AND_PLAN_20260716.md`
4. `CLAIM_EVIDENCE_MATRIX.md`的IJCV J-C1—J-C3
5. `RISK_REGISTER.md`的`R-IJCV-001/002`、`R-INTEGRITY-001`、`R-SCHEDULE-001`
6. `DATA_SOURCE_LEDGER.md`、`DATA_CARD_DATASET_V1.md`、`DATASHEET_DATASET_V1.md`
7. `M1_M2_LAI_GAI_SECOND_PRIMARY_FREEZE_20260714.md`与LAI-GAI manifests
8. `CONTRIBUTION_PRIOR_ART_MATRIX.md`、`LITERATURE_SEARCH_REPORT.md`
9. `WORK_RECORD_POLICY.md`与`WORK_LOG.md`最后一条

## 11. 首轮执行步骤

1. 刷新Git状态，确认分支与本文件；不得修改T-AFFC实验代码。
2. 建立`IJCV_J0_DATASET_AND_NOVELTY_PLAN.md`，为Flickr_LDL、Twitter_LDL、NEmo+、Emotion6、OASIS分别列出：人工标签结构、像素入口、许可、revision、文件树/size/hash、group字段、标签空间、已知近邻使用情况和预计资源。
3. 先做只读官方元数据核验，按硬门筛到最多两个候选；不要一开始批量下载全部候选。
4. 建立`IJCV_PRIOR_ART_COLLISION_MATRIX.md`，逐项比较问题、监督、表征目标、损失、数据、基线和可证伪差异。
5. 起草`IJCV_PREREGISTRATION_DRAFT.md`，只定义JH1—JH3、estimand、指标/SESOI/非劣界、统计单位、种子、调参预算和停止条件，不写预期胜负。
6. 向用户/00提交J0候选结论；获得书面J0 PASS前不创建任务25、不正式训练。

## 12. 接手自检问题

首次回复必须准确回答：

1. 为什么IJCV不能直接复用CARM？
2. J0的两个主数据集最低要求是什么，LAI-GAI之外还缺什么？
3. 当前G1/G2/`formal_split`状态是什么，为什么不阻塞IJCV J0？
4. JH1—JH3各自怎样被证伪？
5. 什么可以在两稿之间共享，什么绝对不能共享？
6. 你准备先核验哪两个第二数据集候选，为什么？

回答后只提出第一批只读J0动作，不下载大包、不训练、不创建任务25，等待用户确认或按已有授权继续无风险只读核验。
