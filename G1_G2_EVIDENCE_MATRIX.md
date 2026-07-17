# G1/G2逐条证据矩阵

> 审核对象：任务10 / M1—M2
> 版本日期：2026-07-17
> 总体结论：G1=`PASS`；2026-07-17非资产复审确认无第二个技术阻塞。用户随后书面接受I3D资产外部证明延期风险，00依据`SC-20260717-01`裁定G2=`PASS_WITH_ACCEPTED_ASSET_RISK`：`G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`，`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`，`formal_split=true`，任务20获准创建。

## G1（最低合格）

| 总纲条件 | 状态 | 证据 | 判定依据/缺口 |
|---|---|---|---|
| 两个合法可用公开数据源 | **PASS** | `DATA_SOURCE_LEDGER.md`、`lai-gai-second-primary-raw-v1.manifest.json`、`TASK00_LAI_GAI_SECOND_PRIMARY_FREEZE_REVIEW_20260715.md` | CSMV人工标签可用；LAI-GAI官网847图、CC BY 4.0、评分文件、人工标签与逐图hash已闭合。旧K8XVH空节点不作为新授权的资产来源 |
| CSMV可按视频分组 | **PASS** | `csmv-primary-raw-v1.manifest.json`、`csmv-split-v1.manifest.json`、`M2_LEAKAGE_AUDIT.md` | 107267条正式评论归属8210视频；视频组跨split交集为0 |
| 第二主集已冻结 | **PASS** | `second-primary-label-map-v1.manifest.json`、`lai-gai-label-provenance-v1.manifest.json`、`lai-gai-split-v1.manifest.json` | `FROZEN_00_APPROVED`；847条`HUMAN_GOLD`、12维连续分布、379组与594/127/126正式split |
| 自建时间可恢复或明确降级 | **PASS_WITH_LIMITATION** | `cuc-canonical-v1.manifest.json`、`CUC_CANONICAL_AUDIT.md` | 仅883/2787有时间；1904缺失，已明确降级为本地辅助且不发布time split |

**G1总判定：`PASS`。** 四项最低合格条件全部满足；第二主集缺口已关闭。

## G2/L2（论文证据级）

| 总纲条件 | 状态 | 证据 | 判定依据/缺口 |
|---|---|---|---|
| 100%样本可追溯 | **PASS_LABEL_AND_URL_METADATA / BLOCKED_FORMAL_INPUT** | CSMV/CUC raw manifest、`csmv-media-lineage-v1.manifest.json`、`csmv-feature-preflight-v1.manifest.json`、LAI-GAI raw/label manifests | LAI-GAI 847/847闭合；CSMV 8210/8210标签与内部ID→URL hash→8008源族闭合。官方README确认特征命名合同，但公开Drive首屏未暴露资产许可、revision、文件树、size/hash或实际8210键，故正式输入仍UNKNOWN |
| 人工标签与银标物理隔离 | **PASS** | 三个tier manifest、`load_label_tier.py` | 目录、manifest、加载入口独立；混装负测拒绝 |
| test评论与输入物理隔离 | **PASS_CURRENT_CSMV** | `human-gold-v1.manifest.json`、泄漏报告 | 派生记录不含评论正文/目标评论字段；评论仅作标签聚合 |
| 正式split泄漏测试零失败 | **PASS_OBSERVABLE_SCOPE** | `lai-gai-split-v1.manifest.json`、`validate_lai_gai_second_primary.py`、`csmv-media-lineage-v1.manifest.json`、`leakage-audit-v1.manifest.json` | LAI-GAI专项零Critical；CSMV 8008源族在video/hashtag协议跨split均为0，负面夹具可阻断；内容指纹/publisher/time不作已证明主张 |
| 预处理可从manifest重跑 | **PASS_CURRENT_PUBLIC_CORE** | `reproducibility-v1.manifest.json`、`scripts/reproduce_m2_minimal.py`、`scripts/validate_m2_release.py`、`TASK00_CSMV_FEATURE_PREFLIGHT_G2_REVIEW_20260715.md` | 00独立重跑`--public-core`：Python `-I -S`、冻结CSMV raw manifest、两套split、泄漏与release；冻结CUC只做字节核验。19项before/after和现场hash全部一致，漂移0；复现陈旧子阻塞关闭 |
| 音频是否为正式输入硬门 | **NOT_REQUIRED_WITH_DISCLOSED_LIMITATION（00已确认）** | `TASK10_AUDIO_MODALITY_FEASIBILITY_REVIEW_REQUEST_20260716.md`、`TASK00_AUDIO_MODALITY_PROTOCOL_REVIEW_20260716.md`、CSMV固定README、NeurIPS 2024论文、T-AFFC General CFP | 音频=`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`并移出G2/取得关键路径；不得据此声称音频实验、随机缺失鲁棒性或自动放行G2 |
| I3D序列处理预注册与可复现 | **PASS_PROTOCOL_ONLY（00已确认）** | `CSMV_I3D_SEQUENCE_PROTOCOL_V1.md`、`csmv-i3d-sequence-protocol-v1.manifest.json`、`TASK00_CSMV_I3D_SEQUENCE_PROTOCOL_AND_GIT_CHECKPOINT_REVIEW_20260716.md`、专项validator与8项单元测试 | 主协议完整序列+mask；主敏感性确定性均匀180步；531个超长样本与资源上限已冻结；00已关闭协议未冻结子缺口，但此PASS不授予资产许可或G2信用 |

