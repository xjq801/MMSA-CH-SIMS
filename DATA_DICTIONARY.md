# Canonical 数据字典 v1

> 状态：`FROZEN_v1`（2026-07-14）
> Schema：`data/manifests/canonical-audience-affect-v1.schema.json`
> 统计单位：视频或帖子；评论只生成标签，不是T0输入。

| 字段 | 类型 | 来源 | `available_at_t0` | 缺失策略 | 敏感等级 |
|---|---|---|---:|---|---|
| `schema_version` | string | 本项目协议 | true | 禁止缺失 | PUBLIC_METADATA |
| `dataset_id` | string | source manifest | true | 禁止缺失 | PUBLIC_METADATA |
| `item_id` | SHA-256 string | 原视频/帖子ID的命名空间哈希 | true | 缺ID时对源文件位置和行号哈希并标记 | PSEUDONYMIZED |
| `label_tier` | enum | 标签来源隔离协议 | false | 禁止缺失 | PUBLIC_METADATA |
| `label_source` | string | 数据集标注或银标管线 | false | 未知写`UNKNOWN`，不得推断 | PUBLIC_METADATA |
| `source_group_id` | string/null | 视频或帖子分组键的哈希 | true | 缺失则不得进入正式split | PSEUDONYMIZED |
| `source_domain` | string/null | 平台/来源域 | true | 未核来源时保留null；用于后续source-held-out | PUBLIC_METADATA |
| `topic_id` | string/null | 原生topic的哈希 | true | 原生字段不存在时保留null | PSEUDONYMIZED |
| `publisher_id` | string/null | 发布者分组键的哈希 | true | 不以文件顺序填充 | RESTRICTED_PSEUDONYMIZED |
| `publish_time` | string/null | 发布者视频列表/源数据 | true，仅当证实为发布时间 | 缺失保留null并置`missing_time=true` | RESTRICTED_METADATA |
| `response_count` | integer | 标签窗口内有效人工反应数 | false | 0表示无标签，不用均值填充 | AGGREGATED_LABEL |
| `emotion_distribution` | object/null | 人工评论情绪聚合 | false | 缺标注类别从分母排除并另计 | AGGREGATED_LABEL |
| `opinion_distribution` | object/null | 人工评论意见极性聚合 | false | 缺标注类别从分母排除并另计 | AGGREGATED_LABEL |
| `distribution_uncertainty` | object/null | 经验分布统计量 | false | 无有效反应时为null | AGGREGATED_LABEL |
| `hashtag_component_id` | string/null | hashtag—视频连通分量哈希 | true | 无hashtag时不得宣称hashtag-held-out | PSEUDONYMIZED |
| `split` | object | 固定算法与salt | true | 只允许train/dev/test/not_assigned | PUBLIC_METADATA |
| `native_label` | scalar/null | 源标签/遗留向量标签 | false | 不跨数据集强制填充 | LABEL_RESTRICTED |
| `continuous_affect` | number/null | CUC遗留连续群体情绪 | false | 多记录冲突时保留首条并登记记录数 | SILVER_RESTRICTED |
| `label_conflict` | boolean | vector标签与本地标签比对 | false | 未匹配不等同于冲突，单独登记 | PUBLIC_METADATA |
| `duplicate_source_id` | boolean | 同源ID计数 | true | 禁止静默去重 | PUBLIC_METADATA |
| `missing_time` | boolean | 发布时间审计 | true | 禁止用文件顺序伪造时间 | PUBLIC_METADATA |
| `legacy_features` | number[48]/null | CUC遗留统计向量 | false | 不插补；M3前不得使用 | SILVER_RESTRICTED |
| `legacy_features_available_at_t0` | boolean | T0字段审计 | true | 当前固定false | PUBLIC_METADATA |
| `available_at_t0` | boolean | 本协议逐记录结论 | true | 标签记录固定false | PUBLIC_METADATA |
| `provenance` | object | 文件hash、行号、revision、规则版本 | true | 禁止缺失 | RESTRICTED_METADATA |

## 明确禁止的字段

`comment`、`comment_text`、目标评论点赞、最终互动量、未来推荐结果和全图统计不得出现在T0加载结果中。CUC遗留48维向量含播放量/热度等未证实T0字段，因此虽可为审计保留，`legacy_features_available_at_t0`固定为`false`。
