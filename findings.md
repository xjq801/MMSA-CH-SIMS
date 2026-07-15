# 发现与决策

## 需求
- 用户要求依据总纲，详尽列出每个Codex任务的工作内容、具体步骤和目标水平。
- 交付应能直接作为新任务的首条提示和验收依据。

## 研究发现
- 唯一总纲为 `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.5；详细任务规格归入第17节。
- 总纲明确：当前任务负责总控；M1数据审计、M3基线、M4教师学生、M5检索记忆和论文写作应按需使用独立任务。
- 已确定的紧凑任务树为：00总控、10数据与协议、20基线与评测、30教师学生、40反应记忆、50正式实验与结果冻结、60论文与投稿。
- 当前已创建 `10-M1–M2 数据与协议`，共用 `D:\MMSA-CH-SIMS`，没有工作树。
- P0开工准备已完成T0政策、Git初始化、环境快照和数据来源台账；统一实验配置、claim-evidence表和更细的安全/凭证轮换仍应由10任务补齐。
- 10任务必须通过G1和G2，才能创建20任务；数据许可、第二人工标注集和物理泄漏隔离是硬门，不是文档形式检查。
- 20任务承接E0/E1和统一评测器，最低要求是可信复现至少一个官方/强基线；未过G3不得创建复杂模型任务。
- 30任务只验证H1：评论特权teacher是否为内容student提供稳定分布监督；若失败，回到标签/聚合，不得直接叠加检索。
- 40任务只验证H2并补H3机制：train-only memory、有效检索、可靠性路由和负对照；随机检索同样好时必须止损。
- 50任务覆盖M6—M8与E0—E9正式证据，负责多种子、OOD、缺失模态、统计、中文压力测试和结果冻结。
- 60任务只能消费冻结结果，覆盖M9—M10，完成论文、复现包、模拟审稿和投稿Go审计，不得在写作阶段改主假设追分。

## 技术决策
| 决策 | 理由 |
|------|------|
| 每个任务采用“目标—输入—步骤—交付物—验收—止损—交接”结构 | 便于直接执行和阶段审计 |
| 设置最低合格线与T-AFFC目标线 | 防止只完成形式性产物就进入下游 |
| 代码写入任务不并行 | 所有任务共用同一Git工作区，避免冲突和证据漂移 |
| 只读查新/许可核查可在同一任务内部并行 | 不产生共享文件写冲突 |
| 任务创建由上游退出门触发 | 避免提前建立过时上下文和绕过止损门 |
| 50任务合并M6—M8 | 三个月共享冻结模型、正式矩阵和结果版本，拆开会增加证据漂移 |
| 60任务合并M9—M10 | 写作、预审、修订和投稿必须围绕同一冻结稿件与复现包 |

## 遇到的问题
| 问题 | 解决方案 |
|------|---------|
| 总纲很长且包含多层月份/实验/门 | 先提取标题和相关区段，再构建交叉映射检查 |

## 最终规格摘要
- 2026-07-14：执行规格已并入总纲第17节；独立规格文件降级为便捷副本，冲突时总纲优先。
- 第17节与独立规格正文机械比对完全一致；七个任务标题、G1—G6、H1—H4、E0—E9和v1.5启动头均通过校验。
- 已向现有任务 `10-M1–M2 数据与协议` 发送v1.5同步提示，要求重新读取总纲第17节。
- 规格文件共645行，覆盖7个任务、G1—G6、H1—H4、E0—E9和全部T0硬边界。
- 每个任务均含定位、总纲映射、启动条件、逐步工作、必须产出、质量等级、止损与禁止。
- 任务10步骤39项；任务20步骤18项；任务30步骤16项；任务40步骤19项；任务50步骤32项；任务60步骤32项。
- 后续任务仍按门逐个创建，不因规格已存在而提前启动。

## 资源
- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md`
- `T0_INPUT_POLICY.md`
- `DATA_SOURCE_LEDGER.md`
- `ENVIRONMENT_LOCK.md`
- `00_开工执行大纲_20260713.md`

## 2026-07-14 步骤34—39：自动化验收与文档

- 新泄漏门覆盖8项Critical合同：item ID交集、source group交集、评论—视频归属、目标评论字段、未来候选字段、train-only索引、time split顺序和fit范围。
- 当前CSMV候选0个Critical失败；负面夹具同时注入跨split重复、目标评论、未来互动、全量fit和逆序time split后正确返回`LEAKAGE_BLOCKED`。
- `time_order`为`NOT_APPLICABLE_NO_TIME_SPLIT`，原因是CSMV无发布时间且未发布时间split；它不是“时间安全已证明”。
- `dataset-v1`与`split-v1`均固定为`LOCAL_CANDIDATE_G1_BLOCKED`，`formal_split=false`、`formal_model_use_allowed=false`；泄漏自动门通过不改写G1/G2状态。
- 标准库管线在Python `-I -S`隔离进程中从原始manifest重跑；18个核心输出重跑前后SHA-256一致，未转发凭证环境。
- 首次隔离重跑暴露相邻模块在`-I`下不可导入；只将已审查的项目`scripts/`目录显式加入路径后重跑成功，未恢复site-packages。
- Data Card、Datasheet、隐私、平台条款、发布边界、数据审计、G1/G2矩阵与任务10交接均已形成。
- G1继续因第二人工主集未冻结而阻塞；G2因G1未过、正式split未形成及语义近重复/发布者审计开放而不具备审核资格。

## 视觉/浏览器发现
- 本任务无需视觉或浏览器材料。

## 2026-07-14 开工准备包审计

- 结论：准备包有必要；它是M1前的泄漏、安全与复现门，不是额外研究工作包。
- 已达标并跳过：`T0_INPUT_POLICY.md`；Git初始化；`.gitignore`对环境、密钥、数据、权重、日志和结果的排除；`DATA_SOURCE_LEDGER.md`；历史环境快照与依赖锁。
- 项目是既有自定义Python研究仓库，根目录含大量未跟踪历史资产；不得自动搬移、删除或套用固定目录模板，本次只做非破坏性补充。
- 当前环境`pip check`通过，torch/CUDA、CatBoost、transformers、scikit-learn、MMSA可导入；`faiss`未安装，因此只能判定历史环境可用，不能宣称正式CARM环境或空环境重建已通过。
- D盘剩余约75.1GB；在M1数据许可门前足够做文档、审计和小型处理，但是否足够容纳两个公开数据集及媒体尚为`UNKNOWN`，禁止据此提前下载大数据。
- 红acted密钥扫描命中0；`.env`被忽略，`configs/`、`paper/`和`references/`应进入Git。
- 缺口：统一实验配置与验证器、目录政策、claim—evidence表、实验登记、安全验收记录、时间/资源政策、BibTeX骨架、环境复现验收报告。
- 上述本地缺口已补齐。重复检查结果：配置有效；未来评论负测试通过；历史环境导入通过；Git忽略通过；密钥扫描0命中；模板残留0；Python编译通过。
- 自动判定为`m1_read_only_work_ready=true`、`formal_model_work_ready=false`。后者是预期门控：faiss缺失且正式数据/检索方案未过M1，不应提前创建或冻结正式训练环境。
- 不能由本地代理代替的外部动作只有账户侧凭证轮换确认；在确认前API与付费调用保持禁止，因此不阻塞M1只读工作，也不会造成额外风险扩散。

## 2026-07-14 M1预下载审计启动

- 准备门已复核通过：允许只读许可核查、数据可行性审计和小型公开元数据验证。
- 正式模型环境仍为`BLOCKED_M1`；不安装faiss、不训练、不下载媒体包。
- 审计顺序：CSMV → iNews → 必要时NEmo+；MVIndEmo仅核合法来源和银标生成边界。
- 所有网页发现只记录为待证事实；必须由官方仓库、论文页、许可文件或作者数据页交叉支持后才能从`PENDING/UNKNOWN`升级。

### 首轮官方入口发现（仍属预审）

- CSMV官方NeurIPS页面确认论文、8210个视频、107267条人工标注评论及官方GitHub入口；GitHub仓库显示Apache-2.0仓库许可，并提供评论JSON、`video_file_id`、I3D/VideoMAEv2特征说明和原始视频URL表。
- CSMV的仓库级Apache-2.0是否明确覆盖数据标注、特征和第三方TikTok媒体/URL仍需分别核验；在此之前许可结论保持`PENDING_REVIEW`，不能把代码许可自动外推到媒体再分发。
- iNews官方ACL论文页、作者GitHub与Hugging Face入口已定位。完整persona版本为gated，标注CC BY-NC-SA 4.0，并要求不重识别、不转交第三方、禁止商业及政治定向用途。
- iNews公开版本不需要persona访问申请，但图像/截图因版权不随数据发布，只提供原Facebook链接、文本和元数据；因此“人工标签可得”与“可复现多模态输入”必须分开判定。
- iNews当前公开划分包含按用户/内容组合设计的personalization/generalization/cold-start场景；本项目仍需另行验证能否按帖子聚合并构造与T0一致的post-group正式测试。

### 第二轮许可与T0风险发现

