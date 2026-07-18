---
session_no: S11
contract_version: 2
suggested_title: "[T-AFFC] S12 等待并监督同一实例恢复绑定"
parent_session: S10
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-18
---

# S11 VC-CSA探索实例绑定失败止损验收交接卡

## 当前状态

- 任务20失败提交`5ddb1f655539c44c60d503d7aa8fbb7b04c0a20d`已由00验收。
- `INSTANCE_BINDING=FAILED_NOT_BOUND`：SSH在密钥交换/认证前拒绝连接，未取得host-key SHA-256或GPU UUID。
- `EXECUTION_ATTEMPT=STOPPED_PRE_ASSET_OPERATION`。
- `EFFECTIVE_I3D_TRANSFER_PERMISSION=SUSPENDED_INSTANCE_BINDING_FAILED_DO_NOT_TRANSFER`。
- 真实I3D上传0项、真实训练0次、远端受限根目录未创建；本地传前fixity、SFTP、远端fixity均未开始。
- 无远端资产需要删除，但这不等于完成了删除核验。
- 合同SHA-256=`77b0a93003d265aae6215caca3ef53fbef4624bd24cf3dfabf46df3978cdaed4`及00验收继续有效；暂停的是执行许可。
- 用户恢复同一实例和endpoint后，任务20可重新从host-key扫描和三元绑定开始；换实例必须重新申请00授权。
- 实验身份继续为`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`，正式证据资格INELIGIBLE。
- G3限制、任务50未完成、任务30冻结、I3D UNKNOWN项与资产止损均不变。

## 监督边界

1. 当前保持任务20 idle，不主动重复失败的SSH探针，不上传、不训练。
2. 用户确认同一实例恢复后，先刷新endpoint身份并完整取得host-key、GPU UUID、endpoint digest；三项未齐不得继续。
3. 若任何身份字段显示新实例或漂移，先暂停并重新申请00授权。
4. 不允许用少量I3D上传、创建远端目录或跳过host-key作为连通性探针。
5. 不创建任务30或IJCV任务，不并发修改任务20实验核心。

## 接续提示词

你是新的“00-T-AFFC总控”，接替S11。先读取`AGENTS.md`、`WORK_RECORD_POLICY.md`、`WORK_LOG.md`末条、总纲v1.16、`TASK00_VCCSA_INSTANCE_BINDING_FAILURE_ACCEPTANCE_20260718.md`、探索合同hash验收单、任务20探索合同、`.light/decision_log.md`和本卡，并刷新`origin/main`与任务20实时状态。当前`INSTANCE_BINDING=FAILED_NOT_BOUND`，`EFFECTIVE_I3D_TRANSFER_PERMISSION=SUSPENDED_INSTANCE_BINDING_FAILED_DO_NOT_TRANSFER`；真实I3D 0上传、训练0次、远端受限目录未创建。合同hash `77b0a930...daed4`仍有效，但同一实例恢复并完成host-key/GPU UUID/endpoint digest三元绑定前不得传输。换实例必须重新申请00授权。不要无新mitigation重复SSH失败；等待用户或平台状态变化。实验永久NON_T0、正式证据资格INELIGIBLE，不得进入T0/G3/统一baseline/任务50/论文claim。继续传播I3D许可/revision/权利方身份/fixity UNKNOWN和资产止损。项目只执行T-AFFC CARM，不创建IJCV J0—J2、JH1—JH3、任务25或65，不得创建任务30。每次会话收尾继续新建下一张`.light/handoff/S<NN>-*.md`并打印接续提示词。
