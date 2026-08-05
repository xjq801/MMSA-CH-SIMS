# CARM可信净收益路由开发预注册

> 版本：v1.0  
> 冻结日期：2026-08-05（Asia/Shanghai）  
> 上位SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.23  
> 状态：`DEVELOPMENT_PREREGISTRATION_FROZEN_NO_FORMAL_TEST`  
> 注册位置：本地Git版本化注册；未提交OSF/AsPredicted，不得写成外部注册  
> 授权边界：只冻结Task40 train/dev开发合同；Task50正式test仍未materialize

## 1. 研究问题与estimand

在目标内容刚发布且目标响应不可见的T0条件下，模型能否只根据目标内容与train-only历史案例，预测使用历史反应记忆相对纯内容预测的**可信净收益**，从而在使用历史、回退纯内容和拒答之间选择，并降低历史证据造成的负迁移？

主要总体为冻结CSMV协议中的视频；统计、分析和paired-bootstrap单位均为视频。评论、fold、响应稀疏化重复和随机种子都不是独立统计样本。

内容专家与历史专家分别为`f0(x_i)`与`fH(x_i,H_i)`。对潜在经验反应分布`theta_i`定义：

```text
Delta_i(theta_i) = JSD(theta_i, f0_i) - JSD(theta_i, fH_i)
```

正值表示历史专家优于内容专家。主机制不是点估计`Delta_i(y_i)`，而是有限响应计数下的：

```text
b_i = P(Delta_i(theta_i) > 0 | c_i, f0_i, fH_i)
l_i = Q_0.05[Delta_i(theta_i) | c_i, f0_i, fH_i]
theta_i | c_i ~ Dirichlet(c_i + 0.5)
```

`Dirichlet(c_i+1)`只作预注册敏感性。点收益路由保留为强基线，不能被删除。

## 2. 数据与信息边界

### 2.1 CSMV核心机制

- 输入标签文件SHA-256：`434eb1f84153be2f71d8db79351acc78cb2cae28691b4d4189f5165f22178869`；
- 8210视频，冻结5698/837/1675 split；有效情绪响应107266，1条情绪缺失；
- 8类计数可从经验分布与有效响应数精确恢复；
- Task40只能读取train及开发所需dev；test标签、test响应和test索引成员保持不可达。

### 2.2 LAI-GAI测量验证

- canonical SHA-256：`ad58c268e34adf02bd8e639338069d34576e1d9602f819a2cc6fa89be6836818`；
- 只做逐维边际有限样本/校准验证；没有联合受访者12维向量；
- H2a/H2b历史记忆为`NOT_APPLICABLE_BY_DESIGN`。

### 2.3 Video2Reaction条件外验

仅在HF revision、所用文件LFS SHA-256、本地SHA-256、许可冲突处理、movie identity和movie-disjoint审计闭合后运行。它不是Task40核心开发的阻塞数据，不得升级为HUMAN_GOLD。

## 3. 划分、OOF与种子

### 3.1 固定算法种子

五个算法随机种子由`SHA256("CARM-CNBR-v1|j")`前4字节映射到正31位整数得到，并在看结果前冻结：

```text
[1364847620, 426925854, 1839464886, 1138176833, 484191872]
```

这些种子只描述算法随机性，不构成五个独立实验对象。

### 3.2 train内部cross-fitting

- 固定5折；source group必须整体进同一fold；
- fold分配由`SHA256(dataset_revision | source_group_id | 1364847620) mod 5`确定；
- 每个样本的`f0_i`、`fH_i`、点收益和后验收益标签均来自未见该样本及其source group的模型；
- OOF manifest必须记录sample工作ID、source group、fold、模型/config/code/data hash与预测hash；
- 任何in-sample收益只能作为`DIAG-01`泄漏诊断，不能训练正式router。

### 3.3 dev选择与校准隔离

dev按source group和冻结hash二分为`DEV_SELECT`与`DEV_CALIBRATE`。模型、K、损失、router阈值和baseline强者只在`DEV_SELECT`选择；预测区域半径、收益概率校准与最终90%动作coverage阈值只在`DEV_CALIBRATE`拟合。两部分不得按结果交换。

## 4. 有限响应协议

### 4.1 CSMV response thinning

- `k={2,4,8,all}`；项目须满足`n_i>=k`；
- 跨k主比较使用`n_i>=8`共同集；
- 每项目每k做200次无放回多元超几何抽样；
- 输出：后验均值误差、90%区间宽度、点收益符号一致率、`b_i`绝对偏离0.5、明确收益/伤害比例；
- 主要可识别性门：从k=2到8，后验区间应收缩且相对全量的收益符号稳定性不能反向恶化；若不成立，有限响应机制claim删除。

### 4.2 LAI-GAI

逐维边际采用`k={8,16,32,all}`；禁止把独立维度重采样写成同一受访者联合向量或12维联合后验。

## 5. 开发实验顺序

