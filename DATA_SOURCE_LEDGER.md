# 数据来源、许可与完整性台账

> 版本：v1.2
> 建立日期：2026-07-14  
> 原则：来源、许可、访问条件、下载时间和 SHA-256 未核验前一律记为 `PENDING` 或 `UNKNOWN`，不得把“能下载”视为“可用于研究或发布”。

## 1. 候选数据源登记

| ID | 数据源 | 研究角色 | 真值等级 | 来源定位 | 当前状态 | 许可/条款 | 本地位置 | SHA-256 | 下一步 |
|---|---|---|---|---|---|---|---|---|---|
| DS-001 | CSMV / MSA-CRVI | 第一公开主 benchmark | `HUMAN_GOLD`评论；已按视频聚合 | https://github.com/IEIT-AGI/MSA-CRVI | CANONICAL_LABELS_READY_MEDIA_PENDING | README声明annotations为CC BY-SA 4.0；根LICENSE为Apache-2.0、README称代码MIT；TikTok媒体/URL与特征权利不外推 | `data/raw/csmv/99d142.../`（Git忽略） | 原始不可变清单见`data/manifests/csmv-primary-raw-v1.manifest.json`；派生标签见`human-gold-v1.manifest.json` | 8210视频、107267评论聚合闭合；video-group与hashtag连通分量split已生成；原生topic缺失，媒体/特征仍PENDING |
| DS-002 | iNews | 第二公开人工标注候选 | `HUMAN_GOLD`多参与者标注 | https://aclanthology.org/2025.acl-long.1217/ | NO_GO_PRIMARY_MEDIA_REPRO | public非persona版CC BY-NC-SA 4.0；图片不随包发布且受第三方条款/版权约束 | `data/raw/inews/a7ad599.../`（Git忽略） | 逐文件见`data/manifests/inews-source-v1.manifest.json` | 标签包可审计；图片不可由固定revision复现且截图含T0后reaction count，当前不作第二多模态主集 |
| DS-003 | NEmo+ | iNews No-Go后的第二主集备选 | `HUMAN_GOLD`众包反应 | https://aclanthology.org/2022.aacl-main.29/ | NO_GO_PRIMARY_LICENSE_MEDIA | 包内未发现LICENSE；论文中的BU-NEmo研究许可不等于NEmo+再使用/再分发许可 | `data/raw/nemo/ACL-Anthology-2022-11-21/`（Git忽略） | 逐文件见`data/manifests/nemo-source-v1.manifest.json` | ACL包有1297条标签记录但0张图片、仅匿名本地路径；需作者许可与媒体入口后复核 |
| DS-004 | MVIndEmo | 银标签辅助集 | `SILVER`自动/模型聚合软标签 | https://doi.org/10.1007/s00530-023-01221-8 | SILVER_ONLY_SOURCE_UNAVAILABLE | 论文开放可读；所列GitHub在2026-07-14网页/API均404，数据许可仍UNKNOWN | 未下载 | UNKNOWN | 三模型评论情感融合并按点赞加权已核；只作辅助且不阻塞G1，合法来源恢复前不使用 |
| DS-005 | CUC-IGPE-v2 | 中文外部压力测试 | `SILVER`；非正式人工测试真值 | 工作区外只读根目录：`D:\李佳怡毕业论文配套代码\极端群体情绪预测数据集` | CANONICAL_LOCAL_ONLY_LICENSE_UNKNOWN | PENDING：平台条款、隐私、匿名化和可发布范围审计 | 2026-07-14只读生成；源文件未改写、未复制入项目 | 132个源文件逐文件hash见`data/manifests/cuc-auxiliary-raw-v1.manifest.json`；canonical hash见`cuc-canonical-v1.manifest.json` | 2787条canonical；2815差28条仍UNKNOWN；221冲突显式保留；8条缺BV、0重复BV、883条有时间（含1条跨发布者匹配警告） |
| DS-006 | CH-SIMS processed | 历史构念不匹配辅助资产 | 数据集既有标签；不作为受众群体情绪主证据 | 当前项目已有本地文件，原始来源/许可待回溯 | LOCAL_PRESENT | PENDING：补原始来源、版本和许可记录 | `data/SIMS/Processed/unaligned_39.pkl` | `C9E20C13EC0454D98BB9C1E520E490C75146BFA2DFEEEA78D84DE047DBDD442F` | 回溯下载来源和版本；仅用于历史 MMSA 基线或辅助实验 |
| DS-007 | LIRIS-ACCEDE Discrete | 第二人工主集新候选；本轮唯一深审 | 多人`HUMAN_GOLD`诱发VA秩；不是离散经验分布 | https://liris-accede.ec-lyon.fr/ | NO_GO_CURRENT_AUTHORIZATION_EULA_CONTACT_REQUIRED | 媒体逐源电影CC；annotations/描述CC BY-NC-SA 3.0；EULA限学术且禁再分发 | 未下载 | UNKNOWN | 9800片段/160电影；Protocol A按电影隔离；需另行授权机构EULA，且VA秩无法无损映射JS分布主任务 |
| DS-008 | PMEmo | 第二人工主集元数据候选 | 457名受试者人工VA；逐项分布可用性未知 | https://github.com/HuiZhangDB/PMEmo | NO_GO_LICENSE_SPLIT_AND_LABEL_DISTRIBUTION_UNKNOWN | 仓库软件MIT；数据、MP3、歌词、评论与标注许可不得外推，当前UNKNOWN | 未下载 | UNKNOWN | README称794歌曲/约1.3GB；split未知；评论非T0；音乐VA与公众视频分布只部分匹配 |
| DS-009 | Emotion6 | 第二人工主集元数据候选 | 每图15人、七类诱发情绪经验分布 | https://openaccess.thecvf.com/content_cvpr_2015/papers/Peng_A_Mixed_Bag_2015_CVPR_paper.pdf | NO_GO_MEDIA_LICENSE_ACCESS_AND_MODALITY | 数据许可、现行官方入口和Flickr逐图权利UNKNOWN | 未下载 | UNKNOWN | 1980单图；论文随机7:3；标签构念高度匹配但非视频/多模态且媒体准入未证实 |

