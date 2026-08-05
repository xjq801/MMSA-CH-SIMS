---
project_name: MMSA-CH-SIMS T-AFFC 总控
created: 2026-07-17
---
# 项目卡：MMSA-CH-SIMS T-AFFC 总控

```yaml
project_name: MMSA-CH-SIMS T-AFFC 总控
goal: 2027-05-12前形成可直接提交IEEE T-AFFC的CARM群体情绪预测论文、代码、数据说明与证据链
current_stage: M5开发启动交接 总纲v1.23与Task40开发预注册已冻结；Task30 CLOSED_NOT_PASSED；Task40与总控04已创建并等待FINAL_ANCHOR
confirmed_idea: 无目标评论与分布偏移下的可靠内容到评论者公开表达反应分布预测；C1严格T0协议/证据 + C2训练折内OOF点/后验历史反应净收益与USE_MEMORY/FALLBACK_CONTENT/ABSTAIN路由 + C3群体分歧/有限响应/模型迁移三源不确定性、校准与经验分布预测区域；Video2Reaction为closest/direct prior
data_status: G1 PASS；CSMV 8210视频与LAI-GAI 847图两个HUMAN_GOLD主集冻结；G2协议/数据通过；I3D资产外部证明为DEFERRED_ACCEPTED_RISK
method_status: 任务20保持G3 PASS_WITH_LIMITATIONS；Task30以CLOSED_NOT_PASSED退出活动claim集；`SC-20260805-01/02`与v1.23已冻结点/后验净收益、response thinning、三源不确定性与formal-test禁令；`AUTH-00-TASK40-CNBR-DEVELOPMENT-20260805`已授权创建Task40。Oracle为Task40内首个开发止损门，不是创建前置
experiment_status: Task40 `019fd19c-abf3-7bf0-8530-759e38c3a6ab`已在独立worktree创建，当前只读等待FINAL_ANCHOR，尚未运行新模型实验；formal test未materialize、Task50未创建。Task20 Attempt2仍`SUPPLEMENT_REQUIRED_NO_ACCEPTANCE_YET`且NON_T0/INELIGIBLE；Task30仍`CLOSED_NOT_PASSED`；Video2Reaction HF revision已定位但许可差异/本地fixity/movie split未闭合，未下载
paper_status: `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md`=v0.1.3、`paper/CLAIM_ARGUMENT_BLUEPRINT.md`=v0.1.1、`CLAIM_EVIDENCE_MATRIX.md`=v1.4；保持MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS。Task10数据/协议段落已受限验收；Task30 teacher已移出活动方法和claim；C1—C3均TO_VERIFY
ppt_status: 不在当前关键路径
code_status: GitHub xjq801/MMSA-CH-SIMS；v1.17历史提交为main@47e9338，当前回退批次提交状态以Git刷新为准
risk_list: I3D许可/revision/权利方fixity未知且禁止再分发；Task20 attempt2不得被误拼为原1—120连续轨迹且逐step时间戳不得补造；Task20受限存储须在2026-08-31 23:59:59 +08:00前完成可见层删除验收且平台控制面仍UNKNOWN；Task30评论特权机制未建立且不得回写正式claim；OOF收益标签若拟合内生成会泄漏，Oracle无headroom或router不胜强通用门时必须降级；三源不确定性若不可辨识不得宣称分解，预测区域须同时报告coverage与width；Video2Reaction为派生特征+银标而非完整原始模态或HUMAN_GOLD；评论分布不得外推所有观众
next_actions: 1) 总控03提交推送S41并向Task40/总控04发送FINAL_ANCHOR后停止SSOT写入；2) Task40先核9个hash并做泄漏/错位/Oracle门，无headroom即关闭；3) 总控04独立审核Task40且不触碰实验核心，并继续Task20最小补证与2026-08-31受限存储删除验收
decision_log: 见 decision_log.md
version_history: 见 version_history.md
```
