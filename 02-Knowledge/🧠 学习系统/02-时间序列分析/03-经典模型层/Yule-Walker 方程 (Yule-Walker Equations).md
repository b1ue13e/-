---
title: "推导2：Yule-Walker方程"
date: 2026-07-31
type: concept
kind: concept
flow: knowledge
course: "02-时间序列分析"
importance: "A"
tags: [学习, 核心概念, 时间序列]
upstream: ["[[自回归模型(AR)]]", "[[自相关函数ACF.md]]"]
downstream: ["[[偏自相关函数(PACF)]]", "Levinson-Durbin 算法（待创建专题）"]
status: learning
source: "MIT OCW 14.384 Lecture 1; Penn State STAT 510 Lesson 1"
---

# Yule-Walker 方程 (Yule-Walker Equations)

> [!NOTE] 核心直觉：皮影戏的逆向还原游戏
> **类比**：假设有一个三维的雕塑，我们看不到它的全貌。但是我们可以用手电筒从各个角度照它，在墙上留下二维的剪影（Shadow）。
> 
> 在时间序列里，真实的 AR 模型参数 $\phi_1, \phi_2 \dots$ 就是那个“三维雕塑”，我们无法直接看到。而我们计算出来的**自相关系数 ACF** $\rho_1, \rho_2 \dots$ 就是“墙上的剪影”。
> **Yule-Walker 方程**提供了一套完美的数学蓝图，让你仅通过观察墙上的剪影（ACF），就能分毫不差地逆向重建出那个看不见的三维雕塑（AR 模型参数）。

## 1. 为什么需要这个知识点？
- **背景**：在量化金融或计量经济学中，当我们认定一组数据符合 AR(p)（自回归）模型时，最核心的任务是：如何根据已有的样本数据，去**估计**出模型的参数 $\phi_1, \dots, \phi_p$。
- **痛点**：传统的 OLS（最小二乘法）当然可以使用，但在数学形式上稍显笨重。Yule-Walker 方程直接在参数和自相关系数之间架起了一座桥梁。
- **意义**：它不仅提供了一种极其优雅的参数矩估计（Method of Moments）方法，还是计算偏自相关函数（PACF）以及使用快速 Levinson-Durbin 递归算法的基石。

## 2. 核心定义与公式推导
假设我们有一个零均值的平稳 AR(p) 模型：
$$ X_t = \phi_1 X_{t-1} + \phi_2 X_{t-2} + \dots + \phi_p X_{t-p} + \epsilon_t $$
其中 $\epsilon_t$ 是方差为 $\sigma^2$ 的白噪声。

### 第一步：方程两边同乘 $X_{t-k}$
我们将方程两边同时乘以 $X_{t-k}$（其中 $k > 0$）：
$$ X_t X_{t-k} = \phi_1 X_{t-1} X_{t-k} + \phi_2 X_{t-2} X_{t-k} + \dots + \phi_p X_{t-p} X_{t-k} + \epsilon_t X_{t-k} $$

### 第二步：两边求数学期望 $E[\cdot]$
取期望，由于模型是平稳的，所以 $E[X_t X_{t-k}]$ 就是自协方差函数 $\gamma_k$：
$$ \gamma_k = \phi_1 \gamma_{k-1} + \phi_2 \gamma_{k-2} + \dots + \phi_p \gamma_{k-p} + E[\epsilon_t X_{t-k}] $$
由于 $\epsilon_t$ 是当前的白噪声，与过去的 $X_{t-k}$ ($k>0$) 完全不相关，所以 $E[\epsilon_t X_{t-k}] = 0$。

此时得到自协方差递推方程：
$$ \gamma_k = \phi_1 \gamma_{k-1} + \phi_2 \gamma_{k-2} + \dots + \phi_p \gamma_{k-p} $$

### 第三步：转化为自相关系数 $\rho_k$
将方程两边同除以方差 $\gamma_0$，我们知道 $\rho_k = \frac{\gamma_k}{\gamma_0}$，且 $\rho_{-k} = \rho_k$，于是得到著名的 **Yule-Walker 方程**：
$$ \rho_k = \phi_1 \rho_{k-1} + \phi_2 \rho_{k-2} + \dots + \phi_p \rho_{k-p}, \quad \text{for } k = 1, 2, \dots, p $$

