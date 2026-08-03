# Task30 H1 开发报告

> 证据身份：`DEVELOPMENT_EVIDENCE_ONLY_H1_GATE_NOT_PASSED`  
> 自报裁定：`NOT_PASSED_MECHANISM_NOT_STABLE`  
> 时间点：`T0`  
> 正式 test：`TEST_ROWS_NOT_MATERIALIZED_OR_USED`  
> Task40：`NOT_CREATED/BLOCKED_NOT_AUTHORIZED`

## 1. 问题与权威边界

Task30只验证：训练期评论作为privileged supervision，是否改善推理期仅读取合法T0内容的student对未来受众公开表达反应分布的预测。Teacher/student与KD只是实现机制，不作为创新。本报告不是Task50五种子正式结果，也不能支撑论文性能claim。

G1保持`PASS`，G2 protocol/data保持`PASS_WITH_LIMITATIONS`，资产可采纳性保持`DEFERRED_ACCEPTED_RISK`，G3保持`PASS_WITH_LIMITATIONS`。I3D许可、官方revision、权利方包身份与fixity仍为`UNKNOWN`。VC-CSA仍永久`NON_T0/FORMAL_EVIDENCE_INELIGIBLE`。

未提交或再分发I3D数组、评论正文、用户标识、逐样本隐私预测、模型权重、凭据或本机绝对路径。没有使用闭源/付费LLM、远程GPU、对象存储或数据外传。

## 2. 数据、泄漏与teacher审计

- CSMV沿用Task20冻结的`group_by_video_v1`：5,698 train / 837 dev / 1,675 test。
- teacher只聚合5,698个train视频的74,727条合法反应；dev/test评论从未提供给teacher，也未写入训练记忆或产物。
- student训练与推理均只读取冻结I3D内容特征；正式test行没有materialize，未参与模型、温度、权重、阈值、早停、校准或超参选择。
- 类别计数：anger 1,130；anticipation 11,798；disgust 6,252；fear 1,543；joy 23,893；sadness 4,045；surprise 5,989；trust 20,076。按1%质量阈值没有稀疏类别。
- 每视频评论数：最小2、中位14、均值13.1146、最大20；1–2条评论的视频119个。缺失emotion标签1条、opinion标签5条，保留在审计并只从各自分母排除。
- teacher置信度定义为`ONE_MINUS_NORMALIZED_EMPIRICAL_ENTROPY`：最小0.0272、中位0.4754、均值0.4958、最大1.0。低/中/高三分位train teacher拟合JSD收益分别为0.04253、0.04797、0.05415，置信度与拟合收益Pearson相关为0.16516。该结果是`TRAIN_TEACHER_FIT_DIAGNOSTIC_NOT_DEV_STUDENT_SUBGROUP`，不能冒充dev student分层收益。
- 未知标签、缺字段、video/count错配、非有限值、未归一化分布或全缺失字段均fail closed。Task20冻结评测核心未修改。

## 3. 最小实现与公平比较

student是最小pooled-I3D content MLP；接口由`DatasetRuntimeSpec`和`configs/task30/dataset-contract-csmv-v1.json`提供dataset ID、动态类别顺序、split、item、target与response-count字段，不再由运行入口硬编码CSMV八类或字段名。模型head按数据集类别数构建；Video2Reaction只保留未来数据集特定head能力，不伪造评论teacher。

六个可部署比较行使用相同的12-trial student预算：hard label、soft distribution、ordinary KD、comment-privileged KD、mismatched-comment teacher control、soft Dirichlet。搜索空间为hidden dimension 128/256/512、dropout 0.1/0.3、learning rate 0.0003/0.001、temperature 1/2/4、KD weight 0.25/0.5/0.75，最多200 epochs、patience 20、batch 64；只按dev JSD→NLL→Brier→参数量→trial顺序选择。

teacher-only仅保留train diagnostic：`NOT_COMPARABLE_DEV_RESPONSES_PROHIBITED`。它不可部署，也不是可比dev上界。

## 4. seed 20260802完整开发搜索

干净代码提交`9adcc0a59d31d16c86e50891ff53fad916130f95`完成72个student trials和837条私有dev预测。入选指标如下：

