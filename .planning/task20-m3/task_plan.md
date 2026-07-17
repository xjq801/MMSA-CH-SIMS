# 20-M3 基线与统一评测执行计划

## 目标与边界

执行总纲 v1.16 第17节任务20的18项清单。所有拟合/归一化/索引/特征选择只读 train，dev 只用于预注册选择，test 只做最终评测。I3D 许可、官方 revision、权利方身份/fixity 仍为 `DEFERRED_ACCEPTED_RISK`，禁止再分发受限资产。

## 批次

- [completed] A. 输入与环境冻结（1–3）：交接/hash复核、独立环境、schema/run manifest。
- [completed] B1. 统一评测核心（4–5）：canonical loader、总体均值、主题均值资格/实现、经验分布、多数类。
- [completed] B2. 统一评测扩展（10–14）：完整指标、bootstrap、预测标准、E0。
- [completed] C. Legacy 基线（6、12）：统一CSMV资格仍被数据协议阻断；已按独立冻结的publisher-disjoint原生二分类合同完成CatBoost/HGB/LightGBM各12-trial重跑，明确非T0、不可比较、不可承担主结论。
- [completed] D. 官方/强基线（7）：官方revision无模型代码且输入非T0的失败证据保留；冻结I3D temporal-attention以强视觉重实现完成12-trial dev选择和单种子test一次评测，明确非VC-CSA官方复现。
- [completed] E. 冻结特征模型与 E1（8–9）：pooled MLP/temporal attention及安全test路径已实现；late fusion/cross-attention/E1按单模态登记不适用。
- [in_progress] F. 运行与交付（15–18）：任务15比较器已按TDD实现，待clean commit后执行全量dev同seed replay；任务16表格冻结与任务18 G3提交随后同批完成。

## 冻结输入指针

- `HANDOFF_10.md` SHA256 `47de656e7a8ff391118858bc932b5f7f1b089d98575b1a29e3f608b4e4ac66fb`
- `dataset-v1.manifest.json` SHA256 `1b8ba9f5c4b801f9530b4e97c8f6b777db4562bce37b24d63aa341b64e3e806e`
- `split-v1.manifest.json` SHA256 `6a15f992b9e5839d6f21b4a6d40619f48bb14445b18a0c1814024794f56b6780`
- `label-provenance-v1.manifest.json` SHA256 `0ac81e2db69f1e883599cb654bb679d10c1411f570e97ab6c2678f7699ce5a43`
- `leakage-audit-v1.manifest.json` SHA256 `982c5a75019ae6178f39797664aa390a65c336e2b78ef45c25ece96eb59991dc`

## 验收原则

- 新功能先有失败测试，再写最小实现。
- 每个 run 保存 config/env/code/input hash、stdout/stderr、raw metrics、sample-level predictions 和失败产物。
- 同 seed 两次独立运行只证明同环境复跑，不外推跨硬件绝对复现。
- topic 字段不可用时，主题均值必须明确 `NOT_APPLICABLE_NATIVE_TOPIC_ABSENT`，不得伪造主题。
- 只有一个合法 T0 模态时，E1 登记 `NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`。

## 远程算力授权与执行边界

- 用户已授权任务20第6–18项使用其租用GPU；高算力实验优先使用远端A30。
- 远端连接信息和认证值不得写入计划、日志、Git或run bundle；run manifest只登记脱敏资源类别与GPU型号。
- 2026-07-17只读预检：SSH端口可达，A30 24258 MiB、检查时显存占用0 MiB、GPU利用率0%；系统PATH暂无`python3`，在运行实验前必须先锁定远端Python/CUDA/依赖环境。
- 若远端GPU后续不可连接、不可见或显存不可用，立即停止高算力步骤并向用户报告，不静默转为本地高算力运行。
- 原始I3D `.npy`不得为远端训练而上传；完整序列模型只能在合法既有数据环境执行，或等待用户明确允许本地GPU正式运行。

## 已知阻塞

- 本地 `.venv-task20` 已完成并通过formal-carm smoke；旧的代理失败仅保留为历史失败证据。
- LightGBM依赖与任务6原生兼容重跑已完成；VC-CSA官方代码缺失和输入不匹配继续保留失败记录。
- CSMV 无原生 topic，`topic_heldout_v1.not_assigned=8210`。

## 当前用户限定

用户已授权继续完成总纲任务20第6–18项，并允许先使用本地3070 Ti；任务7强视觉基线在本地既有只读I3D环境运行，不上传或再分发资产。仍禁止提前引入teacher、memory或完整CARM，禁止修改总纲/G门，禁止再分发受限I3D资产。
