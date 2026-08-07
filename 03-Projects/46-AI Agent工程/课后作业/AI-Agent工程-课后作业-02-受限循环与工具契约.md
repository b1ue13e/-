---
type: project
project_type: homework
topic: "受限循环与工具契约"
course: "AI Agent工程"
assignment_id: "AI-Agent工程-L02"
assignment_level: lesson
assignment_format: lab
stage_id: "01"
requires: ["[[AI-Agent-边界与感知行动循环]]", "[[AI-Agent-ReAct推理行动范式]]", "[[AI-Agent-工具调用与结构化契约]]"]
source_type: local_integration_task
source: "课程原创任务；对齐 Microsoft Lessons 1/3/4 与 Hello-Agents Chapters 1/4/7"
source_url: "https://github.com/microsoft/ai-agents-for-beginners/tree/main/04-tool-use"
accessed: 2026-08-06
license: "任务文本原创；Microsoft MIT；Hello-Agents CC BY-NC-SA 4.0"
assignment_id: "AI-Agent工程-L02"
assignment_level: lesson
assignment_format: lab
stage_id: "01"
requires: ["[[AI-Agent-边界与感知行动循环]]", "[[AI-Agent-ReAct推理行动范式]]", "[[AI-Agent-工具调用与结构化契约]]"]
source_type: local_integration_task
source: "课程原创任务；对齐 Microsoft Lessons 1/3/4 与 Hello-Agents Chapters 1/4/7"
source_url: "https://github.com/microsoft/ai-agents-for-beginners/tree/main/04-tool-use"
accessed: 2026-08-06
license: "任务文本原创；Microsoft MIT；Hello-Agents CC BY-NC-SA 4.0"
created: 2026-08-06
status: planned
flow: project
tags: [作业, 46-AI Agent工程, ReAct, 工具契约]
---

# AI Agent 工程课后作业 02：受限循环与工具契约

## 🎯 学习目标

1. **结构化契约与类型约束**：学会使用 Python `dataclass` 或类型注解定义严格的 Agent 工具 Schema（包含参数校验、返回格式、只读/写权限标记与错误枚举）。
2. **感知-行动受限循环**：实现一个包含步数上限（Max Steps）、状态轨迹追踪（Observation Trajectory）与未知动作安全熔断（Failsafe Termination）的离线 Agent 循环机制。
3. **故障分类与鲁棒处置**：对未知城市、重复动作、未知工具调用、非法参数类型及预算耗尽（Budget Exhaustion）建立明确的错误类型区分与优雅终止策略。
4. **架构权衡与基线对比**：编写一个确定性（Deterministic）非 Agent 条件分支工作流作为对比基线，定量评估 Agent 范式在动态调度上的灵活性与额外 Token/延迟开销。

---

## 🚧 任务背景与边界

在实际 Agent 系统开发中，无限制的模型推理循环极易陷入死循环、无限重试或非预期工具提权。本实验设定的背景为**离线城市温度查询与比较场景**。模型输入由预置决策替身（Mock LLM Persona / Deterministic ReAct Script）提供动作决策，工具端只能读取内置静态字典中的离线数据集，严禁发起真实 HTTP 网络请求或使用真实模型 API 密钥。

**边界与假设**：
- **最大步数限制**：硬性限制 $N_{\max} = 3$ 步。达到 3 步未得出结论必须强制停止并返回状态 `BUDGET_EXHAUSTED`。
- **状态轨迹记录**：每次循环必须精确记录 `(step_idx, action_name, action_args, observation, status_code)`。
- **作用域隔离**：工具仅具备只读权限（Read-only），尝试写入或操作未授权资源时触发 `PERMISSION_DENIED` 异常。

---

## 📝 详细题目与步骤

### 1. 结构化工具定义 (`get_temperature`)
在 `src/tools.py` 中定义城市温度查询工具：
- **Schema**：接收字符串 `city`（支持 `"Beijing"`, `"Shanghai"`, `"Guangzhou"`）。
- **返回值**：成功时返回 JSON 字典 `{"city": str, "temperature_celsius": float, "status": "SUCCESS"}`；传参不存在时返回 `{"error": "UNKNOWN_CITY", "status": "FAILED"}`。
- **权限标记**：在工具装饰器或类属性中明确标记 `permission="READ_ONLY"`。

