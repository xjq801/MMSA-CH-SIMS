# 00对任务20 VC-CSA补充证据的独立审查

## 裁定

`TASK20_VCCSA_SUPPLEMENT=ACCEPTED_WITH_LIMITATIONS`

审查对象：`main@820ce06de09c964b9f55e136cc09c4ba8cf6ad70`，主修复提交`1b91a9596de604bdf4279fda5416276b6f843e37`。

本裁定不改变`G3=PASS_WITH_LIMITATIONS`，也不把smoke升级为全量作者复现、官方main复现或T0复现。

## 独立核验

- 任务20补正前提交`14012c8285790edddb78885723bf2e913479f8eb`可审计，但00发现两项缺口：执行审计仍混用旧“代码缺失”当前态；smoke runtime包含全量标注与映射，故旧“物理无test”证据不足。
- 补正后，构建器必须从作者全量源读取并过滤；持久化runtime的annotation与video mapping ID严格等于selected train/dev并集，缺失、额外ID或无同视频peer均fail closed。
- 新runtime为8 train、4 dev、0 test，annotation IDs=12、video mapping IDs=12；新run完成本地GPU train/dev smoke，未OOM。smoke指标无报告资格。
- `TASK20_BASELINE_EXECUTION_AUDIT.md`已将`99d1424`无代码限定为历史官方main尝试；当前状态为`AUTHOR_ORIGINAL_PATH_SMOKE_EXECUTABLE_FULL_REPRODUCTION_BLOCKED_COMPUTE`，协议身份为`AUTHOR_ORIGINAL_SETTING_NON_T0`。
- `TASK20_POST_SNAPSHOT_VCCSA_ERRATUM_20260718.md`只对VC-CSA当前状态建立优先级；G3 package、baseline表和HANDOFF冻结字节不变。
- 00独立复跑：VC-CSA专项6/6、全量66/66；`validate_work_log.py`为109条且通过；handoff validator为22项通过、`restricted_assets_required=false`；工作区clean。

## 必须传播的限制

1. 构建器读取全量作者源是事实；只有过滤后持久化runtime物理排除test/未选择记录。
2. 旧smoke只能证明入口未迭代test，不能证明旧runtime物理无test；只能引用补正后的新smoke。
3. 全量作者复现未启动；租用A30不可达，本地120 epoch粗估约52天，状态继续受算力阻塞。
4. 作者原任务读取目标评论并使用comment split，属于NON_T0；任何T0适配必须另建并标为`REIMPLEMENTATION`。
5. temporal-attention仍为`REIMPLEMENTATION_STRONG_BASELINE`，任务50五种子/bootstrap仍未完成。
6. I3D许可、官方revision、权利方包身份/fixity仍未知；`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`不变。权利否认或8210 hash/覆盖漂移立即触发`ASSET_INVALIDATED_DO_NOT_REPORT`。
7. `light-consistency`因安装缺`_shared/findings_schema`只能提供PARTIAL文本回扫，不得称完整一致性门通过。

## 00结论

接受任务20的输入隔离补丁、post-snapshot勘误和补正后smoke证据。任务20作者路径当前达到“可执行smoke且输入持久化边界闭合”，未达到全量复现；G3及原有强基线依据均不变。
