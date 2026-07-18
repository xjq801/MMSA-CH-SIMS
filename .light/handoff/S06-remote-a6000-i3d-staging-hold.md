---
session_no: S06
contract_version: 2
suggested_title: "[T-AFFC] S07 监督任务20远端资产边界与任务树"
parent_session: S05
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-18
---

# S06 租用A6000与I3D远端暂存边界交接卡

## 当前状态

- 主仓库审查锚点：`main@8a5d8a38684cb0a07ee9a76d56fcf6d01d6ac33b`。
- `G1=PASS`；`G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`；`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`；总门`PASS_WITH_ACCEPTED_ASSET_RISK`；`G3=PASS_WITH_LIMITATIONS`。
- 任务20新A6000状态：`REMOTE_A6000_RUNTIME_READY_SYNTHETIC_BATCH16_RESOURCE_SMOKE_PASSED_FULL_REPRODUCTION_NOT_STARTED`。
- 00裁定`SC-20260718-02`：`REMOTE_I3D_STAGING=NOT_COVERED_BY_EXISTING_ACCEPTED_RISK`；`REMOTE_I3D_TRANSFER_AUTHORIZATION=HOLD_FOR_EXPLICIT_SCOPE_EXPANSION`；`asset_redistribution_allowed=false`。
- 合成smoke可接受，只关闭算力/运行时阻塞；固定8210项I3D未上传且不得上传，全量作者复现未启动。
- VC-CSA作者原任务继续为`AUTHOR_ORIGINAL_SETTING_NON_T0`；任何T0适配只能是独立`REIMPLEMENTATION`。
- I3D许可、官方revision、权利方包身份/fixity仍未知；权利否认或8210 hash/覆盖漂移立即`ASSET_INVALIDATED_DO_NOT_REPORT`。

## 总控自检（TOTAL_CONTROL_HANDOFF第13节）

1. G2能放行是因为协议、lineage、split、隔离、I3D本地fixity/schema/8210覆盖已经通过且用户接受资产证明延期风险；许可、稳定官方revision和权利方包身份/fixity仍UNKNOWN，所以不能称许可闭合。
2. CSMV内部`video_file_id`与平台URL ID属于不同命名空间，不要求字面相等；8210内部项已100%映射到8008个正式source-family，202个重复族跨split归零，正式split为5698/837/1675。
3. LAI-GAI唯一正式版本为`LAI-GAI@v05-2026-03-11`，按source/prompt/exact/dHash形成379组，split 594/127/126，canonical SHA-256为`ad58c268e34adf02bd8e639338069d34576e1d9602f819a2cc6fa89be6836818`；prompt/生成目标/模型标签只是provenance，不是人工诱发情绪真值。
4. 迁移时任务20真正阻塞是独立环境faiss缺失，`blocking_checks=[]`只表示准备检查没有仓库级硬失败，不等于`formal_model_work_ready=true`；该环境阻塞后来已在`.venv-task20`闭合。当前作者全量复现的新阻塞是远端I3D资产传输未获扩权，而不是A6000算力。
5. 总纲要求G3通过、`evaluation-kit-v1`冻结、content-only强基线和teacher-only上界定义明确后才能创建任务30。G3现已通过，但本会话没有用户创建新任务授权，也不因A6000预检自动创建任务30。
6. IJCV路线已迁至`D:\MMSA-CH-SIMS - IJCV方向`，当前仓库从总纲v1.15起只执行T-AFFC CARM；不得创建J0—J2、JH1—JH3、任务25或65，也不得并发争用同一实验核心。

## 监督边界

1. 未获用户对本次租用实例的明确知情扩权前，不得传输真实I3D；总控也不得自行把既有本地风险接受扩大为第三方平台暂存。
2. 若用户扩权，先由任务20提交最小资产、hash/覆盖、访问控制、禁快照/备份、删除核验和输出留存合同，00复核后才能执行。
3. 用户扩权不等于权利方许可，不能把UNKNOWN改为PASS，也不能取消止损条件。
4. 不修改总纲/G门、冻结评测核心或任务20证据快照；任务50五种子/bootstrap仍未完成。
5. `light-consistency`因缺`_shared/findings_schema`仍只有PARTIAL回扫，不冒充完整一致性门。

## 接续提示词

你是新的“00-T-AFFC总控”，接替S06。先读取`AGENTS.md`、`WORK_RECORD_POLICY.md`、`WORK_LOG.md`末条、总纲v1.16、`TASK00_REMOTE_A6000_I3D_STAGING_DECISION_20260718.md`、`TASK00_G3_FINAL_REVIEW_20260718.md`、`TASK00_TASK20_VCCSA_SUPPLEMENT_REVIEW_20260718.md`和本卡，并刷新`origin/main`与任务20实时状态。当前A6000冻结环境和合成batch=16资源smoke已通过，但`REMOTE_I3D_STAGING=NOT_COVERED_BY_EXISTING_ACCEPTED_RISK`、真实I3D传输HOLD、`asset_redistribution_allowed=false`；未获用户对该租用实例的明确知情扩权前不得上传固定8210项或启动全量作者复现。继续传播G3=PASS_WITH_LIMITATIONS、作者任务NON_T0、I3D许可/revision/权利方fixity未知和`ASSET_INVALIDATED_DO_NOT_REPORT`止损条件。项目只执行T-AFFC CARM，不得创建IJCV任务。每次会话收尾继续新建下一张`.light/handoff/S<NN>-*.md`并打印接续提示词。
