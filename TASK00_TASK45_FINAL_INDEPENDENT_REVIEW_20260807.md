# Task45最终独立关闭审查（总控04）

## 裁定

- 任务：`019fd586-628b-74f0-85ae-b44fa60968ff`
- annotated tag：`task45-t0-benefit-learnability-development-20260806`
- tag peeled commit：`5a842de375873ee5c5794f06b2a5c555f3a91194`
- 状态：`CLOSED_NOT_PASSED_T0_BENEFIT_LEARNABILITY`
- 论文边界：`EXPLORATORY_SUGGESTIVE_SIGNAL`；不支持 C2/C3、router、formal test 或 Task46 已通过。

本审查接受代理回交的 P0/P1/P2 证据作为可审计开发包，但按预注册的 AND 门关闭 Task45。Task40 保持 `CLOSED_NOT_PASSED_ROUTER_MAIN_JSD`；Task50 不创建；formal test 访问、materialization、label、feature、prediction 和 ID 事件均为 0。

## 独立复核的事实

1. P2 machine report 的主指标表面改善：PROB Brier 差 `-0.003122656`，95% CI `[-0.005103636,-0.001159598]`，5/5 seed 为负；MAG MAE 差 `-0.0000674363`，95% CI `[-0.000110523,-0.0000239202]`，5/5 seed 为负。
2. 两个预注册 shuffled-target 阴性对照同样异常优于 constant：PROB 差 `-0.003992584`，CI `[-0.005872947,-0.002109540]`；MAG 差 `-0.003506802`，CI `[-0.003903022,-0.003108101]`。因此不能把主指标改善解释为合法 T0 可学习性。
3. 角色身份为 FIT 3404 视频/3304 source groups、DIAG_CONFIRM 1154/1126、ROUTER_CONFIRM 1140/1111；跨角色 source-group overlap=0。DIAG_CONFIRM 只打开一次，`open_count=1`；旧 DEV、ROUTER_CONFIRM 和 formal test 均未访问。
4. 访问账中 `formal_test_*`、`old_dev_access`、`router_confirm_access` 全为 0，`task40_ignored_cache_imported=false`，formal test 未 materialize。
5. 复核 Windows 工作树 CRLF 规范化后的 SHA-256：P2 machine=`e1e8a45bfd6ba9fc725d099b7d500584d6ba39c390602d48f48b78690580aa5a`；paired evidence=`0ae90e3d0410eddeda96ec31effebf5bbe01334d5a45ecc4a2839b11a9735500`；access ledger=`b03934d14e230fd084208b375400970908a948bb14980312ceed702b33e4da6a`；confirm feature manifest=`6ad89890156a35df1cdfd5227c13d26a87aed50b9ff09585618fd49eba1f08e7`；one-shot marker=`53b53e6153a1ef7cb4d6e79b90bf82268610be4dd273109a4fe8da75ecab2c6a`。原始 Git blob 为 LF，按 Windows checkout 的 CRLF 计算与交付 hash 一致。
6. 交付报告保留了缺 pytest、预期 import 红测、网络 `WinError 10013`、`rg.exe` 拒绝执行、`.venv` 入口不存在和 data-free preparation check `FileNotFoundError` 等失败事实；未把失败运行删除或写成 PASS。
7. P2 配置声明 `torch_threads=4`，实际 machine report 为 14。该偏差已披露；DIAG_CONFIRM one-shot 禁止补跑，不能用补跑修复。

## 结论与后续边界

Task45 的弱 Brier/MAE/Spearman/top-decile 信号只能作为下一条路线的待检验动机，不能写成“收益已经可学习”。有效下一步必须是 v1.25 候选 Task46：新的跨 source-group 负控、FIT 内 nested OOF 后验效用学习、风险预算三动作和一次性 ROUTER_CONFIRM 主 JSD。已看过的 DIAG_CONFIRM、旧 DEV、formal test 永久不作确认集；本文件不授权 Task46 创建、训练或打开确认集。