### 第四步：写成矩阵形式
对于 $k=1, 2, \dots, p$，我们可以把它们写成极其对称漂亮的矩阵形式：
$$ 
\begin{pmatrix}
1 & \rho_1 & \rho_2 & \dots & \rho_{p-1} \\
\rho_1 & 1 & \rho_1 & \dots & \rho_{p-2} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
\rho_{p-1} & \rho_{p-2} & \rho_{p-3} & \dots & 1
\end{pmatrix}
\begin{pmatrix}
\phi_1 \\
\phi_2 \\
\vdots \\
\phi_p
\end{pmatrix}
=
\begin{pmatrix}
\rho_1 \\
\rho_2 \\
\vdots \\
\rho_p
\end{pmatrix}
$$
或者简写为：$R \Phi = \rho$。只需计算矩阵的逆：$\Phi = R^{-1} \rho$，就能算出所有的 $\phi$。

## 3. 具体应用案例
**场景**：你要拟合一只股票的短期波动，猜测它是一个 AR(2) 模型。
1. 用 Pandas 的 `autocorr()` 计算出样本的自相关系数，假设 $\hat{\rho}_1 = 0.5$, $\hat{\rho}_2 = 0.2$。
2. 根据 Yule-Walker 方程写出 $2 \times 2$ 矩阵：
   $$ 
   \begin{pmatrix} 1 & 0.5 \\ 0.5 & 1 \end{pmatrix} \begin{pmatrix} \phi_1 \\ \phi_2 \end{pmatrix} = \begin{pmatrix} 0.5 \\ 0.2 \end{pmatrix}
   $$
3. 解这个二元一次方程组：
   - $\phi_1 + 0.5\phi_2 = 0.5$
   - $0.5\phi_1 + \phi_2 = 0.2$
4. 轻松得出 $\phi_1 = 0.533$, $\phi_2 = -0.066$。参数估计大功告成！

## 4. 常见误区与陷阱 (Pitfalls)
> [!WARNING] 踩坑预警
> - **MA模型不适用**：初学者常以为 Yule-Walker 能解所有问题。注意，这套优雅的线性方程**只适用于纯 AR 模型**！如果是 MA 模型，由于白噪声交叉相乘项不会消掉，得到的方程是非线性的，无法直接解出。
> - **样本方差带来的正定性问题**：在实战用代码求解 $R^{-1}$ 时，必须使用样本自协方差的**有偏估计**（除以 $N$ 而不是 $N-1$），否则在小样本下相关矩阵 $R$ 可能不是正定矩阵，导致矩阵不可逆（求逆失败）。
> - **白噪声方差估计**：解出 $\Phi$ 后，不要忘了白噪声方差 $\sigma^2$。它可以通过 $k=0$ 时的公式算出：$\sigma^2 = \gamma_0 (1 - \phi_1 \rho_1 - \dots - \phi_p \rho_p)$。

## 5. 跨学科链接与双链
- **上游知识**：必须先理解 [[自回归模型(AR)]] 和 [[自相关函数ACF.md]]。
- **下游知识**：它是计算 [[偏自相关函数(PACF)]] 的底层原理，也是 DSP 中求解线性预测编码 (LPC) 滤波器的数学基础。
- **计算提速**：对于高阶 Toeplitz 系统，可用 Levinson-Durbin 算法把经典直接求解的计算量降到 $O(p^2)$；该算法保留为待创建专题。

## 6. 费曼自测清单 (Active Recall)
- [ ] Yule-Walker 方程的核心作用是什么？它连接了哪两个重要物理量？
- [ ] 请手推一遍 $k>0$ 时，公式两边同乘 $X_{t-k}$ 取期望，为什么最后一项误差项会消失？
- [ ] Yule-Walker 方程能用来估计 MA 模型的参数吗？为什么不能？
- [ ] 为什么要计算白噪声方差？如何用解出来的参数去倒推它？
