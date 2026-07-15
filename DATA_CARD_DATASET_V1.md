# Dataset Card：dataset-v1

> 状态：`LOCAL_CANDIDATE_G1_PASS_G2_BLOCKED`；LAI-GAI第二主集已`FROZEN_00_APPROVED`  
> 版本日期：2026-07-16  
> 权威机器清单：`data/manifests/dataset-v1.manifest.json`

## 数据集摘要

dataset-v1是M2阶段的本地发布候选，不是可用于正式模型训练或论文主结果的已放行benchmark。第一人工主集CSMV将107,267条人工评论反应按8,210个内部视频聚合，并通过官方URL元数据归并为8,008个源视频族；第二人工跨域图像主集LAI-GAI含847图与63,682个人工反应。G1已通过，CSMV lineage/split修复已由00接受，当前19项公共核心复现零漂移；本地I3D的schema与8210/8210覆盖已闭合，G2剩余阻塞为资产级许可、稳定官方revision及权利方包身份/fixity确认。

## 预期用途

- 审计公众诱发受众情感分布的标签工程、split和泄漏边界。
- 在G1/G2通过后，作为T0内容侧预测的版本化输入合同。
- 复核标签不确定性、标签冲突与数据缺陷。

当前禁止用途：正式模型比较、正式论文优越性证据、银标与人工test合并、个体用户画像、内容审核自动裁决、政治定向、重新识别或平台用户追踪。

## 数据组成

| 层级 | 数据源 | 记录 | 标签性质 | 当前资格 |
|---|---|---:|---|---|
| `HUMAN_GOLD` | CSMV固定commit | 8,210视频 | 人工评论标签聚合分布 | 当前唯一主集 |
| `SILVER` | CUC-IGPE-v2遗留本地数据 | 2,787视频向量行 | 遗留二分类银标，教师/置信度未知 | 辅助、本地、不可并入test |
| `UNLABELED` | 预留 | 0 | 无 | 空入口 |
| `HUMAN_GOLD`第二主集 | LAI-GAI v05 | 847图 | 12维人工诱发连续分布 | `FROZEN_00_APPROVED` |

评论正文、用户标识、媒体、原始URL、发布者名称和CUC源文件均不在Git发布候选中。

## 标签与构念

目标构念为`public-induced audience affect`，不是说话者情感、画面人物群体情绪或传播链结果。CSMV评论只提供标签监督；其文本和未来互动不得作为T0输入。CUC标签固定为银标，221条冲突、28条2815/2787漂移和教师来源未知均不被抹平。

## Split

- `group_by_video_v1`：平台源视频族互斥，当前5698/837/1675。
- `hashtag_heldout_v1`：同源族与hashtag连通分量共同互斥，当前7211/327/672。
- `topic_heldout_v1`：CSMV无原生topic，未分配。
- 时间split：CSMV无发布时间，未发布，也不声明时间安全。
- 索引：未建立；未来仅允许train候选。

本地候选split在可观察ID/source-group范围内零Critical、第二主集已冻结且当前隔离复现已关闭；正式输入资产准入闭合并由00书面批准G2后才能升级为正式split。当前`formal_split=false`。

## 已知限制与偏差

- 第二人工集按批准范围为跨域单图而非第二视频集；不能声称双视频主集，H1/H2在LAI-GAI为不适用。
- 00已通过`REVIEW-00-AUDIO-MODALITY-PROTOCOL-20260716`将CSMV音频冻结为`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`并移出G2/取得关键路径；本项目不得伪造或插补音频，也不得声称音视频融合、音频增益或音频随机缺失鲁棒性。E1使用`ALL_AVAILABLE_INPUTS`；只有一个T0内容模态时，逐模态增量为`NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`。
- CSMV平台、语言、内容分布和评论者选择机制可能造成代表性偏差；经验分布不是总体公众因果效应。
- CSMV正式输入已收敛到I3D候选。其本地文件树、体量、逐文件hash、`float32[T,1024]` schema及8210/8210覆盖已闭合；资产级许可、稳定官方revision及权利方包身份/fixity仍为`DEFERRED_PENDING_MAINTAINER_REPLY`，因此不得正式训练或发布主结果。
- I3D序列处理在查看test结果前冻结：主协议保留完整序列并使用动态padding/attention mask；主敏感性协议确定性均匀采样至180步，前180仅作补充。规则、资源上限及负面拒绝见`CSMV_I3D_SEQUENCE_PROTOCOL_V1.md`。
- 论文输入主张只限冻结I3D视觉表征，不覆盖端到端视频编码、原始帧学习、音视频融合、音频增益或评论文本T0输入。
- 当前`reproducibility-v1`已在Python `-I -S`公共核心模式下重建并由00独立复核，19项before/after与现场hash零漂移；后续任何数据或文档变化仍须重新构建和验证。
- CUC许可未知、本地限定，48维遗留特征未证明T0可得，不能进入正式输入。
- 自动泄漏测试是可机读否决门，不是所有语义泄漏的完备证明。

## 维护与版本化

原始manifest不可变；任何标签映射、split、标签层级或发布边界变化必须升版，并重新生成泄漏、复现与G门证据。test结果不得用于修改映射。问题应记录到工作日志和对应数据台账，不得静默修补。
# LAI-GAI第二人工跨域图像集增量

- 角色：跨域图像/缺失模态、校准/OOD与H3边界验证；不替代CSMV的视频多模态H1/H2证据。
- 样本：847张AI生成情感图像，63682个通过`consent=YES/useData=Yes/rating_cat=0`的逐图人工反应；每图58—96个反应。
- 真值：12个1—7诱发情绪强度构成的预注册连续分布；prompt和目标情绪只作provenance。
- 许可：官方Data Card标注图像与元数据CC BY 4.0；OSF评分组件CC BY 4.0。
- 隐私：公开canonical仅含聚合N、均值、SD、SE、直方图和分布；逐人标识及人口统计不发布。
- 限制：单图、合成域、负性内容受生成平台安全策略约束；不能外推为真实视频平台因果结论。
