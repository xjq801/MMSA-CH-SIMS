# 任务00：G2非资产条件反事实复审

> 复审日期：2026-07-17  
> 复审问题：若按用户要求暂不把CSMV I3D资产级许可、稳定官方revision和权利方身份/fixity证明计入本轮判断，G2其余条件是否已满足？  
> 反事实结论：`PASS_NON_ASSET_G2_REQUIREMENTS_WITH_LIMITATIONS`  
> 正式门状态：`G2=BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`，未改变

> 后续裁定：本报告的反事实结论已由`SC-20260717-01`正式采纳并取代上述历史门状态。当前`G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`、`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`、总门=`PASS_WITH_ACCEPTED_ASSET_RISK`、`formal_split=true`，任务20获内部研究授权；资产未知项本身仍未闭合。

## 1. 结论

排除I3D资产准入包后，当前G2的其余数据、协议、泄漏、标签隔离、复现和文档条件均已通过现场复核。因此可以准确地说：

> **G2非资产条件已经满足；当前没有第二个非资产G2阻塞。**

但不能在现行总纲v1.15和机器状态合同下把正式G2直接改写为`PASS`。总纲0.2、0.5、第17节任务10完成定义及现有release manifest均把未解决的许可/资产身份问题作为正式门条件；“暂时忽略”不等于证据已经取得，也不能把`UNKNOWN`改写为`PASS`。

## 2. 非资产G2逐项复核

| 条件 | 现场结果 | 裁定 |
|---|---|---|
| CSMV样本与标签血缘 | 8210条记录、107267条人工响应、8008个源视频族；映射与必需文件检查通过 | PASS |
| 第二人工主集 | LAI-GAI 847条、379组、594/127/126；人工真值、图像/评分fixity、精确与近重复零跨split | PASS |
| 人工金标与自建银标隔离 | HUMAN_GOLD 8210、SILVER 2787；混装负测正确拒绝 | PASS |
| 测试评论与T0输入隔离 | 禁止评论/未来候选字段命中0 | PASS |
| ID、视频组与源族泄漏 | video与hashtag协议的train/dev/test交叉均为0 | PASS_OBSERVABLE_SCOPE |
| 泄漏阻断能力 | live门Critical=0；负面夹具输出`LEAKAGE_BLOCKED` | PASS |
| 公共核心复现 | Python 3.8.9、`-I -S`、19项before/after SHA-256一致、`mismatches=[]` | PASS |
| I3D序列处理协议 | 完整序列+动态padding/mask；均匀180主敏感性；确定性、边界和8类负测通过 | PASS_PROTOCOL_ONLY |
| M2发布包与文档 | 5份文档、8项manifest引用、现场hash和步骤34—39本地包通过 | PASS_LOCAL_PACKAGE |
| 时间协议 | CSMV无发布时间，不发布也不声称time split安全 | NOT_APPLICABLE_WITH_LIMITATION |

## 3. 仍然存在但本反事实排除的事项

- I3D预计算特征的资产级研究使用许可仍未由权利方明确；
- 本地包与稳定官方revision的身份对应仍未得到权利方确认；
- 权利方未提供官方manifest/checksum或等价fixity证明。

本地包自身的相对文件名、bytes、逐文件SHA-256、`float32[T,1024]` schema和8210/8210覆盖已经闭合；缺口是外部权利与官方身份，不是本地文件完整性。

## 4. 对是否进入任务20的影响

当前只完成“检查”，没有获得修改总纲门定义或把隔离资产用于正式论文实验的授权，因此：

- `formal_split=false`；
- `formal_model_use_allowed=false`；
- 不创建任务20；
- 不把本报告写成正式G2放行。

如果后续明确决定承担该发表与许可风险，应先做一次书面范围变更，把门拆为：

1. `G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`；
2. `ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`。

即使采用该路径，论文仍必须披露预计算I3D资产来源与许可不确定性，不得宣称权利方已确认或官方包身份已闭合。该路径会提高审稿、复现与后续发布风险，不能与“资产准入已经通过”等同。

## 5. 现场命令

- `scripts/validate_m2_data_engineering.py`：exit 0；本地数据工程条件通过，正式G2状态仍诚实保持blocked。
- `scripts/run_m2_leakage_tests.py --no-write`：exit 0；Critical=0，`PASS_WITH_LIMITATIONS`。
- `scripts/run_m2_leakage_tests.py --selftest`：exit 0；正确输出`LEAKAGE_BLOCKED`。
- `scripts/reproduce_m2_minimal.py --public-core`：exit 0；19项零漂移。
- `scripts/validate_m2_release.py`：exit 0；本地发布包通过，`g2_asset_ready=false`。
- `scripts/validate_csmv_i3d_sequence_protocol.py`：exit 0。
- `scripts/validate_lai_gai_second_primary.py`：exit 0。
- `scripts/run_preparation_checks.py`：exit 0；`blocking_checks=[]`、`formal_model_work_ready=false`。
