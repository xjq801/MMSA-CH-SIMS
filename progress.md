# 进度日志

## 会话：2026-07-14

### 阶段1：总纲与现状提取
- **状态：** complete
- **开始时间：** 2026-07-14
- 执行的操作：
  - 读取 planning-with-files-zh 完整规范及模板。
  - 确认项目根目录此前没有规划文件。
  - 建立本次规划的持久化三文件。
  - 完整提取总纲的研究对象、C1—C3、H1—H4、E0—E9、M1—M10、G1—G6及投稿Go标准。
  - 复核T0政策与数据来源台账。
- 创建/修改的文件：
  - `task_plan.md`
  - `findings.md`
  - `progress.md`

### 阶段2：任务边界与依赖设计
- **状态：** complete
- 执行的操作：
  - 将M1—M10映射为00—60七个Codex任务。
  - 确认任务创建顺序、硬门、止损和并行边界。
  - 为每个任务定义输入、步骤、交付物、质量等级和禁止事项。

### 阶段3：执行规格成文
- **状态：** complete
- 执行的操作：
  - 创建645行的`CODEX_TASK_TREE_EXECUTION_SPEC.md`。
  - 覆盖00、10、20、30、40、50、60七个任务。
- 创建/修改的文件：
  - `CODEX_TASK_TREE_EXECUTION_SPEC.md`

### 阶段4：一致性验证
- **状态：** complete
- 执行的操作：
  - 校验G1—G6、H1—H4、E0—E9全部出现。
  - 校验T0政策、数据台账和LEAKAGE_BLOCKED边界。
  - 扫描模板残留，未发现占位符。

### 阶段5：交付
- **状态：** complete
- 执行的操作：
  - 准备向用户交付详细规格文件、任务摘要和当前执行顺序。

### 阶段6：规格并入总纲
- **状态：** complete
- 执行的操作：
  - 用户要求将详细规格直接并入总纲，避免后续任务遗漏需求。
  - 决定新增总纲第17节并将版本升级为v1.5。
  - 已将00—60完整规格内嵌，并把独立规格文件定位为便捷副本。
  - 已同步开工大纲、T0政策和项目记忆中的现行主纲版本引用。
  - 第17节与独立规格正文机械比对一致；结构、门禁、假设、实验编号和模板残留检查通过。
  - 已通知现有任务10切换到v1.5并重新读取总纲第17节。

### 阶段7：开工准备包审计与补齐
- **状态：** complete
- **开始时间：** 2026-07-14
- 执行的操作：
  - 读取总纲开工准备包八类要求。
  - 读取文件规划与项目结构技能；对现有仓库采用先审计、保留未跟踪资产、不自动移动文件的边界。
  - 会话恢复检查确认上一阶段已同步，无需重做总纲整合。
  - 只读审计Git状态、目录、忽略规则、磁盘、环境、敏感信息信号、符号链接和大文件。
  - 当前历史环境`pip check`及核心导入通过；确认`faiss`缺失、空环境重建尚无证据。
  - 密钥扫描仅输出位置/类型/指纹，实际命中0；未发现子模块、符号链接或根目录非隔离大文件。
  - 新增非破坏性的目录政策、数据/代码/文稿/文献区说明、统一配置、配置验证器、负测试、环境smoke、实验登记、claim—evidence、安全清单、资源政策和验收报告。
  - 运行配置验证和负测试，均通过；Python脚本编译通过。
  - 准备检查器判定`m1_read_only_work_ready=true`；正式CARM环境因faiss缺失按设计判为`BLOCKED_M1`。
  - 总纲开工准备包下新增2026-07-14执行状态，明确允许与禁止事项。
  - 共享任务按用户要求创建本地Git基线提交`847a07c`；无远端，未推送。
  - 修复数据区README父目录仍被忽略的问题，最终正向和反向Git策略检查均通过。

## 测试结果
| 测试 | 输入 | 预期结果 | 实际结果 | 状态 |
|------|------|---------|---------|------|
| 规划文件存在性 | 项目根目录 | 三文件存在 | 已创建 | PASS |
| 任务覆盖 | 执行规格 | 00—60七任务齐全 | 全部存在 | PASS |
| 门/假设/实验覆盖 | 总纲 | G1—G6、H1—H4、E0—E9齐全 | 全部存在 | PASS |
| 模板残留 | 执行规格 | 无占位符 | 未发现 | PASS |
| 第17节唯一性 | 总纲 | 标题恰好1处且无多余字符 | 1处，无`+##` | PASS |
| 权威正文同步 | 总纲第17节/独立副本 | 正文完全一致 | 机械比对一致 | PASS |
| 编号覆盖 | 总纲第17节 | 七任务、G1—G6、H1—H4、E0—E9齐全 | 无缺失 | PASS |
| 启动模板 | 总纲第17节 | v1.5、2026-07-14 | 匹配 | PASS |
| 开工配置契约 | bootstrap配置与验证器 | 配置有效、未来评论被拒绝 | CONFIG_VALID、负测试通过 | PASS |
| 历史环境 | `.venv` | pip完整、核心导入可用 | 通过 | PASS |
| 正式CARM环境 | `.venv` | M1前不得误判可用 | faiss缺失，BLOCKED_M1 | EXPECTED_BLOCK |
| 开工综合检查 | `run_preparation_checks.py` | M1只读工作可开始 | ready=true、blocking=[] | PASS |
| 安全与残留 | 项目文本与准备产物 | 密钥0、模板残留0 | 0/0 | PASS |

## 错误日志
| 时间戳 | 错误 | 尝试次数 | 解决方案 |
|--------|------|---------|---------|
| 2026-07-14 | 首次内嵌时第17节标题误带字面量`+` | 1 | 已删除多余字符，并增加标题唯一性检查 |
| 2026-07-14 | `rg`在当前Windows环境启动被拒绝 | 1 | 改用PowerShell `Select-String`完成扫描 |
| 2026-07-14 | 数据区README因父目录规则仍被Git忽略 | 1 | 逐级解除目录、限制放行扩展名，并增加应可跟踪文件的反向测试 |
| 2026-07-14 | `git ls-remote`核验官方远端HEAD超时 | 2 | 停止使用Git传输协议；改采官方网页显示的verified commit/历史链接，不影响许可预审 |

## 五问重启检查
| 问题 | 答案 |
|------|------|
| 我在哪里？ | 阶段6已完成 |
| 我要去哪里？ | 等待任务10按v1.5执行M1–M2并提交G1/G2证据 |
| 目标是什么？ | 让每个Codex任务可直接执行、验收和交接 |
| 我学到了什么？ | 见 findings.md |
| 我做了什么？ | 已创建七任务规格并将其内嵌至总纲第17节 |

