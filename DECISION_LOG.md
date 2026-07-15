# 项目决策日志

> 维护任务：00-总控与决策  
> 规则：只追加，不覆盖历史决定；详细证据以总纲及被引用决定文件为准。

| 决定编号 | 日期 | 决定 | 依据 | 影响与边界 | 状态 |
|---|---|---|---|---|---|
| `SC-20260714-01` | 2026-07-14 | 将第二人工多模态主集降级为第二人工跨域图像主集/缺失模态验证集；LAI-GAI v05为优先审计候选 | 用户明确批准路径1；`G1_G2_REMEDIATION_REPORT_20260714.md`；`TASK00_LAI_GAI_SCOPE_AND_AUDIT_AUTHORIZATION_20260714.md` | 保留`public-induced audience affect`、`HUMAN_GOLD`、T0和JS；降低双视频复现主张；不放行G1/G2，不创建任务20 | APPROVED_SCOPE_CANDIDATE_NOT_FROZEN |
| `AUTH-00-LAI-GAI-OSF-META-RO-20260714` | 2026-07-14 | 授权任务10只读核验OSF `V8DKM/8P572/K8XVH`公开网页元数据 | `SECOND_PRIMARY_SCOPE_CHANGE_REQUEST_20260714.md` | 仅license/revision/file tree/size/hash/gating；禁止下载资产、API、登录、训练、formal split和任务20 | COMPLETE_NO_GO_PENDING_METADATA |
| `REVIEW-00-LAI-GAI-META-20260714` | 2026-07-14 | 接受任务10合规审计与`NO_GO_PENDING_ASSET_METADATA`；不批准API/下载/登录等扩权 | `M1_LAI_GAI_OSF_METADATA_AUDIT_20260714.md`；`TASK00_LAI_GAI_METADATA_AUDIT_REVIEW_20260714.md` | 任务10停止；建议的元数据专用OSF API方案须用户另行明确批准 | ACCEPTED_EXPANSION_NOT_AUTHORIZED |
| `AUTH-00-LAI-GAI-OSF-API-META-RO-20260714` | 2026-07-14 | 用户明确批准三个LAI-GAI OSF节点的限额元数据API只读GET | 用户回复“批准”；`TASK00_LAI_GAI_OSF_API_METADATA_AUTHORIZATION_20260714.md` | 仅`api.osf.io`、三个节点、GET、100请求/5 MiB、不跟随下载链接；不授权资产内容、评分字段、split、训练或任务20 | CLOSED_NONCONFORMING_NO_RERUN |
| `REVIEW-00-LAI-GAI-OSF-API-20260714` | 2026-07-14 | 接受API交付为带协议偏差的观察证据，不授予G门信用；不批准重跑 | `M1_LAI_GAI_OSF_API_METADATA_AUDIT_20260714.md`；`TASK00_LAI_GAI_OSF_API_METADATA_REVIEW_20260714.md` | 0.996519秒低于硬门；`K8XVH`文件树为空是独立准入阻塞；保留专项validator exit 1 | ACCEPTED_NO_GO_NO_FURTHER_ACCESS |
| `AUTH-00-SECOND-PRIMARY-RESOLUTION-20260714` | 2026-07-14 | 授权从公开、免费、无登录官方入口完成第二主集收口，并在LAI-GAI失败时切OASIS | 用户要求完成第二主集；同名授权文件 | 不继承旧API门信用；允许官方图像/评分取得、manifest、canonical和split；禁止付费、登录、绕过与任务20 | COMPLETE |
| `REVIEW-00-LAI-GAI-FREEZE-20260715` | 2026-07-15 | 正式冻结LAI-GAI为第二人工跨域图像主集，唯一版本为379组、594/127/126，并放行G1 | 冻结报告、三个核心manifest、重建器与专项validator | G2仍因CSMV媒体映射与全局语义审计阻塞；全局`formal_split=false`；不创建任务20 | FROZEN_G1_PASS_G2_BLOCKED |
| `REVIEW-00-CSMV-LINEAGE-G2-20260715` | 2026-07-15 | 接受CSMV内部ID/平台源ID命名空间纠正与8008源族split修复；不放行G2 | CSMV lineage审计、专项正负门、全局泄漏门、00现场hash复核 | G1保持PASS；G2阻塞转为正式输入资产许可/固定性与当前复现manifest陈旧；不创建任务20 | ACCEPTED_LINEAGE_G2_BLOCKED |
| `AUTH-00-CSMV-FEATURE-ASSET-PREFLIGHT-RO-20260715` | 2026-07-15 | 授权任务10只读核验官方README链接的CSMV视觉特征资产元数据，并修复本地核心复现门 | `TASK00_CSMV_FEATURE_PREFLIGHT_AUTHORIZATION_20260715.md` | 禁止登录/API/下载特征或媒体/访问TikTok；页面未显示项保持UNKNOWN；无后续下载授权不得取得内容 | AUTHORIZED_PREFLIGHT_ONLY |
| `POLICY-00-LOCAL-PROXY-TRANSPORT-20260715` | 2026-07-15 | 允许使用用户控制的本机代理访问官方数据来源，并传输已完成准入审查的数据 | 用户明确授权；`TASK00_LOCAL_PROXY_AND_DATA_DOWNLOAD_POLICY_20260715.md` | 代理仅作传输；凭证不落盘；不绕过访问控制；不自动批准大包、媒体、API、付费资源或任务20 | APPROVED_TRANSPORT_ONLY |
| `REVIEW-00-CSMV-FEATURE-PREFLIGHT-G2-20260715` | 2026-07-15 | 接受19项公共核心复现当前零漂移，关闭`REPRODUCIBILITY_STALE`；特征预审维持No-Go | 00独立重跑复现/release/泄漏正负门；特征专项`g2_asset_ready=false` | G1保持PASS；G2收敛为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；formal split与任务20禁令不变 | ACCEPTED_REPRO_CLOSED_G2_ASSET_BLOCKED |
| `AUTH-00-CSMV-ONE-FEATURE-FAMILY-METADATA-COORDINATION-20260715` | 2026-07-15 | 授权针对一个官方特征族进行最小权利方元数据协调 | `TASK00_CSMV_FEATURE_PREFLIGHT_G2_REVIEW_20260715.md`；同名授权文件 | 一次请求+一次跟进；仅许可/revision/manifest/覆盖/schema；可收≤5MiB纯元数据；禁止特征/媒体下载、Drive API、EULA和任务20 | AUTHORIZED_METADATA_COORDINATION_ONLY |
| `REVIEW-00-CSMV-I3D-METADATA-COORDINATION-ATTEMPT-20260715` | 2026-07-15 | 接受GitHub集成403且无外部写入；该结果不是权利方拒绝，原一次请求额度未消耗 | 协调报告、WR-20260715-015、00复审与手工Issue提交包 | 只可在同一官方Issues渠道手工提交或补权限后重试一次，二选一；G2、formal split和任务20禁令不变 | ACCEPTED_NO_EXTERNAL_WRITE_AUTHORIZATION_UNCONSUMED |
| `REVIEW-00-CSMV-OFFICIAL-ISSUE-5-SENT-20260715` | 2026-07-15 | 独立确认官方Issue #5已Open并覆盖许可/fixity/覆盖/schema请求；正式请求额度已使用 | 官方公开Issue #5、协调报告、WR-20260715-016、00复审 | 2026-07-22前不得跟进；之后仅可在同一Issue跟进一次；正文未逐字点名I3D，跟进时应明确；G2不变 | ACCEPTED_REQUEST_SENT_WAITING_RESPONSE |
| `POLICY-00-EFFICIENCY-FIRST-MIRROR-AND-EXPANDED-ACQUISITION-20260715` | 2026-07-15 | 允许可信第三方镜像、公开API和公开资产隔离预取，并扩大项目内部下载范围 | 用户明确要求效率优先；同名政策文件 | 法律许可不能自行扩大；镜像需血缘/hash；未知许可资产只进隔离区；付费/EULA/绕过仍禁；G2不变 | APPROVED_EXPANDED_ACQUISITION_WITH_QUARANTINE_GATE |
| `REVIEW-00-AUDIO-MODALITY-PROTOCOL-20260716` | 2026-07-16 | 音频非CSMV主协议/G2硬门，冻结为结构性不可得；E1/E5/H3按实际可得输入条件化 | 任务10复审请求、T-AFFC General CFP、CSMV固定README、NeurIPS 2024论文、总纲G2条款 | 音频移出取得关键路径；禁止音视频/音频增益/随机缺失主张；G2、`formal_split=false`与任务20禁令不变 | PASS_WITH_LIMITATIONS_AUDIO_NOT_REQUIRED_FOR_PRIMARY_PROTOCOL |
