# M2泄漏测试报告 v1

> 本报告是步骤34—35的自动化证据，不等同于G1/G2通过。

## 门状态

- 泄漏门：`PASS_WITH_LIMITATIONS`
- Critical失败数：0
- G1：`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`
- G2：`NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`

## 检查结果

| 检查 | 结果 | 状态 |
|---|---:|---|
| `id_intersection` | PASS | `PASS` |
| `source_group_intersection` | PASS | `PASS` |
| `same_video_comment_grouping` | PASS | `PASS` |
| `target_comment_fields` | PASS | `PASS` |
| `future_candidate_fields` | PASS | `PASS` |
| `index_train_only` | PASS | `PASS_NOT_BUILT` |
| `time_order` | PASS | `NOT_APPLICABLE_NO_TIME_SPLIT` |
| `fit_scope` | PASS | `PASS_NO_FIT_ARTIFACTS` |

## 边界

- Checks are deterministic but not proof that every semantic near-duplicate or same-event leak has been found.
- No CSMV chronological split is evaluated because publish timestamps are unavailable.
- Publisher and media-fingerprint leakage remain unresolved where source metadata/media are unavailable.

时间顺序检查当前为`NOT_APPLICABLE_NO_TIME_SPLIT`：这表示未发布时间split，不表示时间安全已被证明。
任何后续新增time split、索引、拟合状态或候选字段都必须重新运行本门。
