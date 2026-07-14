# Silver-label pipeline v1

配置权威文件为`configs/silver-label-pipeline-v1.yaml`。当前只导入CUC-IGPE-v2遗留二分类标签，不运行新教师模型。

- 教师模型身份与训练快照未保存，登记为`UNKNOWN_LEGACY_TEACHER`。
- 旧阈值规则仅用于复核缺显式标签的遗留记录；因982条显式标签与阈值不一致，阈值不能定义新人工金标。
- CUC向量标签固定为`SILVER`；与本地连续情绪/显式或旧派生标签不一致的221条保留并置冲突标志，不自动删除或重标。
- 置信度缺失时写`null/UNKNOWN`，禁止伪造概率。
- 银标manifest、目录和加载入口与`HUMAN_GOLD`分离；禁止与公开人工test标签合并。
