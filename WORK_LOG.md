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

## WR-20260714-017 — 完成M1/M2交付的GitHub主同步

- 时间：2026-07-14 20:33:46 +08:00
- 类型：PROGRESS | DOC
- 任务/门：00总控 / GitHub同步
- 状态：完成（主交付已推送；本记录待随收尾提交推送）
- 负责人：Codex

### 背景与目标

在全部安全、工作日志、数据协议、M2 release、第二主集只读审计、Python编译和Git差异门通过后，将本地M1/M2交付同步至用户指定GitHub仓库。

### 实际变更

- 创建提交`e8549bf feat: add M1-M2 data protocol delivery`，纳入92个受Git策略允许的源码、协议、报告、小型manifest和公开文献检索元数据文件。
- 将本地`main`推送至`https://github.com/xjq801/MMSA-CH-SIMS.git`的`origin/main`。
- 推送同时包含此前本地领先的`1d7a210`准备验收提交；原始数据、处理实体、模型、日志、结果和凭证未进入提交。

### 验证与证据

- `git push origin main`返回成功：`847a07c..e8549bf main -> main`。
- 推送后`git status --short --branch`显示`## main...origin/main`，无领先或落后。
- `git log --oneline --decorate -3`显示`e8549bf`同时位于`HEAD -> main`和`origin/main`。

### 影响与边界

GitHub已包含截至`e8549bf`的M1/M2本地交付和00审核材料。同步不改变G1/G2阻塞、`formal_split=false`、第二主集未冻结和任务20禁令。

### 风险、问题与阻塞

无同步错误。研究阻塞仍为第二人工主集未冻结及相关语义/媒体审计未关闭。

### 下一步

1. 验证本记录和综合准备门。
2. 创建并推送仅包含本记录的收尾提交。
3. 后续继续按G1解阻流程工作，不提前创建任务20。

### Git状态

主交付提交`e8549bf`已推送至`origin/main`；本条最终同步记录在写入时尚未提交、未推送，将由下一收尾提交同步。

## WR-20260714-018 — 修复CSMV URL审计并形成G1/G2止损决策
- 时间：2026-07-14 21:05:06 +08:00
- 类型：FIX | AUDIT | DOC | DECISION
- 任务/门：10-M1–M2 数据与协议 / G1/G2未通过项修复
- 状态：本地修复完成；外部数据与范围决策阻塞
- 负责人：Codex

### 背景与目标

用户要求完善G1/G2所有未通过项。复核确认不能用状态字段或新增脚本替代真实数据门：需要继续关闭本地可修问题，同时把必须由上游媒体权利、机构EULA或00范围变更解决的项目明确交回决策。

### 实际变更

- 为`scripts/audit_m1_public_assets.py`增加Strict/Transitional OOXML单元格解析，绕开CSMV上游工作簿损坏theme，不读取样式、公式或外部链接。
- 将CSMV URL表的行数、唯一ID、HTTPS、host、重复URL、表ID—URL路径ID一致性和正式视频ID集合覆盖写入`m1-public-audit-v1.manifest.json`。
- 在`validate_m1_public_audit.py`中固定URL覆盖与错配风险断言，防止后续把错误映射静默写成PASS。
- 更新公开数据审计、可行性矩阵、数据源台账、G1/G2证据矩阵、规划/发现/进度文件；登记VCE和LAI-GAI修复候选。
- 新增`G1_G2_REMEDIATION_REPORT_20260714.md`，区分已修项、外部硬阻塞、三条止损路径与推荐决策。

### 验证与证据

- `audit_m1_public_assets.py`重跑exit 0；原始source manifest hash全部先验验证通过。
- URL表8210行、8210个唯一行ID、0缺ID、0缺URL；正式8210个视频ID集合覆盖差集双向均为0。
- 发现2644行表ID与TikTok URL路径ID不一致、200行完整URL重复、URL路径ID重复202行；`raw_link_mapping_semantically_consistent=false`。
- `validate_m1_public_audit.py`exit 0，证明上述风险被机器保留而非掩盖。
- 首次`validate_work_log.py`因本记录误用元数据键“任务/问题”而exit 1；该失败未删除，已改回规范键“任务/门”后重新验收。
- 修复后`validate_work_log.py`检查18条记录、errors为空、exit 0。
- `run_preparation_checks.py`返回`blocking_checks=[]`、`m1_read_only_work_ready=true`、`formal_model_work_ready=false`；M1/M2本地交付检查全部通过，同时诚实保留G1/G2为false。
- `python -m compileall -q scripts`与`git diff --check`均exit 0；仅有Git未来CRLF→LF提示，无空白错误。

### 影响与边界

CSMV“Excel不可读/行级覆盖未知”已修复，但媒体映射因上游错配转为更具体的阻塞；这不会降低G1要求。VCE不因Fair Use主张升级为合法媒体，LAI-GAI不因论文开放升级为多模态主集。未下载新数据/媒体/特征，未调用API/付费服务，未联系作者，未训练或创建任务20。

### 风险、问题与阻塞

- CSMV需要上游纠正URL manifest，或提供许可、版本、size/hash和ID映射明确的官方特征包。
- 当前不存在满足原“第二人工多模态主集”全部硬门的候选。
- 推荐LAI-GAI会把第二集降为图像跨域人工主集，属于SSOT/协议范围变更，必须由用户与00书面批准；OSF逐资产许可仍待另行授权核验。

### 下一步

1. 等待用户选择：批准LAI-GAI范围降级、授权机构联系/EULA，或维持原要求止损。
2. 获得选择后先提交00变更审核；未批准前不下载数据、不修改G门。
3. 若第二集最终准入，再生成双主集manifest、冻结映射、formal split并运行全部泄漏与复现门。

### Git状态

本条及本轮修复在记录时尚未提交、未推送；G1/G2与`formal_split=false`保持不变。

## WR-20260714-019 — 用户批准LAI-GAI路径并提交00范围变更请求
- 时间：2026-07-14 21:11:12 +08:00
- 类型：DECISION | PROGRESS | DOC
- 任务/门：10-M1–M2 数据与协议 / 第二主集范围变更
- 状态：用户方向已批准；等待00书面范围与只读元数据授权
- 负责人：Codex

### 背景与目标

用户明确选择路径1，同意把LAI-GAI推进为“图像跨域第二人工主集”。该决定解决候选方向选择，但不替代OSF资产许可、版本、体量、字段和split审计，也不自动通过G1/G2。

### 实际变更

- 新增`SECOND_PRIMARY_SCOPE_CHANGE_REQUEST_20260714.md`，冻结不变项、模态降级、论文主张上限、元数据审计请求和禁止边界。
- 更新`G1_G2_REMEDIATION_REPORT_20260714.md`，将路径1标为用户已选择、00待批。
- 向00源任务发送范围变更与只读元数据审计授权请求；发送工具返回任务ID`019f5c27-10fa-7e13-857d-77505594f7fc`。
- 更新规划和进度，新增阶段15；未修改总纲SSOT、G1/G2、formal split或任务20状态。

### 验证与证据

- 用户原文：`同意路径1`。
- 00消息明确只申请核OSF `V8DKM/8P572/K8XVH`三个组件的公开license/revision/file tree/size/hash，不申请下载数据包或调用API。

### 影响与边界

方向从“继续寻找严格多模态候选”冻结为“LAI-GAI图像跨域降级候选”；主指标JS、人工金标、T0和银标隔离不变。论文泛化主张必须降级为视频主集+图像跨域集。

### 风险、问题与阻塞

- 00尚未书面修订SSOT/协议，任务10不能自行把候选写成已冻结主集。
- OSF逐资产许可、文件体量、hash和raw字段仍未知。
- 项目根目录当前没有总纲要求00维护的`DECISION_LOG.md`和`RISK_REGISTER.md`；任务10不越权创建00权威台账，已在计划中登记并交00处理。

### 下一步

1. 等待00书面范围/元数据授权。
2. 获授权后仅做公开网页/文件树元数据审计；若需小型元数据文件，下载前另报。
3. 许可和字段通过后再申请数据下载与正式M2构建；G1/G2仍须00复审。

### Git状态

本记录及相关范围请求在写入时尚未提交、未推送；既有未提交修复一并保留。
## WR-20260714-020 — 完成LAI-GAI路径1的OSF公开网页元数据审计
- 时间：2026-07-14 21:21:26 +08:00
- 类型：AUDIT | DECISION | DOC | TEST
- 任务/门：10-M1–M2 数据与协议 / 第二跨域图像主集下载前准入
- 状态：只读审计完成；`NO_GO_PENDING_ASSET_METADATA`
- 负责人：Codex

### 背景与目标

用户同意路径1后，00以`SC-20260714-01`批准把第二人工多模态主集降级为“第二人工跨域图像主集/缺失模态验证集”，并以`AUTH-00-LAI-GAI-OSF-META-RO-20260714`授权仅核LAI-GAI三个OSF组件的公开网页元数据。本轮目标是判断能否在不下载、不调用API和不登录的前提下关闭逐资产许可与复现元数据门。

### 实际变更

- 只读核验`V8DKM`、`8P572`、`K8XVH`公开定位；未预览、流式读取或下载图像、ZIP、raw data与评分表。
- 精确公开搜索三个节点标识符；结果仅包含OSF通用许可、文件和元数据说明，未发现节点级资产元数据。
- 新增`M1_LAI_GAI_OSF_METADATA_AUDIT_20260714.md`和`lai-gai-osf-metadata-audit-v1.manifest.json`，逐组件保留访问结果与UNKNOWN字段。
- 新增`validate_lai_gai_osf_metadata_audit.py`并接入`run_preparation_checks.py`，机器阻止把网页不可见字段误写为已核。
- 更新数据源台账、可行性矩阵、G1/G2证据、修复报告、规划、发现与进度记录。

### 验证与证据

- `V8DKM`定位存在但合规读取器取得0个可用页面行；`8P572`返回安全打开错误；`K8XVH`返回HTTP 403，均未绕过。
- asset license、revision、file tree/count/size、hash/checksum、gating和公开数据字典全部记录为`UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE`。
- 专项manifest显式固定：0下载、未预览/流式读取、未用API/自动抓取、未登录/Cookie、未联系作者、未构建映射或split。
- `validate_lai_gai_osf_metadata_audit.py`逐项通过：授权范围、0扩权访问、UNKNOWN保留和诚实门状态均为`passed=true`。
- `validate_work_log.py`检查20条记录、errors为空、exit 0。
- `run_preparation_checks.py`返回`blocking_checks=[]`、`m1_read_only_work_ready=true`、`formal_model_work_ready=false`；新增LAI-GAI审计门通过，同时G1/G2继续为false。
- `python -m compileall -q scripts`与`git diff --check`均exit 0；后者只有既有CRLF→LF提示，无空白错误。

### 影响与边界

路径1的研究范围已获批准，但LAI-GAI仍只是优先审计候选。论文CC BY-NC 4.0没有被外推为OSF图像或评分资产许可；论文所述847张图像与N=2470也没有被伪装成已下载manifest。CSMV继续承担视频多模态与H1/H2证据，LAI-GAI若未来准入只承担图像跨域、校准/OOD和缺失模态边界。

### 风险、问题与阻塞

- 公开网页在当前合规访问方式下不足以核验资产许可、固定revision、文件树/size、hash和评分字段。
- HTTP 403或工具打开错误不能被解释为登录门、私有状态或合法使用许可。
- 当前授权明确禁止下载/API/映射/split；任务10不能自行扩权补齐未知项。

### 下一步

1. 将`NO_GO_PENDING_ASSET_METADATA`与独立证据回交00复审。
2. 若00决定继续路径1，先书面批准明确的最小元数据取得方案；执行前列明具体文件或页面、预计大小、许可和用途。
3. 只有资产元数据通过并另获下载授权后，才核逐人评分字段、形成标签映射与split并重跑G1/G2；此前不创建任务20。

### Git状态

本记录与本轮审计产物在写入时尚未提交、未推送；保留工作区中既有未提交修复和00总控变更，不覆盖、不回退。

## WR-20260714-021 — 00完成LAI-GAI范围落纲、只读审计复审与扩权裁定
- 时间：2026-07-14 21:33:01 +08:00
- 类型：DECISION | AUDIT | DOC | TEST
- 任务/门：00-总控与决策 / LAI-GAI范围变更、G1/G2
- 状态：范围变更完成；公开网页审计No-Go已接受；扩权等待用户明确批准
- 负责人：Codex

### 背景与目标

用户批准路径1并要求00处理第二人工集范围变更、只读OSF元数据授权。任务10随后按授权完成公开网页审计并回交`NO_GO_PENDING_ASSET_METADATA`。00需要把范围变化写入唯一总纲，复核任务10是否守权，并决定是否能在用户原“不调用API、不下载图像/raw data包”边界下继续取得元数据。

### 实际变更

- 将总纲升级为v1.6，新增`SC-20260714-01`：第二集降级为跨域图像/缺失模态验证角色；CSMV继续承担完整视频多模态与H1/H2主证据；LAI-GAI不适用的机制实验记`NOT_APPLICABLE_BY_DESIGN`。
- 新增`TASK00_LAI_GAI_SCOPE_AND_AUDIT_AUTHORIZATION_20260714.md`并签发`AUTH-00-LAI-GAI-OSF-META-RO-20260714`；同步更新第17节便捷副本、bootstrap配置/validator、数据台账、G1/G2证据和计划记录。
- 新建`DECISION_LOG.md`和`RISK_REGISTER.md`，登记范围、授权、CSMV映射、LAI-GAI资产元数据和prompt捷径风险。
- 复核任务10的`M1_LAI_GAI_OSF_METADATA_AUDIT_20260714.md`、manifest和专项validator，接受三个组件关键字段均不可见的诚实No-Go结论。
- 新增`TASK00_LAI_GAI_METADATA_AUDIT_REVIEW_20260714.md`，裁定`REVIEW-00-LAI-GAI-META-20260714=ACCEPTED_NO_GO_PENDING_ASSET_METADATA`；不把API、下载、登录或作者联系默认为原授权延伸。
- 向任务10发送两次书面消息：先下发范围/网页只读授权，后确认No-Go并要求停止；两次工具均返回目标任务ID`019f5cf3-1810-7cd2-95bb-ff603551571b`。

### 验证与证据

- `validate_lai_gai_osf_metadata_audit.py`：授权范围、0扩权、UNKNOWN保留、诚实门状态全部`passed=true`，exit 0。
- `validate_experiment_config.py --config configs/experiment.bootstrap.yaml`输出`CONFIG_VALID`，exit 0；配置已切换总纲v1.6和数据集原生内容单元。
- 总纲第17节与`CODEX_TASK_TREE_EXECUTION_SPEC.md`经标题级别归一化后输出`SECTION17_MIRROR_MATCH`。
- `validate_work_log.py`检查20条既有记录、errors为空、exit 0。
- `run_preparation_checks.py`返回`blocking_checks=[]`、LAI-GAI专项门通过、`formal_model_work_ready=false`；G1/G2仍为false。
- `python -m compileall -q scripts`与`git diff --check`均exit 0；仅有既有CRLF→LF提示，无空白错误。

### 影响与边界

范围已正式降级，但LAI-GAI没有被冻结或获得数据准入。公开网页审计已完成并关闭原授权，任务10当前停止。00只提出尚未授权的最小方案：对三个节点执行元数据专用OSF API只读GET、总响应不超过5 MiB、不跟随下载链接、不读取评分内容；只有用户明确同意后才可另签授权。未下载/预览任何资产，未调用API/付费服务，未登录、未训练、未生成正式split，也未创建任务20。

### 风险、问题与阻塞

- LAI-GAI三个组件的asset license、revision、file tree/count/size、hash/checksum、gating和数据字典仍全部UNKNOWN。
- CSMV 2644行ID—URL路径错配仍为独立阻塞，范围降级不修复该问题。
- 若用户不批准元数据API或其他明确最小取得方案，路径1维持`NO_GO_PENDING_ASSET_METADATA`。

### 下一步

1. 等待用户明确决定是否批准限额元数据OSF API只读GET。
2. 若批准，另签独立授权并由任务10执行；若不批准，维持No-Go并重新评估第二人工集策略。
3. 在G1/G2逐条书面通过前保持`formal_split=false`，不创建任务20。

### Git状态

本记录及当前任务10/00联合工作区变更尚未提交、未推送；保留既有用户/任务10修改，不覆盖、不回退。

## WR-20260714-022 — 用户批准LAI-GAI限额OSF元数据API审计
- 时间：2026-07-14 21:37:24 +08:00
- 类型：DECISION | DATA | DOC | TEST
- 任务/门：00-总控与决策 / LAI-GAI下载前元数据门
- 状态：授权完成；等待任务10执行
- 负责人：Codex

### 背景与目标

00在`REVIEW-00-LAI-GAI-META-20260714`中提出严格限额的OSF元数据API只读方案，并要求用户明确决定是否解除原“不调用API”边界。用户回复“批准”，因此需要签发独立的新授权，不能把批准口头扩展为数据内容下载或正式实验准入。

### 实际变更

- 新增`TASK00_LAI_GAI_OSF_API_METADATA_AUTHORIZATION_20260714.md`，签发`AUTH-00-LAI-GAI-OSF-API-META-RO-20260714`。
- 白名单固定为`api.osf.io`、`V8DKM/8P572/K8XVH`、匿名GET、node/license/provider/file-list/文件夹子级/分页元数据关系；请求≤100、响应正文累计≤5 MiB、串行且间隔≥1秒。
- 明确禁止跟随download/content/render/html/upload与非OSF API链接，禁止资产预览/下载、HEAD/Range、登录/Cookie/token、评分内容读取、映射/split、训练和任务20。
- 更新`TASK00_LAI_GAI_METADATA_AUDIT_REVIEW_20260714.md`、`DECISION_LOG.md`、`RISK_REGISTER.md`、`DATA_SOURCE_LEDGER.md`、`G1_G2_EVIDENCE_MATRIX.md`及规划/发现/进度文件。
- 向任务10发送完整授权边界；消息工具返回任务ID`019f5cf3-1810-7cd2-95bb-ff603551571b`。

### 验证与证据

- 授权合同关键字段检查输出`AUTH_CONTRACT_VALID`：授权编号、host、5 MiB、100次、禁止下载、G1阻塞和`formal_split=false`均存在。
- `validate_work_log.py`检查21条既有记录、errors为空、exit 0。
- `run_preparation_checks.py`返回`blocking_checks=[]`、`formal_model_work_ready=false`；现有数据门与LAI-GAI网页审计门保持诚实状态。
- `git diff --check` exit 0；只有既有CRLF→LF提示，无空白错误。

### 影响与边界

任务10现在可以调用受限OSF元数据API，但不能读取或下载任何资产内容。该授权只允许补充下载前准入证据，不表示LAI-GAI许可、固定性、标签字段或split已经通过。G1/G2、`formal_split=false`和任务20禁令不变。

### 风险、问题与阻塞

- API可能仍不显示asset-level license、公开checksum或完整固定revision；UNKNOWN继续阻塞。
- 文件列表可能包含签名下载URL或贡献者信息，tracked产物必须删除，原始JSON只能进入Git忽略目录。
- CSMV 2644行ID—URL路径错配不受本授权影响。

### 下一步

1. 任务10按新授权执行并回交请求清单、响应hash、三节点矩阵和边界validator。
2. 00复审元数据门；若通过，只能再决定是否授权明确资产文件/评分字段审计。
3. 未获后续授权前不下载数据、不生成正式split、不创建任务20。

### Git状态

本记录及当前联合工作区变更尚未提交、未推送；保留任务10与00既有修改。
## WR-20260714-023 — 执行LAI-GAI限额OSF元数据API审计并诚实止损
- 时间：2026-07-14 22:01:26 +08:00
- 类型：DATA | AUDIT | CODE | TEST | DECISION
- 任务/门：10-M1–M2 数据与协议 / LAI-GAI下载前元数据门
- 状态：`NO_GO_PENDING_RATE_INTERVAL_AND_IMAGE_COMPONENT_FILE_TREE`
- 负责人：Codex

### 背景与目标

用户明确批准后，00签发`AUTH-00-LAI-GAI-OSF-API-META-RO-20260714`，允许任务10对`V8DKM/8P572/K8XVH`执行匿名、串行、限额OSF元数据GET。目标是取得三个节点的组件许可、修改时间、provider、文件树/size/checksum和gating证据，同时保持0资产内容访问、0映射/split和G门不变。

### 实际变更

- 新增fail-closed采集器`audit_lai_gai_osf_api_metadata.py`：禁用代理和重定向，只接收`api.osf.io`白名单及返回的license/file-list/分页关系，拒绝download/content/render/html/upload。
- 执行26次匿名GET：3个node、3个provider入口、3个license关系和17个file-list/分页；全部HTTP 200，响应正文累计382,394 bytes。
- 原始JSON只写入Git忽略的`data/raw/lai-gai/osf-api-metadata/20260714T134325Z/`；tracked manifest只投影许可、日期、provider、相对路径、kind、size、checksum、请求hash与门状态。
- 首次采集在网络阶段完成后的manifest构造处因Python小写`false`触发`NameError`。未重跑网络；修正后新增`build_lai_gai_osf_api_manifest.py`，从既有raw响应离线复核SHA-256并重建manifest。
- 新增`M1_LAI_GAI_OSF_API_METADATA_AUDIT_20260714.md`和`validate_lai_gai_osf_api_metadata.py`，更新数据源台账、可行性矩阵、G1/G2证据、修复报告、规划、发现和进度。
- 一次大补丁因00并发更新后的台账状态行不匹配而未应用；已拆成小补丁并保留00最新内容，没有覆盖或回退并发变更。

### 验证与证据

- 请求数26≤100；响应正文382,394≤5,242,880 bytes；26个响应均有本地raw字节数和SHA-256闭合，raw路径经`git check-ignore`确认不可跟踪。
- 三节点均`public=true`并返回`CC-By Attribution 4.0 International`；provider均为`osfstorage`。
- `V8DKM`：9文件、22,108,737 bytes、9/9有公开checksum；`8P572`：137文件、1,122,196,956 bytes、137/137有公开checksum；未读取任何文件内容。
- `K8XVH`文件列表端点HTTP 200但`data=[]`，因此0可见文件、0可见体量和0 checksum；本地raw响应形状复核证明不是tracked投影漏记。
- 边界validator确认host、节点、GET方法、关系父链、资源上限、raw hash、tracked脱敏和诚实G门均通过；但请求2→3的UTC时间间隔为0.996519秒，较1秒硬下限短0.003481秒，因此validator按设计exit 1。
- 未使用容差掩盖速率失败，也未重跑网络请求；采集器已为未来授权运行增加0.1秒安全余量。
- `validate_work_log.py`检查23条记录、errors为空、exit 0。
- `run_preparation_checks.py`按预期exit 1，唯一`blocking_checks`为`lai_gai_osf_api_metadata`；因此`m1_read_only_work_ready=false`、`formal_model_work_ready=false`，没有把本轮审计写成通过。
- `python -m compileall -q scripts`与`git diff --check`均exit 0；只有既有CRLF→LF提示，无空白错误。

### 影响与边界

API成功补齐三个节点的公开状态和组件许可，并补齐`V8DKM/8P572`文件级固定证据；但`K8XVH`图像资产树仍为空。同时，本轮存在一次极小但真实的请求间隔硬门不符合。两项均禁止把审计写成PASS或把LAI-GAI冻结为第二主集。

### 风险、问题与阻塞

- 核心图像节点`K8XVH`在授权API关系下没有文件元数据；不能据此推断图像不存在或自行探索其他位置。
- 一次请求间隔0.996519秒低于授权下限，必须由00复审，不得由任务10自行豁免。
- CSMV 2644行ID—URL路径错配仍是独立G1阻塞。

### 下一步

1. 运行工作记录、综合准备、脚本编译与Git差异检查；保留API边界validator的预期失败。
2. 将完整请求清单、响应hash、三节点矩阵、速率不符合和`K8XVH`空文件树回交00。
3. 00未签发新授权前停止所有LAI-GAI访问，不下载资产、不读取评分内容、不生成映射/split、不训练或创建任务20。

回交已完成：向00源任务发送完整审计结果，工具返回任务ID`019f5c27-10fa-7e13-857d-77505594f7fc`。

### Git状态

本记录与当前任务10/00联合变更尚未提交、未推送；原始API JSON受Git忽略，只有脱敏manifest、报告和脚本可跟踪。
## WR-20260714-024 — 00复审LAI-GAI API元数据审计并关闭非合规授权
- 时间：2026-07-14 22:08:02 +08:00
- 类型：REVIEW | DECISION | DATA | TEST
- 任务/门：00-总控与决策 / LAI-GAI下载前元数据门
- 状态：复审完成；`ACCEPTED_AS_NONCONFORMING_OBSERVATION_NO_GATE_CREDIT`
- 负责人：Codex

### 背景与目标
任务10按`AUTH-00-LAI-GAI-OSF-API-META-RO-20260714`完成受限OSF API元数据审计后回交00。复审目标是分别判断事实证据是否可保留、授权协议是否合规以及这些观察能否获得G1门信用；不得用事后容差掩盖请求间隔硬门失败，也不得在核心图像组件文件树仍不可见时批准重跑或扩大访问。

### 实际变更

- 新增`TASK00_LAI_GAI_OSF_API_METADATA_REVIEW_20260714.md`，签发`REVIEW-00-LAI-GAI-OSF-API-20260714`。
- 裁定26个响应及其本地SHA-256闭合结果可作为“带协议偏差的观察”保留，但不获得G1或下载准入信用；不豁免请求2→3仅`0.996519`秒的硬门失败。
- 确认`K8XVH`授权file-list返回HTTP 200且`data=[]`是独立实质阻塞；即使修复速率间隔，当前仍不能冻结LAI-GAI，因此不授权为修复观感而重跑网络。
- 将原API授权关闭为`CLOSED_NONCONFORMING_NO_RERUN_AUTHORIZED`；不授权进一步访问、替代定位、资产下载、内容读取、映射、split、训练或任务20。
- 更新`TASK00_LAI_GAI_OSF_API_METADATA_AUTHORIZATION_20260714.md`、`M1_LAI_GAI_OSF_API_METADATA_AUDIT_20260714.md`、`DECISION_LOG.md`、`RISK_REGISTER.md`、`DATA_SOURCE_LEDGER.md`、`G1_G2_EVIDENCE_MATRIX.md`、`task_plan.md`、`findings.md`与`progress.md`，统一No-Go、授权关闭和无门信用状态。
- 向任务10源任务发送书面复审结论；消息送达任务ID`019f5cf3-1810-7cd2-95bb-ff603551571b`。

### 验证与证据

- 复审合同断言输出`REVIEW_CONTRACT_VALID`，确认复审编号、无门信用、授权关闭、禁止重跑及G1/G2边界均已落盘。
- `validate_lai_gai_osf_api_metadata.py`按设计exit 1，唯一错误为响应序号3的`RATE_INTERVAL`；raw证据闭合、资源上限、节点矩阵、脱敏与诚实门检查均通过。
- `validate_work_log.py`在追加本记录前检查23条既有记录、errors为空、exit 0。
- `run_preparation_checks.py`按预期exit 1，唯一`blocking_checks`为`lai_gai_osf_api_metadata`，并保持`m1_read_only_work_ready=false`、`formal_model_work_ready=false`。
- `python -m compileall -q scripts` exit 0；`git diff --check` exit 0，仅有既有CRLF→LF提示，无空白错误。
- 本次00复审未发起任何网络请求，完全基于任务10已落盘的脱敏manifest、报告、validator和本地证据闭合结果。
- 追加本记录后的首次强制检查如实失败：`validate_work_log.py`报告`WR-20260714-024缺少元数据: 任务/门`，导致综合准备检查同时列出`work_log`与`lai_gai_osf_api_metadata`两个阻塞；根因是本记录误写字段名`任务/问题`，现已改为规范字段`任务/门`后重跑，未删除或掩盖该失败。

### 影响与边界
`V8DKM`与`8P572`的公开状态、CC BY 4.0、文件数/体量/checksum覆盖以及`K8XVH`空文件树可以作为审计观察引用，但必须同时标注协议偏差，不能写成准入通过。LAI-GAI仍未冻结；`G1=BLOCKED_SECOND_PRIMARY_NOT_FROZEN`、`G2=NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`、`formal_split=false`和任务20禁令不变。

### 风险、问题与阻塞

- `K8XVH`核心图像组件文件树为空，asset-level revision/size/checksum仍不可验证；不得推断图像不存在，也不得自行探索替代位置。
- 请求间隔硬门存在真实不合规；保留失败是审计可信度要求，不能用0.1秒未来余量倒推本次合规。
- CSMV 2644行ID—URL路径错配仍是独立G1阻塞，不因LAI-GAI元数据观察而解除。

### 下一步
1. 任务10保持停止访问和No-Go，不再为本授权执行网络重跑。
2. 若未来继续LAI-GAI，必须由用户另行批准针对`K8XVH`可验证文件树来源的独立最小方案；新方案不得继承本授权。
3. 在G1/G2正式通过前继续禁止正式split、模型实验和任务20。

### Git状态
本记录及当前任务10/00联合工作区变更尚未提交、未推送；保留已有用户/任务10修改，不覆盖、不回退。
## WR-20260714-025 — 接受00对LAI-GAI API审计的无门信用最终复审
- 时间：2026-07-14 22:09:07 +08:00
- 类型：DECISION | AUDIT | DOC | TEST
- 任务/门：10-M1–M2 数据与协议 / LAI-GAI API授权关闭
- 状态：`NO_GO_00_REVIEWED_NOT_FROZEN`
- 负责人：Codex

### 背景与目标

00完成`REVIEW-00-LAI-GAI-OSF-API-20260714`，接受任务10的本地交付与观察事实，但因0.996519秒请求间隔违反无容差硬门，且`K8XVH`授权文件列表为空，裁定本轮不授予任何G门信用。任务10需要把最终复审同步到自身证据链，同时保持失败门和停止状态。

### 实际变更

- 在API manifest新增review块，登记复审编号、`ACCEPTED_AS_NONCONFORMING_OBSERVATION_NO_GATE_CREDIT`、`OBSERVED_WITH_PROTOCOL_DEVIATION_NO_GATE_CREDIT`、授权关闭和最终数据集状态。
- 更新API审计报告的最终复审、授权关闭和`NO_GO_00_REVIEWED_NOT_FROZEN`状态。
- 同步数据可行性矩阵和G1/G2修复报告；保留00已经更新的数据源台账、G1/G2证据、计划和进度内容。
- 将最终复审文件纳入专项validator和综合准备检查的required/trackable集合；新增review closure机器断言，但没有改变速率失败判断。
- 首次整合补丁因00并发更新后的台账状态行不匹配而未应用；重新读取当前事实后拆分小补丁，没有覆盖或回退00变更。

### 验证与证据

- 权威复审文件明确授权状态为`CLOSED_NONCONFORMING_NO_RERUN_AUTHORIZED`，LAI-GAI为`NO_GO_00_REVIEWED_NOT_FROZEN`。
- 专项validator仍须因0.996519秒硬门失败而exit 1；新增review closure检查只验证最终状态，不提供豁免。
- 综合准备门继续只保留`lai_gai_osf_api_metadata`为blocking check，不得加容差、删除或移出综合门。
- 首次收口验证因00并发写入自己的`WR-20260714-024`而发现记录编号重复，`validate_work_log.py`按设计exit 1；任务10记录已顺延为`WR-20260714-025`，未修改00记录。
- 修正后`validate_work_log.py`检查25条记录、errors为空、latest为025；综合准备门恢复为唯一`blocking_checks=[lai_gai_osf_api_metadata]`。
- 专项validator的`review_closure=true`，其余授权、hash、脱敏、矩阵和门状态均通过；只保留原`RATE_INTERVAL`失败并exit 1。
- 全脚本编译和Git差异检查exit 0；没有修改速率判据或移除专项综合门。

### 影响与边界

26个响应hash、脱敏manifest、`V8DKM/8P572`元数据和`K8XVH`空列表可作为带协议偏差观察证据保留，但不能用于冻结LAI-GAI或通过G1/G2。API授权已经关闭，不存在“修正间隔后重跑”的权限。

### 风险、问题与阻塞

- `K8XVH`图像文件对象集合仍未闭合；单纯修复速率无法解决该核心缺口。
- 专项validator和综合准备门保持红色是预期且必须的研究诚信状态。

### 下一步

1. 运行工作记录、专项validator、综合准备、编译和Git差异检查，确认最终复审状态被机器保留。
2. 停止全部LAI-GAI网络访问；除非未来用户批准新的K8XVH独立定位方案并由00签发新授权，否则不再采取动作。
3. G1/G2书面通过前不创建任务20。

### Git状态

本记录及联合工作区变更尚未提交、未推送；原始API JSON继续受Git忽略。

## WR-20260714-026 — 闭合LAI-GAI第二人工跨域图像主集冻结候选

- 时间：2026-07-14 23:59:00 +08:00
- 类型：DATA | FEATURE | FIX | TEST | DOC | PROGRESS
- 任务/门：10-M1–M2 数据与协议 / 第二主集冻结与G1/G2复审输入
- 状态：完成冻结候选；等待00书面复审
- 负责人：Codex

### 背景与目标

用户明确要求“不管怎么样，把第二主集给我搞定”，00据此签发独立收口授权`AUTH-00-SECOND-PRIMARY-RESOLUTION-20260714`。目标是在不继承或篡改旧OSF API失败证据的前提下，优先从LAI-GAI官方、免费、无需登录入口闭合许可、固定版本、847图文件树、逐图人工评分、canonical映射、source-group split和泄漏门；若失败才切换OASIS。

### 实际变更

- 复用旧26个OSF响应离线定位12项最小评分文件，取得并逐文件核验OSF file ID、size和SHA-256；未下载`.RData`或1.12 GiB整节点。
- 核官方首页、下载页与Data Card；确认图像/元数据CC BY 4.0、六项研究、847图、12个1—7离散情绪强度与6个维度评分。官网图片浏览器9页恰好列出847个同源媒体URL并与最终AI评分清单一一映射。
- 完整ZIP约226.2 MiB但官方服务器持续约11 KiB/s，按止损切换官网逐图公开资产；终止重复ZIP和任务10遗留进程，保留使用`.part`原子替换的静态媒体下载。最终847张图、0个临时文件。
- 新增`scripts/fetch_lai_gai_second_primary_assets.py`、`scripts/build_lai_gai_second_primary.py`与`scripts/validate_lai_gai_second_primary.py`。
- 构建847条`HUMAN_GOLD` canonical：按`consent=YES/useData=Yes/rating_cat=0`保留63682个逐图反应；12维均值减量表下界1后归一化为分布，同时保存各维N、样本SD、SE和1—7直方图。
- 生成`lai-gai-second-primary-raw-v1`、`lai-gai-label-provenance-v1`、`lai-gai-split-v1`及更新后的`human-gold-v1`、`second-primary-label-map-v1` manifest；canonical留在Git忽略的`data/processed/HUMAN_GOLD/lai-gai-v1/`。
- source item、文化/性别/年龄变体、同prompt hash、精确和dHash近重复合并为379个group；split为594/127/126，三份均覆盖12类。
- 新增`M1_M2_LAI_GAI_SECOND_PRIMARY_FREEZE_20260714.md`，并同步数据源台账、数据可行性、G1/G2矩阵、Data Card、Datasheet、隐私、条款、发布边界、数据字典、标签映射和`HANDOFF_10.md`。

### 验证与证据

- `python scripts/build_lai_gai_second_primary.py`最终输出：847图、63682反应、379 group、split 594/127/126、canonical SHA-256=`ad58c268e34adf02bd8e639338069d34576e1d9602f819a2cc6fa89be6836818`。
- `python scripts/validate_lai_gai_second_primary.py`输出`LAI_GAI_SECOND_PRIMARY_READY`、exit 0；847图fixity、12评分文件fixity、canonical语义、敏感字段、group交集、精确/近重复跨split、类别覆盖与Git忽略全部PASS。
- 图像—评分lineage为847/847；逐图响应数58—96；图像—参与者重复0；原始`is_AI`与最终清单冲突显式保留，未用来决定真值。
- tracked canonical/manifest键扫描未发现participantID、Prolific ID、年龄、性别、国家、设备、完成日期或prompt正文。

### 影响与边界

LAI-GAI已从旧No-Go候选推进为可复核的第二人工跨域图像主集冻结候选，角色仅限图像跨域、缺失模态、校准/OOD与H3边界；CSMV继续承担视频多模态和H1/H2。prompt与目标类别不是真值，原始逐人响应和图像不入Git。本记录不追溯豁免旧0.996519秒API偏差，也不自行修改全局G1/G2、`formal_split`或创建任务20。

### 风险、问题与阻塞

- 官网完整ZIP下载过慢并产生部分文件，已标记`INCOMPLETE_NOT_USED`；正式证据只采用847个逐图官方资产及其独立hash。
- 初版存储后缀归一化误删合法七字符片段，已改为逐候选删除且必须唯一命中847冻结清单。
- 初版按整个来源数据库分组造成272/120/455失衡，已纠正为原始source item/生成族分组；数据库名只作provenance。
- 全局阶段门仍须00书面复审；旧API validator失败继续保留为历史授权证据。

### 下一步

1. 将新专项validator接入综合准备检查并运行工作记录、综合门、编译和Git差异检查。
2. 向00提交冻结报告、三个核心manifest与专项验证结果，申请书面更新第二主集、G1/G2和`formal_split`。
3. 00通过前不训练、不创建任务20；如00提出Critical，仅修复证据缺口，不改主指标或标签真值规则。

### Git状态

本记录与第二主集交付尚未提交、未推送；原始图像、逐人评分、网页快照、部分ZIP和canonical均受Git忽略，只有脚本、报告与脱敏manifest可跟踪。

## WR-20260715-001 — 修复第二主集重建确定性与旧M2兼容

- 时间：2026-07-15 00:51:00 +08:00
- 类型：FIX | TEST | DATA | PROGRESS
- 任务/门：10-M1–M2 数据与协议 / 第二主集冻结复现门
- 状态：专项门与manifest重建通过；等待00书面冻结
- 负责人：Codex

### 背景与目标

第二主集专项validator已通过，但收口检查发现两项工程一致性问题：`human-gold-v1`升级为多数据集结构后缺少旧验证器读取的顶层CSMV字段；Windows默认CRLF使重建canonical的字节hash与冻结LF文件不一致。两项都不改变样本、标签、split或主指标。

### 实际变更

- 在`human-gold-v1.manifest.json`恢复兼容顶层`dataset_id/path/records/sha256`，同时保留CSMV与LAI-GAI的`datasets`数组。
- 在`build_lai_gai_second_primary.py`显式以LF写canonical，保证Windows/Linux字节一致。
- `response_count`保持为合规图像响应行数；12个维度各自的有效N继续独立记录，避免把缺失维度误写成参与者流失。

### 验证与证据

- 重建脚本exit 0：847 records、63682 valid response rows、2557 study-scoped participants、split 594/127/126，canonical SHA-256=`ad58c268e34adf02bd8e639338069d34576e1d9602f819a2cc6fa89be6836818`。
- 第二主集专项validator exit 0并输出`LAI_GAI_SECOND_PRIMARY_READY`；847图/评分fixity、canonical语义、敏感字段、group/精确/近重复跨split、类别覆盖全部通过。
- 旧M2验证器不再因`human-gold-v1["path"]`缺失抛出`KeyError`；其剩余失败仅反映00尚未把候选状态改为正式冻结。

### 影响与边界

修复只关闭可复现性与向后兼容缺口，不自行签署G1/G2。旧OSF API授权的0.996519秒历史失败继续保留；新的第二主集收口授权和847图官方资产链独立成立。

### 风险、问题与阻塞

- 当前`lai-gai-second-primary-v1.manifest.json`仍残留另一套266-family/573-148-126划分；00已收到请求，须在书面复审中以379-group/594-127-126严格分组版本作为唯一正式split。
- CSMV 2644行媒体ID—路径映射仍是独立G2阻塞，不属于本次第二主集数据缺口。

### 下一步

1. 等待00写入第二主集冻结与G1裁定，并同步所有门状态和验证器。
2. 00签署前不创建任务20；签署后仍须单独关闭CSMV媒体lineage才能达到G2。

### Git状态

本记录及修复尚未提交、未推送；未跟踪任何原始图像、参与者记录或canonical。

## WR-20260715-002 — 接受00冻结复审并同步G1机器门

- 时间：2026-07-15 01:01:00 +08:00
- 类型：DECISION | FIX | TEST | DATA | PROGRESS
- 任务/门：10-M1–M2 数据与协议 / 第二主集正式冻结与G1
- 状态：第二主集`FROZEN_00_APPROVED`；G1 PASS；G2 BLOCKED
- 负责人：Codex

### 背景与目标

00以`REVIEW-00-LAI-GAI-FREEZE-20260715`批准LAI-GAI为第二人工跨域图像主集，并指定379组、594/127/126为唯一正式版本。任务10需要删除旧并行试算的机器歧义，把M2发布候选和验证器从“等待00”同步到书面裁定，同时保持全局G2、`formal_split=false`和任务20禁令。

### 实际变更

- 00删除266组、573/148/126的冲突manifest/canonical，更新LAI-GAI provenance、split和label-map状态为`FROZEN_00_APPROVED`。
- 更新LAI-GAI专项validator，使其同时接受合法的待复审与00已批准状态，不改变任何fixity、标签、隐私或泄漏判据。
- 更新M2数据工程和发布构建/验证状态合同：dataset-v1为`LOCAL_CANDIDATE_G1_PASS_G2_BLOCKED`，G1=`PASS`，G2=`BLOCKED_CSMV_MEDIA_MAPPING_AND_GLOBAL_SEMANTIC_AUDITS`，全局`formal_split=false`。
- 重建dataset-v1、split-v1、label-provenance-v1和数据审计报告，刷新全部引用hash。

### 验证与证据

- `build_lai_gai_second_primary.py` exit 0：847 records、63682 responses、2557 study-scoped participants、594/127/126，canonical SHA-256=`ad58c268e34adf02bd8e639338069d34576e1d9602f819a2cc6fa89be6836818`。
- LAI-GAI专项validator、M2数据工程validator、M2 release builder和M2 release validator全部exit 0。
- M2 release验证确认Critical泄漏0、manifest lineage 5/5、文档hash 5/5、18项最小复现漂移0、G1 PASS、G2 BLOCKED、全局split非正式。
- 工作记录27条在追加本记录前连续有效；全脚本编译和Git空白检查exit 0。
- 综合准备检查只保留历史`lai_gai_osf_api_metadata`为blocking check；该0.996519秒旧授权失败按00要求永久保留，不影响新独立授权下的第二主集冻结事实，但禁止把综合环境写成正式模型就绪。

### 影响与边界

第二主集和G1缺口已经关闭。LAI-GAI只承担图像跨域、缺失模态、校准/OOD和H3边界，不冒充第二视频集；CSMV继续承担视频多模态与H1/H2。G2与任务20仍由CSMV媒体映射及全局语义审计阻塞。

### 风险、问题与阻塞

- CSMV URL表2,644行ID—路径ID错配及200行URL重复仍未关闭，100%媒体lineage不成立。
- 旧OSF API审计失败必须继续在综合门显示，不能因后续独立授权成功而追溯改绿。
- 全局`formal_split=false`，不得训练、构建正式索引或创建任务20。

### 下一步

1. 将本轮冻结复审、状态同步和验证结果交给00完成任务10最终收尾。
2. 若要进入任务20，先在任务10范围关闭CSMV媒体映射与剩余全局语义审计，再申请00书面G2复审。

### Git状态

本轮文件尚未提交、未推送；raw图像、参与者响应和canonical继续受Git忽略。

## WR-20260715-003 — 00收紧正式冻结门并关闭历史授权的当前阻塞效力

- 时间：2026-07-15 01:15:38 +08:00
- 类型：DECISION | FIX | TEST | DOC | PROGRESS
- 任务/门：00总控 / LAI-GAI第二主集正式冻结、G1与综合准备门
- 状态：完成；第二主集正式冻结，G1 PASS，G2 BLOCKED
- 负责人：Codex

### 背景与目标

更正`WR-20260715-002`中的两项过渡表述：00书面复审完成后，LAI专项门不应继续接受“待复审候选”；旧OSF API授权已关闭且没有门信用，其0.996519秒失败必须永久保留，但不应继续阻塞由独立官网资产链批准的当前冻结。目标是让书面裁定、机器合同和综合准备结果严格一致，同时不弱化泄漏、fixity、隐私或历史审计事实。

### 实际变更

- 将`scripts/validate_lai_gai_second_primary.py`状态门收紧为只接受`FROZEN_00_APPROVED`，同时核验三份manifest的`REVIEW-00-LAI-GAI-FREEZE-20260715`一致性及LAI专项`formal_split=true`。
- 在`scripts/run_preparation_checks.py`中纳入正式冻结复审文件；完整调用并嵌入旧OSF验证结果，标记`HISTORICAL_NONCONFORMING_NO_GATE_CREDIT`，不删除原失败，也不再将已关闭授权列为当前blocking check。
- 更新`HANDOFF_10.md`、`M1_M2_LAI_GAI_SECOND_PRIMARY_FREEZE_20260714.md`、`task_plan.md`、`findings.md`和`progress.md`，统一唯一379组版本、G1 PASS、G2阻塞及任务20禁令。
- 冲突的`data/manifests/lai-gai-second-primary-v1.manifest.json`和`data/processed/HUMAN_GOLD/lai-gai/image_labels.v1.jsonl`均确认不存在；正式权威只保留v05 canonical与379组split。

### 验证与证据

- `build_lai_gai_second_primary.py` exit 0：847 records、63,682 valid response rows、2,557 study-scoped participants、594/127/126，canonical SHA-256=`ad58c268e34adf02bd8e639338069d34576e1d9602f819a2cc6fa89be6836818`。
- 收紧后的`validate_lai_gai_second_primary.py` exit 0；检查名`status_frozen_00_approved=true`，379组、精确/近重复跨split均0。
- `build_m2_release.py`、`validate_m2_data_engineering.py`、`validate_m2_release.py`全部exit 0；dataset状态为`LOCAL_CANDIDATE_G1_PASS_G2_BLOCKED`，G1=`PASS`，G2=`BLOCKED_CSMV_MEDIA_MAPPING_AND_GLOBAL_SEMANTIC_AUDITS`，全局`formal_split=false`。
- 单独运行`validate_lai_gai_osf_api_metadata.py`仍按设计exit 1，唯一协议失败为请求间隔0.996519秒；历史No-Go没有被改绿。
- `run_preparation_checks.py` exit 0：`blocking_checks=[]`、`m1_read_only_work_ready=true`、`formal_model_work_ready=false`；报告内完整保留旧OSF失败对象与`historical_validator_passed=false`。

### 影响与边界

第二主集和G1已正式关闭，LAI自己的冻结split可用于其获批角色；dataset-v1整体仍未过G2，不能把专项`formal_split=true`扩写为全局正式benchmark。旧OSF失败继续作为审计事实存在，但不追溯否定后续独立授权、独立资产链和00正式冻结。

### 风险、问题与阻塞

- CSMV仍有2,644行ID—路径错配及200行重复URL，媒体lineage和全局语义审计未闭合。
- 正式模型环境未就绪；G2书面通过前不得训练、建正式索引或创建任务20。
- 当前联合工作区存在大量同一任务未提交变更；本批次未回退、覆盖或提交其他代理的并发成果。

### 下一步

1. 完成工作记录、综合准备、脚本编译和Git差异的最终交付复验。
2. 将任务10当前重点切换为CSMV媒体映射与全局语义审计；完成后再申请00书面G2复审。

### Git状态

本批次及联合任务10/00变更尚未提交、未推送；raw图像、参与者响应和canonical继续受Git忽略。

## WR-20260715-004 — CSMV媒体lineage语义纠正、同源split修复与G2复审候选

- 时间：2026-07-15
- 类型：FIX | DATA | TEST | DOC | PROGRESS | BLOCKER_CHANGE
- 任务/门：10-M1–M2 / CSMV媒体lineage、泄漏门、G2候选
- 状态：本地修复完成；等待00书面G2复审
- 负责人：Codex

### 背景与目标

用户要求处理CSMV的2,644行“媒体ID—路径错配”、200行重复URL及全局语义lineage阻塞。目标是在不下载媒体、不猜测纠正上游映射、不启动训练或任务20的前提下，核清字段语义、识别真实同源风险、修复split并形成可复现G2复审证据。

### 实际变更

- 复核官方固定commit README和`CSMV_rawLinks.xlsx`：确认表内`ID`是内部`video_file_id`，URL路径ID是平台源视频ID，二者不要求相等；旧2,644行错配判断更正为命名空间误判。
- 新增`scripts/csmv_media_lineage.py`与`scripts/validate_csmv_media_lineage.py`；生成`data/manifests/csmv-media-lineage-v1.manifest.json`，逐项仅保留item/source-group/URL的hash、duplicate标记与split，不输出原始URL或平台ID。
- 修改`scripts/build_m2_data_artifacts.py`：把8,210个内部视频归并为8,008个源视频族，标记202个重复族/404条样本；`group_by_video_v1`按源族划分，hashtag协议先连接同源族再划分。
- 修改M1/M2审计与验证脚本，把合法many-to-one映射与泄漏风险分开；综合准备门新增CSMV专项validator。
- 重建CSMV canonical、split、M1审计、全局泄漏报告和M2 release manifests；同步`CSMV_MEDIA_LINEAGE_AUDIT_20260715.md`、Data Card、Datasheet、M1审计、数据源/风险/可行性台账、near-duplicate审计、M2协议、G1/G2矩阵和交接文件。

### 验证与证据

- CSMV重建exit 0：8,210 records；`group_by_video_v1` train/dev/test=`5698/837/1675`；`hashtag_heldout_v1`=`7211/327/672`。
- 专项validator普通运行和`python -I -S`隔离运行均exit 0：8,008源族、202重复族、404重复源行、跨split源族0、负面夹具检测成功、tracked原始URL0。
- 全局泄漏live no-write首次在仅修video split后输出`LEAKAGE_BLOCKED`：hashtag协议仍有train-dev 3、train-test 111、dev-test 1个source-group交叉；随后把同源关系并入hashtag连通分量，重跑Critical失败0、`PASS_WITH_LIMITATIONS`。
- 泄漏负面selftest按预期打印`LEAKAGE_BLOCKED (expected negative fixture)`且exit 0，检测source group、目标评论、未来字段、索引与时间等故障。
- `build_m2_release.py`、`validate_m1_public_audit.py`、`validate_m2_data_engineering.py`、`validate_m2_release.py`均exit 0；dataset=`LOCAL_CANDIDATE_G1_PASS_G2_REVIEW_PENDING`，G1 PASS，G2=`PENDING_00_G2_REVIEW_CSMV_LINEAGE_CLOSED`，`formal_split=false`。
- 交付前`validate_work_log.py`、变更脚本`py_compile`、`git diff --check`均exit 0；`run_preparation_checks.py` exit 0，`blocking_checks=[]`、`m1_read_only_work_ready=true`、CSMV专项通过且跨split源族0。`formal_model_work_ready=false`与当前G2待复审/环境边界一致。

### 失败与恢复（保留）

- 首轮专项validator因用字符串`http`扫描URL泄漏，把统计键`https_row_count`误报为URL；已收紧为仅检测`http://`/`https://`，未削弱原始URL禁止规则。
- 首轮泄漏命令误传不存在的`--live`参数并exit 2；按真实CLI改用`--no-write`。
- 第一次只修video split后，全局泄漏门正确发现hashtag协议115个同源交叉并exit 2；没有绕过门，修复连接逻辑后重跑通过。
- D盘全盘搜索历史CUC只读源目录在20秒超时；用户Desktop/Documents/Downloads/OneDrive有限检索未找到。因此本轮没有重跑需CUC源目录的全量18输出复现器；CSMV专项已在stdlib隔离环境从固定raw工作簿独立闭合。
- 综合准备报告本身exit 0，但用于压缩显示的辅助Python把PowerShell重定向产生的UTF-16文件按UTF-8读取，触发`UnicodeDecodeError`；随后用PowerShell `ConvertFrom-Json`读取同一报告，确认最终状态，不重跑或修改检查结果。

### 影响与边界

CSMV官方URL元数据范围内的100% item→source-family lineage和同源split泄漏已本地关闭。该结果不等于取得原始媒体、特征资产或再分发权，也不宣称发现不可观察的内容级近重复、发布者捷径或时间关系。未下载媒体/特征、未访问TikTok URL、未调用API/付费服务、未训练、未创建任务20。

### 风险、问题与阻塞

- G2尚未由00书面批准；全局`formal_split=false`和任务20禁令仍有效。
- 原始媒体/特征许可、媒体内容指纹、发布者和发布时间仍不在本地可观察范围，不能把URL元数据lineage扩写成媒体字节lineage或时间安全。
- 历史CUC外部只读源目录本轮未定位，未重跑依赖该目录的全量18输出复现器；CSMV专项隔离复现已通过。
- 交付前首次`validate_work_log.py`因本记录缺少本章节而exit 1；现补齐结构并将从头复验，不删除失败证据。

### 下一步

将`CSMV_MEDIA_LINEAGE_AUDIT_20260715.md`、专项validator、全局泄漏门、manifest hash和复现边界提交00书面G2复审。00批准前保持全局`formal_split=false`与任务20禁令。

### Git状态

本批次文件尚未提交、未推送；联合工作区既有其他变更未回退或覆盖。

## WR-20260715-005 — 00接受CSMV lineage修复并阻塞G2于正式输入资产与陈旧复现证据

- 时间：2026-07-15 12:28:44 +08:00
- 类型：REVIEW | DECISION | DATA | FIX | TEST | DOC | BLOCKER_CHANGE
- 任务/门：00总控 / CSMV媒体lineage与G2
- 状态：复审完成；G1 PASS，G2 BLOCKED
- 负责人：Codex

### 背景与目标

任务10回交CSMV命名空间纠正、8008个平台源视频族split和G2候选。00须独立判断旧2644行是否确属错配、202个many-to-one源族是否完成泄漏修复，以及媒体/特征不可观察性和复现证据是否仍违反总纲G2；不得把状态合同validator的exit 0自动解释成G2通过。

### 实际变更

- 新增`TASK00_CSMV_LINEAGE_G2_REVIEW_20260715.md`，签署`REVIEW-00-CSMV-LINEAGE-G2-20260715`：接受不同ID命名空间和source-family split修复；G2改为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_REPRODUCIBILITY_STALE`。
- 新增`TASK00_CSMV_FEATURE_PREFLIGHT_AUTHORIZATION_20260715.md`，签发`AUTH-00-CSMV-FEATURE-ASSET-PREFLIGHT-RO-20260715`：只允许官方README链接特征页面的公开元数据预审，禁止登录/API/下载特征或媒体/访问TikTok；同时允许本地核心复现门修复。
- 将总纲升级为v1.8，更新`DECISION_LOG.md`、`RISK_REGISTER.md`、`DATA_SOURCE_LEDGER.md`、`G1_G2_EVIDENCE_MATRIX.md`、`HANDOFF_10.md`、数据可行性、Data Card、Datasheet、条款、发布边界、CSMV审计、M1审计、LAI冻结报告与规划/发现/进度文件。
- 更新`build_m2_release.py`、`run_m2_leakage_tests.py`、M2验证器和全局manifest状态：G1保持PASS，G2为新阻塞状态，`formal_split=false`、`formal_model_use_allowed=false`。
- 将`reproducibility-v1.manifest.json`从旧PASS改为`STALE_AFTER_CSMV_SOURCE_GROUP_SPLIT_CHANGE`并记录9项当前漂移；`validate_m2_release.py`改为现场重算记录hash，不再只信manifest自报的空mismatch。

### 验证与证据

- 只读README复核确认：`video_file_id`是标注/特征内部键，`CSMV_rawLinks.xlsx`提供raw web link，官方未规定URL路径ID必须与内部键相等；8210内部键100%覆盖支持撤销旧2644行错配裁定。
- 00独立运行`validate_csmv_media_lineage.py`普通与`python -I -S`模式均exit 0：8210 records、8008 groups、202 duplicate groups、404 rows、cross-split=0、negative fixture=true、raw URL=0。
- 00独立运行`run_m2_leakage_tests.py --no-write`：Critical=0、`PASS_WITH_LIMITATIONS`；`--selftest`正确输出`LEAKAGE_BLOCKED (expected negative fixture)`且exit 0。M1 audit、M2 data、旧候选release状态验证均exit 0。
- 00现场将旧`reproducibility-v1.after_sha256`与当前18个文件重算，发现9项不一致，包括CSMV canonical/split、全局split/provenance/leakage/dataset和两份审计报告；因此旧18输出PASS不能覆盖新source-family版本。
- 重建阻塞状态后`build_m2_release.py` exit 0；`validate_m2_data_engineering.py`与更新后的`validate_m2_release.py`均exit 0，后者现场报告9项mismatch、`current_replay_passed=false`、G2 blocked，证明机器合同诚实而非G2放行。
- 首次使用项目`.venv`执行临时Python摘要时，受托管沙箱限制出现`Unable to create process using ... Python38`；未据此否认任务10证据。随后经批准用同一项目虚拟环境完成上述独立正负门复跑。

### 影响与边界

CSMV官方URL元数据范围内的8210 item→8008 source-family lineage和两个已发布split正式获00接受，旧2644错配阻塞关闭。不可观察的publisher/time/content fingerprint继续作为不发布相关协议时的限制；但正式CSMV模型输入资产缺失不是可降级的普通限制，它直接阻止构造合法固定的正式测试输入。CUC继续是辅助SILVER，不得因其外部根缺失阻塞公开主线；复现器应解耦核心公开benchmark。

### 风险、问题与阻塞

- CSMV I3D/VideoMAEv2等正式输入资产的asset-level许可、revision、文件树、体量、hash与8210覆盖仍为UNKNOWN/PENDING。
- 当前完整预处理尚未从冻结manifest重跑到当前source-family版本；9项旧hash漂移已显式阻断G2。
- 原始媒体权利、内容指纹、发布者和时间仍不可观察；不得扩写为已经检查或安全。
- G2、全局`formal_split`、正式训练/索引和任务20禁令均未放行。

### 下一步

1. 任务10按最小只读授权审计官方特征资产；页面未显示字段保持UNKNOWN，不下载内容。
2. 新增不依赖CUC的公开benchmark核心隔离重跑，并让release validator现场核对当前hash。
3. 两项同时闭合后再次回交00；不得自动创建任务20。

### Git状态

本批次及联合工作区变更尚未提交、未推送；未下载CSMV特征/媒体，未访问TikTok URL，未创建任务20。

## WR-20260715-006 — 修复M1台账状态断言并完成00交付复验

- 时间：2026-07-15 12:59:18 +08:00
- 类型：FIX | TEST | DOC
- 任务/门：00总控 / G2复审交付检查
- 状态：完成
- 负责人：Codex

### 背景与目标

`WR-20260715-005`后运行强制综合准备检查，唯一失败为M1 validator仍要求旧台账状态`CANONICAL_LABELS_AND_MEDIA_METADATA_LINEAGE_READY`；00裁定已把DS-001升级为更诚实的`LABEL_AND_URL_LINEAGE_READY_FORMAL_INPUT_BLOCKED`。需要只同步状态断言，不能借此改变G2阻塞。

### 实际变更

- 更新`scripts/validate_m1_public_audit.py`，以新DS-001状态替换旧状态字面量。
- 未修改CSMV标签、source-group、split、许可事实、复现mismatch或G2裁定。

### 验证与证据

- 修复前`run_preparation_checks.py` exit 1，唯一`blocking_checks=[m1_public_audit]`，错误明确为数据台账缺少旧token；其余CSMV、M2、工作记录和安全检查均通过。
- 修复后`validate_m1_public_audit.py` exit 0、errors=[]。
- 修复后`run_preparation_checks.py` exit 0：`blocking_checks=[]`、`m1_read_only_work_ready=true`、`formal_model_work_ready=false`；CSMV专项仍为8210/8008/202/404/跨split 0，M2 release仍报告9项复现陈旧和G2 blocked。

### 影响与边界

综合准备门现在识别新权威状态；这只代表本地审计/文档/状态合同无故障，不表示正式模型环境或G2就绪。

### 风险、问题与阻塞

G2的正式输入资产和当前复现证据两个阻塞均未变化；任务20禁令不变。

### 下一步

按00最小授权回交特征预审与核心隔离复现结果；再次申请G2复审。

### Git状态

本记录及联合变更尚未提交、未推送。

## WR-20260715-007 — 固化本机代理与已批准数据下载传输政策

- 时间：2026-07-15 21:18:07 +08:00
- 类型：DECISION | POLICY | DOC
- 任务/门：00总控 / 网络传输与数据取得边界
- 状态：完成
- 负责人：Codex

### 背景与目标

用户指出官方数据集下载速度较慢，并明确允许后续使用其本机代理访问官方网站及进行部分数据下载。需要把该授权写成可复用的项目级规则，同时避免把“代理提速”误写成绕过权限或任意下载授权。

### 实际变更

- 新增`TASK00_LOCAL_PROXY_AND_DATA_DOWNLOAD_POLICY_20260715.md`，签署`POLICY-00-LOCAL-PROXY-TRANSPORT-20260715`：允许用户控制的本机HTTP(S)/SOCKS代理访问官方来源并传输已完成准入审查的数据。
- 将总纲升级为v1.9并新增本地代理与下载策略；同步`DECISION_LOG.md`、`RESOURCE_TIME_POLICY.md`和`SECURITY_COMPLIANCE_CHECKLIST.md`。
- 修订`TASK00_CSMV_FEATURE_PREFLIGHT_AUTHORIZATION_20260715.md`：撤销“代理本身禁止”的旧表述，但保留官方host、无需登录、metadata-only、禁止API/镜像/绕过和禁止特征/媒体下载的全部边界。
- 在`.env.example`新增空的`HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY`和`NO_PROXY`变量名，未填写真实代理URL或凭证。
- 本批次未发出网络请求，未测试代理，未下载任何数据、特征或媒体。

### 验证与证据

- 通过文本复核确认总纲当前版本为v1.9，统一开工头引用已更新为v1.9。
- 通过diff复核确认代理配置只有空变量名，tracked文档未包含真实代理地址、用户名、密码、Cookie或token。
- `validate_work_log.py` exit 0：33条记录、`errors=[]`、latest=`WR-20260715-007`。
- `run_preparation_checks.py` exit 0：`blocking_checks=[]`、`m1_read_only_work_ready=true`、`formal_model_work_ready=false`；G2仍为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_REPRODUCIBILITY_STALE`，全局`formal_split=false`。
- `python -m compileall -q scripts`与`git diff --check`均exit 0；换行符提示不构成diff错误。
- `.env.example`代理变量检查得到4个变量、非空值0个；综合秘密扫描`hits=[]`。
- 一次用于压缩复验输出的PowerShell包装命令因括号语法错误exit 1，错误发生在解析阶段、未执行项目逻辑且未改文件；拆分命令后完整复验exit 0，新政策文件`git check-ignore`结果为未忽略。

### 影响与边界

以后任务可在直接连接过慢时使用用户本机代理访问官方来源，并下载已经通过来源、许可、revision、体量、用途、磁盘预算和checksum准入的资产。代理只是传输通道，不改变数据许可、访问控制、host白名单、研究用途或可发布边界。

### 风险、问题与阻塞

- 真实代理地址与凭证尚未由用户在本机安全配置；在未配置前保持直连或不执行下载，不猜测代理端口。
- CSMV当前授权仍为只读元数据预审，不允许下载`.npy`特征、视频或音频；具体特征下载仍需在预审闭合后取得书面资产级授权。
- G1、G2、全局`formal_split=false`、正式模型训练/索引和任务20禁令均未改变。

### 下一步

在下一次实际下载前，先记录官方host、许可、revision、文件清单/体量、目标路径、空间预算与checksum；确认本机代理环境变量已安全注入后，使用`.part`、续传、限并发和SHA-256闭合执行。

### Git状态

本记录及联合工作区变更尚未提交、未推送。

## WR-20260715-008 — 配置Git忽略的本机代理端点

- 时间：2026-07-15 21:45:37 +08:00
- 类型：CONFIG | SECURITY | TEST
- 任务/门：00总控 / 本地代理传输配置
- 状态：部分完成
- 负责人：Codex

### 背景与目标

用户补充了本机代理监听端口，需要把它写入仅限本机使用的配置，使后续官方数据访问和已批准下载可以复用，同时不得把真实代理端点写入tracked文件或工作记录。

### 实际变更

- 新增Git忽略的`.env`，配置本机HTTP与HTTPS代理，并为localhost设置直连例外；具体端点值不记录于tracked文档。
- 未修改`.env.example`中的空模板值，未设置系统级环境变量，未写入用户名、密码、Cookie或token。
- 未访问外部网站，未下载数据、特征或媒体。

### 验证与证据

- 创建前确认`.env`不存在，且`git check-ignore .env`命中，防止本地端点进入Git。
- 本机TCP监听检查返回false：配置的本地端点当前未监听；该结果不否定配置，后续实际使用前必须先启动代理客户端并复检。
- `validate_work_log.py` exit 0：34条记录、`errors=[]`、latest=`WR-20260715-008`。
- `run_preparation_checks.py` exit 1，唯一`blocking_checks=[m2_release]`；秘密扫描`hits=[]`。独立`validate_m2_release.py`确认失败来自既有9项复现hash陈旧，当前验证器要求`PASS_CURRENT_CSMV_SOURCE_GROUP_SPLIT`，与`.env`或代理配置无关。本批次未放宽该门。

### 影响与边界

后续下载工具可在明确加载项目`.env`后使用本机HTTP(S)代理。该配置不自动注入所有Windows进程，不扩大任何数据许可、host或下载授权。

### 风险、问题与阻塞

- 当前端口未监听，尚不能证明代理传输可用。
- 若该端口实际只提供SOCKS而非HTTP混合代理，需要把协议方案调整为`socks5h`并确认客户端依赖支持；本批次不猜测切换。
- 综合准备检查因当前M2复现门不满足而exit 1；该既有阻塞需要任务10按原授权完成核心隔离重放，本次端口配置不处理它。
- G2、全局`formal_split=false`、CSMV metadata-only授权和任务20禁令均未改变。

### 下一步

用户启动代理客户端后，在首次下载前复检本机监听和官方host的只读连通性；通过后再按资产级准入执行下载。

### Git状态

`.env`为Git忽略的本地文件；tracked工作记录及联合工作区变更尚未提交、未推送。

## WR-20260715-009 — 更正本机代理端口配置

- 时间：2026-07-15 21:50:44 +08:00
- 类型：FIX | CONFIG | TEST
- 任务/门：00总控 / 本地代理传输配置
- 状态：完成
- 负责人：Codex

### 背景与目标

用户明确指出上一条提供的代理端口有误，需要更正`WR-20260715-008`对应的本地配置，并确认更正后的本机端点是否监听。历史记录保留，不回写旧记录。

### 实际变更

- 仅修改Git忽略的`.env`中HTTP与HTTPS代理端点；具体端点值不写入tracked工作记录。
- 保留localhost直连例外；未修改项目级代理政策、`.env.example`、系统级环境变量或数据下载授权。
- 未访问外部网站，未下载数据、特征或媒体。

### 验证与证据

- `git check-ignore .env`命中，确认更正后的本地端点不会进入Git。
- 本机TCP监听检查返回true，确认更正后的端点当前有服务监听；该检查只证明本机端口可达，不证明具体外部host或下载可用。
- `validate_work_log.py` exit 0：35条记录、`errors=[]`、latest=`WR-20260715-009`。
- `run_preparation_checks.py` exit 0：`blocking_checks=[]`、秘密扫描`hits=[]`、`formal_model_work_ready=false`；G2仍为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_REPRODUCIBILITY_STALE`。

### 影响与边界

后续明确加载项目`.env`的下载工具将使用更正后的本机HTTP(S)代理。未进行协议探测或外部连通测试，因此仍按HTTP混合端口假设执行。

### 风险、问题与阻塞

- 若监听服务不是HTTP混合代理，首次官方host只读访问仍可能失败；届时需据真实错误调整协议，不自动切换或绕过。
- M2复现门、G2、全局`formal_split=false`、CSMV metadata-only授权和任务20禁令均未改变。

### 下一步

在下一次已授权官方数据访问中先做小体量只读连通性检查，再按资产级许可与checksum流程下载。

### Git状态

`.env`为Git忽略的本地文件；tracked纠错记录及联合工作区变更尚未提交、未推送。

## WR-20260715-010 — 记录代理纠错交付复验期间的共享M2合同竞争

- 时间：2026-07-15 21:53:10 +08:00
- 类型：TEST | BLOCKER
- 任务/门：00总控 / 代理纠错交付复验
- 状态：阻塞（仅综合准备门）
- 负责人：Codex

### 背景与目标

`WR-20260715-009`完成端口纠正后进行最终强制复验。第一次复验曾exit 0；在更新同批工作记录后再次复验时，共享工作区中的M2验证合同发生并发变化，需要保留后出现的真实失败。

### 实际变更

- 未修改代理配置、M2验证器、数据manifest、G门或任务10产物。
- 仅追加本失败记录，避免把先前一次成功复验冒充当前最终状态。

### 验证与证据

- `validate_work_log.py` exit 0：35条记录、`errors=[]`、latest=`WR-20260715-009`。
- 后续`run_preparation_checks.py` exit 1：`validate_m2_release.py`读取`dataset-v1.manifest.json`时缺少当前验证器要求的`csmv_input_asset_preflight`字段并抛出`KeyError`。
- 该失败发生在M2 release检查；秘密扫描仍为0。代理端点监听与`.env` Git忽略检查此前均已通过。

### 影响与边界

本机代理端口纠正仍然有效；失败只表示当前共享工作区的M2验证器与manifest处于未同步中间态，不能把综合准备门报告为通过。

### 风险、问题与阻塞

- 任务10或其他并发工作需要完成`csmv_input_asset_preflight`机器合同的原子同步后，综合准备门才能恢复稳定。
- 本批次不据此放宽验证器、补造字段或改写G2事实。

### 下一步

等待任务10完成当前M2合同同步；代理首次实际使用时再执行官方host小体量只读测试。

### Git状态

`.env`为Git忽略的本地文件；tracked工作记录及联合工作区变更尚未提交、未推送。

## WR-20260715-011 — 修复CSMV公共核心复现并完成正式特征资产预审

- 时间：2026-07-15 21:57:09 +08:00
- 类型：FIX | DATA | PROTOCOL | TEST | BLOCKER
- 任务/门：10-M1–M2 / CSMV正式输入资产与G2复现子门
- 状态：部分完成（复现子门本地通过；特征资产No-Go待外部元数据与00复审）
- 负责人：Codex

### 背景与目标

00在`REVIEW-00-CSMV-LINEAGE-G2-20260715`指出两个G2硬阻塞：I3D/VideoMAE等正式输入资产缺少许可、revision、文件树、体量、hash与8210覆盖；旧18输出复现记录属于source-family修复前版本，现场有9项hash漂移。用户要求修复并努力通过G2。

### 实际变更

- 按`AUTH-00-CSMV-FEATURE-ASSET-PREFLIGHT-RO-20260715`只读核验固定README与其公开Google Drive特征目录；建立`CSMV_FEATURE_ASSET_PREFLIGHT_20260715.md`、`data/manifests/csmv-feature-preflight-v1.manifest.json`和`scripts/validate_csmv_feature_preflight.py`。
- 官方README可固定I3D/VideoMAE发布声明与`.npy`按`video_file_id`命名合同；匿名公开页面可达，但初始页面未公开资产许可、revision、文件树、大小、checksum或实际8210键。因此特征预审诚实裁定`NO_GO_PENDING_ASSET_METADATA_AND_LICENSE`，未选择或下载特征族。
- 修改`scripts/build_m2_data_artifacts.py`：新增`--public-core`，从冻结CSMV raw manifest重建公开HUMAN_GOLD主线；CUC只核验冻结canonical/error-review字节，不再要求历史外部源根；同时保持LAI-GAI第二主集`FROZEN_00_APPROVED`合同，不再由旧构建器覆盖。
- 修改`scripts/reproduce_m2_minimal.py`：支持公共核心隔离重放，并把`csmv-media-lineage-v1.manifest.json`加入旧18项之外的复现输出；报告新增scope、冻结辅助输入核验与当前状态。
- 修改`scripts/validate_m2_release.py`：不再接受陈旧自报PASS，现场逐项重算`after_sha256`；纳入特征预审manifest lineage和专项validator。修改`scripts/build_m2_release.py`与`scripts/run_preparation_checks.py`同步新合同。
- 为LAI-GAI provenance补充`UTF-8_LF`序列化声明并更新`second-primary-label-map-v1.manifest.json`的真实引用hash；未修改847条canonical、标签、split或00冻结结论。
- 更新`DATA_SOURCE_LEDGER.md`、`M1_PUBLIC_DATA_AUDIT.md`、`G1_G2_EVIDENCE_MATRIX.md`、`HANDOFF_10.md`以及三份文件化规划记录，明确复现子门已本地关闭、特征资产仍是外部硬阻塞。

### 验证与证据

- `.\.venv\Scripts\python.exe scripts\reproduce_m2_minimal.py --public-core` exit 0：Python 3.8.9，`-I -S`，两条子命令returncode均0，19项before/after SHA-256一致，`mismatches=[]`，凭证环境未转发。
- `.\.venv\Scripts\python.exe scripts\validate_m2_release.py` exit 0：复现现场hash漂移0、19项通过，manifest lineage 7项通过，泄漏Critical为0；正式G2状态仍保持原00裁定，未自行放行。
- `.\.venv\Scripts\python.exe scripts\validate_csmv_feature_preflight.py` exit 0：固定commit/README hash、公开页面观察、UNKNOWN fail-closed和0个本地`.npy`全部通过；`g2_asset_ready=false`。
- `validate_csmv_media_lineage.py` exit 0：8210条、8008源族、202重复族/404行、跨split 0、负面夹具命中。
- `run_m2_leakage_tests.py --no-write` exit 0：`PASS_WITH_LIMITATIONS`、Critical=0；`--selftest`按预期输出`LEAKAGE_BLOCKED`且exit 0。
- `validate_m2_data_engineering.py`、`validate_lai_gai_second_primary.py`和`python -m compileall -q scripts`均exit 0。

### 失败与恢复记录

- `rg`在Windows再次因执行权限失败，改用PowerShell文件扫描，不重复同命令。
- 首次PowerShell响应hash计算使用当前运行时不支持的静态`SHA256.HashData`，hash为空且未纳入证据；改用`SHA256.Create().ComputeHash()`后记录真实响应hash。
- 首次`-I -S --public-core`因相邻模块不在`sys.path`而失败；仅加入已审查的`scripts/`目录后成功，site-packages仍禁用。
- 第二次构建因LAI-GAI provenance引用hash与当前文件不一致而fail-closed；固定序列化声明、更新引用hash并复核canonical不变后成功。
- 共享工作区在新validator已写入、release manifest尚未重建的短暂中间态触发一次00综合门`KeyError`，已由`WR-20260715-010`保留；当前dataset manifest已原子重建并通过独立release验证。

### 影响与边界

旧9项漂移不再是当前本地工程阻塞；CUC银标源也不再阻塞公开benchmark核心复现。特征页可达不等于资产获许可或已固定，专项validator的exit 0仅表示No-Go审计合同真实一致，不表示G2资产门通过。

### 风险、问题与阻塞

- CSMV视觉特征的资产级许可、稳定revision、相对文件清单、总字节数、逐文件SHA-256与实际8210键覆盖仍为`UNKNOWN`。
- 当前授权禁止Drive API、登录、特征下载和作者联系；任务10无法在该权限内合法制造上述外部元数据。
- 正式G2、全局`formal_split=false`、`formal_model_use_allowed=false`与任务20禁令等待00书面复审，不由本批次修改。

### 下一步

向00回交复现PASS与特征No-Go证据；请求00决定是否签发最小外部协调授权，以取得权利方提供的资产许可与单一特征族manifest。只有资产门闭合并获00书面G2通过后才允许任务20。

### Git状态

本记录、脚本、manifest、报告和共享工作区既有变更尚未提交、未推送。

## WR-20260715-012 — 将本机代理固化为网络与下载首选路径

- 时间：2026-07-15 21:57:39 +08:00
- 类型：DECISION | POLICY | DOC
- 任务/门：00总控 / 网络传输优先级
- 状态：完成
- 负责人：Codex

### 背景与目标

用户明确要求以后访问网站或下载数据集时优先使用已经更正并监听的本机代理，需要把“可用”升级为“默认首选”，保证后续任务不会重新默认直连。

### 实际变更

- 更新`TASK00_LOCAL_PROXY_AND_DATA_DOWNLOAD_POLICY_20260715.md`：网络任务优先加载Git忽略`.env`中的本机代理；不可用或不适用时才按原任务授权决定直连或停止。
- 同步`RESOURCE_TIME_POLICY.md`和总纲v1.9的传输顺序；tracked文件不记录具体代理端点。
- 未修改`.env`端点、数据许可、host白名单、下载资产范围、G门或任务20状态。
- 本批次未访问外部网站，未下载数据、特征或媒体。

### 验证与证据

- 文本复核确认三份权威政策均包含“本机代理优先”与“不可用时按原授权直连或停止”规则。
- 首轮日志验证因并发新增任务10记录造成编号冲突而exit 1；未删除任何证据。任务10完成重排后，本记录使用下一个可用编号追加。
- 最终`validate_work_log.py` exit 0：38条记录、`errors=[]`、latest=`WR-20260715-012`；随后任务10追加013后仍按连续编号维护。
- `run_preparation_checks.py` exit 0：`blocking_checks=[]`、`m1_read_only_work_ready=true`、秘密扫描0命中、`formal_model_work_ready=false`；G2保持既有阻塞。

### 影响与边界

以后官方站点访问和已批准下载以本机代理为第一传输选择；这只改变默认顺序，不把代理可用性当作许可、固定版本、数据可用或G门通过证据。

### 风险、问题与阻塞

- 后续执行者必须显式加载项目`.env`；未加载不能声称已使用首选代理。
- 代理未监听或协议不兼容时不得静默切换第三方镜像或绕过访问限制。
- 当前M1/M2合同状态及G2阻塞不由本政策改变。

### 下一步

下一次已授权网络任务先记录代理加载与本机监听检查，再做官方host的小体量只读连通性验证。

### Git状态

tracked政策和工作记录尚未提交、未推送；本机`.env`继续由Git忽略。

## WR-20260715-013 — 同步M1状态断言并完成任务10最终准备门复验

- 时间：2026-07-15 22:03:04 +08:00
- 类型：FIX | TEST | HANDOFF
- 任务/门：10-M1–M2 / G2候选回交前综合验证
- 状态：完成（本地交付通过；正式G2仍待00与外部资产元数据）
- 负责人：Codex

### 背景与目标

任务10完成特征No-Go预审和公共核心复现后，首次综合准备检查发现`validate_m1_public_audit.py`仍要求DS-001旧状态token，未同步最新台账事实。需要修复该状态合同并重新运行强制交付门。

### 实际变更

- 将`scripts/validate_m1_public_audit.py`对`DATA_SOURCE_LEDGER.md`的断言从旧`LABEL_AND_URL_LINEAGE_READY_FORMAL_INPUT_BLOCKED`更新为当前`FEATURE_PREFLIGHT_NO_GO_REPRO_LOCAL_PASS_PENDING_00`。
- 将CSMV特征预审validator加入M1所需脚本清单；未放宽数据许可、UNKNOWN、G2或任务20门。
- 归并本批次共享工作日志编号冲突：00的009/010/012和任务10的011/013均保留原事实并恢复连续物理顺序；没有删除失败记录。

### 验证与证据

- 首次`run_preparation_checks.py` exit 1，唯一`blocking_checks=[m1_public_audit]`，错误为台账缺少旧状态token；其他特征、lineage、M2数据与release门已通过。
- 修复后`validate_work_log.py` exit 0：38条记录、`errors=[]`、当时latest=`WR-20260715-012`。
- 修复后`run_preparation_checks.py` exit 0：`blocking_checks=[]`、`m1_read_only_work_ready=true`、秘密扫描0；特征预审合同、CSMV lineage、M2数据、M2 release均通过。
- 综合门仍诚实输出`formal_model_work_ready=false`：正式环境缺faiss且G2未书面通过；本批次没有把准备门通过误写成正式模型放行。

### 影响与边界

M1机读状态现与权威台账同步，先前共享M2中间态与旧token导致的综合门失败都已闭合。复现本地PASS与特征资产No-Go同时被准备门一致表达。

### 风险、问题与阻塞

- 正式CSMV输入资产的许可、revision、文件树、体量、逐文件SHA-256和8210覆盖仍未取得。
- 任务10不能自行把全局`formal_split`或`formal_model_use_allowed`改为true；需00书面复审。

### 下一步

将`HANDOFF_10.md`、特征预审报告/manifest、当前复现manifest和最终验证结果发送任务00，申请G2裁定与最小外部资产元数据取得决策。

### Git状态

本记录及共享工作区变更尚未提交、未推送。

## WR-20260715-014 — 00复审CSMV特征No-Go并将G2收敛为单一资产阻塞

- 时间：2026-07-15 22:16:50 +08:00
- 类型：REVIEW | DECISION | AUTHORIZATION | TEST | DOC
- 任务/门：00总控 / CSMV特征资产与G2复审
- 状态：完成（复现子门关闭；G2资产门继续阻塞）
- 负责人：Codex

### 背景与目标

任务10按`AUTH-00-CSMV-FEATURE-ASSET-PREFLIGHT-RO-20260715`回交19项公共核心复现PASS与特征资产预审No-Go，请求00独立复审、关闭`REPRODUCIBILITY_STALE`子阻塞，并决定最小外部元数据取得路径。

### 实际变更

- 新增`TASK00_CSMV_FEATURE_PREFLIGHT_G2_REVIEW_20260715.md`，签署`REVIEW-00-CSMV-FEATURE-PREFLIGHT-G2-20260715`：接受19项当前复现零漂移，关闭复现陈旧子阻塞；接受特征专项为诚实No-Go，不给予资产门信用。
- 新增`TASK00_CSMV_ONE_FEATURE_FAMILY_METADATA_COORDINATION_AUTHORIZATION_20260715.md`，签发单一特征族最小权利方元数据协调授权：一次请求、一次跟进、可收不超过5 MiB纯元数据，禁止`.npy`、媒体、Drive API、EULA和任务20。
- 将总纲升级为v1.10；同步`DECISION_LOG.md`、`G1_G2_EVIDENCE_MATRIX.md`、`HANDOFF_10.md`、`DATA_SOURCE_LEDGER.md`、M1审计、风险、可行性、规划/进度/发现文件。
- 将G2机器状态从`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_REPRODUCIBILITY_STALE`收敛为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；同步构建器、泄漏门、M1/M2/release验证器和release manifest。`formal_split=false`、`formal_model_use_allowed=false`不变。
- 本批次未联系权利方、未发送外部消息、未调用Drive API、未下载特征或媒体、未创建任务20。

### 验证与证据

- 00首次独立运行`reproduce_m2_minimal.py --public-core`（裁定变更前）exit 0：19项before/after一致、`mismatches=[]`、凭证环境未转发。
- 特征专项、M2 release、泄漏live门和负面selftest均exit 0；特征专项同时明确`g2_asset_ready=false`，负面夹具正确输出`LEAKAGE_BLOCKED`。
- 更新G2状态合同后的首次重放exit 1：两条构建命令均returncode 0，但5个状态派生文件相对旧baseline改变；该有意状态迁移失败完整保留。以新状态再次重放exit 0：19项before/after一致、`mismatches=[]`。
- 新状态下`validate_m2_release.py`、`validate_m2_data_engineering.py`、`validate_m1_public_audit.py`和`validate_csmv_feature_preflight.py`均exit 0；release现场hash漂移0，G1=`PASS`，G2为新单一资产阻塞。

### 影响与边界

本地复现陈旧不再是G2阻塞；G2只剩一个资产准入工作包，但该工作包含许可、revision、relative path/bytes/SHA-256 manifest、特征schema与8210覆盖六类必需证据。专项validator通过不能替代资产准入，页面HTTP 200也不能替代许可或fixity。

### 风险、问题与阻塞

- 权利方元数据尚未取得，I3D/VideoMAE均未被选为正式输入；任一必需字段为`UNKNOWN`时G2继续阻塞。
- 当前授权只允许元数据协调，不允许特征内容下载；即使收到完整manifest，也须00另行资产准入复审和下载授权。
- 全局`formal_split=false`、正式训练/索引和任务20禁令不变。

### 下一步

任务10按最小授权优先向I3D权利方/维护者请求许可、revision、manifest、schema与8210覆盖；回交脱敏证据后由00决定是否签发限额下载授权。

### Git状态

本记录、书面裁定、授权、机器状态和共享工作区既有变更尚未提交、未推送。
## WR-20260715-015 — CSMV I3D 官方元数据请求因 GitHub 集成权限受阻

- 时间：2026-07-15 22:41:05 +08:00
- 类型：COORDINATION | FAILURE | DOC
- 任务/门：10-M1–M2 / CSMV 正式输入资产 G2 准入
- 状态：阻塞（未产生外部消息；等待 GitHub 写权限或用户手工提交）
- 负责人：Codex

### 背景与目标

00 以 `AUTH-00-CSMV-ONE-FEATURE-FAMILY-METADATA-COORDINATION-20260715` 授权任务10通过一个官方渠道，优先向 I3D 权利方请求许可、固定 revision、逐文件 fixity manifest、特征 schema 与 8,210 键覆盖。授权不包含 `.npy` 或媒体下载。

### 实际变更

- 从官方固定仓库定位公开 GitHub Issues 为单一联系渠道，并检索是否已有相同主题的开放 Issue。
- 安装用户确认的 GitHub 连接器，拟创建一条只请求纯元数据的公开 Issue。
- GitHub 创建操作返回 403 `Resource not accessible by integration`；没有 issue number/URL，确认没有外部写入。
- 新增 `CSMV_I3D_METADATA_COORDINATION_20260715.md`，保存脱敏渠道、请求字段、失败结果与恢复条件；未记录账户、Cookie、token 或个人邮箱。
- 未切换到第二联系渠道，未调用 Drive API，未登录数据目录，未下载特征或媒体，未创建任务20。

### 验证与证据

- GitHub 仓库 Issue 检索结果：相关开放 Issue 为 0。
- GitHub 创建 Issue 结果：HTTP 403，错误为 `Resource not accessible by integration`；无 issue number、无 URL。
- 外部写入数：0；特征下载数：0；媒体下载数：0。
- 协调事实与拟请求六类字段见 `CSMV_I3D_METADATA_COORDINATION_20260715.md`。

### 影响与边界

旧 18 输出的复现陈旧问题已由当前 19 项零漂移重放关闭；本次失败不影响该本地工程结论。G2 仍只被 CSMV 正式输入特征的资产级许可、revision、manifest/fixity、schema 与 8,210 覆盖阻塞，`formal_split=false` 和任务20禁令不变。

### 风险、问题与阻塞

- 当前 GitHub App 对外部官方仓库没有创建 Issue 的权限；读取能力不能替代写入权限。
- 在权利方实际回复前，不得把 README 的公开下载链接或页面 HTTP 200 外推为特征资产许可与固定性。

### 下一步

用户可在 `https://github.com/IEIT-AGI/MSA-CRVI/issues/new` 手工提交 `CSMV_I3D_METADATA_COORDINATION_20260715.md` 中的请求，或补足当前 GitHub 连接器写权限后由任务10在同一渠道重试。收到实质回复后回交00做资产准入复审；未通过复审前不得下载特征内容。

### Git状态

本记录、协调报告及共享工作区既有变更尚未提交、未推送。

## WR-20260715-016 — 核验并登记CSMV官方Issue #5已成功发出

- 时间：2026-07-15 22:47:43 +08:00
- 类型：COORDINATION | PROGRESS | DATA | DOC
- 任务/门：10-M1–M2 / CSMV正式输入资产G2准入
- 状态：部分完成（正式请求已发出；等待权利方实质回复与00复审）
- 负责人：Codex

### 背景与目标

用户提供`https://github.com/IEIT-AGI/MSA-CRVI/issues/5`，用于恢复此前因GitHub集成403而未成功发出的I3D纯元数据请求。需要核验其官方身份、公开状态和正文范围，并把真实协调状态写回权威记录。

### 实际变更

- 匿名只读打开官方Issue #5，核验仓库、Issue编号、Open状态、创建日期、标题和正文请求字段。
- 更新`CSMV_I3D_METADATA_COORDINATION_20260715.md`：保留此前403失败事实，新增手工发送成功证据，并将状态改为`OFFICIAL_ISSUE_OPEN_WAITING_RIGHTS_HOLDER_RESPONSE`。
- 更新`DATA_SOURCE_LEDGER.md`的DS-001：登记公开Issue定位、等待回复状态和不早于2026-07-22跟进边界。
- 更新`HANDOFF_10.md`、`progress.md`和`findings.md`，明确正式请求额度已使用、不得重复创建或切换第二渠道。
- 未评论Issue、未下载附件或特征、未调用Drive API、未改变G2、`formal_split`或任务20状态。

### 验证与证据

- 官方公开页面：`https://github.com/IEIT-AGI/MSA-CRVI/issues/5`。
- 现场事实：repository=`IEIT-AGI/MSA-CRVI`；issue_number=5；state=`Open`；created=2026-07-15。
- 正文覆盖：asset-level research-use license、fixed revision、relative filenames/byte sizes/SHA-256、8,210 `video_file_id` coverage、extractor/version、dtype/shape、total size，并明确独立复审前不下载特征内容。
- 外部追加写入：0；特征/媒体下载：0。

### 影响与边界

协调子状态从“连接器发送受阻”变为“官方请求已发出、等待回复”。这不等于取得许可、manifest、8210覆盖或特征schema，不给G2资产门信用。`REPRODUCIBILITY_STALE`仍保持已关闭，19项公共核心重放结论不变。

### 风险、问题与阻塞

- 权利方尚未实质回复，六类资产准入证据仍为UNKNOWN。
- 不得在2026-07-22前跟进；届时若仍无回复，授权只允许在同一Issue内跟进一次。
- 即使收到回复，也须先由00完成书面资产准入复审，不能自动下载特征或放行G2。

### 下一步

等待Issue #5的维护者回复。收到回复后仅核验不超过5 MiB的纯元数据，并回交00；若2026-07-22仍无回复，再按原授权在同一Issue内至多跟进一次。

### Git状态

本记录、协调状态更新及共享工作区既有变更尚未提交、未推送。

## WR-20260715-017 — 00复审CSMV I3D协调403并保留原请求额度

- 时间：2026-07-15 22:47:57 +08:00
- 类型：REVIEW | DECISION | AUTHORIZATION | DOC | TEST
- 任务/门：00总控 / CSMV正式输入资产G2协调复审
- 状态：完成（接受无外部写入；G2资产门继续阻塞）
- 负责人：Codex

### 背景与目标

任务10回交官方GitHub Issues协调尝试：GitHub集成在创建I3D纯元数据Issue时返回403 `Resource not accessible by integration`，没有issue number/URL、没有外部写入，也没有切换第二渠道。00须判定该失败是否消耗原授权额度，并给出最小恢复路径。

### 实际变更

- 新增`TASK00_CSMV_I3D_METADATA_COORDINATION_ATTEMPT_REVIEW_20260715.md`，签署`REVIEW-00-CSMV-I3D-METADATA-COORDINATION-ATTEMPT-20260715`：接受403事实，但将其归类为连接器写权限阻塞而非权利方拒绝。
- 明确外部写入为0、维护者未被联系，因此原授权的一次正式请求和一次7日后跟进额度均未消耗；原授权有效期不变。
- 新增`CSMV_I3D_GITHUB_ISSUE_REQUEST_20260715.md`，提供不含个人信息、只请求许可/revision/manifest/覆盖/schema的可复制Issue标题与正文。
- 同步原授权、总纲决策表、`DECISION_LOG.md`、`G1_G2_EVIDENCE_MATRIX.md`、`HANDOFF_10.md`、`task_plan.md`和`progress.md`；把新裁定与提交包纳入准备检查必需文件。
- 本批次未重试创建Issue、未访问或下载数据、未调用Drive API、未切换联系渠道、未创建任务20。

### 验证与证据

- `python -m compileall -q scripts`：exit 0。
- `scripts/validate_work_log.py`（追加本记录前）：exit 0，41条记录，`errors=[]`，最新为`WR-20260715-015`。
- `scripts/run_preparation_checks.py`（追加本记录前）：exit 0，`blocking_checks=[]`、`required_files.missing=[]`、`m1_read_only_work_ready=true`、`formal_model_work_ready=false`。
- 同一综合检查确认G1=`PASS`、G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`、19项当前复现零漂移、全局`formal_split=false`；资产预审仍为`NO_GO_PENDING_ASSET_METADATA_AND_LICENSE`。

### 影响与边界

此次403不提供任何资产许可或固定性证据，也不构成维护者拒绝。后续只允许在同一官方Issues渠道二选一：用户手工提交，或连接器取得创建Issue权限后重试一次。任一路径成功后另一条立即停止；满7个自然日无回复时才能在同一issue内跟进一次。

### 风险、问题与阻塞

- GitHub连接器尚无对目标仓库创建Issue的权限；在成功创建公开Issue之前，不能声称已联系权利方。
- I3D许可、稳定revision、逐文件fixity manifest、特征schema与8210键覆盖仍未取得；G2不得放行。
- 收到元数据不自动授权特征下载，仍须00资产准入复审。

### 下一步

用户可使用`CSMV_I3D_GITHUB_ISSUE_REQUEST_20260715.md`在官方仓库手工创建Issue；或者先补足GitHub连接器写Issue权限，再由任务10在同一渠道重试一次。不要同时执行两条路径。

### Git状态

本记录、00复审、手工Issue提交包及共享工作区既有变更尚未提交、未推送。

## WR-20260715-018 — 00确认官方Issue #5已发送并启动等待期

- 时间：2026-07-15 22:54:14 +08:00
- 类型：REVIEW | DECISION | COORDINATION | DOC | TEST
- 任务/门：00总控 / CSMV正式输入资产G2协调复审
- 状态：完成（正式请求已发送；等待权利方回复）
- 负责人：Codex

### 背景与目标

任务10回交用户已在官方`IEIT-AGI/MSA-CRVI`仓库手工创建Issue #5，请求00独立确认正式请求额度、跟进窗口和G2状态。

### 实际变更

- 匿名只读打开官方公开Issue #5，独立确认仓库、编号、Open状态、创建日期、标题和正文请求范围。
- 新增`TASK00_CSMV_OFFICIAL_ISSUE_5_SENT_REVIEW_20260715.md`，签署`REVIEW-00-CSMV-OFFICIAL-ISSUE-5-SENT-20260715`：正式请求额度已使用，2026-07-22前不得跟进。
- 将原授权状态更新为`REQUEST_SENT_WAITING_RIGHTS_HOLDER_RESPONSE`；追加说明连接器重试、重复Issue和第二渠道均停止，唯一一次跟进只能在同一Issue内执行。
- 保留此前403失败及当时“无外部写入”的历史裁定；在旧复审文件追加后续状态，不删除或改写失败证据。
- 同步协调报告、手工提交包、总纲、决策日志、G1/G2矩阵、交接、规划、进度与发现文件；新00复审纳入准备检查必需文件，并删除同一授权文件在必需清单中的重复项。
- 本批次未在Issue发表评论、未下载附件/特征/媒体、未调用Drive API、未创建任务20。

### 验证与证据

- 官方公开页面`https://github.com/IEIT-AGI/MSA-CRVI/issues/5`：仓库`IEIT-AGI/MSA-CRVI`、Issue #5、Open、创建日期2026-07-15。
- 公开正文覆盖资产级研究许可、固定revision、相对文件名/bytes/SHA-256、8210键覆盖、提取器/版本、dtype/shape、总体量，并声明独立复审前不下载特征。
- 诚实边界：公开正文使用`one released visual feature family`，没有逐字点名I3D；因此只接受为授权内的一次正式请求，不声称维护者已收到明确I3D限定。
- `python -m compileall -q scripts`：exit 0。
- `scripts/validate_work_log.py`（追加本记录前）：exit 0，43条、`errors=[]`、最新`WR-20260715-017`。
- `scripts/run_preparation_checks.py`（追加本记录前）：exit 0，`blocking_checks=[]`、必需文件无缺失；G1=`PASS`、G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`、`formal_model_work_ready=false`。
- 针对本批次文件的`git diff --check`：exit 0。

### 影响与边界

协调状态从“可手工提交或补权限重试”收敛为“正式请求已发送、等待回复”。Issue创建不提供许可、revision、fixity、schema或8210覆盖证据，G2无变化。

### 风险、问题与阻塞

- 权利方尚无实质回复，六类资产准入字段继续为UNKNOWN。
- 公开正文没有明确点名I3D；若2026-07-22及以后仍无回复，唯一一次同Issue跟进应明确I3D优先范围。
- 收到回复不自动授权特征内容下载，仍须00书面资产准入复审。

### 下一步

等待权利方回复。2026-07-22前不评论、不催促；若届时仍无回复，才可在同一Issue内跟进一次，并明确I3D优先请求。

### Git状态

本记录、00复审、协调状态与共享工作区既有变更尚未提交、未推送。

## WR-20260715-019 — 成功浅克隆CSMV官方仓库并确认特征资产不在Git中

- 时间：2026-07-15 23:00:33 +08:00
- 类型：DATA | TEST | PROGRESS | DOC
- 任务/门：10-M1–M2 / CSMV正式输入资产可得性
- 状态：完成（GitHub仓库可下载；外部特征资产仍阻塞）
- 负责人：Codex

### 背景与目标

用户提供官方仓库目录、HTTPS、GitHub CLI和SSH克隆方式，并授权尝试直接下载。需要验证官方GitHub仓库的实际下载速度、revision、文件树和是否包含I3D/VideoMAE特征，同时不越权访问Google Drive或媒体资产。

### 实际变更

- 从Git忽略`.env`加载代理环境变量但不回显值，使用HTTPS对`IEIT-AGI/MSA-CRVI`的main分支执行depth=1浅克隆。
- 克隆存入Git忽略目录`data/raw/csmv/upstream-git-20260715/`；未使用GitHub CLI、SSH、Drive API或第三方镜像。
- 新增`CSMV_GITHUB_CLONE_AUDIT_20260715.md`，记录HEAD、体量、文件树、`.npy`/LFS审计和Windows换行边界。
- 更新`DATA_SOURCE_LEDGER.md`、`progress.md`和`findings.md`；未改变G1/G2、正式split或任务20状态。

### 验证与证据

- HTTPS浅克隆exit 0，耗时约20秒；HEAD=`99d14240254b1381dde0b9c56add140381f65117`；pack约4.97 MiB。
- canonical Git提交：10文件、14,436,790 bytes；`CSMV/`目录8文件；`.npy`=0；Git LFS pointer=0。
- `git show HEAD:<path>`逐文件与既有固定raw快照比较：文件集合差异0、snapshot/blob不一致0。
- 工作树有8个文本文件受LF→CRLF checkout转换；该差异已判为本机工作树转换，不是上游revision漂移。

### 影响与边界

官方GitHub仓库可快速直接下载，用户无需代为下载该仓库。仓库只包含标注、split、标签映射、视频—评论映射、URL表与说明，不包含任何正式视觉特征文件，因此不能关闭特征资产许可、fixity、schema和8210覆盖阻塞。

### 风险、问题与阻塞

- Windows工作树文本hash不能用作canonical Git blob fixity；继续使用既有raw快照和`csmv-source-v1.manifest.json`。
- I3D/VideoMAE特征仍位于独立外部入口，当前总纲与00裁定不授权下载；Issue #5仍等待权利方回复。

### 下一步

保留浅克隆用于官方仓库版本审计；等待Issue #5回复。收到权利方许可与manifest后交00复审，再决定是否签发特征下载授权。

### Git状态

raw浅克隆被Git忽略；本记录、克隆审计报告和共享工作区既有变更尚未提交、未推送。

## WR-20260715-020 — 扩大镜像与隔离预取授权并修复release一致性

- 时间：2026-07-15 23:04:14 +08:00
- 类型：DECISION | AUTHORIZATION | DATA | DOC | TEST | FIX
- 任务/门：00总控 / 项目级数据取得政策与M1—M2一致性
- 状态：完成（取得范围已扩大；正式资产门保持阻塞）
- 负责人：Codex

### 背景与目标

用户更正此前“不得切换第三方镜像、不得扩大许可和下载范围”的限制，明确允许为效率切换第三方镜像并扩大项目内部取得范围。需要把该授权写入SSOT，同时区分“内部下载授权扩大”和“第三方法律许可不能自行扩大”。

### 实际变更

- 新增`TASK00_EFFICIENCY_FIRST_MIRROR_AND_ACQUISITION_POLICY_20260715.md`，签署`POLICY-00-EFFICIENCY-FIRST-MIRROR-AND-EXPANDED-ACQUISITION-20260715`。
- 将网络路径改为本机代理优先、必要时官方直连或可信第三方镜像；允许公开API、大包、媒体、特征与多个候选资产在记录体量/目录/磁盘预算后直接进入Git忽略隔离区。
- 建立`METADATA_ONLY`、`QUARANTINE_ACQUIRED`、`FORMAL_USE_APPROVED`三级状态；许可未知资产允许隔离预取，但不得正式训练、建索引、发布、再分发或获得G门信用。
- 明确用户扩大的是项目内部取得授权，不能自行扩大权利方许可、版权、隐私和平台条款；付费、EULA/DUA、机构签署和绕过访问控制仍须停止或另获确认。
- 总纲升级为v1.11；同步旧代理政策、决策日志、资源政策、安全检查、风险、发布边界、CSMV授权/Issue复审、G1/G2矩阵、交接、规划、进度与发现文件。
- 现场核验D盘可用空间为70.09 GiB并更新资源政策。
- 修正Data Card、Datasheet和发布边界中已过期的“复现陈旧”措辞，恢复为当前19项公共核心复现零漂移事实。
- 本批次00未实际访问镜像、下载新资产、调用外部API、训练、建索引或创建任务20；任务10此前官方浅克隆事实由`WR-20260715-019`单独记录。

### 验证与证据

- `python -m compileall -q scripts`：exit 0。
- 首次`run_preparation_checks.py`：exit 1，唯一`blocking_checks=[m2_release]`；原因是政策同步修改了`DATA_RELEASE_BOUNDARY.md`，而dataset manifest仍保存旧文档hash。失败完整保留。
- 首次重建M2 release：构建器exit 0；随后release validator仍exit 1，文档hash已关闭，但`dataset-v1.manifest.json`相对旧reproducibility记录发生预期变化。
- 运行`reproduce_m2_minimal.py --public-core`：exit 0；19项before/after一致、`mismatches=[]`、两条隔离命令returncode均为0。
- 随后`validate_m2_release.py`：exit 0；documentation 5/5、19项现场hash零漂移、G1=`PASS`、G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`、`formal_split=false`。
- `git diff --check`：exit 0，仅输出既有Windows换行提示，无空白错误。

### 影响与边界

后续任务可为效率使用可信第三方镜像，并可在许可最终闭合前预取公开资产做本地审计。该变化取消“必须等许可全闭合才能传输”的内部等待，但不取消正式使用、泄漏、隐私、T0或发布门。

当前CSMV可在等待Issue #5回复期间并行寻找和隔离取得候选特征；但Issue跟进日期、单一联系渠道和G2状态不变。

### 风险、问题与阻塞

- 镜像可能与官方版本不一致；必须记录发布者/revision/体量/hash，冲突时两份都隔离，不静默选用。
- 法律许可、schema和8210覆盖仍未闭合；隔离下载不能进入正式模型。
- D盘当前约70.09 GiB可用，大包仍需逐批预算和安全余量，不能无限下载。

### 下一步

任务10可按新政策并行定位CSMV I3D及必要备选特征的官方副本或可信镜像，先完成体量/磁盘预算，再隔离下载并建立逐文件hash与覆盖清单；正式使用继续等待00资产准入复审。

### Git状态

本记录、新政策、总纲v1.11、重建release与共享工作区既有变更尚未提交、未推送。

## WR-20260715-021 — 重建GitHub克隆审计后的M2派生基线并闭合19项重放

- 时间：2026-07-15 23:04:54 +08:00
- 类型：FIX | TEST | REPRODUCIBILITY | DOC
- 任务/门：10-M1–M2 / GitHub克隆审计后的release fixity
- 状态：完成（派生基线零漂移；G2资产门仍阻塞）
- 负责人：Codex

### 背景与目标

新增CSMV GitHub克隆审计及数据源台账记录后，综合准备检查按fail-closed规则发现`DATA_RELEASE_BOUNDARY.md`的现场hash与`dataset-v1.manifest.json`中的旧引用不一致。需要保留首次失败事实，重建派生release基线，并以第二次隔离重放确认当前输出稳定。

### 实际变更

- 运行`build_m2_release.py`，重算5份release文档引用并更新`dataset-v1.manifest.json`等派生manifest。
- 第一次`reproduce_m2_minimal.py --public-core`如实报告3项从旧基线迁移到当前基线的漂移：`leakage-audit-v1.manifest.json`、`split-v1.manifest.json`和`dataset-v1.manifest.json`；未删除或掩盖失败。
- 在当前基线上执行第二次同命令，19项before/after SHA-256全部一致，`mismatches=[]`。
- 未修改泄漏门阈值、G1/G2裁定、`formal_split`或特征资产授权边界。

### 验证与证据

- `scripts/build_m2_release.py`：exit 0，`gate=PASS_WITH_LIMITATIONS`，`status=LOCAL_CANDIDATE_G1_PASS_G2_BLOCKED`。
- 首次`scripts/reproduce_m2_minimal.py --public-core`：exit 1，19项中3项漂移，`status=REPLAY_FAILED`；该失败用于迁移诊断并被本记录保留。
- 第二次`scripts/reproduce_m2_minimal.py --public-core`：exit 0，`outputs_checked=19`，`mismatches=[]`，`status=PASS_CURRENT_CSMV_SOURCE_GROUP_SPLIT`。
- `scripts/validate_m2_release.py`：exit 0，5份文档hash通过，7项manifest lineage通过，G1=`PASS`，G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`，`steps_34_39_local_package_ready=true`。

### 影响与边界

克隆审计造成的派生文档fixity漂移已经闭合，不能再把旧复现记录列为当前阻塞。剩余唯一研究门问题仍是外部正式特征资产的资产级许可、固定revision、逐文件fixity manifest、schema和8,210样本覆盖；GitHub仓库本身不包含这些资产。

### 风险、问题与阻塞

- Issue #5尚无权利方实质回复，I3D/VideoMAE资产仍不得下载或用于正式模型输入。
- G2未通过、全局`formal_split=false`，不得据此创建任务20。

### 下一步

等待Issue #5权利方回复；收到回复后仅核验授权范围内的资产元数据并交00复审。若2026-07-22仍无回复，才可按既有裁定在同一Issue内进行一次明确I3D范围的跟进。

### Git状态

raw浅克隆被Git忽略；本记录、派生manifest、克隆审计报告和共享工作区既有变更尚未提交、未推送。

## WR-20260715-022 — 更正并发工作日志编号并确认现行取得政策

- 时间：2026-07-15 23:06:23 +08:00
- 类型：FIX | DECISION | TEST | DOC
- 任务/门：00总控 / 并发工作记录与现行数据取得边界
- 状态：完成
- 负责人：Codex

### 背景与目标

00与任务10并发追加工作记录时曾同时占用`WR-20260715-020`，导致工作日志验证器阻断。需要在不删除任何工作内容的前提下恢复编号连续性，并明确并发记录中的旧下载边界已被新政策更新。

### 实际变更

- 保留先写入的00政策记录为`WR-20260715-020`。
- 后写入的任务10派生基线记录已机械顺延为`WR-20260715-021`，元数据字段采用合同要求的“任务/门”；正文、测试结果和失败证据均未删除。
- 确认现行政策以总纲v1.11和`POLICY-00-EFFICIENCY-FIRST-MIRROR-AND-EXPANDED-ACQUISITION-20260715`为准：`WR-20260715-021`中的“当前不授权下载”是并发取得的旧边界，不再代表当前内部下载授权。
- 当前允许官方或可信镜像的隔离预取；正式训练、发布与G2仍须资产准入闭合。

### 验证与证据

- 并发冲突首次由`validate_work_log.py`检出：重复`WR-20260715-020`、后写记录缺少“任务/门”、当日序号不连续；该失败没有删除或改写为通过。
- M2 release已在前两条记录所述的重建/隔离重放后恢复：19项零漂移、G1=`PASS`、G2仍为资产阻塞。

### 影响与边界

本次只修正日志编号和当前政策解释，不改写任务10的克隆事实、复现结果、G1/G2、split或Issue跟进纪律。

### 风险、问题与阻塞

并发代理仍可能同时申请同一日志编号；后续写入前须重新读取最后一条记录，发生冲突时由后写记录顺延并追加说明。

### 下一步

按新效率政策继续镜像/公开资产隔离取得准备；每次新工作批次写日志前重新读取当前最新编号。

### Git状态

本次并发编号更正、新政策、release重建及共享工作区既有变更尚未提交、未推送。

## WR-20260715-023 — 接入并审计用户提供的CSMV I3D本地特征包

- 时间：2026-07-15 23:39:47 +08:00
- 类型：DATA | FEATURE | TEST | PROGRESS | DOC
- 任务/门：10-M1–M2 / CSMV正式输入资产本地隔离准入
- 状态：部分完成（本地fixity/schema/8210覆盖闭合；许可/revision/权利方attestation待复审）
- 负责人：Codex

### 背景与目标

用户提供`D:\soft\I3D-feature-001`并询问如何按官方示意结构使用。需要在不重复复制大包、不训练、不把公开可得误写成正式许可的前提下，建立稳定项目入口，核验真实文件树、NumPy schema、CSMV 8210键覆盖与逐文件fixity，并提供只读加载方式。

### 实际变更

- 保持用户源目录不动，在Git忽略的`data/raw/csmv/features/visual_feature/I3D`建立Windows directory junction，目标为源包内`visual-feature-allCAMV`；没有复制约2.56 GiB内容。
- 新增`scripts/audit_csmv_i3d_asset.py`：从固定`video_to_comment.json`提取8210必需ID，全量读取9942个NumPy header、计算内容hash、核对覆盖并生成tracked隔离manifest。
- 新增`scripts/load_csmv_i3d.py`：可按官方`video_file_id`或canonical `item_id`只读mmap加载；固定`allow_pickle=False`并校验`float32[T,1024]`，不读取评论正文或标签。
- 新增`data/manifests/csmv-i3d-quarantine-v1.manifest.json`和`CSMV_I3D_QUARANTINE_AUDIT_20260715.md`；同步特征预审manifest/validator、数据源台账、G1/G2证据、交接、进度、发现、计划与可选环境变量模板。
- 当前资产状态由纯元数据No-Go更新为`QUARANTINE_ACQUIRED_LICENSE_REVISION_ATTESTATION_PENDING`；`formal_model_input_allowed=false`、`g2_asset_credit=false`、全局`formal_split=false`保持不变。

### 验证与证据

- 现场盘点：9942个`.npy`、1个`feature_shapes.json`；`.npy`共2,752,998,144 bytes，整个目录共2,753,015,726 bytes。
- 全量审计命令`audit_csmv_i3d_asset.py`：exit 0，耗时约33秒；9942个数组均为`float32[T,1024]`、`T=6—1719`、schema错误0；8210/8210必需ID命中、缺失0、附加1732。
- 全包内容树SHA-256=`35be2d18e1d2413ba3765034cdb454baa5e3496d49c540c9be00e81bbc2c1942`；隔离manifest含8210个必需文件逐文件relative path/bytes/SHA-256/shape/dtype，文件SHA-256=`425829cf3271ce3c695a011e75b9efa94c4efab76458fda9f902e6eeb9c99c1e`。
- 加载器正向测试：按`video_file_id`及对应canonical `item_id`均得到同一`float32[100,1024]` mmap；负向`invalid_id`按预期exit 1并拒绝非数字路径输入。
- `validate_csmv_feature_preflight.py`：exit 0；本地9942文件、8210逐文件hash、未知项fail-closed及诚实G2状态全部通过。
- `python -m compileall -q`覆盖3个新增/修改脚本：exit 0。
- `build_m2_release.py`、`reproduce_m2_minimal.py --public-core`、`validate_m2_release.py`均exit 0；19项before/after零漂移，G1=`PASS`，G2仍为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`。

### 影响与边界

截图所示的稳定语义现已落为项目内`visual_feature/I3D`入口；训练代码后续可按ID逐个mmap读取，不需要把源包改名或复制。任务10已得到本地文件树、体量、schema、fixity和8210覆盖证据，但这些只证明当前字节的完整性与可加载性，不证明权利方许可、官方revision或提取器身份。

### 风险、问题与阻塞

- `feature_shapes.json`仅含646条部分shape声明；其646条均匹配，但完整schema以9942文件逐头审计为准。
- 包含1732个非当前CSMV标签集文件；加载正式样本必须以固定8210键集合为白名单，不把额外文件加入样本。
- 资产级许可、稳定官方revision、I3D提取器版本与权利方fixity attestation仍UNKNOWN；需Issue #5回复和00书面复审。
- junction依赖`D:\soft\I3D-feature-001\visual-feature-allCAMV`持续存在；移动源目录后需重建junction或设置`CSMV_I3D_ROOT`。

### 下一步

1. 将`csmv-i3d-quarantine-v1.manifest.json`及审计报告交00复审，确认本地fixity/schema/覆盖子门。
2. 继续等待Issue #5对资产许可、稳定revision和包身份的回复；2026-07-22前不催促。
3. 00未正式放行前不冻结池化/padding策略、不训练、不建正式索引、不创建任务20。

### Git状态

2.56 GiB源特征与junction均被Git忽略；tracked审计脚本、manifest、报告、台账及共享工作区既有变更尚未提交、未推送。

## WR-20260715-024 — 同步M1审计验证器到I3D隔离取得新状态

- 时间：2026-07-15 23:42:22 +08:00
- 类型：FIX | TEST | DOC
- 任务/门：10-M1–M2 / 综合准备检查
- 状态：完成
- 负责人：Codex

### 背景与目标

WR-20260715-023完成后首次综合准备检查唯一阻塞为`m1_public_audit`：验证器仍硬编码要求DS-001旧状态`REPRO_PASS_ASSET_ADMISSIBILITY_BLOCKED_OFFICIAL_ISSUE_OPEN`，与台账已更新的I3D隔离取得事实不一致。需要同步验证合同，同时保留许可和正式使用fail-closed边界。

### 实际变更

- 修改`scripts/validate_m1_public_audit.py`，将DS-001必需状态更新为`I3D_QUARANTINE_8210_COVERAGE_LICENSE_REVISION_PENDING`。
- 新增对`csmv-i3d-quarantine-v1.manifest.json`的schema、隔离状态、8210/8210覆盖、8210逐文件fixity条目、schema错误数及`formal_use_ready=false`验证。
- 将I3D审计脚本和只读加载器加入M1必需脚本清单；未删除原CSMV/iNews/NEmo/MVIndEmo审计要求。

### 验证与证据

- 修改前`run_preparation_checks.py`：exit 0的shell组合中综合对象明确`blocking_checks=["m1_public_audit"]`，错误为旧状态token缺失；该失败在WR-20260715-023后执行输出及本记录中保留。
- 修改后`validate_m1_public_audit.py`：exit 0，`passed=true`、`errors=[]`。
- 修改后`run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`m1_read_only_work_ready=true`；CSMV特征专项仍显示`g2_asset_ready=false`。

### 影响与边界

综合准备检查现在能识别“本地隔离完整性已闭合、正式资产准入仍阻塞”的新状态，不再要求过期字符串。此修复没有把`QUARANTINE_ACQUIRED`改为`FORMAL_USE_APPROVED`，也没有修改G2或任务20状态。

### 风险、问题与阻塞

资产级许可、稳定官方revision、权利方包身份/fixity确认和00复审仍未完成；`formal_model_work_ready=false`是预期结果而非验证器故障。

### 下一步

将本地隔离审计包回交00复审；继续等待Issue #5权利方回复。

### Git状态

本修复、I3D审计包及共享工作区既有变更尚未提交、未推送。

## WR-20260715-025 — 复核I3D论文实验可行性与180步协议差异

- 时间：2026-07-15 23:58:12 +08:00
- 类型：DATA | REVIEW | DECISION | DOC
- 任务/门：10-M1–M2 / CSMV I3D论文实验准入
- 状态：部分完成（科学可行；序列协议与最终资产裁定待冻结）
- 负责人：Codex

### 背景与目标

用户询问从发表论文角度，只有视频特征是否足以支撑实验。需要以正式论文、官方README和本地8210文件为依据，区分“科学上可做实验”与“项目G2/资产许可已闭合”。

### 实际变更

- 只读核验NeurIPS 2024正式论文：作者明确不发布原视频而发布预训练视觉特征，并用I3D/R(2+1)D/VideoMAEv2完成比较实验；论文第3.4节声明代码与数据CC BY-NC-SA 4.0用于学术非商业研究。
- 对`csmv-i3d-quarantine-v1.manifest.json`的8210个必需文件重算长度统计，发现531个`T>180`、最大1719，与README“max tensor length 180”存在协议差异。
- 将论文实验可行性、许可表述差异和序列处理预注册要求补入I3D审计报告与发现台账；未修改特征字节、split、标签、G2或任务20状态。

### 验证与证据

- 正式论文：NeurIPS 2024 Datasets and Benchmarks Track，方法使用预训练视觉特征，实验表含多种I3D baseline、VC-CSA I3D消融和I3D外测。
- 本地manifest统计：8210文件，`T=6—1719`，`T>180`为531，`T=180`为4；中位43、P90=133、P95=211、P99=339。
- 官方README说明24fps、16帧窗口/步长并声称最大tensor长度180；该现场差异已保留，不推定任一方错误。

### 影响与边界

从科学设计看，I3D足以支撑冻结视觉表征上的下游预测、融合、校准和消融；没有原始`.mp4`不阻塞这类实验。不得把结果表述为端到端视频表示学习、原始帧编码改进或音视频模型。正式实验前须冻结序列长度处理并做敏感性分析。

### 风险、问题与阻塞

- README与论文的许可表述不完全一致，特征再分发和最终G2仍须00/权利方确认。
- 531个长序列的处理若在test结果后选择，会构成分析自由度与复现风险。

### 下一步

将“full sequence+mask”与“确定性180步规则”形成预注册候选，由00在创建任务20前冻结；继续等待Issue #5对revision与资产身份的回复。

### Git状态

本记录和两份说明增量尚未提交、未推送；本轮未修改数据或启动训练。

## WR-20260716-001 — 裁定CSMV音频缺失的T-AFFC影响并回交00复审

- 时间：2026-07-16 00:07:14 +08:00
- 类型：REVIEW | DECISION | DOC | PROGRESS
- 任务/门：10-M1–M2 / 音频模态与G2边界
- 状态：部分完成（任务10证据闭合，等待00书面裁定）
- 负责人：Codex

### 背景与目标

用户询问CSMV仍缺音频是否影响向T-AFFC投稿；若不影响，则继续并将结果交00审核。需要区分期刊范围、科学可行性、任务10 G2条文和当前I3D资产准入阻塞，避免把“音频非必需”误写为“所有数据门已通过”。

### 实际变更

- 新增`TASK10_AUDIO_MODALITY_FEASIBILITY_REVIEW_REQUEST_20260716.md`，形成`PASS_WITH_LIMITATIONS_AUDIO_NOT_REQUIRED_FOR_PRIMARY_PROTOCOL`建议裁定及四项00复审请求。
- 更新`HANDOFF_10.md`和`G1_G2_EVIDENCE_MATRIX.md`，把音频登记为待00确认的非独立硬门，同时保留现有G2、`formal_split=false`和任务20禁令。
- 更新Data Card和Datasheet的结构性缺失边界：音频不得伪造/插补，不得声称音视频融合、音频增益或音频随机缺失鲁棒性；“完整模态”只指T0时合法、冻结且实际可得的全部模态。
- 未修改原始/派生数据、split、标签、特征字节、主指标或总纲，也未启动训练或创建任务20。

### 验证与证据

- T-AFFC General Call for Papers现场核验：范围包含视觉情感识别、群体情绪、预测模型、文本/语音分析和多模态识别，但未规定每篇论文必须含音频。
- CSMV官方README现场核验：当前发布I3D/VideoMAE视觉特征，音频标为未来补充；NeurIPS 2024正式论文以预训练视觉特征完成CSMV基线实验。
- 总纲v1.11核验：第4.5节要求原始音视频缺失不伪造，第5节优先官方VideoMAE特征，第11节禁止同时扩张音频等全部模块；任务10 G2条文未列音频退出条件。
- 文档一致性检索确认音频边界已进入交接、G门矩阵、Data Card和Datasheet。

### 影响与边界

音频不再建议作为独立的数据取得阻塞，可继续收敛I3D视觉特征协议。该建议不等于00已批准，也不降低当前I3D资产级许可、稳定revision与包身份/fixity要求。H3只评价实际模态缺失；音频实验必须标`NOT_APPLICABLE_AUDIO_UNAVAILABLE_BY_DATASET_DESIGN`。

### 风险、问题与阻塞

- 无音频会缩小模态覆盖，投稿时必须在方法和限制部分如实披露；审稿人可能质疑“多模态”措辞，需逐数据源列明真实输入。
- 当前G2仍由I3D资产准入裁定阻塞；任务10无权自行放行G2、正式split或任务20。

### 下一步

1. 将音频可行性裁定请求交00书面复审。
2. 若00接受，后续配置把音频固定为结构性不可用，E1/E5/H3按实际可得模态冻结。
3. 继续处理或等待I3D资产许可/revision/fixity裁定，不等待音频发布。

### Git状态

本轮新增审核请求并更新交接/G门/Data Card/Datasheet/工作日志；共享工作区仍有既有未提交变更，本轮未提交、未推送。

## WR-20260716-002 — 重建音频边界文档的release血缘并恢复M2发布验证

- 时间：2026-07-16 00:10:51 +08:00
- 类型：FIX | TEST | DOC
- 任务/门：10-M1–M2 / M2 release文档血缘
- 状态：完成
- 负责人：Codex

### 背景与目标

WR-20260716-001更新Data Card和Datasheet后，首次综合准备检查按设计在`m2_release.documentation`阻断，因为`dataset-v1.manifest.json`仍保存更新前的文档SHA-256。需要用现有确定性构建器重算文档血缘并重新执行公共核心隔离复现，不能删除检查或沿用旧PASS。

### 实际变更

- 执行`scripts/build_m2_release.py`，重算Data Card、Datasheet、隐私、平台条款、发布边界及release关联manifest的现场hash。
- 执行`scripts/reproduce_m2_minimal.py --public-core`，在`-I -S`隔离进程重新构建公共benchmark核心并更新`reproducibility-v1.manifest.json`。
- 未修改原始数据、I3D特征字节、标签定义、split算法、G2状态、`formal_split=false`或任务20禁令。

### 验证与证据

- 修复前`run_preparation_checks.py`：exit 1；唯一`blocking_checks=["m2_release"]`，细分为`documentation.passed=false`；工作日志、泄漏、复现、I3D预审等其余检查通过。该失败保留于本记录。
- `build_m2_release.py`：exit 0，`gate=PASS_WITH_LIMITATIONS`，状态`LOCAL_CANDIDATE_G1_PASS_G2_BLOCKED`。
- `reproduce_m2_minimal.py --public-core`：exit 0；19项before/after SHA-256一致，`mismatches=[]`，凭证环境未转发。
- `validate_m2_release.py`：exit 0；`documentation.passed=true`、`reproducibility.passed=true`、`steps_34_39_local_package_ready=true`；G1=`PASS`，G2仍为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`。

### 影响与边界

音频边界文档现在已进入release可追溯链，旧哈希不再冒充当前证据。该修复只恢复文档与manifest一致性，没有把“音频非必需建议”提升为00已批准，也没有改变正式模型准入。

### 风险、问题与阻塞

I3D资产级许可、稳定官方revision、包身份/fixity及00书面复审仍未闭合；`formal_model_work_ready=false`仍是预期状态。

### 下一步

完成最终综合检查后，将`TASK10_AUDIO_MODALITY_FEASIBILITY_REVIEW_REQUEST_20260716.md`及更新后的交接/G门证据发送00审核。

### Git状态

本轮release重建产物、审核文档和共享工作区既有变更尚未提交、未推送。

## WR-20260716-003 — 00裁定音频非G2硬门并冻结实际可得输入协议

- 时间：2026-07-16 00:24:11 +08:00
- 类型：REVIEW | DECISION | DOC | FIX | TEST
- 任务/门：00总控 / 任务10音频模态复审与G2边界
- 状态：完成（音频边界关闭；G2视觉资产准入仍阻塞）
- 负责人：Codex

### 背景与目标

任务10提交`TASK10_AUDIO_MODALITY_FEASIBILITY_REVIEW_REQUEST_20260716.md`，请求00裁定CSMV当前无音频是否影响T-AFFC可发表性、G2和任务20启动。需要独立复核期刊范围、固定上游资产说明、现有总纲和数据协议，并防止把“音频非硬门”误写成“完整多模态/缺失模态证据已成立”。

### 实际变更

- 新增`TASK00_AUDIO_MODALITY_PROTOCOL_REVIEW_20260716.md`，签署`REVIEW-00-AUDIO-MODALITY-PROTOCOL-20260716`：音频=`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`，移出G2、任务20启动和后续取得关键路径。
- 总纲升为v1.12，CSMV主协议改为单一准入视觉特征族+评论特权监督；E1使用`ALL_AVAILABLE_INPUTS`，E5/H3只对同一样本至少两个实际T0输入模态的协议生效。
- 新增`experiment-protocol-v2.md`并把`experiment-protocol-v1.md`保留为`SUPERSEDED_BY_EXPERIMENT_PROTOCOL_V2`，没有覆盖历史冻结版；同步任务树规格、研究协议审计和贡献先验矩阵。
- 同步`HANDOFF_10.md`、`G1_G2_EVIDENCE_MATRIX.md`、Data Card、Datasheet、M2协议、决策日志、计划/发现/进度文件与综合准备必需文件清单。
- 将bootstrap配置升级为schema 2、总纲v1.12/实验协议v2，显式声明音频结构性不可得、单一实际输入和缺失模态实验不适用；验证器新增对应fail-closed检查。
- 重建M2 release文档血缘和19项公共核心隔离复现manifest；未修改原始数据、标签、split算法、I3D字节、G2或任务20状态。

### 验证与证据

- 官方证据复核：T-AFFC General CFP将视觉、语音、多模态和群体情绪列为并列范围；CSMV固定commit `99d14240254b1381dde0b9c56add140381f65117` README明确当前发布视觉特征、I3D/VideoMAE已发布、音频未来补充；NeurIPS 2024正式入口确认8210视频/107267评论与视频内容基线。
- `validate_experiment_config.py --config configs/experiment.bootstrap.yaml`：`CONFIG_VALID`；`compileall` exit 0。
- 协议文档更新后的首次`run_preparation_checks.py`按设计exit 1，唯一`blocking_checks=["m2_release"]`，原因是5份release文档hash已变化；失败保留，未弱化检查。
- `build_m2_release.py` exit 0，`gate=PASS_WITH_LIMITATIONS`、dataset状态=`LOCAL_CANDIDATE_G1_PASS_G2_BLOCKED`。
- `reproduce_m2_minimal.py --public-core` exit 0：Python `-I -S`、19项before/after一致、`mismatches=[]`、两条隔离命令returncode均0。
- `validate_m2_release.py` exit 0：documentation/reproducibility均通过，G1=`PASS`，G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`，`steps_34_39_local_package_ready=true`。
- `git diff --check` exit 0；仅输出既有Windows换行转换警告，无空白错误。

### 影响与边界

音频不再等待、下载、协调许可、分配存储或阻塞G2；论文仍必须披露其结构性不可得。允许研究冻结视觉表示上的群体情绪分布预测、评论特权监督、检索、校准、OOD与拒绝；禁止音视频融合、音频增益、音频随机缺失鲁棒性、伪音频和端到端原始音视频编码主张。无合格多输入协议时H3必须`NOT_APPLICABLE`，不是失败也不是通过。

### 风险、问题与阻塞

I3D本地包的文件树、schema、逐文件fixity和8210覆盖已闭合，但资产级许可、稳定官方revision与权利方包身份/fixity attestation仍未闭合。G2继续fail-closed，全局`formal_split=false`，正式模型工作与任务20继续禁止。期刊范围支持无音频投稿不等于录用保证。

### 下一步

1. 继续等待/闭合Issue #5对应的I3D资产许可、稳定revision与包身份/fixity，并提交00单独准入复审。
2. G2通过前不创建任务20；后续实验配置必须继承experiment protocol v2的实际可得输入合同。

### Git状态

本次裁定、协议v2、台账同步、验证器修改和release重建均在共享工作区尚未提交、未推送；未把既有其他任务变更归为本次独占修改。

## WR-20260716-004 — 冻结I3D序列协议并收紧论文输入主张

- 时间：2026-07-16 00:58:29 +08:00
- 类型：FEATURE | TEST | DECISION | DOC | PROGRESS
- 任务/门：10-M1—M2 / I3D序列预注册、M2复现与G2边界
- 状态：完成（协议与本地复现）；外部资产证明延期
- 负责人：Codex

### 背景与目标

CSMV官方README描述最大tensor长度180，但8,210个必需I3D文件中531个`T>180`、最大1,719。为防止查看test结果后选择序列规则，需要在不训练、不建索引、不读取test标签的前提下冻结主协议和敏感性协议，并把论文主张限定到实际可得的冻结视觉表征。

### 实际变更

- 新增`CSMV_I3D_SEQUENCE_PROTOCOL_V1.md`、`configs/csmv-i3d-sequence-protocol-v1.json`及机器manifest；主协议=`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`，主敏感性=`UNIFORM_180_ENDPOINT_INCLUSIVE`，前180只作补充。
- 新增确定性实现、manifest构建器、专项validator与8项unittest；完整序列保留、右padding、`True=observed` mask、固定长度桶、64 MiB原始输入张量门及坏输入拒绝均已落码。
- 更新实验协议v2、bootstrap配置/validator、Data Card、Datasheet、数据字典、M2协议、发布边界、claim矩阵、研究冻结审计、数据源台账、G1/G2矩阵与`HANDOFF_10.md`。
- 发布构建器和release/preparation validator纳入I3D序列协议lineage；dataset manifest新增协议引用。
- 新增`TASK10_I3D_SEQUENCE_PROTOCOL_AND_GIT_CHECKPOINT_HANDOFF_20260716.md`作为00回交入口。
- 维护者许可/revision/包身份/fixity按用户指令标`DEFERRED_PENDING_MAINTAINER_REPLY`；本轮未访问或催促Issue。

### 验证与证据

- TDD首轮：`.\.venv\Scripts\python.exe -m unittest tests.test_csmv_i3d_sequence_protocol -v` exit 1，`ModuleNotFoundError`符合实现前红灯预期；失败保留。
- 实现后同命令：8/8通过，exit 0。
- `build_csmv_i3d_sequence_protocol_manifest.py` exit 0：8,210样本、531个`T>180`；manifest SHA-256=`a583f754eaf7dc230fa9967e671e98ddd838472abedef1419f1bf80cc29f9086`。
- `validate_csmv_i3d_sequence_protocol.py` exit 0：状态`PASS_PREREGISTRATION_ONLY_G2_UNCHANGED`；长度、fixity、重复hash、正向/边界和8类负面检查通过。
- `validate_experiment_config.py --config configs\experiment.bootstrap.yaml`输出`CONFIG_VALID`。
- 首次`reproduce_m2_minimal.py --public-core`按预期exit 1：新协议lineage使`dataset-v1.manifest.json`单项漂移；未删门或改断言。确定性构建后重跑19项漂移0、exit 0。
- `validate_m2_release.py`、`validate_m2_data_engineering.py`及泄漏`--no-write`均exit 0；Critical=0。
- 误用不存在的`--selftest-negative`导致argparse exit 2；随后用真实接口`--selftest`重跑，输出预期`LEAKAGE_BLOCKED`且exit 0。失败记录保留。

### 影响与边界

未来只有在G2和任务20获准后，才能按同一配置使用I3D；本轮没有训练、拟合、索引或正式split。论文只允许声称“冻结I3D视觉表征上的公众诱发受众情绪分布预测”，不得声称端到端视频、原始帧、音视频融合、音频增益或评论文本T0输入。E1/E5/H3继续按实际单输入资格和既定`NOT_APPLICABLE`状态执行。

### 风险、问题与阻塞

序列处理与本地复现缺口已经闭合，但资产级许可、稳定官方revision及权利方包身份/fixity仍未闭合。维护者延期不是解决；G2保持`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`，`formal_split=false`。

### 下一步

1. 完成综合准备、compileall、diff和敏感文件/大包Git审计。
2. 建立M1—M2阶段Git提交并推送；随后更新回交与工作日志中的真实commit/push状态。
3. 将最终证据发给00复审；不请求仅因协议通过而放行G2。

### Git状态

本轮变更与此前M1—M2/00裁定仍在共享`main`工作区，当前尚未提交、未推送；不得解释为已同步。

## WR-20260716-005 — 修复延期状态验证合同并完成提交前安全审计

- 时间：2026-07-16 01:08:00 +08:00
- 类型：FIX | TEST | SECURITY | PROGRESS
- 任务/门：10-M1—M2 / 综合准备与Git检查点
- 状态：完成（提交前门）
- 负责人：Codex

### 背景与目标

I3D维护者状态从“等待”收紧为用户明确要求的`DEFERRED_PENDING_MAINTAINER_REPLY`后，综合准备门仍固定寻找旧台账token。需要保留首次失败，更新validator为新且更严格的状态合同，并检查待提交范围不含密钥、Cookie、数据大包或本机敏感路径。

### 实际变更

- 首次`run_preparation_checks.py`失败保留：唯一阻塞为`m1_public_audit`，原因是`validate_m1_public_audit.py`仍要求旧状态`I3D_QUARANTINE_8210_COVERAGE_LICENSE_REVISION_PENDING`。
- 将validator改为必须同时出现`I3D_QUARANTINE_8210_COVERAGE_EXTERNAL_ATTESTATION_DEFERRED`、`DEFERRED_PENDING_MAINTAINER_REPLY`和新序列manifest定位；没有接受旧值或增加容差。
- 从数据源台账移除包含人名的本机CUC绝对路径，改为`CUC_IGPE_ROOT`配置；HANDOFF/progress中的I3D源目录改为非绝对描述。历史`WORK_LOG.md`按追加不可改规则保留早期非敏感`D:\soft`事实记录。
- 审计107个待提交候选文件、Git忽略策略、tracked扩展名与文件体量。

### 验证与证据

- `validate_m1_public_audit.py`：exit 0，`errors=[]`。
- 修复后`run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`m1_read_only_work_ready=true`；`formal_model_work_ready=false`仅因faiss/G2阶段边界，未误报就绪。
- `validate_work_log.py`在本记录前：55条、错误0、latest=`WR-20260716-004`；本记录后将再次验证。
- `python -m compileall -q scripts tests`：exit 0。
- `git diff --check`：exit 0；只有Windows行尾转换warning，无空白错误。
- 候选安全扫描：107文件，敏感绝对路径命中0、密钥模式命中0、tracked坏资产扩展0、未忽略的大包/媒体扩展0、超过10 MiB候选文件0。
- Git远端为`https://github.com/xjq801/MMSA-CH-SIMS.git`；`origin/main...HEAD=0/0`，提交前无远端分叉。

### 影响与边界

综合准备门现在精确匹配用户批准的延期状态，但仍要求G2 blocked和资产外部证明未闭合；没有删除门或把延期当PASS。安全审计只覆盖本次候选提交，不修改原始/processed数据或I3D字节。

### 风险、问题与阻塞

G2外部阻塞仍在；`formal_split=false`。共享工作区包含此前任务10与00的同范围未提交文件，本次检查点将按授权整体纳入，不能把它们误写为当前单一功能独占变更。

### 下一步

1. 再次运行工作日志与综合准备门。
2. 审查stage清单后创建并推送M1—M2阶段提交。
3. 用实际commit/push结果追加记录并更新00回交。

### Git状态

当前`main`与`origin/main`提交层面0/0分叉；107个候选文件仍未stage、未提交、未推送。

## WR-20260716-006 — 更正序列工件hash并闭合staged diff检查

- 时间：2026-07-16 01:15:00 +08:00
- 类型：FIX | TEST | SECURITY
- 任务/门：10-M1—M2 / Git阶段检查点
- 状态：完成（stage复核）
- 负责人：Codex

### 背景与目标

107个候选文件stage后，`git diff --cached --check`识别3个“EOF多余空行”错误。需要保留失败，做不改变语义的最小修复，并重建受代码fixity影响的I3D协议manifest。

### 实际变更

- 删除`lai-gai-osf-metadata-audit-v1.manifest.json`、`csmv_i3d_sequence_protocol.py`和`validate_lai_gai_osf_metadata_audit.py`末尾多余空行；未改协议或审计语义。
- 因I3D协议实现字节变化，重新运行确定性manifest构建器并更新00回交表。
- 更正WR-20260716-004中的预修复hash：最终序列实现SHA-256=`0ecb92fff40f00492283ced2d85917ef746cbd9628013d2bf5c67199ac463017`；最终协议manifest SHA-256=`208615d4059afc8c5c2c57a5ffc13eeafa9a71ece861332d9f1cd62bc9c4d5be`。历史记录不覆盖，以本条为准。

### 验证与证据

- 首次`git diff --cached --check` exit 1，准确报告3个EOF空行；失败保留。
- `build_csmv_i3d_sequence_protocol_manifest.py`重建exit 0。
- `validate_csmv_i3d_sequence_protocol.py`重跑exit 0，状态仍为`PASS_PREREGISTRATION_ONLY_G2_UNCHANGED`。
- 再次`git diff --cached --check` exit 0，仅有行尾转换warning。
- staged范围107个文件，坏资产扩展0、超过10 MiB单文件0；`.npy`、raw/processed数据和媒体未stage。

### 影响与边界

只修复文本格式与相应fixity，不改变主/敏感性规则、数据、split或G门。回交材料使用更正后的最终hash。

### 风险、问题与阻塞

无新增工程阻塞。外部资产证明与G2状态不变。

### 下一步

1. 将本条和更正后的回交材料stage。
2. 创建注明G1 PASS/G2 blocked/`formal_split=false`/未创建任务20的阶段提交并push。
3. 用真实commit/push状态追加最终记录。

### Git状态

候选已stage但尚未提交、未推送；不得写成已同步。

## WR-20260716-007 — 重建序列manifest下游release引用

- 时间：2026-07-16 01:20:00 +08:00
- 类型：FIX | TEST
- 任务/门：10-M1—M2 / release lineage
- 状态：完成
- 负责人：Codex

### 背景与目标

EOF格式修复改变I3D序列实现及其协议manifest hash。提交前综合准备按设计失败，准确指出`dataset-v1`仍引用旧协议manifest hash；需要用现有确定性release构建器刷新下游引用，不能绕过lineage门。

### 实际变更

- 保留`run_preparation_checks.py`的`blocking_checks=["m2_release"]`失败；具体为`manifest_lineage.passed=false`。
- 运行`build_m2_release.py`重建dataset引用，并再次执行19项公共核心隔离重放刷新现场hash。

### 验证与证据

- `build_m2_release.py` exit 0，`gate=PASS_WITH_LIMITATIONS`。
- `reproduce_m2_minimal.py --public-core` exit 0：19项`mismatches=[]`。
- `validate_m2_release.py` exit 0：8项manifest引用闭合，G1=`PASS`、G2仍blocked、`formal_split=false`。

### 影响与边界

仅刷新协议manifest到dataset/reproducibility的hash血缘；数据、标签、split和协议语义不变。

### 风险、问题与阻塞

无新增工程阻塞；外部资产证明延期和G2阻塞不变。

### 下一步

重新运行工作日志、综合准备和cached diff门后提交。

### Git状态

刷新后的release文件尚未重新stage、未提交、未推送。

## WR-20260716-008 — 创建并推送M1—M2阶段检查点

- 时间：2026-07-16 01:27:00 +08:00
- 类型：PROGRESS | TEST | SECURITY | DOC
- 任务/门：10-M1—M2 / Git阶段检查点与00回交
- 状态：完成
- 负责人：Codex

### 背景与目标

在协议、release、复现、工作日志和安全门全部闭合后，需要为此前共享工作区中的M1—M2与00裁定建立可追溯Git检查点，并推送到用户既有GitHub仓库。提交说明必须诚实保留G2与任务20边界。

### 实际变更

- stage并复核107个同范围文件，包含此前M1—M2数据/第二主集/CSMV lineage/00裁定和本轮I3D序列协议；未覆盖或丢弃共享工作区改动。
- 创建内容commit `f885a59`，标题`M1-M2 checkpoint: freeze I3D protocol`；正文明确G1 PASS、G2 blocked、`formal_split=false`、task20未创建。
- fetch后确认远端无新提交，成功推送`main`到用户仓库。
- 更新`TASK10_I3D_SEQUENCE_PROTOCOL_AND_GIT_CHECKPOINT_HANDOFF_20260716.md`与阶段计划，记录真实同步状态。

### 验证与证据

- 提交前`validate_work_log.py`：58条、错误0、latest=`WR-20260716-007`。
- 提交前`run_preparation_checks.py`：exit 0、`blocking_checks=[]`、`m1_read_only_work_ready=true`；formal模型仍因阶段/G2边界为false。
- 提交前`git diff --cached --check`：exit 0。
- `git commit`：exit 0，107 files changed、172,038 insertions、276 deletions。
- `git fetch origin`后`git rev-list --left-right --count origin/main...HEAD`=`0 1`。
- `git push origin main`：exit 0，`26229c0..f885a59 main -> main`。

### 影响与边界

GitHub现具有M1—M2可复现检查点；提交不包含I3D `.npy`、raw/processed数据、模型、索引、密钥、Cookie或敏感绝对路径。推送成功不改变科学门状态，也不授权任务20。

### 风险、问题与阻塞

维护者外部证明仍为`DEFERRED_PENDING_MAINTAINER_REPLY`；G2阻塞未解决。faiss未安装不是本轮失败，因为正式模型工作尚未放行。

### 下一步

1. 提交并推送本条真实同步记录及00回交更新。
2. 将最终tip与验证摘要发送00复审。
3. 停止任务10新增工作，等待00裁定；不创建任务20。

### Git状态

内容检查点`f885a59`已推送至`origin/main`。本条日志与回交状态更新尚待一个小型收尾commit；未在本条提前声称其已推送。

## WR-20260716-009 — 00接受I3D序列协议与M1—M2 Git检查点

- 时间：2026-07-16 02:20:00 +08:00
- 类型：DECISION | REVIEW | TEST | SECURITY | DOC
- 任务/门：00-总控 / I3D序列协议与任务10阶段回交
- 状态：完成
- 负责人：Codex

### 背景与目标

任务10提交I3D序列协议、论文边界、复现和Git检查点，请求00独立复审。用户此前要求只做可能影响论文发表的工作，并把维护者未回复事项暂时跳过，因此本轮只裁定序列处理的可发表性/可复现性，不检查或催促Issue #5。

### 实际变更

- 新增`TASK00_CSMV_I3D_SEQUENCE_PROTOCOL_AND_GIT_CHECKPOINT_REVIEW_20260716.md`，签署`REVIEW-00-CSMV-I3D-SEQUENCE-PROTOCOL-20260716`。
- 接受`FULL_SEQUENCE_DYNAMIC_PADDING_MASK`主协议、`UNIFORM_180_ENDPOINT_INCLUSIVE`主敏感性和`FIRST_180_ONLY_FIXED_DIAGNOSTIC`补充规则，关闭`I3D_SEQUENCE_PROCESSING_PROTOCOL_UNFROZEN`子缺口。
- 总纲升级为v1.13，并同步`DECISION_LOG.md`、`G1_G2_EVIDENCE_MATRIX.md`、`HANDOFF_10.md`、计划/进度/发现和综合准备必需文件列表。
- 保留资产级许可、稳定官方revision、权利方包身份和fixity阻塞；维护者证据继续延期。

### 验证与证据

- 协议manifest及6个证据文件SHA-256现场闭合；manifest SHA-256=`208615d4059afc8c5c2c57a5ffc13eeafa9a71ece861332d9f1cd62bc9c4d5be`。
- `python -m unittest tests.test_csmv_i3d_sequence_protocol -v`：8/8 PASS。
- 协议manifest重建及专项validator：exit 0，`PASS_PREREGISTRATION_ONLY_G2_UNCHANGED`，8个负例PASS。
- `run_m2_leakage_tests.py --no-write`：exit 0、Critical=0；`--selftest`：exit 0并输出预期`LEAKAGE_BLOCKED`。
- `reproduce_m2_minimal.py --public-core`：exit 0，Python 3.8.9 `-I -S`，19项`mismatches=[]`。
- 修改后`validate_m2_release.py`、`run_preparation_checks.py`、`python -m compileall -q scripts`和`git diff --check`均exit 0；综合准备`blocking_checks=[]`，`formal_model_work_ready=false`。
- 审核开始时`HEAD=origin/main=cf6dea18ddb057da91e90d6c0104e3e854f1724a`、`origin/main...HEAD=0/0`、工作区干净；安全枚举262个tracked文件，`.npy`、特征包和超过10 MiB文件均为0。

### 影响与边界

序列处理规则已获得00预注册信用，后续不得根据test结果选择或升级协议。论文只允许声称冻结I3D视觉表征上的受众情绪分布预测，不得声称端到端原始帧、音视频融合、音频增益或评论T0输入。

### 风险、问题与阻塞

- 第一次tracked大文件枚举因Git对非ASCII路径的引号转义导致PowerShell `Test-Path`报错；以`git -c core.quotepath=false ls-files`重跑后成功，失败没有删除。
- 首次整合补丁因`progress.md`预期上下文不匹配而整体拒绝、未部分应用；拆分补丁并读取真实文件尾部后完成。
- G2仍为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；`formal_split=false`；任务20未创建。

### 下一步

1. 运行工作日志与综合门最终复核。
2. 建立并推送00复审小型提交，固定v1.13裁定。
3. 停止维护者等待类工作；仅在收到实质回复或等价证据后复审剩余资产门。

### Git状态

00复审改动尚未提交、未推送；不得写成已同步。

## WR-20260716-010 — 推送00序列协议复审并更正记录时间

- 时间：2026-07-16 01:25:26 +08:00
- 类型：PROGRESS | FIX | DOC
- 任务/门：00-总控 / 复审Git收尾
- 状态：完成
- 负责人：Codex

### 背景与目标

WR-20260716-009完成时把人工填写时间误写为`02:20:00 +08:00`，晚于工作站现场时间；依据只追加政策不改写历史记录，需要在本条明确更正，并记录已经实际发生的提交与推送。

### 实际变更

- 保留WR-20260716-009原文，在本条将其真实记录时点更正为本条现场时间附近；该笔误不影响文件、验证结果或门裁定。
- 创建00复审commit `56205f2ab3075716c8269f8331e7b0b6a6a63759`，标题`Review I3D sequence protocol checkpoint`。
- fetch确认远端无新提交后，将`main`推送到用户GitHub仓库。

### 验证与证据

- 提交前`git diff --cached --check`：exit 0。
- `git commit`：exit 0，10 files changed、163 insertions、9 deletions。
- `git fetch origin`后`origin/main...HEAD=0/1`。
- `git push origin main`：exit 0，`cf6dea1..56205f2 main -> main`。
- 推送后`HEAD=56205f2ab3075716c8269f8331e7b0b6a6a63759`，`origin/main...HEAD=0/0`，工作区干净。

### 影响与边界

GitHub已固定00复审与总纲v1.13。推送不改变科学门：G1=`PASS`；G2 blocked；`formal_split=false`；任务20未创建。

### 风险、问题与阻塞

WR-20260716-009时间是记录笔误，已用只追加方式纠正。资产许可、稳定官方revision、包身份和权利方fixity仍待外部实质证据。

### 下一步

运行最终日志/综合门，提交并推送本条收尾记录后停止本轮工作。

### Git状态

00复审commit `56205f2`已推送；本条收尾记录尚未提交、未推送。

## WR-20260716-011 — IJCV—T-AFFC条件双论文路线与总纲v1.14

- 时间：2026-07-16 12:08:31 +08:00
- 类型：RESEARCH | DECISION | PLAN | DOC | TEST
- 任务/门：00-总控 / IJCV专刊适配与双论文范围变更
- 状态：完成待Git同步
- 负责人：Codex

### 背景与目标

用户提供IJCV专刊“Social, Emotional, and Cognitive Visual Intelligence”三张征稿截图，要求判断与当前群体情绪预测方向的适配性；若可行，则设计兼顾T-AFFC与IJCV的研究微调方案并写入总纲。当前CARM以冻结I3D、评论特权监督和受众反应记忆为主，需判断其是否达到IJCV计算机视觉方法门，并避免同稿双投。

### 实际变更

- 核验Springer/IJCV官方专刊页、期刊范围/文章类型和投稿指南：确认专刊开放、官方截止2026-12-15，范围直接覆盖主观视觉理解、情感、不确定性、观察者差异及跨域泛化；同稿不得同时在其他地方审议。
- 核验PC Loss（CVPR 2021）、SAMNet（2022）和MFRN（AAAI 2025）等直接近邻，确认“分布预测 + 主观性/affective memory + 普通特征精炼”已有前作，冻结I3D+CARM不能原样作为IJCV视觉方法创新。
- 新增`IJCV_TAFFC_DUAL_TRACK_FEASIBILITY_AND_PLAN_20260716.md`，裁定`SC-20260716-02 / CONDITIONAL_GO_TWO_DISTINCT_PAPERS`，冻结两稿独立问题、方法、数据、主结果、共享/不可共享边界和投稿披露要求。
- 将`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md`升级为v1.14，新增第0.6节与第18节：IJCV最小方法核、J0/J1/J2、JH1—JH3、J0—J9、公平基线、双线日历、十项投稿Go标准及条件任务25/65。
- IJCV路线不等待CSMV维护者回复：LAI-GAI之外须在2026-08-12前再冻结至少一个像素级人工情绪分布集；CSMV只在G2通过后作可选视频外验。T-AFFC的G2、`formal_split=false`和任务20禁令未放宽。
- 更新`DECISION_LOG.md`、`RISK_REGISTER.md`、`CLAIM_EVIDENCE_MATRIX.md`、`HANDOFF_10.md`、`task_plan.md`、`findings.md`和`progress.md`，将新颖性、第二像素集、固定截稿与重复投稿列为显式风险/claim边界。

### 验证与证据

- 改动后首次`validate_work_log.py`：exit 0，61条、`errors=[]`、latest=`WR-20260716-010`；本条追加后须最终重跑。
- 改动后首次`run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`m1_read_only_work_ready=true`；`formal_model_work_ready=false`，原因仍为正式CARM环境/CSMV G2阶段边界。
- 同批`git diff --check`：exit 0。
- 本条追加后最终`validate_work_log.py`：exit 0，62条、`errors=[]`、latest=`WR-20260716-011`。
- 本条追加后最终`run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`m1_read_only_work_ready=true`、`formal_model_work_ready=false`；G1=`PASS`、G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`。
- 最终同批`git diff --check`与`git status --short --branch`：exit 0；仅列出本条所述文档与总纲变更，未出现数据、模型或密钥。
- 官方依据与近邻链接已写入总纲第16节及双路线方案；截图中的2027年首轮/修回/最终通知/出版时间未获本轮官方正文核实，保持`UNVERIFIED_SECONDARY_SOURCE_ONLY`。

### 影响与边界

研究方向从单篇T-AFFC规划升级为一个共享科学基础上的两篇实质独立论文。IJCV主问题是响应分布几何驱动的视觉表征，不包含评论teacher、CARM memory/router；T-AFFC继续验证H1/H2。条件任务25/65本轮只进入总纲，未创建、未训练、未查看test、未改变任何数据split。

### 风险、问题与阻塞

- `rg`在本机仍因Access denied失败，改用PowerShell `Select-String`完成只读检索；失败未影响文件。
- 首次向`findings.md`追加近邻结论时因预期标题与实际标题不一致被`apply_patch`拒绝，读取UTF-8文件尾后重试成功；没有部分写入。
- IJCV当前仍为条件路线：第二像素人工集尚未冻结，PC/SAMNet/MFRN尚未正式复现，JH1—JH3均为`TO_VERIFY`。
- CSMV G2仍为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；`formal_split=false`；任务20未创建。维护者未回复事项继续按用户要求延期。

### 下一步

1. 最终重跑工作日志、综合准备和diff检查。
2. 审查变更范围，提交并推送总纲v1.14到`origin/main`。
3. 后续先执行J0：在2026-08-12前审计并冻结第二个像素级人工分布集及IJCV近邻/预注册；J0未过不创建任务25。

### Git状态

本批v1.14与双路线方案尚未提交、未推送；不得写成已同步。当前科学门与模型工作状态未改变。

## WR-20260716-012 — 推送总纲v1.14与IJCV双路线方案

- 时间：2026-07-16 12:12:29 +08:00
- 类型：PROGRESS | GIT | DOC
- 任务/门：00-总控 / IJCV双路线Git收尾
- 状态：完成
- 负责人：Codex

### 背景与目标

WR-20260716-011已完成总纲v1.14、独立双路线方案和所有台账更新。本条只记录已经实际发生的提交、直连失败和代理重试推送，不改变研究裁定。

### 实际变更

- 创建内容commit `d817357`，标题`Plan distinct IJCV and T-AFFC paper tracks`。
- 首次直连GitHub推送因连接重置/443连接失败而未写入远端；按已批准的本机代理传输政策重试后成功。
- 推送后fetch并确认`origin/main...HEAD=0/0`；工作区在本条追加前干净。

### 验证与证据

- 提交前`git diff --cached --check`：exit 0。
- 内容commit：10 files changed、467 insertions、22 deletions，新增双路线方案文件。
- 首次直连`git push`：exit 1，远端仍落后1个commit；失败未被删除或写成成功。
- 代理重试`git push origin main`：exit 0，`c0664c3..d817357 main -> main`。
- 推送后`git rev-list --left-right --count origin/main...HEAD`=`0 0`。

### 影响与边界

GitHub已固定总纲v1.14与IJCV—T-AFFC两稿分界。同步不改变G1/G2、`formal_split=false`或任何任务启动门，也未创建任务25/65。

### 风险、问题与阻塞

直连GitHub本轮不稳定，已使用既有代理政策恢复；未向日志写入代理端点或凭证。IJCV第二像素人工集、方法复现和J0仍未完成。

### 下一步

先执行J0数据/新颖性门；在2026-08-12前冻结第二像素人工集、近邻差异矩阵和IJCV预注册。J0未通过不得创建任务25。

### Git状态

内容commit `d817357`已推送。本条真实同步记录仍需一个小型收尾commit与推送。

## WR-20260716-013 — 迁出IJCV方向并恢复T-AFFC单路线总纲

- 时间：2026-07-16 13:05:00 +08:00
- 类型：DECISION | DOC | SCOPE
- 任务/门：00-总控 / 项目职责分离
- 状态：完成
- 负责人：Codex

### 背景与目标

用户明确要求当前项目继续完成原定T-AFFC路线，并先把完整总纲交给新建的IJCV方向项目。执行前已确认独立IJCV项目保有未删减v1.14、上下文交接、独立分支和启动任务，因此本批次只调整当前项目的活动SSOT与相关台账，不删除历史决策。

### 实际变更

- 将`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md`升级为v1.15，首要目标恢复为2027-05-12前完成T-AFFC CARM论文、代码、数据说明和证据链。
- 从当前活动总纲移除第18节IJCV执行合同、J0—J2、JH1—JH3、任务25/65、IJCV日历、投稿门和活动参考链接；保留`SC-20260716-02`作为历史决策，并新增`SC-20260716-03`迁出裁定。
- 更新`HANDOFF_10.md`与`AGENTS.md`，明确任务10及本项目后续任务只执行T-AFFC第17节任务树。
- 将`IJCV_TAFFC_DUAL_TRACK_FEASIBILITY_AND_PLAN_20260716.md`标记为当前项目只读归档；更新`CLAIM_EVIDENCE_MATRIX.md`、`DECISION_LOG.md`和`RISK_REGISTER.md`，把J-claims和IJCV数据/方法/日程风险迁至独立项目，同时保留跨项目重复发表控制。
- 更新`task_plan.md`与`progress.md`，记录项目职责分离完成。

### 验证与证据

- 独立项目检查：`git -C "D:\MMSA-CH-SIMS - IJCV方向" status --short --branch`显示`codex/ijcv-j0...origin/codex/ijcv-j0`且无修改；最新提交为`c64c954 Record IJCV J0 task creation`。
- 独立项目文件检查：未删减`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md`仍为v1.14且包含第18节；`IJCV_PROJECT_CONTEXT_HANDOFF_20260716.md`存在。
- `git diff --check`：exit 0。
- `.\.venv\Scripts\python.exe scripts\validate_work_log.py`：exit 0，修改前日志63条、`errors=[]`。
- `.\.venv\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`m1_read_only_work_ready=true`、`formal_model_work_ready=false`。
- 搜索活动SSOT与台账：IJCV相关命中仅为迁出说明、历史决策和归档claim/risk，不存在活动第18节或任务25/65启动规格。

### 影响与边界

当前项目唯一活动路线为T-AFFC CARM。该范围分离不改变任何科学门：G1=`PASS`；G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；`formal_split=false`；任务20未创建。独立IJCV项目可读取v1.14和交接材料，但不得反向覆盖本项目v1.15。

### 风险、问题与阻塞

CSMV I3D资产级许可、稳定revision和权利方身份/fixity证明仍等待外部证据；按用户要求暂不因维护者未回复而扩展工作。跨项目共享仍需通过已提交Git状态和书面交接，避免并发修改实验核心及未来重复发表。

### 下一步

提交并推送当前项目v1.15职责分离检查点。之后继续按T-AFFC总纲处理任务10的G2资产阻塞；G2正式通过前不创建任务20。

### Git状态

本条记录追加时改动尚未提交或推送，不写成已同步。

## WR-20260716-014 — 推送T-AFFC单路线v1.15检查点

- 时间：2026-07-16 13:10:00 +08:00
- 类型：GIT | PROGRESS
- 任务/门：00-总控 / 项目职责分离Git收尾
- 状态：完成
- 负责人：Codex

### 背景与目标

WR-20260716-013已完成IJCV迁出与T-AFFC单路线v1.15的文件、台账和验证。本条只记录已经实际发生的内容提交与GitHub同步，不改变研究范围或科学门。

### 实际变更

- 创建内容commit `db89c99`，标题`Refocus master plan on T-AFFC track`。
- 将当前`main`推送到`origin/main`，远端由`0d779d6`前进至`db89c99`。

### 验证与证据

- 提交前`git diff --cached --check`：exit 0。
- 内容commit：10 files changed、100 insertions、146 deletions。
- `git push origin main`：exit 0，输出`0d779d6..db89c99 main -> main`。

### 影响与边界

GitHub上的当前项目已固定T-AFFC-only总纲v1.15。独立IJCV项目仍保持`codex/ijcv-j0@c64c954`，未被本次推送修改。G1/G2、`formal_split=false`和任务20禁令均未变化。

### 风险、问题与阻塞

无新增Git同步阻塞。唯一论文关键外部阻塞仍为CSMV I3D资产许可、revision及权利方身份/fixity证明。

### 下一步

完成本条日志的收尾提交和推送；之后当前项目只按T-AFFC总纲v1.15推进。

### Git状态

内容commit `db89c99`已推送；本条日志本身尚未提交或推送。

## WR-20260717-001 — 复核忽略I3D资产准入后的G2条件

- 时间：2026-07-17 11:21:38 +08:00
- 类型：TEST | DECISION | DATA
- 任务/门：00-总控 / G2反事实复审
- 状态：完成
- 负责人：Codex

### 背景与目标

用户要求暂时忽略CSMV I3D资产准入，检查是否能够通过G2。本批次只做反事实门审计：检查排除资产级许可、稳定官方revision和权利方身份/fixity证明后是否仍有其他G2阻塞；不自动修改总纲、机器状态或任务20启动门。

### 实际变更

- 新建`TASK00_G2_NON_ASSET_COUNTERFACTUAL_REVIEW_20260717.md`，逐项记录非资产G2条件、现场命令、限制和正式门边界。
- 更新`G1_G2_EVIDENCE_MATRIX.md`，登记`PASS_NON_ASSET_G2_REQUIREMENTS_WITH_LIMITATIONS`反事实裁定，同时保持正式G2 blocked。
- 未修改任何原始数据、标签、split算法、I3D字节、dataset/split manifest门状态或训练代码。

### 验证与证据

- `validate_m2_data_engineering.py`：exit 0；8210记录、107267人工响应、8008源族、金标/银标隔离及第二主集映射通过。
- `run_m2_leakage_tests.py --no-write`：exit 0；Critical=0、`PASS_WITH_LIMITATIONS`；`--selftest`：exit 0并正确输出`LEAKAGE_BLOCKED`。
- `reproduce_m2_minimal.py --public-core`：exit 0；Python 3.8.9、`-I -S`、19项before/after一致、`mismatches=[]`。
- `validate_m2_release.py`、`validate_csmv_i3d_sequence_protocol.py`、`validate_lai_gai_second_primary.py`均exit 0。
- `run_preparation_checks.py`：exit 0；`blocking_checks=[]`、`m1_read_only_work_ready=true`、`formal_model_work_ready=false`。

### 影响与边界

排除资产准入后，没有发现第二个非资产G2阻塞，故反事实结论为非资产条件通过。正式G2不能仅凭“忽略”改为PASS：现行总纲和机器合同仍要求许可/官方身份闭合，故`G2=BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`、`formal_split=false`、`formal_model_use_allowed=false`，任务20未创建。

### 风险、问题与阻塞

I3D资产级研究许可、稳定官方revision和权利方包身份/fixity证明仍未知。若未来通过范围变更接受风险，可能影响论文审稿、实验复现、代码/特征发布和后续数据合规；不得把接受风险写成权利方确认。

### 下一步

等待用户决定是否正式修改总纲，把G2拆分为协议/数据通过与资产风险延期接受；在此之前维持现有门状态。

### Git状态

本条记录及两份复审材料尚未提交或推送。

## WR-20260717-002 — 推送G2非资产反事实复审

- 时间：2026-07-17 11:25:00 +08:00
- 类型：GIT | PROGRESS
- 任务/门：00-总控 / G2反事实复审Git收尾
- 状态：完成
- 负责人：Codex

### 背景与目标

WR-20260717-001已完成G2非资产条件现场审计和书面报告。本条只记录已经实际发生的提交与GitHub同步，不改变正式G2状态。

### 实际变更

- 创建commit `7b82aaa`，标题`Audit G2 without I3D asset admissibility`。
- 将`main`推送至`origin/main`，远端由`a74e8d8`前进至`7b82aaa`。

### 验证与证据

- 提交前`git diff --cached --check`：exit 0。
- commit包含3个文件、113行新增；新建反事实复审报告并更新G1/G2矩阵与工作日志。
- `git push origin main`：exit 0，输出`a74e8d8..7b82aaa main -> main`。

### 影响与边界

GitHub已固定“非资产G2条件通过、正式G2仍blocked”的审计结论。未修改总纲、manifest门状态、split或任务20启动条件。

### 风险、问题与阻塞

无新增Git阻塞。资产许可、官方revision和权利方包身份/fixity证明仍未取得。

### 下一步

等待用户决定是否承担该风险并正式修改门定义；未有新决定前保持现状。

### Git状态

commit `7b82aaa`已推送；本条日志本身尚未提交或推送。

## WR-20260717-003 — 拆分G2、接受I3D资产风险并放行任务20

- 时间：2026-07-17 12:20:00 +08:00
- 类型：DECISION | PROTOCOL | DATA | VALIDATION | HANDOFF
- 任务/门：00-总控 / G2正式裁定与任务20启动
- 状态：完成待任务线程创建
- 负责人：Codex

### 背景与目标

用户明确要求修改总纲，将门拆为“协议/数据G2通过”与“资产风险延期接受”，并放行任务20。本批次把该授权写入SSOT、机器manifest、验证器、数据与实验文档；未知许可事实不得因风险接受而改写为已闭合。

### 实际变更

- 总纲升级为v1.16，新增`SC-20260717-01`：`G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`、`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`、总门=`PASS_WITH_ACCEPTED_ASSET_RISK`、`formal_split=true`、`internal_model_use_allowed=true`。
- 新建`TASK00_G2_RISK_ACCEPTANCE_AND_TASK20_AUTHORIZATION_20260717.md`，明确任务20允许范围、I3D再分发禁令、论文披露和权利方否认/hash漂移止损条件。
- 同步G1/G2矩阵、任务10交接、决策/风险/claim台账、Data Card、Datasheet、发布边界、数据源台账、M2数据协议、实验协议、I3D序列协议、研究冻结审计、计划与进度。
- 更新M2 release、泄漏门、数据工程与I3D序列构建/验证脚本；重建dataset、split、label-provenance、leakage、sequence和reproducibility manifests。
- 未修改原始数据、标签定义、split算法或I3D特征字节；I3D资产级许可、稳定官方revision和权利方包身份/fixity仍保持未知。

### 验证与证据

- `python -m compileall -q scripts`：exit 0；I3D序列manifest构建、8项单测和专项validator均exit 0，专项状态=`PASS_PROTOCOL_G2_RISK_ACCEPTED_TASK20_AUTHORIZED`。
- 首次误调用`build_m2_data_artifacts.py`未提供必选参数：exit 2并显示usage；未隐瞒。改用`--public-core`后构建成功。
- M2数据构建、泄漏正门、release构建与数据工程validator均exit 0；首轮release validator因6个授权性状态输出尚未写入复现基线而exit 1，准确报告6项mismatch。
- 随后两次`reproduce_m2_minimal.py --public-core`均exit 0；Python 3.8.9、`-I -S`、19项before/after一致、`mismatches=[]`。最终`validate_m2_release.py` exit 0，G1 PASS、G2风险接受PASS、`formal_split=true`。
- `run_m2_leakage_tests.py --selftest --no-write`：exit 0并正确输出`LEAKAGE_BLOCKED (expected negative fixture)`。
- `run_preparation_checks.py`：exit 0，`blocking_checks=[]`；`formal_model_work_ready=false`仅因当前环境缺少faiss，任务20须先完成正式环境锁定与安装，不撤销其创建授权。

### 影响与边界

任务20已经获得创建与内部研究授权。I3D未知许可/revision/权利方fixity从启动硬阻塞转为持续风险账，不是许可证据；禁止提交或再分发`.npy`，禁止声称权利方确认。若权利方否认、固定hash/8210覆盖漂移或任务绕开冻结协议，相关运行立即标记`ASSET_INVALIDATED_DO_NOT_REPORT`。

### 风险、问题与阻塞

当前无任务20创建阻塞。正式实验环境仍需由任务20安装并锁定faiss等依赖；在该环境门通过前不得把环境诊断写成已就绪。公开发布模型权重、embedding或索引仍须单独审计其是否封装或可逆推出受限特征。

### 下一步

提交并推送本批次状态合同，创建`20-M3 基线与统一评测`任务，绑定最终Git提交并从环境/配置/加载器/指标和最小基线测试开始。

### Git状态

本条及本批次变更在记录时尚未提交或推送；任务20线程尚未创建。

## WR-20260717-004 — 固定G2风险接受提交并创建任务20

- 时间：2026-07-17 12:35:00 +08:00
- 类型：GIT | HANDOFF | PROGRESS
- 任务/门：00-总控 / 任务20正式创建
- 状态：完成
- 负责人：Codex

### 背景与目标

WR-20260717-003已完成G2拆分、机器合同重建与验证。本条记录随后真实发生的Git固定、GitHub同步和任务20创建，不回写或覆盖历史记录。

### 实际变更

- 创建commit `f869732`，标题`Release task 20 with accepted I3D asset risk`，包含总纲v1.16、授权书、机器manifest、验证器和一致性文档。
- 首次`git push origin main`直连超时失败；随后按用户指定的本机7890代理重试成功，远端由`987e2a1`前进至`f869732`。
- 在本地项目`D:\MMSA-CH-SIMS`创建`20-M3 基线与统一评测`任务，任务ID=`019f6e2e-f781-7270-bb45-af8272ff5a5c`。
- 任务20交接明确绑定commit `f869732`与总纲v1.16；要求先锁定环境、解决faiss缺失、冻结统一配置/加载器/指标/预测合同并实现最小基线测试，不提前引入teacher、memory或完整CARM。

### 验证与证据

- 提交前`git diff --check`与`git diff --cached --check`均exit 0。
- commit成功：35个文件，317行新增、144行删除；新建任务20授权文件。
- 首次直连push exit 1，错误为无法连接`github.com:443`；7890代理重试exit 0，输出`987e2a1..f869732 main -> main`。
- `codex_app__create_thread`返回任务ID `019f6e2e-f781-7270-bb45-af8272ff5a5c`；创建后工作区仍为clean。

### 影响与边界

任务20现已正式启动，不再需要重复请求G2许可。它只能进行内部研究，不得再分发I3D或把资产未知项写成权利方确认；faiss安装与正式环境锁定仍须在任务20内通过验证。

### 风险、问题与阻塞

无任务创建阻塞。Git直连不稳定，后续网络同步可优先使用用户指定的7890代理。任务20与00共享本地项目，00收尾不再修改实验核心，避免并发冲突。

### 下一步

由任务20按总纲第17节执行M3并提交G3证据；00只做门审阅和范围监督。

### Git状态

内容commit `f869732`已推送；本条创建记录与计划/进度同步尚未提交或推送。

## WR-20260717-005 — 20-M3 第一批基线与环境审计
- 时间：2026-07-17 13:40:00 +08:00
- 类型：PROGRESS | FEATURE | TEST | ENVIRONMENT
- 任务/门：20-M3 / M3 第一阶段
- 状态：部分完成
- 负责人：Codex

### 背景与目标
按总纲 v1.16 第17节任务20，在已授权且接受 I3D 资产风险的边界内，先锁定独立环境、冻结统一配置与评测合同，并实现最低基线；I3D 许可、官方 revision、权利方身份/fixity 仍保持 UNKNOWN。

### 实际变更
- 新增任务20配置、baseline loader、unittest、独立环境依赖锁和持久化规划目录。
- 配置冻结 T0、manifest 引用、train/dev/test 使用边界、三种最低基线、指标和 teacher/memory/full-CARM 排除项；loader 拒绝评论/未来字段并强制 train-only 拟合。
- 创建独立 `.venv-task20` 并加入 `.gitignore`；未将本机环境或受限资产纳入 Git。

### 验证与证据
- `\.\.venv\Scripts\python.exe -m unittest -v tests.test_task20_baseline`：exit 0，3/3 通过。
- `\.\.venv\Scripts\python.exe -m compileall -q scripts tests`：exit 0。
- `\.\.venv\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0，`blocking_checks=[]`；真实报告 `formal_carm_environment.classification=BLOCKED_M1`、`faiss_available=false`、`formal_model_work_ready=false`。
- 独立环境 pip 25.0.1 升级成功；安装 `pytest`/`faiss-cpu` 因代理不可连接失败，环境未就绪，失败证据保留。

### 影响与边界
最低基线和统一合同已可在历史环境运行自测，但不能宣称正式模型环境已锁定；未接入真实正式预测，不产生论文数字。未读取、复制、提交或再分发 I3D `.npy`、junction、本机路径或可逆受限资产。

### 风险、问题与阻塞
`faiss` 仍缺失，独立环境安装受外部代理连接失败阻塞；I3D 许可/revision/fixity 仍未知。若权利方否认或固定 hash/8210 覆盖漂移，须立即标记 `ASSET_INVALIDATED_DO_NOT_REPORT`。

### 下一步
1. 在可用包源/代理恢复后，仅在 `.venv-task20` 安装并验证 faiss，再更新环境锁定证据。
2. 接入权威 split/label-provenance manifest 的受控样例，生成 prediction/run manifest 与指标输出。

### Git状态
当前未提交、未推送；本条记录与本批次代码/配置变更待同一提交。

## WR-20260717-006 — 压缩旧总控上下文并建立新总控交接包

- 时间：2026-07-17 14:10:00 +08:00
- 类型：DOC | PROGRESS | DECISION | TEST
- 任务/门：00-总控 / 跨项目总控迁移
- 状态：完成待创建新项目
- 负责人：Codex

### 背景与目标

用户指出旧总控对话上下文过长，要求创建新的Codex项目承担00总控责任，并完整总结本次对话、提取总纲和已有项目进展。迁移必须基于提交后的真实状态，不能覆盖任务20并发未提交工作，也不能把完整原始聊天写入仓库。

### 实际变更

- 读取任务20线程`019f6e2e-f781-7270-bb45-af8272ff5a5c`，发现第一批改动未提交；要求任务20自行验证、提交和推送。任务20完成commit `5522619`并报告工作区clean。
- 新建`TOTAL_CONTROL_HANDOFF_20260717.md`，用结构化锚定摘要保存用户纠偏、研究目标、C1—C3/H1—H4、数据唯一版本、G门、任务树、线程ID、已验证证据、IJCV隔离、网络政策、Git纪律、风险与最近三步。
- 建立`.light/passport.yaml`、`project_card.md`、`decision_log.md`、`version_history.md`、`terminology.md`和S00→S01交接链；passport登记任务10已交付、任务20进行中。
- 更新`progress.md`记录总控迁移准备。未修改总纲、G门、数据manifest、任务20代码或实验结果。

### 验证与证据

- 任务20回交：commit `5522619`已推送`origin/main`；单测3/3、compileall、diff check和工作日志验证通过，工作区clean；faiss仍为`BLOCKED_M1`。
- `light-memory-pm/scripts/pm.py --selftest`首次exit 1：本机技能布局无法导入`passport`，错误`ModuleNotFoundError: No module named 'passport'`；该失败保留。
- 改用`light-orchestrator/scripts/passport.py init/append-stage`：均exit 0；首次append把字符串传给整数`--stage`而exit 2，改用10/20后成功。
- `passport.py validate`：exit 0、verdict WARN；警告stage 10的PASS未携带passport内部hash/timestamp，仅能作迁移台账，不能替代原G门科学证据。
- `handoff_contract.py --card .light/handoff/S01-total-control-migration.md --as-of 2026-07-17`：首次因root parent/验证措辞/动作措辞不足exit 1；补建S00链路根并补全证据后最终exit 0、`handoff contract PASS`。
- `git diff --check`：exit 0。

### 影响与边界

新总控无需读取原始超长聊天即可恢复关键事实，但仍必须刷新Git、WORK_LOG、passport与任务线程现实。`.light`账本是跨会话状态入口，不替代总纲、machine manifest或G门证据。旧总控当前不归档，用户只授权迁移责任，未要求删除或归档历史任务。

### 风险、问题与阻塞

`pm.py audit/resume`在当前安装布局不可用，故不能声称完整memory-pm审计通过；底层passport与独立handoff合同已作为诚实降级。任务20正式环境faiss仍未闭合。I3D资产风险、IJCV项目隔离和G3前禁止任务30均保持。

### 下一步

1. 提交并推送总控交接包。
2. 创建独立的新总控Codex项目，传入完整交接与自传播要求。
3. 记录新项目ID并把最终入口交给用户。

### Git状态

本条与交接文件在记录时尚未提交或推送；新总控项目尚未创建。

## WR-20260717-007 — 推送交接包并创建00-T-AFFC新总控

- 时间：2026-07-17 14:25:00 +08:00
- 类型：GIT | HANDOFF | PROGRESS
- 任务/门：00-总控 / 新项目接管
- 状态：完成
- 负责人：Codex

### 背景与目标

WR-20260717-006已形成完整压缩交接与`.light`记忆骨架。本条记录真实发生的提交、GitHub同步和新总控Codex任务创建，使新项目从隔离worktree和全新上下文接管，而不与任务20共享主工作区写入。

### 实际变更

- 创建commit `e6c48c6`，标题`Add durable total-control handoff`，包含完整交接、`.light`台账/交接链、进度与工作记录。
- 使用用户指定的本机7890代理推送`main`，远端由`5522619`前进至`e6c48c6`。
- 以`main@e6c48c6`创建隔离worktree Codex任务，实际任务ID=`019f6e64-0635-7ac0-a70a-65445b0fc1d1`，标题设为`00-T-AFFC 新总控`。
- 新总控启动提示明确：先读S01、passport、project card、完整交接、总纲和授权；刷新Git与任务20实时状态；执行六项压缩自检；只承担00监督，不并发修改实验核心；G3前不创建任务30；交接链必须自传播。

### 验证与证据

- 提交前`git diff --cached --check`：exit 0；commit包含10个文件、429行新增。
- `git push origin main`经7890代理exit 0，输出`5522619..e6c48c6 main -> main`；随后主工作区`main...origin/main` clean。
- `codex_app__create_thread`先返回client id `client-new-thread:fa25eb85-e6a2-4aff-a3e1-57841507098b`；工作树建立后`list_threads`确认实际任务ID、独立cwd和active状态；标题重命名成功。

### 影响与边界

`00-T-AFFC 新总控`现在是后续00责任入口；旧总控不再主动执行新阶段，但未归档或删除，保留只读追溯。任务20继续独立执行M3；新总控只监督和审核G3。IJCV项目、I3D风险边界、G门和总纲v1.16均未改变。

### 风险、问题与阻塞

新总控位于隔离worktree，必须主动读取主仓库和任务20最新提交，不能把创建时`e6c48c6`永久当成实时主分支。`pm.py`包装布局问题仍未解决；交接中已禁止无新mitigation重复失败。

### 下一步

1. 等待新总控完成只读接管审计并报告六项自检结果。
2. 用户后续总控指令转交`00-T-AFFC 新总控`。
3. 旧总控保持只读追溯，不与新总控或任务20并发修改文件。

### Git状态

交接commit `e6c48c6`已推送；本条创建记录与progress追加尚未提交或推送。
## WR-20260717-008 — 完成任务20第1至5项
- 时间：2026-07-17 16:10:00 +08:00
- 类型：PROGRESS | FEATURE | TEST | ENVIRONMENT
- 任务/门：20-M3 / 任务20第1至5项
- 状态：完成
- 负责人：Codex

### 背景与目标
用户将本轮范围明确收敛到总纲 v1.16 第17节任务20第1至5项：复核任务10交接；建立独立正式环境；冻结统一配置与run manifest；建立统一loader；实现总体均值、主题均值、经验分布和多数类基线。

### 实际变更
- 冻结 `HANDOFF_10.md`、dataset/split/label-provenance/leakage manifests 的SHA-256和正式 `group_by_video_v1` split。
- 通过本机7890代理完成 `.venv-task20`；新增 `TASK20_ENVIRONMENT_LOCK.md` 并扩充 `requirements-task20-lock.txt`。
- 新增 `configs/task20/experiment.schema.json`、`baseline-common.json`、`run-manifest.schema.json` 与 `scripts/task20_contracts.py`；四个基线变体只改变 `model` 字段。
- 扩展 `scripts/task20_baseline.py` 的canonical loader、topic mean资格门、topic mean拟合/预测和统一四基线runner；新增 `scripts/run_task20_minimum_baselines.py`。
- 新增/扩展 `tests/test_task20_contracts.py` 与 `tests/test_task20_baseline.py`；更新 `.planning/task20-m3/`。旧YAML配置保留为canonical JSON/schema指针。

### 验证与证据
- 环境锁：Python 3.8.9、PyTorch 2.4.1+cu121/CUDA 12.1、Transformers 4.30.2、faiss 1.7.4、sklearn 1.3.2、CatBoost 1.2.10、LightGBM 4.5.0、MMSA 2.2.1；CUDA/GPU可用。
- `\.\.venv-task20\Scripts\python.exe scripts\environment_smoke.py --profile formal-carm`：exit 0，`passed=true`；`pip check`无破损依赖。
- 测试先后保留三类失败：缺少新API；canonical混合split被误拒；run manifest暴露绝对路径。分别补最小实现、改为验证后筛选split、改为仓库相对路径并禁止仓库外路径。
- `\.\.venv-task20\Scripts\python.exe -m unittest -v tests.test_task20_baseline tests.test_task20_contracts`：exit 0，10项通过；compileall exit 0。
- 正式CSMV train/dev smoke：5698/837，`shared_sample_ids=true`；总体均值、经验分布、多数类完成；主题均值=`NOT_APPLICABLE_NATIVE_TOPIC_ABSENT`。未查看test。
- smoke run manifest schema校验通过；run manifest SHA-256=`2a8c5001b9be03bb33c4bf53cda0c38395b4104b835ff1a5054a2c4c5e1327e8`，metrics SHA-256=`4970b2495b16fca407937aded873e079f2fb778e69dd8299124e56abab4f3924`。

### 影响与边界
任务20第1至5项已形成可复核实现。常数/分组统计基线冻结 `input_features=[]`，不读取评论或I3D；四基线共享sample ID、split与class order。smoke dev数字仅验证实现，不进入论文表格。第6至18项未启动，未修改总纲或G门。

### 风险、问题与阻塞
I3D许可、官方revision、权利方身份/fixity仍未知；环境就绪不等于资产权利闭环。CSMV原生topic完全缺失，因此主题均值只能诚实登记不适用，不能伪造主题。首次faiss单包导入因空环境缺NumPy失败，首次formal-carm smoke因缺MMSA失败，两次失败均已保留并按根因补齐。

### 下一步
等待用户授权后再执行任务20第6项及以后；本轮仅完成并验证第1至5项。

### Git状态
本条与第1至5项代码/配置/规划变更尚未提交或推送。

## WR-20260717-009 — 修复任务20独立环境的准备检查误报
- 时间：2026-07-17 16:20:00 +08:00
- 类型：FIX | TEST | VALIDATION | ENVIRONMENT
- 任务/门：20-M3 / 第1至5项交付门
- 状态：完成
- 负责人：Codex

### 背景与目标
任务20第1至5项完成后，交付前运行项目准备检查。首次检查发现密钥扫描器遍历了新建的 `.venv-task20` 第三方依赖目录并产生误报；本批次要求在不放宽密钥检测规则的前提下修复扫描边界并重新关闭正式准备门。

### 实际变更
- 新增 `tests/test_preparation_checks.py`，以临时目录同时放置命名虚拟环境和真实源码，验证扫描器跳过 `.venv-task20`、但继续报告真实源码命中。
- 更新 `scripts/run_preparation_checks.py`，新增 `should_skip_secret_scan()`，在既有精确排除项之外仅排除 `.venv-*` 命名虚拟环境；`SECRET_PATTERNS` 未修改。
- 向 `.planning/task20-m3/findings.md` 与 `progress.md` 追加首次失败、根因、修复和最终门状态。

### 验证与证据
- 修复前 `\.\.venv-task20\Scripts\python.exe scripts\run_preparation_checks.py`：exit 1，唯一 `blocking_checks=["secret_scan"]`；命中来自 `.venv-task20` 第三方依赖，未发现项目密钥。
- 新回归测试修复前：exit 1，结果同时包含 `.venv-task20\\dependency.py` 与 `src\\application.py`，准确复现目录边界缺失。
- 修复后 `\.\.venv-task20\Scripts\python.exe -m unittest -v tests.test_preparation_checks`：exit 0，1项通过。
- `\.\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，19项通过。
- 修复后 `\.\.venv-task20\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`secret_scan.hits=[]`、`formal_carm_environment.classification=READY_FOR_REVIEW`、`formal_model_work_ready=true`。

### 影响与边界
项目扫描器不再把任务20独立虚拟环境中的第三方测试常量误判为仓库密钥，同时保留对真实项目源码的原有扫描强度。未修改总纲、G门、数据manifest、split、标签、基线算法或受限资产；第6至18项仍未启动。

### 风险、问题与阻塞
I3D许可、官方revision、权利方包身份/fixity仍未知，资产接受风险没有因环境或准备门通过而解决。若权利方否认或固定hash/8210覆盖漂移，仍须立即标记 `ASSET_INVALIDATED_DO_NOT_REPORT`。

### 下一步
运行工作日志验证、最终准备检查、compileall与diff check，确认第1至5项可交付；未经新授权不推进第6至18项。

### Git状态
本条、扫描器修复及任务20第1至5项全部改动尚未提交或推送。

## WR-20260717-010 — 推进任务20第6至18项并记录远端GPU运行时阻塞

- 时间：2026-07-17 17:00:00 +08:00
- 类型：FEATURE | TEST | VALIDATION | ENVIRONMENT | DECISION
- 任务/门：20-M3 / 任务20第6至18项
- 状态：部分完成，正式高算力运行阻塞
- 负责人：Codex

### 背景与目标

用户授权继续执行总纲v1.16任务20第6至18项，并要求高算力实验优先使用其租用GPU；若GPU不可用立即报告。执行继续遵守train-only拟合、dev选择、test仅按预注册规则评测和I3D禁止再分发边界。

### 实际变更

- 新增`scripts/task20_metrics.py`与`scripts/task20_evaluation.py`，实现JS、NLL、EMD、Macro-F1、Balanced Accuracy、Brier、ECE、ACE、AURC-JS、预测标准、E0和视频级paired bootstrap。
- 新增`configs/task20/prediction.schema.json`与`tuning-plan-v1.json`；五个可运行模型族均冻结12 trial，dev按JS选择，NLL/Brier/参数量依次tie-break，test选择期不可见。
- 新增`scripts/task20_models.py`、`task20_training.py`、`build_task20_i3d_pooled.py`和`run_task20_pooled_mlp.py`；实现I3D mean/std不可逆汇总、train-only standardizer、pooled MLP、masked temporal attention、早停和run bundle。
- 新增`tests/test_task20_evaluation.py`、`test_task20_models.py`、`test_task20_training.py`；扩展最低基线到九项指标与标准预测输出。
- 新增`TASK20_BASELINE_EXECUTION_AUDIT.md`、`BASELINE_TABLE_V1.md`、`TASK20_G3_EVIDENCE_DRAFT.md`，并更新实验登记与`.planning/task20-m3/`。
- 官方revision只读审计发现无VC-CSA模型代码且官方输入依赖目标评论；legacy 48维数据无正式split、非T0且为SILVER二分类，均按任务17保留失败根因，不生成或复用不合格数值。

### 验证与证据

- 指标/合同首轮红测因缺模块失败；随后AURC同置信度置换测试真实失败并修复为tie-group同时进入覆盖曲线。
- 神经训练红测因float32 softmax在`1e-8`容差下误拒失败；修复为验证后按`1e-6`接受并归一化，不放宽负值/NaN/明显非概率输入。
- `\.\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，35项通过。
- I3D汇总首次前台命令在3分钟超时，但后台进程真实完成；最终缓存8210条、2048维、train/dev/test=`5698/837/1675`，SHA-256=`3bb7b6bb6620b7b7d4738ad207f7c20eef9c2d9990cfeafa164807910eb8d5ea`，不含标签或原序列。
- 首次pooled-MLP CPU smoke完成后run manifest schema复核因缺`config`/`code`失败；保留失败目录，补hash provenance后新目录schema校验通过。
- 两次独立CPU smoke使用同seed，predictions SHA-256均为`b0ef9a6a979d938f22609b1ed486446aca9541e637dc7b9f15d68e047c0adf86`，metrics SHA-256均为`2f2019b230761cb9a21d3cfa890717991c1e926c04d66067632679d0b55d5d0c`；仅证明同环境工程复跑。
- 租用A30硬件预检可见约24GB显存且空闲；新Conda Python 3.8环境已建立，但两条官方Torch安装通道各在10分钟窗口内无有效进度。平台自带Torch 1.3.1/CUDA 10.1可枚举A30，但最小CUDA矩阵运算30秒未完成；正式状态=`REMOTE_GPU_RUNTIME_UNAVAILABLE_ENVIRONMENT_NOT_READY`。

### 影响与边界

第10至14项实现闭合；第6、7项完成可复核失败审计；第8、9项实现与不适用性合同已建立；第15至18项已有smoke、表格和G3草案。未查看test、未运行正式12-trial或单种子完整实验，CPU smoke不进入论文表格。未上传I3D序列、junction、本机路径或可逆受限资产，未修改总纲、G门或数据manifest。

### 风险、问题与阻塞

远端GPU硬件可见但训练运行时不可用，正式高算力实验暂停并已立即向用户报告。I3D许可、官方revision、权利方包身份/fixity仍未知；权利方否认或固定hash/8210覆盖漂移时仍须标记`ASSET_INVALIDATED_DO_NOT_REPORT`。

### 下一步

1. 等待用户提供/切换到带Ampere兼容PyTorch/CUDA的可用镜像或新实例，再立即复核最小CUDA矩阵运算。
2. 运行冻结的12-trial dev选择、单种子完整run与同seed复跑；选择冻结后才执行test一次评测。
3. 计算2000次视频级paired bootstrap，更新正式baseline-table-v1并提交最终G3证据给00。

### Git状态

本条与任务20第1至18项当前代码、配置、测试、规划和审计材料均尚未提交或推送。

## WR-20260717-011 — 验证任务20第6至18项阶段交付并暂停正式GPU运行

- 时间：2026-07-17 17:10:00 +08:00
- 类型：TEST | VALIDATION | HANDOFF
- 任务/门：20-M3 / 第6至18项阶段交付
- 状态：验证通过，GPU阻塞待用户更换运行时
- 负责人：Codex

### 背景与目标

WR-20260717-010已记录统一评测、模型代码、smoke与远端GPU运行时失败。本条只记录交付前真实门禁和暂停边界，避免把部分完成写成任务20或G3已完成。

### 实际变更

- 未新增算法或数据变更；保持正式高算力运行暂停。
- 一次性远端认证辅助文件和CUDA smoke辅助文件已从工作区删除；认证值未写入Git、工作日志、配置或run bundle。

### 验证与证据

- `\.\.venv\Scripts\python.exe scripts\validate_work_log.py`：exit 0，75条，最新`WR-20260717-010`。
- `\.\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，35项通过。
- `\.\.venv-task20\Scripts\python.exe -m compileall -q scripts tests`与`git diff --check`：exit 0。
- 默认`.venv`与任务20`.venv-task20`分别运行`scripts/run_preparation_checks.py`：均exit 0、`blocking_checks=[]`、`secret_scan.hits=[]`；任务20环境`formal_model_work_ready=true`。
- 最终工作区只包含任务20代码、配置、测试、规划、实验登记、审计与工作日志改动；未修改总纲、G门或数据manifest。

### 影响与边界

第6至18项现有实现可安全交付审查，但正式12-trial、单种子完整run、test一次性评测、正式bootstrap和最终G3提交仍未发生。不得把本阶段状态写成任务20全部完成。

### 风险、问题与阻塞

唯一新增执行阻塞为租用A30的PyTorch/CUDA运行时不可用；GPU硬件可枚举不等于可训练。I3D权利/fixity未知风险继续保留。

### 下一步

用户更换到Ampere兼容、可执行最小CUDA矩阵运算的PyTorch镜像或新实例后，从冻结tuning plan继续，不重新定义实验。

### Git状态

全部改动尚未提交或推送，工作区非clean。

## WR-20260717-012 — 修复test早停泄漏并完成temporal-attention可运行合同

- 时间：2026-07-17 23:10:00 +08:00
- 类型：FIX | FEATURE | TEST | ENVIRONMENT
- 任务/门：20-M3 / 任务20第7、8、12、15、17、18项
- 状态：部分完成；正式GPU运行仍阻塞
- 负责人：Codex

### 背景与目标

继续执行任务20第6至18项：在不传输受限I3D资产的前提下修复租用A30运行时，并补齐强视觉基线runner与train/dev/test负门。

### 实际变更

- 分层诊断远端Conda、PyTorch、网络与磁盘；确认PyPI超时而官方PyTorch索引和国内镜像可达。公开PyTorch 1.13.1/CUDA 11.7 wheel在本机下载并计算SHA-256，分段上传后在远端重组；双端长度均为1,801,800,326字节，SHA-256均为`bbf9546f0d0d8b51263ca479637b426a88335fca0034f42cec63d4d32dee05af`，远端输出确认wheel安装成功。
- 依赖安装期间远端通道异常结束，后续TCP端口不可连接；未执行成功的CUDA矩阵smoke，环境继续登记`REMOTE_GPU_RUNTIME_UNAVAILABLE_ENVIRONMENT_NOT_READY`。未上传原始I3D `.npy`、标签、本机路径或可逆受限资产。
- 在`tests/test_task20_pooled_runner.py`先新增失败回归测试，证明原`run_task20_pooled_mlp.py`会让test进入早停路径；正式test此前未运行。修复后固定为train拟合、dev早停、test仅前向一次，并记录冻结dev selection输入hash。
- 在`tests/test_task20_training.py`和`tests/test_task20_temporal_runner.py`先新增失败测试，再扩展`task20_training.py`和新增`run_task20_temporal_attention.py`：流式train-only时序标准化、冻结完整序列动态padding、确定性批计划、12-trial/dev选择、test负门、预测/指标/模型/环境/manifest/失败产物。
- `task20_models.py`固定`CUBLAS_WORKSPACE_CONFIG=:4096:8`；新增红测验证该确定性合同。
- 更新`TASK20_BASELINE_EXECUTION_AUDIT.md`、`BASELINE_TABLE_V1.md`、`TASK20_G3_EVIDENCE_DRAFT.md`、`experiments/EXPERIMENT_REGISTRY.md`和`.planning/task20-m3/`状态；未修改总纲或G门。

### 验证与证据

- `.\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，44项全部通过。
- temporal runner在固定32个train、16个dev、1 trial、2 epochs、CPU条件下独立smoke两次；两次`predictions.jsonl` SHA-256均为`5d66b46ca21386d3cd8be6838d4c80cc343a24243a9673b16c8abaf4c9739971`，`metrics.json`均为`023519d164a893a91a6b2754c1641506b6e25f96f68d5b9d67eee2af27e63f82`，`selection.json`均为`cdac127a4a9bf238b8cf295f80ee08e0d019d02feebbe4e7adf519f39cffb9f8`。
- 两个temporal smoke的`run-manifest.json`均通过`configs/task20/run-manifest.schema.json`；`python -m compileall -q scripts tests` exit 0。
- 最终远端端口复查失败；未启动12-trial、正式test或正式bootstrap。

### 影响与边界

pooled与temporal模型的test路径现在不会用test选择epoch；temporal强视觉基线具备端到端工程运行能力。所有smoke数字仅作实现验证，不进入论文表。I3D许可、官方revision、权利方身份/fixity继续未知；资产风险状态未改变。

### 风险、问题与阻塞

租用A30实例当前不可连接，CUDA最小矩阵未验证；完整序列temporal模型又受原始I3D不得上传边界约束。正式dev选择、完整run、一次性test、2000次paired bootstrap和最终G3包仍未完成。

### 下一步

1. 等待租用GPU恢复或更换实例后先完成CUDA最小矩阵和远端依赖锁，再运行pooled MLP正式dev选择。
2. 对temporal完整序列正式运行，需使用合法既有I3D环境；不得通过上传原始`.npy`绕过资产边界。
3. 正式运行完成后再执行一次性test、paired bootstrap、冻结baseline-table-v1和最终G3证据。

### Git状态

本批次改动待验证后有意提交；写入时尚未提交或推送，工作区非clean。

## WR-20260717-013 — 更正WR-20260717-012时间字段

- 时间：2026-07-17 15:08:07 +08:00
- 类型：DOC
- 任务/门：20-M3 / 工作记录纠错
- 状态：完成
- 负责人：Codex

### 背景与目标

`WR-20260717-012`的时间字段误写为当日未来时间；按只追加政策不改写原记录，追加本条更正。

### 实际变更

仅声明`WR-20260717-012`的正确记录时间为`2026-07-17 15:08:07 +08:00`；其余行为、文件、验证结果和Git状态不变。

### 验证与证据

- `Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'`：`2026-07-17 15:08:07 +08:00`。

### 影响与边界

只更正日志时间，不改变实验、资产、G门或结论。

### 风险、问题与阻塞

无新增风险；远端GPU阻塞沿用`WR-20260717-012`。

### 下一步

继续执行提交前项目门禁。

### Git状态

本条与`WR-20260717-012`同批待提交，尚未推送。

## WR-20260717-014 — 完成任务20本批次提交前门禁并更正测试总数

- 时间：2026-07-17 15:09:35 +08:00
- 类型：TEST | VALIDATION | DOC
- 任务/门：20-M3 / 提交前门禁
- 状态：验证通过；正式GPU运行仍阻塞
- 负责人：Codex

### 背景与目标

对`WR-20260717-012`所述实现执行项目规定的完整提交前门禁，并按只追加政策更正其中记录早于最终测试发现的测试总数。

### 实际变更

- `WR-20260717-012`记录的44项测试是当时运行结果；加入两个smoke/test策略负门后，最终测试总数为46项，原记录不回改。
- 尝试清理操作系统临时目录中的公开wheel和隔离SSH辅助环境时，递归删除命令被执行策略拒绝；临时内容不在仓库内、不含项目数据或认证值，未改用跨shell破坏性命令绕过。

### 验证与证据

- `.\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，46项全部通过。
- `.\.venv-task20\Scripts\python.exe -m compileall -q scripts tests`：exit 0。
- `git diff --check`：exit 0。
- `.\.venv\Scripts\python.exe scripts\validate_work_log.py`：exit 0，78条、最新`WR-20260717-013`、`passed=true`。
- `.\.venv\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`secret_scan.hits=[]`；默认环境仍诚实报告`formal_model_work_ready=false`，原因是默认`.venv`无faiss，不冒充任务20独立环境。

### 影响与边界

本批代码、配置、文档和日志通过当前项目门禁。默认环境状态未被改写；任务20独立环境仍需单独复核。临时公开运行时文件不属于Git交付物。

### 风险、问题与阻塞

远端实例不可连接，正式实验仍未运行。操作系统临时目录清理被策略拒绝，但不影响仓库安全扫描或实验边界。

### 下一步

1. 用`.venv-task20`补跑准备检查，确认独立正式环境状态。
2. 刷新diff/status并有意提交、推送本批次。

### Git状态

本条写入时尚未提交或推送，工作区非clean。

## WR-20260717-015 — 提交并同步任务20统一基线实现批次

- 时间：2026-07-17 15:12:49 +08:00
- 类型：PROGRESS | SYNC
- 任务/门：20-M3 / 任务20第1至18项阶段实现
- 状态：代码批次已提交并推送；正式实验仍阻塞
- 负责人：Codex

### 背景与目标

将已通过项目门禁的任务20统一配置、最低基线、完整指标、预测与E0合同、pooled/temporal runner、测试、规划和阶段证据作为一个有意实现提交同步到`main`。

### 实际变更

- 提交`9c06a149146d766186eecf8065a9f1897167f556`，提交说明为`feat(task20): add unified baseline evaluation`，共35个文件、3360行新增、52行删除。
- 使用本机代理推送`main`；远端`origin/main`从`4d1861908c24570599ad6b48d6f908b8a1efcb0d`前进到`9c06a149146d766186eecf8065a9f1897167f556`。
- 受保护的总纲、G门、00授权文件、`HANDOFF_10.md`和数据manifest均未进入提交。

### 验证与证据

- `git push origin main`使用一次性代理配置：exit 0，输出`main -> main`。
- `git rev-parse HEAD`与`git rev-parse origin/main`均为`9c06a149146d766186eecf8065a9f1897167f556`。
- 推送后`git status --short --branch`为`## main...origin/main`。

### 影响与边界

任务20阶段实现已在远端仓库可复核；`results/`、原始I3D `.npy`、模型权重、连接信息和认证值未提交或推送。该同步不代表正式baseline数值、G3或总任务20已完成。

### 风险、问题与阻塞

租用A30仍不可连接，正式12-trial、完整run、一次性test、paired bootstrap和最终G3包继续阻塞；I3D权利/fixity未知状态未改变。

### 下一步

远端实例恢复或更换后，先验证最小CUDA矩阵与依赖锁，再从冻结dev调参计划继续；不得重新定义实验或上传受限I3D资产。

### Git状态

实现提交`9c06a149146d766186eecf8065a9f1897167f556`已推送`origin/main`；本条日志将作为后续日志提交同步。

## WR-20260717-016 — 完成任务20第6项原48维native legacy重跑

- 时间：2026-07-17 22:36:36 +08:00
- 类型：PROGRESS | EXPERIMENT | TEST | DOC
- 任务/门：20-M3 / 总纲任务20第6项
- 状态：legacy原生兼容重跑完成；不具备CSMV统一正式结果资格
- 负责人：Codex

### 背景与目标

用户明确要求重跑任务6，并允许优先使用本地3070 Ti；若耗时过长再租算力。原48维资产为CUC 2787条SILVER二分类、含非T0字段且没有CSMV正式split，故不能改写为八类分布正式结果。本批目标是在不修改总纲、G门或CSMV冻结协议的前提下，建立独立native legacy合同，重新运行CatBoost/HGB/LightGBM且不复用旧论文数字。

### 实际变更

- 新增`configs/task20/legacy-48-native-rerun-v1.json`，固定`LEGACY_NATIVE_COMPATIBILITY_ONLY`、publisher hash split、每模型12-trial、dev按Macro-F1选择和test一次性评测。
- 新增`scripts/task20_legacy48.py`与`scripts/run_task20_legacy48.py`：加载有限48维二分类记录、输出单向hash样本/组ID、验证发布者组不跨split、计算Macro-F1/Balanced Accuracy/AUPRC/Recall等指标，并禁止将该结果标为CSMV统一主表资格。
- 新增`tests/test_task20_legacy48.py`共6项测试；先后出现缺模块与缺API两轮预期失败，再完成最小实现。
- 运行三模型各1个dev-only trial，合计约4.8秒；据此判断完整36 trial无需GPU。完整本地CPU运行耗时36.4秒，split为train/dev/test 1905/307/575条、28/6/9个发布者组。
- CatBoost/HGB/LightGBM的test Macro-F1分别为0.5346/0.4591/0.3645，Balanced Accuracy为0.6006/0.5514/0.4766，AUPRC为0.6884/0.5989/0.4581，正类Recall为0.2183/0.1338/0.0528；每模型test调用均为1次，不做test后调参。
- 本机忽略的run bundle位于`results/task20/legacy48-native-rerun-v1/`，包含metrics、predictions、split/run manifest及artifact hashes；不含原始48维特征、本机路径、旧论文数字或I3D资产。
- 更新`BASELINE_TABLE_V1.md`、`TASK20_BASELINE_EXECUTION_AUDIT.md`、`experiments/EXPERIMENT_REGISTRY.md`与`.planning/task20-m3/`三份规划记录；原统一正式尝试的`FAILED_DATA_MISMATCH_NO_FROZEN_SPLIT_T0_INELIGIBLE`历史记录继续保留。

### 验证与证据

- 租用A30 TCP连通性复查：5秒超时，`TCP_REACHABLE=False`；未标记为可用，也未向远端传输数据。
- `\.venv-task20\Scripts\python.exe -m unittest tests.test_task20_legacy48 -v`：首次因`task20_legacy48`缺失失败，第二次因`build_split_manifest`缺失失败；实现后6/6通过。
- `\.venv-task20\Scripts\python.exe scripts\run_task20_legacy48.py --data-dir <external-local-read-only> --output results\task20\legacy48-dev-smoke-20260717 --max-trials-per-model 1 --dev-only`：exit 0，三模型test均`NOT_EVALUATED_DEV_ONLY`。
- 同一runner完整运行：exit 0，三模型各12 trial、test各调用1次、1725条test预测，状态`COMPLETED_LEGACY_NATIVE_NON_T0_NON_COMPARABLE`。
- run bundle合同复核：`RUN_BUNDLE_CONTRACT_OK=True`，路径/项目名扫描无命中；metrics、run manifest、split manifest、predictions四个SHA-256已写入本机`artifact-hashes.json`。
- `\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，52项全部通过。
- `\.venv-task20\Scripts\python.exe -m compileall -q scripts tests`：exit 0。
- `git diff --check`：exit 0。

### 影响与边界

任务6现在拥有重新计算的独立legacy原生兼容结果，但这些特征非T0、标签为SILVER二分类、资产2787/2815版本漂移和221条标签冲突仍未解决。结果只能进入明确的legacy附表，不能与CSMV八类分布结果比较、不能承担主结论或升级G门。I3D许可、官方revision、权利方包身份/fixity未知状态未改变。

### 风险、问题与阻塞

- 租用A30当前不可连接；本批树模型因实测仅36.4秒而按用户授权使用本地CPU完成，不构成高算力替代。
- LightGBM的跨发布者test Balanced Accuracy低于0.5，三模型正类Recall均低；失败表现如实保留，不静默删除或test后调参。
- CSMV正式I3D训练、任务7正式强基线及最终G3证据仍受合格GPU运行时和既有资产边界约束。

### 下一步

1. 运行`validate_work_log.py`与`run_preparation_checks.py`两项项目门禁。
2. 复核diff与Git状态；若门禁通过，再有意提交和同步本批任务6实现与聚合文档，继续排除`results/`原始run bundle。

### Git状态

本条写入时改动尚未提交或推送，工作区非clean；`results/`保持Git忽略。

## WR-20260717-017 — 更正WR-20260717-016验证命令路径

- 时间：2026-07-17 22:37:27 +08:00
- 类型：DOC
- 任务/门：20-M3 / 工作记录纠错
- 状态：完成
- 负责人：Codex

### 背景与目标

`WR-20260717-016`的四条任务20独立环境验证命令误将开头的`.\`写成了`\`。按只追加政策不改写原记录，追加本条更正。

### 实际变更

`WR-20260717-016`中的四条对应命令实际均以`.\.venv-task20\Scripts\python.exe`开头；其参数、退出码、测试数量和结果不变。

### 验证与证据

- 本条仅纠正命令文本；实际终端输出已在`WR-20260717-016`记录为6/6新测试、52/52全量测试、compileall exit 0和完整runner exit 0。

### 影响与边界

不改变代码、实验数值、资产边界、G门或Git状态。

### 风险、问题与阻塞

无新增风险；任务6的legacy资格限制和远端GPU不可用状态沿用`WR-20260717-016`。

### 下一步

继续执行提交前项目门禁。

### Git状态

本条与`WR-20260717-016`同批待提交，尚未推送。

## WR-20260717-018 — 完成任务6提交前项目门禁

- 时间：2026-07-17 22:39:11 +08:00
- 类型：TEST | VALIDATION
- 任务/门：20-M3 / 任务6提交前门禁
- 状态：验证通过
- 负责人：Codex

### 背景与目标

在任务6代码、配置、聚合结果文档与运行记录进入有意提交前，执行AGENTS要求的工作日志验证和准备检查，并复核任务20独立正式环境。

### 实际变更

- 本条仅追加验证事实；未改动实验配置、模型结果、总纲、G门或数据manifest。

### 验证与证据

- `.\.venv\Scripts\python.exe scripts\validate_work_log.py`：exit 0，82条记录、最新`WR-20260717-017`、`passed=true`。
- `.\.venv\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`secret_scan.hits=[]`；默认环境诚实报告`formal_model_work_ready=false`，原因为默认`.venv`无faiss。
- `.\.venv-task20\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`secret_scan.hits=[]`、`formal_carm_environment.classification=READY_FOR_REVIEW`、`faiss_available=true`、`formal_model_work_ready=true`。

### 影响与边界

门禁证明当前任务6批次满足工作日志、敏感信息扫描、Git忽略和任务20独立环境要求；不改变legacy结果只能用于非T0原生兼容附表的资格限制。

### 风险、问题与阻塞

默认`.venv`无faiss的历史状态未伪装为已解决；任务20独立环境可用。远端A30不可连接和CSMV正式高算力运行阻塞仍保留。

### 下一步

因本条使日志计数变化，复跑强制日志与准备检查，然后复核diff/status并有意提交、推送本批次。

### Git状态

本条写入时尚未提交或推送，工作区非clean；`results/`继续保持忽略。

## WR-20260717-019 — 提交并同步任务20第6项重跑批次

- 时间：2026-07-17 22:40:53 +08:00
- 类型：PROGRESS | SYNC
- 任务/门：20-M3 / 总纲任务20第6项
- 状态：实现批次已提交并推送
- 负责人：Codex

### 背景与目标

将已通过门禁的任务6 native legacy配置、运行器、测试、聚合结果文档、规划与工作记录作为有意提交同步到`main`。

### 实际变更

- 提交`02a82b6d9e16463759cd5477580a7fab3917e465`，提交说明为`feat(task20): rerun native legacy baselines`，共11个文件、913行新增、11行删除。
- 使用本机一次性代理配置推送`main`；远端`origin/main`从`98d81787cc4dff79dec716ca35f4d76742c730b7`前进到`02a82b6d9e16463759cd5477580a7fab3917e465`。
- 总纲、G门、00授权文件、数据manifest、原始48维资产、`results/`run bundle和I3D资产均未进入提交。

### 验证与证据

- `git push origin main`使用一次性本机代理：exit 0，输出`main -> main`。
- `git rev-parse HEAD`与`git rev-parse origin/main`均为`02a82b6d9e16463759cd5477580a7fab3917e465`。
- 推送后`git status --short --branch`为`## main...origin/main`。

### 影响与边界

任务6独立legacy原生兼容重跑已可在远端仓库审计；本次同步不升级其CSMV统一结果资格，不改变I3D未知权利/fixity状态或任何G门。

### 风险、问题与阻塞

租用A30仍不可连接；CSMV正式高算力运行仍阻塞。任务6低Recall与非T0/SILVER/版本漂移限制保持不变。

### 下一步

复跑日志验证与准备检查，将本条同步记录作为日志收尾提交推送，并确认最终工作区clean。

### Git状态

实现提交已推送；本条日志尚待收尾提交与同步。

## WR-20260717-020 — 完成任务7本地GPU预检与temporal运行加速

- 时间：2026-07-17 23:08:01 +08:00
- 类型：PROGRESS | TEST | FIX | EXPERIMENT
- 任务/门：20-M3 / 总纲任务20第7项正式run准备
- 状态：准备完成；正式dev调参待固定clean commit后启动
- 负责人：Codex

### 背景与目标

用户要求完成任务7，并已允许优先使用本地3070 Ti。官方VC-CSA固定snapshot缺少模型代码且依赖目标评论，不能冒充当前T0分布预测的官方复现；本批继续执行已登记的冻结I3D temporal-attention强视觉重实现，并在正式运行前验证本地GPU、资产fixity、test负门和预计耗时。

### 实际变更

- 本地GPU预检确认PyTorch 2.4.1+cu121识别NVIDIA GeForce RTX 3070 Ti Laptop GPU；任务20独立环境CUDA可用。
- 复跑CSMV feature preflight：8210个必需I3D文件hash/覆盖通过，许可、稳定revision和权利方包身份/fixity证明仍保持`DEFERRED_ACCEPTED_RISK`，未写成已解决。
- 运行32 train/16 dev、1 trial、2 epoch的本地GPU smoke，只评dev、不读取test。
- 全量5698 train/837 dev单epoch边界计时为30.4秒、峰值CUDA显存154 MiB。根因审计确认旧runner在每epoch重复打开数千个I3D文件，按早停耐心20估计原12-trial需约2–6小时。
- 在`tests/test_task20_temporal_runner.py`先新增“每个底层受限序列只读一次、不写内存数组”的测试并看到缺API预期失败；随后在`scripts/run_task20_temporal_attention.py`新增进程内只读memoization，不写磁盘、不缓存标签、不改变train-only标准化、模型、预算、split或指标。
- 优化后全量train/dev两epoch实测20.8秒，峰值CUDA显存154 MiB；12-trial常见早停预计20–60分钟，因此无需租新实例，也避免受限I3D外传。
- 更新`.planning/task20-m3/task_plan.md`、`findings.md`与`progress.md`，将任务7置为正式dev调参待启动。

### 验证与证据

- `nvidia-smi`及任务20 Python CUDA探针：exit 0，CUDA可用并识别本地3070 Ti。
- `.\.venv-task20\Scripts\python.exe scripts\validate_csmv_feature_preflight.py`：exit 0，`passed=true`、`required_file_hashes=8210`、未知权利状态fail-closed保留。
- `.\.venv-task20\Scripts\python.exe -m unittest tests.test_task20_temporal_runner tests.test_task20_training -v`：修改前11/11通过；新增测试首次因`memoize_sequence_loader`缺失失败，实现后12/12通过。
- GPU smoke runner：exit 0，状态`COMPLETED`、仅dev、smoke=true；本机run bundle位于Git忽略的`results/task20/temporal-attention-gpu-smoke-task7-20260717-a/`。
- 全量边界计时：旧路径1 epoch 30.4秒；新增只读内存缓存后2 epoch 20.8秒；两次均只用train/dev，不读取test。
- `.\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，53项全部通过。
- `.\.venv-task20\Scripts\python.exe -m compileall -q scripts tests`与`git diff --check`：exit 0。

### 影响与边界

正式temporal-attention运行不再为每个epoch重复打开I3D文件，但数据语义、FULL_SEQUENCE_DYNAMIC_PADDING_MASK、train-only拟合、12-trial预算、dev选择和test一次性规则完全不变。缓存只存在进程内，不落盘、不进入Git或run bundle。官方复现失败证据继续保留，强基线只能标记`REIMPLEMENTATION_STRONG_BASELINE`。

### 风险、问题与阻塞

- I3D许可、官方revision和权利方包身份/fixity仍未知；若后续权利方否认或8210 hash/覆盖漂移，必须标记`ASSET_INVALIDATED_DO_NOT_REPORT`。
- 8GB显存不是当前瓶颈；正式运行实际时长仍取决于各trial最佳epoch，若超出冻结200 epoch上限或出现OOM/非确定算子将如实失败，不缩减trial或改test规则。

### 下一步

1. 运行工作日志与准备检查，提交并推送当前缓存优化，使正式run绑定clean commit。
2. 从固定commit执行12-trial dev选择，冻结selection后对test评测一次。

### Git状态

本条写入时改动尚未提交或推送，工作区非clean；所有I3D与`results/`产物保持Git忽略。

## WR-20260717-021 — 完成任务7强视觉基线正式单种子运行

- 时间：2026-07-17 23:27:02 +08:00
- 类型：PROGRESS | EXPERIMENT | TEST | DOC
- 任务/门：20-M3 / 总纲任务20第7项
- 状态：完成（强视觉重实现）；官方VC-CSA复现失败状态保留
- 负责人：Codex

### 背景与目标

在固定官方snapshot缺少VC-CSA模型代码、且官方目标评论输入不符合T0合同的前提下，按任务7“至少一个官方/强基线”分支完成冻结I3D temporal-attention强视觉重实现的正式dev选择与单种子test一次评测。运行必须绑定clean commit、train-only拟合、dev调参和不可适配的test路径。

### 实际变更

- dev正式run绑定clean提交`14027a088de2ad1e003ff58fe523aa57718ab1e5`，本地3070 Ti、PyTorch 2.4.1+cu121、float32、AMP关闭，`group_by_video_v1`为5698 train/837 dev。
- 完整执行冻结12-trial搜索，按JSD、NLL、Brier、参数量选择trial 4：hidden=128、dropout=0.3、learning_rate=0.001、best epoch=5；dev JSD=0.177014。
- 冻结`selection.json` SHA-256 `dce53eeb8f3d618d2ed6e09fecc49164a0e6ac72b5254a065ebf4f493c97dfbf`；随后仅一次启动test runner，使用train拟合、dev早停、test前向，未再搜索或适配。
- test共1675条预测；JSD=0.182668、NLL=1.715192、EMD=0.162983、Brier=0.227379、ECE=0.053885、ACE=0.054004、AURC=0.175399、Macro-F1=0.137048、Balanced Accuracy=0.148577。
- test重训产生的dev JSD与冻结selection完全一致；test predictions SHA-256为`ca7276b759248ef0c8fcc17ee1ea98bafcb88d41161d4e1feec6251d698bba9f`，metrics SHA-256为`05f4785cc084bfc8ebe04a8f1d035ac81c97d127347dc4712cd1fe25fa2aeb7e`，manifest SHA-256为`0f5949a8dce4922dcb2559054370288f1e037408b722d3b68b0d0432c0539186`。
- 更新`BASELINE_TABLE_V1.md`、`TASK20_BASELINE_EXECUTION_AUDIT.md`、`experiments/EXPERIMENT_REGISTRY.md`、`TASK20_G3_EVIDENCE_DRAFT.md`及`.planning/task20-m3/`三份规划记录。

### 验证与证据

- dev runner：exit 0，12/12 trial、`status=COMPLETED`、耗时约13分30秒、`fit_scope=train_only`、`test_visible_during_selection=false`、git dirty=false。
- dev bundle核查：selection hash冻结、manifest提交一致、路径扫描`PASS`；8210必需I3D hash/覆盖在test前再次预检通过。
- test runner：exit 0，唯一冻结配置、`evaluation_split=test`、`test_adaptation=false`、`smoke=false`、`redistribution=PROHIBITED`、耗时约91秒。
- test bundle核查：1675条predictions、1条trial、frozen selection输入hash一致、路径扫描`PASS`；未发现本机路径或原始I3D序列。
- `.\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，53项全部通过。
- `.\.venv-task20\Scripts\python.exe -m compileall -q scripts tests`与`git diff --check`：exit 0。

### 影响与边界

任务7以`COMPLETED_VIA_REIMPLEMENTATION_STRONG_BASELINE_SINGLE_SEED`闭合。VC-CSA官方复现仍为`FAILED_OFFICIAL_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH`，不得删除或改写。单种子数值可进入baseline-table-v1的受限正式行，但任务50五种子统计与正式paired bootstrap尚未完成，不能写成最终论文优越性结论。

### 风险、问题与阻塞

- 运行继续受`DEFERRED_ACCEPTED_RISK`约束；I3D许可、官方revision和权利方包身份/fixity仍未知。若权利方否认或8210 hash/覆盖漂移，立即标记`ASSET_INVALIDATED_DO_NOT_REPORT`。
- 本地run bundle含模型权重与标准化器，只供内部复核，保持Git忽略且禁止提交、发布或再分发。

### 下一步

1. 运行工作日志验证、准备检查、全量测试与diff check，提交并推送聚合证据，不提交`results/`。
2. 后续任务15/16/18继续完成其余正式比较、paired bootstrap、重复运行与最终G3包。

### Git状态

本条写入时聚合文档和日志尚未提交或推送，工作区非clean；正式run bundle保持Git忽略。

## WR-20260717-022 — 完成任务7证据批次提交前门禁

- 时间：2026-07-17 23:30:59 +08:00
- 类型：TEST | VALIDATION
- 任务/门：20-M3 / 任务7提交前门禁
- 状态：验证通过
- 负责人：Codex

### 背景与目标

对任务7正式run的聚合证据、baseline-table更新、实验登记、G3草案和工作记录执行提交前完整门禁；本条只记录验证事实。

### 实际变更

- 未修改模型、selection、test结果、总纲、G门或数据manifest；仅追加本次验证记录。

### 验证与证据

- 两个正式dev/test `run-manifest.json`均通过`configs/task20/run-manifest.schema.json`校验，`RUN_MANIFEST_SCHEMA=PASS count=2`。
- `.\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，53项全部通过。
- `.\.venv-task20\Scripts\python.exe -m compileall -q scripts tests`与`git diff --check`：exit 0。
- `.\.venv\Scripts\python.exe scripts\validate_work_log.py`：exit 0，86条记录、最新`WR-20260717-021`、`passed=true`。
- `.\.venv\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`secret_scan.hits=[]`；默认环境继续诚实报告无faiss。
- `.\.venv-task20\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`secret_scan.hits=[]`、`formal_model_work_ready=true`。
- Git diff仅涉及任务7聚合文档、实验登记、G3草案、规划和WORK_LOG；`results/`与I3D资产未出现。

### 影响与边界

任务7证据批次达到当前仓库提交门要求；验证不升级I3D资产权利状态，不替代任务50统计或00的G3验收。

### 风险、问题与阻塞

无新增失败。`DEFERRED_ACCEPTED_RISK`、VC-CSA官方复现失败和剩余任务15–18工作继续保留。

### 下一步

复跑因本条新增而变化的工作日志/准备检查，随后有意提交并推送任务7聚合证据；继续排除所有run bundle。

### Git状态

本条写入时尚未提交或推送，工作区非clean。

## WR-20260717-023 — 提交并同步任务7正式强基线证据

- 时间：2026-07-17 23:32:45 +08:00
- 类型：PROGRESS | SYNC
- 任务/门：20-M3 / 总纲任务20第7项
- 状态：任务7证据已提交并推送
- 负责人：Codex

### 背景与目标

将已通过门禁的任务7单种子强视觉基线聚合证据、baseline-table、实验登记、G3草案、规划和工作日志同步到`main`；run bundle继续只保留本机。

### 实际变更

- 提交`aa9140fc873d582a5b3f7920a4637dc4b6fbaa2e`，提交说明为`docs(task20): record strong baseline formal run`，共8个文件、129行新增、12行删除。
- 使用本机一次性代理配置推送`main`；远端`origin/main`从`14027a088de2ad1e003ff58fe523aa57718ab1e5`前进到`aa9140fc873d582a5b3f7920a4637dc4b6fbaa2e`。
- 总纲、G门、00授权文件、数据manifest、I3D `.npy`、模型权重、预测、standardizer和`results/`均未进入提交。

### 验证与证据

- `git push origin main`使用一次性本机代理：exit 0，输出`main -> main`。
- `git rev-parse HEAD`与`git rev-parse origin/main`均为`aa9140fc873d582a5b3f7920a4637dc4b6fbaa2e`。
- 推送后`git status --short --branch`为`## main...origin/main`。

### 影响与边界

任务7的官方复现失败证据与替代强基线单种子正式结果已在远端仓库可审计；同步不等于任务50五种子统计完成，不改变资产风险或G门。

### 风险、问题与阻塞

I3D权利/fixity未知和`DEFERRED_ACCEPTED_RISK`继续保留；正式run bundle只在本机内部复核，禁止再分发。

### 下一步

复跑工作日志验证与准备检查，提交并推送本条同步记录，确认最终工作区clean。后续继续任务15–18剩余工作。

### Git状态

任务7证据提交已推送；本条同步记录尚待日志收尾提交。

## WR-20260717-024 — 实现任务15正式run一致性比较合同

- 时间：2026-07-17 23:42:01 +08:00
- 类型：FEATURE | TEST | PROGRESS
- 任务/门：20-M3 / 总纲任务20第15、16、18项启动
- 状态：比较器实现完成；正式dev replay待clean commit后执行
- 负责人：Codex

### 背景与目标

用户要求完成任务15、16、18。现有证据已覆盖smoke与单种子完整run，但正式全量GPU dev尚无独立同seed replay；任务16仍为部分表，任务18仍为未提交00的草案。本批先建立fail-closed的正式run比较合同，且不再次运行或查看test。

### 实际变更

- 新增`tests/test_task20_reproducibility.py`，覆盖clean Git提交不同但代码hash相同可比较、预测内容漂移必须失败、dirty run必须失败三条合同。
- 新增`scripts/compare_task20_runs.py`，先验证两侧manifest声明的全部artifact fixity，再比较experiment/model/fit scope/split/eval/seed/config/input/code/environment身份和`predictions.jsonl`、`metrics.json`、`selection.json`、`trial_results.json`四项核心产物hash。
- 比较报告边界固定为`SAME_ENVIRONMENT_FIXED_SEED`，明确不建立跨硬件或跨release bitwise复现结论。
- 更新`.planning/task20-m3/task_plan.md`、`findings.md`和`progress.md`，登记正式dev replay缺口、比较口径与下一步。

### 验证与证据

- 首次运行`.\.venv-task20\Scripts\python.exe -m unittest -v tests.test_task20_reproducibility`：exit 1，因`compare_task20_runs`不存在按预期红测失败。
- 实现后复跑同一命令：exit 0，3/3通过。
- `git diff --check`：exit 0。

### 影响与边界

任务15现在具备正式同seed run对的可审计比较入口；尚未执行全量replay，不得提前写成一致性已通过。比较只使用run bundle内哈希和脱敏元数据，不输出I3D序列、本机资产路径或可逆受限资产。

### 风险、问题与阻塞

- `rg`在当前Windows会话被系统拒绝执行；已改用PowerShell原生只读检索，未重复同一失败。
- I3D许可、官方revision和权利方包身份/fixity仍未知；若权利方否认或8210 hash/覆盖漂移，立即停止并标记`ASSET_INVALIDATED_DO_NOT_REPORT`。

### 下一步

1. 运行全量测试与项目门禁，提交并推送比较器代码，使正式replay绑定clean commit。
2. 复跑I3D preflight后执行一次全量dev同seed replay，仅比较dev产物，不再次评测test。
3. 冻结任务16表格，形成任务18最终G3证据包并提交00任务。

### Git状态

本条写入时比较器、测试和规划记录尚未提交或推送，工作区非clean。

## WR-20260717-025 — 完成任务15比较器代码批次提交前门禁

- 时间：2026-07-17 23:43:50 +08:00
- 类型：TEST | VALIDATION
- 任务/门：20-M3 / 任务15正式replay准备
- 状态：验证通过
- 负责人：Codex

### 背景与目标

在正式全量dev replay前，为新增一致性比较器建立clean Git基线，并执行项目要求的全量测试、工作日志验证、准备检查、编译和diff门禁。

### 实际变更

- 未改变比较逻辑、模型、配置、split、test结果、总纲或G门；仅追加本次验证记录。

### 验证与证据

- `.\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，56/56通过。
- `.\.venv\Scripts\python.exe scripts\validate_work_log.py`：exit 0，89条记录、最新`WR-20260717-024`、`passed=true`。
- `.\.venv\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0、`blocking_checks=[]`、`secret_scan.hits=[]`；默认旧环境继续诚实报告faiss缺失和`formal_model_work_ready=false`。
- `.\.venv-task20\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0、`blocking_checks=[]`、`secret_scan.hits=[]`、`formal_model_work_ready=true`。
- `.\.venv-task20\Scripts\python.exe -m compileall -q scripts tests`与`git diff --check`：exit 0。
- 比较器对既有正式dev bundle自比较：exit 0，四项核心产物fixity和hash均匹配。

### 影响与边界

新增代码已达到提交门要求，可用于任务15同环境同seed dev replay比较；尚未执行replay，不提前声明任务15完成。

### 风险、问题与阻塞

无新增阻塞。默认旧环境faiss缺失不是独立任务20正式环境状态；资产权利未知风险继续保留。

### 下一步

提交并推送本批比较器代码，确认工作区clean；随后复跑资产预检并启动全量dev replay。

### Git状态

本条写入时变更尚未提交或推送，工作区非clean。

## WR-20260718-001 — 完成任务15 replay与任务16表格并生成任务18 G3包

- 时间：2026-07-18 00:00:26 +08:00
- 类型：EXPERIMENT | TEST | DOC | PROGRESS
- 任务/门：20-M3 / 总纲任务20第15、16、18项
- 状态：任务15、16完成；任务18证据包待提交推送后发送00
- 负责人：Codex

### 背景与目标

在clean比较器提交后完成正式同seed replay，冻结baseline-table-v1，并形成不自行修改G门、可交00独立审查的G3证据包。

### 实际变更

- 比较器代码提交`f6a8363bc79144775d63c9bd62f149ce51cb9ff7`已推送；随后在clean工作区以本地3070 Ti、seed `20260717`、5698 train/837 dev、完整12-trial执行attempt 2 replay。
- replay耗时833秒，状态`COMPLETED`；只读取train/dev，未再次运行或查看test。
- 比较报告确认原正式dev与replay的config、inputs、代码文件hash、环境、seed、split相同，predictions、metrics、selection、trial_results四项SHA-256完全一致；model state与standardizer SHA-256也一致。
- 将`BASELINE_TABLE_V1.md`冻结为任务16 v1，明确官方复现尝试、重实现、legacy兼容与reference model四类证据身份。
- 新增`TASK20_G3_EVIDENCE_PACKAGE_20260718.md`，逐项映射1–18证据、正式数值、验证门和必须传播的风险；原`TASK20_G3_EVIDENCE_DRAFT.md`标记为被正式包取代。
- 更新`TASK20_BASELINE_EXECUTION_AUDIT.md`、`experiments/EXPERIMENT_REGISTRY.md`和`.planning/task20-m3/`三份规划文件。

### 验证与证据

- 运行前`nvidia-smi`确认本地3070 Ti可见；`validate_csmv_feature_preflight.py` exit 0、8210 required hash/覆盖通过，未知权利状态保留。
- 正式runner exit 0；开始`2026-07-17T23:45:27.082220+08:00`，结束`2026-07-17T23:59:17.474389+08:00`。
- `compare_task20_runs.py` exit 0、`passed=true`、`matching_artifacts=4`；核心hash为predictions `e08c5b3d...cbf`、metrics `0271a654...100`、selection `dce53eeb...fbf`、trial results `b5a246c3...f1f`。
- replay manifest schema：`PASS`；manifest SHA-256 `2b5b3473473ffe1d50435d2838642de1cae00b6618b29f93df79a5facfcfde3d`；比较报告SHA-256 `5d85fa1dbfdd263e5c5086e57bab3ce5305af4c340e28cf4315a1bbcbea1458d`。
- replay文本产物绝对路径扫描无命中；run bundle继续位于Git忽略范围。

### 影响与边界

任务15以smoke、单种子完整run和正式dev同seedreplay闭合；任务16交付冻结。任务18目前只完成包生成，必须在提交推送后实际发送00才能标记完成。replay不增加test查看次数，也不替代任务50五种子统计。

### 风险、问题与阻塞

I3D许可、官方revision和权利方包身份/fixity仍未知；资产状态继续为`DEFERRED_ACCEPTED_RISK`。若权利方否认或8210 hash/覆盖漂移，立即标记`ASSET_INVALIDATED_DO_NOT_REPORT`。同seed一致性不外推跨硬件或跨release绝对复现。

### 下一步

1. 运行全量测试、日志验证、准备检查和diff门，提交并推送任务15/16/18证据批次。
2. 将远端commit与正式G3包指针发送00任务，记录实际提交状态；不预填G3 PASS。

### Git状态

本条写入时证据文档和规划更新尚未提交或推送；正式run bundle保持Git忽略。

## WR-20260718-002 — 完成任务15至18证据批次提交前门禁

- 时间：2026-07-18 00:03:32 +08:00
- 类型：TEST | VALIDATION
- 任务/门：20-M3 / 任务15、16、18证据交付
- 状态：验证通过
- 负责人：Codex

### 背景与目标

对正式replay证据、冻结baseline-table-v1和G3提交包执行提交前全量门禁，确保不把本机run bundle、受限资产、秘密或未通过状态带入Git。

### 实际变更

- 未修改模型、运行结果、split、总纲或G门；仅追加本次验证记录。

### 验证与证据

- `.\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，56/56通过；随后`compileall` exit 0。
- `.\.venv\Scripts\python.exe scripts\validate_work_log.py`：exit 0，91条记录、最新`WR-20260718-001`、`passed=true`。
- 默认`.venv`准备检查：exit 0、`blocking_checks=[]`、`secret_scan.hits=[]`；旧环境faiss缺失与`formal_model_work_ready=false`继续保留。
- `.venv-task20`准备检查：exit 0、`blocking_checks=[]`、`secret_scan.hits=[]`、`formal_model_work_ready=true`。
- replay run manifest schema通过；`git diff --check` exit 0。
- `git check-ignore -v`确认replay `run-manifest.json`及其父目录由`.gitignore`的`results/`规则排除。

### 影响与边界

任务15/16/18证据文件达到提交门要求；任务18仍需在远端commit可见后实际发送00任务，不能仅以文件存在替代提交。

### 风险、问题与阻塞

无新增阻塞。资产权利未知、VC-CSA官方复现失败、单种子统计边界继续在G3包中显式传播。

### 下一步

有意提交并推送证据批次，随后将commit和G3包指针发送00任务，再记录任务18实际提交状态。

### Git状态

本条写入时证据批次尚未提交或推送，工作区非clean。

## WR-20260718-003 — 向新00总控提交任务20 G3证据

- 时间：2026-07-18 00:05:36 +08:00
- 类型：PROGRESS | SYNC | DOC
- 任务/门：20-M3 / 总纲任务20第18项
- 状态：任务18完成；G3结论待00独立审查
- 负责人：Codex

### 背景与目标

任务18要求把G3证据提交00。旧总控已迁移，因此必须确认并发送给新的00总控任务，而不是把证据发回旧长上下文线程。

### 实际变更

- 任务15/16/18证据提交`b89d8dc1d62b5d6ea7b07b1d30cc8f19224c030d`已推送`main`，本地与`origin/main`一致。
- 只读核对旧总控迁移记录和新00线程，确认当前新00总控任务ID为`019f6e64-0635-7ac0-a70a-65445b0fc1d1`。
- 向新00发送正式审查请求，包含commit、`TASK20_G3_EVIDENCE_PACKAGE_20260718.md`、任务15同seed复跑证据、任务16分类表、56/56测试、I3D accepted-risk和强制止损边界。
- 将G3包状态更新为`SUBMITTED_TO_00_PENDING_REVIEW_WITH_ACCEPTED_ASSET_RISK`，规划批次F标记完成；不修改总纲或G门。

### 验证与证据

- 推送`b89d8dc`：exit 0，`main -> main`；`HEAD`与`origin/main`均为完整hash `b89d8dc1d62b5d6ea7b07b1d30cc8f19224c030d`。
- 新00线程只读核对成功，标题为总控02、工作目录为隔离worktree。
- `send_message_to_thread`返回成功并确认目标threadId `019f6e64-0635-7ac0-a70a-65445b0fc1d1`。

### 影响与边界

任务18的证据提交动作已经完成；G3是否接受仍完全由00独立裁定。未创建任务30，未把单种子结果写成任务50完成，未提交run bundle或受限资产。

### 风险、问题与阻塞

无新增技术阻塞。00隔离worktree可能落后于main，因此消息明确要求以`origin/main@b89d8dc`刷新现实。I3D未知权利状态与`ASSET_INVALIDATED_DO_NOT_REPORT`止损继续保留。

### 下一步

等待00独立审查；若返回补证请求，只按其明确缺口处理，不自行扩大实验或G门。

### Git状态

本条状态收尾和规划更新尚待日志提交推送；证据主体`b89d8dc`已在远端可见。
## WR-20260718-004 — 00独立审查任务20 G3证据包
- 时间：2026-07-18 01:30:00 +08:00
- 类型：AUDIT | TEST | DECISION | RISK
- 任务/门：00-总控 / 任务20 G3
- 状态：补证挂起，未判G3 PASS
- 负责人：Codex

### 背景与目标
对任务20提交的`b89d8dc`、`TASK20_G3_EVIDENCE_PACKAGE_20260718.md`及配套审计材料进行独立审查，不直接采纳任务20自报的G3结论。

### 实际变更
- 刷新并确认主仓库`main`与`origin/main`均为`b89d8dc`，工作区clean。
- 独立核对G3包、baseline表、执行审计、实验登记、run manifest schema、tuning plan及总纲任务20/ G3条款。
- 未修改任务20实验核心、总纲、G门或受限资产。

### 验证与证据
- `.\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，56/56通过。
- `.\.venv-task20\Scripts\python.exe scripts\validate_work_log.py`：exit 0，93条记录、无错误。
- `.\.venv-task20\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`formal_model_work_ready=true`、`faiss_available=true`、资产未知状态保持fail-closed。
- `.\.venv-task20\Scripts\python.exe -m compileall -q scripts tests`与`git diff --check`：均exit 0。
- G3包报告temporal-attention单种子test JSD=0.182668及dev replay四项核心产物逐字节一致；其边界明确为`SAME_ENVIRONMENT_FIXED_SEED`，不冒充任务50五种子或跨硬件复现。
- `Test-Path HANDOFF_20.md`：False。总纲第17节任务20必需产出明确要求`HANDOFF_20.md与G3报告`，当前`b89d8dc`缺少该文件。

### 影响与边界
裁定为`TASK20_EXECUTION_EVIDENCE=ACCEPTED_FOR_G3_REVIEW`、`G3=HOLD_FOR_SUPPLEMENT`，不是G3 PASS，也不是拒绝。VC-CSA仍为`FAILED_OFFICIAL_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH`；temporal-attention只能作为`REIMPLEMENTATION_STRONG_BASELINE`。I3D许可、官方revision、权利方身份/fixity仍未知，`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`继续传播；任务50五种子/bootstrap未完成。

### 风险、问题与阻塞
1. 缺失`HANDOFF_20.md`使任务20交付合同未闭合。
2. 强基线为项目重实现而非官方代码复现；最终G3文字必须继续区分两者，并给出可审计的“强基线可信复现”依据。
3. 在补证和00最终裁定前不得创建任务30。

### 下一步
1. 要求任务20补交与当前`b89d8dc`和证据hash绑定的`HANDOFF_20.md`，说明冻结输入、split、指标、调参预算、限制和未完成项。
2. 收到补证后00再次独立核对并作G3 PASS_WITH_LIMITATIONS或REJECT结论。

### Git状态
本审查记录为总控文档追加，尚未提交或推送；任务20提交`b89d8dc`保持不变。

## WR-20260718-005 — 生成与commit及证据hash绑定的HANDOFF_20补证

- 时间：2026-07-18 00:18:45 +08:00
- 类型：FEATURE | TEST | DOC | PROGRESS
- 任务/门：20-M3 / G3补证
- 状态：补证生成并通过专项验证；待提交推送和00最终复核
- 负责人：Codex

### 背景与目标

00独立审查确认任务20执行证据可进入G3复核，但总纲4.5必需产出`HANDOFF_20.md`在`b89d8dc`缺失，因此`G3=HOLD_FOR_SUPPLEMENT`。本批补交可离线核验的交接文件，并显式绑定提交hash与证据SHA-256。

### 实际变更

- 开工时发现00尚未提交的`WORK_LOG.md` WR-20260718-004与`.light/handoff/S03-task20-g3-review-hold.md`；任务20未stage或改写，先通知00固定其文件。00随后自行提交推送为`3273ab2926581a877f89d5adc7da591dbe1dba2d`。
- 新增`tests/test_task20_handoff.py`，覆盖commit原始字节匹配、SHA-256漂移fail-closed、单条证据commit覆盖、绝对/父目录路径拒绝和必需风险词。
- 新增`scripts/validate_task20_handoff.py`，从Git对象库读取声明commit的blob原始字节，核验SHA-256/长度；不需要受限I3D或本机run bundle。
- 新增`data/manifests/task20-handoff-v1.manifest.json`，绑定证据主体`b89d8dc1d62b5d6ea7b07b1d30cc8f19224c030d`、提交状态`aed141b78b0babe4bad10555f335587f983f479b`、22项tracked证据、4项运行时输入hash和12项本机run不可逆artifact hash。
- 新增`HANDOFF_20.md`，交接冻结输入、split、标签/T0、环境、九项指标、12-trial预算、baseline身份、正式run/replay、单种子结果、完成/未完成项、I3D止损和任务30继承合同。
- 更新G3证据包、manifest README及`.planning/task20-m3/`，状态保持补证待00最终复核，不修改总纲或G门。

### 验证与证据

- 首次`.\.venv-task20\Scripts\python.exe -m unittest -v tests.test_task20_handoff`：exit 1，因validator模块不存在按预期红测失败。
- validator最小实现后专项3/3通过；新增row-level commit覆盖测试首次因错误使用默认commit失败，修复后专项4/4通过。
- `validate_task20_handoff.py`：exit 0，`passed=true`、`tracked_evidence_checked=22`、`restricted_assets_required=false`。
- manifest SHA-256=`6d75e2190a50dc4a2191458d6d379a7d49a84f630d5ccf3eb27ac83294f96e91`；`HANDOFF_20.md` SHA-256=`5a503d90308781620b4e4a7c99b409e29f30cd0872fc6f8b51da6c580a9b56cb`。
- HANDOFF与manifest绝对路径扫描无命中；`git diff --check` exit 0。

### 影响与边界

总纲要求的交接文件现在已生成且可在00隔离worktree离线核验tracked证据；本批不复制run bundle、I3D `.npy`、模型权重、预测正文或本机路径。补证生成不等于G3通过，任务30继续冻结。

### 风险、问题与阻塞

- I3D许可、官方revision和权利方包身份/fixity仍未知，继续为`DEFERRED_ACCEPTED_RISK`；否认或8210 hash/覆盖漂移时标记`ASSET_INVALIDATED_DO_NOT_REPORT`。
- WR-20260718-004时间字段晚于本条实际写入时间；该记录归00所有并已提交，任务20按append-only规则不改写，只按真实当前时间记录本条。

### 下一步

1. 运行专项/全量测试、handoff validator、工作日志与准备检查。
2. 有意提交并推送补证文件，不包含00或受限资产的额外改动。
3. 将补证commit与HANDOFF/manifest SHA-256发送00，请其作最终G3裁定。

### Git状态

本条写入时任务20补证文件尚未提交或推送；00审查commit `3273ab2`已在`main`与`origin/main`。

## WR-20260718-006 — 完成HANDOFF_20补证提交前全量门禁

- 时间：2026-07-18 00:21:36 +08:00
- 类型：TEST | VALIDATION | RISK
- 任务/门：20-M3 / G3补证提交前门禁
- 状态：验证通过，待有意提交和推送
- 负责人：Codex

### 背景与目标

在提交`HANDOFF_20.md`及其证据manifest前执行项目强制门禁和任务20专项检查，确认交接hash可复核、测试无回归、正式环境可用，并继续区分旧默认环境与独立正式环境。

### 实际变更

- 未修改模型、split、实验结果、总纲或G门；仅追加本次真实门禁记录。
- 提交范围复核只包含任务20补证、配套测试/validator、manifest说明、G3证据包状态与任务20规划记录；00的审查文件已固定在父提交`3273ab2`，本批没有覆盖其内容。

### 验证与证据

- `.\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，60/60通过。
- `.\.venv-task20\Scripts\python.exe -m compileall -q scripts tests`：exit 0。
- `.\.venv-task20\Scripts\python.exe scripts\validate_task20_handoff.py`：exit 0，`passed=true`、`tracked_evidence_checked=22`、`restricted_assets_required=false`；HANDOFF SHA-256=`5a503d90308781620b4e4a7c99b409e29f30cd0872fc6f8b51da6c580a9b56cb`，manifest SHA-256=`6d75e2190a50dc4a2191458d6d379a7d49a84f630d5ccf3eb27ac83294f96e91`。
- `.\.venv\Scripts\python.exe scripts\validate_work_log.py`：exit 0，95条记录、最新`WR-20260718-005`、`passed=true`。
- `.\.venv\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`secret_scan.hits=[]`；旧默认环境继续如实为`formal_model_work_ready=false`、faiss缺失。
- `.\.venv-task20\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`secret_scan.hits=[]`、`formal_model_work_ready=true`、faiss可用。
- `git diff --check`：exit 0。

### 影响与边界

补证批次已达到提交门禁；正式环境已就绪不改变旧默认环境的历史状态。本批仍不携带I3D `.npy`、run bundle、模型权重、预测正文、本机绝对路径或其他可逆受限资产。

### 风险、问题与阻塞

G3仍为`HOLD_FOR_SUPPLEMENT_PENDING_00_FINAL_REVIEW`，任务20不自行裁定。I3D许可、官方revision及权利方包身份/fixity仍未知；任何权利否认或8210 hash/覆盖漂移继续触发`ASSET_INVALIDATED_DO_NOT_REPORT`。

### 下一步

有意提交并通过本机7890代理推送`main`，核对远端commit后把补证hash发送新00总控做独立最终G3裁定。

### Git状态

本条写入时补证批次尚未提交或推送，工作区非clean。

## WR-20260718-007 — 00最终裁定任务20 G3 PASS_WITH_LIMITATIONS
- 时间：2026-07-18 02:30:00 +08:00
- 类型：AUDIT | TEST | DECISION | SYNC
- 任务/门：00-总控 / 任务20 G3
- 状态：完成，带明确限制
- 负责人：Codex

### 背景与目标
任务20补交hash-bound `HANDOFF_20.md`后，00按要求刷新`origin/main@e49ef9e`并独立完成最终G3复核。

### 实际变更
- 新增`TASK00_G3_FINAL_REVIEW_20260718.md`，记录独立裁定与证据hash。
- 未修改任务20实验核心、总纲、G1/G2或受限资产。

### 验证与证据
- `.\.venv-task20\Scripts\python.exe scripts\validate_task20_handoff.py`：exit 0，`passed=true`、`tracked_evidence_checked=22`、`restricted_assets_required=false`。
- 独立SHA-256：`HANDOFF_20.md=5a503d90308781620b4e4a7c99b409e29f30cd0872fc6f8b51da6c580a9b56cb`；handoff manifest=`6d75e2190a50dc4a2191458d6d379a7d49a84f630d5ccf3eb27ac83294f96e91`。
- `.\.venv-task20\Scripts\python.exe -m unittest discover -v tests`：exit 0，60/60通过。
- `.\.venv-task20\Scripts\python.exe scripts\validate_work_log.py`：exit 0，96条记录、无错误。
- `.\.venv-task20\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0，`blocking_checks=[]`、`formal_model_work_ready=true`。
- `.\.venv-task20\Scripts\python.exe -m compileall -q scripts tests`：exit 0。

### 影响与边界
最终裁定为`G3=PASS_WITH_LIMITATIONS`。允许按总纲启动条件进入任务30后续流程，但不能将temporal-attention写成VC-CSA官方复现，不能把单seed写成任务50统计结论，也不解除I3D`DEFERRED_ACCEPTED_RISK`。

### 风险、问题与阻塞
VC-CSA官方复现失败、I3D许可/revision/权利方fixity未知、任务50五种子/bootstrap未完成均继续传播；权利否认或8210 hash/覆盖漂移时必须`ASSET_INVALIDATED_DO_NOT_REPORT`。

### 下一步
1. 任务30启动前读取`HANDOFF_20.md`、handoff manifest、T0 policy、experiment protocol和冻结调参计划。
2. 任务30不得修改任务20冻结split、评测器、class order和test规则。

### Git状态
本条与最终审查记录尚未提交或推送。

## WR-20260718-008 — 推送HANDOFF_20补证并接收00最终G3裁定

- 时间：2026-07-18 00:28:30 +08:00
- 类型：PROGRESS | SYNC | DOC
- 任务/门：20-M3 / G3补证收尾
- 状态：任务20补证完成；00独立裁定G3 PASS_WITH_LIMITATIONS
- 负责人：Codex

### 背景与目标

完成总纲必需`HANDOFF_20.md`缺口的可审计提交与远端同步，并接收00基于该补证形成的独立最终G3裁定。

### 实际变更

- 任务20补证主体已创建提交`e49ef9e57cac2b072d638811e68b621ec254e6d2`（`docs(task20): add hash-bound handoff supplement`）并通过本机7890代理推送`main`。
- 向新00总控任务`019f6e64-0635-7ac0-a70a-65445b0fc1d1`发送补证commit、HANDOFF/manifest SHA-256、22项证据校验结果、环境差异和全部风险边界。
- 00独立复核后新增`TASK00_G3_FINAL_REVIEW_20260718.md`与WR-20260718-007，裁定`G3=PASS_WITH_LIMITATIONS`；任务20不改写其裁定正文。
- 更新G3包和任务20规划状态以引用00裁定，不修改总纲、G1/G2或受限资产。

### 验证与证据

- 补证提交前`git diff --cached --check`：exit 0；暂存10个任务20补证文件。
- `git commit`：exit 0，提交`e49ef9e57cac2b072d638811e68b621ec254e6d2`，607 insertions、3 deletions。
- `git -c http.proxy=http://127.0.0.1:7890 -c https.proxy=http://127.0.0.1:7890 push origin main`：exit 0，`3273ab2..e49ef9e main -> main`；随后HEAD与`origin/main`一致。
- `send_message_to_thread`返回目标threadId `019f6e64-0635-7ac0-a70a-65445b0fc1d1`。
- 00记录的独立复核结果为handoff validator `passed=true`、`tracked_evidence_checked=22`、`restricted_assets_required=false`，HANDOFF/manifest SHA-256匹配，60/60测试通过，正式环境`formal_model_work_ready=true`。

### 影响与边界

`HANDOFF_20.md`缺失项和G3裁定均已闭合。任务30现可按总纲启动条件进入后续流程，但本批不创建；任务50五种子/bootstrap仍未完成。

### 风险、问题与阻塞

I3D许可、官方revision及权利方包身份/fixity仍未知，`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`不变；权利否认或8210 hash/覆盖漂移立即标记`ASSET_INVALIDATED_DO_NOT_REPORT`。VC-CSA官方代码缺失/目标输入不匹配失败状态及重实现强基线身份继续显式传播。

### 下一步

运行最终工作日志、准备检查、handoff validator和diff门禁，有意提交并推送00裁定记录及任务20收尾状态；不在本批创建任务30。

### Git状态

本条写入时最终审查文件与状态收尾尚未提交或推送，工作区非clean。

## WR-20260718-009 — 固定并推送任务20最终G3审查状态

- 时间：2026-07-18 00:32:51 +08:00
- 类型：SYNC | VALIDATION | PROGRESS
- 任务/门：20-M3 / G3最终收尾
- 状态：最终裁定与任务20状态已推送，工作区已核对clean
- 负责人：Codex

### 背景与目标

在00独立裁定`G3=PASS_WITH_LIMITATIONS`后，固定其审查文件和任务20状态收尾，并记录真实远端同步结果。

### 实际变更

- 有意提交`TASK00_G3_FINAL_REVIEW_20260718.md`、WR-20260718-007/008、G3证据包状态和任务20规划收尾；未修改总纲、G1/G2、实验核心或受限资产。
- 创建提交`e20a4eeffc644ee32ddc7a907108fd294f972e4c`（`docs(g3): record task20 final review`）并通过本机7890代理推送`main`。

### 验证与证据

- 提交前工作日志：98条、最新`WR-20260718-008`、`passed=true`；双环境准备检查均exit 0且`blocking_checks=[]`，正式`.venv-task20`为`formal_model_work_ready=true`，旧`.venv`继续如实为false/faiss缺失。
- handoff validator：exit 0，`passed=true`、`tracked_evidence_checked=22`、`restricted_assets_required=false`；`git diff --check` exit 0。
- `git commit`：exit 0，`e20a4eeffc644ee32ddc7a907108fd294f972e4c`，127 insertions、4 deletions。
- 代理push：exit 0，`e49ef9e..e20a4ee main -> main`；随后`HEAD`与`origin/main`均为`e20a4eeffc644ee32ddc7a907108fd294f972e4c`，工作区clean。

### 影响与边界

任务20交接缺口和G3独立裁定已在远端闭合。任务30可按总纲启动条件进入后续流程，但未在本批创建；任务50仍为`TASK50_NOT_COMPLETED`。

### 风险、问题与阻塞

I3D许可、官方revision及权利方包身份/fixity仍未知，`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`不变；权利否认或8210 hash/覆盖漂移立即标记`ASSET_INVALIDATED_DO_NOT_REPORT`。VC-CSA失败和重实现身份继续传播。

### 下一步

本批无剩余任务20补证工作；后续由总控按`PASS_WITH_LIMITATIONS`边界决定任务30启动。

### Git状态

本条写入前`main`、`origin/main`均为`e20a4eeffc644ee32ddc7a907108fd294f972e4c`且工作区clean；本条日志自身待提交推送。

## WR-20260718-010 — 定位VC-CSA作者实现并更正代码缺失结论

- 时间：2026-07-18 12:17:14 +08:00
- 类型：AUDIT | TEST | DECISION | PROGRESS
- 任务/门：20-M3 / 任务7补充证据
- 状态：作者代码已定位；依赖预检失败；尚未训练
- 负责人：Codex

### 背景与目标

用户提供`JackySnake/MSA-CRVI`候选仓库，要求重新核实此前“VC-CSA官方代码缺失”的判断，区分可克隆仓库、作者实现和T0协议资格。

### 实际变更

- 只读核验远端refs、GitHub仓库/PR元数据、commit历史、完整文件树、README、VC-CSA模型、dataset loader、训练/评测入口和shell脚本。
- 将作者fork以`--filter=blob:none --no-checkout`克隆至Git忽略的`downloads/MSA-CRVI-JackySnake-audit`，固定HEAD `3e8c42608f4e89bc2082c55760aa63535e8e276a`后进行静态预检；不把上游代码纳入项目Git。
- 更新`TASK20_BASELINE_EXECUTION_AUDIT.md`、实验登记和任务20规划事实：原“作者代码缺失”被更正为`AUTHOR_RELEASED_IMPLEMENTATION_LOCATED_PR3_OPEN_NOT_YET_REPRODUCED`，但历史官方main审计不删除。
- 未修改冻结评测器、split、任务7既有结果、G3裁定或总纲。

### 验证与证据

- `git ls-remote https://github.com/JackySnake/MSA-CRVI.git`：HEAD/main均为`3e8c42608f4e89bc2082c55760aa63535e8e276a`。
- GitHub API：该仓库是`IEIT-AGI/MSA-CRVI`的fork；官方PR #3标题`add source code`、状态open、未合并、head=`3e8c426`、base=`99d1424`；README联系人为论文第一作者Qi Jia。
- `git ls-tree -r --name-only HEAD`确认存在`source_vcssa/model_VCCSA.py`、`main.py`、`main_eval.py`、训练/评测脚本与配置。
- 代码检查确认dataset/model读取目标`comment_info.comment`并用RoBERTa编码，输出评论级opinion/emotion；原split为随机comment 7:1:2，因此不能直接进入本项目T0视频级分布主表。
- `.\.venv-task20\Scripts\python.exe -m compileall -q downloads/MSA-CRVI-JackySnake-audit/source_vcssa`：exit 0。
- `main.py --help`与`main_eval.py --help`：均exit 1，在CUDA前因`ModuleNotFoundError: en_vectors_web_lg`停止；作者环境清单未声明该依赖。脚本另有`video_feature`/`${video_feature_dir}`变量不一致和续行空格问题。
- 本轮未读取受限I3D、未运行训练、未调用GPU。

### 影响与边界

任务7官方复现的阻塞原因不再包括“找不到任何作者代码”，改为作者代码候选已定位但尚未完成依赖修复/原设定复现；目标评论与split不符合T0的科学边界完全不变。既有强基线仍是`REIMPLEMENTATION_STRONG_BASELINE`，不能改称VC-CSA。

### 风险、问题与阻塞

- PR未合并，作者forkrevision身份必须显式披露，不能写成官方main已发布。
- faithful原任务复现需RoBERTa、旧依赖、作者comment split和视频特征；T0适配必须另建实验且降为重实现。
- GPU当前没有被调用；可运行性在依赖/脚本修复前即失败，因此尚不存在GPU不可用结论。
- I3D许可/revision/权利方fixity风险继续为`DEFERRED_ACCEPTED_RISK`。

### 下一步

1. 先让00复核并更新G3限制措辞，不把代码定位自动写成复现成功。
2. 若继续任务7补充复现，冻结`3e8c426`、建立作者环境兼容/修复账本并先做无数据入口测试；需要GPU时优先检查用户租用实例，不可用立即报告。
3. 作者原设定复现与T0适配重实现分开配置、分开结果、分开命名。

### Git状态

本条写入时审计更正尚未提交或推送；上游fork克隆位于Git忽略目录。

## WR-20260718-011 — 推送VC-CSA代码资格更正并通知00

- 时间：2026-07-18 12:20:54 +08:00
- 类型：SYNC | PROGRESS | DOC
- 任务/门：20-M3 / 任务7补充证据
- 状态：更正已推送并提交00复核
- 负责人：Codex

### 背景与目标

固定作者代码定位、可运行性预检与T0边界更正，并将会影响G3限制措辞的新证据提交00总控。

### 实际变更

- 有意提交任务20执行审计、实验登记、规划事实和WR-20260718-010；上游作者代码克隆继续位于Git忽略目录。
- 向新00总控任务发送commit、作者fork/PR身份、入口预检失败和T0不匹配边界，请其更新“代码缺失”限制措辞但不把定位冒充复现成功。

### 验证与证据

- `git diff --cached --check`：exit 0；暂存5个任务20审计/登记/规划文件。
- `git commit -m "docs(task20): correct VC-CSA source availability"`：exit 0，commit `d5f22f7ca27d33612bebb55fae399bbb8dfe42ac`，83 insertions、1 deletion。
- 7890代理push：exit 0，`5e1e5e2..d5f22f7 main -> main`；随后HEAD与`origin/main`均为`d5f22f7ca27d33612bebb55fae399bbb8dfe42ac`，工作区clean。
- `send_message_to_thread`返回目标threadId `019f6e64-0635-7ac0-a70a-65445b0fc1d1`。

### 影响与边界

项目远端现已反映“作者实现已定位但未复现”的真实状态。G3现有强基线依据不自动失效；是否修订00最终审查措辞由00独立决定。

### 风险、问题与阻塞

原实现依赖/脚本尚需修复；PR未合并；目标评论和comment split仍不满足T0。I3D资产风险不变。本批未运行GPU。

### 下一步

等待00审查更正；如用户要求继续原设定复现，先建立冻结环境和补丁账本，再检查租用GPU可用性。

### Git状态

本条写入前`main`与`origin/main`均为`d5f22f7ca27d33612bebb55fae399bbb8dfe42ac`且工作区clean；本条同步记录自身待提交推送。

## WR-20260718-012 — 总控更正G3中的VC-CSA证据身份与限制措辞

- 时间：2026-07-18 13:05:00 +08:00
- 类型：AUDIT | DECISION | DOC | VALIDATION
- 任务/门：00-T-AFFC总控 / G3证据更正
- 状态：G3继续PASS_WITH_LIMITATIONS；作者实现已定位但尚未复现
- 负责人：Codex

### 背景与目标

独立复核任务20在`d5f22f7ca27d33612bebb55fae399bbb8dfe42ac`提交的新证据，纠正G3最终审查中已过时的“作者代码缺失”限制，同时防止把代码定位扩大成官方复现成功或T0资格。

### 实际变更

- 更新`TASK00_G3_FINAL_REVIEW_20260718.md`：将VC-CSA状态改为`AUTHOR_RELEASED_IMPLEMENTATION_LOCATED_PR3_OPEN_NOT_YET_REPRODUCED`，保留官方`main@99d1424`原审计时无代码为历史事实。
- 明确作者fork/上游PR #3身份、入口依赖与脚本预检失败、未运行GPU，以及目标comment、随机comment split、评论级输出与T0协议不匹配。
- 明确既有temporal-attention仍为`REIMPLEMENTATION_STRONG_BASELINE`，作者实现定位不使G3强基线依据失效；`G3=PASS_WITH_LIMITATIONS`不变。
- 新建`.light/handoff/S04-g3-vccsa-evidence-correction.md`，传播更正后的SSOT边界和下一会话提示词。
- 未修改总纲、G1/G2、冻结实验核心、I3D资产、任务50状态或IJCV隔离边界。

### 验证与证据

- 开工状态：`main`与`origin/main`均为`11f96fe`，工作区clean；该提交已固定任务20的WR-20260718-011同步记录。
- `light-orchestrator lifecycle.py intake --root D:\MMSA-CH-SIMS`：exit 0、`state=resume`、`blockers=[]`；其`next_action=stage 20`落后于实时G3裁定，仅作状态诊断，不用于回滚门状态。
- GitHub独立核验：`JackySnake/MSA-CRVI`页面标识为`IEIT-AGI/MSA-CRVI`的fork；上游PR #3标题`add source code`、状态Open、目标`IEIT-AGI:main`、来源`JackySnake:main`，提交链末端显示`3e8c426`。
- 作者fork README独立核验：任务输入包含视频和评论，输出评论级opinion/emotion；train/dev/test为随机comment ID的7:1:2划分，与T0禁用目标评论及`group_by_video_v1`不匹配。
- 任务20已提交审计记录的静态预检：compileall exit 0；两个入口因`en_vectors_web_lg`缺失exit 1；本轮无GPU运行。
- 提交前门禁结果见本条后续追加记录；失败不会删除或改写。

### 影响与边界

G3维持`PASS_WITH_LIMITATIONS`，但“当前作者代码缺失”不再是有效措辞。代码定位不等于上游main发布、环境可运行、faithful reproduction成功或T0官方复现；VC-CSA不得进入T0统一主表，除非后续建立边界清晰的独立适配实验，并仍按重实现报告。

### 风险、问题与阻塞

- PR仍open且未合并，作者fork revision必须固定并披露。
- 依赖清单与shell脚本存在已知缺陷，尚无GPU或训练级复现证据。
- I3D许可、官方revision、权利方包身份/fixity仍未知；`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`不变，权利否认或8210 hash/覆盖漂移即`ASSET_INVALIDATED_DO_NOT_REPORT`。

### 下一步

执行工作日志、准备检查和diff门禁；有意提交并推送00更正文档、WR-20260718-012与S04交接卡。继续监督任务树，避免把作者原任务复现与T0适配混写。

### Git状态

本条写入时上述00文件尚未提交或推送，工作区非clean。

## WR-20260718-013 — 完成G3证据更正门禁并记录任务20重跑授权状态

- 时间：2026-07-18 13:14:00 +08:00
- 类型：VALIDATION | SYNC | RISK
- 任务/门：00-T-AFFC总控 / G3证据更正收尾
- 状态：更正文档门禁通过；待提交推送
- 负责人：Codex

### 背景与目标

闭合WR-20260718-012承诺的提交前验证，并记录任务20在总控审查期间收到的最新用户授权和GPU可用性边界。

### 实际变更

- 运行AGENTS要求的工作日志与准备检查，并复核任务20隔离环境和hash-bound handoff。
- 在S04补记：用户已授权任务20用作者代码重跑和修复依赖/脚本；租用A30当前connection refused，任务20先在本地3070 Ti做TDD/smoke。
- 未执行作者代码、未修改实验核心，也未把连接失败写成GPU训练失败或把本地smoke写成复现完成。

### 验证与证据

- `.\.venv\Scripts\python.exe scripts\validate_work_log.py`：exit 0，`passed=true`，102条，最新`WR-20260718-012`。
- `.\.venv\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0、`blocking_checks=[]`；旧环境继续如实显示formal CARM环境`faiss_available=false`、`formal_model_work_ready=false`。
- `.\.venv-task20\Scripts\python.exe scripts\run_preparation_checks.py`：exit 0、`blocking_checks=[]`、`formal_model_work_ready=true`。
- `.\.venv-task20\Scripts\python.exe scripts\validate_task20_handoff.py`：exit 0、`passed=true`、`tracked_evidence_checked=22`、`restricted_assets_required=false`。
- `git diff --check`：exit 0。
- 对双环境准备检查的重复摘要命令因120秒超时exit 124；没有据此覆盖前一轮已完整返回的真实结果，也未重复采用已知失败的`light-memory-pm pm.py`包装器。

### 影响与边界

G3仍为`PASS_WITH_LIMITATIONS`。重跑授权只扩展任务20可执行的作者代码兼容/复现工作，不授权修改T0冻结协议、不把faithful作者任务与T0适配混并，也不改变I3D接受风险。

### 风险、问题与阻塞

租用A30端点当前TCP/SSH connection refused；本地3070 Ti约6.47GB空闲是否足以全量运行尚未由任务20证明。依赖与脚本修复必须保留补丁账本，且不得越过作者原任务/T0适配身份边界。

### 下一步

提交并推送00更正文档、WR-20260718-012/013与S04；向任务20回传commit hash，随后持续监督其TDD、smoke和运行证据。

### Git状态

本条写入时上述00文件仍未提交或推送，工作区非clean。

## WR-20260718-014 — 修复VC-CSA作者原设定路径并完成本地GPU smoke

- 时间：2026-07-18 12:53:40 +08:00
- 类型：FEATURE | TEST | EXPERIMENT | RISK | PROGRESS
- 任务/门：20-M3 / 任务7补充复现
- 状态：作者原路径smoke可执行；全量因算力阻塞未启动
- 负责人：Codex

### 背景与目标

按用户授权使用作者代码重跑并解决已定位的依赖、脚本和入口问题；严格区分作者原comment级非T0复现与后续T0重实现，并优先检查租用GPU。

### 实际变更

- 新增`configs/task20/vccsa-author-original-v1.json`与`configs/task20/requirements-vccsa-author-lock.txt`，冻结作者fork revision、RoBERTa revision、环境版本、原comment/split身份和零test smoke合同。
- 新增`scripts/prepare_vccsa_author_reproduction.py`与`tests/test_vccsa_author_reproduction.py`；测试先红后绿，补丁器不复制作者源码，只修复可验证的死依赖/死导入、RoBERTa路径、shell变量/续行和未声明的禁用辅助任务默认值。
- 在Git忽略的作者checkout、独立环境和runtime目录完成补丁、模型快照、评论smoke输入与本地GPU运行；未提交作者代码、评论、I3D、权重、预测或本机绝对路径。
- 更新`TASK20_BASELINE_EXECUTION_AUDIT.md`、实验登记和任务20规划事实；未修改总纲、G门、T0评测核心或既有结果。

### 验证与证据

- 红测1：新测试模块因`prepare_vccsa_author_reproduction`不存在exit 1；随后最小实现后4/4通过。
- 红测2：无效dataset类导入、缺失`layers`死导入和`aux_task`未定义均先由真实入口/GPU堆栈暴露，再新增测试后修复；`main.py --help`与`main_eval.py --help`最终均exit 0。
- PyTorch首次安装：2.26GB官方wheel经pip下载时`ReadTimeoutError`、exit 1；可续传下载后安装成功。锁定环境实测Python 3.8.9、torch 1.13.1+cu117、CUDA 11.7可用、RTX 3070 Ti可见，NumPy 1.22.4、scikit-learn 1.2.1、transformers 4.26.1。
- GPU smoke：8 train / 4 dev / 0 test、batch 1、1 epoch；146.05439M参数，训练段约4秒，完整训练与dev评测exit 0且未OOM。小样本指标不具报告资格。
- 作者全split统计：train 75,086 / dev 10,727 / test 21,454；按smoke粗估本地单epoch约10.4小时、120 epoch约52天，且上游early stop未实现。
- 租用A30端点开工前及smoke后两次TCP检查均失败；这是连接不可达，不是GPU训练失败。全量未启动，已立即向用户报告需恢复可用GPU。

### 影响与边界

状态更新为`AUTHOR_ORIGINAL_PATH_SMOKE_EXECUTABLE_FULL_REPRODUCTION_BLOCKED_COMPUTE`，不得升级为完整作者复现、官方main复现或T0基线。T0适配继续要求独立`REIMPLEMENTATION`。I3D `DEFERRED_ACCEPTED_RISK`及`ASSET_INVALIDATED_DO_NOT_REPORT`止损条件不变。

### 风险、问题与阻塞

PR #3仍open/未合并；作者源码需任务20兼容补丁；RoBERTa作者未声明固定revision，本批显式冻结本地快照。全量需要可连接的高显存GPU，当前租用A30不可达；本地约52天估算不可接受。

### 下一步

运行全量单测、工作日志/准备检查和diff门禁；有意提交推送本批tracked证据。待用户恢复可连接GPU后，先锁定远端环境和数据合规路径，再运行作者原设定全量train/dev与预注册test评测。

### Git状态

本条写入时本批tracked改动尚未提交或推送；所有运行产物和上游源码均位于Git忽略目录。

## WR-20260718-015 — 完成VC-CSA兼容批次提交前门禁

- 时间：2026-07-18 12:58:00 +08:00
- 类型：VALIDATION | TEST | RISK
- 任务/门：20-M3 / 任务7补充复现
- 状态：提交前门禁通过；全量算力阻塞不变
- 负责人：Codex

### 背景与目标

在提交兼容补丁与smoke证据前，执行AGENTS要求的工作日志、准备检查、全量测试、handoff和diff门禁。

### 实际变更

本条只追加验证结果；未修改总纲、G门、实验核心或运行产物。

### 验证与证据

- `.venv-task20`全量unittest：64/64通过；新增VC-CSA专项4/4包含NON_T0身份、静默T0改名拒绝、补丁和零test smoke输入。
- `scripts/validate_work_log.py`：exit 0、104条、latest=`WR-20260718-014`、errors=[]。
- 默认`.venv`运行`scripts/run_preparation_checks.py`：exit 0、blocking_checks=[]；既有`faiss_available=false`使`formal_model_work_ready=false`，未改写为就绪。
- 正式`.venv-task20`运行同一准备检查：exit 0、blocking_checks=[]、`formal_model_work_ready=true`。
- `scripts/validate_task20_handoff.py`：exit 0、22项snapshot evidence通过、`restricted_assets_required=false`；旧handoff仍按其冻结commit字节验证，不被本次补充审计冒充重绑定。
- `git diff --check`与`scripts/tests compileall`均exit 0；secret scan无命中。

### 影响与边界

本批代码与文档具备提交条件，但只证明作者原路径可执行smoke；不证明全量复现、T0资格或I3D资产问题解决。

### 风险、问题与阻塞

默认`.venv`的faiss缺失和租用A30不可达继续如实保留；全量作者复现仍等待可用高显存GPU。

### 下一步

复跑日志与准备检查以覆盖本条新增记录，检查staged文件范围后提交并经7890代理推送main，随后向00同步状态。

### Git状态

本条写入时本批tracked改动未提交或推送，工作区非clean。

## WR-20260718-016 — 提交推送VC-CSA作者路径兼容批次

- 时间：2026-07-18 13:02:40 +08:00
- 类型：SYNC | PROGRESS
- 任务/门：20-M3 / 任务7补充复现
- 状态：代码与证据已提交推送
- 负责人：Codex

### 背景与目标

固定WR-20260718-014/015已验证的兼容补丁、冻结配置和smoke审计，并同步远端main。

### 实际变更

- 有意提交10个tracked代码、配置、测试、规划和审计文件；未纳入Git忽略的上游源码、环境、模型、数据或运行产物。
- 经本机7890代理推送main。

### 验证与证据

- `git diff --cached --check`：exit 0；staged范围10个预期文件。
- `git commit -m "feat(task20): enable VC-CSA author smoke"`：exit 0，commit `b173e38cde73ed813216c532b3966f28cfba45c0`，666 insertions、1 deletion。
- `git push origin main`：exit 0，`6644f2d..b173e38 main -> main`。
- 推送后`HEAD`与`origin/main`均为`b173e38cde73ed813216c532b3966f28cfba45c0`，工作区clean。

### 影响与边界

远端现可审计作者原路径smoke兼容实现；全量复现仍未完成，NON_T0与I3D风险边界不变。

### 风险、问题与阻塞

租用A30仍不可达，本地全量约52天；不得把smoke或提交成功扩写为作者全量复现。

### 下一步

提交并推送本条同步记录，向00总控发送代码hash、smoke状态、全量算力阻塞和风险边界。等待用户恢复可连接GPU。

### Git状态

本条写入前`main`与`origin/main`均为`b173e38cde73ed813216c532b3966f28cfba45c0`且工作区clean；本条日志自身待提交推送。

## WR-20260718-017 — 修复VC-CSA smoke输入隔离并建立post-snapshot勘误

- 时间：2026-07-18 13:15:04 +08:00
- 类型：FIX | TEST | DOC | AUDIT | RISK
- 任务/门：20-M3 / VC-CSA补充复现与G3后证据一致性
- 状态：输入隔离缺口已修复并重跑smoke；文档勘误已建立
- 负责人：Codex

### 背景与目标

00复核指出两项问题：执行审计仍把官方main历史失败写成当前状态；smoke构建器虽然写空`test_set.json`，却把含全量记录的作者源标注字典和video映射原样持久化，故“runtime物理无test”证据不足。

### 实际变更

- TDD修复`scripts/prepare_vccsa_author_reproduction.py`：构建器仍如实读取含全量记录的作者源压缩包，但持久化runtime的标注字典和video映射ID必须严格等于选中train/dev并集；缺失、额外ID或无法形成同视频peer均fail closed。
- 将真实smoke选择改为各自train/dev split内按作者顺序、仅选择可组成同视频peer的确定性子集；不读取test split作选择。
- 更新源码docstring，明确区分source read与runtime persistence。
- 修正`TASK20_BASELINE_EXECUTION_AUDIT.md`：旧`99d1424`代码缺失只保留为历史官方main尝试；当前状态为`AUTHOR_ORIGINAL_PATH_SMOKE_EXECUTABLE_FULL_REPRODUCTION_BLOCKED_COMPUTE`且NON_T0。
- 新建`TASK20_POST_SNAPSHOT_VCCSA_ERRATUM_20260718.md`，对G3 package、冻结baseline表和hash-bound handoff中的旧VC-CSA文字建立有限范围优先级；三份冻结文件保持字节不变。

### 验证与证据

- 新增含`te0`的负测后，旧实现出现两项预期失败：输出标注仍含`tr2/te0`，singleton peer未fail closed。最小修复后VC-CSA专项5/5通过。
- 真实旧“前8/前4”选择首次重建因一个视频只有单个selected peer而按新合同exit 1；改为确定性peer-safe选择后，runtime报告train=8、dev=4、test=0、annotation_ids=12、video_comment_ids=12，且两组ID集合严格一致。
- 使用新run名重跑本地GPU smoke：146.05439M参数、batch 1、1 epoch，训练约3秒，训练/dev完整exit 0且未OOM；smoke指标仍无报告资格。
- 冻结文件SHA-256保持：G3 package=`cf906a93c9cd1c8ad6c022d7bfe019d323ba19d0f6aa4bd7786a338c152248c6`；baseline表=`7a2b612c16ebe8110a67a4108877ae0aca4082d8b7ab7d87897dc48f6c651f44`；HANDOFF=`5a503d90308781620b4e4a7c99b409e29f30cd0872fc6f8b51da6c580a9b56cb`。
- `light-consistency`首次用系统Python运行因PyYAML缺失exit 1；改用`.venv-task20`后自测因skill安装缺`_shared/findings_schema`仍exit 1，`--report`无法生成`light.findings.v1`。改用其`--json`内部报告完成5份材料文本回扫，结果为2项warn/info、无该工具可识别的硬冲突；因仅有`.light/terminology.md`而无四份registry，结论明确为PARTIAL，不宣称全项目一致。

### 影响与边界

修复后可证明持久化smoke runtime物理排除test和未选择记录；同时诚实保留“构建器读取作者全量源压缩包”事实。首次smoke入口未迭代test，但旧runtime隔离证据不足；新smoke才闭合物理隔离证据。全量VC-CSA复现仍未完成，作者原任务仍为NON_T0。

### 风险、问题与阻塞

`light-consistency`缺`_shared`导致标准`light.findings.v1`与delta门不可用，只完成内部JSON部分覆盖回扫；该工具阻塞不影响项目自身单测、handoff或准备检查，但不得写成完整一致性门通过。租用A30不可达和I3D accepted-risk不变。

### 下一步

运行专项/全量测试、冻结hash、handoff、日志和双环境准备检查；检查diff与敏感资产边界后提交推送，并向00回传勘误和输入隔离闭合证据。

### Git状态

本条写入时上述代码、测试、执行审计、post-snapshot erratum和本日志尚未提交或推送，工作区非clean。

## WR-20260718-018 — 完成VC-CSA输入隔离补丁的提交前门禁

- 时间：2026-07-18 13:18:11 +08:00
- 类型：VALIDATION | TEST | AUDIT | RISK
- 任务/门：20-M3 / VC-CSA补充复现NON_T0证据一致性
- 状态：代码与文档门禁通过；待提交推送
- 负责人：Codex

### 背景与目标

验证WR-20260718-017记录的runtime输入物理隔离修复、post-snapshot勘误及冻结证据边界，确保本批只证明过滤后的作者路径smoke可执行，不把结果升级为全量复现。

### 实际变更

本条仅追加提交前验证结果；未改写总纲、G门、冻结G3 package、冻结baseline表、hash-bound handoff或实验指标。

### 验证与证据

- `.venv-task20`全量unittest：66/66通过，exit 0；新增覆盖含test记录的源压缩包、runtime精确ID集合、singleton peer fail-closed、冻结字节与勘误优先级。
- `scripts/validate_work_log.py`：exit 0，107条，latest=`WR-20260718-017`，`errors=[]`。
- 默认`.venv`运行`scripts/run_preparation_checks.py`：exit 0，`blocking_checks=[]`；继续如实报告`faiss_available=false`与`formal_model_work_ready=false`，未把旧环境写成已就绪。
- 正式`.venv-task20`运行同一准备检查：exit 0，`blocking_checks=[]`，`formal_model_work_ready=true`。
- `.venv-task20`运行`scripts/validate_task20_handoff.py`：exit 0，22项证据通过，`restricted_assets_required=false`。
- 冻结SHA-256复核不变：G3 package=`cf906a93c9cd1c8ad6c022d7bfe019d323ba19d0f6aa4bd7786a338c152248c6`；baseline表=`7a2b612c16ebe8110a67a4108877ae0aca4082d8b7ab7d87897dc48f6c651f44`；HANDOFF=`5a503d90308781620b4e4a7c99b409e29f30cd0872fc6f8b51da6c580a9b56cb`。
- `git diff --check`与scripts/tests `compileall`均exit 0；准备检查内secret scan无命中。
- `light-consistency`标准findings仍因skill安装缺`_shared/findings_schema`不可生成；仅有内部JSON部分回扫，故一致性结论保持PARTIAL而非完整通过。

### 影响与边界

本批具备提交条件。构建器读取包含全量记录的作者源压缩包，但持久化runtime只保留选中train/dev并物理排除test及未选择记录；这是source read与runtime persistence的精确边界。当前VC-CSA状态仍为`AUTHOR_ORIGINAL_PATH_SMOKE_EXECUTABLE_FULL_REPRODUCTION_BLOCKED_COMPUTE`、`NON_T0`。

### 风险、问题与阻塞

全量作者任务仍受可用高显存GPU阻塞；I3D许可、官方revision及权利方包身份/fixity仍未知。不得把本批smoke、输入隔离修复或勘误写成全量复现完成、T0合格或资产风险解除。

### 下一步

覆盖本条重跑AGENTS要求的工作日志与准备检查，检查staged范围后有意提交并经本机7890代理推送main；随后记录同步hash并向00回传。

### Git状态

本条写入时本批5个预期文件尚未提交或推送，工作区非clean。

## WR-20260718-019 — 提交推送VC-CSA输入隔离与post-snapshot勘误

- 时间：2026-07-18 13:21:40 +08:00
- 类型：SYNC | PROGRESS | AUDIT
- 任务/门：20-M3 / VC-CSA补充复现NON_T0证据一致性
- 状态：代码与证据已提交推送；本同步记录待提交
- 负责人：Codex

### 背景与目标

固定WR-20260718-017/018已验证的输入隔离修复、历史状态勘误和冻结快照优先级，并把实际远端同步结果写入审计链。

### 实际变更

- 有意提交5个文件：执行审计、post-snapshot勘误、工作日志、smoke输入构建器和专项测试。
- 未提交或改写冻结G3 package、冻结baseline表、hash-bound handoff、作者源码、数据、评论、模型、预测、运行产物或本机路径。
- 经本机7890代理推送`main`。

### 验证与证据

- `git diff --cached --check`：exit 0；staged范围严格为上述5个文件。
- `git commit -m "fix(task20): isolate VC-CSA smoke inputs"`：exit 0；commit=`1b91a9596de604bdf4279fda5416276b6f843e37`，344 insertions、22 deletions。
- `git push origin main`：exit 0；`14012c8..1b91a95 main -> main`。

### 影响与边界

远端现可审计：构建器会读取作者全量源压缩包，但只把选中train/dev记录持久化到runtime，物理排除test及未选择记录；旧快照中的过时VC-CSA状态由新勘误按限定范围覆盖。当前状态仍为`AUTHOR_ORIGINAL_PATH_SMOKE_EXECUTABLE_FULL_REPRODUCTION_BLOCKED_COMPUTE`、`NON_T0`，G3仍为`PASS_WITH_LIMITATIONS`。

### 风险、问题与阻塞

全量作者复现仍未完成且受可用高显存GPU阻塞；`light-consistency`标准findings依赖缺失仍只允许PARTIAL结论；I3D资产未知项和止损条件不变。

### 下一步

验证并提交推送本同步记录；确认`HEAD`与`origin/main`一致、工作区clean后向00回传最终hash和边界。

### Git状态

主补丁`1b91a9596de604bdf4279fda5416276b6f843e37`已推送；本条同步记录自身尚未提交或推送，工作区非clean。

## WR-20260718-020 — 00独立接受任务20 VC-CSA补充证据

- 时间：2026-07-18 13:31:00 +08:00
- 类型：AUDIT | DECISION | TEST | DOC
- 任务/门：00-T-AFFC总控 / 任务20 VC-CSA补充验收
- 状态：ACCEPTED_WITH_LIMITATIONS；全量复现仍受算力阻塞
- 负责人：Codex

### 背景与目标

基于任务20的`1b91a9596de604bdf4279fda5416276b6f843e37`与同步提交`820ce06de09c964b9f55e136cc09c4ba8cf6ad70`，独立审查post-snapshot勘误、smoke输入物理隔离补丁和重跑证据，不以任务20自报替代总控裁定。

### 实际变更

- 新建`TASK00_TASK20_VCCSA_SUPPLEMENT_REVIEW_20260718.md`，裁定`TASK20_VCCSA_SUPPLEMENT=ACCEPTED_WITH_LIMITATIONS`。
- 新建`.light/handoff/S05-task20-vccsa-supplement-accepted.md`，传播G3不变、NON_T0、source read/runtime persistence边界、算力阻塞和I3D风险。
- 未修改总纲、G1/G2/G3、冻结评测核心、任务50状态、hash-bound G3 package/HANDOFF、冻结baseline表或受限资产。

### 验证与证据

- 开工与远端：`main`、`origin/main`均为`820ce06de09c964b9f55e136cc09c4ba8cf6ad70`，工作区clean；任务20线程实时状态已读取。
- 00首次独立复跑补正前提交：专项4/4、全量64/64、日志106条、task20正式环境就绪、handoff 22项通过；组合命令第一次仅因10秒超时exit 124，120秒重跑exit 0。
- 00代码审查发现旧构建器把总标注和完整video映射持久化到runtime；任务20按红测修复后提交`1b91a95`，新测试覆盖test/unselected物理排除和singleton peer fail closed。
- 00对最终提交独立复跑：VC-CSA专项6/6、全量66/66，均exit 0；`validate_work_log.py`为109条、最新WR-019、`passed=true`；handoff validator为22项、`passed=true`、`restricted_assets_required=false`。
- 最终文档批次门禁：默认`.venv`的`validate_work_log.py` exit 0；`run_preparation_checks.py` exit 0、`blocking_checks=[]`、`faiss_available=false`、`formal_model_work_ready=false`；`.venv-task20`同检查exit 0、`blocking_checks=[]`、`faiss_available=true`、`formal_model_work_ready=true`；`git diff --check` exit 0。
- `light-orchestrator` intake返回resume、blockers=[]，但passport next_action仍是stage20且evidence_state=PLANNED，落后于项目专用SSOT；不据此回滚G3或补充验收。

### 影响与边界

接受过滤后作者原路径GPU smoke的可执行性与输入持久化边界证据。构建器读取全量作者源仍是事实；旧smoke只证明入口未迭代test，只有新smoke证明runtime物理排除test/未选择记录。当前状态为`AUTHOR_ORIGINAL_PATH_SMOKE_EXECUTABLE_FULL_REPRODUCTION_BLOCKED_COMPUTE`、`AUTHOR_ORIGINAL_SETTING_NON_T0`；`G3=PASS_WITH_LIMITATIONS`不变。

### 风险、问题与阻塞

- 全量作者复现尚未启动：A30不可达，本地120 epoch粗估约52天。
- I3D许可、官方revision、权利方包身份/fixity仍未知；权利否认或8210 hash/覆盖漂移立即`ASSET_INVALIDATED_DO_NOT_REPORT`。
- `light-consistency`因技能安装缺`_shared/findings_schema`仅完成PARTIAL回扫，未通过完整一致性门。

### 下一步

提交推送00验收单、WR-020与S05交接卡；持续监督可用GPU恢复和任务树边界，不把smoke冒充全量复现，不创建IJCV任务。

### Git状态

本条写入时上述00文件尚未提交或推送，工作区非clean。
## WR-20260718-021 — 完成新租用A6000的VC-CSA全量复现资源预检

- 时间：2026-07-18 16:20:09 +08:00
- 类型：VALIDATION | ENVIRONMENT | TEST | RISK | PROGRESS
- 任务/门：20-M3 / VC-CSA作者原设定NON_T0全量复现预检
- 状态：高显存GPU与冻结运行时可用；全量复现未启动
- 负责人：Codex

### 背景与目标

用户提供新的租用GPU，要求判断能否运行VC-CSA作者原设定全量复现。本批只验证连接、硬件、冻结环境、公开源码/模型和batch=16资源合同，不在资产边界未明确前上传受限I3D或启动全量实验。

### 实际变更

- 在租用实例建立独立`vccsa-author`环境，固定Python 3.8.20与任务20要求的PyTorch/NumPy/sklearn/transformers/easydict版本；未把平台预装PyTorch 2.5环境写成正式环境。
- 从公开来源固定作者fork`3e8c42608f4e89bc2082c55760aa63535e8e276a`和项目兼容补丁；幂等复核补丁未产生额外改动。
- 传输并逐文件核对公开RoBERTa冻结快照；未传输I3D、全量评论runtime、模型权重、预测或本机路径。
- 构造独立合成资源runtime，使用32 train、16 dev、0 test和最坏长度180×1024的合成视觉序列，仅用于显存/吞吐验证。
- 更新`TASK20_BASELINE_EXECUTION_AUDIT.md`，把远端状态从旧A30不可达更新为新A6000资源预检通过，同时保留“全量未启动”和NON_T0边界。

### 验证与证据

- SSH与硬件：认证成功；RTX A6000 48GB约48.7GB空闲，350GB磁盘、85GB可用内存，无其他GPU计算进程。
- 现成PyTorch 2.5.1+cu121环境CUDA矩阵通过，但因版本漂移未用于冻结实验。
- 冻结环境：Python 3.8.20、torch 1.13.1+cu117、NumPy 1.22.4、sklearn 1.2.1、transformers 4.26.1；CUDA可见A6000，4096平方矩阵有限。
- 串行PyTorch下载速度降至约0.29MiB/s后主动停止；16连接下载平均约12MiB/s，Linux wheel SHA-256=`bbf9546f0d0d8b51263ca479637b426a88335fca0034f42cec63d4d32dee05af`并通过校验。
- 失败1：首次本地wheel安装因`--no-index`无法解析`typing-extensions`而exit 1；补齐公开依赖并用`--no-deps`安装后成功。
- 作者源码兼容补丁二次运行`changed_files=[]`，revision验证正确，compileall exit 0；RoBERTa 15个文件hash mismatch为0。
- 合成合同：32 train/16 dev/0 test，annotation_ids=48、video_comment_ids=48、24个合成视频；真实受限I3D为0。
- 失败2：镜像缺`/usr/bin/time`导致Python入口前exit 127；移除非必要计时包装后继续。
- 失败3：16 train仅一个batch时完成batch=16训练步骤且未OOM，随后作者日志`elapsed/step`除零exit 1；不修改作者代码，改为32 train两个batch后完整训练/dev/checkpoint exit 0，约10秒，146.05439M参数，无OOM。合成指标无报告资格。
- 输入容量估算：固定8210项I3D约2.13GiB、公开RoBERTa约0.47GiB；作者每epoch checkpoint约1.66GiB，120轮约199GiB，远端350GiB技术上足够。
- 首次本机`run_preparation_checks.py`因忽略目录中的临时Paramiko依赖源码被secret scan识别为`private_key`模式而exit 1；命中位于第三方`cryptography`包且不含用户凭证。核对源目录位于项目`downloads`后，将该可再生临时工具目录整体移出工作区，再重跑门禁；失败未删除或改写。
- `.venv-task20`全量unittest 66/66通过。首次`validate_work_log.py`因WR-021误插入WR-012与WR-013之间而exit 1；在提交前将未提交新记录机械移至WR-020之后，随后111条、latest=`WR-20260718-021`、`passed=true`。
- 清理临时工具命中后，默认`.venv`的`run_preparation_checks.py` exit 0、`blocking_checks=[]`、secret scan无命中；正式`.venv-task20`同检查exit 0、`formal_model_work_ready=true`。
- `.venv-task20`运行`validate_task20_handoff.py`：exit 0，22项冻结证据通过，HANDOFF SHA-256仍为`5a503d90308781620b4e4a7c99b409e29f30cd0872fc6f8b51da6c580a9b56cb`，`restricted_assets_required=false`。
- `git diff --check` exit 0；tracked diff仅为执行审计与本工作日志，敏感连接信息、本机路径和密码模式回扫无命中。

### 影响与边界

旧状态`REMOTE_GPU_RUNTIME_UNAVAILABLE_ENVIRONMENT_NOT_READY`只描述先前A30。当前资源状态更新为`REMOTE_A6000_RUNTIME_READY_SYNTHETIC_BATCH16_RESOURCE_SMOKE_PASSED_FULL_REPRODUCTION_NOT_STARTED`。这证明高显存GPU、冻结环境与作者batch=16资源路径可执行，不证明作者全量结果、官方main复现、T0复现或跨环境bitwise一致。

### 风险、问题与阻塞

- 全量运行仍未启动。`asset_redistribution_allowed=false`不变；在明确远端暂存权限前，不得把受限I3D上传至租用平台。若获准，仍只能暂存固定8210项并逐文件复核hash/覆盖。
- Python patch版本为3.8.20而非本地3.8.9，须在run manifest披露；同主次版本与冻结包不等于跨环境bitwise一致。
- 作者`early_stop=5`未实现，120 epoch会实际执行并生成约199GiB checkpoint；正式run必须监控磁盘、进程和失败产物。
- I3D许可、稳定官方revision、权利方包身份/fixity未知项及`ASSET_INVALIDATED_DO_NOT_REPORT`止损条件不变。

### 下一步

1. 由用户/00明确租用实例是否属于获准的内部暂存边界；未明确前不上传I3D。
2. 若获准，只传固定8210项与公开/获准运行输入，完成远端hash/覆盖门和真实小规模batch=16 smoke。
3. 真实smoke通过后再预注册启动全量train/dev，test只在dev checkpoint选择冻结后评测。

### Git状态

本条写入时执行审计与WR-20260718-021尚未提交或推送；本机运行工具与远端产物均在Git忽略或远端隔离目录，不纳入仓库。

## WR-20260718-022 — 裁定租用A6000不属于既有I3D本地暂存边界

- 时间：2026-07-18 16:34:42 +08:00
- 类型：DECISION | AUDIT | RISK | DOC
- 任务/门：00-T-AFFC总控 / 任务20远端资产边界
- 状态：完成；真实I3D远端传输保持HOLD
- 负责人：Codex

### 背景与目标

任务20在`main@8a5d8a38684cb0a07ee9a76d56fcf6d01d6ac33b`提交新租用RTX A6000的冻结环境与合成batch=16资源预检，并请求00裁定租用实例是否已被既有`DEFERRED_ACCEPTED_RISK`内部暂存边界覆盖。目标是独立区分算力就绪与资产传输授权，防止把用户租用GPU或合成smoke推导为I3D再分发权。

### 实际变更

- 新建`TASK00_REMOTE_A6000_I3D_STAGING_DECISION_20260718.md`，裁定`REMOTE_I3D_STAGING=NOT_COVERED_BY_EXISTING_ACCEPTED_RISK`、`REMOTE_I3D_TRANSFER_AUTHORIZATION=HOLD_FOR_EXPLICIT_SCOPE_EXPANSION`，并保留`asset_redistribution_allowed=false`。
- 接受`REMOTE_A6000_RUNTIME=READY_FOR_SYNTHETIC_RESOURCE_VALIDATION`，但不把其改写为真实I3D smoke、全量复现或许可闭合。
- 在`.light/decision_log.md`追加`SC-20260718-02`；新建`.light/handoff/S06-remote-a6000-i3d-staging-hold.md`传播裁定、自检与接续提示词。
- 未上传、读取或修改I3D `.npy`，未修改总纲、G1/G2/G3、任务20实验核心、冻结证据包或任务树。

### 验证与证据

- 开工刷新：`git status --short --branch`显示`main...origin/main`且clean；`git fetch origin`后`HEAD=origin/main=8a5d8a38684cb0a07ee9a76d56fcf6d01d6ac33b`。
- 实时审计：读取任务20线程最新状态；核对`TASK20_BASELINE_EXECUTION_AUDIT.md`第10节，确认真实I3D、全量评论runtime、权重与预测均未上传，全量未启动。
- 权威边界：逐字读取`TASK00_G2_RISK_ACCEPTANCE_AND_TASK20_AUTHORIZATION_20260717.md`、`DATA_RELEASE_BOUNDARY.md`、`TASK00_G3_FINAL_REVIEW_20260718.md`和`TASK00_TASK20_VCCSA_SUPPLEMENT_REVIEW_20260718.md`。现有授权只覆盖固定本地I3D字节且明确不产生再分发权。
- 文本检索首选`rg`因本机`Access is denied`失败；未重复无mitigation失败，改用PowerShell `Select-String`完成只读边界回扫。
- 首轮提交前门禁：默认`.venv`运行`validate_work_log.py`为112条、latest=`WR-20260718-022`、`passed=true`；`run_preparation_checks.py` exit 0、`blocking_checks=[]`、secret scan无命中，同时如实保留默认环境`faiss_available=false`与`formal_model_work_ready=false`；`git diff --check` exit 0。

### 影响与边界

A6000算力/运行时阻塞已关闭，资产跨边界复制阻塞未关闭。任务20可保留公开代码、公开模型、环境和合成smoke，但不得上传固定8210项I3D或启动全量作者复现。若用户未来单独扩权，仍须先提交最小资产、hash/覆盖、访问控制、禁快照、删除核验和输出留存合同；该决定不能证明权利方许可。

### 风险、问题与阻塞

- I3D许可、官方revision、权利方包身份/fixity仍未知；权利否认或8210 hash/覆盖漂移继续触发`ASSET_INVALIDATED_DO_NOT_REPORT`。
- 租用平台的备份、快照、运维访问和删除语义尚无证据；在明确合同前不能把实例称为既有内部隔离区。
- `light-data-engineering`与`light-research-ethics`要求许可UNKNOWN与新跨边界处理保持fail-closed；技能没有导致资产操作。

### 下一步

1. 任务20保持I3D上传与全量复现HOLD，并保留A6000环境。
2. 若用户明确知情扩权，任务20先回交远端暂存执行合同，由00复核后再传输。
3. 继续监督G3限制、NON_T0身份、任务50未完成与I3D止损边界。

### Git状态

本条写入时上述00裁定、决策日志、WORK_LOG与S06交接卡尚未提交或推送；工作区非clean。

## WR-20260718-023 — 提交推送远端I3D暂存HOLD裁定

- 时间：2026-07-18 16:42:00 +08:00
- 类型：SYNC | PROGRESS | AUDIT
- 任务/门：00-T-AFFC总控 / 任务20远端资产边界
- 状态：00裁定已提交推送；同步日志待提交
- 负责人：Codex

### 背景与目标

固定WR-20260718-022已验证的`SC-20260718-02`、决策日志和S06交接合同，并把实际远端同步结果写入审计链。

### 实际变更

- 仅显式暂存四项00所有权文件：`.light/decision_log.md`、`.light/handoff/S06-remote-a6000-i3d-staging-hold.md`、`TASK00_REMOTE_A6000_I3D_STAGING_DECISION_20260718.md`和`WORK_LOG.md`。
- 创建提交`5d831b42374e73e86f765b3216cf0fcfb1ad83a8`并推送`origin/main`。
- 任务20并发生成的未跟踪`TASK20_REMOTE_A6000_I3D_STAGING_EXECUTION_CONTRACT_20260718.md`未被00暂存、改写或提交。

### 验证与证据

- `git diff --cached --check`：exit 0；缓存文件严格为上述四项00产物。
- `git commit -m "docs(task00): hold remote I3D staging"`：exit 0，commit=`5d831b42374e73e86f765b3216cf0fcfb1ad83a8`，4 files changed，134 insertions。
- `git push origin main`：exit 0，`8a5d8a3..5d831b4 main -> main`；提交后`HEAD=origin/main=5d831b42374e73e86f765b3216cf0fcfb1ad83a8`。

### 影响与边界

远端main现可审计00裁定：A6000合成资源预检被接受，但真实I3D远端暂存不在既有accepted-risk范围内，保持HOLD。任务20合同仍由任务20所有，不因共享工作区出现而被00视为已提交证据或已获执行许可。

### 风险、问题与阻塞

共享工作区因任务20未跟踪合同文件而非clean；该并发文件未进入00提交。真实I3D仍未获远端传输授权，许可/revision/权利方fixity未知与止损条件不变。

### 下一步

1. 向任务20发送`5d831b4`裁定hash，要求其在该父提交后有意提交执行合同，不得上传I3D。
2. 任务20合同提交后由00独立复核；只有用户明确知情扩权且合同通过，才可能另行裁定是否执行。

### Git状态

本条同步日志自身尚未提交或推送；任务20未跟踪合同继续由任务20所有，00不处理。

## WR-20260718-024 — 审批当前A6000实例固定8210项I3D临时暂存

- 时间：2026-07-18 16:49:00 +08:00
- 类型：DECISION | AUDIT | RISK | DOC
- 任务/门：00-T-AFFC总控 / 任务20远端资产执行合同
- 状态：实例限定批准；传输前硬门待任务20执行
- 负责人：Codex

### 背景与目标

在`SC-20260718-02`明确既有accepted-risk不自动覆盖第三方租用实例后，用户进一步书面授权：仅把固定manifest中的8210项I3D临时上传至其私人租用实例，仅用于内部研究训练，完成后删除，不发布或转交第三方。任务20据此起草执行合同并保持`PENDING_00_REVIEW_NO_TRANSFER_YET`，请求00独立复核。

### 实际变更

- 新建`TASK00_REMOTE_A6000_I3D_STAGING_APPROVAL_20260718.md`，裁定`REMOTE_I3D_TRANSFER_AUTHORIZATION=APPROVED_FOR_THIS_INSTANCE_ONLY_WITH_PRETRANSFER_GATES`。
- 批准精确合同SHA-256=`82aa89cdc3c6f98bd2896c8b5524dc87beca6d31c25857dbc8b1149eee015752`、106行；合同文件继续由任务20所有，00未暂存或改写。
- 新增合同固化、实例唯一绑定、访问/快照、本地严格8210集合、传后fixity和真实train/dev smoke六道执行门。host key、GPU UUID、端点或实例身份变化即批准失效。
- 在`.light/decision_log.md`追加`SC-20260718-03`，新建`.light/handoff/S07-remote-a6000-i3d-staging-approved.md`传播实例限定批准与接续提示词。

### 验证与证据

- `git status --short --branch`：审查时`HEAD=origin/main=5d831b42374e73e86f765b3216cf0fcfb1ad83a8`；仅00同步日志modified与任务20合同untracked。
- 完整读取任务20合同第1—9节；确认覆盖8210严格集合、SFTP/0700/0600、禁Git/对象存储/快照/镜像、`UNKNOWN_PLATFORM_CONTROL_PLANE`、train/dev与冻结后test隔离、跨split peer fail-closed、输出回传边界和删除核验。
- `Get-FileHash -Algorithm SHA256`得到`82aa89cdc3c6f98bd2896c8b5524dc87beca6d31c25857dbc8b1149eee015752`；行数106。
- 对合同回扫密码、SSH端点、账户、Cookie、token、secret和private-key模式，无命中。

### 影响与边界

用户扩权缺口已关闭，但授权只对当前实例和精确合同有效；任务20尚须先提交合同并完成全部传输前门。批准不等于I3D权利方许可、一般再分发权或平台绝对删除证明；不授权将权重、checkpoint、逐样本预测、评论或完整run bundle回传/发布。实验继续为`AUTHOR_ORIGINAL_SETTING_NON_T0`，不进入T0统一主表。

### 风险、问题与阻塞

- 平台运维访问、底层备份和物理擦除语义仍UNKNOWN，用户只接受本次残余操作风险。
- 合同尚未提交；实例绑定与操作者侧快照检查尚无执行证据，因此当前不得立即传输。
- I3D许可、官方revision、权利方包身份/fixity仍未知；权利否认或8210 hash/覆盖漂移继续触发`ASSET_INVALIDATED_DO_NOT_REPORT`。

### 下一步

1. 提交推送00批准文件、WR-023/024、决策日志和S07，不纳入任务20合同。
2. 向任务20发送批准commit/hash；任务20以其为父提交精确合同并执行传输前门。
3. 任务20完成传后fixity与真实smoke后回报；00持续监督，不并发修改实验核心。

### Git状态

本条写入时上述00批准、日志、决策日志和S07尚未提交或推送；任务20合同仍未跟踪且由任务20所有。

## WR-20260718-025 — 独立确认VC-CSA作者peer依赖触发泄漏止损

- 时间：2026-07-18 17:03:00 +08:00
- 类型：AUDIT | DECISION | DATA | RISK | TEST
- 任务/门：00-T-AFFC总控 / VC-CSA作者原设定全量复现
- 状态：`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`；禁止传输I3D
- 负责人：Codex

### 背景与目标

任务20在接受实例绑定硬门后，于任何真实传输前对作者固定split与同video peer依赖做只读聚合预检，报告7,854个video跨split以及train/dev/test各122/2,750/1,573个split内singleton。该结果若成立，会比实例授权更早触发合同第5节泄漏止损。00不以任务20自报替代裁定，独立复算并读取作者loader。

### 实际变更

- 新建`TASK00_VCCSA_AUTHOR_PEER_ISOLATION_REVIEW_20260718.md`，裁定`AUTHOR_ORIGINAL_FULL_REPRODUCTION=LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`和`EFFECTIVE_I3D_TRANSFER_PERMISSION=BLOCKED_DO_NOT_TRANSFER`。
- 修改未提交的`TASK00_REMOTE_A6000_I3D_STAGING_APPROVAL_20260718.md`：保留用户对当前实例残余风险的原则批准，但明确执行许可未激活；第0门peer物理隔离已失败。
- 更正`.light/decision_log.md`中的`SC-20260718-03`摘要；以`.light/handoff/S07-remote-a6000-i3d-execution-blocked.md`取代未提交的批准版S07。
- 未修改、暂存或提交任务20合同/代码；未连接远端、未上传I3D、未启动真实smoke或训练。

### 验证与证据

- 使用正式`.venv-task20`直接调用项目已有`audit_peer_isolation()`读取作者固定split、压缩标注与video映射，只输出聚合计数：train 75,086 comments/8,190 videos/122 singleton；dev 10,727/5,833/2,750；test 21,454/7,360/1,573；`videos_spanning_splits=7854`；状态`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`。
- 上述组合命令随后因第一次指定的作者loader目录`downloads/MSA-CRVI/source_vcssa`不存在而整体exit 1；聚合器本身已成功输出。失败保留后，定位实际作者代码到Git忽略目录`downloads/MSA-CRVI-JackySnake-audit/source_vcssa`。
- 直接读取作者`csmv_dataset.py`：`get_video_other_comment_info()`从`video_to_comment[videoid]`执行`random.choice`，并在等于当前comment时循环重抽，随后读取peer的comment与opinion/emotion标签。
- 因此严格split内映射会使singleton无法取peer；全量映射则因7,854个跨split视频使train可读dev/test peer评论与标签。GPU、环境或I3D上传不能修复该逻辑冲突。

### 影响与边界

用户的实例风险扩权仍是事实，但数据最小化与合同fail-closed要求在第0门失败后不传输任何I3D。此前8 train/4 dev smoke只证明人为选择的peer-safe子集可执行，不证明完整作者split可隔离运行。删除singleton、self-peer、跨split peer、固定/合成peer、取消peer损失或视频级重分割都改变作者合同，只能另建`REIMPLEMENTATION_NON_FAITHFUL_PEER_ADAPTATION`并重新审批。

### 风险、问题与阻塞

- faithful作者原设定全量复现现在由协议/泄漏冲突阻断，不再由A6000算力或用户实例风险授权阻断。
- 真实I3D仍0项上传；任务20不得为了利用已租算力而绕过止损。
- I3D许可、官方revision、权利方包身份/fixity未知与`ASSET_INVALIDATED_DO_NOT_REPORT`条件不变。

### 下一步

1. 提交推送00阻断裁定、peer独立审查、WR-023—025、决策日志和S07，继续排除任务20合同。
2. 指令任务20提交合同、peer聚合器/测试及聚合证据，但保持远端资产操作为0。
3. 如用户希望尝试peer适配，要求独立REIMPLEMENTATION预注册与00新授权，不自动复用实例批准。

### Git状态

本条写入时上述00文件尚未提交或推送；任务20合同仍未跟踪且由任务20所有。

## WR-20260718-026 — 复核任务20最终peer阻断合同与67项测试

- 时间：2026-07-18 17:10:00 +08:00
- 类型：AUDIT | TEST | DOC | RISK
- 任务/门：00-T-AFFC总控 / VC-CSA作者peer隔离最终证据
- 状态：最终合同接受为NO_TRANSFER阻断证据
- 负责人：Codex

### 背景与目标

任务20根据00实例绑定要求和已触发的peer止损更新执行合同、聚合器与负测。00需复核新合同hash、增强字段、专项/全量测试和真实数据聚合，确保最终裁定绑定当前证据而非已被取代的106行合同。

### 实际变更

- 将`TASK00_REMOTE_A6000_I3D_STAGING_APPROVAL_20260718.md`、`TASK00_VCCSA_AUTHOR_PEER_ISOLATION_REVIEW_20260718.md`与S07绑定到最终合同SHA-256=`5dbf891d1fcd6307ee19f98dc46c8e3f7c35a712c167a5b258c4c10b79d28d3c`、120行、状态`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY_NO_TRANSFER`。
- 明确旧106行合同hash仅为审查历史，不具执行效力。
- 增补三split singleton全部`cross_split_only_peer_ids`且`no_global_peer_ids=0`的证据；未改写或暂存任务20代码、测试与合同。

### 验证与证据

- 完整读取最终120行合同；实例绑定新增SSH host-key SHA-256、GPU UUID和端点摘要，任一漂移使授权失效；第9—10节明确peer止损优先、真实I3D上传0和不得传输。
- `Get-FileHash`复核最终合同SHA-256为`5dbf891d1fcd6307ee19f98dc46c8e3f7c35a712c167a5b258c4c10b79d28d3c`。
- 00独立运行`.venv-task20` VC-CSA专项：7/7通过；全量unittest：67/67通过；均exit 0。
- 00独立运行增强后的真实`audit_peer_isolation()`：train/dev/test singleton与cross-split-only peer均为122/2,750/1,573，三split`no_global_peer_ids=0`，跨split视频7,854，报告不含comment IDs/text，exit 0。
- 最终脚本差异只新增聚合审计字段；负测构造train singleton仅能从test取peer并断言fail-closed、无ID泄漏。

### 影响与边界

最终合同作为“为何不传输/不运行”的证据被00接受，不是上传执行许可。实例风险授权原则上存在，但当前有效传输权限明确为`BLOCKED_DO_NOT_TRANSFER`。任务20可提交其代码、测试、合同和聚合证据；不得连接远端做资产操作。

### 风险、问题与阻塞

作者原peer机制和随机comment split的冲突已构成结构性阻塞。任何改法都会改变实验身份，必须另建REIMPLEMENTATION；不能因A6000租用成本或用户资产扩权绕过。

### 下一步

1. 完成00文件门禁并只提交00所有权文件，排除任务20四项并发改动。
2. 向任务20发送00阻断提交hash，允许其随后提交最终合同、聚合器、负测和自身日志。
3. 若无另行REIMPLEMENTATION授权，任务20作者全量复现以该结构性阻断收尾。

### Git状态

本条写入时00批准/阻断文件尚未提交；任务20合同、脚本和测试并发改动继续由任务20所有。

## WR-20260718-027 — 提交推送VC-CSA peer泄漏阻断裁定

- 时间：2026-07-18 17:18:00 +08:00
- 类型：SYNC | PROGRESS | AUDIT
- 任务/门：00-T-AFFC总控 / VC-CSA作者原设定全量复现
- 状态：00阻断裁定已提交推送；同步日志待提交
- 负责人：Codex

### 背景与目标

固定WR-20260718-023—026记录的实例风险边界、最终合同复核和peer结构性阻断，并把实际远端同步结果写入审计链。

### 实际变更

- 仅显式暂存五项00文件：`.light/decision_log.md`、S07、A6000实例风险批准/执行阻断、peer隔离独立审查和`WORK_LOG.md`。
- 创建提交`8f4b495edb3a7037adb3073d80f2c1af533028ab`并推送`origin/main`。
- 任务20并发修改的执行审计、peer聚合器、测试与合同均未被00暂存、改写或提交。

### 验证与证据

- 提交前默认`.venv`的`validate_work_log.py`：116条、latest=`WR-20260718-026`、`passed=true`；`run_preparation_checks.py` exit 0、`blocking_checks=[]`、secret scan无命中，同时默认环境继续如实为`faiss_available=false`、`formal_model_work_ready=false`。
- S07独立handoff合同6项通过；`git diff --check`和`git diff --cached --check`均exit 0；缓存文件严格为五项00产物。
- `git commit -m "docs(task00): block VC-CSA transfer on peer leakage"`：exit 0，commit=`8f4b495edb3a7037adb3073d80f2c1af533028ab`，5 files changed，326 insertions。
- `git push origin main`：exit 0，`5d831b4..8f4b495 main -> main`；推送后`HEAD=origin/main=8f4b495edb3a7037adb3073d80f2c1af533028ab`。

### 影响与边界

远端main现正式记录：用户接受当前实例风险，但作者faithful全量路径触发peer泄漏止损，有效I3D传输权限为`BLOCKED_DO_NOT_TRANSFER`。最终任务20合同hash仅作为NO_TRANSFER阻断证据；任何REIMPLEMENTATION须另行预注册与审批。

### 风险、问题与阻塞

共享工作区仍因任务20四项并发文件非clean；这些文件由任务20所有。真实I3D仍0上传，结构性阻断和资产UNKNOWN边界不变。

### 下一步

1. 提交推送本同步日志后向任务20发送`8f4b495`及最终同步hash。
2. 任务20基于00提交有意提交其合同、聚合器、测试、执行审计和自身日志，不进行远端资产操作。
3. 总控后续仅审查任务20提交和可能的独立REIMPLEMENTATION提案，不并发修改其实验核心。

### Git状态

本条同步日志自身尚未提交或推送；任务20四项并发文件继续由任务20所有，00不处理。

## WR-20260718-028 — 固化VC-CSA作者peer隔离阻断并保持I3D零上传

- 时间：2026-07-18 16:59:08 +08:00
- 类型：AUTH | TDD | AUDIT | DATA | RISK | DOC
- 任务/门：20-M3 / VC-CSA作者原设定全量复现
- 状态：`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY`；`EFFECTIVE_I3D_TRANSFER_PERMISSION=BLOCKED_DO_NOT_TRANSFER`
- 负责人：Codex

### 背景与目标

用户明确书面扩权：固定manifest中的8210项I3D可临时上传到其私人租用实例，仅用于内部研究训练，任务完成后删除，不发布或转交第三方。任务20须先把该扩权约束为实例限定执行合同，并在任何真实传输前检查作者随机comment split与同video peer采样能否满足train/dev/test物理隔离；不能因已租A6000而绕过泄漏门。

### 实际变更

- 新建`TASK20_REMOTE_A6000_I3D_STAGING_EXECUTION_CONTRACT_20260718.md`，覆盖固定8210严格集合、传前/传后fixity、SFTP最小权限、禁Git/对象存储/快照/镜像、`UNKNOWN_PLATFORM_CONTROL_PLANE`、实例host-key/GPU UUID/端点摘要绑定、输出回传和删除核验。最终合同状态为`LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY_NO_TRANSFER`，SHA-256=`5dbf891d1fcd6307ee19f98dc46c8e3f7c35a712c167a5b258c4c10b79d28d3c`、120行。
- 在`scripts/prepare_vccsa_author_reproduction.py`新增`audit_peer_isolation()`：只读作者split、压缩标注和video映射，验证ID/annotation/map完整性，输出split级video、singleton、cross-split-only peer与无全局peer聚合计数；报告不含comment ID或正文。
- 在`tests/test_vccsa_author_reproduction.py`先加“train singleton只能从test取peer”的负测；首次因函数尚不存在产生ImportError，最小实现后通过。随后增加`cross_split_only_peer_ids`/`no_global_peer_ids`断言，先因KeyError失败，补齐聚合字段后通过。
- 在`TASK20_BASELINE_EXECUTION_AUDIT.md`新增用户扩权后的传输前peer隔离止损章节，保留此前算力预检为历史事实，并将当前阻塞从算力更新为结构性泄漏冲突。
- 未修改00裁定、S07、总纲、G门、T0冻结协议或任务50状态；未连接远端、未上传/读取远端I3D、未启动真实smoke或训练。

### 验证与证据

- 真实作者数据聚合：train 75,086 comments / 8,190 videos / 122 singleton；dev 10,727 / 5,833 / 2,750；test 21,454 / 7,360 / 1,573；跨split视频7,854。
- 三split的singleton全部具有全局peer，但peer只存在于其他split：`cross_split_only_peer_ids=122/2750/1573`，`no_global_peer_ids=0/0/0`。因此完整作者映射会让train读取dev/test评论或标签；物理过滤后原loader无法为singleton取得另一comment。
- VC-CSA专项单测：7/7通过；正式`.venv-task20`全量unittest：67/67通过；`py_compile`通过。
- 合同定向扫描未发现SSH端点、端口、认证值、账户或本机绝对资产路径。首次首选`rg`因系统`Access is denied`失败，改用PowerShell完成扫描；一次宽泛`[A-Za-z]:\\`扫描把代码字符串中的`g:\\n`误报为路径，收紧到已知绝对根模式后通过，失败与mitigation均保留。
- 00独立复核已固定在`8f4b495edb3a7037adb3073d80f2c1af533028ab`，同步日志后父状态为`c7edb5499a908541ae24646e76ca03f0b4472274`；00独立得到相同聚合计数、7/7与67/67，并裁定实例风险原则接受但有效I3D传输权限为`BLOCKED_DO_NOT_TRANSFER`。
- 交付前默认`.venv`：`validate_work_log.py`为118条、latest=`WR-20260718-028`、`passed=true`；`run_preparation_checks.py` exit 0、`blocking_checks=[]`，同时如实保留`faiss_available=false`与`formal_model_work_ready=false`。正式`.venv-task20`准备检查exit 0、`blocking_checks=[]`、`faiss_available=true`、`formal_model_work_ready=true`。
- `git diff --check`通过；合同hash/120行复核一致。首次对完整`WORK_LOG.md`做本机根模式扫描命中6条历史路径而失败；改为只扫描WR-028新增diff并对其他四项任务20文件做全量扫描后无端点、端口、认证值、账户或本机绝对资产路径命中。

### 影响与边界

作者faithful全量路径不能同时满足原peer采样与无泄漏物理隔离，因此GPU、环境和用户实例风险扩权均不能解除该阻断。真实I3D保持0上传。删除singleton、self-peer、固定/合成peer、取消peer损失、跨split peer或视频级重分割都会改变作者合同，只能另建`REIMPLEMENTATION_NON_FAITHFUL_PEER_ADAPTATION`并重新预注册与申请00审批；不得冒充作者faithful全量复现。

I3D许可、官方revision、权利方包身份/fixity仍未知，`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`与`ASSET_INVALIDATED_DO_NOT_REPORT`止损条件不变。合同只作为NO_TRANSFER阻断证据，不是公开发布、再分发或权利方许可证明。

### 风险、问题与阻塞

- 当前结构性阻塞无法通过增加算力解决；租用实例不应继续为本faithful路径消耗费用。
- 若用户希望执行peer适配，必须接受其为非faithful重实现，并在任何资产操作前完成独立协议、泄漏测试与00书面审批。

### 下一步

1. 执行项目强制门禁、diff/secret检查，只提交任务20合同、聚合器、负测、执行审计和本记录。
2. 推送后向00回传commit/hash；不连接远端，不传输真实I3D。
3. 未获独立REIMPLEMENTATION授权前，以结构性阻断结束作者全量复现尝试。

### Git状态

本条写入时上述任务20五项改动尚未提交或推送；工作区非clean。真实I3D远端上传数为0。

## WR-20260718-029 — 00独立验收任务20 peer阻断提交

- 时间：2026-07-18 17:35:00 +08:00
- 类型：AUDIT | TEST | DECISION | DOC
- 任务/门：00-T-AFFC总控 / 任务20 VC-CSA阻断收尾
- 状态：`TASK20_PEER_BLOCKER_SUBMISSION=ACCEPTED`
- 负责人：Codex

### 背景与目标

任务20报告已按00父状态`c7edb54`有意提交并推送最终NO_TRANSFER合同、执行审计、peer聚合器、负测和WR-028，commit=`baaac078add841bb40fa6be1b44fa202c60f6e2b`。00须刷新实时状态并独立复核，不能以任务20自报替代验收。

### 实际变更

- 新建`TASK00_TASK20_PEER_BLOCKER_SUBMISSION_ACCEPTANCE_20260718.md`，接受`baaac078`作为结构性peer阻断的正式可审计提交。
- 新建`.light/handoff/S08-task20-peer-blocker-submission-accepted.md`，传播NO_TRANSFER、NON_T0、REIMPLEMENTATION新审批和I3D UNKNOWN边界。
- 未修改任务20代码、测试、合同、执行审计、总纲、G门、冻结G3 package/HANDOFF、T0协议或任务50状态。

### 验证与证据

- 开工刷新：`git status --short --branch`为`main...origin/main`且clean；`git fetch origin`后`HEAD=origin/main=baaac078add841bb40fa6be1b44fa202c60f6e2b`；任务20线程idle。
- `git show baaac078`确认相对父状态严格五项：执行合同、执行审计、聚合器、负测和WR-028。
- 合同SHA-256=`5dbf891d1fcd6307ee19f98dc46c8e3f7c35a712c167a5b258c4c10b79d28d3c`、120行；`git diff --check c7edb54..baaac078` exit 0。
- 00独立`.venv-task20`全量unittest 67/67通过；真实peer聚合重算7,854个跨split视频，train/dev/test singleton与cross-split-only peer均122/2,750/1,573，三split`no_global_peer=0`，报告不含comment IDs/text。
- 默认`.venv`的`validate_work_log.py`为118条、latest=`WR-20260718-028`、`passed=true`；默认准备检查exit 0、`blocking_checks=[]`，但`faiss_available=false`、`formal_model_work_ready=false`。
- 正式`.venv-task20`准备检查exit 0、`blocking_checks=[]`、`faiss_available=true`、`formal_model_work_ready=true`；handoff validator 22项通过、`restricted_assets_required=false`。

### 影响与边界

任务20faithful作者全量路径可按结构性泄漏止损正式收尾；其阻断证据可重复，且没有通过传输I3D或运行真实实验才发现问题。接受阻断证据不等于接受作者复现结果。任何peer适配都必须另建`REIMPLEMENTATION_NON_FAITHFUL_PEER_ADAPTATION`并重新预注册与审批。

### 风险、问题与阻塞

- I3D许可、官方revision、权利方包身份/fixity继续UNKNOWN；本验收不产生再分发或发布权。
- 用户曾接受当前A6000实例风险，但faithful实验已被更早的数据泄漏门阻断；不得继续为该路径上传或训练。
- 默认与正式task20环境状态不同，后续材料不得混写。

### 下一步

1. 提交推送00验收单、WR-029和S08交接卡。
2. 若用户不提出独立REIMPLEMENTATION方案，任务20本轮保持idle并按结构性阻断收尾。
3. 继续监督任务树、G3限制、任务50未完成和I3D止损边界，不创建IJCV任务。

### Git状态

本条写入时上述三项00文件尚未提交或推送；工作区非clean。

## WR-20260718-030 — 提交推送任务20 peer阻断验收

- 时间：2026-07-18 17:44:00 +08:00
- 类型：SYNC | PROGRESS | AUDIT
- 任务/门：00-T-AFFC总控 / 任务20 VC-CSA阻断收尾
- 状态：00验收已提交推送；同步日志待提交
- 负责人：Codex

### 背景与目标

固定WR-029完成的独立验收、正式验收单和S08交接合同，并记录实际远端同步结果。

### 实际变更

- 仅暂存`TASK00_TASK20_PEER_BLOCKER_SUBMISSION_ACCEPTANCE_20260718.md`、`.light/handoff/S08-task20-peer-blocker-submission-accepted.md`和`WORK_LOG.md`三项00文件。
- 创建提交`78b680817c3bfad96a49e91b44fd4fb26357927f`并推送`origin/main`。

### 验证与证据

- 提交前`validate_work_log.py`为119条、latest=`WR-20260718-029`、`passed=true`；默认`run_preparation_checks.py` exit 0、`blocking_checks=[]`，继续如实为`faiss_available=false`、`formal_model_work_ready=false`。
- S08独立handoff合同6项通过；`git diff --check`与`git diff --cached --check`均exit 0；缓存范围严格为三项00文件。
- `git commit -m "docs(task00): accept task20 peer blocker submission"`：exit 0，commit=`78b680817c3bfad96a49e91b44fd4fb26357927f`，3 files changed，135 insertions。
- `git push origin main`：exit 0，`baaac07..78b6808 main -> main`；推送后工作区clean。

### 影响与边界

远端main现包含00对任务20 `baaac078`阻断提交的独立验收及S08接续合同。faithful作者全量路径保持结构性阻断，真实I3D保持0上传；未授权任何peer适配或新实验。

### 风险、问题与阻塞

I3D许可、官方revision、权利方包身份/fixity继续UNKNOWN；任何非faithful peer适配仍须重新预注册与审批。

### 下一步

1. 提交推送本同步日志，确认`HEAD=origin/main`和工作区clean。
2. 任务20保持idle；若用户不提出REIMPLEMENTATION方案，该路径按结构性阻断收尾。
3. 总控继续监督任务树、G3限制和任务50未完成边界。

### Git状态

本条同步日志自身尚未提交或推送；主验收提交`78b680817c3bfad96a49e91b44fd4fb26357927f`已推送。

## WR-20260718-031 — 裁定VC-CSA泄漏风险接受型隔离探索

- 时间：2026-07-18 23:02:08 +08:00
- 类型：DECISION | AUTH | RISK | DOC
- 任务/门：00-T-AFFC总控 / VC-CSA作者原设定泄漏接受型探索
- 状态：原则允许；新探索合同hash复核前不得传输
- 负责人：Codex

### 背景与目标

用户明确表示不再以跨split peer数据泄漏作为停止理由，并要求继续作者代码训练。任务20没有自行解封，而是建议将唯一诚实身份固定为`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`，保留作者完整comment split、全量映射和peer逻辑，同时把结果隔离于正式证据。00需区分用户对方法学风险的知情接受与I3D许可/fixity闭合，并裁定既有实例专用传输扩权能否在新合同下恢复。

### 实际变更

- 新建`TASK00_VCCSA_LEAKAGE_ACCEPTED_EXPLORATORY_AUTHORIZATION_20260718.md`，记录`SC-20260718-04`。
- 更新`.light/decision_log.md`，固定探索身份、正式证据禁入和合同hash复核前的有效权限状态。
- 新建`.light/handoff/S09-vccsa-leakage-accepted-exploratory-authorized.md`，传播下一会话的复核硬门。
- 未修改任务20代码、测试、旧NO_TRANSFER合同、执行审计、总纲、G门、冻结G3 package/HANDOFF或实验核心。

### 验证与证据

- 开工前读取`AGENTS.md`、`WORK_RECORD_POLICY.md`、WORK_LOG末条、现有SC-20260718-03与S08边界，并刷新Git和任务20状态；当时`HEAD=origin/main=c5a552b131eebc7d7a37ac017d33dc95d95b0542`、工作区clean、任务20 idle。
- 复核既有聚合证据：7,854个跨split视频，train/dev/test的cross-split-only singleton为122/2,750/1,573；该事实不因用户接受风险而改变。
- 按`light-data-engineering`和`light-research-ethics`要求区分正式无泄漏证据门与用户知情“带病推进”的隔离探索；用户指令优先，但所有限制和披露必须落盘。
- 裁定状态为`APPROVED_IN_PRINCIPLE`而非立即执行：新合同精确SHA-256未获00接受前，真实I3D仍为0上传，真实全量训练不得启动。

### 影响与边界

跨split peer泄漏不再阻止这一次隔离探索，但永久阻止其进入T0、统一baseline、G3主证据、任务50、论文主表以及泛化/无泄漏/公平比较claim。作者完整映射可在新合同下保留；所有结果必须披露train可读取dev/test peer评论与标签及dev/test指标污染。

用户此前对当前私人租用实例固定8210项I3D临时上传、内部训练、任务后删除且不发布/不转交的扩权原则上可复用，但I3D许可、官方revision、权利方包身份/fixity仍UNKNOWN。权利方否认、8210 hash/覆盖漂移或实例绑定漂移继续触发`ASSET_INVALIDATED_DO_NOT_REPORT`。

### 风险、问题与阻塞

- 任务20尚未提交新的探索合同，故`EFFECTIVE_I3D_TRANSFER_PERMISSION=PENDING_EXPLORATORY_CONTRACT_HASH_REVIEW`。
- 平台控制面残余、I3D权利链和资产fixity未知项未被用户的方法学风险接受所消除。
- 单次探索指标受结构性泄漏污染；增加种子不能提升其正式证据资格。

### 下一步

1. 提交并推送本裁定、决策日志、WR-031与S09。
2. 通知任务20基于该父提交新建独立探索合同；在00接受精确hash前保持0上传/0真实训练。
3. 00随后只读复核合同与实例/资产/结果隔离条款，不并发修改任务20实验核心。

### Git状态

本条写入时上述四项00文件尚未提交或推送；任务20仍不得执行真实I3D传输。

## WR-20260718-032 — 提交推送VC-CSA泄漏接受型探索原则授权

- 时间：2026-07-18 23:09:04 +08:00
- 类型：SYNC | PROGRESS | AUDIT
- 任务/门：00-T-AFFC总控 / VC-CSA泄漏接受型探索授权
- 状态：原则授权已推送；合同hash复核待任务20提交
- 负责人：Codex

### 背景与目标

固定WR-031的用户方法学风险接受边界、`SC-20260718-04`裁定和S09交接合同，并记录实际Git同步结果。

### 实际变更

- 仅暂存并提交四项00所有权文件：`.light/decision_log.md`、`.light/handoff/S09-vccsa-leakage-accepted-exploratory-authorized.md`、`TASK00_VCCSA_LEAKAGE_ACCEPTED_EXPLORATORY_AUTHORIZATION_20260718.md`和`WORK_LOG.md`。
- 创建提交`e5397d29c8211a3af274161defad7bc082b48f8a`并推送`origin/main`。
- 未修改或提交任务20实验代码、测试、旧NO_TRANSFER合同、执行审计或运行资产。

### 验证与证据

- 首次`validate_work_log.py`因WR-031把必需元数据键写成“任务/问题”而报告`缺少元数据: 任务/门`，`run_preparation_checks.py`相应给出`blocking_checks=[work_log]`；修正键名后重跑通过。
- 修正后`validate_work_log.py`：121条、latest=`WR-20260718-031`、`passed=true`。
- 修正后默认`.venv`的`run_preparation_checks.py`：exit 0、`blocking_checks=[]`；同时如实保持`faiss_available=false`、`formal_model_work_ready=false`。
- S09交接卡结构6项通过；`git diff --check`与`git diff --cached --check`均exit 0。
- `git commit -m "docs(task00): authorize leakage-accepted VC-CSA exploration"`：commit=`e5397d29c8211a3af274161defad7bc082b48f8a`，4 files changed、152 insertions。
- `git push origin main`：`c5a552b..e5397d2 main -> main`；推送后`HEAD=origin/main=e5397d29c8211a3af274161defad7bc082b48f8a`、工作区clean。

### 影响与边界

远端main现正式记录：该隔离探索原则允许，但有效传输许可仍为`PENDING_EXPLORATORY_CONTRACT_HASH_REVIEW`。任务20只有在新合同精确hash被00另行接受后，才可上传固定8210项并启动该次单种子探索；其结果始终不具正式证据资格。

### 风险、问题与阻塞

当前唯一执行阻塞是任务20尚未提交新的独立探索合同。I3D许可、官方revision、权利方包身份/fixity和平台控制面残余风险均不变。

### 下一步

1. 向任务20发送`e5397d29`和合同要求，指令其只起草/提交新探索合同，合同获接受前保持0上传/0训练。
2. 00收到提交后独立复核实例绑定、8210 fixity、结果隔离、删除核验和止损条款，并绑定精确SHA-256。
3. 若合同满足硬门，再单独激活`APPROVED_FOR_BOUND_EXPLORATORY_CONTRACT`。

### Git状态

本同步日志自身尚未提交或推送；主裁定提交`e5397d29c8211a3af274161defad7bc082b48f8a`已推送。

## WR-20260718-033 — 建立VC-CSA泄漏接受型隔离探索合同

- 时间：2026-07-18 23:16:09 +08:00
- 类型：FEATURE | TEST | DOC | RISK
- 任务/门：任务20 / VC-CSA作者原设定单种子隔离探索
- 状态：新合同已完成并提交00精确hash复核；有效传输权限仍待批准
- 负责人：Codex

### 背景与目标

00在`e5397d29c8211a3af274161defad7bc082b48f8a`裁定用户仅接受一次隔离探索的方法学泄漏风险，并要求任务20新建独立合同；在00另行绑定精确SHA-256前，真实I3D必须保持0上传、真实训练保持0次。旧NO_TRANSFER合同及其固定hash不得原地改写。

### 实际变更

- 新建`TASK20_VCCSA_LEAKAGE_ACCEPTED_EXPLORATORY_EXECUTION_CONTRACT_20260718.md`，唯一身份固定为`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`，明确train可读取dev/test peer评论与标签、dev/test指标污染和正式证据禁入。
- 合同仅允许`single seed=3407`工程诊断，并把T0、G3、`BASELINE_TABLE_V1.md`、任务50、论文claim、排名和显著性比较全部排除。
- 合同覆盖指定实例SSH host-key SHA-256/GPU UUID/endpoint digest三元绑定、固定8210项传前传后fixity、SFTP与0700/0600、禁Git/对象存储/快照、最小输出回传、删除核验、`UNKNOWN_PLATFORM_CONTROL_PLANE`及`ASSET_INVALIDATED_DO_NOT_REPORT`止损。
- 在`tests/test_vccsa_author_reproduction.py`新增合同负测/合同测试；未修改旧`TASK20_REMOTE_A6000_I3D_STAGING_EXECUTION_CONTRACT_20260718.md`、00裁定、S09、总纲或G门。

### 验证与证据

- TDD红灯：先运行新专项测试，因新合同不存在得到预期`FileNotFoundError`，1项失败；随后最小新增合同，同一专项测试1/1通过。
- `.venv-task20`任务20 VC-CSA专项8/8通过；正式环境全量unittest 68/68通过。
- `.venv-task20`准备检查exit 0，`blocking_checks=[]`、`faiss_available=true`、`formal_model_work_ready=true`。
- 新合同SHA-256=`77b0a93003d265aae6215caca3ef53fbef4624bd24cf3dfabf46df3978cdaed4`，PowerShell按物理换行计48行；旧NO_TRANSFER合同diff为空。
- 首轮默认`validate_work_log.py`因本条把必需元数据键写成“任务/问题”而失败，报告`WR-20260718-033缺少元数据: 任务/门`；已将本条未提交记录修正为校验器要求的“任务/门”并保留失败事实。修正后复跑：`validate_work_log.py`共123条、latest=`WR-20260718-033`、`passed=true`；默认`.venv`准备检查exit 0、`blocking_checks=[]`，如实保持`faiss_available=false`与`formal_model_work_ready=false`；正式`.venv-task20`准备检查exit 0、`blocking_checks=[]`、`faiss_available=true`、`formal_model_work_ready=true`。
- `git diff --check`通过；新合同与测试定向敏感端点/凭证扫描命中0；旧NO_TRANSFER合同diff为空。截至验证结束，未连接远端，真实I3D上传0项，真实训练0次。

### 影响与边界

本批只建立供00精确hash复核的执行合同，不构成`APPROVED_FOR_BOUND_EXPLORATORY_CONTRACT`。探索结果即使后续产生也永久为`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`，不得进入正式baseline或论文证据。I3D许可、官方revision、权利方包身份/fixity仍为UNKNOWN。

### 风险、问题与阻塞

- `EFFECTIVE_I3D_TRANSFER_PERMISSION=PENDING_EXPLORATORY_CONTRACT_HASH_REVIEW`仍是当前硬门；00接受精确hash前不得上传或训练。
- 平台控制面删除/备份能力不可独立验证；合同仅约束操作者可见层，保留`UNKNOWN_PLATFORM_CONTROL_PLANE`。

### 下一步

1. 运行项目强制门禁、diff与敏感信息检查，有意提交本合同、测试和WR-033。
2. 推送后向00回传commit、合同SHA-256、行数和门禁结果，等待独立hash复核。
3. 仅在00另行记录`APPROVED_FOR_BOUND_EXPLORATORY_CONTRACT`后才允许执行实例绑定和资产传输。

### Git状态

本条写入时新合同、测试和WR-033尚未提交或推送，工作区非clean；真实I3D上传0项，真实训练0次。

## WR-20260718-034 — 独立验收VC-CSA探索合同精确hash并激活绑定权限

- 时间：2026-07-18 23:21:32 +08:00
- 类型：AUDIT | TEST | DECISION | AUTH | DOC
- 任务/门：00-T-AFFC总控 / VC-CSA泄漏接受型探索合同hash复核
- 状态：合同接受；绑定合同范围内的传输执行权限生效
- 负责人：Codex

### 背景与目标

任务20基于`bbccdf0`提交新的独立探索合同并请求00仅做精确hash复核。00需验证当前远端字节、提交范围、旧合同不变性和合同测试，不重新审议用户已接受的方法学泄漏风险，也不改任务20实验核心。

### 实际变更

- 新建`TASK00_VCCSA_EXPLORATORY_CONTRACT_HASH_ACCEPTANCE_20260718.md`，记录`SC-20260718-05`并绑定合同精确SHA-256。
- 更新`.light/decision_log.md`，把有效权限改为`APPROVED_FOR_BOUND_EXPLORATORY_CONTRACT`。
- 新建`.light/handoff/S10-vccsa-exploratory-contract-hash-accepted.md`，传播实例、8210 fixity、单种子和删除监督门。
- 未修改任务20新/旧合同、测试、实验代码、总纲、G门、冻结G3 package/HANDOFF或实验结果。

### 验证与证据

- 开工刷新：`HEAD=origin/main=4ebcb260dfccf357e9cfb9c7a92c9d348a1b28d9`、工作区clean、任务20线程idle。
- `git diff --name-status bbccdf0..4ebcb260`严格为新合同、`WORK_LOG.md`和合同测试三项；旧NO_TRANSFER合同diff为空。
- 00独立`Get-FileHash -Algorithm SHA256`得到`77b0a93003d265aae6215caca3ef53fbef4624bd24cf3dfabf46df3978cdaed4`，与任务20回传一致。
- 当前合同物理行数由`Get-Content -Encoding utf8`独立得到100；任务20回传48行不正确，`git show --stat`同样显示新增100行。hash一致，故字节版本未漂移；00验收材料使用100行并停止传播48行。
- `.venv-task20\Scripts\python.exe -m unittest tests.test_vccsa_author_reproduction -v`：8/8通过，exit 0。
- `git diff --check bbccdf0..4ebcb260`：exit 0。
- 本次使用`light-data-engineering`维持泄漏结果正式证据禁入，使用`light-research-ethics`把用户知情带病推进限定于透明、隔离且可止损的探索合同；两者没有把用户已接受的风险重新设为执行阻塞。

### 影响与边界

任务20现在可执行已接受合同，但必须先通过实例三元绑定和传前8210 fixity，再传输、远端复核并运行一次seed=3407诊断。批准不证明传输、训练、结果或删除已经完成；验收时真实I3D仍0上传、真实训练0次。

结果永久为`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`，不得进入T0、G3、统一baseline、任务50或论文正式claim。I3D未知项、平台控制面残余风险和资产止损条件不变。

### 风险、问题与阻塞

- 任务20回传的合同物理行数错误，已由00纠正为100；后续hash仍是唯一字节身份锚点。
- 执行仍受实例三元绑定、8210传前/传后fixity、最小权限、输出边界和删除核验约束；任一失败即停止。

### 下一步

1. 提交推送本验收单、决策日志、WR-034与S10。
2. 向任务20发送验收commit、合同hash和100行更正，允许其严格按合同开始实例绑定与传前检查。
3. 持续监督上传、单种子诊断和删除核验；不得扩大到更多种子或正式证据。

### Git状态

本条写入时上述四项00文件尚未提交或推送；有效权限裁定尚未进入远端main，任务20应继续等待提交hash。

## WR-20260718-035 — 提交推送VC-CSA探索合同hash验收

- 时间：2026-07-18 23:25:10 +08:00
- 类型：SYNC | PROGRESS | AUDIT
- 任务/门：00-T-AFFC总控 / VC-CSA探索合同生效同步
- 状态：合同hash验收已推送；绑定合同权限正式生效
- 负责人：Codex

### 背景与目标

固定WR-034的独立hash复核、100行更正、`SC-20260718-05`和S10监督合同，并记录实际远端同步结果。

### 实际变更

- 仅暂存并提交四项00所有权文件：`.light/decision_log.md`、`.light/handoff/S10-vccsa-exploratory-contract-hash-accepted.md`、`TASK00_VCCSA_EXPLORATORY_CONTRACT_HASH_ACCEPTANCE_20260718.md`和`WORK_LOG.md`。
- 创建提交`c77eff30ba31d3db293014aff4b3b97cf3f46980`并推送`origin/main`。
- 未修改或提交任务20合同、测试、实验代码或受限资产。

### 验证与证据

- 提交前`validate_work_log.py`：124条、latest=`WR-20260718-034`、`passed=true`。
- 默认`.venv`的`run_preparation_checks.py`：exit 0、`blocking_checks=[]`；同时如实保持`faiss_available=false`、`formal_model_work_ready=false`。
- S10交接结构6项通过；`git diff --check`和`git diff --cached --check`均exit 0。
- `git commit -m "docs(task00): accept VC-CSA exploratory contract hash"`：commit=`c77eff30ba31d3db293014aff4b3b97cf3f46980`，4 files changed、142 insertions。
- `git push origin main`：`4ebcb26..c77eff3 main -> main`；推送后`HEAD=origin/main=c77eff30ba31d3db293014aff4b3b97cf3f46980`、工作区clean。

### 影响与边界

远端main现正式激活`EFFECTIVE_I3D_TRANSFER_PERMISSION=APPROVED_FOR_BOUND_EXPLORATORY_CONTRACT`。任务20可严格按hash为`77b0a93003d265aae6215caca3ef53fbef4624bd24cf3dfabf46df3978cdaed4`的合同执行；任何字节、实例或资产漂移都会使批准失效。

### 风险、问题与阻塞

执行尚未发生，实例三元绑定、传前/传后8210 fixity、一次seed=3407诊断和删除核验仍须逐门完成。合同指标始终不具正式证据资格。

### 下一步

1. 向任务20回传`c77eff30`及100行更正，允许按已接受合同开始实例绑定和传前检查。
2. 持续监督传输、诊断和删除；失败即停止并记录。
3. 禁止任务20扩大到更多种子、正式baseline、任务50或论文claim。

### Git状态

本同步日志自身尚未提交或推送；主验收提交`c77eff30ba31d3db293014aff4b3b97cf3f46980`已推送。

## WR-20260718-036 — VC-CSA探索实例三元绑定前SSH握手失败止损

- 时间：2026-07-18 23:29:33 +08:00
- 类型：TEST | SECURITY | PROGRESS | RISK
- 任务/门：任务20 / VC-CSA泄漏接受型隔离探索实例绑定门
- 状态：阻挡；实例SSH在密钥交换前拒绝连接，未传输资产、未训练
- 负责人：Codex

### 背景与目标

00已在`c77eff30ba31d3db293014aff4b3b97cf3f46980`接受任务20探索合同精确SHA-256，并在同步后的`main@2d5e182ff790595654f150245c97227d0171af99`激活`EFFECTIVE_I3D_TRANSFER_PERMISSION=APPROVED_FOR_BOUND_EXPLORATORY_CONTRACT`。任务20按合同顺序首先尝试获取SSH host-key SHA-256、GPU UUID和endpoint digest三元绑定；三元绑定完成前禁止fixity、传输和训练。

### 实际变更

- 快进刷新`main`并完整读取`TASK00_VCCSA_EXPLORATORY_CONTRACT_HASH_ACCEPTANCE_20260718.md`与S10，确认合同精确SHA-256仍为`77b0a93003d265aae6215caca3ef53fbef4624bd24cf3dfabf46df3978cdaed4`。
- 采纳00纠正：合同当前物理行数为100，停止传播此前错误的48行。
- 对用户指定实例执行只读SSH host-key扫描和最小TCP/SSH握手诊断；未创建远端目录、未认证、未上传、未执行远端命令。
- 因实例在密钥交换前拒绝连接，三元绑定无法形成；按合同立即停止，未继续本地8210传前fixity、SFTP、远端fixity或seed=3407诊断。

### 验证与证据

- 开工状态：`HEAD=origin/main=2d5e182ff790595654f150245c97227d0171af99`，工作区clean。
- 合同复核：SHA-256=`77b0a93003d265aae6215caca3ef53fbef4624bd24cf3dfabf46df3978cdaed4`，`Get-Content -Encoding utf8`为100个物理行。
- 首次`ssh-keyscan`返回空并以`SSH_HOST_KEY_SCAN_EMPTY`失败；未取得可绑定host-key指纹。
- 最小握手诊断显示TCP连接一度建立，但随后在认证前得到`kex_exchange_identification: write: Connection refused`和`banner exchange ... Connection refused`；`Test-NetConnection`同时报告`TcpTestSucceeded=False`。
- SSH host-key SHA-256未取得、GPU UUID未取得，因此三元绑定状态为`FAILED_NOT_BOUND`。真实I3D上传0项，真实训练0次，远端受限根目录未创建。
- 交付门禁：`validate_work_log.py`共126条、latest=`WR-20260718-036`、`passed=true`；默认`.venv`准备检查exit 0、`blocking_checks=[]`且如实保持`faiss_available=false`、`formal_model_work_ready=false`；正式`.venv-task20`准备检查exit 0、`blocking_checks=[]`、`faiss_available=true`、`formal_model_work_ready=true`；`git diff --check`通过。

### 影响与边界

本次失败发生在任何资产操作之前，不构成合同字节、8210资产或远端权限漂移，也没有需要删除的远端受限资产。实验身份仍永久为`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`，`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`；T0、G3、统一baseline、任务50、论文claim、总纲和G门均未修改。

### 风险、问题与阻塞

- 当前用户指定实例SSH服务不可完成握手，GPU可用性和GPU UUID无法验证；按用户要求认定当前实例不可用于本次全量诊断并立即报告。
- 未取得三元绑定意味着既有合同不得用于传输；不得把原则授权迁移到其他端点或实例。
- I3D许可、官方revision、权利方包身份/fixity仍为UNKNOWN；`UNKNOWN_PLATFORM_CONTROL_PLANE`与`ASSET_INVALIDATED_DO_NOT_REPORT`边界不变。

### 下一步

1. 运行工作日志、准备检查和diff门禁，仅提交本次失败记录。
2. 向00回传实例绑定失败、0上传/0训练和当前阻塞状态。
3. 等待用户恢复同一实例SSH服务或提供新的实例；新实例必须重新取得00实例绑定授权，不能沿用当前三元组批准。

### Git状态

本条写入时仅`WORK_LOG.md`有未提交变更；未连接成功远端、未上传I3D、未启动训练。

## WR-20260718-037 — 验收VC-CSA实例绑定失败止损并暂停传输权限

- 时间：2026-07-18 23:32:48 +08:00
- 类型：AUDIT | DECISION | SECURITY | RISK | DOC
- 任务/门：00-T-AFFC总控 / VC-CSA探索实例绑定失败验收
- 状态：失败止损接受；等待同一实例恢复或新实例重新授权
- 负责人：Codex

### 背景与目标

任务20按已接受合同从实例三元绑定开始，但SSH在密钥交换前拒绝连接，无法取得host-key与GPU UUID，遂在任何资产操作前停止并提交WR-036。00需独立复核提交范围、止损顺序和零资产事实，并冻结等待状态，避免无新mitigation重复连接失败。

### 实际变更

- 新建`TASK00_VCCSA_INSTANCE_BINDING_FAILURE_ACCEPTANCE_20260718.md`，记录`SC-20260718-06`。
- 更新`.light/decision_log.md`，将有效传输权限暂停为`SUSPENDED_INSTANCE_BINDING_FAILED_DO_NOT_TRANSFER`。
- 新建`.light/handoff/S11-vccsa-instance-binding-failure-accepted.md`，传播同一实例恢复与换实例重授权边界。
- 未重试实例连接，未获取或记录端点/凭证，未修改任务20合同、代码、测试或实验核心。

### 验证与证据

- 开工刷新：`HEAD=origin/main=5ddb1f655539c44c60d503d7aa8fbb7b04c0a20d`、工作区clean、任务20线程idle。
- `git show`确认`5ddb1f6`相对`2d5e182`仅向`WORK_LOG.md`追加WR-036，共48行；`git diff --check` exit 0。
- WR-036如实记录`ssh-keyscan`为空、认证前kex/banner connection refused、`Test-NetConnection=False`，host-key与GPU UUID均未取得。
- 复核操作顺序：本地8210传前fixity未开始、SFTP未开始、远端fixity未开始、seed=3407诊断未开始；真实I3D 0上传、训练0次、远端受限根目录未创建。
- 使用`light-data-engineering`确认零传输与未启动fixity的资产状态不被误写为已核验；使用`light-research-ethics`确认失败和未知平台原因不被包装为完成或绝对安全结论。

### 影响与边界

任务20正确执行了fail-closed合同。合同hash验收仍有效，但当前实例未绑定，故执行权限暂停。同一实例恢复后可重试三元绑定；换实例不得继承本批准。

无远端受限资产意味着无需执行删除动作，但不能声称远端删除核验已完成。没有产生指标、权重、预测或实验结果。

### 风险、问题与阻塞

- SSH拒绝的根因未被独立确认；不能把一次连接失败外推为平台永久故障。
- 当前工作阻塞于用户/平台恢复同一实例，或用户提供新实例并重新申请00授权。
- I3D许可、官方revision、权利方包身份/fixity继续UNKNOWN。

### 下一步

1. 提交推送本验收单、决策日志、WR-037与S11。
2. 通知任务20保持idle，不无新mitigation重复探针；同一实例恢复后从三元绑定重新开始。
3. 若用户更换实例，先完成新实例授权，不沿用旧绑定批准。

### Git状态

本条写入时上述四项00文件尚未提交或推送；任务20应继续保持0上传/0训练。

## WR-20260718-038 — 提交推送VC-CSA实例绑定失败止损验收

- 时间：2026-07-18 23:35:12 +08:00
- 类型：SYNC | PROGRESS | AUDIT
- 任务/门：00-T-AFFC总控 / VC-CSA实例绑定失败同步
- 状态：止损验收已推送；等待外部实例状态变化
- 负责人：Codex

### 背景与目标

固定WR-037的失败验收、`SC-20260718-06`、暂停权限和S11等待合同，并记录实际远端同步结果。

### 实际变更

- 仅暂存并提交四项00文件：`.light/decision_log.md`、`.light/handoff/S11-vccsa-instance-binding-failure-accepted.md`、`TASK00_VCCSA_INSTANCE_BINDING_FAILURE_ACCEPTANCE_20260718.md`和`WORK_LOG.md`。
- 创建提交`f95815f742abb941571461a41a8b948e5a71d759`并推送`origin/main`。
- 未重试SSH、未修改任务20合同/代码/测试，未操作任何I3D资产。

### 验证与证据

- 提交前`validate_work_log.py`：127条、latest=`WR-20260718-037`、`passed=true`。
- 默认`.venv`的`run_preparation_checks.py`：exit 0、`blocking_checks=[]`，如实保持`formal_model_work_ready=false`。
- S11交接结构6项通过；`git diff --check`和`git diff --cached --check`均exit 0。
- `git commit -m "docs(task00): accept VC-CSA instance binding stop"`：commit=`f95815f742abb941571461a41a8b948e5a71d759`，4 files changed、134 insertions。
- `git push origin main`：`5ddb1f6..f95815f main -> main`；推送后`HEAD=origin/main=f95815f742abb941571461a41a8b948e5a71d759`、工作区clean。

### 影响与边界

远端main现正式记录`EFFECTIVE_I3D_TRANSFER_PERMISSION=SUSPENDED_INSTANCE_BINDING_FAILED_DO_NOT_TRANSFER`。合同hash验收仍有效；同一实例恢复可重试三元绑定，换实例必须重新授权。

### 风险、问题与阻塞

当前阻塞依赖用户或平台恢复实例SSH服务。无新mitigation前不得重复失败探针；真实I3D保持0上传、训练0次。

### 下一步

1. 通知任务20验收提交与暂停状态，要求保持idle。
2. 等待用户确认同一实例恢复，或提供新实例以重新授权。
3. 继续监督G3、任务50和资产/claim边界。

### Git状态

本同步日志自身尚未提交或推送；主验收提交`f95815f742abb941571461a41a8b948e5a71d759`已推送。

## WR-20260719-001 — 扩权任务20在新GPU实例完成完整探索链

- 时间：2026-07-19 10:45:59 +08:00
- 类型：DECISION | AUTH | SECURITY | RISK | DOC
- 任务/门：00-T-AFFC总控 / VC-CSA新实例完整执行授权
- 状态：任务20完整探索执行获批；取消中间二次签字
- 负责人：Codex

### 背景与目标

用户先提供一个与S11失败目标不同的新GPU实例并请求绑定授权，随后明确要求以完成实验为核心并授权任务20的一切必要请求。00需把扩权落成可执行范围，避免每个绑定/排障步骤再次等待总控，同时保持实验身份和不可伪造事实边界。

### 实际变更

- 新建`TASK00_VCCSA_NEW_INSTANCE_FULL_EXECUTION_AUTHORIZATION_20260719.md`，记录`SC-20260719-01`并绑定当前规范化endpoint digest。
- 更新`.light/decision_log.md`，授权任务20完成三元绑定后直接执行原探索合同全链及必要工程排障。
- 新建`.light/handoff/S12-task20-new-instance-full-execution-authorized.md`，把00职责改为持续监督而非逐步卡签。
- 未连接新实例，未修改任务20合同/代码/测试，未读取、hash或传输I3D。

### 验证与证据

- 开工发现本线程隔离worktree仍停在`e6c48c6`且已有旧S02/WORK_LOG未提交改动，故未在旧worktree写入或覆盖；经用户批准切换到共享主仓库审查。
- 共享主仓库刷新为`HEAD=origin/main=b914edef1c660ac4958ec9535c3f2927f7f71f71`、工作区clean；任务20线程idle。
- 任务20回传规范化endpoint digest=`4af92a8622db78ce968bdb49b98f06ef26d4151a943c885ad03de5548eb32cdc`，并确认授权前SSH 0连接、I3D 0上传、训练0次、远端受限目录0创建。
- 00只记录digest，不记录或传播端点原文、用户名、端口、密码或其他凭据。
- 用户后续明确扩权取消额外审批等待；00未把该扩权解释为允许泄露凭据、公开受限资产、伪造结果或扩展至任务20之外。

### 影响与边界

任务20现在可自主完成当前探索诊断所需的连接、绑定、依赖、传输、运行、故障重试和清理。三元绑定成功后无需回00二次签字；实例失败时可排障或换实例重绑定。

探索结果仍永久NON_T0/INELIGIBLE，不能进入正式证据；任务30、任务50和IJCV不在本扩权范围。

### 风险、问题与阻塞

- 新实例host-key与GPU UUID尚未验证；任务20须在首次资产操作前完成本地三元绑定。
- 用户曾在私密会话提供认证信息；该信息不得进入仓库、日志或回传材料，建议任务完成后轮换。
- I3D许可、官方revision、权利方包身份/fixity继续UNKNOWN。

### 下一步

1. 提交推送本扩权、决策日志、WR-001与S12。
2. 通知任务20直接推进三元绑定与完整合同执行，无需逐步回请00。
3. 00持续监督失败实录、单完成seed、NON_T0/INELIGIBLE和删除核验。

### Git状态

本条写入时上述四项00文件尚未提交或推送；新实例尚未连接。

## WR-20260719-002 — 提交推送任务20新实例完整执行扩权

- 时间：2026-07-19 10:53:44 +08:00
- 类型：SYNC | PROGRESS | AUDIT
- 任务/门：00-T-AFFC总控 / 任务20完整探索执行授权同步
- 状态：完整执行扩权已推送；任务20可直接推进
- 负责人：Codex

### 背景与目标

固定WR-001的用户优先级、`SC-20260719-01`完整执行扩权和S12监督合同，并记录实际远端同步结果。

### 实际变更

- 仅暂存并提交四项00所有权文件：`.light/decision_log.md`、`.light/handoff/S12-task20-new-instance-full-execution-authorized.md`、`TASK00_VCCSA_NEW_INSTANCE_FULL_EXECUTION_AUTHORIZATION_20260719.md`和`WORK_LOG.md`。
- 创建提交`6c3b2cf924ad383f324daffb30fde68fcd0bd69a`并推送`origin/main`。
- 未连接新实例，未操作I3D，未修改任务20实验代码或合同。

### 验证与证据

- 第一次用临时统一补丁向共享主仓库落盘时，因hunk声明行数与实际正文不一致，`git apply`在写入前以`corrupt patch`失败；主仓库未改动。随后使用`git apply --recount`按实际行数重算，检查与应用均通过。
- 提交前`validate_work_log.py`：129条、latest=`WR-20260719-001`、`passed=true`。
- 默认`.venv`的`run_preparation_checks.py`：exit 0、`blocking_checks=[]`；如实保持`formal_model_work_ready=false`。
- S12交接结构6项通过；`git diff --check`和`git diff --cached --check`均exit 0；secret scan无命中。
- `git commit -m "docs(task00): authorize task20 full exploratory execution"`：commit=`6c3b2cf924ad383f324daffb30fde68fcd0bd69a`，4 files changed、135 insertions。
- `git push origin main`：`b914ede..6c3b2cf main -> main`；推送后`HEAD=origin/main=6c3b2cf924ad383f324daffb30fde68fcd0bd69a`、工作区clean。

### 影响与边界

远端main现正式授权任务20在三元绑定后无需00二次签字，直接完成8210 fixity、传输、远端复核、唯一seed=3407、最小证据和删除核验，并可自主处理工程故障或替代实例重绑定。

### 风险、问题与阻塞

实例身份尚未验证，凭据仍须只在私密执行上下文使用。实验结果永久NON_T0/INELIGIBLE，不能升级为正式证据。

### 下一步

1. 通知任务20刷新`6c3b2cf`并直接推进完整探索执行。
2. 00持续监督关键阶段证据、失败实录和删除核验，不再制造逐步审批等待。
3. 保持任务30、任务50执行和IJCV范围冻结。

### Git状态

本同步日志自身尚未提交或推送；主授权提交`6c3b2cf924ad383f324daffb30fde68fcd0bd69a`已推送。

## WR-20260719-003 — 验收任务20受限存储、快照与配置镜像补充授权

- 时间：2026-07-19 12:43:35 +08:00
- 类型：DECISION | AUTH | DATA | RISK | DOC
- 任务/门：00-T-AFFC总控 / VC-CSA受限资产存储补充授权
- 状态：私有存储、快照和配置镜像获批并可执行
- 负责人：Codex

### 背景与目标

用户明确新增最高授权，允许任务20受限I3D进入MatBox网盘、对象存储或环境快照，并允许配置镜像；同时要求总控验收且不改写此前禁止这些载体的历史合同。任务20报告作者原设定探索训练已在A30以seed=3407启动。

### 实际变更

- 新建`TASK00_VCCSA_RESTRICTED_STORAGE_AND_IMAGE_SUPPLEMENT_AUTHORIZATION_20260719.md`，记录`SC-20260719-02`，以补充授权方式允许私有网盘、对象存储、环境/卷快照及配置镜像。
- 更新`.light/decision_log.md`，保留旧合同历史字节并固定存储范围、fixity、权限、保留/删除和claim边界。
- 新建`.light/handoff/S13-restricted-storage-and-image-supplement-accepted.md`，传播目标绑定、8210 fixity、30日保留和删除监督要求。
- 未修改任务20旧/新合同、代码、测试、A30运行过程或未跟踪`tmp/`运行材料；未执行任何网盘、对象存储或快照操作。

### 验证与证据

- 开工刷新：`HEAD=origin/main=8f9fae4442ec3b4b74b7ace30bd04ae3d2e9701d`；任务20线程报告A30训练已启动并请求00验收。
- 共享主仓库存在任务20所有权的未跟踪`tmp/`运行目录，包含作者runtime/评论/模型归档和传输脚本；00仅目录级盘点，未读取、移动、暂存、提交或删除其中任何受限材料。
- 用户明确允许MatBox、对象存储、快照和配置镜像；00将此解释为内部私有处理授权，不冒充权利方许可、公开发布或再分发权。
- 使用`light-data-engineering`将存储对象限制为固定8210和可重算fixity；使用`light-research-ethics`将保留期限、删除可见层证据、平台控制面UNKNOWN和结果claim边界显式落盘。

### 影响与边界

任务20可立即创建私有存储目标、绑定非秘密摘要、备份/恢复8210与运行环境并继续训练，无需00逐步签字。运行快照可包含为运行所必需的受限runtime，但Git不得承载任何I3D或可逆受限材料。

实验身份仍为`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`，`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`；存储扩权不进入G3、T0、统一baseline、任务50或论文正式claim。

### 风险、问题与阻塞

- 实际MatBox/bucket/snapshot目标尚未由任务20绑定；本授权定义逻辑区域与私有ACL要求，实际定位符不得入Git。
- I3D许可、官方revision、权利方包身份/fixity继续UNKNOWN；用户接受的是内部处理与平台控制面风险。
- 当前A30训练运行中，00不得并发改写任务20核心或运行材料。

### 下一步

1. 提交推送本补充授权、决策日志、WR-003和S13。
2. 通知任务20可创建私有存储/快照、记录非秘密绑定与fixity摘要，并继续seed=3407训练。
3. 持续监督训练结果、存储目标、删除计划和NON_T0/INELIGIBLE边界。

### Git状态

本条写入时上述四项00文件尚未提交或推送；任务20的未跟踪`tmp/`仍由任务20所有。

## WR-20260719-004 — 提交推送任务20受限存储补充授权

- 时间：2026-07-19 12:54:28 +08:00
- 类型：SYNC | PROGRESS | AUDIT
- 任务/门：00-T-AFFC总控 / VC-CSA受限存储补充授权同步
- 状态：补充授权已推送；任务20可执行私有存储/快照/配置镜像
- 负责人：Codex

### 背景与目标

固定WR-003的`SC-20260719-02`、S13和版本化存储边界，并记录环境门禁与Git权限失败的真实结果及后续同步状态。

### 实际变更

- 仅暂存并提交四项00所有权文件：`.light/decision_log.md`、`.light/handoff/S13-restricted-storage-and-image-supplement-accepted.md`、`TASK00_VCCSA_RESTRICTED_STORAGE_AND_IMAGE_SUPPLEMENT_AUTHORIZATION_20260719.md`和`WORK_LOG.md`。
- 创建提交`29cee82f6af22f7c392d799e5e276af0cf21c4b9`并推送`origin/main`。
- 未暂存、移动、读取或删除任务20未跟踪`tmp/`运行材料，未执行存储、快照、传输或训练命令。

### 验证与证据

- 默认`.venv`与`.venv-task20`均因其`pyvenv.cfg`指向已不存在的`C:\Users\86183\AppData\Local\Programs\Python\Python38`而无法启动`validate_work_log.py`/`run_preparation_checks.py`；失败未删除。
- 使用Codex bundled Python运行`validate_work_log.py`：131条、latest=`WR-20260719-003`、`passed=true`；同一解释器运行准备检查因缺少`yaml`模块失败，未冒充通过。
- S13交接结构6项通过，`git diff --check`通过。
- 首次普通Git暂存/提交因无法创建`.git/index.lock`超时失败，未产生提交；经提升Git索引写权限后，`git diff --cached --check`通过，暂存范围严格为四项00文件。
- `git commit -m "docs(task00): authorize restricted storage supplement"`：commit=`29cee82f6af22f7c392d799e5e276af0cf21c4b9`，4 files changed、137 insertions。
- `git push origin main`：`8f9fae4..29cee82 main -> main`；推送后`HEAD=origin/main=29cee82f6af22f7c392d799e5e276af0cf21c4b9`。工作区仅余任务20所有的未跟踪`tmp/`。

### 影响与边界

远端main现正式允许私有MatBox、私有对象存储、私有环境/卷快照和非敏感配置镜像。任务20可直接绑定实际私有目标、执行fixity、备份/恢复及继续A30训练；旧合同字节与NON_T0/INELIGIBLE结果边界不变。

### 风险、问题与阻塞

- 本地两套Python 3.8虚拟环境已漂移失效，且bundled Python缺少PyYAML；本批准备检查没有可运行环境，需后续修复/重建，但不影响远端A30训练事实。
- 平台控制面、I3D许可、官方revision和权利方包身份/fixity继续UNKNOWN；用户已接受私有存储残余风险。

### 下一步

1. 通知任务20使用`29cee82`授权，创建私有存储/快照目标并记录非秘密绑定、ACL和fixity摘要。
2. 持续监督A30 seed=3407训练、存储恢复及30日删除计划；不再并发改写任务20运行材料。
3. 修复本地Python门禁环境后重跑项目准备检查，并如实记录结果。

### Git状态

本同步日志自身尚未提交或推送；主补充授权提交`29cee82f6af22f7c392d799e5e276af0cf21c4b9`已推送，`tmp/`仍未跟踪且归任务20所有。

## WR-20260719-005 — Task20 private MatBox backup binding and fixity verification

- 时间：2026-07-19 +08:00
- 类型：DATA | SECURITY | PROGRESS
- 任务/门：Task20 VC-CSA exploratory execution / SC-20260719-02
- 状态：completed for MatBox I3D backup and configuration mirror; runtime snapshot deferred while training is active
- 负责人：Codex

### 背景与目标

Apply the accepted restricted-storage supplement to the active A30 seed=3407 exploratory run without changing its permanent `AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY` and `FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE` boundaries.

### 实际变更

- Refreshed `main` at `bd6bfbdaa06571f2afb82ed9f6c041e1373cd801` and read `TASK00_VCCSA_RESTRICTED_STORAGE_AND_IMAGE_SUPPLEMENT_AUTHORIZATION_20260719.md` plus S13.
- Bound one private MatBox target: `storage_target_digest=2c9b6bedc811c90ecfd230d1fd03d7b236e29d9a9b49f38be7c8415f50ca9e58`; region category `matbox-private`; target ACL summary `directory 0700, owner-only`; encryption/platform control-plane status `UNKNOWN_PLATFORM_CONTROL_PLANE`.
- Copied only the fixed 8210 I3D `.npy` files to that target and created a separate non-sensitive configuration mirror: `storage_target_digest=f2d4841dcda36c912d5b94984fd823c1cb64caf08753d10af440c71ef855551c`; region category `config-mirror`; ACL summary `directory 0700, files 0600`.
- Did not create a runtime/volume snapshot because A30 training is active; did not create object storage; did not place restricted assets, comments, labels, weights, predictions, credentials, or endpoint text in Git.

### 验证与证据

- `tmp/task20_remote_fixity.py` verified the source before copy and the MatBox copy after copy: `files=8210`, `bytes=2283804928`, `missing=[]`, `extra=[]`, `size_mismatch=[]`, `sha256_mismatch=[]`, `content_tree_sha256=592eb698694388f3ab169c924f88e470daa64d5b496ff007cec390f7d1ada925`, directories `0700`, file-mode errors `0`.
- Remote mount inspection reported a private mounted volume with 55 GB free and no public/anonymous ACL evidence exposed through the mount; GPU training remained active during copy.
- Configuration mirror contains only a sorted dependency lock and Python version record; no restricted reversible content or credentials.

### 影响与边界

The current A30 run can now be recovered from a private MatBox I3D copy after fresh fixity verification. This storage action does not make the experiment formal evidence, T0-compatible, leakage-free, publishable, or eligible for G3, unified baselines, Task50, or paper claims.

### 风险、问题与阻塞

- Static encryption and platform-side retention are not observable from the mounted volume and remain `UNKNOWN_PLATFORM_CONTROL_PLANE`.
- The storage supplement requires restricted I3D/runtime material to be deleted 30 calendar days after minimum-evidence acceptance unless the user extends retention. Runtime snapshot creation is deferred until training is paused/completed because platform guidance advises against saving an active environment.
- Initial remote-copy invocation failed locally before connection because PowerShell expanded a shell variable; no remote directory was created by that failed attempt. The fixed command subsequently completed.

### 下一步

1. Monitor the active seed=3407 training and create a private runtime snapshot only at a safe pause/completion point.
2. Record final training evidence, retention deadline, and visible-layer deletion plan; run the required work-log and preparation checks once a runnable local gate environment is restored.

### Git状态

`WORK_LOG.md` is modified and uncommitted; `tmp/` remains untracked Task20 operational material. No restricted asset is staged or committed.

## WR-20260719-006 — 00接受Task20 MatBox存储补充执行

- 时间：2026-07-19 +08:00
- 类型：DECISION | AUDIT | DATA | SECURITY | DOC
- 任务/门：00 T-AFFC总控 / SC-20260719-03
- 状态：接受已报告的MatBox I3D备份和非敏感配置镜像；运行时快照仍延期
- 负责人：Codex

### 背景与目标

Independently review task20's S13 execution record at `origin/main@229dbcd0b38cd13ecb945c63c94f31feab91f687` against the versioned storage authorization, while preserving task20 ownership of ignored runtime material.

### 实际变更

- Added `TASK00_TASK20_STORAGE_SUPPLEMENT_EXECUTION_ACCEPTANCE_20260719.md`, decision-log entry `SC-20260719-03`, and S14 handoff.
- Accepted only the reported private MatBox I3D backup (target digest `2c9b6bedc811c90ecfd230d1fd03d7b236e29d9a9b49f38be7c8415f50ca9e58`) and separate non-sensitive configuration mirror (digest `f2d4841dcda36c912d5b94984fd823c1cb64caf08753d10af440c71ef855551c`).
- Did not read, stage, move, delete or inspect contents of task20-owned ignored `tmp/`; did not connect to MatBox or access raw endpoints, credentials, or restricted files.

### 验证与证据

- `git fetch origin; git status --short --branch; git log --oneline -5 origin/main; git rev-parse origin/main` refreshed `origin/main=229dbcd0b38cd13ecb945c63c94f31feab91f687`; only `?? tmp/` was untracked.
- `git show --format=fuller --no-ext-diff --unified=35 229dbcd -- WORK_LOG.md` independently reviewed WR-20260719-005. It reports I3D `count=8210`, `bytes=2283804928`, all four mismatch lists empty, tree hash `592eb698694388f3ab169c924f88e470daa64d5b496ff007cec390f7d1ada925`, private `0700`/`0600` modes, and UNKNOWN platform control plane.
- The reported target scope and retention policy match SC-20260719-02. This is documentary acceptance: 00 did not directly rerun the target-side copy, fixity, or ACL check.

### 影响与边界

The private backup/config mirror is accepted as an authorized operational artifact. `RUNTIME_SNAPSHOT=DEFERRED_NOT_STARTED`; A30 seed=3407 is only reported active, not complete and not accepted as a result. The exploration remains NON_T0/INELIGIBLE; no G3, T0, unified baseline, Task50 or paper claim is created.

### 风险、问题与阻塞

- Platform control plane and static encryption remain UNKNOWN. I3D license, official revision, and rightsholder package identity/fixity remain UNKNOWN; denial or 8210 drift invalidates assets for reporting.
- Local `.venv` and `.venv-task20` remain unusable because their configured Python 3.8 is absent; bundled Python lacks PyYAML, so 00 cannot truthfully rerun preparation checks in this checkout.

### 下一步

1. Supervise task20's active exploratory run, safe runtime snapshot if created, and final retention/deletion evidence.
2. Repair a local gate environment before independently rerunning the preparation check; retain the actual failure record until then.

### Git状态

This 00 acceptance batch is uncommitted at write time. Only 00-owned decision, acceptance, handoff and WORK_LOG files are intended for staging; `tmp/` remains task20-owned and untracked.

## WR-20260720-001 — 全项目复盘并登记Task20实时训练中断

- 时间：2026-07-20 +08:00
- 类型：AUDIT | PROGRESS | RISK | DOC
- 任务/门：00-T-AFFC总控 / 全项目状态复盘
- 状态：完成全景复盘；Task20 A30探索训练中断待恢复
- 负责人：Codex

### 背景与目标

用户要求详细说明项目从开始至今的工作、成果、问题、整体思路和下一步目标。总控需要以实时Git、权威门文件、实验台账和任务20实时状态交叉复核，不能把旧交接卡或过期`.light`状态当成当前事实。

### 实际变更

- 新建`PROJECT_STATUS_RETROSPECTIVE_20260720.md`，按研究重构、数据协议、统一评测、VC-CSA补充探索、存储、成果、问题和下一步组织全项目快照。
- 新建`.light/handoff/S15-project-retrospective-and-task20-runtime-failure.md`，传播实时训练中断和账本治理缺口。
- 未读取、移动、暂存或删除任务20所有的未跟踪`tmp/`运行材料；未修改实验核心、模型、结果或受限资产。

### 验证与证据

- `git fetch origin; git status --short --branch; git log --oneline --decorate -12 origin/main`：刷新到`main=origin/main=6534a0834f793426afc4aa2a97da697f1825ea66`，仅`?? tmp/`未跟踪。
- 读取总纲v1.16、`.light/passport.yaml`、`.light/project_card.md`、G1/G2/G3复审、dataset/split/label manifests、baseline table、实验登记、风险登记和134条既有WORK_LOG标题。
- 任务20实时线程在2026-07-20报告：A30训练因`DataLoader worker ... killed by signal: Killed`停止，GPU空闲，未完成首epoch；约0.36 loss只作诊断，不作结果。
- 文件存在性审计确认`TASK_REGISTRY.md`、`GATE_G1.md`至`GATE_G6.md`和`TAFFC_GO_NO_GO.md`尚不存在；handoff目录无S02而S03的`parent_session: S02`。
- 首次运行独立`handoff_contract.py`对S15返回exit 1：内容存在但使用英文节标题，缺少机器要求的`当前阶段/已完成/工作区状态/待用户回答/下一步/阻塞/风险/必读文件/禁止`固定章节；失败保留后已按模板修正，待重新验证。
- 第二次运行`handoff_contract.py`仍返回exit 1：`待用户回答`的none格式、三条已完成证据写法和工作区dirty/unpushed措辞不符合机器合同；继续保留失败并收紧为精确artifact—verification、裸`none`和Git状态表述，待第三次验证。
- 第三次运行`handoff_contract.py`仍返回exit 1：裸`none`被判空，且三条英文`verified`不命中验证证据词表；已按模板改为唯一`- none — 具体原因`并将证据措辞改为`验证/commit/PASS`，待第四次验证。
- 第四次运行`handoff_contract.py --as-of 2026-07-20`返回PASS；bundled Python工作日志验证为135条、latest=WR-20260720-001、passed=true，`git diff --check`通过。
- 当前`.venv`/`.venv-task20`的`pyvenv.cfg`均指向Python 3.8.9，基础解释器路径现为存在；但`.venv`的`python --version`、日志校验和准备检查组合在30秒内无输出并超时。bundled Python运行准备检查明确因`ModuleNotFoundError: yaml`返回exit 1，故当前总控准备门仍不可运行，未冒充通过。

### 影响与边界

正式门不变：G1 PASS、G2协议/数据PASS_WITH_LIMITATIONS、资产DEFERRED_ACCEPTED_RISK、G3 PASS_WITH_LIMITATIONS。Task20探索永久NON_T0/INELIGIBLE；本批没有接受其训练结果，也没有创建任务30。

### 风险、问题与阻塞

- Task20 A30探索因DataLoader worker被Killed而中断，需降低worker并监控RAM后再恢复。
- `.light/passport.yaml`和`.light/project_card.md`仍停留在G3前状态，且本地总控Python门禁环境漂移；这些治理缺口不推翻正式审查文件，但必须在任务30前修复。
- I3D许可、官方revision和权利方包身份/fixity仍UNKNOWN；资产止损条件不变。

### 下一步

1. 监督任务20记录并修复DataLoader失败，独立审查恢复后的真实证据。
2. 重建本地门禁环境，使用底层passport路径更新过期账本并修复/说明S02链缺口。
3. 待任务20停止修改实验核心且交接完整后，再复核任务30创建条件。

### Git状态

本条写入时，全项目复盘、S15和WORK_LOG尚未提交；只计划暂存这三项00文件，`tmp/`继续未跟踪且归任务20所有。

## WR-20260720-002 — Task20 DataLoader worker failure and recovery

- 时间：2026-07-20 +08:00
- 类型：FIX | PROGRESS | TEST | RISK
- 任务/门：Task20 VC-CSA author exploratory seed=3407 / S15 follow-up
- 状态：失败已保留，`num_workers=0` 恢复运行中
- 负责人：Codex

### 背景与目标

00 已审计：原作者训练在第 1 epoch 未完成时因 DataLoader worker 被系统杀掉而中断。本批仅处理 worker 数与恢复运行，不改实验身份、分割、指标或 claim 边界。

### 实际变更

- 保留原始失败日志，不覆盖。原运行到 epoch 1 step 4269/4692，最后可见 `Loss_sum=0.1785` 仅为诊断，随后报告 `DataLoader worker ... killed by signal: Killed`。
- 将远端作者启动器的 `num_workers` 从 8 降至 0，保留同一 `seed=3407`、批大小、学习率、数据和模型配置。
- 重新启动后使用独立日志文件，不把失败尝试写成完成。

### 验证与证据

- 失败时远端 RAM 可用约 85 GB，故不将诊断结果写成 GPU OOM；根因仅记为 worker 被系统杀掉。
- 恢复后实时进程证据显示作者入口包含 `--num_workers 0` 且进程存活；约 step 126/4692，GPU 约 82%，显存约 14518 MiB，RAM 可用约 82 GB。
- 恢复日志当前最新诊断 loss 约 `Loss_sum=0.3637`，不作任何结果或 epoch 完成证据。

### 影响与边界

当前只是同一个已注册 seed 的工程恢复尝试；任务仍永久 `AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY` 且 `FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`。首个 epoch 尚未完成，不形成训练结果。

### 风险、问题与阻塞

- `num_workers=0` 可降低 worker 被杀风险，但训练速度和是否能完成首个 epoch 仍待监控。
- 本地 git 上游已是 `48201e9`；此次仅追加 Task20 自有工作记录，不修改 00 复盘/S15。

### 下一步

1. 持续监控进程、RAM/GPU、最新 loss 和 checkpoint。
2. 首个 epoch 或新失败出现后追加真实证据；不将中断、超时或部分运行标记为完成。

### Git状态

本条记录待提交；`tmp/` 继续为 Task20 所有的未跟踪运行工具。

## WR-20260720-003 — 00验收Task20 DataLoader恢复为运行中未完成

- 时间：2026-07-20 16:19:48 +08:00
- 类型：DECISION | PROGRESS | TEST | RISK | DOC
- 任务/门：00总控 / Task20 VC-CSA author exploratory seed=3407 / S16
- 状态：完成；恢复状态验收为`ACCEPTED_RUNNING_NOT_COMPLETED`
- 负责人：00-T-AFFC总控Codex

### 背景与目标

Task20在保留epoch 1 DataLoader worker被`Killed`的失败记录后，将远端启动器`num_workers`从8降为0，并推送仅含自身WORK_LOG的`main@7d686dd`。本批由00独立复核提交边界、实时任务状态和claim边界，决定是否接受恢复状态。

### 实际变更

- 新增`TASK00_TASK20_DATALOADER_RECOVERY_ACCEPTANCE_20260720.md`，裁定`TASK20_DATALOADER_RECOVERY=ACCEPTED_RUNNING_NOT_COMPLETED`。
- 新增`.light/handoff/S16-task20-dataloader-recovery-running.md`，延续总控交接链。
- 未修改总纲、G门、实验代码、运行配置或Task20的`tmp/`。

### 验证与证据

- 运行`git fetch origin`、`git status --short --branch`、`git log -5`、`git show 7d686dd`和`git diff --name-status 48201e9..7d686dd`：`main=origin/main=7d686dd2497b90099ac63596f531d3e8ef7286f9`，Task20提交仅修改`WORK_LOG.md`。
- 读取任务20实时任务：恢复进程报告使用`--num_workers 0`并存活至约step 126/4692；GPU约82%、显存约14518 MiB、RAM可用约82 GB。00未直接登录远端，以上是Task20报告并由tracked日志固定的证据。
- 原失败保留为epoch 1 step 4269/4692后worker被信号`Killed`；失败时RAM可用约85 GB，不支持GPU OOM表述。
- `Loss_sum=0.1785`和恢复运行中的约`0.3637`均为中途诊断值；首个epoch、checkpoint及完整训练均未完成。
- 首次运行`handoff_contract.py --as-of 2026-07-20`失败：两条已完成事项缺少机器可识别的验证证据、一条下一步动作格式不足；修正验证措辞后第二次仍因“运行”不匹配动作词正则而失败；再将其改为“跑”后，第三次仍定位出另一条的“重建”不在动作词正则。三次均未改变科学裁定，失败全部保留，并将相应动词改为合同可识别字面后再次复验。
- 第四次运行同一`handoff_contract.py`命令得到`handoff contract PASS`。
- 用bundled Python运行`scripts/run_preparation_checks.py`失败，真实错误为`ModuleNotFoundError: No module named 'yaml'`；这是已知本地门禁环境阻塞，未冒充准备检查通过。

### 影响与边界

恢复动作可继续，但不得升级为结果。实验继续永久为`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`、`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`。G1、G2、资产风险和G3裁定均不变；任务50未完成，任务30未创建。

### 风险、问题与阻塞

- `num_workers=0`是否足以完成首个epoch仍UNKNOWN；新失败必须单独记录。
- 本地旧venv不可用，bundled Python缺PyYAML，准备检查仍不可完整复跑；不得冒充当前准备门PASS。
- I3D许可、官方revision、权利方包身份/fixity仍UNKNOWN；8210项hash/覆盖漂移或权利方否认仍触发`ASSET_INVALIDATED_DO_NOT_REPORT`。
- `.light/passport.yaml`、`.light/project_card.md`和任务/门索引仍待后续修复。

### 下一步

1. 持续监督同一seed；首个epoch/checkpoint完成、完整训练完成或再次失败时再更新状态。
2. 用新mitigation修复本地门禁与陈旧`.light`账本；不要重复已知包装导入失败。
3. Task20仍修改或运行共享实验核心时不创建任务30。

### Git状态

本条写入时，00验收文件、S16和WR-20260720-003尚未提交；计划只暂存这三项00文件，`tmp/`继续未跟踪且归Task20所有。

## WR-20260723-001 — 形成教师阶段汇报并刷新Task20远端状态

- 时间：2026-07-23 +08:00
- 类型：AUDIT | PROGRESS | RISK | DOC
- 任务/门：00总控 / 教师阶段汇报 / Task20收尾监督
- 状态：完成汇报稿；Task20远端状态UNAVAILABLE
- 负责人：00-T-AFFC总控Codex

### 背景与目标

用户即将向老师汇报，要求用简洁、连贯、易懂的语言概括项目开始至今的任务、工作、问题和下一步。总控需要先刷新Git和任务20实时状态，避免把2026-07-20的运行中状态误写成2026-07-23的完成事实。

### 实际变更

- 新增`TEACHER_BRIEFING_20260723.md`，将研究重构、数据工程、统一评测、VC-CSA补充、主要风险和后续路线合并为可口头汇报的长句与段落。
- 新增`.light/handoff/S17-teacher-briefing-and-task20-unreachable.md`，传播最新远端UNAVAILABLE状态和下一会话入口。
- 未修改总纲、正式G门、实验核心或结果，未触碰任务20的`tmp/`。

### 验证与证据

- `git fetch origin; git status --short --branch; git log -8`确认`main=origin/main=24a3af3241e897569caccb03e756b9dae61e94ae`，仅`?? tmp/`未跟踪。
- 读取AGENTS、WORK_RECORD_POLICY、S16、全项目复盘和最新WORK_LOG，确认正式门仍为G1 PASS、G2协议/数据PASS_WITH_LIMITATIONS、资产DEFERRED_ACCEPTED_RISK、G3 PASS_WITH_LIMITATIONS。
- 读取任务20实时任务：2026-07-23探针报告原远端SSH端口不可达，无法确认训练继续、停止或实例释放；因此维持“无已验收完成证据”，不把此前运行中推定为完成。
- bundled Python运行`scripts/validate_work_log.py`得到`entries=138`、`latest_id=WR-20260723-001`、`passed=true`；运行`handoff_contract.py --as-of 2026-07-23`得到`handoff contract PASS`，`git diff --check`通过。
- bundled Python运行`scripts/run_preparation_checks.py`仍失败于`ModuleNotFoundError: No module named 'yaml'`；该既有环境失败保留，未冒充准备门通过。

### 影响与边界

本批只形成面向教师的阶段汇报和最新状态交接，不新增科研结果。Task20统一基线/G3主体已完成，但VC-CSA探索仍永久NON_T0/INELIGIBLE且未闭环；任务50和任务30均未完成或创建。

### 风险、问题与阻塞

- 远端SSH不可达使VC-CSA训练后续状态UNAVAILABLE；不可解释为完成或失败。
- I3D许可、官方revision、权利方包身份/fixity仍UNKNOWN。
- 本地门禁环境、陈旧`.light`账本、任务/门索引和S02链缺口仍待修复。

### 下一步

1. 监督任务20恢复连接或形成明确终止/不可用收尾证据。
2. 修复本地门禁和总控账本，在任务20完成共享核心收尾后复核任务30创建条件。
3. 按总纲继续任务30、40、50、60，逐步形成CARM方法、正式统计和论文证据。

### Git状态

本条写入时，教师汇报稿、S17和WR-20260723-001尚未提交；计划只暂存这三项00文件，`tmp/`继续未跟踪且归Task20所有。
