# M1 数据可行性矩阵

> 版本：v0.2
> 审计日期：2026-07-14
> 状态：步骤11—18实证完成；第二主集未通过，未构成G1通过证据。

| 数据源 | 角色 | 人工真值 | T0任务匹配 | 分组划分条件 | 多模态输入可复现性 | 当前裁定 | 主要缺口 |
|---|---|---|---|---|---|---|---|
| CSMV / MSA-CRVI | 第一主集 | 人工评论意见3类与Plutchik 8类 | 高；评论可作为未来响应标签，但不得进入T0输入 | 已实证：8210个视频均可按`video_file_id`聚合；官方split视频严重交叉；35个hashtag可做held-out，无原生topic | 标注可复现；I3D/VideoMAEv2仅有入口，原媒体仅URL，权利/体量/存活率未知 | `GROUPABLE_LABELS_VERIFIED_MEDIA_PENDING` | 正式视频级split、特征大小/hash、URL行级覆盖、媒体权利与存活率 |
| iNews public | 第二主集首选 | 多参与者VAD、9类离散情绪 | 中高；内容诱发反应匹配，但需从个体标注聚合到post分布 | 标签可按2736个post重划；原公开任务文件存在post重叠，不能直接作为本项目split | 文本/标签可得；固定公开包无图片和媒体字段，截图恢复依赖第三方且含reaction count | `NO_GO_PRIMARY_MEDIA_REPRO` | 合法可复现图片、T0去互动量、2899/2736差异；direct6会丢37.95%标注与227个post |
| NEmo+ | iNews失败后的备选 | T/I/TI三条件众包人工反应 | 高；直接测内容诱发人群反应与模态差分 | 可按1297个news item隔离条件，但尚未生成split | ACL包含标签但0张图片、仅匿名本地图片路径；包内0许可文件 | `NO_GO_PRIMARY_LICENSE_MEDIA` | 明确许可、对应图片与hash、稳定合法入口 |
| MVIndEmo | 银标辅助 | 否；三评论模型融合并按点赞加权 | 仅适合弱监督、迁移或压力测试 | 不进入人工金标正式测试 | 论文所列GitHub当前404 | `SILVER_ONLY_SOURCE_UNAVAILABLE` | 合法入口与许可；不阻塞G1、不升级为金标 |
| CUC-IGPE-v2 | 中文外部压力测试 | 无标签/银标 | 仅无标签或银标外验 | 需publisher/topic/time隔离 | 本地位置和媒体缺失待登记 | `UNKNOWN` | canonical根目录、时间恢复、2815/2787漂移、221冲突 |

## 当前门判断

- CSMV的video-group重建已通过样本级结构验证；官方comment split不得复用，正式split仍待M2冻结。
- iNews已执行No-Go；按规则切换审计NEmo+，但NEmo+同样未通过许可与媒体可复现性门。
- 第二人工标注多模态主集未确定；G1仍为`BLOCKED`，G2不得启动正式验收。

## 下一轮最小动作

1. 不拉取CSMV大特征或媒体；先冻结视频聚合质量规则和split约束草案。
2. 由用户/00总控决定是否联系iNews/NEmo+作者核许可与媒体入口。
3. 若无法恢复两者，批准审计另一套现成多人类标注公开集或缩小跨数据主张；不以MVIndEmo替代人工金标。