| 方法 | JSD ↓ | NLL ↓ | Brier ↓ | ECE ↓ | ACE ↓ |
|---|---:|---:|---:|---:|---:|
| hard label | 0.180825 | 1.790076 | 0.239266 | 0.041093 | 0.045672 |
| soft distribution | 0.172843 | **1.703714** | 0.218402 | 0.048944 | 0.061966 |
| ordinary KD | 0.171793 | 1.712183 | 0.219297 | 0.041235 | 0.060414 |
| comment-privileged KD | **0.169667** | 1.723492 | 0.220087 | **0.028594** | **0.052400** |
| mismatched-comment control | 0.171766 | 1.714517 | 0.218371 | 0.044501 | 0.064686 |
| soft Dirichlet | 0.172688 | 1.706831 | **0.213503** | 0.072300 | 0.067911 |

privileged KD在该seed的主指标JSD更好，且ECE/ACE未恶化；但NLL/Brier差于soft baseline。Dirichlet相对softmax的JSD变化很小且校准明显变差，不能替代softmax默认head。

privileged teacher的train diagnostic为JSD 0.014677、ECE 0.347062。因其消费train privileged输入并在train诊断，该数值不能与dev student横向比较。

## 5. 三种子稳定性与机制负对照

seed 20260802选中的配置随后冻结。同种子重放只运行冻结配置；两个额外development seeds也不再调参。

| seed | privileged JSD | gain vs soft | gain vs ordinary KD | gain vs mismatch | ECE |
|---|---:|---:|---:|---:|---:|
| 20260802 | 0.169667 | +0.003176 | +0.002126 | +0.002100 | 0.028594 |
| 20260803 | 0.169030 | +0.003141 | +0.001716 | +0.001741 | 0.049316 |
| 20260804 | 0.170083 | +0.002883 | -0.000003 | -0.000304 | 0.032705 |
| mean | 0.169593 | +0.003067 | +0.001280 | +0.001179 | 0.036872 |

正gain表示privileged JSD更低。它相对soft为3/3正，但相对ordinary KD与mismatch只在2/3为正；第三seed没有正确评论的特异优势。三种子平均ECE为0.03687，未差于ordinary KD的0.04123或mismatch的0.03724，但校准不能挽救不稳定的机制归因。因此不能把soft-label/参数量/训练随机性收益写成评论privileged机制成功。

## 6. 评论数、分歧、噪声与错误边界

seed 20260802中，privileged相对soft的JSD收益按评论数为：1–2条`+0.02200`（n=15）、3–10条`+0.00470`（n=238）、11条以上`+0.00207`（n=584）。低评论组样本很小，只作描述。

目标混合度显示：低熵`+0.00890`（n=169）、mixed`+0.00547`（n=490），但高熵为`-0.00858`（n=178）。标签噪声代理的低/中/高三分位收益为`+0.00604/+0.00068/+0.00279`。这说明收益没有稳定解释高分歧样本。

讽刺固定为`NOT_EVALUABLE_DEV_RESPONSE_TEXT_UNREACHABLE`，不能打开dev评论正文制造定性案例。跨域H1固定为`NOT_APPLICABLE_NO_SECOND_COMMENT_BEARING_DATASET`；LAI-GAI只能提供内容/校准边界，不能冒充跨域评论机制错误分析。

## 7. 数据集适用性

- **CSMV：** H1适用，但本报告只有development evidence。
- **LAI-GAI：** 无评论字段，H1=`NOT_APPLICABLE_COMMENT_FIELD_UNAVAILABLE`。真实T0图像内容边界为594 train / 127 dev；softmax JSD 0.054140、Dirichlet 0.054456、train overall-mean 0.074507，ECE约0.233/0.254，只能说明内容/校准边界。
- **Video2Reaction原生：** H1=`NOT_APPLICABLE_DATA_NOT_RELEASED`；未从派生分布反推或伪造评论teacher。
- **第二个comment-bearing公开集：** `NOT_EVALUABLE_DATA_NOT_RELEASED`。这不是可由Task30代码补齐的实验缺口。

## 8. 冻结与复现身份

tracked非敏感冻结位于`experiments/task30-h1-development-v1/`。私有预测、完整epoch日志和六个入选模型state只保留在Git-ignored本地run目录，禁止提交、发布或再分发；tracked层仅保留哈希。

