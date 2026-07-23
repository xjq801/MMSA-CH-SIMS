# 步骤23：Baseline候选清单

> 状态：CANDIDATES_FROZEN_v2
> 日期：2026-07-24
> 注意：这是M1候选与复现成本审计，不授权启动M3训练。G1/G2通过前仅可做代码/许可只读核验。

## 1. 统一成本口径

- 低：预计半天内完成适配，单GPU或CPU可跑，依赖清晰，无大权重。
- 中：预计1—3天适配，需处理序列/多模态接口或旧依赖，单GPU可控。
- 高：预计3天以上，依赖旧CUDA/预训练权重/FAISS-GPU/扩散模型或受限数据；须另行资源审查。
- `UNKNOWN`许可证表示截至本次审计未在官方入口确认，不等于可自由复用。

## 2. 候选表

| ID | Baseline | 角色/任务匹配度 | 代码可得性 | 代码许可 | 预计成本 | 冻结处置 |
|---|---|---|---|---|---|---|
| B00 | Train-label empirical prior | 分布预测最低下界；高匹配 | 本项目实现即可 | 项目许可 | 低 | 必做 |
| B01 | 单模态linear/MLP（text/image/video） | 内容可预测性与模态贡献；高匹配 | 本项目实现即可 | 项目许可 | 低 | 必做 |
| B02 | CatBoost/HGB + 冻结深度特征 | 复用既有传统强基线；中高匹配 | 现有代码可复用但须换split/T0 | CatBoost Apache-2.0；本项目代码按仓库许可 | 低—中 | 必做；旧分数只作历史 |
| B03 | Early/late fusion + zero-fill/mask | H3最小公平基线；高匹配 | 本项目实现即可 | 项目许可 | 低 | 必做 |
| B04 | Tensor Fusion Network (TFN) | 经典多模态融合；中匹配 | 论文有社区实现，未核到作者官方维护实现 | `UNKNOWN`（逐实现核） | 中 | 候选；优先级低于MulT/MISA |
| B05 | Multimodal Transformer (MulT) | 未对齐多模态强基线；中高匹配 | [官方代码](https://github.com/yaohungt/Multimodal-Transformer) | MIT | 中 | 必选强基线候选；需改分布头 |
| B06 | MISA | 模态不变/特异表示；中高匹配 | [官方代码](https://github.com/declare-lab/MISA) | MIT | 中 | 必选强基线候选；需改分布头 |
| B07 | VC-CSA / CSMV论文baseline | 构念最近，但原任务以目标评论+视频预测单条评论；T0不匹配 | [官方仓库](https://github.com/IEIT-AGI/MSA-CRVI)公开数据，模型代码完整性待核 | 根LICENSE Apache-2.0；README另称代码MIT、标注CC BY-SA 4.0，须资产分层 | 中—高 | 只作最近任务/非T0诊断对照，不得作为公平T0输入 |
| B08 | NEmo+论文分布baseline | 公众诱发分布直接前作；高构念匹配 | ACL附数据与论文方法；代码入口未核 | 代码`UNKNOWN`；数据许可未过本项目门 | 中 | 第二主集若合法可用则强制比较；当前BLOCKED_DATA |
| B09 | Generalized distillation | H1方法祖先；高机制匹配 | 无需依赖特定官方实现，可按论文实现 | 论文/代码复用另核 | 中 | H1必做概念基线 |
| B10 | M2PKD式privileged distillation | 情感识别中最接近的特权模态蒸馏；高机制匹配 | 官方论文可得；本轮未确认官方代码 | `UNKNOWN` | 中—高 | H1强制适配候选，不提前实现 |
| B11 | No/random/BM25/CLIP-kNN retrieval | H2因果负对照与简单检索；极高匹配 | 本项目实现；BM25/CLIP依赖需锁版本 | 按具体库/权重另核 | 低—中 | H2全部必做 |
| B12 | RAMER式检索增强 | 缺失模态检索直接前作；高方法匹配、目标不同 | [官方代码](https://github.com/WooyoohL/Retrieval_Augment_MER) | Apache-2.0 | 高 | H2强制思想/组件对照；FAISS缺失且数据EULA使原样复现暂阻塞 |
| B13 | 最大概率/熵阈值拒绝 | 最小selective prediction基线；高可靠性匹配 | 本项目实现即可 | 项目许可 | 低 | H2/H3必做 |
| B14 | Selective Classification / SelectiveNet | 经典与端到端拒绝；高可靠性匹配 | [SelectiveNet官方代码](https://github.com/geifmany/selectivenet)可见，但仓库未显示LICENSE | `UNKNOWN` | 中 | 算法可重实现；未明许可前不复制代码 |
| B15 | MissModal | 多模态情感缺失鲁棒；高H3匹配 | 论文可得；本轮未确认官方代码入口 | `UNKNOWN` | 中—高 | H3近期强基线候选 |
| B16 | IMDer | 缺失模态扩散恢复；高H3匹配 | [官方代码](https://github.com/mdswyz/IMDer) | MIT | 高 | 资源允许时强基线；旧PyTorch/CUDA和预训练权重需隔离环境 |
| B17 | HRLF | NeurIPS 2024不确定缺失模态强基线；高H3匹配 | 论文可得；本轮未确认官方代码入口 | `UNKNOWN` | 高 | H3强基线候选，先做代码可得性二次审计 |
| B18 | Video2Reaction式VLM直接微调/LDL | 当前closest/direct prior；任务目标极高匹配 | arXiv与公开项目页可得；具体代码、权重、许可和split须在任务50前复核 | `UNKNOWN_PENDING_AUDIT` | 高 | CSMV主表强制适配；不能公平执行时提交输入/标签/split/许可/资源/预算审计 |

## 3. 最小公平组合（供G1/G2后M3选择）

在不预先开发模型的前提下，建议M3至少从以下集合选择并冻结：

1. B00—B03：不可省略的低成本下界、单模态与简单融合。
2. B05/B06至少一个：公开、MIT、可适配的强多模态序列baseline；若预算允许两者都做。
3. B07/B08/B18：任务最近前作，必须严格标记输入、标签、split与许可；B18为正式closest-prior义务。
4. H1阶段再启用B09/B10；H2阶段再启用B11—B14；H3正式实验再从B15—B17选近期强基线。

## 4. 当前阻塞

- 当前G1=`PASS`、G2协议/数据=`PASS_WITH_LIMITATIONS`、G3=`PASS_WITH_LIMITATIONS`；本清单升级不授权创建任务30，仍须等待Task20收尾与00决定。
- 普通`.venv`的faiss状态与Task20正式环境不同；任何复现必须绑定实际环境，不复用历史`BLOCKED_M1`描述。
- B07的仓库根许可证、README代码声明和标注许可证口径不一致，必须按代码/标注/特征/媒体分层。
- `UNKNOWN`许可证的代码只能阅读方法描述或自行实现思想；未确认许可前不得复制、改发或纳入项目代码。
