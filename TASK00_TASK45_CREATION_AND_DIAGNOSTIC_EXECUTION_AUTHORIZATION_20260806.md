# Task45创建与诊断执行授权

> 授权ID：`AUTH-00-TASK45-T0-BENEFIT-LEARNABILITY-20260806`  
> 签发者：00-T-AFFC总控04  
> 计划锚点：`origin/main@8a5ab2c2c543051e00427154db205bb3937de2bf`  
> 授权状态：`AUTHORIZED_TO_CREATE_READONLY_UNTIL_TASK45_FINAL_ANCHOR`  
> 任务性质：`DEVELOPMENT_DIAGNOSTIC_ONLY`

## 1. 裁定

批准创建一个新的独立Task45 worktree任务，名称为“45-T0历史收益可学习性诊断”，建议分支`codex/task45-t0-benefit-learnability`。Task45不是Task40修复代理，不继承Task40的实验授权或成功信用；Task40永久保持`CLOSED_NOT_PASSED_ROUTER_MAIN_JSD`。

Task45创建后，在总控04发送`TASK45_DIAGNOSTIC_FINAL_ANCHOR`前只读。FINAL_ANCHOR必须给出包含本授权、Task45线程ID和S43的最新`origin/main` commit；收到后才可从P0开始。

## 2. 唯一执行范围

Task45只可串行执行：

1. **P0 identity/access/leakage**：重算冻结source manifest hash、三角色公式/计数、source-group零重叠、FIT内fold隔离和旧DEV/router-confirm/formal-test零事件；
2. **P1 FIT nested group OOF**：只在`TRAIN_DIAG_FIT`生成专家OOF预测与`b=P(Delta>0)`、`m=E[max(Delta,0)]`、`Q05`目标；只在FIT内部4-fold group CV选择冻结四项小网格；
3. **P2 one-shot DIAG_CONFIRM**：所有选择冻结后一次性评估full G0—G3相对同容量G0-only的Brier与MAE；执行shuffled-target、预注册支持量分层、五seed零动作机制审计和逐组消融；
4. **交付**：无论PASS/FAIL/INCONCLUSIVE都立即停止，提交可审计branch、annotated tag、`HANDOFF_45.md`、machine/human report、paired evidence、hash、失败运行与零访问账供总控独立审核。

Task45不得训练或执行`USE_MEMORY/FALLBACK_CONTENT/ABSTAIN`两阶段路由器，不得计算matched-coverage路由主JSD、负迁移或P5结果。

## 3. 数据与访问合同

- 唯一数据范围：CSMV原始train 5698视频/5541 source group。
- 角色：FIT=3404、DIAG_CONFIRM=1154、ROUTER_CONFIRM=1140；精确公式与salt以`.light/carm-v124-access-boundary.json`为准。
- Task45允许：FIT；全部选择冻结后的DIAG_CONFIRM；train-only内容特征、聚合计数和候选历史。
- Task45禁止：旧DEV_SELECT、旧DEV_CALIBRATE、TRAIN_ROUTER_CONFIRM、formal-test IDs/features/labels/predictions/aggregates、Task40 ignored caches、查询响应支持量/评论/真实收益作为模型输入。
- 允许只读参考Task40 annotated tag的tracked代码和报告；不得cherry-pick整个Task40结果链、导入ignored cache或把Task40的DEV结果当确认。复用代码须逐文件记录来源commit/hash。
- 任一禁止访问或role/group overlap事件`>0`，立即fail-closed并保留失败证据。

## 4. Primary门与停止

两条primary必须同时通过：

- `Brier(full)-Brier(G0)`的source-group cluster-bootstrap 95%CI上界`<0`，且至少4/5 seed点差`<0`；
- `MAE(full)-MAE(G0)`满足相同条件；
- shuffled-target不得以95%CI上界`<0`优于constant；访问、OOF、预算和角色门全部通过。

