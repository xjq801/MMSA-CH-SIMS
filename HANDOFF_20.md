# HANDOFF_20：M3基线与统一评测交接

> 提交给：任务00总控最终G3复核；G3通过后供任务30读取  
> SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.16 第17节任务20  
> 补交状态：`SUPPLEMENT_READY_FOR_00_FINAL_G3_REVIEW`  
> 当前G3：`HOLD_FOR_SUPPLEMENT_PENDING_00_FINAL_REVIEW`，本文件不自行判定G3 PASS  
> 证据主体commit：`b89d8dc1d62b5d6ea7b07b1d30cc8f19224c030d`  
> 提交状态commit：`aed141b78b0babe4bad10555f335587f983f479b`  
> 机器证据manifest：`data/manifests/task20-handoff-v1.manifest.json`  
> manifest SHA-256：`6d75e2190a50dc4a2191458d6d379a7d49a84f630d5ccf3eb27ac83294f96e91`

## 请求00最终复核

本文件补齐总纲4.5遗漏的必需产出`HANDOFF_20.md`。请00按机器manifest复核commit与证据SHA-256后，独立裁定`G3=PASS_WITH_LIMITATIONS`或`G3=REJECT`。在00书面裁定前，任务30不得创建或启动；任务20不修改总纲、G门或00审查文件。

## 提交与哈希绑定规则

- `b89d8dc`是任务15重复一致性、任务16冻结表和任务18 G3证据主体快照；机器manifest对该commit中的tracked文件按Git blob原始字节计算SHA-256和长度。
- `aed141b`记录G3包已发送00及任务18状态收尾；机器manifest同时绑定该commit中的G3包和工作日志字节。
- Windows运行时manifest可能因CRLF与Git LF快照产生不同字节SHA-256；机器manifest分别登记`runtime_input_evidence`与`tracked_evidence`，换行差异不得冒充科学内容漂移。
- `local_run_evidence`只登记本机内部run的不可逆SHA-256、长度和artifact ID，不含目录、原始I3D序列、模型内容、预测正文或本机绝对路径。

离线复核命令：

```powershell
.\.venv-task20\Scripts\python.exe scripts\validate_task20_handoff.py
```

该命令不需要受限I3D资产或本机run bundle；它从Git对象库读取声明commit的原始tracked证据进行核验。

## 冻结输入与数据角色

| 输入 | 运行时SHA-256 | Git快照SHA-256（`b89d8dc`） | 冻结角色 |
|---|---|---|---|
| `HANDOFF_10.md` | `47de656e7a8ff391118858bc932b5f7f1b089d98575b1a29e3f608b4e4ac66fb` | 同左 | 上游标签、split、风险与禁止动作 |
| `dataset-v1.manifest.json` | `1b8ba9f5c4b801f9530b4e97c8f6b777db4562bce37b24d63aa341b64e3e806e` | `086e7094dd20249c456fdfc5fe97f2c0e530e1d7ba8116ebd82e5303f0054693` | 数据集版本与角色 |
| `split-v1.manifest.json` | `6a15f992b9e5839d6f21b4a6d40619f48bb14445b18a0c1814024794f56b6780` | `7f96f84a8c2cff0f3a1445302db41522e397a390b62de9274ac30b5d7a2a5d8f` | 正式split合同 |
| `label-provenance-v1.manifest.json` | `0ac81e2db69f1e883599cb654bb679d10c1411f570e97ab6c2678f7699ce5a43` | `ebb4afada253139be668500b257d31c53c19435f76041b6df43cf4fe7bdf8154` | 人工分布标签来源 |
| `leakage-audit-v1.manifest.json` | `982c5a75019ae6178f39797664aa390a65c336e2b78ef45c25ece96eb59991dc` | `23cfd8ec931b4fead93fc0d517cec472dfd80efc73e9d2db144c1c8b2f4afc28` | 泄漏审计与负门 |
| `T0_INPUT_POLICY.md` | 见Git证据 | `287356695d0be3b6cbbd5760ee926e43dde90437abf4bfcd920b3c1276cea1d5` | T0可用/禁用输入 |
| `experiment-protocol-v2.md` | 见Git证据 | `53a08ff90608c982c700759683566fb0a52216ebeed33f185b2406373ba4d976` | train/dev/test与实验协议 |
| `leakage-threat-model.md` | 见Git证据 | `88a4896012992c6c74b55f774bfe22227ddec8a12276f477fe85856a7218182c` | 泄漏威胁边界 |

