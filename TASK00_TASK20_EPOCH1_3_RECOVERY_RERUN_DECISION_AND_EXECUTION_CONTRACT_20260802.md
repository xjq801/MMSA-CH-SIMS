# Task00 对 Task20 Epoch 1—3恢复复跑的裁定与执行合同

> 版本：v1.0  
> 日期：2026-08-02（Asia/Shanghai）  
> 决定编号：`AUTH-00-TASK20-EPOCH1-3-RECOVERY-20260802`  
> 用户授权：`USER_AUTHORIZATION_20260802_TASK20_EPOCH1_3_RECOVERY`（选择B）  
> 裁定父状态：`origin/main@051faa160e65fb9f1a71b7c41c4e69eafeec87e0`  
> 唯一新运行ID：`TASK20_VCCSA_EPOCH1_3_RECOVERY_RERUN_SEED3407_ATTEMPT2`  
> 执行状态：`AUTHORIZED_AFTER_BOUND_PREFLIGHT`  
> 正式证据资格：`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`

## 1. 裁定

用户明确允许Task20为缺失的Epoch 1—3运行记录执行一次独立恢复复跑，并在展示层把新复跑的Epoch 1—3与既有原运行的Epoch 4—120并列。00据此批准一个隔离、单种子、只到Epoch 3的恢复attempt；该批准不重开Task20正式核心，不修改G3，也不恢复原运行中已经冻结为缺失的证据。

本次新运行永久继承且不得缩写、弱化或改标：

- `EXPERIMENT_IDENTITY=AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`；
- `METHOD_LEAKAGE_RISK=USER_ACCEPTED_FOR_EXPLORATORY_ONLY`；
- `FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`；
- `ATTEMPT_ID=TASK20_VCCSA_EPOCH1_3_RECOVERY_RERUN_SEED3407_ATTEMPT2`；
- `RELATION_TO_ORIGINAL_RUN=INDEPENDENT_RERUN_NOT_A_RESUME_NOT_A_CONTINUATION`。

“恢复”只表示重新生成一个独立attempt的Epoch 1—3诊断记录；不表示从原运行恢复状态，不表示原Epoch 1—3被找回，也不表示获得了一条原始Epoch 1—120连续轨迹。

## 2. 永久不变的历史事实

1. 既有`seed=3407`作者原设定探索运行完成120个epoch，但当前可核验私有包只有Epoch 4—120的117组loss、dev metrics与dev predictions。
2. 原运行Epoch 1—3的raw loss、dev metrics和dev predictions继续固定为`KNOWN_EVIDENCE_GAP_EPOCH_1_3_NOT_RECOVERABLE_FROM_AVAILABLE_SOURCES`；不得覆盖、补造、回填、重命名或宣称已恢复。
3. 新attempt即使使用相同GPU型号、相同seed、相同软件和输入，也不是原运行的确定性延续；实例、初始化执行、底层算子和浮点轨迹均须按独立来源处理。
4. 既有`HANDOFF_20.md`、G3证据包、最终closeout manifest、Epoch 4—120 CSV/PNG/Word及其hash-bound提交保持原字节不变。
5. I3D许可、官方revision、权利方包身份/fixity继续为`UNKNOWN`；本授权不是权利方许可、公开发布或再分发授权。

## 3. 唯一允许的运行范围

