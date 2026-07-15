# LAI-GAI v05 OSF公开网页元数据只读审计

> 审计日期：2026-07-14  
> 范围决定：`SC-20260714-01`  
> 授权：`AUTH-00-LAI-GAI-OSF-META-RO-20260714`  
> 审计方式：无需登录的公开网页与公开搜索结果；不调用API，不登录，不预览、流式读取或下载任何资产  
> 当前裁定：`NO_GO_PENDING_ASSET_METADATA`

## 1. 审计目的与不可外推边界

本审计只判断LAI-GAI v05是否具备进入下载前准入复审所需的逐组件元数据，不判断模型效果，也不生成标签映射或split。论文和项目介绍可证明数据集的研究设计与公开意图，但论文许可不能自动外推为OSF图像、评分数据、代码或派生发布的资产级许可。

LAI-GAI若最终准入，只承担“第二人工跨域图像主集/缺失模态验证集”角色；CSMV继续承担完整社交视频多模态及H1/H2机制证据。生成prompt、预设目标类别和模型输出不得作人工真值，默认只保留为provenance。

## 2. 组件级审计结果

| OSF组件 | 预期角色 | 公开定位 | 合规访问结果 | asset-level license | revision/更新时间 | 文件树/文件数/size | hash/checksum | gating/字段说明 |
|---|---|---|---|---|---|---|---|---|
| `V8DKM` | 项目入口 | https://osf.io/v8dkm/ | 定位存在，但合规网页读取器未取得可用页面行 | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` |
| `8P572` | 分析/评分数据 | https://osf.io/8p572/ | 合规网页读取返回安全打开错误；未绕过 | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` |
| `K8XVH` | 图像资产 | https://osf.io/k8xvh/ | 合规网页读取返回HTTP 403；不能据此推断登录门或许可状态 | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` | `UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE` |

对三个节点标识符执行的精确公开搜索没有返回节点级资产元数据，仅返回OSF通用许可、文件与元数据说明。因此不能用通用OSF条款填补任一组件的具体许可、revision、文件树、体量或校验和。

## 3. 可确认与不可确认

可确认：

- 00已批准LAI-GAI的跨域单图角色降级，但只把它列为优先审计候选；
- 官方项目材料将`V8DKM`、`8P572`、`K8XVH`分别指向项目、分析/评分和图像资产；
- 论文级信息支持847张图像、六项研究和N=2470的研究设计描述；这些数字尚不是本地资产manifest证据；
- OSF通用文档明确许可需要由资源持有者选择，且不同OSF对象可有不同许可，故不得把平台或论文许可当成资产许可。

不可确认：

- 三个组件分别适用的资产级许可、许可文本定位与派生发布边界；
- 固定revision、公开更新时间或可复核快照；
- 文件名、文件数、逐文件或汇总体量；
- 页面公开展示的hash/checksum及算法；
- 评分数据逐图、逐参与者字段及公开数据字典；
- 图像—评分稳定键、缺失率、可形成经验分布的有效样本数；
- 适用于后续group/split与prompt泄漏测试的原始字段。

## 4. 合规说明

本轮下载资产为0；未使用OSF或其他API，未使用登录态、Cookie、机构账号或付费服务，未预览/流式读取图像、ZIP、raw data或评分表，未通过下载补算hash，未联系作者，未构建标签映射/split，未训练模型，也未创建任务20。

## 5. 准入判断与下一门

LAI-GAI当前为`NO_GO_PENDING_ASSET_METADATA`，不能冻结为第二人工跨域图像主集。G1保持`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`，G2保持`NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`，`formal_split=false`。

若继续路径1，需要00另行批准一种能合法取得节点级元数据的最小方案，并在执行前明确具体文件或页面、预计大小、许可和用途。取得资产级许可、固定revision、文件树/size、诚实hash固定方案及评分字段证据后，才能申请数据下载，再讨论标签映射、split和完整泄漏门。

## 6. 证据定位

- 范围与授权：`TASK00_LAI_GAI_SCOPE_AND_AUDIT_AUTHORIZATION_20260714.md`
- 机器清单：`data/manifests/lai-gai-osf-metadata-audit-v1.manifest.json`
- 官方项目页：https://www.affectdatabases.amu.edu.pl/
- OSF许可说明：https://help.osf.io/article/148-licensing
- OSF文件说明：https://help.osf.io/article/387-files
- OSF元数据说明：https://help.osf.io/article/696-metadata-on-the-osf

