# Task00 对 Task20 post-snapshot 最终收尾的独立裁定

- 裁定ID：`REVIEW-00-TASK20-FINAL-CLOSEOUT-20260801`
- 验收对象：`main@b7855074acbf3aee6bca640a66c891cc4e21ebf9`
- 验收日（D0）：`2026-08-01`（Asia/Shanghai）
- 裁定：`ACCEPTED_WITH_PERMANENT_LIMITATIONS`
- 生命周期状态：`CLOSED_ACTIVE_TIME_BOUND_RETENTION`
- 可见层删除截止：`2026-08-31 23:59:59 +08:00`

## 1. 接受范围

00接受Task20关于唯一`seed=3407`作者原设定探索运行已经完成120个epoch、训练与sidecar正常退出、最小私有证据已冻结且运行实例已释放的收尾提交。接受只闭合Task20探索执行和当前运行态，不改变G3历史裁定，也不把该探索升级为正式结果。

永久实验身份保持：

- `AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`
- `FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`

因此该运行不得进入T0结果、G3主证据、统一baseline、Task50、论文性能claim或“无泄漏复现”主张。Epoch 1—3原始loss、dev metrics和dev predictions三件套缺失是冻结缺口，不补造；I3D许可、官方revision及权利方包身份/fixity继续为`UNKNOWN`。

## 2. 独立核验锚点

提交`b785507`只新增两份收尾文档和一份manifest，并追加`WORK_LOG.md`；四个历史证据提交均存在且为该提交祖先：

- 训练完成：`49c54a5902532f9d6a6f12717cc8acb85305e861`
- 私有最终证据：`787da347366b9e52401585f25501ced0c86ef8aa`
- Word归档：`a7cf77cbaa03ab922e3281b1f4d58a03ee890e4b`
- Epoch 4—120曲线与数据：`b1217a017a5c563f8a8591ef49b930edde5291bf`

本次本地复算的受控文件为：

| 文件 | bytes | SHA-256 |
|---|---:|---|
| `HANDOFF_20_POST_SNAPSHOT_CLOSEOUT_20260801.md` | 5,742 | `c3c0cb9e8bae5587b8829bf9bf26a5f4a16f0f671ed5969d9f0554768b207366` |
| `TASK20_RESTRICTED_STORAGE_LIFECYCLE_CLOSEOUT_20260801.md` | 3,872 | `3ba43927b36c34106788ed473a0a8157152ee497e19f63f2d142f2394fcf9c39` |
| `data/manifests/task20-vccsa-exploratory-final-closeout-v1.manifest.json` | 2,669 | `aaa46ae544e40321c61bfadd95d4bae121501662c02f636b8705a61e190b0fdb` |
| `deliverables/TASK20_VCCSA_EXPLORATORY_ARCHIVE_SUMMARY_20260731.docx` | 131,186 | `73b39428d8c9ff4a50623bdcb9061e847de4668669a19374487c14f6f1417ef4` |
| `deliverables/TASK20_VCCSA_EPOCH_4_120_LOSS_CURVE_20260731.png` | 95,180 | `e7e335701794e686fa26d9a69df8740db3947fa6b8c8c9736be94c143678ced1` |

Word容器完整性检查无坏项，正文明确标记NON_T0/INELIGIBLE及Epoch 1—3缺口；PNG可解码为`1854×917 RGBA`。manifest可解析，绑定最终checkpoint SHA-256 `cd16e7412eec8d3a255e5fa5bc46c8bc53b604c2fe5e22ae0600b8c064428978`、Epoch 116 best权重 SHA-256 `e5033f5dd35dcf02ae660a3af4139c4385d08fbdb1bc3958c7af50d4c6189771`及固定8210项I3D台账。

`WR-20260801-002`保留了提交前“后续将运行门禁”的时点措辞，不能单独证明提交后门已运行；00本批以独立JSON/commit/哈希/容器检查和项目强制门复跑闭合该限制，不追溯改写Task20日志。

## 3. 受限存储生命周期

按`SC-20260719-02/03`和本次接受日，30日受限保留时钟从`2026-08-01`启动，可见层删除截止为`2026-08-31 23:59:59 +08:00`。状态`CLOSED_ACTIVE_TIME_BOUND_RETENTION`只表示训练与复制停止、对象范围和截止日冻结；不表示当前已删除、平台备份已擦除或平台控制面可核验。

届期须另行提交可见层删除清单、计数/缺失探针和可访问控制面证据。平台备份、快照内部副本与物理擦除继续标记`UNKNOWN_PLATFORM_CONTROL_PLANE`；若届期无法访问，应记录失败并继续追踪，不能写成已删除。

## 4. Task30创建门

裁定：`UNBLOCKED_ELIGIBLE_FOR_00_CREATION_NOT_CREATED`。

理由：G3已为`PASS_WITH_LIMITATIONS`，evaluation-kit与正式content-only强基线已冻结，teacher-only上界及普通KD/错配评论/content-only公平比较合同已在总纲v1.21任务30规格中明确；Task20探索的运行态阻断现已闭合。活动30日保留是资产生命周期跟踪项，不会修改实验核心，也不是Task30启动依赖。

本裁定仅解除创建门，不等于本批已创建Task30。创建时仍须用最新main生成独立提示和`HANDOFF_30.md`，传播G3限制、I3D风险、Video2Reaction双轨接口、Task20探索永久禁入边界，并避免与Task10论文段落回填并发修改同一文件。

## 5. 最终结论

Task20状态更新为`FORMAL_CORE_COMPLETED_G3_PASS_WITH_LIMITATIONS_EXPLORATORY_CLOSED_ACTIVE_TIME_BOUND_RETENTION`。本次接受不提升任何论文证据等级；后续只剩受限存储届期删除验收与常驻资产风险追踪，Task30可由00另行创建。
