# 公开数据标签空间映射草案

> 版本：draft-v0.1
> 日期：2026-07-14
> 状态：只用于M1选择门与损失审计；不是冻结的`label-provenance-v1`。

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

正式映射冻结前必须先确定第二主集、统计单位、类别保留策略与主指标；不得查看test结果后改变映射。
