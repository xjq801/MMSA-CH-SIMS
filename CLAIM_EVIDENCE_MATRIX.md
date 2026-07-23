# Claim—Evidence矩阵

> 版本：v1.1；日期：2026-07-24  
> 原则：没有证据的主张保持`TO_VERIFY`，不得写成论文结论。

| Claim ID | 核心主张 | 所需证据 | 对应实验/材料 | 当前状态 | 允许措辞 |
|---|---|---|---|---|---|
| C1 | 无泄漏T0协议能形成可审计的公众公开表达诱发反应分布预测证据 | 两个公开人工标注集、内容单元划分、物理泄漏隔离、Data Card | G1/G2、E0、`T0_INPUT_POLICY.md` | TO_VERIFY | 仅可描述协议/证据贡献；任务与分布输出均不称首创 |
| C2 | 评论特权教师能改善仅看内容学生的分布预测或校准 | content-only、teacher上界、普通蒸馏、目标方法；至少5种子与CI | H1、E2、任务30 | TO_VERIFY | 不得宣称有效 |
| C3 | train-only反应记忆、可靠性router与rejection优于无/随机检索并减少错误证据负迁移 | 去memory/router/rejection、稀疏/稠密/可学习检索、错域邻居、risk-coverage | H2、E2/E4/E7、任务40/50 | TO_VERIFY | 不得宣称检索或路由增益 |
| C4 | 方法在movie/group、topic、time、platform、跨数据和适用缺失场景具有更可靠表现 | 严格OOD、跨数据、适用缺失、中文压力测试；统计与失败案例 | C3、E5—E9、任务50 | TO_VERIFY | 不得宣称泛化或代表所有观众 |

状态只能是`TO_VERIFY`、`SUPPORTED_LIMITED`、`SUPPORTED`、`REFUTED`。任何状态变更必须填写结果文件、统计证据和复核日期。

## 2026-07-14 前作约束（不改变实验支持状态）

| Claim/边界 | 已核前作 | 对允许措辞的限制 | 证据文件 |
|---|---|---|---|
| C1任务定位 | NEmo+、CSMV/MSA-CRVI、MVIndEmo、iNews | 不得声称首次提出公众诱发情绪或分布预测；只可强调严格T0与group-held-out协议 | `LITERATURE_SEARCH_REPORT.md`、`CONTRIBUTION_PRIOR_ART_MATRIX.md` |
| C2-H1机制 | LUPI、generalized distillation、M2PKD | teacher/student和训练期特权信息不是贡献；必须做普通KD和特权蒸馏对照 | 同上 |
| C2-H2机制 | RAMER | 检索增强缺失模态情绪识别已有直接前作；必须做no/random/BM25/CLIP-kNN和RAMER式对照 | 同上 |
| C3可靠性 | Selective Classification、SelectiveNet、MissModal、IMDer、HRLF | 拒绝和缺失模态鲁棒不是模块级首创；只检验其在public-induced distribution、OOD和自然缺失下的证据 | 同上 |

上述查新只冻结主张上限，不把C1—C3从`TO_VERIFY`升级为`SUPPORTED`；任何有效性表述仍须等待预注册实验与统计证据。

## 2026-07-23 Video2Reaction增量约束

| Claim/边界 | 新近前作 | 对允许措辞的限制 | 强制证据动作 |
|---|---|---|---|
| C1任务定位 | Video2Reaction，arXiv:2607.06875 v1；workshop展示已确认；ECCV为作者报告待正式条目 | C1只能称严格T0、HUMAN_GOLD、group-held-out和future-comment isolation的协议/证据贡献；禁止任务首创与“分布输出即创新” | 任务50执行其VLM直接微调/LDL公平适配，或提交输入/标签/split/许可/资源/预算不可比审计 |
| C2-H1评论教师 | Video2Reaction未覆盖已定位的训练期评论特权链，但LUPI/M2PKD/评论增强已覆盖组件 | 只能检验严格T0下的特权评论收益，不能把teacher/student或蒸馏写成新机制 | 普通KD、特权蒸馏、错配评论和teacher upper-bound对照 |
| C2-H2反应记忆 | Video2Reaction未覆盖已定位的train-only反应记忆与负迁移拒绝；RAMER/SelectiveNet覆盖相邻组件 | 不得以模块组合证明创新；必须证明学习检索优于随机/普通近邻且路由识别有害邻居 | E2/E4/E7、错误邻居、OOD、负迁移率和risk-coverage |

