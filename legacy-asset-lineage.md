# 现有代码—数据—结果 Lineage

> 版本：v1.0
> 冻结日期：2026-07-14
> 范围：总纲第17节任务10步骤6；只审计既有资产，不认可其为新论文证据。

## 1. 数据节点

| 节点 | 位置/来源 | 当前可复核状态 | 关键风险 |
|---|---|---|---|
| LEGACY-CUC-RAW | `D:\李佳怡毕业论文配套代码\极端群体情绪预测数据集` | 5话题、45发布者目录；44套标签/视频列表/向量文件 | 原始评论敏感；许可、可发布范围未完成；不是Git资产 |
| LEGACY-CUC-LABEL | 每个发布者的`3.视频群体情绪值对应.csv` | 13794行；2665行显式二分类，11129行由旧阈值派生 | 982条显式标签与旧阈值不一致；同BV多行 |
| LEGACY-CUC-VECTOR | 每个发布者的`5.预测向量.csv` | 2787条有效48维记录；2779个非空且唯一BV；8条缺BV | 字段含播放量、热度等非T0特征；当前版本与论文2815条相差28条 |
| LEGACY-CUC-TIME | 每个发布者的`6.发布者视频列表.csv` | 883/2779个向量BV可全局关联发布时间 | 不足以支持全量严格时间协议；缺失时不得用文件顺序冒充时间 |
| LEGACY-CUC-COMMENT | 每个发布者的`1.评论数据*.csv` | 含目标评论、评论时间、评论点赞、用户和最终互动字段 | 仅可作标签/训练期特权监督；不得进入T0学生输入或公开仓库 |
| CH-SIMS-PROCESSED | `data/SIMS/Processed/unaligned_39.pkl` | 本地存在，SHA-256见`DATA_SOURCE_LEDGER.md` | 说话者情感构念，不是公众诱发受众情绪主真值 |

## 2. 2787/2815漂移与221冲突

2026-07-14只读复跑：

```powershell
.\.venv\Scripts\python.exe audit_group_dataset.py "D:\李佳怡毕业论文配套代码\极端群体情绪预测数据集"
```

得到以下可重复计数：

- 当前有效向量记录：2787；论文/总纲记录版本：2815；漂移：28条。
- 2787条中有BV的记录为2779条，且BV唯一；另有8条缺BV。
- 2772条向量能匹配同发布者标签记录；其中2551条二分类标签一致，故冲突为`2772-2551=221`条。
- 另有7条非空BV缺少同发布者标签匹配；因此221只表示“可匹配记录中的标签不一致”，不是全部数据异常数。
- 当前没有论文2815条原始manifest，28条差异的删除、过滤或缺失原因保持`UNKNOWN`；不得混用两个版本。

## 3. 代码—数据—结果链

