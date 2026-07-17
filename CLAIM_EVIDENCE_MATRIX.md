# Claim—Evidence矩阵

> 版本：v1.0；日期：2026-07-14  
> 原则：没有证据的主张保持`TO_VERIFY`，不得写成论文结论。

| Claim ID | 核心主张 | 所需证据 | 对应实验/材料 | 当前状态 | 允许措辞 |
|---|---|---|---|---|---|
| C1 | 无泄漏T0协议能形成可审计的公众诱发情绪分布预测任务 | 两个公开人工标注集、视频级划分、物理泄漏隔离、Data Card | G1/G2、E0、`T0_INPUT_POLICY.md` | TO_VERIFY | 仅可描述研究问题与协议 |
| C2 | 评论特权教师能改善仅看内容学生的分布预测或校准 | content-only、teacher上界、普通蒸馏、目标方法；至少5种子与CI | H1、E2、任务30 | TO_VERIFY | 不得宣称有效 |
| C3 | train-only反应记忆与可靠性路由优于无检索和随机检索，并减少负迁移 | 无/随机/稀疏/稠密/可学习检索、负对照、risk-coverage | H2/H3、E3—E5、任务40/50 | TO_VERIFY | 不得宣称检索增益 |
| C4 | 方法在跨话题、跨数据、缺失模态场景具有更稳健表现 | OOD、跨数据、缺失模态、中文压力测试；统计与失败案例 | H4、E6—E9、任务50 | TO_VERIFY | 不得宣称泛化 |

状态只能是`TO_VERIFY`、`SUPPORTED_LIMITED`、`SUPPORTED`、`REFUTED`。任何状态变更必须填写结果文件、统计证据和复核日期。

## 2026-07-14 前作约束（不改变实验支持状态）

| Claim/边界 | 已核前作 | 对允许措辞的限制 | 证据文件 |
|---|---|---|---|
| C1任务定位 | NEmo+、CSMV/MSA-CRVI、MVIndEmo、iNews | 不得声称首次提出公众诱发情绪或分布预测；只可强调严格T0与group-held-out协议 | `LITERATURE_SEARCH_REPORT.md`、`CONTRIBUTION_PRIOR_ART_MATRIX.md` |
| C2-H1机制 | LUPI、generalized distillation、M2PKD | teacher/student和训练期特权信息不是贡献；必须做普通KD和特权蒸馏对照 | 同上 |
| C2-H2机制 | RAMER | 检索增强缺失模态情绪识别已有直接前作；必须做no/random/BM25/CLIP-kNN和RAMER式对照 | 同上 |
| C3可靠性 | Selective Classification、SelectiveNet、MissModal、IMDer、HRLF | 拒绝和缺失模态鲁棒不是模块级首创；只检验其在public-induced distribution、OOD和自然缺失下的证据 | 同上 |

上述查新只冻结主张上限，不把C1—C3从`TO_VERIFY`升级为`SUPPORTED`；任何有效性表述仍须等待预注册实验与统计证据。

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