任一primary点差`>=0`或阴性对照异常，关闭为`CLOSED_NOT_PASSED_T0_BENEFIT_LEARNABILITY`；方向有利但CI跨0或seed方向不足，关闭为`INCONCLUSIVE_T0_BENEFIT_LEARNABILITY`。不得增加seed、放宽CI门、换metric、删不利seed、交换角色或用secondary挽救。

`PASS_LEARNABILITY_DIAGNOSTIC`也不授权Task46；Task45必须停机回交。

## 5. 固定预算与公平性

- 五seed：`1364847620/426925854/1839464886/1138176833/484191872`；
- 每个target×feature-set最多4 trial；固定HGB网格、5-fold专家OOF、4-fold诊断CV、200 posterior draws、10000 cluster-bootstrap replicate；
- full与G0共享模型、数据、折、draw、trial、seed和评估器；
- 不新增数据、下载、付费API、云GPU、闭源LLM或大模型模块。

## 6. 交付物与tag

最低交付：

- `HANDOFF_45.md`；
- P0 access/leakage machine report与validator；
- FIT/DIAG_CONFIRM角色manifest、fold manifest、target/feature schema及hash；
- 两条primary的per-item paired JSONL、machine report、人读报告与独立validator；
- 逐组消融、support/Q05/零动作secondary报告，清楚标记不能改主门；
- formal-test、旧DEV和router-confirm分项零事件账；
- tests、environment、config、failed-run evidence、WORK_LOG；
- annotated tag建议：`task45-t0-benefit-learnability-development-20260806`。

Task45分支不得push或merge main，除非用户另行授权。总控只从commit/tag独立审核，不与Task45并发修改实验核心。

## 7. 绑定工件

| 工件 | SHA-256 |
|---|---|
| 可发表性/closest-prior审计 | `253efbf3d31e4dfa918d2af4af082a3ac3d7c179c02dc2696282ecebcbd02056` |
| Task45研究方案 | `43146a2952128df25001f3e7476c44dc54db3e9f3d2ac68c1839dbc7a9065ddf` |
| Task45预注册 | `e9778586b98ec31dfcaef5fb360393074b1148151a2976a72b71d04c83f81263` |
| 实验矩阵 | `6da934ca6acdd3cf02412a175009fcb4e1694cbd6bc54f3b490db2516e231c3b` |
| data identity | `f14bc4d4458c228185a6de2b24d03962e40bc8418f52dc67e8de5a3bbacffe1e` |
| access boundary | `9385bf45888b2dc760e66f19c0c88a03ef9a07119de371bddd772b3fdd4db85a` |
| target chain | `2f71817ba9c44ea48119c70517cdf9000240ccf30f49534a0061bb63cff7d324` |
| failure tree | `f23f699319b99384836ede953d45cc9b257a414db3127e6148da8f8ac8bab64f` |
| plan package manifest | `52bdc02ce6f7171c0b493218a414c7ccc753b5e601ab2351075519d23cb70439` |
| reproducibility checklist | `f237762ccc0abfd1db2c9b817ca6897a82fc192d6ce77d945f03452400251bb1` |

## 8. 基础设施例外与非豁免声明

`target_chain.py`、`failure_tree_gate.py`与`plan_lint.py`分别PASS/PASS/100；`plan_gate.py`确认公平baseline与可量化反证，但当前技能安装缺`_shared`，无法产出`light.findings.v1`，因此最终package gate保留两个schema/gate错误。总控只接受这是工具打包基础设施例外，不豁免任何科学、泄漏、公平、反证或访问门，也不伪称package gate PASS。

## 9. 不变边界

G1、G2、G3不变；I3D许可/官方revision/权利方包身份-fixity仍UNKNOWN且禁止再分发；Task20 NON_T0/INELIGIBLE与2026-08-31截止不变；Task30、Task40关闭；Task46/50不创建；论文仍`MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS`且C1—C3=`TO_VERIFY`。

