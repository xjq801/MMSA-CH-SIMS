# M2 数据工程与标签隔离协议 v1

## 冻结边界

- 先按视频/帖子或更高层group划分，再允许训练集内建索引、拟合预处理或采样。
- CSMV评论只在单个内部视频ID内聚合，输出经验分布、有效评论数、熵、最大类占比、有效类别数和逐类二项标准误；不输出评论正文。split之前再用官方URL表把内部ID归并为平台源视频族，所有协议必须保持同一源族不跨split。
- `group-by-video-v1`使用固定salt的哈希划分；`hashtag-held-out-v1`按hashtag—视频二部图连通分量划分，保证同一hashtag分量不跨split。
- CSMV没有原生topic，`topic-held-out`保持`BLOCKED_NATIVE_TOPIC_ABSENT`，不得把hashtag改名为topic。
- 任何检索索引状态在M2固定为`NOT_BUILT`；后续只能读取train记录建索引。

## 第二主集映射

LAI-GAI v05已由`REVIEW-00-LAI-GAI-FREEZE-20260715`冻结为第二人工跨域图像主集：847图、63,682条合规人工响应、379组、594/127/126唯一split。`LABEL_SPACE_MAPPING_DRAFT.md`及`data/manifests/second-primary-label-map-v1.manifest.json`只能按该冻结合同升版，不得恢复旧266组试算，也不得依据test结果改类别。

## 实际可得输入与音频边界

- CSMV音频按`REVIEW-00-AUDIO-MODALITY-PROTOCOL-20260716`冻结为`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`，不是G2独立前置条件，也不进入后续取得关键路径。
- CSMV正式内容输入只允许一个经00准入的视觉特征族；评论是标签/训练期特权监督，不是T0学生推理输入。
- `ALL_AVAILABLE_INPUTS`只包含T0合法、冻结且实际可得的输入。只有一个内容模态时，不运行逐模态增量或随机缺失实验，登记`NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`。
- 任何全零、生成或代理音频均不得进入数据、模型、消融或论文主张。

## 近重复与发布者捷径边界

当前可机械检查精确item/group重复、官方URL源视频族、hashtag分量交叉、重复BV和发布者字段可用性。CSMV的8210条内部ID→URL映射形成8008个源族，202重复族必须先归并后划分；媒体未下载且无发布者元数据，因此内容感知哈希、不可观察近重复和发布者捷径仍标记为`UNKNOWN/NOT_TESTABLE_WITH_CURRENT_ASSETS`。

## CSMV I3D序列处理冻结

- 输入固定为`float32[T,1024]`；空序列、坏shape、非float32及NaN/Inf fail-closed。
- 主协议`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`完整保留所有时间步，batch内右补零，`True=observed`；固定长度分桶与64 MiB原始输入张量上限只控制batch大小，不截断样本。
- 主敏感性`UNIFORM_180_ENDPOINT_INCLUSIVE`覆盖首尾；短序列只补零。前180步固定为补充诊断，不能按test结果替换主敏感性。
- 规则只依据输入shape，所有split同配置，无随机性、无test覆盖。该协议不读取标签、不训练、不建索引。
- 协议可复现不等于资产可正式使用；维护者证明=`DEFERRED_PENDING_MAINTAINER_REPLY`，G2与`formal_split=false`不变。

## 标签层级

- `HUMAN_GOLD`：公开人工标注经视频级聚合后的标签。
- `SILVER`：模型、规则或遗留统计流程生成的标签；教师或置信度未知时必须显式写`UNKNOWN`。
- `UNLABELED`：无标签输入或ID映射，不得混入标签评测。

加载器一次只接受一个层级。公开人工test标签永不与银标合并；银标只能进入单独适配/敏感性流程，且不能替代G1第二人工主集。
