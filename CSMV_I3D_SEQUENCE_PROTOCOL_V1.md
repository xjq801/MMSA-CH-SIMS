# CSMV I3D序列处理协议 v1

> 冻结日期：2026-07-16  
> 状态：`PREREGISTERED_BEFORE_TEST_RESULTS`  
> 适用输入：CSMV冻结I3D视觉表征，`float32[T,1024]`  
> 正式资产边界：仍为隔离候选；本协议不授予许可、G2或正式split信用

## 1. 冻结依据

8,210个CSMV必需I3D文件的输入长度审计显示：`T=6—1719`，531个`T>180`，4个`T=180`，中位数43、P90=133、P95=211、P99=339。官方README同时写有“max tensor length 180”。如果在查看test结果后才选择截断、采样或保留完整序列，会产生结果驱动的协议选择风险，因此本规则在任何训练和test评测前冻结。

规则选择只使用输入shape与资源约束，不读取test标签、评论正文或模型结果。

## 2. 主协议：完整序列

主协议固定为`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`：

- 保留每个样本全部`T`步，不截断、不采样、不池化；
- batch内右侧补零到该batch最大长度；mask为布尔数组，`True`表示真实观测步，`False`表示padding；
- 所有split使用完全相同的规则、代码和配置，不允许test专属覆盖；
- 使用固定长度桶`32/64/128/256/512/1024/2048`规划batch，桶内按`(T,item_id)`稳定排序；不随机打乱序列处理规则；
- `max_batch_size=64`，每批原始输入张量最多16,384个padding后时间步，即64 MiB `float32`特征值。此上限只约束输入张量，不代表未来模型激活、梯度或优化器的总显存；超限时减小batch而不是截断样本；
- 当前最长1,719步的单样本约6.71 MiB，可在上述输入上限内完整保留。因此现有资源画像没有触发从主协议降级为180步规则的证据。

## 3. 主敏感性协议：均匀180步

主敏感性规则固定为`UNIFORM_180_ENDPOINT_INCLUSIVE`：

- `T<=180`：保留全部观测，右侧补零至180并产生mask，不重复短序列观测；
- `T>180`：用180个严格递增、包含首尾端点的确定性整数索引覆盖完整时间轴；无随机种子、无标签依赖；
- 选择均匀采样而非前180步，是因为前180会对531个长序列系统性删除尾段，而均匀采样保持全时间覆盖；
- `FIRST_180_ONLY_FIXED_DIAGNOSTIC`预先登记为补充诊断，不得根据test表现升级为主敏感性结果。

## 4. 输入拒绝与重复性

空序列、非二维数组、尾维非1024、非`float32`、NaN或Inf全部拒绝，不做隐式转换或修复。实现不访问标签、评论、互动量或split表现。相同输入、配置和顺序必须产生逐字节相同的特征、mask、索引与batch计划。

机器可读配置：`configs/csmv-i3d-sequence-protocol-v1.json`。  
机器可读证据：`data/manifests/csmv-i3d-sequence-protocol-v1.manifest.json`。  
实现：`scripts/csmv_i3d_sequence_protocol.py`。  
验证：`scripts/validate_csmv_i3d_sequence_protocol.py`与`tests/test_csmv_i3d_sequence_protocol.py`。

## 5. 论文与实验边界

本协议只支持“冻结I3D视觉表征上的公众诱发受众情绪分布预测”。不得据此声称端到端视频编码、原始帧学习、音视频融合、音频增益或把评论文本作为T0学生输入。音频保持`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`。

E1在CSMV上只有一个实际T0内容模态，`ALL_AVAILABLE_INPUTS`即I3D，逐模态增量为`NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`。E5/H3的缺失模态分支不因完整序列与180步处理方式而获得资格；若无其他同样本多输入协议，H3为`NOT_APPLICABLE_NO_ELIGIBLE_MULTIMODAL_PROTOCOL`。主协议与180步敏感性只构成视觉序列处理消融。

维护者许可、稳定revision和权利方包身份/fixity证明按用户指令暂记`DEFERRED_PENDING_MAINTAINER_REPLY`。这不是已解决：G1保持`PASS`，G2保持`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`，`formal_split=false`，不创建任务20。