- iNews公开版页面明确标注`CC BY-NC-SA 4.0`；预审页面计数曾被记录为12276，固定revision下载后实证为11320行，后者作为权威包级计数。完整persona版需要申请且附带更严格的隐私/不转交约束；当前主任务不需要persona字段。
- iNews媒体不是数据包组成部分。作者只提供帖子URL和截图工具，并要求使用者自行遵守网站条款、限速、法律与伦理要求；因此多模态图像输入当前仍为`PENDING_MEDIA_REPRODUCIBILITY`，不能仅凭标签CSV可访问就判G1通过。
- iNews论文示例prompt含最终互动量、评论量和分享量。这些字段违反本项目T0政策，必须在数据字典中标为`available_at_t0=false`并从任何正式输入/截图OCR派生字段中物理排除。
- 若自行恢复Facebook截图，画面可能直接显示互动量或评论信息，存在视觉通道泄漏；即使截图采集合法，也必须定义裁剪/遮挡和自动验收规则。未获批前不运行作者截图工具。
- iNews论文报告机构伦理审批与知情同意，为人工标注真值提供伦理来源证据；这不自动解决新闻图片版权、Facebook条款或本项目再分发权限。
- iNews公开文件页显示当前数据仓库约26.5MB，含train/dev和三个公开test CSV、codebook；页面给出verified revision `a7ad599`。该体量仅用于预下载预算判断，不代表字段或许可已最终验收。
- CSMV评论目录公开列出train/dev/test、标签映射、压缩的全量标注字典和`video_to_comment.json`，说明视频级重聚合在结构上可行；仍须在授权下载小型标注后做字段与覆盖率实证。

## 2026-07-14 开工准备五项复核结论

- 总纲选中步骤1—5已由现有准备包实质覆盖：安全与大文件边界、凭证阻塞、统一配置、数据目录政策、claim—evidence与文献入口均有文件和自动检查证据，不需要重复建设。
- 本地可执行项全部复核通过。唯一不能由本地代理完成的是账户侧凭证轮换确认；它保持外部阻塞，并通过“禁止API/付费调用”隔离风险，不阻碍M1只读审计。
- 形式环境仍缺`faiss`，但这属于M1门前的预期`BLOCKED_M1`，不应为了准备步骤提前安装。

## 2026-07-14 步骤6—10现有资产审计（进行中）

- 使用只读脚本`audit_group_dataset.py`复跑外部数据根目录，得到：2787条有效向量行、其中2779条有BV且均唯一、8条缺BV；2772条能匹配同发布者标签记录，其中2551条标签一致，因此“约221条冲突”可由`2772-2551=221`复核。
- 标签表共有13794条记录，其中2665条显式二分类、11129条由旧阈值派生；982条显式标签与旧阈值规则不一致，说明旧阈值不能作为新标签定义。
- 只有883/2779个唯一向量BV能在全局关联到发布时间；现有全量数据不足以支持严格时间协议。195条旧子集的“chronological”结果若以缺失时间回退文件顺序，必须降为探索证据。
- 旧代码存在直接目标评论泄漏路径：`run_bert_text_fusion_experiment.py`读取评论内容与评论点赞数、选取高赞评论并拼入文本特征；`run_llm_ready_emotion_student.py`、StepFun缓存评估等也从目标视频评论生成情绪元特征。它们可保留为teacher/标签工程代码参考，但其原结果不得作为T0 content-only证据。
- 多个旧脚本明确使用固定随机80/20或70/30；既有审计显示topic/publisher held-out性能大幅下降，旧随机高分仅能作为历史或探索结果。

### 冻结结论

- 已形成`legacy-asset-lineage.md`，将外部只读数据、旧代码、实验JSON与报告串成11条lineage；2815版本缺少原始manifest，28条漂移去向保持`UNKNOWN`。
- 48维向量表头包含播放量与热度系列；其采集时点未证明为发布时可得，因此按T0默认禁止。旧48维模型代码可复用，旧数值只能作历史诊断。
- 已按“可复用代码、历史基线、仅探索结果、禁止进入新论文证据”冻结旧资产用途；评论特征、评论用户全图、未来互动和旧随机高分均不能进入新论文证据。
- `research-question-v1.md`将`public-induced audience affect`与说话者情感、画面群体情绪、第三章传播链明确分离。
- `experiment-protocol-v1.md`冻结T0为主任务；T+Δ因CUC时间覆盖不足保持`DISABLED_PENDING_TIME_AUDIT`；统计/划分/bootstrap单位均为视频或帖子；二分类仅为兼容次任务。
- `leakage-threat-model.md`覆盖目标评论、未来互动、推荐结果、同作者/近重复、索引、全图构建，并补充预处理与伪时间两类风险。该模型是当前威胁清单，不宣称查全全部泄漏。

## 2026-07-14 步骤11—18官方证据核验（进行中）

- `[snapshot 2026-07-14, src=NeurIPS论文页/官方GitHub]` CSMV论文确认8210视频、107267人工标注评论；官方仓库README明确comment字段含`video_file_id`、`comment`、opinion、emotion和hashtag，并声明官方7:1:2是按comment data ID随机划分。
- `[snapshot 2026-07-14, src=官方GitHub]` CSMV README对许可给出比根LICENSE更细的说明：代码MIT、annotations CC BY-SA 4.0；仓库根部GitHub识别的LICENSE为Apache-2.0。三者需按资产分层，不能把Apache自动外推到标注或TikTok媒体。
- `[snapshot 2026-07-14, src=官方GitHub]` CSMV提供I3D和VideoMAEv2视频特征下载入口，文件名与`video_file_id`对应；原媒体仅给TikTok URL表，媒体版权、链接存活率和再分发仍未知。
- `[snapshot 2026-07-14, src=iNews作者GitHub/HF]` iNews公开版为emotion labels only、无persona、开放访问；HF标记CC BY-NC-SA 4.0，viewer显示Post_ID、Annotator_ID、V/A/D、9类Discrete及5个公开split。
- `[snapshot 2026-07-14, src=iNews作者GitHub]` 图片因存储与版权不随包发布，需从URL自行截图；作者明确要求遵守网站条款、限速、伦理与法律。该路径尚不能满足可复现多模态输入门。
- `[snapshot 2026-07-14, src=ACL Anthology]` NEmo+有1297组新闻标题+主图、38910条众包标注，并明确支持诱发情绪分布预测；ACL页面直接提供Dataset.zip，但许可、图片再分发和实际字段仍待包级审计。

## 2026-07-14 步骤11—18实证与选择门结论

- CSMV固定上游commit为`99d14240254b1381dde0b9c56add140381f65117`。小型标注/映射/URL清单共14,436,790 bytes；逐文件URL、大小、日期与SHA-256已写入`data/manifests/csmv-source-v1.manifest.json`。
- CSMV正式split为75,086/10,727/21,454条评论，评论ID无交叉；但train/dev/test视频交叉分别为5,819、7,341、5,332个，且5,319个视频同时出现在三者。官方comment split对本研究构成视频级泄漏。
- CSMV的107,267条正式评论均有`video_file_id`和hashtag，覆盖8,210个视频与35个hashtag；group-by-video和hashtag-held-out结构上可构造，无原生topic字段。opinion有5条`None`，emotion有1条`None`，不得静默填充。
- CSMV README明确annotations为CC BY-SA 4.0；根LICENSE为Apache-2.0、README称代码MIT。标注、代码、特征、TikTok媒体必须分层处理，不能互相外推许可。
- CSMV官方URL清单已固定版本并核hash；表格工具因上游theme的非法百分比OpenXML值两次导入失败，已停止重试。URL行级覆盖/存活率保持`PENDING`，未下载媒体或特征。
- iNews public固定HF revision为`a7ad599a257e94f04f796a86d39635adadb5f7cb`，公开包26,502,742 bytes，含11,320行、2,736个post；相比论文2,899个post少163个，原因保持`UNKNOWN`。
- iNews九类离散标注为anger、contempt、disgust、fear、happy、neutral、other、sad、surprise；VAD范围均为1—7。公开文件内generalization-test与train重叠1,214个post，cold-start与personalization-test重叠343个post，不能直接作为本项目split。
- iNews公开包没有图片文件或直接媒体字段；作者要求另从Facebook恢复。论文说明截图保留reaction count，违反T0输入边界。裁定`NO_GO_PRIMARY_MEDIA_REPRO`。
- direct6草案对iNews只保留7,024/11,320行（62.05%），丢4,296行；227/2,736个post会完全失去标注。因此不将direct6替代原生九类/VAD，只作为将来预注册的敏感性分析。
- iNews No-Go后已按规则审计NEmo+。ACL附件2,080,204 bytes，含1,297个news item及T/I/TI各12,970条反应；包内0张图片、0个许可文件，图片引用均为不可解析的`anonymous-source/*.jpg`相对路径。裁定`NO_GO_PRIMARY_LICENSE_MEDIA`。
- MVIndEmo论文明确标签由三个评论情感模型置信融合，并按评论点赞加权聚合。论文所列GitHub在网页与API核验均404；固定为`SILVER_ONLY_SOURCE_UNAVAILABLE`，不阻塞G1也不计入人工金标。
- 当前选择门结论：CSMV视频分组结构级通过；iNews与NEmo+均未形成合法可复现的第二多模态输入，第二人工标注主集未冻结，G1保持`BLOCKED`，G2未进入验收。

## 2026-07-14 步骤19—23四路查新与协议冻结

