# T-AFFC CARM项目总控完整交接（2026-07-17）

> 用途：替代超长聊天上下文，供新的00总控项目直接接管。  
> 源总控任务：`019f5c27-10fa-7e13-857d-77505594f7fc`  
> 执行仓库：`D:\MMSA-CH-SIMS`  
> GitHub：`xjq801/MMSA-CH-SIMS`  
> 当前SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.16  
> 本文是压缩交接，不覆盖SSOT、manifest、决策台账或实时Git状态；接手后必须先刷新现实。

## 1. 用户真实目标与最早纠偏

1. 项目业务始终是“群体情绪预测/公众诱发受众情绪分布预测”。早期曾把“圣遗物的重塑”误读为《原神》系统；用户明确要求忽略该解释。后续任何任务都不得恢复游戏业务理解。
2. 用户曾提供五份论文修改纲要Word文档作为参考，但随后指定`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md`为唯一总纲。参考文档不能覆盖总纲。
3. 用户要求先完成开工准备包：T0输入政策、Git初始化、环境锁定、数据来源台账等；已完成部分不得重复。
4. 项目最终目标：在2027-05-12前形成可直接提交IEEE T-AFFC的CARM群体情绪预测论文、代码、数据说明和证据链。目标是高质量提交，不是保证录用。

## 2. 当前研究问题与冻结边界

- 构念：`public-induced audience affect`，即内容发布后多名受众在评论中表达的情绪反应经验分布；不是说话者自身情绪、画面中多人共同情绪，也不是传播链指标。
- 主任务：T0内容预测。推理时只允许发布时可见且经协议冻结的内容输入；目标评论、未来互动量、推荐结果和任何标签生成信息不得进入学生推理输入。
- 主输出：K类受众情绪分布、分歧/熵、预测不确定性与拒绝分数；旧二分类风险只作次任务。
- 统计、split和bootstrap单位均为内容项：CSMV按视频，LAI-GAI按图像；不能把评论、fold或seed当独立样本量。
- 主指标：Jensen–Shannon divergence；辅以NLL、Wasserstein/EMD、Brier、ECE/ACE、risk-coverage、AURC等。正式结果至少5 seeds，按内容项paired bootstrap 95% CI并做配对检验和多重比较校正。

## 3. 三项贡献上限与假设

### C1：无泄漏的公众诱发情绪预测协议

评论仅作标签或训练期特权监督；视频/同源事件分组；金标、银标、test物理隔离；从硬标签升级为分布、分歧和不确定性。不得声称“首次提出公众诱发情绪预测”。

### C2：评论特权教师 + 可拒绝的受众反应记忆

训练期教师读取内容与评论；学生训练/推理只看合法T0内容；memory只存train内容、反应分布与置信信息；可靠性路由根据相似度、邻居分歧、域/时间距离与输入质量融合、降权或拒绝。

### C3：跨话题、跨平台和自然缺失下的可靠性证据

必须报告跨split/OOD、校准、选择性风险、效率和失败案例。只有同一样本至少两个实际T0输入模态时才有缺失模态实验资格；不得伪造音频或把结构性无音频写成随机缺失鲁棒性。

### 假设

- H1：评论特权教师能稳定改善CSMV内容学生；LAI-GAI缺少同构评论字段时为`NOT_APPLICABLE_BY_DESIGN`。
- H2：train-only反应记忆有效，可靠性拒绝可减少OOD负迁移；必须比较no/random/BM25/CLIP-kNN/learned retrieval。
- H3：仅对合格的真实多输入协议检验缺失感知平稳退化；无合格协议则`NOT_APPLICABLE_NO_ELIGIBLE_MULTIMODAL_PROTOCOL`。
- H4：NEmo+配对T/I/TI增强为可选，不是当前硬门。

## 4. 数据事实与唯一权威版本

### CSMV主集

