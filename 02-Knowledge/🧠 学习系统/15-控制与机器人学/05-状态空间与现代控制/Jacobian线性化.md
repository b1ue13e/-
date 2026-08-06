---
type: study
topic: "Jacobian线性化"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段5-状态空间与现代控制]]"
flow: knowledge
kind: derivation
concept: ["Jacobian线性化", "泰勒展开", "非线性系统"]
prerequisites: ["状态方程", "微积分基础"]
related: ["小扰动分析", "车辆线性化"]
upstream: ["[[05-状态空间与现代控制/状态方程]]"]
source: "Modern Control Engineering (Ogata) Ch.9"
tags: [学习, 控制与机器人学, 状态空间]
---

# Jacobian线性化

## 0. 为什么学它

真实系统几乎都是非线性的 $\dot x=f(x,u)$，而设计工具（LQR、极点配置）需要线性模型。**Jacobian 线性化**在工作点附近做泰勒展开，得到线性状态空间——是"非线性 → 线性"的标准桥梁。

## 1. 核心方法

对 $\dot x=f(x,u)$，在平衡点 $(x_0,u_0)$（$f(x_0,u_0)=0$）展开：

$$A=\frac{\partial f}{\partial x}\Big|_{(x_0,u_0)},\qquad B=\frac{\partial f}{\partial u}\Big|_{(x_0,u_0)},$$

$$\Delta\dot x = A\Delta x+B\Delta u,\qquad \Delta x=x-x_0.$$

**线性化方程**：$\Delta\dot x = A\Delta x + B\Delta u$（在平衡点邻域有效）。

**有效范围**：小扰动；大偏离/分岔点处线性化失效。

## 2. 最小可手算例子

**题目**：单摆 $\ddot\theta=-\frac{g}{l}\sin\theta$ 在 $\theta=0$ 线性化。

**解**：状态 $x=(\theta,\dot\theta)$：$f=\begin{pmatrix}\dot\theta\\-\frac{g}{l}\sin\theta\end{pmatrix}$。
$\frac{\partial f}{\partial x}=\begin{pmatrix}0&1\\-\frac{g}{l}\cos\theta&0\end{pmatrix}$，在 $\theta=0$：$A=\begin{pmatrix}0&1\\-\frac{g}{l}&0\end{pmatrix}$ ✓（小角度单摆线性方程）。

**易错点**：必须在平衡点（$f=0$）展开；$\cos\theta\approx1$ 只在 $\theta\approx0$ 成立。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 线性化全局有效 | 仅平衡点邻域，大扰动失效 |
| 平衡点选错 | 必须 $f(x_0,u_0)=0$ |
| 忽略高阶项 | 泰勒展开舍高阶项即近似 |

## 4. 与后续知识连接

- [[小扰动分析]]：线性化前提；
- [[车辆线性化]]：车辆应用；
- [[Lyapunov稳定]]：非线性稳定性（线性化仅局部）；
- [[LQR代价函数]]：线性模型 → LQR。

## 5. 检索练习（闭卷）

1. 写出线性化公式；
2. 线性化单摆；
3. 说明有效范围；
4. 平衡点条件。

## 6. 通过标准

- 能做 Jacobian 线性化；
- 能确定平衡点；
- 能说明近似边界。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重做线性化；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
