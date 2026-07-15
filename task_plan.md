# 任务计划：Codex任务树执行规格

## 目标
基于 `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` 当前v1.12，为00—60七个Codex任务形成可直接执行、可验收、可交接的详细工作规格。

## 当前阶段
阶段18的CSMV命名空间纠正与同源split已获00接受，公共核心19项复现零漂移，G1=`PASS`。音频已裁定为结构性不可得并移出G2/取得关键路径；当前G2只剩一个CSMV视觉特征族的资产许可、稳定revision与权利方包身份/fixity准入。G2书面通过前不进入任务20。

### 00专项：音频模态与实际可得输入协议复审（2026-07-16）
- [x] 独立复核T-AFFC General CFP、CSMV固定README、NeurIPS 2024正式入口及总纲G2条款
- [x] 签署`REVIEW-00-AUDIO-MODALITY-PROTOCOL-20260716`
- [x] 冻结音频=`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`并移出G2/取得关键路径
- [x] 将E1/E5/H3改为仅对实际T0输入生效，建立三个机器可读`NOT_APPLICABLE`状态
- [x] 同步总纲v1.12、实验协议v2、G门、交接、Data Card、Datasheet和决策日志
- [ ] 继续等待/闭合I3D资产许可、稳定revision与包身份/fixity；未放行G2或任务20
- **状态：** audio_boundary_closed_g2_visual_asset_blocked

## 各阶段

### 阶段1：总纲与现状提取
- [x] 确认唯一总纲及版本
- [x] 确认任务树编号与当前已创建任务
- [x] 提取每个月份、假设、实验矩阵、退出门和交付物
- **状态：** complete

### 阶段2：任务边界与依赖设计
- [x] 将M1—M10映射到00—60七个任务
- [x] 定义每个任务的输入、输出、步骤、验收水平和禁止事项
- [x] 定义任务间交接契约与并行边界
- **状态：** complete

### 阶段3：执行规格成文
- [x] 创建 `CODEX_TASK_TREE_EXECUTION_SPEC.md`
- [x] 覆盖00、10、20、30、40、50、60全部任务
- [x] 明确每个阶段的最低水平、T-AFFC目标水平和止损条件
- **状态：** complete

### 阶段4：一致性验证
- [x] 对照总纲检查月份、H/E编号和G门无遗漏
- [x] 检查与T0政策、数据台账及当前任务结构一致
- [x] 检查无越权下载、付费调用或未来泄漏建议
- **状态：** complete

### 阶段5：交付
- [x] 更新 findings.md 和 progress.md
- [x] 向用户交付文件并概述任务数量和当前动作
- **状态：** complete

### 阶段6：规格并入总纲
- [x] 将详细任务规格内嵌为总纲第17节
- [x] 总纲版本由v1.4升级为v1.5
- [x] 更新项目内上位总纲版本引用和独立规格副本定位
- [x] 校验总纲章节、G/H/E覆盖、任务步骤和模板残留
- [x] 通知已创建的10任务改用v1.5
- **状态：** complete

### 阶段7：开工准备包审计与补齐
- [x] 按总纲八类准备项建立“已完成/部分完成/缺失”证据表
- [x] 跳过已达标项，仅补齐目录与版本、环境、数据存储、实验纪律、安全合规、时间资源、文献写作缺口
- [x] 执行最小导入、密钥/大文件/Git忽略、配置重跑能力等验收
- [x] 形成开工准备验收报告，并把不可代替用户完成的外部动作明确隔离
- [x] 更新总纲/项目记忆中的实际准备状态，通知任务10读取交付物
- **状态：** complete