- 数据与方法：只运行既有作者原设定NON_T0泄漏接受型VC-CSA路径；固定`seed=3407`、作者comment split、完整`video_to_comment`映射和原peer逻辑。
- 训练语义：保持原冻结配置的`max_epoch=120`及由此派生的scheduler总步数，不得把`max_epoch`直接改为3；以独立、可测试的执行守卫在Epoch 3训练、dev评估、预测和checkpoint完整落盘后干净停止。
- 起点：从新的模型/optimizer/scheduler/RNG初始化开始；禁止加载原运行Epoch 3/4、best、final或任何其他checkpoint。
- 终点：完成Epoch 1、2、3后停止；不得继续Epoch 4，不得根据loss或dev结果选择性续跑、重启或调参。
- 评估：只允许冻结dev计算；`test_access=0`，不得读取或报告test指标/预测。
- 次数：只允许一个完成的attempt2。OOM、断电、依赖或脚本失败可以工程修复后继续同一attempt目录，但必须保留全部失败证据；凡是重新初始化训练，必须分配新的attempt编号并先回交00，不得覆盖attempt2。
- 范围隔离：不得修改Task30实验核心、Task20冻结统一评测器、Task50接口、总纲或论文SSOT。

若现有代码不能在不改变120-epoch scheduler语义的前提下于Epoch 3后干净停止，Task20只可增加最小执行守卫及其失败先行测试；不得通过修改学习率计划、数据顺序、loss、batch size、peer逻辑或评估定义达到停止目的。

## 4. 启动前的精确绑定

Task20须从包含本文件的已推送main提交开始，并在任何真实资产写入或训练前生成非秘密preflight记录。以下冻结锚必须逐项复核：

| 锚 | 冻结值/要求 |
|---|---|
| 决策代码父状态 | `051faa160e65fb9f1a71b7c41c4e69eafeec87e0`；实际授权提交记录为“包含本文件的main commit” |
| 作者源码revision | `3e8c42608f4e89bc2082c55760aa63535e8e276a` |
| 基础配置 | `configs/task20/vccsa-author-original-v1.json` SHA-256 `5b3fcd91c2354e51b6baec85dc34d65bc14676b0d8a7f365dc0fce2f4f4c62f6` |
| 环境锁 | `configs/task20/requirements-vccsa-author-lock.txt` SHA-256 `db32dd636de2d92b210ff45985c5fc5d09f6afd770c5fb1ef50d75f515853697` |
| I3D manifest | `data/manifests/csmv-i3d-quarantine-v1.manifest.json` SHA-256 `425829cf3271ce3c695a011e75b9efa94c4efab76458fda9f902e6eeb9c99c1e`，恰好8210项 |
| runtime生成器 | `scripts/prepare_vccsa_author_reproduction.py` SHA-256 `1c97d7509d4ccace0b7f9acac19195c1101bfde2f9359986dfc453a177e1d31a` |
| 断点/状态runtime | `scripts/vccsa_resume_runtime.py` SHA-256 `0726a788a11639348c58691809120b503bf64c2e36131843e63852fbfb583b95` |
| 既有Epoch 4—120数据 | `paper/figures/task20_vccsa_loss_curve.csv` SHA-256 `5f99e7825934c8440f2fb1e0d73d848a5dcbf2095435e18d141ff819a0483163`；只读 |
| 既有Epoch 4—120图 | `deliverables/TASK20_VCCSA_EPOCH_4_120_LOSS_CURVE_20260731.png` SHA-256 `e7e335701794e686fa26d9a69df8740db3947fa6b8c8c9736be94c143678ced1`；只读 |

执行前还必须记录：

1. `run_manifest_sha256`、派生attempt配置SHA-256、完整argv摘要和代码commit；若工作树非净，另存非秘密diff SHA-256并解释原因。
2. 远端runtime文件清单及聚合tree SHA-256；关键既有runtime应复核`main.py=949e82066905cf8684a9420d5878a042804d5de6a404b3a7aa3086d6962164b3`、`train_vccsv.py=c1ecf88c7a548c23ba693ff02ff4738ea57ebab2d135242635fad641028343f3`、`csmv_dataset.py=f7f39355766b8ae336453aa63b9c80a3857fa06450960faeb3dc93306b3df325`、`resume_utils.py=0726a788a11639348c58691809120b503bf64c2e36131843e63852fbfb583b95`；若不一致，停止并提交差异，不得直接运行。
3. Python、依赖锁、CUDA、cuDNN、driver、GPU型号/UUID、CPU、内存和区域摘要及`environment_sha256`。
4. 非秘密实例三元组：SSH host-key SHA-256、GPU UUID、规范化endpoint digest。不得记录endpoint原文、端口、账号、密码、私钥、Cookie或秘密链接；任一字段缺失或漂移都禁止上传与训练。
5. 输入manifest/hash、8210计数/总字节、`missing/extra/size_mismatch/sha256_mismatch`四类差异；只有四类均为空才可运行。
6. 私有MatBox/存储目标digest、区域类别、owner-only ACL摘要、加密状态和创建时间；任何公共链接、第三方共享或未知可写主体均为停止条件。

