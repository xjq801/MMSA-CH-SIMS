---
session_no: S05
contract_version: 2
suggested_title: "[T-AFFC] S06 监督任务20算力阻塞与任务树"
parent_session: S04
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-18
---

# S05 任务20 VC-CSA补充证据验收交接卡

## 当前状态

- 主仓库验收锚点：`main@820ce06de09c964b9f55e136cc09c4ba8cf6ad70`；主修复`1b91a9596de604bdf4279fda5416276b6f843e37`。
- `G3=PASS_WITH_LIMITATIONS`不变。
- `TASK20_VCCSA_SUPPLEMENT=ACCEPTED_WITH_LIMITATIONS`。
- VC-CSA当前状态：`AUTHOR_ORIGINAL_PATH_SMOKE_EXECUTABLE_FULL_REPRODUCTION_BLOCKED_COMPUTE`；身份：`AUTHOR_ORIGINAL_SETTING_NON_T0`。
- 过滤后的runtime为8 train/4 dev/0 test，annotation/video mapping各12个ID；新本地GPU smoke完成且未OOM，指标不得报告。
- 构建器仍读取作者全量源；只有持久化runtime物理排除test/未选择记录。旧smoke不具该物理隔离证据。
- post-snapshot erratum优先解释VC-CSA当前状态；G3 package、baseline表、HANDOFF冻结字节不变。
- 00独立复跑专项6/6、全量66/66、日志109条和handoff 22项通过。
- 全量作者复现仍因可用高显存GPU阻塞；A30不可达，本地粗估约52天。
- I3D许可/revision/权利方包身份/fixity未知与止损条件不变。

## 监督边界

1. 不得把smoke、输入隔离修复或代码提交写成全量、官方main或T0复现。
2. faithful作者原任务与T0适配必须分开配置、结果和命名；后者只能是`REIMPLEMENTATION`。
3. 若恢复高显存GPU，在全量运行前重新确认revision、补丁账本、环境、数据不外传与test预注册边界。
4. 不创建或执行IJCV J0—J2、JH1—JH3、任务25或65；任务50仍未完成。
5. `light-consistency`当前仅PARTIAL，不得冒充完整一致性门。

## 接续提示词

你是新的“00-T-AFFC总控”，接替S05。先读取`AGENTS.md`、`WORK_RECORD_POLICY.md`、`WORK_LOG.md`末条、总纲v1.16、`TASK00_G3_FINAL_REVIEW_20260718.md`、`TASK00_TASK20_VCCSA_SUPPLEMENT_REVIEW_20260718.md`、`TASK20_POST_SNAPSHOT_VCCSA_ERRATUM_20260718.md`和本卡，并刷新`origin/main`与任务20实时状态。当前G3仍为PASS_WITH_LIMITATIONS；VC-CSA只达到过滤后作者原路径GPU smoke可执行，全量复现受算力阻塞且NON_T0。持续区分source read与runtime persistence、faithful作者任务与T0重实现，传播I3D接受风险及任务50未完成。项目只执行T-AFFC CARM，不得创建IJCV任务。每次会话收尾继续新建下一张`.light/handoff/S<NN>-*.md`并打印接续提示词。
