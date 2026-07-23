# IEEE T-AFFC 第四章十个月总纲（唯一主路线）

> 版本：v1.17  
> 生效日期：2026-07-23  
> 最终目标：2027-05-12前形成可审计、可复现、满足Go标准的T-AFFC投稿包  
> 项目：仅执行T-AFFC的CARM公众诱发受众情绪预测路线  
> 权威关系：本文件规定研究方向、阶段门、任务依赖和成功标准；数据、实验、claim、风险与决策的细节分别以其专用台账为准。

## 0. 当前决策与状态

### 0.1 不可漂移的项目边界

- 研究对象是`public-induced audience affect`：内容发布后，多名受众形成的情绪反应经验分布；不是说话者情绪、画面中的群体情绪或传播链。
- 主任务是严格T0预测：推理时只能使用发布时可见内容、合法静态/历史信息及train-only或严格更早案例。
- 目标评论、未来互动、发布后推荐结果、test样本及其派生统计禁止进入模型输入、拟合过程或索引。
- 当前仓库只执行T-AFFC CARM路线。IJCV方向位于`D:\MMSA-CH-SIMS - IJCV方向`；不得在本项目创建或执行J0—J2、JH1—JH3、任务25或65。
- 不以LLM、GNN、RAG、蒸馏、动态权重、缺失模态mask或模块拼接本身作为创新。

### 0.2 当前门与任务状态

| 项目 | 当前权威状态 | 边界 |
|---|---|---|
| G1 | `PASS` | 两个人工主集已冻结 |
| G2协议/数据 | `PASS_WITH_LIMITATIONS` | `formal_split=true` |
| I3D资产 | `ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK` | 许可、稳定官方revision、权利方包身份/fixity仍`UNKNOWN` |
| G2总门 | `PASS_WITH_ACCEPTED_ASSET_RISK` | 只允许内部研究，不构成权利证明 |
| G3 | `PASS_WITH_LIMITATIONS` | 统一评测与强视觉重实现已交付；当前正式数值仍是单种子 |
| 任务20 | 基线/G3主体完成，VC-CSA探索未闭环 | 探索永久`NON_T0/INELIGIBLE`，不得进入论文主证据 |
| 任务30/40/50/60 | 未启动 | 按依赖逐项创建，不并发修改同一实验核心 |

若权利方否认研究使用，或固定8210项I3D的hash/覆盖漂移，立即执行
`ASSET_INVALIDATED_DO_NOT_REPORT`：停止相关正式运行并撤销其论文证据资格。

### 0.3 v1.17相对v1.16的变更

1. 把论文创新评估、方法边界和性能目标并入SSOT。
2. 将CARM核心机制收紧为“train-only受众反应记忆 + 收益感知可靠性路由”，但仍是`PLANNED/TO_VERIFY`，不是已验证成果。
3. 固定3%开发趋势、5%论文最低效应、8%强结果和可靠性Pareto门。
4. 明确当前正式协议没有合格的同一样本多T0模态，H3/E5为条件性N/A；H4继续作为NEmo+可选增强。
5. 删除月度路线与任务树之间的重复说明；已完成的任务10/20改为证据摘要，执行细节由HANDOFF和审计文件承载。
6. 不改变G1—G3、资产风险、split、T0政策、数据角色或任务依赖。

---

## 1. 研究问题、输出与贡献上限

### 1.1 冻结研究问题

- **RQ1/C1**：严格T0和video/post-group划分下，发布时内容能否预测未来受众情绪分布、分歧和不确定性？
- **RQ2/H1**：仅训练期读取评论的特权教师，能否稳定改善推理时只看T0内容的学生？
- **RQ3/H2**：train-only历史受众反应记忆能否提供真实增益，可靠性路由能否识别并减少检索负迁移？
- **RQ4/H3（条件性）**：只有同一样本至少含两个合法、冻结、实际可得T0模态时，质量/缺失感知能否使模型平稳退化？
- **RQ5/H4（可选）**：只有NEmo+等配对条件合法闭合后，能否预测增加图像带来的受众反应分布变化？

### 1.2 输出与统计单位

- 主输出：K类受众情绪概率分布。
- 辅助输出：分布熵/分歧、预测不确定性、检索可靠性和可选拒绝分数。
- 兼容输出：自然流行率下的二分类风险，仅作次任务。
- 统计、划分、bootstrap单位均为数据集原生内容单元：CSMV视频、LAI-GAI图像；评论、seed和fold不是独立样本量。

