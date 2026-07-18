# 00对租用A6000临时暂存I3D的实例限定风险批准与执行阻断

> 决策编号：`SC-20260718-03`  
> 日期：2026-07-18  
> 父裁定：`SC-20260718-02`  
> 审查锚点：`main@5d831b42374e73e86f765b3216cf0fcfb1ad83a8`

## 最终裁定

- `REMOTE_INSTANCE_RISK_AUTHORIZATION=APPROVED_FOR_THIS_INSTANCE_ONLY`
- `AUTHOR_ORIGINAL_FULL_REPRODUCTION=LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`
- `EFFECTIVE_I3D_TRANSFER_PERMISSION=BLOCKED_DO_NOT_TRANSFER`

用户已明确书面扩权：仅将固定manifest中的8210项I3D临时上传至其私人租用实例，仅用于内部研究训练，任务完成后删除，不发布或转交第三方。该范围与任务20提交审查的`TASK20_REMOTE_A6000_I3D_STAGING_EXECUTION_CONTRACT_20260718.md`一致。

00最终复核合同的精确审查字节：

- 合同版本：`task20-remote-a6000-i3d-staging-v1`
- SHA-256：`5dbf891d1fcd6307ee19f98dc46c8e3f7c35a712c167a5b258c4c10b79d28d3c`
- 审查时行数：120
- 审查时状态：`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY_NO_TRANSFER`
- 前一版审查hash `82aa89cdc3c6f98bd2896c8b5524dc87beca6d31c25857dbc8b1149eee015752`已由本版取代，不具执行效力。

本批准将`SC-20260718-02`中的“用户是否接受本实例残余风险”缺口闭合，但不激活实际传输许可。00在传输前独立复算发现作者原split与peer采样存在不可兼得的泄漏/可执行性冲突，合同第5节的强制止损已经触发。任何新实例、新端点或实例身份漂移仍必须重新申请，不得复用本批准。

## 高优先级执行阻断

作者loader对每条comment从同video随机选择另一comment，并循环拒绝当前comment。00使用任务20提供的只读聚合器对作者固定split独立复算：

- 固定split：train 75,086、dev 10,727、test 21,454条comment；
- 跨split视频：7,854个；
- split内singleton video/ID：train 122、dev 2,750、test 1,573；这些singleton全部只有跨split全局peer，`no_global_peer_ids=0`；
- 聚合器状态：`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`。

如果按split物理过滤`video_to_comment`和annotations，train的122条singleton必然无法取得“另一comment”，原loader会在拒绝自身的循环中无法结束；dev/test同样存在大量singleton。如果保留作者全量映射以保证peer可取，由于7,854个video跨split，train会读取dev/test的评论、标签或其派生输入，违反合同的物理隔离和无泄漏要求。

因此，faithful作者原实现、作者固定comment split、每条样本必须同video取另一comment、以及train/dev/test物理隔离四者无法同时成立。该问题在真实I3D传输前已被发现；依据数据最小化原则，没有必要也不允许先上传8210项再验证。

## 批准依据

合同已充分覆盖：

1. 只允许`csmv-i3d-quarantine-v1.manifest.json`固定8210项，禁止额外1732项、junction、本机路径和其他受限资产。
2. 上传前/后按相对路径、字节数和SHA-256严格集合比较；missing/extra/size/hash任一漂移均fail closed并触发删除与`ASSET_INVALIDATED_DO_NOT_REPORT`。
3. 仅SSH/SFTP，临时根目录`0700`、文件`0600`；禁止Git、对象存储、网盘、镜像、快照、模板和公开服务。
4. 明确保留`UNKNOWN_PLATFORM_CONTROL_PLANE`，用户接受该残余操作风险；没有把它写成绝对删除证明或权利方许可。
5. train/dev阶段物理排除test；dev checkpoint选择冻结后才可建立独立test runtime；跨split peer依赖必须`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`。
6. I3D输入暂存不自动授权回传权重、checkpoint、逐样本预测、评论、标签字典或完整run bundle；只允许最小聚合审计证据。
7. 删除范围、删除触发器和本实例可观察删除核验完整；平台底层备份/物理擦除继续标UNKNOWN。
8. 实验身份持续为`AUTHOR_ORIGINAL_SETTING_NON_T0`，不得进入T0统一主表、冒充官方main或T0复现。

## 传输前强制门

以下门原本构成本实例传输合同，但第0门已经失败，因此本实验不得传输第一个真实I3D字节：

0. **作者peer物理隔离门**：失败，状态`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`。
1. **合同固化门**：任务20可提交合同与peer聚合证据用于审计，但提交不激活传输。
2. **实例唯一绑定门**：若未来另行批准REIMPLEMENTATION，须记录SSH host-key指纹、GPU UUID和租用端点的实例绑定摘要；当前无需连接远端补证。
3. **访问与快照门**：若未来另行批准，仍须`umask 077`、0700/0600并禁主动快照、镜像、模板和公开服务。
4. **本地集合门**、**传后fixity门**和**真实smoke门**：当前均不得执行，因为第0门已失败。

## 执行与报告边界

- 当前不得上传I3D、运行真实smoke或启动全量train/dev/test；A6000可保留公开环境和合成资源证据。
- 删除singleton、跨split取peer、允许self-peer、固定替代peer、取消peer损失或改为视频级split都会改变作者数据/模型合同，只能另建并明确标为`REIMPLEMENTATION_NON_FAITHFUL_PEER_ADAPTATION`；须重新预注册、重新审查资产传输与claim边界。
- 本批准只覆盖该实例上的临时受控处理，不是公开发布、第三方转交、权利方许可、官方revision确认、权利方包身份/fixity确认或一般性再分发权。
- `ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`、`G3=PASS_WITH_LIMITATIONS`和任务50未完成均不变。
- 实验完成、停止租用或任一止损触发后，必须执行合同第8节删除核验，并向00回交最小审计摘要。

## 对任务20的即时指令

1. 提交精确合同、peer聚合器/测试和只含聚合计数的阻断证据；不要改写00文件。
2. 保持真实I3D上传数为0，不连接远端执行资产操作，不启动真实smoke或全量训练。
3. 若用户希望继续，另行提出明确标为`REIMPLEMENTATION_NON_FAITHFUL_PEER_ADAPTATION`的最小方案；在00独立审批前不得复用本实例风险批准来传输资产。
