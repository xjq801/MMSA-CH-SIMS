# CARM三idea统一路线研究与实验计划

> 版本：v1.1  
> 日期：2026-08-05（Asia/Shanghai）  
> 决策编号：`SC-20260805-01`  
> 上位SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.23  
> 状态：`PREREGISTRATION_GATES_CLOSED_AWAITING_EXACT_TASK40_CREATION_AUTHORIZATION`  
> 证据等级：计划与预注册草案；不构成实验结果、Task40创建或论文claim支持  

## 1. 路线决策与边界

用户授权把三个想法合并为一条版本化路线并写入总纲：严格T0时目标评论不可见；模型判断历史反应经验是否适用于当前内容；用群体分歧、有限反应抽样和模型/OOD三源不确定性控制使用历史、回退纯内容或拒答。

Task30保持`CLOSED_NOT_PASSED`，H1开发门保持`NOT_PASSED_MECHANISM_NOT_STABLE`，正式H1仍`NOT_ADJUDICATED_ON_FORMAL_TEST`。本路线不恢复评论文本teacher/KD，不materialize Task30 formal test，不把Task30开发数值写入论文。评论在主路线中只用于构造训练样本的经验反应分布、反应支持量和历史记忆标签。

Task40仍未创建。本计划要求的系统查新、数据identity/fitness、目标链、失败树、实验矩阵和公平基线门已以v1.23文档包闭合；只有由00再形成精确创建授权后，才能创建“无teacher可信净收益反应记忆”Task40。Oracle headroom是Task40创建后的第一个开发止损门，不是创建Task40的前置条件。Task50仍只承担未来formal test与五种子正式推断。

## 2. 研究问题、对象、单位与estimand

### 2.1 研究问题

在目标视频刚发布、尚无目标评论的严格T0条件下，能否只根据目标内容与train-only历史案例诊断，提前判断历史受众反应记忆会改善还是伤害当前受众公开表达反应分布预测，并根据三源不确定性选择使用历史、回退纯内容或拒答？

### 2.2 外推边界

- 目标构念：社交媒体评论者公开表达的诱发反应经验分布；不是所有观看者的内在情绪或人口总体参数。
- 主要总体：CSMV冻结协议中的视频；外部证据按LAI-GAI图像和Video2Reaction视频各自定义，禁止合并label space或样本量。
- 统计单位、分析单位与bootstrap单位：原生内容单元；CSMV/Video2Reaction为视频，LAI-GAI为图像。
- 随机种子和cross-fitting fold只估计算法随机性或生成OOF标签，不是独立统计样本。

### 2.3 专家、效用与主estimand

内容专家为`f0(x_i)`，历史记忆专家为`fH(x_i,H_i)`。在train内部cross-fitting中定义：

```text
Delta_i = JSD(y_i, f0(x_i)) - JSD(y_i, fH(x_i,H_i))
```

`Delta_i>0`表示历史记忆相对纯内容有益。对有限反应计数`c_i`冻结`theta_i|c_i ~ Dirichlet(c_i+0.5)`（敏感性分析改为`+1`），计算`b_i=P(Delta_i(theta_i)>0|c_i)`与`l_i=Q_0.05(Delta_i(theta_i)|c_i)`。点收益路由只预测期望收益；可信净收益路由则使用`b_i/l_i`，只有当历史有益的后验证据足够时才选`USE_MEMORY`。路由器`g(z_i)`只能读取T0内容、train-only邻居相似度/分歧/支持量、合法域距离和推理时可得的模型不确定性。

主estimand是：在预注册coverage相同的CSMV开发/正式评测中，收益感知路由相对最强固定融合或通用选择性gate的内容单元平均JSD差，以及负迁移率差。主要统计判据为视频级配对bootstrap 95%CI；不恢复已撤回v1.17的3%/5%/8%硬效应门。

## 3. 可证伪假设与失败树

| 假设 | 陈述 | 主检验 | 支持条件 | 反证/止损条件 |
|---|---|---|---|---|
| H2a | 内容相似不保证反应相似，且不同样本对历史记忆存在可选择的真实净收益差异 | 连续content-similarity—reaction-distance分析；Oracle headroom | 控制反应支持量、source family和抽样不稳定性后错位关系仍存在；Oracle相对最强单专家/固定融合的改善CI下界大于0 | 控制混杂后错位消失，或Oracle无稳定headroom：停止学习router |
| H2b | OOF净效用路由能在T0提前识别有害历史并减少负迁移 | matched-coverage JSD、负迁移率、routing regret、AURC | 相对最强固定融合/相似度/熵/OOD/generic gate，在公平预算下JSD差CI上界小于0，且负迁移或选择性风险至少一项改善、校准不恶化 | 不优于任一强简单对照，或优势只在人工hard pairs：删除收益感知路由主张 |
| H2c | 群体分歧、有限响应抽样和模型/OOD不确定性可被分别验证并支持更可靠决策 | 三类独立验证+80/90/95%经验分布预测区域 | 各不确定性分别预测其预注册外部/重采样判据；经验分布区域达到目标coverage且OOD下选择性风险受控 | 三源不可区分，或区域系统性失配：删除三源分解/coverage claim，保留普通不确定性结果 |