- 检索类型固定为`SCOPING`，截止日2026-07-14；四条检索独立留痕，覆盖OpenAlex、Crossref、DOAJ的自动召回，并以论文、正式会议页面、预印本或官方代码仓库复核核心条目。自动召回噪声较高，只作候选池，不把排序分数当相似性或新颖性结论。
- 评论特权监督的直接方法锚点为LUPI、generalized distillation和M2PKD。M2PKD已在情感识别中以训练期额外音频模态教视觉学生，证明“训练期特权、测试期缺席”并非本项目首创；本项目可检验的差异仅是评论作为受众响应特权信息、分布目标与严格T0隔离。
- 公众诱发情绪方向的最近任务锚点为MVIndEmo、CSMV/MSA-CRVI和iNews。CSMV直接建模视频诱发的评论情绪但其公开baseline把目标评论作为输入；本项目不得声称首次提出公众诱发情绪，最多检验content-only T0下的受众分布预测和无泄漏协议。
- 检索增强方向的直接锚点为RAMER。其官方实现使用FAISS和检索到的多模态情绪样本处理缺失模态，许可证为Apache-2.0；因此H2必须包含无检索、随机检索、BM25/CLIP-kNN与RAMER式检索对比，并以train-only index和OOD负迁移作为差异边界。
- 可靠性/缺失模态方向的锚点包括MissModal、IMDer、HRLF、Selective Classification与SelectiveNet。缺失模态鲁棒性和拒绝学习均已有成熟前作；本项目只能主张其在public-induced distribution目标、T0和联合OOD/缺失协议下的验证，不得把模块组合写成一般性首创。
- `CARM`已明确重名：至少存在Confidence-aware Recommender Model、Constraint-Aware Retrieval Module、Conformal Association Rule Mining、Cache-aware Roofline Model、CarM episodic memory及多个视觉模块。正式标题和模型名继续标记`NAME_BLOCKED`，直到另行选名并复查。
- `research-question-v1.md`与`experiment-protocol-v1.md`已有FROZEN_v1内容与总纲C1—C3、H1—H4一致；本轮只增加交叉核验记录，不改主指标、不扩贡献上限。主指标保持JS divergence；NLL/EMD、Brier/ECE/ACE、risk-coverage/AURC为预注册辅指标与可靠性指标。

## 2026-07-14 步骤24—33 M2数据工程与标签隔离

- CSMV固定源hash复核后，107267条正式人工评论可无损归属到8210个视频；视频级聚合后不再携带评论ID或正文。每个经验分布同时保留反应数与可解释的不确定性统计，避免把少量评论与大量评论视为同等确定。
- 固定salt的`group_by_video_v1`得到train/dev/test=5719/816/1675；hashtag—视频连通分量方案得到5990/602/1618，35个连通分量跨split为0。CSMV没有原生topic，不能把hashtag伪装为topic。
- 构建顺序已经机器化为“核原始manifest→按item聚合→分配split→未来仅取train建索引”；当前索引明确`NOT_BUILT`，未因M2实现提前安装faiss或进入检索建模。
- 当前资产只能排除精确item/group交叉，不能排除媒体感知近重复或语义同源事件。CSMV无媒体/标题事件指纹和发布者字段，因此这些项保持`UNKNOWN/NOT_TESTABLE_WITH_CURRENT_ASSETS`，不是PASS。
- CUC的132个源文件建立逐文件hash、样本数与字段清单；许可仍未知，源路径仅以匿名hash进入manifest。canonical复现2787条、8条缺BV、0条重复BV、221条标签冲突及883条发布时间覆盖。
- 883条CUC时间匹配中有1条只在另一个发布者目录找到，表明发布者目录/元数据lineage存在捷径风险；该记录保留`GLOBAL_CROSS_PUBLISHER`标记，不静默视为普通本地匹配。
- 2815历史口径没有原始manifest，28条漂移仍无法解释；221冲突只标记不自动重标。100条错误审查候选为`PENDING_HUMAN`，不能作为正式性能证据。
- `HUMAN_GOLD`、`SILVER`、`UNLABELED`已物理分区并分别建manifest。加载器一次只接受一个tier，拒绝评论正文键；CUC教师快照和置信度未知，因此保留银标身份。
- 第二人工主集仍未冻结。版本化映射清单明确`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`且禁止test驱动改表；因此本地M2产物检查通过不等于G1/G2通过。

## 2026-07-14 第二人工主集只读候选审计（进行中）

- 授权编号为`AUTH-00-M1-SECOND-PRIMARY-READONLY-20260714`：短名单不超过3个，仅深审1个；不下载数据、媒体或特征，不使用登录态/绕过gating，不调用API/付费服务，不联系作者，不修改G门。
- 初筛硬门为：公开可定位、人工诱发情感标注、内容项可分组、媒体可合法复现、至少具备可定义的T0内容输入、许可不依赖推断；`UNKNOWN`不按通过处理。
- `[snapshot 2026-07-14, src=LIRIS-ACCEDE官方站/官方论文/官方EULA]` LIRIS-ACCEDE含160部CC电影的9800个8—12秒片段；离散标注使用CrowdFlower成对比较，最终提供valence/arousal秩。官方Protocol A按电影划分4900/4900 train/test，避免同电影跨split。
- `[snapshot 2026-07-14, src=LIRIS-ACCEDE官方站/官方EULA]` 获取任何六类集合均需由永久学术职位人员签署EULA并邮件申请，且只限学术非商业使用、禁止再分发；片段沿用各源电影CC许可，annotations/描述文件为CC BY-NC-SA 3.0。本轮授权禁止联系作者或通过gating，因此当前只能裁定为准入阻塞候选，不能下载核验。
- `[snapshot 2026-07-14, src=LIRIS-ACCEDE官方论文]` valence有582k次标注、187k次比较、1517名trusted annotator；arousal有665k次标注、221k次比较、2442名trusted annotator。公开的是最终秩而非原始worker judgments，因此可验证多人诱发情感监督，但不能直接重建与CSMV同形的经验离散分布及其不确定性。
- ArtEmis预筛显示约8万件艺术品、45.5万条主导诱发情绪及解释，但官方访问同样要求表单批准，原WikiArt图像版权由研究者自行承担，输入主要为单图；因此不纳入本轮3项短名单。
- `[snapshot 2026-07-14, src=PMEmo作者官方GitHub]` PMEmo公开说明794首歌、457名受试者、静态与0.5秒动态VA、EDA、副歌MP3和音频特征；2019更新加入歌词与中英文在线评论，全包约1.3GB。完整歌曲因版权不提供；仓库MIT文本限定“Software”，不能自动覆盖数据、MP3、歌词、评论或标注。
- PMEmo仓库当前commit可定位为`90289847fcb84e82024c3be1512b0f1d83925a55`，但dataset目录只有`.gitkeep`，实际2018/2019数据在外部Drive且没有公开hash或固定split。在线评论属于T0后/目标邻接信息，必须禁止输入；因此裁定`NO_GO_LICENSE_SPLIT_AND_LABEL_DISTRIBUTION_UNKNOWN`。
- `[snapshot 2026-07-14, src=CVPR官方论文]` Emotion6含1980张Flickr图像，每个搜索类别330张，432名独立受试者、每图15人；人工真值为Ekman六类加neutral的七类诱发情绪分布及VA。论文只报告随机7:3，不是来源组或事件组隔离。
- 定向官方入口检索未定位到仍由作者维护、带明确许可和固定revision的Emotion6数据发布页；Flickr逐图权利、包体量和hash保持`UNKNOWN`。其标签构念最贴合但只有单图模态，裁定`NO_GO_MEDIA_LICENSE_ACCESS_AND_MODALITY`；该检索为scoping，不声称穷尽互联网。
- 三项短名单最终固定为LIRIS-ACCEDE、PMEmo、Emotion6；仅LIRIS-ACCEDE进入深审。当前没有任何候选达到`FIT`或`READY_TO_DOWNLOAD`，G1/G2与`formal_split=false`不变。

## 2026-07-14 G1/G2缺口修复检索（进行中）

