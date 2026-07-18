# 任务20 VC-CSA 泄漏接受型隔离探索执行合同

> 合同 ID：`task20-vccsa-leakage-accepted-exploratory-v1`  
> 日期：2026-07-18  
> 唯一实验身份：`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`  
> 方法风险：`METHOD_LEAKAGE_RISK=USER_ACCEPTED_FOR_EXPLORATORY_ONLY`  
> 正式证据资格：`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`  
> 当前权限：`EFFECTIVE_I3D_TRANSFER_PERMISSION=PENDING_EXPLORATORY_CONTRACT_HASH_REVIEW`

## 1. 生效门与授权边界

- 本合同是任务20所有权的新合同，不替代、不修改旧 NO_TRANSFER 合同及其固定 SHA-256。
- 00 必须对本文件精确 SHA-256 另行记录 `APPROVED_FOR_BOUND_EXPLORATORY_CONTRACT`，本合同才可用于指定实例的一次性探索。
- 在该书面记录出现前，硬门保持：`真实 I3D 上传=0`、`真实训练=0`；任务20不得自行裁定通过。
- 用户接受的是本次探索的方法学泄漏风险和指定私人租用实例的临时内部研究处理风险，不是 I3D 许可、官方 revision、权利方包身份/fixity 或再分发权的证明。
- 不创建任务30，不修改总纲、G 门、T0 冻结协议或任何历史 hash-bound 快照。

## 2. 方法学泄漏披露

- 作者原始 comment split、完整 `video_to_comment` 映射和原始 peer 采样逻辑必须保持；这一路径是 NON_T0，不得重标为 T0 适配。
- 真实聚合显示 7,854 个视频跨 split；train/dev/test 中只有跨 split peer 的 singleton 数分别为 122 / 2,750 / 1,573。
- 因完整映射与作者 peer 逻辑被保留，train 可读取 dev/test peer 评论与标签；这不是潜在风险，而是本实验明确接受的结构性行为。
- dev/test 指标受到污染，不能估计严格 held-out generalization，不能支持无泄漏、公平比较、泛化、优越性或正式复现 claim。
- 本合同不允许通过删 singleton、self-peer、固定/合成 peer、去除 peer loss、视频级重分 split 或其他适配来改变作者路径；任何此类工作须另建 `REIMPLEMENTATION_NON_FAITHFUL_PEER_ADAPTATION` 并重新预注册、审批。

## 3. 唯一允许的运行

- 仅允许一次 `single seed=3407` 工程诊断；禁止新增种子、重复挑选、bootstrap、显著性检验或任务50统计。
- 冻结作者参数与既有兼容补丁；不得根据 dev/test 结果追加调参、改 split、改 peer 或选择性重跑。
- 允许输出最小聚合诊断、资源日志、退出状态和非敏感环境摘要；失败、OOM、中断、超时或磁盘不足必须原样登记，不得冒充完成。
- 本合同获 00 精确 hash 接受后，仍须先完成实例绑定、资产预检和远端 fixity，全部通过才可启动单种子诊断。

## 4. 正式证据隔离

本次结果永久禁止进入、改写或支撑：

1. T0 统一 baseline、统一 baseline 排名或 `BASELINE_TABLE_V1.md` 正式列；
2. G3 主证据、冻结 G3 package 或 hash-bound `HANDOFF_20.md` 快照；
3. 任务50、多种子统计、bootstrap、显著性比较或正式消融；
4. 论文主表、摘要、结论以及泛化、优越性、公平比较、无泄漏等论文 claim；
5. 与 temporal-attention、legacy baseline 或其他正式模型的排名、显著性或数值优劣比较。

任何材料引用该诊断时，必须同时展示唯一实验身份、泄漏事实和 `FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`。

## 5. 指定实例三元绑定

- 授权不可迁移，只绑定用户本次指定的私人租用实例；凭证和原始 endpoint 不得写入 Git、合同、日志、脚本或结果包。
- 首次资产操作前须记录非凭证三元组：当前 SSH host-key SHA-256、GPU UUID、规范化 endpoint 的 `endpoint digest`。
- 三元组须由本地预检和远端回执双向一致确认，并与 00 接受记录绑定；任一字段缺失、变化或漂移立即失效，禁止上传和训练。
- 平台管理员访问、底层备份、物理擦除和不可见副本仍为 `UNKNOWN_PLATFORM_CONTROL_PLANE`，不得表述为可验证的绝对隔离或物理删除。

