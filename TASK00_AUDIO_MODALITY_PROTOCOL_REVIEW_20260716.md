# 00总控：CSMV音频模态可发表性与协议边界复审

> 裁定编号：`REVIEW-00-AUDIO-MODALITY-PROTOCOL-20260716`  
> 日期：2026-07-16  
> 复审对象：`TASK10_AUDIO_MODALITY_FEASIBILITY_REVIEW_REQUEST_20260716.md`及任务10交接/G门/Data Card/Datasheet  
> 总裁定：`PASS_WITH_LIMITATIONS_AUDIO_NOT_REQUIRED_FOR_PRIMARY_PROTOCOL`

## 1. 裁定结论

任务10提出的“音频不是CSMV主协议或G2的独立前置条件”成立。音频从后续资产取得关键路径、G2阻塞项和任务20启动条件中移除，冻结状态为：

`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`

该裁定只表示当前研究可以采用无音频协议继续推进，不表示音频已取得、不表示音频不具有科学价值，也不保证论文录用。论文是否可发表仍取决于问题新颖性、强基线、无泄漏证据、统计充分性和主张强度是否匹配。

## 2. 独立证据复核

1. IEEE T-AFFC General Call for Papers把面部/身体视觉情感识别、文本和语音分析、听觉与视觉情感爆发、多模态识别、群体情绪和预测性情感模型列为并列的范围示例，没有规定每篇投稿必须包含音频：<https://www.computer.org/digital-library/journals/ta/tac-general-call-for-papers>。
2. CSMV固定上游commit `99d14240254b1381dde0b9c56add140381f65117`的README明确写明当前发布视频视觉部分、I3D与VideoMAE特征，并把音频特征列为未来补充；`.npy`按`video_file_id`对应：<https://raw.githubusercontent.com/IEIT-AGI/MSA-CRVI/99d14240254b1381dde0b9c56add140381f65117/README.md>。
3. NeurIPS 2024正式入口将任务定义为利用视频内容推断评论响应，公开摘要确认8,210段微视频、107,267条人工标注评论及VC-CSA视觉内容基线：<https://proceedings.neurips.cc/paper_files/paper/2024/hash/bbf090d264b94d29260f5303efea868c-Abstract-Datasets_and_Benchmarks_Track.html>。
4. 总纲v1.11任务10的G2条款要求追溯、标签隔离、test评论隔离、零泄漏split和manifest重放，没有音频退出条件。

上述证据支持“无音频协议不因期刊范围或当前CSMV公开资产而自动失格”，但不支持“音频不重要”或“仅凭视觉即已完成原多模态假设”。

## 3. 四项请求的书面裁定

| 请求 | 裁定 | 生效边界 |
|---|---|---|
| 1. 音频冻结为结构性不可得且不作为G2前置条件 | **批准** | 状态固定为`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`；不等待、不伪造、不插补音频 |
| 2. CSMV正式输入限定为一个准入视觉特征族，优先I3D | **有条件批准** | 仅在I3D资产许可、稳定revision、包身份/fixity及00准入复审闭合后正式使用；评论只作标签/训练期特权监督，不是T0推理输入 |
| 3. 按实际可得模态重写E1/E5/H3 | **批准并收紧** | 使用`ALL_AVAILABLE_INPUTS`，不得称“音频齐全的完整多模态”；只有数据协议实际含至少两个T0合法、冻结、可得输入模态时，才运行随机缺失/逐模态增量实验 |
| 4. 保持G2、`formal_split=false`和任务20禁令 | **批准** | 本裁定不放行I3D、不放行G2、不创建任务20、不训练或建正式索引 |

## 4. E1/E5/H3的权威解释

- **E1**：比较单个实际可得输入与`ALL_AVAILABLE_INPUTS`。若某数据集只有一个T0合法内容模态，则“逐模态增量”记`NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`，不得把同一I3D序列的不同池化方式写成不同模态。
- **E5**：随机缺失率、缺一/缺二模态只在同一样本确有至少两个实际输入模态时运行。CSMV音频缺失是数据集设计导致的结构性不可得，不是从完整样本随机删失；音频分支固定为`NOT_APPLICABLE_AUDIO_UNAVAILABLE_BY_DATASET_DESIGN`。
- **H3**：保留为条件性假设。若后续没有任何符合上述条件的数据协议，H3必须降级为`NOT_APPLICABLE_NO_ELIGIBLE_MULTIMODAL_PROTOCOL`，不能用CSMV与LAI-GAI之间的视频/图像域差异替代同一样本的缺失模态鲁棒性证据。
- **评论文本**：只可作为标签来源、训练期特权教师或train-only反应记忆；不得在T0学生推理时出现，也不得和视觉特征一起冒充“完整T0多模态输入”。

## 5. 允许与禁止的论文主张

允许：冻结视觉表示上的公众诱发受众情感分布预测、评论特权监督、train-only反应记忆、校准、OOD、拒绝预测和视觉序列处理消融。

禁止：音视频融合、音频增益、声学线索解释、音频随机缺失鲁棒性、端到端原始帧/音频编码器改进、伪音频或全零音频补齐，以及未标明训练/推理角色的笼统“完整多模态输入”表述。

## 6. 门状态与下一路径

- G1=`PASS`。
- G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`。
- 全局`formal_split=false`。
- `formal_model_work_ready=false`，任务20继续禁止。
- 后续取得路径只收敛I3D（或另一个经书面改选的单一视觉特征族）的资产准入；音频不再列入下载、许可协调、存储预算或G2恢复条件，但必须继续作为论文限制和机器可读不适用状态披露。

