---
title: "测度论-题型-单调收敛定理与Radon-Nikodym证明阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "测度论作业"
course: "25-测度论"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["测度论", "勒贝格积分", "Radon-Nikodym定理"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/28-数学分析/🗺️ 数学分析学习路径|数学分析]]"]
related: ["[[实变函数-题型-L2空间完备性与Weierstrass反例阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/25-测度论/🗺️ 测度论学习路径|测度论学习路径]]"]
downstream: []
tags: [学习, 25-测度论, 作业, 纸笔推导, 阶梯作业]
aliases: ["MT-HW01-单调收敛与Radon定理作业"]
---

# 测度论 - HW01：单调收敛定理与 Radon-Nikodym 证明阶梯作业

> 🎯 **作业目标**：计算 Cantor 集 Lebesgue 测度、严密证明单调收敛定理 (MCT) 与 Radon-Nikodym 定理。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **求解工具**：`SymPy` / `Lean 4` (`mathlib4`)
- **开源标杆仓库**：[Lean 4 mathlib4 Measure Theory Proofs](https://github.com/leanprover-community/mathlib4) / Folland Real Analysis
- **核心依赖**：`sympy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 手算测度无误 | 手算 Cantor 集的 $1$-维 Lebesgue 测度为 0，验证 $\sigma$-代数可数交并性质。 |
| 🟡 **L2 - Medium Baseline** | 极限与积分可交换 | 严格推导并证明 **单调收敛定理 (MCT)** 与 **控制收敛定理 (DCT)**。 |
| 🔴 **L3 - Strong Baseline** | 严密纸笔证明 | **严格书写 Radon-Nikodym 定理** 关于绝对连续测度概率密度的存在唯一性证明。 |
| 👑 **L4+ - 极客拓展** | **Lean 4 形式化证明** | 在 Lean 4 证明器中形式化证明可测函数列的 Fatou 预备定理 (Fatou's Lemma)。 |

---

## 3. 🧪 自动化测试 Harness (SymPy Verification)

```python
import sympy as sp

def test_cantor_set_measure():
    # 验证 Cantor 集除去区间总长度为 1
    # 除去长度 = sum_{n=0}^\inf 2^n * (1/3)^{n+1} = 1/3 * 1 / (1 - 2/3) = 1.0
    n = sp.Symbol('n', integer=True, nonnegative=True)
    length_removed = sp.summation((2**n) * (sp.Rational(1, 3)**(n + 1)), (n, 0, sp.oo))
    
    assert length_removed == 1, "Cantor 集在 [0,1] 中除去开集总测度必须为 1，故 Cantor 集测度为 0"
```

---

## 🃏 Anki 卡片

- Q: 简述测度论中 Radon-Nikodym 定理的结论与前提条件。
- A: 若 $\nu$ 是可测空间 $(X, \Sigma)$ 上的可数可加测度，$\mu$ 是 $\sigma$-有限测度，且 $\nu$ 关于 $\mu$ 绝对连续 ($\nu \ll \mu$)，则存在唯一的非负可测函数 $f \ge 0$（称为 Radon-Nikodym 导数 $\frac{d\nu}{d\mu}$），使得对任意可测集 $A \in \Sigma$，均有 $\nu(A) = \int_A f d\mu$。
