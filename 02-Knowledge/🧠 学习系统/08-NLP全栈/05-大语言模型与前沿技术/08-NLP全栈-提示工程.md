---
sources: ['Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. NeurIPS 2022.', 'Yao, S., et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. NeurIPS 2023.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "提示工程"
created: 2026-08-06
status: completed
assessment_exempt: false
difficulty: intermediate
stage_moc: "[[🧭 阶段5-大语言模型与前沿技术]]"
upstream: ["[[08-NLP全栈-HuggingFace生态系统]]"]
tags: [学习, NLP, 提示工程, CoT, ToT, Few-shot, ReAct]
---

# 08-NLP全栈-提示工程

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 大语言模型在面对复杂的多步逻辑推理（如数学计算、符号推导、代码生成）时，如果直接要求其输出最终答案（Direct Prompting），准确率往往极低。如何通过结构化的 Prompt 提示设计（Zero-shot, Few-shot, Chain-of-Thought, Tree-of-Thoughts）显式诱导 LLM 的推理链，是发挥模型潜能的关键技术。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是无需参数训练即可提升大模型复杂推理能力（Reasoning Capabilities）的最轻量级工程手段。
- **实际应用场景**：Chain-of-Thought (CoT 思维链)、Self-Consistency (自一致性采样投票)、Tree-of-Thoughts (ToT 树状探索与回溯)。

---


### 3.1 形式化概率模型与 In-Context Learning 条件概率

提示工程的核心是通过上下文示例 $C = (x_1, y_1, x_2, y_2, \dots, x_k, y_k)$ 改变语言模型的条件概率分布：
$$P(y \mid x, C) = \frac{P(x_1, y_1, \dots, x_k, y_k, x, y)}{P(x_1, y_1, \dots, x_k, y_k, x)}$$

Chain-of-Thought (CoT) 将最终推导拆解为隐式思维链中间步骤 $\mathbf{z} = (z_1, z_2, \dots, z_m)$：
$$P(y \mid x) = \sum_{\mathbf{z}} P(y, \mathbf{z} \mid x) = \sum_{\mathbf{z}} P(y \mid \mathbf{z}, x) \prod_{j=1}^{m} P(z_j \mid z_{<j}, x)$$


## 3. 核心 Prompt 范式对比

| 范式名称 | 英文全称 | 核心原理 | 适用场景 |
| :--- | :--- | :--- | :--- |
| **Few-shot Prompting** | 少样本提示 | 给出 1~5 个 `Input -> Output` 示例 | 格式规范化、特定输出结构控制 |
| **CoT** | Chain-of-Thought | 在示例或指令中加入 `"Let's think step by step"` | 算术、逻辑推理、符号求值 |
| **Self-Consistency** | 自一致性 | 高 Temperature 采样多条 CoT 推理链，Majority Vote 投票 | 高精度数学与代码断言 |
| **ToT** | Tree-of-Thoughts | 生成 Thought 分支，结合 DFS/BFS 树检索与 LLM 自评估评估节点 | 复杂棋局、长流程决策规划 |

---

## 4. Python 代码示例：CoT 与 Self-Consistency 实现

```python
from collections import Counter
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 示例：构造 CoT 提示词模版
def build_cot_prompt(question: str) -> str:
    return f"""Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?
A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls. 5 + 6 = 11. The answer is 11.

Q: {question}
A: Let's think step by step."""

print(build_cot_prompt("Janet has 3 cats. Each cat eats 2 cans of food per day. How many cans for 7 days?"))
```

---


## 5. 常见误区与对比矩阵

| Prompt 策略 | 适用场景 | 格式示例 | 核心优缺点 |
| :--- | :--- | :--- | :--- |
| **Zero-Shot** | 基础指令理解、简单分类 | `"请总结以下文本：..."` | 无需样例，极其简便；对复杂推理准确率低 |
| **Few-Shot** | 格式标准化、特定域输出 | `"[示例1] -> [输出1]
[输入] -> "` | 显著提升输出格式一致性；受样例顺序敏感度影响 |
| **Chain-of-Thought (CoT)** | 算术推理、逻辑推理、代码生成 | `"Let's think step by step."` | 激活模型中间推理路径；增加了生成的 Token 耗时 |
| **Tree of Thoughts (ToT)** | 棋类规划、博弈、复杂决策搜索 | 结合 BFS/DFS 搜索树与评估器 | 探索全局最优解；调用开销呈指数级增长 |





## 6. 闭卷自测与验收入口

请在不查阅资料的前提下尝试解答以下问题，或完成对应关联作业：
1. 本知识点的核心定义与推导公式是什么？
2. 相比传统方法，它的核心优势与工程选型 Trade-offs 是什么？
3. 如何在 PyTorch / Python 中实现并校验其关键张量维度与运算逻辑？


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《提示工程》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《提示工程》的核心机制及其与上下游模块的连接逻辑。
2. **代数/代码自测**：手写关键代数推导步骤或 PyTorch/Python 核心实现伪代码。
3. **防错自测**：如果输入数据出现极小值或极大值离群点，该模块会发生什么异常？如何做数值稳定防护？


---

## 🛠️ 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
