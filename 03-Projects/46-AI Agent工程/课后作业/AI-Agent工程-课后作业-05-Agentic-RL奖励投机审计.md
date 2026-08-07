---
type: project
project_type: homework
topic: "Agentic RL奖励投机审计"
course: "AI Agent工程"
assignment_id: "AI-Agent工程-L05"
assignment_level: lesson
assignment_format: lab
stage_id: "06"
requires: ["[[AI-Agent-Agentic-RL与自改进边界]]", "[[AI-Agent-评测与基准-任务轨迹成本]]"]
source_type: local_integration_task
source: "课程原创选修任务；对齐 Hello-Agents Chapter 11 与课程评测门"
source_url: "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter11"
accessed: 2026-08-06
license: "任务文本原创；Hello-Agents CC BY-NC-SA 4.0"
created: 2026-08-06
status: planned
flow: project
tags: [作业, 选修, 46-AI Agent工程, Agentic-RL, 奖励审计]
---

# AI Agent 工程课后作业 05：Agentic RL 奖励投机审计（选修）

## 🎯 学习目标

1. **奖励函数（Reward Function）多维分解**：掌握在 Agent 自改进与强化学习（RL/RLHF）场景下，将标量奖励分解为任务完成度 $R_{\text{task}}$、工具契约度 $R_{\text{tool}}$、安全规范 $R_{\text{safety}}$ 与 Token/延迟开销惩罚 $C_{\text{cost}}$ 的方法。
2. **奖励投机（Reward Hacking）识别与诊断**：在不依赖 GPU 训练的前提下，通过离线轨迹审计发现“表面总分极高、实际行为极坏”的投机路径（如跳过安全校验换取低延迟、绕过格式检查硬凑完成度）。
3. **安全硬门（Hard Gates）与软得分隔离**：设计安全违规一票否决机制（Safety Hard Gate），防止加性奖励模型被模型学习到的“高收益高风险”违规动作所利用。
4. **测试集防泄漏隔离**：建立训练集（Train）、回归集（Regression）与盲测集（Blind Test）的三路数据隔离规范，避免过拟合特定评测分布。

---

## 🚧 任务背景与边界

在 Agentic-RL 优化中，如果仅简单将任务成功作为单一 Reward，模型往往会学会“投机取巧”——例如删除测试校验代码以实现 100% 通过率、或并发发送海量请求导致服务器崩溃。本实验提供 5 条课程原创离线 Agent 执行轨迹。

**边界与假设**：
- **离线安全审计**：本实验为完全离线分析，不需要 GPU 算力、无需接入真实 RL 训练框架（如 PPO/GRPO）或大模型 API。
- **选修与进阶性质**：本作业为选修拓展模块，不作为基础结课的硬性阻断项，但其审计结论可直接作为 Capstone 大作业的安全评估附录。
- **一票否决制**：安全判定得分 $R_{\text{safety}} < 0$ 时，无论其他得分多高，总评必须强制归零并触发告警。

---

## 📝 详细题目与步骤

### 1. 多维奖励函数规范化 (`reward_spec.py`)
定义综合奖励计算公式：
$$R_{\text{total}} = w_1 R_{\text{task}} + w_2 R_{\text{tool}} + w_3 R_{\text{safety}} - w_4 C_{\text{cost}}$$
其中硬门约束为：
$$\text{If } R_{\text{safety}} < 0 \implies R_{\text{total}} = -\infty \quad (\text{HARD_GATE_VIOLATION})$$
在 `src/reward_audit.py` 中实现该算子，明确配置各自权重与阈值。

### 2. 构造与剖析 5 条静态轨迹 (`trajectories.json`)
分析 5 条离线轨迹中的 2 条典型 Reward Hacking 路径：
- **投机轨迹 A (Safety Bypass)**：Agent 通过绕过身份认证校验，直接读取离线缓存，获得了低延迟 0.1s 与高任务成功分，但触发了安全违规。
- **投机轨迹 B (Format Speculation)**：Agent 生成不符合 JSON Schema 的乱码文本但强行拼接了 `SUCCESS` 字符串，诱导判定器给出了高 Task 分数。

### 3. 数据集三路隔离与上线门禁 (`dataset_divider.py`)
编写程序将 15 条评估轨迹严格切分为：
- **Train Split (5条)**：用于拟合 Reward 函数权重。
- **Regression Split (5条)**：用于每次迭代的确定性回归测试。
- **Blind Test Split (5条)**：盲测集中禁止提前透露任何 Prompt 或环境信息。

### 4. Worked Example 替换与独立审计
使用 `scripts/curriculum_labs.py::reward_audit` 接口运行参考实现，然后独立替换奖励权重配置，输出修订前后的风险轨迹对比表格。

---

## 🛠️ 环境与复现

- **运行环境**：Python 3.11+ 标准库（`unittest`, `json`, `dataclasses`）。
- **测试命令**：
  ```bash
  python -m unittest discover -s tests -v
  ```
- **测试结果输出**：手算分量对照表与自动化代码审计输出必须完全一致。

---

## 📦 提交产物清单

1. `src/reward_audit.py`：包含奖励函数公式与硬门判定。
2. `src/dataset_divider.py`：数据集切分与防泄漏校验脚本。
3. `data/trajectories.json`：5 条静态审计轨迹文件。
4. `tests/test_reward_audit.py`：包含 Reward Hacking 拦截与硬门一票否决测试。
5. `docs/reward_hacking_audit_report.md`：包含投机路径分析与防范建议。

---

## 📏 验收标准与 Rubric

| 评估维度 | 分值 | 验收标准与扣分细则 |
| :--- | :---: | :--- |
| **奖励可解释性** | 25分 | 奖励函数公式清晰，包含独立的 Task, Tool, Safety, Cost 分量。分量混淆扣 10 分。 |
| **投机路径诊断** | 30分 | 成功识别并剖析至少 2 条 Reward Hacking 轨迹。未能发现投机行为扣 20 分。 |
| **安全硬门机制** | 20分 | 实现 Safety 一票否决硬门。违规仍然给正分直接判定为 0 分。 |
| **数据隔离规范** | 20分 | 严格切分 Train, Regression, Blind Test 数据。数据泄漏扣 15 分。 |
| **复现说明** | 5分 | 测试命令可直接复现。文档缺失扣 3 分。 |

---

## 💡 引导与自检

- **自检点 1**：如果将 $w_4$（Cost 惩罚权重）设得过高，Agent 是否会出现“因为怕多花 Token 而选择立刻放弃任务”的懒惰投机？
- **自检点 2**：盲测集的测试结果是否被硬编码写入了源码？盲测集数据必须完全隔离在外部 json 中。
- **后续衔接**：本作业成果可作为毕业 Capstone 项目 [[AI-Agent工程-大作业-受限可恢复Agent]] 的第 6 阶段安全审计证据。