- `[snapshot 2026-07-14, src=BEAT官方项目页]` BEAT有124个视频和245名标注者，并展示11类比例分布；但任务要求标注者持续判断目标角色的情绪，属于他人情绪感知而非观众自身被诱发情绪。官方页下载仍为`TBD`，网页CC BY-SA许可也不能外推到未发布数据或Hollywood媒体，因此不满足第二主集门。
- `[snapshot 2026-07-14, src=EmoVerse官方HF数据卡]` EmoVerse虽标CC BY-NC 4.0并称234,189图像，但核心标注由Gemini/GPT-4o/EmoViT/Critic Agent生成，只有约10,000样本接受人工检查；媒体混合公开集、网页URL和AIGC，且HF当前公开文件总量仅11.8kB。它不是多人类反应金标，不得替代第二人工主集。
- EmoVid官方页提供Google表单数据入口，但公开说明聚焦艺术媒体的emotion label、视觉属性和caption，没有逐内容多人观众反应分布证据；电影片段权利和数据许可也未在项目页明确，暂不进入主集候选。
- 首轮宽检索仍以LIRIS-ACCEDE为最接近的合法视听诱发情感集，但其公开输出为VA秩且受EULA邮件门约束；“媒体合法”与“主指标标签适配”是两个独立条件，不能只解决前者就放行。
- `[snapshot 2026-07-14, src=NeurIPS 2022官方论文页/论文]` Video Cognitive Empathy（VCE）是当前新发现中标签最匹配者：约60,000个视频、27类观众自身被诱发情绪，每视频平均13名MTurk人工标注（最少12、最多15），目标为反应分布。需要继续核官方数据入口、媒体来源、license、固定revision、包体量和group字段；这些未知关闭前不能判`FIT`。
- System1广告观众情绪集有超过30,000广告、平均约75名观众，并声称公开26,637个5秒片段子集；但论文同时明确底层数据来自System1专有方法，数据可用性是“non-commercial access”，模型权重公开不等于媒体/标签公开许可。当前只作为受限候选，不优先于VCE。
- Video2Reaction任务与本项目几乎同形且规模10,348片段，但标签由多阶段开源LLM从评论生成，只有人工验证，不是多人类反应金标；底层Movieclips/YouTube媒体仍要求使用者自行核源许可。因此只能是SILVER/最相近前作，不能补G1第二人工主集。
- Cowen/Keltner类高维视频诱发情绪资源具有逐视频多人反应比例，但需进一步核其刺激视频的公开许可和可再分发/可复现入口；仅论文描述不能当数据准入。
- `[snapshot 2026-07-14, src=VCE NeurIPS官方supplement]` VCE确有400名合格MTurk标注者，明确要求选择“视频使你自己感到”的27类情绪并给1—10强度；它在构念和分布真值上优于既有短名单。
- 同一官方supplement也给出致命媒体边界：视频由学生从Reddit和Instagram抓取，部分可能受版权保护；作者不为视频提供正式许可，而以美国Fair Use §107作为非商业学术研究依据。annotations为CC BY-SA 4.0、代码MIT，但不能覆盖视频。对本项目所在地和论文可复现要求，Fair Use主张不能自动等于明确合法媒体许可。
- VCE视频来源可用于source/hashtag级分组设计，且标注时无音频（依赖音频者标invalid）；这意味着它不是本项目希望的视听多模态输入。即使找到下载入口，媒体权利与无音频两项仍需00判断，当前不得冻结为第二多模态主集。
- `[snapshot 2026-07-14, src=OASIS官方论文/OSF入口]` OASIS包含900张开放图像，总计822名MTurk参与者；每图分别约101—108个valence评分和100—104个arousal评分，具有高密度多人类规范数据。论文说明图像主要来自Pixabay/Wikipedia，并在收集时限定为允许修改和再分发的素材，因此媒体权利证据明显强于Emotion6/VCE。
- OASIS主实验最终使用“图像自身的valence/arousal”指令，而非观众自身诱发状态指令；论文只明确发布逐图均值与标准差，尚未证明公开包含逐标注者原始评分。因此它可作为VA规范集候选，但当前不能证明能构造CSMV同形的经验离散分布，也不是视听多模态第二主集。
- OASIS的OSF网页在当前只读工具中返回HTTP 403；这不是许可否定，但阻止了对当前文件树、显式license、revision、包体量和原始评分字段的独立核验。未下载、未绕过访问限制，状态保持`PENDING_ACCESS_AND_LABEL_GRANULARITY`。
- LAI-GAI官方项目页可访问，属于AI生成情感图像的人类评价资源；下一步只核官方页面所列样本数、参与者、评分层级、许可、文件入口及是否提供逐人评分，不在元数据门前下载数据。
- `[snapshot 2026-07-14, src=LAI-GAI官方项目页/论文页/下载页]` LAI-GAI v05（2026-03）公开847张带生成元数据的AI图像、12个目标情感状态、六项研究、58个国家和2400余名参与者，并称问卷统一覆盖18项离散及维度情感量表。官方入口提供按研究分组的图像、prompts、CSV汇总和文档，构念与媒体可追溯性比自然网络图像候选更有潜力。
- 当前官网用语是“participant ratings”和“CSV summaries/rating stats”，尚未证明发布逐参与者响应或每图经验分布；公开页也未显示明确license文本、文件大小、hash或固定split。它仍是单图而非视听数据，且目标情感由生成prompt预设，需防止用prompt/目标类别形成标签捷径。故当前状态为`PROMISING_BUT_NOT_FIT_PENDING_LICENSE_RAW_RATINGS_AND_SCOPE_DECISION`，不能直接解除G1。
- `[snapshot 2026-07-14, src=LAI-GAI官方论文v05]` 论文明确声明847张图在六项研究中由N=2470参与者验证，测量的是图像实际诱发的主观反应；847张中544张（64%）的最高真人评分与预设目标情感一致，说明不能把生成prompt当作真值替代人工评分。
- 论文明确称OSF发布了所有图像的raw data、均值和标准差，并获得Open Data/Open Materials/Preregistration badges；这关闭了“只有汇总统计”的主要疑点，理论上可从逐人反应构造经验分布。项目稳定指针为OSF DOI `10.17605/OSF.IO/V8DKM`，分析数据组件为`10.17605/OSF.IO/8P572`，图像组件为`10.17605/OSF.IO/K8XVH`。
- 论文正文自身为CC BY-NC 4.0，但这只直接覆盖文章；图像、raw data和代码各自的OSF license仍需逐组件核验，不能把文章许可外推到数据资产。LAI-GAI因此从“未知标签粒度”升级为`PROMISING_PENDING_ASSET_LICENSE_SIZE_AND_SCOPE_APPROVAL`，但仍不能在未获总纲/00范围批准时把单图集替换成第二视听主集。
- OSF公开页面可定位三个稳定组件，但当前网页读取器对OSF页面返回空正文，并拒绝直接打开`api.osf.io`元数据URL；搜索引擎也未索引这些API节点。该工具限制不能被误记为资产不可用，亦不能据此补写未知的license、size、hash或revision字段；下一步只能在“不下载数据”的边界内用公开HTTP元数据请求核验，或先向00回报并申请小型元数据包授权。
- CSMV官方`CSMV_rawLinks.xlsx`可绕过损坏theme，以Strict OOXML直接读取8210个数据行。行ID均唯一、无缺ID/URL，且与正式8210个视频ID集合完全相等；此前“URL行级覆盖PENDING”已由可复现脚本关闭。
- 但逐行语义核验发现2644行的表内ID与TikTok URL路径视频ID不一致，200行完整URL重复、URL路径ID重复202行。URL路径中的ID全部属于正式集合，但错配/重复说明表内链接存在置换或复用，不能用于批量恢复媒体或语义近重复审计；状态必须是`BLOCKED_UPSTREAM_LINK_MISMATCH`而不是PASS。
- 当前精确多模态候选仍无一同时满足明确媒体许可、固定可复现输入、多人自身诱发分布和主指标适配。最可执行的止损方向是由00批准把LAI-GAI作为图像跨域第二人工主集；这保持人工分布与JS指标，但改变“第二多模态主集”范围，必须先修订SSOT/协议并核OSF逐资产许可。

## 2026-07-14 00范围变更与只读授权结论

- 用户批准路径1后，00以`SC-20260714-01`将总纲升级为v1.6：LAI-GAI仅作为第二人工跨域图像主集/缺失模态验证集候选，不能声称第二多模态视频复现。
- 构念`public-induced audience affect`、`HUMAN_GOLD`、T0和JS不变。生成prompt、目标生成情绪和模型标签不得替代人类真值；prompt默认只作provenance并排除主输入。
- LAI-GAI若缺同构评论/历史案例字段，H1/H2记`NOT_APPLICABLE_BY_DESIGN`；CSMV承担核心机制证据，LAI-GAI主要承担内容分布、跨域校准/OOD与H3边界。
- `AUTH-00-LAI-GAI-OSF-META-RO-20260714`仅允许核OSF三组件公开网页元数据。网页未展示的license/revision/size/hash必须记`UNKNOWN`，不得通过下载或API补算。
- G1/G2、`formal_split=false`和任务20禁令保持不变；CSMV 2644行ID—URL路径错配仍是独立开放风险。
- 任务10按授权完成公开网页审计后，三个OSF组件的asset license、revision、file tree/count/size、hash/checksum、gating和公开数据字典全部仍为`UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE`；00接受`NO_GO_PENDING_ASSET_METADATA`。
- 剩余路径都需要新权限。00未把API、下载、登录或作者联系默认为既有授权延伸；建议的5 MiB上限元数据专用OSF API只读GET必须先取得用户明确同意。
- 用户已明确批准上述最小扩展，授权编号`AUTH-00-LAI-GAI-OSF-API-META-RO-20260714`。该授权只改变元数据取得方式，不改变数据准入、G1/G2、formal split或任务20状态。
## 2026-07-14 — LAI-GAI OSF public-page metadata audit (path 1)

- 00 approved scope change `SC-20260714-01` and read-only authorization `AUTH-00-LAI-GAI-OSF-META-RO-20260714`; LAI-GAI v05 remains an audit candidate, not a frozen second primary dataset.
- Compliant public-page checks were limited to `https://osf.io/v8dkm/`, `https://osf.io/8p572/`, and `https://osf.io/k8xvh/`; no API, login, preview, stream, or asset download was used.
- The compliant reader obtained no usable component metadata from `V8DKM`, could not safely open `8P572`, and received HTTP 403 for `K8XVH`.
- Exact public web searches for all three node identifiers returned only generic OSF licensing/files/metadata documentation, not node-specific asset metadata.
- Therefore asset-level license/locator scope, revision/update timestamp, visible file tree/count/size, checksums, and public data dictionary remain `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE`. Generic OSF terms and help pages cannot substitute for an explicit asset-level license.
- Current admission verdict: `NO_GO_PENDING_ASSET_METADATA`; G1/G2 and `formal_split=false` are unchanged. Any metadata file or asset access requires a new written authorization.
## 2026-07-14 — LAI-GAI bounded OSF metadata API authorization

