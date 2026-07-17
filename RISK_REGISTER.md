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
| `R-DATA-003` | CSMV I3D资产许可与官方身份仍未知 | 本地9942文件、8210必需键、schema和hash闭合；权利方未确认asset license、稳定revision或包身份/fixity | 可能影响审稿、复现、模型/特征发布及后续合规；若权利方否认，依赖I3D的结果须撤回 | 用户以`SC-20260717-01`接受延期风险；仅内部研究、禁止再分发、强制披露；继续等待Issue #5但不阻塞任务20 | ACCEPTED_HIGH_RISK_NONBLOCKING_G2；权利方否认或hash漂移立即止损 |
| `R-REPRO-001` | source-family修复后复现manifest陈旧 | 旧18输出manifest的记录hash与当时9项文件不一致；旧validator未现场重算 | 不能证明当前split可从manifest隔离重建，可能把旧PASS误作新PASS | 公共核心隔离重放扩为19项；validator现场重算；00独立重跑 | CLOSED_20260715；19项当前零漂移，后续任一漂移继续fail-closed |
| `R-IJCV-001` | 当前CARM视觉方法性不足且与VEDL近邻撞车 | 专刊强调新CV方法；PC Loss、SAMNet、MFRN已覆盖分布结构、主观分支/affective memory和特征精炼 | 仅影响已迁出的IJCV方向，不再影响本项目G门 | 风险及J0/J1/J2控制已迁至独立IJCV项目；本项目不执行视觉表征路线 | TRANSFERRED_TO_IJCV_PROJECT_20260716 |
| `R-IJCV-002` | 缺少第二个像素可得、许可固定的人工主观分布集 | LAI-GAI已冻结；其他图像集仍需逐资产准入 | 仅影响已迁出的IJCV方向，不再是本项目数据门 | 第二像素人工集准入由独立IJCV项目维护；本项目任务10不再取得该数据 | TRANSFERRED_TO_IJCV_PROJECT_20260716 |
| `R-INTEGRITY-001` | IJCV与T-AFFC形成一稿多投或重复发表 | 两路线可能共享研究构念与部分数据基础 | 若未来两项目都形成稿件，仍可能产生投稿伦理风险 | 项目、分支、总纲、claim和主实验已物理分离；跨项目只消费已提交事实并在投稿时披露相关稿 | CONTROLLED_CROSS_PROJECT；不阻塞本项目当前G门 |
| `R-SCHEDULE-001` | IJCV 2026-12-15固定截稿压缩方法与复现周期 | IJCV方向已独立迁出 | 不再挤占本项目T-AFFC日历与资源优先级 | 本项目恢复2027-05-12 T-AFFC单线日历；IJCV期限由独立项目自行管理 | TRANSFERRED_TO_IJCV_PROJECT_20260716 |