### 1.3 三项贡献及新颖性边界

#### C1：严格T0、无泄漏的受众情绪分布预测协议

贡献在于目标评论物理隔离、video/post-group split、train-only索引、经验分布与OOD/可靠性评价。公众诱发情绪和反应分布预测已有前作，不得声称首次提出任务。

#### C2：评论特权学习与收益感知受众反应记忆

评论只在训练期形成teacher和分布监督；student训练/推理均只接收T0输入。历史记忆只含train或严格更早案例。路由器预测检索相对content-only是正收益还是负收益，决定融合、降权或拒绝。

teacher/student、LUPI、generalized distillation、评论增强、kNN/RAG和选择性拒绝均不是模块级首创。方法贡献必须由H1/H2、错配评论、随机/错误邻居、固定融合和OOD判别实验共同支撑。

#### C3：跨域、污染与选择性风险证据

联合报告分布误差、校准、risk-coverage、负迁移、效率和失败案例；证明邻居质量下降时路由权重下降、拒绝上升并减少伤害，而不是只报随机split Accuracy。

### 1.4 当前论文成熟度

- 已完成：问题、数据、T0/split、统一评测器、强视觉重实现和G1—G3地基。
- 未完成：H1/H2实现、五种子、paired bootstrap、OOD、完整E0—E9和结果冻结。
- 当前裁定：路线具备T-AFFC潜力，但尚不能声称已形成或验证新方法，也不具备立即投稿条件。

---

## 2. 数据、输入与证据角色

| 数据 | 规模与角色 | 允许主张 | 禁止 |
|---|---|---|---|
| CSMV/MSA-CRVI | 8210视频、107267人工标注评论；核心机制主集 | 冻结I3D视觉表征上的受众反应分布、H1/H2、video-group与适用OOD | 目标评论T0输入、官方复现已成功、端到端视频/音视频融合 |
| LAI-GAI | 847图像、63682人工响应；split 594/127/126 | 独立人工真值上的跨域图像分布、校准和适用OOD | 冒充第二视频复现集；用prompt/生成目标类别作受众真值输入 |
| MVIndEmo | 7153微视频；自动模型聚合标签 | 银标预训练、迁移或压力测试 | 承担人工test主结论 |
| CUC-IGPE-v2 | 2787条canonical；标签冲突和时间覆盖受限 | 中文、跨平台、自然缺失的无标签/银标压力测试 | 报银标准确率为核心证据；复用旧随机高分 |
| NEmo+ | 1297图文对、T/I/TI配对条件 | 数据和许可另过门后运行H4 | 当前主线必成条件 |

### 2.1 CSMV冻结输入

- 当前唯一T0内容输入是固定8210项I3D `float32[T,1024]`视觉序列。
- 主协议：`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`。
- 主敏感性：`UNIFORM_180_ENDPOINT_INCLUSIVE`。
- `FIRST_180_ONLY_FIXED_DIAGNOSTIC`只作补充。
- 音频为`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`。
- CSMV的`ALL_AVAILABLE_INPUTS`就是I3D单输入；序列裁剪不是模态消融。

### 2.2 标签与索引

- HUMAN_GOLD、SILVER、UNLABELED物理隔离。
- train评论可用于标签与teacher；dev只用于预注册选择/校准；test评论只在盲评端构造真值。
- 必须先split后拟合、建图和建索引；主索引只含train，有可靠时间时还须`candidate_time < query_time`。
- 任一目标评论、未来信息、跨split实体、test拟合或全图穿越检查失败，运行立即标记`LEAKAGE_BLOCKED`。

---

## 3. CARM-v1计划方法

### 3.1 最小结构

```text
train评论 ──> 反应teacher ──> 个体/视频分布与置信度 ──> 特权分布蒸馏
T0内容 ─────> content student ────────────────> p_s(y|x)
                              │
                              └─> train-only反应记忆 ─> p_m(y|x)
                                   │
                                   └─> 收益感知可靠性路由 r(x)
                                           ├─ 融合：(1-r)p_s+r p_m
                                           └─ 高风险：降权或拒绝
```

### 3.2 记忆与路由的计划形式

