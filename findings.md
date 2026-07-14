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
