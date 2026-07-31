---
session_no: S26
contract_version: 2
suggested_title: "[T-AFFC] S27 maintain evidence-gated manuscript and close Task20"
parent_session: S25
project: mmsa-ch-sims-taffc-master-control
date: 2026-07-31
---

# S26 Living manuscript SSOT v0.1.0 handoff

## 当前阶段

- 当前研究SSOT仍为`TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.21；本批没有修改总纲、G门、实验协议或Task20。
- G1=`PASS`、`G2_PROTOCOL_DATA=PASS_WITH_LIMITATIONS`、`ASSET_ADMISSIBILITY=DEFERRED_ACCEPTED_RISK`、G3=`PASS_WITH_LIMITATIONS`；Task30仍未创建。
- 英文论文已进入`MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS`：允许维护稳定定义、论证、方法与实验合同，不允许把单seed、开发趋势、NON_T0或泄漏接受探索结果写成论文证据。

## 已完成

- `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md` v0.1.0 — `validate_manuscript_ssot.py`复跑`passed=true`；英文正文含18个显式结果门，覆盖标题边界、摘要合同、引言、相关工作、问题定义、方法公式、实验与统计、结果槽位、讨论、局限、数据/代码/伦理/AI披露及补充材料计划。
- `paper/CLAIM_ARGUMENT_BLUEPRINT.md` — `validate_manuscript_ssot.py`验证6类citation slot均有registry记录并PASS；三项总纲贡献上限与内部C1—C4 claim、P1—P5论证链、反证条件、图表、审稿攻击和负结果降级路径已绑定。
- `scripts/validate_manuscript_ssot.py` — 首次红灯2项后修复；最终`passed=true manuscript_bytes=34313 blueprint_bytes=13806 citation_slots=6 result_gates=18`。
- `paper/README.md` — 人工确认总纲/claim矩阵→Markdown论文→Word/LaTeX/PDF为单向权威关系，且明确当前无正式结果。
- `.light/decision_log.md`、`.light/version_history.md`、`.light/project_card.md`、`.light/passport.yaml` — passport revision=8，state hash重算为`sha256:8f28b24b71a8c243f6661b8835c5c300faf3d8c1df39b8e4878f2d4578a5b972`；底层passport validate为历史WARN而非hash错误。

## 工作区状态

- 本批开工与收尾前刷新时共享主仓库基线为`main=origin/main=278bfbed1f296fad84097f7d82ae06b2b39383ad`；最终提交以本卡所在Git commit为准。
- 用户已有未跟踪`NEmoP/`、`__MACOSX/`与`tmp/`未读取、未修改、未暂存。
- 按用户要求，本批没有向Task20发送消息；只读取了Git中已提交的最新WORK_LOG现实。
- `light-memory-pm pm.py`既知`_shared/passport`布局失败未重试；使用底层passport脚本重算和校验state hash。

## 待用户回答

- none — 当前没有待用户决策的问题，因为本批只建立不含正式结果的论文骨架，并未改变研究范围、G门或实验授权。

## 核心决策

1. 总纲继续是研究事实SSOT；论文Markdown只管理论文结构与措辞，不能反向改变数据、协议、门或claim状态。
2. Word、LaTeX、PDF和补充材料只能从论文Markdown单向生成，禁止派生文档独立改稿。
3. 论文贡献保持总纲三项上限：C1协议/证据；C2评论特权监督+收益感知记忆；C3分布偏移/选择性可靠性。内部claim矩阵仍用C1—C4细分证据。
4. Video2Reaction必须称closest/direct prior；V2R-A/V2R-B分轨、HUMAN_GOLD/银标边界和跨数据不可横比合同不变。
5. 正文现有`RESULT-GAP`、`CITATION-GAP`和`DECISION-GAP`是准入门，不是待随意润色的占位符；只能由冻结证据、核验引用和记录决策替换。

## 验证与覆盖边界

- `.\.venv\Scripts\python.exe scripts\validate_manuscript_ssot.py`：PASS；18个结果门，6类citation slot已登记。
- `git diff --check`：PASS。
- `light-consistency`对总纲、claim矩阵、正文和蓝图回扫：0项术语变体冲突、0项指标冲突、0项claim/contribution强度漂移；因项目尚无`.light/consistency`四份完整YAML registry，只能报告`PARTIAL`，并有9条中英文材料覆盖差异INFO，不冒充全门通过。
- 正式项目门禁和handoff合同必须在提交前复跑并以WORK_LOG记录为准。

## 阻塞/风险

- C1—C4全部仍为`TO_VERIFY`，G4—G6没有正式证据；摘要、结果、讨论和结论不能完成为投稿口吻。
- Task20 NON_T0探索和受限存储生命周期仍未闭环；其数值永久`INELIGIBLE`，不能进入论文。
- Video2Reaction revision/fixity、V2R-A公平适配与V2R-B原生外验尚未执行。
- I3D许可、官方revision及权利方包身份/fixity仍为UNKNOWN；内部风险接受不等于公开再分发或权利闭合。
- CARM名称查重未闭合，当前只作内部工作名。

## 必读文件

- `.light/handoff/S26-living-manuscript-ssot-v010.md`
- `.light/passport.yaml`
- `.light/project_card.md`
- `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.21，尤其0.8—0.11、3、6、7、11和第17节任务30—60
- `paper/README.md`
- `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md`
- `paper/CLAIM_ARGUMENT_BLUEPRINT.md`
- `CLAIM_EVIDENCE_MATRIX.md`
- `TAFFC_CLAIM_BLACKLIST_20260724.md`
- 最新`WORK_LOG.md`

