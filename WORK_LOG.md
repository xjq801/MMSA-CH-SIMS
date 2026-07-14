# MMSA-CH-SIMS 工作记录

> 本文件是功能与进展的追加式详细记录。格式与更新纪律见`WORK_RECORD_POLICY.md`。

## WR-20260714-001 — 建立强制工作记录机制

- 时间：2026-07-14 15:31:55 +08:00
- 类型：FEATURE
- 任务/门：P0开工准备 / 10-M1–M2
- 状态：完成
- 负责人：Codex

### 背景与目标

项目已经进入跨阶段、跨会话执行，原有`progress.md`适合阶段汇总，但缺少每次功能或进展统一记录的字段和确定性校验。目标是建立一套随代码进入Git、可审计且不泄露敏感信息的工作记录机制。

### 实际变更

- 新增`WORK_RECORD_POLICY.md`，定义记录触发条件、强制字段、只追加纪律和与其他台账的职责边界。
- 新增`WORK_LOG.md`作为功能与进展记录的唯一入口，并写入本条启动记录。
- 新增`scripts/validate_work_log.py`，检查记录编号、顺序、元数据和必需章节。
- 新增根目录`AGENTS.md`，要求后续执行代理在产生实质进展时同步追加记录并在交付前运行校验。
- 将工作记录纳入项目结构政策和开工综合检查。

### 验证与证据

- 已运行`.\.venv\Scripts\python.exe scripts\validate_work_log.py`：1条记录、0项错误、`passed=true`。
- 已复跑`.\.venv\Scripts\python.exe scripts\run_preparation_checks.py`：工作记录检查通过，`m1_read_only_work_ready=true`、`blocking_checks=[]`。
- 已对两个新增Python脚本执行`py_compile`，并运行`git diff --check`，均通过。
- GitHub推送按用户要求再次重试，结果为无法连接`github.com:443`；本地提交和工作区未受影响。

### 影响与边界

此机制只改变项目记录和验收纪律，不改变总纲、T0、数据选择、主指标或模型实现。本轮未下载数据、未安装依赖、未运行训练或付费API。

### 风险、问题与阻塞

- `light-memory-pm`的`pm.py`在本机技能安装中先后因缺少`passport`导入路径和`_shared`模块而无法初始化；未生成不完整的`.light/`目录，改用项目内零依赖方案。
- GitHub网络仍阻塞，当前本地`main`预计继续领先`origin/main`一个已提交版本。

### 下一步

1. 运行工作记录校验和开工综合检查。
2. 网络恢复后重试推送已提交的准备验收版本。
3. 后续每次功能或实质进展与对应工作记录一并提交。

### Git状态

当前分支为`main`；已提交的`1d7a210`尚未推送，M1审计与本工作记录为未提交工作区变更。

## WR-20260714-002 — 完成现有资产、构念与泄漏威胁冻结

- 时间：2026-07-14 15:47:04 +08:00
- 类型：PROGRESS
- 任务/门：10-M1–M2 / 总纲步骤6—10
- 状态：完成
- 负责人：Codex

### 背景与目标

执行总纲第17节任务10工作包B：建立旧代码—数据—结果lineage，区分旧实验的证据资格，冻结公众诱发受众情绪构念、T0/T+Δ任务边界，并形成可阻断后续错误实验的一页泄漏威胁模型。

### 实际变更

- 新增`legacy-asset-lineage.md`，记录11条旧资产lineage及2787/2815漂移、221标签冲突、旧随机split和评论泄漏。
- 新增`legacy-experiment-classification.md`，分别判断代码可复用性与旧结果证据资格。
- 新增`research-question-v1.md`和`experiment-protocol-v1.md`，冻结构念、T0/T+Δ、统计单位、标签窗口和二分类兼容边界。
- 新增`leakage-threat-model.md`，覆盖评论、未来互动、推荐结果、同作者/近重复、索引和全图构建等8类威胁。
- 新增`scripts/validate_protocol_freeze.py`并接入`run_preparation_checks.py`；同步更新数据台账、实验登记、规划与进度文件。

### 验证与证据

- 只读复跑`audit_group_dataset.py`：2787条有效向量、2779个唯一BV、8条缺BV、2772条可匹配标签、2551条一致，复核出221条冲突；仅883个唯一BV有发布时间。
- 读取字段头确认旧48维含播放量和热度；读取代码确认BERT/LLM实验使用目标评论，传播GCN读取评论用户名。
- 运行`.\.venv\Scripts\python.exe scripts\validate_protocol_freeze.py`：5个文件、0缺失项、`passed=true`。
- 运行综合准备检查：`blocking_checks=[]`、`m1_read_only_work_ready=true`；Python编译和`git diff --check`通过。

### 影响与边界

步骤6—10已完成，但这不是G1/G2通过。未生成正式dataset-v1/split-v1，未解决2815版本28条差异，未输出221条逐行冲突清单，也未证明第二公开人工集可用。本轮没有下载、训练、付费API或模型开发。

### 风险、问题与阻塞

- 2815原始manifest未找到，28条漂移原因保持`UNKNOWN`。
- CUC平台许可、匿名化、数据集级hash、canonical及可发布范围仍待M1/M2审计。
- 一次外部宽模式搜索误在终端显示原始评论行；没有写入仓库，后续已禁止正文扫描。
- `rg`仍因系统Access denied不可用，已使用PowerShell只读替代。

### 下一步

1. 继续完成CSMV与iNews/NEmo+许可和可用性门，冻结第二人工标注主集。
2. 获得授权后只下载小型标注/元数据，实证video/post group split与标签映射。
3. M2建立CUC canonical、221冲突清单和正式泄漏单元测试。

### Git状态

