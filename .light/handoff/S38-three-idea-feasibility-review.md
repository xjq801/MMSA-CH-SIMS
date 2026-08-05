---
session_no: S38
contract_version: 2
suggested_title: "[TAFFC-CARM] S39 三idea统一路线查新与数据门裁定"
parent_session: S37
project: mmsa-ch-sims-taffc-carm
date: 2026-08-05
source_context: total-control-03-read-only-idea-review
target_thread: total-control-03
---

## 当前阶段

本卡记录用户要求的“三idea统一路线”只读初审：T0目标评论不可用、历史经验适用性判断、可预测性与三源不确定性/预测区域。它不是路线批准、实验授权、SSOT变更或论文claim。`main/origin/main`在审查开始时均为`e51621a18f87b2648d8b1a6f8770d5a41d98e74f`；工作树已有用户/侧对话变更，未被覆盖或暂存。

Task30仍为`CLOSED_NOT_PASSED`，H1开发门为`NOT_PASSED_MECHANISM_NOT_STABLE`，formal test未materialize，Task40/50未创建。G1—G3、I3D许可/revision/权利方身份/fixity UNKNOWN、Task20 NON_T0/INELIGIBLE及受限存储删除边界均不变。

## 已完成

- 四技能与SSOT复核 — 命令读取并人工确认`light-literature-search`、`light-data-engineering`、`light-idea-critique`、`light-research-plan`全文，以及总纲v1.21第2—7、10、11、17节、S37、数据卡、数据台账和论文SSOT。
- 定向前作地图 — 在线检索验证Video2Reaction、T-BPPM、AAAI 2025 synthetic live-comment features、SCRAG、RAMER/RAER、LEEP/LogME、2026 uncertainty routing、情感识别conformal prediction及有限标注不确定性工作可定位；人工确认本轮覆盖内未发现完全同构组合，但不等于穷尽检索或世界首创证明。
- `data/processed/HUMAN_GOLD/csmv/video_labels.v1.jsonl`与`data/processed/HUMAN_GOLD/lai-gai-v1/canonical.jsonl` — PowerShell只读命令验证CSMV `n=8210`、评论数`min=2, q25=10, median=14, q75=17, max=20`且`1959/8210`少于10条；LAI-GAI `n=847`、`min=58, median=75, max=96`。
- `.light/handoff/S38-three-idea-feasibility-review.md` — 人工确认统一候选问题、数据角色、一般实验顺序、T-AFFC条件性判断和kill criteria已形成，且未写入实验授权或正式claim。
- 独立收尾门 — `handoff_contract.py`最终返回PASS；`scripts/validate_work_log.py`验证261条、0错误；`git diff --check` exit 0；`scripts/run_preparation_checks.py` exit 0、`blocking_checks=[]`，同时诚实保留`formal_model_work_ready=false`、`faiss_available=false`和`g2_asset_ready=false`。

## 工作区状态

- Git现实：审查开始时worktree为`dirty`；本地`main`跟踪`origin/main`且两者一致，已有`WORK_LOG.md`修改、未跟踪S37及用户目录`NEmoP/`、`__MACOSX/`、`tmp/`；这些先存变更未被覆盖、移动、暂存或删除。`git rev-parse HEAD`与`git rev-parse origin/main`均为commit `e51621a18f87b2648d8b1a6f8770d5a41d98e74f`。本轮仅新增S38并向WORK_LOG追加记录，处于`unpushed`状态，尚未暂存、提交或推送。

## 待用户回答

- decision_id=CARM_IDEA_20260805_UNIFIED_ROUTE | question=是否授权把“三idea统一候选”升级为版本化系统查新与数据fitness任务？ | option_a=授权只读查新与数据门；影响：允许冻结检索协议、数据身份/适配合同和idea-critique，但不授权模型实验、formal test或正式claim | option_b=仅保留一般方案；影响：停止新增研究范围，保持Task30关闭与Task40/50未创建

## 接受吸收的判断

