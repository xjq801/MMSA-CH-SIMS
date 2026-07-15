# 任务00：CSMV特征资产预审与G2复审裁定

> 复审编号：`REVIEW-00-CSMV-FEATURE-PREFLIGHT-G2-20260715`  
> 复审日期：2026-07-15  
> 复审对象：任务10按`AUTH-00-CSMV-FEATURE-ASSET-PREFLIGHT-RO-20260715`提交的特征资产预审与公共核心复现证据  
> 最终裁定：`REPRODUCIBILITY_STALE_CLOSED_ASSET_ADMISSIBILITY_BLOCKS_G2`

## 1. 00裁定

1. **接受复现陈旧子阻塞已关闭。** 00独立执行`reproduce_m2_minimal.py --public-core`，在Python 3.8.9、`-I -S`下两条子命令均exit 0；19项输出before/after SHA-256完全一致，`mismatches=[]`，凭证环境未转发。`validate_m2_release.py`现场重算19项hash，漂移0并exit 0。
2. **接受特征预审的诚实No-Go。** `validate_csmv_feature_preflight.py` exit 0表示授权边界、固定README和UNKNOWN fail-closed合同一致；其同时明确`g2_asset_ready=false`。公开Drive页面HTTP 200不等于资产获得许可、版本固定或8210覆盖。
3. **G1保持`PASS`，G2不通过。** G2收敛为单一资产准入阻塞：`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`。这里的“单一”指一个资产准入工作包，不表示只缺一个字段。
4. **全局`formal_split=false`、`formal_model_use_allowed=false`。** 不创建任务20，不训练CARM，不建正式索引，不把当前页面可达性写成正式输入可复现。
5. **授权最小外部元数据协调。** 具体范围以`AUTH-00-CSMV-ONE-FEATURE-FAMILY-METADATA-COORDINATION-20260715`为准；该授权不含特征内容下载。

## 2. 独立复核证据

| 复核项 | 00执行结果 | 裁定 |
|---|---|---|
| 公共核心隔离重放 | 19项；两条命令returncode=0；before/after一致；`mismatches=[]` | 复现陈旧关闭 |
| M2 release现场校验 | exit 0；19项当前hash零漂移；7项manifest lineage通过 | 本地发布包可复核 |
| 特征预审专项 | exit 0；`g2_asset_ready=false`；本地`.npy`为0 | No-Go合同有效，不给资产门信用 |
| 泄漏live门 | exit 0；Critical=0；`PASS_WITH_LIMITATIONS` | 可观察范围内通过 |
| 负面夹具 | exit 0；正确输出`LEAKAGE_BLOCKED` | 阻断能力通过 |
| 当前资产元数据 | 许可、revision、文件树/数量、bytes、checksum、8210实际键均UNKNOWN | G2继续阻塞 |

复现边界：该结果是标准库隔离进程重放，不是从全新操作系统/容器重新安装依赖；它足以关闭本项目当前“输出陈旧”子阻塞，但不能替代正式输入资产的外部固定性。

## 3. G2剩余唯一资产准入包

任务10必须为一个且仅一个官方特征族（优先I3D；不可用时才评估VideoMAE）取得并验证：

1. 权利方明确的资产级研究使用许可或书面许可定位，且说明预计算特征是否在许可覆盖范围内；
2. 稳定revision、不可变快照或由权利方签发的版本标识；
3. 机器可读manifest：相对文件名、单文件bytes、单文件SHA-256；
4. 与8210个正式`video_file_id`的精确覆盖结果、缺失/额外键清单及处理规则；
5. 总下载量、校验/解压后空间预算；
6. 特征语义：家族名、提取器/权重版本、dtype、shape或维度、必要的采样/聚合配置。

任一项仍为`UNKNOWN`时，资产准入不通过。若权利方只能确认“可下载”而不能确认许可与固定manifest，G2继续阻塞。

## 4. 后续门顺序

1. 先执行最小外部元数据协调，不下载`.npy`或媒体；
2. 任务10回交权利方证据、脱敏摘要与元数据manifest；
3. 00复审资产准入并选定唯一特征族；
4. 只有资产准入通过后，00另行签发限额下载授权；
5. 下载、逐文件hash、8210覆盖和输入schema全部通过后，00才可重新裁定G2和`formal_split`。

本文件不授权联系范围以外的人员、不授权Drive API、登录数据存储、接受EULA、购买服务、下载特征/媒体或启动任务20。

