# Task40最终独立审核与关闭裁定

> 审核方：00-T-AFFC总控04  
> 日期：2026-08-05  
> 审核性质：独立、只读、development-only；未代跑新增实验，未materialize formal test，未创建Task50  
> 上游锚点：`origin/main@6b4015e16aca6b6cd5a41540255e0f977413632e`  
> 被审核分支：`codex/task40-carm-cnbr`（未push、未merge）  
> 被审核annotated tag：`refs/tags/task40-carm-cnbr-development-20260805`  
> tag dereference：`c0fe21dc472b508e52ff6c29b8ea54afd7322e0e`

## 1. 裁定

总控04接受Task40的可审计开发交付，并按预注册固定顺序将Task40关闭为：

`CLOSED_NOT_PASSED_ROUTER_MAIN_JSD`

本裁定不是formal-test否定结论。它表示可信净收益router没有通过预先冻结的DEV_CALIBRATE主JSD开发门，因而不得进入可信负迁移、P5、formal test或Task50：

- P0：`PASS`；train=5698、DEV_SELECT=393、DEV_CALIBRATE=444，物理分区与train-only索引闭合；
- P1：`PASS_CONTROLLED_NATURAL_MISMATCH`；top-decile高相似样本570个，受控错位6个，率0.010526，95% CI `[0.003509, 0.019298]`；
- P2：`PASS_STABLE_ORACLE_HEADROOM`；5/5 seed点估计与95% CI下界均为正；
- P3/P4：`CLOSED_NOT_PASSED_ROUTER_MAIN_JSD`；可信router相对每seed由DEV_SELECT选出的最强control为0/5通过；
- 可信负迁移：`NOT_TESTED_FIXED_ORDER_MAIN_JSD_FAILED`；
- P5 thinning、三源不确定性、80/90/95%经验分布预测区域：`NOT_EXECUTED_FIXED_ORDER_ROUTER_MAIN_JSD_FAILED`；
- Task50：`NOT_CREATED`，且本裁定不授权创建。

## 2. Git与fixity独立复核

审核时Task40工作树clean，`HEAD=c0fe21dc472b508e52ff6c29b8ea54afd7322e0e`，相对`origin/main@6b4015e...` ahead 15。annotated tag对象存在并解引用到同一HEAD；两个保留失败运行commit `9cec46a410b130ec3d31dd1370ed01d98ae4b2bd`与`9bd53b31efbea5ee4efa7967ed9c5fcd4ade8f71`均为tag祖先。

总控04从tag工作树重新计算的SHA-256与交付完全一致：

| 证据 | SHA-256 |
|---|---|
| `HANDOFF_40.md` | `6e427c34a3771e7dbb1079fa2fcec8f721cd7566b2e7c49a75e6eb8328f4b8b2` |
| `experiments/task40-carm-cnbr-v1/p3-p4-router.json` | `8b8ca7b33968fb014d4960468fbcdda4b45c11a253976fa47c5d0a9769583b76` |
| 主control配对JSONL | `07fb1117748967caa1436553f76567a6ccbc7d95adfdd2c878a59367c91157da` |
| point/credible直接配对JSONL | `e24befd4fab91428d05357b4387e470852ca121763476584ab74c092b30967d6` |
| P3/P4人读报告 | `3f1d4055df09811454ae332c0005fc4eb7e1c0c792971ae82745c909a32d126e` |
| P5未执行报告 | `c747f7ae67f6b7a53ed8c9f56aed194d384dfda7d876d0a8aef1fdfd0ed34875` |

## 3. 主门独立重算

两份配对JSONL各含2220行，即5 seed×444个DEV_CALIBRATE视频。每种方法、每seed精确回答400/444。按冻结贡献定义重算所得：

| 模型seed | Credible JSD | 最强control JSD | Credible-control | 95% CI | 主门 |
|---:|---:|---:|---:|---:|---|
| 1364847620 | 0.171691 | 0.168647 | +0.003044 | [-0.005744, 0.011977] | FAIL |
| 426925854 | 0.175362 | 0.170473 | +0.004890 | [-0.003587, 0.013020] | FAIL |
| 1839464886 | 0.173515 | 0.168551 | +0.004964 | [-0.003585, 0.013920] | FAIL |
| 1138176833 | 0.172672 | 0.166456 | +0.006216 | [-0.003221, 0.015983] | FAIL |
| 484191872 | 0.172868 | 0.167716 | +0.005152 | [-0.003897, 0.014168] | FAIL |

