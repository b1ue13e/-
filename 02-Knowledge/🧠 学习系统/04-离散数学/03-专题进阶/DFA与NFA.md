---
type: study
course: "离散数学"
topic: "DFA与NFA"
title: "DFA与NFA"
created: 2026-08-05
status: ongoing
difficulty: intermediate
concept: ["确定有限自动机", "非确定有限自动机", "DFA", "NFA", "正则语言"]
prerequisites: ["集合函数与基数"]
related: ["正则表达式与正则语言"]
tags: [学习, 离散数学, 自动机, DFA, NFA]
flow: knowledge
kind: concept
proof_mode: true
sources:
  - title: "MIT 6.042J Mathematics for Computer Science"
    url: "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/"
    locator: "Lecture 18-20, PS12"
    source_type: open-courseware
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-05
  - title: "Introduction to the Theory of Computation (Sipser)"
    locator: "Chapter 1"
    source_type: textbook
stage_moc: "[[02-Knowledge/🧠 学习系统/04-离散数学/03-专题进阶/🧭 阶段3-专题进阶]]"
upstream: ["[[02-Knowledge/🧠 学习系统/04-离散数学/01-基础奠基/集合函数与基数]]"]
---
---

# DFA与NFA

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类**
- **判断理由**：DFA 和 NFA 是形式语言理论的第一层——定义了"正则语言"的计算模型。它们是编译器词法分析、正则表达式引擎、协议验证的理论基础。MIT 6.042J PS12 考查。

---

## 1. 这个知识点解决什么问题？

> 什么样的"模式"能被有限内存的机器识别？DFA 用有限状态+确定性转移定义了这类计算——没有额外内存，只有当前状态。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：DFA → NFA → 正则表达式 → 正则语言 → 泵引理。Chomsky 谱系的最底层。
- **应用**：词法分析器（LEX）、文本搜索（grep）、硬件控制器。

---

## 3. 学它之前需要哪些前置知识？

1. **[[集合函数与基数]]**：状态集、转移函数。

---

## 4. 定义复述

**DFA（确定有限自动机）**：五元组 $M = (Q, \Sigma, \delta, q_0, F)$
- $Q$：有限状态集
- $\Sigma$：有限字母表
- $\delta: Q \times \Sigma \to Q$：转移函数（确定性）
- $q_0 \in Q$：初始状态
- $F \subseteq Q$：接受状态集

**NFA（非确定有限自动机）**：$\delta: Q \times \Sigma_\varepsilon \to \mathcal{P}(Q)$（转移函数值是一个状态**集合**），允许 $\varepsilon$-转移。

**语言 $L(M)$**：$M$ 接受的所有字符串的集合。

**定理**：DFA 和 NFA 识别**完全相同**的语言类（正则语言）。NFA 可通过子集构造转化为 DFA（可能指数膨胀）。

### 符号说明

| 符号 | 含义 |
| :--- | :--- |
| $Q$ | 状态集 |
| $\Sigma$ | 字母表 |
| $\delta$ | 转移函数 |
| $q_0$ | 初始状态 |
| $F$ | 接受状态集 |

---

## 5. 直觉与图像

- **直觉类比**：DFA 像一个自动售货机——每个状态（待机/收钱/出货）对应明确定义，投币（输入字符）触发唯一的状态转移。NFA 多了"猜测"能力——同一输入可能选择多条路径，只要有一条到达接受状态就算接受。
- **一句话直觉本质**：DFA = 无额外内存、无回溯的最简计算机模型。

---

## 6. 定理陈述与证明重建

### NFA → DFA 的子集构造

**定理**：每个 NFA 存在等价的 DFA。

**证明（子集构造）**：DFA 的每个状态对应 NFA 的**状态集合**。$Q_{\text{DFA}} = \mathcal{P}(Q_{\text{NFA}})$。转移：$\delta_{\text{DFA}}(S, a) = \bigcup_{q \in S} \delta_{\text{NFA}}(q, a)$。初始状态为 $\{q_0\}$ 的 $\varepsilon$-闭包。接受状态为含至少一个 NFA 接受状态的集合。

**关键"转念"**：DFA 通过"同时追踪所有可能的 NFA 路径"来消除非确定性——每读一个字符，追踪"现在可能处于哪些状态"的集合。这本质上是并行模拟。

---

## 7. 经典反例库

### 反例：子集构造的指数膨胀

- 语言 $L_n = \{w \mid w$ 的倒数第 $n$ 个字符是 $a\}$。NFA 只需 $n+1$ 个状态，但任何 DFA 至少需要 $2^n$ 个状态。子集构造必然导致指数膨胀。

---

## 8. 条件变式

| 变式 | 结论 |
| :--- | :--- |
| 添加 $\varepsilon$-转移 | 识别能力不变（仍为正则语言） |
| DFA 最小化 | 存在唯一最小 DFA（Myhill-Nerode） |

---

## 9. 相关知识点与 Obsidian 双链建议

- **上游**：[[集合函数与基数]]
- **下游**：[[正则表达式与正则语言]]

---

## 10. 闭卷验收（数学模式）

- [ ] **定义复述**：写出 DFA 的五元组定义
- [ ] **定理陈述**：陈述 NFA 和 DFA 的等价性
- [ ] **证明重建**：对给定的 NFA，执行子集构造得到等价 DFA
- [ ] **反例复现**：构造一个 NFA 其最小 DFA 有指数个状态
- [ ] **条件变式**：设计识别"偶数个 0 和奇数个 1"的 DFA

---

## 11. 分级习题

| 题号 | 难度 | 来源 |
| :--- | :--- | :--- |
| 1 | 基础 | MIT PS12 |
| 2 | 基础 | Sipser Ch 1 |
| 3 | 中等 | MIT PS12 |
| 4 | 中等 | Sipser Ch 1 |
| 5 | 较难 | Sipser Ch 1 |

### 题目与解析

#### 1. 设计 DFA 识别 $\{w \in \{0,1\}^* \mid w$ 包含子串 "01"$\}$
> - 状态：$q_0$（还没看到0），$q_1$（刚看到0），$q_2$（已看到01，接受）。转移略。

#### 2. 给定字母表 $\{a,b\}$，设计识别"以 $a$ 开头，以 $b$ 结尾"的 DFA。
> - 需要4个状态：开始、以a开头但未到结尾、以a开头且以b结尾（接受）、错误。

---

## 12. 我的主动回忆区

>

### 下次复习日期
- [ ] 明天 · [ ] 3天后 · [ ] 7天后 · [ ] 14天后

---

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/04-离散数学/03-专题进阶/`
- **关联已有笔记**：`[[集合函数与基数]]` `[[正则表达式与正则语言]]`
- **建议标签**：`#学习` `#离散数学` `#自动机` `#DFA` `#NFA`
