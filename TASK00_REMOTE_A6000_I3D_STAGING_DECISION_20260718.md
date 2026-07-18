# 00对租用A6000暂存I3D的边界裁定

> 决策编号：`SC-20260718-02`  
> 日期：2026-07-18  
> 审查锚点：`main@8a5d8a38684cb0a07ee9a76d56fcf6d01d6ac33b`

## 裁定

- `REMOTE_A6000_RUNTIME=READY_FOR_SYNTHETIC_RESOURCE_VALIDATION`
- `REMOTE_I3D_STAGING=NOT_COVERED_BY_EXISTING_ACCEPTED_RISK`
- `REMOTE_I3D_TRANSFER_AUTHORIZATION=HOLD_FOR_EXPLICIT_SCOPE_EXPANSION`
- `asset_redistribution_allowed=false`

任务20提交的A6000硬件、冻结环境和合成batch=16资源smoke证据可以接受；它关闭的是算力与运行时阻塞，不是资产传输门。现有`SC-20260717-01`只授权任务20使用`csmv-i3d-quarantine-v1.manifest.json`固定的**本地**I3D字节开展内部研究，并明确该风险接受“不产生I3D再分发权”。租用GPU由第三方平台控制，向其实例复制I3D会形成新的外部传输与暂存边界，即使实例私有、仅用于内部实验，也不能自动等同于既有本地隔离区。

因此，任务20当前不得上传固定8210项I3D，不得以用户租用算力、平台私有实例、合成smoke通过或`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`推导出上传权。任务20可以继续保留已完成的公开代码、公开模型、冻结环境与合成输入预检，但全量作者原设定复现保持`FULL_REPRODUCTION_NOT_STARTED`。

## 证据与边界

1. `TASK00_G2_RISK_ACCEPTANCE_AND_TASK20_AUTHORIZATION_20260717.md`把允许输入限定为固定的本地I3D字节，并明确`formal_split=true`不产生再分发权。
2. `DATA_RELEASE_BOUNDARY.md`规定I3D `.npy`、junction和本机源路径不可进入Git或公开边界；资产风险接受不等于发布或转移授权。
3. `TASK00_G3_FINAL_REVIEW_20260718.md`继续禁止提交、发布或再分发I3D及可逆受限工件；I3D许可、官方revision、权利方包身份/fixity仍未知。
4. `main@8a5d8a3`只证明RTX A6000、冻结运行时、公开RoBERTa和合成180×1024视觉序列可执行batch=16，不证明真实I3D可被合法复制至该平台。

本裁定不否认租用实例可作为计算资源，也不把私有暂存等同于公开发布；它只确认“现有授权没有覆盖这次新跨边界复制”。用户对租用GPU的使用授权不能替代I3D权利方许可，也不能被写成许可已闭合。

## 若用户决定单独扩权

必须取得面向本次租用实例的明确、知情、书面范围决定后，任务20才能提交新的执行合同供00复核。该合同至少应冻结：

- 仅固定8210项I3D，源manifest、文件数、逐文件SHA-256与覆盖必须在上传前后完全一致；任何漂移立即`ASSET_INVALIDATED_DO_NOT_REPORT`。
- 私有、认证、非共享的临时目录；禁止Git、公开对象存储、镜像、快照和平台模板；不得上传junction、本机源路径或超出合同的评论/用户标识。
- 传输加密、最小访问主体、运行期间容量/进程监控、实验结束后的远端删除与删除核验。
- 真实batch=16 smoke只读train/dev；通过后才能按冻结作者原设定启动全量train/dev。test仍只能在dev checkpoint选择冻结后按预注册规则评测。
- 权重、预测、checkpoint和run bundle的远端留存/回传需单列边界；不能由I3D输入暂存授权自动推出。
- 实验始终标为`AUTHOR_ORIGINAL_SETTING_NON_T0`；不得进入T0统一主表或冒充官方main/T0复现。

即使用户接受上述操作风险，状态也只能是“用户允许在未知资产许可条件下进行受控远端内部暂存”，不能表述为权利方授权、合法再分发已确认或资产风险已关闭。

## 对任务20的即时指令

1. 保持真实I3D上传为HOLD；不得启动全量作者复现。
2. 保留A6000环境与合成smoke证据，不修改G3、总纲或冻结评测核心。
3. 若用户明确扩权，先回交远端暂存执行合同，由00复核后再进行任何I3D传输。

