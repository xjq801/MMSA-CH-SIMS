# 步骤22：研究问题、贡献上限、假设与指标冻结审计

> 审计日期：2026-07-14
> 决策：`FROZEN_v1_CONFIRMED`
> 事实源优先级：总纲v1.5 > 本审计 > `research-question-v1.md` / `experiment-protocol-v1.md`的便捷表达。

## 1. 研究问题v1

- RQ1/C1：严格T0和video/post-group划分下，发布时可见多模态内容能否预测未来受众情绪经验分布、分歧与不确定性。
- RQ2/C2-H1：只在训练期读取评论的特权教师，能否稳定改善推理期content-only学生，同时不让评论信息进入测试输入。
- RQ3/C2-H2/H3：train-only或严格更早的受众反应记忆，配合可靠性降权/拒绝，能否优于无检索和随机检索，并减少跨话题、跨平台或缺失模态负迁移。
- RQ4/C3-H4（增强）：仅在合法可复现的配对模态数据成立时，预测加入图像后受众反应分布的变化；不作为主线必成条件。

## 2. C1—C3贡献上限

| ID | 冻结上限 | 不得越界 |
|---|---|---|
| C1 | 无泄漏的公众诱发情绪预测协议：评论只作标签/训练期特权监督；video-group、topic/hashtag-held-out；T0禁未来信息 | 不声称首次提出公众诱发情绪或分布任务；随机split高分不作主证据 |
| C2 | 评论特权教师 + 可拒绝的train-only受众反应记忆 | 不把teacher/student、RAG、FAISS、LLM、GNN或模块拼接本身写成贡献；不检索目标评论/未来案例 |
| C3 | 跨话题、跨平台和自然缺失下的可靠性证据 | 不用银标冒充人工金标；不只报Accuracy；第二人工主集未通过时不得声称跨集成立 |

## 3. H1—H4与止损条件

| ID | 主检验 | 冻结失败/止损条件 |
|---|---|---|
| H1 | CSMV与第二公开人工主集上的JS/NLL；评论特权teacher vs最强content-only | 对两主集最强content-only均无稳定改善，或提升只来自随机划分 |
| H2 | learned retrieval vs no/random/BM25/CLIP-kNN；AURC/ECE | 随机检索同样好，或跨话题/平台下校准和分布误差更差 |
| H3 | 全模态、单模态、随机/自然缺失 | 不优于简单late fusion、zero-fill或近期缺失模态基线 |
| H4（增强） | NEmo+上的`p_TI-p_T`、`p_TI-p_I` | 无法超过独立预测两个分布后相减的简单基线；数据门不过则不启用 |

## 4. 指标、统计与成功门

- 主指标：Jensen–Shannon divergence。冻结后不得因test表现更换。
- 分布辅指标：NLL、Wasserstein/EMD。
- 可靠性指标：Brier、ECE/ACE、risk-coverage、AURC；AUGRC若采用只能作为预注册补充。
- 二分类兼容指标：Macro-F1、Balanced Accuracy、AUPRC、Recall；不替代分布主任务。
- 正式统计：至少5个种子；视频/帖子级paired bootstrap 95% CI；配对检验和多重比较校正。
- 主成功门：两个公开人工主集上，主要分布指标对最强公平baseline有视频级区间支持且校准不恶化；或形成“分布误差不劣、OOD校准/选择性风险更优”的清晰Pareto优势。单个随机split高分不算成功。

## 5. 全局硬失败

- 任一目标评论、未来互动、未来候选、跨split实体、test拟合或全图穿越检查失败：运行标为`LEAKAGE_BLOCKED`，结果禁止进入论文证据。
- 第二人工多模态公开主集未冻结：G1保持`BLOCKED`，不创建M3正式baseline任务。
- 银标或自动/LLM标签只能标`SILVER`，不得承担主测试真值。
- 任何变更RQ、C1—C3、H1—H4、主指标、split或标签窗口的请求必须新建v2并记录理由；不得原地改写v1。

## 6. 一致性结论

`research-question-v1.md`与`experiment-protocol-v1.md`的实质内容与总纲v1.5一致，本轮无需改主协议正文。查新只收紧表述上限：增加M2PKD、NEmo+、RAMER和选择性预测/缺失模态前作作为后续强制对照，不改变主指标和假设。
