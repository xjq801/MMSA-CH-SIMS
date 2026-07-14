# M1 公开数据许可与可用性审计

> 版本：v1.0
> 审计日期：2026-07-14
> 范围：总纲 v1.5 第17节任务10步骤11—18
> 结论：CSMV小型标注包可审计且可按视频重划分；iNews与NEmo+当前均不能作为可复现的第二多模态主集，G1继续阻塞。

## 1. 下载边界与可复现入口

本轮只下载许可和体量已核明、用于结构审计的小型公开资产。没有下载视频、图片、I3D/VideoMAEv2特征、persona数据或任何付费资源。下载脚本为`scripts/fetch_m1_public_assets.py`，结构审计脚本为`scripts/audit_m1_public_assets.py`。

| 数据源 | 固定版本 | 本地原始资产 | 实际下载体量 | SHA-256记录 |
|---|---|---:|---:|---|
| CSMV | Git commit `99d14240254b1381dde0b9c56add140381f65117` | README、LICENSE、标注、映射、官方split、`video_to_comment`、URL清单 | 14,436,790 bytes | `data/manifests/csmv-source-v1.manifest.json` |
| iNews public | HF revision `a7ad599a257e94f04f796a86d39635adadb5f7cb` | README、codebook、5个公开CSV | 26,502,742 bytes | `data/manifests/inews-source-v1.manifest.json` |
| NEmo+ | ACL附件，Last-Modified 2022-11-21 | 官方Dataset.zip，仅用于许可/结构检查 | 2,080,204 bytes | `data/manifests/nemo-source-v1.manifest.json` |

原始资产位于Git忽略的`data/raw/`；Git只跟踪脚本、统计结果和manifest。磁盘审计时D盘可用空间约75.68 GB，以上资产不触发采购或扩容。

## 2. CSMV / MSA-CRVI

### 2.1 来源、许可与文件

- 论文入口：NeurIPS 2024 Datasets and Benchmarks；官方仓库：`IEIT-AGI/MSA-CRVI`。
- 仓库根`LICENSE`为Apache-2.0；README另称代码MIT、annotations为CC BY-SA 4.0。标注下载依据是README中针对annotations的明确声明；代码许可的MIT/Apache不一致保持为已知限制。
- TikTok媒体、原始URL和Google Drive特征不因仓库/标注许可自动获得再分发权。本轮不下载媒体或特征，相关权利、体量、版本和SHA保持`PENDING/UNKNOWN`。
- 官方`CSMV_rawLinks.xlsx`已按固定commit下载并核hash；表格工具两次因上游theme中的非法OpenXML百分比值无法导入，因此URL清单的行级覆盖率仍为`PENDING`，不据此宣称媒体可恢复。

### 2.2 标签结构与聚合单位

结构审计确认官方正式split共107,267条评论，标注归档另含117,057条记录。正式split中的每条记录共同具备：`comment`、`emotion_label`、`hashtag`、`opinion_label`、`video_file_id`。其中：

- `video_file_id`缺失数为0；`video_to_comment.json`覆盖8,210个视频；
- `hashtag`缺失数为0，共35个不同值；没有原生`topic`字段；
- opinion为positive/neutral/negative，但有5条`None`；emotion为Plutchik八类，但有1条`None`；这些异常不得静默填充；
- 评论可按`video_file_id`聚合为视频级经验分布，并保留评论数、类别计数、概率和不确定性。

### 2.3 官方split泄漏与重划分可行性

| 检查 | 结果 |
|---|---:|
| train/dev/test评论数 | 75,086 / 10,727 / 21,454 |
| 评论ID跨split重复 | 0 |
| train/dev/test涉及视频数 | 8,190 / 5,833 / 7,360 |
| train∩dev视频 | 5,819 |
| train∩test视频 | 7,341 |
| dev∩test视频 | 5,332 |
| 同时出现在三个split的视频 | 5,319 |

因此官方comment-ID随机split对本研究是明确的视频级泄漏，禁止沿用。`group-by-video`可构造；`hashtag-held-out`可构造；`topic-held-out`只能在先冻结“hashtag→topic”映射后构造，不能把模型或测试结果反向用于话题归并。正式`split-v1`尚未生成，本轮结论只是结构可行性通过。

