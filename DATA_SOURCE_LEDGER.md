# 数据来源、许可与完整性台账

> 版本：v1.5
> 建立日期：2026-07-14  
> 原则：来源、许可、访问条件、下载时间和 SHA-256 未核验前一律记为 `PENDING` 或 `UNKNOWN`，不得把“能下载”视为“可用于研究或发布”。

## 1. 候选数据源登记

| ID | 数据源 | 研究角色 | 真值等级 | 来源定位 | 当前状态 | 许可/条款 | 本地位置 | SHA-256 | 下一步 |
|---|---|---|---|---|---|---|---|---|---|
| DS-001 | CSMV / MSA-CRVI | 第一公开主 benchmark | `HUMAN_GOLD`评论；已按视频聚合 | https://github.com/IEIT-AGI/MSA-CRVI；元数据请求：https://github.com/IEIT-AGI/MSA-CRVI/issues/5 | I3D_QUARANTINE_8210_COVERAGE_EXTERNAL_ATTESTATION_DEFERRED | README声明annotations为CC BY-SA 4.0；根LICENSE为Apache-2.0、README称代码MIT；TikTok媒体/URL与特征权利不外推 | 固定annotations位于`data/raw/csmv/99d142.../`；I3D稳定入口为`data/raw/csmv/features/visual_feature/I3D/`（均Git忽略） | 标签/URL lineage闭合；本地I3D 9942文件、8210/8210覆盖、schema错误0、逐文件hash见`csmv-i3d-quarantine-v1.manifest.json`；序列协议见`csmv-i3d-sequence-protocol-v1.manifest.json`；资产许可/revision/权利方attestation仍UNKNOWN | 按用户指令将维护者协调标`DEFERRED_PENDING_MAINTAINER_REPLY`，本轮不等待、不催促、不重复核验；正式使用与G2不自行放行 |
| DS-002 | iNews | 第二公开人工标注候选 | `HUMAN_GOLD`多参与者标注 | https://aclanthology.org/2025.acl-long.1217/ | NO_GO_PRIMARY_MEDIA_REPRO | public非persona版CC BY-NC-SA 4.0；图片不随包发布且受第三方条款/版权约束 | `data/raw/inews/a7ad599.../`（Git忽略） | 逐文件见`data/manifests/inews-source-v1.manifest.json` | 标签包可审计；图片不可由固定revision复现且截图含T0后reaction count，当前不作第二多模态主集 |
| DS-003 | NEmo+ | iNews No-Go后的第二主集备选 | `HUMAN_GOLD`众包反应 | https://aclanthology.org/2022.aacl-main.29/ | NO_GO_PRIMARY_LICENSE_MEDIA | 包内未发现LICENSE；论文中的BU-NEmo研究许可不等于NEmo+再使用/再分发许可 | `data/raw/nemo/ACL-Anthology-2022-11-21/`（Git忽略） | 逐文件见`data/manifests/nemo-source-v1.manifest.json` | ACL包有1297条标签记录但0张图片、仅匿名本地路径；需作者许可与媒体入口后复核 |
| DS-004 | MVIndEmo | 银标签辅助集 | `SILVER`自动/模型聚合软标签 | https://doi.org/10.1007/s00530-023-01221-8 | SILVER_ONLY_SOURCE_UNAVAILABLE | 论文开放可读；所列GitHub在2026-07-14网页/API均404，数据许可仍UNKNOWN | 未下载 | UNKNOWN | 三模型评论情感融合并按点赞加权已核；只作辅助且不阻塞G1，合法来源恢复前不使用 |
| DS-005 | CUC-IGPE-v2 | 中文外部压力测试 | `SILVER`；非正式人工测试真值 | 工作区外只读根目录由本机`CUC_IGPE_ROOT`配置，不在tracked材料记录绝对路径 | CANONICAL_LOCAL_ONLY_LICENSE_UNKNOWN | PENDING：平台条款、隐私、匿名化和可发布范围审计 | 2026-07-14只读生成；源文件未改写、未复制入项目 | 132个源文件逐文件hash见`data/manifests/cuc-auxiliary-raw-v1.manifest.json`；canonical hash见`cuc-canonical-v1.manifest.json` | 2787条canonical；2815差28条仍UNKNOWN；221冲突显式保留；8条缺BV、0重复BV、883条有时间（含1条跨发布者匹配警告） |
| DS-006 | CH-SIMS processed | 历史构念不匹配辅助资产 | 数据集既有标签；不作为受众群体情绪主证据 | 当前项目已有本地文件，原始来源/许可待回溯 | LOCAL_PRESENT | PENDING：补原始来源、版本和许可记录 | `data/SIMS/Processed/unaligned_39.pkl` | `C9E20C13EC0454D98BB9C1E520E490C75146BFA2DFEEEA78D84DE047DBDD442F` | 回溯下载来源和版本；仅用于历史 MMSA 基线或辅助实验 |
| DS-007 | LIRIS-ACCEDE Discrete | 第二人工主集新候选；本轮唯一深审 | 多人`HUMAN_GOLD`诱发VA秩；不是离散经验分布 | https://liris-accede.ec-lyon.fr/ | NO_GO_CURRENT_AUTHORIZATION_EULA_CONTACT_REQUIRED | 媒体逐源电影CC；annotations/描述CC BY-NC-SA 3.0；EULA限学术且禁再分发 | 未下载 | UNKNOWN | 9800片段/160电影；Protocol A按电影隔离；需另行授权机构EULA，且VA秩无法无损映射JS分布主任务 |
| DS-008 | PMEmo | 第二人工主集元数据候选 | 457名受试者人工VA；逐项分布可用性未知 | https://github.com/HuiZhangDB/PMEmo | NO_GO_LICENSE_SPLIT_AND_LABEL_DISTRIBUTION_UNKNOWN | 仓库软件MIT；数据、MP3、歌词、评论与标注许可不得外推，当前UNKNOWN | 未下载 | UNKNOWN | README称794歌曲/约1.3GB；split未知；评论非T0；音乐VA与公众视频分布只部分匹配 |
| DS-009 | Emotion6 | 第二人工主集元数据候选 | 每图15人、七类诱发情绪经验分布 | https://openaccess.thecvf.com/content_cvpr_2015/papers/Peng_A_Mixed_Bag_2015_CVPR_paper.pdf | NO_GO_MEDIA_LICENSE_ACCESS_AND_MODALITY | 数据许可、现行官方入口和Flickr逐图权利UNKNOWN | 未下载 | UNKNOWN | 1980单图；论文随机7:3；标签构念高度匹配但非视频/多模态且媒体准入未证实 |
| DS-010 | Video Cognitive Empathy (VCE) | 第二视频主集修复候选 | `HUMAN_GOLD`；每视频约13人、27类自身诱发情绪 | https://proceedings.neurips.cc/paper_files/paper/2022/hash/75ff01252ab45ce278cb060effce4ca1-Abstract-Datasets_and_Benchmarks.html | NO_GO_MEDIA_LICENSE_AND_AUDIO | annotations CC BY-SA 4.0、代码MIT；Reddit/Instagram媒体无正式许可，作者依赖美国Fair Use | 未下载 | UNKNOWN | 构念匹配但媒体权利不满足严格合法门；标注时无音频，不冻结为第二多模态主集 |
| DS-011 | LAI-GAI v05 | 第二人工跨域图像主集/缺失模态验证集 | `HUMAN_GOLD`；六项研究逐人诱发评分聚合 | https://www.affectdatabases.amu.edu.pl/ | FROZEN_00_APPROVED | 官方Data Card明确图像/元数据CC BY 4.0；评分OSF组件CC BY 4.0；旧K8XVH空节点与协议偏差只保留为历史观察，新授权从官网847图文件树独立闭合 | `data/raw/lai-gai/second-primary-resolution/20260714/`（Git忽略） | 847图逐图size/SHA-256/dHash见`lai-gai-second-primary-raw-v1.manifest.json`；标签与split见三个`lai-gai-*-v1.manifest.json` | 847/847图像—人工评分闭合；63682个有效逐图反应；379个source group；594/127/126正式split；专项validator全PASS；复审`REVIEW-00-LAI-GAI-FREEZE-20260715` |

