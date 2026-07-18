# 00对任务20 VC-CSA泄漏接受型探索合同的精确hash验收

> 日期：2026-07-18  
> 决策号：`SC-20260718-05`  
> 审查提交：`4ebcb260dfccf357e9cfb9c7a92c9d348a1b28d9`  
> 父状态：`bbccdf0c3078e4f9dc7afcb9abd8fde7ad5c08ac`

## 裁定

`TASK20_EXPLORATORY_CONTRACT=ACCEPTED`

`APPROVED_CONTRACT_SHA256=77b0a93003d265aae6215caca3ef53fbef4624bd24cf3dfabf46df3978cdaed4`

`EFFECTIVE_I3D_TRANSFER_PERMISSION=APPROVED_FOR_BOUND_EXPLORATORY_CONTRACT`

`EXPERIMENT_IDENTITY=AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`

`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`

00接受`TASK20_VCCSA_LEAKAGE_ACCEPTED_EXPLORATORY_EXECUTION_CONTRACT_20260718.md`的当前精确字节版本。任务20现可在该合同范围内执行实例三元绑定、固定8210项传前fixity、SFTP暂存、远端复核、一次`seed=3407`探索诊断和合同规定的删除核验。

该权限仅在全部传前硬门通过时生效；任何合同字节、实例三元组、8210 manifest/hash/覆盖、权限或平台状态漂移均使本批准失效，须停止且不得把结果写成可报告证据。

## 独立复核

- `HEAD=origin/main=4ebcb260dfccf357e9cfb9c7a92c9d348a1b28d9`，工作区clean，任务20线程idle。
- 审查提交相对父状态严格包含三项：新探索合同、对应测试、`WORK_LOG.md`中的WR-033。
- 00用`Get-FileHash -Algorithm SHA256`独立计算合同SHA-256为`77b0a93003d265aae6215caca3ef53fbef4624bd24cf3dfabf46df3978cdaed4`，与任务20回传一致。
- 00用`Get-Content -Encoding utf8`复核当前文件为100个物理行。任务20回传的“48行”不正确；`git show --stat`同样显示合同新增100行。精确hash一致，因此该行数错误不构成字节漂移，但后续材料必须使用100行，不得传播48行。
- 旧`TASK20_REMOTE_A6000_I3D_STAGING_EXECUTION_CONTRACT_20260718.md`相对父状态diff为空。
- `.venv-task20`独立运行`tests.test_vccsa_author_reproduction`：8/8通过；其中新合同测试验证泄漏披露、NON_T0身份、正式证据禁入和不得静默重标T0。
- `git diff --check bbccdf0..4ebcb260`：exit 0。

## 生效范围

批准只覆盖：

1. 用户指定的当前私人租用实例，且必须先冻结SSH host-key SHA-256、GPU UUID和规范化endpoint digest；
2. 冻结manifest中的恰好8210项I3D，传前和传后均须逐项hash/字节数/覆盖一致；
3. 仅一次`single seed=3407`的作者原协议泄漏接受型工程诊断；
4. 合同限定的最小聚合输出、资源日志、退出状态和删除核验。

该批准不覆盖额外1732项、其他实例、实例快照、对象存储、公开链接、第三方转交、更多种子、bootstrap、任务50、T0适配或任何peer改法。三元绑定或fixity任一失败时，不得开始传输或训练。

## 证据与claim边界

本批准不改变以下事实：作者完整映射使train可读取dev/test peer评论与标签，dev/test指标受污染。运行结果永久不得进入T0统一baseline、`BASELINE_TABLE_V1.md`正式列、G3主证据、冻结G3 package、任务50、论文主表或泛化/无泄漏/公平比较/优越性claim，也不得与temporal-attention或其他正式baseline做排名或显著性比较。

I3D许可、官方revision、权利方包身份/fixity仍为UNKNOWN；本验收不是再分发许可或权利方证明。权利方否认、8210 hash/覆盖漂移、实例绑定漂移或删除核验失败立即触发`ASSET_INVALIDATED_DO_NOT_REPORT`。

## 执行要求

任务20可从现在开始按已接受合同执行，但必须按顺序：实例三元绑定通过 → 本地8210传前fixity通过 → SFTP传输 → 远端8210复核通过 → 单种子诊断 → 最小证据回传 → 删除与核验。每个阶段须追加WORK_LOG；失败必须原样记录并停止，不得自行扩大授权。

`G3=PASS_WITH_LIMITATIONS`、任务50未完成、任务30冻结及T-AFFC CARM单路线均不变。