- 8,210个内部视频、107,267条人工评论反应。
- 早期“2,644行内部ID与URL路径ID错配”被证明是命名空间误判：前者是`video_file_id`，后者是平台源视频ID，官方README未要求二者相等。
- 8,210条映射覆盖100%，形成8,008个平台源视频族；202个重复源族涉及404条记录。
- 修复后所有正式协议同源族跨split为0。
- `group_by_video_v1`：train/dev/test=`5698/837/1675`。
- `hashtag_heldout_v1`：train/dev/test=`7211/327/672`。
- 无原生topic与发布时间；不得声称topic-held-out或时间安全。

### CSMV I3D输入

- 用户本地包只读隔离接入；全包9,942个`.npy`，正式必需8,210键覆盖100%。
- schema为`float32[T,1024]`；本地文件树、体量、逐文件SHA-256和覆盖已闭合。
- 8,210样本长度`T=6—1719`；531个`T>180`，4个`T=180`，中位数43，P90=133，P95=211，P99=339。
- 主序列协议：`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`；完整保留序列、batch内右补零、`True=observed` mask。
- 主敏感性：`UNIFORM_180_ENDPOINT_INCLUSIVE`；长序列首尾覆盖均匀180步。`FIRST_180_ONLY_FIXED_DIAGNOSTIC`仅作补充。
- 本地隔离包内容树SHA-256历史记录为`35be2d18e1d2413ba3765034cdb454baa5e3496d49c540c9be00e81bbc2c1942`；当前manifest及其引用以仓库机器文件现场值为准。
- 官方仓库Issue #5已由用户手工创建，请求I3D许可、revision、文件manifest/hash、8210覆盖和schema；维护者尚无实质回复。不要等待或催促作为当前启动前置。
- 音频=`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`，不下载、不插补、不伪造，不声称音视频融合或音频增益。

### LAI-GAI第二人工跨域图像主集

- 唯一正式版本：`LAI-GAI@v05-2026-03-11`。
- 847张AI生成情感图像、63,682条合规人工响应、12维人工诱发情绪连续分布。
- 严格按source/prompt/exact/dHash形成379组，split=`594/127/126`，group/精确/近重复跨split均为0。
- canonical SHA-256：`ad58c268e34adf02bd8e639338069d34576e1d9602f819a2cc6fa89be6836818`。
- 生成prompt、目标生成类别和模型标签只作provenance，不是真值，默认不作主输入。
- 它承担跨域图像、校准/OOD和结构性输入边界证据；不冒充第二视频集，不强制复刻CSMV的H1/H2。
- 历史OSF API审计曾有0.996519秒速率间隔偏差及空组件文件树；该失败保留为历史，不覆盖后续独立授权形成的正式冻结事实。

### CUC与其他数据

- CUC-IGPE-v2为本地SILVER/中文压力测试层：2,787 canonical记录、221条标签冲突、8条缺BV、1,904条缺发布时间；不能进入人工金标test。
- MVIndEmo只能作银标辅助；不能替代第二人工主集。
- NEmo+可选支持H4，尚不是当前任务20硬门。

## 5. 当前G门与风险接受裁定

当前权威状态由`SC-20260717-01`和`TASK00_G2_RISK_ACCEPTANCE_AND_TASK20_AUTHORIZATION_20260717.md`确定：

- `G1=PASS`
- `G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`
- `ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`
- 总门`G2=PASS_WITH_ACCEPTED_ASSET_RISK`
- `formal_split=true`
- `internal_model_use_allowed=true`

含义：样本血缘、标签隔离、T0隔离、泄漏正负门、第二主集、I3D本地fixity/schema/覆盖、序列协议、19项隔离复现和M2 release已经通过；I3D资产级许可、稳定官方revision和权利方包身份/fixity仍未知，但用户接受延期风险，不再阻止内部任务20。

这不是许可证据。禁止提交、公开或再分发I3D `.npy`、junction、本机源路径或可逆受限资产；禁止声称权利方已授权或官方包身份已确认。若权利方否认研究使用，或固定字节/hash/8210覆盖漂移，立即停止并将相关结果标记`ASSET_INVALIDATED_DO_NOT_REPORT`。