### 阶段8：M1预下载许可与可用性审计
- **状态：** in_progress
- **开始时间：** 2026-07-14
- 已完整读取准备验收报告、目录政策、bootstrap配置、实验登记、claim-evidence矩阵、安全清单和资源政策。
- 重复运行`run_preparation_checks.py`：`m1_read_only_work_ready=true`、`formal_model_work_ready=false`、`blocking_checks=[]`；`faiss`缺失仍为预期的`BLOCKED_M1`。
- 保持账户凭证轮换前禁止API/付费调用；本阶段只做公开网页和仓库的只读预下载审计。
- 已定位CSMV官方NeurIPS页/GitHub，以及iNews官方ACL页/GitHub/Hugging Face公开与gated入口；完成首轮许可与媒体可得性差异记录。
- 已确认iNews公开版许可标记、人工标注规模、图像不随数据发布及截图工具边界；识别到互动量字段与截图视觉泄漏的T0 Critical风险。
- 尝试一次批量`git ls-remote`记录三个官方仓库HEAD，因其中至少一个端点超时而整体退出；未下载内容。后续改为逐仓库核验，不重复批量命令。
- 第二次仅核GitHub远端仍超时；已停止该路径，避免第三次重复失败。修订证据改由官方仓库网页记录。
- 已更新`DATA_SOURCE_LEDGER.md`，将CSMV和iNews从笼统`PENDING`细化为`PRE_DOWNLOAD_REVIEW`，但未宣称G1通过。
- 已创建`data-feasibility-matrix.md`与`license-ethics-matrix.md`初稿，记录代码/标注/媒体分层许可、iNews图像可复现风险和T0字段禁用规则。
- 本轮未下载任何数据、代码仓库、特征或媒体，未调用需要凭证的API，未安装依赖或训练模型。

### 开工准备五项复核（2026-07-14）
- 按总纲第17节任务10的开工步骤1—5执行“只验收、只补缺口”；既有工件均已覆盖要求，因此未重复创建或改写核心政策文件。
- 复跑`run_preparation_checks.py`：`m1_read_only_work_ready=true`、`blocking_checks=[]`；密钥扫描0命中、Git忽略与应跟踪文件反向检查通过。
- 复核`.env.example`只含空变量名；StepFun调用代码通过`STEPFUN_API_KEY`环境变量取值，未发现硬编码凭证值。账户侧已暴露凭证轮换仍为`USER_ACTION_REQUIRED`，确认前继续禁止API和付费调用。
- 统一bootstrap配置包含数据版本、split、T0、种子、输入模态、baseline、主指标和停止条件；配置有效与未来评论拒绝两项契约测试直接调用均通过。
- Git对象树复核未发现大型已跟踪文件；原始/处理数据、模型、索引、日志和结果仍由忽略规则阻断，小型manifest和政策文件可跟踪。
- `pytest`当前环境未安装，因此未新增依赖；测试文件中的两个契约函数改为直接调用并通过。正式CARM环境仍按计划保持`BLOCKED_M1`。
- Git远端已配置为`https://github.com/xjq801/MMSA-CH-SIMS.git`；尝试普通HTTPS及HTTP/1.1兼容模式推送准备验收提交`1d7a210`，均因连接被重置失败。当前本地`main`仍比`origin/main`领先1个提交，未把未提交的M1审计草稿混入推送。

### 强制工作记录机制（2026-07-14）
- **状态：** complete
- 新增`WORK_RECORD_POLICY.md`与追加式`WORK_LOG.md`，明确每次功能、进展、修复、重要测试、决策和阻塞变化的必记字段。
- 新增`scripts/validate_work_log.py`及根目录`AGENTS.md`，把“记录后再交付”变成执行代理规范和确定性检查。
- 将工作记录纳入`PROJECT_STRUCTURE_POLICY.md`和`run_preparation_checks.py`；校验器、Python编译、综合准备检查及`git diff --check`均通过。
- `light-memory-pm`初始化脚本因本机技能安装缺少`passport`导入路径及`_shared`模块未能运行；未生成残缺`.light/`目录，采用项目内零新增依赖方案。
- 按用户“重试”要求再次推送GitHub，失败原因为无法连接`github.com:443`；本地`main`仍领先远端1个已提交版本。

### 步骤6—10：现有资产与构念审计（2026-07-14）
- **状态：** complete
- 已读取总纲第17节任务10工作包B与`T0_INPUT_POLICY.md`，冻结本轮只读审计边界。
- `rg`再次被系统拒绝启动，已记录并切换为PowerShell `Select-String`，不再重复失败。
- 已定位旧脚本、报告、实验JSON和外部只读数据根目录之间的主要lineage。
- 已只读复跑`audit_group_dataset.py`，实证2787有效行、2779唯一BV、8条缺BV、221条可匹配标签冲突及883条发布时间覆盖。
- 已定位目标评论进入特征和旧随机split的代码证据，正在形成lineage、旧实验分类、构念/协议冻结和泄漏威胁模型。
- 已完成`legacy-asset-lineage.md`与`legacy-experiment-classification.md`，冻结旧代码和旧结果的不同证据资格。
- 已完成`research-question-v1.md`、`experiment-protocol-v1.md`和`leakage-threat-model.md`，覆盖总纲步骤8—10全部边界。
- 新增`scripts/validate_protocol_freeze.py`并接入综合准备检查；5个冻结文件、必需术语、Git可跟踪性、密钥扫描和模板残留均通过。
- 将CUC-IGPE-v2台账从根目录未知更新为工作区外`LOCAL_PRESENT_REVIEW`；许可、数据集hash、canonical与可发布范围仍未通过。
- 外部宽模式搜索曾误显示原始评论行；未写入项目文件。已停止正文扫描并改为只读字段头、计数和代码证据。

### 步骤11—18：公开数据选择门（2026-07-14）
- **状态：** complete（G1 BLOCKED）
- 已开始以官方论文页、作者仓库、LICENSE和数据卡分层核验CSMV、iNews与NEmo+。
- CSMV已确认字段、特征入口、`video_file_id`、hashtag和comment-ID随机split；许可需按代码/annotations/外部媒体分层。
- iNews已确认公开版字段、VAD、9类离散情绪和post/annotator标识；媒体恢复/版权/T0截图泄漏仍是硬门。
- NEmo+已确认规模、众包标注和分布预测构念，许可与包内字段仍待核。
- 通过无凭证官方HTTP API固定CSMV commit和iNews revision；首次Web API直接URL被工具安全策略拒绝，已改用官方只读HTTP接口。
- `Invoke-WebRequest -Method Head`读取ACL附件首次触发空引用；改用`curl.exe -I`后确认附件2,080,204 bytes，没有重复失败。
- 仅下载CSMV标注/映射/URL清单、iNews public非persona CSV和NEmo+ ACL附件，总计约43 MB；没有下载视频、图片、特征、persona或付费资源。
- 新增`scripts/fetch_m1_public_assets.py`，固定URL/revision/预期大小并生成三份逐文件SHA-256 manifest；新增`scripts/audit_m1_public_assets.py`，只输出聚合计数与泄漏统计，不输出评论、URL或标识符。
- CSMV正式split实证107,267条评论、8,210个视频、`video_file_id`零缺失；train/dev/test存在大规模视频交叉，确认官方split不可复用。35个hashtag可支持held-out，无原生topic。
- 表格技能导入CSMV URL清单时，因上游theme中`95%`/`170%`等非法OpenXML值连续两次失败；按错误恢复规则停止重试。源文件hash已记录，URL行级覆盖保持`PENDING`。
- iNews public实证11,320行、2,736个post、VAD 1—7和九类离散情绪；公开包不含图片/媒体字段，且论文截图含reaction count。已裁定`NO_GO_PRIMARY_MEDIA_REPRO`。
- direct6映射草案显示iNews丢失37.95%行并使227个post完全失标；已在`LABEL_SPACE_MAPPING_DRAFT.md`显式登记，不强制合并类别。
- 已执行切换审计NEmo+：1,297个news item、38,910条T/I/TI人工反应；ACL包0图片、0许可文件，仅匿名本地图片路径，裁定`NO_GO_PRIMARY_LICENSE_MEDIA`。
- MVIndEmo自动标签生成过程已核实，论文所列仓库网页/API均404；固定为`SILVER_ONLY_SOURCE_UNAVAILABLE`，不阻塞G1。
- 新增`M1_PUBLIC_DATA_AUDIT.md`、`LABEL_SPACE_MAPPING_DRAFT.md`、`DATASET_SELECTION_DECISION.md`；更新数据来源台账、可行性矩阵与许可伦理矩阵。
- 当前门状态：CSMV视频分组结构级PASS；第二人工标注多模态主集未冻结，G1仍BLOCKED，G2未评估；未创建任务20、未训练模型。

