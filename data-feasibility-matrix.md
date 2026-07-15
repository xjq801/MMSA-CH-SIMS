# M1 数据可行性矩阵

> 版本：v0.3
> 审计日期：2026-07-14
> 状态：LAI-GAI第二主集已正式冻结；CSMV媒体元数据lineage/split已由00接受；G1通过，G2因CSMV正式输入资产与复现证据陈旧而阻塞。

| 数据源 | 角色 | 人工真值 | T0任务匹配 | 分组划分条件 | 多模态输入可复现性 | 当前裁定 | 主要缺口 |
|---|---|---|---|---|---|---|---|
| CSMV / MSA-CRVI | 第一主集 | 人工评论意见3类与Plutchik 8类 | 高；评论可作为未来响应标签，但不得进入T0输入 | 8210个内部视频均可聚合；源族与hashtag协议已零交叉，无原生topic | URL表闭合8210条/8008源族；I3D/VideoMAEv2资产许可、revision、文件树、体量和hash仍未知 | `LABEL_AND_URL_LINEAGE_READY_FORMAL_INPUT_BLOCKED` | 按最小授权只读预审官方特征资产；完成当前核心隔离复现 |
| iNews public | 第二主集首选 | 多参与者VAD、9类离散情绪 | 中高；内容诱发反应匹配，但需从个体标注聚合到post分布 | 标签可按2736个post重划；原公开任务文件存在post重叠，不能直接作为本项目split | 文本/标签可得；固定公开包无图片和媒体字段，截图恢复依赖第三方且含reaction count | `NO_GO_PRIMARY_MEDIA_REPRO` | 合法可复现图片、T0去互动量、2899/2736差异；direct6会丢37.95%标注与227个post |
| NEmo+ | iNews失败后的备选 | T/I/TI三条件众包人工反应 | 高；直接测内容诱发人群反应与模态差分 | 可按1297个news item隔离条件，但尚未生成split | ACL包含标签但0张图片、仅匿名本地图片路径；包内0许可文件 | `NO_GO_PRIMARY_LICENSE_MEDIA` | 明确许可、对应图片与hash、稳定合法入口 |
| MVIndEmo | 银标辅助 | 否；三评论模型融合并按点赞加权 | 仅适合弱监督、迁移或压力测试 | 不进入人工金标正式测试 | 论文所列GitHub当前404 | `SILVER_ONLY_SOURCE_UNAVAILABLE` | 合法入口与许可；不阻塞G1、不升级为金标 |
| CUC-IGPE-v2 | 中文外部压力测试 | 无标签/银标 | 仅无标签或银标外验 | 需publisher/topic/time隔离 | 本地位置和媒体缺失待登记 | `UNKNOWN` | canonical根目录、时间恢复、2815/2787漂移、221冲突 |
| VCE | 第二视频主集修复候选 | 每视频平均约13名MTurk参与者、27类自身诱发情绪 | 构念与经验分布高度匹配 | 来源/hashtag可候选分组，尚无包级复现 | Reddit/Instagram视频无正式媒体许可，作者依赖美国Fair Use；标注时不提供音频 | `NO_GO_MEDIA_LICENSE_AND_AUDIO` | 明确可跨司法辖区使用的媒体权利；正式包revision/size/hash；音频缺失裁定 |
| LAI-GAI v05 | 第二人工跨域图像主集/缺失模态验证集 | 847图；六项研究；63682个合规逐图反应；每图58—96；12个1—7离散情绪强度维度 | 直接测图像诱发反应；按12维去量表下界后归一化为连续分布；prompt/目标类别不作真值或输入 | 379个source group；594/127/126；source/文化/性别/年龄/同prompt/精确与dHash近重复均不跨split | 官方Data Card和OSF组件均为CC BY 4.0；847官网图与评分100%闭合；逐图hash固定 | `FROZEN_00_APPROVED` | 单图/AI生成域，仅承担图像跨域、校准/OOD、缺失模态与H3边界；H1/H2=`NOT_APPLICABLE_BY_DESIGN` |

## 当前门判断

- CSMV的video-group重建已通过样本级结构验证；官方comment split不得复用。URL清单的两类ID属于不同命名空间；旧2644错配判断已撤销。202个重复源族现已在`group_by_video`和hashtag协议中零交叉。
- iNews已执行No-Go；按规则切换审计NEmo+，但NEmo+同样未通过许可与媒体可复现性门。
- 00以`REVIEW-00-CSMV-FEATURE-PREFLIGHT-G2-20260715`独立确认19项公共核心复现当前PASS并关闭陈旧子阻塞；G2状态收敛为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`，任务20禁令不变。

## 下一轮最小动作

1. 按`AUTH-00-CSMV-FEATURE-ASSET-PREFLIGHT-RO-20260715`只读核验官方特征入口；不得下载特征或媒体，不把URL元数据lineage冒充输入字节lineage。
2. 旧API审计仍保留`ACCEPTED_AS_NONCONFORMING_OBSERVATION_NO_GATE_CREDIT`；其validator失败不得删除，也不用于新冻结候选的通过证据。
3. 新独立授权`AUTH-00-SECOND-PRIMARY-RESOLUTION-20260714`已完成官网847图与评分资产闭合；专项validator与00冻结复审均通过。全局`formal_split=false`继续由G2阻塞。
