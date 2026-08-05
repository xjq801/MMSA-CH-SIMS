---
session_no: S37
contract_version: 2
suggested_title: "[TAFFC-CARM] S38 内容—反应错位候选路线独立裁定"
parent_session: S36
project: mmsa-ch-sims-taffc-carm
date: 2026-08-04
source_context: side-conversation-research-synthesis
target_thread: total-control-03
---

## 当前阶段

本卡是用户在侧对话中要求形成的研究构想备忘，供“00-T-AFFC总控03”只读吸收与独立裁定。它不构成路线变更、实验授权、SSOT事实或论文claim。正式pipeline仍保持S36裁定：Task30=`CLOSED_NOT_PASSED`，H1开发门=`NOT_PASSED_MECHANISM_NOT_STABLE`，formal test未materialize，Task40/50未创建；G1—G3、I3D UNKNOWN边界与Task20 NON_T0/INELIGIBLE边界均不变。

侧对话围绕“视频内容预测群体观众反应”梳理八篇最相关前作，审查用户提出的两个创新点，并形成一个优先候选：**内容—反应错位的反例引导学习**（counterexample-guided content–reaction discordance learning）。该候选尚未完成系统查新、数据可行性门、idea critique或预注册，不得直接进入实验。

## 已完成（具体产物/commit/决策定位 + 验证摘要）

- `.light/handoff/S37-audience-reaction-idea-side-review.md` — 人工确认已把侧对话中的前作定位、两个原始idea、因果与测量边界、候选方法、基线、OOD评估和止损条件压缩为自包含备忘；人工敏感内容检查未发现评论正文、用户标识、凭据或受限资产。
- 八篇相关工作对照与公开地址 — 在线检索验证八个标题均可定位至论文/出版社/arXiv/会议官方页面；人工核对并区分“训练时评论、推理时视频”“测试时仍需评论”“预测群体分布”“预测单条评论情绪”四类任务，避免把相邻任务误写为同一问题。
- 创新性初筛 — 人工审查验证三项高碰撞：普通门控/混合专家已有大量先例，MVIndEmo已使用点赞加权，Video2Reaction已覆盖视频到群体反应分布并包含纵向分析；因此不建议以“加一个gate”或“按点赞/回复加权”单独支撑T-AFFC主贡献。
- 优先候选与反证门 — 人工确认本卡定义了内容相似度`S_c`、反应分布差异`D_r=JS(y_i,y_j)`、两类反常配对、反例引导表征、Oracle router、routing regret、分组OOD及三项kill criteria；这些均为待验证假设，不是实验结果。

## 工作区状态

造卡前实际锚点为`main@e51621a18f87b2648d8b1a6f8770d5a41d98e74f`且`origin/main`同commit。新增本卡并向`WORK_LOG.md`追加一条记录，均保持未暂存、未提交、未推送，留给总控03独立阅读和决定是否纳入正式SSOT。用户自有未跟踪目录`NEmoP/`、`__MACOSX/`、`tmp/`未读取、未移动、未暂存、未删除。未修改实验代码、数据、任务注册表、passport、project card、总纲或论文SSOT。

## 待用户回答

- decision_id=CARM_IDEA_20260804_ROUTE | question=是否把“内容—反应错位的反例引导学习”升级为正式路线候选并启动独立查新与数据可行性门？ | option_a=进入查新与数据门；影响：允许投入只读查新和数据审计，但不授权实验或修改正式claim，并保留数据门否决空间 | option_b=仅归档为备选；影响：保持现有CARM路线和零新增实验范围，但暂停验证该候选并放弃近期重路由机会

## 下一步（≤3 条，最小动作）

1. 读取并独立核查本卡、八篇前作及现有总纲/论文SSOT，向用户回报“吸收/拒绝/待核查”清单，不把侧对话结论直接写成事实。
2. 验证Video2Reaction与现有可用数据能否构造无泄漏的内容—反应错位配对、movie/creator/event/time分组及评论参与度敏感性分析，先过数据可行性门再讨论模型。
3. 若用户选择option_a，建立版本化idea-critique与预注册合同，冻结question、唯一机制变化、seeds、dev-only选择、停止规则和formal-test禁止项；在此之前不创建Task40或实验批次。

