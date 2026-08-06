# Task45 T0历史收益可学习性诊断实验矩阵

> 版本：v1.0（2026-08-06）  
> 状态：`FROZEN_DIAGNOSTIC_ONLY_NO_ROUTER_NO_FORMAL_TEST`  
> 上位方案：`TASK00_TASK45_T0_BENEFIT_LEARNABILITY_RESEARCH_PLAN_20260806.md`

| 实验ID | 对应假设 | 数据集/角色 | baseline | 唯一变化 | 指标 | 混淆/负对照 | seed | 完成判定 |
|---|---|---|---|---|---|---|---|---|
| EXP-4500 | H451/H452 | CSMV原train三角色 | 冻结Task40 P0身份 | 新三角色hash隔离 | overlap/access事件 | source-group全局去重、禁止角色负测 | 固定五seed | role/group/fold overlap=0；旧DEV/router-confirm/formal五类事件=0 |
| EXP-4501 | H451 | FIT→DIAG_CONFIRM | 同容量G0 content-only、prevalence constant | 加G1-G3 T0诊断 | Brier paired差 | shuffled target；同模型/网格/折 | 固定五seed | Brier差CI上界<0且至少4/5 seed差<0 |
| EXP-4502 | H452 | FIT→DIAG_CONFIRM | 同容量G0 content-only、mean constant | 加G1-G3 T0诊断 | MAE paired差 | shuffled target；同模型/网格/折 | 固定五seed | MAE差CI上界<0且至少4/5 seed差<0 |
| ABL-4501 | H451/H452 | FIT→DIAG_CONFIRM | full G0-G3 | 去G1 retrieval geometry | Brier、MAE | 其余组与预算固定 | 固定五seed | 报告G1的Brier、MAE增量及95%CI，不改变primary门 |
| ABL-4502 | H451/H452 | FIT→DIAG_CONFIRM | full G0-G3 | 去G2 evidence quality | Brier、MAE | 其余组与预算固定 | 固定五seed | 报告G2的Brier、MAE增量及95%CI，不改变primary门 |
| ABL-4503 | H451/H452 | FIT→DIAG_CONFIRM | full G0-G3 | 去G3 expert disagreement | Brier、MAE | 其余组与预算固定 | 固定五seed | 报告G3的Brier、MAE增量及95%CI，不改变primary门 |
| ABL-4504 | H451/H452 | FIT→DIAG_CONFIRM | full G0-G3 | 仅G1+G2+G3、无G0 | Brier、MAE | 与full/G0相同预算 | 固定五seed | 报告content与历史诊断的Brier、MAE差及95%CI |
| DIAG-4501 | H451/H452 | DIAG_CONFIRM | 全量响应target | 固定支持量分层和`c+1`敏感性 | b/m/Q05分布、误差 | 查询支持量不作输入 | 固定五seed | 固定5个支持层报告b/m/Q05分布与误差，不得改主门 |
| DIAG-4502 | H451/H452 | Task40冻结负证据+FIT/DIAG_CONFIRM | Task40 point/credible动作 | 不训练router，只审计target/threshold/可分性 | action prevalence、分位、关联 | 不访问ignored cache，不重调阈值 | 固定五seed | 5/5 seed报告action prevalence、分位与关联，不恢复Task40 |

## 公平性与固定顺序

1. 全部trainable诊断器共享数据、折、target draw、模型族、四项网格、trial、seed和评估器。
2. 先EXP-45-00；再同时冻结并执行EXP-45-01/02；只有两者均通过才允许解释消融。
3. Task45不执行效用动作、matched-coverage JSD、负迁移或P5；这些只可能属于未来另行授权Task46。
4. 不增加seed、不删除不利seed、不事后换metric、不访问旧DEV或formal test。
