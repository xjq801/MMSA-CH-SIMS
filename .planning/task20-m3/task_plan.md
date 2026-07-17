# 20-M3 基线与统一评测

- [completed] 现状审计：确认 `f869732`、总纲 v1.16、formal split 和接受资产风险边界。
- [in_progress] 正式环境锁定：创建独立 `.venv-task20`，但 faiss 安装受代理不可连接阻塞，未宣称就绪。
- [completed] 第一批契约与测试：新增任务20配置、JSONL loader、三种 train-only 基线及指标合同。
- [pending] 接入权威数据清单并生成受控预测/指标 manifest。
- [pending] 环境可用后运行完整门检查与交付审计。

## 不变量

- 拟合/索引/选择只看 train；dev 只校准/选择；test 只最终评测。
- 不引入 teacher、memory、完整 CARM；不复用旧论文数字。
- I3D 许可、官方 revision、权利方身份/fixity 未解决；不得发布或再分发 I3D 资产。
