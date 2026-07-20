# T-AFFC CARM项目全程复盘与当前状态

> 快照日期：2026-07-20（Asia/Shanghai）  
> 当前总纲：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.16  
> 当前远端主线：`main@6534a0834f793426afc4aa2a97da697f1825ea66`  
> 说明：本报告区分已验证事实、已接受限制、当前失败和后续计划；聊天与交接卡不能替代实时Git、门报告和实验台账。

## 一、项目现在处于什么位置

项目已完成“研究问题重构—数据/协议地基—统一评测与强基线”三层基础建设，正式门状态为：

- `G1=PASS`；
- `G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`；
- `ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`；
- 总体G2=`PASS_WITH_ACCEPTED_ASSET_RISK`，`formal_split=true`；
- `G3=PASS_WITH_LIMITATIONS`；
- 任务50五种子、bootstrap、完整消融和结果冻结尚未完成；任务30、40、50、60尚未启动。

因此，当前准确定位是：**M1–M3科学地基已经建立，G3已通过；M4正式创新模型尚未启动；任务20正在进行一个永久NON_T0/INELIGIBLE的作者原设定补充探索，该探索不是G3主证据。**

截至本快照，A30上的VC-CSA探索训练已异常停止：DataLoader worker被系统以`Killed`终止，GPU已空闲；停止前尚未完成首个epoch。日志中约0.36的总loss只能用于排障，不能作为实验结果。

## 二、项目为什么要重做

项目最初继承了毕业论文第四章的“历史相似案例检索 + 48维特征 + CatBoost二分类”路线，但审计发现旧证据不足以直接升级为T-AFFC论文：

1. 论文中的2815条与当前可加载2787条不一致，另有221条向量标签与标签表冲突。
2. 旧随机划分存在严重发布者重叠，195条LLM/Temporal子集只有4个发布者、9个话题，所谓时间划分实际没有有效时间戳。
3. 目标视频未来评论既参与标签，又被BERT/LLM当作输入，若声称发布时预测则构成直接泄漏。
4. 旧GNN在划分前构全图，属于传导式设置，且属于第三章传播链而非本项目主线。
5. 旧论文中部分表格与文字提升幅度互相矛盾，CatBoost 90.07%也未能按当前材料可信复现。

因此项目没有继续“换一个深度模型刷分”，而是把研究问题改造成：在目标内容发布时，只使用当时合法可见的内容证据，预测未来公众评论所体现的群体情绪分布，并在检索不可靠、话题/平台变化或输入缺失时给出可校准的不确定性或拒绝判断。

工作模型暂名CARM：`Calibrated Audience-Response Memory`。

## 三、整体研究思路

项目按“协议先于模型、证据先于主张、开发与正式统计分层”的思路推进。

### 1. C1：先建立无泄漏T0预测协议

冻结研究对象为`public-induced audience affect`，即一条内容发布后，多位受众在评论中表达的情绪反应分布。它不同于说话者自身情绪、画面中多人的群体情绪和传播链指标。

主任务为T0内容预测：推理时不能读取目标内容的未来评论、未来互动量、推荐结果或任何由未来反馈构造的信息。评论可以在训练阶段承担人工标签来源或特权监督，但不能进入T0学生模型的推理输入。

### 2. C2：评论特权教师与内容学生

后续任务30将只在训练阶段让teacher读取训练评论，学习更细的受众反应分布；student在训练和推理时始终只读取T0内容。重点不是加入更多模块，而是验证评论特权监督是否能稳定改善分布预测与校准。

### 3. C2后半：train-only受众反应记忆

任务40计划从训练集历史案例中构建可审计的反应记忆，检索相似内容及其历史受众分布；索引必须train-only，不能用dev/test评论或未来信息。模型还要判断“检索到的历史是否可信”，不可信时减少依赖或拒绝预测。

### 4. C3：跨域与可靠性证据

CSMV承担社交视频主协议和评论聚合主证据；LAI-GAI承担跨域单图像、校准和OOD边界验证。二者统计单位不同，不伪装成两个同构多模态视频集。中文自建数据只作无金标/银标压力测试，不能冒充独立人工测试金标。

### 5. 分阶段证据等级

- L0：只能证明能跑，不能进下游门；
- L1：输入、环境、配置、种子和输出可内部复现；
- L2：协议、强基线、公平预算、统计与限制完整，可成为论文候选证据；
- L3：结果、代码、数据说明、图表和claim-evidence全部冻结，可投稿。

## 四、从开始到现在具体做了什么

### 阶段A：开工、旧资产盘点与研究问题冻结（2026-07-13至07-14）

