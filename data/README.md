# 数据区政策

- `raw/`：原始下载物，只读保存；禁止人工覆盖。实体文件由`.gitignore`排除。
- `processed/`：可重建的处理产物；必须关联处理脚本、输入哈希和配置。
- `manifests/`：可提交的小型清单、schema和哈希记录，不含评论正文或用户标识。

任何下载前先更新根目录的 `DATA_SOURCE_LEDGER.md`。许可、条款或再分发边界为`PENDING/UNKNOWN`时，不得进入正式实验。
