# LIRIS-ACCEDE第二人工主集只读深审

> 日期：2026-07-14
> 授权：`AUTH-00-M1-SECOND-PRIMARY-READONLY-20260714`
> 审计范围：只读公开官网、官方EULA和官方论文
> 最终状态：`NO_GO_CURRENT_AUTHORIZATION_EULA_CONTACT_REQUIRED`

## 1. 来源与revision

| 项目 | 公开证据 | 结论 |
|---|---|---|
| 官方入口 | [LIRIS-ACCEDE官网](https://liris-accede.ec-lyon.fr/) | 官方入口可公开读取 |
| 数据说明 | [Database content](https://liris-accede.ec-lyon.fr/database.php) | 六类集合、电影清单和逐电影CC许可公开展示 |
| 许可合同 | [官方EULA](https://liris-accede.ec-lyon.fr/files/EULA.pdf) | 当前公开EULA覆盖六类集合 |
| 方法与协议 | [IEEE TAC论文作者公开稿](https://liris.cnrs.fr/Documents/Liris-7059.pdf) | 记录离散集构建、标注与Protocol A/B/C |
| revision | 站点未公开数据发布号、tag、commit、不可变manifest或包hash | `LIVE_UNVERSIONED_METADATA_SNAPSHOT_2026-07-14`；数据revision=`UNKNOWN` |

没有把网页快照日期伪装成数据revision。获得下载权限前无法核验包内文件清单、mtime、字节数或SHA-256。

## 2. 许可、访问与发布边界

- 官网要求打印、签署EULA并发邮件申请，免费邮箱请求会被拒绝，下载链接通过邮件发放。
- EULA要求由学术机构永久职位人员签署，最多列入5名同机构研究人员；只允许学术用途，禁止数据库或其部分的再分发（学术展示的小片段例外）。
- 视频片段继承源电影的逐项Creative Commons许可；具体许可记录位于随片段提供的描述XML。annotations及其他描述文件为CC BY-NC-SA 3.0。
- 官方网页列出电影使用BY、SA、NC组合且排除ND。即使总体可学术使用，也必须在取得授权后按片段解析许可；不能用一个统一许可证覆盖所有媒体。

本轮授权明确禁止联系作者、登录或绕过gating，因此不能签发EULA、申请账号或访问下载链接。裁定为`NO_GO_CURRENT_AUTHORIZATION_EULA_CONTACT_REQUIRED`，不是断言数据永久不可用。

## 3. 规模与公开文件树证据

| 资产 | 公开规模 | 文件级可核状态 |
|---|---:|---|
| Discrete | 160部电影、9800个8—12秒片段；片段总时长26:57:08；源电影总时长73:41:07 | 文件名、包字节数、hash均`UNKNOWN` |
| Continuous | 30部电影；10名法国付费参与者的连续自评及GSR | 文件名、包字节数、hash均`UNKNOWN` |
| MediaEval 2015 | 10900片段；100部电影/6144片段development，99部/4756片段test | 公开页面给逻辑规模，包清单`UNKNOWN` |
| MediaEval 2016—2018 | 额外短片、长电影、VA/fear标注与部分音视频特征 | 包清单、版本、字节数、hash均`UNKNOWN` |

官网宣称视频、annotations、features和protocols可获取，但实际获取受EULA邮件门约束。未执行HEAD、下载或对下载地址探测。

## 4. 多人标注与真值形态

- Discrete集通过CrowdFlower做成对比较。valence收集超过582,000次判断、约187,000个比较，来自1,517名trusted annotator；arousal超过665,000次判断、约221,000个比较，来自2,442名trusted annotator，均覆盖89个国家。
- 单次pivot比较至少由3人判断，至少2人一致后确定相对顺序。最终每个片段只有0—9799的valence秩和arousal秩。
- 为保护众包者隐私，官方不发布形成排序的原始worker annotations，只发布最终VA秩。因此它是可审计的多人`HUMAN_GOLD`诱发情感监督，但不是逐片段可重建的人群离散经验分布，也无法从公开秩计算评论数型不确定性。
- Continuous集提供10名参与者的连续自评，人数较小且与Discrete集标签形态不同；不能静默合并两者。

## 5. split与泄漏审计

| 风险 | 公开证据与结论 | 状态 |
|---|---|---|
| 同电影片段跨split | Protocol A把160部电影分为80/80，每侧4900片段；训练再按40/40电影分训练/验证 | 结构上`PASS_GROUP_BY_FILM`，需包级ID复核 |
| leave-one-movie-out | Protocol B逐电影留一 | 可作敏感性分析，不替代独立test冻结 |
| topic/genre held-out | 论文列9个电影genre，Protocol C为同genre建模，不是topic-held-out | `NOT_PROVIDED`，需另行预注册且不得test驱动 |
| 片段近重复/相邻上下文 | 同一电影片段保持时序；按电影隔离可阻断跨split相邻片段，但跨电影复用素材未知 | `PARTIAL_UNKNOWN` |
| 发布者/作者捷径 | 电影创作者和片名公开，但官方协议未报告作者组交叉审计 | `UNKNOWN` |
| train-only拟合 | 官方预计算特征与VA估计过程的fit范围未由公开元数据完全证明 | `UNKNOWN`；正式使用前必须重核 |

在无法访问manifest时，Protocol A只能记为“设计证据通过、包级实证待核”，不能宣称split已经由本项目复现。

## 6. T0输入合同

建议候选T0定义为：一个8—12秒片段内的原始音频与画面，截止片段结束。允许片段内部的自然语音/字幕画面；禁止目标VA秩、估计分数、worker判断、GSR、测试标签和任何基于全库/全电影拟合的派生信息。

需额外限制：

- 电影名、源URL、创作者、片段在完整电影中的绝对位置默认不作为模型输入，以免形成源电影捷径；
- 预计算features只有在其提取器、fit范围和片段边界可审计后才能标`available_at_t0=true`；
- 数据本身没有目标评论或未来互动量，因而不引入CSMV式评论泄漏，但这不等于所有源电影或预计算特征泄漏已排除。

## 7. 构念与标签映射

| 本项目目标 | LIRIS-ACCEDE | 映射结论 |
|---|---|---|
| public-induced audience affect | 明确测量观众观看片段后“felt/induced”valence与arousal | 构念高度一致 |
| 离散公众情绪分布 | Discrete只发布最终VA秩；MediaEval提供三档VA或fear等派生标签 | 不能无损映射到CSMV离散经验分布 |
| 样本不确定性 | 原始worker判断不发布 | 无法计算与评论数同形的不确定性；必须标缺失 |
| 中文/社交视频域 | 主要为英语电影，少量其他语言；非社交平台短视频 | 明显跨域，只能作为外部泛化或VA辅助主集候选 |
| 统一主指标JS divergence | 排名/连续VA不是类别概率分布 | 不满足现有主任务主指标，除非总纲另行批准任务/指标变体；本任务无权修改 |

最关键不匹配不是媒体，而是标签对象：LIRIS测量诱发VA排序，CSMV主任务预测离散公众反应分布。不能为了“凑齐第二主集”把VA秩强制离散化并声称等价。

## 8. 深审结论与重新准入条件

当前`No-Go`由两层独立阻塞构成：

1. **访问阻塞**：本轮禁止签EULA/联系作者，无法取得包级revision、size、manifest和hash。
2. **任务阻塞**：公开标签不是可直接用于JS divergence的离散人群分布，主任务映射不可无损完成。

若00将来考虑把它作为第二VA辅助主集或跨域验证集，必须先另行授权机构EULA流程；在任何下载前报告文件名、预计大小、逐层许可和用途。取得合法访问后还需验证描述XML、Protocol A ID交集、媒体hash、预计算feature fit范围及实际标签字段。上述条件满足也不会自动通过G1，仍需00重新审查其是否符合“第二公开人工主benchmark”的冻结定义。