### 2. 手算推导与追踪轨迹
请在提交报告中手工书写并列出以下追踪轨迹（Formatting Checklist）：
- 目标：比较北京与上海的摄氏温度。
- **Step 1**：`Action: get_temperature(city="Beijing")` $\rightarrow$ `Observation: {"city": "Beijing", "temperature_celsius": 20.0}`
- **Step 2**：`Action: get_temperature(city="Shanghai")` $\rightarrow$ `Observation: {"city": "Shanghai", "temperature_celsius": 24.0}`
- **Step 3**：推理得出结论 `"Shanghai is warmer by 4°C"` $\rightarrow$ `Status: FINISHED`。

### 3. 受限 Agent 循环实现 (`LimitedAgentLoop`)
在 `src/limited_agent.py` 中实现 Agent 循环主体类 `LimitedAgentLoop`：
```python
class LimitedAgentLoop:
    def __init__(self, tools_registry: dict, max_steps: int = 3):
        ...
    def run(self, goal: str, action_provider: Callable) -> AgentRunResult:
        ...
```
必须实现以下故障拦截逻辑：
- **未知工具调用**：若 action_provider 返回不存在的工具名，拦截并记录 `UNKNOWN_TOOL`，终止循环。
- **重复动作检测**：若连续两次请求相同的 `(tool_name, args_hash)`，触发 `REPEATED_ACTION_STOP` 熔断。
- **非法参数类型**：对非字符串或注入格式参数直接返回 `INVALID_ARGUMENT`。

### 4. 确定性工作流基线与对比
编写 `src/baseline_workflow.py`：不依赖模型决策，直接顺序调用工具并对比温度。编写对比报告说明：
- 确定性工作流的执行延迟（延迟约 0ms，开销 0 Token）。
- Agent 范式在大规模工具选型与非结构化输入解析上的扩展性优势。

---

## 🛠️ 环境与复现

- **运行环境**：Python 3.11+ 标准库（仅使用 `unittest`, `json`, `dataclasses`, `typing`），不需要安装外部第三方依赖。
- **测试命令**：
  ```bash
  python -m unittest discover -s tests -v
  ```
- **可重复性保障**：设定随机种子为 `0`，预置替身动作以固定 List 结构返回，保证单元测试每次执行输出 100% 确定。

---

## 📦 提交产物清单

1. `src/tools.py`：包含 `get_temperature` 及类型定义。
2. `src/limited_agent.py`：包含 `LimitedAgentLoop` 与故障处理枚举。
3. `src/baseline_workflow.py`：确定性对比基线实现。
4. `tests/test_limited_agent.py`：包含正常完成、重复动作熔断、未知工具拦截、超出步数限制等 6 个单元测试。
5. `docs/trace_and_analysis.md`：包含手算轨迹表与 Agent/固定工作流选型分析。

---

## 📏 验收标准与 Rubric

| 评估维度 | 分值 | 验收标准与扣分细则 |
| :--- | :---: | :--- |
| ** Schema 与契约** | 25分 | 必须包含显式类型声明与只读标记。缺少只读标记扣 10 分；未进行参数校验扣 10 分。 |
| **受限循环控制** | 30分 | 严格在 $\le 3$ 步内完成。超过 3 步未停止直接判定为 0 分；轨迹未能精确记录步数扣 10 分。 |
| **故障防护与熔断** | 30分 | 对未知工具、未知城市、重复动作及参数错误有独立枚举状态。缺一种拦截策略扣 8 分。 |
| **基线与选型分析** | 15分 | 包含完整基线代码与开销对比报告。缺少基线比较扣 10 分。 |

---

## 💡 引导与自检

- **自检点 1**：工具是否写成了纯函数（Pure Function）？工具内部不得保留任何跨调用共享的状态。
- **自检点 2**：故意在测试中传入 `city="InvalidCity"` 或 `action="delete_database"`，观察循环是否在 1 步内捕获错误并优雅退出。
- **后续衔接**：完成本作业后，请进入阶段综合实践 [[AI-Agent工程-阶段作业-01-有限ReAct工具台]]。
