# CSMV媒体lineage与同源split审计（2026-07-15）

> 结论：`CSMV_MEDIA_LINEAGE_CLOSED_00_ACCEPTED`。00复审`REVIEW-00-CSMV-LINEAGE-G2-20260715`接受命名空间纠正和同源split修复；G2因正式输入资产许可/固定性及复现manifest陈旧而保持阻塞，`formal_split=false`且不创建任务20。

## 1. 语义纠正

官方固定commit `99d14240254b1381dde0b9c56add140381f65117`中的`CSMV_rawLinks.xlsx`有三列：`No.`、`ID`、`URL`。`ID`是CSMV内部`video_file_id`，URL末尾数字是TikTok平台源视频ID。该表本身就是“内部ID → 源URL”的权威映射，官方README没有规定两种ID必须相等。因此2,644行“不相等”不是映射错误；旧校验把两个不同命名空间误当作同一命名空间。

原始工作簿保持只读，SHA-256为`cb3a6a1a524faf3665e03bee523f68185a995cd4411f0888387dc1719727a4c3`。解析器只读取单元格文本，不加载损坏样式，不修改工作簿，不访问URL。

## 2. 真实风险与修复

8,210个内部视频ID对应8,008个平台源视频ID；其中202个源视频族各对应2个内部样本，共404条样本。修复前按内部ID散列会使100个源族跨`group_by_video_v1`，并使115个源族跨`hashtag_heldout_v1`。

修复后：

- `source_group_id = SHA-256("csmv-source-platform-video-v1|" + 平台源视频ID)`；tracked manifest不写原始URL或平台ID；
- `group_by_video_v1`按`source_group_id`划分；
- hashtag连通分量先合并同一源视频族的hashtags，再划分held-out；
- 8,008个源族在`group_by_video_v1`、`hashtag_heldout_v1`和未分配的topic协议中跨split交集均为0；
- 负面夹具强制把同源样本放入不同split时，validator能检测并阻断。

修复后的规模：

| 协议 | train | dev | test | 同源族跨split |
|---|---:|---:|---:|---:|
| `group_by_video_v1` | 5,698 | 837 | 1,675 | 0 |
| `hashtag_heldout_v1` | 7,211 | 327 | 672 | 0 |

## 3. 可复现证据

- 统一解析与语义：`scripts/csmv_media_lineage.py`
- 构建器：`scripts/build_m2_data_artifacts.py`
- 逐项脱敏lineage：`data/manifests/csmv-media-lineage-v1.manifest.json`
- split摘要：`data/manifests/csmv-split-v1.manifest.json`
- 专项门：`scripts/validate_csmv_media_lineage.py`
- 全局泄漏门：`scripts/run_m2_leakage_tests.py`

专项门核对8,210/8,008/202/404、逐项item—source group—URL hash—split闭合、工作簿hash、零同源交叉和负面夹具。全局门同时检查item、source group、评论归属、目标评论字段、未来候选字段、train-only索引、时间合同与fit范围。

## 4. 诚实边界

- 本轮没有下载、预览、流式读取或补采任何视频/特征包，没有访问TikTok URL。
- 该修复建立的是官方固定工作簿上的100% ID→URL元数据lineage，以及可观察源视频ID范围内的同源隔离；不宣称拥有或可再分发原始媒体。
- 未观察的内容级近重复、发布者捷径和时间顺序仍分别受“无媒体指纹”“无发布者字段”“无发布时间”限制；时间协议保持`NOT_APPLICABLE_NO_TIME_SPLIT`。
- 00已接受本专项的lineage/split结论，但不据此自动通过G2；具体阻塞与最小授权见`TASK00_CSMV_LINEAGE_G2_REVIEW_20260715.md`和`TASK00_CSMV_FEATURE_PREFLIGHT_AUTHORIZATION_20260715.md`。
