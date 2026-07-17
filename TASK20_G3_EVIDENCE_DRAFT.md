# 任务20 G3证据草案（已被正式包取代）

> 当前裁定：`SUPERSEDED_BY_TASK20_G3_EVIDENCE_PACKAGE_20260718`  
> 正式提交材料见`TASK20_G3_EVIDENCE_PACKAGE_20260718.md`；本文件保留历史草案，不修改G门、不代表00已验收。

## 已闭合证据

- 独立正式本地环境与依赖锁，formal-carm smoke通过。
- 统一配置、run manifest、预测schema、sample-ID/split/class-order合同。
- 九项统一指标：JS、NLL、EMD、Macro-F1、Balanced Accuracy、Brier、ECE、ACE、AURC-JS。
- 视频级配对bootstrap接口与E0 train/eval重叠、样本错位负门。
- 查看test前冻结等预算12-trial、early stopping、dev选择与tie-break规则。
- 最低基线dev smoke；主题均值不适用状态诚实保留。
- 冻结I3D pooled MLP与temporal-attention完整runner；两者CPU工程smoke与同seed一致性验证。
- pooled与temporal的test路径均固定为train拟合、dev早停、test仅前向一次；test数据不会进入epoch选择。
- 任务6/7/8/9不可运行或不适用根因、baseline-table-v1及失败状态。
- 本地3070 Ti正式环境、temporal-attention 12-trial dev选择与冻结selection后的单种子test一次评测；任务7以`REIMPLEMENTATION_STRONG_BASELINE`闭合，VC-CSA官方复现失败状态保留。

## 未闭合证据

- 远端A30运行时仍未就绪，但任务7已由用户明确授权的本地3070 Ti完成；其余需要GPU的正式比较仍需逐项确认环境与资产边界。
- temporal-attention与最低基线的2000次视频级paired bootstrap及任务50五种子统计。
- 正式baseline-table数值与可交00的最终G3包。

## 止损边界

I3D许可、官方revision、权利方包身份/fixity仍未知；若权利方否认或固定hash/8210覆盖漂移，所有相关运行标记`ASSET_INVALIDATED_DO_NOT_REPORT`。禁止提交、发布或再分发I3D序列、junction、本机路径或可逆受限资产。
