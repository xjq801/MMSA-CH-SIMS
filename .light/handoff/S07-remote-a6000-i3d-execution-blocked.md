---
session_no: S07
contract_version: 2
suggested_title: "[T-AFFC] S08 监督任务20 peer阻断与替代方案边界"
parent_session: S06
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-18
---

# S07 A6000实例风险扩权与VC-CSA faithful执行阻断交接卡

## 当前状态

- 00父裁定提交：`main@5d831b42374e73e86f765b3216cf0fcfb1ad83a8`。
- 用户已明确接受当前私人租用实例的残余操作风险；`REMOTE_INSTANCE_RISK_AUTHORIZATION=APPROVED_FOR_THIS_INSTANCE_ONLY`。
- 任务20最终合同审查字节SHA-256：`5dbf891d1fcd6307ee19f98dc46c8e3f7c35a712c167a5b258c4c10b79d28d3c`，120行，状态`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY_NO_TRANSFER`。
- 新的高优先级裁定：`AUTHOR_ORIGINAL_FULL_REPRODUCTION=LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`；`EFFECTIVE_I3D_TRANSFER_PERMISSION=BLOCKED_DO_NOT_TRANSFER`。
- 00独立复算：作者固定split为75,086/10,727/21,454 comments；7,854个video跨split；split内singleton为train 122、dev 2,750、test 1,573，且全部只有跨split全局peer、`no_global_peer=0`。
- 严格split内映射使singleton无法取得“另一comment”；保留全量映射会让train读取dev/test peer评论与标签。两者均不满足faithful+无泄漏合同。
- 真实I3D上传仍为0；未执行远端资产连接、真实smoke或全量训练。
- `G3=PASS_WITH_LIMITATIONS`；既有temporal-attention仍为`REIMPLEMENTATION_STRONG_BASELINE`；任务50未完成。
- I3D许可、官方revision、权利方包身份/fixity与平台控制面残余风险仍UNKNOWN。

## 监督边界

1. 当前不得传输8210项I3D。用户实例风险授权不覆盖一个已被数据/泄漏门判定不可执行的faithful实验。
2. 删除singleton、跨split取peer、self-peer、固定/合成peer、取消peer损失或改为视频级split都会改变作者合同，只能另建`REIMPLEMENTATION_NON_FAITHFUL_PEER_ADAPTATION`。
3. 新REIMPLEMENTATION须单独冻结数据处理、estimand、对照、split/peer合同和资产传输范围，并由00重新审批；不得复用本卡作为上传许可。
4. 此阻断不回滚G3，不使既有强基线失效，不授权任务50主结论。
5. 任一权利否认或8210 hash/覆盖漂移继续触发`ASSET_INVALIDATED_DO_NOT_REPORT`。
6. 不修改总纲/G门、冻结评测核心，不创建IJCV任务。

## 接续提示词

你是新的“00-T-AFFC总控”，接替S07。先读取`AGENTS.md`、`WORK_RECORD_POLICY.md`、`WORK_LOG.md`末条、总纲v1.16、`TASK00_REMOTE_A6000_I3D_STAGING_DECISION_20260718.md`、`TASK00_REMOTE_A6000_I3D_STAGING_APPROVAL_20260718.md`、`TASK00_VCCSA_AUTHOR_PEER_ISOLATION_REVIEW_20260718.md`、任务20最终合同（SHA-256 `5dbf891d1fcd6307ee19f98dc46c8e3f7c35a712c167a5b258c4c10b79d28d3c`）/peer审计和本卡，并刷新`origin/main`与任务20实时状态。当前用户已接受当前A6000实例残余风险，但00独立复算确认作者loader的同video peer要求与随机comment split无法同时满足faithful和物理无泄漏：7,854个video跨split，singleton为train 122/dev 2,750/test 1,573，且全部只有跨splitpeer。因此`EFFECTIVE_I3D_TRANSFER_PERMISSION=BLOCKED_DO_NOT_TRANSFER`，真实I3D仍0上传，不得真实smoke或全量训练。若用户提出peer适配，只能另建`REIMPLEMENTATION_NON_FAITHFUL_PEER_ADAPTATION`并重审，不能冒充作者原设定。继续传播G3=PASS_WITH_LIMITATIONS、任务50未完成、I3D许可/revision/权利方fixity UNKNOWN与止损条件。项目只执行T-AFFC CARM，不得创建IJCV任务。每次会话收尾继续新建下一张`.light/handoff/S<NN>-*.md`并打印接续提示词。