**G2总判定：`PASS_WITH_ACCEPTED_ASSET_RISK`。** `G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`；本地相对文件名/体量/逐文件hash、特征schema、8210键覆盖、泄漏门、复现和序列协议均已闭合。资产级许可、稳定官方revision及权利方包身份/fixity保持`DEFERRED_ACCEPTED_RISK`，不计作已解决；用户授权其不再阻塞内部任务20。

维护者外部证明现按用户指令标记`DEFERRED_PENDING_MAINTAINER_REPLY`：暂时跳过协调，不等待、不催促、不重复检查；延期不等于缺口关闭。

## 2026-07-17 非资产G2反事实复审

用户要求暂时忽略CSMV I3D资产准入并检查G2。00现场复核结论为`PASS_NON_ASSET_G2_REQUIREMENTS_WITH_LIMITATIONS`：排除资产级许可、稳定官方revision与权利方包身份/fixity证明后，G2其余数据血缘、标签隔离、T0评论隔离、泄漏正负门、第二主集、I3D序列协议、19项隔离复现和M2本地发布包均通过，未发现第二个非资产阻塞。详细证据见`TASK00_G2_NON_ASSET_COUNTERFACTUAL_REVIEW_20260717.md`。

该反事实检查随后由用户正式转化为`SC-20260717-01`范围变更：总纲和机器合同已修改，G2=`PASS_WITH_ACCEPTED_ASSET_RISK`，ASSET_ADMISSIBILITY=`DEFERRED_ACCEPTED_RISK`，`formal_split=true`，任务20获准创建。未知许可仍不得写成已通过。

## 止损执行

