# Task45：T0历史收益可学习性诊断研究方案

> 版本：v1.0  
> 日期：2026-08-06（Asia/Shanghai）  
> 上位SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.24  
> 状态：`FROZEN_DIAGNOSTIC_ONLY_NO_ROUTER_NO_FORMAL_TEST`  
> 决策：`SC-20260806-01`

## 1. 研究问题、estimand与反证

研究问题：Task40存在稳定Oracle headroom却出现五seed零`USE_MEMORY`退化，究竟是旧`Q05(Delta)`监督过于保守，还是严格T0下历史收益本身不可学习？

Task45只回答两个estimand：

1. 在未参与拟合和选择的`TRAIN_DIAG_CONFIRM`视频上，T0诊断特征对后验获益概率`b_i=P(Delta_i>0)`的Brier loss，是否优于同容量content-only特征模型；
2. 同一确认集上，T0诊断特征对正收益幅度`m_i=E[max(Delta_i,0)]`的MAE，是否优于同容量content-only特征模型。

统计、分析和bootstrap单位均为冻结source group/video；fold和seed不是独立样本。任一主estimand不通过、泄漏、确认集被用于选择、或阴性对照异常通过，都足以阻止后续路由任务。

## 2. 为什么必须新建Task45

Task40的目标、模型选择、DEV_SELECT和DEV_CALIBRATE均已看过，不能被重新命名为确认证据。把替代头继续塞入Task40会造成修复循环和范围漂移。Task45因此是新的独立开发任务，只消费原始train身份与冻结Task40负边界，不继承Task40的开发确认信用。

Task45与未来候选Task46物理分开：Task45诊断通过后停止；未来Task46若获授权，才可训练两阶段效用模型并在此前完全封存的`TRAIN_ROUTER_CONFIRM`上一次性开发确认。Task46现在不创建。

## 3. 数据身份与三角色隔离

唯一数据是`CSMV@99d14240254b1381dde0b9c56add140381f65117`的原始train成员，共5698项、5541个source group。角色由source group一次性确定：

```text
salt = CARM-v124-task45-train-role-v1
u = u64be(SHA256(dataset_revision|source_group_id|salt)) / 2^64
u < 0.6              -> TRAIN_DIAG_FIT
0.6 <= u < 0.8       -> TRAIN_DIAG_CONFIRM
u >= 0.8             -> TRAIN_ROUTER_CONFIRM
```

| 角色 | source groups | videos | Task45权限 |
|---|---:|---:|---|
| `TRAIN_DIAG_FIT` | 3304 | 3404 | 允许生成nested group OOF目标、调固定小网格、拟合诊断器 |
| `TRAIN_DIAG_CONFIRM` | 1126 | 1154 | 一次性诊断确认；不得调参、选特征、换终点或阈值 |
| `TRAIN_ROUTER_CONFIRM` | 1111 | 1140 | Task45完全不可达；只为未来另行授权的Task46保留 |

原`DEV_SELECT`、`DEV_CALIBRATE`、formal test、LAI-GAI、Video2Reaction和MVIndEmo在Task45均不可读取或materialize。角色公式与计数只能因identity/hash不一致而fail-closed，不能按结果交换。

## 4. 目标构造与nested group OOF

内容专家`f0`和历史专家`fH`沿用冻结T0定义；收益为：

```text
Delta_i(theta) = JSD(theta_i,f0_i) - JSD(theta_i,fH_i)
theta_i | c_i ~ Dirichlet(c_i + 0.5)
b_i = P(Delta_i(theta)>0)
m_i = E[max(Delta_i(theta),0)]
l_i = Q05(Delta_i(theta))
```

每项使用固定200个后验draw；`Dirichlet(c+1)`仅作冻结敏感性，不得替换主先验。`TRAIN_DIAG_FIT`中的专家预测与目标必须来自5-fold source-group OOF；诊断器的超参数选择再用其内部4-fold group CV。`TRAIN_DIAG_CONFIRM`的专家只能由全部`TRAIN_DIAG_FIT`训练，不能读取确认标签进行模型或阈值选择。

`b_i`和`m_i`是两个primary target；`l_i`、原点`Delta`、响应支持量分层和Task40五seed零动作退化是secondary mechanism diagnostics，不能挽救主门。

## 5. T0特征组与禁止输入

