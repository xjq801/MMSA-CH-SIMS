# 00对VC-CSA泄漏风险接受型探索实验的授权裁定

> 日期：2026-07-18  
> 决策号：`SC-20260718-04`  
> 父状态：`main@c5a552b131eebc7d7a37ac017d33dc95d95b0542`

## 裁定

`METHOD_LEAKAGE_RISK=USER_ACCEPTED_FOR_EXPLORATORY_ONLY`

`EXPERIMENT_IDENTITY=AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`

`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`

`REMOTE_I3D_TRANSFER_AUTHORIZATION=APPROVED_IN_PRINCIPLE_FOR_THIS_INSTANCE_AND_THIS_EXPLORATORY_RUN_ONLY`

`EFFECTIVE_I3D_TRANSFER_PERMISSION=PENDING_EXPLORATORY_CONTRACT_HASH_REVIEW`

用户已明确要求不再以跨 split peer 泄漏作为停止该次探索运行的理由。00接受该方法学风险仅用于隔离的工程探索，不把泄漏重新解释为不存在、已修复或可用于正式评估。任务20可按作者完整 comment split、完整 `video_to_comment` 和原 peer 逻辑起草新的探索执行合同；在00复核并绑定该合同的精确SHA-256前，真实I3D仍不得传输。

## 实验身份与披露

该运行必须始终使用`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`身份，不得简称为无泄漏复现、可信复现、官方main复现、T0适配或正式baseline。所有运行记录和结果说明必须显式披露：

- 作者随机comment split中有7,854个视频跨split；
- train/dev/test分别有122/2,750/1,573个split内singleton，其可用peer仅来自其他split；
- 保留作者完整映射时，train阶段可能读取dev/test的peer评论与标签；
- 因而dev/test指标受污染，不能估计held-out泛化、不能支持无泄漏或公平比较claim。

本授权不要求修改peer逻辑，也不允许把该运行改写成`REIMPLEMENTATION_NON_FAITHFUL_PEER_ADAPTATION`。既有`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`仍是faithful、clean、formal评估路径的有效结论；本裁定只建立一个用户知情接受风险的隔离探索例外。

## 结果隔离

该运行只允许作为一次单种子工程诊断。增加种子不能修复证据资格，未经00另行书面授权不得扩成五种子、bootstrap或任务50。

结果不得进入或回写：

1. T0统一baseline或`BASELINE_TABLE_V1.md`正式比较列；
2. G3主证据、冻结G3 package或`HANDOFF_20.md`的既有证据快照；
3. 任务50、多种子统计、论文主表或支持泛化/优越性/无泄漏的claim；
4. 与temporal-attention或其他legacy baseline的排名、显著性或数值优劣比较。

允许保存最小化的聚合运行诊断和资源日志；模型权重、逐样本预测、评论正文、标签明细、I3D特征和本机路径不得进入Git或公开材料。

## 资产与实例硬门

用户此前对当前私人租用实例、固定manifest中8210项I3D、仅内部研究训练、任务后删除且不发布/不转交第三方的扩权继续有效，但不闭合I3D许可、官方revision、权利方包身份或fixity。`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`不变。

任务20的新探索合同至少必须继续绑定并验证：

- 当前实例的SSH host-key SHA-256、GPU UUID和端点摘要；任一漂移即授权失效；
- 仅固定8210项，传前/传后逐文件SHA-256和覆盖一致；不得补传额外1732项或任何未冻结资产；
- SFTP、远端目录`0700`、文件`0600`，禁Git、对象存储、快照、镜像、公开链接和第三方转交；
- 训练输出回传边界、敏感内容最小化、任务后删除及删除核验；
- `UNKNOWN_PLATFORM_CONTROL_PLANE`残余风险和用户知情接受；
- 任一权利方否认、8210 hash/覆盖漂移或实例绑定漂移立即触发`ASSET_INVALIDATED_DO_NOT_REPORT`并停止。

旧合同SHA-256=`5dbf891d1fcd6307ee19f98dc46c8e3f7c35a712c167a5b258c4c10b79d28d3c`继续作为NO_TRANSFER历史证据，不得原地改写为执行许可。任务20应新建独立探索合同；00只在逐条复核并记录其精确hash后，才可把`EFFECTIVE_I3D_TRANSFER_PERMISSION`改为`APPROVED_FOR_BOUND_EXPLORATORY_CONTRACT`。

## 不变边界

- `G3=PASS_WITH_LIMITATIONS`不变；本探索不重开G3。
- temporal-attention仍为`REIMPLEMENTATION_STRONG_BASELINE`。
- 任务50未完成；任务30继续冻结。
- 项目只执行T-AFFC CARM；不得创建IJCV J0—J2、JH1—JH3、任务25或65。
- 任务20不得自行裁定合同通过，不得在合同hash获00接受前上传真实I3D或启动真实全量训练。

## 结论

00原则上允许这次泄漏风险接受型探索运行，也原则上恢复其当前实例专用的8210项临时传输资格；但执行许可尚未生效。下一步仅由任务20起草一份新的、独立的、实例绑定且明确`NON_T0`与`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`的探索合同，交00做精确hash复核。复核前保持0项上传。
