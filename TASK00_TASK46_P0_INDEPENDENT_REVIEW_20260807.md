# TASK46 P0 独立总控复核（2026-08-07）

## 裁定

总控04接受独立 Task46 线程的 P0 交付，裁定为：

`PASS_P0_GATES_BLOCKED_P1_CONTENT_ASSET_ADMISSIBILITY`

这不是 utility learnability、policy 或论文 claim 的通过。P1/P2/P3 未执行，P4、formal test 与 Task50 继续未授权。

## 交付身份与复核锚点

- 执行线程：`019fda1c-0f78-7053-9ad1-769f0bd5e899`。
- 起始锚点：`origin/main@e3a7864de6ae8fa13221b710011b53833dc2af0d`。
- 独立本地提交：`6a1aa5cbe99addd5cc12075288f76db56925cf7f`，父提交为 `e3a7864...`；未推送、未合并 main。
- P0 delivery manifest SHA-256：`488b632176a146d37843c3df6f66aff5911809e07e9450f984b38488a2978b33`。
- P0 artifact-set SHA-256：`13e331a739d23228a56a670153555cb3ab0cd4b3c8743394e26e1e6d2779ad3d`。

## P0 证据

- FIT：3,404 videos / 3,304 source groups；角色间和 FIT fold source-group overlap 均为 0。
- 跨 source-group、support-stratified derangement：200/200 通过；最小 target-change rate `0.9935370153`，最大 `|Spearman rho|` `0.0493317220`，同源分配 0，层内边际精确保留。
- asset-free null sanity：shuffled ridge-minus-constant cluster-bootstrap 95% CI `[0.0004761685, 0.0009114618]`，未优于 constant。该 sanity 只用于实现/泄漏护栏，不是 scientific T0 证据。
- zero-event ledger：旧 DEV、旧 TRAIN_DIAG_CONFIRM 复用、TRAIN_ROUTER_CONFIRM 提前访问、formal-test access/ID/label/feature/prediction、真实 I3D 读取均为 0；Task50 未创建。
- 验证：P0 validator exit 0；10/10 tests OK；delivery payload 19/19 SHA 一致；`git diff --check` exit 0；WORK_LOG validator 280 条、0 错误。
- 正式 P0 runner 外层命令曾超时 exit 124，但完整 artifact 已落盘；该失败被保留，独立 validator 对 artifact 重算通过，不把超时伪写成成功。

## P1 阻塞与边界

当前没有第二个已冻结、可审计的 T0 content representation。CSMV 的 I3D/VideoMAE 资产仍处于 `UNKNOWN` 许可、官方 revision、权利方包身份与 fixity 状态；本次未读取真实 I3D。response support、source identity hash pseudo-feature 不能替代 T0 内容输入，也不能进入 P1/P2 scientific claim。

因此不解除 `BLOCKED_P1_CONTENT_ASSET_ADMISSIBILITY`。除非另行冻结一个 T0 内容表示及其来源、许可、revision、覆盖、逐文件 hash 和使用合同，否则不得进入 posterior utility prediction、nested OOF、policy simulation 或任何 confirmation role。

## 继续禁止

Task40 仍为 `CLOSED_NOT_PASSED_ROUTER_MAIN_JSD`；Task45 仍为 `CLOSED_NOT_PASSED_T0_BENEFIT_LEARNABILITY`；不得重跑或改判。不得访问旧 DEV/DIAG_CONFIRM/ROUTER_CONFIRM，formal test 继续零 materialization，Task50 不创建。I3D 不确认、不再分发。

## 证据路径

完整交付位于独立提交 `6a1aa5c...` 的 `HANDOFF_46.md`、`experiments/task46-v125-posterior-utility/p0/`、`scripts/task46_p0.py`、`scripts/validate_task46_p0.py` 与 `tests/test_task46_p0.py`。本文件只记录总控裁定，不复制或重写实验核心结果。