- User approval was recorded by 00 and authorization `AUTH-00-LAI-GAI-OSF-API-META-RO-20260714` is active.
- Allowed scope is anonymous sequential HTTPS GET to host `api.osf.io` for nodes `V8DKM`, `8P572`, `K8XVH`, their node/files endpoints, returned license/file-list/folder-child relations, and `links.next` metadata pagination only.
- Hard ceilings: at most 100 requests, at most 5 MiB cumulative response bodies, at least one second between requests, no concurrency.
- Forbidden: download/content/render/html/upload links, HEAD/Range, asset preview/content, login/Cookie/token, other nodes/services, score-table contents, label mapping, split, training, or task20.
- Raw JSON must remain under ignored `data/raw/lai-gai/osf-api-metadata/`; tracked outputs must exclude contributor/person/contact data and signed asset URLs.
- Even a successful metadata audit cannot freeze LAI-GAI or authorize asset download; it can only produce `FIT_FOR_NEXT_REVIEW` for 00.
- First collector execution ended after requests at tracked-manifest construction because Python `false` was used instead of `False`. Raw per-request metadata/responses were already preserved. Network collection must not be repeated; rebuild from the existing raw run offline.

## 2026-07-14 — LAI-GAI bounded OSF metadata API results

- Exactly 26 sequential anonymous GET requests were completed; all returned HTTP 200. Cumulative response bodies were 382,394 bytes, below the 5 MiB limit.
- `V8DKM`: public, CC BY 4.0, `osfstorage`, 9 files, 22,108,737 known bytes, 9/9 files with public checksum metadata.
- `8P572`: public, CC BY 4.0, `osfstorage`, 137 files, 1,122,196,956 known bytes, 137/137 files with public checksum metadata. No score-table content was read.
- `K8XVH`: public, CC BY 4.0, `osfstorage`, but its authorized file-list endpoint returned HTTP 200 with an empty `data` array. It therefore has 0 visible files, 0 visible bytes, and 0 checksums under the authorized metadata path.
- The K8XVH empty list was confirmed from the locally saved API metadata response shape (`data_count=0`); it is not a projection bug. It does not prove images do not exist elsewhere, and authorization forbids exploring other relationships or URL variants.
- Honest verdict remains `NO_GO_PENDING_ASSET_METADATA`, specifically pending the image component file tree/size/checksums. LAI-GAI cannot be frozen and no asset download is authorized.
- Boundary validation found one observed UTC request interval of 0.996519 seconds (request 2 to 3), 0.003481 seconds below the hard one-second minimum. No tolerance may hide this and network requests must not be repeated. Final verdict must also record API audit rate nonconformance.

## 2026-07-14 — 00 final review of LAI-GAI API audit

- Review `REVIEW-00-LAI-GAI-OSF-API-20260714` accepts the local artifacts and observations only as `OBSERVED_WITH_PROTOCOL_DEVIATION_NO_GATE_CREDIT`.
- Authorization is closed as `CLOSED_NONCONFORMING_NO_RERUN_AUTHORIZED`; no rerun, URL variants, other relations, scripts, downloads, mirrors, or author contact are authorized.
- The 0.996519-second interval receives no retroactive waiver, and K8XVH's empty authorized file list remains an independent admission blocker.
- LAI-GAI final status is `NO_GO_00_REVIEWED_NOT_FROZEN`; the failing specialist validator and the preparation gate's sole blocking check must remain unchanged.
- 00 review `REVIEW-00-LAI-GAI-OSF-API-20260714` accepts the 26 hashed responses and node matrix only as `OBSERVED_WITH_PROTOCOL_DEVIATION_NO_GATE_CREDIT`. The rate violation is not waived, and the empty `K8XVH` tree independently prevents asset fixation.
- The API authorization is closed without rerun. The failing specialized validator and preparation blocker remain intentional evidence; no tolerance or test removal is allowed to restore a green status.

## 2026-07-14 — 第二主集恢复：OASIS首轮官方证据

- 本轮不触碰已关闭的LAI-GAI分支；新候选为Open Affective Standardized Image Set（OASIS，Kurdi、Lozano、Banaji），官方论文DOI为`10.3758/s13428-016-0715-3`，当前OSF公开项目定位为`https://osf.io/6pnd7/`。
- 官方论文定义OASIS为900张开放图像的人工规范集，总参与者N=822；每图valence约101—108人、arousal约100—104人，均为1—7量表。它满足“每内容单元多人类评分”和图像跨域统计单位要求。
- 媒体权利证据优于既有网络视频候选：论文称646张主要来自Pixabay、172张来自Wikipedia，检索限定为允许修改和再分发的图像，并明确允许在在线/离线研究中免费复用和修改。该论文陈述仍需由当前资产级license/file tree/revision证据闭合，不能单独替代逐资产台账。
- 构念存在明确限制：预实验比较“图像本身评价”和“图像在我身上诱发的状态”后未发现显著差异，但主研究最终采用image-focused instructions；因此OASIS最多是`public-induced affect proxy with construct limitation`，不能无条件写成与CSMV同构的人群诱发离散情绪。
- 标签空间是主要风险：论文公开描述的随附表仅含逐图valence/arousal均值、标准差、样本量及性别分层；当前尚未证明公开逐参与者原始评分，也没有离散情绪分布。若资产只有汇总VA，不能伪造离散JS真值或为通过G1临时改变主指标。
- 当前裁定为`PROMISING_PENDING_CURRENT_ASSET_METADATA_AND_LABEL_GRANULARITY`，不是冻结。下一步只读核OSF当前节点的license、revision、文件树、size、checksum和评分文件字段说明；UNKNOWN不记为PASS。
- 精确公开检索确认OSF节点`6pnd7`的wiki入口仍可被索引，但搜索结果未展示文件名、体量、checksum或节点license。Codex网页读取器拒绝直接打开`api.osf.io/v2/nodes/6pnd7`及其`files`端点，属于工具安全限制，不得写成OASIS资产不存在或不可访问。
- 直接打开OSF项目根页得到空正文，文件页返回HTTP 403；精确文件名检索也没有找到可核的当前OSF文件树。当前公开网页证据只能确认项目定位与论文宣称的下载内容，仍不能关闭revision、asset-level license、size、checksum和raw-rating粒度。
- 作者当前网站搜索结果仍提供“VALENCE AND AROUSAL RATINGS”入口，但搜索摘要未证明该入口包含逐参与者评分；不得把“ratings”一词推断为raw judgments。

## 2026-07-14 — 第二主集恢复：SMID初筛

- Socio-Moral Image Database（SMID）公开记录声明2,941张可自由使用照片、2,716名参与者、820,525次个体判断，包含valence/arousal、moral wrongness和五类moral relevance；PLOS Figshare记录标为CC BY 4.0并指向OSF `2rqad`。
- 相比OASIS，SMID更可能同时满足开放媒体和“个体判断可形成经验分布”，但当前搜索摘要尚不能证明公开文件内保留逐人响应、当前图像包的逐资产来源许可、固定revision/hash及可用于JS的原始量表字段。
- SMID是社会/道德刺激集，affective VA只是其中一部分；若准入，构念必须限定为图像诱发的VA跨域代理，不能把moral wrongness或MFT标签当受众情绪真值或主输入。
- 当前裁定：`PROMISING_PENDING_OFFICIAL_PAPER_AND_FILE_LEVEL_AUDIT`。Figshare页面在当前读取器返回403，不等于资产不可用。
- 正确官方论文为PLOS ONE 2018，DOI`10.1371/journal.pone.0190954`。Study 2对2,941张图的八个维度均使用1—5量表；每图每维目标至少20人，平均34.88次评分，合计820,565次评分。valence锚点为unpleasant/negative→pleasant/positive，arousal为calming→exciting。
- 论文明确图像由Wikimedia Commons/Flickr URL收集，并通过平台API取得license/作者/标题元数据，只保留Creative Commons或同等宽松许可；排除名人、文字、水印/商标和非照片后形成2,941张最终集。当前Availability还声明发布每图URL、title、author、license，媒体权利链可逐图审计。
- 论文Availability列出的规范字段是均值、标准差、标准误和“rating frequencies”。结合正文用语，`rating frequency`主要指每图评分次数，而不一定是五个量表取值的直方图；在未看实际字段前不能据此宣称可构造5-bin经验分布或JS真值。
- 论文承认SMID并非主要为affective image set设计，但所有图均有VA规范；这支持跨域代理角色，同时要求把社会道德内容偏置作为OOD/构念限制登记。
- SMID现为首选候选，状态提升为`PREFERRED_PENDING_FILE_SCHEMA_LICENSE_REVISION_AND_DISTRIBUTION_LABEL_PROOF`；若实际文件只有mean/SD/N，则仍不能满足冻结的分布主指标。
- 当前公开搜索未索引SMID规范文件名；OSF项目根页可定位但正文为空，文件页被读取器判定不安全。与OASIS相同，这只是网页工具限制，不能替代文件级审计。
- PLOS Figshare记录公开显示一个约5.82 MB、CC BY 4.0的dataset bundle；其体量远小于2,941张图像总包，适合作为下载前候选元数据/补充材料，但在实际取得前不能假定其不含敏感字段、也不能假定它包含逐档频数。

