---
type: index
topic: "生成式AI基础与Prompt工程前置知识"
course: "生成式AI基础与Prompt工程"
stage_id: "00"
created: 2026-08-09
status: active
flow: knowledge
kind: moc
source: "Stanford CS336 Spring 2025 prerequisites; MIT OCW 6.7960 Fall 2024 prerequisites"
source_url: "https://cs336.stanford.edu/spring2025/"
accessed: 2026-08-09
license: "课程页公开；本地诊断与桥接内容为原创"
tags: [索引, 前置知识, 生成式AI, Prompt工程]
---

# 生成式AI基础与Prompt工程：前置知识

## 为什么先学这些

本课既包含 Prompt 实验，也提供生成模型实现选修。所有学习者都要能运行 Python、验证 JSON、固定数据并手算最小概率例子；只有进入 MIT/CS336 实现分支时，才需要第三张神经网络数学桥接卡。前置层只补到能开始本课，不复制完整 Python、概率论或最优化课程。

## 进入课程的最低标准

先独立完成以下诊断，不看答案：

1. 运行一段 Python，读取 JSON，并让缺字段输入触发明确异常。
2. 手算 `[0, 0]` 与 `[ln 3, 0]` 的 softmax，解释为什么先减最大 logit。
3. 说明开发集和测试集为什么必须隔离。
4. 仅当选择模型实现分支：手算一层 ReLU 的链式法则，并用有限差分核对。

前 3 项全部通过即可进入阶段 1；第 4 项未通过时仍可走 Prompt 主线，但不能开始阶段 2 的官方实现选修。

## 补学顺序

1. [[课程前置-Python-JSON测试与实验复现]]：建立可运行、可解析、可回归的实验底座。
2. [[课程前置-概率向量与Softmax最小补丁]]：读懂 Token 概率、温度与注意力分数。
3. [[课程前置-神经网络数学-凸性几何链式法则与优化]]：模型实现分支所需的几何、梯度与非凸优化桥接。

## 复习与回顾

- 第一次通过后 3 天：不看卡片重写 JSON 校验器和稳定 softmax。
- 进入阶段 3 前：重新解释“格式有效率”和“任务正确率”的区别。
- 任何作业出现解析失败、标签泄漏或结果不可复现时，回到前两张卡定位，不重复通读整门课。

## 阶段验收与作业

```dataview
LIST
FROM "03-Projects/45-生成式AI基础与Prompt工程"
WHERE type = "project" AND project_type = "homework" AND stage_id = "00"
SORT assignment_level ASC, file.name ASC
```

通过前置诊断后进入 [[🧭 阶段1-模型心智模型]]；若选择从零实现语言模型，再额外通过神经网络数学诊断后进入 [[🧭 阶段2-模型实现选修]]。

