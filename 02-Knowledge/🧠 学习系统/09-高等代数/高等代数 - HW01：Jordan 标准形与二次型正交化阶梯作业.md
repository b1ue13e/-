---
title: "高等代数-题型-Jordan标准形与二次型正交化阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "高等代数作业"
course: "09-高等代数"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: intermediate
importance: A
concept: ["线性代数", "Jordan标准形", "SVD分解"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/17-机器学习/🗺️ 机器学习学习路径|线性代数]]"]
related: ["[[最优化方法-题型-内点法与ADMM求解器手撕阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/09-高等代数/🗺️ 高等代数学习路径|高等代数学习路径]]"]
downstream: []
tags: [学习, 09-高等代数, 作业, 纸笔推导, 阶梯作业]
aliases: ["LA-HW01-Jordan与SVD作业"]
---

# 高等代数 - HW01：Jordan 标准形与二次型正交化阶梯作业

> 🎯 **作业目标**：手算特征值与特征向量、计算 Gram-Schmidt 正交化、化简二次型为标准型，并严格证明 Cayley-Hamilton 定理。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **求解工具**：`SymPy` / `NumPy` / `Lean 4`
- **开源标杆仓库**：[MIT 18.06 Linear Algebra (Gilbert Strang)](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)
- **核心依赖**：`sympy`, `numpy`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验收标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 矩阵计算 100% 正确 | 手算矩阵行列式、逆矩阵、特征多项式与特征值。 |
| 🟡 **L2 - Medium Baseline** | 正交化与标准型化简 | **手写 Gram-Schmidt 正交化算法** 与二次型正交变换化为标准型。 |
| 🔴 **L3 - Strong Baseline** | 严密纸笔证明 | 严密书写 **Jordan 标准形** 变换矩阵求解，证明 Cayley-Hamilton 定理与 SVD 存在性。 |
| 👑 **L4+ - 极客拓展** | **Lean 4 形式化证明** | 在 Lean 4 证明器中形式化证明对称矩阵特征值为实数及 Cayley-Hamilton 定理。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_gram_schmidt_orthonormal():
    from algebra_tools import gram_schmidt
    A = np.random.randn(5, 5)
    Q = gram_schmidt(A)
    
    # Q^T * Q == I
    identity_check = Q.T @ Q
    np.testing.assert_allclose(identity_check, np.eye(5), atol=1e-5, err_msg="Gram-Schmidt 得到的矩阵必须完全正交")
```

---

## 🃏 Anki 卡片

- Q: 矩阵 $A$ 的奇异值分解 (SVD) $A = U \Sigma V^T$ 中，左奇异向量 $U$ 与右奇异向量 $V$ 的几何含义是什么？
- A: $V$ 表示输入空间的正交基，$\Sigma$ 表示沿基方向的拉伸/缩放比例，$U$ 表示输出空间的正交基。SVD 将任意线性变换分解为“旋转-缩放-旋转”。
