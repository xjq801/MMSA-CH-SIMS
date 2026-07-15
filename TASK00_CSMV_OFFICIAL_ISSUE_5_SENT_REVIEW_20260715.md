# 任务00：CSMV官方Issue #5发送状态复审

> 复审编号：`REVIEW-00-CSMV-OFFICIAL-ISSUE-5-SENT-20260715`  
> 复审日期：2026-07-15  
> 上游授权：`AUTH-00-CSMV-ONE-FEATURE-FAMILY-METADATA-COORDINATION-20260715`  
> 官方定位：`https://github.com/IEIT-AGI/MSA-CRVI/issues/5`  
> 复审状态：`ACCEPTED_REQUEST_SENT_WAITING_RESPONSE`

## 1. 独立复核事实

00于2026-07-15匿名只读打开公开页面，确认：

- 仓库为官方公开仓库`IEIT-AGI/MSA-CRVI`；
- issue number为`5`，状态为`Open`，页面显示创建日期为2026-07-15；
- 标题为`Request for License Clarification and Fixity Metadata for CSMV/MSA-CRVI Visual Features`；
- 正文请求资产级研究使用许可、固定revision、相对文件名/bytes/SHA-256机器manifest、8210个正式`video_file_id`覆盖、提取器/版本、dtype/shape和总体量；
- 正文明示在许可与固定性经独立复审前不下载特征内容。

公开页面当前没有权利方实质回复。此前GitHub集成HTTP 403且无外部写入的失败仍作为历史证据保留，不与手工创建成功相互覆盖。

## 2. 范围一致性与诚实边界

Issue正文与原授权第5节的推荐请求文本一致，覆盖正式资产准入所需字段，因此00接受其为原授权下的**一次正式请求**。

公开正文使用`one released visual feature family`和`selected family`，没有逐字点名`I3D`。这不使请求越界，也不恢复第二次发送额度，但不能写成“权利方已经收到明确限定I3D的请求”。当前按原授权的I3D优先级等待回复；若到允许跟进日期仍无回复，唯一一次同Issue跟进应明确写明优先请求I3D元数据。

## 3. 授权额度与等待期裁定

- 一次正式请求额度：**已于2026-07-15使用**。
- 连接器重试或另建重复Issue：**禁止**。
- 切换邮件、社交平台或其他第二渠道：**禁止**。
- 唯一一次跟进额度：尚未使用；最早可在**2026-07-22**于同一Issue #5内使用。
- 2026-07-22前：不得评论、催促或补发相同请求。
- 若权利方在此之前实质回复：停止计时，不自行下载；将公开回复及不超过5 MiB的纯元数据回交00复审。

## 4. 资产准入与门状态

Issue创建成功只关闭“尚未成功联系权利方”的协调子状态，不提供资产级许可、revision、fixity manifest、schema或8210覆盖证据。

- G1：`PASS`。
- G2：`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`。
- 全局：`formal_split=false`。
- 正式训练、索引与任务20：继续禁止。
- 特征或媒体下载：未授权。

最终裁定：`REQUEST_SENT_WAITING_RIGHTS_HOLDER_RESPONSE`。下一有效事件只能是权利方回复，或在2026-07-22及以后于同一Issue内执行至多一次跟进。

## 5. 后续效率政策更新（2026-07-15）

用户随后扩大项目内部下载授权。Issue等待与跟进纪律不变，但`POLICY-00-EFFICIENCY-FIRST-MIRROR-AND-EXPANDED-ACQUISITION-20260715`允许在等待期间从官方或可信镜像隔离预取公开候选特征。任何预取资产仍不得获得许可或G门信用。