## 6. 任务树、线程与当前进度

| 任务 | 状态 | 责任/门 |
|---|---|---|
| 00 总控 | 本交接后由新总控项目接管 | SSOT、决策、G1—G6、风险和任务创建 |
| 10 M1–M2 数据与协议 | 已完成并交接 | G1/G2协议数据、manifest、泄漏、数据文档 |
| 20 M3 基线与统一评测 | 已启动，部分完成 | 统一评测器、强基线、G3 |
| 30 M4 评论教师与内容学生 | 未创建 | 只有G3通过后创建；验证H1 |
| 40 M5 反应记忆与可靠性检索 | 未创建 | H1开发门后创建；验证H2 |
| 50 M6–M8 正式实验与结果冻结 | 未创建 | G4/G5/G6、5 seeds、统计、冻结结果 |
| 60 M9–M10 论文与投稿 | 未创建 | G6后写作、图表、复现包、投稿 |

关键Codex任务：

- 旧总控/源任务：`019f5c27-10fa-7e13-857d-77505594f7fc`。
- 任务10主要执行来源：`019f5cf3-1810-7cd2-95bb-ff603551571b`。
- 任务20：`019f6e2e-f781-7270-bb45-af8272ff5a5c`。

### 任务20最新事实

- commit `5522619`已推送`origin/main`：新增`configs/task20-baseline-v1.yaml`、`scripts/task20_baseline.py`、`tests/test_task20_baseline.py`、`requirements-task20-lock.txt`及`.planning/task20-m3/`。
- 最低基线/loader/指标合同单测3/3通过，compileall和diff check通过。
- 独立`.venv-task20`已建立但不进Git；安装`pytest/faiss-cpu`因代理不可连接失败。
- `run_preparation_checks.py`仍真实报告`formal_carm_environment=BLOCKED_M1`、`faiss_available=false`、`formal_model_work_ready=false`，同时`blocking_checks=[]`。
- `blocking_checks=[]`不等于正式模型环境就绪。任务20下一步应恢复可用包源/代理，在独立环境安装并验证faiss，然后接入权威manifest受控样例，生成prediction/run manifest与指标输出。
- 未完成G3前不得创建任务30，不得提前引入teacher、memory或完整CARM。

## 7. 已验证的M1–M2证据

- 泄漏live门Critical=0；负面夹具正确输出`LEAKAGE_BLOCKED`。
- Python 3.8.9、`-I -S`公共核心隔离重放19项输出，before/after一致、`mismatches=[]`。
- M2 data engineering、M2 release、LAI-GAI专项、CSMV lineage和I3D序列专项均通过。
- I3D序列8项单测通过。
- 历史失败必须保留：OSF API速率间隔、首次GitHub集成403、首次M2构建漏`--public-core`、首次release在授权状态变化后出现6项预期复现mismatch、任务20独立环境包安装失败。后续不得把这些写成“从未失败”。

## 8. IJCV方向已经迁出

- 曾评估IJCV专刊“Social, Emotional, and Cognitive Visual Intelligence”，认为方向有条件匹配，但当前I3D+CARM不足以直接形成IJCV视觉方法贡献。
- 随后用户决定分项目：IJCV完整路线迁至`D:\MMSA-CH-SIMS - IJCV方向`，历史分支`codex/ijcv-j0@c64c954`。
- 当前仓库从总纲v1.15起只执行T-AFFC CARM路线；禁止创建或执行J0—J2、JH1—JH3、任务25或任务65。
- 两项目只能通过已提交Git状态和书面交接共享通用事实；不得并发修改同一实验核心，也不得把IJCV主方法/主结果纳入本稿。

## 9. 网络、下载与执行政策