## 2026-07-14 — 第二主集收口新授权与首轮在线核验

- 用户以“不管怎么样，把第二主集给我搞定了”明确授权将任务目标从只读审计提升为第二主集收口；新授权仍限定公开、免费、无需登录和合法入口，不包含付费、绕过gating、代签EULA或秘密镜像。
- `[snapshot 2026-07-14, src=LAI-GAI官方项目页]` 官方首页明确给出847张图像、12个目标情感、六个文化队列、2400+参与者评分，并提供`Dataset files`、OSF仓库、Data Card和公开样例浏览入口；这表明旧`K8XVH`空列表可能不是唯一官方资产入口，值得只针对官网明确链接继续定位。
- `[snapshot 2026-07-14, src=OASIS原论文/官方OSF]` 情感OASIS包含900张500×400彩色图像、N=822的valence/arousal人工规范；论文明确图像可免费用于线上/线下研究，原始规范文件包含图像ID、主题、类别、来源、VA均值/标准差和样本量。当前仍需核现行下载入口、文件树、hash及是否只有汇总规范而无逐人评分。
- 搜索结果中`oasis.cs.princeton.edu`是同名的单图3D表面数据集，不是本项目所需的Open Affective Standardized Image Set；后续必须使用论文、Harvard作者页和OSF `6PND7`作为身份锚，避免同名污染。
- `[snapshot 2026-07-14, src=LAI-GAI官网下载页]` 官网明确公开直链`/media/all_images.zip`，描述为完整分辨率、按研究分组的图像ZIP；这关闭了“图像只能从空OSF节点取得”的错误假设，K8XVH空文件树不再等同于核心输入不可获得。
- `[snapshot 2026-07-14, src=LAI-GAI图片详情页]` 单图详情页公开稳定UUID页面、文件名、目标情绪、生成prompt和评分概览；抽查首图显示`N=79`。官网浏览器总计847图，提供按研究、文化和情绪筛选，说明图像级评分样本量和provenance可按图审计。
- 官网ZIP直链由网页工具以“400 OK”形式报告二进制抓取错误，属于网页解析器不适合大文件，不代表资源HTTP失败；下一步使用本地串行HTTP头与受控下载核验真实状态、大小和SHA-256。
- 官网`all_images.zip`的HEAD请求在约31.6秒内未返回字节，而普通下载页/Data Card均HTTP 200；服务器可能未实现或不及时响应HEAD，不能据此判ZIP失效，后续改用受控GET并记录真实结果。
- 既有8P572元数据清单已包含完整评分资产线索：`S1_data.csv`至`S6_data.csv`、多份逐研究输出、`image_emotion_means_S123456.csv`、`SupplementaryData_30112025.xlsx`、`prompt_dict.csv`、`target_emotions.csv`和`1README.pdf`均有固定大小与OSF checksum。评分节点总计137文件、1,122,196,956 bytes；无需下载整节点，可只取README、最终逐图汇总、必要逐人原始CSV和prompt字典。
- Git忽略的既有OSF raw元数据保存了15页8P572文件列表，可离线恢复公开文件ID和下载关系，无需重复旧API请求。已定位12个最小候选文件：README、两份最终逐图汇总、六项研究原始CSV、SupplementaryData、prompt字典和目标情绪表，合计约27.18 MB。
- 12个目标均有OSF file ID、公开大小和SHA-256，可在下载后逐文件闭合；该最小集合足以先审计评分粒度、图像ID、prompt隔离和最终汇总，不需要下载382 MB `.RData`或整个1.12 GB评分节点。
- 12个最小评分文件已从OSF公开下载关系成功取得并逐文件通过官方SHA-256与字节数双重校验；合计27,838,544 bytes。原始文件位于Git忽略目录`data/raw/lai-gai/second-primary-resolution/20260714/`，未进入Git。
- 下载耗时约427秒但没有hash、HTTP或资源上限失败；慢速不影响固定性。后续不再重复下载这些文件，所有结构审计从本地只读副本执行。
- 六项研究原始表结构一致，各54列，共94,292条图像评分记录；每行含12个离散情感强度、6个维度/动机强度、`Image_name`、目标/provenance字段及参与者元数据。S1—S6分别含193/145/241/121/103/146个主图像，参与者数620/314/770/290/239/376。
- 原始表含`participantID`和`prolific_id`，属于不应进入Git或canonical的参与者标识；年龄、性别、国家、设备和完成日期也只用于偏差/质量聚合，不进入T0模型输入。raw目录隔离是必要的，不得公开逐行表。
- 12项离散情感字段为`Amusement/Awe/Anger/Attachment_love/Craving/Disgust/Excitement/Fear/Joy/Neutral/Nurturant_love/Sadness`，可形成逐参与者响应向量；最终汇总表提供每图均值、标准差和`n`，满足构造带样本量不确定性的群体响应轮廓所需字段。
- 最终汇总有944行，带描述版943行，超过官网847图；这意味着必须用`is_ai`、研究使用状态和实际ZIP文件集合做交集，不能直接把汇总所有行当第二主集。
- `SupplementaryData_30112025.xlsx`含生成、文化、性别、年龄适配图的文件名、来源、AI模型、prompt和研究使用字段；这些是分组/近重复/provenance依据，但prompt和目标情绪不得进入主模型输入或替代人工真值。
- 首次结构画像在数据读完后的终端JSON输出因GBK无法编码Unicode列名而exit 1；固定`PYTHONIOENCODING=utf-8`后只读重跑成功，没有修改源文件。
- 在AI图像且`useData`严格等于`Yes`的保守口径下，得到60,562条有效评分、802张图、1,492个去重参与者ID；每图58–96人（中位75），每图51–94条完整12维评分且没有零完整评分图像，规模与密度足以作为第二人工图像主集。
- 94,292条原始记录全部`consent=YES`，但`useData`存在Yes 92,388、No 1,174、空692和`Sim.` 38。`Sim.`语义上可能是葡萄牙语“是”，空值可能来自未设置该题的批次，但在预处理脚本确认前不能自行纳入；当前802图是保守下限。
- 847个AI图与97个原始比较图在最终944图汇总中通过`is_ai`明确区分；97个比较图不进入第二集。最终主集只消费AI图，保留比较图为审计provenance但不进入正式split。
- `1README.pdf`只有1页文本层，列出原始数据、清洗notebook、建模文件和输出文件关系，确认`S1_data.csv`—`S6_data.csv`属于预处理输出。README没有解释`useData`编码；需要读取`AIPS_preprocv3_all.ipynb`的实际过滤逻辑。
- 系统无Poppler，README通过`pypdf`完整提取1/1页文本；本次判断不依赖视觉排版，视觉通道未覆盖并明确记为未审。
- `[snapshot 2026-07-14, src=LAI-GAI官方首页与下载页]` 官网首页与`/download/`均返回HTTP 200；下载页直接列出官方OSF项目和`/media/all_images.zip`，不是第三方镜像或猜测链接。`/data-card`为错误路径，官网实际入口是`/datacard/`，后续仅使用页面明确链接。
- `[local audit 2026-07-14, src=已取得的LAI-GAI评分CSV]` 六项研究原始表具有一致的54列结构，含独立人工评分的12个离散情绪强度、VA/动机维度、`Image_name`、研究/参与者标识及同意/可用性字段；最终逐图汇总表含12维均值/标准差、`n`与provenance。原始参与者标识和人口统计只留Git忽略目录，tracked canonical不得携带。
- `[snapshot 2026-07-14, src=LAI-GAI /datacard/]` 官网Data Card页返回HTTP 200，并以内嵌官方静态资产`/media/laigai_data_card.html`展示导出的Data Card；页面摘要明确12种情感状态与跨文化标准化人工评分。该入口可用于冻结字段与使用边界，但具体许可仍须从正文/仓库许可关系交叉核验。
- `[snapshot 2026-07-14, src=LAI-GAI官方Data Card静态正文]` Data Card明确847图、6项研究、N=2470/58国、每图18个1–7人工评分维度；图像和元数据均标注CC BY 4.0，开放访问，OSF提供版本记录。Data Card同时声明原始参与者文件匿名化；本项目仍只发布聚合标签，不跟踪原始逐人记录。
- `[snapshot 2026-07-14, src=LAI-GAI官方图片浏览器]` `/images/`返回HTTP 200并直接列出详情UUID与同源`/media/images/...jpg`；`per_page=100`一次可公开列出100个图像资产。由此可在完整ZIP过慢时改用官网明确列出的逐图资产，仍保持官方来源、无需登录和逐图固定文件名/内容hash。
- `[local audit 2026-07-14]` 847张最终AI清单均在六项研究原始CSV中有合规人工评分；按`consent=YES`、`useData=Yes`、`rating_cat=0`过滤后共63,682个逐图反应，每图58–96人、均值75.19，图像—参与者重复0。原始`is_AI`在49张最终AI图上误记0，同时有4张相反偏差，因此纳入清单必须以最终逐图汇总的`is_ai=True`为准并保留冲突审计。
- `[final local gate 2026-07-14]` 官网图片浏览器的847个同源静态媒体与最终847评分清单双向闭合；逐图解码、size、SHA-256和dHash均已固定。12项评分文件与既有OSF公开size/SHA-256全部一致。
- `[final local gate 2026-07-14]` source item/变体/同prompt/精确与dHash近重复合并后得到379个group；确定性split为train/dev/test=594/127/126，三份均覆盖12个目标类别，group、精确重复和近重复跨split均0。
- 标签构念门通过：63682个人工诱发反应生成12维连续分布，并保留每维N/SD/SE/1—7直方图；prompt、目标类别、raw `is_AI`和生成来源仅作provenance。LAI-GAI可作为批准的跨域图像/缺失模态第二主集冻结候选，但正式G1/G2仍须00签署。
## 2026-07-14 LAI-GAI 官方预处理逻辑核验（阶段17续）

