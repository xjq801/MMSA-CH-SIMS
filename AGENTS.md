# 项目执行代理规范

本目录及所有子目录内的执行工作受以下规则约束：

1. 研究与阶段需求以`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md`当前版本为唯一总纲；任务10以总纲第17节任务10为准。
   - 本项目从总纲v1.15起只执行T-AFFC的CARM群体情绪预测路线；当前执行版本为v1.25（Task30/40负结果不变；Task45因阴性对照失效保持`CLOSED_NOT_PASSED`待00独立终审；未来Task46改为后验效用分布学习与risk-budget三动作，但仍未创建，`TRAIN_ROUTER_CONFIRM`与formal test封存；Task50未创建；保留Video2Reaction双轨强基线，不恢复已撤回v1.17数值门）。
   - IJCV方向已迁至`D:\MMSA-CH-SIMS - IJCV方向`；本项目不得创建或执行J0—J2、JH1—JH3、任务25或任务65。
2. 开工前读取`WORK_RECORD_POLICY.md`及`WORK_LOG.md`最后一条记录，先运行`git status --short --branch`刷新现实状态。
3. 每次新增功能、实质进展、修复、重要测试、决策或阻塞变化，必须在同一工作批次向`WORK_LOG.md`追加完整记录；历史记录不得改写。
4. 记录必须包含实际文件、验证命令和真实结果。失败不得删除，未推送不得写成已同步。
5. 提交或交付前运行：
   - `.\.venv\Scripts\python.exe scripts\validate_work_log.py`
   - `.\.venv\Scripts\python.exe scripts\run_preparation_checks.py`
6. 工作记录不得包含密钥、Cookie、敏感评论正文、用户标识或秘密下载链接。
7. 专用事实继续写入其权威台账；`WORK_LOG.md`只记录本次行为与证据，不替代数据、实验和claim—evidence台账。
