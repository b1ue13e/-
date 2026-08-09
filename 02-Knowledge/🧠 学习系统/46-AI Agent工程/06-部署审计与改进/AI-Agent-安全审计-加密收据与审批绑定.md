---
type: study
topic: "AI Agent安全审计：加密收据与审批绑定"
course: "AI Agent工程"
tags: [学习, 46-AI Agent工程, AI-Agent, 加密收据, 审计]
created: 2026-08-06
status: completed
difficulty: advanced
concept: [加密收据, 防篡改审计, 审批绑定]
prerequisites: ["AI-Agent-安全威胁建模与系统评测", "AI-Agent-可观测性与生产运行-轨迹审批恢复"]
related: ["AI-Agent-工具调用与结构化契约", "AI-Agent-部署与本地运行-伸缩路由烟测"]
stage_moc: "[[🧭 阶段6-部署审计与改进]]"
upstream: ["[[AI-Agent-部署与本地运行-伸缩路由烟测]]", "[[AI-Agent-安全威胁建模与系统评测]]"]
flow: knowledge
kind: concept
source: "Microsoft AI Agents for Beginners Lesson 18; cryptographic implementation must follow current standards and reviewed libraries"
source_urls: ["https://github.com/microsoft/ai-agents-for-beginners/tree/main/18-securing-ai-agents"]
accessed: 2026-08-08
license: "Microsoft AI Agents for Beginners MIT；加密实现须另循生产库与标准许可"
anki_deck: "46-AI Agent工程::安全审计"
anki_tags: [加密收据, Ed25519, 哈希链, 审批]
---

# AI Agent 安全审计：加密收据与审批绑定

## 0. 学习边界

- **类别**：**B 类（高风险系统必学）**。
- **判断理由**：普通日志能被有权限的人改写。对付款、发布、删除、审批等动作，需要证明“这组字节由持有某密钥的一方签发，之后未被篡改”，并把人类批准绑定到确切动作。
- **边界**：加密收据证明完整性、来源和顺序，不证明输入事实真实、模型判断正确或动作合规。

## 1. 这个知识点解决什么问题？

> **麻烦**：事故后日志显示“用户批准了付款”，但无法确认批准的是不是这笔金额、日志是否被改过、步骤是否被删过、谁持有签名密钥。

加密收据把动作摘要、策略版本、审批摘要、上一个收据哈希等字段规范化后签名，使独立验证者能检测内容修改、身份伪造和链条断裂。

## 2. 为什么它重要？它有什么用？

- 高风险工具执行前后形成可独立验证的证据。
- 人类审批绑定到确切的工具、参数、资源、金额与过期时间。
- 多步 Agent 用哈希链发现步骤被删除、插入或重排。
- 跨服务审计时不必完全信任单一日志数据库。

## 3. 学它之前需要哪些前置知识？

1. [[AI-Agent-工具调用与结构化契约]]：需要稳定表示工具名和参数。
2. [[AI-Agent-安全威胁建模与系统评测]]：明确要防谁、保护什么、密钥边界在哪。
3. [[AI-Agent-可观测性与生产运行-轨迹审批恢复]]：收据补强 trace，不替代 trace。

## 4. 用直觉语言解释它

> “先把要执行的动作打印成格式唯一的合同，对合同指纹签名；下一张合同再写入上一张的指纹。”

格式唯一避免同一语义被编码成不同字节；数字签名让公钥验证者检查签发者；哈希链让顺序可查。

## 5. 正式定义、核心公式与字段

设规范化函数为 $J$，哈希为 $H$，私钥签名为 $Sign_{sk}$：

$$
d_i = H(J(receipt_i)), \qquad \sigma_i = Sign_{sk}(d_i)
$$

链式收据包含：

$$
receipt_i.previous\_hash = H(J(receipt_{i-1}) \parallel \sigma_{i-1})
$$

### 最小字段

