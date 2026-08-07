---
type: project
project_type: homework
topic: "协议边界与沙箱执行"
course: "AI Agent工程"
assignment_id: "AI-Agent工程-S04"
assignment_level: stage
assignment_format: lab
stage_id: "04"
requires: ["[[AI-Agent-多智能体协作与消息协议]]", "[[AI-Agent-协议-MCP与A2A互操作]]", "[[AI-Agent-安全威胁建模与系统评测]]", "[[AI-Agent-环境交互-代码网页与沙箱执行]]"]
source_type: local_integration_task
source: "课程原创任务；概念对齐官方 MCP/A2A 规范与 Microsoft Lessons 8/11/15"
source_url: "https://modelcontextprotocol.io/docs/learn/architecture"
accessed: 2026-08-06
license: "任务文本原创；协议与课程材料按各自许可；实现为本地模拟而非官方SDK兼容声明"
assignment_id: "AI-Agent工程-S04"
assignment_level: stage
assignment_format: lab
stage_id: "04"
requires: ["[[AI-Agent-多智能体协作与消息协议]]", "[[AI-Agent-协议-MCP与A2A互操作]]", "[[AI-Agent-安全威胁建模与系统评测]]", "[[AI-Agent-环境交互-代码网页与沙箱执行]]"]
source_type: local_integration_task
source: "课程原创任务；概念对齐官方 MCP/A2A 规范与 Microsoft Lessons 8/11/15"
source_url: "https://modelcontextprotocol.io/docs/learn/architecture"
accessed: 2026-08-06
license: "任务文本原创；协议与课程材料按各自许可；实现为本地模拟而非官方SDK兼容声明"
created: 2026-08-06
status: planned
flow: project
tags: [作业, 阶段作业, 46-AI Agent工程, MCP, A2A, 沙箱]
---

# AI Agent 工程阶段作业 04：协议边界与沙箱执行

## 🎯 学习目标

1. **MCP (Model Context Protocol) 概念模拟**：实现主机（Host）与工具服务器（Tool Server）间的能力发现（Capability Discovery）、工具列表注册与只读 JSON-RPC 消息交互。
2. **A2A (Agent-to-Agent) 任务生命周期管理**：设计包含 `SUBMITTED`, `WORKING`, `INPUT_REQUIRED`, `COMPLETED`, `FAILED`, `CANCELED` 状态的远程任务委托协议。
3. **沙箱文件路径规范化与隔离**：强制对 Agent 请求的文件路径进行 `os.path.realpath` 规范化校验，防止路径穿越攻击（Path Traversal, e.g. `../../etc/passwd`）。
4. **审批绑定与安全协议屏障**：确保任何涉及文件修改或外部写操作的动作必须通过生成包含 `action_digest` 与 `nonce` 的收据进行二次确认。

---

## 🚧 任务背景与边界

随着 Agent 接入外部工具与多 Agent 协作，系统边界急剧扩大。本阶段作业要求在**本地模拟 MCP 只读工具与 A2A 长任务委托框架**。

**边界与假设**：
- **概念模拟声明**：本实验代码仅用于核心安全协议逻辑验证，不得宣称与官方 MCP 或 A2A Python SDK 100% 字节级兼容。
- **沙箱根目录隔离**：所有写操作限制在 `tmp/sandbox/` 目录下。任何超出该目录的写请求必须立即抛出 `PATH_OUT_OF_SANDBOX` 异常。
- **网络域名白名单**：URL 请求仅允许命中的 Allowlist 域名（如 `https://api.github.com`），禁止内网 IP (如 `127.0.0.1`, `169.254.169.254`)。

---

## 📝 详细题目与里程碑

