# Task20 post-snapshot最终收尾交接

> 日期：2026-08-01
> 所有者：20-M3 基线与统一评测
> 提交给：00-T-AFFC总控独立验收
> 历史快照：`HANDOFF_20.md`及其hash-bound证据保持原字节不变
> 申请状态：`REQUEST_00_TASK20_FINAL_CLOSEOUT_REVIEW`

## 1. 文档优先级与边界

本文件是`HANDOFF_20.md`之后的post-snapshot收尾补充，只更新Task20的后续运行事实、私有证据归档与存储生命周期状态，不改写历史G3包、历史交接或既有裁定。只有00总控独立验收并绑定本文件所在提交后，本文件才能成为Task20最终运行状态的优先补充；Task20不得自行裁定验收通过、修改G门或创建Task30。

正式门保持：

- `G3=PASS_WITH_LIMITATIONS`；
- Task20正式统一基线与评测核心已完成并冻结；
- I3D继续为`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`，许可、官方revision及权利方包身份/fixity仍为`UNKNOWN`；
- VC-CSA探索永久为`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`；
- `FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`，不得进入T0、G3主证据、统一baseline、任务50或论文claim。

## 2. post-snapshot完成事实

唯一`seed=3407`探索运行于2026-07-31完成预注册的120个epoch。训练进程和SwanLab sidecar正常退出，主日志未报告NaN、OOM、Killed、Traceback、No-space或I/O错误；没有新增种子、选择性重跑或额外test声明。

- 训练完成提交：`49c54a5902532f9d6a6f12717cc8acb85305e861`；
- 私有最终证据包提交：`787da347366b9e52401585f25501ced0c86ef8aa`；
- Word归档提交：`a7cf77cbaa03ab922e3281b1f4d58a03ee890e4b`；
- Epoch 4–120数据表与loss曲线提交：`b1217a017a5c563f8a8591ef49b930edde5291bf`。

最终精确checkpoint为mode `0600`、size `1,743,138,427` bytes、SHA-256 `cd16e7412eec8d3a255e5fa5bc46c8bc53b604c2fe5e22ae0600b8c064428978`。冻结best为Epoch 116，权重SHA-256 `e5033f5dd35dcf02ae660a3af4139c4385d08fbdb1bc3958c7af50d4c6189771`。相关数值仅用于识别探索运行及核验证据完整性，不具有正式论文结果资格。

## 3. 最终证据包

私有MatBox `final-run-bundle`包含Epoch 4–120共117组loss、dev performance和dev prediction，以及完整主训练日志、`log_run.txt`、TensorBoard事件、环境清单、非秘密运行参数、输入hash记录、manifest和总`SHA256SUMS`。发布后事实为：

- payload文件：362；总文件：363（含`SHA256SUMS`）；
- payload总字节：401,916,659；
- 目录权限：`0700`；非`0600`文件数：0；
- 362个payload逐文件SHA-256复核通过；
- 最终包不复制I3D、评论正文、标签正文、凭据、端点或候选非best权重。

Git中的非敏感查看材料：

- `deliverables/TASK20_VCCSA_EXPLORATORY_ARCHIVE_SUMMARY_20260731.docx`：131,186 bytes，SHA-256 `73b39428d8c9ff4a50623bdcb9061e847de4668669a19374487c14f6f1417ef4`；
- `deliverables/TASK20_VCCSA_EPOCH_4_120_LOSS_CURVE_20260731.png`：95,180 bytes，SHA-256 `e7e335701794e686fa26d9a69df8740db3947fa6b8c8c9736be94c143678ced1`。

Epoch 1–3原始loss、dev metrics与dev predictions在最终实例和MatBox均不存在，固定为`KNOWN_EVIDENCE_GAP_EPOCH_1_3_NOT_RECOVERABLE_FROM_AVAILABLE_SOURCES`；不得补造、挑选性重跑或把Epoch 3 best冒充精确断点。

## 4. 存储生命周期

生命周期合同见`TASK20_RESTRICTED_STORAGE_LIFECYCLE_CLOSEOUT_20260801.md`。截至本提交：

- 私有MatBox固定8210项I3D备份此前已由00接受为Task20报告证据；count、字节、覆盖和逐文件hash差异均已闭合；
- 私有配置镜像此前已接受；其若不含受限数据、凭据或端点，可保留至项目归档；
- 平台个人环境`.snap`工件曾在亚太2区私有MatBox可见，但控制面跨实例可启动性未获独立验收；按受限runtime处理，不将其写成“镜像复用已验证”；
- GPU实例已由用户释放；当前无训练进程或活动实例可供远端再核；不得把“无实例可连”写成已验证物理删除；
- 依据S13，受限材料的30日保留期从00接受本次最小证据之日开始。00验收前，状态为`RETENTION_CLOCK_PENDING_00_MINIMUM_EVIDENCE_ACCEPTANCE`。

## 5. Task20完成判定

总纲Task20步骤1–18均已完成、按协议登记不适用，或以明确限制闭合。CLIP/SigLIP/VideoMAE、late fusion、多模态cross-attention和E1不因本次探索被追溯扩项；五种子、正式paired bootstrap与论文统计继续属于Task50。

建议00验收后的Task20状态：

`FORMAL_CORE_COMPLETED_G3_PASS_WITH_LIMITATIONS_EXPLORATORY_COMPLETED_TIME_BOUND_PRIVATE_RETENTION`

该状态表示Task20实现、评测与探索运行均已停止，不表示资产许可闭合、正式VC-CSA无泄漏复现完成、论文结果成立或Task30自动获批。

## 6. 请求00独立执行

1. 复核本文件、`data/manifests/task20-vccsa-exploratory-final-closeout-v1.manifest.json`及绑定提交，出具接受、补证或拒绝裁定。
2. 若接受，以验收日`D0`登记30日受限保留截止日并批准`ACTIVE_TIME_BOUND_RETENTION`作为生命周期闭环状态；到期后另行核验可见层删除。
3. 更新`TASK_REGISTRY.md`及`.light`当前状态，移除“跨区断点阻塞/探索未完成”的过时事实；历史交接卡不改写。
4. 仅在Task20收尾与共享评测核心静止均获接受后，独立判断Task30创建门；本文件不创建Task30。

## 7. 必须停止报告的条件

权利方否认，或固定8210项覆盖、字节、hash、manifest发生无法解释的漂移时，立即标记`ASSET_INVALIDATED_DO_NOT_REPORT`并停止报告相关结果。平台控制面备份和物理擦除继续为`UNKNOWN_PLATFORM_CONTROL_PLANE`。