### 阶段8：M1预下载许可与可用性审计
- [x] 读取准备验收交接文件并复跑准备门
- [x] 核验CSMV官方来源、分层许可、文件树、标签字段、固定版本与分组划分条件
- [x] 核验iNews官方来源、许可、媒体输入、多人标注、VAD/离散标签与映射损失
- [x] 执行iNews No-Go，并以同一标准审计NEmo+；冻结MVIndEmo银标边界
- [x] 仅下载小型审计资产，生成URL/版本/大小/SHA-256 manifest并验证
- [x] 更新数据来源台账、可行性矩阵、许可伦理矩阵、选择决定和审计发现
- **状态：** complete（G1 BLOCKED；不进入任务20）

### 阶段9：现有资产、构念与泄漏威胁冻结（步骤6—10）
- [x] 建立代码—数据—结果lineage并定位2787/2815、221冲突、旧随机split和目标评论泄漏证据
- [x] 将旧实验按四级证据用途分类
- [x] 冻结`public-induced audience affect`构念及排除边界
- [x] 冻结T0/T+Δ、统计单位、标签窗口与二分类兼容任务
- [x] 输出一页泄漏威胁模型并完成项目记录与自动检查
- **状态：** complete

### 阶段10：贡献级查新与协议上限冻结（步骤19—23）
- [x] 四条检索线分别完成前沿、经典和跨领域方法检索，并记录覆盖边界
- [x] 建立“最相近前作—相同点—不同点—必须对比实验”矩阵
- [x] 检查CARM工作名重名风险并冻结正式标题使用状态
- [x] 复核研究问题v1、C1—C3上限、H1—H4、主指标和失败条件
- [x] 输出baseline候选清单，记录代码、许可、任务匹配和预计复现成本
- [x] 更新查新协议、项目记录与自动验收
- **状态：** complete（CARM=`NAME_BLOCKED`；G1=`BLOCKED`）

### 阶段11：M2数据工程与标签隔离（步骤24—33）
- [x] 为已冻结主集建立不可变原始manifest；第二主集未冻结时显式阻塞，不伪造主集身份
- [x] 建立canonical schema、逐字段数据字典和T0/敏感等级约束
- [x] 将CSMV评论按视频聚合为经验分布，并生成video-group与hashtag-held-out划分
- [x] 建立先划分后索引、近重复/同源事件和发布者捷径审计边界
- [x] 生成CUC-IGPE-v2 canonical、漂移/冲突/重复BV/缺失时间台账
- [x] 物理隔离HUMAN_GOLD、SILVER、UNLABELED及加载入口
- [x] 固化银标管线元数据和100条错误审查候选协议
- [x] 增加确定性验收，更新进度、发现与工作记录
- **状态：** complete（步骤27已由00批准的LAI-GAI第二主集关闭；G1已通过）

### 阶段12：M2泄漏门、数据发布候选与G1/G2交接（步骤34—39）
- [x] 建立覆盖ID交集、同视频评论、目标评论字段、未来候选、train-only索引、时间顺序和fit范围的可机读泄漏门
- [x] 任一Critical命中时输出`LEAKAGE_BLOCKED`、返回非零状态并禁止写出正式split
- [x] 生成受G1状态约束的dataset-v1、split-v1、label-provenance-v1与数据审计报告
- [x] 完成Data Card、Datasheet、隐私、平台条款和可发布边界文档
- [x] 从原始manifest在隔离Python模式重跑最小预处理并固定哈希证据
- [x] 形成G1/G2逐条证据矩阵与`HANDOFF_10.md`，并已提交00任务审核
- **状态：** complete_with_g2_blocker（步骤34—39状态合同完成；G1通过，G2因CSMV正式输入资产与当前复现证据阻塞，不进入任务20）

### 阶段13：第二人工主集只读候选审计（AUTH-00-M1-SECOND-PRIMARY-READONLY-20260714）
- [x] 读取00审核结论并冻结只读授权、禁止下载/联系/gating/API边界
- [x] 形成不超过3个公开候选的元数据短名单
- [x] 仅深入审计1个候选的来源、revision、许可、规模、split、媒体、多人标注、T0与构念映射
- [x] 更新数据源台账与审计证据；保持G1/G2和`formal_split=false`不变
- [x] 运行专项验证、工作记录验证和准备验收，并回交00复审
- **状态：** complete_with_no_go（只读候选审计已完成并诚实No-Go；后续由阶段17的独立收口授权解决第二主集）