### 里程碑 1 (M1)：四方信任威胁建模 (`docs/threat_model.md`)
绘制包含 Host、Tool Server、Remote Agent 及 End User 的四方信任边界图，列出主要风险点：
- **Prompt 注入提权**：Remote Agent 试图篡改 Host 传递的敏感参数。
- **越界路径读取**：Tool Server 试图读取沙箱外的系统配置文件。
- **重放与无休止重试**：恶意请求通过重复 `nonce` 触发大量计算开销。

### 里程碑 2 (M2)：MCP-like 工具服务器与沙箱隔离 (`src/mcp_server.py`)
实现 `search_notes` 只读工具与 `write_sandbox_file` 沙箱写工具：
```python
def write_sandbox_file(rel_path: str, content: str, sandbox_root: Path) -> dict:
    target_path = (sandbox_root / rel_path).resolve()
    if not str(target_path).startswith(str(sandbox_root.resolve())):
        raise PermissionError("PATH_OUT_OF_SANDBOX")
    ...
```

### 里程碑 3 (M3)：A2A-like 任务委托与生命周期状态机 (`src/a2a_dispatcher.py`)
实现 `TaskDispatcher` 类，管理远程代理 `writer_agent` 的执行生命周期：
```python
class TaskState(Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input_required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
```
实现 `cancel_task(task_id)` 与超时自动取消逻辑。

### 里程碑 4 (M4)：故障注入与协议漏洞测试 (`tests/test_protocol_security.py`)
编写至少 12 个针对以下攻击场景的自动化测试：
1. **路径穿越**：传入 `rel_path = "../../../system.ini"` 被成功拦截。
2. **SSRF 内网请求**：传入 `url = "http://169.254.169.254/latest/meta-data"` 被白名单拦截。
3. **未授权发布**：跳过 `approval_digest` 直接发布生成内容被阻断。
4. **任务取消重放**：对已取消的 `CANCELED` 任务再次发送更新指令被拒绝。

---

## 🛠️ 环境与复现

- **运行环境**：Python 3.11+ 标准库，固定测试临时目录 `tmp/sandbox/`。
- **测试命令**：
  ```bash
  python -m unittest discover -s tests -v
  ```
- **清理逻辑**：单元测试的 `tearDown` 方法中必须自动清理生成的临时沙箱文件。

---

## 📦 提交产物清单

1. `src/mcp_server.py`：MCP 只读工具与沙箱写入工具。
2. `src/a2a_dispatcher.py`：A2A 任务调度器与状态机。
3. `tests/test_protocol_security.py`：包含 12+ 个协议安全与沙箱隔离测试用例。
4. `docs/threat_model.md`：四方信任边界与威胁模型报告。
5. `output/approval_receipt_sample.json`：生成的合规审批收据示例。

---

## 📏 验收标准与 Rubric

| 评估维度 | 分值 | 验收标准与扣分细则 |
| :--- | :---: | :--- |
| **四方信任与威胁建模** | 20分 | 边界清晰，准确识别 SSRF、路径穿越与提权风险。扣分项：缺少威胁模型扣 10 分。 |
| **消息协议与生命周期** | 25分 | 完整实现 A2A 六种状态枚举与状态转移逻辑。状态缺失扣 10 分。 |
| **沙箱隔离与审批绑定** | 30分 | 路径规范化 100% 拦截沙箱越界写入，审批收据防篡改。越界写入判定为 0 分。 |
| **故障注入与安全测试** | 20分 | 覆盖 4 类主要攻击测试且全数通过。每缺一类扣 5 分。 |
| **协议诚实性** | 5分 | 明确声明为本地概念模拟而非官方 SDK 兼容。未声明扣 5 分。 |

---

## 💡 引导与自检

- **自检点 1**：路径校验是否在 `resolve()` 之后进行？未经过 `resolve()` 解析符号链接的路径判定极其容易被 bypass。
- **自检点 2**：A2A 任务取消后，后端的异步执行流程是否会立刻中断并释放锁资源？
- **后续衔接**：通过本阶段项目后，请进入阶段五 [[🧭 阶段5-评测与生产运行]]。
