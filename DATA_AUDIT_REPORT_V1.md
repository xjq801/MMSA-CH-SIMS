# 数据审计报告 v1

## 结论

- 发布级别：`LOCAL_CANDIDATE_G1_BLOCKED`，不是正式benchmark发布。
- 泄漏自动门：`PASS_WITH_LIMITATIONS`，Critical失败数 `0`。
- G1：`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`。
- G2：`NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`。

## 数据闭环

| 层级 | 数据 | 记录数 | 定位 |
|---|---|---:|---|
| HUMAN_GOLD | CSMV视频级人工评论经验分布 | 8210 | 唯一当前公开人工主集 |
| SILVER | CUC-IGPE-v2遗留银标canonical | 2787 | 辅助、本地、不得并入人工test |
| UNLABELED | 预留入口 | 0 | 当前为空 |

CSMV的`group_by_video_v1`为train/dev/test `{"dev": 816, "test": 1675, "train": 5719}`；`hashtag_heldout_v1`为 `{"dev": 602, "test": 1618, "train": 5990}`。原生topic和发布时间缺失，因此topic/time协议未发布。

## 已证实问题

- CUC历史2815与当前2787相差 `28` 条，缺少2815原始manifest，去向未解释。
- CUC有 `221` 条标签冲突、`1904` 条缺发布时间；许可仍为`UNKNOWN_LOCAL_ONLY`。
- CSMV媒体、发布者和媒体指纹未纳入本地包，语义近重复、同源事件和发布者捷径不能声明已查全。
- 第二人工多模态主集未冻结，故dataset-v1/split-v1只能是本地候选。

## 泄漏边界

已自动检查ID交集、source group、评论—视频归属、目标评论字段、未来候选字段、train-only索引合同、时间split合同和fit范围。检查是确定性的启发式门，不替代媒体/语义人工审计。任一Critical失败时构建器先退出并输出`LEAKAGE_BLOCKED`，不会写出新的release manifest。
