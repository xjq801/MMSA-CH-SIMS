# CSMV官方GitHub仓库直接克隆审计

> 日期：2026-07-15  
> 来源：`https://github.com/IEIT-AGI/MSA-CRVI.git`  
> 本地目录：`data/raw/csmv/upstream-git-20260715/`（Git忽略）  
> 裁定：`GITHUB_REPOSITORY_DOWNLOAD_READY_FEATURE_ASSETS_ABSENT`

## 1. 下载结果

- 使用HTTPS执行浅克隆：`git clone --depth 1 --single-branch --branch main`。
- 克隆成功，耗时约20秒；Git pack约4.97 MiB，不需要用户代为下载。
- HEAD：`99d14240254b1381dde0b9c56add140381f65117`，与项目既有固定上游revision一致。
- 仓库状态：`main...origin/main`，无本地修改。

## 2. 提交内容审计

- Git提交共10个文件，canonical blob总量14,436,790 bytes。
- `CSMV/`目录共8个文件、14,647,070个工作树字节，内容为评论标注、split、标签映射、`video_to_comment`和`CSMV_rawLinks.xlsx`。
- 提交内`.npy`文件数：0。
- Git LFS pointer命中数：0。
- 因此官方GitHub仓库没有内嵌I3D、VideoMAE/VideoMAEv2或其它正式视频特征内容；README中的外部Drive链接仍是独立资产入口。

## 3. Windows换行与fixity边界

本机Git checkout对8个文本文件执行了LF→CRLF工作树转换，导致工作树SHA-256不同于canonical Git blob；`git status`仍为clean。这不是上游数据漂移。

通过`git show HEAD:<path>`读取canonical blob后逐文件与既有固定快照`data/raw/csmv/99d14240254b1381dde0b9c56add140381f65117/`比较：

- 文件集合差异：0；
- snapshot与Git blob hash/bytes不一致：0；
- 发生工作树换行转换的路径：8；
- 既有固定快照继续是canonical字节依据，逐文件SHA-256见`data/manifests/csmv-source-v1.manifest.json`。

## 4. G2影响

本次克隆证明GitHub仓库本身可快速、匿名、可复现取得，并再次闭合小型标注包revision；它不提供特征资产级许可、特征文件树、bytes/SHA-256、特征schema或8,210键实际覆盖。因此：

- G1保持`PASS`；
- G2保持`BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE`；
- 全局`formal_split=false`；
- 不授权或触发Google Drive、`.npy`、视频或媒体下载；
- 不创建任务20。