### 阶段14：G1/G2缺口修复与止损决策
- [x] 确认GitHub同步完成、工作区干净并恢复规划上下文
- [x] 逐项区分本地工程缺口与必须由外部数据/授权解决的硬阻塞
- [x] 检索并核验可替代第二主集；确认严格多模态候选仍无FIT，LAI-GAI仅可作范围降级候选
- [x] 对CSMV媒体/特征许可、topic/time/语义审计可关闭范围形成诚实裁定；恢复URL表解析并发现2644行语义错配
- [x] 形成`G1_G2_REMEDIATION_REPORT_20260714.md`，向用户报告许可/EULA/数据范围决策
- [x] 获得LAI-GAI第二主集并构建正式双主集manifest、标签映射、379组split与泄漏门；00已放行G1
- [ ] 闭合CSMV正式输入资产并完成当前核心隔离复现；只有00书面G2通过后才允许任务20
- **状态：** in_progress_g2_only
- **当前等待：** 按最小授权只读预审官方特征资产；新增不依赖CUC的公开benchmark核心隔离重跑并现场核hash。

### 阶段15：LAI-GAI范围变更与下载前准入审计
- [x] 用户明确选择路径1：LAI-GAI作为图像跨域第二人工主集方向
- [x] 形成`SECOND_PRIMARY_SCOPE_CHANGE_REQUEST_20260714.md`并向00发送范围变更/只读元数据授权请求
- [x] 取得00对SSOT模态降级、论文主张边界和OSF只读元数据审计的书面批准（`SC-20260714-01` / `AUTH-00-LAI-GAI-OSF-META-RO-20260714`）
- [x] 核OSF三个组件的公开网页asset license、revision、file tree、size、hash与gating；页面未显示项全部记`UNKNOWN`，未调用API或下载数据包
- [x] 在后续独立收口授权下形成LAI-GAI标签空间、样本量、split/group、prompt泄漏与T0映射
- [x] 在下载前完成确切文件、大小、许可和用途审查，并取得独立收口授权
- [x] 按独立授权构建原始manifest、正式标签映射/split并提交G1/G2复审
- **状态：** superseded_and_closed（本阶段旧网页/API授权保持No-Go；阶段17依据新的独立授权完成正式冻结，不追溯豁免旧失败）

### 阶段16：LAI-GAI限额OSF元数据API审计
- [x] 读取`AUTH-00-LAI-GAI-OSF-API-META-RO-20260714`并冻结host、节点、关系、请求数、体量、速率和禁止边界
- [x] 建立fail-closed顺序GET脚本；执行前验证raw目录受Git忽略、禁止重定向与下载链接跟随
- [x] 执行三个节点node/license/provider/file-list/分页元数据审计，记录26次请求、状态、字节数和响应SHA-256
- [x] 生成脱敏tracked manifest与三节点license/revision/provider/file tree/count/size/checksum/gating矩阵
- [x] 建立并运行边界validator；发现一次0.996519秒速率硬门失败，连同`K8XVH`空文件树写入台账与G1/G2证据
- [x] 回交00复审；当前No-Go且停止访问，不下载资产、不冻结LAI-GAI、不创建任务20
- **状态：** complete_with_no_go（00接受交付为带协议偏差观察证据；授权关闭、不重跑；`K8XVH`空文件树与速率硬门继续阻塞）

