# LAI-GAI v05 限额OSF元数据API审计

> 审计日期：2026-07-14  
> 授权：`AUTH-00-LAI-GAI-OSF-API-META-RO-20260714`  
> 前置复审：`REVIEW-00-LAI-GAI-META-20260714`  
> 最终复审：`REVIEW-00-LAI-GAI-OSF-API-20260714`  
> 方式：匿名、串行、仅HTTPS GET、仅`api.osf.io`元数据关系  
> 裁定：`NO_GO_PENDING_RATE_INTERVAL_AND_IMAGE_COMPONENT_FILE_TREE`
> 最终状态：`NO_GO_00_REVIEWED_NOT_FROZEN`

## 1. 执行摘要

本轮完成26次授权内GET请求，全部HTTP 200；响应正文累计382,394 bytes，低于5 MiB上限，请求数低于100次上限。请求清单、UTC时间、状态、字节数与响应SHA-256见`data/manifests/lai-gai-osf-api-metadata-v1.manifest.json`。原始JSON只保存在Git忽略目录`data/raw/lai-gai/osf-api-metadata/20260714T134325Z/`。

没有跟随任何download/content/render/html/upload链接，没有使用HEAD、Range、重定向、代理、Cookie、token、登录或第三方镜像；没有读取评分表内部内容，也没有构建标签映射或split。

边界validator发现请求2→3的UTC时间间隔为0.996519秒，比授权的1秒硬下限短0.003481秒。该偏差被作为合规失败保留；没有使用容差掩盖，也没有重跑网络请求。采集器的未来实现已增加0.1秒安全余量，但不能追溯改变本次事实。

## 2. 三节点矩阵

| 节点 | 角色 | public | 组件许可 | date_modified | provider | 可见文件 | 已知总大小 | 有公开checksum | 裁定 |
|---|---|---:|---|---|---|---:|---:|---:|---|
| `V8DKM` | 项目入口 | true | CC-By Attribution 4.0 International | 2026-03-07T12:09:14.185446 | osfstorage | 9 | 22,108,737 bytes | 9/9 | 元数据闭合 |
| `8P572` | 分析/评分数据 | true | CC-By Attribution 4.0 International | 2026-03-11T20:48:23.318238 | osfstorage | 137 | 1,122,196,956 bytes | 137/137 | 元数据闭合；内容未读取 |
| `K8XVH` | 图像资产 | true | CC-By Attribution 4.0 International | 2025-11-07T12:53:59.832314 | osfstorage | 0 | 0 bytes | 0/0 | `NO_GO_EMPTY_AUTHORIZED_FILE_LIST` |

三个组件的许可关系均返回同一CC BY 4.0许可对象。这里只登记OSF节点API明确返回的组件许可，不把它扩大为本地尚未取得资产的内容审查结论。

## 3. K8XVH阻塞证据

授权内端点`/v2/nodes/k8xvh/files/osfstorage/`返回HTTP 200和合法JSON，但`data`数组为空；返回顶层仅含`data`、`links`、`meta`，没有可投影文件。该结果经本地raw响应复核，排除了tracked投影器漏记文件的可能。

该空列表只说明授权内API文件列表没有公开图像资产元数据，不能推断图像不存在、节点私有或许可禁止。按授权不得继续尝试URL变体、其他关系、网页脚本、下载链接、第三方镜像或作者联系，因此在此停止。

## 4. 首次运行错误与恢复

采集器在全部网络请求结束后的manifest构造处因误用Python小写`false`触发`NameError`。错误已写入规划与工作记录。没有重跑任何网络请求；修正代码后使用`build_lai_gai_osf_api_manifest.py`从既有raw响应离线校验SHA-256并重建tracked manifest，避免重复计入授权额度。

## 5. 下载前准入结论

`V8DKM`和`8P572`的组件许可、修改时间、provider、文件树、size和公开checksum已在API元数据层闭合；但图像角色节点`K8XVH`没有可见文件树、体量或checksum，第二主集的核心输入资产仍无法固定。

因此当前裁定为`NO_GO_PENDING_RATE_INTERVAL_AND_IMAGE_COMPONENT_FILE_TREE`：一项执行边界不符合，另有核心图像资产元数据缺口。这不是对LAI-GAI研究设计的否定，也不是技术准入PASS。

- LAI-GAI：未冻结；
- G1：`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`；
- G2：`NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`；
- `formal_split=false`；
- 资产下载、标签映射、split、训练和任务20：仍禁止。

下一步只能回交00复审。除非00基于新的用户明确批准签发另一份书面授权，否则任务10不得继续访问或下载。

## 6. 可复现证据

- 请求与脱敏元数据：`data/manifests/lai-gai-osf-api-metadata-v1.manifest.json`
- fail-closed采集器：`scripts/audit_lai_gai_osf_api_metadata.py`
- 离线重建器：`scripts/build_lai_gai_osf_api_manifest.py`
- 边界验证器：`scripts/validate_lai_gai_osf_api_metadata.py`
- 授权全文：`TASK00_LAI_GAI_OSF_API_METADATA_AUTHORIZATION_20260714.md`

## 7. 00复审结果

00以`REVIEW-00-LAI-GAI-OSF-API-20260714`接受本交付为`OBSERVED_WITH_PROTOCOL_DEVIATION_NO_GATE_CREDIT`，但不授予G门信用；不豁免0.996519秒速率失败，不批准重跑。`K8XVH`空文件树继续独立阻塞资产固定，API授权已关闭为`CLOSED_NONCONFORMING_NO_RERUN_AUTHORIZED`。权威文件为`TASK00_LAI_GAI_OSF_API_METADATA_REVIEW_20260714.md`。