完整22项tracked证据及长度以机器manifest为准。

## 正式split、标签与输入合同

- 主数据：CSMV HUMAN_GOLD，共8210个视频级样本。
- 唯一正式split：`group_by_video_v1`，train/dev/test=`5698/837/1675`；source family先归并后划分，禁止随机评论split。
- 目标：八类受众情绪分布，class order固定为`anger, anticipation, disgust, fear, joy, sadness, surprise, trust`。
- T0输入：获内部研究风险接受的冻结I3D视觉序列，主协议为`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`；评论、目标评论、未来互动和test标签均不是T0输入。
- 拟合边界：standardizer、模型、任何索引或选择只拟合train；dev只用于预注册调参与早停；test只按冻结selection评测一次且`test_adaptation=false`。
- CSMV没有原生topic，主题均值固定为`NOT_APPLICABLE_NATIVE_TOPIC_ABSENT`。
- 实际只有一个合法T0内容模态，E1、late fusion和multimodal cross-attention固定为`NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`；不得伪造模态增量。
- CUC 48维仅为`LEGACY_NATIVE_COMPATIBILITY_ONLY`：SILVER二分类、非T0、独立publisher-disjoint split=`1905/307/575`，不能与CSMV八类分布主结果比较。

## 正式环境锁

- Python `3.8.9`；PyTorch `2.4.1+cu121`；CUDA runtime `12.1`；NumPy `1.24.4`；scikit-learn `1.3.2`；transformers `4.30.2`；faiss-cpu `1.7.4`；CatBoost `1.2.10`；LightGBM `4.5.0`。
- 依赖锁：`requirements-task20-lock.txt`，Git快照SHA-256 `51e986891ba1ed64cebee6503fc820adc67c8b0dcfe5b7ef0bf8f78a1e3c3b6d`。
- 正式强基线使用本地NVIDIA GeForce RTX 3070 Ti Laptop GPU、float32、AMP关闭；远端A30运行时仍为`REMOTE_GPU_RUNTIME_UNAVAILABLE_ENVIRONMENT_NOT_READY`，不得改写为已就绪。
- 默认旧`.venv`缺faiss不是任务20正式环境；独立`.venv-task20`准备检查为`formal_model_work_ready=true`。

## 统一评测合同

统一输出九项指标：

1. Jensen–Shannon divergence（主指标，越低越好）；
2. negative log likelihood；
3. earth mover's distance；
4. Macro-F1；
5. Balanced Accuracy；
6. Brier score；
7. ECE；
8. ACE；
9. AURC-JS。

预测行固定包含sample ID、split、真实分布、预测分布、置信度、拒绝分数、model ID和config ID。E0会拒绝train/eval重叠、sample ID错位、非法概率和错误class order。视频级paired bootstrap接口已验证；正式五种子统计与正式配对比较属于任务50，当前状态为`TASK50_NOT_COMPLETED`。

## 调参预算与模型选择

