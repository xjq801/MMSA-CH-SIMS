# 任务10第二人工主集只读审计回交

> 授权：`AUTH-00-M1-SECOND-PRIMARY-READONLY-20260714`
> 回交日期：2026-07-14
> 建议00结论：维持G1/G2阻塞，不授权下载或任务20/M3。

## 已完成

- 形成恰好3个候选的元数据短名单：LIRIS-ACCEDE、PMEmo、Emotion6。
- 仅深入审计LIRIS-ACCEDE，覆盖source、revision、license、size、split、media、multi-annotator、T0和construct mapping。
- 记录ArtEmis为短名单外预筛项，未扩张到第4个短名单候选。
- 未下载任何数据、媒体、特征或小型元数据包；未使用登录态/API/付费服务、绕过gating或联系作者。

## 逐项回交摘要

| 证据项 | LIRIS-ACCEDE深审结果 |
|---|---|
| source | 官方站、database页、官方EULA、作者公开IEEE TAC论文 |
| revision | 实时站点无数据版本号/manifest/hash；`UNKNOWN` |
| license | 媒体逐源电影CC；annotations/描述CC BY-NC-SA 3.0；EULA限学术、禁再分发 |
| size | 9800片段、26:57:08；下载包字节数`UNKNOWN` |
| split | Protocol A按电影80/80隔离，训练可按40/40再分；未包级复现 |
| media | 8—12秒CC电影视听片段；逐片段许可在受限XML中，尚未核 |
| multi-annotator | valence 1517名、arousal 2442名trusted annotator；只发布最终VA秩 |
| T0 | 片段内AV可定义T0；源电影ID/位置、标签、GSR和全库拟合特征禁止 |
| construct | felt/induced VA高度匹配；但不是离散公众分布，无法无损接入JS divergence主任务 |

## 裁定

LIRIS-ACCEDE为`NO_GO_CURRENT_AUTHORIZATION_EULA_CONTACT_REQUIRED`，且存在标签形态不匹配；PMEmo为`NO_GO_LICENSE_SPLIT_AND_LABEL_DISTRIBUTION_UNKNOWN`；Emotion6为`NO_GO_MEDIA_LICENSE_ACCESS_AND_MODALITY`。因此第二人工主集仍未冻结。

## 门状态

- G1：`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`
- G2：`NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`
- split-v1：`formal_split=false`
- 任务20/M3：继续禁止

详细证据见`M1_SECOND_PRIMARY_SHORTLIST_20260714.md`、`M1_LIRIS_ACCEDE_DEEP_AUDIT_20260714.md`和`data/manifests/second-primary-readonly-audit-v1.manifest.json`。
