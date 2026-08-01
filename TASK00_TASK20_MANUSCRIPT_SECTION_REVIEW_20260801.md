# Task00 对 Task20 论文基线与评测段落的独立审查（2026-08-01）

## 1. 裁定

- 裁定：`ACCEPTED_WITH_LIMITATIONS`
- 审查对象：`main@5e1386d79ef00136c87491edbde6f77437d3715b`
- 论文SSOT：`paper/TAFFC_CARM_MANUSCRIPT_SSOT.md` v0.1.2
- 论文SSOT SHA-256：`37cd9dda4f0c3158b957d9ad99508c3d117be2b8896f4fbc723b5ee3a2758b95`
- Task20完成说明 SHA-256：`779dd19f42f05b007805f16032769d395092cfa9e4d86f7158a7d94a85a6eff0`

Task20在授权范围内完成了Sec.5.4、5.6、5.8、受限Sec.6.1、Sec.8及Supplement S3/S4/S9的基线、指标、实现复现和局限性文字。所写环境版本、12-trial调参上限、九项指标操作定义、train-only/dev/test边界和同环境同seed回放范围均可追溯到冻结文件或实现；未把单seed工程结果、VC-CSA NON_T0探索、不可用模型或N/A多模态实验冒充正式论文结果。

## 2. 独立核验

1. Git范围：提交仅修改论文SSOT、Task20完成说明和WORK_LOG三项授权文件；`git diff --check 9a1612f..5e1386d`通过。
2. 文件绑定：两项提交SHA-256与Task20回交值逐字一致。
3. 事实核对：`TASK20_ENVIRONMENT_LOCK.md`与Sec.5.8版本一致；`configs/task20/tuning-plan-v1.json`支持每族最多12 trials、dev JS选择和NLL/Brier/参数量tie-break；`scripts/task20_metrics.py`与Sec.5.6九项指标定义一致。
4. 自动门：`validate_manuscript_ssot.py`通过，报告`citation_slots=6`、`result_gates=20`；`validate_work_log.py`通过，237条、0错误；`run_preparation_checks.py` exit 0、`blocking_checks=[]`，同时诚实保留`formal_model_work_ready=false/faiss_available=false`。
5. 独立测试：`.venv-task20`运行`python -m unittest discover -s tests -v`，74/74通过；另行抽取Task20指标、合同和回放15项测试也通过。两个环境均未安装pytest，因此未把pytest入口写成成功。

## 3. 验收限制

1. 本裁定只接受Task20所有权段落，不接受尚待独立审核的Task10段落，也不构成整篇论文Stage-8/投稿验收。
2. 稿件状态必须保持`MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS`，`result_freeze=NOT_AVAILABLE`，C1—C4继续`TO_VERIFY`。
3. temporal-attention仅为单seed `REIMPLEMENTATION_STRONG_BASELINE`工程证据；正式五种子、paired bootstrap、置信区间和比较结论仍归Task50。
4. VC-CSA作者原设定探索永久NON_T0且不具正式证据资格；其性能值不得进入论文主表、模型选择、G3主证据或claim。
5. CLIP/SigLIP/VideoMAE保持`NOT_AVAILABLE_IN_FROZEN_T0_PROTOCOL`；late fusion、cross-attention和E1保持`NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`。
6. I3D许可、官方revision、权利方包身份/fixity仍为UNKNOWN并禁止再分发；受限存储仍须在2026-08-31 23:59:59 +08:00前后完成可见层删除验收。
7. 通用claim-evidence门因缺少`evidence_strength.json`且skill `_shared`不可达而降级，不能冒充完整claim绑定通过；正式基线引用仍有CITATION GAP。
8. 正文中的G3、T0、NON_T0等内部工程术语在Task60面向外部读者改写，但在结果冻结前保留有助于防止证据越界。

## 4. 对任务树的影响

- Task20论文段落填写状态关闭为`MANUSCRIPT_SECTIONS_ACCEPTED_WITH_LIMITATIONS`；Task20实验核心不重开。
- G1、G2、资产风险、G3和Task30创建资格均不改变。
- 下一优先事项是00独立审查Task10论文数据/协议段落；随后才能把当前论文骨架作为Task30写作接口继续演进。