## 3. iNews

### 3.1 许可、标注与公开包

- 论文报告2,899个Facebook新闻帖、291名参与者、平均5.18名标注者；含1—7的V/A/D和九类离散情绪。
- HF公开非persona版许可证为CC BY-NC-SA 4.0，固定revision含11,320行、2,736个唯一`Post_ID`。相对论文少163个帖子（5.62%），差异原因未在当前证据中完全解释，保持`UNKNOWN`。
- 每行有`Post_ID`、`Annotator_ID`、文本描述、V/A/D、Discrete、Source、Relevance和场景/话题分类等字段；每帖公开标注数范围1—6，中位数4。
- 公开文件之间存在任务设计导致的post重叠：generalization-test与train重叠1,214个post；cold-start-test与personalization-test重叠343个post。若用于本项目，必须丢弃原任务split并按`Post_ID`重新划分。

### 3.2 媒体与T0风险

公开包没有图片文件，也没有可直接消费的图片路径/URL字段。作者仓库要求另行依据Facebook内容恢复图片，并提醒遵守平台条款、限速、伦理与法律。论文说明标注者看到的截图保留reaction count、但排除comments；reaction count属于发布后互动量，`available_at_t0=false`。即使未来合法恢复图片，也必须先证明裁剪/遮挡后互动量物理为零，才能进入T0输入。

当前不能从固定公开revision重建与标注时一致的多模态输入，媒体版权、帖子存活率和截图去泄漏均未通过，因此iNews对“第二人工标注多模态主集”的裁定为`NO_GO_PRIMARY_2026-07-14`。公开标签包可保留为只读标签研究材料，但不能冒充完整多模态benchmark。

## 4. NEmo+切换审计

按同一标准审计ACL官方附件：

- 1,297条新闻记录，T/I/TI各12,970条人类反应，总计38,910条；每个条件每条新闻10人标注；
- 八类为Amusement、Anger、Awe、Contentment、Disgust、Excitement、Fear、Sadness，另有1—5强度和匿名自由文本理由；
- 附件中没有图片文件；1,297个图片引用均为`anonymous-source/*.jpg`形式的本地相对路径，不能从附件恢复；
- 附件没有LICENSE/COPYING，论文只说明研究中获准使用BU-NEmo，不能替代对NEmo+再使用/再分发许可的明确授权。

因此已执行从iNews切换到NEmo+的审计动作，但NEmo+当前裁定为`NO_GO_PRIMARY_PENDING_LICENSE_AND_MEDIA`。恢复条件是作者或权利方提供明确研究许可、可追溯图片输入及稳定获取说明；在恢复前不进入正式测试。

## 5. MVIndEmo银标边界

论文说明7,153个TikTok微视频覆盖8个话题。标签不是人工受众真值，而是三个评论情感模型的置信融合结果，再按评论点赞加权聚合；同时提供hard label和soft distribution。论文列出的官方GitHub仓库在2026-07-14网页和GitHub API核验均返回404。

固定裁定：`SILVER_ONLY_SOURCE_UNAVAILABLE`。若将来获得合法来源，只能用于训练适配、迁移或压力测试，不能进入人工金标主表、正式测试真值或G1“第二人工标注主集”计数；其不可得不阻塞G1。

## 6. 当前门状态

| 门 | 当前状态 | 证据 |
|---|---|---|
| G1：至少两个合法可用公开源 | **BLOCKED** | CSMV标注结构通过，但iNews与NEmo+都未形成合法可复现的第二多模态输入；自建真实时间问题也未在本工作包解决 |
| G1：CSMV按视频分组可构造 | **PASS（结构级）** | 8,210个视频均有`video_file_id`映射；正式split尚待M2冻结 |
| G2/L2 | **NOT_EVALUATED / BLOCKED_BY_G1** | 尚无两个公开集正式split，尚未形成全部样本lineage与零失败泄漏测试 |

未过G1/G2前，不创建任务20，不训练CARM，不下载大媒体/特征包，不调用付费LLM或API。
