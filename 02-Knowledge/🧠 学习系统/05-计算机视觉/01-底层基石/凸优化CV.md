---
type: study
course: "05-计算机视觉"
topic: "凸优化 (Convex Optimization)"
created: 2026-08-06
status: ongoing
difficulty: intermediate
concept: ["凸集", "凸函数", "梯度下降", "拉格朗日对偶", "KKT条件"]
prerequisites: ["线性代数基础CV", "梯度下降CV"]
related: ["优化器SGD到Adam", "Softmax与SVM损失函数"]
upstream: ["[[梯度下降CV]]"]
flow: knowledge
stage_moc: "[[🧭 阶段1-底层基石]]"
kind: concept
source: "《Mathematics for Machine Learning》Ch.7; Boyd & Vandenberghe"
tags: [学习, 计算机视觉, 优化, 凸优化]
---

# 凸优化 (Convex Optimization)

> 所属模块：[[🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[🧭 阶段1-底层基石|第一阶段：底层基石]]
> 建议先看：[[线性代数基础CV]]、[[梯度下降CV]]

---

## 0. 类别：A 类核心概念

凸优化是理解"为什么 SGD 能收敛"的理论基础。虽然深度学习的损失函数通常**不是**凸的，但理解凸优化才能理解什么时候收敛有保证、什么时候会出问题。

---

## 1. 直觉：碗状的损失函数

凸函数（convex function）形状像一口碗：

$$f(\theta \mathbf{x} + (1-\theta)\mathbf{y}) \leq \theta f(\mathbf{x}) + (1-\theta) f(\mathbf{y}), \quad \forall \theta \in [0,1]$$

> **几何意义**：函数图像上任意两点连线在函数图像上方。即"没有局部最小值，只有全局最小值"。

局部极小值 = 全局极小值。梯度下降**保证**收敛到全局最优（对于凸函数）。

---

## 2. 凸 vs 非凸

| 特性 | 凸函数 | 非凸函数 |
|:---|:---|:---|
| 局部极小值 | = 全局极小值 | 可能有多个局部极小值 |
| 梯度下降 | 保证收敛 | **不保证**收敛到全局最优 |
| 典型例子 | 线性回归、SVM、Logistic 回归 | 神经网络损失函数、矩阵分解 |
| 优化难度 | 低（多项式时间） | 高（NP-hard 最坏情况） |

### 深度学习为什么能工作（尽管非凸）？

1. **过参数化**：参数远多于样本时，局部极小值趋向全局最优
2. **SGD 的噪声**：随机梯度帮助跳出差的局部极小值和鞍点
3. **批量归一化 + 残差连接**：平滑损失景观（loss landscape），使其更接近凸

---

## 3. 凸函数判定

### 一阶条件（梯度单调性）

$$f(\mathbf{y}) \geq f(\mathbf{x}) + \nabla f(\mathbf{x})^T(\mathbf{y} - \mathbf{x})$$

即函数图像在任意切线上方。

### 二阶条件（Hessian 半正定）

$$\nabla^2 f(\mathbf{x}) \succeq 0 \quad (\text{半正定})$$

- 所有特征值 ≥ 0
- 对于二次函数 $f(\mathbf{x}) = \frac{1}{2}\mathbf{x}^T\mathbf{Q}\mathbf{x} + \mathbf{b}^T\mathbf{x}$：凸 ⇔ $\mathbf{Q} \succeq 0$

```python
import numpy as np

def is_convex_quadratic(Q):
    """检查二次型 x^T Q x 是否为凸函数"""
    eigenvalues = np.linalg.eigvalsh(Q)  # 对称矩阵的特征值
    return np.all(eigenvalues >= -1e-10)

# 示例
Q_convex = np.array([[2, 1], [1, 2]])   # 特征值: 3, 1 → 凸
Q_nonconvex = np.array([[1, 3], [3, 1]])  # 特征值: 4, -2 → 非凸
print(f"Q_convex is convex: {is_convex_quadratic(Q_convex)}")     # True
print(f"Q_nonconvex is convex: {is_convex_quadratic(Q_nonconvex)}")  # False
```

---

## 4. CV 中的凸优化问题

| 问题 | 凸性 | 求解方法 |
|:---|:---|:---|
| 线性回归（最小二乘） | ✅ 凸 | 闭式解或梯度下降 |
| Logistic 回归（交叉熵） | ✅ 凸 | 梯度下降 |
| **线性 SVM（Hinge Loss）** | ✅ 凸 | SMO / 次梯度 |
| **稀疏编码（L1正则）** | ✅ 凸 | ISTA / FISTA |
| CNN 损失函数 | ❌ 非凸 | SGD + 动量 |
| GAN 的 minimax 博弈 | ❌ 非凸非凹 | 交替梯度下降 |
| 矩阵补全（低秩） | ❌ 非凸 | 交替最小化 |

---

## 5. 常见误区

- ❌ "凸函数就没有局部极小" — **严格凸**函数才有唯一全局最小；一般凸函数可能有一条"平坦谷底"
- ❌ "深度学习因为非凸所以不存在收敛保证" — 实践中 SGD 在过参数化网络上通常能找到好的解
- ❌ "只要 Hessian 半正定就是凸" — 这是**必要条件**，但仅在函数二阶可微时；很多凸函数不可微（如 ReLU 在 0 点）

---

## 6. 适用边界与注意事项

- **理论保证的边界**：一阶/二阶条件与"梯度下降保证收敛到全局最优"只对**凸**问题成立。深度学习损失函数非凸，因此 SGD **没有全局收敛保证**——实践中能找到好解，是过参数化 + 架构平滑（BN、残差连接）的"经验成果"，不是定理。
- **可以直接用凸求解器的场景**：线性 / 逻辑回归、线性 SVM（SMO）、L1 稀疏编码（ISTA / FISTA）——闭式或凸优化器能稳定求解，不必靠 SGD。
- **必须用 SGD 的场景**：CNN、Transformer、GAN 等非凸目标，凸优化理论只能提供"局部近似"或初始化参考，主循环仍是随机梯度 + 动量 / Adam。
- **常见误用**：不要因为"知道凸优化"就试图给 CNN 套凸求解器；也不要认为"非凸 = 无法优化"——两类问题用两套工具。

---

## 🧪 自测题

1. **(基础)** $f(x) = x^2$ 是凸函数吗？$f(x) = -x^2$ 呢？
   <details><summary>💡 思路</summary>用二阶导数符号判断：若 $f''(x)\ge 0$ 对所有 $x$ 成立，则凸；若 $f''(x)\le 0$ 则凹。注意凸/凹是「整体」性质，不能只看某一点。</details>

2. **(中等)** 为什么线性回归（MSE Loss）的损失函数是凸的，但神经网络的 MSE Loss 不是？
   <details><summary>💡 思路</summary>看预测 $\hat{y}$ 对参数 $\mathbf{w}$ 是不是线性/仿射映射。线性回归 $\hat{y}=\mathbf{w}^T\mathbf{x}$ 关于 $\mathbf{w}$ 是线性的，复合 MSE 后仍保持凸性；神经网络是多层层叠的非线性变换，破坏了这一结构——关键在「线性 vs 非线性复合」。</details>

3. **(较难)** 如果损失函数非凸，梯度下降到 0 的点可能是什么？如何判断是局部极小值还是鞍点？
   <details><summary>💡 思路</summary>梯度为 0 只是「驻点」，未必是最优。用 Hessian 的特征值符号区分：全正 / 全负 / 正负混合分别对应什么？结合深度学习的实际经验，哪种情况更常见？</details>

---

## 🔀 学完本节后的横向连接

- 配合 [[优化器SGD到Adam|优化器 SGD→Adam]] 理解凸 vs 非凸对优化器选择的影响
---

## 学完后可以完成

> 下列作业在 `requires` 中引用了本卡，由 Dataview 实时派生（非人工维护反向链接）：

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

本卡另以前置「🧪 自测题」与闭卷复现作为形成性验收。

## 🔗 知识图谱

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
