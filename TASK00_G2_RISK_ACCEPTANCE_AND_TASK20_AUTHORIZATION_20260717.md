# 任务00：G2风险接受与任务20启动授权

> 决策编号：`SC-20260717-01`  
> 日期：2026-07-17  
> 用户指令：修改总纲，将门拆为“协议/数据G2通过”和“资产风险延期接受”，放行任务20  
> 总体裁定：`G2=PASS_WITH_ACCEPTED_ASSET_RISK`  

## 1. 正式裁定

1. `G1=PASS`保持不变。
2. `G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`：样本血缘、标签隔离、T0评论隔离、泄漏正负门、第二主集、I3D本地fixity/schema/8210覆盖、序列协议、19项隔离复现和M2本地发布包均已通过。
3. `ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`：I3D资产级许可、稳定官方revision和权利方包身份/fixity证明仍未知；用户明确接受其延期风险，该风险不再阻塞内部研究。
4. `formal_split=true`，仅表示冻结数据协议可用于本项目内部验证性实验；不产生I3D再分发权。
5. `internal_model_use_allowed=true`；允许创建任务20、安装正式环境、训练统一基线和建立train-only索引。

## 2. 授权范围

任务20只可使用`csmv-i3d-quarantine-v1.manifest.json`固定的本地I3D字节、8210必需键和既定split。允许：

- 建立锁定环境与统一配置；
- 实现数据加载、指标、预测文件和公平基线；
- 在train/dev上调参与选择，在冻结test上按预注册规则评测；
- 建立仅含train候选的索引；
- 生成不含原始特征的模型、日志、预测与统计工件。

## 3. 禁止与强制披露

- 禁止把I3D `.npy`、junction、本机源路径或派生可逆特征提交Git、公开发布或再分发；
- 禁止声称“权利方已授权”“官方revision已固定”“官方checksum已闭合”或“本地包已获官方身份确认”；
- 论文、Data Card和复现说明必须披露资产许可/revision/权利方fixity未知，以及本地hash与获取边界；
- 禁止因放行任务20而改变T0、标签、split、序列协议或test隔离；
- 禁止把任务20基线结果直接写成最终论文主结论；正式五种子与全局冻结仍由任务50完成。

## 4. 止损条件

若权利方明确否认研究使用、证明本地包身份不一致，或出现I3D字节/8210覆盖/hash漂移，则立即：

1. 停止依赖该资产的新实验；
2. 将相关结果标记`ASSET_INVALIDATED_DO_NOT_REPORT`；
3. 回到任务10更换合法输入或收缩论文；
4. 不以已投入算力为理由保留不可发表结果。

## 5. 任务20启动合同

- 任务名称：`20-M3 基线与统一评测`
- SSOT：总纲v1.16第17节任务20
- 输入：`HANDOFF_10.md`、dataset/split/label-provenance manifests、T0政策、实验协议、泄漏威胁模型、本授权文件
- 第一阶段：只完成环境/配置/加载器/指标/最小基线计划与测试，不并发引入teacher、memory或CARM完整方法
- 退出门：G3；公平基线、统一评测、预测文件合同和可复现包通过00复审