五个差值方向均不利于credible，且五个95% CI均跨0；不能声称credible优于强control。直接credible-minus-point差也全部为正（`+0.000554/+0.003611/+0.002919/+0.001682/+0.002028`），五个CI均跨0。point在五个seed分别仅选择memory `3/1/1/1/0`次，credible均为0次；这支持“可信下分位监督在本开发实现中退化为全content fallback”的诊断，但不支持对所有可信路由的普遍否定。

机读差异对象内重复出现的`seed=1364847620`是`paired_selective_difference(..., seed)`返回的冻结bootstrap重采样seed；外层五个模型seed完整且配对行按模型seed区分，不是模型seed覆盖或证据身份错误。

## 4. 固定顺序、失败运行与零test事件

- 主JSD门要求每个冻结seed的95% CI上界 `<0`；实际0/5，因此固定顺序在主门处停止。
- `negative_migration.status=NOT_TESTED_FIXED_ORDER_MAIN_JSD_FAILED`且结果数组为空；没有用后续终点挽救主门。
- P5报告只登记未执行边界，没有thinning数值、三源p值、Holm结论或prediction-region coverage/width。
- 第一次失败运行`9cec46a...`在router训练前因float32批形状容差停止，没有科学结果；第二次`9bd53b3...`完成五seed后因报告字典误用JSON布尔量而序列化失败，没有最终机读报告；clean rerun生成最终固定证据。两次失败均在machine report和WORK_LOG保留。
- 最终`access_audit`为train labels 5698、DEV_SELECT labels/features 393、DEV_CALIBRATE labels/features 444；formal-test access/label/feature/prediction/IDs五类计数全部为0。
- tag内没有Task50路径，也没有formal-test标签或预测产物；Task40分支未push、未merge main。

## 5. 独立验证

在tag工作树运行：

- `python -m unittest discover -s tests -p 'test_task40*.py' -v`：25/25通过；
- `validate_task40_p0.py --input-root D:\MMSA-CH-SIMS`：PASS；
- `validate_task40_p1.py --input-root D:\MMSA-CH-SIMS --device cuda`：PASS；
- `validate_task40_p2.py --input-root D:\MMSA-CH-SIMS --device cuda`：PASS；
- `validate_task40_p3_p4.py`：PASS，scientific status为关闭、主门0/5、固定顺序未检验负迁移、formal-test事件0；
- `validate_work_log.py`：285条、0错误、latest=`WR-20260805-025`；
- `git diff --check 6b4015e...tag`：exit 0。

通用`run_preparation_checks.py`仍exit 1，错误是data-free独立worktree相对路径缺少`data/processed/HUMAN_GOLD/csmv/video_labels.v1.jsonl`的`FileNotFoundError`。这与交付披露一致，不是Task40专项validator失败，也未被绕过。

## 6. Claim、风险与后续边界

- C2不得升级：本次仅提供development-only不通过证据，不是formal test；活动可信净收益router候选已关闭，不得写“稳定减少负迁移”或“优于强generic gate”。
- C3未被检验：P5因固定顺序未执行，不得写“三源无效”或“预测区域未校准”；正确表述是“前序router主JSD开发门失败，故未检验”。
- C1不由本次结果升级。C1—C3的论文有效性状态不产生任何`SUPPORTED`升级；稿件继续为`MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS`。
- P1/P2只证明开发现象与Oracle可选择空间，不能覆盖P3/P4失败，也不能进入正式论文结果表。
- 不创建Task50、不恢复Task30 teacher/KD、不运行Video2Reaction B轨、不新增seed/trial/module/coverage追分。任何替代路线或新实验都必须由用户另行明确授权并重新冻结计划。
- G1、G2、G3，Task20永久NON_T0/INELIGIBLE与2026-08-31受限存储截止，以及I3D许可/revision/权利方包身份/fixity为UNKNOWN的边界均不变。

