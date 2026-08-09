---
type: study
topic: "Python、JSON、测试与实验复现"
course: "生成式AI基础与Prompt工程"
tags: [学习, 45-生成式AI基础与Prompt工程, Python, 实验方法]
created: 2026-08-05
status: completed
mastery: not_started
difficulty: beginner
stage_moc: "[[🧭 生成式AI基础与Prompt工程-前置知识]]"
concept: ["可复现实验", "结构化数据", "单元测试"]
prerequisites: ["Python变量与函数"]
related: ["Prompt工程-需求-任务规格与结构化输出", "Prompt评测-实验-指标数据集与误差分析"]
flow: knowledge
kind: concept
source: "Stanford CS336 Spring 2025 Assignment 1 setup and tests; Python standard library documentation"
source_url: "https://cs336.stanford.edu/spring2025/"
accessed: 2026-08-09
license: "课程页公开；CS336 A1 仓库为 MIT License"
anki_deck: "45-生成式AI基础与Prompt工程::课程前置"
anki_tags: [Python, JSON, 测试, 复现]
---

# 课程前置：Python、JSON、测试与实验复现

## 0. 学习边界

- **类别**：A 类（所有作业的基础设施）。
- **判断理由**：Prompt 改写如果没有固定输入、结构校验和回归测试，只是不可复现的聊天体验。

## 1. 这个知识点解决什么问题？

> 同一个方案昨天“看起来有效”，今天却无法复现；模型输出少字段后，后续程序悄悄得到错误结果。

本卡把一次模型调用变成可保存、可比较、可失败的实验记录。

## 2. 为什么它重要？它有什么用？

- 固定随机种子、样本、Prompt 版本和评分器版本。
- 用 JSON 表达输入输出契约，用断言阻止错误继续传播。
- 为 Prompt、RAG 和 Agent 作业建立共同的离线验收层。

## 3. 学它之前需要哪些前置知识？

1. 会定义 Python 函数、列表和字典。
2. 会在终端运行 `python 文件名.py`；若不会，先完成作业 00 的环境诊断。

## 4. 用直觉语言解释它

> “实验像烹饪复刻：数据是食材，配置是称量表，日志是操作记录，测试是出餐标准。”

只有把四者同时保存，改 Prompt 后的差异才有解释价值。

## 5. 正式定义、核心公式、符号解释

一次实验记录定义为 $r=(d,p,m,s,o,e)$，分别表示数据版本、Prompt 版本、模型版本、随机种子、输出和评测结果。

| 符号 | 含义 | 示例 | 约束 |
| :--- | :--- | :--- | :--- |
| $d$ | 数据集版本 | `dev-v1` | 不在调参中偷换 |
| $p$ | Prompt 版本 | `baseline-02` | 文本或哈希可追踪 |
| $m$ | 模型版本 | `model-x-2025-01` | 不只写品牌名 |
| $e$ | 指标与错误标签 | `valid_json=true` | 规则固定 |

JSON 契约至少声明字段名、类型、必需性、范围和额外字段策略。

## 6. 推导思路和思想来源

- **直接方法局限**：肉眼挑几个漂亮输出会产生选择偏差。
- **关键转念**：把模型视为待测函数，把非确定性纳入实验配置。
- **主线**：固定输入 → 调用或读取缓存 → 解析 → 校验 → 评分 → 保存记录 → 比较版本。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

10 条输出中 8 条是合法 JSON，结构有效率为 $8/10=80\%$。不能因为 8 条内容优美就报告“准确率 80%”，因为这只是格式指标。

### 例子 2：中等例子

方案 A 正确 7 条、合法 10 条；方案 B 正确 8 条、合法 8 条。若下游必须自动执行，B 的两条解析失败可能使端到端成功率不高于 A，必须分层报告。

### 例子 3：实际应用例子（可运行 Python）