本节不改变C1—C4的`TO_VERIFY`状态，不追溯改变G1—G3；它只收紧后续论文主张和公平对比义务。

## 2026-07-24 Claim blacklist与构念边界

- `TAFFC_CLAIM_BLACKLIST_20260724.md`是活动主张禁用表，覆盖标题、摘要、引言、贡献、相关工作、结论、PPT和答辩材料。
- 社媒评论标签只支持“评论者公开表达的诱发反应分布”，不支持“所有观看者真实内在情绪”。
- Video2Reaction必须称`closest/direct prior`；“尚未定位完全同构方法”只允许写成scoping未检出，不得写世界首创。
- 本节不升级任何有效性状态。

## 2026-07-16 CSMV输入与主张上限

| 边界 | 冻结证据 | 允许措辞 | 禁止措辞 |
|---|---|---|---|
| CSMV内容输入 | `csmv-i3d-sequence-protocol-v1.manifest.json`；8210/8210 shape/fixity | “冻结I3D视觉表征上的公众诱发受众情绪分布预测” | 端到端视频编码、原始帧学习 |
| 序列处理 | 完整序列主协议；确定性均匀180步主敏感性；前180补充 | 视觉序列处理消融/敏感性 | 多模态增量、看到test后选择规则 |
| 音频与评论 | `experiment-protocol-v2.md`；00音频复审 | 评论特权监督；音频结构性不可得 | 音视频融合、音频增益、评论文本T0输入 |
| 资产准入 | 本地fixity已闭合；维护者证明延期；`SC-20260717-01` | “内部研究使用，资产外部证明为已接受延期风险” | “官方资产已确认”“权利方已授权”“官方checksum已闭合” |

本节只收紧未来论文措辞，不把C1—C4的有效性状态升级为`SUPPORTED`。

## 2026-07-16 IJCV独立claim合同（已迁出归档）

> 下列J-claims是总纲v1.14时期的历史快照，已随`SC-20260716-03`迁至独立IJCV项目。本项目不得执行、更新或把它们计入当前claim集合；T-AFFC当前claim集合只有C1—C4。表内`TO_VERIFY`仅记录迁出时状态，不代表本项目仍有对应待办。

| Claim ID | 核心主张 | 所需证据 | 对应实验/材料 | 当前状态 | 允许措辞 |
|---|---|---|---|---|---|
| J-C1 | 响应分布几何监督能学习更适合主观情绪分布的视觉表征 | 至少两个像素人工分布集；PC/SAMNet/MFRN及强ViT/CLIP公平基线；JSD/EMD/NLL、5种子、按图像CI | JH1、J1—J3、任务25 | TO_VERIFY | 仅可描述假设与方法动机 |
| J-C2 | 显式分歧建模能改善区间/选择性可靠性且分布误差非劣 | 可识别的观察者分歧estimand、coverage/NLL/Brier/AURC、softmax/Dirichlet/ensemble对照 | JH2、J4—J5、任务25 | TO_VERIFY | 不得把预测熵等同观察者分歧或认知不确定性 |
| J-C3 | 分布几何保持能在标签空间不完全同构时支持跨域视觉迁移 | 预注册跨域estimand、数据集特定head、source-only/fine-tune/域适配对照 | JH3、J6/J8、任务25 | TO_VERIFY | 不得声称统一标签空间或跨域有效 |

迁出边界：J-C1—J-C3及其后续证据只在`D:\MMSA-CH-SIMS - IJCV方向`维护；本项目不得把其主实验、主表或方法改名复用。历史方案文件仅用于解释范围变化，当前执行事实源为T-AFFC总纲v1.15。
