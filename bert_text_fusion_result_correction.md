# BERT 融合结果勘误（2026-07-10）

以可追溯的 `D:\MMSA-CH-SIMS\experiments\bert_text_fusion\bert_text_fusion_results.json` 为准，HGB 的 `48维 + LLM情绪元 + Temporal + BERT文本` 当前应报告为：Accuracy 94.92%、Precision 93.55%、Recall 96.67%、F1 95.08%。旧报告中出现的 96.61%/96.67% 属于旧版本残留。

同一随机划分下，HGB 的 `48维 + LLM情绪元 + Temporal` 为 Accuracy 98.31%、F1 98.31%；CatBoost 对应为 Accuracy 96.05%、F1 96.14%。由于目前只有一个固定的 70/30 划分、195 个视频，且模型随机种子没有改变测试集，暂时只能说 HGB 在这次探索性划分上更高，不能据此断言其在整个数据集上优于 CatBoost。

正式比较应补做：重复分层划分或 5 折交叉验证、时间划分、发布者分组划分，并统一特征构造和时间口径。