若CI跨越判定边界或不同自然group split方向不一致，结果记`INCONCLUSIVE`，不得以增加模块继续追分；回到研究方案重新规划或降低claim。

## 4. 数据集、获取与证据角色

| 数据集 | 当前身份与规模 | 本路线用途 | 获取/执行状态 | 禁止外推 |
|---|---|---|---|---|
| CSMV/MSA-CRVI | 8210视频；107267条人工评论标注；冻结5698/837/1675 source-family split；每视频2—20条反应、中位数14 | 唯一核心机制集：T0内容、历史净效用、OOF路由、三源不确定性、自然source-family/group OOD | canonical与标签已冻结；仅允许固定I3D内部研究，资产许可/revision/权利方身份/fixity仍UNKNOWN/accepted risk | 不声称原始视频端到端、音视频融合、time/topic/publisher OOD或可再分发I3D |
| LAI-GAI | 847图、63682人工反应、594/127/126 split、379组、CC BY 4.0 | HUMAN_GOLD外部测量：群体分歧、有限抽样、校准和预测区域；不承担视频历史记忆 | 已冻结，可按现有Data Card执行 | 无评论历史/视频时序；H2a/H2b记`NOT_APPLICABLE_BY_DESIGN` |
| Video2Reaction | 10348视频、21类反应分布；公开派生特征与`SILVER_LLM_HUMAN_VERIFIED`标签 | closest/direct prior；A轨CSMV公平适配；B轨movie-disjoint银标外部记忆/路由验证 | 先做revision/file tree/size/hash/license/movie identity intake；未冻结前不运行 | 不是第三HUMAN_GOLD；不保证原评论、原始视频/音频可再分发；不跨数据横比绝对指标 |
| MVIndEmo | 论文报告7153视频、8话题、银标 | 仅候选银标压力测试 | 所列仓库当前404，identity/license/revision未闭合，状态`NOT_FIT_CURRENTLY` | 不进入主表、不阻塞主路线、不据论文描述推定数据已取得 |

NEmo+与用户未跟踪`NEmoP/`不在本路线必需数据中；未经单独数据identity/fitness审计，不读取或纳入实验。

## 5. 技术路线

```text
训练样本评论标签/计数 ──> 经验反应分布 y 与支持量 n ──> train-only历史记忆
T0内容 x ──> content expert f0 ─────────────────────────────┐
       └─> 检索train-only邻居 ─> memory expert fH ─────────┤
OOF(f0,fH) ─> Delta标签 ─> benefit router g(z) ────────────┤
群体分歧 / 有限抽样 / ensemble-OOD ─> 三源不确定性 ───────┤
                                                         └─> 使用历史 / 回退f0 / 拒答
                                                             + 经验反应分布预测区域
```

### 5.1 三源不确定性操作化

1. **群体分歧`U_group`**：经验反应分布的归一化熵/离散度；用held-out评论或split-half分歧复核，不由模型误差反推。
2. **有限抽样`U_sample`**：根据每内容响应数`n_i`做Dirichlet-multinomial后验或非参数评论重采样；以不同子样本经验分布间JSD作为外部判据。
3. **模型/OOD`U_epi`**：独立初始化ensemble分歧、内容到train support距离和自然group-held-out错误；不得用单一Dirichlet浓度同时冒充三源。

### 5.2 预测区域

在独立dev calibration子集上校准JS半径：

```text
C_i = {p in simplex(K): JSD(p, p_hat_i) <= q_i}
```

报告80%/90%/95%目标coverage、区域半径/体积代理、分组coverage和risk-coverage。保证对象首先是可观察的经验反应分布；对潜在总体反应、沉默观看者或因果社会效应不作coverage保证。Conformal集合大小不直接解释为群体真实分歧。

## 6. 具体实验步骤

### P0：计划、数据与泄漏准备门（00；只读/文档）

