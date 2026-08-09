---
type: study
course: "属性数据分析"
topic: "Logistic模型参数估计与Fisher得分算法"
stage_moc: "[[🧭 阶段2-二项响应与Logistic回归]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: ["似然函数", "Score方程", "Fisher信息矩阵", "Newton-Raphson", "IRLS"]
prerequisites: ["[[属性数据分析-二项Logistic回归模型与参数解释]]", "[[属性数据分析-极大似然估计与渐近推断三大检验]]"]
upstream: ["[[属性数据分析-二项Logistic回归模型与参数解释]]", "[[属性数据分析-极大似然估计与渐近推断三大检验]]"]
status: completed
tags: [学习, 属性数据分析, 优化算法, 最大似然, IRLS]
created: 2026-08-09
---

# 属性数据分析-Logistic模型参数估计与Fisher得分算法

## 1. 对数似然函数推导

设独立样本 $(y_1, \mathbf{x}_1), \dots, (y_n, \mathbf{x}_n)$，$y_i \in \{0, 1\}$，$\pi_i = \pi(\mathbf{x}_i) = \frac{1}{1 + e^{-\mathbf{x}_i^T \boldsymbol{\beta}}}$。

似然函数为：
$$
L(\boldsymbol{\beta}) = \prod_{i=1}^n \pi_i^{y_i} (1 - \pi_i)^{1 - y_i}
$$

对数似然函数为：
$$
\ell(\boldsymbol{\beta}) = \sum_{i=1}^n \left[ y_i \ln\pi_i + (1 - y_i) \ln(1 - \pi_i) \right] = \sum_{i=1}^n \left[ y_i \mathbf{x}_i^T \boldsymbol{\beta} - \ln\left( 1 + \exp(\mathbf{x}_i^T \boldsymbol{\beta}) \right) \right]
$$

在矩阵形式下，设 $\mathbf{y} = (y_1, \dots, y_n)^T$，$X$ 为 $n \times (p+1)$ 设计矩阵：
$$
\ell(\boldsymbol{\beta}) = \mathbf{y}^T X \boldsymbol{\beta} - \sum_{i=1}^n \ln(1 + e^{\mathbf{x}_i^T \boldsymbol{\beta}})
$$

---

## 2. 梯度向量（Score 向量）与 Hessian 矩阵

### 2.1 梯度向量 (Score Function)
对 $\boldsymbol{\beta}$ 求一阶导数：
$$
U(\boldsymbol{\beta}) = \frac{\partial \ell}{\partial \boldsymbol{\beta}} = \sum_{i=1}^n \left( y_i - \frac{e^{\mathbf{x}_i^T \boldsymbol{\beta}}}{1 + e^{\mathbf{x}_i^T \boldsymbol{\beta}}} \right) \mathbf{x}_i = \sum_{i=1}^n (y_i - \pi_i) \mathbf{x}_i = X^T (\mathbf{y} - \boldsymbol{\pi})
$$
Score 方程为非线性方程组：$X^T \mathbf{y} = X^T \hat{\boldsymbol{\pi}}$，无解析闭式解。

### 2.2 Hessian 矩阵与 Fisher 信息矩阵
对 $\boldsymbol{\beta}$ 求二阶导数：
$$
H(\boldsymbol{\beta}) = \frac{\partial^2 \ell}{\partial \boldsymbol{\beta} \partial \boldsymbol{\beta}^T} = -\sum_{i=1}^n \pi_i (1 - \pi_i) \mathbf{x}_i \mathbf{x}_i^T = -X^T W X
$$
其中权重矩阵 $W = \text{diag}(\pi_1(1-\pi_1), \dots, \pi_n(1-\pi_n))$ 为正定对角阵。
因此，Fisher 信息矩阵为：
$$
\mathcal{I}(\boldsymbol{\beta}) = -\mathbb{E}[H(\boldsymbol{\beta})] = X^T W X
$$
因为对所有非共线 $X$ 均有 $X^T W X \succ 0$，故对数似然函数 $\ell(\boldsymbol{\beta})$ 是**全局严格凹函数（Strictly Concave）**，保证了 MLE 的唯一存在性。

---

## 3. Newton-Raphson 与迭代加权最小二乘 (IRLS)

### 3.1 Newton-Raphson 迭代更新式
$$
\boldsymbol{\beta}^{(t+1)} = \boldsymbol{\beta}^{(t)} - H(\boldsymbol{\beta}^{(t)})^{-1} U(\boldsymbol{\beta}^{(t)}) = \boldsymbol{\beta}^{(t)} + \left( X^T W^{(t)} X \right)^{-1} X^T (\mathbf{y} - \boldsymbol{\pi}^{(t)})
$$

### 3.2 IRLS 等价形式推导
将更新式合并写为加权最小二乘形式：
$$
\boldsymbol{\beta}^{(t+1)} = \left( X^T W^{(t)} X \right)^{-1} X^T W^{(t)} \left[ X \boldsymbol{\beta}^{(t)} + (W^{(t)})^{-1} (\mathbf{y} - \boldsymbol{\pi}^{(t)}) \right] = \left( X^T W^{(t)} X \right)^{-1} X^T W^{(t)} \mathbf{z}^{(t)}
$$
其中 $\mathbf{z}^{(t)} = \boldsymbol{\eta}^{(t)} + (W^{(t)})^{-1} (\mathbf{y} - \boldsymbol{\pi}^{(t)})$ 称为**工作响应变量（Adjusted Working Response）**。

