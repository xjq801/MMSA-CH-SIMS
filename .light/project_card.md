---
project_name: MMSA-CH-SIMS T-AFFC 总控
created: 2026-07-17
---
# 项目卡：MMSA-CH-SIMS T-AFFC 总控

```yaml
project_name: MMSA-CH-SIMS T-AFFC 总控
goal: 2027-05-12前形成可直接提交IEEE T-AFFC的CARM群体情绪预测论文、代码、数据说明与证据链
current_stage: M4 Task30 CLOSED_NOT_PASSED；Task40未创建
confirmed_idea: 无目标响应与分布偏移下的可靠内容到受众公开表达反应分布预测；C1严格T0协议/证据 + C2评论特权教师与train-only记忆/router/rejection + C3严格OOD/校准/选择性证据；Video2Reaction为closest/direct prior
data_status: G1 PASS；CSMV 8210视频与LAI-GAI 847图两个HUMAN_GOLD主集冻结；G2协议/数据通过；I3D资产外部证明为DEFERRED_ACCEPTED_RISK
method_status: 任务20统一评测与强基线已获G3 PASS_WITH_LIMITATIONS；Task30评论特权teacher/student开发门因机制跨种子不稳定以CLOSED_NOT_PASSED关闭，不能支持C2正式claim；Video2Reaction仍为closest/direct prior且标签固定SILVER_LLM_HUMAN_VERIFIED；收益感知router与完整CARM均未获下游创建资格
experiment_status: 任务20正式核心与论文段落已受限验收；独立NON_T0/INELIGIBLE Attempt2已在`main@da9c52a`提交，但00裁定`SUPPLEMENT_REQUIRED_NO_ACCEPTANCE_YET`且不授权复跑；Task30冻结ref `9086bd537b36cad5635eaa9db81aaeb6756b4088`已由00只按冻结ref导入main并独立裁定`CLOSED_NOT_PASSED`，证据永久为DEVELOPMENT_EVIDENCE_ONLY，formal test未materialize，不授权修复；Task40/50未创建，Video2Reaction尚未冻结revision或下载
paper_status: `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md`现为v0.1.2且保持MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS；Task20在`main@5e1386d`提交的基线、指标、复现、受限Sec.6.1及相关局限/supplement已获00受限验收；Task10在`main@1d2018c`引入的数据/协议段落仍待00独立验收；C1—C4均TO_VERIFY
ppt_status: 不在当前关键路径
code_status: GitHub xjq801/MMSA-CH-SIMS；v1.17历史提交为main@47e9338，当前回退批次提交状态以Git刷新为准
risk_list: I3D许可/revision/权利方fixity未知且禁止再分发；Task20 attempt2不得被误拼为原1—120连续轨迹，逐step时间戳未记录且不得事后补造；Task20受限存储须在2026-08-31 23:59:59 +08:00前完成可见层删除验收且平台控制面仍UNKNOWN；Task30 H1仅相对soft baseline为3/3改善、相对ordinary KD与错配teacher均为2/3，评论特权机制未建立且不得进入论文正式claim；Video2Reaction公开包是派生特征+LLM人工核验银标而非完整原始模态或HUMAN_GOLD；评论分布不得外推所有观众；H3/E5当前无合格多T0模态协议
next_actions: 1) 独立审核Task10论文数据/协议段落；2) 审核Task20最小追加式补证且不授权复跑；3) 在2026-08-31截止前后验收Task20受限存储可见层删除；Task40保持未创建，任何方法重路由须用户另行决定
decision_log: 见 decision_log.md
version_history: 见 version_history.md
```