1. 冻结本计划、实验矩阵、数据identity/fitness和系统查新范围。
2. 记录CSMV/LAI-GAI精确数据与split hash；Video2Reaction完成intake后另升数据版本。
3. 检查train/dev/test ID、source family、近重复、索引成员和目标响应不可达。
4. 冻结开发种子`[1364847620, 426925854, 1839464886, 1138176833, 484191872]`、5-fold group OOF、最大trial数、主指标、threshold/coverage选择规则和预算。
5. 划分`DEV_SELECT`与`DEV_CALIBRATE`；本文档门闭合只能解除Task40创建阻断，Oracle、router和区域的结果门都必须在Task40内按顺序执行。

### P1：内容—反应错位现象门（Task40候选；train/cross-fit only）

1. 用冻结内容表示计算train-fold内近邻相似度；禁止从dev/test建库。
2. 计算邻居反应JSD、支持量差和重采样稳定性。
3. 以连续回归/秩相关为主，评估内容相似度与反应距离；控制`n_i`、source family和抽样不稳定性。CSMV按`k=2/4/8/all`做200次response thinning，跨`k`主比较限定在`n>=8`的共同样本。
4. 高内容相似且高反应距离的hard pairs只作解释性审计；阈值只由train分位数冻结，不作为主统计证据。
5. 人工审核固定子集的ID/内容关系与标签分布，不读取或公开敏感评论正文。

### P2：Oracle headroom门（Task40候选；train/cross-fit + dev）

1. 在相同预算下训练content-only、固定memory、固定融合。
2. 只用OOF预测计算逐样本`Delta_i`与Oracle选择上界。
3. 对Oracle相对最强单专家/固定融合的JSD差做视频级paired bootstrap。
4. Oracle没有稳定headroom时立即停止P3，不训练router，不查看formal test。

### P3：OOF收益路由（Task40候选；dev-only模型选择）

1. memory仅保存train ID、内容表示、经验分布、支持量和合法质量字段。
2. 比较no-memory、random、BM25/TF-IDF、表示kNN、learned retrieval。
3. 用train内部cross-fitting生成点`Delta`及`b_i/l_i`后验目标；公平比较通用gate、点收益路由和可信净收益路由。
4. 动作空间固定为`USE_MEMORY`、`FALLBACK_CONTENT`、`ABSTAIN`；阈值只在dev按预注册coverage选择。
5. 比较固定融合、相似度阈值、预测熵、OOD距离、generic MLP/MoE gate、SelectiveNet式拒绝以及Oracle上界。
6. 在random/错域/低相似邻居、库缩小、top-k和自然source-family OOD下检查负迁移；主可靠性终点冻结为匹配coverage下的可信路由负迁移率差。

### P4：三源不确定性与预测区域（Task40候选；dev only）

1. `U_group`与held-out/split-half群体分歧做Spearman/误差分析。
2. `U_sample`与评论下采样造成的经验分布JSD/方差做对应分析；按支持量分层。
3. `U_epi`预测自然group OOD或高误差样本，报告AUROC/AUPRC和risk-coverage。
4. 在dev calibration子集校准80/90/95% JS预测区域；报告总体和分组coverage。
5. 做单变量消融：分别去掉`U_group`、`U_sample`、`U_epi`，不能联合移除后宣称单源贡献。

### P5：外部验证（Task50候选；需单独准入）

1. LAI-GAI只运行content distribution、三源中可测的group/sample/epistemic部分和预测区域；历史记忆记N/A。
2. Video2Reaction先复现公开特征基线，再按movie identity建立movie-disjoint协议；只用train反应分布建库。
3. CSMV、LAI-GAI、Video2Reaction分表报告，禁止pooling或绝对指标横比。

### P6：正式统计与结果冻结（仅Task50）

1. formal test只在方法、阈值、种子、预算和claim全部冻结后一次性materialize。
2. 目标方法与所有强基线使用同一五种子和最大调参预算。
3. 按原生内容单元做paired bootstrap 95%CI和预注册comparison-family校正。
4. 完整报告失败seed、负结果、效率、AURC、routing regret、负迁移率、prediction-region coverage和失败案例。

## 7. 实验矩阵与公平对照

