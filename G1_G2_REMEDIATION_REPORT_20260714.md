# 任务10 G1/G2缺口修复与决策报告

> 日期：2026-07-14  
> 依据：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.6，第17节任务10  
> 当前结论：本地可修项已继续关闭；G1、G2仍不能诚实判定通过，任务20仍禁止创建。
> 00后续决定：`SC-20260714-01`已批准路径A的范围降级；`AUTH-00-LAI-GAI-OSF-META-RO-20260714`已授权公开网页只读元数据审计。该决定不改变本报告的G1/G2阻塞结论。

## 0. 路径1最新执行结果

公开网页只读元数据审计已完成，详见`M1_LAI_GAI_OSF_METADATA_AUDIT_20260714.md`。`V8DKM`未向合规读取器呈现可用页面行，`8P572`返回安全打开错误，`K8XVH`返回HTTP 403；精确公开搜索也未发现节点级资产元数据。三组件的asset license、revision、file tree、size、hash、gating与字段说明均保持`UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE`。

因此路径1当前为`NO_GO_PENDING_ASSET_METADATA`，不是失败取消，也不是数据准入通过。若继续，必须由00另行批准具体的最小元数据取得方案；本轮未下载、未调用API、未生成映射/split，G1/G2与`formal_split=false`不变。

00随后依据用户明确批准签发`AUTH-00-LAI-GAI-OSF-API-META-RO-20260714`。限额API审计完成26次匿名GET、共382,394 bytes，三节点均公开并声明CC BY 4.0；`V8DKM`与`8P572`文件级size/checksum闭合，但`K8XVH`文件列表为空。边界validator另发现一次UTC请求间隔为0.996519秒，低于1秒硬门且不使用容差掩盖。因此止损状态为`NO_GO_PENDING_RATE_INTERVAL_AND_IMAGE_COMPONENT_FILE_TREE`。任务10已停止访问并回交00，不下载资产、不生成映射/split。

00最终以`REVIEW-00-LAI-GAI-OSF-API-20260714`接受上述交付为`ACCEPTED_AS_NONCONFORMING_OBSERVATION_NO_GATE_CREDIT`，并关闭授权为`CLOSED_NONCONFORMING_NO_RERUN_AUTHORIZED`。LAI-GAI状态固定为`NO_GO_00_REVIEWED_NOT_FROZEN`；不得重跑或继续探索，专项validator与综合阻塞保留。

## 1. 本轮已经修复

1. **CSMV URL表不再因Excel样式损坏而不可读。** 新增Strict OOXML单元格解析，只读工作表内容而不加载上游损坏的theme/styles。
2. **URL表覆盖率已机器核验。** 8210行ID均唯一，并与正式评论split中的8210个视频ID集合100%一致；0缺ID、0缺URL、8210条均为TikTok HTTPS链接。
3. **把“行齐全”与“映射正确”分开验收。** 自动审计发现2644行的表内ID与URL路径视频ID不一致、200行URL重复（URL路径ID重复202行），并把该事实固定到`m1-public-audit-v1.manifest.json`及validator；没有把它写成媒体可恢复PASS。
4. **扩展第二主集止损检索。** VCE在构念/多人分布上高度匹配，但媒体无正式许可且标注时无音频；LAI-GAI有847张AI生成图像、N=2470真人诱发评分，论文明确开放raw data，但它是单图且OSF资产许可仍待逐组件核验。

## 2. 仍未通过及原因

| 门项 | 当前状态 | 不能由本地代码直接修复的原因 | 重新准入条件 |
|---|---|---|---|
| CSMV完整媒体可复现 | `BLOCKED_UPSTREAM_LINK_MISMATCH` | 上游URL表2644行语义错配；TikTok媒体权利、存活率及特征资产许可/版本/size/hash未知 | 上游给出纠正manifest，或确认官方特征包的资产许可、固定版本、完整hash和视频ID映射 |
| 第二人工跨域图像主集/缺失模态验证集 | `BLOCKED_SECOND_PRIMARY_NOT_FROZEN` | 00已批准角色降级，但LAI-GAI逐资产许可、revision、文件树、size/hash、raw字段和split威胁尚未核验 | 先按只读授权完成OSF三组件元数据审计；任何下载或字段检查另行申请；最终由00冻结 |
| G1 | `BLOCKED` | 缺第二合法可复现公开人工主集，CSMV媒体链也有开放问题 | 上述数据门关闭后，由00逐条书面审核 |
| G2 | `NOT_ELIGIBLE` | G1未过；第二主集manifest/split不存在；CSMV语义近重复/同源事件无法在错误媒体映射下完整审计 | 双主集manifest、冻结映射和formal split完成；全部泄漏测试零失败；00书面通过 |
| `formal_split` | `false` | 当前只有CSMV本地候选split；不能把单集候选改名为双主集正式split | 第二主集冻结后重新生成dataset/split/label-provenance并跑全门 |
| 任务20 | `PROHIBITED` | 总纲3.12明确规定未过G1/G2不得创建 | 00书面标记G1、G2均通过 |

## 3. 需要用户/00决定的问题

### 路径A：批准范围降级（建议）

把“第二人工**多模态**主集”改为“第二人工**跨域图像**主集”，首选LAI-GAI：保留`public-induced audience affect`、人工金标、T0与JS divergence，不把生成prompt当标签；把它明确定位为缺失模态/跨域验证，而不是第二视频复现集。

该路径需要：

- 00修订总纲/协议中的第二主集模态要求并记录证据降级；
- 先授权只读核OSF三个组件的license、revision、文件树、size和hash；如必须取得小型公开元数据文件，下载前另报文件名、大小、许可与用途；
- 许可通过后再申请实际数据下载与M2正式构建授权。

优点是媒体来自可追溯生成流程、论文明确有人类raw ratings，最有机会保持JS分布主指标；代价是论文只能声称“视频主集 + 图像跨域人工集”，不能声称两个多模态视频主集。

### 路径B：保持两个多模态主集

授权机构联系人/EULA流程，优先向CSMV核URL/特征资产、向LIRIS-ACCEDE或iNews/NEmo+核许可与媒体入口。该路径周期和成功率不可控；即使LIRIS获批，VA秩仍不能无损承担离散分布主指标。

### 路径C：保持原要求并止损

维持G1阻塞，暂停第四章模型主线，不创建任务20；继续文献、协议和许可等待，不用银标或“能访问的URL”冒充第二人工金标。

## 4. 本任务的推荐请求

请求用户先确认是否同意**路径A的范围降级方向**。若同意，本任务再向00提交`LAI-GAI只读资产元数据审计`授权请求；在获得授权前不调用API、不下载数据/媒体、不修改G门。

## 5. 用户选择与执行状态

- 2026-07-14：用户明确回复“同意路径1”。
- 任务10已把该选择写入`SECOND_PRIMARY_SCOPE_CHANGE_REQUEST_20260714.md`并发送00总控。
- 00已批准`SC-20260714-01`并签发`AUTH-00-LAI-GAI-OSF-META-RO-20260714`；它冻结方向并允许公开网页只读元数据审计，但不等于LAI-GAI资产许可已通过、第二主集已冻结或G1/G2已通过。