- 记忆单元：`(内容表示z_i, 经验分布q_i, 响应数n_i, 域d_i, 时间t_i, 质量m_i)`。
- 检索分布：`p_m(y|x)=Σ_i α_i q_i`。
- train内部用cross-fitting/out-of-fold预测构造效用：
  `u(x)=JSD(p_s,y)-JSD(p_m,y)`；`u>0`表示检索有益。
- 路由器以相似度、邻居分布分歧、域/时间距离、响应置信度和输入质量预测`u`或`P(u>0)`。
- 最终融合或拒绝阈值只由train/预注册dev确定，test不得反向训练或调阈值。

该形式是任务40的优先实现方向；任务40开始前必须冻结损失、cross-fitting、阈值、对照和计算预算。若只实现固定权重最小版，论文应降低新颖性措辞。

### 3.3 实现纪律

- 编码器优先冻结或LoRA；不从头训练大型视频模型或依赖不可复现闭源API。
- 先比较softmax与简单Dirichlet头，不堆生成模块、GNN或原型库。
- 每个创新组件必须有单变量消融和负对照。
- 所有公平基线使用同数据、split、评测器和可比调参预算。

---

## 4. 假设、效应门与失败树

### 4.1 总体效应门

最终分母是任务50在同数据、同split、同预算下五种子重跑的**最强公平基线**。当前单种子temporal-attention仅作规划锚点。

| 档位 | 主指标与统计要求 | 决策 |
|---|---|---|
| 无实质收益 | JSD改善<3%、CI跨0或seed方向不稳定 | 不支持方法主张 |
| 开发趋势 | JSD改善≥3%，至少4/5 seed同方向，ECE恶化≤0.005 | 可进入下一开发阶段，不是论文结论 |
| 论文最低 | JSD改善≥5%，原生内容单元paired bootstrap 95% CI优于0，多重校正后成立 | 可支持准确性主张 |
| 强结果 | JSD改善≥8%，NLL/EMD方向一致且校准改善 | 强方法证据 |
| 可靠性Pareto | JSD绝对非劣界`+0.003`内，AURC改善≥10%，负迁移率下降≥20%，ECE不恶化 | 可支持可靠性主张 |

按当前单种子JSD 0.182668换算：5%目标约`≤0.173535`，8%目标约`≤0.168055`。这些绝对值不是冻结最终门，任务50基线变化时按相对效应重算。

### 4.2 H1—H4

| 假设 | 成功 | 失败/止损 |
|---|---|---|
| H1 评论特权teacher | CSMV相对最强content-only：开发≥3%，论文≥5%；NLL/EMD一致，ECE恶化≤0.005；错配评论无同等级收益 | CI跨0、仅随机split有效、普通KD同样好或校准明显变差：撤销或降级teacher主张 |
| H2 反应记忆与路由 | learned显著优于random；相对no retrieval JSD≥3%或Pareto门成立；路由降低负迁移≥20%或AURC≥10% | random同样好、固定融合同样好、OOD持续受害且无法识别：撤掉检索创新 |
| H3 缺失/质量感知 | 仅合格多模态协议运行；30/50%缺失时JSD优于强缺失基线≥5%或性能损失缩小≥20% | 当前无合格协议，登记`NOT_APPLICABLE_NO_ELIGIBLE_MULTIMODAL_PROTOCOL` |
| H4 配对模态变化 | NEmo+合法闭合后，直接预测分布变化相对“分别预测后相减”改善≥5%且CI优于0 | 数据门失败或不超过简单差分：取消 |

### 4.3 G4失败树

- H1/H2至少一条达到论文最低门：保留相应方法主张。
- 只有3%开发趋势：继续开发但不得写入摘要结论。
- H1成立、H2失败：降级为严格T0评论特权分布学习。
- H1失败、H2成立：降级为train-only历史反应记忆与可靠性路由。
- H1/H2均失败：转为协议、benchmark纠错和负结果边界；重新执行T-AFFC Go/No-Go，不堆新模块补分。

---

## 5. 基线、实验与预期结果

### 5.1 必跑基线

1. 总体均值、经验分布、多数类及适用的主题均值。
2. 旧48维+CatBoost/HGB/LightGBM，仅作legacy兼容。
3. CSMV官方材料与作者实现，严格区分官方复现、重实现和NON_T0诊断。
4. 冻结I3D pooled MLP、temporal attention及适用的CLIP/SigLIP/VideoMAE参考。
5. content-only、teacher-only上界、普通KD和comment-privileged KD。
6. no/random/BM25/TF-IDF/CLIP/SBERT/learned retrieval及RAMER式适配。
7. 固定融合、相似度阈值、熵/最大概率拒绝与收益感知路由。
8. 小型开源MLLM只作参考，不替代公平训练基线。

