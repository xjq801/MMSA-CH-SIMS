---
session_no: S34
contract_version: 2
suggested_title: "总控03"
parent_session: S33
project: mmsa-ch-sims-taffc-carm
date: 2026-08-02
source_thread: 019fbdab-9037-7320-9fda-9000c58a5c4b
target_thread: next-total-control-session
---

## 当前阶段

总控03已根据用户选择B形成Task20 Epoch 1—3独立恢复复跑裁定。正式pipeline仍处于M4 Task30 H1开发门；Task20只被临时授权执行一个隔离NON_T0/INELIGIBLE attempt，不重开正式核心。总控不得参与Task30实验核心。

## 已完成（具体产物/commit/决策定位 + 验证摘要）

- `TASK00_TASK20_EPOCH1_3_RECOVERY_RERUN_DECISION_AND_EXECUTION_CONTRACT_20260802.md` v1.0 — 以`origin/main@051faa160e65fb9f1a71b7c41c4e69eafeec87e0`为父状态，验证并冻结唯一attempt ID、配置/代码/环境/输入hash、实例/MatBox绑定、逐step证据和失败保留合同。
- `AUTH-00-TASK20-EPOCH1-3-RECOVERY-20260802` — 用户选择B的授权已落入两套决策日志；验证其永久保持NON_T0/INELIGIBLE，原Epoch 1—3缺口不变，不进入T0/G3/Task50/论文正式claim。
- `TASK_REGISTRY.md` v1.10、`.light/project_card.md`与`.light/version_history.md` — 验证Task20只新增隔离attempt状态，Task30仍是活动正式阶段且H1未裁定。
- 展示合同 — 验证“合并”只指两段曲线/数据按attempt分区并列；Epoch 3/4必须显示独立attempt边界，禁止连续连线、跨界平滑或“完整原1—120轨迹”表述。

## 工作区状态

本批开工锚点为`HEAD=origin/main=051faa160e65fb9f1a71b7c41c4e69eafeec87e0`。用户未跟踪`NEmoP/`、`__MACOSX/`、`tmp/`保持未读取、未移动、未暂存、未删除。总控只修改裁定、SSOT台账、WORK_LOG和本交接卡，不修改Task30或Task20实验核心。实际授权提交为“包含本合同的已推送main commit”，接续时必须重新读取Git现实。

## 待用户回答

- none — 用户已明确选择B；当前只需按冻结合同执行和独立复审，不需要新的方法学选择。

## 下一步（≤3 条，最小动作）

1. read Task20实时状态，确认其从包含2026-08-02合同的main提交启动唯一attempt2，并在任何资产写入前完成非秘密三元绑定与hash preflight。
2. audit Task20回交的逐step loss/LR、Epoch 1—3 dev metrics/predictions/checkpoint、stdout/stderr、失败证据和边界图；只作接受、补证或拒绝，不提升证据等级。
3. verify Task30 H1开发门、Task10论文数据段落和2026-08-31受限存储删除义务仍按各自独立链推进。

## 阻塞/风险

- 最大科研诚信风险是把attempt2的Epoch 1—3静默拼成原attempt1的连续1—120轨迹；数据、图、标题和文字均必须显式编码边界与不可比性。
- 新实例即使同为4090也不等于同一实例或逐bit相同；必须以host-key hash、GPU UUID和endpoint digest绑定，并禁止凭据进入Git/日志。
- I3D许可、官方revision、权利方包身份/fixity仍UNKNOWN且禁止再分发；8210覆盖/hash或权限漂移触发`ASSET_INVALIDATED_DO_NOT_REPORT`。
- 本授权不延长2026-08-31 23:59:59 +08:00可见层删除截止，平台控制面残余继续为UNKNOWN。
- Task30仍在独立worktree执行H1；总控和Task20均不得修改其核心，未过H1不得创建Task40。

## 必读文件（按序）

1. `.light/handoff/S34-task20-epoch1-3-recovery-authorization.md`
2. `TASK00_TASK20_EPOCH1_3_RECOVERY_RERUN_DECISION_AND_EXECUTION_CONTRACT_20260802.md`
3. `.light/passport.yaml`
4. `.light/project_card.md`
5. `TASK_REGISTRY.md`
6. `TASK00_TASK20_FINAL_CLOSEOUT_REVIEW_20260801.md`
7. `HANDOFF_20_POST_SNAPSHOT_CLOSEOUT_20260801.md`
8. `data/manifests/task20-vccsa-exploratory-final-closeout-v1.manifest.json`
9. `HANDOFF_30.md`
10. `WORK_LOG.md`末条与Task20/30实时任务

## 禁止

- 不得把新Epoch 1—3写成原运行恢复、resume或原1—120连续轨迹；不得覆盖历史Epoch 4—120或closeout证据。
- 不得让attempt2进入T0、G3、Task30、Task50、论文SSOT、主表、排名、统计或任何泛化/无泄漏/优越性claim。
- 不得记录或提交endpoint原文、端口、账号、密码、私钥、Cookie、受限I3D、评论/标签正文、预测或checkpoint。
- 不得创建或执行IJCV的J0—J2、JH1—JH3、任务25或65；未过H1不得创建Task40。
- Do not treat this card as current fact; run git status/log first；不得凭记忆继续，必须读取Task20/30实时状态。

## 接续提示词

你是“00-T-AFFC总控03”的接续会话。先读取AGENTS.md与WORK_RECORD_POLICY.md，运行`git fetch origin`、`git status --short --branch`、`git log -3`和`git rev-parse HEAD/origin/main`；再按序读取`.light/handoff/S34-task20-epoch1-3-recovery-authorization.md`、2026-08-02 Task20恢复复跑合同、passport、project card、TASK_REGISTRY、Task20最终closeout、HANDOFF_30及WORK_LOG末条，并刷新Task20/30实时任务。Task20仅可执行`TASK20_VCCSA_EPOCH1_3_RECOVERY_RERUN_SEED3407_ATTEMPT2`：新Epoch 1—3与原Epoch 4—120只可在展示层断开并列，永久NON_T0/INELIGIBLE，原缺口不变，不得进入T0/G3/Task50/论文claim。总控不是Task20或Task30执行代理；未过H1不得创建Task40。每次收尾继续创建下一张S<NN>交接卡并打印接续提示词。
