# G1/G2逐条证据矩阵

> 审核对象：任务10 / M1—M2
> 版本日期：2026-07-14
> 总体结论：G1=`BLOCKED`；G2=`NOT_ELIGIBLE/ BLOCKED`。本地泄漏门通过不能替代阶段门。

## G1（最低合格）

| 总纲条件 | 状态 | 证据 | 判定依据/缺口 |
|---|---|---|---|
| 两个合法可用公开数据源 | **FAIL** | `DATASET_SELECTION_DECISION.md`、`DATA_SOURCE_LEDGER.md` | CSMV人工标注可用；iNews与NEmo+均No-Go，第二人工主集不存在 |
| CSMV可按视频分组 | **PASS** | `csmv-primary-raw-v1.manifest.json`、`csmv-split-v1.manifest.json`、`M2_LEAKAGE_AUDIT.md` | 107267条正式评论归属8210视频；视频组跨split交集为0 |
| 第二主集已冻结 | **FAIL** | `second-primary-label-map-v1.manifest.json` | `BLOCKED_SECOND_PRIMARY_NOT_FROZEN`；不得以CUC银标替代 |
| 自建时间可恢复或明确降级 | **PASS_WITH_LIMITATION** | `cuc-canonical-v1.manifest.json`、`CUC_CANONICAL_AUDIT.md` | 仅883/2787有时间；1904缺失，已明确降级为本地辅助且不发布time split |

**G1总判定：`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`。** 不满足“两个合法公开人工主集”和“第二主集冻结”。

## G2/L2（论文证据级）

| 总纲条件 | 状态 | 证据 | 判定依据/缺口 |
|---|---|---|---|
| 100%样本可追溯 | **PARTIAL/BLOCKED** | CSMV/CUC raw manifest、canonical manifest | 当前CSMV与CUC候选可追溯；第二主集缺失，CUC历史2815版本无manifest且许可未知 |
| 人工标签与银标物理隔离 | **PASS** | 三个tier manifest、`load_label_tier.py` | 目录、manifest、加载入口独立；混装负测拒绝 |
| test评论与输入物理隔离 | **PASS_CURRENT_CSMV** | `human-gold-v1.manifest.json`、泄漏报告 | 派生记录不含评论正文/目标评论字段；评论仅作标签聚合 |
| 正式split泄漏测试零失败 | **NOT_ELIGIBLE** | `leakage-audit-v1.manifest.json`、`split-v1.manifest.json` | 当前本地候选自动门零Critical，但`formal_split=false`；第二主集和语义近重复/发布者审计仍开放 |
| 预处理可从manifest重跑 | **PASS_LOCAL_ISOLATED** | `reproducibility-v1.manifest.json` | 标准库脚本以`-I -S`隔离进程重跑，受检输出hash一致；不是新OS/container安装证明 |

**G2总判定：`NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`。** 当前只能确认本地候选的自动化与物理隔离，不得进入任务20。

## 止损执行

- 不训练模型、不建立正式索引、不创建任务20。
- 不下载媒体/大数据、不购买资源、不调用API或付费LLM。
- 不把银标写成人工金标，不把`NOT_APPLICABLE`时间检查写成时间安全PASS。
- 下一可执行动作由00任务决定：批准审计新的第二人工多模态主集，或维持G1阻塞。
