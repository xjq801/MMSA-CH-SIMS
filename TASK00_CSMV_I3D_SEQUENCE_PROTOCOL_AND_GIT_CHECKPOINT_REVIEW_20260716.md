# 任务00：CSMV I3D序列协议与M1—M2 Git检查点复审

> 决定编号：`REVIEW-00-CSMV-I3D-SEQUENCE-PROTOCOL-20260716`  
> 日期：2026-07-16  
> 审核对象：任务10回交 `TASK10_I3D_SEQUENCE_PROTOCOL_AND_GIT_CHECKPOINT_HANDOFF_20260716.md`  
> 审核基线：`cf6dea18ddb057da91e90d6c0104e3e854f1724a`  
> 裁定：`ACCEPTED_PREREGISTRATION_ONLY_G2_UNCHANGED`

## 1. 结论

00接受任务10提交的I3D序列处理协议、论文主张边界、可复现证据和M1—M2 Git检查点，正式关闭`I3D_SEQUENCE_PROCESSING_PROTOCOL_UNFROZEN`子缺口。

本裁定只确认序列处理规则在查看训练/test结果前已经冻结、可执行且可复现，不提供CSMV I3D资产许可、稳定官方revision、权利方包身份或官方fixity信用。因此：

- G1=`PASS`；
- G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；
- 全局`formal_split=false`；
- 不创建任务20，不训练，不建立正式索引；
- 维护者外部证明继续为`DEFERRED_PENDING_MAINTAINER_REPLY`，按用户要求暂时跳过，不等待、不催促、不重复检查，也不写成已解决。

## 2. 正式冻结的协议

1. 主协议：`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`。完整保留`float32[T,1024]`序列，batch内右补零，布尔mask中`True`表示真实时间步；所有split执行同一规则，不允许test自适应。
2. 主敏感性：`UNIFORM_180_ENDPOINT_INCLUSIVE`。对`T>180`使用确定性、严格递增且包含首尾的180个索引；对`T<=180`保留全部观测并右补零。
3. 补充敏感性：`FIRST_180_ONLY_FIXED_DIAGNOSTIC`。只能作预注册补充，不得根据test表现升级为主方案。
4. 资源规则：确定性长度分桶，`max_batch_size=64`，原始输入张量上限为16,384个padding后时间步，即64 MiB float32输入。若模型激活/梯度导致显存不足，只允许确定性缩小batch，不得无记录地截断序列或改变主协议。
5. 协议变更：查看test结果后不得依据结果选择主规则。若训练前发现确定的实现错误或不可执行资源事实，必须建立版本化v2、说明原因并重新交00复审；旧版本和失败证据不得删除。

## 3. 独立复核证据

### 3.1 输入长度与fixity

- 从冻结`csmv-i3d-quarantine-v1.manifest.json`重新计算8,210个必需样本：`T=6—1719`，`T>180`为531，`T=180`为4，中位数43，P90/95/99为133/211/339。
- 最长单样本原始输入为7,041,024 bytes，等于`1719×1024×4`。
- 协议manifest SHA-256独立复核为`208615d4059afc8c5c2c57a5ffc13eeafa9a71ece861332d9f1cd62bc9c4d5be`。
- manifest列出的6个证据文件SHA-256全部与现场文件一致。

### 3.2 代码、泄漏与复现

- `python -m unittest tests.test_csmv_i3d_sequence_protocol -v`：8/8通过。
- `build_csmv_i3d_sequence_protocol_manifest.py`后专项validator：`PASS_PREREGISTRATION_ONLY_G2_UNCHANGED`；8个fail-closed负例全部通过。
- 泄漏live门：0个Critical失败；负面selftest正确输出`LEAKAGE_BLOCKED`。
- `reproduce_m2_minimal.py --public-core`：Python 3.8.9、`-I -S`、19项输出、`mismatches=[]`。
- `validate_m2_release.py`：通过；G1=`PASS`、G2 blocked、`formal_split=false`。
- `run_preparation_checks.py`：exit 0、`blocking_checks=[]`、`m1_read_only_work_ready=true`、`formal_model_work_ready=false`。

### 3.3 Git与安全边界

- 审核开始时`HEAD=origin/main=cf6dea18ddb057da91e90d6c0104e3e854f1724a`，`origin/main...HEAD=0/0`，工作区干净。
- 内容检查点`f885a592c680e68b5be525212ba77cfce4c9b985`和收尾检查点`cf6dea18ddb057da91e90d6c0104e3e854f1724a`均存在于`main`历史。
- 现场枚举262个tracked文件：`.npy`为0、特征包为0、超过10 MiB文件为0；综合secret scan为0命中。
- 第一次大文件枚举因Git对非ASCII路径的引号转义导致PowerShell `Test-Path`报错；随后以`git -c core.quotepath=false ls-files`重跑并得到上述有效结果。失败未被删除或改写为成功。

## 4. 论文主张边界

允许主张：在冻结I3D视觉表征上进行public-induced audience affect分布预测，并研究训练期评论特权监督、train-only受众反应记忆、校准、OOD和拒绝预测。

禁止主张：端到端视频编码、原始帧学习、完整音视频输入、音频增益、音频随机缺失鲁棒性、评论正文作为T0学生输入，或把CSMV与LAI-GAI的跨域差异写成同一样本随机缺失模态证据。

E1使用`ALL_AVAILABLE_INPUTS`且在当前CSMV协议中等于I3D单输入；E5为`NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`；没有其他合格多输入协议时，H3为`NOT_APPLICABLE_NO_ELIGIBLE_MULTIMODAL_PROTOCOL`。

## 5. 剩余恢复条件

当前不再要求任务10继续处理会等待维护者回复的工作。只有在权利方提供实质回复或用户提供等价的可审计证据后，00才复审以下剩余资产门：

1. 资产级研究使用许可及适用对象；
2. 稳定官方revision；
3. 本地包与官方/权利方资产的身份一致性；
4. 权利方manifest/checksum或等价fixity与8,210键覆盖证明。

在上述条件闭合并重新运行I3D专项、M2 release、泄漏与综合门之前，不得将G2改为PASS，不得将`formal_split`改为true，也不得创建任务20。
