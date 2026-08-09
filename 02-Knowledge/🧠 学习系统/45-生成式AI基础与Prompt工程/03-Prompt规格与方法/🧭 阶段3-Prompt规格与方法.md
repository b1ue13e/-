---
type: index
topic: "生成式AI基础与Prompt工程阶段3 Prompt规格与方法"
course: "生成式AI基础与Prompt工程"
stage_id: "03"
created: 2026-08-09
status: active
flow: knowledge
kind: moc
source: "CMU 17-630 Prompt Engineering；Stanford CS324 Winter 2022"
source_url: "https://www.cs.cmu.edu/~breaux/prompting/schedule.html"
accessed: 2026-08-09
license: "[待验证]（公开课程页面；本阶段为原创融合与总结）"
tags: [索引, Prompt工程, 实验设计]
---

# 阶段 3：Prompt 规格与方法

## 为什么现在学

阶段 1 已经说明模型是在条件分布上生成，不会自动理解模糊需求，也不会因为语气坚定就获得事实依据。本阶段因此先写任务契约和评测协议，再选择指令、示例或分解方法。顺序不能倒过来：没有固定数据和成功标准，所谓“Prompt 变好了”只是一段无法复现的演示。

## 学完能做什么

- 把自然语言需求改写成输入、输出、约束、拒答和验收规则明确的任务规格。
- 建立固定开发集与测试集，报告任务指标、结构有效率、方差、成本和错误类型。
- 在 zero-shot、few-shot、任务分解与外部验证之间做有证据的选择。
- 识别示例泄漏、顺序敏感、共同偏差和过度分解，并用受控实验修正。

## 学习顺序

1. [[Prompt工程-需求-任务规格与结构化输出]]：先定义任务边界、输出 schema 与失败处理。
2. [[Prompt评测-实验-指标数据集与误差分析]]：把“好答案”转成可运行的评测协议。
3. [[Prompt工程-方法-指令示例推理与约束]]：在规格和基线之上选择最小充分的提示手段。
4. [[Prompt工程-上下文学习-示例选择与提示敏感性]]：用分层示例和多顺序实验检验 few-shot。
5. [[Prompt工程-推理-任务分解自一致性与验证]]：仅在复杂任务需要时引入可验证分解。

## 复习与回顾

- 完成第 2 张卡后，闭卷写出一份 10 样本最小实验协议；若不能说明数据隔离和主指标，不进入方法比较。
- 完成第 4 张卡后，互换两种示例顺序并解释均值与方差，禁止只保留最高分排列。
- 完成第 5 张卡后，把一个真实任务画成依赖图；若每一步没有验证器，合并回更简单的单步方案。

## 阶段验收与作业

```dataview
LIST
FROM "03-Projects/45-生成式AI基础与Prompt工程"
WHERE type = "project" AND project_type = "homework" AND stage_id = "03"
SORT assignment_level ASC, file.name ASC
```

通过标准：至少完成一份 Prompt 基线和一份受控改写，使用相同数据、模型与解码参数；提交逐样本结果、自动 Gate、误差分类和回退结论。只给成功截图、没有原始输出或同时改变多个变量均不通过。

## 下一阶段

进入 [[🧭 阶段4-增强评测与可靠性]]，把本阶段协议扩展到检索证据、LLM Judge、事实核验和提示注入防护。
