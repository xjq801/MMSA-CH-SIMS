# S43 — Task45诊断任务创建、授权边界与总控04接续

## 1. 接续身份与Git锚点

- 当前总控：00-T-AFFC总控04，task/thread `019fd19d-b8ef-71f2-82b3-433168211358`。
- 项目只执行IEEE T-AFFC CARM路线；不得创建或执行IJCV J0—J2、JH1—JH3、任务25或65。
- Task45：`019fd586-628b-74f0-85ae-b44fa60968ff`。
- Task45独立worktree：`C:/Users/86183/.codex/worktrees/5096/MMSA-CH-SIMS`。
- Task45创建HEAD：`origin/main@560a3dc86116cf5b60471fe55b105b6778a44354`；其计划锚点为`origin/main@8a5ab2c2c543051e00427154db205bb3937de2bf`。
- 创建授权：`TASK00_TASK45_CREATION_AND_DIAGNOSTIC_EXECUTION_AUTHORIZATION_20260806.md`，SHA-256=`9733559fd2a6f162576e43119698108be3ea521dbd4507f2e01113cd66a5d098`。
- 本S43随creation closure提交；Task45收到`TASK45_DIAGNOSTIC_FINAL_ANCHOR`前保持只读。

## 2. 当前门与任务状态

- G1=`PASS`。
- G2协议/数据=`PASS_WITH_LIMITATIONS`；I3D资产=`DEFERRED_ACCEPTED_RISK`；总G2=`PASS_WITH_ACCEPTED_ASSET_RISK`；`formal_split=true`。
- G3=`PASS_WITH_LIMITATIONS`。
- Task10=`CLOSED_MANUSCRIPT_DATA_SECTIONS_ACCEPTED_WITH_LIMITATIONS`。
- Task20=`FORMAL_CORE_CLOSED_RECOVERY_ATTEMPT2_SUPPLEMENT_REQUIRED`；Attempt2永久`NON_T0/INELIGIBLE`且尚未验收；受限存储可见层删除截止`2026-08-31 23:59:59 +08:00`不变。
- Task30永久`CLOSED_NOT_PASSED`，不恢复teacher/KD。
- Task40永久`CLOSED_NOT_PASSED_ROUTER_MAIN_JSD`，不授权修复。
- Task45=`CREATED_READONLY_PENDING_FINAL_ANCHOR`。
- Task46=`NOT_CREATED_REQUIRES_TASK45_PASS_AND_NEW_PREREGISTRATION`；Task50=`NOT_CREATED_FIXED_ORDER_BLOCKED`。
- formal test未materialize且访问事件必须为0；论文继续`MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS`，C1—C3=`TO_VERIFY`。

## 3. 可发表性与Task45唯一科学目的

- 可发表性裁定为`CONDITIONAL_GO_DIAGNOSTIC_ONLY_METHOD_NOVELTY_BLOCKED`：一般两阶段utility routing已有强近邻，不能作为方法首创。
- Task45只回答严格T0诊断能否同时预测历史memory相对content的获益概率与正获益幅度；不是Task40修复，不训练或评估路由动作。
- 数据只来自原CSMV train：5541 source groups/5698 videos。固定salt=`CARM-v124-task45-train-role-v1`，角色为FIT 3304/3404、DIAG_CONFIRM 1126/1154、ROUTER_CONFIRM 1111/1140；最后一角色对Task45完全不可访问。
- 目标固定为`Delta=JSD(theta,f0)-JSD(theta,fH)`、`b=P(Delta>0)`、`m=E[max(Delta,0)]`和secondary `l=Q05(Delta)`；`theta|c~Dirichlet(c+0.5)`，200 draws，仅允许`c+1`敏感性。
- 两条AND primary是full T0 diagnostics相对同容量G0 content-only的Brier差与MAE差；各自要求source-group cluster bootstrap 10000次的95%CI上界小于0且至少4/5 seed方向为负。shuffled target不得优于constant。
- Q05、响应支持量、五seed零`USE_MEMORY`退化与逐组消融只作secondary，不得挽救primary。

## 4. 执行顺序、访问边界与停止规则

