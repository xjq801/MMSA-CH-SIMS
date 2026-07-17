# 任务20第6–9项基线执行审计

> 日期：2026-07-17  
> SSOT：总纲v1.16第17节任务20、`experiment-protocol-v2.md`  
> 状态：任务6已完成独立legacy原生兼容重跑；任务7已由强视觉重实现完成单种子正式run，官方VC-CSA复现失败证据继续保留

## 1. 原48维 legacy baseline（任务6）

固定的CUC legacy数据共有2787条、每条48维，但存在三个不可绕过的统一评测不匹配：

- `legacy_features_available_at_t0=false`覆盖2787/2787；
- 标签层为`SILVER`，原生目标为二分类，不是CSMV八类人工受众情绪分布；
- `group_by_video_v1`、`publisher_heldout_v1`、`topic_heldout_v1`均为`not_assigned=2787`。

因此，若现在重建随机split、把银标二分类与CSMV分布目标混表，或把非T0特征改写成T0，将违反任务4、实验协议和任务10冻结边界。本轮裁定：

`FAILED_DATA_MISMATCH_NO_FROZEN_SPLIT_T0_INELIGIBLE`

CatBoost/HGB/LightGBM依赖和等预算空间已冻结。上述裁定继续适用于“把48维结果纳入CSMV统一正式评测”的尝试，属于任务17要求保留的`DATA_MISMATCH`，不是GPU失败。

用户随后明确要求重跑任务6。为保留原生任务含义且不修改CSMV冻结协议，新增独立配置`configs/task20/legacy-48-native-rerun-v1.json`，证据类别固定为`LEGACY_NATIVE_COMPATIBILITY_ONLY`：

- 数据仍为2787条CUC原48维与原生SILVER二分类标签，不改写为八类分布或T0输入；
- 采用发布者级SHA-256确定性分组，train/dev/test为1905/307/575条、28/6/9个发布者组，组交集为0；
- CatBoost、HGB、LightGBM各执行冻结的12个trial，只用dev按Macro-F1选择，test对选中模型各评测一次；
- 本地CPU完整运行耗时36.4秒，未复用旧论文或旧脚本数值，run bundle未记录本机数据路径。

| 模型 | 选中trial | test Macro-F1 | Balanced Accuracy | AUPRC | 正类Recall |
|---|---:|---:|---:|---:|---:|
| CatBoost | 07 | 0.5346 | 0.6006 | 0.6884 | 0.2183 |
| HGB | 09 | 0.4591 | 0.5514 | 0.5989 | 0.1338 |
| LightGBM | 04 | 0.3645 | 0.4766 | 0.4581 | 0.0528 |

本次成功状态仅为`COMPLETED_LEGACY_NATIVE_NON_T0_NON_COMPARABLE`。低Recall和跨发布者泛化下降如实保留；不做test后调参，不进入CSMV统一数值表或主结论。

## 2. VC-CSA官方复现（任务7）

只读固定官方仓库revision `99d14240254b1381dde0b9c56add140381f65117`。现场文件树只含README、根LICENSE与CSMV数据文件，没有VC-CSA模型/训练/评测代码。README声称代码MIT、标注CC BY-SA 4.0，但根LICENSE为Apache-2.0，许可层次冲突继续保留。

官方任务以“视频+目标评论”预测单条评论情感；目标评论是本项目T0禁用输入，官方随机评论split也不是当前`group_by_video_v1`视频级分布预测。因此不能把官方论文数字或评论输入模型改写为公平T0复现。本轮裁定：

`FAILED_OFFICIAL_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH`

替代的强基线为本项目重实现的冻结I3D temporal-attention分布模型；它只能标为`REIMPLEMENTATION_STRONG_BASELINE`，不得标为VC-CSA官方复现。

用户明确允许使用本地3070 Ti后，在不上传I3D资产的前提下完成替代强基线正式运行：

- 固定代码提交`14027a088de2ad1e003ff58fe523aa57718ab1e5`，工作区clean；PyTorch 2.4.1+cu121，本地3070 Ti，float32、AMP关闭；
- `group_by_video_v1`为5698 train / 837 dev / 1675 test，完整序列使用`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`；
- 12个冻结trial仅在dev按JSD/NLL/Brier/参数量选择，选中trial 4：hidden=128、dropout=0.3、learning_rate=0.001，best epoch=5；
- 冻结selection SHA-256为`dce53eeb8f3d618d2ed6e09fecc49164a0e6ac72b5254a065ebf4f493c97dfbf`；test仅对该配置评测一次，1675条预测完整；
- dev JSD=0.177014；test JSD=0.182668、NLL=1.715192、EMD=0.162983、Brier=0.227379、ECE=0.053885、ACE=0.054004、AURC=0.175399、Macro-F1=0.137048、Balanced Accuracy=0.148577。

