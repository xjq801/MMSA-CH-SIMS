# 开工准备包验收报告

> 验收日期：2026-07-14  
> 上位总纲：`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.5

## 结论

开工准备包必要。它冻结T0边界、复现入口和安全红线，能防止M1阶段在许可、泄漏和环境未明确时直接下载或训练。已存在且达标的项目没有重做；新增工作均为非破坏性文件，不移动历史资产。

| 类别 | 判定 | 主要证据 | 后续边界 |
|---|---|---|---|
| 研究边界 | PASS | `T0_INPUT_POLICY.md` | 变更必须版本化并重跑受影响实验 |
| 目录与版本 | PASS | Git基线`847a07c`、`.gitignore`、`PROJECT_STRUCTURE_POLICY.md`、各区README | 历史资产不自动移动或删除；仓库暂无远端 |
| 环境 | PARTIAL/BLOCKED_M1 | `ENVIRONMENT_LOCK.md`、`requirements-lock.txt`、环境smoke脚本 | 历史环境可用；正式CARM环境和空环境重建待数据门后冻结，当前缺faiss |
| 数据与存储 | PASS_PRE_DOWNLOAD | `DATA_SOURCE_LEDGER.md`、`data/README.md`、约75GB可用空间 | 数据大小/许可未明，禁止批量下载 |
| 实验纪律 | PASS | `configs/experiment.bootstrap.yaml`、验证器、测试、实验登记表 | 正式脚本必须接受`--config`并保存运行清单 |
| 安全与合规 | PASS_LOCAL/BLOCKED_EXTERNAL | `.env.example`、`.gitignore`、安全清单；本地密钥扫描0命中 | 账户侧凭证轮换需用户确认；此前禁止API/付费调用 |
| 时间与资源 | PASS | `RESOURCE_TIME_POLICY.md` | M1前云预算0元，每月至少4天缓冲 |
| 文献与写作 | PASS_SCAFFOLD | `references/references.bib`、`CLAIM_EVIDENCE_MATRIX.md` | 文献真实性和claim证据随M1—M8逐条填充 |

## 开工判定

允许立即进入M1的只读许可核查、数据可行性审计和小型元数据验证。仍禁止批量下载媒体、购买存储、调用付费LLM、训练新模型或宣称正式CARM环境已冻结。

重复验收命令：`.\.venv\Scripts\python.exe scripts\run_preparation_checks.py`。