### 阶段17：第二人工跨域图像主集恢复
- [x] 保留旧LAI-GAI授权与失败证据不变；依据用户新指令签发独立收口授权`AUTH-00-SECOND-PRIMARY-RESOLUTION-20260714`
- [x] 优先补齐LAI-GAI核心图像资产定位与图像—评分关系；不重复旧26请求
- [x] LAI-GAI已闭合，无需切换OASIS；OASIS保留止损候选证据
- [x] 核验逐资产许可、固定revision、文件树/size/hash、公开字段和逐人/逐图人工标签粒度
- [x] 核验构念、T0输入、主指标兼容性、统计单位和group/near-duplicate/split威胁
- [x] 形成候选准入报告、数据源台账更新和00冻结申请；UNKNOWN不记为PASS
- [x] 只从公开、免费、无需登录且许可明确的入口下载最小必要资产；原始数据Git忽略，构建manifest/映射/split冻结候选
- [x] 复跑专项门、M2数据工程/发布门和工作记录验证；00以`REVIEW-00-LAI-GAI-FREEZE-20260715`书面批准第二主集并放行G1
- **状态：** complete_g1_pass_g2_blocked（847图、63682反应、379 group、594/127/126唯一split已冻结；G2转由CSMV正式输入资产与复现证据阻塞，禁止任务20）

### 阶段18：CSMV lineage修复与00 G2复审
- [x] 复核固定README与rawLinks工作簿，撤销内部ID必须等于平台ID的错误约束
- [x] 将8210样本归并为8008个平台源族，并重建video/hashtag split
- [x] 普通与隔离专项门、全局泄漏正负门均通过
- [x] 00接受命名空间纠正与202个重复源族零交叉结果
- [x] 00识别旧18输出复现manifest与当前9项hash不一致
- [x] 00裁定正式输入资产许可/revision/size/hash仍为G2硬阻塞，并签发最小只读预审授权
- [x] 任务10完成特征资产预审、公共benchmark核心隔离重跑和现场hash验证后再次回交G2
- **状态：** remediation_complete_pending_00_review（特征预审诚实No-Go；复现19项漂移0；不创建任务20）

### 阶段19：CSMV特征预审与当前复现链修复（2026-07-15）
- [x] 按`AUTH-00-CSMV-FEATURE-ASSET-PREFLIGHT-RO-20260715`匿名读取官方固定README所链公开Drive页面；未登录、未调用API、未下载特征或媒体
- [x] 建立特征预审manifest、报告和fail-closed validator；许可/revision/file tree/size/checksum/8210实测覆盖保持`UNKNOWN`
- [x] 为M2构建器增加`--public-core`，将CUC外部源根从公开benchmark核心重放解耦，同时核验冻结银标字节
- [x] 修复Python `-I -S`相邻模块导入与第二主集manifest fixity；保持LAI-GAI冻结合同
- [x] 从冻结CSMV raw manifest重建source-family、两套split、泄漏与release；19项before/after及现场hash漂移0
- [x] release validator改为现场重算复现hash，并纳入CSMV特征预审lineage
- [x] 首次官方GitHub Issues元数据请求尝试因集成权限返回403；无外部写入、请求额度未消耗，00已完成书面复审
- [x] 用户已在同一官方Issues渠道手工创建Issue #5；正式请求额度已使用，连接器重试和第二渠道停止
- [x] 用户扩大内部取得授权：允许可信第三方镜像、公开API和许可未闭合资产的隔离预取；正式使用门不变
- [x] 00独立复跑19项公共核心复现、release现场hash和泄漏正负门；关闭`REPRODUCIBILITY_STALE`子阻塞
- [x] 00接受特征预审为诚实No-Go，将G2收敛为单一资产准入包
- [x] 签发单一特征族最小元数据协调授权；不授权特征内容下载
- [x] 接入用户提供I3D兼容本地包；完成9942文件全量header/fixity审计、8210/8210覆盖和只读加载入口
- [x] 建立`csmv-i3d-quarantine-v1.manifest.json`，固定8210个必需文件逐文件hash与全包内容树hash
- [ ] 取得权利方资产级许可、稳定官方revision和包身份/fixity attestation，并将本地隔离证据再次回交00
- **状态：** repro_and_local_quarantine_integrity_closed_license_revision_attestation_pending
- **剩余硬阻塞：** 资产级许可、稳定官方revision、权利方对I3D包身份/fixity的确认与00书面复审；全局`formal_split=false`，不创建任务20