### 步骤19—23：贡献级查新与协议冻结（2026-07-14）
- **状态：** complete（G1仍BLOCKED）
- 已读取总纲第17节步骤19—23、`research-question-v1.md`、`experiment-protocol-v1.md`和现有项目记录。
- 检索范围由用户选定的四条独立研究线限定；采用中等深度scoping review，覆盖经典与近三年前沿，优先英文同行评议/正式预印本及官方代码仓库。
- 使用免key公开学术源与官方论文/代码页；不使用付费数据库、付费LLM或受版权限制全文。
- 当前只做查新、名称核验、协议上限与baseline清单，不启动模型开发或训练。
- 四条检索已分别完成三层自动召回与核心前作人工核验；四个行内去重候选池合计500条、跨行去重后488条。宽检索噪声明确记录，不用自动排序作新颖性结论。
- 新增`LITERATURE_SEARCH_REPORT.md`、`CONTRIBUTION_PRIOR_ART_MATRIX.md`、`CARM_NAME_AUDIT.md`、`RESEARCH_PROTOCOL_FREEZE_AUDIT.md`和`BASELINE_CANDIDATES.md`。
- `CARM`已核到多个机器学习/检索/记忆同名，冻结为`NAME_BLOCKED`；总纲中的CARM-v1仅保留历史工作包代号意义。
- `research-question-v1.md`与`experiment-protocol-v1.md`通过一致性复核，主指标仍为JS，H1—H4与失败条件未改；查新只增加必须对比前作与表述红线。
- 新增冻结检索协议、四份原始召回JSON及`validate_literature_freeze.py`，并接入准备检查；协议门与本地验证均通过。
- 未下载数据/媒体/模型权重，未训练，未安装faiss，未调用API/付费LLM，未创建任务20。第二人工多模态主集仍未冻结，G1继续`BLOCKED`。

### 步骤24—33：M2数据工程与标签隔离（2026-07-14）
- **状态：** complete_with_blocker（本地项完成；G1仍BLOCKED）
- 已恢复并复核规划文件、工作记录政策、最新工作记录与Git状态。
- 已确认CSMV小型标注资产、固定revision及现有source manifest可用；现有source manifest尚缺逐文件样本数和字段清单。
- 已确认CUC外部只读根目录仍存在，含44组标签表、44组预测向量表和44组发布者视频列表；本阶段只生成派生canonical与审计台账，不改写源文件。
- 第二人工主集仍未冻结，因此步骤27只能形成版本化阻塞记录，不能伪造已完成标签映射或放行G1。
- 本轮不会补采媒体、启动训练、安装faiss或调用API/付费LLM。
- 新增canonical schema、逐字段数据字典、M2协议、银标协议、错误审查协议、近重复/同源事件审计和CUC canonical审计。
- 新增确定性构建器：校验原始source hash后，将107267条CSMV人工评论聚合为8210条视频分布；`group_by_video_v1`为5719/816/1675，`hashtag_heldout_v1`为5990/602/1618，35个hashtag连通分量跨split为0。
- CSMV输出不含评论正文；经验分布保存有效反应数、熵、归一化熵、有效类别数、最大类占比和逐类二项标准误。原生topic缺失，topic split保持`not_assigned/BLOCKED_NATIVE_TOPIC_ABSENT`。
- CUC生成2787条`SILVER` canonical：2779条有BV、8条缺BV、0重复BV、221标签冲突、883条有发布时间；其中1条发布时间为跨发布者目录全局匹配，已显式标记。
- 建立132个CUC源文件的匿名路径ID、样本数、字段、大小与SHA-256清单；许可继续`UNKNOWN_NOT_CLEARED_FOR_REDISTRIBUTION`。
- 物理建立`HUMAN_GOLD/SILVER/UNLABELED`入口及独立manifest；加载器拒绝层级混装和目标评论字段。银标教师与置信度未知，未伪造。
- 确定性抽取100条`PENDING_HUMAN`审查候选，仅用于数据缺陷；没有执行人工裁定或计算模型优越性。
- `validate_m2_data_engineering.py`全部通过；综合准备检查`blocking_checks=[]`、`m1_read_only_work_ready=true`、`formal_model_work_ready=false`。M2报告仍明确G1失败、G2未评估。
- 最终检查曾因M1验收器仍要求旧CSMV状态字面量而误报；已将断言同步到`CANONICAL_LABELS_READY_MEDIA_PENDING`。修复后M1/M2、工作记录、全脚本编译、综合准备检查和`git diff --check`均通过。

### 步骤34—39：自动化验收、数据文档与G1/G2交接（2026-07-14）
- **状态：** complete_with_blocker（本地包完成；G1/G2阻塞）
- 新增`scripts/run_m2_leakage_tests.py`，覆盖ID/source group、评论归属、目标评论、未来候选、索引、时间和fit范围；任一Critical失败输出`LEAKAGE_BLOCKED`并非零退出。
- 负面自测注入7类问题后命中全部预期检查；真实CSMV候选0个Critical失败，门状态为`PASS_WITH_LIMITATIONS`。
- 新增`scripts/build_m2_release.py`，只在泄漏门通过后写出`dataset-v1`、`split-v1`、`label-provenance-v1`和数据审计；候选状态固定为`LOCAL_CANDIDATE_G1_BLOCKED`，不是正式split。
- 完成Data Card、Datasheet、隐私说明、平台条款说明和可发布/不可发布边界；CUC继续本地银标、许可未知，评论/媒体/用户标识不发布。
- 新增`scripts/reproduce_m2_minimal.py`；首次`-I -S`重跑因相邻模块导入失败而保留失败证据，修复仅限本地`scripts/`路径后，两个隔离命令返回0、18个输出hash零漂移。
- 新增`scripts/validate_m2_release.py`并接入综合准备检查；本地步骤34—39包已通过，G1/G2字段保持false。
- 形成`G1_G2_EVIDENCE_MATRIX.md`与`HANDOFF_10.md`，等待/提交任务00审核；不创建任务20、不训练、不建正式索引。
- 已将交接路径、验证结果、G1/G2阻塞状态和第二主集决策请求发送至任务00源任务`019f5c27-10fa-7e13-857d-77505594f7fc`；发送工具返回同一任务ID，当前等待审核，不视为门已通过。

