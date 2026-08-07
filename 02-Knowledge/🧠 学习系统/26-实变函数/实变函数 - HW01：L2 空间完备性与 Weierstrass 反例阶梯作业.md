---
title: "实变函数-题型-L2空间完备性与Weierstrass反例阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "实变函数作业"
course: "26-实变函数"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["实变函数", "Lebesgue积分", "L2空间完备性"]
prerequisites: ["[[🗺️ 数学分析学习路径|数学分析]]"]
related: ["[[泛函分析-题型-三大定理与Hilbert空间算子阶梯作业]]"]
upstream: ["[[🗺️ 实变函数学习路径|实变函数学习路径]]"]
downstream: []
tags: [学习, 26-实变函数, 作业, 纸笔推导, 阶梯作业]
aliases: ["RA-HW01-L2完备性与Weierstrass作业"]
---

# 实变函数 - HW01：L2 空间完备性与 Weierstrass 反例阶梯作业

> 🎯 **作业目标**：构造处处连续但处处不可导的 Weierstrass 函数、证明 Egorov 依测度收敛定理与 $L^2$ 空间完备性 (Riesz-Fischer 定理)。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **绘图与工具**：`Matplotlib` / `SymPy` / `Lean 4`
- **开源标杆仓库**：[Rudin Real Analysis Solutions](https://github.com/vittorioromeo/baby-rudin-solutions)
- **核心依赖**：`matplotlib`, `numpy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 集合交并判定正确 | 证明开集与闭集的有限/无限交并拓扑性质。 |
| 🟡 **L2 - Medium Baseline** | 分形函数绘图无误 | 构造处处连续但处处不可导的 Weierstrass 病态函数 $f(x) = \sum a^n \cos(b^n \pi x)$ 并数值绘图。 |
| 🔴 **L3 - Strong Baseline** | 严密纸笔推导 | **严格书写 $L^2$ 空间完备性 (Riesz-Fischer 定理)**：Cauchy 序列的 $L^2$ 范数收敛性证明。 |
| 👑 **L4+ - 极客拓展** | **Lean 4 形式化证明** | 在 Lean 4 中形式化证明 Vitali 不可测集的存在性（选择公理 Axiom of Choice 的应用）。 |

---

## 3. 🧪 自动化测试 Harness (Matplotlib Visualization & PyTest)

```python
import pytest
import numpy as np

def test_weierstrass_function_non_differentiable():
    # 模拟 Weierstrass 函数数值微分
    a = 0.5
    b = 13
    x = np.linspace(0, 1, 1000)
    
    f = np.zeros_like(x)
    for n in range(50):
        f += (a**n) * np.cos((b**n) * np.pi * x)
        
    df_dx = np.diff(f) / np.diff(x)
    # 微分极其剧烈震荡，无界
    assert np.max(np.abs(df_dx)) > 100.0, "Weierstrass 函数数值导数必须呈现剧烈发散震荡"
```

---

## 🃏 Anki 卡片

- Q: 简述实变函数中叶戈罗夫定理 (Egorov's Theorem) 的核心结论。
- A: 若可测集 $E$ 的测度有限 ($\mu(E) < \infty$)，可测函数列 $f_n(x)$ 在 $E$ 上几乎处处收敛于 $f(x)$，则对任意 $\epsilon > 0$，存在可测子集 $E_\epsilon \subset E$，使得 $\mu(E \setminus E_\epsilon) < \epsilon$，且 $f_n(x)$ 在 $E_\epsilon$ 上一致收敛于 $f(x)$（几乎处处收敛 $\implies$ 近乎一致收敛）。