### 5.2 E0—E9

| 实验 | 唯一变化 | 预期/最低验收 |
|---|---|---|
| E0 数据与split | 数据、索引和拟合边界 | 所有强制泄漏检查0失败；失败即`LEAKAGE_BLOCKED` |
| E1 实际输入 | 单输入与`ALL_AVAILABLE_INPUTS` | CSMV主协议相对简单pooled基线JSD改善目标≥5%；单模态时不冒充模态增量 |
| E2 检索方式 | no/random/稀疏/稠密/learned | learned相对no retrieval开发≥3%、论文≥5%；相对random目标≥5%；random不得同样好 |
| E3 teacher/KD | hard、soft、普通KD、privileged、错配评论 | privileged相对content-only开发≥3%、论文≥5%；相对普通KD目标≥2%；错配评论无同等级收益 |
| E4 路由 | 无路由、固定权重、简单拒绝、收益感知 | 负迁移下降≥20%或AURC改善≥10%；JSD劣化≤0.003、ECE劣化≤0.005 |
| E5 缺失模态 | 10/30/50/70%及自然缺失 | 当前N/A；仅新合格多模态协议升版后运行 |
| E6 OOD | topic/hashtag、source、time、platform及跨场景 | 每个适用维度单报；聚合JSD目标≥3%，或JSD非劣+AURC≥10%；最差域不得被平均隐藏 |
| E7 检索污染 | 错邻居、低相似、库缩小、top-k | 路由减少污染新增损失≥30%；严重污染时退回content-only附近，额外JSD≤0.003或相对2% |
| E8 旧任务兼容 | 自然流行率二分类 | 不劣于最强合法二分类基线超过1个百分点；若声称提升，Macro-F1/AUPRC至少+2个百分点且有CI |
| E9 效率 | 参数、显存、时间、索引、延迟 | 单A30 24GB可运行；目标峰值≤20GB、单run≤2 GPU小时、推理≤1.5×、索引≤5GB |

### 5.3 指标与统计

- 主指标：Jensen–Shannon divergence。
- 辅助分布指标：NLL、Wasserstein/EMD。
- 分类兼容：Macro-F1、Balanced Accuracy；旧二分类另报AUPRC、Recall。
- 可靠性：Brier、ECE/ACE、risk-coverage、AURC。
- 检索：Recall@K/nDCG@K、邻居反应一致性、负迁移率及检索效用相关。
- 正式结果：至少5个seed；按原生内容单元paired bootstrap 95% CI；配对检验和多重比较校正；全部seed和失败运行保留。

---

## 6. 十个月路线与阶段门

> 日期是资源计划；实际推进只认G门和证据，不因日历越门。

| 月份 | 日期 | 目标 | 退出门 |
|---|---|---|---|
| M1 | 2026-07-13—08-12 | 构念、数据、许可、查新 | G1 |
| M2 | 2026-08-13—09-12 | canonical、group split、标签隔离、泄漏测试 | G2 |
| M3 | 2026-09-13—10-12 | 统一环境、评测器、强基线 | G3 |
| M4 | 2026-10-13—11-12 | teacher/student与E3 | H1开发门 |
| M5 | 2026-11-13—12-12 | memory、检索、路由与E2/E4/E7 | H2开发门 |
| M6 | 2026-12-13—2027-01-12 | 两主集第一轮五种子 | G4 |
| M7 | 2027-01-13—02-12 | OOD、跨平台、中文压力测试 | G5 |
| M8 | 2027-02-13—03-12 | E0—E9、统计与结果冻结 | G6 |
| M9 | 2027-03-13—04-12 | 论文、图表、匿名复现包 | submission-ready draft |
| M10 | 2027-04-13—05-12 | 模拟审稿、修订、Go/No-Go与投稿 | T-AFFC Go |

### 6.1 G1—G6定义

