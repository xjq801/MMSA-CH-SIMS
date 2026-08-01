# Task00 对 Task30 的创建授权（2026-08-01）

## 1. 授权结论

- 决定：`AUTHORIZED_TO_CREATE_TASK30`
- 创建基线：`main@9b5a44dc5d6d186ed4e0d78905e40629f5262de6`
- 任务名称：`30-M4 评论教师与内容学生`
- 唯一科学目标：验证H1——训练期评论作为privileged supervision，能否改善推理时只读取T0内容的学生对未来受众公开表达反应分布的预测。
- 任务身份：开发门任务，不是正式五种子结果任务；teacher/student或KD本身不作为创新。

创建条件已满足：G3=`PASS_WITH_LIMITATIONS`，evaluation-kit-v1和content-only强基线已冻结，Task20正式核心已接受收尾且Task30运行态创建门已解除。Task10论文段落尚待00审核，但不改变已冻结的数据、split、T0输入与G1—G3，因此不阻塞Task30启动。

## 2. 必读权威输入

1. `AGENTS.md`、`WORK_RECORD_POLICY.md`、`WORK_LOG.md`末条；
2. `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.21第5节与第17节任务依赖；
3. `HANDOFF_20.md`及`data/manifests/task20-handoff-v1.manifest.json`；
4. `TASK00_G3_FINAL_REVIEW_20260718.md`、`TASK20_POST_SNAPSHOT_VCCSA_ERRATUM_20260718.md`、`TASK00_TASK20_FINAL_CLOSEOUT_REVIEW_20260801.md`；
5. `T0_INPUT_POLICY.md`、`experiment-protocol-v2.md`、`leakage-threat-model.md`；
6. `TASK20_ENVIRONMENT_LOCK.md`、`configs/task20/tuning-plan-v1.json`、Task20 evaluation/config/prediction schemas；
7. `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md` v0.1.2仅作claim边界参考，不得填入未冻结结果。

## 3. 执行合同

1. 开工先刷新`origin/main`和工作区现实，复核Task20 handoff的22项tracked evidence；交接卡不替代Git事实。
2. 新建独立`.venv-task30`或等价锁定环境；不得把主`.venv`当前`formal_model_work_ready=false/faiss=false`或Task20旧环境状态偷换为Task30已就绪。
3. 只允许train评论参与teacher、标签聚合、温度/损失选择或任何缓存；dev仅用于预注册选择，test评论和test标签不得进入训练、teacher、索引、早停或选择。
4. Task30只跑开发协议：正式test、五种子、paired bootstrap和论文主表归Task50。任何单seed数值只能标为development evidence。
5. 以最简单content-only student为公平基线，依次比较hard label、soft distribution、普通KD、comment-privileged KD、错配评论负对照和teacher-only上界；保持参数量、预算和选择规则可审计。
6. 先写泄漏/分布合法性/数值稳定性测试，再实现最小teacher/student；不得同时加入memory、retrieval、router、GNN、生成模块或完整CARM。
7. teacher/student接口不得硬编码CSMV标签数或字段名；LAI-GAI没有原生评论teacher字段时只做其支持的内容分布/校准边界，不伪造H1；Video2Reaction原生分支H1固定`NOT_APPLICABLE_DATA_NOT_RELEASED`。
8. 资产边界保持：I3D许可、官方revision、权利方包身份/fixity为UNKNOWN；仅在既有accepted-risk内部研究范围读取，禁止提交、发布或再分发I3D数组、评论正文、模型权重、预测隐私数据、凭据和本机路径。
9. 不得修改Task20冻结评测核心来迁就结果；确有接口缺陷时停止并向00提交最小变更请求和影响分析。
10. 闭源/付费LLM、远程GPU、对象存储、数据外传或新增付费资源均不在本授权内，必须另行取得用户与00的精确授权。

## 4. 必须产出与退出门

- `teacher-student-v1`代码、配置、环境锁和可重跑命令；
- teacher标签/置信度、评论数偏差、类别稀疏与异常样本审计；
- hard/soft/KD/privileged-KD/错配teacher/teacher-only开发结果与E3消融；
- test评论不可达的数据流图和可执行负测；
- 校准、数值稳定性、错误案例与数据集适用性边界；
- `HANDOFF_30.md`更新为最终交付状态及H1开发门报告。

只有CSMV开发设置相对最强content-only呈稳定趋势、无泄漏、校准无不可接受恶化且E3能隔离特权监督贡献时，才可向00请求创建Task40。Task30不得自批H1门或创建Task40。

## 5. 永久传播边界

- G1=`PASS`；G2协议/数据=`PASS_WITH_LIMITATIONS`；资产=`DEFERRED_ACCEPTED_RISK`；G3=`PASS_WITH_LIMITATIONS`。
- VC-CSA 120-epoch探索永久NON_T0且不具正式证据资格。
- 论文仍为`MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS`，C1—C4=`TO_VERIFY`。
- IJCV方向独立，禁止创建或执行J0—J2、JH1—JH3、任务25或65。