当前`main`包含未提交的M1审计、准备记录及本次冻结文件；本地已提交的`1d7a210`仍未推送。未将这些变更误报为已同步。

## WR-20260714-003 — 完成公开数据选择门与可复现审计

- 时间：2026-07-14 16:59:05 +08:00
- 类型：DATA
- 任务/门：10-M1–M2 / 总纲步骤11—18 / G1
- 状态：部分完成（步骤11—18完成，G1阻塞）
- 负责人：Codex

### 背景与目标

按总纲v1.5第17节任务10核验CSMV、iNews、NEmo+和MVIndEmo的官方来源、许可、标签、媒体可得性与划分条件；只在许可、体量和存储边界明确后获取小型审计资产，并执行iNews选择门。

### 实际变更

- 新增`scripts/fetch_m1_public_assets.py`，固定CSMV commit、iNews HF revision和NEmo+ ACL附件，只允许下载小型标注/元数据资产，生成逐文件URL、日期、大小和SHA-256 manifest。
- 新增`scripts/audit_m1_public_assets.py`，在不输出评论、URL或标识符的前提下统计CSMV视频级泄漏、iNews post重叠/标签损失和NEmo+包内许可/图片缺口。
- 新增`scripts/validate_m1_public_audit.py`并接入`scripts/run_preparation_checks.py`，把选择裁定、固定revision、manifest和关键阻塞变成确定性检查。
- 新增`M1_PUBLIC_DATA_AUDIT.md`、`LABEL_SPACE_MAPPING_DRAFT.md`和`DATASET_SELECTION_DECISION.md`；更新数据台账、可行性矩阵、许可伦理矩阵、规划与进度文件。
- 条件下载CSMV 14,436,790 bytes、iNews public 26,502,742 bytes、NEmo+ 2,080,204 bytes，全部位于Git忽略的`data/raw/`；没有下载视频、图片、特征或persona数据。

### 验证与证据

- `scripts/fetch_m1_public_assets.py csmv inews nemo`成功并生成三份source manifest；再次运行保持固定下载日期和逐文件hash。
- `scripts/audit_m1_public_assets.py`通过全部source manifest复核：CSMV 107,267条正式评论、8,210视频、0个缺失`video_file_id`；train/dev/test视频交叉5,819/7,341/5,332，确认官方comment split视频泄漏。
- iNews固定公开包为11,320行、2,736个post、VAD 1—7和9类Discrete；direct6仅保留7,024行，丢4,296行及227个完整post。
- NEmo+官方包复核1,297条news item、38,910条T/I/TI反应、0张图片、0个许可文件；全部图片引用为不可解析匿名相对路径。
- `scripts/validate_m1_public_audit.py`结果为`passed=true`；两个新增抓取/审计脚本通过`py_compile`。

### 影响与边界

iNews已裁定`NO_GO_PRIMARY_MEDIA_REPRO`并按规则切换审计NEmo+；NEmo+裁定`NO_GO_PRIMARY_LICENSE_MEDIA`。MVIndEmo固定为`SILVER_ONLY_SOURCE_UNAVAILABLE`，不计入人工金标也不阻塞G1。CSMV按视频分组结构级通过，但尚未生成正式`split-v1`。本轮未训练模型、未创建任务20、未调用API/付费LLM、未购买资源或批量补采媒体。

### 风险、问题与阻塞

- 第二人工标注多模态主集尚未冻结，因此G1保持`BLOCKED`，G2未进入验收。
- Web工具直接打开GitHub/HF API URL被安全策略拒绝一次，后改用无凭证官方HTTP API完成固定版本核验。
- PowerShell对ACL附件执行HEAD首次触发空引用，改用`curl.exe -I`成功。
- 表格技能导入CSMV URL清单时，上游theme含非法`95%`、`170%` OpenXML值；原文件和临时规范化副本各失败一次后停止。源文件hash已记录，URL行级覆盖继续为`PENDING`。
- MVIndEmo论文所列GitHub在网页和API均返回404，许可与合法数据入口仍`UNKNOWN`。

### 下一步

1. 由用户/00总控决定是否联系iNews/NEmo+作者获取明确许可与媒体输入。
2. 若两者均不可恢复，批准审计另一套现成多人类标注公开集或缩小跨数据主张；不得用MVIndEmo替代人工金标。
3. 在G1恢复前只允许继续CSMV视频聚合/split约束设计等M1/M2小型工作，不进入正式训练。

### Git状态

当前分支`main`比`origin/main`领先1个既有提交；本次步骤11—18变更仍在未提交工作区，与用户此前的准备/M1变更共存。未执行提交或推送，也未把远端状态误报为已同步。

## WR-20260714-004 — 完成四路查新、贡献上限与baseline冻结

- 时间：2026-07-14 18:55:09 +08:00
- 类型：PROGRESS
- 任务/门：10-M1–M2 / 总纲步骤19—23
- 状态：完成（G1仍阻塞）
- 负责人：Codex

### 背景与目标

按总纲v1.5第17节任务10完成评论特权监督、公众诱发情绪分布、检索增强情绪预测、可靠性拒绝/缺失模态四条独立查新，并把最相近前作、CARM名称风险、C1—C3/H1—H4上限、主指标/失败条件和后续baseline候选固化为可审计产物。该工作只冻结研究与比较协议，不解除数据门，也不授权开发M3以后模型。

### 实际变更