### 第二人工主集公开元数据只读审计（2026-07-14）
- **状态：** complete_with_blocker（授权内交付完成；第二主集仍未冻结）
- 按`AUTH-00-M1-SECOND-PRIMARY-READONLY-20260714`形成恰好3项短名单：LIRIS-ACCEDE、PMEmo、Emotion6；ArtEmis只记短名单外预筛。
- 仅深审LIRIS-ACCEDE，覆盖来源/revision/许可/大小/split/媒体/多人标注/T0/构念映射；没有访问下载链接或探测受限包。
- LIRIS-ACCEDE的视听输入、felt/induced VA和按电影Protocol A结构高度匹配，但获取必须签署EULA并邮件联系，且公开只发布最终VA秩而非离散人群分布，裁定`NO_GO_CURRENT_AUTHORIZATION_EULA_CONTACT_REQUIRED`。
- PMEmo裁定`NO_GO_LICENSE_SPLIT_AND_LABEL_DISTRIBUTION_UNKNOWN`；Emotion6裁定`NO_GO_MEDIA_LICENSE_ACCESS_AND_MODALITY`。
- 新增短名单、深审、00回交、只读manifest和专项validator，并将专项门接入综合准备检查；未下载数据/媒体/特征，未联系作者、调用API/付费服务或修改G门。
- G1=`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`、G2=`NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`、`formal_split=false`，继续禁止任务20/M3。

### 阶段14：G1/G2缺口修复与止损决策（2026-07-14）
- **状态：** in_progress
- 用户明确要求完善所有尚未通过项；该授权允许继续本地修复和公开候选研究，但不自动构成机构EULA签署、作者联系、付费资源或大数据下载授权。
- 00总控已完成GitHub同步：`main`与`origin/main`均为`26229c0`，开始本阶段时工作区干净。
- 已重新读取总纲、G1/G2矩阵、数据可行性与许可矩阵；确认核心硬阻塞仍是第二公开人工主集，不是校验脚本或状态字段。
- `planning-with-files-zh`会话恢复脚本因Windows GBK无法编码特殊符号退出1；恢复摘要已显示15条未同步消息，实际Git与规划文件已覆盖这些事实。按失败协议不重复原命令。
- 已扩展只读候选核验：VCE构念/多人分布匹配，但媒体依赖美国Fair Use且标注无音频；LAI-GAI v05公开847张AI生成图像和N=2470真人诱发评分，论文明确OSF含raw data，但仅单图且逐资产许可仍待核。
- 已修复CSMV URL清单读取：新增Strict OOXML解析，不加载损坏theme；8210行ID对正式视频集合100%覆盖，专项validator通过。
- 同一审计发现2644行表ID与URL路径ID不一致、200行URL重复；因此关闭的是“不可读”问题，不是媒体可复现问题。CSMV媒体状态升级为更精确的`MEDIA_MAPPING_BLOCKED`。
- 已生成`G1_G2_REMEDIATION_REPORT_20260714.md`，给出三条止损路径。推荐由00批准LAI-GAI作为图像跨域第二人工主集；该选择保持人工分布与JS指标，但需要正式修改第二主集模态范围。
- 当前等待用户/00选择；未下载新数据/媒体/特征，未调用API/付费服务，未联系作者，未改变G1/G2、`formal_split=false`或任务20禁令。
- 回归完成：M1专项、18条工作记录、综合准备检查、全脚本编译和Git空白检查均通过；`blocking_checks=[]`表示本地验收器无故障，不等于G1/G2通过。正式模型环境仍按预期`BLOCKED_M1`。

### 阶段15：LAI-GAI范围变更与下载前准入审计（2026-07-14）
- **状态：** in_progress（00范围变更与只读审计授权已完成；等待任务10执行）
- 用户明确回复“同意路径1”，授权把LAI-GAI推进为图像跨域第二人工主集方向；该授权不自动等于G1/G2通过，也不自动授权下载图像/raw data。
- 已向00源任务`019f5c27-10fa-7e13-857d-77505594f7fc`发送范围变更请求：保留构念、HUMAN_GOLD、T0和JS，禁止生成prompt作为真值；只申请核OSF三个组件的公开元数据。
- 00已将总纲升级为v1.6并登记`SC-20260714-01`：第二集降级为跨域图像/缺失模态验证角色，CSMV继续承担完整视频多模态与H1/H2主证据；生成prompt只作provenance。
- 00已签发`AUTH-00-LAI-GAI-OSF-META-RO-20260714`，任务10只可核OSF `V8DKM/8P572/K8XVH`公开网页展示的license/revision/file tree/size/hash/gating；禁止下载、API、登录、训练和正式split。
- 尝试读取总纲要求00维护的`DECISION_LOG.md`与`RISK_REGISTER.md`时发现文件不存在；任务10不越权伪建总控权威记录，改为任务10范围变更请求交00接管。
- 当前继续保持G1/G2 blocked、`formal_split=false`、任务20禁止；范围批准和只读授权均不等于资产准入或阶段门通过。
- 任务10已完成公开网页只读审计：V8DKM无可用页面行、8P572安全打开错误、K8XVH HTTP 403；全部关键资产字段保持`UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE`，裁定`NO_GO_PENDING_ASSET_METADATA`。
- 00以`REVIEW-00-LAI-GAI-META-20260714`接受该合规No-Go交付。当前不扩权；建议的元数据专用OSF API方案须用户明确批准，任务10在此之前停止。
- 用户随后明确回复“批准”；00签发`AUTH-00-LAI-GAI-OSF-API-META-RO-20260714`，仅允许三个节点、`api.osf.io`、匿名GET、100请求/5 MiB和元数据关系遍历，不跟随资产下载链接。
### LAI-GAI路径1公开网页元数据审计（2026-07-14）

- **状态：** complete_with_blocker
- 已按`SC-20260714-01`和`AUTH-00-LAI-GAI-OSF-META-RO-20260714`核验OSF `V8DKM`、`8P572`、`K8XVH`公开网页。
- 合规读取未获得节点级asset license、revision、file tree、size、hash、gating或公开字段说明；全部保持`UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE`。
- 新增`M1_LAI_GAI_OSF_METADATA_AUDIT_20260714.md`、机器清单和专项验证脚本；裁定`NO_GO_PENDING_ASSET_METADATA`。
- 未下载、预览或流式读取任何数据资产，未使用API/登录/Cookie，未构建标签映射或split。
- 专项验证、20条工作记录校验、综合准备检查、脚本编译与Git差异检查均exit 0；综合门仍诚实返回`formal_model_work_ready=false`。
- G1/G2与`formal_split=false`保持不变；下一步须由00另行批准明确的最小元数据取得方案。
### LAI-GAI限额OSF元数据API审计启动（2026-07-14）

