# Task20受限存储生命周期收尾合同

> 日期：2026-08-01
> 状态：`REQUEST_00_ACCEPT_ACTIVE_TIME_BOUND_RETENTION`
> 依据：`TASK00_VCCSA_RESTRICTED_STORAGE_AND_IMAGE_SUPPLEMENT_AUTHORIZATION_20260719.md`与`TASK00_TASK20_STORAGE_SUPPLEMENT_EXECUTION_ACCEPTANCE_20260719.md`

## 1. 当前受控对象

| 对象类别 | 当前事实 | 保留/删除规则 |
|---|---|---|
| 固定8210项I3D私有MatBox备份 | 00已接受Task20报告的私有目标绑定与fixity；不进入Git | 最小证据获00接受后保留30个日历日，期满执行可见层删除 |
| final-run-bundle | 私有；363个文件，目录0700、文件0600；不含I3D/评论/标签正文 | 含预测和运行证据，按受限运行材料执行同一30日规则 |
| 最终checkpoint与Epoch 116 best | 私有；hash与size已登记 | 按受限运行材料执行同一30日规则 |
| 平台个人环境`.snap` | 私有工件曾可见；跨实例控制面复用未独立验收 | 可能含运行runtime，按受限材料执行30日规则 |
| 非敏感配置镜像 | 已接受；不得含I3D、评论/标签、凭据或端点 | 经内容边界保持合规时可保留至项目归档 |
| Git中的Word、PNG、合同和hash-only manifest | 不含可逆受限资产或凭据 | 可按项目版本史保留 |

## 2. 目标与fixity锚

- 私有MatBox目标摘要：`2c9b6bedc811c90ecfd230d1fd03d7b236e29d9a9b49f38be7c8415f50ca9e58`；
- I3D对象数：8210；总字节：2,283,804,928；
- I3D content-tree SHA-256：`592eb698694388f3ab169c924f88e470daa64d5b496ff007cec390f7d1ada925`；
- 差异：`missing=[]`、`extra=[]`、`size_mismatch=[]`、`sha256_mismatch=[]`；
- ACL摘要：目录0700、文件0600、owner-only；静态加密与平台控制面为`UNKNOWN_PLATFORM_CONTROL_PLANE`。

以上是既有Task20报告并由00按文件证据接受的摘要，不代表00直接访问了私有MatBox。

## 3. 保留时钟

S13规定保留期从“`seed=3407`最小证据获验收”后开始。截至2026-08-01，120轮完成与最终包尚无新的00独立验收，因此：

- `RETENTION_START=D0_PENDING_00_ACCEPTANCE`；
- `RETENTION_DEADLINE=D0_PLUS_30_CALENDAR_DAYS`；
- `CURRENT_LIFECYCLE=ACTIVE_PRIVATE_RETENTION_PENDING_00_CLOCK_START`。

若00在2026-08-01接受，则建议将可见层删除截止日登记为2026-08-31 23:59:59 +08:00；若验收日晚于2026-08-01，按实际`D0+30`顺延。用户若要延长，必须在截止日前书面记录新的期限。

## 4. 到期删除范围与核验

到期删除范围：8210项I3D私有备份、受限runtime/卷快照、含受限运行材料的`.snap`、评论/标签运行副本、checkpoint、权重、逐样本预测、缓存、失败中间文件和final-run-bundle。不得删除Git中的非敏感合同、聚合hash、Word、PNG或工作记录。

删除批次必须记录：

1. 非秘密目标摘要、删除对象类别和删除前对象计数；
2. 删除命令类别、时间和exit code；
3. 删除后可见层对象计数、进程数、残留临时文件数；
4. 不得声称平台不可见备份或物理擦除已验证，继续保留`UNKNOWN_PLATFORM_CONTROL_PLANE`。

当前保留期尚未启动且用户要求保存最终证据，本文件不提前执行不可恢复删除。

## 5. 异常止损

用户撤回授权、权利方否认、公共可达性出现、ACL漂移，或8210覆盖/hash/fixity漂移时，不等待保留期结束：停止进一步复制，删除操作者可见层副本，并标记`ASSET_INVALIDATED_DO_NOT_REPORT`。

## 6. 生命周期闭环定义

00可在接受最小证据并登记`D0`后，将Task20运行态标为`CLOSED_ACTIVE_TIME_BOUND_RETENTION`。该状态表示训练和资产复制已停止、对象范围及期限已冻结、未来删除动作已具备可审计合同；不表示30日已届满或可见层删除已经执行。到期删除仍须形成单独验收记录。
