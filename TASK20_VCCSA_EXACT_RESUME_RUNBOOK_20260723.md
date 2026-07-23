# Task20 VC-CSA完整断点续训运行说明

## 适用范围

本说明只适用于`AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`、
`FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`的单种子`seed=3407`诊断运行。它不改变
T0、G3、统一baseline、任务50或论文claim边界。

作者源码必须先通过`apply_compatibility_patch()`生成运行时。补丁会把
`scripts/vccsa_resume_runtime.py`复制为作者运行目录内的`resume_utils.py`，并修改
`main.py`、`train_vccsv.py`和`csmv_dataset.py`。

## 断点合同

`last-resume.ckpt`使用原子“临时文件写入、fsync、同目录replace”更新。每个断点包含：

- 模型、AdamW optimizer和linear scheduler状态；
- 当前epoch、下一batch、global step和TensorBoard step；
- 当前epoch累计loss、历史dev结果、最佳分数和最佳epoch；
- Python、NumPy、Torch CPU、全部CUDA RNG状态；
- 显式DataLoader generator、epoch起始洗牌状态；
- seed、数据集、batch size、epoch数、每epoch step数和train/dev样本数身份合同。

恢复时身份必须完全一致，否则在修改模型前fail closed。精确epoch内重放要求
`num_workers=0`；恢复器会重建相同shuffle顺序、跳过已经持久化的batch，并在继续计算
前恢复断点时的随机数流。

默认每500个optimizer step覆盖一次`last-resume.ckpt`，每个epoch完成dev评估后再覆盖
一次。SIGTERM或SIGINT会在当前batch安全结束后立即写断点并以143退出。硬断电最多会
丢失最后一个已落盘断点之后的计算，但从最后断点恢复的训练状态是完整的。

## 4090首次启动

原A30的Epoch 1作者checkpoint只含模型和optimizer，不符合新schema，不能冒充完整续训
断点。迁移到4090后的本次严格运行应从Epoch 0重新开始。

在原作者启动参数保持不变的基础上，至少追加：

```bash
--seed 3407 \
--num_workers 0 \
--checkpoint_every_steps 500 \
--resume_checkpoint_out /PRIVATE_MATBOX/task20-vccsa-seed3407/last-resume.ckpt
```

断点路径应位于当前区域的私有MatBox目标，并保持既有ACL、加密、fixity和保留策略。
不要放入Git、公开对象存储或镜像的非受限层。

## 恢复启动

必须使用与首次启动完全相同的模型、数据、split、batch size、`max_epoch`和seed参数，
并追加：

```bash
--resume_checkpoint /PRIVATE_MATBOX/task20-vccsa-seed3407/last-resume.ckpt \
--resume_checkpoint_out /PRIVATE_MATBOX/task20-vccsa-seed3407/last-resume.ckpt
```

日志以append模式继续，不再截断已有`log_run.txt`。

## 安全暂停

优先对训练Python进程发送`SIGTERM`，不要立即释放实例：

```bash
kill -TERM <TRAINING_PID>
```

等待进程退出码143，确认`last-resume.ckpt.tmp`不存在、正式断点大小和SHA-256稳定，
再执行`sync`并停止或释放实例。若平台直接断电，则下次从最后一个完整
`last-resume.ckpt`恢复；残留`.tmp`不会覆盖旧断点。

## 跨GPU边界

断点可用`map_location=cpu`从A30/4090等单GPU实例载入，并恢复到目标GPU。不同GPU架构、
CUDA、cuDNN或PyTorch版本可能产生后续浮点轨迹差异，因此跨卡恢复是完整状态恢复，
但不宣称跨硬件逐bit一致。若要求最强可比性，应保持冻结软件栈并从Epoch 0在4090完成
整次运行。