- **状态：** in_progress
- 用户已明确批准，00签发`AUTH-00-LAI-GAI-OSF-API-META-RO-20260714`。
- 已冻结匿名串行GET、`api.osf.io`、三个节点、≤100请求、≤5 MiB、请求间隔≥1秒及只跟随返回的元数据关系边界。
- 将先建立fail-closed采集器和raw Git忽略预检，再执行API；不访问任何asset content/download/render链接。
- 首次采集在网络阶段结束后的manifest序列化处因代码误用小写`false`触发`NameError`；已停止，不重复网络请求，将从既有Git忽略raw响应离线重建。
- 已从既有raw响应离线重建manifest：26次GET、382,394B、全部HTTP 200；没有重复网络请求。
- `V8DKM`为9文件/22,108,737B/9 checksum，`8P572`为137文件/1,122,196,956B/137 checksum；三节点均public且CC BY 4.0。
- `K8XVH`授权文件列表返回空`data`数组，图像文件树/size/checksum未闭合，裁定`NO_GO_PENDING_IMAGE_COMPONENT_FILE_TREE`并停止访问。
- 新增API审计报告和边界validator；待运行专项及综合验收后回交00。
- 专项validator首次运行exit 1：除速率外所有边界通过；第2→3次请求UTC间隔0.996519秒，低于1秒硬下限。已保留失败，不采用容差或重跑网络。
- 最终综合准备检查按预期exit 1，唯一阻塞为LAI-GAI API边界validator；`m1_read_only_work_ready=false`、`formal_model_work_ready=false`。
- 23条工作记录校验、全脚本编译与Git差异检查通过；当前等待00复审，API访问保持停止。
- 00以`REVIEW-00-LAI-GAI-OSF-API-20260714`完成复审：保留26个响应及节点矩阵为`OBSERVED_WITH_PROTOCOL_DEVIATION`，但0.996519秒违反硬门且`K8XVH`文件树为空，不授予G门信用。
- API授权已关闭为`CLOSED_NONCONFORMING_NO_RERUN_AUTHORIZED`；不批准重跑或继续探索，专项validator与综合准备门的失败必须保留。
- 最终review closure机器检查通过；25条工作记录连续有效，综合准备唯一阻塞仍为`lai_gai_osf_api_metadata`。
- 已向00源任务回交请求/响应证据、三节点矩阵、速率硬门失败和No-Go裁定；发送工具返回同一任务ID。

### 阶段17：第二人工跨域图像主集恢复（2026-07-14）

- **状态：** in_progress
- 用户要求继续解决第二主集；本阶段不把“无论如何”解释为可绕过许可、标签真实性或00退出门。
- LAI-GAI授权已关闭且禁止重跑，保持原No-Go证据不动；后续改审新的公开人工图像候选。
- 优先评估现有证据中媒体权利链较清楚、每图多人评分密度高的OASIS；先做无需登录、无需资产下载的官方来源、许可、版本、文件树、标签粒度和split威胁审计。
- 未授权登录、付费服务、作者联系、大数据下载、模型训练、正式split或任务20。

### 阶段17：第二主集收口授权与候选重开（2026-07-14）

- 用户明确要求完成第二主集，00新建`AUTH-00-SECOND-PRIMARY-RESOLUTION-20260714`，允许从公开、免费、无需登录的官方入口获取完成准入所需的元数据和数据资产。
- 旧LAI-GAI审计失败和关闭状态保持历史有效；本轮不继承旧授权，也不重跑旧26请求，只补核心图像定位和图像—评分关系。
- 首轮官方检索确认LAI-GAI站点另有`Dataset files`、Data Card与样例入口；同时确认情感OASIS为900张开放图像、N=822 VA人工规范候选，需继续核现行资产与许可链。
- 已更新阶段17执行顺序：LAI-GAI抢救→OASIS替代→其他候选；任何候选仍须通过来源、许可、revision、文件树、HUMAN_GOLD、T0和泄漏硬门。
- 官网已定位公开直链`/media/all_images.zip`，且图片详情页提供文件名、目标情绪、prompt和评分样本量；旧K8XVH空列表不再是唯一资产定位路径。
- 官网ZIP的HEAD请求超时但下载页正常；已停止重复HEAD。既有OSF manifest显示评分节点含可用的逐研究CSV、最终逐图汇总、README、prompt与目标情感表，下一步从本地raw元数据恢复公开下载定位，只取最小必要文件。
- 已从既有Git忽略raw元数据离线定位12个最小评分文件及其OSF file ID/大小/SHA-256，预计约27.18 MB；将跳过`.RData`和其余重复中间产物。

### 阶段17完成：LAI-GAI第二主集冻结候选（2026-07-14）

- **状态：** ready_for_00_freeze_review
- 新独立授权下未重跑旧26个OSF请求；从既有raw元数据取得并核验12项最小评分资产，从官网图片浏览器闭合并取得847张公开图像。
- 847张图均通过解码、size、SHA-256与dHash固定；评分侧按`consent=YES/useData=Yes/rating_cat=0`保留63682个逐图人工反应，每图58—96，图像—参与者重复0。
- 12个人工1—7诱发情绪强度按预注册规则减去量表下界1后归一化为连续分布；保留各维N、SD、SE与直方图。prompt、目标类别和生成模型字段不作真值或输入。
- source item、文化/性别/年龄变体、同prompt、精确与dHash近重复并成379个group；确定性split为594/127/126，三个split均覆盖12类，group/精确/近重复跨split均0。
- 新增抓取、构建、专项验证脚本及raw/canonical/split/label provenance manifest；专项validator输出`LAI_GAI_SECOND_PRIMARY_READY`且全部检查通过。
- 原始图像、逐人响应及canonical均在Git忽略目录；tracked文件不含参与者ID、Prolific ID、人口统计、设备、完成日期或prompt正文。
- 已同步Data Card、Datasheet、隐私、条款、发布边界、标签映射、数据字典、数据源台账、G1/G2矩阵和交接文件。全局G1/G2、`formal_split`和任务20仍等待00书面复审，不由任务10自行放行。
- 已完成12个最小评分文件下载，官方大小/SHA-256全部匹配，合计27,838,544 bytes；raw目录经`git check-ignore`确认不跟踪。
- 首次CSV/XLSX结构画像在JSON输出阶段因Windows GBK无法编码Unicode列名而exit 1；未修改数据，后续固定UTF-8输出后重跑。
- UTF-8重跑成功：六项研究共94,292条逐图人工评分，原始表结构一致并含12维离散情感；同时发现参与者/Prolific标识和人口学字段，确认raw必须私有隔离，canonical只保留图像级聚合与非识别性provenance。
- 汇总表944/943行大于官网847图，下一步必须以实际图像ZIP和`is_ai/used_in_study`交集确定最终样本，不能直接全收。
- 保守过滤`is_AI=1 && useData=Yes`后已有802张AI图、60,562条人工评分、每图58–96人；数据规模门基本关闭。`Sim.`与空`useData`暂不纳入，待预处理notebook核语义。
- README 1/1页文本读取完成，确认六项研究CSV是官方清洗输出，但未解释`useData`；系统无Poppler，视觉通道未审且不影响本次字段血缘判断。
- 系统PATH未提供Poppler的`pdfinfo/pdftotext`，README首轮PDF读取未启动；将改用工作区`pypdf`做文本层读取，视觉版式不作为本次数据字段判断依据。
### 阶段17：LAI-GAI 预处理代码核验续（2026-07-14）