- 建立总纲、工作记录政策、环境锁、Git/敏感文件边界和claim-evidence入口。
- 盘点旧代码、旧数据和旧报告，将其分为可复用代码、历史基线、探索结果和禁止进入新论文证据四类。
- 冻结T0、构念、主指标、失败条件和泄漏威胁模型。
- 完成四路贡献级查新，并把创新上限收敛为无泄漏协议、评论特权监督/反应记忆和跨域可靠性三条。
- 第一轮G1/G2未通过时没有越门训练，而是保留`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`并继续数据补证。

### 阶段B：第二人工集与数据工程闭合（2026-07-14至07-16）

- 审计iNews、NEmo+、LIRIS-ACCEDE等候选，最终按用户批准路径将第二集调整为跨域图像人工验证集。
- 冻结LAI-GAI v05：847张图、63,682条合规人工响应、379组，split为594/127/126。
- 纠正CSMV内部ID与平台ID的命名空间，识别8008个源族和202个重复源视频族，执行“先归并同源、后划分”，消除跨split同源泄漏。
- 建立canonical schema、数据字典、原始manifest、dataset-v1、split-v1、label-provenance-v1、Data Card、Datasheet、隐私/平台条款和发布边界。
- 物理隔离`HUMAN_GOLD`、`SILVER`和`UNLABELED`；自动/LLM标签只能是SILVER，不能与公开人工test混用。
- 建立正负泄漏门和19项公共核心隔离重放；错误split、目标评论输入、索引非train-only、同源跨split等情况会fail closed。
- 冻结CSMV正式group-by-video split：train=5698、dev=837、test=1675；另有hashtag-heldout 7211/327/672。原生topic和可靠时间戳不可用，分别保留为BLOCKED/NOT_RELEASED，而非伪造。

### 阶段C：输入资产、音频和I3D协议（2026-07-15至07-17）

- 官方仓库审计确认特征资产不在Git；官方Issue #5已用于请求许可、revision、manifest/覆盖和schema说明。
- 用户提供的本地I3D包经隔离审计后，固定manifest覆盖8210项；文件级hash、schema和覆盖闭合，但许可、稳定官方revision、权利方包身份/fixity仍未得到外部确认。
- 音频冻结为`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`，移出关键路径；项目不再声称音视频融合、音频增益或音频缺失鲁棒性。
- I3D主协议冻结为完整`float32[T,1024]`序列、动态右补零和mask；主敏感性是确定性均匀180步。8210项中731项长度超过180，最长2719，因此不能把“取前180帧”冒充完整序列。
- 通过`SC-20260717-01`将G2拆成“科学协议/数据门”和“资产准入风险”。前者通过，后者由用户接受延期风险，从而只允许固定I3D包用于内部研究，不产生再分发或官方许可信用。

### 阶段D：范围治理与项目拆分（2026-07-16至07-17）

- 曾短暂设计IJCV与T-AFFC双路线，随后按用户决定将IJCV完整迁移至独立项目。
- 当前仓库从总纲v1.15起只执行T-AFFC CARM；J0–J2、JH1–JH3、任务25和任务65不再属于本项目。
- 旧长上下文总控迁移为独立00总控，建立`.light`账本、决策记录和跨会话交接链。

### 阶段E：任务20统一评测与基线（2026-07-17至07-18）

- 建立独立任务20环境锁、统一实验配置schema、run manifest、prediction schema、数据加载器和指标实现。
- 指标覆盖JSD、NLL、EMD、Macro-F1、Balanced Accuracy、Brier、ECE、ACE和AURC-JS。
- 实现最低基线、E0检查、错位sample/非归一化/泄漏split拒绝、train-only拟合与索引约束。
- 重跑原48维CatBoost/HGB/LightGBM，但明确标为`LEGACY_NATIVE_COMPATIBILITY`，不与CSMV八类分布任务作主表横比。
- 完成冻结I3D temporal-attention强基线的12-trial dev选择、一次性test评测和同环境同seed独立dev replay。
- replay未重跑test，只比较原run与replay的predictions、metrics、selection和trial_results；四项SHA-256逐字节一致，证明范围仅为`SAME_ENVIRONMENT_FIXED_SEED`。
- 形成`BASELINE_TABLE_V1.md`、G3证据包、22项tracked evidence的hash绑定HANDOFF和正式审计报告。
- 00独立复核后裁定`G3=PASS_WITH_LIMITATIONS`。

### 阶段F：VC-CSA作者实现补充审计与探索（2026-07-18至今）

