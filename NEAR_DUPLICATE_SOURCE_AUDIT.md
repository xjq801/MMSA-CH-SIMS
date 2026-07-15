# 近重复、同源事件与发布者捷径审计 v1

## 当前可验证结果

| 数据 | 检查 | 结果 | 结论 |
|---|---|---:|---|
| CSMV | canonical item ID重复 | 0 | PASS |
| CSMV | `group-by-video-v1`视频跨split | 0 | PASS |
| CSMV | hashtag连通分量跨split | 0 | PASS |
| CSMV | 官方URL平台源视频族跨`group-by-video-v1` | 0/8008 | PASS |
| CSMV | 官方URL平台源视频族跨`hashtag-held-out-v1` | 0/8008 | PASS |
| CSMV | 重复源视频族 | 202族/404条 | 已先合并后划分；负面夹具可阻断 |
| CSMV | 评论正文进入canonical | 0字段 | PASS |
| CSMV | 原生topic可用性 | 不存在 | `BLOCKED_NATIVE_TOPIC_ABSENT` |
| CSMV | 媒体感知哈希/视觉近重复 | 无媒体 | `NOT_TESTABLE_WITH_CURRENT_ASSETS` |
| CSMV | 同源事件检测 | 官方URL源视频ID可检测范围已闭合；无标题/媒体内容指纹 | `PASS_OBSERVABLE_SOURCE_ID / UNKNOWN_BEYOND_OBSERVABLE` |
| CSMV | 发布者捷径 | 无发布者字段 | `UNKNOWN` |
| CUC-IGPE-v2 | 重复BV行 | 0 | PASS（仅精确BV） |
| CUC-IGPE-v2 | 跨发布者目录时间匹配 | 1 | WARN，保留`GLOBAL_CROSS_PUBLISHER`来源 |
| CUC-IGPE-v2 | 发布者group字段 | 44个目录可哈希分组 | 后续split必须按发布者隔离 |
| CUC-IGPE-v2 | 媒体近重复/同一事件 | 未建立媒体指纹 | `UNKNOWN` |

## 边界

该审计只覆盖精确ID、显式group和现有元数据，不能宣称查全语义近重复或同源事件。正式G2前若媒体/标题合法可得，应在划分前生成train无关的内容指纹和人工复核候选；任何指纹阈值必须在test结果不可见时冻结。
