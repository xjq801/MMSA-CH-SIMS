# 00对VC-CSA作者split/peer物理隔离的独立审查

> 日期：2026-07-18  
> 作者代码：`JackySnake/MSA-CRVI@3e8c42608f4e89bc2082c55760aa63535e8e276a`  
> 实验身份：`AUTHOR_ORIGINAL_SETTING_NON_T0`

## 裁定

`AUTHOR_ORIGINAL_FULL_REPRODUCTION=LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`

`EFFECTIVE_I3D_TRANSFER_PERMISSION=BLOCKED_DO_NOT_TRANSFER`

## 独立复算

00直接运行`audit_peer_isolation()`读取作者固定`train_set.json`、`dev_set.json`、`test_set.json`、压缩标注字典和`video_to_comment.json`，只输出聚合计数，不输出comment ID或正文：

| split | comment数 | video数 | split内singleton video/ID | 每video最小/最大comment数 |
|---|---:|---:|---:|---:|
| train | 75,086 | 8,190 | 122 | 1 / 19 |
| dev | 10,727 | 5,833 | 2,750 | 1 / 7 |
| test | 21,454 | 7,360 | 1,573 | 1 / 12 |

跨split视频数为7,854。train/dev/test的`cross_split_only_peer_ids`分别为122/2,750/1,573，恰好等于各split singleton数；三者`no_global_peer_ids`均为0。审计器返回`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`。

00同时直接读取作者`csmv_dataset.py`：`get_video_other_comment_info()`从`video_to_comment[videoid]`随机取comment，并在取到当前comment时循环重抽，随后读取该peer的comment与opinion/emotion标签。故：

- split内singleton在严格过滤映射下无法取得另一comment，循环不能结束；
- 保留全量映射会使大量跨split视频的train样本读取dev/test peer评论与标签，违反物理隔离；
- 该冲突不是GPU、I3D、环境或batch问题，不能通过更多算力解决。

任务20新增负测验证“当前split内singleton但全局peer只来自另一split”时必须fail closed；00独立复跑VC-CSA专项7/7、全量67/67和真实聚合审计，均exit 0。最终任务20合同为120行、SHA-256=`5dbf891d1fcd6307ee19f98dc46c8e3f7c35a712c167a5b258c4c10b79d28d3c`，状态明确为`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY_NO_TRANSFER`。

## 结论与边界

faithful作者全量路径在当前无泄漏标准下不可执行。此前8 train/4 dev的smoke通过，是因为构建器有意选择每个split内存在peer的子集；它不证明完整作者split可物理隔离执行。

任何删除singleton、跨split取peer、self-peer、固定/合成peer、取消peer分支或视频级重新split都会改变作者合同，只能标为`REIMPLEMENTATION_NON_FAITHFUL_PEER_ADAPTATION`，不得写成作者原设定可信全量复现。该新实验若被提出，须单独冻结数据处理、estimand、对照和资产传输合同，并由00重新审批。

本阻断不改变`G3=PASS_WITH_LIMITATIONS`，不使既有`REIMPLEMENTATION_STRONG_BASELINE`失效，也不关闭I3D许可/revision/权利方fixity UNKNOWN风险。