- 已取得并校验官方总预处理 Notebook；hash 与已冻结公开 OSF 文件元数据一致。
- 已确认逐图人工评分汇总、跨研究参与者编号隔离、AI 文件识别及 prompt 仅作来源字段的实现逻辑。
- `useData` 的同意/排除规则仍需精确核验；在规则闭合前继续采用最保守 `Yes` 筛选，不把 `Sim.` 或空值自动解释为同意。
### 阶段17：官方清洗输出与图片取得状态（2026-07-14）

- 六个分研究预处理 Notebook 与六个 `S*_data_out.csv` 已全部按公开元数据 size/SHA-256 闭合。
- 正式第二主集候选已收敛为 802 张、58,432 条清洗后 HUMAN_GOLD 评分；不再把 847 张资产总数误写为全部有标签。
- 单包 ZIP 官方连接因约 11 KiB/s 吞吐和中途失败未完成；局部文件保留供续传证据，但不参与处理。下一步从同一官网的逐图公开 URL 取得资产。
- 逐图官方路径已完成847张资产取得，合计86,947,800 bytes；四方文件名集合一致、解码零失败。阶段样本数已按最终汇总更正为847张，每图54--93名合格评分者。

### 阶段17正式收口：第二主集冻结与G1通过（2026-07-15）

- 00签署`REVIEW-00-LAI-GAI-FREEZE-20260715`：LAI-GAI=`FROZEN_00_APPROVED`，G1=`PASS`。
- 唯一权威版本为`LAI-GAI@v05-2026-03-11`：847图、63,682条合规人工响应、379组、split 594/127/126；266组并行试算及其canonical已删除。
- 重建脚本固定跨平台LF并保持响应行数与逐维N分栏；重建exit 0，canonical SHA-256=`ad58c268e34adf02bd8e639338069d34576e1d9602f819a2cc6fa89be6836818`。
- LAI-GAI专项、M2数据工程、M2 release build/validate、工作记录、脚本编译与Git空白检查均通过；M2状态为`LOCAL_CANDIDATE_G1_PASS_G2_BLOCKED`。
- G2=`BLOCKED_CSMV_MEDIA_MAPPING_AND_GLOBAL_SEMANTIC_AUDITS`，全局`formal_split=false`；CSMV 2,644行ID—路径错配及200行URL重复关闭前，不创建任务20、不训练、不建正式索引。
- 旧`lai_gai_osf_api_metadata`专项仍按事实exit 1；综合准备检查将完整失败对象标为`HISTORICAL_NONCONFORMING_NO_GATE_CREDIT`并由新冻结复审取代其当前门作用，因此`blocking_checks=[]`、`m1_read_only_work_ready=true`。正式模型环境仍因faiss/G2边界保持未就绪。

### 阶段18：CSMV媒体lineage与同源split本地收口（2026-07-15）

- 撤销旧的“2,644行ID—URL路径错配”判断：两列分别是内部ID与平台ID，不存在相等约束；官方固定工作簿hash保持不变。
- 识别8,008个源视频族、202个重复族/404条；修复前100个video split和115个hashtag split同源交叉均已量化。
- 构建器现按源族hash设置`source_group_id`和`duplicate_source_id`，所有split先满足同源约束；新计数为video 5698/837/1675、hashtag 7211/327/672。
- `validate_csmv_media_lineage.py`普通与`-I -S`隔离运行均exit 0；全局泄漏live门Critical=0，负面selftest按预期输出`LEAKAGE_BLOCKED`并exit 0。
- M1审计、M2数据工程、release构建/验证均exit 0；dataset状态为`LOCAL_CANDIDATE_G1_PASS_G2_REVIEW_PENDING`，G2等待00书面复审，全局`formal_split=false`。
- 历史CUC外部只读源目录本轮未在有限路径找到；一次D盘全盘检索20秒超时，未重跑全量复现器。CSMV专项已从固定raw工作簿在stdlib隔离环境闭合，不以此掩盖全量复现源目录缺口。

### 阶段18复审：00接受CSMV lineage但不放行G2（2026-07-15）

- 00独立复跑CSMV专项普通/`-I -S`、全局泄漏live门与负面selftest，全部符合任务10报告；正式接受2644行为命名空间误判以及8008源族/202重复族的split修复。
- 00现场对`reproducibility-v1.after_sha256`与当前18项文件重算，发现9项不一致；旧release validator未现场重算hash，故旧复现PASS不能覆盖本次新split。
- CSMV标签与URL元数据lineage已经闭合，但正式模型输入的视频/特征资产许可、revision、文件树、体量与hash仍UNKNOWN，不能构造合法固定的正式多模态测试输入。
- 签署`REVIEW-00-CSMV-LINEAGE-G2-20260715`：G1继续PASS，G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_REPRODUCIBILITY_STALE`，全局`formal_split=false`，任务20禁止。
- 签发`AUTH-00-CSMV-FEATURE-ASSET-PREFLIGHT-RO-20260715`：只读预审官方特征页面元数据，禁止登录/API/下载/访问TikTok；同时授权本地公共benchmark核心隔离复现与现场hash门修复。

### 阶段19：CSMV特征预审与公共核心复现（2026-07-15）

- **状态：** reviewed_repro_closed_asset_admissibility_blocked
- [x] 固定README commit/hash与官方Drive folder locator；匿名页面GET为HTTP 200，未使用登录、Cookie、API或第三方镜像。
- [x] 公开首屏没有I3D/VideoMAE文件列表、大小、更新时间、checksum或许可；三族矩阵及8210覆盖全部按证据记`UNKNOWN`，未选择下载族。
- [x] 新增特征预审manifest、报告与validator；专项exit 0代表“诚实No-Go合同有效”，不代表资产可用。
- [x] `--public-core`只重建CSMV HUMAN_GOLD主线并核验冻结CUC辅助字节；历史CUC外部根不再阻塞公开benchmark复现。
- [x] Python `-I -S`下两条命令均exit 0；19项before/after SHA-256一致，`mismatches=[]`，凭证/代理环境未传入子进程。
- [x] release validator对manifest记录逐项现场重算，当前19项漂移0；旧9项漂移已实质关闭。
- [x] 00独立复跑19项隔离复现、release现场hash和泄漏正负门；确认漂移0并关闭复现陈旧子阻塞。
- [x] 00签署`REVIEW-00-CSMV-FEATURE-PREFLIGHT-G2-20260715`：G2收敛为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`。
- [x] 00签发`AUTH-00-CSMV-ONE-FEATURE-FAMILY-METADATA-COORDINATION-20260715`：允许一次请求和一次跟进，可收≤5MiB纯元数据，不下载`.npy`或媒体。
- [ ] 取得权利方许可/revision/manifest/schema/8210覆盖并再次申请资产准入复审。
- **外部缺口：** 一个选定特征族的资产级许可、revision、相对文件名/bytes/SHA-256 manifest、schema和8210覆盖；后续效率政策已允许官方或可信镜像的隔离预取，但正式使用仍禁止。
## 2026-07-15 — CSMV I3D 元数据协调发送受阻