## 阻塞/风险

- **创新碰撞风险**：generic gating、mixture-of-experts、selective transfer和negative-transfer avoidance均非新概念；仅预测“是否参考历史经验”很可能被审稿人视为已有门控的应用。
- **构造伪难例风险**：按固定阈值挖出的“语义双胞胎/情感陌生人”可能由电影身份、剪辑、语言、发布时间或标签噪声造成；需人工审计、跨编码器稳定性和自然分组OOD共同验证。
- **因果越界风险**：点赞数和二级回复数是平台参与度代理，不等于真实曝光；没有impression/ranking logs、时间快照与完整回复树时，不得声称“社会情绪极化因果贡献”。
- **数据识别风险**：回复数不是极化本身；需要回复内容、立场分歧、情感距离和图结构。若只拿到聚合likes/replies，第二idea只能做engagement-conditioned sensitivity analysis。
- **任务拼贴风险**：把路由与互动加权简单相加会形成“A+B式”论文。只有当统一假设“内容相似但参与度放大机制不同会导致负迁移”得到数据支持时，才可合并。
- **查新完整性风险**：侧对话做的是定向检索而非穷尽式systematic review，不能写成“前人从未做过”。

## 必读文件（按序）

1. `.light/handoff/S37-audience-reaction-idea-side-review.md`
2. `.light/handoff/S36-task30-h1-closed-not-passed.md`
3. `.light/passport.yaml`
4. `.light/project_card.md`
5. `TASK_REGISTRY.md`
6. `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.21第5、9、10、17节
7. `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md`
8. `TASK00_TASK30_H1_FINAL_INDEPENDENT_REVIEW_20260804.md`
9. `WORK_LOG.md`末条与Task10/20/30实时状态
10. 本卡“相关工作地图”“候选方案”和“claim边界”三节列出的公开论文页面

## 禁止

- 不得把本卡当作当前事实；必须先运行`git status`/`git log`并刷新Task10/20/30实时状态，禁止凭记忆继续。
- 不得仅凭侧对话把优先候选写入master plan、passport、Registry、论文claim或实验矩阵；任何路线变更需用户明确选择与00版本化裁定。
- 不得继续Task30调参、materialize formal test、创建Task40/50或与Task30并发修改实验核心。
- 不得把likes/replies写成verified exposure，把engagement association写成causal polarization，或把reply count写成polarization本身。
- 不得把普通gate、点赞加权、时间建模或Dirichlet输出单独宣称为首创；须对其最近前作给出差异证据。
- 不得改写G1—G3、H1失败门、I3D UNKNOWN、Task20 NON_T0/INELIGIBLE身份、受限存储删除截止或论文SSOT的`TO_VERIFY`边界。
- 不得创建或执行IJCV的J0—J2、JH1—JH3、任务25或65。

## 侧对话问题与核心结论

### 用户提出的两个原始创新点

1. **历史经验适用性判断**：内容相似不等于观众反应相似；模型应先判断历史反应经验是否适用于当前视频，再决定是否参考。
2. **互动放大差异**：评论点赞与二级回复不同会造成不同参与度和潜在社会情绪放大，应区别建模。

总体判断：两点都有真实问题意识，但原始表述不足以单独支撑T-AFFC。第一点需要从普通门控升级为可证伪的“反应可迁移性/内容—反应错位”问题；第二点必须从粗糙计数升级为测量模型并严格限制因果语言。推荐以第一点的反例化版本为主贡献，第二点只在数据充分时作为机制解释或稳健性分析。

## 八篇相关工作地图

| # | 论文 | 主要任务/方法 | 与本项目的碰撞或差异 | 最可能的审稿质疑 | 公开地址 |
|---|---|---|---|---|---|
| 1 | Discovering Attractive Segments in the User-Generated Video Streams | 用视频与时间同步评论学习视频到评论语义的迁移，预测新视频片段的流行度/观众情绪；评论是训练期“transcendental knowledge” | 已覆盖“评论作训练期特权知识、部署时视频单模态”的骨架，是最危险前作 | 目标混合情绪与热度；自采数据和评论标签偏差；迁移收益是否来自流行度捷径 | https://doi.org/10.1016/j.ipm.2019.102130 |
| 2 | Video2Reaction: Mapping Video to Audience Reaction Distribution in the Wild | 从视频视觉、音频和描述预测21维真实观众反应分布；评论用于构造标签，推理不输入评论 | 与最终预测目标最接近，直接定义video-to-audience-reaction-distribution benchmark | LLM标注噪声、电影来源偏差、同电影泄漏、标签稀疏与时间漂移、资产许可 | https://arxiv.org/abs/2607.06875 |
| 3 | MVIndEmo | TikTok微视频公共诱发情绪；用评论情感及点赞数聚合离散标签和概率分布 | 已显式使用`likes+1`加权，直接压缩“点赞应加权”的新颖性；忽略深层回复 | 点赞不是曝光或因果影响；标签由同一评论聚合可能形成循环监督；主题/平台偏差 | https://link.springer.com/article/10.1007/s00530-023-01221-8 |
| 4 | Enhancing Multimodal Affective Analysis with Learned Live Comment Features | 用对比学习让视频编码器生成synthetic live-comment features，再做情感、情绪、讽刺任务 | 与“评论特权监督/评论表示蒸馏”机制高度重合，但目标不是群体反应分布 | synthetic feature是否只是强文本表征捷径；下游提升能否归因于评论知识；跨平台泛化 | https://arxiv.org/abs/2410.16407 |
| 5 | Infer Induced Sentiment of Comment Response to Video | CSMV/VC-CSA输入视频和单条评论，输出该评论对视频的观点与诱发情绪；多尺度视频、语义一致性和golden grounding | 预测单位是视频—单评论对，测试时仍需要评论，不是视频到群体分布 | 评论文本可能支配结果；视觉增益小；I3D/数据资产可复现与许可；不等同于未来观众预测 | https://papers.nips.cc/paper_files/paper/2024/hash/bbf090d264b94d29260f5303efea868c-Abstract-Datasets_and_Benchmarks_Track.html |
| 6 | Visual-Textual Emotion Analysis with Deep Coupled Video and Danmu Neural Networks | 同时编码视频帧与同步弹幕，以情绪词嵌入和深度典型相关多视图学习融合，预测观众一般情绪 | 直接做视频+弹幕情绪，但部署仍需要弹幕，不满足评论缺失场景 | 自采小数据、标签和任务定义含混；强文本模态掩盖视频贡献；跨域复现不足 | https://arxiv.org/abs/1811.07485 |
| 7 | Video Emotion Analysis Enhanced by Recognizing Emotion in Video Comments | 视觉信息增强评论情绪识别，再用评论情绪和时间关联增强视频情绪分析 | 目标偏视频情绪属性而非群体诱发分布；测试通常依赖评论 | perceived/induced emotion混淆；两阶段误差传播；评论存在时才适用 | https://doi.org/10.1007/s41060-022-00317-0 |
| 8 | Incorporating Social Media Comments in Affective Video Retrieval | 融合音视频与YouTube评论，用Dempster–Shafer决策级融合做情感视频检索 | 早期“评论增强视频情感”路线；不是评论缺失部署或未来群体反应预测 | 数据规模与时代局限；DEAP与YouTube评论配对外部效度；评论模态可用性 | https://doi.org/10.1177/0165551515593689 |

## 原始idea 1：从普通门控升级为反应可迁移性

更精确的问题不是“模型从相似历史视频检索经验”，而是：训练分布学到的`content → reaction`映射在当前视频上是否可迁移。普通deep model未必显式检索相似视频，因此论文不能建立在错误的retrieval前提上。

可执行形式：

- 基础专家：`f_0(x)`，只做常规视频到反应分布预测。
- 历史/反应专家：`f_H(x,H_k)`，允许利用训练库的邻域、原型或反应几何。
- 对样本`i`用交叉拟合得到真实转移收益：

  `Delta_i = D(y_i, f_0(x_i)) - D(y_i, f_H(x_i,H_i))`

- 路由器只用推理时可用信息预测`Delta_i`及其不确定性；`Delta_i`必须来自out-of-fold预测，防止标签泄漏和训练内收益自证。
- 评价必须包含：content similarity vs reaction similarity、Oracle router、routing regret、movie/creator/event/time grouped OOD、content-kNN、confidence gate、generic MoE、LEEP、LogME等基线。

止损：若Oracle routing相对基础模型没有稳定收益，或学习路由不优于generic gate/transferability baselines，则该机制停止，不用额外调参掩盖问题。

## 原始idea 2：互动条件下的情绪放大，而非未经识别的因果极化

若只有根评论情绪`e_i`、点赞`l_i`、回复数`r_i`，可先定义可审计的描述性分布：

- 自发表达分布：`P_prevalence = mean_i(e_i)`
- 认可加权分布：`P_endorse = sum_i log(1+l_i)e_i / sum_i log(1+l_i)`
- 讨论加权分布：`P_discussion = sum_i log(1+r_i)e_i / sum_i log(1+r_i)`
- 参与度放大差异：`JS(P_prevalence, P_endorse)`与`JS(P_prevalence, P_discussion)`

若有完整回复内容和树结构，才可进一步构造：

`Pol_i = log(1+r_i) * Disagreement_i * AffectDistance_i`

这里`Disagreement_i`须由回复立场相对根评论的分歧估计，`AffectDistance_i`刻画情绪/效价距离。点赞或回复数不能独自替代两者。

最低数据要求：根评论、likes、完整回复树与文本、时间戳、抓取快照年龄；若要说真实曝光或因果贡献，还需impression/ranking logs、时间变化或准实验。没有这些数据时，只能称为**engagement-conditioned affect amplification proxy**，不能称为社会情绪极化的因果贡献。

## 优先候选：内容—反应错位的反例引导学习

暂定工作名：**From Semantic Twins to Affective Strangers: Counterexample-Guided Audience Reaction Forecasting**。

核心现象：

- **Affective Strangers**：内容高度相似，但观众反应分布显著不同。
- **Affective Twins**：内容差异较大，但观众反应分布相近。

定义视频内容相似度`S_c(i,j)`，反应分布距离`D_r(i,j)=JS(y_i,y_j)`：

- `P_CD = {(i,j): high S_c(i,j), high D_r(i,j)}`，即内容近而反应远。
- `P_RC = {(i,j): low S_c(i,j), low D_r(i,j)}`，即内容远而反应近。

贡献应形成闭环，而不是仅新增loss：

1. 定量证明content–reaction discordance是自然存在、跨编码器稳定、并显著伤害现有模型的失效模式。
2. 构建人工抽检且防group leakage的hard-pair/quadruplet stress test。
3. 学习反应专属几何，使anchor在反应空间更接近reaction twin而非content twin；方法必须直接针对上述失效模式。
4. 在自然movie/creator/event/time OOD上验证，并报告校准、不确定性和拒答/回退行为。

最近相邻工作与差异边界：ViSiL已有通用视频相似度hard negatives，但不是观众反应几何；Muszynski等T-AFFC工作区分perceived与induced emotion，但未构造社交媒体群体反应错位压力测试；Video2Reaction已做群体反应分布并报告同电影内差异，因此我们必须证明新意在**系统化错位现象、专门benchmark与反例学习闭环**，而不是再次预测分布。

Kill criteria：

- 强基线在discordant pairs上没有显著退化；
- 人工审计发现hard pairs主要是标签噪声或不可控混杂；
- 改进只存在于人工构造stress test，在自然grouped OOD上消失。

任一核心条件成立，都应降级或终止该主线。

## 其他候选及优先级

1. **群体appraisal分布预测**：预测`P(emotion, appraisal)`，appraisal可含novelty、goal congruence、agency、control、norm violation和uncertainty；解释“为什么群体这样反应”。理论契合T-AFFC，但需可靠人工标注，且Video2Reaction已有粗粒度`reaction_reason_type`，必须证明不是简单reason prediction。
2. **三源不确定性分解**：分离真实群体异质性、有限评论抽样不确定性、模型/OOD不确定性，可再加入LLM/标注混淆。可行性较高，但generic Dirichlet/label-distribution confidence已有先例，创新必须来自观众反应特定的测量和coverage协议。
3. **沉默多数/发言选择偏差校正**：建模`P(E|comment) != P(E|view)`并按参与倾向后分层。科学价值高、重合度低，但没有views/impressions、用户历史或调查数据时不可识别，当前可行性低。
4. **时间反应漂移**：Video2Reaction已提供纵向分析；单独“加入时间建模”碰撞较高，只能作为评估维度或辅助分析。

## 推荐的T-AFFC贡献结构

不建议把“gate + 点赞/回复加权”直接堆叠成论文。更审稿人友好的结构是：

1. 一个新的、可证伪的群体情感现象：内容—反应错位；
2. 一个直接暴露该失效模式的评估范式；
3. 一个与失效机制对应的反例引导方法；
4. 强grouped OOD、校准、不确定性与人工审计；
5. 若数据充分，再把互动放大或appraisal作为解释层，而非第二条孤立主线。

该结构与T-AFFC的契合点是群体诱发情感及其可迁移机制。若论文最终退化为通用视频检索、社会热度预测或互动计数建模，则venue fit会变弱。

## claim边界

- 可说：定向检索尚未发现与“内容—反应错位压力测试 + 反例学习 + 群体反应分布”完全相同的组合。
- 不可说：前人从未研究内容与反应不一致；普通hard-negative、metric learning、gating或distribution prediction是我们首创。
- 可说：likes/replies与评论的可见参与度、认可或讨论强度相关，可用于敏感性/代理分析。
- 不可说：likes/replies等于曝光，或其权重识别了对社会情绪极化的因果贡献。
- 可说：目标是群体诱发反应分布，不是屏幕人物的perceived emotion。
- 不可说：评论样本分布代表所有观看者，除非另有选择偏差识别数据。

## 补充查新入口

- ViSiL视频相似度hard negatives：https://openaccess.thecvf.com/content_ICCV_2019/papers/Kordopatis-Zilos_ViSiL_Fine-grained_Spatio-Temporal_Video_Similarity_Learning_ICCV_2019_paper.pdf
- perceived/induced emotion差异：https://doi.org/10.1109/TAFFC.2019.2902091
- Example Transfer Network：https://openaccess.thecvf.com/content_CVPR_2019/html/Cao_Learning_to_Transfer_Examples_for_Partial_Domain_Adaptation_CVPR_2019_paper.html
- LEEP：https://proceedings.mlr.press/v119/nguyen20b.html
- LogME：https://proceedings.mlr.press/v139/you21b.html
- computational appraisal：https://aclanthology.org/2023.cl-1.1/
- Dirichlet emotion uncertainty：https://arxiv.org/abs/2211.04834
- social-media selection bias：https://arxiv.org/abs/1911.03855
- IEEE T-AFFC scope：https://www.computer.org/digital-library/journals/ta/tac-general-call-for-papers

## 接续提示词

你是“00-T-AFFC总控03”，不是Task30执行代理。用户要求你阅读吸收侧对话研究备忘`.light/handoff/S37-audience-reaction-idea-side-review.md`，但该卡不是实时事实或路线授权。先读取AGENTS.md与WORK_RECORD_POLICY.md，运行`git fetch origin`、`git status --short --branch`、`git log -3`及`git rev-parse HEAD/origin/main`；再按S37必读顺序核查S36、passport、project card、Registry、总纲v1.21、论文SSOT与Task10/20/30实时状态。向用户明确回报你接受、拒绝和仍需核查的研究判断。优先评估“内容—反应错位的反例引导学习”，先做系统查新与数据可行性，不得直接授权实验或写入正式claim。likes/replies只能作为参与度代理，禁止冒充曝光或因果极化贡献。Task30仍为`CLOSED_NOT_PASSED`，H1未通过，formal test未materialize，Task40/50未创建；G1—G3、I3D UNKNOWN与Task20 NON_T0/INELIGIBLE边界不变。如用户选择推进，必须先建立版本化idea-critique和预注册合同。每次收尾继续创建下一张S<NN>交接卡并打印接续提示词。