| 组 | 允许的T0特征 | 机制问题 |
|---|---|---|
| G0 content | `f0`分布、entropy、margin、冻结内容表示质量/缺失mask | 纯内容不确定性是否已足够 |
| G1 retrieval geometry | top-k相似度、top1-top2 margin、邻居距离分布、邻居多样性 | 检索几何是否预示历史适配 |
| G2 historical evidence quality | 邻居自身响应支持量、邻居后验宽度、邻居反应分布一致性 | 历史证据质量是否可在T0审计 |
| G3 expert disagreement | `f0`与`fH`的预测JSD、固定融合差异、候选专家分歧 | 专家冲突是否预示净收益 |

机制化消融固定为：G0-only；G1—G3 diagnostics-only；G0+G1+G2+G3；以及对完整组逐一leave-one-group-out。不得添加话题、时间、publisher等CSMV未冻结字段。

绝对禁止：查询项真实反应分布、查询响应数/支持量、目标评论/文本、未来互动、真实`Delta`、拟合内收益、原DEV结果、formal-test ID/特征/预测/标签。查询响应支持量只可用于结果后的标签可靠性分层，不能作为预测输入。

## 6. 固定模型与公平baseline

本节是`fair_baseline`合同；详细primary与停止规则已在本地版本化`preregistration`中冻结。

概率与幅度各使用一个低容量`HistGradientBoostingRegressor`，两类特征模型共享同一实现、损失、early stopping和四项小网格；最大4 trial/target/feature-set，不增加模型族。五个算法seed保持：

```text
[1364847620, 426925854, 1839464886, 1138176833, 484191872]
```

诊断公平比较是完整T0特征模型对同容量G0 content-only模型；另含prevalence/constant、shuffled-target阴性对照。数据、折、目标draw、参数网格、trial数、训练轮数和评估器完全相同。

未来Task46若获授权，必须在相同训练预算和相同coverage/risk budget下对比：最强content-entropy、Task40 point router、generic gate、SelectiveNet、fixed fusion。该公平比较不在Task45执行。

## 7. 访问边界与零事件合同

- Task45允许读取：原始train成员、train标签/聚合计数、train-only内容特征、train-only历史候选、Task40 tag的代码与负结果文档只读参考。
- Task45禁止读取：旧DEV_SELECT、旧DEV_CALIBRATE、formal test、任何test loader输出、Task40 ignored预测cache。
- 必须分别记录旧DEV、formal test和`TRAIN_ROUTER_CONFIRM`的access/label/feature/prediction/ID事件，全部阈值为0。
- 任一禁止事件非0立即停止，依赖运行作废并交总控；不得清日志重跑后隐去失败。

## 8. 成功、失败、不确定与下一动作

Task45只在两条primary均满足以下条件时记`PASS_LEARNABILITY_DIAGNOSTIC`：

1. 完整T0模型相对G0 content-only的配对loss差，source-group cluster bootstrap 95%CI上界小于0；
2. 五seed中至少4个点估计方向小于0；
3. shuffled-target阴性对照不优于对应constant基线；
4. 所有访问、OOF、角色和预算门通过。

任一primary点估计非负或阴性对照异常通过，记`CLOSED_NOT_PASSED_T0_BENEFIT_LEARNABILITY`。点估计为负但CI跨0，记`INCONCLUSIVE_T0_BENEFIT_LEARNABILITY`；不允许以响应支持分层、`Q05`、某一seed或某一特征消融改判。

通过也不授权路由训练。总控须复核Task45 tag/hash/配对证据，并另行冻结Task46的获益概率+幅度效用、expected regret/risk budget、三动作、最强公平baseline和`TRAIN_ROUTER_CONFIRM`一次性门。主JSD通过后才允许负迁移和P5；formal test仍封存。

## 9. 资源、风险与Plan B

- 单机本地、无付费API、无远程GPU、无新增数据下载；复用冻结特征，诊断模型低容量。
- 不以增加seed补power；五seed仅衡量算法稳定性，统计推断按source group/video。
- 风险：I3D资产外部证明UNKNOWN、有限响应目标噪声、Task40知识污染、训练角色有效样本缩小、通用效用路由新颖性碰撞。
- Plan B：Task45失败/不确定即形成可审计负诊断并关闭替代路由；论文降级为严格T0协议、content-only可靠性或负结果，不堆模块。
