# 任务10：I3D序列协议与M1—M2 Git检查点回交

> 回交日期：2026-07-16  
> 回交对象：00总控  
> 状态：`READY_FOR_00_REVIEW_G2_UNCHANGED`  
> SSOT：总纲v1.12

## 1. 本轮完成项

1. 在任何训练和test结果前冻结CSMV I3D序列处理：主协议为完整序列+动态padding/mask，主敏感性为确定性均匀180步，前180仅作补充。
2. 建立版本化协议文档、JSON配置、机器manifest、确定性实现/构建器/validator及8项单元测试。
3. 把允许论文主张收紧为“冻结I3D视觉表征上的公众诱发受众情绪分布预测”，并同步实验协议v2、Data Card、Datasheet、数据字典、M2协议、claim矩阵、G门和HANDOFF。
4. 将音频保持为`STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED`；E1/E5/H3只按实际输入资格运行。
5. 维护者许可/revision/包身份与fixity证明按用户指令标记`DEFERRED_PENDING_MAINTAINER_REPLY`；本轮未等待、未催促、未重复检查，也未写成已解决。

## 2. 协议证据与SHA-256

| 工件 | SHA-256 |
|---|---|
| `CSMV_I3D_SEQUENCE_PROTOCOL_V1.md` | `e584ecb136c50050a8ac29d06df1236cf4750c07e265526684e27323b272515d` |
| `configs/csmv-i3d-sequence-protocol-v1.json` | `42a7384a6bf2a3c4a18578942decb6ac8afde0ffbf5899cb1f7c111b3c86179d` |
| `data/manifests/csmv-i3d-sequence-protocol-v1.manifest.json` | `208615d4059afc8c5c2c57a5ffc13eeafa9a71ece861332d9f1cd62bc9c4d5be` |
| `scripts/csmv_i3d_sequence_protocol.py` | `0ecb92fff40f00492283ced2d85917ef746cbd9628013d2bf5c67199ac463017` |
| `scripts/validate_csmv_i3d_sequence_protocol.py` | `eda1d9f369128602d3b8589189af4fcb7bc6ec5a6190b4f1288ab4e4a3d1e51f` |

长度证据：8,210样本，`T=6—1719`，531个`T>180`、4个`T=180`，P50/90/95/99=`43/133/211/339`；最长单样本原始输入7,041,024 bytes。输入张量门为64 MiB，未触发主协议降级。

## 3. 验证实录

- TDD红灯：`python -m unittest tests.test_csmv_i3d_sequence_protocol -v`首次exit 1，原因是实现模块尚不存在；失败保留。
- 实现后同命令：8/8通过，exit 0。
- 专项validator：`PASS_PREREGISTRATION_ONLY_G2_UNCHANGED`，长度、fixity、重复hash、正向/边界及8类fail-closed检查通过。
- 首次公共核心重放：exit 1，只有`data/manifests/dataset-v1.manifest.json`因新协议lineage发生预期漂移；未删门或弱化断言。
- 用现有确定性构建器重建后再次重放：19项before/after漂移0，exit 0。
- `validate_m2_release.py`：PASS；G1=`PASS`、G2仍blocked、`formal_split=false`。
- 泄漏live no-write：Critical=0；负面selftest输出预期`LEAKAGE_BLOCKED`并exit 0。
- 一次命令误写为不存在的`--selftest-negative`，argparse exit 2；随后按脚本真实接口`--selftest`重跑成功。失败未删除。

## 4. Git与安全状态

- M1—M2内容检查点commit：`f885a59`（`M1-M2 checkpoint: freeze I3D protocol`）。
- commit正文明确：G1 PASS；G2 blocked on CSMV asset license/fixity；`formal_split=false`；task20 not created。
- `git fetch origin`后`origin/main...HEAD=0/1`，随后`git push origin main`成功：`26229c0..f885a59 main -> main`。
- stage审计：107文件；敏感绝对路径0、密钥模式0、tracked数据/媒体大包0、超过10 MiB文件0；`.npy`、raw/processed大包与junction未进入Git。
- 本回交及最终工作日志状态由后续小型收尾commit记录；以最终`origin/main` tip为复审入口。

## 5. 门状态与00请求

- G1=`PASS`。
- G2=`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`。
- 全局`formal_split=false`。
- 未创建任务20、未训练、未建正式索引、未按test标签选择规则。

请求00只复审本轮I3D序列协议、论文边界、复现证据和Git检查点；外部维护者缺口保持延期，不请求据此放行G2。
