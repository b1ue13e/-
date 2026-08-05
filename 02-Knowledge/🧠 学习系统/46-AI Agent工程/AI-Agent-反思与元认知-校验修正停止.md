---
type: study
topic: "AI Agent反思与元认知：校验、修正与停止"
tags: [学习, 46-AI Agent工程, AI-Agent, Reflection, 元认知]
created: 2026-08-06
status: completed
difficulty: intermediate
concept: [Reflection, 元认知, 自我修正]
prerequisites: ["AI-Agent-ReAct推理行动范式", "AI-Agent-规划状态与工作流编排"]
related: ["AI-Agent-上下文工程-选择压缩隔离", "AI-Agent-评测与基准-任务轨迹成本", "AI-Agent-可观测性与生产运行-轨迹审批恢复"]
flow: knowledge
kind: concept
source: "Microsoft AI Agents for Beginners Lesson 9; Datawhale Hello-Agents Chapter 4.4 (repositories verified 2026-08-06)"
source_urls: ["https://github.com/microsoft/ai-agents-for-beginners/tree/main/09-metacognition", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter4"]
anki_deck: "46-AI Agent工程::反思与元认知"
anki_tags: [Reflection, 元认知, 校验, 停止]
---

# AI Agent 反思与元认知：校验、修正与停止

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心控制机制）**。
- **判断理由**：一次生成很难同时完成方案搜索、执行和质量校验。显式反思可以把“哪里错、如何改、何时停”变成可测试状态，但无界反思会增加成本并放大错误。

## 1. 这个知识点解决什么问题？

> **麻烦**：Agent 得到一个看似合理的答案，却没有检查事实、约束、工具结果或完成标准；发现问题后又只是重新生成相同内容。

反思机制把一次尝试拆成：**生成候选 → 用明确标准检查 → 产生结构化反馈 → 有限修正 → 达到门槛或停止。**

## 2. 为什么它重要？它有什么用？

- 代码 Agent：运行测试并按失败类别修复，而不是凭感觉改代码。
- RAG Agent：检查引用是否支持陈述、是否存在未覆盖问题。
- 工作流 Agent：判断计划是否仍可执行，是否应重规划或请求人工输入。
- 多 Agent：把 critic 作为角色或确定性验证器，但不把“多一个 LLM”误当成真实独立证据。

## 3. 学它之前需要哪些前置知识？

1. **[[AI-Agent-ReAct推理行动范式]]**：理解观察如何反馈到下一步行动。
2. **[[AI-Agent-规划状态与工作流编排]]**：反思循环必须有状态、预算和终止条件。
3. **测试与评测基础**：反馈必须来自可验证标准，而非“请更好一点”。

## 4. 用直觉语言解释它

> “先交草稿，再拿着评分表逐项核对；只修改没过的项，达到门槛就交卷。”

反思不是神秘的“让模型想更久”，而是一个带外部证据的反馈控制器。

## 5. 正式定义、核心公式、符号解释

设第 $k$ 次候选为 $y_k$，验证器为 $V$，反馈为 $f_k$：

$$
f_k = V(x, y_k, E), \qquad y_{k+1}=R(x,y_k,f_k)
$$

$$
\text{stop if } pass(f_k) \lor k \ge K \lor cost \ge B \lor no\_progress(f_{k-m:k})
$$

| 符号 | 含义 |
| :--- | :--- |
| $x$ | 任务与验收标准 |
| $E$ | 测试、工具结果、证据或人工反馈 |
| $V$ | 验证器，可为确定性规则、测试或模型评审 |
| $R$ | 根据反馈执行定向修正的策略 |
| $K,B$ | 最大轮数与成本预算 |

### 三类验证器

| 类型 | 优点 | 局限 | 例子 |
| :--- | :--- | :--- | :--- |
| 确定性验证 | 稳定、便宜 | 覆盖有限 | JSON Schema、单元测试 |
| 外部环境反馈 | 接近真实任务 | 可能慢或有副作用 | 编译器、数据库只读查询 |
| 模型评审 | 能处理开放质量 | 偏差、漂移、同源盲点 | 按 rubric 评文章 |

优先级通常是：**确定性验证 > 受控环境证据 > 模型评审 > 无依据自我感觉。**

## 6. 推导思路和思想来源

1. 生成器负责提出候选，不保证知道候选是否满足外部世界。
2. 把完成标准外显，验证器才能返回可操作差距。
3. 反馈必须包含失败类别、证据和建议动作，避免全量重写。
4. 每轮必须比较进展，否则同一错误会循环。
5. 达不到门槛时要暴露不确定性、请求输入或安全失败，而不是伪造成功。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算

验收有 4 项，每项 1 分，门槛 4/4。首稿通过 3 项，只缺“包含来源”。反馈应为 `missing_citation`，修正只添加可验证引用；若无来源则停止并报告证据不足，而非编造 URL。

### 例子 2：反思与重规划

若失败是“工具暂时超时”，执行策略可有限重试；若失败是“计划依赖不存在的数据”，应回到规划阶段；若失败是“需要付款权限”，应进入人工审批。三者不能都归为“再想一次”。

### 例子 3：可运行 Python

```python
from dataclasses import dataclass

@dataclass
class Feedback:
    passed: bool
    reason: str

def verify_json_like(text: str) -> Feedback:
    required = ['"answer"', '"source_id"']
    missing = [key for key in required if key not in text]
    return Feedback(not missing, "missing: " + ", ".join(missing))

def revise(text: str, feedback: Feedback, known_source: str | None) -> str:
    if '"source_id"' in feedback.reason and known_source:
        return text.rstrip("}") + f', "source_id": "{known_source}"}}'
    return text

candidate = '{"answer": "42"}'
for attempt in range(2):
    feedback = verify_json_like(candidate)
    print(attempt, feedback)
    if feedback.passed:
        break
    new_candidate = revise(candidate, feedback, known_source="doc-7")
    if new_candidate == candidate:
        raise RuntimeError("no progress; escalate instead of looping")
    candidate = new_candidate
print(candidate)
```

输出应在第二轮包含 `source_id`。把 `known_source=None` 后，程序会因无进展停止，而不是伪造来源。

## 8. 常见误区和易混概念

### 误区 1：让同一模型批评自己就能消除幻觉

生成与评审可能共享盲点。事实问题要引入工具、来源或独立测试。

### 误区 2：反思轮数越多越好

超过有效反馈覆盖范围后，更多轮数只会增加延迟、成本和偏航风险。

### 误区 3：Reflection 等于重试

重试可使用相同输入；Reflection 必须记录失败证据并改变下一步策略。

| 概念 | 触发 | 是否需要反馈证据 | 典型动作 |
| :--- | :--- | :---: | :--- |
| Retry | 暂态失败 | 可选 | 原步骤有限重试 |
| Reflection | 质量或逻辑差距 | 是 | 定向修正 |
| Replan | 路径不可行 | 是 | 改任务分解/依赖 |
| Human escalation | 权限或判断超界 | 是 | 请求批准或澄清 |

## 9. 双教材定位与 Obsidian 双链

- **Microsoft Lesson 9**：元认知、规划、Corrective RAG 与代码工具，提供能力视角。
- **Hello-Agents Chapter 4.4**：Reflection 的记忆、编码实现、运行分析和成本收益，提供机制案例。
- 上游：[[AI-Agent-ReAct推理行动范式]]、[[AI-Agent-规划状态与工作流编排]]。
- 下游：[[AI-Agent-评测与基准-任务轨迹成本]]。

## 10. 闭卷复现任务

- [ ] 写出生成、验证、反馈、修正、停止五个状态。
- [ ] 区分 retry、reflection、replan 和人工升级。
- [ ] 给一个开放任务设计至少一个非 LLM 验证器。
- [ ] 写出无进展检测与最大预算条件。
- [ ] 修改代码，记录每轮失败类别和累计成本。

## 11. 自测题：5 道

### 1. #自测题/基础
Reflection 比普通重试多了什么？
> [!question]- 答案解析
> 显式验证、结构化失败反馈，以及根据反馈改变修正策略。

### 2. #自测题/基础
为什么单元测试通常优先于模型评审？
> [!question]- 答案解析
> 对可形式化条件更稳定、便宜、可复现，且不与生成器共享语言判断偏差。

### 3. #自测题/中等
检索不到证据时应怎样反思？
> [!question]- 答案解析
> 判断是查询差、索引缺、权限阻塞还是事实不存在；有限改写查询，仍失败则报告证据不足，不生成虚假引用。

### 4. #自测题/中等
何时应该 replan 而不是 retry？
> [!question]- 答案解析
> 当前路径的依赖、能力或前提不成立时；暂态超时才适合原步骤重试。

### 5. #自测题/较难
设计一个防止“模型既出题又判卷”的评测流程。
> [!question]- 答案解析
> 固定独立测试集/标准，优先确定性验证；模型 judge 使用不同提示或模型并校准人工样本，保留逐样本证据与盲评。

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，说明一次有效反思为什么必须改变状态。

### 我的推导复现
> 为自己的项目写停止条件：通过、轮数、预算、无进展、权限升级。

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/46-AI Agent工程/`
- **建议标签**：`#学习` `#Reflection` `#元认知`
- **拆分建议**：项目中积累 5 类以上反馈时，拆出评测规则或错题卡。

## 🃏 Anki 卡片

有效 Reflection 的五步是什么？::生成候选、按标准验证、生成结构化反馈、定向修正、通过或触发停止条件。
Reflection 与 Retry 的区别是什么？::Reflection 使用失败证据改变策略；Retry 可以只是重复原步骤。
反思循环至少有哪些停止条件？::通过验收、达到轮数/成本预算、连续无进展、需要权限或人工判断。
验证器的常见优先级是什么？::确定性验证优先，其次受控环境证据，再次经校准的模型评审，最后才是无依据自评。
