# Task40可信净收益反应记忆创建授权

> 版本：v1.0  
> 日期：2026-08-05（Asia/Shanghai）  
> 授权ID：`AUTH-00-TASK40-CNBR-DEVELOPMENT-20260805`  
> 裁定：`AUTHORIZED_TO_CREATE_TASK40_DEVELOPMENT_ONLY`  
> 当前事实：`TASK40_NOT_YET_CREATED_USER_TASK_ACTION_REQUIRED`  
> 授权人：00-T-AFFC总控03  

## 1. 授权结论

根据用户“做这些”的明确指令，00已闭合系统查新、CSMV/LAI-GAI有限反应数据适配、Video2Reaction条件准入、target chain、failure tree、OOF泄漏合同、公平基线、五种子、主终点、多重比较与formal-test禁令。现授权用户创建Task40开发任务。

这不表示Task40已创建、Oracle已通过、router已验证、formal test已materialize或C1—C3已获支持。本总控任务不直接执行Task40实验核心。

## 2. 绑定的预注册包

| 文件 | SHA-256 |
|---|---|
| `TASK00_CARM_UNIFIED_ROUTE_RESEARCH_PLAN_20260805.md` | `a168780328673da1e8a687272dae8463795bd3e7e38afdf3830c5130beb73b79` |
| `TASK00_CARM_CREDIBLE_NET_BENEFIT_PREREGISTRATION_20260805.md` | `d6f02a2ae993d3cea80f642fbc31ef12ea6c783e7aca45a77e81824f15582a89` |
| `TASK10_CARM_RESPONSE_SUPPORT_DATA_FITNESS_ADDENDUM_20260805.md` | `3b27aab4115a4e9b20d54021e10879e4a8454c34650cb59e196a8062c0cce816` |
| `TASK00_CARM_ROUTE_CLOSEST_PRIOR_SEARCH_20260805.md` | `f06af9e9470fbf74c1ec4f9337ecc9dfb61e0b8471a467930d2e13e72e1ed04e` |
| `experiments/CARM_UNIFIED_ROUTE_EXPERIMENT_MATRIX_20260805.md` | `5a68b043d00bbae22fb7aeb10fc43da9fe7d7d8755153232b64d6189fd86af93` |
| `.light/carm-v123-target-chain.json` | `780d57a68fcdcf2a98eff393e0e5ef83a4e0f8acec488278079dfc7f733bc20f` |
| `.light/carm-v123-failure-tree.json` | `93e7f7a913235b54d5f8f81c162c279158aec0a497f2c5b02616ab8f96c462f2` |
| `.light/carm-v123-data-identity-fitness.json` | `5431f6749ce09bedbfe69d38c6406220a817a658478525ffb5a49b46f1fc0682` |
| `.light/carm-v123-plan-package.manifest.json` | `2fa7750a14d44f6726e6bc23b24dc1e6dde82b054dd4456548fa1e4d59376bee` |

任一绑定文件发生实质修改时，Task40必须先停止并由00发布版本化amendment；不得静默调参或修改成功条件。

## 3. 数据授权与新数据裁定

- 核心Task40只需现有CSMV冻结聚合标签、冻结I3D内部输入与既有split；不需要新数据集。
- LAI-GAI只授权与历史记忆非同构的边际response-thinning、校准和预测区域开发；H2a/H2b为`NOT_APPLICABLE_BY_DESIGN`。
- Video2Reaction不是Task40阻断数据。许可表述差异、本地fixity和movie-disjoint未闭合前，禁止下载或运行原生B轨。
- 不读取或纳入未审计的`NEmoP/`、`__MACOSX/`或`tmp/`。

## 4. Task40串行开发门

1. 只读验证本授权与绑定hash，建立独立worktree/branch，不与00同时修改控制文件。
2. P0：通过source-group OOF、train-only index、target-response不可达和test loader fail-closed测试。
3. P1：仅在train OOF完成连续内容—反应错位分析；hard pairs只作解释。
4. P2：在train OOF/DEV_SELECT公平比较content-only、memory-only和fixed fusion，计算Oracle headroom。Oracle无稳定headroom时立即以`CLOSED_NOT_PASSED_NO_ORACLE_HEADROOM`关闭，不训练router。
5. P3/P4：只在P2通过后，以完全相同的架构、输入、候选池、预算和种子比较point router与credible router。
6. P5：只在router强门通过后验证三源与80/90/95%经验分布预测区域。

## 5. 冻结统计合同

- 五个开发种子：`1364847620, 426925854, 1839464886, 1138176833, 484191872`。
- 5-fold group OOF；`DEV_SELECT`与`DEV_CALIBRATE`分离。
- CSMV response thinning：`2/4/8/all`、每项每k 200次；跨k主比较仅`n>=8`。
- 主方法终点：90%回答coverage下，credible router相对最强合格point/generic router的视频级配对JSD差，95%CI上界须小于0。
- 固定顺序可靠性终点：主JSD通过后才检验可信负迁移率差；后续三源家族用Holm校正。
- 单个可训练方法不超过12 trials；资源用尽时报告失败/不确定，不增加模块或看test。

## 6. 绝对禁令

- Task40不得读取、生成或materialize CSMV formal-test预测/标签/结果；formal test只属Task50。
- 不得恢复Task30 teacher/KD、修复Task30、继承Task30开发数值或创建Task50。
- 不得改变G1—G3、I3D UNKNOWN/accepted-risk、Task20 NON_T0/INELIGIBLE或受限存储删除截止。
- 不得宣称世界首创、已验证可信路由、所有观众情绪或因果社会效应。

## 7. 必须回交

Task40必须回交数据流图、OOF/index/test泄漏测试、错位报告、Oracle报告、point/credible router公平对比、response-thinning报告、三源/区域报告、完整失败证据、run/config/code/env/input hashes、`HANDOFF_40.md`和精确commit/ref。只有00独立审核可以决定Task40关闭状态或是否允许创建Task50。