- 起初官方main无模型代码，后定位到作者相关fork `JackySnake/MSA-CRVI@3e8c426...`，对应上游未合并PR #3；因此更正为“作者释放实现已定位，但未完成复现”。
- TDD修复其`en_vectors_web_lg`死依赖、RoBERTa路径、train.sh变量/续行、无效导入和未定义变量，并完成本地3070 Ti小样本GPU smoke。
- 修复smoke运行时输入构建器，确保所持久化标注和video-comment映射严格等于选中train∪dev，test物理排除；相关测试从红转绿。
- 新租用A6000完成48GB显存、依赖环境和batch16合成资源smoke，证明算力和模型显存可行。
- 随后发现作者随机comment split与同视频随机peer机制存在结构冲突：7854个video跨split；train/dev/test分别有122/2750/1573个split内singleton，它们的peer只能来自其他split。保留作者完整映射会让train读取dev/test评论或标签，物理隔离又会使singleton无法取peer。
- 用户明确接受该方法学泄漏风险后，探索身份永久固定为`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`，正式证据资格永久为`INELIGIBLE`。它不得进入T0、G3主证据、统一baseline、任务50或论文主张。
- 多个租用实例曾出现TCP/SSH握手失败；后续获完整执行授权并在A30启动seed=3407探索训练。
- 2026-07-20实时监控显示该训练因DataLoader worker被系统Killed而停止，尚未完成首个epoch；下一次恢复需降低`num_workers`并监控主机内存。

### 阶段G：私有备份与运行恢复能力（2026-07-19）

- 用户授权私有MatBox、私有对象存储、私有环境/卷快照和非敏感配置镜像。
- 已完成私有MatBox I3D备份：8210项、2,283,804,928字节；前后missing/extra/size/SHA mismatch均为空，内容树SHA-256为`592eb698...a925`。
- 目标目录0700 owner-only、文件0600；静态加密和平台控制面仍为UNKNOWN。
- 非敏感配置镜像已建立，只含依赖锁和Python版本记录。
- 运行时快照尚未创建，状态为`DEFERRED_NOT_STARTED`；须在安全暂停或训练完成时创建。受限材料保留至最小证据验收后30个日历日，届时记录可见层删除；平台控制面残余不能冒充物理擦除已证明。

## 五、已经取得的可核查成果

### 1. 数据与协议成果

- CSMV：8210个人工金标视频、107,267条人工评论反应，正式video-group split已冻结。
- LAI-GAI：847张跨域图像、63,682条人工响应、379组，独立split已冻结。
- 2787条旧自建/银标记录被隔离为辅助证据，不进入公开人工test金标。
- 数据血缘、标签来源、T0字段、split、同源去重、发布边界和泄漏门均形成版本化文件与hash台账。

### 2. 工程与复现成果

- 统一评测器、实验schema、run/prediction manifest、指标、train-only拟合与错误输入拒绝机制已建立。
- G3最终审查时60/60测试通过；后续VC-CSA兼容、隔离和合同负测扩展到最新已记录68/68。
- G3 handoff绑定22项tracked evidence，不要求把受限资产提交Git。
- 强基线同环境同seed replay四类核心产物逐字节一致。

### 3. 当前正式单种子强基线结果

冻结I3D temporal-attention（`REIMPLEMENTATION_STRONG_BASELINE`）一次性test结果：

- JSD 0.182668；
- NLL 1.715192；
- EMD 0.162983；
- Brier 0.227379；
- ECE 0.053885；ACE 0.054004；
- AURC-JS 0.175399；
- Macro-F1 0.137048；
- Balanced Accuracy 0.148577。

这些是已接受资产风险下的单seed开发阶段证据，不是任务50最终五种子结论，也不能用于宣称方法优越性。

### 4. 门与治理成果

- G1、G2科学协议/数据门和G3均已有00书面独立审查。
- 项目保留失败尝试和状态更正，没有静默删除官方基线失败、远端连接失败、依赖失败和泄漏发现。
- IJCV与T-AFFC已物理拆分，避免同一SSOT、任务树和实验核心被两篇稿件争用。
- 受限I3D、评论正文、模型权重、预测、凭据和端点原文均未进入Git。

## 六、遇到的主要问题及当前处理

### 1. I3D许可与权利方证明仍未知

这是最重要的外部风险。内部8210覆盖、schema和hash已闭合，但许可、官方revision及权利方包身份/fixity没有闭合。当前做法是用户接受内部研究风险、禁止再分发并强制论文披露。若权利方否认或8210 hash/覆盖漂移，立即标记`ASSET_INVALIDATED_DO_NOT_REPORT`。

### 2. 作者VC-CSA与本项目T0目标不兼容

