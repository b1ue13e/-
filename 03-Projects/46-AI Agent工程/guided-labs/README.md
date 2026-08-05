---
type: project
topic: "双教材渐进实验：标准库 Agent Lab"
created: 2026-08-06
status: active
progress: 0%
tags: [项目, 46-AI Agent工程, 渐进支架, 标准库]
flow: project
kind: moc
source: "Original worked baseline aligned with Microsoft AI Agents for Beginners and Datawhale Hello-Agents"
---

# 双教材渐进实验：标准库 Agent Lab

## 运行方式

在本目录执行：

```powershell
python -m unittest -v
python curriculum_labs.py
```

当前 baseline 不需要模型 API、GPU、云账号或第三方库。它用确定性输入模拟模型决策、工具、协议和环境，让学习者先掌握控制流与验收，再替换真实依赖。

## 四级支架

每个 P 项目都按四级完成，不允许跳过故障注入：

1. **Worked**：运行 `curriculum_labs.py` 的现成函数，先预测输出，再逐行解释。
2. **Completion**：复制一个函数到个人练习文件，只改一个策略点；保留测试，直到输出与预期一致。
3. **Independent**：不看实现，只看任务规格、输入和 Gate，重写同一能力。
4. **Transfer**：换领域、工具或数据格式，重新定义威胁与评测；只改名称不算迁移。

## P0–P8 任务卡

| 项目 | Worked | Completion | Independent | Transfer | 反馈测试 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P0 工具契约 | `validate_tool_call` | 增加 `lookup_order` schema | 从零写未知工具/畸形参数错误 | 把订单换成课程资料搜索 | `test_p0_*` |
| P1 有限循环 | `bounded_loop` | 改为 2 步预算并记录原因 | 设计 observation/终止状态 | 将天气换成只读诊断 | `test_p1_*` |
| P2 状态机 | `run_pipeline` | 加 `checkpoint` 字段 | 画并实现失败分支 | 将聚合换成报告流水线 | `test_p2_*` |
| P3 上下文 | `build_context` | 增加去重/敏感项拒绝 | 手写 800-token 装配器 | 将证据换成论文/课程笔记 | `test_p3_*` |
| P4 反思 | `reflect_report` | 增加最大成本停止 | 设计确定性引用验证器 | 将报告换成代码修复评审 | `test_p4_*` |
| P5 协议 | `AgentCard`/`delegate` | 加认证声明与取消 | 区分 MCP-like tool 与 A2A-like task | 换成本地/远程两个服务 | `test_p5_*` |
| P6 评测 | `metrics` | 加 P95/成本 | 写逐样本 eval spec | 换成领域安全样本 | `test_p6_*` |
| P7A 旅行 | `plan_trip` | 增加只读航班证据 | 设计行程 Agent 状态图 | 换成会议安排 | `test_p7a_*` |
| P7B 小镇 | `tick_town` | 增加 NPC 记忆上限 | 写离线状态转移规则 | 换成客服会话模拟 | `test_p7b_*` |
| P7C 深度研究 | `research_report` | 增加冲突来源标记 | 设计 TODO 驱动检索流程 | 换成本库资料研究 | `test_p7_*` |
| P8 奖励审计 | `reward_audit` | 增加长度/延迟惩罚 | 找两条投机轨迹 | 用自有指标复核 | `test_p8_*` |

## 反馈规则

- 测试失败先按 `contract / state / data / permission / orchestration / environment` 分类，再改代码。
- 通过测试不等于掌握：每项还需在 `../作业映射/AI-Agent工程-双教材渐进实践-知识点映射.md` 的学习证据表记录预测差异、故障和迁移。
- 两次同类失败后只回退一个支架级别，不重新抄整章。
- 真实框架接线另建环境；本目录的离线通过不能冒充 Microsoft、Datawhale 或 Berkeley 官方成绩。
