---
type: study
topic: "线性ODE"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: beginner
stage_moc: "[[🧭 阶段1-控制地基]]"
flow: knowledge
kind: concept
concept: ["线性常微分方程", "特征方程", "叠加原理"]
prerequisites: ["ODE基础"]
related: ["拉氏变换", "传递函数", "二阶系统"]
upstream: ["[[ODE基础]]"]
source: "Modern Control Engineering (Ogata), Ch.2"
tags: [学习, 控制与机器人学, 微分方程]
---

# 线性ODE

## 0. 为什么学它

控制系统建模后大多是**线性常系数 ODE**：$\ddot{x}+a_1\dot{x}+a_0 x = b u$。线性 ODE 之所以重要，是因为它满足**叠加原理**——这使系统的响应可以分解为"零输入响应 + 零状态响应"，也让拉氏变换（线性算子）得以施展。特征方程则直接揭示解的形态。

## 1. 核心定义

**n 阶线性常系数 ODE**：

$$x^{(n)} + a_{n-1}x^{(n-1)} + \cdots + a_1\dot{x} + a_0 x = b_m u^{(m)} + \cdots + b_0 u.$$

**齐次方程**：右边 = 0（自由运动）；**非齐次方程**：右边 ≠ 0（受迫运动）。

**通解结构**：$x(t) = x_h(t) + x_p(t)$，其中 $x_h$ 为齐次通解（自由模态），$x_p$ 为一个特解（强迫响应）。

## 2. 齐次解与特征方程

令 $x = e^{\lambda t}$ 代入齐次方程，得**特征方程**：

$$\lambda^n + a_{n-1}\lambda^{n-1} + \cdots + a_1\lambda + a_0 = 0.$$

| 特征根类型 | 模态 $x_h$ 项 | 工程含义 |
|:---|:---|:---|
| 相异实根 $\lambda_i$ | $C_i e^{\lambda_i t}$ | 指数衰减/增长 |
| 重根 $\lambda$（重数 k） | $(C_0+C_1t+\cdots)t^{k-1}e^{\lambda t}$ | 多项式×指数 |
| 共轭复根 $\sigma\pm j\omega$ | $e^{\sigma t}(A\cos\omega t+B\sin\omega t)$ | 振荡+衰减 |

## 3. 最小可手算例子

**题目**：$\ddot{x}+5\dot{x}+6x=0,\ x(0)=1,\ \dot{x}(0)=0$。

**解**：特征方程 $\lambda^2+5\lambda+6=0 \Rightarrow \lambda=-2,-3$。
通解 $x=C_1e^{-2t}+C_2e^{-3t}$。
由初值：$C_1+C_2=1$，$-2C_1-3C_2=0 \Rightarrow C_1=3,\ C_2=-2$。
故 $x(t)=3e^{-2t}-2e^{-3t}$（两个衰减模态，无振荡）。

**易错点**：初值条件代入的是**通解**而非特解；重根时漏掉 $t^k$ 因子。

## 4. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 把非线性方程当线性解 | 叠加原理只对线性方程成立 |
| 重根只写 $Ce^{\lambda t}$ | 重根 k 次需 $t$ 多项式因子 |
| 忽略稳态特解 | 非齐次方程缺 $x_p$ 时通解不完整 |

## 5. 与后续知识连接

- [[ODE基础]]：本卡的入门；
- [[拉氏变换]]：用代数方法求解同一类方程（更强大）；
- [[传递函数]]：由 ODE 系数直接写出；
- [[二阶系统]]：二阶线性 ODE 的标准形。

## 6. 检索练习（闭卷）

1. 写出二阶线性齐次 ODE 通解结构；
2. 解 $\ddot{x}+4\dot{x}+4x=0$（重根情形）并说明模态形式；
3. 解释叠加原理为何只在线性方程成立；
4. 由 $\ddot{x}+2\zeta\omega_n\dot{x}+\omega_n^2x=0$ 的根判断阻尼类型。

## 7. 通过标准

- 能写出线性 ODE 通解结构并求解齐次方程；
- 能处理相异实根、重根、复根三类模态；
- 能代入初值确定任意常数；
- 能说出线性性对叠加原理的意义。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重做检索练习 2；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
