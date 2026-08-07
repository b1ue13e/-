---
type: study
topic: "AI Agent边界与感知行动循环"
course: "AI Agent工程"
tags: [学习, 46-AI Agent工程, AI-Agent, Agent循环]
created: 2026-08-05
status: completed
difficulty: beginner
concept: [AI Agent, 感知行动循环, 自主性]
prerequisites: [Python编程与NLP工具, Prompt工程-需求-任务规格与结构化输出]
related: [ReAct, 工具调用, 工作流编排]
stage_moc: "[[🧭 阶段1-Agent基础与受限循环]]"
upstream: ["[[AI-Agent-前置-消息JSON异常与单元测试]]"]
flow: knowledge
kind: concept
assessment_exempt: false
source: "UC Berkeley CS 194/294-196 F24 overview; Microsoft AI Agents for Beginners Lessons 1 and 3; Datawhale Hello-Agents Chapters 1-2; Hugging Face Agents Course Unit 1"
source_urls: ["https://github.com/microsoft/ai-agents-for-beginners/tree/main/01-intro-to-ai-agents", "https://github.com/microsoft/ai-agents-for-beginners/tree/main/03-agentic-design-patterns", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter1", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter2"]
accessed: 2026-08-06
license: "Microsoft MIT；Hello-Agents CC BY-NC-SA 4.0；Berkeley许可待核验；本卡为原创整合"
anki_deck: "46-AI Agent工程::01-基础"
anki_tags: [46-AI-Agent工程, Agent循环, 基础]
---

# AI Agent：边界与感知—行动循环

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：如果把“一次生成”“固定流水线”和“会自主选择下一动作的系统”都叫 Agent，就无法判断成本、风险、测试方法和是否真的需要自主性。Agent 工程首先是边界工程。

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：一次模型调用只能根据当前上下文给出一次输出；真实任务往往需要观察环境、选择动作、读取结果、修正状态并判断是否停止。

本卡解决三个问题：什么是 Agent、一个最小 Agent 需要哪些部件、什么时候应退化为确定性工作流。

## 2. 为什么它重要？它有什么用？

- **连接大图景**：ReAct、工具调用、规划、记忆和多智能体都只是感知—行动循环的不同扩展。
- **实际应用场景**：检索问答、代码修复、数据分析、客服任务、网页操作和科研助手。
- **高频题型/任务**：识别系统是否具备 Agent 性；设计状态、动作、观察和终止条件；解释失控风险。

## 3. 学它之前需要哪些前置知识？

1. **[[08-NLP全栈/01-基础准备/NLP全栈-Python编程与NLP工具|Python 编程与工具]]**：动作最终要落到可调用函数；异常是环境反馈的一种。
2. **[[Prompt工程-需求-任务规格与结构化输出|Prompt 与消息规格]]**：模型通过消息读取目标、历史、工具结果和约束。

## 4. 用直觉语言解释它

> “这东西其实就像一个蒙眼找钥匙的人：每走一步都要摸一摸环境，再决定下一步；不能只在起点写完全部动作。”

- **直觉类比**：恒温器读取温度再开关空调，是最简单的闭环；LLM Agent 把策略换成了可处理语言的模型。
- **为什么很自然**：当动作结果不可提前确定时，系统必须依据新观察重新决策。
- **一句话直觉本质**：Agent 是在目标约束下，基于状态反复选择动作并吸收环境反馈的闭环系统。

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义

在离散步 $t$，Agent 根据目标 $g$、内部状态 $s_t$ 与观察 $o_t$，由策略 $\pi$ 选择动作 $a_t$；环境返回新观察，状态更新函数 $f$ 形成下一状态，直至满足终止条件 $T$。

### 2. 核心公式

$$a_t = \pi(g, s_t, o_t),\qquad o_{t+1}=E(a_t),\qquad s_{t+1}=f(s_t,a_t,o_{t+1})$$

工程上还应约束总效用：

