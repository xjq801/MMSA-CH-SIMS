# T-AFFC 论文写作区

本目录维护英文论文的**单一写作事实源**（manuscript SSOT）。研究问题、数据、协议、任务门和 claim 状态仍由仓库上位 SSOT 管理；本目录不得反向改写已经冻结的研究事实。

## 权威关系

```text
TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md v1.21
        + CLAIM_EVIDENCE_MATRIX.md
        + 冻结结果/统计/审计
                         │
                         ▼ 单向吸收
paper/TAFFC_CARM_MANUSCRIPT_SSOT.md
                         │
                         ▼ 单向生成
IEEE LaTeX / Word / PDF / Supplement
```

- 总纲决定“研究做什么、什么证据可以支持什么主张”。
- `CLAIM_EVIDENCE_MATRIX.md`决定 claim 的活动状态；`TO_VERIFY`不能在论文中写成结果。
- `TAFFC_CLAIM_BLACKLIST_20260724.md`约束标题、摘要、引言、贡献、相关工作、结论、图注和补充材料。
- 本目录的 Markdown 是正文措辞与结构的权威源；Word、LaTeX 和 PDF 只允许由它单向生成，不接受在派生文件中单独改稿。

## 当前文件

- `TAFFC_CARM_MANUSCRIPT_SSOT.md`：英文论文正文骨架与稳定段落。
- `CLAIM_ARGUMENT_BLUEPRINT.md`：claim—论证—实验—图表—反证映射，以及结果准入合同。
- `figures/`：未来程序化图表源文件；当前不得放入手工伪造或 AI 生成的数据图。

## 当前状态

`MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS`。目前允许完成问题定义、相关工作结构、方法符号、实验协议、伦理和局限框架；摘要结果句、主结果、讨论和结论必须等待任务50冻结的五种子结果、原生内容单元置信区间和 claim 状态复核。

## 更新流程

1. 先在上位台账验收新事实或结果。
2. 按 `CLAIM_ARGUMENT_BLUEPRINT.md` 找到对应 claim 和段落。
3. 只替换有来源的 `[RESULT-GAP:*]`、`[CITATION-GAP:*]` 或 `[DECISION-GAP:*]`。
4. 运行 `python scripts/validate_manuscript_ssot.py`。
5. 回扫摘要、贡献、结果、讨论和结论，确保措辞强度一致。
6. 提交时记录来源文件、结果冻结版本和 Git commit；不得只在聊天或派生 Word 中更新。
