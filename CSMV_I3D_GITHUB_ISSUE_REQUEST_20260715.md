# CSMV I3D官方GitHub Issue手工提交包

> 目标仓库：`IEIT-AGI/MSA-CRVI`  
> 目标渠道：GitHub Issues  
> 范围：只请求可公开复现的资产元数据，不请求或下载特征内容
> 提交状态：已于2026-07-15作为官方Issue #5提交；本文件不得再次用于重复创建Issue

## 建议标题

Request for I3D feature asset license and reproducibility manifest

## 建议正文

Hello MSA-CRVI maintainers,

We are preparing a reproducible academic evaluation using the public CSMV/MSA-CRVI benchmark. Before using the released I3D visual feature family, could you please clarify or publish the following metadata?

1. The asset-level license or research-use permission applicable to the released I3D feature files.
2. A stable release revision, snapshot identifier, or dated version.
3. A machine-readable manifest containing relative filenames, byte sizes, and SHA-256 checksums.
4. Coverage of the 8,210 official `video_file_id` values, including any missing or extra keys.
5. Total asset size and expected download/storage size.
6. The feature extractor and weights version, sampling configuration, dtype, and per-file tensor shape.

A small CSV, JSON, or SHA-256 manifest in the repository or an official release would be sufficient. We are requesting metadata only and will not download or use the feature content until the license and fixity have been independently reviewed.

Thank you for your help.

## 提交后记录

手工提交成功后，只记录公开的issue number、公开URL和创建日期；不要把Cookie、账户标识、私有通知或其他个人信息写入Git。成功创建后不得通过连接器重复发送。

已提交定位：`https://github.com/IEIT-AGI/MSA-CRVI/issues/5`。唯一一次跟进最早为2026-07-22，且只能在该Issue内进行。
