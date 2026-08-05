# Task40创建与总控04迁移记录

> 版本：v1.0  
> 日期：2026-08-05（Asia/Shanghai）  
> 创建起点：`origin/main@51686ee5fe1f46b13745820840666ac3ccb3d853`  
> 上位授权：`AUTH-00-TASK40-CNBR-DEVELOPMENT-20260805`  
> 状态：`TASK40_CREATED_DEVELOPMENT_ONLY_AND_TOTAL_CONTROL_04_CREATED_WAITING_FINAL_ANCHOR`

## 1. 创建结果

| 角色 | Codex任务ID | 环境 | 当前状态 |
|---|---|---|---|
| Task40可信净收益反应记忆与三源可靠性 | `019fd19c-abf3-7bf0-8530-759e38c3a6ab` | 独立Codex worktree | 已创建；收到`TASK40_CREATION_FINAL_ANCHOR`前只读 |
| 00-T-AFFC总控04 | `019fd19d-b8ef-71f2-82b3-433168211358` | 独立Codex worktree | 已创建；收到`TOTAL_CONTROL_04_FINAL_ANCHOR`前只读 |

总控03为移交方：`019fbdab-9037-7320-9fda-9000c58a5c4b`。两个新任务均从上述同一main锚点创建；本记录提交推送后，由总控03分别发送最终锚点。

## 2. Task40边界

- 只执行`train/DEV_SELECT/DEV_CALIBRATE`开发证据；formal test不得materialize，test access event必须为0。
- 串行门固定为P0泄漏→P1自然错位→P2 Oracle→P3 point router→P4 credible router→P5三源/区域；Oracle无稳定headroom即关闭且不训练router。
- 逐项核对创建授权的9个SHA-256；任一漂移须停止并请求00版本化amendment。
- 不恢复Task30 teacher/KD，不创建Task50，不修改G1—G3、Task20或资产风险；不得直接合入main，必须回交总控04独立审核。

## 3. 总控04边界

- 维护总纲、passport/Registry、decision/risk/claim/论文SSOT与交接链；刷新任务实时状态，交接卡不作为当前事实。
- 独立审核Task40的commit/ref、泄漏门、预算公平、失败证据、hash和claim强度；不得代跑Task40或与其并发修改实验核心。
- Task40未通过开发门不得创建Task50；formal test仍只属于未来Task50。
- 继续监督Task20的最小补证边界与2026-08-31 23:59:59 +08:00受限存储删除验收。

## 4. 不变科学锚点

G1=`PASS`；G2_PROTOCOL_DATA=`PASS_WITH_LIMITATIONS`；ASSET_ADMISSIBILITY=`DEFERRED_ACCEPTED_RISK`；总G2=`PASS_WITH_ACCEPTED_ASSET_RISK`；formal_split=true；G3=`PASS_WITH_LIMITATIONS`。I3D许可/revision/权利方包身份/fixity仍UNKNOWN。Task20 Attempt2永久NON_T0/INELIGIBLE且补证未验收。Task30=`CLOSED_NOT_PASSED`。论文仍为`MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS`，C1—C3仍`TO_VERIFY`。

## 5. 交接协议

总控04必须先读取`.light/handoff/S41-total-control-04-migration.md`及其必读链并刷新Git/任务实时状态。总控03在本迁移提交推送后停止后续SSOT写入；Task40只与总控04进行后续审核回交。
