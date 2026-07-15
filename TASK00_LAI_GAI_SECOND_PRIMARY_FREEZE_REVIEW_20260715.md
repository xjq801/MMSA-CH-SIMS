# 任务00：LAI-GAI第二人工跨域图像主集冻结复审

> 复审编号：`REVIEW-00-LAI-GAI-FREEZE-20260715`  
> 复审日期：2026-07-15  
> 授权依据：`AUTH-00-SECOND-PRIMARY-RESOLUTION-20260714`  
> 范围依据：`SC-20260714-01`

## 1. 正式裁定

1. **批准冻结LAI-GAI为第二人工跨域图像主集/自然缺失模态验证集。** 状态为`FROZEN_00_APPROVED`。
2. **唯一权威版本**是`LAI-GAI@v05-2026-03-11`、847图、63,682条合规人工响应、379个source group、train/dev/test=`594/127/126`。早先试算的266组、`573/148/126`及`official-web` canonical不是正式版本，相关冲突manifest已删除。
3. **G1通过。** 两个合法可用公开人工数据源、CSMV视频分组、第二主集冻结和自建时间降级四项均满足。
4. **G2不通过。** 状态为`BLOCKED_CSMV_MEDIA_MAPPING_AND_GLOBAL_SEMANTIC_AUDITS`：CSMV URL表仍有2,644行ID—路径ID错配及200行URL重复，全局100%媒体lineage和正式split条件未闭合。
5. **全局`formal_split=false`保持不变。** LAI-GAI自己的379组split为正式冻结split；这不等于整个dataset-v1已经达到G2。
6. **不创建任务20、不训练、不建正式索引。** 只有CSMV媒体映射与剩余全局语义审计关闭、G2再经00书面通过后，才可创建任务20。

## 2. 冻结证据

- 847/847官网图像、人工评分、canonical、split和逐图SHA-256闭合；图像全部可解码。
- HUMAN_GOLD仅来自六项独立人类诱发情绪研究；逐图响应数58—96。
- 12个1—7人工强度维度减去量表下界1后归一化为概率分布；保留逐维N、样本SD、SE和1—7直方图。
- prompt、目标生成类别和生成模型信息不作真值且不进入T0模型输入。
- source item、文化/性别/年龄变体、相同prompt hash、精确重复和dHash近重复合并为379组；group、精确重复、近重复跨split均为0，三个split均覆盖12类。
- canonical SHA-256：`ad58c268e34adf02bd8e639338069d34576e1d9602f819a2cc6fa89be6836818`。
- `scripts/build_lai_gai_second_primary.py`重建exit 0；`scripts/validate_lai_gai_second_primary.py`输出`LAI_GAI_SECOND_PRIMARY_READY`、exit 0。

## 3. 历史证据处理

旧OSF API授权中的0.996519秒速率偏差和`K8XVH`空文件列表继续作为`OBSERVED_WITH_PROTOCOL_DEVIATION_NO_GATE_CREDIT`保留，不追溯豁免、不改写。此次冻结依据是后续独立授权下的官网847图资产链、官方Data Card/CC BY 4.0说明、评分组件固定hash和新建的完整lineage；它不复用旧失败授权的门信用。

## 4. 研究边界

LAI-GAI只支持跨域图像、自然缺失音频/视频、校准/OOD和H3边界验证，不冒充第二视频集，也不承担缺少评论和历史案例字段的H1/H2机制证据。原始图片、逐人响应、参与者标识和人口统计继续留在Git忽略区；仓库只跟踪代码、脱敏manifest和审计文档。