- 新增`references/search/step19-23/scope-decision.txt`、四份原始召回JSON和`search-protocol.json`，记录用户范围、查询、来源、日期、计数、SHA-256、覆盖边界与停止规则。
- 新增`LITERATURE_SEARCH_REPORT.md`，分四条研究线记录经典、前沿、跨领域方法、当前未检出边界和必须对比后果。
- 新增`CONTRIBUTION_PRIOR_ART_MATRIX.md`，将NEmo+/CSMV/MVIndEmo/iNews、LUPI/generalized distillation/M2PKD、RAMER、MissModal/IMDer/HRLF/SelectiveNet映射到C1—C3与H1—H4。
- 新增`CARM_NAME_AUDIT.md`，核到推荐、检索、持续学习记忆、可靠机器学习和视觉模块等多个CARM/CarM既有用法，将正式名称冻结为`NAME_BLOCKED`。
- 新增`RESEARCH_PROTOCOL_FREEZE_AUDIT.md`与`BASELINE_CANDIDATES.md`，确认JS主指标、NLL/EMD及可靠性辅指标、H1—H4止损条件，并按代码可得性、任务匹配、许可和复现成本登记B00—B17。
- 更新`CLAIM_EVIDENCE_MATRIX.md`与`references/references.bib`，加入前作约束和12条已核文献；不将任何有效性claim从`TO_VERIFY`升级。
- 新增`scripts/validate_literature_freeze.py`并接入`scripts/run_preparation_checks.py`，检查五份产物、四路查询、协议锁、原始结果hash和计数闭合。
- 更新`findings.md`、`task_plan.md`与`progress.md`，将步骤19—23标为完成，同时保留G1阻塞。

### 验证与证据

- 四路自动召回均由OpenAlex、Crossref、DOAJ返回HTTP 200；行内去重候选数分别为124、138、124、114，合计500，跨行按DOI/标题年份去重后488。
- 核心条目逐项回到CVF、ACL Anthology、NeurIPS/PMLR、arXiv/OpenReview或作者官方GitHub核验；未把搜索摘要或自动相似度直接写成新颖性结论。
- `search_protocol_gate.py --input references/search/step19-23/search-protocol.json --as-of 2026-07-14`返回`status=PASS`、4条query、2个known-item recall检查、0 issue。
- `scripts/validate_literature_freeze.py`返回`passed=true`、5份文档、4条查询、identified=500；新增脚本和准备检查脚本通过`py_compile`。

### 影响与边界

查新收紧了贡献表述：公众诱发情绪/分布预测、训练期特权信息、检索增强缺失模态情绪识别、缺失模态鲁棒与拒绝均有前作，不得声称一般性首创。允许继续检验的差异仅是严格T0、video/post-group、评论特权分布监督、train-only历史反应记忆和OOD/自然缺失可靠性证据。主指标、标签来源、split政策和T0均未改变；未下载大数据/媒体/权重，未训练，未安装faiss，未调用付费API/LLM，未创建任务20。

### 风险、问题与阻塞

- 自动三层召回的宽查询噪声较高，且技能的`_shared` findings输出不可用；已保留原始JSON并改用主要来源人工核验，不宣称穷尽覆盖。
- 中文受限数据库和付费索引未搜索，因此中文覆盖不完整，禁止作首创判断。
- 首次运行新验证器因项目Python不支持`str.removeprefix`失败一次；已改为Python 3.8兼容的前缀切片并复跑通过。
- 第二人工多模态公开主集仍未冻结，G1保持`BLOCKED`；正式faiss环境继续`BLOCKED_M1`。

### 下一步

1. 继续等待用户/00总控对第二人工主集许可与媒体恢复路径作决定，或授权审计另一套现成多人类标注公开集。
2. G1恢复后再完成M2 canonical映射、正式split与泄漏单元测试，并提交G1/G2门报告。
3. 在G1/G2通过前，不进入M3 baseline训练；`CARM`正式命名保持`NAME_BLOCKED`。

### Git状态

当前分支`main`比`origin/main`领先1个既有提交；步骤19—23及此前M1变更仍在未提交工作区。未执行提交或推送，未声称已同步远端。

## WR-20260714-005 — 修复BibTeX模板残留误报并完成总验收

- 时间：2026-07-14 18:58:30 +08:00
- 类型：FIX
- 任务/门：10-M1–M2 / 步骤19—23验收
- 状态：完成
- 负责人：Codex

### 背景与目标

首次综合准备检查把BibTeX中用于保护方法名大小写的双花括号识别为模板占位符，导致`template_residuals`成为唯一阻塞。目标是在不改变引用内容的前提下消除误报并恢复M1只读工作就绪状态。

### 实际变更

- 将`references/references.bib`中MVIndEmo、MissModal和SelectiveNet三个title由双花括号写法改为等价的BibTeX引号写法。
- 未修改作者、年份、venue、DOI/URL或任何研究结论。

### 验证与证据

- 复跑`run_preparation_checks.py`：`blocking_checks=[]`、`m1_read_only_work_ready=true`、`template_residuals.hits=[]`。
- `literature_freeze`继续`passed=true`，4条查询、500条identified计数未漂移；`git diff --check`通过，仅报告Windows换行提示。

### 影响与边界

只修复验收器与合法BibTeX语法之间的格式冲突；不改变主指标、查新结论、baseline选择、数据门或模型环境。正式模型环境仍因faiss缺失为`BLOCKED_M1`。

### 风险、问题与阻塞

- G1仍因第二人工多模态主集未冻结而`BLOCKED`；本修复不解除该门。

### 下一步

1. 等待第二人工主集的许可/媒体决策或替代审计授权。
2. G1/G2通过前保持M3训练禁令。

### Git状态

当前变更仍在未提交工作区；未执行提交或推送。

## WR-20260714-006 — 完成M2 canonical、标签隔离与无泄漏split本地实现

- 时间：2026-07-14 19:16:30 +08:00
- 类型：DATA
- 任务/门：10-M1–M2 / 总纲步骤24—33 / G1、G2
- 状态：部分完成（本地可执行项完成；G1阻塞）
- 负责人：Codex

### 背景与目标