## 6. 固定 8210 项资产与 fixity

- 唯一输入 SSOT 为 `data/manifests/csmv-i3d-quarantine-v1.manifest.json` 的固定 8210 项 `.npy`；禁止额外 1732 项、junction、原始媒体、音频、缓存、本机绝对路径或任何其他可逆受限资产。
- 传输前必须逐项核验相对路径、字节数和 SHA-256，得到恰好 8210 项且 `missing=[]`、`extra=[]`、`size_mismatch=[]`、`sha256_mismatch=[]`。
- 传输后须在远端独立重算同一清单并逐项比对；只有覆盖仍为 8210 且四类差异均为空时才可训练。
- tracked 证据只保存计数、集合摘要 hash、manifest hash 和差异计数，不保存 I3D 字节、样本标识、绝对路径或可逆清单。

## 7. 传输、权限与平台限制

- 只允许 SSH/SFTP 加密传输；临时根目录权限固定 `0700`，每个受限文件权限固定 `0600`。
- 禁止公开链接、Jupyter 公网入口、Git/Git LFS、对象存储、网盘、第三方转交、实例快照、备份、镜像、模板或平台持久卷。
- 不得把凭证写入 shell 历史、环境导出、远端脚本、配置、日志或 run bundle；不得回显凭证。
- 任何权限漂移、意外持久化、公共可达性或平台安全门失败均须停止、删除本轮暂存并执行资产止损。

## 8. 输出回传与留存

- 允许回传的最小证据仅限：聚合指标、冻结配置、代码/输入/环境 hash、相对 artifact hash、exit code、起止时间、资源摘要和删除核验结果。
- I3D、评论正文、标签明细、样本预测、样本 ID、模型权重、checkpoint、standardizer、缓存和含本机/远端绝对路径的日志不得进入 Git、公开材料或第三方系统。
- 权重、checkpoint 和逐样本输出仅可在受限临时根目录内保留到诊断核验结束，随后必须与输入资产一并删除；不得以回传结果为由扩大资产授权。

## 9. 删除与核验

- 诊断结束、租用结束、用户撤回授权、合同失效或任一止损条件触发时，立即停止进程并删除：8210 项 I3D、全部 runtime、评论/标签运行副本、checkpoint、权重、逐样本输出、缓存及失败中间文件。
- 删除后须核验：受限根目录不存在、远端搜索命中 I3D 数为 0、相关进程数为 0，并记录删除前后磁盘摘要、删除时间、命令类别和 exit code。
- 删除核验只能证明操作者可见层面的删除；平台控制面仍是 `UNKNOWN_PLATFORM_CONTROL_PLANE`。

## 10. 资产止损与不可报告状态

以下任一情况立即停止上传/训练、终止进程、删除远端暂存，并标记 `ASSET_INVALIDATED_DO_NOT_REPORT`：

- 权利方否认或撤回相关使用；
- 固定 8210 项的 hash、字节数、覆盖或 manifest 漂移；
- SSH host-key SHA-256、GPU UUID 或 endpoint digest 与绑定记录不一致；
- 出现额外/缺失文件、junction、不可解释副本、权限漂移、快照/对象存储/Git 持久化或公共访问；
- 无法完成输出边界、进程终止或删除核验。

止损结果不得用于 T0、G3、统一 baseline、任务50、论文 claim 或正式报告。

## 11. 审批槽与当前事实

- 00 精确合同 SHA-256：`PENDING`
- 00 绑定批准记录：`PENDING`
- 三元绑定摘要：`PENDING_NOT_TRACKED_UNTIL_APPROVAL`
- 传前 8210 fixity：`NOT_RUN`
- 传后 8210 fixity：`NOT_RUN`
- 真实 I3D 上传：0 项
- 真实训练：0 次

因此，本文件提交仅供 00 复核，不构成有效传输许可，也不证明探索已执行或全量复现已完成。