作者实现读取目标评论、使用随机comment split并依赖跨split同视频peer。它可以作为泄漏风险被接受的作者原设定探索，但不能作为无泄漏T0复现。若以后改变peer规则或改为视频级split，只能另立`REIMPLEMENTATION`。

### 3. 当前A30训练中断

最新失败不是GPU OOM或loss爆炸，而是DataLoader worker被系统Killed，较可能与主机内存、worker数或数据加载方式有关。尚未完成首epoch，因此没有可验收结果。建议从`num_workers=0`或2恢复，并同时监控RAM、进程和checkpoint完整性。

### 4. 远端资源和环境不稳定

先后出现A30/A6000端点不可达、SSH握手失败、慢速依赖下载、旧PyTorch/CUDA、工具缺失和脚本兼容问题。项目通过环境冻结、合成资源smoke、实例三元绑定和失败即止损控制了范围，但完整作者探索仍未完成。

### 5. 本地总控门禁环境漂移

当前主仓库`.venv`和`.venv-task20`仍指向本机Python 3.8.9；2026-07-20检查时基础解释器路径已存在，但项目虚拟环境调用在30秒内无输出并超时。bundled Python能运行工作日志校验，但缺PyYAML，不能重跑准备检查。历史G3时任务20独立环境曾为`formal_model_work_ready=true`，但不能把历史环境状态冒充当前总控环境可用。

### 6. 项目管理账本落后于科研现实

`.light/passport.yaml`和`.light/project_card.md`仍停留在2026-07-17的“G3未过/faiss阻塞”状态，与G3已通过的正式文件冲突；passport的G1/G2 evidence_state仍为PLANNED/fresh=false。总纲要求的`TASK_REGISTRY.md`、独立`GATE_G1.md`至`GATE_G6.md`和最终`TAFFC_GO_NO_GO.md`尚未按这些精确文件名建立；目前G1/G2/G3由专项复审文件承担。交接目录还缺S02实体，而S03指向S02，属于交接链治理缺口。

这些不推翻已有科研门裁定，但会降低外部审阅者按账本恢复项目的可靠性，应该在进入任务30前修复。

### 7. 正式统计尚未完成

当前强基线只有单seed。五种子、视频/图像级bootstrap、paired comparison、完整消融、OOD与结果冻结属于任务50，当前状态仍为`TASK50_NOT_COMPLETED`。

## 七、下一步目标

### P0：先恢复并收尾任务20的补充探索

1. 将A30训练的DataLoader `num_workers`降至0–2，监控RAM/GPU和数据吞吐，确认checkpoint是否可安全恢复；失败记录必须入任务20日志。
2. 若恢复成功，只完成授权的seed=3407探索；完成最小证据后再创建私有运行时快照，不扩展为多seed或正式论文实验。
3. 明确记录训练完成/失败、最小输出、快照绑定、保留截止日和可见层删除计划；不提交权重、预测、评论或I3D。

### P0：修复总控可恢复性

1. 重建可运行的本地门禁环境，重新执行工作日志与准备检查。
2. 将`.light/passport.yaml`和`.light/project_card.md`更新到G3已通过、任务20补充探索失败待恢复的事实；使用底层passport工具，不重复已知的memory-pm包装导入失败。
3. 补齐或正式说明S02缺失，建立`TASK_REGISTRY.md`和统一G1–G3门索引，避免多份状态源冲突。

### P1：任务20正式收尾后再决定任务30

任务30的科学启动门G3已满足，但不应在任务20仍修改共享实验核心时并发启动。待任务20停止修改核心、提交最终HANDOFF和工作树清晰后，由00复核创建条件，再创建M4任务。

任务30目标是验证H1：评论只作为train-time privileged teacher，content-only student在推理时严格只读T0内容；比较hard label、soft distribution、普通蒸馏和comment-privileged蒸馏，并检查校准是否恶化。

### P2：任务40、50、60

- 任务40：构建train-only受众反应记忆、检索可靠性门、缺失/不可靠检索时降权或拒绝。
- 任务50：完成五种子、bootstrap、配对比较、两主集实验、OOD/中文压力测试、完整消融和结果冻结，形成G4–G6。
- 任务60：围绕claim-evidence写论文，制作图表与复现包，完成伦理/许可披露、模拟审稿、Go/No-Go并在2027-05-12前形成T-AFFC可投稿包。

## 八、一句话总结

项目最大的成果不是目前某个分数，而是把一个存在版本漂移、标签冲突、随机split和未来评论泄漏的旧实验，重建成了有数据血缘、无泄漏T0协议、统一评测器、强基线、门禁和审计链的T-AFFC研究地基。现在真正缺的是CARM创新模型、正式多种子统计和投稿证据，而不是再堆一个未经审计的模型。