```python
# 输入：JSON 字符串；输出：标准化结果或明确异常。
import json

def parse_answer(raw: str) -> dict[str, object]:
    data = json.loads(raw)
    if set(data) != {"answer", "confidence"}:
        raise ValueError("字段必须恰好是 answer 与 confidence")
    confidence = float(data["confidence"])
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence 必须位于 [0, 1]")
    return {"answer": str(data["answer"]), "confidence": confidence}

assert parse_answer('{"answer":"A","confidence":0.8}')["answer"] == "A"
try:
    parse_answer('{"answer":"A","confidence":2}')
except ValueError as error:
    print(type(error).__name__, str(error))
```

输出包含 `ValueError confidence 必须位于 [0, 1]`。

## 8. 常见误区和易混概念

- **误区**：代码不报错就等于实验正确。解析成功、任务正确和端到端成功是三种指标。
- **误区**：temperature 为 0 就绝对可复现。服务端版本、并行实现和后端更新仍可能改变结果。

| 概念 | 核心问题 | 区别 | 场景 |
| :--- | :--- | :--- | :--- |
| 单元测试 | 一个小函数对不对 | 快、离线、定位精确 | 解析器与评分器 |
| 集成测试 | 多组件能否协同 | 较慢、故障面更大 | 模型→解析→评分 |
| 实验复现 | 结论能否再次得到 | 还需版本、种子和数据 | Prompt A/B 比较 |

## 9. 课程连接

- 本卡只补到能运行课程实验、保存结构化结果并定位解析失败，不替代完整 Python 课程。
- 课程主线会在 [[Prompt工程-需求-任务规格与结构化输出]] 与 [[Prompt评测-实验-指标数据集与误差分析]] 中复用这里的契约和测试方法。
- 横向：[[AI-Agent-前置-消息JSON异常与单元测试|Agent 前置测试]]。

## 10. 闭卷复现任务

- [ ] 说出一次实验最少要保存的六类信息。
- [ ] 写出只接受两个字段的 JSON 校验函数。
- [ ] 解释格式有效率与任务正确率为什么不能混用。
- [ ] 为同一输入重复运行设计可复现记录。
- [ ] 解释测试替身为何能减少 API 成本与波动。
- [ ] 区分解析成功、任务正确与端到端成功。
- [ ] 说明开发集与测试集的职责差异。
- [ ] 为非法额外字段设计失败测试。
- [ ] 解释模型版本为何必须精确记录。
- [ ] 说出一个真实 Prompt 回归测试场景。

## 11. 自测题：5 道

1. `json.loads` 成功是否证明字段正确？给出理由。 `#自测题/基础`
2. 20 条输出中 18 条可解析，15 条正确，分别计算两种比率。 `#自测题/基础`
3. 为什么测试集不能边调 Prompt 边查看？ `#自测题/中等`
4. 设计三条针对 `confidence` 的边界测试。 `#自测题/中等`
5. 为一次 Prompt A/B 实验写出最小记录 schema。 `#自测题/较难`

> [!question]- 参考答案与评分点
> 1. 不能，还需字段、类型、范围和额外字段校验。2. 90% 与 75%。3. 会向测试集过拟合，应使用开发集调参。4. `0`、`1` 应通过，负数或大于 1 应失败。5. 至少含数据/Prompt/模型/种子/原始输出/评分；每项 1 分。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/45-生成式AI基础与Prompt工程"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 12. 我的主动回忆区

- **闭卷复述**：
- **手写校验器结果**：
- **最容易漏记的实验字段**：
- [ ] 明天  [ ] 3 天后  [ ] 7 天后  [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- 本卡是 45 与 46 两门课共同先修，不再拆成“JSON/测试/日志”三张碎片卡。
- 作业报告应链接本卡并附 `config.json`、逐样本结果和测试命令。

## 🃏 Anki 卡片

Q: 一次可复现实验最少保存哪六类信息？
A: 数据版本、Prompt 版本、模型版本、随机种子、原始输出、评测结果。

Q: 为什么合法 JSON 不等于任务正确？
A: JSON 校验只证明结构满足契约，语义正确性需要独立指标或人工判断。