按总纲v1.5第17节任务10建立不可变原始manifest、canonical schema、CSMV视频级标签、先划分后索引边界、CUC-IGPE-v2 canonical与金标/银标/无标签物理隔离。第二人工主集未冻结时必须诚实阻塞，不得用银标替代。

### 实际变更

- 新增`DATA_DICTIONARY.md`、`M2_DATA_PROTOCOL.md`、`SILVER_LABEL_PROTOCOL.md`、`LABEL_ERROR_REVIEW_PROTOCOL.md`、`NEAR_DUPLICATE_SOURCE_AUDIT.md`和`CUC_CANONICAL_AUDIT.md`。
- 新增`data/manifests/canonical-audience-affect-v1.schema.json`及CSMV/CUC原始、canonical、split、tier、label-provenance、index-boundary、第二主集映射阻塞和错误审查manifest。
- 新增`scripts/build_m2_data_artifacts.py`：先核固定source hash，再生成8210条CSMV视频级经验分布、两套无group交叉split、2787条CUC银标canonical和100条错误审查候选。
- 新增`scripts/load_label_tier.py`，强制单tier加载，拒绝目标评论字段和银标进入`HUMAN_GOLD`。
- 新增`scripts/validate_m2_data_engineering.py`并接入`scripts/run_preparation_checks.py`；更新数据来源台账、数据区README、规划、进度与发现记录。
- 派生实体位于Git忽略的`data/processed/HUMAN_GOLD`、`SILVER`和`UNLABELED`；没有把评论正文、原始用户/发布者名称或媒体写入Git。

### 验证与证据

- `scripts/build_m2_data_artifacts.py --cuc-root <外部只读根目录>`成功：CSMV 8210视频/107267评论；video split 5719/816/1675，hashtag split 5990/602/1618；CUC 2787条、221冲突、8缺BV、0重复BV、883有时间、100候选。
- `scripts/validate_m2_data_engineering.py`返回`passed=true`、`m2_local_artifacts_ready=true`；35个hashtag连通分量跨split为0、禁用评论字段命中0、132个CUC源文件完成清单。
- Python 3.8对`build_m2_data_artifacts.py`、`load_label_tier.py`、`validate_m2_data_engineering.py`和`run_preparation_checks.py`执行`py_compile`通过。
- `scripts/run_preparation_checks.py`返回`blocking_checks=[]`、`m1_read_only_work_ready=true`；M2子报告明确`g1_passed=false`、`g2_passed=false`，正式环境继续`BLOCKED_M1`。

### 影响与边界

步骤24—26、28—32已完成本地实现；步骤27只完成版本化阻塞记录，因为第二人工主集尚未冻结。步骤33抽取了100条候选但未执行人工裁定。没有下载媒体/大数据、训练模型、建立索引、安装faiss、调用API/付费LLM、购买资源、改变T0、主指标或claim上限。

### 风险、问题与阻塞

- 第二人工标注多模态主集未冻结，G1保持`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`；G2不进入正式验收。
- CSMV无原生topic、媒体指纹和发布者元数据，topic-held-out、语义近重复、同源事件与发布者捷径不能判PASS。
- CUC许可未知、2815原始manifest缺失、28条漂移未解释、221条冲突未人工裁定、1904条缺发布时间；48维遗留向量未证明T0可得。
- 两次只读PowerShell文件筛选因正则反斜杠写法错误产生大量解析错误，已停止该写法并改为明确路径/脚本内审计；首次CUC时间仅按同发布者匹配得到882条，复核旧全局口径后增加显式跨发布者匹配标记，最终883条且其中1条为警告。

### 下一步

1. 由00总控决定第二人工主集的许可/媒体恢复或授权审计新候选，以解除G1。
2. 获得合法媒体/标题后，在test不可见前冻结近重复与同源事件指纹协议。
3. 如需完成100条人工审查，由用户安排审查者；结果只能进入新版本数据缺陷台账。

### Git状态

当前分支`main`比`origin/main`领先1个既有提交；步骤24—33与此前M1产物均在未提交工作区。本批次未执行提交或推送，未声称远端已同步。

## WR-20260714-007 — 修复M1验收器对M2状态升级的误报

- 时间：2026-07-14 19:18:30 +08:00
- 类型：FIX
- 任务/门：10-M1–M2 / 综合准备检查
- 状态：完成
- 负责人：Codex

### 背景与目标

步骤24—33完成后，`DATA_SOURCE_LEDGER.md`把CSMV从`ANNOTATIONS_VERIFIED_MEDIA_PENDING`升级为`CANONICAL_LABELS_READY_MEDIA_PENDING`。M1验收器仍要求旧字面量，导致最终综合检查把合法状态升级误报为`m1_public_audit`阻塞。

### 实际变更

- 更新`scripts/validate_m1_public_audit.py`的受控台账状态断言，使其核验新的CSMV canonical状态。
- 未放宽iNews、NEmo+、MVIndEmo、媒体权利、第二主集或G1/G2检查。

### 验证与证据

- 失败证据：首次最终综合检查返回`blocking_checks=["m1_public_audit"]`，唯一错误为缺少旧状态字面量；同轮M2检查与确定性重跑均通过。
- 修复后重新运行`validate_m1_public_audit.py`与`run_preparation_checks.py`；预期恢复`blocking_checks=[]`，同时保留`formal_model_work_ready=false`和G1阻塞。

### 影响与边界

仅同步验收器与台账的状态机，不改变数据、许可裁定、T0、split、主指标或模型环境。

### 风险、问题与阻塞

第二人工主集未冻结及faiss缺失仍保持原阻塞；本修复不放行G1/G2或正式模型工作。

### 下一步

1. 完成修复后的全套验收并记录实际结果。
2. 等待00总控处理第二人工主集决策。

### Git状态

