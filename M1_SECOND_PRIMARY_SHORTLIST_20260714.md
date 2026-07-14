# 第二人工主集公开候选元数据短名单

> 审计日期：2026-07-14
> 授权：`AUTH-00-M1-SECOND-PRIMARY-READONLY-20260714`
> 审计类型：公开网页、论文、许可和仓库文件树的只读元数据审计
> 边界：未下载数据、媒体、特征或小型元数据包；未登录、绕过gating、调用API/付费服务或联系作者。

## 1. 需求卡与判定规则

第二人工主集需能独立支撑`public-induced audience affect`，而不是说话者情绪、画面内人物情绪或评论者事后表达。最低证据包括：官方来源与可固定revision、明确许可、包体量、可复现内容输入、多人独立人工标注、内容项分组split能力、T0输入边界和与CSMV主标签的预注册映射。任一关键项为`UNKNOWN`时不得判为准入。

## 2. 短名单（固定为3项）

| 优先级 | 候选 | 来源/revision | 许可与获取 | 大小 | split | 媒体/模态 | 多人标注 | T0与构念映射 | 当前裁定 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | LIRIS-ACCEDE（Discrete） | [官方站](https://liris-accede.ec-lyon.fr/)与[官方论文](https://liris.cnrs.fr/Documents/Liris-7059.pdf)；站点为实时未版本化页面，数据revision未公开 | 视频片段逐源电影CC许可；annotations/描述文件CC BY-NC-SA 3.0；必须由永久学术职位人员签EULA并邮件申请 | 包字节数`UNKNOWN_NOT_PUBLICLY_EXPOSED`；9800个8—12秒片段，约26:57:08 | 官方Protocol A按160部电影分组：80电影/4900片段训练，80/4900测试；训练可再按40/40电影分验证 | 视听电影片段；媒体逐片段许可需从受限XML核验 | 离散集valence 1517名、arousal 2442名trusted annotator；只发布最终秩 | 内容AV可定义T0；诱发VA高度匹配，但非离散人群分布，原始判断不可重建 | `NO_GO_CURRENT_AUTHORIZATION_EULA_CONTACT_REQUIRED`；本轮唯一深审对象 |
| 2 | PMEmo | [作者官方GitHub](https://github.com/HuiZhangDB/PMEmo)，仓库快照commit `90289847fcb84e82024c3be1512b0f1d83925a55`；外部数据包版本为2018/2019，未固定hash | 仓库LICENSE为MIT且明指“Software”；不能外推到歌曲片段、歌词、评论或标注。Google Drive无需本轮访问，但数据资产许可`UNKNOWN` | README称全包约1.3GB | 官方README未给固定split，`UNKNOWN` | MP3副歌、音频特征、歌词、评论、EDA；完整歌曲因版权不提供 | 794首歌、457名受试者；静态与0.5秒动态VA标注 | 原始音频/歌词可候选T0；在线评论必须`available_at_t0=false`且不得作为输入；音乐诱发VA接近但非公众视频分布 | `NO_GO_LICENSE_SPLIT_AND_LABEL_DISTRIBUTION_UNKNOWN` |
| 3 | Emotion6 | [CVPR 2015官方论文](https://openaccess.thecvf.com/content_cvpr_2015/papers/Peng_A_Mixed_Bag_2015_CVPR_paper.pdf)；论文可固定，未定位到仍由作者维护的官方数据revision/入口 | 数据许可与Flickr逐图权利`UNKNOWN` | 1980张约VGA图像；包字节数`UNKNOWN` | 论文使用随机7:3，不是来源/事件分组split | 单图像，无音频/视频/文本内容模态 | 432名独立受试者；每图15人 | 图像可定义T0；7-bin（Ekman六类+neutral）经验分布与构念最贴合，但为单图、非多模态视频 | `NO_GO_MEDIA_LICENSE_ACCESS_AND_MODALITY` |

## 3. 未入短名单的预筛项

ArtEmis虽然含约8万件艺术品和约45.5万条人类诱发情绪及解释，但官方获取需表单批准，WikiArt图像版权风险由使用者承担，输入主要为单图；它未优于Emotion6对分布标签的匹配，因此不占用3项短名单额度。

## 4. 选择深审对象的理由

LIRIS-ACCEDE同时满足视听输入、诱发而非表达情感、多人标注和按源电影隔离四个关键结构条件，是三项中最接近第二视频主集者。它也存在最明确的当前授权冲突：签署EULA并邮件申请属于gating和联系作者。本轮深审因此只核公开证据，并以`No-Go under current authorization`结束，不尝试获得访问。

## 5. 结论与止损

- 短名单没有任何候选达到`FIT`或`READY_TO_DOWNLOAD`。
- 不申请、不下载、不把PMEmo代码MIT外推到数据、不把Emotion6论文可读性当数据许可。
- 不冻结第二主集、不修改标签映射、G1/G2与`formal_split=false`保持不变。
- 如00后续考虑LIRIS-ACCEDE，必须另行授权机构EULA/联系动作；取得访问后还需先报告确切文件、大小、许可、用途，再决定是否下载。
