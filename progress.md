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
