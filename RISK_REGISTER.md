# 项目风险登记

> 维护任务：00-总控与决策  
> 当前快照：2026-08-05  
> 规则：风险关闭必须链接到可复核证据；`UNKNOWN`不能按通过处理。

| 风险ID | 风险 | 当前证据 | 影响 | 当前控制 | 状态/恢复条件 |
|---|---|---|---|---|---|
| `R-DATA-001` | CSMV内部ID与平台ID命名空间混淆及同源split泄漏 | 旧规则误要求两类ID相等；真实风险为202个重复源视频族，修复前100族跨video split、115族跨hashtag split | 错误阻塞媒体lineage或产生同源泄漏 | 已建立官方映射语义、8008个哈希源族、先归并后划分、专项负面门；00独立复核通过 | CLOSED_OBSERVABLE_LINEAGE_20260715；内容指纹/publisher/time边界继续受控开放 |
| `R-DATA-002` | LAI-GAI核心图像资产文件树、size/hash和内容对象集合未闭合 | 旧API的`K8XVH`为空；后续独立授权已从官网9页闭合847图、评分、hash和canonical | 原曾阻塞第二主集与G1 | 保留旧失败；以新授权官网资产链和专项validator作为独立证据 | CLOSED_20260715；`REVIEW-00-LAI-GAI-FREEZE-20260715` |
| `R-PROTOCOL-001` | LAI-GAI API审计请求间隔违反硬下限 | 请求2→3为0.996519秒，低于1秒0.003481秒；专项validator exit 1 | 本轮不能声明授权合规，综合准备门保持阻塞 | 不设容差、不追溯豁免、不重跑；采集器未来余量+0.1秒 | CLOSED_FOR_THIS_RUN_NONCONFORMING；历史失败永久保留 |
| `R-CLAIM-001` | 把图像跨域验证夸大为第二多模态视频复现 | LAI-GAI为单图，缺音频/视频；H1/H2字段可能不适用 | 论文构念、实验同构性和投稿可信度受损 | 总纲v1.6限定主张；不适用项记`NOT_APPLICABLE_BY_DESIGN` | CONTROLLED_OPEN；G4/G6据真实证据重新审核 |
| `R-LEAK-001` | 生成prompt或目标类别形成标签捷径 | 预设目标与人类最高评分并非完全一致 | T0输入泄漏、人工真值被伪标签替代 | prompt只存hash/provenance，目标类别标为非真值，二者均禁止进入模型；专项字段与负面门通过 | CLOSED_FOR_LAI_GAI_V1；映射或输入合同升版时重开 |
| `R-DATA-003` | CSMV I3D资产许可与官方身份仍未知 | 本地9942文件、8210必需键、schema和hash闭合；权利方未确认asset license、稳定revision或包身份/fixity | 可能影响审稿、复现、模型/特征发布及后续合规；若权利方否认，依赖I3D的结果须撤回 | 用户以`SC-20260717-01`接受延期风险；仅内部研究、禁止再分发、强制披露；继续等待Issue #5但不阻塞任务20 | ACCEPTED_HIGH_RISK_NONBLOCKING_G2；权利方否认或hash漂移立即止损 |
| `R-REPRO-001` | source-family修复后复现manifest陈旧 | 旧18输出manifest的记录hash与当时9项文件不一致；旧validator未现场重算 | 不能证明当前split可从manifest隔离重建，可能把旧PASS误作新PASS | 公共核心隔离重放扩为19项；validator现场重算；00独立重跑 | CLOSED_20260715；19项当前零漂移，后续任一漂移继续fail-closed |
| `R-IJCV-001` | 当前CARM视觉方法性不足且与VEDL近邻撞车 | 专刊强调新CV方法；PC Loss、SAMNet、MFRN已覆盖分布结构、主观分支/affective memory和特征精炼 | 仅影响已迁出的IJCV方向，不再影响本项目G门 | 风险及J0/J1/J2控制已迁至独立IJCV项目；本项目不执行视觉表征路线 | TRANSFERRED_TO_IJCV_PROJECT_20260716 |
| `R-IJCV-002` | 缺少第二个像素可得、许可固定的人工主观分布集 | LAI-GAI已冻结；其他图像集仍需逐资产准入 | 仅影响已迁出的IJCV方向，不再是本项目数据门 | 第二像素人工集准入由独立IJCV项目维护；本项目任务10不再取得该数据 | TRANSFERRED_TO_IJCV_PROJECT_20260716 |
| `R-INTEGRITY-001` | IJCV与T-AFFC形成一稿多投或重复发表 | 两路线可能共享研究构念与部分数据基础 | 若未来两项目都形成稿件，仍可能产生投稿伦理风险 | 项目、分支、总纲、claim和主实验已物理分离；跨项目只消费已提交事实并在投稿时披露相关稿 | CONTROLLED_CROSS_PROJECT；不阻塞本项目当前G门 |
| `R-SCHEDULE-001` | IJCV 2026-12-15固定截稿压缩方法与复现周期 | IJCV方向已独立迁出 | 不再挤占本项目T-AFFC日历与资源优先级 | 本项目恢复2027-05-12 T-AFFC单线日历；IJCV期限由独立项目自行管理 | TRANSFERRED_TO_IJCV_PROJECT_20260716 |
| `R-NOVELTY-001` | CARM被评价为检索、后验、校准和拒绝的模块拼接 | 检索记忆、有限标注后验、选择性拒绝、不确定性估计和分布预测均各有前作 | T-AFFC方法新颖性与完整论文定位 | 总纲v1.23把可证伪的新颖性压在同一决策问题：OOF点/后验净收益、三动作、Oracle headroom、点/generic router强对照、response thinning和负迁移机制链 | OPEN_HIGH；若Oracle无headroom、可信router不优于点/generic router，或收益随稀释/先验翻转，删除可信历史路由主张 |
| `R-NOVELTY-002` | Video2Reaction直接覆盖“视频内容→受众反应分布”的C1任务层目标 | arXiv:2607.06875于2026-07-08公开；官方HF包已公开标签、metadata和多模态派生特征；DataMFM展示确认，ECCV正式论文集状态待核 | “任务首创”和“分布输出即创新”失效；若只引用、不做公平直接对比可导致拒稿 | 总纲v1.21保持可靠预测定位；任务50双轨：CSMV同协议适配为主，Video2Reaction原生复现/movie-disjoint为外部验证；分表且禁绝对指标横比 | OPEN_HIGH；投稿前滚动查新，只有H1/H2和OOD选择性证据成立才保留完整方法claim |
| `R-DATA-004` | Video2Reaction公开包被误写为完整原始音视频文本与人工金标，或忽略许可表述冲突 | HF公开派生特征和LLM生成分布；HF卡标CC BY-NC-SA 4.0，GitHub README/API层有CC BY 4.0/NOASSERTION表述；底层媒体受第三方条款 | 错误数据预算、许可外推、银标冒充金标及跨数据不公平比较 | DS-012绑定HF revision与GitHub commit，状态`CONDITIONAL_EXTERNAL_VALIDATION_NOT_CORE_REQUIRED`；许可差异解决前不下载/运行B轨 | OPEN_HIGH；不阻断CSMV核心Task40，但阻断Video2Reaction原生外验 |
| `R-CONSTRUCT-001` | 把社媒评论分布外推为所有观众的真实内在情绪 | 评论者自选择、公开表达与未评论观看者不可观测；Video2Reaction同样依赖社媒反应 | 构念效度被拒稿、伦理与应用主张过度 | 统一称“评论者公开表达的诱发反应分布”；HUMAN_GOLD主测试与SILVER训练隔离；报告评论数、分歧、置信度和代表性限制 | OPEN_HIGH；任务60必须通过claim blacklist与构念人工审计 |
| `R-EVIDENCE-001` | 把单seed强基线或计划阈值写成正式优越性 | 当前temporal-attention只有单seed正式test，任务50尚未完成 | 过度主张、统计无效与拒稿 | 所有效应claim保持TO_VERIFY；正式门要求五种子、原生单位paired bootstrap CI和多重校正 | OPEN_NONBLOCKING_UNTIL_TASK50；G4/G6前不得升级 |
| `R-OPS-001` | Task20 VC-CSA探索已收尾，受限存储进入定时保留 | 唯一seed=3407已完成120 epoch并冻结最小私有证据；00于2026-08-01接受收尾。Epoch 1—3原始三件套永久缺失；固定8210项I3D、最终证据和受控环境仍在私有存储，可见层尚未删除，平台控制面UNKNOWN | 若漏过截止日或把活动保留误写为已删除，会形成受限资产残留与审计失真 | 永久NON_T0/INELIGIBLE；D0=2026-08-01，2026-08-31 23:59:59 +08:00前另做可见层删除验收；控制面无法核验时保持UNKNOWN并记录失败 | CONTROLLED_OPEN_TIME_BOUND_RETENTION；不再阻塞Task30创建，见`REVIEW-00-TASK20-FINAL-CLOSEOUT-20260801` |
| `R-MEASUREMENT-001` | aleatoric、epistemic与transfer/retrieval三源不确定性不可辨识，或把经验预测集合夸大成有保证的置信区域 | 当前只有方案定义，尚无可观测性证明、校准集证据或有限样本coverage/width结果 | 机制claim不可识别、校准主张过强、选择性结果难以复现 | 在Task40创建前冻结三源操作定义、可观测量和反例；预测区域同时报告经验coverage与width并限定交换性/分布假设；分解不成立时只报告总不确定性 | OPEN_HIGH；若消融不能证明第三源的独立决策价值或区域未达到预注册coverage，则删除“三源分解/预测区域”正式claim |
| `R-ROUTE-001` | OOF收益标签泄漏或历史路由没有可利用的真实净收益 | 同一样本拟合内收益会乐观；内容相似不等于反应相似；当前尚无Oracle headroom结果 | 路由可能学习数据泄漏、容量差或噪声，造成负迁移 | 收益标签只能由5-fold group OOF预测生成；Task40首先运行Oracle headroom和错配历史负对照；与固定融合、相似度、熵、generic gate、SelectiveNet及点收益路由公平比较 | OPEN_TASK40_FIRST_DEVELOPMENT_GATE；Oracle无headroom或OOF审计失败时关闭Task40路由开发，不训练router |
| `R-MEASUREMENT-002` | 点收益标签把有限反应抽样噪声当成真实历史净效用 | CSMV每视频只有2—20条反应；净收益符号可能随响应子样本或Dirichlet先验翻转 | router学会标签噪声，“伤害避免”主张不稳定 | 同时报告点`Delta`、`P(Delta>0)`与5%下分位；CSMV 2/4/8/all×200 thinning；Dirichlet(0.5/1)与bootstrap敏感性；点/后验router公平比较 | OPEN_HIGH；若收益符号、动作或负迁移主结论对稀释/先验不稳定，删除“可信净收益”强claim |