- 00 已关闭 `REPRODUCIBILITY_STALE`：当前公共核心 19 项隔离重放与现场 hash 均为零漂移。
- 00 已将 G2 收敛为 `BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`，并授权通过一个官方渠道请求 I3D 纯元数据。
- 已定位官方 GitHub Issues、检索重复主题并尝试创建请求；GitHub 集成返回 403，未产生 Issue 或任何外部写入。
- 已落盘 `CSMV_I3D_METADATA_COORDINATION_20260715.md`；下一步需用户手工提交，或为连接器补足对该公开仓库创建 Issue 的权限。

## 2026-07-15 — CSMV I3D 官方元数据请求已成功发出

- 用户已在官方 `IEIT-AGI/MSA-CRVI` 仓库创建公开 Issue #5；匿名现场核验为 Open，创建日期为2026-07-15。
- 正文满足单一渠道协调授权的六类字段要求，并明确不在独立许可/fixity复审前下载特征。
- 当前从“发送权限阻塞”转为“等待权利方实质回复”；2026-07-22前不得跟进，之后至多在同一Issue跟进一次。
- 00签署`REVIEW-00-CSMV-OFFICIAL-ISSUE-5-SENT-20260715`：正式请求额度已使用；公开正文覆盖准入字段但未逐字点名I3D，若执行唯一一次跟进须在同一Issue明确I3D优先范围。
- G2仍为 `BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`，未创建任务20。

## 2026-07-15 — CSMV官方GitHub仓库直接克隆验证

- HTTPS浅克隆约20秒成功，HEAD为固定上游`99d142...`，pack约4.97 MiB；无需用户代下载。
- 提交共10文件、canonical blob 14,436,790 bytes；与既有固定快照逐文件一致。
- `CSMV/`只有标注、split、映射和URL表；`.npy`与Git LFS pointer均为0，I3D/VideoMAE特征不在GitHub仓库内。
- 新增`CSMV_GITHUB_CLONE_AUDIT_20260715.md`；G2资产阻塞和下载边界不变。
- 00复审接受该次尝试为`ACCEPTED_NO_EXTERNAL_WRITE_AUTHORIZATION_UNCONSUMED`：403不是维护者拒绝，一次正式请求额度仍在；已落盘可直接手工提交的`CSMV_I3D_GITHUB_ISSUE_REQUEST_20260715.md`，且只允许同一渠道二选一恢复。

## 2026-07-15 — 效率优先镜像与扩展取得政策

- 用户明确允许切换第三方镜像并扩大项目内部下载范围；总纲升级为v1.11并签署`POLICY-00-EFFICIENCY-FIRST-MIRROR-AND-EXPANDED-ACQUISITION-20260715`。
- 网络取得改为本机代理优先、必要时直连或可信镜像；公开大包、媒体和特征可先进入Git忽略隔离区，不再逐包等待内部下载授权。
- 法律许可不能由项目自行扩大；未知许可资产只标`QUARANTINE_ACQUIRED`，不得正式训练、建索引、发布或获得G门信用。
- 当前CSMV可在等待Issue #5回复期间并行预取候选特征，但G2、`formal_split=false`和任务20禁令不变。

## 2026-07-15 — CSMV I3D用户本地包隔离接入

- 用户提供本机I3D特征包；源目录保持不变，项目通过Git忽略的`data/raw/csmv/features/visual_feature/I3D` directory junction只读接入，没有重复复制2.56 GiB数据，tracked材料不记录绝对源路径。
- 全量核验9,942个`.npy`：总计2,752,998,144 bytes，全部为`float32[T,1024]`，`T=6—1719`，schema错误0。
- 官方`video_to_comment.json`要求的8,210个`video_file_id`全部命中，缺失0；包内另有1,732个非当前标签集文件。
- 8,210个必需文件的相对路径、bytes、shape、dtype和SHA-256已写入`csmv-i3d-quarantine-v1.manifest.json`；全包内容树SHA-256=`35be2d18e1d2413ba3765034cdb454baa5e3496d49c540c9be00e81bbc2c1942`。
- 新只读加载器支持官方`video_file_id`与canonical `item_id`，采用mmap且禁止pickle；当前仅`QUARANTINE_ACQUIRED`，未训练、未建索引。
- 本地文件树、体量、schema、fixity和覆盖已闭合；资产级许可、稳定官方revision和权利方attestation仍待Issue #5与00复审，G2暂不改变。

## 2026-07-16 — 00音频模态与协议边界复审

- 00联读任务10复审请求、交接、G门矩阵、Data Card、Datasheet，并复核T-AFFC General CFP、CSMV固定README和NeurIPS 2024正式入口。
- 签署`REVIEW-00-AUDIO-MODALITY-PROTOCOL-20260716`：音频=`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`，不是G2/任务20独立前置条件，移出后续取得关键路径。
- 总纲升为v1.12；E1改为实际单输入与`ALL_AVAILABLE_INPUTS`，E5/H3只在同一样本至少两个实际T0输入模态时有资格运行。
- CSMV音频分支=`NOT_APPLICABLE_AUDIO_UNAVAILABLE_BY_DATASET_DESIGN`；单模态协议的逐模态增量=`NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`；全项目无合格协议时H3=`NOT_APPLICABLE_NO_ELIGIBLE_MULTIMODAL_PROTOCOL`。
- G1仍`PASS`，G2仍`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`，全局`formal_split=false`，未创建任务20、未训练、未建正式索引。

## 2026-07-16 — I3D序列协议与论文边界冻结

- 已建立`CSMV_I3D_SEQUENCE_PROTOCOL_V1.md`、JSON配置、机器manifest、确定性实现/构建器/validator和8项单元测试。
- 主协议完整保留序列并使用动态padding/mask；主敏感性确定性均匀180步；前180固定为补充。
- 初始测试因模块缺失exit 1并保留；实现后8/8通过，专项validator=`PASS_PREREGISTRATION_ONLY_G2_UNCHANGED`。
- 已更新实验协议v2、Data Card、Datasheet、数据字典、M2协议、发布边界、claim矩阵、G门证据和HANDOFF。
- 维护者协调=`DEFERRED_PENDING_MAINTAINER_REPLY`，本轮跳过且不冒充解决。下一步重建release、执行全套验证、安全审计与Git阶段检查点。
- M1—M2内容检查点`f885a59`已成功推送到`origin/main`；最终回交与真实同步记录由后续收尾commit固定。

## 2026-07-16 — 00接受I3D序列协议与M1—M2检查点

- 00独立复核协议manifest及6个证据hash、8项单测、专项validator、泄漏正负门、19项隔离重放、M2 release与综合准备，结果均与任务10回交一致。
- 签署`REVIEW-00-CSMV-I3D-SEQUENCE-PROTOCOL-20260716`，正式关闭`I3D_SEQUENCE_PROCESSING_PROTOCOL_UNFROZEN`子缺口。
- 主协议、均匀180主敏感性、前180补充和论文主张边界已冻结；不得按test结果变更。
- 维护者证据继续延期。G1=`PASS`；G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；`formal_split=false`；任务20未创建。

