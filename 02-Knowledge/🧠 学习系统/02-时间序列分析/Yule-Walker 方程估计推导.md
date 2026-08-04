---
title: "Yule-Walker 方程估计推导"
date: 2026-07-31
type: derivation
kind: derivation
flow: knowledge
course: "02-时间序列分析"
importance: "A"
tags: [推导, 时间序列, YW方程]
upstream: ["[[自回归模型(AR)]]"]
downstream: ["[[参数估计]]"]
status: learning
---

# Yule-Walker 方程估计推导

> [!NOTE] 核心直觉：从影子倒推雕塑
> Yule-Walker 方程是整个时间序列推导中最优美的一环。它的核心思想是：利用“方程两边同乘历史项并取期望”的“正交投影法”，把不可解的带白噪声的 AR 方程，完美转化成完全由已知的“自相关系数（影子）”和未知的“AR参数（雕塑）”组成的纯代数方程组。

## 1. 推导目标
给定一个零均值的平稳 AR(p) 模型，如何纯通过样本计算出的自协方差 $\gamma_k$ 去推导出 AR 参数 $\phi_1, \dots, \phi_p$？

## 2. 一步步推导过程 (Step-by-step)
**起点：AR(p) 方程**
$$ X_t = \phi_1 X_{t-1} + \phi_2 X_{t-2} + \dots + \phi_p X_{t-p} + \epsilon_t $$
其中 $\epsilon_t \sim WN(0, \sigma^2)$，且 $\epsilon_t$ 独立于过去的所有的 $X_{t-k} (k>0)$。

### Step 1: 乘以历史项并取期望（投影）
将等式两边同乘 $X_{t-k}$（其中 $k > 0$），得到：
$$ X_t X_{t-k} = \phi_1 X_{t-1} X_{t-k} + \dots + \phi_p X_{t-p} X_{t-k} + \epsilon_t X_{t-k} $$

对方程两边求数学期望 $E[\cdot]$：
$$ E[X_t X_{t-k}] = \phi_1 E[X_{t-1} X_{t-k}] + \dots + \phi_p E[X_{t-p} X_{t-k}] + E[\epsilon_t X_{t-k}] $$

### Step 2: 引入协方差定义化简
根据平稳性假设，自协方差函数 $\gamma_k = E[X_t X_{t-k}]$。
对于最后一项，因为未来的白噪声冲击 $\epsilon_t$ 与历史状态 $X_{t-k}$ 互不相关，所以 $E[\epsilon_t X_{t-k}] = 0$。

代入后得到差分方程：
$$ \gamma_k = \phi_1 \gamma_{k-1} + \phi_2 \gamma_{k-2} + \dots + \phi_p \gamma_{k-p}, \quad k > 0 $$

### Step 3: 标准化为自相关系数 (ACF)
方程两边同除以方差 $\gamma_0$，利用 $\rho_k = \gamma_k / \gamma_0$，得到：
$$ \rho_k = \phi_1 \rho_{k-1} + \phi_2 \rho_{k-2} + \dots + \phi_p \rho_{k-p}, \quad k = 1, 2, \dots, p $$

### Step 4: 矩阵形式求解
将 $k=1, 2, \dots, p$ 一次性写成矩阵形式：
$$ 
\begin{pmatrix} 1 & \rho_1 & \dots & \rho_{p-1} \\ \rho_1 & 1 & \dots & \rho_{p-2} \\ \vdots & \vdots & \ddots & \vdots \\ \rho_{p-1} & \rho_{p-2} & \dots & 1 \end{pmatrix} 
\begin{pmatrix} \phi_1 \\ \phi_2 \\ \vdots \\ \phi_p \end{pmatrix} = 
\begin{pmatrix} \rho_1 \\ \rho_2 \\ \vdots \\ \rho_p \end{pmatrix} 
$$
这就是 Yule-Walker 方程。只要左侧的自相关矩阵 (Toeplitz 矩阵) 可逆，直接求逆即可得到参数 $\Phi$。

## 3. 陷阱与注意事项 (Pitfalls)
> [!WARNING] 计算白噪声方差的隐藏考点
> 很多人算完了 $\phi_i$ 就觉得做完了！千万别忘了白噪声方差 $\sigma^2$ 是多少！
> 把最初的方程同乘 $X_t$ (此时 $k=0$) 取期望：
> $\gamma_0 = \phi_1 \gamma_1 + \dots + \phi_p \gamma_p + E[\epsilon_t X_t]$
> 注意！此时 $E[\epsilon_t X_t] = E[\epsilon_t (\phi_1 X_{t-1} + \dots + \epsilon_t)] = E[\epsilon_t^2] = \sigma^2$！
> 整理得：$\sigma^2 = \gamma_0 - \phi_1 \gamma_1 - \dots - \phi_p \gamma_p$。

## 4. 费曼自测
- [ ] 为什么 $E[\epsilon_t X_{t-k}]$ 在 $k>0$ 时等于 0，而在 $k=0$ 时等于 $\sigma^2$？
- [ ] 推导出的矩阵方程中，矩阵为什么一定是对称的？
