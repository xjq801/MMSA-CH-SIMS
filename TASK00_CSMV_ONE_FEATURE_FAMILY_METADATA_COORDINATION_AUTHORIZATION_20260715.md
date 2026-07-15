# 任务00：CSMV单一特征族最小元数据协调授权

> 授权编号：`AUTH-00-CSMV-ONE-FEATURE-FAMILY-METADATA-COORDINATION-20260715`  
> 签发日期：2026-07-15  
> 依据：`REVIEW-00-CSMV-FEATURE-PREFLIGHT-G2-20260715`  
> 状态：`REQUEST_SENT_WAITING_RIGHTS_HOLDER_RESPONSE`  
> 有效期：至2026-08-15或权利方完成一次实质回复，以先到者为准

## 1. 授权目的

通过最小外部协调取得一个官方CSMV视觉特征族的资产级许可与固定manifest，解决当前公开页面无法显示的外部元数据。优先请求I3D；只有权利方明确表示I3D不可提供或不可授权时，才可把同一请求范围切换为VideoMAE。

## 2. 允许动作

- 从固定官方仓库、论文或机构页面定位项目维护者/权利方的公开官方联系渠道。
- 通过一个官方渠道发送一次简洁请求；7个自然日无回复时最多发送一次跟进。不得多渠道重复轰炸。
- 请求权利方提供或在官方仓库/存储端公开以下材料：
  1. 预计算特征的资产级研究使用许可或许可声明；
  2. 稳定revision/快照；
  3. 相对文件名、bytes、SHA-256的机器可读manifest；
  4. 8210个正式`video_file_id`覆盖清单；
  5. 总体量、特征dtype/shape和提取器/权重/采样配置。
- 可接收不超过5 MiB的纯元数据附件（`.txt/.md/.csv/.json/.sha256`）或官方页面更新；不得接收或下载`.npy`、压缩特征包、视频、音频或原始媒体。
- 官方站点访问优先使用项目Git忽略`.env`中的本机代理；代理只作传输，不改变联系身份或权限。
- 原始往来与邮件头仅存Git忽略目录；tracked文件只保存脱敏摘要、时间、官方身份定位、响应/附件SHA-256和裁定，不保存个人邮箱、签名、Cookie或账户标识。

## 3. 禁止动作

- 不登录Google Drive数据目录，不调用Drive API，不绕过配额、验证码、地域或访问控制。
- 不接受EULA/DUA、不承诺署名或再分发条件、不代表学校签署法律文件；出现此类要求立即回交00和用户。
- 不购买服务，不请求秘密链接，不使用第三方镜像，不下载任何特征内容或媒体。
- 不训练、不建索引、不创建任务20，不把权利方未明确回答的字段自行推断为允许。

## 4. 回交合同

任务10回交时须提供：官方联系渠道定位、发送日期、请求范围、是否回复、权利方身份验证方法、逐项六字段矩阵、元数据附件字节数/SHA-256、仍为UNKNOWN的字段以及建议的唯一特征族。原始个人信息不得进入Git。

成功取得材料不自动放行G2，也不自动授权下载。只有00书面资产准入复审通过后，才可另签限额内容下载授权。

## 5. 推荐请求文本（可按渠道压缩）

> We are conducting a reproducible academic study using the public CSMV/MSA-CRVI benchmark. Before using one released visual feature family, could the project rights holder clarify the asset-level research-use license and provide a fixed revision plus a machine-readable manifest containing relative filenames, byte sizes, SHA-256 checksums, and coverage of the 8,210 official `video_file_id` values? For the selected family, feature extractor/version, dtype/shape and total size would also be helpful. We are requesting metadata only and will not download feature content until permission and fixity are independently reviewed.

## 6. 首次执行状态（2026-07-15）

任务10在官方`IEIT-AGI/MSA-CRVI`仓库尝试通过GitHub集成创建一次I3D纯元数据Issue，但集成返回HTTP 403 `Resource not accessible by integration`，未生成issue number/URL，外部写入为0。按`REVIEW-00-CSMV-I3D-METADATA-COORDINATION-ATTEMPT-20260715`，该结果属于连接器写权限阻塞，不是权利方拒绝；一次正式请求额度尚未消耗。

后续只能在同一官方Issues渠道二选一恢复：用户手工提交`CSMV_I3D_GITHUB_ISSUE_REQUEST_20260715.md`，或在连接器取得创建Issue权限后重试一次。任一路径成功后另一条立即停止；不得切换第二渠道或重复发送。

## 7. 正式请求已发出（2026-07-15）

用户已在同一官方仓库手工创建公开Issue #5：`https://github.com/IEIT-AGI/MSA-CRVI/issues/5`。按`REVIEW-00-CSMV-OFFICIAL-ISSUE-5-SENT-20260715`，一次正式请求额度已经使用，连接器重试、重复Issue和第二渠道均停止。

唯一一次跟进额度尚未使用，但2026-07-22前不得跟进。公开正文覆盖授权要求的元数据字段，不过没有逐字点名I3D；若到允许日期仍无回复，跟进应在同一Issue内明确I3D优先范围。收到任何实质回复后先回交00，回复不自动授权特征下载或放行G2。

## 8. 后续效率政策影响（2026-07-15）

`POLICY-00-EFFICIENCY-FIRST-MIRROR-AND-EXPANDED-ACQUISITION-20260715`允许在等待Issue回复期间，从官方副本或可信第三方镜像隔离取得公开候选特征资产。该取得行为与本文件的单一联系渠道纪律分离：不得另行联系第二渠道，但可并行执行公开资产传输和完整性审计。

隔离取得不等于许可准入；在00确认许可、revision/fixity、schema和8210覆盖前，不得正式训练、建索引、发布或放行G2。
