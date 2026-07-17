# Experiment Protocol v2

> 状态：FROZEN_v2  
> 冻结日期：2026-07-16  
> 取代：`experiment-protocol-v1.md`  
> 适用：任务10之后所有数据、模型、检索和评测工作

## 1. 任务时点

### 主任务：T0

在目标视频/帖子发布时预测其未来受众情绪分布。模型只能接收已证明在发布时可用的内容、静态/历史元数据、模态质量信息，以及train或严格更早历史案例。目标评论、最终互动、发布后推荐与任何未来派生特征禁止输入。

### 可选次任务：T+Δ

只有当评论时间戳和内容发布时间覆盖可靠、观察窗口可复现时才启用。输入仅限发布后`[0, Δ]`内的早期反应，目标是预测预先冻结的更晚窗口；必须使用独立配置、字段、split和结果表，不能与T0混报。当前CUC时间覆盖不足，T+Δ为`DISABLED_PENDING_TIME_AUDIT`。

## 2. 统计与数据单位

- 统计单位、划分单位、bootstrap单位：视频、帖子或数据集原生内容单元。
- 评论是同一视频/帖子的重复响应，只用于标签聚合或许可的特权监督；不能当独立样本跨split。
- seed、fold和评论数不得冒充独立统计样本量。
- 近重复内容、同源事件、发布者和话题作为group/OOD审计维度；正式主split优先video/post group，另报告适用的topic/hashtag held-out。

## 3. 标签窗口原则

1. 每个数据集在查看test结果前冻结响应窗口、纳入/排除规则、最少响应数和缺失处理。
2. 主标签是K类经验受众情绪分布；同时保留每个内容单元的有效响应数和分布不确定性。
3. train评论可构造标签和训练teacher；dev评论只用于预注册的选择/校准；test评论只在隔离评测端构造盲评标签。
4. 不同数据集可以使用不同的原生响应窗口，但必须在manifest中显式登记，不能在同一结果表隐式混用。
5. 自动模型生成标签标为`SILVER`，不得与`HUMAN_GOLD`合并或承担test真值。

## 4. 输出与指标

- 主输出：K类概率分布、分布熵/分歧、预测不确定性、可选拒绝分数。
- 主指标：Jensen–Shannon divergence；辅以NLL、Wasserstein/EMD。
- 可靠性：Brier、ECE/ACE、risk-coverage与AURC。
- 统计：至少5个种子，按数据集原生内容单元做paired bootstrap 95% CI，配对检验与多重比较校正。

## 5. 二分类兼容任务边界

- 二分类风险只作为与旧工作兼容的次任务，不取代分布预测主任务。
- 阈值、正类定义与类权重只能在train或预先授权的dev上冻结；不得查看test后修改。
- CUC旧二分类标签存在221条冲突和版本漂移，在canonical解决前仅作历史标签，不得成为新主结论。
- 没有人工真值的CUC-IGPE-v2不得报告准确率、F1或校准提升为核心证据。
- 二分类报告使用Macro-F1、Balanced Accuracy、AUPRC和Recall，不以单一Accuracy作为成功门。

## 6. Split、拟合与索引

1. 先按内容单元完成train/dev/test，再聚合可跨样本传播的信息、构图或建索引。
2. 归一化、插补、PCA、特征选择、聚类、阈值和原型只在train拟合；dev仅用于预注册选择。
3. 主索引只包含train；有可靠时间戳时还要求`candidate_publish_time < query_publish_time`。
4. 同一内容/source group、同作者捷径、同源事件和近重复不得跨正式split；group/topic held-out结果优先于随机split。
5. 随机split可作为诊断对照，但不得作为唯一主结果或论文成功证据。

## 7. 实际可得输入与缺失模态资格

1. `ALL_AVAILABLE_INPUTS`只表示数据协议在T0合法、冻结且实际可得的全部输入，不表示理论上可能存在的音频、原始帧或未来评论。
2. CSMV音频固定为`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`；不得用零向量、生成音频或代理变量补齐，音频分支固定为`NOT_APPLICABLE_AUDIO_UNAVAILABLE_BY_DATASET_DESIGN`。
3. E1逐模态增量、E5随机缺失率与H3缺失模态鲁棒性只在同一样本至少含两个实际T0输入模态的数据协议上有资格运行。只有一个模态时登记`NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`；项目无合格协议时H3登记`NOT_APPLICABLE_NO_ELIGIBLE_MULTIMODAL_PROTOCOL`。
4. 评论文本只可用于标签、训练期特权教师或train-only反应记忆，不得在T0学生推理时与视觉特征组合成所谓“完整多模态输入”。
5. CSMV与LAI-GAI之间的视频/图像域差异属于跨域/结构性输入边界，不能替代同一样本随机删除模态的实验。

## 8. 证据资格与失败状态

- 运行必须绑定数据版本、split版本、标签窗口、T0/T+Δ、实际输入模态、seed、baseline、主指标和停止条件。
- 预测文件必须反查到配置、代码提交、数据manifest、模型和索引manifest。
- 任一目标评论、未来互动、未来候选、跨split实体、test拟合或全图穿越检查失败，运行立即标为`LEAKAGE_BLOCKED`，结果不得进入论文。
- 旧实验资格按`legacy-experiment-classification.md`执行；高分不能覆盖协议失败。

## 9. CSMV冻结I3D序列合同

1. CSMV当前唯一候选T0内容输入为冻结I3D视觉表征`float32[T,1024]`；允许主张仅限“冻结I3D视觉表征上的公众诱发受众情绪分布预测”。不得声称端到端视频编码、原始帧学习、音视频融合、音频增益或评论文本T0输入。
2. 查看test结果前冻结主规则`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`：保留完整序列，batch内右补零，布尔mask中`True`表示真实时间步；固定长度分桶与输入张量上限见`configs/csmv-i3d-sequence-protocol-v1.json`。
3. 主敏感性规则为`UNIFORM_180_ENDPOINT_INCLUSIVE`：长序列用包含首尾的180个确定性均匀索引，短序列保留并右补零；`FIRST_180_ONLY_FIXED_DIAGNOSTIC`只作预注册补充，不得按test结果改变等级。
4. 空序列、坏shape、非`float32`或非有限值一律拒绝；所有split同规则，无test覆盖、无随机性、无标签依赖。协议全文及fixity证据见`CSMV_I3D_SEQUENCE_PROTOCOL_V1.md`和对应manifest。
5. E1的`ALL_AVAILABLE_INPUTS`在CSMV即I3D单输入；E5为`NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`。完整序列与180步是同一视觉模态的处理消融，不得冒充模态增量或缺失模态实验；H3资格保持条件化。
6. 许可、稳定revision和权利方包身份/fixity证明为`DEFERRED_ACCEPTED_RISK`，不是已解决或已获权利方确认。按`SC-20260717-01`，`G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`、`formal_split=true`，任务20获内部研究授权；禁止再分发I3D，论文必须披露风险。权利方否认或资产hash/覆盖漂移时，相关运行立即失去正式证据资格。

## 10. 变更纪律

本协议如需变更必须发布新版本，记录理由、受影响实验和重跑清单。不得为改善test表现而改T0、窗口、阈值、主指标、模态资格或split。