- **G1**：两个公开人工主集角色、来源和可用性闭合。
- **G2**：样本lineage、split、标签隔离、T0和泄漏门闭合；资产风险单独披露。
- **G3**：统一评测器、强公平基线、配置/预测/run manifest和重放证据闭合。
- **G4**：H1/H2至少一条在CSMV达到论文最低门；第二集提供独立跨域/校准/OOD证据。
- **G5**：OOD失败可量化、解释或被拒绝机制识别。
- **G6**：两集适用实验、五种子、E0—E9、统计、效率、失败案例、中文压力测试和claim-evidence全部冻结。

### 6.2 算力与预算

- 正式主线规划：470—755 A30 GPU小时；按¥2.20/GPU·小时约¥1034—1661，正式建议上限约¥1700。
- VC-CSA NON_T0探索是额外90—180 GPU小时，不计入G6必需证据。
- 先1卡开发，再3卡跑冻结五种子，6卡只用于短时独立矩阵；首批3—5个真实smoke后重估。
- 单卡运行、日志同步和关机优先，避免空闲计费；存储、流量、快照和税费另留10%—15%。

---

## 7. 任务树与依赖

### 7.1 统一规则

1. 顺序：`00 → 10 → 20 → 30 → 40 → 50 → 60 → 00最终Go`。
2. 上游门未书面通过，不创建下游任务；两个任务不得并发修改同一实验代码、评测器或结果文件。
3. 每个任务开工先读`AGENTS.md`、本总纲、上游HANDOFF、权威协议和`WORK_LOG.md`末条，并运行`git status --short --branch`。
4. 每个实验绑定Git提交、环境、数据、split、seed、配置、索引、预测、指标和停止条件。
5. 每个实质进展同批追加`WORK_LOG.md`；失败记录不得删除。
6. 大数据、评论、特征、权重、预测、密钥和本机路径不进入Git。
7. 完成定义：产物齐、测试过、Git可追溯、交接完整、00书面验收、无未处理Critical。

### 7.2 任务00：总控

职责：维护SSOT、任务登记、G1—G6、风险/决策/claim边界、范围控制、结果冻结和最终Go/No-Go；不直接承担长训练。

必需产物：本总纲、`TASK_REGISTRY.md`、G门报告、`DECISION_LOG.md`、`RISK_REGISTER.md`、任务提示/交接、`TAFFC_GO_NO_GO.md`。

### 7.3 任务10：M1—M2数据与协议

状态：**主体完成并通过G1/G2协议数据门**。权威证据为`HANDOFF_10.md`、`G1_G2_EVIDENCE_MATRIX.md`、Data Card/Datasheet、dataset/split/label manifests、泄漏测试及00审查。

继续传播：I3D资产外部证明未闭合；LAI-GAI与CSMV角色不同；HUMAN_GOLD/SILVER不可混用。

### 7.4 任务20：M3基线与统一评测

状态：**G3=`PASS_WITH_LIMITATIONS`**。已完成统一配置、loader、评测器、预测/run manifest、强视觉重实现、单seed正式test及同环境dev replay。

限制：

- temporal-attention是`REIMPLEMENTATION_STRONG_BASELINE`，不是VC-CSA官方复现。
- 当前正式结果是单seed，五种子/CI归任务50。
- 作者VC-CSA探索永久`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`、`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`。
- 探索训练、运行时快照和受限存储生命周期尚未闭环；收尾前不得并发修改共享实验核心或创建任务30。

### 7.5 任务30：M4评论teacher与content student

**目标：**只验证H1和E3。

**启动：**G3通过；Task20共享核心不再被修改/运行；evaluation-kit与content-only基线冻结；H1预注册获00批准。

**必做：**

1. teacher只读取train评论与合法内容；student训练/推理只读取T0内容。
2. 比较hard、soft、普通KD、comment-privileged KD、teacher上界和错配评论负对照。
3. 比较softmax/Dirichlet；分析评论数、分歧、teacher置信度和噪声。
4. 固定等预算调参、至少开发seed趋势、校准和错误案例。
5. 冻结`teacher-student-v1`、预测、配置、E3和`HANDOFF_30.md`。

**进入任务40：**相对最强content-only JSD改善≥3%，方向稳定，ECE恶化≤0.005，错配评论无同等级收益且无泄漏。最终论文门仍须任务50确认≥5%和CI。

**止损：**teacher无有效分布监督或普通KD同样好时，修标签/teacher、降级无teacher检索或停止完整CARM，不直接叠加memory掩盖失败。

### 7.6 任务40：M5反应记忆与可靠性路由

**目标：**验证H2、E2/E4/E7并冻结CARM-v1。