用户对“相同4090”的描述只作为租用意图；必须以实际GPU型号与UUID绑定为事实，不能据此宣称与原实例相同或逐bit可比。

## 5. 每个epoch与逐step证据

attempt2必须写入新的、不可覆盖的私有目录。至少保留：

- 开始/结束时间（含时区）、wall time、PID、exit code、停止原因、完整stdout与stderr；
- 每个optimizer step的epoch、step、global step、未平滑loss、各loss分量、learning rate和时间戳；
- 每个Epoch 1—3的聚合train loss、完整dev九项指标、样本数、评估配置和非有限值检查；
- 每个Epoch 1—3的dev逐样本预测、样本身份映射和预测文件SHA-256；这些内容保持私有，不进入Git或公开材料；
- Epoch 1、2、3 checkpoint（若代码生成）及最终Epoch 3 checkpoint的bytes、mode与SHA-256；不得把它们称为原运行checkpoint；
- config、code tree、environment、input、stdout、stderr、step log、metrics、predictions、checkpoint和总`SHA256SUMS`的hash清单；
- 若出现OOM、NaN/Inf、Traceback、I/O错误、信号退出、存储不足、权限失败或中断，保留最后完整checkpoint、stderr、exit code、failure manifest和已产生的所有证据，不得删除失败记录或写成完成。

任何凭据、endpoint原文、I3D字节、评论/标签正文、本机绝对路径、逐样本预测或checkpoint均不得进入Git。Git只允许非秘密配置、聚合摘要、相对artifact名和hash。

## 6. “合并曲线”的唯一允许含义

允许生成一个新的版本化展示包，但不得覆盖现有Epoch 4—120 CSV/PNG/Word。新CSV的每行必须携带`attempt_id`、`epoch_label`、`source_artifact_sha256`、`run_instance_digest`和`cross_attempt_comparable=false`；新图必须：

1. 用不同颜色/线型/图例分别绘制attempt2的Epoch 1—3与原attempt1的Epoch 4—120；
2. 在Epoch 3/4之间画清晰断点或留白，并标注`INDEPENDENT ATTEMPT BOUNDARY`；禁止用一条连续折线跨过边界；
3. 图注同时写明`NON_T0`、`INELIGIBLE`、原Epoch 1—3仍缺失、跨实例/跨初始化不可比；
4. 禁止跨边界平滑、插值、移动平均、累计量、AUC、单轨趋势拟合或“完整1—120训练曲线”命名；
5. dev metrics只能按attempt分区并列，不得拼成一条同源时间序列，不得据此进行模型选择、显著性、排名或优越性比较。

推荐新文件名前缀：`TASK20_VCCSA_NON_T0_EPOCH1_3_ATTEMPT2_WITH_EPOCH4_120_ATTEMPT_BOUNDARY_20260802`。任何标题和图注不得使用“recovered original Epoch 1—3”“completed original curve”或等义表述。

## 7. 资产、MatBox与保留边界

