# 00对任务20 VC-CSA探索实例绑定失败止损的验收

> 日期：2026-07-18  
> 决策号：`SC-20260718-06`  
> 审查提交：`5ddb1f655539c44c60d503d7aa8fbb7b04c0a20d`  
> 父状态：`2d5e182ff790595654f150245c97227d0171af99`

## 裁定

`TASK20_INSTANCE_BINDING_FAILURE_SUBMISSION=ACCEPTED`

`INSTANCE_BINDING=FAILED_NOT_BOUND`

`EXECUTION_ATTEMPT=STOPPED_PRE_ASSET_OPERATION`

`EFFECTIVE_I3D_TRANSFER_PERMISSION=SUSPENDED_INSTANCE_BINDING_FAILED_DO_NOT_TRANSFER`

`REMOTE_RESTRICTED_ASSET_RESIDUE=NONE_CREATED`

任务20按已接受合同首先执行实例绑定，并在SSH密钥交换前连接被拒、无法取得host-key与GPU UUID后立即停止。该行为符合合同的fail-closed顺序。没有完成三元绑定，因此当前不得执行传前fixity、SFTP、远端fixity或seed=3407诊断。

## 独立验收

- `HEAD=origin/main=5ddb1f655539c44c60d503d7aa8fbb7b04c0a20d`，工作区clean，任务20线程idle。
- 审查提交相对父状态仅向`WORK_LOG.md`追加WR-20260718-036，共48行；未修改合同、代码、测试、总纲、G门或受限资产。
- 记录显示首次`ssh-keyscan`为空；最小握手在认证前返回`kex_exchange_identification: write: Connection refused`及banner exchange connection refused，`Test-NetConnection`同时为False。
- SSH host-key SHA-256和GPU UUID均未取得，故三元绑定不是部分成功，而是`FAILED_NOT_BOUND`。
- 任务20未创建远端受限根目录，真实I3D上传0项、真实训练0次；本地8210传前fixity、SFTP和远端fixity均未开始。
- `git diff --check 2d5e182..5ddb1f6`：exit 0。

00未获得或保存实例秘密端点、凭证、用户标识或远端路径，因此不自行重试网络连接。任务20的失败报告足以证明其在资产操作前停止，但不能证明平台整体故障原因。

## 授权状态

合同SHA-256=`77b0a93003d265aae6215caca3ef53fbef4624bd24cf3dfabf46df3978cdaed4`及其00验收继续有效；暂停的是当前执行许可，不是合同字节验收。

- 若用户恢复同一指定实例和同一endpoint，任务20可从`ssh-keyscan`与三元绑定重新开始；在三元绑定完整通过前，传输权限继续暂停。
- 若endpoint、实例、GPU或host-key指向新的实例/身份，旧批准不得迁移；必须重新向00提交实例绑定授权请求。
- 不允许通过跳过host-key、只验证TCP、预先上传少量I3D、先做远端目录或使用不受合同约束的传输渠道来“测试可用性”。

只有同一实例三元绑定成功并按合同记录后，`EFFECTIVE_I3D_TRANSFER_PERMISSION`才可恢复为`APPROVED_FOR_BOUND_EXPLORATORY_CONTRACT`并继续传前8210 fixity。

## 资产与结果边界

由于远端受限根目录从未创建、真实I3D上传为0，不存在合同要求的远端资产删除对象；不得把“无需删除”写成“已完成远端删除核验”。本次也不产生实验指标、模型权重、预测或可报告结果。

实验身份仍为`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`，`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`。I3D许可、官方revision、权利方包身份/fixity继续UNKNOWN，`ASSET_INVALIDATED_DO_NOT_REPORT`止损条件不变。

`G3=PASS_WITH_LIMITATIONS`、任务50未完成、任务30冻结及T-AFFC CARM单路线均不变。
