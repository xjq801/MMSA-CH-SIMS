# 20-M3 findings

## 2026-07-17 完整任务启动审计

- Git 起点为 `main` 与 `origin/main` 同步、工作区 clean。
- 正式 split 为 `group_by_video_v1`：train/dev/test=`5698/837/1675`；fit scope=`train_only`。
- CSMV 原生 topic 缺失，正式 manifest 明示 `topic_heldout_v1.not_assigned=8210`，故主题均值不能伪造为已实现正式基线。
- legacy 代码存在 CatBoost/HGB 及历史48维资产；LightGBM 与 VC-CSA 可执行入口尚未发现。
- 任务20必须新增 JS/NLL/EMD/Macro-F1/Balanced Accuracy/Brier/ECE/ACE/AURC、视频级 bootstrap、预测标准与 E0 对齐/泄漏负门。

## 第1–5项实现结论

- `.venv-task20` formal-carm smoke 已通过；此前 faiss 单包导入因缺 NumPy 失败，补齐完整环境后关闭。
- 配置冻结在 `configs/task20/experiment.schema.json` 与 `baseline-common.json`；基线变体只改变 `model` 字段。
- 常数/分组统计基线的 `input_features=[]`，四种基线共享 frozen sample IDs、`group_by_video_v1` 与同一标签class order，不读取评论或受限视觉资产。
- CSMV train/dev 实际 smoke 为5698/837，`shared_sample_ids=true`；topic mean 为 `NOT_APPLICABLE_NATIVE_TOPIC_ABSENT`。
- run manifest 最初写绝对路径，回归测试命中后改为仓库相对路径并禁止仓库外路径。

- 旧 `.venv` 为 Python 3.8.9，numpy 1.24.4、scikit-learn 1.3.2 可用，faiss 不可用。
- 独立 `.venv-task20` 已创建；pip 25.0.1 升级成功，但安装 `pytest`/`faiss-cpu` 因代理不可连接失败，环境保持未就绪。
- 任务20最小基线测试使用标准库 unittest，3/3 通过；compileall 通过。
- `run_preparation_checks.py` 真实结果：`blocking_checks=[]`，但 `formal_carm_environment.classification=BLOCKED_M1`、`faiss_available=false`、`formal_model_work_ready=false`。

## 第1–5项交付门修复

- 独立环境就绪后，首次正式准备检查因密钥扫描器只排除精确目录名 `.venv`、误扫 `.venv-task20` 的第三方依赖而失败；命中均位于环境依赖目录，未发现项目密钥。
- 新增回归测试证明命名虚拟环境应跳过、真实源码仍必须扫描；仅扩展目录边界为 `.venv-*`，未放宽任何密钥识别模式。
- 修复后全量单测 19/19 通过；正式准备检查 `blocking_checks=[]`、`secret_scan.hits=[]`、`formal_model_work_ready=true`。

## 第6–18项启动与远端GPU预检

- 用户授权使用租用GPU执行高算力实验，但认证信息不得进入项目文件、run bundle或工作日志。
- 远端SSH端口可达且认证成功；`nvidia-smi`报告 NVIDIA A30、24258 MiB，总显存检查时使用0 MiB、利用率0%，driver 470.57.02。
- 根文件系统约350 GiB、检查时基本空闲；系统PATH中`python3`不可用，因此GPU可用不等于实验环境已就绪，必须继续盘点Conda/Python/CUDA兼容性。

## 第6–18项实现与阻塞结论

- 第10–14项已实现：九项指标、预测标准、E0、视频级paired bootstrap、等预算12-trial/dev-only选择计划；AURC同置信度顺序依赖与float32概率容差均由红测发现并修复。
- CUC legacy 48维2787条全部`legacy_features_available_at_t0=false`，三个split scheme均`not_assigned`，目标为SILVER二分类；不能在不改数据协议的情况下进入统一正式评测。
- 固定官方CSMV revision只含README/LICENSE/数据，没有VC-CSA模型代码；官方输入依赖目标评论，与T0 content-only合同不匹配。
- 已生成8210条I3D mean/std缓存，约69.5MB，不含标签、原始序列或本机路径；pooled MLP与temporal attention实现完成。
- A30硬件可见且空闲，但两种Torch安装通道均无有效进度；平台自带Torch 1.3.1/CUDA 10.1的最小CUDA矩阵运算30秒未完成，远端GPU运行时判定不可用。
- 本地CPU两epoch smoke在修复manifest缺字段后通过；同seed两次predictions/metrics SHA-256完全一致，仅支持工程复跑，不是正式论文结果。

