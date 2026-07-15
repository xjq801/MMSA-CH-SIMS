# 任务10：CSMV音频缺失可发表性裁定与00复审请求

> 提交方：10-M1–M2 数据与协议  
> 提交给：00总控  
> 日期：2026-07-16  
> 总纲：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.11，第17节任务10  
> 任务10建议裁定：`PASS_WITH_LIMITATIONS_AUDIO_NOT_REQUIRED_FOR_PRIMARY_PROTOCOL`  
> 请求00裁定：确认音频不是G2或任务20启动的独立前置条件；不自行修改现有G门

## 1. 结论

CSMV当前缺少音频**不构成向IEEE Transactions on Affective Computing投稿的硬性阻塞，也不构成任务10 G2条文中的独立阻塞**。可以继续以冻结I3D视觉时序特征为主输入，开展公众诱发受众情感分布的内容侧预测、评论特权监督、train-only反应记忆、校准、OOD和可靠性拒绝研究。

该结论是“允许采用无音频协议”，不是“音频已获得”或“音频不重要”。正式论文和实验必须把音频登记为`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`，并收缩相应主张。

## 2. 证据

### 2.1 T-AFFC没有规定投稿必须含音频

T-AFFC General Call for Papers把视觉情感识别、群体情绪、预测性用户情感状态模型、文本/语音分析和多模态识别列为并列的范围示例，而不是要求每篇论文同时覆盖视觉、文本和音频。因此，本项目以视觉内容与受众反应分布为核心，仍属于期刊范围。

- 官方范围：<https://www.computer.org/digital-library/journals/ta/tac-general-call-for-papers>

### 2.2 CSMV官方发布本身就是“视觉已发布、音频未来提供”

CSMV官方README明确说明当前发布视频帧提取的I3D/VideoMAE视觉特征，并将音频特征列为未来补充。NeurIPS 2024正式论文报告的CSMV和VC-CSA实验使用预训练视觉特征；因此，缺少音频不是偏离当前公开benchmark资产的异常状态。

- 官方仓库说明：<https://github.com/IEIT-AGI/MSA-CRVI/blob/main/README.md>
- NeurIPS 2024正式论文入口：<https://proceedings.neurips.cc/paper_files/paper/2024/hash/bbf090d264b94d29260f5303efea868c-Abstract-Datasets_and_Benchmarks_Track.html>

### 2.3 总纲已把音频排除在必做扩张之外

总纲v1.11明确规定：原始音视频缺失不伪造；不同时扩张音频、视频、图像、文本、GNN、RAG和大模型；正式视频输入优先复用官方VideoMAE/I3D特征。任务10的G2/L2条款要求的是样本追溯、标签物理隔离、test评论隔离、正式split零泄漏和manifest重跑，并未把音频列为退出条件。

## 3. 允许继续的实验与主张

- CSMV：冻结I3D视觉时序表示上的分布预测、content-only基线、评论特权教师、蒸馏、train-only检索、校准、OOD、拒绝预测和视觉序列消融。
- LAI-GAI：图像跨域、自然缺失模态、校准/OOD与H3边界验证。
- CUC：仅按既有协议作为中文银标辅助和自然缺失外部压力测试。
- 论文可表述为“基于可用内容模态/视觉内容的公众诱发受众情感预测”；若使用“多模态”，必须指明实际模态和训练/推理角色，不能暗示包含音频。

## 4. 必须删除或降级的主张

- 不得声称完成音视频融合、音频编码器训练或音频增益实验。
- 不得把全零向量、生成音频或其他伪信号当作真实音频模态。
- 不得把“从有音频随机删失”作为已验证的音频缺失鲁棒性；CSMV只能报告音频结构性不可用。
- E1中的“完整模态”必须解释为**该数据源在T0合法、冻结且实际可得的全部模态**，不是理论上的音频齐全。
- H3仍可研究视觉/图像/文本等实际模态的缺失与自然跨域缺失，但音频分支记`NOT_APPLICABLE_AUDIO_UNAVAILABLE_BY_DATASET_DESIGN`。
- 不得声称端到端原始视频表示学习、原始帧编码器改进或复现依赖评论文本输入的原论文同一任务指标。

## 5. 对G门的影响

| 项目 | 任务10建议 |
|---|---|
| G1 | 保持`PASS`；音频不新增阻塞 |
| G2 | 音频项建议`NOT_REQUIRED_WITH_DISCLOSED_LIMITATION`，但**不因此自动PASS** |
| 当前G2剩余阻塞 | 仍是I3D资产级许可、稳定官方revision与包身份/fixity的00裁定 |
| `formal_split` | 00复审前仍为`false` |
| 任务20 | 仍须00书面通过G2后创建；任务10不自行创建或训练 |

## 6. 请求00书面确认

请00复审并裁定以下四项：

1. 音频状态冻结为`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`，不作为G2独立前置条件；
2. CSMV正式输入族限定为一个经准入的视觉特征族，优先I3D；
3. E1/E5/H3按“实际可得模态”重写，音频相关实验标`NOT_APPLICABLE_BY_DATASET_DESIGN`；
4. 保持现有G2、`formal_split=false`和任务20禁令，待I3D资产准入另行裁定，不把本文件误作G2放行。

## 7. 诚实限制

无音频会缩小论文的模态覆盖并减少对声学线索贡献的解释力，审稿人可能要求在限制部分说明。补救方式应是清楚定义估计对象、报告实际模态、运行强视觉基线和缺失模态边界实验，而不是等待未承诺的音频发布或伪造音频。
