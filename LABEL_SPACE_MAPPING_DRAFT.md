# 公开数据标签空间映射草案

> 版本：v1.0-frozen
> 日期：2026-07-15
> 状态：CSMV历史映射保留；LAI-GAI映射已由00正式冻结，机器权威见`lai-gai-label-provenance-v1.manifest.json`。

## 1. 映射原则

1. 保留各数据集原生分布作为第一表示，不为追求跨数据可比性强行合并构念。
2. 跨数据离散情绪只采用语义直接等价的`audience_affect_direct6_v0`：`joy`、`anger`、`fear`、`sadness`、`disgust`、`surprise`。
3. `happy→joy`、`sad→sadness`仅做词面同义映射；其余类别不凭主观判断并入相近类。
4. 丢弃不可映射标注会改变分布并造成选择偏差；所有损失必须同时报告行/反应数和内容单元数。
5. VAD保留为连续1—7标度，不在本草案中以阈值离散化。

## 2. 类别映射

| 数据源 | 原始类别 | direct6映射 | 处理 |
|---|---|---|---|
| CSMV | joy | joy | 直接保留 |
| CSMV | anger / fear / sadness / disgust / surprise | 同名 | 直接保留 |
| CSMV | trust / anticipation | `UNMAPPABLE` | 不强行并入positive或joy |
| CSMV | emotion=`None` | `INVALID_PENDING` | 1条，需数据质量规则处理 |
| iNews | happy | joy | 词面同义映射 |
| iNews | sad | sadness | 词面同义映射 |
| iNews | anger / fear / disgust / surprise | 同名 | 直接保留 |
| iNews | contempt / neutral / other | `UNMAPPABLE` | 保留原生空间；不强行映射 |
| NEmo+ | Anger / Fear / Sadness / Disgust | 对应小写同名 | 直接保留 |
| NEmo+ | Amusement / Awe / Contentment / Excitement | `UNMAPPABLE` | 不将awe或contentment强制等同joy |
| LAI-GAI | 12个1—7强度：amusement/awe/anger/attachment love/craving/disgust/excitement/fear/joy/neutral/nurturant love/sadness | 12维连续分布 | 每维均值减量表下界1后归一化；不压缩到direct6主目标 |

CSMV的opinion positive/neutral/negative是独立三极性任务，可保留为数据集内兼容目标；它不与iNews的VAD或NEmo+八类自动等价。

## 3. 映射损失

| 数据源 | 总标注/反应 | direct6保留 | 丢弃 | 保留率 | 内容单元额外损失 |
|---|---:|---:|---:|---:|---:|
| CSMV正式split | 107,267 | 61,684 | 45,583 | 57.51% | 待视频聚合后计算；不得按评论随机丢弃后直接作视频真值 |
| iNews public | 11,320 | 7,024 | 4,296 | 62.05% | 227/2,736个post没有任何direct6标注 |
| NEmo+ T/I/TI合计 | 38,910 | 23,971 | 14,939 | 61.61% | 待按news item×condition聚合后计算 |

iNews的不可映射行占37.95%，且8.30%的post会完全消失；因此direct6不能替代iNews原生九类/VAD作为主标签，只能作为预注册后的跨数据敏感性分析。NEmo+同理。

## 4. 构念差异

- CSMV是评论者对视频的人工意见/情绪标注，再聚合为视频级公众反应；评论在T0后产生，只能作标签。
- iNews是受试参与者看到新闻帖截图后的个体VAD/离散反应，具有实验标注者与模态条件；不是平台自然评论分布。
- NEmo+是受试者在T、I、TI三种实验条件下的诱发情绪，主题集中于美国枪支暴力新闻；其条件差分有独立科学含义。
- MVIndEmo是评论模型推断并按点赞加权的自动聚合，不属于人工金标空间。
- LAI-GAI是独立受试者对单图的诱发情绪强度，属于跨域图像`HUMAN_GOLD`；prompt与目标类别仅描述生成意图，不能替代人类反应。

LAI-GAI映射版本固定为`lai-gai-label-map-v1`，主指标保持Jensen–Shannon divergence；任何修改必须形成新版本，禁止查看test结果后改变映射。