## 下一步

1. 先刷新origin/main、Git状态和最新WORK_LOG，不把本卡写入的Task20快照当实时事实。
2. Task30/40推进时，只把已冻结的方法、符号、预注册和逐句引用审计结果写入论文；不要提前生成结果叙事。
3. results-freeze-v1形成后，按结果准入合同更新C1—C4并程序化生成图表，再完成摘要、结果、讨论和结论及IEEE模板转换。

## 禁止

- Do not treat this card as current fact; run git status/log first。本卡不是当前事实，必须先刷新Git和最新WORK_LOG。
- 不得把论文骨架完成写成论文已完成、可投稿或已达到T-AFFC标准。
- 不得把Video2Reaction淡化为间接前作，不得恢复任务首创或分布输出即创新。
- 不得把评论标签外推为所有观看者的内在情绪。
- 不得把Task20探索数值、单seed、smoke或泄漏接受结果写入论文主表或claim。
- 不得触碰或提交`NEmoP/`、`__MACOSX/`或`tmp/`。

## Continuation prompt

You are the 00-T-AFFC total controller taking over S26. Read AGENTS.md and perform startup checks, then read S26, passport, project_card, the master plan v1.21 sections 0.8-0.11, 3, 6, 7, 11 and task specs 30-60, paper/README.md, paper/TAFFC_CARM_MANUSCRIPT_SSOT.md, paper/CLAIM_ARGUMENT_BLUEPRINT.md, CLAIM_EVIDENCE_MATRIX.md, the claim blacklist and the latest WORK_LOG. Refresh origin/main and Git reality; this handoff is not current fact. Keep G1 PASS, G2 protocol/data PASS_WITH_LIMITATIONS, asset admissibility DEFERRED_ACCEPTED_RISK and G3 PASS_WITH_LIMITATIONS. Treat the manuscript as MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS: only ingest frozen methods, preregistrations, verified citations and accepted evidence. Never insert Task20 single-seed, NON_T0, leakage-accepted or smoke values. Preserve the three contribution families, internal C1-C4 claim states, Video2Reaction closest/direct-prior dual-track contract, construct boundary and I3D risk. Do not create Task30 until its total-control gate is satisfied. At session close create S27 and print the next continuation prompt.