| 字段 | 作用 |
| :--- | :--- |
| receipt_id / request_id | 关联一次执行与幂等键 |
| action / tool | 绑定具体能力 |
| args_digest | 绑定规范化后的准确参数，不在日志暴露敏感原文 |
| result_digest | 绑定结果或 artifact |
| policy/model/tool_version | 解释当时依据和运行版本 |
| approved_action_digest | 证明批准的正是该动作 |
| approver / expires_at / nonce | 防身份混淆、过期和重放 |
| previous_hash | 链接上一步 |
| signature / key_id | 供验证者选择公钥并验签 |

### 规范化为什么必要

JSON 的键顺序、空白、数字和 Unicode 表示可不同。生产互操作应采用明确规范，例如 RFC 8785 JCS，不能只说“把 JSON 转字符串”。

### 签名不等于加密

- **数字签名**：私钥签，公钥验；目标是来源与完整性。
- **加密**：控制谁能读；收据仍可能需要单独加密或只保存摘要。
- **HMAC**：双方共享密钥，适合封闭域完整性，不提供公钥式独立验证与不可否认性。

## 6. 从审批到验证的完整流程

1. 对高风险 action + args 做规范化并计算 `action_digest`。
2. 审批界面展示人类可理解的精确动作；批准结果包含 digest、审批者、过期时间、nonce。
3. 执行层重新计算 digest，常量时间比较，检查审批未过期且未使用。
4. 工具执行后生成 result/artifact digest。
5. 收据写入上一个收据哈希、版本与策略，使用受管私钥签名。
6. 独立验证者检查 schema、规范化、签名、key 状态、时间、nonce、approval digest 和链连续性。
7. 验证失败时拒绝把收据当可信证据；不能“记录警告后继续”。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：审批被偷换

用户批准 `transfer(amount=100, to=A)`。执行前参数变成 `amount=1000`。若批准只记录 `approved=true`，攻击可通过；若记录 `approved_action_digest`，重新计算会不一致并拒绝。

### 例子 2：链条被删除

收据 3 的 `previous_hash` 指向收据 2。删除收据 2 后，收据 3 无法接到收据 1；验证器发现断链。注意：若攻击者控制签名私钥，可重签整链，因此密钥管理仍是根边界。

### 例子 3：标准库完整性演示

```python
import hashlib
import hmac
import json

SECRET = b"demo-only-shared-secret"

def canonical_bytes(value: dict) -> bytes:
    # 教学用确定性 JSON，不宣称完整实现 RFC 8785 JCS。
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def sign_demo(receipt: dict) -> str:
    return hmac.new(SECRET, canonical_bytes(receipt), hashlib.sha256).hexdigest()

def verify_demo(receipt: dict, signature: str) -> bool:
    return hmac.compare_digest(sign_demo(receipt), signature)

action = {"tool": "transfer", "args": {"amount": 100, "to": "A"}}
receipt = {
    "request_id": "req-7",
    "action_digest": hashlib.sha256(canonical_bytes(action)).hexdigest(),
    "approved_action_digest": hashlib.sha256(canonical_bytes(action)).hexdigest(),
    "previous_hash": "GENESIS",
}
signature = sign_demo(receipt)
print(verify_demo(receipt, signature))
receipt["approved_action_digest"] = "tampered"
print(verify_demo(receipt, signature))
```

输出为 `True`、`False`。生产系统应使用经过审查的 Ed25519/JCS 实现和密钥管理服务；不要把演示 HMAC 当成跨组织签名方案。

课程运行时的 `ApprovalGate` 已实现封闭域 HMAC 收据：请求先冻结 `action/resource/parameters/nonce/issued_at/expires_at`，批准后返回签名 token；执行时重新验证签名、完整参数、时效和一次性 nonce。`SafeWorkspace` 把内容字节数与 SHA-256 纳入参数，因此“批准写 A 内容、执行时换成 B 内容”会失败关闭。它仍不提供审批者身份认证、公钥不可否认性、跨进程持久化、密钥轮换或收据链，不能替代本卡描述的生产级 Ed25519/JCS/KMS 方案。

