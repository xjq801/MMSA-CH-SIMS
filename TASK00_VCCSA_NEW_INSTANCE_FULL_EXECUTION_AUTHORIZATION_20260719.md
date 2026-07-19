# 00对任务20新GPU实例完整探索执行的授权

> 日期：2026-07-19  
> 决策号：`SC-20260719-01`  
> 父状态：`b914edef1c660ac4958ec9535c3f2927f7f71f71`

## 裁定

`USER_PRIORITY=COMPLETE_TASK20_EXPERIMENT`

`TASK20_OPERATIONAL_REQUEST_AUTHORITY=APPROVED_WITHIN_TASK20_EXPLORATORY_SCOPE`

`NEW_INSTANCE_EXECUTION_AUTHORIZATION=APPROVED_FOR_FULL_CONTRACT_SEQUENCE`

`AUTHORIZED_ENDPOINT_DIGEST=4af92a8622db78ce968bdb49b98f06ef26d4151a943c885ad03de5548eb32cdc`

`EFFECTIVE_I3D_TRANSFER_PERMISSION=APPROVED_AFTER_LOCAL_BINDING_WITHOUT_ADDITIONAL_00_ROUNDTRIP`

用户明确要求以跑完实验为核心目标，并授权任务20为完成该探索诊断提出和执行所需操作。00据此取消“新实例三元绑定成功后必须再次等待00”的中间审批门：任务20可在本裁定进入main后连接目标、完成绑定，并在本地确认三元组通过后直接进入原合同的完整执行链。

## 任务20可自主执行的范围

任务20可在不逐项回请00的情况下：

1. 使用用户私下提供的认证材料连接新GPU实例，完成SSH host-key SHA-256、GPU UUID和endpoint digest绑定；
2. 安装或修复完成任务20所需的依赖、环境、兼容脚本、传输与运行工具，并执行必要的CPU/GPU smoke；
3. 对冻结manifest中的8210项I3D执行本地传前fixity、SFTP暂存和远端逐项fixity；
4. 构建作者原协议runtime，执行唯一`seed=3407`探索诊断，处理OOM、中断、依赖或脚本故障并进行有证据的工程重试；
5. 回传最小聚合证据，随后删除远端I3D、runtime、权重、预测、缓存和中间文件并核验；
6. 若当前实例不可用，可租用或切换替代GPU实例并重新完成三元绑定，不需再次等待00，但须为每个实际使用实例记录新的非秘密endpoint digest、host-key SHA-256和GPU UUID。

三元绑定仍是防止把资产送往错误目标的执行前检查，但不再是需要00二次签字的审批点。绑定失败时任务20可以在不上传资产的前提下诊断、修复和重试；更换实例后重新绑定即可继续。

## 仍须保留的最小事实边界

用户的“忽略安全协议”被落实为取消额外审批和授权任务20自主排障，不解释为允许泄露凭据、公开受限资产或伪造实验结论：

- 端点原文、用户名、端口、密码、私钥和认证材料不得写入Git、WORK_LOG、脚本、run bundle或公开回传；
- I3D只限内部研究临时处理，不得公开、转交第三方、提交Git/Git LFS、对象存储、快照或镜像；
- 只允许冻结8210项，不得混入额外1732项；任一hash/覆盖漂移须停止该批资产并重建可信输入；
- 可进行失败后的工程重试，但不得根据dev/test指标选择性调参或重复挑选结果；只允许一个完成的seed=3407结果；
- 失败、OOM、中断、重试、删除不完全和平台控制面UNKNOWN必须如实记录。

任务20不得扩大到任务30、任务50五种子/bootstrap、完整CARM、IJCV任务或正式论文主张；这些不是“跑完本次探索诊断”的必要操作。

## 结果身份

实验身份永久为`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`，`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`。结果不得进入T0、G3主证据、统一baseline正式列、任务50、论文主表、排名、显著性比较或泛化/无泄漏/优越性claim。

I3D许可、官方revision、权利方包身份/fixity继续UNKNOWN；本授权不是权利方许可或再分发授权。权利方否认或冻结8210资产无法恢复fixity时触发`ASSET_INVALIDATED_DO_NOT_REPORT`。

`G3=PASS_WITH_LIMITATIONS`、任务50未完成、任务30冻结及T-AFFC CARM单路线不变。
