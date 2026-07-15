# CSMV I3D本地隔离资产审计与使用说明

> 日期：2026-07-15  
> 状态：`QUARANTINE_ACQUIRED`  
> 正式模型使用：禁止，等待资产级许可、稳定revision、权利方fixity确认与00复审

## 1. 已建立的项目目录

用户提供的源目录保持不变、未复制、未重命名；tracked材料不记录本机绝对源路径。

项目在Git忽略隔离区建立只读使用入口：

```text
data/raw/csmv/features/
└── visual_feature/
    └── I3D/  -> <USER_LOCAL_I3D_PACKAGE>
        ├── 6634586132120079622.npy
        ├── ...
        └── feature_shapes.json
```

该入口是Windows directory junction，不额外占用约2.56 GiB磁盘。原目录被移动或删除后入口会失效。

## 2. 现场审计结果

| 项目 | 结果 |
|---|---:|
| `.npy`文件 | 9,942 |
| `.npy`总字节数 | 2,752,998,144 |
| CSMV要求的`video_file_id` | 8,210 |
| 已命中 | 8,210 |
| 缺失 | 0 |
| 非当前CSMV标签集附加文件 | 1,732 |
| dtype | 9,942个均为`float32` |
| shape | 9,942个均为`(T, 1024)` |
| 时间步范围 | 6—1,719 |
| schema错误 | 0 |
| 全包内容树SHA-256 | `35be2d18e1d2413ba3765034cdb454baa5e3496d49c540c9be00e81bbc2c1942` |

`feature_shapes.json`只有646条声明，是部分shape清单；这646条全部有对应文件且声明长度与数组头一致。完整9,942文件schema由审计脚本直接读取NumPy header核验，不依赖该部分清单。

逐文件fixity与8,210覆盖证据位于：

`data/manifests/csmv-i3d-quarantine-v1.manifest.json`

## 3. 如何读取

按官方`video_file_id`读取并仅显示shape：

```powershell
.\.venv\Scripts\python.exe scripts\load_csmv_i3d.py --video-file-id 6815001842360143109
```

按本项目canonical `item_id`读取：

```powershell
.\.venv\Scripts\python.exe scripts\load_csmv_i3d.py --item-id 210c4a127f25c6c25246df2f1e656d1b1f6d33c8b7c2dacf2ef332e19ff70778
```

在Python代码中使用：

```python
from scripts.load_csmv_i3d import load_by_item_id

features = load_by_item_id(item_id)  # numpy.memmap, shape=(T, 1024), float32
```

加载器使用`mmap_mode="r"`与`allow_pickle=False`，不一次性把全包读入内存。序列处理现已在任何训练和test结果前冻结：主协议为完整序列+动态padding/mask，主敏感性为确定性均匀180步；见`CSMV_I3D_SEQUENCE_PROTOCOL_V1.md`。本轮仍不执行训练或全量物化预处理。

如果不使用项目junction，可在本机`.env`或进程环境中设置`CSMV_I3D_ROOT`，也可向CLI传`--feature-root`。绝对本机路径不写入tracked manifest。

## 4. 复核命令

```powershell
.\.venv\Scripts\python.exe scripts\audit_csmv_i3d_asset.py `
  --feature-root data\raw\csmv\features\visual_feature\I3D `
  --observed-date 2026-07-15 `
  --output data\manifests\csmv-i3d-quarantine-v1.manifest.json
```

该命令读取全部文件头并计算SHA-256，当前耗时约33秒，不修改特征文件。

## 5. 诚实边界

- `float32[T,1024]`、文件夹名称与官方README命名共同支持“I3D兼容包”判断，但不能替代权利方对资产身份和提取器版本的确认。
- 本地逐文件hash能固定“当前拿到的字节”，不能证明它与官方某个稳定revision相同。
- 资产级许可仍为`UNKNOWN_NOT_EXPLICITLY_COVERED`；公开可下载或用户已取得不等于允许正式训练、发表或再分发。
- 因此当前只闭合了本地文件树、体量、schema、fixity和8,210覆盖；G2及`formal_split=false`暂不改变，也不创建任务20。

## 6. 论文实验可行性复核

CSMV的NeurIPS 2024正式论文明确说明：为保护隐私不发布原始视频，而发布I3D、R(2+1)D和VideoMAEv2等预训练视觉特征，并用同一批特征评估所提方法；论文实验表也直接包含TBJE、SELF-MM、MISA、MMIM、CubeMLP和VC-CSA的I3D结果。因此，预提取I3D本身足以支撑与原论文同类的下游预测、融合、校准和消融实验，不必取得`.mp4`才能开展这类研究。

该训练前协议缺口现已关闭：官方README写“limit the max tensor length as 180”，而8,210个正式文件中531个`T>180`，最大1719；中位数43、P90=133、P95=211、P99=339。任务10在查看test结果前把完整序列+padding/mask冻结为主协议，把覆盖首尾的确定性均匀180步冻结为主敏感性协议；前180步仅作补充诊断。资源画像显示最长单样本原始输入约6.71 MiB，未触发主协议降级。

论文第3.4节还写明代码与数据按CC BY-NC-SA 4.0用于学术非商业研究，而仓库README只明确代码MIT、annotations CC BY-SA 4.0。前者为开展学术实验提供了强支持，但两处许可表述并不完全一致；在00正式裁定前，特征再分发与最终G2仍保持fail-closed。

维护者证明按用户指令暂记`DEFERRED_PENDING_MAINTAINER_REPLY`；本轮不等待、不催促、不重复检查Issue，也不把该延期写成已解决。
