# M2 数据工程与标签隔离协议 v1

## 冻结边界

- 先按视频/帖子或更高层group划分，再允许训练集内建索引、拟合预处理或采样。
- CSMV评论只在单个视频内部聚合，输出经验分布、有效评论数、熵、最大类占比、有效类别数和逐类二项标准误；不输出评论正文。
- `group-by-video-v1`使用固定salt的哈希划分；`hashtag-held-out-v1`按hashtag—视频二部图连通分量划分，保证同一hashtag分量不跨split。
- CSMV没有原生topic，`topic-held-out`保持`BLOCKED_NATIVE_TOPIC_ABSENT`，不得把hashtag改名为topic。
- 任何检索索引状态在M2固定为`NOT_BUILT`；后续只能读取train记录建索引。

## 第二主集映射

第二人工标注多模态主集尚未冻结。`LABEL_SPACE_MAPPING_DRAFT.md`为版本化候选草案，`data/manifests/second-primary-label-map-v1.manifest.json`固定记录`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`。在G1恢复前，不生成“最终映射”，也不依据test结果改类别。

## 近重复与发布者捷径边界

当前可机械检查精确item/group重复、hashtag分量交叉、重复BV和发布者字段可用性。CSMV媒体未下载且无发布者元数据，因此感知哈希、同源事件和发布者捷径只能标记为`UNKNOWN/NOT_TESTABLE_WITH_CURRENT_ASSETS`，不能宣称查全。

## 标签层级

- `HUMAN_GOLD`：公开人工标注经视频级聚合后的标签。
- `SILVER`：模型、规则或遗留统计流程生成的标签；教师或置信度未知时必须显式写`UNKNOWN`。
- `UNLABELED`：无标签输入或ID映射，不得混入标签评测。

加载器一次只接受一个层级。公开人工test标签永不与银标合并；银标只能进入单独适配/敏感性流程，且不能替代G1第二人工主集。
