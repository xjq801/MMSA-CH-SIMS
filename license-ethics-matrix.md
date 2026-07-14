# M1 许可与伦理矩阵

> 版本：v0.2
> 审计日期：2026-07-14
> 边界：研究记录，不构成法律意见；未知项不视为许可。

| 数据源/组成 | 来源 | 许可或条件 | 隐私/伦理 | 再分发边界 | 当前状态 |
|---|---|---|---|---|---|
| CSMV仓库代码 | 官方GitHub `IEIT-AGI/MSA-CRVI` | 根LICENSE为Apache-2.0；README称代码MIT，存在上游表述不一致 | 代码本身非个人数据 | 使用前需按文件级证据解决MIT/Apache差异并保留许可/归属 | `PENDING_CODE_LICENSE_CONFLICT` |
| CSMV评论标注 | 官方GitHub `CSMV/Comments_Anno` | README明确annotations为CC BY-SA 4.0 | 评论正文可能含用户表达；本项目不输出原文或平台标识 | 本地只读审计可继续；不在本项目公开仓库再发布原始评论，只发布聚合统计、split ID与脚本 | `LICENSE_IDENTIFIED_LOCAL_AUDIT` |
| CSMV TikTok媒体/原始URL | `CSMV_rawLinks.xlsx`与外部平台 | 第三方平台内容，不因仓库Apache许可自动获得媒体版权 | 可能含创作者、用户及平台标识 | 默认不再分发；媒体获取需另行授权并核平台条款 | `RESTRICTED_UNKNOWN` |
| iNews public标签包 | HF `pitehu/inews_public`固定revision | CC BY-NC-SA 4.0 | 不含persona；含伪匿名Annotator_ID；原始CSV仅存Git忽略区 | 仅非商业、署名、相同方式共享；派生发布需逐项核兼容性 | `LICENSE_AND_SCHEMA_VERIFIED` |
| iNews完整persona包 | HF `pitehu/inews` | CC BY-NC-SA 4.0 + gated申请与不重识别/不转交等条件 | 敏感人口学和人格信息；需更高安全控制 | 本项目当前无必要使用，默认不申请、不下载 | `OUT_OF_SCOPE_DEFAULT` |
| iNews新闻图片/截图 | Facebook帖子URL；作者截图工具 | 图片因版权不随数据发布；另受网页/平台条款约束 | 论文明确截图含reaction count；属于T0后信息 | 默认不采集/不发布；合法恢复、裁剪、保存与发布均需单独审计 | `NO_GO_PRIMARY_PENDING_MEDIA_RIGHTS` |
| NEmo+标签附件 | ACL Anthology Dataset.zip | 包内无LICENSE；论文所述BU-NEmo研究许可不能外推为NEmo+许可 | 含匿名自由文本理由，原始内容不得进入Git或日志 | 仅作本地许可/结构检查；明确许可前不进入正式研究使用或再分发 | `LICENSE_UNKNOWN` |
| NEmo+新闻图片 | Dataset.zip中的`anonymous-source/*.jpg`引用 | 包内0张图片，无可解析外部URL | 媒体来源和权利链不可审计 | 不可复现、不可再分发 | `MEDIA_UNAVAILABLE` |
| MVIndEmo标签/URL | Springer论文；论文所列GitHub | 数据仓库404，许可UNKNOWN | 标签由评论模型和点赞聚合；不得误称人工真值 | 合法来源恢复前不使用；恢复后也只作SILVER辅助 | `SILVER_SOURCE_UNAVAILABLE` |

## T0专用合规规则

- iNews的engagement、comment和share字段一律标为`available_at_t0=false`。
- 任何帖子截图若显示未来互动或评论，必须在进入模型前被物理裁剪/遮挡并由测试拒绝残留。
- CSMV目标评论只用于标签聚合和训练期特权监督；test评论不得进入输入、索引或调参。
- 许可未知、媒体权利未知或含未脱敏标识的资产不得进入公开Git仓库。

## 官方定位

- CSMV论文页：https://proceedings.neurips.cc/paper_files/paper/2024/hash/bbf090d264b94d29260f5303efea868c-Abstract-Datasets_and_Benchmarks_Track.html
- CSMV仓库：https://github.com/IEIT-AGI/MSA-CRVI
- iNews论文页：https://aclanthology.org/2025.acl-long.1217/
- iNews代码：https://github.com/pitehu/inews
- iNews公开数据卡：https://huggingface.co/datasets/pitehu/inews_public
- iNews gated数据卡：https://huggingface.co/datasets/pitehu/inews
- NEmo+论文与附件页：https://aclanthology.org/2022.aacl-main.29/
- MVIndEmo论文：https://doi.org/10.1007/s00530-023-01221-8
