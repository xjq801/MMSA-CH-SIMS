# 任务20第6–9项基线执行审计

> 日期：2026-07-17  
> SSOT：总纲v1.16第17节任务20、`experiment-protocol-v2.md`  
> 状态：任务6已完成独立legacy原生兼容重跑；任务7强视觉重实现已完成；作者发布的VC-CSA实现候选于G3后定位，待依赖修复与原任务复现，T0输入不匹配仍成立

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

官方任务以“视频+目标评论”预测单条评论情感；目标评论是本项目T0禁用输入，官方随机评论split也不是当前`group_by_video_v1`视频级分布预测。因此不能把官方论文数字或评论输入模型改写为公平T0复现。以下仅是当时审计官方main `99d14240254b1381dde0b9c56add140381f65117`所得的历史尝试状态，已被第8—9节后续作者实现定位与smoke证据取代，不是当前VC-CSA状态：

`HISTORICAL_OFFICIAL_MAIN_99D1424_ATTEMPT_FAILED_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH`

替代的强基线为本项目重实现的冻结I3D temporal-attention分布模型；它只能标为`REIMPLEMENTATION_STRONG_BASELINE`，不得标为VC-CSA官方复现。

用户明确允许使用本地3070 Ti后，在不上传I3D资产的前提下完成替代强基线正式运行：

- 固定代码提交`14027a088de2ad1e003ff58fe523aa57718ab1e5`，工作区clean；PyTorch 2.4.1+cu121，本地3070 Ti，float32、AMP关闭；
- `group_by_video_v1`为5698 train / 837 dev / 1675 test，完整序列使用`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`；
- 12个冻结trial仅在dev按JSD/NLL/Brier/参数量选择，选中trial 4：hidden=128、dropout=0.3、learning_rate=0.001，best epoch=5；
- 冻结selection SHA-256为`dce53eeb8f3d618d2ed6e09fecc49164a0e6ac72b5254a065ebf4f493c97dfbf`；test仅对该配置评测一次，1675条预测完整；
- dev JSD=0.177014；test JSD=0.182668、NLL=1.715192、EMD=0.162983、Brier=0.227379、ECE=0.053885、ACE=0.054004、AURC=0.175399、Macro-F1=0.137048、Balanced Accuracy=0.148577。

任务7据此以`COMPLETED_VIA_REIMPLEMENTATION_STRONG_BASELINE_SINGLE_SEED`闭合。上述代码缺失状态仅保留为官方main `99d1424`原尝试的历史记录，并已被后续作者fork定位证据取代；当前状态见第9节的`AUTHOR_ORIGINAL_PATH_SMOKE_EXECUTABLE_FULL_REPRODUCTION_BLOCKED_COMPUTE`。作者原设定仍为NON_T0，替代强基线仍不得改名为官方复现。数值尚待任务50五种子统计与正式配对bootstrap，不是最终论文比较结论。

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

## 7. 任务15 smoke、完整run与重复一致性

- smoke：temporal-attention已完成32 train/16 dev、1 trial、2 epoch的CPU双run，以及本地3070 Ti GPU smoke；均只读取train/dev。
- 单种子完整run：12-trial正式dev选择和冻结selection后的唯一test评测已完成；test未在任务15中再次运行。
- 正式重复运行：以clean commit `f6a8363bc79144775d63c9bd62f149ce51cb9ff7`、相同seed `20260717`、相同本地3070 Ti环境重跑完整12-trial dev，运行时间833秒，状态`COMPLETED`。
- fail-closed比较验证两侧config、inputs、代码文件SHA-256、环境、seed、split一致；`predictions.jsonl`、`metrics.json`、`selection.json`和`trial_results.json`四项SHA-256逐字节一致，model state与standardizer文件SHA-256也分别一致。
- replay manifest SHA-256为`2b5b3473473ffe1d50435d2838642de1cae00b6618b29f93df79a5facfcfde3d`，比较报告SHA-256为`5d85fa1dbfdd263e5c5086e57bab3ce5305af4c340e28cf4315a1bbcbea1458d`；run bundle保持本机Git忽略且禁止再分发。

该证据只支持`SAME_ENVIRONMENT_FIXED_SEED`工程复跑，不证明跨硬件、跨驱动或跨PyTorch release的bitwise复现，也不替代任务50五种子统计。

## 8. G3后VC-CSA作者代码定位与结论更正

