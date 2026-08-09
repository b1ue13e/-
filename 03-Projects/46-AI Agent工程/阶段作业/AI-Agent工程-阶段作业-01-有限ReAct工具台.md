---
type: project
project_type: homework
topic: "有限ReAct工具台"
course: "AI Agent工程"
assignment_id: "AI-Agent工程-S01"
assignment_level: stage
assignment_format: lab
stage_id: "01"
requires: ["[[AI-Agent-前置-消息JSON异常与单元测试]]", "[[AI-Agent-边界与感知行动循环]]", "[[AI-Agent-ReAct推理行动范式]]", "[[AI-Agent-工具调用与结构化契约]]"]
source_type: local_integration_task
source: "课程原创综合任务；融合 Microsoft Lessons 1/3/4 与 Hello-Agents Chapters 1/4/7"
source_url: "https://github.com/microsoft/ai-agents-for-beginners/tree/main/04-tool-use"
accessed: 2026-08-08
license: "任务文本原创；Microsoft MIT；Hello-Agents CC BY-NC-SA 4.0"
created: 2026-08-06
status: planned
flow: project
tags: [作业, 阶段作业, 46-AI Agent工程, ReAct]
---

# AI Agent 工程阶段作业 01：有限 ReAct 工具台

## 🎯 学习目标

1. **ReAct (Reason + Act) 模式离线实现**：将 Thought、Action、Action Input 与 Observation 形成确定性的五步感知-行动循环（Decide $\rightarrow$ Validate $\rightarrow$ Execute $\rightarrow$ Observe $\rightarrow$ Terminate）。
2. **多工具注册与协议隔离**：设计支持多工具（天气查询 `get_weather` + 四则运算 `calculator`）注册与调度的 `ToolRegistry`，实现参数 Schema 严格校验与错误分类拦截。
3. **收敛与安全停止条件**：建立限制步数（Max Steps = 4）、限制工具错误上限（Max Tool Errors = 2）、限制本地超时（Max Time = 1.0s）及重复动作熔断的多重安全屏障。
4. **端到端测试与基线对照**：编写覆盖正常查询、除零错误、畸形 JSON 与未知工具调用的完整单元测试集，评估 Agent 与固定条件工作流（Hardcoded Workflow）的适用边界。

---

## 🚧 任务背景与边界

在阶段一的学习中，我们推导了 ReAct 范式的核心思想。本阶段作业要求手撕一个**离线“天气比较与温度计算”复合工具台**。模型端由预制决策表（Mock ReAct Policy）或结构化规则驱动，不允许发起真实网络 API 调用。

**边界与假设**：
- **资源限制**：单次任务循环最大步数 $N_{\max} = 4$；连续工具异常最大容忍次数 $E_{\max} = 2$。
- **作用域与权限**：只允许调用已注册工具，绝对禁止执行未授权代码（如 `eval()`）或访问本地文件系统。
- **结构化 Trace**：每一步必须向 `trace.jsonl` 中追加包含完整Thought、Action、Observation 及 Status 的结构化 JSON 行。

---

## 📝 详细题目与里程碑

### 里程碑 1 (M1)：工具契约与结构化 Schema (`src/tools.py`)
定义两个核心工具：
1. `get_weather(city: str)`：返回 `{"city": str, "temp_c": float, "status": "SUCCESS"}`。对未知城市返回 `UNKNOWN_CITY`。
2. `calculator(expression: str)`：仅支持安全算术表达式 `a + b`, `a - b`, `a * b`, `a / b`。当 $b=0$ 时返回 `DIVISION_BY_ZERO`。

### 里程碑 2 (M2)：ReAct 感知-行动受限循环 (`src/react_agent.py`)
实现 `ReActAgentHarness` 类：
```python
class ReActAgentHarness:
    def __init__(self, registry: ToolRegistry, max_steps: int = 4):
        ...
    def step(self, prompt: str) -> StepResult:
        ...
    def run_until_complete(self, goal: str) -> RunResult:
        ...
```
包含以下状态收敛判断：
- 当 Action 为 `Finish[final_answer]` 时，正常结束并输出 `STATUS_SUCCESS`。
- 若连续两次产生的 `Action(name, args)` 完全一致，触发 `REPEATED_ACTION_STOP` 熔断。

