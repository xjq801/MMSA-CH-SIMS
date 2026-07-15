# CSMV I3D 元数据协调记录

> 授权：`AUTH-00-CSMV-ONE-FEATURE-FAMILY-METADATA-COORDINATION-20260715`  
> 日期：2026-07-15  
> 当前状态：`OFFICIAL_ISSUE_OPEN_WAITING_RIGHTS_HOLDER_RESPONSE`

## 官方渠道定位

- 官方项目仓库：`https://github.com/IEIT-AGI/MSA-CRVI`
- 选定的单一联系渠道：该仓库的公开 GitHub Issues。
- 选择依据：仓库 README 明确邀请数据集问题联系项目方，Issues 属于仓库维护者可见的官方公开渠道。

## 拟请求范围

仅请求 I3D 视觉特征族的元数据，不请求或下载特征内容：

1. 预计算 I3D 特征的资产级研究使用许可或书面许可定位；
2. 稳定 revision、不可变快照或权利方签发的版本标识；
3. 相对文件名、单文件 bytes、单文件 SHA-256 的机读 manifest；
4. 对 8,210 个正式 `video_file_id` 的覆盖、缺失键、额外键与处理规则；
5. 总下载量与解压后空间；
6. 提取器/预训练权重版本、dtype、shape/维度及采样/聚合配置。

## 发送结果

- 安装并连接 GitHub 集成后，先对官方仓库检索相关公开 Issue；未发现相同主题的开放 Issue。
- 2026-07-15 通过 GitHub 集成尝试创建一次公开 Issue。
- GitHub 返回 HTTP 403：`Resource not accessible by integration`。
- 结果中没有 issue number 或 URL；因此没有产生外部消息、没有联系到维护者、没有上传附件，也没有消耗任何数据下载授权。
- 未切换邮件、其它社交平台或第三方渠道，避免多渠道重复联系。

## 手工发送恢复与公开证据

- 用户于 2026-07-15 在同一官方 GitHub Issues 渠道成功创建公开 Issue #5：`https://github.com/IEIT-AGI/MSA-CRVI/issues/5`。
- 现场匿名核验结果：仓库严格等于 `IEIT-AGI/MSA-CRVI`，Issue number 为 5，状态为 `Open`，创建日期为 2026-07-15。
- 标题为 `Request for License Clarification and Fixity Metadata for CSMV/MSA-CRVI Visual Features`。
- 正文请求资产级研究许可、固定 revision、相对文件名/bytes/SHA-256 manifest、8,210 个正式 `video_file_id` 覆盖、提取器/版本、dtype/shape 和总体量，并明确在许可与固定性独立复审前不下载特征内容。
- 诚实边界：公开正文使用`one released visual feature family`与`selected family`，没有逐字点名I3D；00接受其为授权内的一次正式请求，但不声称权利方已收到明确限定I3D的措辞。
- 因请求已成功发出，禁止连接器重复创建 Issue，也不得切换邮件或其它第二渠道。

## 当前阻塞与恢复条件

当前不再被发送权限阻塞，而是等待权利方实质回复。在 2026-07-22 前不得跟进；若届时仍无回复，原授权至多允许在同一 Issue 内跟进一次。

在收到并核验权利方实质答复前，六类资产元数据继续为 `UNKNOWN`，G2 保持 `BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`。即使收到回复，也必须先由00完成书面资产准入复审；回复本身不自动授权下载特征内容或放行G2。

00复审编号为`REVIEW-00-CSMV-OFFICIAL-ISSUE-5-SENT-20260715`；正式请求额度已使用，唯一一次同Issue跟进最早为2026-07-22。若届时仍无回复，跟进应明确I3D为优先请求特征族。