| Lineage ID | 代码入口 | 读取数据/特征 | 结果位置 | 已知协议问题 | 当前用途 |
|---|---|---|---|---|---|
| LG-01 | `audit_group_dataset.py` | LEGACY-CUC的标签、向量、视频列表，只读取计数/ID | 终端审计；`group_dataset_audit.md`为历史摘要 | 无正式canonical输出；未解析2815版本 | 可复用审计代码 |
| LG-02 | `diagnose_catboost_self_built.py` | 48维向量及二分类标签 | `experiments/catboost_diagnosis/*.json`、`catboost_diagnosis_report.md` | 随机80/20；48维含未来播放量/热度；数据版本为2787 | 历史诊断，不进新论文主证据 |
| LG-03 | `run_self_built_mw_ep_tabular.py` | 2787条48维与旧硬标签 | `experiments/self_built_dataset/tabular_mw_ep/results.json` | 同上；构念仍是旧二分类 | 代码候选，结果仅探索 |
| LG-04 | `run_llm_ready_emotion_student.py`、`evaluate_stepfun_llm_cache*.py` | 48维 + 目标视频评论内容/评论点赞 | `experiments/llm_ready_emotion_student/results.json`及StepFun缓存结果 | 目标评论泄漏；固定随机split；银标/模型输出与旧硬标签循环 | 结果禁止作为T0证据；评论处理代码仅可迁移到train teacher |
| LG-05 | `run_stepfun_llm_emotion_student.py` | 目标视频高赞评论、48维、旧标签 | `experiments/stepfun_llm_emotion_student/*` | 195条子集；目标评论；闭源API缓存；旧随机split | 仅教师/银标管线历史参考，结果禁止 |
| LG-06 | `run_bert_text_fusion_experiment.py` | 标题/标签/简介 + 目标高赞评论 + StepFun情绪元 + 48维 | `experiments/bert_text_fusion/*.json`、相关报告 | `make_text`明确拼接“代表评论”；固定70/30；195条 | 结果禁止；冻结BERT/PCA代码可拆出复用 |
| LG-07 | `run_catboost_llm_temporal.py`、`run_llm_temporal_gnn.py` | 48维 + 由目标评论产生的LLM情绪元 + 缺失时间/文件顺序 | 对应`experiments/*_temporal*`与报告 | 目标评论泄漏；时间戳缺失；随机split；Temporal/GNN偏离主线 | 仅探索结果，不能进入新证据 |
| LG-08 | `run_temporal_gnn.py` | 48维、发布者、发布时间或行顺序 | `experiments/temporal_gnn/*`、`temporal_gnn_report.md` | 随机80/20；缺失时间回退文件顺序；48维含未来字段 | 仅探索结果 |
| LG-09 | `run_propagation_gcn.py` | 48维 + 评论用户名构建视频关系图 | `experiments/propagation_gcn/*`、`propagation_gcn_report.md` | 读取目标评论用户；可能先全图后split；随机split；第三章传播构念 | 结果禁止进入第四章新证据 |
| LG-10 | `run_formal_hgb_catboost_comparison.py` | 195条缓存节点、48维、发布者与时间字段 | `experiments/formal_hgb_catboost/*`、比较报告 | 随机CV；所谓时间划分受全0/缺失时间影响；样本小 | 历史模型比较，不作正式优越性证据 |
| LG-11 | `run_my_catboost_on_sims.py`、`run_self_mm*_sims.py`、`MMSA/` | CH-SIMS processed说话者多模态情感 | `results/`、`saved_models/`及Self-MM报告 | 构念不匹配；不能替代受众反应数据 | 可复用公开基线代码；结果仅历史参照 |

## 4. 明确的泄漏证据

- `run_bert_text_fusion_experiment.py:106-119`读取评论点赞和评论内容，并把高赞目标评论拼入模型文本；同文件`160`行把该文本写入样本。
- `run_llm_ready_emotion_student.py:81-122`按目标BV读取评论并生成情绪元，随后用固定随机split评测。
- `run_stepfun_llm_emotion_student.py:84-120`选择目标视频高赞评论送入规则/LLM标注管线。
- `run_propagation_gcn.py:85-95`读取评论用户名构图；若对全量数据构图后再划分，会产生跨split信息通道。
- 48维向量表头包含播放量和热度系列；其采集时点没有证明等于发布时T0，按`T0_INPUT_POLICY.md`默认禁止。

## 5. Lineage使用规则

1. 旧代码可以拆分复用，但新入口必须接受版本化配置并通过T0字段、group split、train-only fit/index测试。
2. 旧结果不能因脚本可运行而升级为正式证据；证据资格由`legacy-experiment-classification.md`决定。
3. 任何正式数据必须另建immutable manifest、hash、字段可用时点和衍生链；本文件不是dataset-v1 manifest。
4. 未找到2815原始manifest、28条差异去向和221条逐行冲突清单前，CUC-IGPE-v2保持`UNKNOWN/辅助外验`，不承担G1人工金标。