$$J=\mathbb{E}[R]-\lambda_c C-\lambda_r Risk$$

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $g$ | 任务目标 | 文本或结构化规格 | 应含完成标准 |
| $s_t$ | 内部状态 | 消息、变量、计划 | 不等于全部历史原文 |
| $o_t$ | 环境观察 | 工具结果/错误 | 必须视为可能不可信 |
| $a_t$ | 动作 | 工具调用/回答/停止 | 应来自允许动作集合 |
| $R,C,Risk$ | 收益、成本、风险 | 可比较的指标 | 不能只优化正确率 |

### 4. 常见变体与适用条件

- **适用条件**：下一步依赖前一步结果；环境有不确定性；允许多轮试错。
- **限制条件**：高风险不可逆动作、规则完全确定或低延迟批处理，优先确定性代码与人工审批。

## 6. 推导思路和思想来源

- **最初困难**：把整个开放任务塞进一次 prompt，模型无法访问新信息，也无法验证动作结果。
- **直接方法局限**：预先列完步骤是假设环境完全可预测；实际工具会报错、数据会缺失。
- **关键“转念”**：不要求模型一次“想完”，而是把决策限制成一次选择，再把真实结果送回。
- **推导主线与动机**：目标→状态→允许动作→执行→观察→状态更新→终止。
- **为什么自然得到此结论**：任何反馈控制系统都要闭环；语言模型只是策略的一种实现。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

- **题目**：Agent 最多走 4 步，每步成本 2，完成得 15 分，失败得 0。它在第 3 步完成，效用是多少？若第 5 步才可能完成，应否继续？
- **解题思路与关键步骤**：前三步成本 $3\times2=6$，效用 $15-6=9$；第 5 步超过步数预算，必须在第 4 步停止，而非继续追求答案。
- **最终答案**：9；不应继续。
- **易错点**：只写成功奖励，不把 token、时间和风险计入停止决策。
- **🤔 追问**：若每次危险工具动作另有风险罚分 6，策略应如何调整？

### 例子 2：中等例子（条件判断与多步推理）

天气查询只需“解析城市→查 API→格式化”，且无分支探索，用工作流即可；旅行规划要根据预算、天气、库存反复修订，才适合受限 Agent。关键不是有没有 LLM，而是下一动作是否要依据观察动态选择。

### 例子 3：实际应用例子（真实场景/代码）

以下标准库程序让 Agent 通过猜测观察更新上下界。输入目标 `73`，输出会显示动作轨迹和完成状态。

```python
from dataclasses import dataclass, field

@dataclass
class SearchState:
    lower: int = 1
    upper: int = 100
    steps: int = 0
    trace: list[str] = field(default_factory=list)

def run_agent(target: int, max_steps: int = 7) -> SearchState:
    state = SearchState()
    while state.steps < max_steps:
        action = (state.lower + state.upper) // 2
        state.steps += 1
        if action == target:
            state.trace.append(f"guess={action}, observation=correct")
            return state
        if action < target:
            state.trace.append(f"guess={action}, observation=too low")
            state.lower = action + 1
        else:
            state.trace.append(f"guess={action}, observation=too high")
            state.upper = action - 1
    return state

result = run_agent(73)
print(result.trace)
print(result.trace[-1].endswith("correct"))
```

预期最后一行输出：`True`。

## 8. 常见误区和易混概念

### 误区 1：用了 LLM 就是 Agent

- **错误直觉**：智能来自模型，所以模型调用自动等于智能体。
- **为什么错**：没有状态、动作、观察和终止循环的一次调用只是生成组件。
- **正确理解**：Agent 是系统架构；LLM 只是策略、解析器或评估器。

### 误区 2：自主性越高越先进

- **错误直觉**：让模型自由决定所有步骤会更通用。
- **为什么错**：自由度同时扩大错误传播、权限和成本空间。
- **正确理解**：采用完成任务所需的最小自主性。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| Agent | 下一步应根据观察做什么？ | 动态策略与闭环 | 开放任务、工具探索 |
| 工作流 | 已知步骤如何稳定执行？ | 路径主要预定义 | ETL、审批、固定管线 |
| 聊天机器人 | 如何维持对话并回答？ | 可有对话状态但未必行动 | FAQ、写作助手 |
| 模型调用 | 这次输入生成什么？ | 单步、无环境闭环 | 分类、摘要、抽取 |