## 2026-07-16 — 启动IJCV专刊适配与双论文路线评估

- 用户提供三张专刊征稿截图并授权：若有希望，详细设计兼顾T-AFFC与IJCV的研究微调方案并写入总纲。
- 已启用期刊匹配、研究方案与文件化规划流程；当前只完成截图结构化观察，尚未把二次转述当作官方事实。
- 下一步以Springer/IJCV官方页核验范围、截止日期和重复投稿规则，再决定是否升级总纲。

## 2026-07-16 — IJCV—T-AFFC条件双论文路线已写入总纲

- 官方核验确认IJCV专刊范围强匹配主观视觉情绪分布、观察者差异、不确定性和跨域泛化，固定截稿为2026-12-15；同稿不得同时在其他地方审议。
- 近邻审计确认PC Loss、SAMNet和MFRN已覆盖情绪分布结构、主观分支/affective memory及特征精炼；当前冻结I3D+CARM不能原样满足IJCV视觉方法门。
- 总纲升为v1.14并裁定`CONDITIONAL_GO_TWO_DISTINCT_PAPERS`：IJCV独立研究响应分布几何驱动视觉表征；T-AFFC保留评论teacher、反应memory与可靠性路由。
- 新建`IJCV_TAFFC_DUAL_TRACK_FEASIBILITY_AND_PLAN_20260716.md`，冻结J0/J1/J2、JH1—JH3、J0—J9、公平基线、双线日历、两稿共享/隔离和十项IJCV Go标准。
- IJCV不等待CSMV维护者回复；LAI-GAI之外须在2026-08-12前再冻结至少一个像素级人工分布集。CSMV仅在G2通过后作可选视频外验，任务20禁令不变。
- 总纲条件增加任务25与65，但本轮不创建；只有J0/J2分别通过后才创建。下一步完成工作日志、机器检查、Git提交与同步。
- 内容commit `d817357`已推送到`origin/main`；首次直连失败后按既有代理政策重试成功，远端与本地内容tip一致。同步不改变任何科学门。

## 2026-07-16 — IJCV方向迁出，当前项目恢复T-AFFC单路线

- 独立项目`D:\MMSA-CH-SIMS - IJCV方向`已保有未删减总纲v1.14、项目上下文交接及独立启动任务，固定在`codex/ijcv-j0@c64c954`。
- 当前项目总纲升级为v1.15，唯一目标恢复为2027-05-12前完成T-AFFC CARM群体情绪预测论文及证据链。
- J0—J2、JH1—JH3、任务25/65、IJCV日历和投稿门已从当前项目活动总纲与任务树中移除；历史双路线方案只读归档。
- 任务10交接、代理规范、决策日志、风险台账和claim边界已同步为T-AFFC-only，避免后续任务误读双路线。
- 科学门没有借迁出而放宽：G1=`PASS`；G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；`formal_split=false`；任务20仍未创建。

## 2026-07-17 — G2拆分并放行任务20

- 用户明确要求将总纲中的G2拆为协议/数据门与资产风险状态，并放行任务20；该指令登记为`SC-20260717-01`。
- 非资产复审已证明没有第二个数据、协议、泄漏、标签隔离或复现阻塞，因此`G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`。
- I3D资产级许可、稳定官方revision及权利方包身份/fixity仍未获确认，诚实登记为`DEFERRED_ACCEPTED_RISK`，不改写为PASS或维护者已确认。
- 总门更新为`PASS_WITH_ACCEPTED_ASSET_RISK`，`formal_split=true`，任务20获内部研究授权；I3D与受限资产不得再分发，论文必须披露风险。
- 若权利方否认使用、固定资产hash/覆盖漂移或任务20绕开冻结协议，相关运行立即停止并失去正式证据资格。
- 当前正在重建机器manifest、M2 release和综合门；验证并绑定Git提交后创建任务20。

## 2026-07-17 — 任务20已正式创建

- G2风险接受状态合同已在commit `f869732`固定并推送至`origin/main`。
- 已创建Codex任务`20-M3 基线与统一评测`，任务ID=`019f6e2e-f781-7270-bb45-af8272ff5a5c`，绑定总纲v1.16与上述提交。
- 任务20已收到环境锁定、统一配置/run/prediction manifest、加载器、指标与最小基线的首批工作要求；当前faiss缺失由任务20先行解决。
- 维护者证明不再作为启动等待项；I3D风险披露、禁止再分发、hash/覆盖漂移止损继续有效。

## 2026-07-17 — 旧总控上下文压缩与新总控迁移准备

- 用户因旧总控对话过长，要求创建新项目承担00总控责任并完整交接。
- 任务20第一批已由其自身提交为`5522619`并推送，迁移前主分支恢复clean；正式环境仍因faiss缺失为`BLOCKED_M1`。
- 新建`TOTAL_CONTROL_HANDOFF_20260717.md`，压缩保存用户纠偏、总纲、研究边界、数据、门状态、任务树、线程、风险、网络政策和下一步。
- 建立`.light/passport.yaml`、项目卡、决策/版本/术语台账以及S00→S01交接链；底层passport验证为WARN（历史G门未附passport内部hash/timestamp），S01交接合同PASS。
- `light-memory-pm`封装器因本机技能布局缺`_shared/passport`导入失败，未伪报完整pm audit通过；改用底层`passport.py`和独立handoff validator。
- 交接包已在commit `e6c48c6`推送；已创建隔离worktree任务`019f6e64-0635-7ac0-a70a-65445b0fc1d1`并命名为`00-T-AFFC 新总控`，由其接替00责任。

## 2026-07-24 — Video2Reaction直接前作中修

- **状态：** completed
- 刷新共享主仓库为`main=origin/main=51c9235`，tracked clean，仅Task20自有`tmp/`未跟踪。
- Task20实时状态：4090冻结环境与完整断点恢复已验证，训练安全暂停在Epoch 0 step 12；探索身份永久`NON_T0/INELIGIBLE`，G1—G3不变。
- 在线核验确认Video2Reaction arXiv与DataMFM workshop展示；workshop归档状态与ECCV正式论文集状态仍需按分层证据措辞。
- 深读外部Word总纲，确认其为v1.14双路线历史快照，不能覆盖仓库v1.18 SSOT。
- 已冻结总纲v1.19、claim blacklist、closest-prior矩阵、实验增量、三类拒稿预演和外部Word单向回填合同；Task20文档所有权暂停保持到本批提交。
- 项目专用定位校验、文献冻结专项门、综合准备检查、passport与handoff合同均通过；跨材料一致性仅声明项目专用文本门通过，不冒充缺依赖的完整语义一致性审计。
- G1=`PASS`、G2=`PASS_WITH_ACCEPTED_ASSET_RISK`、G3=`PASS_WITH_LIMITATIONS`均未改变；Task30仍未创建。
- SSOT内容提交`63be49c`已推送`origin/main`，并已通知Task20刷新v1.19、解除文档暂停及保持新增任务30—50实验义务不在Task20并发实现。