- 访问网站或下载时优先使用本机代理`127.0.0.1:7890`；代理不可用可直连或切换可信第三方镜像，以效率为先。
- 允许扩大公开、免费、无需登录资产的取得范围并放入Git忽略隔离区，但必须记录来源、revision/时间、体量和hash。
- 不得绕过登录、访问控制、验证码、付费墙、地域/账户权限或服务配额；EULA/DUA、付费和机构承诺仍需用户另行确认。
- 第三方镜像与下载成功不等于许可或再分发权；未知项必须保留。
- 下载采用`.part`、续传、有限并发/重试、完成后原子改名与SHA-256。

## 10. Git与记录纪律

- 仓库：`D:\MMSA-CH-SIMS`；主分支`main`；远端`https://github.com/xjq801/MMSA-CH-SIMS.git`。
- 本交接前最新已推送commit：`5522619`；关键前序：`e805fc3`（任务20线程交接）、`f869732`（G2风险接受并放行20）、`987e2a1`（非资产G2复审）。
- 开工先读`AGENTS.md`、`WORK_RECORD_POLICY.md`、`WORK_LOG.md`最后一条并运行`git status --short --branch`。
- `WORK_LOG.md`只能追加，不能改写历史；实质进展、失败、测试、决策和阻塞变化必须同批记录。
- 交付前运行`validate_work_log.py`与`run_preparation_checks.py`；失败不得删除，未推送不得写成已同步。
- 旧审计/复审文件中仍保留当时`formal_split=false`或G2 blocked的历史状态；不得用全文搜索命中旧句就覆盖当前v1.16裁定。当前事实优先级：总纲v1.16 → 最新正式决策/授权 → 当前machine manifests → 最新工作日志/Git现实 → 历史审计。

## 11. 新总控职责与最近三步

新总控只做00责任：监督SSOT、核实证据、批准G门、协调任务、更新风险/决策/claim台账；不要与任务20并发修改实验核心。

1. 读取本交接、总纲v1.16、`.light/passport.yaml`、`.light/project_card.md`，然后刷新Git与任务20实时状态。
2. 监督任务20先闭合独立环境/faiss和统一prediction/run manifest，再按总纲任务20完成公平强基线；没有G3证据不创建任务30。
3. 任务20回交后，00独立复核同split/同输入/同评测器、调参预算、泄漏、官方/强基线复现与可追溯性，书面裁定G3。

## 12. 必读文件索引

1. `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md`
2. `TASK00_G2_RISK_ACCEPTANCE_AND_TASK20_AUTHORIZATION_20260717.md`
3. `HANDOFF_10.md`
4. `G1_G2_EVIDENCE_MATRIX.md`
5. `WORK_RECORD_POLICY.md`与`WORK_LOG.md`末条
6. `T0_INPUT_POLICY.md`、`experiment-protocol-v2.md`、`leakage-threat-model.md`
7. `data/manifests/dataset-v1.manifest.json`、`split-v1.manifest.json`、`label-provenance-v1.manifest.json`、`reproducibility-v1.manifest.json`
8. `CSMV_I3D_SEQUENCE_PROTOCOL_V1.md`及`data/manifests/csmv-i3d-sequence-protocol-v1.manifest.json`
9. `.planning/task20-m3/task_plan.md`、`configs/task20-baseline-v1.yaml`、`scripts/task20_baseline.py`
10. `.light/handoff/S01-total-control-migration.md`

## 13. 压缩质量自检问题

新总控读完后应能准确回答：

1. 当前G2为什么能放行任务20，但仍不能声称I3D许可已闭合？
2. CSMV内部ID与平台URL ID为何不要求相等，正式source-group和split是多少？
3. LAI-GAI唯一正式分组/split/canonical hash是什么，prompt为何不是真值？
4. 任务20当前真正阻塞是什么，为什么`blocking_checks=[]`不等于环境ready？
5. 哪些条件满足前不能创建任务30？
6. IJCV任务为何不属于本仓库？

若不能回答，先重读对应权威文件，不得凭摘要猜测。