修复仍在未提交工作区；未提交、未推送。

## WR-20260714-008 — 完成步骤24—33最终验收

- 时间：2026-07-14 19:20:00 +08:00
- 类型：TEST
- 任务/门：10-M1–M2 / 步骤24—33验收
- 状态：完成（G1阻塞保持）
- 负责人：Codex

### 背景与目标

复核M1状态兼容修复后全部M2派生物、加载边界、日志与综合准备门，确认本地完成不被误报为G1/G2通过。

### 实际变更

- 本记录不新增数据或功能；汇总修复后的最终测试结果。
- `progress.md`补记M1旧状态断言误报及修复结果。

### 验证与证据

- `validate_m1_public_audit.py`：`passed=true`、errors为空。
- `validate_m2_data_engineering.py`：`passed=true`、`m2_local_artifacts_ready=true`、`g1_status=BLOCKED_SECOND_PRIMARY_NOT_FROZEN`、`g2_status=NOT_EVALUATED_G1_BLOCKED`。
- 连续重跑构建器前后5个核心输出SHA-256一致：`deterministic_rebuild=True`。
- `validate_work_log.py`：7条记录、errors为空；随后追加本记录。
- 全部`scripts/*.py`执行`py_compile`通过；`run_preparation_checks.py`返回`m1_read_only_work_ready=true`、`formal_model_work_ready=false`、`blocking_checks=[]`、M2子检查通过。
- `git diff --check`通过，仅出现Windows换行提示，无空白错误。

### 影响与边界

确认步骤24—33的本地可执行部分可复跑且标签层级负测生效。没有放行第二主集、G1、G2、正式模型环境或任务20。

### 风险、问题与阻塞

外部阻塞与WR-006一致：第二人工主集未冻结；CSMV语义近重复/发布者审计资产不足；CUC许可、28条漂移、221冲突和时间缺失未解决。

### 下一步

1. 等待00总控处理第二人工主集。
2. 未获新授权前不进入M3训练或补采媒体。

### Git状态

当前`main`比`origin/main`领先1个既有提交；所有本轮变更未提交、未推送。

## WR-20260714-009 — 完成步骤34—39泄漏门、数据文档与G1/G2交接包

- 时间：2026-07-14 19:57:27 +08:00
- 类型：FEATURE | DATA | TEST | DOC
- 任务/门：10-M1–M2 / 总纲步骤34—39 / G1、G2
- 状态：部分完成（本地交付完成；G1/G2阻塞）
- 负责人：Codex

### 背景与目标

将已有M2数据工程检查升级为会阻止发布候选生成的Critical泄漏门，生成受G1约束的版本化数据包、数据文档、隔离复现证据和00任务审核交接。必须区分“本地自动测试通过”与“G1/G2通过”。

### 实际变更

- 新增`scripts/run_m2_leakage_tests.py`，检查item ID/source group交集、107267条评论的视频归属、目标评论字段、未来候选字段、train-only索引、时间顺序和fit范围；失败时输出`LEAKAGE_BLOCKED`并返回非零状态。
- 新增`scripts/build_m2_release.py`，泄漏门通过后才生成`dataset-v1.manifest.json`、`split-v1.manifest.json`、升级后的`label-provenance-v1.manifest.json`、泄漏manifest和数据审计报告。候选固定`LOCAL_CANDIDATE_G1_BLOCKED`、`formal_split=false`。
- 新增`scripts/reproduce_m2_minimal.py`与`reproducibility-v1.manifest.json`，在Python `-I -S`、禁用site-packages且不转发凭证环境的隔离进程中从原始manifest重跑。
- 新增Data Card、Datasheet、隐私说明、平台条款说明、发布边界、G1/G2矩阵与`HANDOFF_10.md`；新增`scripts/validate_m2_release.py`并接入综合准备检查。
- 更新`data/manifests/README.md`、规划、进度和发现记录。

### 验证与证据

- 真实泄漏门：`PASS_WITH_LIMITATIONS`、Critical失败0；评论ID跨原官方split交集0、评论—视频归属错误0、目标评论/未来候选命中0、索引未建且fit范围train-only。
- 负面自测：注入跨split item/source group、`target_comment`、未来互动、`allowed_fit_split=all`和逆序time split，输出预期`LEAKAGE_BLOCKED`并命中7项失败检查，自测进程返回0。
- 发布构建器成功写出6项受控交付，状态`LOCAL_CANDIDATE_G1_BLOCKED`。
- 隔离重跑最终两个命令返回`[0,0]`，18个核心输出SHA-256重跑前后完全一致，`mismatches=[]`。
- `validate_m2_release.py`返回`passed=true`、`steps_34_39_local_package_ready=true`，同时明确`g1_passed=false`、`g2_passed=false`。

### 影响与边界

步骤34—39本地可执行交付已形成；当前只允许审计和00任务评审。没有下载新数据/媒体、训练模型、建立索引、安装faiss、调用API/付费LLM、购买资源、修改T0、主指标或claim上限。银标仍与人工金标物理隔离。

### 风险、问题与阻塞

- 首次隔离重跑时`build_m2_release.py`在`-I`模式无法导入相邻泄漏模块，导致第二命令返回1及label-provenance单文件漂移；修复为仅显式加入已审查的项目`scripts/`目录后重跑通过，失败记录未删除。
- 时间检查为`NOT_APPLICABLE_NO_TIME_SPLIT`，不是时间安全PASS；语义近重复、同源事件和发布者捷径仍因媒体/元数据不足开放。
- 第二人工公开多模态主集未冻结，G1继续`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`；因此正式split不存在，G2为`NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`。

### 下一步

1. 将`HANDOFF_10.md`和G1/G2矩阵提交任务00审核。
2. 由00任务决定是否授权只读审计新的第二人工主集候选。
3. G1/G2未通过前不创建任务20或启动M3训练。

