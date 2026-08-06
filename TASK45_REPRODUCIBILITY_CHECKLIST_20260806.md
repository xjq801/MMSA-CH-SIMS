# Task45 reproducibility checklist

> 状态：`LOCAL-ONLY` diagnostic development checklist

- [x] 数据revision、原train成员来源、三角色salt/公式/计数已冻结。
- [x] source group是role、fold和bootstrap的共同隔离单位。
- [x] primary target、200 posterior draws、主先验与敏感性先验已冻结。
- [x] 五个算法seed已冻结；seed/fold不冒充独立n。
- [x] 模型族、四项超参网格、trial上限、tie-break与clip已冻结。
- [x] full、G0、constant与shuffled control共享评估器和预算。
- [x] `PYTHONHASHSEED`必须记录；Python/NumPy/scikit-learn版本与环境lock必须在Task45 P0导出。
- [x] cuDNN deterministic/benchmark状态必须记录；若不使用GPU，登记`NOT_APPLICABLE_CPU_DIAGNOSTIC`。
- [x] DataLoader worker数、shuffle RNG和posterior RNG必须记录；若不用DataLoader，登记`NOT_APPLICABLE`并记录等价迭代顺序。
- [x] 输入、config、代码、角色manifest、feature cache、target、prediction、paired evidence与报告均须SHA-256。
- [x] 旧DEV、router-confirm与formal-test访问事件必须分别为0，失败运行不得删除。
- [x] Task45最终以annotated tag交付；分支不merge main，结果先由总控04独立审核。

