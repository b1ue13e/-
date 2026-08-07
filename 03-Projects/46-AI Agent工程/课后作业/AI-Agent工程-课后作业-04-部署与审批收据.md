---
type: project
project_type: homework
topic: "部署与审批收据"
course: "AI Agent工程"
assignment_id: "AI-Agent工程-L04"
assignment_level: lesson
assignment_format: lab
stage_id: "06"
requires: ["[[AI-Agent-部署与本地运行-伸缩路由烟测]]", "[[AI-Agent-安全审计-加密收据与审批绑定]]"]
source_type: local_integration_task
source: "课程原创任务；对齐 Microsoft Lessons 16-18"
source_url: "https://github.com/microsoft/ai-agents-for-beginners/tree/main/18-securing-ai-agents"
accessed: 2026-08-06
license: "任务文本原创；Microsoft MIT"
created: 2026-08-06
created: 2026-08-06
status: planned
flow: project
tags: [作业, 46-AI Agent工程, 部署, 收据, 审批]
---

# AI Agent 工程课后作业 04：部署与审批收据

## 🎯 学习目标

1. **多级部署门禁机制**：区分服务存活（Liveness）、就绪检查（Readiness）、离线评估（Offline Eval）与灰度门禁（Canary Gate），建立渐进式发布流程。
2. **结构化动作审批收据 (Action Receipt)**：掌握在 Agent 试图执行写操作（如写数据库、发送邮件、发布代码）前生成包含动作摘要与审批绑定的规范收据格式。
3. **加密完整性与防重放校验**：使用 Python 标准库 `hmac` 与 `hashlib` 计算 SHA-256 哈希值，防止入参篡改、时效过期（Expiration）与重放攻击（Replay Attack）。
4. **离线安全熔断策略**：在缺乏有效签名收据或任何一门部署检查失败时，确保系统强制阻断敏感动作执行。

---

## 🚧 任务背景与边界

在将 AI Agent 部署到生产环境时，绝对不能将控制权无条件交给模型直接写入真实系统。本实验采用离线模拟发布报告场景，不连接任何真实云服务 API、外部数据库或支付网关。

**边界与假设**：
- **哈希与签名模拟**：加密部分使用 HMAC-SHA256 示范规范化与摘要计算。此实现用于原理校验，真实生产环境必须替换为基于非对称密钥对（如 Ed25519 或 RSA-2048）的数字签名库。
- **收据过期时限**：收据默认 TTL 为 $T_{\exp} = 300$ 秒，超期直接认定为无效收据。
- **不可否认性**：收据必须与具体 `action_name` 和 `args_digest` 强关联，防止参数偷换。

---

## 📝 详细题目与步骤

### 1. 部署门禁四级检查定义 (`deployment_gates.py`)
实现四种独立评估方法：
```python
class DeploymentGate:
    def check_smoke(self) -> bool: ...     # 1. 语法/服务存活烟测
    def check_readiness(self) -> bool: ... # 2. 依赖/模型权重加载就绪
    def check_eval_pass(self) -> bool: ... # 3. 离线 Eval 准确率 ≥ 85%
    def check_canary_gate(self) -> bool: ...# 4. 灰度小流量告警率 < 0.1%
```
任一检查返回 `False` 时，整个门禁状态返回 `GATE_REJECTED`。

### 2. 规范化动作收据 (`action_receipt.py`)
定义 `CanonicalReceipt` 数据结构：
```python
@dataclass
class CanonicalReceipt:
    request_id: str
    action: str
    args_digest: str        # sha256(json.dumps(args, sort_keys=True))
    approval_digest: str    # hmac_sha256(secret_key, request_id + action + args_digest)
    nonce: str
    expires_at: int         # unix timestamp
    result_digest: str = ""
```
编写生成函数 `create_receipt(...)` 与验证函数 `verify_receipt(...)`。

### 3. 重放攻击与篡改测试 (`test_security.py`)
在单元测试中模拟三类真实攻击：
- **参数偷换**：保留原始 `approval_digest`，但将 `args` 中的目标金额从 `$10` 修改为 `$10000`，断言 `verify_receipt` 返回 `INVALID_DIGEST`。
- **过期收据**：传入 `expires_at = current_time - 10` 的收据，断言返回 `EXPIRED_RECEIPT`。
- **重放攻击**：使用相同的 `nonce` 连续二次请求，断言第二次拦截返回 `REPLAY_ATTACK_DETECTED`。

### 4. 串接部署门与审批收据 (`deployment_pipeline.py`)
实现 `execute_agent_action(gate: DeploymentGate, receipt: CanonicalReceipt)`：
- 依次校验 4 类门禁检查。
- 校验 `receipt` 有效性。
- 两者均通过方可输出 `ACTION_SUCCESS`，否则输出 `EXECUTION_BLOCKED`。

---

## 🛠️ 环境与复现

- **运行环境**：Python 3.11+ 标准库（仅使用 `unittest`, `hmac`, `hashlib`, `time`, `json`）。
- **测试命令**：
  ```bash
  python -m unittest discover -s tests -v
  ```
- **时钟替身 (Clock Mock)**：测试中使用 Mock 时间戳（如 `current_time = 1700000000`），避免依赖系统时间差异导致测试不稳定。

---

## 📦 提交产物清单

1. `src/deployment_gates.py`：四类部署检查逻辑。
2. `src/action_receipt.py`：HMAC 收据生成与验证器。
3. `src/deployment_pipeline.py`：门禁与收据串接工作流。
4. `tests/test_security.py`：包含篡改、过期、重放攻击拦截与门禁拒接等 7 个测试用例。
5. `docs/security_boundary_notes.md`：签名机制与生产部署边界说明。

---

## 📏 验收标准与 Rubric

| 评估维度 | 分值 | 验收标准与扣分细则 |
| :--- | :---: | :--- |
| **部署门禁区分** | 25分 | 必须明确区分 4 类检查。未区分烟测与 Eval 直接扣 10 分。 |
| **动作审批绑定** | 35分 | 收据哈希必须绑定 `request_id + action + args_digest`。未绑定参数扣 15 分。 |
| **篡改与重放防护** | 25分 | 单元测试成功拦截参数篡改、过期与重复 nonce。缺任一防护扣 8 分。 |
| **边界与可扩展性** | 15分 | 明确区分 HMAC 演示与生产非对称签名。缺少说明扣 10 分。 |

---

## 💡 引导与自检

- **自检点 1**：签名的输入是否经过了 JSON `sort_keys=True` 规范化？未排序的 JSON 字符串在解析后顺序不一致会导致合法摘要校验失败。
- **自检点 2**：烟测通过是否能代表可以直接发布？烟测仅验证服务未崩溃，不能替代离线 Eval 评估。
- **后续衔接**：本课后作业可选做 [[AI-Agent工程-课后作业-05-Agentic-RL奖励投机审计]]，核心主线请进入课程 Capstone 大作业 [[AI-Agent工程-大作业-受限可恢复Agent]]。
