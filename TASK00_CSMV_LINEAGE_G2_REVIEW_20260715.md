# 任务00：CSMV媒体lineage与G2候选复审

> 复审编号：`REVIEW-00-CSMV-LINEAGE-G2-20260715`  
> 复审日期：2026-07-15  
> 审核对象：任务10 / M1—M2数据与协议  
> 总纲依据：v1.8第2月G2、第17节任务10第3.11—3.12节

## 1. 正式裁定

1. **接受命名空间纠正。** `CSMV_rawLinks.xlsx`中的`ID`是CSMV内部`video_file_id`，URL路径末段是TikTok平台源视频ID。官方README只把工作簿定义为内部视频到原始网页链接的映射，并未规定两种ID必须相等；8210个内部键对正式集合100%覆盖。因此旧“2644行ID—URL路径ID错配”裁定撤销为`CLOSED_NAMESPACE_MISINTERPRETATION`，不要求改写上游映射。
2. **接受同源split修复。** 8210个内部样本形成8008个平台源视频族；202个重复族、404条样本已在划分前归并。修复后`group_by_video_v1`和`hashtag_heldout_v1`的source-group跨split均为0，负面夹具能够阻断故意制造的同源交叉。
3. **G1继续为`PASS`。** LAI-GAI冻结和此前G1裁定不变。
4. **G2暂不通过。** 正式状态为`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_REPRODUCIBILITY_STALE`。
5. **全局`formal_split=false`、`formal_model_use_allowed=false`保持。** 不创建任务20、不训练、不建正式索引。

## 2. 独立复核证据

- 00独立运行`scripts/validate_csmv_media_lineage.py`普通模式与`python -I -S`隔离模式，均exit 0：8210条、8008组、202重复组、404重复源行、跨split 0、负面夹具命中、tracked raw URL为0。
- 00独立运行全局泄漏live门，Critical失败0、`PASS_WITH_LIMITATIONS`；独立运行负面selftest，正确输出`LEAKAGE_BLOCKED (expected negative fixture)`且exit 0。
- M1审计、M2数据工程和M2 release状态合同验证均exit 0；这些结果证明当前候选状态被一致表达，不自动等于G2通过。
- `CSMV_MEDIA_LINEAGE_AUDIT_20260715.md`、`csmv-media-lineage-v1.manifest.json`、`csmv-split-v1.manifest.json`与当前canonical的item/source-group/split关系一致。

## 3. G2继续阻塞的两个硬原因

### 3.1 CSMV正式模型输入资产仍未冻结

总纲M1明确要求“下载并验证CSMV标注、视觉特征、官方代码和许可”；G2要求所有正式样本可追溯，任务20启动条件还要求CSMV按其角色合法、固定、可追溯地复现。当前只闭合了人工标签与URL元数据lineage：

- 未取得或验证I3D/VideoMAEv2等正式输入特征包；
- 特征包的资产级许可、固定revision、文件树、总字节数和逐文件hash仍为`UNKNOWN/PENDING`；
- TikTok原始媒体权利和再分发权未被标注许可覆盖；
- 因此当前不能从已冻结manifest构造CSMV正式多模态测试输入。

URL hash和平台源ID能够解决同源分组，但不能替代模型输入字节的许可、固定性与可复现性。不可观察的发布者、时间和内容级近重复可作为不发布相关协议时的限制；正式输入资产不存在则是G2硬阻塞。

### 3.2 当前复现manifest属于旧split

`data/manifests/reproducibility-v1.manifest.json`记录的是source-family修复前的18输出成功重跑。00对其`after_sha256`与当前文件重算后发现9项不一致：

- `DATA_AUDIT_REPORT_V1.md`
- `M2_LEAKAGE_AUDIT.md`
- `data/manifests/csmv-split-v1.manifest.json`
- `data/manifests/dataset-v1.manifest.json`
- `data/manifests/human-gold-v1.manifest.json`
- `data/manifests/label-provenance-v1.manifest.json`
- `data/manifests/leakage-audit-v1.manifest.json`
- `data/manifests/split-v1.manifest.json`
- `data/processed/HUMAN_GOLD/csmv/video_labels.v1.jsonl`

现有`validate_m2_release.py`只检查旧manifest自报的`mismatches=[]`，没有把记录hash与当前文件重算比较；因此其exit 0仅证明旧复现声明格式合法，不能证明本次新split已完成18输出隔离复现。CSMV专项隔离验证有效，但不能替代总纲要求的完整预处理重跑。

## 4. 关闭G2的最小条件

必须同时完成：

1. 取得一个明确用于正式CSMV协议的官方输入资产族（优先单一官方特征族），闭合资产级许可、官方定位、访问条件、固定版本/快照、文件树、总大小、逐文件hash以及8210样本覆盖；许可不明不得进入正式实验。
2. 从冻结raw manifest在隔离进程重建当前CSMV source-family canonical、两个split、泄漏manifest和M2 release；若CUC外部银标根不可用，必须增加不依赖CUC的“公开benchmark核心复现模式”，不得用直接抄写当前hash冒充重跑。
3. 修复release validator，使其现场重算`reproducibility-v1.after_sha256`对应文件；任何漂移必须阻断G2。
4. 完成后由任务10再次回交00；只有新的00书面裁定可以把全局`formal_split`和`formal_model_use_allowed`改为true并允许创建任务20。

## 5. 研究边界

本复审不否认任务10已完成的lineage与泄漏修复，也不要求访问TikTok媒体URL。CUC是辅助SILVER，其质量不足不应阻塞公开benchmark；但当前复现器把CUC与公开主集耦合，必须通过核心复现模式或恢复合法只读根解除工程耦合。时间split、publisher-held-out和内容指纹审计继续标记`NOT_APPLICABLE/UNOBSERVABLE`，不得宣称已证明安全。