- 配置：`configs/task20/tuning-plan-v1.json`，SHA-256 `01878e74f6f9c150d583ad591b0b7b5fb662208119076aef51ccb237ab741cf9`。
- 每个登记模型族最多12个trial；不同模型只能改变model字段，不得改变split、输入、指标或test规则。
- 冻结I3D pooled MLP与temporal attention网格：hidden dim=`128/256/512`，dropout=`0.1/0.3`，learning rate=`0.0003/0.001`；max epochs=200，patience=20。
- dev选择顺序：JSD、NLL、Brier、较少参数；仍相同时使用稳定trial顺序。test在selection冻结前不可见。
- temporal-attention选中trial 4：hidden=128、dropout=0.3、learning rate=0.001、best epoch=5；selection SHA-256=`dce53eeb8f3d618d2ed6e09fecc49164a0e6ac72b5254a065ebf4f493c97dfbf`。
- CatBoost/HGB/LightGBM的原生legacy重跑也各为12 trial，只用各自dev选择，test各调用一次；其数值只进legacy附表。

## 基线身份与失败状态

| 基线 | 身份 | 状态/边界 |
|---|---|---|
| 总体均值、经验分布、多数类 | `REIMPLEMENTATION` | train-only实现与dev smoke完成 |
| 主题均值 | `REIMPLEMENTATION` | `NOT_APPLICABLE_NATIVE_TOPIC_ABSENT` |
| 48维CatBoost/HGB/LightGBM | `LEGACY_NATIVE_COMPATIBILITY` | 已原生重跑；非T0、非同任务、不可承担主结论 |
| VC-CSA | `OFFICIAL_REPRODUCTION_ATTEMPT` | `FAILED_OFFICIAL_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH` |
| 冻结I3D pooled MLP | `REIMPLEMENTATION` | 工程smoke；未作为正式主数值 |
| 冻结I3D temporal attention | `REIMPLEMENTATION_STRONG_BASELINE` | 单种子正式dev/test及dev replay完成；不是VC-CSA官方复现 |
| CLIP/SigLIP/VideoMAE+MLP | `REFERENCE_MODEL` | `NOT_AVAILABLE_IN_FROZEN_T0_PROTOCOL`，不另行下载或伪造 |
| late fusion/cross-attention | `REIMPLEMENTATION` | `NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY` |

失败根因完整保留在`TASK20_BASELINE_EXECUTION_AUDIT.md`，不得因G3复核而删除或改写。

## 正式run与重复一致性

- 正式dev：5698 train / 837 dev、seed `20260717`、12/12 trial；dev JSD=`0.17701422654440738`。
- 唯一正式test：1675条预测，冻结selection后只运行一次；没有test适配或test后调参。
- 正式dev replay：相同环境、seed、config、input、代码文件hash和split，attempt 2耗时833秒；未读取test。
- 原dev与replay的`predictions`、`metrics`、`selection`、`trial_results`四项SHA-256逐字节一致；model state和train-only standardizer SHA-256也一致。
- 该证据范围仅为`SAME_ENVIRONMENT_FIXED_SEED`，不证明跨硬件、跨驱动或跨PyTorch release的bitwise复现。

关键不可逆run证据：

| artifact ID | SHA-256 |
|---|---|
| formal dev predictions | `e08c5b3d94217d145e94baa03ad6e0323c150898cee0d12a2044f78152760cbf` |
| formal dev metrics | `0271a6547d6245bd1fcd1cee9615af30bedf7fb588048f67369e58ce70ae2100` |
| formal dev trial results | `b5a246c3422052487e38baede213bf8c92c052e8782bdf75bc5bb01c1ba14f1f` |
| formal test manifest | `0f5949a8dce4922dcb2559054370288f1e037408b722d3b68b0d0432c0539186` |
| formal test predictions | `ca7276b759248ef0c8fcc17ee1ea98bafcb88d41161d4e1feec6251d698bba9f` |
| formal test metrics | `05f4785cc084bfc8ebe04a8f1d035ac81c97d127347dc4712cd1fe25fa2aeb7e` |
| dev replay manifest | `2b5b3473473ffe1d50435d2838642de1cae00b6618b29f93df79a5facfcfde3d` |
| reproducibility comparison | `5d85fa1dbfdd263e5c5086e57bab3ce5305af4c340e28cf4315a1bbcbea1458d` |

完整artifact长度与hash见机器manifest。

## 单种子正式test结果

