# 项目风险登记

> 维护任务：00-总控与决策  
> 当前快照：2026-07-16  
> 规则：风险关闭必须链接到可复核证据；`UNKNOWN`不能按通过处理。

| 风险ID | 风险 | 当前证据 | 影响 | 当前控制 | 状态/恢复条件 |
|---|---|---|---|---|---|
| `R-DATA-001` | CSMV内部ID与平台ID命名空间混淆及同源split泄漏 | 旧规则误要求两类ID相等；真实风险为202个重复源视频族，修复前100族跨video split、115族跨hashtag split | 错误阻塞媒体lineage或产生同源泄漏 | 已建立官方映射语义、8008个哈希源族、先归并后划分、专项负面门；00独立复核通过 | CLOSED_OBSERVABLE_LINEAGE_20260715；内容指纹/publisher/time边界继续受控开放 |
| `R-DATA-002` | LAI-GAI核心图像资产文件树、size/hash和内容对象集合未闭合 | 旧API的`K8XVH`为空；后续独立授权已从官网9页闭合847图、评分、hash和canonical | 原曾阻塞第二主集与G1 | 保留旧失败；以新授权官网资产链和专项validator作为独立证据 | CLOSED_20260715；`REVIEW-00-LAI-GAI-FREEZE-20260715` |
| `R-PROTOCOL-001` | LAI-GAI API审计请求间隔违反硬下限 | 请求2→3为0.996519秒，低于1秒0.003481秒；专项validator exit 1 | 本轮不能声明授权合规，综合准备门保持阻塞 | 不设容差、不追溯豁免、不重跑；采集器未来余量+0.1秒 | CLOSED_FOR_THIS_RUN_NONCONFORMING；历史失败永久保留 |
| `R-CLAIM-001` | 把图像跨域验证夸大为第二多模态视频复现 | LAI-GAI为单图，缺音频/视频；H1/H2字段可能不适用 | 论文构念、实验同构性和投稿可信度受损 | 总纲v1.6限定主张；不适用项记`NOT_APPLICABLE_BY_DESIGN` | CONTROLLED_OPEN；G4/G6据真实证据重新审核 |
| `R-LEAK-001` | 生成prompt或目标类别形成标签捷径 | 预设目标与人类最高评分并非完全一致 | T0输入泄漏、人工真值被伪标签替代 | prompt只存hash/provenance，目标类别标为非真值，二者均禁止进入模型；专项字段与负面门通过 | CLOSED_FOR_LAI_GAI_V1；映射或输入合同升版时重开 |
| `R-DATA-003` | CSMV正式视频/特征输入资产许可与固定性未知 | README仅明确annotations许可；TikTok媒体与Google Drive特征未取得资产级license/revision/file tree/size/hash | 无法构造合法、固定、可追溯的CSMV正式多模态测试输入 | Issue #5等待权利方回复；效率政策允许从官方或可信镜像隔离预取候选特征并核hash/覆盖，但不外推许可、不用于正式模型 | BLOCKING_G2；关闭条件为选定特征族许可/revision/manifest/schema与8210覆盖闭合 |
| `R-REPRO-001` | source-family修复后复现manifest陈旧 | 旧18输出manifest的记录hash与当时9项文件不一致；旧validator未现场重算 | 不能证明当前split可从manifest隔离重建，可能把旧PASS误作新PASS | 公共核心隔离重放扩为19项；validator现场重算；00独立重跑 | CLOSED_20260715；19项当前零漂移，后续任一漂移继续fail-closed |
| `R-IJCV-001` | 当前CARM视觉方法性不足且与VEDL近邻撞车 | 专刊强调新CV方法；PC Loss、SAMNet、MFRN已覆盖分布结构、主观分支/affective memory和特征精炼 | scope匹配但可能因增量性/应用层建模被拒 | 独立IJCV合同改为响应分布几何视觉表征；J0近邻矩阵、J1强基线、J2单变量证据硬门 | OPEN_BLOCKING_IJCV；J2前不得写成可投稿 |
| `R-IJCV-002` | 缺少第二个像素可得、许可固定的人工主观分布集 | LAI-GAI已冻结；Flickr_LDL/Twitter_LDL/Emotion6/OASIS/NEmo+仍需逐资产准入 | 单一847图小集不足以支撑IJCV视觉方法与泛化主张 | 2026-08-12前执行J0；至少再冻结一个像素人工集；CSMV只作可选外验 | OPEN_BLOCKING_J0；失败则停止IJCV专刊冲刺 |
| `R-INTEGRITY-001` | IJCV与T-AFFC形成一稿多投或重复发表 | 两路线共享研究构念与部分数据基础；IJCV明确禁止稿件同时在别处审议 | 直接伦理拒稿、撤稿或声誉风险 | 主问题/方法/主表/claim-evidence/文稿物理隔离；任务65做重叠审计；投稿时披露相关稿 | CONTROLLED_OPEN；任一重叠Critical即双稿至少一稿No-Go |
| `R-SCHEDULE-001` | IJCV 2026-12-15固定截稿压缩方法与复现周期 | 从2026-07-16起不足五个月；J0数据、强基线、五种子与写作均未完成 | 为赶截稿跳过公平基线、统计或许可门 | J0 08-12、J1 09-12、J2 11-15；任一失败即止损；T-AFFC顺延到2027-05 | OPEN_HIGH；不得通过加班承诺替代阶段证据 |
