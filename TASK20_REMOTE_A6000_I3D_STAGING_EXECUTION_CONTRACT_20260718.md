# 任务20租用A6000临时暂存I3D执行合同

> 合同版本：`task20-remote-a6000-i3d-staging-v1`  
> 日期：2026-07-18  
> 实验身份：`AUTHOR_ORIGINAL_SETTING_NON_T0`  
> 当前状态：`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY_NO_TRANSFER`

## 1. 授权与非授权事实

- 用户已书面授权：把固定manifest中的8210项I3D临时上传到其私人租用实例，仅用于内部研究训练；任务完成后删除；不发布或转交第三方。
- 本授权是用户对未知资产许可风险下的本次受控处理决定，不是I3D权利方许可、官方revision证明、权利方包身份/fixity证明或再分发权确认。
- `ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`、`G3=PASS_WITH_LIMITATIONS`和`ASSET_INVALIDATED_DO_NOT_REPORT`止损条件不变。
- 00书面复核与全部传输前硬门均通过前不得上传真实I3D或启动全量实验；第9节预检现已触发更早的泄漏止损，因此本合同当前不允许传输。

## 2. 唯一允许的输入集合

- 源SSOT：`data/manifests/csmv-i3d-quarantine-v1.manifest.json`。
- 只允许manifest中`required_files`列出的8210个`.npy`；预期总字节数约2.13GiB。
- 每个远端文件必须由manifest相对路径、字节数和SHA-256三元组识别；上传前后集合必须严格相等。
- 禁止上传额外1732项、junction、目录绝对路径、本机源路径、缓存、原始媒体、音频、模型权重、既有预测或其他可逆受限资产。
- 任一缺失、额外文件、字节数不等、SHA-256不等或8210覆盖漂移立即停止，删除本轮远端暂存并标记`ASSET_INVALIDATED_DO_NOT_REPORT`；不得启动训练或报告结果。

## 3. 传输与访问控制

- 仅使用SSH/SFTP加密通道；不使用公开URL、对象存储、Git、Git LFS、网盘、镜像、快照或平台模板。
- 远端目录必须新建为认证后可访问的临时目录，权限固定为`0700`；文件权限固定为`0600`。
- 最小访问主体为当前租用实例的单一实验账户。不得创建共享账户、公开服务、Jupyter公开链接或额外下载入口。
- 操作者不得主动创建实例快照、备份、镜像或模板。平台运维访问、底层备份与物理擦除语义仍为`UNKNOWN_PLATFORM_CONTROL_PLANE`；用户的本次知情授权接受这一残余操作风险，但不得把它表述为绝对删除证明或权利方许可。
- 连接凭证只存在于本次会话内存，不写入仓库、合同、日志、shell历史、远端脚本或run bundle。
- 首次传输前必须用SSH host-key SHA-256指纹、GPU UUID和端点规范化字符串的SHA-256摘要建立一次性实例绑定；tracked证据只保存这些非凭据指纹/摘要，不保存端点或认证值。任一字段缺失、更换或漂移都使本次授权自动失效，必须重新复核，禁止把授权迁移到另一实例。

## 4. 上传门与远端fixity

上传分两步执行：

1. 本地根据manifest生成仅含8210项的传输队列；队列不得输出绝对源路径或评论正文。
2. 远端完成后独立生成相对路径、字节数和SHA-256清单，与本地manifest逐项比较。

只有同时满足以下条件才可进入真实smoke：

- `remote_file_count=8210`；
- `missing=[]`；
- `extra=[]`；
- `size_mismatch=[]`；
- `sha256_mismatch=[]`；
- 远端目录和文件权限符合`0700/0600`；
- GPU、磁盘与冻结环境复检通过。

远端清单本身不得包含本机路径；可回传的审计证据仅限计数、manifest hash、集合hash、错误计数与非敏感环境摘要。

## 5. train/dev与test物理隔离

### 阶段A：train/dev

- 仅允许作者固定train/dev split进入训练runtime；`test_set.json`必须为空。
- runtime annotation与video-to-comment映射必须严格等于阶段A选中ID集合；任何test或未选择ID持久化即fail closed。
- 模型拟合、优化、checkpoint选择和全部选择逻辑只看train/dev；不得实例化test loader。
- 真实batch=16 smoke先运行最小train/dev子集；通过后才能启动全量train/dev。

### 阶段B：冻结后test

- 只有在全量train/dev完成、dev checkpoint选择规则和选中checkpoint hash冻结后，才可新建独立test评测runtime。
- test只做预注册前向与指标计算，不得用于训练、早停、超参数选择、epoch选择或重跑决策。
- 若作者实现必须依赖跨split peer或全量映射，立即停止并登记`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`；不得通过持久化test记录来绕过。