## 关键问题
1. 如何在细化步骤时遵守总纲v1.6已冻结的研究问题、数据角色和证据等级？
2. 如何避免把十个月机械拆成十个上下文割裂的Codex任务？
3. 每个任务达到什么水平才允许创建并进入下一任务？

## 已做决策
| 决策 | 理由 |
|------|------|
| 总纲当前v1.12为唯一SSOT，详细任务规格归入第17节 | LAI-GAI与CSMV lineage复审均已落盘；19项本地复现已获00确认，G2仅剩CSMV正式视觉输入资产准入；音频已移出关键路径且E1/E5/H3按实际可得输入条件化 |
| 使用7任务结构：00总控+6执行任务 | 保留阶段连续性，同时控制上下文规模 |
| 当前只已创建10-M1–M2任务 | 后续任务必须由上游退出门触发 |
| 独立规格文件仅作为总纲第17节的便捷副本 | 后续任务只需读取一个权威文件即可获得研究与执行要求 |
| 总纲第17节优先于独立规格副本 | 防止双重权威和需求漂移 |

## 遇到的错误
| 错误 | 尝试次数 | 解决方案 |
|------|---------|---------|
| 首次内嵌时第17节标题误带字面量`+` | 1 | 已删除多余字符并纳入结构校验 |
| `rg`在当前Windows环境启动被拒绝 | 1 | 改用PowerShell `Select-String`完成只读扫描 |
| 初次`.gitignore`例外未解除`data/raw`等父目录忽略 | 1 | 改为逐级解除目录并只放行受控README/manifest扩展名，加入自动反向检查 |
| 步骤6—10审计再次调用`rg`被系统拒绝启动 | 2 | 不再重试；继续使用PowerShell递归文件清单和`Select-String` |
| Web工具拒绝直接打开GitHub/HF API URL | 1 | 改用无凭证、只读的官方HTTP API；固定commit/revision后写入manifest |
| PowerShell `Invoke-WebRequest -Method Head`读取ACL附件触发空引用 | 1 | 改用`curl.exe -I`，确认附件为2,080,204 bytes |
| 表格工具导入CSMV URL清单时上游theme含非法百分比OpenXML值 | 2 | 已改用不加载样式的Strict OOXML只读解析；8210行ID集合覆盖通过，但发现2644行ID—URL路径错配，媒体映射转为显式BLOCKED |
| 步骤34—39盘点时`rg --files`仍因Windows执行权限被拒绝 | 3 | 不再调用`rg`；统一改用PowerShell `Get-ChildItem`与`Select-String` |
| 首次`-I -S`隔离重跑时发布构建器无法导入相邻泄漏模块 | 1 | 在构建器中仅显式加入已审查的`scripts/`目录；不恢复site-packages，随后重建基线并重跑 |
| 阶段19首次调用`rg`扫描工作区时Windows再次拒绝执行 | 1 | 立即改用PowerShell `Get-ChildItem`/`Select-String`，未重复同命令 |
| PowerShell运行时不支持静态`SHA256.HashData` | 1 | 改用`SHA256.Create().ComputeHash()`；首次结果未作为hash证据 |
| `build_m2_data_artifacts.py -I -S --public-core`首次无法导入相邻`csmv_media_lineage` | 1 | 仅把已审查`scripts/`目录加入`sys.path`，保持site-packages禁用；重跑成功 |
| 公共核心首轮被第二主集provenance引用hash漂移阻断 | 1 | 固定provenance序列化声明并更新其引用hash；不改LAI-GAI canonical或冻结标签合同，随后fixity门通过 |