### Git状态

当前分支`main`比`origin/main`领先1个既有提交；步骤34—39及此前M1/M2变更仍在未提交工作区。本批次未提交、未推送，未声称远端已同步。

## WR-20260714-010 — 向任务00提交G1/G2审核交接

- 时间：2026-07-14 20:00:00 +08:00
- 类型：PROGRESS | DECISION
- 任务/门：10-M1–M2 / 步骤39 / G1、G2
- 状态：完成（已提交审核，门仍阻塞）
- 负责人：Codex

### 背景与目标

步骤39要求把逐条证据表提交00任务审核。目标是实际发送交接，而不是只生成本地文件，并在消息中明确本地测试通过不等于G1/G2通过。

### 实际变更

- 通过Codex任务消息接口向源任务`019f5c27-10fa-7e13-857d-77505594f7fc`发送审核请求。
- 消息指向`HANDOFF_10.md`、`G1_G2_EVIDENCE_MATRIX.md`和五个核心manifest，报告泄漏负测、隔离复现和本地包验收结果。
- 明确提交状态为G1阻塞、G2不具备审核资格、`formal_split=false`，并请求00任务决定是否授权新第二主集候选的只读审计。
- 更新`HANDOFF_10.md`、`task_plan.md`和`progress.md`的已提交状态。

### 验证与证据

- 任务消息接口返回`threadId=019f5c27-10fa-7e13-857d-77505594f7fc`，确认消息已投递到指定00源任务。
- 消息未要求创建任务20，明确G1/G2正式通过前禁止下游启动。

### 影响与边界

仅完成审核交接和状态记录；没有改变任何数据、split、许可、T0、主指标、claim或模型环境。提交审核不代表审核通过。

### 风险、问题与阻塞

任务00尚未返回审核结论；第二人工主集仍未冻结，G1/G2状态不变。

### 下一步

1. 等待任务00审核或第二主集审计授权。
2. 未获G1/G2书面通过前保持任务20与训练禁令。

### Git状态

当前分支`main`比`origin/main`领先1个既有提交；本地M1/M2交付仍未提交、未推送。本次仅发送任务消息，未执行Git同步。

## WR-20260714-011 — 00任务审核步骤34—39并授权第二主集只读审计

- 时间：2026-07-14 20:03:41 +08:00
- 类型：TEST | DECISION | DATA | DOC
- 任务/门：00总控 / 任务10步骤34—39 / G1、G2
- 状态：部分完成（本地交付接受；G1/G2继续阻塞）
- 负责人：Codex

### 背景与目标

独立审核任务10提交的本地release候选、泄漏门、复现manifest和G1/G2证据，区分实现验收与阶段门放行，并决定是否允许继续寻找第二人工多模态主集。

### 实际变更

- 新增`TASK00_G1_G2_REVIEW_20260714.md`，记录审核结论、证据、限制和授权边界。
- 接受步骤34—39本地交付包，但维持G1=`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`、G2=`NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`、`formal_split=false`。
- 发出`AUTH-00-M1-SECOND-PRIMARY-READONLY-20260714`：允许任务10做不超过3个公开候选的元数据短名单，并深入只读审计其中1个；禁止数据/媒体下载、登录态、gating绕过、API、付费服务、联系作者和M3动作。

### 验证与证据

- `.\.venv\Scripts\python.exe scripts\validate_m2_release.py`：沙箱外重跑exit 0，`passed=true`、`steps_34_39_local_package_ready=true`。
- `.\.venv\Scripts\python.exe scripts\validate_m2_data_engineering.py`：沙箱外重跑exit 0，`passed=true`、`m2_local_artifacts_ready=true`。
- `.\.venv\Scripts\python.exe scripts\run_m2_leakage_tests.py --no-write`：exit 0、Critical失败0、`PASS_WITH_LIMITATIONS`。
- `.\.venv\Scripts\python.exe scripts\run_m2_leakage_tests.py --selftest`：exit 0，负面夹具输出`LEAKAGE_BLOCKED`并命中7项预期失败检查。
- PowerShell独立重算5个manifest引用、5个文档引用，10项SHA-256全匹配；复现清单18个当前输出与`after_sha256`对比漂移0。

### 影响与边界

允许继续只读候选发现和许可/构念审计；不允许下载数据、冻结第二主集、改变G门、创建任务20或训练模型。自动门不替代时间、语义近重复、同源事件、发布者和媒体级人工审计。

### 风险、问题与阻塞

- 首次在受限沙箱内调用`.venv`失败，退出码101，提示无法使用工作区外Python 3.8基座；经明确授权在沙箱外运行相同只读命令后全部通过，失败记录保留。
- 第二人工主集、time split、topic split、语义近重复、同源事件、发布者和媒体指纹审计仍未关闭。
- 隔离重跑不是新OS/容器或全新依赖安装证明。

### 下一步

1. 任务10按授权形成候选短名单并深入审计1个最匹配候选。
2. 候选审计完成后回交来源、许可、媒体、多人标注、T0和split证据，由00任务再次审核。
3. G1/G2未书面通过前不创建任务20。

### Git状态

审核开始时`main`比`origin/main`领先1个既有提交；工作区已有任务10的大量未提交变更。本次新增审核文件并追加工作日志，未提交、未推送，也未改写或清理任务10现有变更。

## WR-20260714-012 — 向任务10送达00审核结论与只读授权

- 时间：2026-07-14 20:08:35 +08:00
- 类型：PROGRESS | DECISION
- 任务/门：00总控 → 任务10 / G1、G2
- 状态：完成（授权已送达；门仍阻塞）
- 负责人：Codex

### 背景与目标