## 2. 本地文件快照

| 记录日期 | 文件 | 字节数 | 修改时间（UTC） | SHA-256 | Git策略 |
|---|---|---:|---|---|---|
| 2026-07-14 | `data/SIMS/Processed/unaligned_39.pkl` | 1,228,189,774 | 2026-07-04T14:10:50.3568601Z | `C9E20C13EC0454D98BB9C1E520E490C75146BFA2DFEEEA78D84DE047DBDD442F` | 不纳入 Git；保留本地并后续决定 DVC/对象存储政策 |
| 2026-07-14 | CSMV小型审计资产（10文件） | 14,436,790 | 固定上游commit | 逐文件见`data/manifests/csmv-source-v1.manifest.json` | 原始文件不入Git；manifest和脚本可入Git |
| 2026-07-14 | iNews public审计资产（7文件） | 26,502,742 | 固定HF revision | 逐文件见`data/manifests/inews-source-v1.manifest.json` | 原始CSV不入Git；manifest和聚合统计可入Git |
| 2026-07-14 | NEmo+ ACL Dataset.zip | 2,080,204 | ACL附件Last-Modified 2022-11-21 | 见`data/manifests/nemo-source-v1.manifest.json` | 原始包/展开内容不入Git；仅许可与结构审计 |

## 3. 每次下载必须补充的字段

- 数据源 ID、版本或发布日期；
- 官方页面、论文页和实际下载地址；
- 许可名称、条款快照位置和访问限制；
- 下载日期、下载者、原始文件名、字节数和 SHA-256；
- 是否包含个人信息、评论文本、媒体内容或平台标识；
- 原始数据是否可再分发，处理特征/ID/split 是否可发布；
- 处理脚本版本、输出文件、数据 lineage 和已知缺口；
- 删除、撤回或访问到期要求。

## 4. 证据等级规则

- `HUMAN_GOLD`：独立人工标注且标注协议、样本单位和质量证据可审计。
- `SILVER`：规则、模型、LLM 或集成生成，只可用于训练、筛选、适配和压力测试。
- `UNLABELED`：只报告无需真值的域距离、覆盖率、预测熵、拒绝率和定性案例。
- `UNKNOWN`：来源、许可、版本或标签生成过程未核验；不得进入正式实验。

正式论文主要定量结论必须来自两个通过许可与可复现性审计的 `HUMAN_GOLD` 公开数据集。

## 5. 官方证据与实证快照（2026-07-14）

| 数据源 | 官方证据 | 当前可确认 | 仍不可确认 |
|---|---|---|---|
| CSMV | NeurIPS论文页；官方GitHub固定commit；本地manifest与结构审计 | 正式split 107267评论、8210视频；`video_file_id`零缺失、35个hashtag；官方comment split存在大量视频交叉 | TikTok媒体权利/存活率；特征包版本、体量/hash；URL清单因上游theme格式问题未完成行级覆盖核验 |
| iNews | ACL论文页；作者GitHub；HF public固定revision；本地结构审计 | 11320行、2736个post、VAD 1—7、9类Discrete；CC BY-NC-SA 4.0；可按post重划标签 | 图片不在包内；媒体合法恢复率；截图T0去互动量；与论文2899 post差异原因 |
| NEmo+ | ACL论文页与官方Dataset.zip | 1297条新闻、T/I/TI各12970反应、总38910；八类人类诱发情绪 | 包内0图、0许可文件；匿名本地图片路径不可解析；再使用/再分发许可 |
| MVIndEmo | Springer开放论文与论文所列GitHub | 7153视频、8话题；三评论模型融合并按评论点赞加权，属于SILVER | 仓库404；合法数据入口、许可、媒体可得性 |
| LIRIS-ACCEDE | 官方站、database页、官方EULA、IEEE TAC作者公开稿 | 9800个8—12秒视听片段、160电影；多人VA秩；Protocol A按电影隔离 | 数据revision、包字节数/hash、受限XML逐片段许可；EULA邮件门；非离散经验分布 |
| PMEmo | 作者官方GitHub固定仓库commit；README | 794歌曲、457受试者、静态/动态VA；约1.3GB；副歌MP3/特征/歌词/评论/EDA | 数据资产许可、固定数据revision/hash、split和逐项标注分布；评论必须排除T0 |
| Emotion6 | CVPR官方论文 | 1980图像、432受试者、每图15人；七类诱发情绪分布；论文随机7:3 | 现行官方数据入口、许可、包体量/hash、Flickr逐图权利；仅图像模态 |

下载成功不等于`FIT`或G1通过。CSMV的视频级人工标签、不可变manifest和两套无group交叉split已可复跑；但第二人工标注多模态主集尚未确定。新一轮只读短名单与LIRIS-ACCEDE深审没有关闭访问和标签形态阻塞，步骤27保持`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`，G1继续`BLOCKED`，G2不进入验收。