## 2. 本地文件快照

| 记录日期 | 文件 | 字节数 | 修改时间（UTC） | SHA-256 | Git策略 |
|---|---|---:|---|---|---|
| 2026-07-14 | `data/SIMS/Processed/unaligned_39.pkl` | 1,228,189,774 | 2026-07-04T14:10:50.3568601Z | `C9E20C13EC0454D98BB9C1E520E490C75146BFA2DFEEEA78D84DE047DBDD442F` | 不纳入 Git；保留本地并后续决定 DVC/对象存储政策 |
| 2026-07-14 | CSMV小型审计资产（10文件） | 14,436,790 | 固定上游commit | 逐文件见`data/manifests/csmv-source-v1.manifest.json` | 原始文件不入Git；manifest和脚本可入Git |
| 2026-07-15 | CSMV官方GitHub浅克隆（同10文件） | canonical Git blobs 14,436,790；pack约4.97 MiB | `99d14240254b1381dde0b9c56add140381f65117` | canonical blob与既有`csmv-source-v1.manifest.json`逐文件一致；Windows工作树8个文本发生LF→CRLF | 克隆位于`data/raw/csmv/upstream-git-20260715/`且不入Git；`.npy`与LFS pointer均为0，不给特征资产门信用 |
| 2026-07-15 | 用户提供CSMV I3D兼容特征包 | 9,942个`.npy`；2,752,998,144 bytes | 官方revision仍UNKNOWN；本地内容revision为树hash | 全包树SHA-256=`35be2d18e1d2413ba3765034cdb454baa5e3496d49c540c9be00e81bbc2c1942`；8,210个必需文件逐文件见`csmv-i3d-quarantine-v1.manifest.json` | 原目录不改动；项目Git忽略junction只读接入；状态`QUARANTINE_ACQUIRED`，不等于正式许可或G2通过 |
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
| CSMV | NeurIPS论文页；官方GitHub固定commit；本地manifest与Strict OOXML结构审计；用户提供I3D兼容包隔离审计 | 正式评论107267条、内部视频8210个；URL表映射覆盖100%；8008个源视频族、202重复族均已group隔离；I3D本地9942文件、8210/8210覆盖、`float32[T,1024]`、逐文件hash | 原始媒体权利/存活率和内容指纹未验证；特征资产级许可、稳定官方revision、提取器版本与权利方fixity attestation仍未取得；不外推媒体或特征再分发权利 |
| iNews | ACL论文页；作者GitHub；HF public固定revision；本地结构审计 | 11320行、2736个post、VAD 1—7、9类Discrete；CC BY-NC-SA 4.0；可按post重划标签 | 图片不在包内；媒体合法恢复率；截图T0去互动量；与论文2899 post差异原因 |
| NEmo+ | ACL论文页与官方Dataset.zip | 1297条新闻、T/I/TI各12970反应、总38910；八类人类诱发情绪 | 包内0图、0许可文件；匿名本地图片路径不可解析；再使用/再分发许可 |
| MVIndEmo | Springer开放论文与论文所列GitHub | 7153视频、8话题；三评论模型融合并按评论点赞加权，属于SILVER | 仓库404；合法数据入口、许可、媒体可得性 |
| LIRIS-ACCEDE | 官方站、database页、官方EULA、IEEE TAC作者公开稿 | 9800个8—12秒视听片段、160电影；多人VA秩；Protocol A按电影隔离 | 数据revision、包字节数/hash、受限XML逐片段许可；EULA邮件门；非离散经验分布 |
| PMEmo | 作者官方GitHub固定仓库commit；README | 794歌曲、457受试者、静态/动态VA；约1.3GB；副歌MP3/特征/歌词/评论/EDA | 数据资产许可、固定数据revision/hash、split和逐项标注分布；评论必须排除T0 |
| Emotion6 | CVPR官方论文 | 1980图像、432受试者、每图15人；七类诱发情绪分布；论文随机7:3 | 现行官方数据入口、许可、包体量/hash、Flickr逐图权利；仅图像模态 |
| VCE | NeurIPS官方论文页与supplement | 约60000视频、400名合格标注者、每视频12—15人；27类自身诱发情绪分布 | Reddit/Instagram媒体无正式许可且标注无音频；包revision/size/hash |
| LAI-GAI | 官方项目页/Data Card、官网图片浏览器、论文v05、OSF DOI、评分组件固定元数据与本地不可变manifest | 官网847图文件树与最终AI评分清单一一闭合；847图逐图hash；12项最小评分文件OSF hash闭合；图像/元数据CC BY 4.0；63682个合规人工反应；00已正式冻结 | 旧K8XVH空列表与0.996519秒偏差不获旧授权门信用；单图域不承担CSMV的视频H1/H2证据 |

下载成功不等于`FIT`。CSMV标签、URL元数据lineage和同源split已由00接受，19项公共核心复现也已由00独立确认当前PASS，但URL hash不能替代正式模型输入资产。LAI-GAI已冻结，G1=`PASS`。按`SC-20260717-01`，`G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`、`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`、总门=`PASS_WITH_ACCEPTED_ASSET_RISK`、全局`formal_split=true`，任务20获内部研究授权。许可、稳定revision与权利方包身份/fixity仍未获确认；禁止I3D再分发及虚构许可信用，权利方否认或hash/覆盖漂移触发停用和结果失效。
