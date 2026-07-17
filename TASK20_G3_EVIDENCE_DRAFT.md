# 任务20 G3证据草案

> 当前裁定：`NOT_READY_REMOTE_GPU_RUNTIME_AND_FORMAL_RUNS_INCOMPLETE`  
> 本文件不修改G门，不代表00已验收。

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

## 未闭合证据

- 可用远端GPU运行时；公开CUDA wheel已校验上传并输出安装成功，但实例随后失联，最小矩阵仍未验证。
- 12-trial正式dev选择、单种子完整run、预注册test一次评测。
- temporal-attention正式run和与最低基线的2000次视频级paired bootstrap。
- 正式baseline-table数值与可交00的最终G3包。

## 止损边界

I3D许可、官方revision、权利方包身份/fixity仍未知；若权利方否认或固定hash/8210覆盖漂移，所有相关运行标记`ASSET_INVALIDATED_DO_NOT_REPORT`。禁止提交、发布或再分发I3D序列、junction、本机路径或可逆受限资产。