| 身份 | SHA-256 |
|---|---|
| full manifest | `97d50c320eda6eec6c6bf8fa44d36b17b0fe3d64dd444fee43fed0ee930b6ce0` |
| full aggregate | `70c6275693ced69f9955e370e2af9a3b87497358ec781487998628a659e5d1f8` |
| same-seed replay manifest | `145b7a222d4158a402ddc7499a9137fa7785225b1221f03b9ab95843d81f20bc` |
| seed-20260803 manifest | `41295136f5e890a4adce2353e5e4dbd763f53c6e42104b4853ea311378a3ff6b` |
| seed-20260804 manifest | `53ad21a9c2fb3173f70520e210632a0b1aaa4207719ae7aaecca16c5eb115a4b` |
| same-seed private predictions | `195e60290d867ca2ce75be75830bffb4bd808228f0786b9f65deb019e5ade53a` |
| model hash index | `7bd83b2b4bfba03f3d8b42eaf85c3bf44aa631e1e84480e074cf9a8e184d5085` |
| full training history（2473行） | `cdb09668b0587a9069e81963cd07f3e289b305dc79f34e111735ef4d28db0ade` |

full与same-seed replay的预测逐字节一致，六个模型文件hash与canonical tensor hash全部一致，六行dev指标全部一致。full manifest记录`dirty=false`、精确commit、开始/结束时间、完整argv、exit code 0、72-trial矩阵身份、输入/代码hash和`test_adaptation=false`。所有运行为本地RTX 3070 Ti；未租用大算力，完整搜索约32分40秒。

## 9. 总纲第5节第1–16项闭合表

| 项 | 状态 | 证据/边界 |
|---:|---|---|
| 1 | COMPLETE | Task20 split、指标、预算冻结未改 |
| 2 | COMPLETE | teacher仅train评论；dev/test评论不可达 |
| 3 | COMPLETE | 评论级标签编码、视频级聚合、评论数与经验置信度审计 |
| 4 | COMPLETE | 类别质量/稀疏、评论数偏差、缺失异常、置信度统计已冻结 |
| 5 | COMPLETE | content-only student训练/推理只读T0内容 |
| 6 | COMPLETE | softmax与最小Dirichlet公平比较 |
| 7 | COMPLETE | 普通KD/privileged KD损失、温度、权重与dev选择范围明确 |
| 8 | COMPLETE_WITH_BOUNDARY | 六行公平比较完成；teacher-only仅train diagnostic，不伪造dev上界 |
| 9 | COMPLETE_WITH_BOUNDARY | 评论数、置信度、噪声分析完成；置信度只允许train teacher诊断 |
| 10 | COMPLETE | 去teacher语义行、ordinary KD、mismatch E3和参数/预算公平控制完成 |
| 11 | COMPLETE | 分布、有限值、梯度与完整2473行epoch历史冻结；模型state仅本地私有 |
| 12 | COMPLETE_WHERE_APPLICABLE | CSMV完成；LAI-GAI只做真实内容/校准边界；第二评论集未发布，不能伪造 |
| 12a | COMPLETE | 配置驱动动态class/field/head接口；V2R H1固定N/A |
| 13 | COMPLETE_WHERE_EVALUABLE | 混合、少评论、高分歧、噪声已聚合；讽刺/跨域评论案例受政策与数据限制N/A |
| 14 | COMPLETE | 三种子ECE/ACE审计；校准未恶化但不替代机制稳定门 |
| 15 | COMPLETE | tracked配置/聚合/hash冻结；私有预测、历史、六个state在ignored run中冻结 |
| 16 | TASK30_SELF_REVIEW_COMPLETE_EXTERNAL_REVIEW_REQUIRED | 自报`NOT_PASSED_MECHANISM_NOT_STABLE`；00独立审核不可由Task30代行 |

## 10. 开发门裁定与剩余限制

Task30自报：`NOT_PASSED_MECHANISM_NOT_STABLE`。

结果不是`H1_SUCCESS`：相对soft的总体收益稳定，但正确train评论相对ordinary KD与错配评论的特异优势不稳定，高分歧组也恶化。结果也不是formal-test上的`H1_REJECTED`，因为正式test、Task50五种子统计与第二comment-bearing公开集均未运行。

以下不是未做的Task30实现工作，而是精确外部/N/A边界：

- 00独立裁定：`EXTERNAL_REVIEW_REQUIRED_NOT_SELF_APPROVABLE`；
- 第二comment-bearing公开集：`NOT_EVALUABLE_DATA_NOT_RELEASED`；
- teacher-only dev上界：`NOT_COMPARABLE_DEV_RESPONSES_PROHIBITED`；
- 讽刺：`NOT_EVALUABLE_DEV_RESPONSE_TEXT_UNREACHABLE`；
- 跨域H1：`NOT_APPLICABLE_NO_SECOND_COMMENT_BEARING_DATASET`；
- Video2Reaction H1：`NOT_APPLICABLE_DATA_NOT_RELEASED`。

在00新书面授权前，Task30停止调参、不查看test、不进入Task40/50。
