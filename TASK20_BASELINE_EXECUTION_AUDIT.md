# 任务20第6–9项基线执行审计

> 日期：2026-07-17  
> SSOT：总纲v1.16第17节任务20、`experiment-protocol-v2.md`  
> 状态：部分完成；正式高算力运行被远端GPU运行时阻塞

## 1. 原48维 legacy baseline（任务6）

固定的CUC legacy数据共有2787条、每条48维，但存在三个不可绕过的统一评测不匹配：

- `legacy_features_available_at_t0=false`覆盖2787/2787；
- 标签层为`SILVER`，原生目标为二分类，不是CSMV八类人工受众情绪分布；
- `group_by_video_v1`、`publisher_heldout_v1`、`topic_heldout_v1`均为`not_assigned=2787`。

因此，若现在重建随机split、把银标二分类与CSMV分布目标混表，或把非T0特征改写成T0，将违反任务4、实验协议和任务10冻结边界。本轮裁定：

`FAILED_DATA_MISMATCH_NO_FROZEN_SPLIT_T0_INELIGIBLE`

CatBoost/HGB/LightGBM依赖和等预算空间已冻结，但不执行无资格数值，不复用旧论文表格。该失败属于任务17要求保留的`DATA_MISMATCH`，不是GPU失败。

## 2. VC-CSA官方复现（任务7）

只读固定官方仓库revision `99d14240254b1381dde0b9c56add140381f65117`。现场文件树只含README、根LICENSE与CSMV数据文件，没有VC-CSA模型/训练/评测代码。README声称代码MIT、标注CC BY-SA 4.0，但根LICENSE为Apache-2.0，许可层次冲突继续保留。

官方任务以“视频+目标评论”预测单条评论情感；目标评论是本项目T0禁用输入，官方随机评论split也不是当前`group_by_video_v1`视频级分布预测。因此不能把官方论文数字或评论输入模型改写为公平T0复现。本轮裁定：

`FAILED_OFFICIAL_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH`

替代的强基线为本项目重实现的冻结I3D temporal-attention分布模型；它只能标为`REIMPLEMENTATION_STRONG_BASELINE`，不得标为VC-CSA官方复现。

## 3. 冻结特征模型与E1（任务8–9）

- 已实现冻结I3D mean/std不可逆汇总、train-only standardizer、MLP分布头和masked temporal-attention分布头。
- 汇总缓存不含标签、原始序列或本机资产路径；仅内部研究使用，禁止再分发。
- CLIP、SigLIP与VideoMAE特征不在已冻结且获内部使用授权的T0输入合同中；不得为补齐清单另行下载或伪造，登记`NOT_AVAILABLE_IN_FROZEN_T0_PROTOCOL`。
- CSMV实际可用T0内容模态只有I3D视觉。late fusion、跨模态cross-attention与E1逐模态增量均登记`NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`；音频固定`NOT_APPLICABLE_AUDIO_UNAVAILABLE_BY_DATASET_DESIGN`。

## 4. 算力状态

用户授权的租用A30可被`nvidia-smi`枚举且空闲，但新环境Torch下载两条官方通道均在10分钟窗口内无有效进度；平台自带PyTorch 1.3.1/CUDA 10.1虽能枚举A30，最小CUDA矩阵运算未在30秒内完成。正式裁定：

`REMOTE_GPU_RUNTIME_UNAVAILABLE_ENVIRONMENT_NOT_READY`

未启动正式高算力实验，未静默转为本地GPU。仅在本地CPU执行两epoch、单trial工程smoke，不具有论文结果资格。

## 5. 远端运行时修复与再次失联

后续分层诊断确认远端根文件系统约347 GiB可用、A30空闲，失败主因不是显存或磁盘：平台旧环境为PyTorch 1.3.1/CUDA 10.1；独立`task20`环境为Python 3.8.20但无PyTorch；远端访问PyPI超时，官方PyTorch索引与国内镜像可达但带宽较低。

为避免计费实例长时间慢速下载，从本机代理下载公开的PyTorch 1.13.1/CUDA 11.7 wheel并校验后，仅上传该公开运行时文件。重组前后文件长度均为1,801,800,326字节，SHA-256均为`bbf9546f0d0d8b51263ca479637b426a88335fca0034f42cec63d4d32dee05af`；远端输出确认wheel安装成功。随后依赖安装期间SSH通道异常结束，端口复查为不可连接，故未能执行最小CUDA矩阵验证，环境仍不得标记为就绪。本轮更新裁定仍为：

`REMOTE_GPU_RUNTIME_UNAVAILABLE_ENVIRONMENT_NOT_READY`

未向远端上传原始I3D `.npy`、标签、可逆受限资产或本机路径。完整序列temporal-attention正式运行也不能通过重新分发I3D资产来绕过此边界。

## 6. test泄漏修复与temporal-attention工程验证

代码审计发现pooled MLP runner的test分支虽读取dev冻结配置，却把test传入早停函数，存在test选择epoch风险。正式test此前未运行，因此没有污染既有结果。修复后，test分支固定使用train拟合、dev早停，test仅做一次前向和指标计算；回归测试用不同dev/test特征证明test特征不会进入早停。

新增完整I3D序列temporal-attention训练与runner：标准化统计只遍历train时序，按冻结`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`和16,384 padded-step上限批处理，dev选择，test同样只前向一次。32个train/16个dev、单trial、两epoch的本地CPU smoke独立运行两次，`predictions.jsonl`、`metrics.json`和`selection.json`的SHA-256分别完全一致。该证据只验证工程合同，不进入正式baseline数值。
