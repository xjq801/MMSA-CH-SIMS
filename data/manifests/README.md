# 数据清单区

仅保存可提交的小型schema、ID清单、哈希与lineage元数据。不得包含评论正文、平台用户标识、Cookie、密钥或受限下载链接。

M2按`HUMAN_GOLD`、`SILVER`、`UNLABELED`分别维护manifest。原始清单必须记录固定revision、逐文件hash、样本数、字段、来源和许可状态；派生清单必须记录输出hash和处理协议。许可未知不等于可用，`UNKNOWN`不得改写为`PASS`。

步骤34—39的发布候选使用`dataset-v1.manifest.json`、`split-v1.manifest.json`、`label-provenance-v1.manifest.json`、`leakage-audit-v1.manifest.json`和`reproducibility-v1.manifest.json`。当前状态必须保持`LOCAL_CANDIDATE_G1_BLOCKED`；只有00任务书面通过G1/G2后才能建立正式split或改为正式benchmark状态。

第二人工主集公开元数据只读审计使用`second-primary-readonly-audit-v1.manifest.json`。它只登记3项短名单和1项深审的公开证据，不是数据下载manifest、许可放行或主集冻结；`downloaded_assets`必须为空，G1/G2和`formal_split=false`必须保持阻塞状态。