- 已从既有公开 OSF 文件清单定位并下载 `AIPS_preprocv3_all.ipynb`；本地文件 864,040 bytes，SHA-256 为 `d55034d5736b241d34af2a46bb57501d0dc8a4287e733fd5d70fcd92f3b9a7a1`，与公开清单记录一致。
- Notebook 显示官方汇总流程按 `image_name` 聚合 12 个离散情绪维度与维度评分的 mean/std，并以去重参与者数形成 `n`；六项研究合并前会偏移内部参与者编号，避免研究间编号碰撞。
- `is_ai` 是按文件名规则判定；prompt 只在 AI 图像上合并为生成来源信息。由此确认 prompt 是 provenance，不是 HUMAN_GOLD，也不得进入 T0 模型输入。
- 当前尚未从该总 Notebook 的长输出中闭合 `useData` 的筛选语义；下一步仅抽取其相邻代码行，必要时再读取分研究预处理 Notebook，不凭字段字面自行扩收样本。
## 2026-07-14 LAI-GAI 清洗与图像包核验（阶段17续）

- 六个分研究 Notebook 均实现同一准则：注意力题 18 项中至少 17 项为 7 才通过宽松检查；`useData` 规范化为 `no` 时剔除；另剔除内部试测编号与未满 18 岁者。`Sim.` 和空值不会仅因字面值被判为拒绝，但所有记录的独立 `consent` 字段均为 `YES`。
- 已取得并按公开 SHA-256 验证 `S1_data_out.csv` 至 `S6_data_out.csv`。官方清洗输出共 89,242 行、1,468 名去重内部参与者编号；宽松注意力门全部通过，拒绝使用值为 0，最低年龄 18。
- 正式图片评分行限定 `rating_cat=0 && is_AI=1` 后为 58,432 行、802 张唯一 AI 图片、每图 54--93 条评分；12 情绪完整向量为 55,541 行、每图 49--92 条。六项研究的图片集合互不交叉。
- 官网页面列出的 847 张 AI 图是资产全集；只有其中 802 张出现在合格正式人工评分中。因此 canonical 只允许 802 张，另 45 张记为“有图无合格 HUMAN_GOLD，不准入”。
- 官方 ZIP 确认总长约 226.2 MiB，但单连接平均仅约 11 KiB/s并在续传约 22 分钟后失败；局部 ZIP 不是完整资产、不得解压或用作准入证据。改用官网图片详情页逐图官方地址。
- 官网9个分页直接给出原始文件名、详情UUID与实际 `/media/images/` 路径；逐图取得后共847个JPEG、86,947,800 bytes，全部RGB且Pillow解码零失败。官网列表、本地图像、下载映射和官方汇总表四方文件名集合847/847一致。
- 先前“802张有合格评分”的判断只覆盖六个 `S*_data_out.csv` 中间文件，漏掉后续S3b/文化变体合并，并含4个被中间`is_AI`误标的原始比较图。最终权威 `image_emotion_means_S123456.csv` 以文件名规则重算AI状态：847张AI图全部有完整12维均值、`n=54--93`且目标/研究字段无缺失，因此正式样本应为847而非802。

## 2026-07-15 — 00正式冻结结论

- `REVIEW-00-LAI-GAI-FREEZE-20260715`已批准LAI-GAI为第二人工跨域图像主集，状态只能是`FROZEN_00_APPROVED`；待复审候选状态不再满足当前专项门。
- 唯一权威数据合同为847图、63,682条合规人工响应、2,557个study-scoped参与者、379组、train/dev/test=`594/127/126`，canonical SHA-256=`ad58c268e34adf02bd8e639338069d34576e1d9602f819a2cc6fa89be6836818`。
- LAI-GAI专项正式split为`formal_split=true`；dataset-v1全局仍为`formal_split=false`。两者分别表示第二主集本身已冻结，以及CSMV媒体lineage尚未达到G2，不构成矛盾。
- G1=`PASS`；G2=`BLOCKED_CSMV_MEDIA_MAPPING_AND_GLOBAL_SEMANTIC_AUDITS`。下一阻塞是CSMV 2,644行ID—路径错配、200行重复URL及剩余全局语义审计，不再是第二主集。
- 旧OSF API验证器仍因0.996519秒间隔返回exit 1，原始失败完整保留为`HISTORICAL_NONCONFORMING_NO_GATE_CREDIT`；综合准备门只将其作为历史证据嵌入，不再把已关闭授权当作当前G门阻塞。

## 2026-07-15 — CSMV媒体lineage语义纠正与同源split

- `[local fixed-commit audit]` `CSMV_rawLinks.xlsx`的`ID`是CSMV内部`video_file_id`，URL路径末尾是TikTok平台源视频ID；官方README只声明该工作簿提供raw web link，没有声明两类ID必须相等。此前2,644行“不相等”是跨命名空间误判，不是上游映射置换证据。
- 8,210条内部ID→URL映射覆盖正式视频集合100%，形成8,008个平台源视频族；202个族各含2个内部样本，共404条。完整URL重复200行与路径ID重复202行是many-to-one同源关系，必须作为group约束处理。
- 修复前按内部ID散列导致100个源族跨`group_by_video_v1`；仅按hashtag分量划分又导致115个源族跨`hashtag_heldout_v1`。修复后源族先合并、再合并hashtag分量，两协议源族交叉均为0。
- 新`csmv-media-lineage-v1.manifest.json`逐项保存item hash、source-group hash、URL hash与split，不保存原始URL或平台ID；专项负面夹具强制跨split时可检测。
- 本结论关闭官方URL元数据范围内的媒体lineage和同源泄漏，不外推原始媒体拥有权、再分发权、内容指纹近重复、发布者或时间协议。
- G2从CSMV本地阻塞转为`PENDING_00_G2_REVIEW_CSMV_LINEAGE_CLOSED`；任务10不自行批准G2，`formal_split=false`和任务20禁令等待00书面复审。

## 2026-07-15 — 00对CSMV lineage/G2的独立裁定

- 00复跑确认：普通与`-I -S`专项均为8210 records、8008 source groups、202 duplicate groups、404 rows、cross-split=0、negative fixture detected；全局泄漏门Critical=0，负面selftest正确阻断。
- “内部ID必须等于URL路径ID”没有官方依据；8210内部键100%覆盖和README对`video_file_id`/raw web link的不同角色支持命名空间纠正。该旧阻塞正式关闭。
- G2没有因此自动通过。CSMV正式模型输入仍没有资产级license、revision、file tree、size/hash或本地8210覆盖；URL metadata只能支撑分组，不能替代输入字节。
- 旧`reproducibility-v1`是source-family修复前的成功记录。00现场重算发现18项中9项hash漂移；release validator此前只信任manifest自报字段，未核当前文件，这是确定的验证缺口。
- 最终裁定：`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_REPRODUCIBILITY_STALE`。最小恢复路线是先只读预审一个官方特征族，再以公共benchmark核心模式隔离重建并现场核hash；不需要让CUC银标源阻塞公开主线。

## 2026-07-15 — CSMV官方特征页预审与当前复现结果

- `[fixed official README]` 上游`IEIT-AGI/MSA-CRVI@99d14240254b1381dde0b9c56add140381f65117`明确：视觉特征按24fps帧、16帧窗口/步长提取，最大时序长度180；每个微视频为一个按`video_file_id`命名的`.npy`。README称当前已发布I3D与VideoMAE，示意树另写VideoMAEv2并列出R(2+1)D。
- `[anonymous public page observation 2026-07-15]` README链接的Google Drive公开folder匿名GET返回HTTP 200、最终host严格为`drive.google.com`；授权范围内取得的初始HTML未出现I3D、VideoMAE、R(2+1)D或`.npy`资产名，也未公开文件列表/体量/checksum。页面响应为动态内容，单次响应hash不能充当资产revision。
- README License段只明确代码MIT与annotations CC BY-SA 4.0；仓库根LICENSE又为Apache-2.0。没有文本把视觉特征明确纳入annotations许可，因此特征资产许可继续为`UNKNOWN_NOT_EXPLICITLY_COVERED`，不能因公开可达推断可用于正式模型。
- 公开元数据不能验证8210个`video_file_id`实际覆盖，也不能计算最小特征族空间。当前合理裁定是`NO_GO_PENDING_ASSET_METADATA_AND_LICENSE`，不是选择I3D或VideoMAE后直接下载。
- `[local isolated replay]` 新公共核心模式从冻结CSMV raw manifest重建8210条canonical、8008源族约束、video split 5698/837/1675、hashtag split 7211/327/672、泄漏manifest与release；CUC只核验冻结canonical/review字节，不读取历史外部源根。
- 重放在Python 3.8.9 `-I -S`下两条命令均exit 0；检查旧18项并新增`csmv-media-lineage-v1.manifest.json`，共19项before/after hash一致、现场漂移0。release validator已改为逐项重算，后续任何漂移会fail-closed。

