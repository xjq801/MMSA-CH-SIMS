# 20-M3 progress

## 2026-07-17 完整18项任务续跑

- 已读取完整任务20清单与实验编码技能合同，按六个批次展开。
- 已冻结 HANDOFF、dataset、split、label-provenance、leakage 五个输入 SHA256。
- 已确认工作区 clean；下一步先用7890代理重试独立环境安装，再以测试先行扩展统一评测核心。

## 2026-07-17 第1–5项完成

- 用7890代理完成独立正式环境，formal-carm smoke与pip check通过。
- 新增冻结JSON schema、common config、run manifest schema和manifest构建器。
- 扩展canonical loader、topic mean资格门与四种最低基线统一runner。
- 测试经历三次预期红测：缺API、混合split误拒、绝对路径泄漏；均按根因修复，最终10项通过。
- 在正式CSMV train/dev上完成smoke，不运行test、不产生论文表格；第6–18项未启动。

## 2026-07-17

- 完成审计、计划隔离与第一批实现。
- 新增 `scripts/task20_baseline.py`、`tests/test_task20_baseline.py`、`configs/task20-baseline-v1.yaml`、`requirements-task20-lock.txt`。
- 已通过：`python -m unittest -v tests.test_task20_baseline`（3/3）；`python -m compileall -q scripts tests`；`scripts/run_preparation_checks.py` 返回无 blocking checks，但 formal 环境仍 BLOCKED_M1。
- 已记录失败：独立环境 pip 安装因代理不可连接失败；不得写成 faiss 已解决。

## 2026-07-17 第1–5项交付门关闭

- 准备检查首次因误扫 `.venv-task20` 第三方依赖而阻塞；先新增失败回归测试，再最小修复虚拟环境目录排除规则。
- 修复后回归测试与全量单测 19/19 通过，准备检查 exit 0，`formal_model_work_ready=true`。

## 2026-07-17 第6–18项启动

- 用户授权继续执行第6–18项，并授权高算力实验优先使用租用GPU。
- 已完成远端只读预检：SSH可达并认证成功，A30 24GB空闲；远端PATH无`python3`，环境锁定仍在进行。
- 已把统一评测扩展（10–14）置为当前实现批次；其后依次执行legacy、官方/强基线、冻结特征模型与运行交付。

## 2026-07-17 第6–18项阶段进展与GPU阻塞

- 第10–14项代码与冻结配置完成；全量测试增至35项通过。
- 官方revision与legacy数据资格审计完成；两者均因可复核的数据/代码/输入不匹配未运行虚假数值。
- I3D不可逆汇总缓存、pooled MLP、temporal attention与训练runner完成；CPU smoke和同seed一致性通过。
- 远端A30硬件可见但GPU运行时未通过；正式12-trial、单种子完整run、test一次评测、正式bootstrap和最终G3包暂停。

## 2026-07-17 GPU修复与强视觉runner闭环

- 定位远端安装失败主因为PyPI不可达；公开CUDA wheel经双端SHA-256一致性校验并输出安装成功，但实例随后失联，CUDA smoke仍未完成并已立即报告。
- 发现并以红测修复pooled test早停泄漏：test不再进入训练或epoch选择。
- 实现完整序列temporal-attention train-only标准化、冻结动态padding、12-trial/dev选择和test只前向runner。
- temporal本地CPU工程smoke两次同seed独立复跑通过，三类核心产物hash一致；全量测试增至46项通过。

## 2026-07-17 任务6原48维重跑

- 先新增6项legacy测试并经历缺模块/缺API两轮预期红测，随后实现48维loader、发布者隔离split、二分类指标、dev-only选择与test一次性负门。
- 冻结独立native legacy配置；三模型单trial dev-only smoke合计约4.8秒，确认无需租用GPU。
- CatBoost/HGB/LightGBM各12-trial完整重跑完成，test各评测一次，总耗时36.4秒；结果标记`COMPLETED_LEGACY_NATIVE_NON_T0_NON_COMPARABLE`。
- 已生成本机忽略的metrics/predictions/split/run/hash bundle，并更新基线表、执行审计和实验登记；CSMV正式协议与G门未修改。

## 2026-07-17 任务7正式run准备

- 复核官方snapshot仍只有README/LICENSE/数据，VC-CSA代码缺失且目标评论输入不符合T0；不冒充官方复现。
- 本地3070 Ti + PyTorch CUDA预检通过，I3D必需8210 hash/覆盖无漂移；GPU smoke只评dev并完成。
- 通过红测新增进程内只读序列缓存，消除每epoch重复打开I3D文件；全量两epoch由旧路径外推的长时运行降至20.8秒实测。
- 全量测试增至53项通过；下一步先提交固定clean commit，再执行12-trial dev选择与冻结selection后的test一次评测。

## 2026-07-17 任务7完成

- 缓存优化提交`14027a0`后，以clean commit执行全量temporal-attention 12-trial dev搜索，13分30秒完成并冻结selection。
- 按冻结selection执行唯一一次test，91秒完成；1675条预测、manifest、指标和test负门复核通过，无本机路径。
- baseline-table、执行审计、实验登记、G3草案与计划状态已更新；任务7标记为`COMPLETED_VIA_REIMPLEMENTATION_STRONG_BASELINE_SINGLE_SEED`，非VC-CSA官方复现。

## 2026-07-17 任务15/16/18启动

- 审计确认任务15仍缺正式全量GPU dev同seed独立复跑；任务16已有草表但未冻结为任务16交付，任务18仍是未提交00的G3草案。
- 新增任务20 run比较器测试，首轮因比较模块不存在按预期失败；最小实现后3/3通过。
- 比较合同要求clean、completed、同config/input/code/environment/seed/split，并逐项验证manifest声明fixity和四个核心产物hash；下一步提交clean代码后运行正式dev replay。
