# StepFun 大模型情绪元标注 Smoke Test

实验日期：2026-07-09  
脚本：`D:\MMSA-CH-SIMS\run_stepfun_llm_emotion_student.py`  
结果文件：`D:\MMSA-CH-SIMS\experiments\stepfun_llm_emotion_student\stepfun_llm_student_results.json`  
缓存文件：`D:\MMSA-CH-SIMS\experiments\stepfun_llm_emotion_student\llm_annotations.jsonl`

## 1. 实验目的

验证 StepFun API 能否用于“大模型辅助情绪元标注 + 轻量学生模型”。

本次不是最终论文实验，只是最小可行性测试：

```text
视频评论
↓
StepFun LLM 输出视频级情绪元 JSON
↓
情绪元特征与原48维特征融合
↓
CatBoost 学生模型
↓
极端群体情绪二分类
```

## 2. StepFun 接入情况

已验证：

- Chat Completions API 可用；
- `step-3.7-flash` 可以返回 JSON；
- 需要使用英文极简提示，中文严格 JSON 提示不够稳定；
- `max_tokens` 需要放大，否则模型可能只输出 reasoning，正文 JSON 为空或不完整；
- 已加入本地 JSONL 缓存，避免重复消耗额度。

安全提醒：API key 已经出现在聊天中，建议实验完成后在 StepFun 平台重新生成密钥。

## 3. 大模型情绪元字段

当前让 LLM 输出 7 个视频级情绪元：

| 字段 | 含义 |
|---|---|
| polarity_pos | 正向情绪程度 |
| polarity_neg | 负向情绪程度 |
| intensity | 情绪强度 |
| aggressiveness | 攻击性/敌意 |
| sarcasm | 讽刺/调侃 |
| controversy | 争议程度 |
| confidence | 模型置信度 |

## 4. 小样本结果

样本数：20 个视频  
标签分布：0 类 10 个，1 类 10 个  
测试集：约 6 个视频  

由于测试集极小，下面结果只能说明流程可跑通，不能作为论文正式结果。

| 输入特征 | Accuracy | Precision | Recall | F1 Score |
|---|---:|---:|---:|---:|
| 原始48维 | 33.33% | 0.00% | 0.00% | 0.00% |
| LLM情绪元 only | 50.00% | 50.00% | 33.33% | 40.00% |
| 原始48维 + LLM情绪元 | 66.67% | 100.00% | 33.33% | 50.00% |

## 5. 初步判断

这次实验说明：

1. StepFun API 可以接入当前项目；
2. LLM 可以输出结构化情绪元；
3. 情绪元特征能够进入学生模型训练流程；
4. 小样本上“原48维 + LLM情绪元”优于单独原48维，但样本太小，不能下正式结论。

## 6. 下一步

建议下一步扩大到至少 200 个视频：

1. 保持当前 JSONL 缓存；
2. 每个视频抽取高赞评论 + 早期评论；
3. 标注 200 个视频；
4. 用固定 80/20 划分评估：
   - 原48维；
   - 规则情绪元；
   - StepFun LLM情绪元；
   - 原48维 + StepFun LLM情绪元；
5. 若 200 视频仍有提升，再扩展到全量。

目前阶段可以在论文中写成：

> 初步小样本实验验证了大模型情绪元标注模块的可行性。后续将扩大标注规模，并通过轻量学生模型验证其对群体情绪预测的增益。
