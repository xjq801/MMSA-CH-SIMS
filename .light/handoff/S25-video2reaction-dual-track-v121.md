---
session_no: S25
contract_version: 2
suggested_title: "[T-AFFC] S26 monitor Task20 and preregister Video2Reaction intake"
parent_session: S24
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-28
---

# S25 Video2Reaction dual-track v1.21 handoff

## 当前阶段

- 当前SSOT为`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.21，第17节规格v1.5。
- G1=`PASS`、`G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`、`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`、G3=`PASS_WITH_LIMITATIONS`；Task30仍未创建。
- Task20正式核心不变；最新已提交记录为Epoch 27—28闭环，Epoch 29运行中，永久`NON_T0/INELIGIBLE`，不能进入任务50或论文claim。

## 已完成

- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` — 新增Video2Reaction公开资产边界与双轨执行合同；`validate_taffc_v121_video2reaction_plan.py`复跑`passed=true`。
- `DATA_SOURCE_LEDGER.md`、`CLAIM_EVIDENCE_MATRIX.md`、`CONTRIBUTION_PRIOR_ART_MATRIX.md`、`RISK_REGISTER.md`、`TASK_REGISTRY.md`与`.light/*` — 同步`SILVER_LLM_HUMAN_VERIFIED`、双轨证据角色和不可横比规则；专项validator检查8个活动文件并PASS、`errors=[]`。
- `scripts/validate_taffc_v121_video2reaction_plan.py` — 检查Task20未追溯扩项及银标未误标HUMAN_GOLD；首次红灯3项后复跑`passed=true`。
- arXiv:2607.06875与`infofusionlab/Video2Reaction` Hugging Face数据卡 — 官方源人工确认复核完成；本批下载0项、模型运行0次。

## 工作区状态

- 本批刷新时共享主仓库`main=origin/main=4b68eb0`；tracked变更仅为00所有的v1.21总纲、配套台账、validator、工作日志和本卡。
- 用户已有未跟踪`NEmoP/`、`__MACOSX/`与Task20 `tmp/`均未读取、未暂存、未修改。
- `light-memory-pm pm.py`的既知`_shared/passport`布局问题未重试；直接使用底层`passport.py`重算state hash。passport validate为WARN，仅因历史stage10 gate缺hash/timestamp，不是本批新增失败。
- `check_project_card.py`首次误用不存在的`--root`参数而exit 2；改用`--project-dir .`后累计0条发现并通过，失败未删除。

## 待用户回答

- none — 用户已明确批准“就这么完善总纲”；本批没有下载、付费、远程训练或Task30创建授权。

## 核心决策

1. Video2Reaction是closest/direct prior，但其公开标签固定为`SILVER_LLM_HUMAN_VERIFIED`，不是第三HUMAN_GOLD主集。
2. V2R-A是论文主对比义务：在CSMV冻结协议上公平适配直接内容模型/LDL；V2R-B是独立银标视频域外部验证。
3. 两轨分表；Video2Reaction论文原生Top-3 F1只用于同协议复现核对，不与CSMV绝对指标横比。
4. V2R-B原始评论不公开，H1固定`NOT_APPLICABLE_DATA_NOT_RELEASED`；memory只能使用train公开内容表示与反应分布。
5. 本版不改变G1—G3、Task20评测核心、I3D风险、Task30创建状态，也不恢复v1.17数值硬门。

## 阻塞/风险

- Video2Reaction HF revision、逐文件fixity、movie overlap和原始视频合法恢复率尚未冻结；B轨仍为计划。
- Video2Reaction原始视频不直接再分发，独立音频、完整转写和原始评论不保证公开；不得把派生特征包写成完整原始音视频文本。
- Task20探索与受限存储生命周期仍未闭环，继续阻止Task30创建。
- CARM、收益感知router及全部G4—G6有效性仍为`TO_VERIFY`。

## 必读文件

- `.light/handoff/S25-video2reaction-dual-track-v121.md`
- `.light/passport.yaml`
- `.light/project_card.md`
- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.21，尤其0.8.1与第17节任务30/40/50
- `DATA_SOURCE_LEDGER.md` DS-012
- `CLAIM_EVIDENCE_MATRIX.md`
- `TASK_REGISTRY.md`
- 最新`WORK_LOG.md`与Task20实时任务

## 下一步

1. 运行`git fetch origin`、`git status --short --branch`和Task20实时读取，刷新唯一seed探索与受限存储状态。
2. 写入Video2Reaction intake字段与V2R-A/V2R-B预算表，但在Task50授权前不下载资产。
3. 核验Task20闭环、H1/H2预注册与共享核心静止条件，再由00书面裁定是否创建Task30。

## 禁止

- Do not treat this card as current fact; run git status/log first。本卡不是当前事实，必须刷新最新WORK_LOG与Task20现实状态。
- 不得把Video2Reaction银标写成人工金标、把公开派生特征写成完整原始音视频文本，或跨数据横比绝对指标。
- 不得追溯改变G1—G3，不得把文本合同通过写成模型有效或论文可发表。
- 不得在Task20未闭环时创建Task30，不得触碰或提交`NEmoP/`、`__MACOSX/`或`tmp/`。

## Continuation prompt

You are the 00-T-AFFC total controller taking over S25. Read AGENTS.md and perform startup checks, then read S25, passport, project_card, master plan v1.21 sections 0.8.1 and 17 tasks 30/40/50, DATA_SOURCE_LEDGER DS-012, CLAIM_EVIDENCE_MATRIX, TASK_REGISTRY and the latest WORK_LOG. Refresh origin/main, git status/log and the live Task20 task; this handoff is not current fact. Keep G1 PASS, G2 protocol/data PASS_WITH_LIMITATIONS, asset admissibility DEFERRED_ACCEPTED_RISK and G3 PASS_WITH_LIMITATIONS. Treat Video2Reaction as closest/direct prior with SILVER_LLM_HUMAN_VERIFIED labels. Preserve the dual-track contract: V2R-A is the mandatory CSMV same-split/T0/evaluator/five-seed/budget fair adaptation; V2R-B is separate native-feature reproduction, movie-disjoint audit and applicable train-only memory/router external validation. Do not compare native Top-3 F1 directly with CSMV, do not invent unavailable comments/audio/transcripts, and keep native H1 NOT_APPLICABLE_DATA_NOT_RELEASED. Do not change Task20 or create Task30 until Task20 exploration and restricted-storage lifecycle close. At session close create S26 and print the next continuation prompt.
