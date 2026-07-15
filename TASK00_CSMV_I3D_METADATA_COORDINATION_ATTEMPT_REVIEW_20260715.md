# 任务00：CSMV I3D元数据协调首次尝试复审

> 复审编号：`REVIEW-00-CSMV-I3D-METADATA-COORDINATION-ATTEMPT-20260715`  
> 复审日期：2026-07-15  
> 上游授权：`AUTH-00-CSMV-ONE-FEATURE-FAMILY-METADATA-COORDINATION-20260715`  
> 复审状态：`ACCEPTED_NO_EXTERNAL_WRITE_AUTHORIZATION_UNCONSUMED`

## 1. 复审结论

00接受任务10对首次官方渠道协调尝试的事实回交：任务10已定位官方公开仓库`IEIT-AGI/MSA-CRVI`的GitHub Issues，并在相关开放Issue检索为0后尝试创建一次I3D纯元数据请求；GitHub集成返回HTTP 403 `Resource not accessible by integration`，未生成issue number或公开URL。

该结果裁定为**连接器写权限/传输层阻塞**，不是项目维护者或权利方的拒绝。由于外部写入为0、维护者未被联系，原授权中的“一次正式请求”与“一次7日后跟进”额度均未消耗。

## 2. 接受的证据

- `CSMV_I3D_METADATA_COORDINATION_20260715.md`记录官方渠道、请求范围、HTTP 403、无issue定位符以及未切换第二渠道。
- `WORK_LOG.md`的`WR-20260715-015`记录同一失败及本地验证结果，失败没有被删除或改写成已发送。
- 未发现issue number、issue URL、外部回复或资产下载记录；因此不能声称已联系维护者、已取得许可或已取得manifest。

## 3. 后续授权状态

原授权继续有效至2026-08-15或权利方完成一次实质回复（以先到者为准），无需为同一官方Issues渠道另签新授权。只允许以下两条恢复路径任选其一：

1. 用户在`IEIT-AGI/MSA-CRVI`官方仓库手工提交`CSMV_I3D_GITHUB_ISSUE_REQUEST_20260715.md`中的请求；
2. GitHub连接器取得对该仓库创建Issue的权限后，在同一仓库、同一Issues渠道重试一次。

两条路径不得并行重复发送。任一路径成功取得公开issue number/URL后，另一条立即停止；从成功创建日期起满7个自然日仍无回复时，才可在同一issue内跟进一次。当前不得切换邮件、社交媒体或其他第二渠道。

## 4. 继续有效的边界

- 请求仅限I3D资产级许可、稳定revision、相对文件名/bytes/SHA-256、8210键覆盖、总体量与特征schema。
- 可接收不超过5 MiB的纯元数据；不得下载`.npy`、压缩特征包、视频、音频或其他媒体。
- 不登录Google Drive，不调用Drive API，不绕过访问控制，不接受或签署EULA/DUA。
- 若权利方提供材料，须先由00复审许可、固定性、覆盖与schema；收到材料不自动授权内容下载，也不自动放行G2。

## 5. 门状态

- G1：`PASS`。
- G2：`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`。
- 全局：`formal_split=false`。
- 任务20：继续禁止创建、训练或建索引。

本次复审只接受“未发送成功”的协调证据并保留原授权额度，不改变任何数据集、split或资产准入状态。

## 6. 后续状态（2026-07-15）

用户随后在同一官方渠道成功创建Issue #5。此前关于403和当时无外部写入的事实继续有效，但“请求额度未消耗”的操作状态已由`REVIEW-00-CSMV-OFFICIAL-ISSUE-5-SENT-20260715`更新为“正式请求额度已使用、等待权利方回复”。