| 指标 | 值 |
|---|---:|
| JSD | 0.18266823488401895 |
| NLL | 1.7151920543922174 |
| EMD | 0.1629829121007144 |
| Brier | 0.22737851247036292 |
| ECE | 0.053885089409458985 |
| ACE | 0.05400352094861094 |
| AURC-JS | 0.17539896294783275 |
| Macro-F1 | 0.13704838144402784 |
| Balanced Accuracy | 0.14857733746597548 |

这些是单种子内部研究证据，不是任务50最终论文统计，也不支持“优于所有方法”的主张。

## 已完成项

- 独立正式环境与依赖锁；统一schema、loader、run manifest和prediction格式。
- 最低基线、legacy原生兼容重跑、强视觉重实现、九项指标、E0、bootstrap接口、等预算调参合同。
- smoke、单种子完整run、test一次评测、同环境同seed正式dev replay。
- `BASELINE_TABLE_V1.md`、失败根因审计、实验登记、G3证据包与本交接。
- 全量测试、compileall、工作日志验证和准备检查在证据提交前通过。

## 未完成、不可用与后续归属

- `TASK50_NOT_COMPLETED`：五种子、正式bootstrap、paired comparison和论文级统计结论由任务50完成。
- VC-CSA官方代码缺失且输入目标评论不符合T0，官方复现失败状态继续保留；没有计划用论文数字填补。
- CLIP/SigLIP/VideoMAE不在冻结T0协议；late fusion、cross-attention和E1因单可用模态不适用。
- teacher、memory和完整CARM均未在任务20引入；只允许在00通过G3并创建任务30后按新任务合同开发。
- 远端A30运行时未就绪；任务20正式强基线已在用户授权的本地GPU完成，不得倒写为A30结果。

## 资产风险与强制止损

- I3D许可、官方revision、权利方包身份/fixity仍未知；`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`，仅授权内部研究。
- 禁止提交、发布或再分发I3D `.npy`、junction、模型权重、standardizer、预测正文、本机路径或可逆受限资产。
- 若权利方否认、固定hash漂移或8210覆盖漂移，立即停止相关工作并标记`ASSET_INVALIDATED_DO_NOT_REPORT`；回交任务00/10，不得继续报告相关结果。
- 总门继续为`PASS_WITH_ACCEPTED_ASSET_RISK`；本交接不把资产风险改写为已解决。

## 下游任务30必须继承的合同

1. 启动前必须读取本文件、机器manifest、`T0_INPUT_POLICY.md`、`experiment-protocol-v2.md`和冻结调参计划。
2. 不得修改统一评测器、split、class order、主指标、test规则或任务20已冻结基线来迁就新模型。
3. teacher只能使用训练期允许信息；test评论、test标签和未来互动不得进入训练、检索、早停或选择。
4. 所有index、standardizer、feature selection和memory只拟合train；dev选择；test按预注册规则一次评测。
5. 不得把temporal-attention写成VC-CSA官方复现，不得把单种子结果写成任务50完成。
6. 若00最终G3不是PASS_WITH_LIMITATIONS/PASS，任务30保持冻结。

## 00复核探针

00可用以下六问快速检查交接完整性：

1. 证据主体commit是什么？`b89d8dc1d62b5d6ea7b07b1d30cc8f19224c030d`。
2. 正式split是什么？`group_by_video_v1`，5698/837/1675。
3. test是否重跑用于任务15一致性？否，只重跑dev；test总计按冻结selection评测一次。
4. 强基线身份是什么？`REIMPLEMENTATION_STRONG_BASELINE`，不是VC-CSA官方复现。
5. 当前最重要限制是什么？I3D为`DEFERRED_ACCEPTED_RISK`且任务50未完成。
6. 什么情况必须停止报告？权利方否认或固定hash/8210覆盖漂移，标记`ASSET_INVALIDATED_DO_NOT_REPORT`。

只有机器validator通过且六问答案与本文件一致，才应进入00最终G3裁定。
