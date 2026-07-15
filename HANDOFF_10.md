# HANDOFF_10：M1—M2数据与协议交接

> 提交给：任务00总控审核
> SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.13 第17节任务10
> 交接日期：2026-07-16
> 提交状态：00已接受I3D序列协议与Git检查点；G1通过，复现陈旧和序列协议子阻塞关闭，G2仅保留CSMV输入资产准入阻塞

## 请求的审核结论

00已确认以下状态，且未放行任务20：

- 步骤34—39本地可执行交付是否达到任务10文档与自动化要求；
- G1=`PASS`；
- LAI-GAI=`FROZEN_00_APPROVED`，唯一正式split为379组、594/127/126；
- CSMV媒体元数据lineage与同源split已由00接受；`REVIEW-00-CSMV-FEATURE-PREFLIGHT-G2-20260715`又关闭当前复现陈旧子阻塞；G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；全局`formal_split=false`。

本轮新增已获00裁定证据：

- `reproducibility-v1`已更新为当前source-family版本：Python `-I -S`、`PUBLIC_BENCHMARK_CORE`、19项输出、漂移0、现场hash复核通过；CUC只按冻结字节核验，不再依赖历史外部源根。
- CSMV特征预审为`NO_GO_PENDING_ASSET_METADATA_AND_LICENSE`：官方README的I3D/VideoMAE发布与命名规则可定位，但公开Drive首屏没有许可、revision、文件树、体量、checksum或8210实际键清单。

## 2026-07-14 第二主集收口增量交接

- 依据`AUTH-00-SECOND-PRIMARY-RESOLUTION-20260714`及`REVIEW-00-LAI-GAI-FREEZE-20260715`，LAI-GAI已正式冻结为`FROZEN_00_APPROVED`：847张官网图像、63682个合规逐图人工反应、100%图像—评分lineage。
- 许可与版本：官网Data Card明确图像/元数据CC BY 4.0；评分组件8P572固定到`2026-03-11T20:48:23.318238`；12项最小评分文件和847图均有本地size/SHA-256。
- 标签：只使用12个1—7人工诱发评分；减去量表下界1后归一化为连续分布，保留各维N/SD/SE/直方图；prompt、目标类别与生成模型字段不是真值且不进入输入。
- split：379个source group，train/dev/test=`594/127/126`；source item、文化/年龄/性别变体、同prompt、精确重复和dHash近重复均不跨split，专项Critical为0。
- 原始逐人记录与图像只在Git忽略目录；tracked manifest和canonical均不含参与者ID、Prolific ID、人口统计、设备或完成日期。
- 00已通过`REVIEW-00-LAI-GAI-FREEZE-20260715`完成复审：第二主集正式冻结并放行G1；G2与全局`formal_split=false`保持阻塞，任务20仍禁止。

## 本轮交付

- 可阻断泄漏门：`scripts/run_m2_leakage_tests.py`；负面自测会产生预期`LEAKAGE_BLOCKED`。
- 受门控发布构建器：`scripts/build_m2_release.py`；泄漏失败时不写release manifest。
- 版本化候选：`dataset-v1.manifest.json`、`split-v1.manifest.json`、`label-provenance-v1.manifest.json`。
- 数据文档：Data Card、Datasheet、隐私、平台条款、发布边界、数据审计报告。
- 隔离复现：`scripts/reproduce_m2_minimal.py --public-core`与`reproducibility-v1.manifest.json`；当前19项before/after hash一致，release validator现场重算0漂移。
- 正式输入预审：`CSMV_FEATURE_ASSET_PREFLIGHT_20260715.md`、`csmv-feature-preflight-v1.manifest.json`及`validate_csmv_feature_preflight.py`；审计合同通过，但资产准入本身为No-Go。
- G门证据：`G1_G2_EVIDENCE_MATRIX.md`。

## 关键结果

