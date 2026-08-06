# Task45 T0历史收益可学习性诊断预注册

> 版本：v1.0  
> 冻结日期：2026-08-06（Asia/Shanghai）  
> registration status：`LOCAL-ONLY`  
> 状态：`DIAGNOSTIC_ONLY_NO_ROUTER_NO_FORMAL_TEST`  
> 授权：仅Task45 train内部诊断；不是外部注册，不是正式结果预注册

## 1. Primary questions and endpoints

`Q-PROB`：完整T0诊断特征是否比同容量content-only特征更准确地预测后验获益概率`b_i=P(Delta_i>0)`？

- primary metric：`Brier = mean((b_hat_i-b_i)^2)`；
- primary contrast：`Brier(full T0)-Brier(G0 content-only)`；
- success：`TRAIN_DIAG_CONFIRM`上的source-group cluster paired-bootstrap 95%CI上界`<0`，且至少4/5 seed的点差`<0`。

`Q-MAG`：完整T0诊断特征是否比同容量content-only特征更准确地预测正收益幅度`m_i=E[max(Delta_i,0)]`？

- primary metric：`MAE = mean(abs(m_hat_i-m_i))`；
- primary contrast：`MAE(full T0)-MAE(G0 content-only)`；
- success：同样要求95%CI上界`<0`且至少4/5 seed点差`<0`。

两条primary是串联AND门，不做择优；任一不通过即不得申请Task46。bootstrap replicate固定10000，置信水平95%，source group为cluster；seed/fold不作为独立n。

## 2. Targets

```text
Delta_i(theta) = JSD(theta_i,f0_i) - JSD(theta_i,fH_i)
theta_i | c_i ~ Dirichlet(c_i+0.5)
b_i = P(Delta_i(theta)>0)
m_i = E[max(Delta_i(theta),0)]
l_i = Q0.05(Delta_i(theta))
```

主先验固定`0.5`，每项200 draws。draw RNG由`SHA256(item_work_id|expert_seed|CARM-v124-posterior-v1)`确定。`Dirichlet(c+1)`、`l_i`和点`Delta`是secondary，不得替换primary。

## 3. Roles, nesting and access

- 三角色公式、salt与计数以研究方案和`.light/carm-v124-access-boundary.json`为准。
- `TRAIN_DIAG_FIT`：5-fold source-group OOF生成专家预测/target；4-fold group CV选择固定小网格。
- `TRAIN_DIAG_CONFIRM`：只在全部选择冻结后执行一次；不得用于early stopping、特征筛选、超参选择、校准、阈值或终点选择。
- `TRAIN_ROUTER_CONFIRM`、旧DEV_SELECT、旧DEV_CALIBRATE、formal test：Task45五类访问事件全部必须为0。

## 4. Model, tuning and budget

概率与幅度均用`HistGradientBoostingRegressor`。固定网格：

```text
max_leaf_nodes in {7, 15}
l2_regularization in {1.0, 10.0}
learning_rate = 0.05
max_iter = 100
min_samples_leaf = 30
early_stopping = false
```

每个target×feature-set最多4 trial；inner-CV仅用`TRAIN_DIAG_FIT`，选择规则为平均group-held-out loss最小，完全相等时依次选更少leaf、更多L2。概率输出clip到`[0,1]`，幅度输出clip到`[0,+inf)`；这些clip对所有baseline相同。

## 5. Mechanistic feature groups and ablations

- G0 content：content prediction、entropy、margin、合法质量/missingness；
- G1 retrieval geometry：top-k similarity/margin/距离分布/邻居多样性；
- G2 historical evidence quality：邻居支持量、邻居后验宽度、邻居分布一致性；
- G3 expert disagreement：`JSD(f0,fH)`、固定融合差异、候选专家分歧。

预注册比较：constant、G0-only、G1+G2+G3、G0+G1+G2+G3、完整组分别减G1/G2/G3，以及shuffled-target。消融只解释机制，不改变两条primary的full-vs-G0门。

查询真实响应、查询响应数、目标评论、未来互动、真实收益、拟合内收益、旧DEV和formal-test信息均禁止作为特征。查询响应支持量只在确认后按`2-4/5-8/9-12/13-16/17-20`固定层级做secondary标签可靠性分析。

## 6. Secondary and exploratory analyses

Secondary：

- `l_i=Q05(Delta)`分布、`b_i`分布、`m_i`分布及其与响应支持量的关系；
- Task40五seed零`USE_MEMORY`退化的标签prevalence、阈值位置、可分性和feature-group关联；
- full相对constant的Brier/MAE、Spearman、top-decile positive-benefit enrichment；
- leave-one-group-out消融与既有五seed方向。

Exploratory：`Dirichlet(c+1)`敏感性与误差案例。Exploratory不得改变primary、申请Task46或进入正式主张。

## 7. Negative controls and guardrails

- shuffled-target：在source group内按冻结置换规则打乱`b/m`；不得优于prevalence/mean constant的95%CI上界`<0`。若异常通过，判潜在泄漏/实现错误并停止。
- identity/OOF：任何role overlap、source-group跨role/跨fold、拟合内target或非法索引为0容忍。
- budget：full与G0相同模型、网格、trial、seed、折和评估器。
- no optional stopping：五seed和10000 bootstrap固定；不得增加seed、删seed或看到结果后换metric。

## 8. Failure, inconclusive and stopping

- `PASS_LEARNABILITY_DIAGNOSTIC`：两primary均通过，阴性对照与所有guardrail通过。
- `CLOSED_NOT_PASSED_T0_BENEFIT_LEARNABILITY`：任一primary点差非负、阴性对照异常、或发现泄漏/预算不公。
- `INCONCLUSIVE_T0_BENEFIT_LEARNABILITY`：两primary方向有至少一项CI跨0，或有效确认精度不足，且无硬失败。

任一非PASS立即停止，不创建Task46。PASS也立即停止；只允许总控独立审核后另行预注册和授权。

## 9. Amendment policy

看到任何Task45 outcome后的修改必须追加版本化amendment并把受影响分析降为exploratory。不得覆盖本文件，不得在旧DEV_CALIBRATE调阈值，不得用formal test确认，不得放宽旧Task40门。

