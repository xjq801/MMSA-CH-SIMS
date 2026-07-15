# LAI-GAI第二人工跨域图像主集正式冻结报告

> 状态：`FROZEN_00_APPROVED`；00复审见`TASK00_LAI_GAI_SECOND_PRIMARY_FREEZE_REVIEW_20260715.md`。G1已通过；G2与全局`formal_split=false`因CSMV媒体映射继续阻塞。

## 准入结论

- 官方图像与人工评分闭合：847/847（100%）。
- 有效逐图人工反应：63682；每图反应数58—96。
- 每维有效N范围：54—96；原始参与者标识未进入canonical或tracked manifest。
- 真值仅来自独立人类诱发情感评分；prompt、目标类别和生成模型字段只作provenance并禁止进入主输入。
- 图像与元数据许可：官方Data Card和OSF组件均定位为CC BY 4.0；原始资产保留于Git忽略目录。

## 标签与构念

- 12个1—7连续人工强度维度先减去量表下界1，再在12维归一化为连续分布；主指标保持Jensen–Shannon divergence。
- 每维保留N、样本标准差、标准误和1—7直方图，不把均值伪装成单一人工类别。
- 本集角色限于图像跨域、缺失模态、校准/OOD与H3边界；H1/H2为`NOT_APPLICABLE_BY_DESIGN`。

## Split与泄漏

- group数：379；最大group：21；split={'dev': 127, 'test': 126, 'train': 594}。
- 精确重复对：94；dHash近重复候选对：137；全部并入同一source group后再划分。
- source数据库、文化/性别/年龄变体、相同prompt hash、精确和近重复均禁止跨split。

## 已知限制

- 原始`is_AI`与最终清单冲突图像：49；以最终847图清单为准并保留冲突标志。
- 生成式图像不代表真实社交媒体视频；仅作为批准的跨域图像/缺失模态验证集。
- 00已书面裁定G1=`PASS`；后续复审已接受CSMV lineage/split修复并关闭公共核心复现陈旧子阻塞，但G2仍因正式输入资产准入为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`，全局`formal_split=false`。本任务未创建任务20、未训练模型。