1. T0目标评论不可用是正式信息协议，不是方法创新；训练评论优先只用于构造历史反应计数/分布与监督标签。
2. 核心方法候选是out-of-fold历史净效用预测：`Delta_i=D(y_i,f0(x_i))-D(y_i,fH(x_i,H_i))`，路由器只能读取T0内容、train-only邻居诊断和推理时可得不确定性。
3. 三源不确定性须分别验证：群体真实分歧、有限评论采样、模型/OOD；预测区域对经验分布的coverage与对潜在总体反应的解释必须分开。
4. 主路线应先跑现象门与Oracle headroom，再决定是否训练路由器；不得先堆teacher、MoE、RAG或复杂Dirichlet头。

## 拒绝或降级的判断

1. “训练看评论、测试只看视频”“视频到观众反应分布”“普通gate”“Dirichlet输出”“conformal prediction”均已有直接或相邻前作，任何一项单独都不足以支撑T-AFFC主创新。
2. Task30评论特权KD没有稳定通过；本候选不得通过改名恢复该分支。评论文本教师保持关闭，除非用户另行授权全新预注册修复批次。
3. 当前CSMV无发布时间、原生topic、publisher，禁止承诺time/topic/publisher OOD；只能执行已冻结group/source-family/hashtag协议和明确可得的外部域验证。
4. LAI-GAI不支持历史评论记忆机制，只支持人工金标下的分布预测、有限样本测量校验、校准/OOD边界；Video2Reaction为银标且无原始评论保证，不得升级为第三HUMAN_GOLD主集。

## 数据可行性初判

| 数据集 | 获取/当前状态 | 统一路线角色 | 主要限制 |
|---|---|---|---|
| CSMV | 标签与canonical已本地冻结；I3D内部研究可用但资产风险仍接受式延期 | 主机制：T0、历史净效用、三源不确定性 | 每视频2—20评论；仅冻结I3D；无time/topic/publisher |
| LAI-GAI | 847图与63,682人工响应已冻结，CC BY 4.0链闭合 | HUMAN_GOLD外部校准与不确定性验证 | 图像域；无历史评论/视频记忆机制 |
| Video2Reaction | HF公开约8.95GB下载、约41.12GB展开；尚未冻结revision/hash | movie-disjoint银标外部历史记忆验证与closest prior | 原视频不直接再分发；标签为LLM银标；原评论/支持量不保证公开 |
| MVIndEmo | 论文称CC BY-SA 4.0，但所列GitHub当前404；项目未取得 | 仅可选银标压力测试 | 合法入口、revision、媒体可得性未闭合，当前不可执行 |

## 一般实验顺序

1. `P0 数据/构念门`：冻结数据身份、split、支持量和可用字段；不合并不同标签空间；formal test保持不可见。
2. `P1 现象门`：在训练折内交叉拟合content-only与固定历史专家，量化content similarity—reaction distance错位；控制评论数、source group和标签不确定性，并做人审子集。
3. `P2 Oracle门`：计算Oracle在开发证据上的最大可得收益。若Oracle相对content-only/固定融合无稳定headroom，停止路由主张。
4. `P3 OOF效用路由`：只用OOF `Delta`训练路由器；比较相似度阈值、entropy/OOD门、固定融合、generic gate/MoE、LEEP/LogME式可迁移性信号和随机路由。
5. `P4 三源不确定性`：用反应熵/分歧、响应支持量下的后验/重采样稳定性、ensemble/OOD误差分别验证三源；构造对经验反应分布的校准JS预测区域，报告coverage与区域大小，不冒充总体人口保证。
6. `P5 外部验证`：LAI-GAI只验证分布/不确定性；Video2Reaction完成intake后做movie-disjoint银标外验；各数据集分表，不横比不可比指标。
7. `P6 正式统计`：仅在预注册后由未来正式任务执行五种子、内容单元paired bootstrap 95%CI、matched-coverage risk、AURC、routing regret、negative-transfer rate、效率和失败案例。

## Kill criteria

