---
session_no: S04
contract_version: 2
suggested_title: "[T-AFFC] S05 监督G3后续与任务树边界"
parent_session: S03
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-18
---

# S04 G3 VC-CSA证据更正交接卡

## 当前裁定

- `G3=PASS_WITH_LIMITATIONS`，作者实现定位没有改变该门结论。
- VC-CSA当前身份：`AUTHOR_RELEASED_IMPLEMENTATION_LOCATED_PR3_OPEN_NOT_YET_REPRODUCED`。
- `JackySnake/MSA-CRVI@3e8c42608f4e89bc2082c55760aa63535e8e276a`是`IEIT-AGI/MSA-CRVI`的fork，对应上游仍open、未合并的PR #3 `add source code`。
- 上游官方`main@99d1424`在原审计时无代码只作为历史事实，不再写成当前作者代码缺失。
- static compileall通过；两个入口在CUDA前因未声明`en_vectors_web_lg`依赖失败，shell脚本还有变量/续行缺陷；未运行GPU，不能写成复现成功。
- 作者原任务使用目标comment、随机comment split和评论级opinion/emotion输出，与T0禁用目标评论、`group_by_video_v1`视频级分布任务不匹配。
- temporal-attention仍仅为`REIMPLEMENTATION_STRONG_BASELINE`；任务50五种子/bootstrap仍为`TASK50_NOT_COMPLETED`。
- I3D许可、官方revision、权利方包身份/fixity仍未知，`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`不变；权利否认或8210 hash/覆盖漂移即`ASSET_INVALIDATED_DO_NOT_REPORT`。
- 用户已明确授权任务20用作者代码重跑并修复依赖/脚本；租用A30端点当前TCP/SSH connection refused，任务20已报告并计划先在本地3070 Ti做兼容层TDD与smoke。该授权不改变G3、T0适配身份或受限资产边界。

## 接续边界

1. 继续监督任务树；不得把PR open或代码定位冒充官方main发布、可运行或复现成功。
2. 若后续验证VC-CSA，faithful作者任务复现与T0适配重实现必须分开配置、结果和命名；后者不能称官方复现。
3. 监督任务20先固定作者revision与补丁账本；A30不可达不得写成GPU运行失败，本地smoke也不得提前写成全量复现完成。
4. 任务30可按已通过G3的总纲条件进入后续流程，但不得修改任务20冻结评测器、split、class order或test规则，也不得将任务50成果写成已完成。
5. 项目只执行T-AFFC CARM；不得创建IJCV J0—J2、JH1—JH3、任务25或65。

## 接续提示词

你是新的“00-T-AFFC总控”，接替S04继续维护SSOT、监督任务树并独立审核。先读取`AGENTS.md`、`WORK_RECORD_POLICY.md`、`WORK_LOG.md`末条、总纲v1.16、`TASK00_G3_FINAL_REVIEW_20260718.md`和本卡，并刷新`origin/main`及相关任务实时状态。当前`G3=PASS_WITH_LIMITATIONS`；VC-CSA状态是`AUTHOR_RELEASED_IMPLEMENTATION_LOCATED_PR3_OPEN_NOT_YET_REPRODUCED`，不得恢复为当前代码缺失，也不得写成官方复现成功。持续传播T0目标评论/split不匹配、单种子/任务50未完成和I3D资产接受风险。项目只执行T-AFFC CARM，不得创建IJCV任务。每次会话收尾继续新建下一张`.light/handoff/S<NN>-*.md`并打印接续提示词。