**启动：**H1开发门通过，或00书面批准无teacher降级路线；student表示、split和评测器冻结。

**必做：**

1. 先split后建库；索引manifest记录成员、配置和hash。
2. 实现no/random/BM25/TF-IDF/CLIP/SBERT/learned retrieval及RAMER式对照。
3. 用train内部cross-fitting构造检索效用，禁止test参与路由训练。
4. 比较固定融合、相似度阈值、熵拒绝和收益感知路由。
5. 完成错邻居、低相似、库缩小、top-k、OOD和负迁移分析。
6. 冻结`CARM-v1`、索引、E2/E4/E7、案例图、效率初测和`HANDOFF_40.md`。

**进入任务50：**learned明显优于random；相对no retrieval JSD≥3%或Pareto门成立；路由降低负迁移≥20%或AURC≥10%；泄漏检查0失败。

**止损：**random同样好则删除检索创新；OOD持续受害且路由不能识别则完整CARM不得进入任务50。

### 7.7 任务50：M6—M8正式实验与结果冻结

**启动：**CARM-v1或降级方法、数据/split/评测器/索引冻结；主假设、主指标、seed、调参和停止条件预注册；00批准矩阵。

**执行：**

1. 两个人工主集运行content-only、teacher/student、CARM和最强公平基线。
2. 每个主模型五种子；按原生内容单元paired bootstrap 95% CI。
3. 完成全部适用E0—E9、OOD、污染、校准、效率、失败案例和敏感性。
4. CSMV完成H1/H2；LAI-GAI只承担适用跨域/校准/OOD，不虚构同构teacher/memory。
5. CUC只作中文无标签/银标压力测试。
6. 所有预注册失败结果保留；形成`results-freeze-v1`和claim-evidence-map。

**退出：**依次执行G4、G5、G6；任一失败则降级、延期或重新匹配投稿层级，不硬冲。

### 7.8 任务60：M9—M10论文与投稿

**启动：**G6通过、结果与claim-evidence冻结、复现链可追溯、00批准写作。

**论证结构：**

1. 问题：随机comment split和目标评论输入不等于T0未来受众反应预测。
2. 协议：严格T0、group split、经验分布和train-only历史案例。
3. 方法：评论特权学习与收益感知反应记忆。
4. 证据：两主集、H1/H2、OOD、负对照、校准、选择性风险、效率和失败边界。

**必需产物：**英文论文、出版级图表、匿名复现包、Data/Ethics/Limitations声明、模拟审稿、投稿清单和`HANDOFF_60.md`。

**禁止：**把N/A写成通过、银标写成人工真值、资产风险写成已解决、单seed写成稳定优势或NON_T0探索写入主证据。

### 7.9 允许并行范围

| 来源→下游 | 硬依赖 | 允许并行 |
|---|---|---|
| 10→20 | 数据/split/label与G1/G2 | 只读文献可并行 |
| 20→30 | evaluation-kit、强基线、G3 | 不并发改评测器/teacher核心 |
| 30→40 | teacher/student与H1门 | 不提前建正式memory |
| 40→50 | CARM-v1、索引与H2门 | 不边改方法边跑五种子 |
| 50→60 | 结果冻结、统计与G6 | 写作骨架可早建，主结果不得提前定稿 |

---

## 8. T-AFFC最终Go标准

只有同时满足下列条件才直接投稿：

1. 两个人工主集可合法、可追溯地按各自角色复现。
2. 评论与未来互动从推理输入中物理隔离，索引只含train/历史数据。
3. 所有适用group/topic/source/time/platform协议完整；不适用项有预注册理由。
4. 对最强公平基线达到论文最低JSD门，或达到可靠性Pareto门。
5. teacher、memory、router均有单变量消融；错配评论、随机/错误邻居负对照通过。
6. 五种子、原生单位CI、多重校正、校准、效率、失败案例和伦理说明完整。
7. 两个人工主集承担主要定量结论；中文银标只作压力测试。
8. 代码、配置、split、日志、预测、索引和可发布数据全部可追溯。
9. 模拟审稿不存在构念错位、未来泄漏、模块拼接、放水基线或随机划分高分等Critical。
10. I3D风险按投稿时事实披露；若触发资产止损则依赖I3D的结果不得报告。

若只达到3%开发趋势、CI跨0或只有单数据集/单seed结果，不得以完整T-AFFC方法论文直接投稿。