> [!TIP]
> **IRLS 算法精髓**：每一轮迭代，均把非线性 Logistic 回归转化为以 $W^{(t)}$ 为加权矩阵、以 $\mathbf{z}^{(t)}$ 为响应变量的加权线性回归（WLS），通常 4~6 次迭代即可高精度收敛。

---

## 4. 手写 Python IRLS 求解器实现

```python
import numpy as np

def fit_logistic_irls(X, y, max_iter=20, tol=1e-8):
    # 使用 IRLS 算法手写求解 Logistic 回归 MLE
    n, p = X.shape
    beta = np.zeros(p)
    
    for iteration in range(max_iter):
        eta = X @ beta
        pi = 1.0 / (1.0 + np.exp(-eta))
        
        # 权重矩阵对角元素
        w_diag = pi * (1.0 - pi)
        # 防止除以零
        w_diag = np.clip(w_diag, 1e-10, 1.0)
        
        W = np.diag(w_diag)
        # 工作变量 z = eta + (y - pi) / w_diag
        z = eta + (y - pi) / w_diag
        
        # WLS 求解: beta_new = (X^T W X)^(-1) X^T W z
        XtW = X.T @ W
        XtWX = XtW @ X
        XtWz = XtW @ z
        
        beta_new = np.linalg.solve(XtWX, XtWz)
        
        # 检查收敛
        diff = np.max(np.abs(beta_new - beta))
        beta = beta_new
        if diff < tol:
            print(f"IRLS 在第 {iteration+1} 次迭代成功收敛!")
            break
            
    # 计算渐近协方差矩阵 (X^T W X)^(-1)
    cov_matrix = np.linalg.inv(X.T @ np.diag(pi * (1 - pi)) @ X)
    se = np.sqrt(np.diag(cov_matrix))
    return beta, se

# 验证测试
np.random.seed(42)
N = 500
x1 = np.random.normal(size=N)
X_mat = np.column_stack([np.ones(N), x1])
true_beta = np.array([-0.5, 1.5])
prob = 1 / (1 + np.exp(-X_mat @ true_beta))
y_sample = np.random.binomial(1, prob)

beta_est, se_est = fit_logistic_irls(X_mat, y_sample)
print("估计参数:", beta_est)
print("参数标准误:", se_est)
```

---

## 🃏 Anki 卡片

### Card 1: Score 向量与 Hessian 矩阵
- **Front**: 在二项 Logistic 回归中，已知设计矩阵 $X$ 和响应概率向量 $\boldsymbol{\pi}$，写出对数似然函数的 Score 向量 $U(\boldsymbol{\beta})$ 与 Hessian 矩阵 $H(\boldsymbol{\beta})$。
- **Back**: 
  - Score 向量：$U(\boldsymbol{\beta}) = X^T (\mathbf{y} - \boldsymbol{\pi})$
  - Hessian 矩阵：$H(\boldsymbol{\beta}) = -X^T W X$，其中 $W = \text{diag}(\pi_i(1-\pi_i))$。
  - 由于 $W \succ 0$，Hessian 矩阵负半定，对数似然全局严格凹。

### Card 2: IRLS 工作响应变量
- **Front**: 解释 Logistic 回归 Fisher 得分算法（IRLS）中工作响应变量 $\mathbf{z}^{(t)}$ 的定义与代数几何意义。
- **Back**: 
  - 定义：$\mathbf{z}^{(t)} = \boldsymbol{\eta}^{(t)} + (W^{(t)})^{-1} (\mathbf{y} - \boldsymbol{\pi}^{(t)})$，其中 $\boldsymbol{\eta}^{(t)} = X\boldsymbol{\beta}^{(t)}$。
  - 几何意义：$\mathbf{z}^{(t)}$ 是线性预测量 $\boldsymbol{\eta}$ 在点 $\boldsymbol{\pi}^{(t)}$ 处的一阶泰勒线性化推展。每一轮迭代将非线性 MLE 问题转化为以 $W^{(t)}$ 为权重的加权最小二乘（WLS）求解 $\boldsymbol{\beta}^{(t+1)} = (X^T W X)^{-1} X^T W \mathbf{z}$。

---

## 5. 核心自测与检索练习

- [ ] 写出 Logistic 回归的 Score 向量 $X^T(\mathbf{y} - \boldsymbol{\pi})$，并解释为什么它的期望为零。
- [ ] 为什么 Logistic 回归的对数似然函数是严格凹函数？这在凸优化中有什么重要保证？
- [ ] 工作响应变量 $\mathbf{z}$ 的本质是什么？它如何将非线性优化转化为 WLS？

---

## 6. 学完后可以完成

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/31-属性数据分析"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

```dataview
LIST
FROM "03-Projects/31-属性数据分析"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