- CSMV：8210内部视频、107267条正式评论反应；官方URL表形成8008个平台源视频族，202个重复族已先归并后划分；video/hashtag split同源交叉均为0。
- CUC：2787条银标，221冲突、8缺BV、1904缺时间、历史漂移28，许可未知；仅辅助、本地。
- 泄漏自动门覆盖ID、source group、评论—视频归属、目标评论、未来候选、train-only索引、time split合同和fit范围。
- 时间检查为`NOT_APPLICABLE_NO_TIME_SPLIT`，因为CSMV无发布时间；不能解释为已证明时间安全。
- 语义近重复、同源事件与发布者捷径因媒体/元数据不足仍是开放风险。

## 禁止下游动作

在任务00明确通过G2以前，不创建任务20、不启动M3训练、不安装faiss以宣称正式环境就绪、不构建正式检索索引。LAI-GAI可写为已冻结第二人工跨域图像主集，但dataset-v1整体仍不是G2正式benchmark。

## 建议决定

00已接受公共benchmark核心复现子门关闭，并把G2剩余缺口收敛为CSMV正式输入资产。`AUTH-00-CSMV-ONE-FEATURE-FAMILY-METADATA-COORDINATION-20260715`已用于官方Issue #5；后续效率政策允许在等待回复期间从官方副本或可信镜像隔离预取公开候选特征，但不授权正式使用、发布或G2放行。

首次GitHub Issues发送尝试因集成缺少写权限返回403，未生成issue number/URL、外部写入为0。00已签署`REVIEW-00-CSMV-I3D-METADATA-COORDINATION-ATTEMPT-20260715`：这不是权利方拒绝，一次正式请求额度未消耗；后续仅可在同一官方Issues渠道二选一，使用`CSMV_I3D_GITHUB_ISSUE_REQUEST_20260715.md`手工提交，或补足连接器创建Issue权限后重试一次。G2与`formal_split=false`不变。

用户已于2026-07-15在同一官方渠道成功创建公开Issue #5：`https://github.com/IEIT-AGI/MSA-CRVI/issues/5`。现场核验其为`IEIT-AGI/MSA-CRVI`的Open Issue，正文覆盖授权要求的许可、revision、relative path/bytes/SHA-256 manifest、8210覆盖、特征schema与总体量，并声明在独立复审前不下载特征。正式请求额度已使用；不得重复创建或切换第二渠道。2026-07-22前不得跟进，收到回复后先交00书面复审。G2、`formal_split=false`和任务20禁令不变。

00已签署`REVIEW-00-CSMV-OFFICIAL-ISSUE-5-SENT-20260715`确认上述发送状态。公开正文没有逐字点名I3D，因此不得写成“维护者已收到明确I3D限定”；若2026-07-22及以后仍无回复，唯一一次同Issue跟进应明确I3D优先范围。

## 2026-07-15 I3D本地隔离取得增量交接

- 用户提供本机I3D特征包；任务10未重新下载或改写源文件，在Git忽略目录建立`visual_feature/I3D` junction，tracked材料不记录绝对源路径。
- 审计9,942个`.npy`、2,752,998,144 bytes；8,210个CSMV必需`video_file_id`全部覆盖，缺失0、附加1,732。
- 全部数组为`float32[T,1024]`，`T=6—1719`，schema错误0；8,210个必需文件逐文件bytes/SHA-256已写入`csmv-i3d-quarantine-v1.manifest.json`。
- 全包内容树SHA-256为`35be2d18e1d2413ba3765034cdb454baa5e3496d49c540c9be00e81bbc2c1942`；加载器支持官方`video_file_id`与canonical `item_id`，只读mmap且不接触标签正文。
- 当前裁定仅为`QUARANTINE_ACQUIRED_LICENSE_REVISION_ATTESTATION_PENDING`。请00复核本地fixity/schema/覆盖证据；资产级许可、稳定官方revision和权利方attestation仍需Issue #5回复，任务10不自行放行G2或任务20。

## 2026-07-16 音频缺失非阻塞裁定（00已签署）

