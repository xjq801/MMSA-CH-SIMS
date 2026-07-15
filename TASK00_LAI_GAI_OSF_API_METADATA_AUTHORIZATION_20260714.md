# 00授权：LAI-GAI OSF元数据API只读取得

> 授权编号：`AUTH-00-LAI-GAI-OSF-API-META-RO-20260714`  
> 授权日期：2026-07-14  
> 授权依据：用户明确回复“批准”  
> 执行任务：10-M1–M2 数据与协议  
> 前置复审：`REVIEW-00-LAI-GAI-META-20260714`  
> 状态：`CLOSED_NONCONFORMING_NO_RERUN_AUTHORIZED`

## 1. 授权目的

允许任务10使用OSF公开API取得`V8DKM`、`8P572`、`K8XVH`三个节点的节点级与文件级**元数据JSON**，用于核验asset license、固定revision/更新时间、provider、文件树/文件数/size、公开checksum和gating。该授权只解除原授权中的“不得调用API”限制，不解除任何资产内容下载、评分内容读取、标签映射、split、训练或任务20禁令。

## 2. 允许的请求

仅允许匿名HTTPS `GET`，host必须严格等于`api.osf.io`，节点范围必须严格属于：

- `V8DKM`
- `8P572`
- `K8XVH`

允许访问：

1. `/v2/nodes/{node_id}/`；
2. `/v2/nodes/{node_id}/files/`；
3. 上述响应中由`relationships.license`或文件provider/file-list关系给出的`api.osf.io`元数据链接；
4. 文件夹元数据的子级file-list链接和同一列表的`links.next`分页链接。

不得手工扩展到其他节点、注册、fork、用户、评论、wiki、活动日志、搜索或第三方provider内容端点。任何响应中的`download`、`render`、`html`、`upload`或非`api.osf.io`链接均不得跟随。

## 3. 资源与速率上限

- 全部HTTP响应正文累计上限：5 MiB；达到上限立即停止。
- 请求总数上限：100次；达到上限立即停止。
- 请求间隔不少于1秒；不得并发请求。
- 不发送Authorization、Cookie、机构凭证或登录态；不得使用代理绕过、浏览器会话或付费服务。
- 401、403、404、429或5xx均记录后停止对应分支；不切换镜像、不猜测URL、不绕过gating。

## 4. 可保存与可入Git内容

- 原始API JSON只允许保存在Git忽略的`data/raw/lai-gai/osf-api-metadata/`，记录请求URL、UTC时间、HTTP状态、Content-Type、字节数和SHA-256。
- Git可跟踪manifest只保留研究准入需要的组件/文件元数据：node ID、license、revision/date_modified、provider、相对文件路径、kind、size、公开checksum、gating、响应hash和访问结果。
- contributor、用户ID、姓名、邮箱、头像、评论、活动日志、Cookie、请求头秘密和签名下载URL不得写入Git、工作记录或报告；若API返回，必须在tracked产物中删除。
- 仅API明确提供的checksum可登记；不得通过下载资产补算hash。

## 5. 明确禁止

- 不得访问、预览、流式读取或下载任何图像、ZIP、raw data、评分表、代码包或其他资产内容；
- 不得跟随file对象中的下载/content/render链接，不得使用Range、HEAD或签名URL探测资产；
- 不得读取评分表内部字段、构建标签映射、统计样本、生成split或进行泄漏测试；
- 不得登录、使用Cookie/API token、联系作者、调用付费服务或第三方镜像；
- 不得修改G1/G2为通过、不得将`formal_split`改为`true`、不得训练模型或创建任务20。

## 6. 必须产出与停止条件

任务10必须产出：

1. API请求清单及响应SHA-256；
2. 三节点的license/revision/provider/file tree/count/size/checksum/gating矩阵；
3. 机器校验器，证明只访问白名单host/节点/关系、未跟随下载链接、总量和请求数未超限；
4. `FIT_FOR_NEXT_REVIEW`或`NO_GO_PENDING_*`裁定，UNKNOWN不得按通过处理；
5. 更新`DATA_SOURCE_LEDGER.md`、G1/G2证据、`WORK_LOG.md`与交接报告。

若API仍不能提供资产级许可、固定revision、文件树/size或诚实固定方案，立即停止并保持`NO_GO`。即使元数据门通过，也只能向00申请下一步“明确文件下载与字段审计”授权，不能直接下载数据或冻结LAI-GAI。

## 7. 门状态

授权生效时：

- LAI-GAI：`NOT_FROZEN_METADATA_API_AUDIT_AUTHORIZED`
- G1：`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`
- G2：`NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`
- `formal_split=false`
- 任务20：`PROHIBITED`

## 8. 执行后关闭

任务10执行后由`REVIEW-00-LAI-GAI-OSF-API-20260714`关闭本授权：一次请求间隔0.996519秒低于1秒硬门，且`K8XVH`授权file-list为空。已有响应仅作带协议偏差的观察证据，不授予G门信用；不批准重跑或继续网络访问。