| `planning-with-files-zh`会话恢复脚本在Windows GBK终端输出特殊符号失败 | 1 | 已读取恢复摘要；不重复原命令，改以Git状态和三份规划文件作为恢复事实源 |
| 读取00应维护的`DECISION_LOG.md`/`RISK_REGISTER.md`时文件不存在 | 1 | 不在任务10伪建00权威台账；改建任务10范围变更请求并发送00，由00决定是否创建/更新总控文件 |
| LAI-GAI API采集器首次运行在最终manifest构造处使用Python小写`false`，触发`NameError` | 1 | 不重复网络采集；保留已写raw请求证据，修正布尔量并增加离线重建模式，从现有响应生成tracked产物 |
| API审计整合补丁因00并发更新后`DATA_SOURCE_LEDGER.md`状态行与旧上下文不匹配而校验失败 | 1 | 补丁未部分应用；重新读取当前行并拆分为新增文件、逐文件小补丁，保留00最新内容 |
| LAI-GAI API边界validator发现请求2→3的UTC间隔仅0.996519秒，短于授权≥1秒 | 1 | 不使用容差、不重跑网络；登记独立No-Go合规项，采集器增加0.1秒安全余量，离线manifest固定实际最小间隔并交00复审 |
| 00最终复审落盘并并发更新台账后，任务10基于上一版状态行的整合补丁校验失败 | 1 | 补丁未部分应用；读取00最新状态，只补manifest review块、可行性矩阵和任务10证据，不覆盖总控更新 |
| 00与任务10并发追加工作日志，双方均使用`WR-20260714-024`导致编号重复 | 1 | 保留00的024，任务10记录顺延为025；复验连续性与综合门 |
| LAI-GAI CSV/XLSX首次结构画像在终端输出阶段因GBK无法编码Unicode列名而失败 | 1 | 数据只读解析已完成但未形成输出；固定`PYTHONIOENCODING=utf-8`后重跑，不修改源文件 |
| 系统PATH中未找到`pdfinfo.exe`和`pdftotext.exe`，README首轮PDF读取无法启动 | 1 | 不重复同命令；改用已加载的工作区Python `pypdf`提取文本，并明确视觉版式未覆盖 |
| SMID官方论文首次按猜测的PLOS DOI打开了无关植物生态论文 | 1 | 不复用猜测DOI；改由题名/作者精确检索定位正确论文与数据记录 |
| LAI-GAI浏览器存储名首次按全局七字符后缀正则归一化，误删合法`hygiene`片段 | 2 | 改为逐个候选删除并要求恰好命中冻结847清单；随后9页847项双向闭合 |
| 官方ZIP与逐图下载期间00和任务10出现并发下载进程 | 1 | 停止重复ZIP及任务10遗留子进程；保留使用`.part`原子替换的官网静态媒体下载器，最终对847图全部重算hash和解码验证 |
| 构建器遍历OSF单对象`data`时误按字典键迭代，且Python 3.8不支持`int.bit_count` | 2 | 将单对象统一包装为列表；汉明距离改用`bin(x).count('1')`，无网络重访 |
| 首版把整个来源数据库合并为group，导致split为272/120/455且test覆盖修复代价过大 | 1 | 将source定义收紧为原始source item/生成族，数据库名仅作provenance；重建为379 group和594/127/126，所有12类覆盖且跨split近重复为0 |

## 备注
- 网页或外部材料只写入findings.md，不写入本计划。
- 每完成一个阶段即更新状态。
## 阶段17续：已记录问题（2026-07-14）

