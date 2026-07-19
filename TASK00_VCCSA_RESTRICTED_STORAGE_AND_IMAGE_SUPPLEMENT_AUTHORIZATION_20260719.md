# 00对VC-CSA受限资产存储与镜像的补充授权/验收

> 日期：2026-07-19  
> 决策号：`SC-20260719-02`  
> 父状态：`main@8f9fae4442ec3b4b74b7ace30bd04ae3d2e9701d`  
> 补充对象：任务20探索合同 `77b0a93003d265aae6215caca3ef53fbef4624bd24cf3dfabf46df3978cdaed4`

## 裁定

`RESTRICTED_STORAGE_SUPPLEMENT=APPROVED_EXECUTABLE`

`USER_ACCEPTED_STORAGE_AND_PLATFORM_CONTROL_PLANE_RISK=true`

`HISTORICAL_CONTRACTS=UNCHANGED`

用户明确授权把任务20受限I3D保存到MatBox私有网盘、私有对象存储或环境快照，并允许保存配置镜像。该授权以本补充文件新增执行范围，不修改、替换或重写旧NO_TRANSFER合同、旧探索合同或其历史hash。对当前正在A30运行的`seed=3407`探索训练，本补充授权立即可执行。

## 存储区域与对象范围

允许的逻辑区域固定为：

| 区域 | 用途 | 允许对象 | 禁止对象 |
|---|---|---|---|
| `matbox-private/task20-vccsa-exploratory-20260719/` | 用户私有网盘备份 | 固定8210项I3D、manifest/fixity报告、最小运行配置 | 原始媒体、额外1732项、公开分享链接、凭据 |
| `object-private/task20-vccsa-exploratory-20260719/` | 用户私有对象存储 | 与MatBox同范围的受限备份及加密归档 | 公共bucket/prefix、Git/Git LFS、匿名下载、第三方复制 |
| `snapshot-private/task20-vccsa-exploratory-20260719-*` | A30环境/卷快照 | 环境、代码、冻结配置及为运行所需的8210 I3D/runtime | 面向公众的模板/镜像市场、含凭据的镜像 |
| `config-mirror/task20-vccsa-exploratory-20260719/` | 配置镜像 | 环境lock、包版本、脚本、非敏感配置、容器/环境定义 | 密钥、Cookie、端点原文、I3D字节、评论正文、标签明细 |

实际MatBox路径、bucket/容器、snapshot ID、账户和endpoint原文只保存在用户与任务20的私有执行上下文；进入Git的仅是每个实际目标的`storage_target_digest`、区域类别、对象计数、聚合hash、权限摘要和时间戳。

## 权限、绑定与fixity

1. 每一个实际存储目标在首次写入前记录：区域类别、私有目标标识的SHA-256、提供方/区域摘要、ACL摘要、加密状态和创建时间；不得记录凭据或原始定位符。
2. ACL必须为用户私有：禁止匿名/公开读写、公开链接、第三方分享和公共镜像市场；允许用户、任务20运行账户及平台控制面不可避免的管理员访问。用户已知并接受`UNKNOWN_PLATFORM_CONTROL_PLANE`。
3. I3D写入只允许固定manifest中的恰好8210项`.npy`。每次上传/快照前后均须核验相对路径、字节数和SHA-256；报告`count=8210`、`missing=[]`、`extra=[]`、`size_mismatch=[]`和`sha256_mismatch=[]`才可称fixity一致。
4. snapshot或对象归档若同时包含作者runtime、评论/标签运行副本、权重、预测或缓存，仍属受限运行材料；不得公开或进入Git，但可在本补充授权的私有区域暂存。
5. 配置镜像仅可包含非敏感配置/环境/代码；任何凭据、端点原文或可逆受限数据命中时不得制作或发布该配置镜像。

任务20已获完整探索执行授权，可自行创建、绑定和使用上述私有区域，无需再等待00逐步签字；每次目标创建、写入、校验、快照、恢复或删除须追加WORK_LOG并保留非秘密摘要。

## 保留、镜像与删除策略

- 受限I3D、完整卷快照、对象归档及运行材料：保留至`seed=3407`探索的最小证据被验收后30个日历日；期满自动删除，除非用户在期满前书面延长。用户撤回授权、权利方否认或fixity无法恢复时立即停止进一步复制，并删除可见层副本。
- 配置镜像：可保留至项目归档，前提是不含受限资产、凭据或端点原文；若含受限内容，按受限材料的30日策略处理。
- 删除需记录对象数/快照数、目标摘要、删除时间、命令类别、exit code和删除后可见层计数。平台控制面备份/快照残余继续标记`UNKNOWN_PLATFORM_CONTROL_PLANE`，不得宣称物理擦除已证实。
- 删除前，任务20可从已核验的私有备份恢复当前A30运行环境；恢复后仍须验证8210范围与hash，不得以恢复为由扩展对象范围。

## 结果与claim边界

本补充只改变存储与镜像边界，不改变实验身份。所有运行、备份、快照或恢复的结果仍是`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`，`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`。不得进入T0、G3主证据、统一baseline、任务50、多种子统计、论文主表、排名或泛化/无泄漏/优越性claim。

I3D许可、官方revision、权利方包身份/fixity仍为UNKNOWN；本补充是用户的内部处理与存储授权，不是权利方许可、公开发布或再分发证明。`G3=PASS_WITH_LIMITATIONS`、任务30冻结、T-AFFC CARM单路线不变。

## 允许的下一步

任务20可立即：为当前A30创建私有存储目标/快照与配置镜像、绑定目标摘要、核验固定8210项、备份当前运行环境和恢复必要材料；同时继续或恢复已启动的`seed=3407`训练。完成后须回传各目标的非秘密绑定/fixity摘要、保留截止日、训练状态及删除计划。不得把这些授权解释为公开分发或正式证据升级。