用户提供`JackySnake/MSA-CRVI`后，现场核验确认该仓库不是无关第三方镜像，而是`IEIT-AGI/MSA-CRVI`的fork；HEAD为`3e8c42608f4e89bc2082c55760aa63535e8e276a`，README联系人为论文第一作者Qi Jia。该HEAD同时是官方仓库PR #3（标题`add source code`）的head，PR状态为open、未合并，base仍是原先审计的`99d14240254b1381dde0b9c56add140381f65117`。

代码树包含`source_vcssa/model_VCCSA.py`、`main.py`、`main_eval.py`、训练/评测脚本和配置。因此，原结论中的“没有可定位的作者代码”被新证据取代；更正后的代码资格为：

`AUTHOR_RELEASED_IMPLEMENTATION_LOCATED_PR3_OPEN_NOT_YET_REPRODUCED`

原失败记录继续作为当时只审计官方main的历史事实保留，不删除。当前也不能直接升级为“官方主分支可信复现”，原因如下：

- PR尚未合并，正式revision身份需按作者fork commit `3e8c426`单独冻结；
- 原实现明确读取`comment_info.comment`并以RoBERTa编码目标评论，同时读取视频特征，任务仍是评论级3类opinion/8类emotion分类；本项目T0禁止目标评论输入，目标为视频级未来受众分布，协议不匹配仍成立；
- 官方脚本使用随机comment split，不是`group_by_video_v1`；其原任务结果只能作为非T0官方原设定参考复现，不能直接进入统一T0主表；
- `train.sh`定义`video_feature`却传入`${video_feature_dir}`，且续行符后存在空格；根README写`source_vcsa`而实际目录为`source_vcssa`，需要显式修复账本；
- Python语法编译通过，但在独立任务20环境运行`main.py --help`与`main_eval.py --help`均在CUDA前因未声明依赖`en_vectors_web_lg`缺失而exit 1。尚未启动训练，也未消耗GPU。

后续若执行复现，必须分成两个不可混写的实验：先以作者原comment输入/原split复现论文设定并记录修复差异；再如需T0比较，另建去评论、group-by-video、视频级分布目标的适配版，并标`REIMPLEMENTATION`而非官方复现。现有temporal-attention强基线和`G3=PASS_WITH_LIMITATIONS`不因代码定位自动失效，但00必须更新“代码缺失”限制措辞。

## 9. 作者原设定兼容修复与GPU smoke

用户授权继续后，冻结作者fork `3e8c42608f4e89bc2082c55760aa63535e8e276a`、作者comment级train/dev/test split和目标评论输入，并将本实验硬标为`AUTHOR_ORIGINAL_SETTING_NON_T0`。任何去评论或视频级分布适配必须另建`REIMPLEMENTATION`，不得继承作者复现身份。

兼容修复采用测试先行，未复制或提交作者源码，仅提供对固定checkout执行的最小补丁器。修复项为：

- 将未使用主路径的`en_vectors_web_lg`改为延迟可选依赖；旧GloVe路径真的被调用时仍显式失败；
- 参数化dataset中的RoBERTa路径，训练与评测脚本显式传入本地模型目录；
- 修复`train.sh`的`video_feature`/`video_feature_dir`变量不一致与续行空格；
- 删除源码中不存在且从未使用的`CSMV_Dataset_VideoMAEv2FPS16`、`MLP`与`LayerNorm`死导入；
- 为上游训练循环读取但从未声明的`aux_task`固定默认值`False`，保持当前主损失路径；
- 保留作者模型结构、目标评论、comment split、标签和dev checkpoint选择逻辑不变。

独立环境已锁定为Python 3.8.9、PyTorch 1.13.1+cu117、NumPy 1.22.4、scikit-learn 1.2.1、transformers 4.26.1、easydict 1.10；CUDA可见本地RTX 3070 Ti。RoBERTa快照冻结为`FacebookAI/roberta-base@e2da8e2f811d1448a5b465c236feacd80ffbac7b`。首次Torch wheel安装因2.26GB下载超时失败，随后用可续传下载完成安装；失败未删除。

首次GPU smoke的训练入口只迭代8个train与4个dev，`test_set.json`为空且未实例化test loader；但后续审查发现，旧构建器仍把含全部评论/标签的总标注字典和完整`video_to_comment`映射复制到runtime。因此首次运行只能证明“入口未迭代test split”，不能证明“物理输入无test记录”，此前零test物理隔离表述证据不足。