- 控制响应支持量和group混杂后，内容—反应错位不稳定或主要由标签噪声解释；
- Oracle路由没有稳定headroom；
- 学习路由不优于相似度/entropy/generic gate或固定融合；
- 三类不确定性不能分别预测分歧、重采样不稳定和OOD误差；
- 预测区域达不到预设coverage，或收益只存在于人工hard-pair而不出现在自然grouped OOD。

## T-AFFC初判

当前为`PROMISING_CONDITIONAL_NOT_GO`。T-AFFC适配来自群体诱发情感、反应异质性、可靠性决策与可证伪失败机制；创新上限不是三个旧模块的并集，而是“历史净效用驱动的预测区域收缩/回退/拒答”及其群体反应专属验证。只有现象门、Oracle门、强generic baselines、自然OOD和三源外部验证均通过，才可能支撑完整T-AFFC方法稿；否则应降级为可靠性测量/负结果或协议论文。

## 阻塞/风险

- 定向检索不是冻结的系统查新，完全同构前作仍可能遗漏；当前新颖性只能保持条件性UNKNOWN/候选。
- CSMV仅有冻结I3D且缺发布时间、原生topic和publisher；Video2Reaction未冻结revision/hash且为银标；MVIndEmo入口404。
- 三源不确定性存在可识别性风险：群体分歧、有限抽样和模型误差不能只靠一个Dirichlet浓度参数自我解释，必须各有外部或重采样校验。
- Oracle headroom、自然内容—反应错位与学习路由优势尚无实验结果；任一核心门失败都应止损，不得追加模块掩盖。

## 下一步

1. 读取用户对`CARM_IDEA_20260805_UNIFIED_ROUTE`的选择并记录精确授权边界；当前分析不授权实验。
2. 验证授权后再冻结系统查新协议、数据fitness合同、question/estimand、primary endpoint、OOF规则和kill criteria。
3. 检查新合同通过前Task30保持关闭、Task40/50保持未创建，且实验核心与正式claim无变化。

## 必读文件

1. `.light/handoff/S38-three-idea-feasibility-review.md`
2. `.light/passport.yaml`
3. `.light/project_card.md`
4. `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.21第2—7、10、11、17节
5. `TASK_REGISTRY.md`
6. `DATA_SOURCE_LEDGER.md`
7. `DATA_CARD_DATASET_V1.md`
8. `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md`
9. `TASK00_TASK30_H1_FINAL_INDEPENDENT_REVIEW_20260804.md`
10. `WORK_LOG.md`末条与Task10/20/30实时状态

## 禁止

- 不得把本卡当作当前事实；下次必须先运行`git status --short --branch`、`git log -3`及`git rev-parse HEAD/origin/main`刷新现实，禁止凭记忆继续。
- 不得把本轮定向检索写成“前人从未做过”或世界首创证明；正式新颖性判断须有冻结的多源查新合同。
- 不得恢复Task30评论特权KD、materialize formal test、创建Task40/50或修改实验核心，除非用户另行授权且00预注册合同通过。
- 不得把LAI-GAI写成视频历史记忆证据，把Video2Reaction写成HUMAN_GOLD，或把CSMV缺失的time/topic/publisher字段伪造成可用协议。
- 不得改写G1—G3、I3D UNKNOWN、Task20 NON_T0/INELIGIBLE、论文`TO_VERIFY`或受限存储删除截止。

## 接续提示词

你是“00-T-AFFC总控03”，不是Task30执行代理。先读取AGENTS.md与WORK_RECORD_POLICY.md，刷新Git与Task10/20/30实时状态；再读S38、passport、project card、Registry、总纲v1.21和论文SSOT。S38只是三idea统一路线的只读初审，不是实验授权或世界首创新颖性证明。若用户选择推进，先建立版本化系统查新、数据identity/fitness、idea-critique和预注册合同；在此之前保持Task30=`CLOSED_NOT_PASSED`、H1未通过、Task40/50未创建，不修改G1—G3、I3D UNKNOWN、Task20 NON_T0/INELIGIBLE或论文`TO_VERIFY`边界。