## GPU修复、test负门与强视觉runner

- 远端网络根因分层：PyPI超时；官方PyTorch索引和国内镜像可达。公开PyTorch 1.13.1/CUDA 11.7 wheel经本地代理下载、并行上传和远端重组后，长度与SHA-256一致并输出安装成功。
- 后续依赖安装时SSH通道异常结束，端口复查不可连接；未能执行CUDA最小矩阵，因此远端环境继续是`REMOTE_GPU_RUNTIME_UNAVAILABLE_ENVIRONMENT_NOT_READY`。
- pooled runner原test路径把test用于早停；正式test从未运行。新增红测后改为train拟合、dev早停、test只前向一次，并让冻结dev selection进入manifest输入hash。
- temporal-attention新增train-only流式时序标准化、冻结动态padding训练、12-trial runner、dev/test负门、失败产物和manifest；test同样只前向一次。
- temporal CPU smoke固定32 train/16 dev、1 trial、2 epochs；两次独立同seed运行的predictions/metrics/selection hash完全一致，manifest均通过schema；不具有论文结果资格。

## 任务6原48维native legacy重跑

- 租用A30端口复查超时，不得标记为可用；用户允许本地3070 Ti，但2787×48树模型单trial烟测仅约4.8秒/三模型，故统一使用本地CPU以保持三模型执行口径稳定。
- 新增独立`LEGACY_NATIVE_COMPATIBILITY_ONLY`合同，不改变CSMV八类分布/T0正式协议；publisher hash split为1905/307/575条，28/6/9组，交集为0。
- CatBoost/HGB/LightGBM各执行12个冻结trial，dev选参后test各调用一次；完整运行36.4秒。
- test Macro-F1分别为0.5346/0.4591/0.3645，正类Recall分别为0.2183/0.1338/0.0528；低值与跨publisher泛化问题原样保留，不做test后适配。
- run bundle只含单向hash样本/组ID和聚合fixity，不含原始特征、本机路径、旧论文数字或受限I3D资产；结果仅用于legacy附表。

## 任务7本地GPU预检与运行性能根因

- 本地3070 Ti Laptop GPU可被PyTorch 2.4.1+cu121识别；任务20独立环境CUDA可用，8210个必需I3D hash/覆盖预检通过，许可、revision与权利方证明仍保持待定风险。
- temporal runner/test负门11项通过；GPU smoke为32 train/16 dev、1 trial、2 epoch，只看dev且未读test。
- 全量5698 train/837 dev单epoch旧路径耗时30.4秒、峰值CUDA显存154 MiB；静态调用审计显示20-epoch trial会重复触发约13万次序列访问，瓶颈是重复文件打开而非GPU算力。
- 新增只在当前进程内的只读序列memoization，先以缺API红测证明测试有效；每个底层I3D文件只加载一次，不写磁盘、不改变标准化统计、模型、预算或split。
- 优化后全量两epoch耗时20.8秒，预计12-trial常见早停总耗时20–60分钟；无需租新实例，且继续满足禁止I3D外传边界。

## 任务7正式强基线结果

- dev运行绑定clean commit `14027a0`，12/12 trial完成；选中trial 4（hidden=128、dropout=0.3、lr=0.001、best epoch=5），冻结selection hash为`dce53eeb...c97dfbf`，dev JSD=0.177014。
- 唯一test运行使用同一seed和冻结selection，train拟合/dev早停/test一次前向；重训dev JSD与冻结值完全一致，1675条预测完整，test JSD=0.182668。
- test其余指标：NLL 1.715192、EMD 0.162983、Brier 0.227379、ECE 0.053885、ACE 0.054004、AURC 0.175399、Macro-F1 0.137048、Balanced Accuracy 0.148577。
- task7以强视觉重实现单种子结果闭合；VC-CSA官方代码缺失/目标评论输入不匹配失败保持不变。结果仍受accepted asset risk约束，并待任务50五种子统计。