任务7据此以`COMPLETED_VIA_REIMPLEMENTATION_STRONG_BASELINE_SINGLE_SEED`闭合。官方复现仍是`FAILED_OFFICIAL_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH`，不得因替代基线完成而删除。数值尚待任务50五种子统计与正式配对bootstrap，不是最终论文比较结论。

## 3. 冻结特征模型与E1（任务8–9）

- 已实现冻结I3D mean/std不可逆汇总、train-only standardizer、MLP分布头和masked temporal-attention分布头。
- 汇总缓存不含标签、原始序列或本机资产路径；仅内部研究使用，禁止再分发。
- CLIP、SigLIP与VideoMAE特征不在已冻结且获内部使用授权的T0输入合同中；不得为补齐清单另行下载或伪造，登记`NOT_AVAILABLE_IN_FROZEN_T0_PROTOCOL`。
- CSMV实际可用T0内容模态只有I3D视觉。late fusion、跨模态cross-attention与E1逐模态增量均登记`NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`；音频固定`NOT_APPLICABLE_AUDIO_UNAVAILABLE_BY_DATASET_DESIGN`。

## 4. 算力状态

用户授权的租用A30可被`nvidia-smi`枚举且空闲，但新环境Torch下载两条官方通道均在10分钟窗口内无有效进度；平台自带PyTorch 1.3.1/CUDA 10.1虽能枚举A30，最小CUDA矩阵运算未在30秒内完成。正式裁定：

`REMOTE_GPU_RUNTIME_UNAVAILABLE_ENVIRONMENT_NOT_READY`

该裁定描述当时的远端状态：当时未启动正式高算力实验，也未静默转为本地GPU。随后用户明确允许使用本地3070 Ti；本地CUDA运行时通过且受限I3D无需外传，因此任务7强视觉基线已在本地完成正式单种子run。远端A30状态仍不得改写为已就绪。

## 5. 远端运行时修复与再次失联

后续分层诊断确认远端根文件系统约347 GiB可用、A30空闲，失败主因不是显存或磁盘：平台旧环境为PyTorch 1.3.1/CUDA 10.1；独立`task20`环境为Python 3.8.20但无PyTorch；远端访问PyPI超时，官方PyTorch索引与国内镜像可达但带宽较低。

为避免计费实例长时间慢速下载，从本机代理下载公开的PyTorch 1.13.1/CUDA 11.7 wheel并校验后，仅上传该公开运行时文件。重组前后文件长度均为1,801,800,326字节，SHA-256均为`bbf9546f0d0d8b51263ca479637b426a88335fca0034f42cec63d4d32dee05af`；远端输出确认wheel安装成功。随后依赖安装期间SSH通道异常结束，端口复查为不可连接，故未能执行最小CUDA矩阵验证，环境仍不得标记为就绪。本轮更新裁定仍为：

`REMOTE_GPU_RUNTIME_UNAVAILABLE_ENVIRONMENT_NOT_READY`

未向远端上传原始I3D `.npy`、标签、可逆受限资产或本机路径。完整序列temporal-attention正式运行也不能通过重新分发I3D资产来绕过此边界。

## 6. test泄漏修复与temporal-attention工程验证

代码审计发现pooled MLP runner的test分支虽读取dev冻结配置，却把test传入早停函数，存在test选择epoch风险。正式test此前未运行，因此没有污染既有结果。修复后，test分支固定使用train拟合、dev早停，test仅做一次前向和指标计算；回归测试用不同dev/test特征证明test特征不会进入早停。

新增完整I3D序列temporal-attention训练与runner：标准化统计只遍历train时序，按冻结`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`和16,384 padded-step上限批处理，dev选择，test同样只前向一次。32个train/16个dev、单trial、两epoch的本地CPU smoke独立运行两次，`predictions.jsonl`、`metrics.json`和`selection.json`的SHA-256分别完全一致。该证据只验证工程合同，不进入正式baseline数值。

正式运行前发现重复文件打开使全量单epoch耗时30.4秒；测试先行新增只在进程内存在的只读序列缓存后，全量两epoch降至20.8秒，不改变train-only标准化、模型或预算，也不写出I3D。正式dev 12-trial耗时约13分30秒，唯一test运行约91秒；test重训得到的dev JSD与冻结selection完全一致。预测、指标与manifest均无本机路径，模型权重、标准化器和全部run bundle保持Git忽略且禁止再分发。