## 8. 常见误区和易混概念

### 误区 1：签名收据证明动作正确

它只证明签名内容未改且来自某密钥。错误事实、错误策略也能被忠实签名。

### 误区 2：把 `approved=true` 签名就够了

批准必须绑定规范化后的精确 action digest、身份、过期和 nonce。

### 误区 3：有哈希链就不用保护私钥

私钥泄露后攻击者可伪造新收据或重建链；需 KMS/HSM、轮换、撤销和 key ID。

| 机制 | 能检测内容修改 | 能识别签发者 | 能发现顺序断裂 |
| :--- | :---: | :---: | :---: |
| 普通日志 | 弱 | 弱 | 弱 |
| 单条哈希 | 是（有可信锚时） | 否 | 否 |
| 数字签名 | 是 | 是 | 否 |
| 签名哈希链 | 是 | 是 | 是 |

## 9. 教材与官方实现定位

- 教材入口：[Microsoft Lesson 18 - Securing AI Agents](https://github.com/microsoft/ai-agents-for-beginners/tree/main/18-securing-ai-agents)，核验 2026-08-06。
- 本卡保留 Lesson 18 的核心学习目标：规范化、签名、验证、链式收据与人类批准绑定。
- 具体 Ed25519、JCS、密钥格式和库 API 必须依据当前标准与安全评审，不能从教学代码直接复制到生产。

## 10. 闭卷复现任务

- [ ] 区分哈希、HMAC、数字签名和加密。
- [ ] 写出收据的 10 个最小字段。
- [ ] 解释规范化为何在签名前完成。
- [ ] 画出 action digest 与 approval digest 的绑定。
- [ ] 修改演示代码，加入一次性 nonce 集合并拒绝重放。
- [ ] 说明签名收据不能证明的三件事。

## 11. 自测题：5 道

### 1. #自测题/基础
为什么不能直接签名普通 JSON 字符串？
> [!question]- 答案解析
> 同一对象可能因键顺序、空白、数字或 Unicode 编码产生不同字节，导致验签不一致或语义混淆。

### 2. #自测题/基础
数字签名与加密的目标分别是什么？
> [!question]- 答案解析
> 签名验证来源与完整性；加密控制可读性。

### 3. #自测题/中等
审批记录应绑定哪些内容？
> [!question]- 答案解析
> 精确 action/args digest、审批者、有效期、nonce、策略/资源上下文，且执行前重新验证。

### 4. #自测题/中等
哈希链为什么仍需要外部可信锚？
> [!question]- 答案解析
> 若攻击者可改全部数据且没有已知头/签名，可重算整条普通哈希链；签名、公钥和外部锚提供独立参照。

### 5. #自测题/较难
怎样验证人类批准的是“这次发布”而不是同内容的另一次重放？
> [!question]- 答案解析
> digest 还应包含 request/resource ID、环境、nonce 和过期时间；服务端记录 nonce 已使用并采用幂等键。

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，从动作参数开始画到独立验证结束。

### 我的推导复现
> 为当前项目定义一条收据 schema 和 key rotation 失败处理。

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/46-AI Agent工程/`
- **建议标签**：`#学习` `#加密收据` `#安全审计`
- **拆分建议**：真实密钥与收据仅放项目安全配置，不写入知识卡或 Git。

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

加密收据能证明什么？::在密钥未泄露且验证正确的前提下，证明签名内容来自相应密钥、之后未被修改；链式收据还能发现顺序断裂。
为什么人类审批必须绑定 action digest？::避免 `approved=true` 被挪用到不同工具、金额、对象或参数。
为什么签名前要规范化？::数字签名针对字节；规范化使同一数据得到唯一、可复现的字节表示。
签名收据不能证明什么？::不能证明事实真实、模型判断正确、策略合理或签名密钥没有被滥用。