## 9. 来源定位与关系

- 外部语义前置：[[08-NLP全栈/01-基础准备/NLP全栈-Python编程与NLP工具|Python 编程与工具]]、[[Prompt工程-需求-任务规格与结构化输出|Prompt 与消息规格]]。
- 横向关联：[[🎯 阶段2：马尔可夫决策过程|马尔可夫决策过程]]同样使用状态、动作和转移描述序贯决策。
- 直接知识依赖以 frontmatter `upstream` 为唯一事实源；直接后续由本文末 Dataview 反向派生。

## 10. 闭卷复现任务

- [ ] 1. 用一句话区分 Agent 与一次 LLM 调用。
- [ ] 2. 画出目标、状态、动作、观察、状态更新和终止的闭环。
- [ ] 3. 写出 $a_t$ 与 $s_{t+1}$ 的公式。
- [ ] 4. 解释为什么环境观察不能默认可信。
- [ ] 5. 给出一个应使用确定性工作流而不是 Agent 的例子。
- [ ] 6. 说明最大步数、成本预算和权限白名单的作用。
- [ ] 7. 手算第 7 节效用题。
- [ ] 8. 说出两个“自主性过高”的风险。
- [ ] 9. 解释 LLM 在 Agent 中可承担的三个角色。
- [ ] 10. 用代码重建一个有终止条件的闭环。

## 11. 自测题：5 道

### 1. #自测题/基础
**题目**：固定执行 A→B→C，错误就退出，是 Agent 吗？
> [!question]- 答案解析
> - **答案**：通常是工作流，不是具有动态策略的 Agent。
> - **解析**：它有执行状态但路径预定义；除非 B 的观察会让系统在多个动作中自主选择。
> - **易错原因**：把“多步骤”误当成“自主决策”。

### 2. #自测题/基础
**题目**：写出最小循环的六个组成。
> [!question]- 答案解析
> - **答案**：目标、状态、策略、动作、环境观察、终止条件。
> - **解析**：状态更新连接相邻两轮，也应在实现中显式存在。

### 3. #自测题/中等
**题目**：为什么“回答正确率”不足以选择 Agent？
> [!question]- 答案解析
> - **答案**：还需衡量成本、延迟、风险、权限使用、稳定性和失败可恢复性。
> - **解析**：核心公式中的 $J$ 同时惩罚成本和风险。

### 4. #自测题/中等
**题目**：搜索 Agent 连续两次得到相同错误，应如何设计？
> [!question]- 答案解析
> - **答案**：记录失败签名，限制相同重试次数，改用备选动作或终止并上报。
> - **解析**：否则形成无效循环并浪费预算。

### 5. #自测题/较难
**题目**：为“自动退款 Agent”划定最小自主边界。
> [!question]- 答案解析
> - **答案**：可自主读取订单、核对规则、生成建议；金额超阈值、证据冲突或不可逆退款必须人工批准；所有工具最小权限并审计。
> - **解析**：依据动作可逆性、金额风险和证据质量分级，而不是全开或全关。

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释 Agent 为什么是系统而不是模型：

### 我的推导复现
> 写出状态转移公式，并标出一次工具报错出现在哪个变量：

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/46-AI Agent工程/`
- **关联已有笔记**：[[AI-Agent-ReAct推理行动范式]]、[[AI-Agent-规划状态与工作流编排]]
- **建议标签**：`#学习` `#AI-Agent` `#Agent循环`
- **拆分建议**：当前保持主题卡；若未来加入形式化 POMDP 推导，再拆 derivation 卡。

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

- AI Agent 的最小闭环是什么？::目标与状态进入策略，策略选择动作，环境返回观察，状态更新，直到终止条件成立。
- 何时应优先工作流而不是 Agent？::当步骤与分支可预先定义、风险较高或需要低成本高确定性时，优先确定性工作流。
- Agent 工程为什么强调最小自主性？::自主性扩大动作空间，也扩大错误传播、权限滥用、成本与不可预测性；只开放任务所需的最小自由度。