- 不训练模型、不建立正式索引、不创建任务20。
- 公开资产可按效率政策进入Git忽略隔离区审计，但隔离取得不得冒充正式准入；不绕过访问控制，不因下载成功自动获得许可或G2信用。
- 不把银标写成人工金标，不把`NOT_APPLICABLE`时间检查写成时间安全PASS。
- `AUTH-00-LAI-GAI-OSF-META-RO-20260714`只读审计已完成：三组件页面未提供足以核验的节点级资产元数据，全部缺失字段已保持`UNKNOWN`，裁定`NO_GO_PENDING_ASSET_METADATA`。
- `AUTH-00-LAI-GAI-OSF-API-META-RO-20260714`已执行：26次匿名GET、382,394B、全HTTP 200；三节点均public/CC BY 4.0，但`K8XVH`文件列表为空，且一次UTC请求间隔0.996519秒低于1秒硬门，裁定`NO_GO_PENDING_RATE_INTERVAL_AND_IMAGE_COMPONENT_FILE_TREE`。
- 00复审`REVIEW-00-LAI-GAI-OSF-API-20260714`接受上述结果为`OBSERVED_WITH_PROTOCOL_DEVIATION_NO_GATE_CREDIT`；不追溯豁免速率失败，不批准重跑，`K8XVH`空文件树仍是独立Critical准入缺口。
- 用户后续明确要求完成第二主集，00独立签发`AUTH-00-SECOND-PRIMARY-RESOLUTION-20260714`。新授权未重跑旧26请求，改从官网Data Card、图片浏览器与既有OSF评分元数据闭合847图及63682人工反应；旧失败证据原样保留。
- 新专项validator返回`LAI_GAI_SECOND_PRIMARY_READY`：图像/评分fixity、标签构念、敏感字段、source group、精确/近重复和split覆盖全部通过。该结果是00复审输入，不是任务10自行修改G门。
- 00复审`REVIEW-00-CSMV-LINEAGE-G2-20260715`接受CSMV lineage/split修复但不放行G2；已签发只读特征资产预审授权，`formal_split=false`与任务20禁令保持不变。
- 特征预审已按授权完成：公开Drive页匿名GET为HTTP 200，但初始页面没有可核验资产清单；I3D/VideoMAE的许可、revision、文件数、体量、checksum和8210覆盖全部诚实保留`UNKNOWN`，裁定`NO_GO_PENDING_ASSET_METADATA_AND_LICENSE`。
- 公共benchmark核心隔离重放已完成：不访问CUC外部根，19项输出现场漂移0；release validator现对`after_sha256`逐项重算，任何漂移都会失败。该本地PASS等待00独立复审，不自行放行G2。
- 00复审`REVIEW-00-CSMV-FEATURE-PREFLIGHT-G2-20260715`接受上述19项复现PASS并关闭陈旧子阻塞；同时接受特征预审为诚实No-Go。已签发单一特征族元数据协调授权，不含`.npy`或媒体下载。
- 首次官方GitHub Issues协调因集成创建Issue权限不足返回403，无issue定位符、无外部写入。`REVIEW-00-CSMV-I3D-METADATA-COORDINATION-ATTEMPT-20260715`将其裁定为传输/权限阻塞而非权利方拒绝；原一次请求额度未消耗，只允许同一渠道手工提交或补权限后重试，G2不变。
- 用户随后在官方仓库创建公开Issue #5；`REVIEW-00-CSMV-OFFICIAL-ISSUE-5-SENT-20260715`独立确认其Open、创建日期和元数据请求字段，正式请求额度已使用。2026-07-22前不得跟进；Issue成功不提供资产准入信用，G2继续阻塞。
- `POLICY-00-EFFICIENCY-FIRST-MIRROR-AND-EXPANDED-ACQUISITION-20260715`允许官方副本或可信镜像隔离预取公开候选特征；镜像身份、hash和覆盖须单独记录。隔离预取不关闭许可/fixity缺口，不改变G2。
- 用户提供`I3D-feature-001`后，任务10建立Git忽略junction并完成全包审计：9942个`float32[T,1024]`数组、总计2,752,998,144 bytes、8210/8210必需键覆盖、缺失0、schema错误0；8210个必需文件逐文件SHA-256及全包树hash已固定于`csmv-i3d-quarantine-v1.manifest.json`。该证据只取得`QUARANTINE_ACQUIRED`信用，尚未取得正式许可、官方revision或G2信用。
- `REVIEW-00-AUDIO-MODALITY-PROTOCOL-20260716`已确认音频不构成G2独立硬门；后续只收敛一个视觉特征族的资产准入。E1/E5/H3按实际可得输入条件化，音频和无合格多模态协议均使用明确`NOT_APPLICABLE`状态。