### 里程碑 3 (M3)：故障注入与鲁棒性校验
实现针对 6 类异常情况的确定性捕获与分类：
1. **未知工具**：Action 试图调用 `exec_command` $\rightarrow$ 拦截并记录 `TOOL_NOT_FOUND`。
2. **畸形 JSON**：Action Input 无法解析为合法 JSON $\rightarrow$ 拦截并记录 `MALFORMED_INPUT`。
3. **除零错误**：`calculator("10 / 0")` $\rightarrow$ 工具返回错误信息，Agent 捕获后记录 `TOOL_EXECUTION_ERROR`。
4. **字段缺失**：传参缺少 `city` 字段 $\rightarrow$ 拦截并记录 `MISSING_PARAM`。
5. **重复动作**：连续两次请求相同参数 $\rightarrow$ 触发无进展熔断 `NO_PROGRESS`。
6. **超出步数**：达到 4 步未完成 $\rightarrow$ 强制终止并返回 `MAX_STEPS_EXCEEDED`。

### 里程碑 4 (M4)：确定性工作流基线与对比报告 (`docs/agent_vs_workflow.md`)
编写 `src/baseline_workflow.py` 顺序执行逻辑，比较两者在：
- 失败定位难度（Trace 可读性）
- 逻辑分支扩展成本
- 单元测试覆概率等维度的异同。

---

## 任务分层

- **基础要求**：至少两个只读工具、有限 ReAct 循环、完整 trace 和正常/异常/预算耗尽测试。
- **必要提示**：先冻结工具 schema 与停止条件，再接入 action provider；先构建可重复的固定工作流基线。
- **常见错误**：把 thought 文本当授权、未知工具自动重试、终止只依赖模型输出某个词。
- **可选进阶**：使用本机 HTTP decision adapter 替换 fake model，并报告边界错误与延迟差异。

## 🛠️ 环境与复现

- **运行环境**：Python 3.11+ 标准库，不依赖外部第三方库。
- **测试命令**：
  ```bash
  python -m unittest discover -s tests -v
  ```
- **测试用例要求**：必须编写至少 12 个独立的单元测试，覆盖正常与所有 6 类故障注入场景。

---

## 📦 提交产物清单

1. `src/tools.py`：`get_weather` 与 `calculator` 工具实现。
2. `src/react_agent.py`：ReAct 循环与熔断状态机。
3. `src/baseline_workflow.py`：确定性条件分支对比基线。
4. `tests/test_react_agent.py`：包含 12+ 个单元测试用例。
5. `output/trace.jsonl`：导出的运行轨迹样本。
6. `docs/agent_vs_workflow.md`：对比分析与失败复盘报告。

---

## 📏 验收标准与 Rubric

| 评估维度 | 分值 | 验收标准与扣分细则 |
| :--- | :---: | :--- |
| ** Schema 与工具契约** | 20分 | 工具 Schema 严谨，禁止使用危险 `eval()`。违规直接判定为 0 分。 |
| **ReAct 循环与终止** | 25分 | 严格按照步数限制与终止标记收敛。产生无限循环扣 25 分。 |
| **工具真实执行** | 20分 | 工具输入输出结构化且支持跟踪。缺失日志扣 10 分。 |
| **故障注入测试** | 25分 | 覆盖 6 类故障测试且全数通过。每缺一类测试扣 4 分。 |
| **对比分析与复盘** | 10分 | 包含详尽的基线比较与架构选型说明。缺少对比扣 8 分。 |

---

## 💡 引导与自检

- **自检点 1**：Action Input 的解析是否支持容错（如剥离 Markdown 代码块标志 ` ```json `）？
- **自检点 2**：`trace.jsonl` 是否可被 Python 内置 `json.loads()` 逐行流畅解析？
- **后续衔接**：通过本阶段验收后，请进入阶段二 [[🧭 阶段2-运行时规划与状态]]。
