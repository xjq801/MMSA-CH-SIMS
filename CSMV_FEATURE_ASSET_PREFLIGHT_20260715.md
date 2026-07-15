# CSMV正式输入特征资产预审

> 授权：`AUTH-00-CSMV-FEATURE-ASSET-PREFLIGHT-RO-20260715`  
> 审计日期：2026-07-15  
> 固定上游：`IEIT-AGI/MSA-CRVI@99d14240254b1381dde0b9c56add140381f65117`  
> 裁定：`NO_GO_PENDING_ASSET_METADATA_AND_LICENSE`

## 结论

官方固定README确认：视觉特征由I3D、R(2+1)D、VideoMAEv2等预训练模型生成；当前声明已发布I3D与VideoMAE；每个视频保存一个`.npy`，文件名应对应`video_file_id`。README的固定SHA-256为`39a1162df89dbf7a50d89435b640043c1397eaa6b1827e63ebbf77584a75d1e3`，并明确链接一个公开Google Drive特征目录。

匿名HTTPS GET可到达该公开目录页面，现场返回HTTP 200且最终host为`drive.google.com`。但授权范围内取得的初始HTML没有公开列出I3D/VideoMAE目录、`.npy`文件名、文件数量、单文件/总大小、更新时间或checksum。页面响应还是动态内容，单次响应hash不能替代稳定资产revision。

因此，当前不能选择“唯一最小特征族”，不能估算磁盘预算，也不能验证8210键覆盖。任何资产级许可、revision、文件树、体量、逐文件hash和覆盖率均保持`UNKNOWN`；本预审不取得G2资产信用。

## 许可边界

| 对象 | 官方可定位声明 | 当前裁定 |
|---|---|---|
| 代码 | README称MIT，仓库根LICENSE为Apache-2.0 | 保留冲突；不外推到数据资产 |
| 评论annotations | README明确CC BY-SA 4.0 | 已用于现有标注审计 |
| I3D/VideoMAE视觉特征 | README声明发布，但License段未明确覆盖 | `UNKNOWN_NOT_EXPLICITLY_COVERED` |
| TikTok原始媒体 | 无资产级授权或再分发说明 | `UNKNOWN_NOT_COVERED` |

“公开可下载”不等于获得研究使用与再分发许可；代码许可和annotations许可都不能自动覆盖派生视觉特征。

## 特征族矩阵

| 特征族 | README状态 | 文件树/数量 | 体量 | revision | checksum | 8210覆盖 |
|---|---|---|---|---|---|---|
| I3D | 声明已发布 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | 0个公开值 | 仅有命名规则声明，未验证 |
| VideoMAE/VideoMAEv2 | 声明已发布，但正文与示意命名不一致 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | 0个公开值 | 仅有命名规则声明，未验证 |
| R(2+1)D | 示意结构中出现，未明确称当前已发布 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | 0个公开值 | 未验证 |

## 已遵守的边界

- 未登录Google账户，未使用Cookie/token，未调用Google Drive API或第三方镜像。
- 未下载、预览或流式读取任何`.npy`、视频或音频；未访问TikTok URL。
- 未建索引、未训练、未创建任务20。
- 机读事实位于`data/manifests/csmv-feature-preflight-v1.manifest.json`；未知字段没有改写成PASS。

## 关闭缺口的最小外部动作

需要权利方或官方存储端公开提供并明确绑定到一个特征族（优先I3D或VideoMAE中的一个）：

1. 资产级研究使用许可；
2. 稳定revision或不可变快照标识；
3. 相对文件名、字节数和SHA-256 manifest；
4. 8210个`video_file_id`的精确覆盖声明或可机读键清单；
5. 总体量与建议解压/校验空间。

在取得上述材料及00后续书面下载授权前，正式CSMV多模态输入仍不可冻结。

## 2026-07-15本地隔离取得补充

上述内容保留为取得前的历史预审。此后用户提供本地包`I3D-feature-001`，现行
`POLICY-00-EFFICIENCY-FIRST-MIRROR-AND-EXPANDED-ACQUISITION-20260715`
允许在许可闭合前进入Git忽略隔离区审计。任务10没有重新下载数据，而是建立项目内directory junction并完成只读核验：

- 9,942个`.npy`，共2,752,998,144 bytes；
- 官方评论映射要求的8,210个`video_file_id`全部存在，缺失0，另有1,732个非当前标签集文件；
- 全部数组为`float32[T,1024]`，`T=6—1719`，schema错误0；
- 8,210个必需文件已有逐文件bytes/SHA-256；全包内容树SHA-256为
  `35be2d18e1d2413ba3765034cdb454baa5e3496d49c540c9be00e81bbc2c1942`；
- 证据见`CSMV_I3D_QUARANTINE_AUDIT_20260715.md`和
  `data/manifests/csmv-i3d-quarantine-v1.manifest.json`。

当前状态更新为`QUARANTINE_ACQUIRED_LICENSE_REVISION_ATTESTATION_PENDING`。本地文件树、
体量、schema、fixity和8210覆盖已经现场闭合；资产级许可、稳定官方revision、权利方对包身份与fixity的确认仍未闭合。
因此`formal_model_input_allowed=false`、`g2_asset_credit=false`保持不变，等待00书面复审。