1. **P0审计**：数据hash、split、目标响应不可达、索引train-only、source-group OOF测试。
2. **P1自然错位**：连续内容相似度—反应JSD，控制支持量、source group和后验不稳定性；hard pairs仅解释。
3. **P2 Oracle**：在相同预算的content-only、memory-only、fixed fusion之间计算OOF Oracle headroom。无headroom即停止，不训练router。
4. **P3 point router**：用点`Delta`训练三动作路由，作为强基线。
5. **P4 credible router**：用`b_i/l_i`训练可信净收益路由；只改变收益监督，架构、输入和预算与point router一致。
6. **P5三源与区域**：分别验证群体分歧、有限抽样、模型/OOD，并校准80/90/95%经验分布JS区域。
7. **P6外验**：LAI-GAI仅适用测量项；Video2Reaction仅在独立准入后分表运行。

## 6. 公平baseline与唯一变化

必须比较：

- content-only、memory-only、fixed fusion；
- no/random/BM25或TF-IDF/表示kNN/learned retrieval；
- similarity、predictive entropy、OOD distance、generic MLP/MoE gate、SelectiveNet式拒答；
- point-OOF net-benefit router；
- credible/posterior OOF net-benefit router；
- Oracle上界与错配/错域/低相似邻居负对照。

所有可训练gate共享同一T0输入、候选池、主干预测、最大trial数、early stopping、五种子和dev选择规则。可信路由与点路由的唯一机制变化是监督目标，不允许额外参数量、更多调参或额外输入。

## 7. 终点、比较族与判定

### 7.1 主终点

在90%回答coverage下，可信净收益路由相对最强合格generic/point router的逐视频JSD差：

```text
E_video[JSD(CNBR,y) - JSD(best_control,y)]
```

paired video bootstrap 95%CI上界小于0才支持改善。100%和80% coverage及完整risk-coverage曲线为secondary。

### 7.2 固定顺序可靠性终点

只有主JSD终点通过后，才检验可信负迁移率差。对路由选择`USE_MEMORY`的项目，若评价后验满足`P(Delta<0|counts)>=0.95`则记可信负迁移；fallback与abstain不伪记为历史收益。相对最强control的paired-bootstrap 95%CI上界小于0才支持“减少负迁移”。

固定顺序为：H2a Oracle headroom → H2b主JSD → H2b可信负迁移 → H2c三源/区域。前一门失败时，后续只能标exploratory，不用于恢复失败的主张。三源的三个独立消融形成一个family，使用Holm校正，family-wise alpha=0.05。

### 7.3 次要终点

- AURC、routing regret、有害检索AUROC/AUPRC、被避免可信负迁移比例；
- NLL、EMD、Brier、ECE/ACE；
- 80/90/95%经验分布区域coverage、半径/体积代理；
- 响应稀疏化下收益符号稳定性与后验区间宽度；
- 训练/推理时间、显存、索引大小和检索延迟。

## 8. success / failure / inconclusive

- **SUCCESS**：Oracle headroom通过；90% coverage主JSD通过；可信负迁移率固定顺序门通过；三源中每一项只在自己的外部判据和Holm校正后保留；无泄漏和预算不公平。
- **FAILURE**：Oracle无headroom；可信路由不优于point/generic gate；自然OOD负迁移不降；后验收益只在人工hard pairs有效；任何收益标签或索引泄漏。
- **INCONCLUSIVE**：CI跨0、自然group方向不一致、有效样本精度不足或prediction region在交换性审计后无法解释。默认动作是降claim或重新规划新数据，不是增加模块或继续看test。

## 9. 正式test不可见合同

- Task40不读取或materialize CSMV正式test预测/标签，不运行Task50五种子正式比较；
- test loader默认disabled，任何test access event必须fail-closed并写入审计；
- 只有Task40开发门通过、方法/config/seeds/阈值/比较族/claim全部冻结，且00另行创建Task50后，formal test才可一次性materialize；
- formal test一旦materialize，不得根据结果改变模型、阈值、K、损失、不确定性组合、主终点或纳入/排除规则；
- Video2Reaction native test也遵守其独立的相同禁令。

## 10. 资源与停止规则

- P1/P2前禁止大规模扫参；P2无Oracle headroom立即停止router支出；
- 单个可训练方法最大trial数相同，具体上限在Task40实现合同内绑定硬件预算，但不得超过Task20每族12-trial现有公平上限，除非00先书面修订所有方法预算；
- 不使用付费API、远程GPU、闭源LLM、未准入数据或新增大包下载；
- 固定N为现有冻结数据，不把fold/seed扩充冒充统计power。Task50前须基于Task40未看test的dev残差做固定N精度/MDE敏感性并版本化，不能结果后补写。

## 11. 修订政策

任何看到开发outcome后的改变必须追加amendment，说明是否看过outcome、影响哪个claim，并把受影响分析降为exploratory。不得覆盖本文件或把事后时间戳冒充事前注册。
