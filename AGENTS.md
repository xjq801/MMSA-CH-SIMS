# IJCV方向项目执行代理规范

本目录及所有子目录内的执行工作受以下规则约束：

1. 全局研究与双论文边界以`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md`当前版本为SSOT；IJCV专线优先读取第0.6节、第18节、`IJCV_TAFFC_DUAL_TRACK_FEASIBILITY_AND_PLAN_20260716.md`及`IJCV_PROJECT_CONTEXT_HANDOFF_20260716.md`。
2. 本项目当前只执行IJCV的J0数据/新颖性/预注册准备；J0书面通过前不得把自己当作任务25，不得正式训练、查看test后选方案或承诺投稿。
3. T-AFFC的评论teacher、train-only受众记忆、CARM路由、CUC舆情外验与任务20—60在本项目只读；不得改名复用为IJCV主创新。CSMV仅在其G2通过后才可作可选视频外验，不能阻塞IJCV J0。
4. 工作目录固定为`D:\MMSA-CH-SIMS - IJCV方向`，当前工作分支为`codex/ijcv-j0`。IJCV新增物优先进入`paper/ijcv/`、`experiments/ijcv/`、`configs/ijcv/`和`references/ijcv/`；不得与原项目另一个任务并发修改同一共享文件。
5. 开工前读取`WORK_RECORD_POLICY.md`及`WORK_LOG.md`最后一条记录，先运行`git status --short --branch`刷新现实状态。源项目的新事实只通过已提交Git状态或书面交接吸收，不能凭聊天猜测。
6. 每次实质进展、修复、重要测试、决策或阻塞变化，必须在同一批次向`WORK_LOG.md`追加完整记录；历史记录不得改写。记录必须含实际文件、验证命令和真实结果。
7. 提交或交付前运行：
   - `.\.venv\Scripts\python.exe scripts\validate_work_log.py`
   - `.\.venv\Scripts\python.exe scripts\validate_ijcv_project_handoff.py`
   - `.\.venv\Scripts\python.exe scripts\run_preparation_checks.py`（继承的全量诊断；本独立克隆未复制Git忽略的I3D `.npy`时，`csmv_feature_preflight/m2_release`预期失败，必须记录但不阻塞只读J0）
   - `git diff --check`
8. 不记录或提交密钥、Cookie、敏感评论正文、用户标识、秘密下载链接、原始大包、模型权重或`.env`。未知许可资产只可进入Git忽略隔离区，不得取得正式实验信用。
9. 正式结论必须按图像/视频等独立内容单元统计；随机种子不是样本量。主指标、SESOI、非劣界、种子、调参预算和多重比较族必须在正式test前冻结。
10. IJCV与T-AFFC必须是两篇实质独立论文；同一稿件、主方法、主表、关键消融或大段正文不得同时送审。正式投稿时按要求披露相关稿。