## 6. 运行与容量监控

- 冻结作者fork：`3e8c42608f4e89bc2082c55760aa63535e8e276a`；兼容补丁hash与环境版本沿用任务20审计第10节。
- 冻结主运行参数：seed 3407、batch 16、max epoch 120、learning rate 0.00005、language length 512、video length 180、AMP关闭；不得因test结果修改。
- Python patch版本3.8.20与本地3.8.9差异必须进入manifest；不得宣称跨环境bitwise一致。
- 每个epoch约1.66GiB checkpoint、120轮约199GiB。启动前至少保留220GiB输出与失败缓冲；运行中每个epoch记录磁盘、GPU进程、显存峰值、wall time和exit状态。
- OOM、超时、断连、磁盘不足、进程被抢占或max epoch到达均按真实termination记录，不得冒充完成。

## 7. 输出留存与回传边界

- I3D暂存授权不自动授权回传checkpoint、模型权重、standardizer、逐样本预测、评论正文、标签字典或完整run bundle。
- checkpoint、权重、逐样本预测和含评论/标识的日志只在远端临时目录保留到验证结束，禁止提交、发布、共享或转交。
- 允许回传到本地Git忽略目录的最小证据：聚合指标、配置、代码/输入/环境hash、相对artifact hash、exit code、非敏感stdout/stderr摘要、开始/结束时间和删除核验结果。
- Git只允许提交不含路径、凭证、评论正文、样本标识、I3D字节或可逆受限内容的审计摘要。
- 实验结果始终标为`AUTHOR_ORIGINAL_SETTING_NON_T0`；不得进入T0统一主表，不得冒充官方main复现或T0复现。

## 8. 删除与删除核验

以下任一条件触发删除：实验完成并提取最小允许证据；用户停止租用；授权撤回；hash/覆盖漂移；权利方否认；安全或泄漏门失败。

删除范围包括：8210项I3D、train/dev与test runtime、评论运行副本、checkpoint、权重、逐样本预测、临时缓存和失败中间文件。公开代码、公开依赖和公开RoBERTa可按用户决定保留，但不得含受限runtime引用。

删除后必须执行并回传：

- 受限临时根目录不存在；
- 远端搜索命中I3D文件数为0；
- 运行进程数为0；
- 删除前后磁盘占用摘要；
- 删除时间、命令类别和exit code；
- 明确声明平台控制面的备份/物理擦除仍不可独立证明。

## 9. 上传前作者peer隔离预检（已触发止损）

2026-07-18在本地只读作者评论标注上执行聚合审计；未读取I3D字节，报告不含评论ID、评论正文或本机路径：

- 作者split：train 75,086 / dev 10,727 / test 21,454，跨split重复comment ID为0；
- 7,854个视频跨越两个或三个split；
- split内仅有一条评论的视频/ID：train 122、dev 2,750、test 1,573；这些ID在全量映射中均有peer，但peer全部来自其他split（无全局peer的ID为0）；
- 作者loader对每条样本必须从同视频随机选择另一评论，并读取该peer的评论与标签；
- 因此，若完整保留75,086条train并使用作者全量映射，至少122条train样本必须依赖dev/test peer；若物理过滤为train-only映射，这122条样本没有合法peer，作者循环无法按原合同执行。

裁定：`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`。真实I3D上传数保持0，远端全量实验未启动。不得通过持久化dev/test记录、删除原split样本或静默修改peer采样来冒充作者全量复现。任何改变peer逻辑、去除单例或重构为视频级split的实验都必须另立`REIMPLEMENTATION`合同，并重新申请是否需要远端I3D暂存；本次上传授权不自动扩张到该实验。

## 10. 00复核请求

请00复核用户扩权与本合同边界，并优先确认第9节泄漏止损。即使资产边界本身可作条件批准，当前作者全量复现也不得进入传输；只有另行批准且不冒充faithful reproduction的实验合同，才可重新评估`REMOTE_I3D_TRANSFER_AUTHORIZATION=APPROVED_FOR_THIS_INSTANCE_ONLY`：

1. 用户书面扩权与本合同范围一致；
2. 8210项、hash/覆盖、加密传输、最小访问和禁主动快照边界明确；
3. train/dev与test物理隔离及跨split peer fail-closed明确；
4. 输出回传和删除核验不由输入授权自动扩张；
5. UNKNOWN许可与止损状态保持。
6. SSH host-key、GPU UUID和端点摘要在传输前完成实例唯一绑定且无漂移。

当前`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`未解除前，不执行任何真实I3D传输。
