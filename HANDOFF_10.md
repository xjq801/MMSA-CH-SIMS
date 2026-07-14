# HANDOFF_10：M1—M2数据与协议交接

> 提交给：任务00总控审核
> SSOT：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.5 第17节任务10
> 交接日期：2026-07-14
> 提交状态：已发送至任务00（源任务`019f5c27-10fa-7e13-857d-77505594f7fc`），等待审核结论

## 请求的审核结论

请任务00确认以下状态，而不是放行任务20：

- 步骤34—39本地可执行交付是否达到任务10文档与自动化要求；
- G1继续`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`；
- G2继续`NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`；
- 是否授权下一轮只读审计一个新的、现成的、多人类标注且媒体/许可可复现的第二主集候选。

## 本轮交付

- 可阻断泄漏门：`scripts/run_m2_leakage_tests.py`；负面自测会产生预期`LEAKAGE_BLOCKED`。
- 受门控发布构建器：`scripts/build_m2_release.py`；泄漏失败时不写release manifest。
- 版本化候选：`dataset-v1.manifest.json`、`split-v1.manifest.json`、`label-provenance-v1.manifest.json`。
- 数据文档：Data Card、Datasheet、隐私、平台条款、发布边界、数据审计报告。
- 隔离复现：`scripts/reproduce_m2_minimal.py`与`reproducibility-v1.manifest.json`。
- G门证据：`G1_G2_EVIDENCE_MATRIX.md`。

## 关键结果

- CSMV：8210视频、107267条正式评论反应；当前两套视频/hashtag split无自动检查到的实体交叉。
- CUC：2787条银标，221冲突、8缺BV、1904缺时间、历史漂移28，许可未知；仅辅助、本地。
- 泄漏自动门覆盖ID、source group、评论—视频归属、目标评论、未来候选、train-only索引、time split合同和fit范围。
- 时间检查为`NOT_APPLICABLE_NO_TIME_SPLIT`，因为CSMV无发布时间；不能解释为已证明时间安全。
- 语义近重复、同源事件与发布者捷径因媒体/元数据不足仍是开放风险。

## 禁止下游动作

在任务00明确通过G1/G2以前，不创建任务20、不启动M3训练、不安装faiss以宣称正式环境就绪、不构建正式检索索引，也不把本地候选写成正式benchmark。

## 建议决定

维持G1/G2阻塞；将“冻结第二人工多模态主集”作为唯一优先解阻动作。若没有合法且媒体可复现的现成候选，应记录止损并暂停模型主线，而不是用CUC/MVIndEmo银标补位。