- 既有`SC-20260719-02/03`的私有MatBox、私有对象存储与配置镜像权限只在owner-only、非公开、固定8210项和本次内部研究范围内继续适用；不允许公开、转交第三方、Git/Git LFS、公共bucket、公共镜像或可匿名下载。
- attempt2必须使用新的版本化私有prefix/目录和新的`storage_target_digest`；禁止写入或覆盖原final-run-bundle、原checkpoint、原预测和原Epoch 4—120证据。
- 本授权不延长既有受限材料的删除期限。既有及本次可见层受限副本均不得晚于`2026-08-31 23:59:59 +08:00`完成删除，除非用户在截止前另行书面延长；平台备份、快照内部副本和物理擦除继续为`UNKNOWN_PLATFORM_CONTROL_PLANE`。
- 权利方否认、8210 hash/覆盖漂移、权限/公开性漂移或无法完成可见层删除核验时，立即停止并标记`ASSET_INVALIDATED_DO_NOT_REPORT`。

## 8. 正式证据与任务树隔离

attempt2及其展示包永久禁止进入或支撑：

1. T0结果、统一baseline正式列、`BASELINE_TABLE_V1.md`或任何正式排名；
2. G3主证据、既有G3 package或hash-bound `HANDOFF_20.md`；
3. Task30 H1、Task40、Task50、五种子、bootstrap、paired comparison或正式消融；
4. 论文SSOT、主表、摘要、结论、性能claim、泛化/公平/无泄漏/优越性claim；
5. 把这次运行称为原运行resume、原Epoch 1—3恢复、完整1—120轨迹或作者官方无泄漏复现。

`G1=PASS`、`G2=PASS_WITH_ACCEPTED_ASSET_RISK`、`G3=PASS_WITH_LIMITATIONS`、Task20正式核心关闭、Task30独立H1开发门及“未过H1不得创建Task40”均不变。

## 9. Task20允许提交的范围

Task20完成后只可提交：

- 新的attempt2非秘密派生配置、run manifest/hash ledger、执行守卫及对应测试；
- 新的NON_T0展示CSV/PNG/SVG及其生成脚本，前提是图中和文件名保留attempt边界；
- `TASK20_VCCSA_EPOCH1_3_RECOVERY_RERUN_COMPLETION_20260802.md`；
- `experiments/EXPERIMENT_REGISTRY.md`的独立attempt行和同批`WORK_LOG.md`追加记录。

禁止修改或提交总纲、G门裁定、论文SSOT、Task30/40/50实现、`HANDOFF_20.md`、`TASK20_VCCSA_EXACT_RESUME_RUNBOOK_20260723.md`、既有final-closeout manifest、既有Epoch 4—120 CSV/PNG/Word，以及任何凭据、受限资产、预测或checkpoint正文。

提交前至少运行Task20专项测试、attempt manifest/边界图验证、`validate_work_log.py`、`run_preparation_checks.py`和`git diff --check`；失败必须保留并回报。推送后以`REQUEST_00_TASK20_EPOCH1_3_RECOVERY_REVIEW`回交精确commit、全部非秘密文件SHA-256、运行/失败状态和剩余限制；Task20不得自批完成或自行提升证据等级。

## 10. 立即停止条件

遇到下列任一条件，停止上传/训练/展示合并并回交00：实例三元绑定不全或漂移；冻结hash或8210覆盖不一致；无法证明从新初始化开始；scheduler语义因三epoch停止而改变；访问test；缺失逐step loss/LR、dev metrics/predictions或stdout/stderr；失败证据无法保留；旧证据被覆盖；公共可达性或ACL漂移；用户撤回；权利方否认。

## 11. 总控结论

`AUTH-00-TASK20-EPOCH1-3-RECOVERY-20260802=APPROVED_FOR_ONE_BOUND_INDEPENDENT_ATTEMPT`。

批准对象只有`TASK20_VCCSA_EPOCH1_3_RECOVERY_RERUN_SEED3407_ATTEMPT2`。它可以填充内部展示材料中“另一次运行的Epoch 1—3”这一栏，不能填充历史证据中“原运行Epoch 1—3”这一缺口。任何跨attempt并列都必须把不可连续、不可比较和正式证据不合格直接编码进数据、图形与文字。
