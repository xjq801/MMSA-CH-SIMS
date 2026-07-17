# 数据审计报告 v1

## 结论

- 发布级别：`PROTOCOL_DATA_G2_PASS_ASSET_RISK_ACCEPTED`，允许内部研究使用。
- 泄漏自动门：`PASS_WITH_LIMITATIONS`，Critical失败数 `0`。
- G1：`PASS`；LAI-GAI已冻结为第二人工跨域图像主集。
- G2：`PASS_WITH_ACCEPTED_ASSET_RISK`；协议/数据门通过，资产外部证明延期接受。

## 数据闭环

| 层级 | 数据 | 记录数 | 定位 |
|---|---|---:|---|
| HUMAN_GOLD | CSMV视频级人工评论经验分布 | 8210 | 视频主集；承担H1/H2 |
| HUMAN_GOLD | LAI-GAI图像级人工诱发情绪分布 | 847 | 第二跨域图像主集；承担OOD/校准/H3边界 |
| SILVER | CUC-IGPE-v2遗留银标canonical | 2787 | 辅助、本地、不得并入人工test |
| UNLABELED | 预留入口 | 0 | 当前为空 |

CSMV的`group_by_video_v1`为train/dev/test `{"dev": 837, "test": 1675, "train": 5698}`；`hashtag_heldout_v1`为 `{"dev": 327, "test": 672, "train": 7211}`。原生topic和发布时间缺失，因此topic/time协议未发布。

## CSMV I3D输入协议

- 本地候选输入的文件树、逐文件hash、`float32[T,1024]` schema与8210/8210覆盖已闭合；资产许可、稳定官方revision及权利方包身份/fixity为`DEFERRED_ACCEPTED_RISK`。用户授权仅覆盖项目内部研究，不产生许可信用或再分发权。
- 任何训练/test结果前已冻结完整序列+动态padding/mask主协议，以及首尾覆盖的确定性均匀180步主敏感性；前180只作补充。所有split同规则，禁止test自适应。
- 论文主张只限冻结I3D视觉表征上的公众诱发受众情绪分布预测；音频=`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`，评论不是T0学生输入。

## 已证实问题

- CUC历史2815与当前2787相差 `28` 条，缺少2815原始manifest，去向未解释。
- CUC有 `221` 条标签冲突、`1904` 条缺发布时间；许可仍为`UNKNOWN_LOCAL_ONLY`。
- CSMV官方URL表是内部`video_file_id`到平台源视频URL的映射；内部ID与平台ID不要求相等。8,210条映射形成8,008个源视频族，202个重复族已在全部已发布split中保持零交叉。
- 原始媒体、发布者和媒体内容指纹未纳入本地包；因此只声明官方URL元数据可识别的同源族已闭合，不外推到不可观察的内容级近重复。协议/数据G2已书面通过，split正式用于内部实验；I3D不得再分发，投稿时必须披露资产风险。

## 泄漏边界

已自动检查ID交集、source group、评论—视频归属、目标评论字段、未来候选字段、train-only索引合同、时间split合同和fit范围。检查是确定性的启发式门，不替代媒体/语义人工审计。任一Critical失败时构建器先退出并输出`LEAKAGE_BLOCKED`，不会写出新的release manifest。