| ID | 假设 | 数据 | 唯一变化 | 主要对照 | 主指标/完成判定 |
|---|---|---|---|---|---|
| EXP-00 | H2a | CSMV train OOF | 连续内容相似度→反应距离 | shuffled reaction、source/support controls | 控制混杂后的关系与自然错位证据；不成立即止损 |
| EXP-01 | H2a | CSMV train/dev | Oracle在`f0/fH`间选择 | content-only、memory-only、fixed fusion | Oracle JSD改善CI下界>0，否则停止router |
| EXP-02 | H2b | CSMV train/dev | OOF点收益与可信净收益路由 | similarity/entropy/OOD/generic gate/SelectiveNet | matched-coverage JSD差CI上界<0；可信路由的负迁移率不劣且优于点路由 |
| MEAS-01 | H2a/H2b/H2c | CSMV/LAI-GAI | response thinning与后验敏感性 | all-response、bootstrap、Dirichlet(0.5/1) | 收益符号/后验决策对有限反应稳定；LAI-GAI仅维度边际 |
| EXP-03 | H2b | CSMV自然group/OOD | 邻居质量下降 | random/wrong-domain/low-sim neighbors | 负迁移率或AURC优于最强简单gate |
| ABL-01 | H2b | CSMV | 只去benefit target，保留同架构 | generic gate | 判断收益来自净效用监督而非参数量 |
| ABL-02/03/04 | H2c | CSMV/LAI-GAI | 每次只去一个不确定性源 | 完整三源模型 | 各源须改善其对应外部判据，不靠平均JSD归因 |
| CAL-01 | H2c | CSMV/LAI-GAI | JS预测区域校准 | global radius、entropy-only | 达到预设经验分布coverage并报告区域效率 |
| GEN-01 | H2b/H2c | Video2Reaction | 只切到movie-disjoint银标外域 | direct/LDL、fixed memory/gate | 分表外部效度；不升级HUMAN_GOLD主张 |

所有可训练基线必须同数据、split、T0输入、候选池、模型选择规则、最大trial数和种子；无法达到公平预算的对照须降级为参考，不能用于SOTA结论。

## 8. 指标、统计与选择规则

- **Primary**：matched-coverage下路由相对最强固定融合/generic gate的内容单元平均JSD差。
- **Primary reliability**：在90%回答coverage下，可信净收益路由相对最强点收益/generic router的负迁移率差；AURC固dbsecondary。
- **Secondary**：NLL、EMD、Brier、ECE/ACE、routing regret、harmful-retrieval AUROC/AUPRC、被避免负迁移比例、coverage和区域效率。
- **Exploratory**：hard-pair案例、不同支持量/情绪类别/邻居K的异质性。
- 模型选择只看dev；formal test不用于选择阈值、coverage、K、损失、head或不确定性组合。
- 缺失预测、数值异常或无合法邻居按事前fallback回退content-only并单列失败率，不静默删除。
- 多重比较按预注册family使用Holm或BH；确切方法在Task40创建合同中冻结。

## 9. 资源、产物与复现

- 先使用冻结I3D和小型MLP/attention/router；单卡12—24GB为目标，不从头训练大视频模型。
- P1/P2通过前不做大规模扫参；P3最大trial数须与generic gate相同。
- 每次run绑定Git commit、环境、数据/split/index/config hash、seed、stdout/stderr、预测和指标；失败run同样保留。
- 私有模型state、逐样本预测和受限资产保持Git忽略；Git只保存非秘密manifest、hash、汇总与代码。
- Task40最低产物：数据flow图、OOF效用manifest、Oracle报告、三源验证报告、实验矩阵、失败树、索引manifest、开发结果与`HANDOFF_40.md`。

## 10. 创建与停止门

### Task40创建前必须全部满足

1. 本计划与总纲v1.23提交并推送；
2. 系统查新范围和closest-prior矩阵冻结，但不得宣称穷尽或世界首创；
3. CSMV与LAI-GAI数据identity/fitness合同闭合，Video2Reaction保持独立准入；
4. question→estimand→endpoint→analysis→falsifier目标链通过；
5. success/failure/inconclusive失败树通过；
6. 公平基线、cross-fitting、正式test禁令、预算和阈值规则通过00独立审核；
7. 另有明确`AUTH-00-TASK40-...`创建文件。Oracle headroom不在本列：它是Task40创建后、router训练前的第一开发止损门。

### 全路线kill criteria

- 内容—反应错位由支持量/source/noise解释后不稳定；
- Oracle无headroom；
- OOF路由不优于最强简单/generic gate；
- 三源不能分别预测各自判据；
- prediction region不能达到预设coverage；
- 收益只来自人工hard pairs、随机split、同源捷径或不公平预算；
- 发生任何目标响应、test、未来候选或跨split索引泄漏。

任一核心kill触发时，禁止增加teacher、GNN、MLLM或额外模块掩盖失败；路线降级为content-only可靠性测量、协议/负结果研究，或由用户决定停止。