- `rg` 对既有 raw 元数据目录执行时被 Windows 拒绝访问并 exit 1；未改变文件，后续改用 Python/PowerShell 只读解析，不重复该命令。
- 首次联合画像脚本引用清洗输出中不存在的 `is_careless_2` 列并触发 `KeyError`；原因是误把预清洗 `S*_data.csv` 当成 `S*_data_out.csv`。失败保留，后续已取得官方 `_out` 文件并按其实际列重跑。
- 官方 `all_images.zip` 可续传 GET 确认总长约 226.2 MiB，但服务器平均仅约 11 KiB/s；本次从既有 7,598,080 bytes 续传后在约 22 分钟处失败，局部文件保留。下一步改用同一官网公开图片详情页的逐图官方地址，限并发取得 847 张图片并与评分键闭合。
- 首次逐图 Python 获取继承了本机失效代理环境，TLS 代理连接触发 `ProxyError/FileNotFoundError`；未写入图片，改为 `requests.Session(trust_env=False)` 后直连官网成功。
- 4路逐图批次被主动终止以检查吞吐，已完整保留275张；16路续跑完成847张和映射清单后，仅清理旧 `.part` 时因瞬时文件锁 exit 1。进程结束后复核目录为847个JPEG、0个part，正式资产不受影响。
- 首次 canonical builder 在 Python 3.8 上调用不可用的 `int.bit_count()`，处理到近重复哈希阶段后 exit 1、未写manifest；已改为 `bin(x).count("1")` 保持相同汉明距离语义。
- 一次诊断脚本错误假设 `S1_data_out.csv` 含 `target_emotion` 列而触发 `KeyError`；只读失败，随后按实际列重跑。最终标签以官方逐图汇总表而非分研究中间表为权威源。
- 合并任务10候选后，首次按新追溯manifest重建canonical得到SHA-256 `caffd153...`，与候选冻结hash `ad58c268...` 不同并fail-closed；原canonical未覆盖。下一步保留临时输出并逐字段比较，定位序列化或字段合同差异。

## 阶段18回交记录：CSMV媒体lineage与同源split修复（2026-07-15）

- **状态：** reviewed_lineage_accepted_g2_blocked
- [x] 复核官方README、固定commit工作簿字段和8,210条集合关系，撤销“内部ID必须等于URL平台ID”的错误假设。
- [x] 识别8,008个平台源视频族、202个重复族/404条样本；量化修复前100个video-split与115个hashtag-split同源交叉。
- [x] 建立脱敏逐项lineage manifest；按源族重建`group_by_video_v1`并把同源族并入hashtag连通分量。
- [x] 专项validator、全局泄漏live门与负面selftest通过；同源族在全部已发布协议跨split为0。
- [x] 同步Data Card、Datasheet、数据源台账、风险台账、G1/G2证据与交接材料。
- **当前等待：** 按`AUTH-00-CSMV-FEATURE-ASSET-PREFLIGHT-RO-20260715`完成官方特征元数据预审；修复公开benchmark核心隔离重跑与现场hash门。
- **复现限制：** CSMV专项已用Python `-I -S`隔离验证；旧18输出复现记录经00现场核验有9项与当前版本不一致，已改为显式STALE，不能继续作为当前G2 PASS。

### 阶段20：I3D序列协议、论文边界与Git检查点（2026-07-16）

- [x] 读取总纲v1.12、00音频裁定、工作记录政策和最新日志，刷新共享Git状态。
- [x] 测试先行冻结完整序列+动态padding/mask主协议；初始测试按预期因模块不存在失败。
- [x] 冻结确定性均匀180步主敏感性与前180补充规则，闭合短序列、最长边界、dtype/shape、非有限值、资源门与test自适应负面测试。
- [x] 建立版本化文档、JSON配置、机器manifest、构建器、实现和validator；专项验证通过。
- [x] 收紧论文主张及E1/E5/H3、Data Card/Datasheet、G门和回交合同。
- [x] 重建19项公共核心release并完成综合检查、compileall、diff/security审计。
- [x] 建立M1—M2 Git阶段提交、推送当前分支并回交00复审。
- [x] 00独立复核并签署`REVIEW-00-CSMV-I3D-SEQUENCE-PROTOCOL-20260716`；序列协议子缺口关闭，资产G2不变。
- **维护者状态：** `DEFERRED_PENDING_MAINTAINER_REPLY`；本轮不等待、不催促、不重复检查，不写成已解决。
- **门状态：** G1=`PASS`；G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；`formal_split=false`；未创建任务20。