- 00已签署`TASK00_AUDIO_MODALITY_PROTOCOL_REVIEW_20260716.md`，正式裁定为`PASS_WITH_LIMITATIONS_AUDIO_NOT_REQUIRED_FOR_PRIMARY_PROTOCOL`。
- 依据T-AFFC官方范围、CSMV固定README、NeurIPS 2024正式论文及总纲v1.12，音频不是期刊投稿或任务10 G2条文的硬性必备模态；CSMV官方当前本就只发布视觉特征并把音频列为未来工作。
- 音频已冻结为`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`并移出G2、任务20启动条件和后续取得关键路径。允许继续视觉特征下游预测、评论特权监督、检索、校准、OOD和拒绝研究；禁止音视频融合、音频增益、音频随机缺失鲁棒性和伪音频主张。
- E1统一使用`ALL_AVAILABLE_INPUTS`；只有一个T0内容模态时，逐模态增量记`NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`。音频分支固定为`NOT_APPLICABLE_AUDIO_UNAVAILABLE_BY_DATASET_DESIGN`。
- E5/H3的随机/自然缺失实验只在同一样本至少含两个T0合法、冻结、实际可得输入模态时运行；若无合格协议，H3降为`NOT_APPLICABLE_NO_ELIGIBLE_MULTIMODAL_PROTOCOL`。
- 该裁定不关闭I3D资产许可/revision/包身份阻塞，不修改G2、`formal_split=false`或任务20禁令。

## 2026-07-16 I3D序列协议与论文主张冻结回交

- 8,210个正式I3D输入中531个`T>180`、4个`T=180`、范围6—1,719；在任何训练和test结果前冻结`CSMV_I3D_SEQUENCE_PROTOCOL_V1.md`。
- 主协议=`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`：完整保留序列，batch内右补零，布尔mask中`True=observed`；确定性长度分桶，`max_batch_size=64`、原始输入张量上限16,384 padding后时间步/64 MiB。最长单样本约6.71 MiB，当前没有资源证据要求降级。
- 主敏感性=`UNIFORM_180_ENDPOINT_INCLUSIVE`：长序列首尾覆盖的确定性180步，短序列保留并补零；`FIRST_180_ONLY_FIXED_DIAGNOSTIC`仅为预注册补充，不得按test表现升级。
- `tests/test_csmv_i3d_sequence_protocol.py`覆盖正向、最长边界、重复hash、错误shape、空序列、非float32、非有限值、资源超限及test自适应拒绝；专项validator状态=`PASS_PREREGISTRATION_ONLY_G2_UNCHANGED`。
- 论文只允许声称冻结I3D视觉表征上的公众诱发受众情绪分布预测；不得声称端到端视频编码、原始帧学习、音视频融合、音频增益或评论文本T0输入。E1/E5/H3按`experiment-protocol-v2.md`实际单输入合同执行。
- 维护者许可/revision/权利方包身份与fixity证明按用户指令暂记`DEFERRED_PENDING_MAINTAINER_REPLY`。本轮不等待、不催促、不重复检查，也不写成已解决。
- 门状态保持：G1=`PASS`；G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；全局`formal_split=false`；未创建任务20、未训练、未建立正式索引。

## 2026-07-16 I3D序列协议与Git检查点复审（00已签署）

- 00已签署`TASK00_CSMV_I3D_SEQUENCE_PROTOCOL_AND_GIT_CHECKPOINT_REVIEW_20260716.md`，裁定`ACCEPTED_PREREGISTRATION_ONLY_G2_UNCHANGED`。
- 00现场复核协议manifest SHA-256=`208615d4059afc8c5c2c57a5ffc13eeafa9a71ece861332d9f1cd62bc9c4d5be`及6个证据文件hash；8项单测、专项validator、泄漏正负门、19项隔离重放、M2 release和综合准备均通过。
- 正式关闭`I3D_SEQUENCE_PROCESSING_PROTOCOL_UNFROZEN`子缺口；主协议、两级敏感性、资源门和论文主张边界不得按test结果改变。
- 审核基线`cf6dea18ddb057da91e90d6c0104e3e854f1724a`在复审开始时与`origin/main`一致且工作区干净；tracked `.npy`、特征包和超过10 MiB文件均为0。
- 维护者证明继续`DEFERRED_PENDING_MAINTAINER_REPLY`。剩余G2缺口只有资产级许可、稳定官方revision、包身份与权利方fixity；`formal_split=false`，任务20仍禁止。