## 2026-07-15 — 00对CSMV特征预审与G2的最终复审

- 00独立执行`reproduce_m2_minimal.py --public-core`，确认19项before/after SHA-256一致、`mismatches=[]`、两条隔离子命令returncode均0、凭证环境未转发；`REPRODUCIBILITY_STALE`子阻塞正式关闭。
- `validate_m2_release.py`现场重算19项hash为零漂移；泄漏live门Critical=0，负面selftest正确输出`LEAKAGE_BLOCKED`。
- 特征专项exit 0只表示No-Go合同真实，实际`g2_asset_ready=false`；许可、revision、文件树/bytes/checksum、schema和8210实际覆盖仍UNKNOWN。
- 正式G2状态收敛为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；全局`formal_split=false`、任务20禁令不变。
- 已授权针对一个特征族（优先I3D）进行最小权利方元数据协调：一次请求、一次跟进、最多5 MiB纯元数据；不授权Drive API、EULA、`.npy`或媒体下载。
## 2026-07-15 — CSMV I3D 官方协调渠道事实

- `[official repository observation]` `IEIT-AGI/MSA-CRVI` README 公开邀请数据集问题联系项目方，仓库启用 Issues，故选定公开 GitHub Issue 为授权内的单一官方联系渠道。
- `[connector write attempt]` 当前 GitHub 集成可以读取/检索该仓库，但创建 Issue 返回 HTTP 403 `Resource not accessible by integration`；没有返回 issue number/URL，因此没有发生外部写入。
- 该权限失败不能转化为许可、revision、manifest、schema 或 8,210 覆盖证据；G2 资产门继续 fail-closed。

## 2026-07-15 — CSMV官方Issue #5现场核验

- `[public official issue observation]` `https://github.com/IEIT-AGI/MSA-CRVI/issues/5`位于官方仓库，状态为Open，创建日期为2026-07-15。
- Issue正文公开请求资产级研究许可、固定revision、relative filename/bytes/SHA-256 manifest、8,210个正式`video_file_id`覆盖、提取器/版本、dtype/shape与总体量，并声明独立复审前不下载特征内容。
- 该事实只关闭“尚未成功联系”的协调子状态；在权利方实质回复并经00复审前，所有资产准入UNKNOWN和G2阻塞保持不变。

## 2026-07-15 — CSMV GitHub直接克隆内容边界

- `[official git clone]` `https://github.com/IEIT-AGI/MSA-CRVI.git`可在约20秒内完成main分支浅克隆，HEAD固定为`99d14240254b1381dde0b9c56add140381f65117`。
- `[git object audit]` canonical提交共10文件、14,436,790 bytes，与既有固定raw快照逐文件完全一致；`.npy`数量0、Git LFS pointer数量0。
- `[Windows checkout boundary]` 8个文本工作树文件因本机Git LF→CRLF转换而改变SHA-256；canonical Git blob与既有raw快照无漂移，不能使用转换后的工作树hash替代原始fixity。
- GitHub仓库可下载不等于外部Drive特征可下载或已获许可；G2资产准入UNKNOWN不变。
- `[00 independent review]` 正式请求额度已使用，2026-07-22前不得跟进。公开正文没有逐字点名I3D；这不使请求越界，但不能写成维护者已收到明确I3D限定，必要的唯一一次跟进应在同一Issue澄清。

## 2026-07-15 — 效率优先取得范围更新

- 用户允许可信第三方镜像和更广的公开资产下载；项目内部取得授权不再等同于只读官方页面或已完成准入的小包。
- 为兼顾效率与证据诚实，许可未知的公开资产可先进入Git忽略隔离区并完成hash/格式/覆盖审计；第三方法律许可本身不能由项目扩大。
- 镜像若无官方checksum，只能先作为隔离审计材料；须保留发布者、revision/获取时间、体量、本地SHA-256和尽可能的第二来源交叉核验。
- CSMV候选特征可在Issue #5等待期并行取得，但只有许可、fixity、schema与8210覆盖闭合后才能用于正式模型。

## 2026-07-15 — CSMV I3D本地包身份、覆盖与schema发现

- `[local quarantine audit]` 用户提供目录含9,942个`.npy`而不是截图中的多特征族层级；项目将其接到`visual_feature/I3D`稳定入口，未移动或复制源文件。
- `[coverage]` 从固定官方`video_to_comment.json`提取8,210个`video_file_id`后与文件名比较：命中8,210、缺失0、额外1,732。额外文件不自动进入当前CSMV标签集。
- `[schema]` 9,942个NumPy header全部可由`allow_pickle=False`读取，dtype全为`float32`、shape全为`(T,1024)`，时间步6—1,719。该布局与I3D兼容，但shape本身不证明权利方身份或提取器版本。
- `[partial sidecar]` `feature_shapes.json`只有646个键；646个均有文件且声明时间长度与header一致，但不能作为全包文件树。完整schema结论来自逐文件header审计。
- `[fixity]` 8,210个必需文件已有逐文件SHA-256；全包内容树SHA-256=`35be2d18e1d2413ba3765034cdb454baa5e3496d49c540c9be00e81bbc2c1942`。这是本地内容revision，不等同官方稳定revision。
- `[gate boundary]` 本地文件树/体量/schema/fixity/覆盖已形成00复审证据；特征资产许可、稳定官方revision和权利方attestation仍UNKNOWN，故只可`QUARANTINE_ACQUIRED`，不可正式训练、发布或取得G2信用。
- `[publication feasibility]` NeurIPS 2024正式论文明确以预训练I3D/R(2+1)D/VideoMAEv2特征替代原始视频发布，并在主实验、消融和YouTube外测中使用I3D。因此“不拥有原始mp4”不是开展同类下游模型实验的科学性阻塞；结论必须限定为冻结视觉表征上的预测/融合方法，不能声称端到端视频编码或原始帧学习。
- `[license evidence tension]` 正式论文第3.4节称代码与数据按CC BY-NC-SA 4.0供学术非商业使用；仓库README则写代码MIT、annotations CC BY-SA 4.0，未逐字绑定visual features。论文证据显著增强学术实验可用性，但许可表述差异仍须00/权利方裁定后才可放行再分发与最终G2。
- `[sequence protocol critical]` README描述最大tensor长度180；8210个必需I3D文件现场为T=6—1719，其中531个T>180（中位43、P90=133、P95=211、P99=339）。训练前必须冻结full-sequence+mask或确定性180步处理规则并做敏感性分析，禁止依据test结果选择。

## 2026-07-16 — 音频可发表性与缺失模态证据边界

- `[venue scope]` T-AFFC General CFP把视觉、语音、多模态、群体情绪和预测性情感模型列为并列范围，未规定每篇稿件必须含音频；这只支持“无音频不自动失格”，不构成录用保证。
- `[upstream asset fact]` CSMV固定README明确当前发布视觉特征、I3D/VideoMAE已发布、音频未来补充；因此音频属于上游结构性不可得，而非项目随机删除。
- `[decision]` `REVIEW-00-AUDIO-MODALITY-PROTOCOL-20260716`将音频冻结为`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`并移出G2、任务20启动和后续取得关键路径；I3D资产准入阻塞不变。
- `[claim boundary]` 视觉I3D加训练期评论特权监督可以构成跨模态学习设置，但评论不是T0学生推理输入，不能写成完整音视频/文本推理输入。
- `[experimental eligibility]` E1/E5/H3的逐模态增量和随机缺失只对同一样本至少两个实际T0输入模态的协议有效；CSMV—LAI-GAI的视频/图像跨域差异不能替代同一样本缺失模态鲁棒性。

## 2026-07-16 — I3D序列长度与预注册选择

- 8,210个必需I3D输入的长度分布为6—1,719；531个超过180、4个等于180，中位数43、P90/95/99为133/211/339。
- 完整序列最长单样本原始输入为7,041,024 bytes（约6.71 MiB），低于冻结的64 MiB batch原始输入张量门；当前资源画像不支持把主协议降级为180步。
- 前180步会对全部531个长序列系统性丢失尾段；确定性首尾覆盖均匀180步具有更好的时间覆盖，因此冻结为主敏感性，前180只作补充。
- 初始8项unittest按预期因`csmv_i3d_sequence_protocol`不存在而失败；实现后8/8通过。专项validator同时闭合重复hash、坏shape/空/非float32/非有限值、资源超限和test自适应拒绝。
- 该协议只关闭序列处理的发表/复现缺口，不关闭资产许可、revision或权利方包身份；维护者证据按用户指令延期。

## 2026-07-16 — 00序列协议复审发现

- `[independent fixity]` 协议manifest SHA-256为`208615d4059afc8c5c2c57a5ffc13eeafa9a71ece861332d9f1cd62bc9c4d5be`，其6个证据文件hash现场闭合。
- `[independent replay]` 8项单测、8个fail-closed负例、实时泄漏门、负面夹具、19项`-I -S`隔离重放和M2 release均通过，未发现任务10回交夸大。
- `[publication gate]` 协议未冻结风险已关闭；这使实验处理规则可预注册、可复现，但不提供资产权利或官方身份信用。
- `[git hygiene]` 审核基线与`origin/main`一致；tracked `.npy`、特征包和超过10 MiB文件均为0。第一次枚举因Git非ASCII路径引号转义报错，使用`core.quotepath=false`后有效重跑。