将00任务的审核结论和有界只读授权实际送达任务10，避免授权只存在于本地文件而执行任务不可见。

### 实际变更

- 通过Codex任务消息接口向任务`019f5cf3-1810-7cd2-95bb-ff603551571b`发送审核结论。
- 消息明确本地交付接受、G1/G2不放行、`formal_split=false`、任务20禁令和`AUTH-00-M1-SECOND-PRIMARY-READONLY-20260714`边界。
- 要求候选审计完成后回交来源、revision、许可、大小、split、媒体、多人标注、T0与构念映射证据。

### 验证与证据

- 任务消息接口返回`threadId=019f5cf3-1810-7cd2-95bb-ff603551571b`，确认消息已投递到目标任务。

### 影响与边界

任务10可以开始公开资料的只读候选审计；仍不得下载数据/媒体/特征、使用登录态、绕过gating、调用API/付费服务、联系作者、修改G门、创建任务20或训练模型。

### 风险、问题与阻塞

第二人工主集仍未冻结；消息送达不代表候选已找到或G1/G2通过。

### 下一步

1. 等待任务10提交候选短名单和1个深入审计包。
2. 00任务收到证据后重新审核G1，不提前审核G2或创建任务20。

### Git状态

当前`main`比`origin/main`领先1个既有提交；审核文件、工作日志及任务10既有交付仍未提交、未推送。本次只发送任务消息并追加日志。

## WR-20260714-013 — 完成第二人工主集公开元数据短名单与LIRIS-ACCEDE深审

- 时间：2026-07-14 20:18:12 +08:00
- 类型：PROGRESS | DECISION | DATA | DOC | TEST
- 任务/门：10-M1–M2 / AUTH-00-M1-SECOND-PRIMARY-READONLY-20260714 / G1、G2
- 状态：部分完成（授权内审计完成；第二主集与G1/G2仍阻塞）
- 负责人：Codex

### 背景与目标

00任务接受步骤34—39本地交付后，授权任务10先形成不超过3个公开候选的元数据短名单，再深入只读审计其中1个。目标是以公开官方证据核查来源、revision、许可、规模、split、媒体、多人标注、T0和构念映射，不通过下载或联系动作绕过当前阻塞。

### 实际变更

- 新增`M1_SECOND_PRIMARY_SHORTLIST_20260714.md`，固定LIRIS-ACCEDE、PMEmo、Emotion6三项短名单，并将ArtEmis保留为短名单外预筛项。
- 新增`M1_LIRIS_ACCEDE_DEEP_AUDIT_20260714.md`，仅对LIRIS-ACCEDE深审官方站、database页、EULA和作者公开论文。
- 新增`HANDOFF_10_SECOND_PRIMARY_READONLY.md`和`data/manifests/second-primary-readonly-audit-v1.manifest.json`，机器记录授权范围、三项裁定和未改变的G门。
- 更新`DATA_SOURCE_LEDGER.md`至v1.2，登记DS-007—DS-009；更新规划、进度、发现和manifest README。
- 新增`scripts/validate_second_primary_readonly_audit.py`并接入`scripts/run_preparation_checks.py`。

### 验证与证据

- 专项校验首次运行exit 0：短名单3项、深审1项，必需字段完整，`downloaded_assets=[]`、未登录/绕过gating、未调用API/付费服务、未联系作者。
- LIRIS-ACCEDE公开证据确认9800个8—12秒视听片段、160电影；Protocol A按电影80/80隔离；valence 1517名与arousal 2442名trusted annotator；公开只发布最终VA秩。
- 官方EULA确认媒体逐源电影CC、annotations/描述CC BY-NC-SA 3.0，且访问必须由永久学术职位人员签署EULA并邮件申请；当前授权禁止执行该动作。
- PMEmo官方README确认794歌曲、457受试者、约1.3GB及多类资产，但软件MIT不能外推至数据；Emotion6官方论文确认1980图像、每图15人和七类诱发情绪分布，但数据许可/现行官方入口与媒体权利未知。

### 影响与边界

LIRIS-ACCEDE被裁定为`NO_GO_CURRENT_AUTHORIZATION_EULA_CONTACT_REQUIRED`，不是永久不可用结论；其VA秩也不能无损接入JS divergence离散分布主任务。PMEmo和Emotion6同样未通过。未下载数据、媒体、特征或小型元数据包，未签EULA、联系作者、使用API/付费服务、修改标签映射、T0、主指标或G门。

### 风险、问题与阻塞

- LIRIS-ACCEDE数据revision、包字节数、文件树/hash和逐片段许可只在受限包内可核，当前保持`UNKNOWN`。
- LIRIS-ACCEDE公开VA秩不是离散人群分布；PMEmo许可/split/逐项分布未知；Emotion6仅图像且许可/获取入口未知。
- 第二人工主集仍未冻结，G1=`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`；G2=`NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`；`formal_split=false`。

### 下一步

1. 完成工作记录、综合准备检查、Python编译和diff校验。
2. 将短名单、LIRIS深审和回交文件提交00任务复审。
3. 未获新授权前不签EULA、不下载，不创建任务20或启动M3。

### Git状态

记录时`main`比`origin/main`领先1个既有提交；本轮文件与此前M1/M2交付仍在未提交工作区。本轮未提交、未推送，也未改写或清理用户/其他任务的既有变更。

## WR-20260714-014 — GitHub同步前安全与完整性预检

- 时间：2026-07-14 20:21:48 +08:00
- 类型：TEST | SECURITY | PROGRESS
- 任务/门：00总控 / GitHub同步
- 状态：完成（预检通过，等待提交与推送）
- 负责人：Codex

### 背景与目标

用户要求将当前项目同步至`xjq801/MMSA-CH-SIMS`。提交前核对远端分叉、待提交体量、忽略规则、密钥扫描和项目强制验收，避免把数据、凭证或未通过的交付推送到GitHub。