经TDD修复后，构建器从作者总标注压缩包读取源记录，但输出`lable_data_dict.json`与`video_to_comment.json`的ID集合必须严格等于`selected_train ∪ selected_dev`；缺失、额外ID或无法形成同视频peer均fail closed。真实runtime重建后包含8个train、4个dev、0个test，标注ID=12、video映射ID=12，并用新run名重跑batch=1、1 epoch GPU smoke；146.05439M参数模型完成训练与dev前向，训练段约3秒，未OOM。smoke小样本指标没有统计意义，不得进入baseline表或写成作者结果。当前状态为：

`AUTHOR_ORIGINAL_PATH_SMOKE_EXECUTABLE_FULL_REPRODUCTION_BLOCKED_COMPUTE`

作者全split为75,086 train、10,727 dev、21,454 test。按本地batch=1 smoke粗估，单epoch约10.4小时，120 epoch约52天；上游声明的`early_stop=5`并未在训练循环实现。租用A30端点复查仍为TCP不可达，因此没有在本地盲跑全量，也没有读取test。全量作者原设定复现必须等待可连接的高显存GPU；远端连接失败不得写成GPU训练失败。

I3D许可、官方revision、权利方包身份/fixity仍未知，`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`不变；未提交、上传或再分发I3D `.npy`、作者评论数据、模型权重、预测文件、本机路径或其他可逆受限资产。权利否认或8210 hash/覆盖漂移仍立即触发`ASSET_INVALIDATED_DO_NOT_REPORT`。

## 10. 新租用RTX A6000全量复现资源预检

用户提供新的租用GPU后，仅执行连接、环境、公开依赖与合成资源预检；未上传受限I3D、全量评论runtime、模型权重、预测或本机路径，也未启动作者全量train/dev/test。

- SSH认证成功；远端为NVIDIA RTX A6000 48GB，约48.7GB显存空闲、350GB磁盘空闲、85GB内存可用，无其他计算进程。
- 平台现成`myconda`环境的PyTorch 2.5.1+cu121 CUDA探针通过，但版本不符合冻结合同，未用于正式复现。
- 新建独立`vccsa-author`环境：Python 3.8.20、PyTorch 1.13.1+cu117、NumPy 1.22.4、scikit-learn 1.2.1、transformers 4.26.1、easydict 1.10；CUDA可见A6000，4096平方矩阵结果有限。Python patch版本与本地3.8.9不同，后续manifest必须如实记录，不能声称跨环境bitwise一致。
- PyTorch串行下载因带宽下降被主动停止并保留日志；改用16连接下载后平均约12MiB/s，1.8018GB Linux wheel的SHA-256核为`bbf9546f0d0d8b51263ca479637b426a88335fca0034f42cec63d4d32dee05af`。首次本地wheel安装因`--no-index`无法解析`typing-extensions`而失败，补齐公开依赖并用`--no-deps`安装后闭合。
- 作者fork仍固定`3e8c42608f4e89bc2082c55760aa63535e8e276a`；兼容补丁幂等复核`changed_files=[]`，compileall通过。固定RoBERTa快照15个文件逐项hash一致。
- 合成资源预检使用32 train、16 dev、0 test，annotation与video map均为48 ID；24个合成视频固定为最坏长度`180×1024`，明确不含真实I3D。batch=16、146.05439M参数完成2个训练batch、dev前向和checkpoint保存，约10秒、exit 0、无OOM。合成指标无报告资格。
- 两个失败探针如实保留：缺`/usr/bin/time`时入口前exit 127；16 train只有一个batch时，作者日志`elapsed/step`触发`ZeroDivisionError`，但该次已完成一个batch=16训练步骤且未OOM。改用两个train batch后不修改作者代码即通过。

资源结论更新为：

`REMOTE_A6000_RUNTIME_READY_SYNTHETIC_BATCH16_RESOURCE_SMOKE_PASSED_FULL_REPRODUCTION_NOT_STARTED`

该结论关闭“没有可用高显存GPU/运行时”的算力阻塞，但不等于全量复现完成。正式运行前仍须在现有`asset_redistribution_allowed=false`边界下明确远端I3D暂存权限，并只暂存固定8210项、复核逐文件hash/覆盖；若没有该权限，不得借租用GPU绕过资产边界。作者代码每epoch约保存1.66GB checkpoint，120 epoch约199GB；当前350GB磁盘在技术上足够，但必须保留容量监控。作者原任务身份继续为`AUTHOR_ORIGINAL_SETTING_NON_T0`，任何T0适配仍须独立标`REIMPLEMENTATION`。
