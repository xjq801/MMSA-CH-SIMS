# CUC-IGPE-v2 canonical 审计 v1

## Canonical结果

- 当前可复跑向量行：2,787；历史口径：2,815；差异28条因缺少历史原始manifest保持`UNRESOLVED_NO_2815_MANIFEST`。
- 2,779条具有唯一可解析BV，8条缺BV；当前向量表中精确重复BV为0。
- 2,772条能在同发布者目录匹配本地标签，其中2,551条与向量二分类标签一致；其余221条置`label_conflict=true`，不自动删除或重标。
- 发布时间覆盖883/2,779个BV；2,787条canonical中1,904条缺时间。883条中有1条只可通过跨发布者目录匹配，已置`timestamp_scope=GLOBAL_CROSS_PUBLISHER`作为捷径/lineage警告。
- 48维遗留向量含播放量和热度类字段，采集时点未证明为T0，因此`legacy_features_available_at_t0=false`。

## 标签与许可定位

该表物理位于`data/processed/SILVER/cuc_igpe_v2/`，不进入Git；小型hash/统计清单位于`data/manifests/cuc-canonical-v1.manifest.json`。教师快照和置信度未知，许可及再发布范围未澄清，因此只允许本地辅助审计，不得替代公开人工金标或进入公开数据发布。

## 未解决项

1. 找回2,815版本原始manifest才能解释28条漂移。
2. 221条冲突需要按`LABEL_ERROR_REVIEW_PROTOCOL.md`人工裁定；当前只抽取100条候选，不形成模型结论。
3. 时间缺失不能用文件顺序回填；T+Δ继续禁用。
