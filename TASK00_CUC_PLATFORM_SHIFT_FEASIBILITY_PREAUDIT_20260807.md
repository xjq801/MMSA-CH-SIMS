# TASK00 CUC-IGPE 平台情绪偏移只读预审

> 审计编号：`SC-20260807-01`  
> 执行角色：00-T-AFFC 总控04  
> 日期：2026-08-07（+08:00）  
> 类型：只读身份/字段/T0/标签/许可预审；不是Task35创建或训练授权

## 1. 输入与可追溯性

| 输入 | 结果 |
|---|---|
| `D:\soft\v1.26_TAFFC路线修改提案 (1).docx` | SHA-256=`CF144F8D0CA8569784AF56FE8ED9A3CA82E5FE3769704EBD208DB2A095765249`；已用`docx_read.py`读取标题、段落、runs、表格、layout与props |
| `D:\MMSA-CH-SIMS\data\processed\SILVER\cuc_igpe_v2\canonical.v1.jsonl` | 2,787行；SHA-256=`407D68D96071DD11A850BE59B42879E725026493D58B44220D4CFB79F571A415` |
| `D:\MMSA-CH-SIMS\data\manifests\cuc-canonical-v1.manifest.json` | SHA-256=`3A8E9CF24CF547A8F73259D89CD0FC787974FEB7ECDFE6C1636C4D81B035B3F7`；`license_status=UNKNOWN_LOCAL_ONLY` |
| `CUC_CANONICAL_AUDIT.md` | 已有审计SHA-256=`C9CFE589D5A4D7B552B81171AEBA668A8D68C610B9C877B628456E30A975B66C`；2,815历史manifest仍缺失 |
| 用户共享对话 | `https://chatgpt.com/s/t_6a7585993ca881919a150d05febc55b5`在当前无登录网页读取仅返回登录壳，未获得对话正文；不据此补造事实 |

## 2. 只读字段与身份检查

通过PowerShell/Python只读遍历canonical（只输出字段名、计数与哈希摘要，不输出评论正文、用户标识或原始平台值）：

- 字段集合含`publisher_id`、`source_domain`、`topic_id`、`publish_time`、`response_count`、`legacy_features`等；没有独立`platform`字段。
- `publisher_id`存在于2,787/2,787行，但其语义不能未经来源证明升级为平台处理变量或因果干预。
- `publish_time`仅883行存在，1,904行缺失；28行历史漂移、221条label conflict、8条缺BV仍未闭合。
- 2,787/2,787行均为`label_tier=SILVER`且`label_source=silver_legacy_vector_binary_label`；无独立人工金标闭合证据。
- 2,787/2,787行均为`available_at_t0=false`与`legacy_features_available_at_t0=false`；48维legacy向量不能作为合法T0平台或内容输入。
- canonical split仍为`not_assigned`，不能直接支持跨平台held-out或同内容配对泛化结论。

## 3. 门判定

| 门 | 判定 | 依据 |
|---|---|---|
| canonical identity/fixity | `WARN_BLOCKED` | 当前版本可hash，但2,815→2,787漂移无原始manifest解释 |
| platform provenance | `FAIL` | 无独立platform字段；publisher/source不能直接替代 |
| same-content cross-platform support | `UNKNOWN_BLOCKED` | 当前canonical未提供可审计配对与覆盖合同 |
| T0 content/input | `FAIL` | 全部`available_at_t0=false`，legacy全禁 |
| label/response role | `BLOCKED` | 全部SILVER，人工金标与响应窗口未闭合 |
| license/privacy/platform terms | `UNKNOWN_BLOCKED` | manifest为`UNKNOWN_LOCAL_ONLY`，未形成可发布/可复核合同 |

## 4. 裁定与边界

本次只读预审裁定：`PLATFORM_SHIFT_FEASIBILITY_BLOCKED_NO_PLATFORM_FIELD_T0_GOLD_OR_LICENSE`。

因此：

1. 不计算或报告平台间JSD、熵或极化为科学结果；不把publisher差异写成平台效应或因果效应。
2. 不创建`Task35-Pilot`执行线程，不训练Platform Encoder/Context Adapter，不把CUC字段加入Task46。
3. Task40保持`CLOSED_NOT_PASSED_ROUTER_MAIN_JSD`；Task45保持`CLOSED_NOT_PASSED_T0_BENEFIT_LEARNABILITY`；Task46保持`P0_ACCEPTED_P1_BLOCKED_CONTENT_ASSET_ADMISSIBILITY`。
4. `TRAIN_ROUTER_CONFIRM`、旧DEV/DIAG_CONFIRM、formal test与Task50继续零事件/封存。

## 5. 若未来重新申请Task35，最低补件

必须由用户另行明确授权并提交独立hash-bound创建合同，至少包含：平台字段来源和采集时间、同内容跨平台配对与覆盖、合法T0内容表示、人工/银标角色与响应窗口、publisher/topic/time split、许可/隐私/平台条款、逐文件fixity、失败树与停止门。P0任一项未闭合即关闭，不得用跨平台均值差或CUC银标替代。

## 6. 可复核命令

```powershell
(Get-FileHash 'D:\MMSA-CH-SIMS\data\processed\SILVER\cuc_igpe_v2\canonical.v1.jsonl' -Algorithm SHA256).Hash
(Get-FileHash 'D:\MMSA-CH-SIMS\data\manifests\cuc-canonical-v1.manifest.json' -Algorithm SHA256).Hash
```

上述命令均为只读；本预审未访问I3D、formal test、旧确认角色或目标评论正文。
