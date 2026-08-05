---
title: "离散数学 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "离散数学 4-Tier 阶梯作业规范"
course: "离散数学"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [离散数学, 4Tier作业, 阶梯作业, 编程实战, PyTest, MIT6042J, Rosen]
---

# 🧮 离散数学 4-Tier 阶梯作业全景规范说明书 (MIT 6.042J & Rosen 范式)

> 本说明书为 **04-离散数学** 路径（基于 Rosen《Discrete Mathematics and its Applications》与 MIT 6.042J）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ Python 集合运算 / 内置 itertools 排列组合 / 逻辑真值表生成
🟡 L2 - Medium Baseline   │ 模运算与欧几里得算法 / 递归与数学归纳法验证
🔴 L3 - Strong Baseline   │ [核心] 不调用高级库，从零手撕 扩展欧几里得 (exGCD) / 中国剩余定理 (CRT) / 关系传递闭包 (Warshall)
👑 L4 - Boss Baseline     │ Lean 4 定理证明 (自然数皮亚诺公理, 形式化逻辑推理) / 复杂图着色 (Graph Coloring) SAT 规约求解
```

---

## 🎯 离散数学阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 命题逻辑与集合论 (Logic & Sets)
- **开源溯源**：Rosen Ch 1-2 / MIT 6.042J Lec 1-3
- 🟢 **L1**: 编写程序生成任意命题逻辑公式的真值表 (Truth Table)。
- 🟡 **L2**: 实现集合的幂集 (Power Set) 生成算法与笛卡尔积 (Cartesian Product)。
- 🔴 **L3 (手撕核心)**：**从零手撕 命题逻辑公式到合取范式 (CNF) 的转化算法，实现简单的 DPLL 形式化验证器 (SAT Solver)**。
- 👑 **L4**: 在 Lean 4 中形式化证明德摩根定律 (De Morgan's Laws) 与集合分配律。

### 2. HW02 - 数论与密码学基础 (Number Theory & Cryptography)
- **开源溯源**：Rosen Ch 4 / MIT 6.042J Lec 4
- 🟢 **L1**: 实现快速幂 (Modular Exponentiation) 与素数判定 (Trial Division)。
- 🟡 **L2**: 实现 费马小定理 (Fermat's Little Theorem) 素性测试与寻找原根。
- 🔴 **L3 (手撕核心)**：**手撕 扩展欧几里得算法 (Extended GCD) 求模逆元，以及 中国剩余定理 (Chinese Remainder Theorem, CRT) 构造求解算法**。
- 👑 **L4**: 实现完整的 RSA 加密解密体系流程 (密钥生成、大素数生成 Miller-Rabin 测试)。

### 3. HW03 - 关系与偏序集 (Relations & Posets)
- **开源溯源**：Rosen Ch 9 / MIT 6.042J Lec 7
- 🟢 **L1**: 用邻接矩阵表示有限集上的二元关系。
- 🟡 **L2**: 判断关系的自反性、对称性与传递性，找出等价类。
- 🔴 **L3 (手撕核心)**：**从零手撕 Warshall 算法求解关系的传递闭包 (Transitive Closure)，以及实现偏序集 (Poset) 的拓扑排序算法**。
- 👑 **L4**: 实现 Hasse Diagram (哈斯图) 自动约简可视化算法。

### 4. HW04 - 组合数学与离散概率 (Combinatorics & Discrete Probability)
- **开源溯源**：Rosen Ch 6-8 / MIT 6.042J Lec 14-19
- 🟢 **L1**: 计算排列组合数 $\binom{n}{k}$ 避免大数溢出。
- 🟡 **L2**: 编写模拟器验证 生日悖论 (Birthday Paradox) 与 蒙提霍尔问题 (Monty Hall)。
- 🔴 **L3 (手撕核心)**：**手撕 容斥原理 (Inclusion-Exclusion Principle) 计算引擎，以及解线性常系数齐次递推关系 (如斐波那契通项) 的特征方程法**。
- 👑 **L4**: 实现 马尔可夫链 (Markov Chain) 稳态分布计算。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-discrete/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-discrete/tests/test_hw01_sat.py
pytest 03-Projects/projects-discrete/tests/test_hw02_crt.py
pytest 03-Projects/projects-discrete/tests/test_hw03_warshall.py
```