---

## 9. 风险、禁止与止损

### 9.1 最高风险

- **新颖性：**模块组合被CRC-MRC、评论增强、generalized distillation、RAMER和选择性拒绝前作覆盖。
- **资产：**I3D许可、revision与权利方fixity外部证明未知。
- **证据：**CSMV单T0模态、LAI-GAI跨结构，不能伪造多模态或同构复现。
- **泛化：**发布者、话题、平台和时间捷径可能使随机split高分失真。
- **算力：**任务30/40真实run成本尚待首批smoke校准；远端实例有失联历史。

### 9.2 明确不做

- 不恢复IJCV任务、传播链、GCN/Temporal GNN或第三章主线。
- 不用CH-SIMS/Self-MM高分替代受众反应证据。
- 不用目标评论、最终互动或未来推荐预测T0标签。
- 不追逐旧90.07% Accuracy或195条随机子集高分。
- 不生成伪音频/伪视频补齐模态。
- 不在test后修改split、主指标、阈值、假设、top-k或调参预算。
- 不隐藏失败seed、负结果、不利OOD或资产限制。
- 不同时让两个任务修改同一实验代码或结果文件。

### 9.3 变更纪律

任何研究问题、输入、标签、split、主指标、效应门、方法核心或证据等级变化，都必须：

1. 发布总纲新版本并记录supersedes关系；
2. 更新决策、风险、claim与术语台账；
3. 列出受影响实验和重跑清单；
4. 在使用test结果前完成预注册；
5. 由00书面批准后执行。

---

## 10. 当前执行顺序

1. 任务20完成VC-CSA探索的完成/失败/不可用收尾、运行时快照与受限存储生命周期记录；其结果不进入正式证据。
2. 00确认共享实验核心不再被任务20修改或运行。
3. 创建任务30，先冻结H1目标链、3%开发门、5%论文门、校准guardrail和错配评论负对照。
4. H1开发门通过后创建任务40；否则按失败树降级。
5. H2开发门通过后创建任务50，冻结五种子正式矩阵。
6. G6通过后创建任务60；最终由00执行T-AFFC Go/No-Go。

---

## 11. 权威文件与引用格式

### 11.1 核心SSOT

- 总纲：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.17。
- T0：`T0_INPUT_POLICY.md`。
- 当前实验协议：`experiment-protocol-v2.md`。
- 构念/RQ：`research-question-v1.md`。
- 数据与门：`G1_G2_EVIDENCE_MATRIX.md`、Data Card/Datasheet、data manifests。
- G3：`TASK00_G3_FINAL_REVIEW_20260718.md`、`HANDOFF_20.md`、`BASELINE_TABLE_V1.md`。
- 创新与效应依据：`TAFFC_PAPER_INNOVATION_AND_EXPERIMENT_TARGETS_20260723.md`。
- claim：`CLAIM_EVIDENCE_MATRIX.md`；当前C1—C4有效性均不得在任务50前擅自升级。
- 管理：`TASK_REGISTRY.md`、`WORK_LOG.md`、决策日志、风险登记和`.light/handoff/`。

### 11.2 任务首条提示必须写明

```text
主纲版本：v1.17
当前门状态：G1 PASS；G2_PROTOCOL_DATA PASS_WITH_LIMITATIONS；
ASSET_ADMISSIBILITY DEFERRED_ACCEPTED_RISK；G3 PASS_WITH_LIMITATIONS
上游commit/HANDOFF：
本任务唯一目标：
允许修改：
禁止修改：
退出门：
```

历史文件中的旧版本、旧门和旧任务状态只描述当时事实；当前执行必须回到本节权威文件刷新。

---

## 12. v1.17压缩说明

v1.16的历史决策、任务10/20逐步执行细节、IJCV迁出过程和外部依据未删除其证据，只从活动SSOT移至以下权威材料：

- `.light/decision_log.md`、`.light/version_history.md`；
- `WORK_LOG.md`；
- `HANDOFF_10.md`、`HANDOFF_20.md`及任务审计；
- `PROJECT_STATUS_RETROSPECTIVE_20260720.md`；
- `CONTRIBUTION_PRIOR_ART_MATRIX.md`和`LITERATURE_SEARCH_REPORT.md`。

精简不等于放宽：T0、split、资产、统计、负对照、任务依赖和Go标准均保持或收紧。