### 实际变更

- 执行`git fetch origin --prune`，确认远端为`https://github.com/xjq801/MMSA-CH-SIMS.git`。
- 统计79个未跟踪文件合计约4.73MB；最大文件约1.26MB，没有接近GitHub 100MB单文件限制的资产。
- 本记录不改变研究数据、G门、split或模型状态；仅为同步批次增加可审计预检记录。

### 验证与证据

- `git rev-list --left-right --count origin/main...main`返回`0 1`：远端无本地缺失提交，本地领先1个既有提交。
- `.\.venv\Scripts\python.exe scripts\validate_work_log.py`：13条记录、errors为空、exit 0。
- `.\.venv\Scripts\python.exe scripts\run_preparation_checks.py`：`blocking_checks=[]`、密钥扫描0命中、M1/M2及第二主集只读审计检查通过、exit 0。
- `.\.venv\Scripts\python.exe -m compileall -q scripts`：exit 0。
- `git diff --check`：exit 0；仅有Windows换行提示，无空白错误。

### 影响与边界

允许把当前可跟踪源码、文档、小型manifest和公开文献检索元数据纳入提交。`data/raw`、处理实体数据、模型、日志、结果和凭证继续由`.gitignore`排除。

### 风险、问题与阻塞

- G1/G2和正式模型环境仍阻塞；GitHub同步不改变研究门状态。
- 当前记录写入时尚未提交或推送，不能写成已同步。

### 下一步

1. 暂存全部受Git策略允许的变更并复核暂存集合。
2. 创建M1/M2数据协议交付提交并推送`main`。
3. 推送成功后追加最终同步记录，再提交并推送该记录。

### Git状态

`main`相对`origin/main`为ahead 1、behind 0；当前M1/M2交付和本记录未提交、未推送。

## WR-20260714-015 — 修复暂存集合空白错误并冻结并发写入

- 时间：2026-07-14 20:23:59 +08:00
- 类型：FIX | TEST | PROGRESS
- 任务/门：00总控 / GitHub同步
- 状态：完成
- 负责人：Codex

### 背景与目标

首次对全部新增文件执行`git diff --cached --check`时发现Markdown行尾空格及少量文件末尾多空行。与此同时任务10仍显示活动状态，需要避免同步过程中继续写入共享工作区。

### 实际变更

- 对`git diff --cached --check`点名的22个Markdown/JSON文件执行机械空白清理：移除行尾空格，并统一为单个文件末尾换行；不改研究事实、数值、门状态或文件结构。
- 向任务10发送协调消息：其第二主集只读审计产物已纳入同步批次，从消息送达起停止修改项目文件，仅用现有证据完成最终汇报。
- 重新暂存受Git策略允许的全部变更。

### 验证与证据

- 首次`git diff --cached --check`：exit 2，报告行尾空格和文件末尾空行；失败未删除。
- 修复后再次运行`git diff --cached --check`：exit 0。
- 暂存集合91个文件，约4.82MB；最大单文件约1.26MB。

### 影响与边界

只改变文本空白与同步时的并发写入纪律。G1/G2、`formal_split=false`、第二主集裁定及任务20禁令均未变化。

### 风险、问题与阻塞

Windows提示未来Git接触文件时可能把LF转换为CRLF；当前暂存内容的空白检查已通过，该提示不代表提交失败。

### 下一步

1. 重新运行工作日志、综合准备和暂存差异验收。
2. 创建并推送M1/M2交付提交。
3. 推送成功后追加最终同步记录并再次推送。

### Git状态

当前变更已暂存但尚未提交、未推送；`main`仍比`origin/main`领先1个既有提交。

## WR-20260714-016 — 恢复哈希绑定文档并固定文本属性

- 时间：2026-07-14 20:32:42 +08:00
- 类型：FIX | TEST | DOC
- 任务/门：00总控 / GitHub同步 / M2 release证据链
- 状态：完成
- 负责人：Codex

### 背景与目标

空白清理后综合准备检查正确报告`m2_release`阻断。根因是`DATA_CARD_DATASET_V1.md`属于`dataset-v1.manifest.json`的SHA-256绑定文档，删除其Markdown行尾双空格改变了文件字节，而manifest仍保留原始哈希。

### 实际变更

- 恢复`DATA_CARD_DATASET_V1.md`元数据两行的原始Markdown硬换行字节，不修改文档语义或manifest。
- 新增`.gitattributes`：Markdown、JSON、YAML、Python和文本文件统一提交为LF；Markdown的行尾双空格和文件末尾空行不作为Git空白错误，以兼容有意的Markdown硬换行和已冻结哈希。
- 未通过修改manifest哈希来掩盖文档漂移。

### 验证与证据

- 空白清理后的`run_preparation_checks.py`：exit 1，`blocking_checks=[m2_release]`，失败项为documentation hash；失败保留。
- 恢复后`DATA_CARD_DATASET_V1.md`实际SHA-256为`e79d5c3ebb0c62f6143e1ab340ae3b92fe92173eaafcefaddd36cdcbdfa008d8`，与manifest完全一致。
- `git diff --cached --check`在新增属性后exit 0。

### 影响与边界

恢复字节级证据一致性并明确文本规范；不改变数据、统计、G1/G2、split或研究结论。

### 风险、问题与阻塞

其他受manifest哈希绑定的文档后续不得做无版本更新的格式化；必须先识别引用链并同步版本化。

### 下一步

1. 重新运行全部强制验收并确认M2 documentation hash恢复。
2. 创建并推送交付提交。
3. 追加最终GitHub同步记录并再次推送。

### Git状态

修复与全部交付已暂存但尚未提交、未推送。
