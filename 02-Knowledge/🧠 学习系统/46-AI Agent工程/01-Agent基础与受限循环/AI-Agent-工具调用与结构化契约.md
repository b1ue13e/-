---
type: study
topic: "AI Agent工具调用与结构化契约"
course: "AI Agent工程"
tags: [学习, 46-AI Agent工程, AI-Agent, 工具调用]
created: 2026-08-05
status: completed
difficulty: intermediate
concept: [工具调用, 函数契约, 结构化输出]
prerequisites: [Python编程与NLP工具, Prompt工程-需求-任务规格与结构化输出, AI-Agent-边界与感知行动循环]
related: [ReAct, 工作流编排, 最小权限]
stage_moc: "[[🧭 阶段1-Agent基础与受限循环]]"
upstream: ["[[AI-Agent-边界与感知行动循环]]", "[[AI-Agent-ReAct推理行动范式]]"]
flow: knowledge
kind: concept
source: "UC Berkeley CS 194/294-196 F24 frameworks; Microsoft AI Agents for Beginners Lesson 4; Datawhale Hello-Agents Chapters 1 and 7; Hugging Face Agents Course Unit 1 Tools"
source_urls: ["https://github.com/microsoft/ai-agents-for-beginners/tree/main/04-tool-use", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter7"]
accessed: 2026-08-08
license: "Microsoft MIT；Hello-Agents CC BY-NC-SA 4.0；Berkeley许可待核验；本卡为原创整合"
anki_deck: "46-AI Agent工程::03-工具"
anki_tags: [46-AI-Agent工程, 工具调用, 契约]
---

# AI Agent：工具调用与结构化契约

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：Agent 的现实影响来自工具，而不是文字。没有契约、校验和权限控制的 tool calling，只是把模型的不确定输出直接接到真实系统。

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：自然语言有歧义，函数需要精确参数；模型可能调用不存在的工具、漏字段、传错类型或重复执行有副作用的动作。

本卡用“工具描述→结构化调用→参数校验→权限判定→执行→结构化结果”建立可测试边界。

## 2. 为什么它重要？它有什么用？

- **连接大图景**：ReAct 的 Action 通过工具契约落地；多 Agent 也常把对方能力包装成工具。
- **实际应用场景**：数据库查询、计算器、文件读写、订单操作、代码执行与检索。
- **高频题型/任务**：设计 schema、校验参数、区分纯函数与副作用、处理超时与幂等性。

## 3. 学它之前需要哪些前置知识？

1. **[[02-Knowledge/🧠 学习系统/08-NLP全栈/01-基础准备/08-NLP全栈-Python编程与NLP工具|Python 编程与工具]]**：理解参数、返回值、异常和纯函数。
2. **[[AI-Agent-边界与感知行动循环]]**：工具结果会成为下一轮观察。

## 4. 用直觉语言解释它

> “这东西其实就像医院检验申请单：医生可以选择检验，但必须填对项目、样本和患者；检验科按标准单执行并返回结构化结果。”

- **直觉类比**：工具 schema 是插座标准，不负责决定用哪台电器，却阻止错误接线。
- **为什么很自然**：把开放语言压缩成有限动作与有限参数，系统才可验证。
- **一句话直觉本质**：让模型只能提出受约束的动作建议，由可信执行层校验后实施。

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义

工具 $k$ 是带有名称、语义描述、输入 schema $S_k$、输出 schema $O_k$、权限 $P_k$ 和副作用级别 $e_k$ 的可执行能力。调用 $c=(k,x)$ 只有同时满足结构、业务与权限约束才可执行。

### 2. 核心公式

$$Allow(c,u,s)=Valid_{S_k}(x)\land Policy(u,k,x,s)\land Budget(s)>0$$

$$result=Execute(k,x),\qquad Valid_{O_k}(result)=true$$

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $k$ | 工具名 | 白名单字符串 | 不接受任意代码名 |
| $x$ | 参数对象 | JSON-like 字典 | 先校验再执行 |
| $u$ | 调用主体 | 用户/Agent 身份 | 权限不能只靠 prompt |
| $e_k$ | 副作用等级 | read/write/destructive | 决定审批策略 |
| $result$ | 结构化结果 | success/data/error | 错误也是合法观察 |

### 4. 常见变体与适用条件

- **变体**：function calling、代码生成执行、MCP 工具、HTTP API wrapper。
- **限制条件**：代码执行比参数化工具自由度高，也更需要 sandbox、资源限额和网络隔离。

## 6. 推导思路和思想来源

- **最初困难**：让模型输出“请查北京天气”还需另一个脆弱解析器猜含义。
- **直接方法局限**：把整句拼接进 shell/SQL 会产生注入和不可预测副作用。
- **关键“转念”**：模型只选择工具与参数；可信程序负责 schema、授权、执行与结果包装。
- **推导主线与动机**：列能力→最小参数→约束→副作用分级→错误语义→测试。
- **为什么自然得到此结论**：软件工程早已用类型与接口隔离组件；Agent 工具是同一原则面对概率模型的加强版。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

- **题目**：`score_review(food, service)` 要求两个评分均为 1–5。输入 `(4, 6)` 能执行吗？若规则是几何平均，合法 `(4, 5)` 的分数是多少？
- **解题思路与关键步骤**：6 超界，第一组拒绝；合法组分数 $\sqrt{4\times5}=\sqrt{20}\approx4.472$。
- **最终答案**：第一组不能执行；第二组约 4.472。
- **易错点**：先执行再修正；把模型“保证参数合法”当校验。
- **🤔 追问**：评分写成字符串 `"5"` 应自动转换还是拒绝？依据是什么？

### 例子 2：中等例子（条件判断与多步推理）

`get_reviews` 是只读且可重试；`refund_order` 有资金副作用，必须有订单归属校验、金额上限、幂等键和人工审批。两者不能因为都叫“工具”而使用同一策略。

### 例子 3：实际应用例子（真实场景/代码）

输入两个评分，注册表负责名称白名单、参数集合和范围校验；输出 `{'ok': True, 'data': 4.472}`。

```python
from math import sqrt
from typing import Callable

def score_review(food: int, service: int) -> float:
    if not all(isinstance(value, int) and 1 <= value <= 5 for value in (food, service)):
        raise ValueError("ratings must be integers from 1 to 5")
    return round(sqrt(food * service), 3)

TOOLS: dict[str, Callable[..., object]] = {"score_review": score_review}

def execute(call: dict[str, object]) -> dict[str, object]:
    name = call.get("name")
    arguments = call.get("arguments")
    if name not in TOOLS or not isinstance(arguments, dict):
        return {"ok": False, "error": "invalid tool call"}
    if set(arguments) != {"food", "service"}:
        return {"ok": False, "error": "unexpected arguments"}
    try:
        return {"ok": True, "data": TOOLS[name](**arguments)}
    except (TypeError, ValueError) as error:
        return {"ok": False, "error": str(error)}

print(execute({"name": "score_review", "arguments": {"food": 4, "service": 5}}))
```

本课程的可运行版本位于 `03-Projects/46-AI Agent工程/scripts/agent_runtime.py`。其中 `ToolSpec` 同时声明参数名、参数类型和返回值验证器；`ToolRegistry` 在调用 handler 前后分别校验输入与输出。`HttpDecisionModel` 只接受 HTTPS（本机回环测试可显式放宽），拒绝重定向、非 JSON 响应、超限响应和错误的 `action/tool` 类型。这样把“模型选择动作”与“控制面是否允许执行”分成两个独立可测边界。

## 8. 常见误区和易混概念

### 误区 1：schema 校验等于安全

- **错误直觉**：类型正确就可以执行。
- **为什么错**：合法整数仍可能越权退款；合法 URL 仍可能访问内网。
- **正确理解**：schema、业务规则、身份权限、资源预算和结果校验缺一不可。

### 误区 2：工具错误应隐藏

- **错误直觉**：报错会干扰模型，应只返回空结果。
- **为什么错**：空结果掩盖失败，Agent 会基于错误假设继续。
- **正确理解**：返回稳定错误码与可行动信息，不泄露敏感堆栈。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| 参数化工具 | 调哪个受限能力？ | 白名单、schema、可审计 | 业务 API、检索 |
| 代码执行 | 生成任意程序做什么？ | 表达力高、风险高 | 数据分析、修复 |
| 结构化输出 | 模型输出长什么样？ | 可能不执行副作用 | 抽取、分类 |
| 普通文本指令 | 想表达什么？ | 歧义最大、最难校验 | 低风险写作 |

## 9. 来源定位与关系

- API 设计与工具调用都强调稳定契约、错误码和版本控制；缺少系统 API 设计基础时，将其作为语义补救主题，不伪造计划性链接。
- 直接知识依赖以 frontmatter `upstream` 为唯一事实源；直接后续由本文末 Dataview 反向派生。

## 10. 闭卷复现任务

- [ ] 1. 定义一个工具的六项元数据。
- [ ] 2. 写出 `Allow` 公式。
- [ ] 3. 区分 schema 与业务校验。
- [ ] 4. 解释副作用分级。
- [ ] 5. 为只读查询设计错误返回。
- [ ] 6. 为退款动作设计审批门。
- [ ] 7. 手算几何平均评分。
- [ ] 8. 说出代码执行的三项隔离要求。
- [ ] 9. 给工具调用设计四个测试。
- [ ] 10. 解释为什么工具观察不应包含敏感堆栈。

## 11. 自测题：5 道

### 1. #自测题/基础
**题目**：工具调用最少要校验哪两层？
> [!question]- 答案解析
> - **答案**：结构/schema 合法性和业务/权限合法性。
> - **解析**：类型正确不代表主体有权执行。

### 2. #自测题/基础
**题目**：未知工具名应如何处理？
> [!question]- 答案解析
> - **答案**：拒绝并返回稳定错误，不动态导入或执行同名代码。
> - **解析**：工具名必须来自注册白名单。

### 3. #自测题/中等
**题目**：为什么写操作需要幂等键？
> [!question]- 答案解析
> - **答案**：网络重试或 Agent 重复调用时，幂等键防止同一业务动作执行多次。
> - **解析**：尤其适用于付款、退款、发信等副作用。

### 4. #自测题/中等
**题目**：`{"amount": 10}` 通过 JSON schema 后为何仍可能被拒绝？
> [!question]- 答案解析
> - **答案**：用户可能无权限、订单不属于用户、余额不足或操作超预算。
> - **解析**：schema 只回答形状，不回答业务授权。

### 5. #自测题/较难
**题目**：设计一个安全网页抓取工具的最小限制。
> [!question]- 答案解析
> - **答案**：协议/域名白名单，禁止私网与重定向绕过，响应大小和超时限制，内容类型检查，去除凭据，输出按不可信数据处理并记录审计。
> - **解析**：同时控制 SSRF、资源耗尽、数据泄漏和间接注入。

## 12. 我的主动回忆区

### 我的闭卷复述
> 解释“模型提议、执行层裁决”：

### 我的推导复现
> 为一个真实工具写输入/输出/错误契约：

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/46-AI Agent工程/`
- **关联已有笔记**：[[AI-Agent-ReAct推理行动范式]]、[[AI-Agent-安全威胁建模与系统评测]]
- **建议标签**：`#学习` `#工具调用` `#结构化契约`
- **拆分建议**：MCP/A2A 只在形成独立协议实验时另建卡。

## 🔗 直接后续（派生）

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/46-AI Agent工程"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

## 🧪 学完本节后可完成的作业

```dataview
LIST
FROM "03-Projects/46-AI Agent工程"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 🃏 Anki 卡片

- 安全工具调用的完整判定链是什么？::工具白名单、输入 schema、业务规则、身份权限、资源预算、执行隔离以及输出 schema 都通过后才允许执行。
- 为什么 schema 校验不等于授权？::schema 只验证数据形状和类型，不能证明调用者有权对具体资源执行该动作。
- 为什么写操作需要幂等键？::防止超时重试或 Agent 重复决策导致付款、退款、发信等副作用重复发生。