1. P0只重算source manifest hash、三角色计数/零重叠、FIT fold与旧DEV/router-confirm/formal-test零事件；任一失败立即停止。
2. P1只在`TRAIN_DIAG_FIT`执行5-fold expert OOF与4-fold诊断CV；固定五seed、200 posterior draws与4-trial HGB网格。
3. P2在所有选择冻结后一次性打开`TRAIN_DIAG_CONFIRM`；PASS/FAIL/INCONCLUSIVE均停止并回交总控04。
4. 禁止访问旧`DEV_SELECT`、旧`DEV_CALIBRATE`、`TRAIN_ROUTER_CONFIRM`或formal test；禁止导入Task40 ignored cache。
5. 禁止训练`USE_MEMORY/FALLBACK_CONTENT/ABSTAIN`路由、matched-coverage主JSD、负迁移或P5；禁止新增seed、换metric、放宽门、事后调阈值或创建Task46/50。
6. Task45须回交annotated tag、`HANDOFF_45.md`、machine/human reports、paired evidence、hash、测试、失败运行与零访问账；不得push或merge main。

## 5. 冻结工件与已知基础设施例外

- 可发表性审计=`253efbf3d31e4dfa918d2af4af082a3ac3d7c179c02dc2696282ecebcbd02056`。
- 研究方案=`43146a2952128df25001f3e7476c44dc54db3e9f3d2ac68c1839dbc7a9065ddf`；预注册=`e9778586b98ec31dfcaef5fb360393074b1148151a2976a72b71d04c83f81263`。
- 实验矩阵=`6da934ca6acdd3cf02412a175009fcb4e1694cbd6bc54f3b490db2516e231c3b`。
- data identity=`f14bc4d4458c228185a6de2b24d03962e40bc8418f52dc67e8de5a3bbacffe1e`；access boundary=`9385bf45888b2dc760e66f19c0c88a03ef9a07119de371bddd772b3fdd4db85a`。
- target chain=`2f71817ba9c44ea48119c70517cdf9000240ccf30f49534a0061bb63cff7d324`；failure tree=`f23f699319b99384836ede953d45cc9b257a414db3127e6148da8f8ac8bab64f`。
- plan manifest=`52bdc02ce6f7171c0b493218a414c7ccc753b5e601ab2351075519d23cb70439`；复现清单=`f237762ccc0abfd1db2c9b817ca6897a82fc192d6ce77d945f03452400251bb1`。
- 源Task40 P0 train manifest=`b556c3824d56e8edafee656541eba2b6e57d814da325931cae17c9a01e3389a9`。
- Light package final gate仅因技能包缺`_shared`而保留`PLAN_FINDINGS_SCHEMA_GAP`与`PLAN_FINDINGS_GATE_GAP`；这是显式记录的基础设施例外，不是科学门豁免，不得伪造findings文件。

## 6. 最近行动、最高风险与下一项总控动作

最近三项行动：

1. 发布并推送总纲v1.24、可发表性/数据/target/failure/公平基线与预注册包，计划锚点为`8a5ab2c...`。
2. 签发hash-bound Task45创建及P0→P2诊断授权并推送`560a3dc...`。
3. 创建Task45独立任务与worktree，记录正式task/thread ID和创建HEAD。

三个最高风险：

1. 一般utility routing新颖性碰撞，Task45即使PASS也只能支撑窄领域诊断，不能直接声称方法首创。
2. 旧DEV、router-confirm或formal test一旦被Task45读取会造成不可修复的确认污染。
3. 有限响应支持使`Delta`后验目标含测量噪声；响应支持量只能作可靠性分层，不能作为查询输入或事后挽救主门。

下一项总控动作：推送本creation closure并向Task45发送精确`TASK45_DIAGNOSTIC_FINAL_ANCHOR`；随后只审计P0证据与零访问账，不代跑Task45实验核心。

## 7. 接续提示词

```text
你是00-T-AFFC总控04的接续会话，不是Task45执行代理。项目根目录D:\MMSA-CH-SIMS，只执行IEEE T-AFFC CARM路线；禁止J0—J2、JH1—JH3、任务25/65。先fetch并确认origin/main包含S43及Task45 creation closure，再完整读取AGENTS.md、WORK_RECORD_POLICY.md、WORK_LOG末条、.light/passport.yaml revision 22、.light/project_card.md、TASK_REGISTRY.md v1.18、总纲v1.24、DECISION_LOG末条、RISK_REGISTER、CLAIM_EVIDENCE_MATRIX.md v1.6、Task45创建授权和本S43。Task45为019fd586-628b-74f0-85ae-b44fa60968ff，只允许P0→P1→P2 train-only诊断；总控只监督commit/ref、hash、测试、访问账与claim边界，不代跑实验。Task40保持CLOSED_NOT_PASSED_ROUTER_MAIN_JSD，Task46/50未创建，formal test零事件。Task45 PASS/FAIL/INCONCLUSIVE均须先停止并回交，任何两阶段路由都需要总控新预注册和用户新授权。继续监督Task20 2026-08-31受限存储删除截止与I3D UNKNOWN边界。
```
