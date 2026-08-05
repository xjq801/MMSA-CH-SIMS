---
project_name: MMSA-CH-SIMS T-AFFC 总控
created: 2026-07-17
---
# 项目卡：MMSA-CH-SIMS T-AFFC 总控

```yaml
project_name: MMSA-CH-SIMS T-AFFC 总控
goal: 2027-05-12前形成可直接提交IEEE T-AFFC的CARM群体情绪预测论文、代码、数据说明与证据链
current_stage: M4R 总纲v1.22统一路线方案已冻结；Task30 CLOSED_NOT_PASSED；Task40未创建
confirmed_idea: 无目标评论与分布偏移下的可靠内容到评论者公开表达反应分布预测；C1严格T0协议/证据 + C2训练折内OOF历史反应净收益标签与USE_MEMORY/FALLBACK_CONTENT/ABSTAIN路由 + C3 aleatoric/epistemic/transfer-retrieval三源不确定性、校准与分布预测区域；Video2Reaction为closest/direct prior
data_status: G1 PASS；CSMV 8210视频与LAI-GAI 847图两个HUMAN_GOLD主集冻结；G2协议/数据通过；I3D资产外部证明为DEFERRED_ACCEPTED_RISK
method_status: 任务20统一评测与强基线已获G3 PASS_WITH_LIMITATIONS；Task30评论特权teacher/student开发门因机制跨种子不稳定以CLOSED_NOT_PASSED关闭，不能支持正式claim且不在v1.22恢复；`SC-20260805-01`已冻结无teacher的历史反应净收益路由与三源不确定性方案，状态为PLAN_FROZEN_EXECUTION_NOT_YET_AUTHORIZED；Task40仍须先过数据准入、Oracle headroom、OOF泄漏审计、强通用门和test不可见等创建门
experiment_status: 任务20正式核心与论文段落已受限验收；独立NON_T0/INELIGIBLE Attempt2已在`main@da9c52a`提交，但00裁定`SUPPLEMENT_REQUIRED_NO_ACCEPTANCE_YET`且不授权复跑；Task30冻结ref `9086bd537b36cad5635eaa9db81aaeb6756b4088`已由00只按冻结ref导入main并独立裁定`CLOSED_NOT_PASSED`，证据永久为DEVELOPMENT_EVIDENCE_ONLY，formal test未materialize，不授权修复；v1.22只新增方案与实验矩阵，未运行新实验、未创建Task40/50，Video2Reaction尚未冻结revision或下载
paper_status: `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md`现为v0.1.2且保持MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS；其方法蓝图尚未吸收v1.22路线，须在数据/预注册门通过后另行受控升版，不得把计划写成已验证贡献；Task20在`main@5e1386d`提交的受限段落已获00受限验收；Task10在`main@1d2018c`引入的数据/协议段落仍待00独立验收；C1—C4均TO_VERIFY
ppt_status: 不在当前关键路径
code_status: GitHub xjq801/MMSA-CH-SIMS；v1.17历史提交为main@47e9338，当前回退批次提交状态以Git刷新为准
risk_list: I3D许可/revision/权利方fixity未知且禁止再分发；Task20 attempt2不得被误拼为原1—120连续轨迹且逐step时间戳不得补造；Task20受限存储须在2026-08-31 23:59:59 +08:00前完成可见层删除验收且平台控制面仍UNKNOWN；Task30评论特权机制未建立且不得回写正式claim；OOF收益标签若拟合内生成会泄漏，Oracle无headroom或router不胜强通用门时必须降级；三源不确定性若不可辨识不得宣称分解，预测区域须同时报告coverage与width；Video2Reaction为派生特征+银标而非完整原始模态或HUMAN_GOLD；评论分布不得外推所有观众
next_actions: 1) 为v1.22完成数据identity/许可/构念/split准入，特别是Video2Reaction；2) 冻结target chain、failure tree、估计量、五种子和正式test materialization合同；3) 仅在train/dev验证内容基线与Oracle headroom，满足创建门后再书面决定是否创建Task40；4) 继续审核Task10论文段落、Task20最小补证并在2026-08-31截止前后验收受限存储删除
decision_log: 见 decision_log.md
version_history: 见 version_history.md
```
