---
type: study
topic: "Stanley公式"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: derivation
concept: ["Stanley", "横向控制", "几何跟踪"]
prerequisites: ["横向偏差", "自行车模型"]
related: ["Stanley前馈", "Stanley调参", "PP算法"]
upstream: ["[[运动学横向]]"]
source: "Stanford Stanley (2006); PythonRobotics stanley_control.py"
tags: [学习, 控制与机器人学, 横向控制]
---

# Stanley公式

## 0. 为什么学它

**Stanley 控制器**（斯坦福无人车）用**前轮中心**做跟踪点，转向角由**横向偏差 + 航向误差**两项构成：$\delta = e_\psi + \arctan(k e_y / v)$。相比 PP，Stanley 直接用偏差反馈，**跟踪更准、收敛更快**，是几何法中精度更高的方案。

## 1. 核心公式

**Stanley 控制律**（前轮中心为参考点）：

$$\delta(t) = \psi(t) + \arctan\left(\frac{k\, e_y(t)}{v(t)}\right),$$

- $\psi$：航向误差（车辆航向 − 路径切线角）；
- $e_y$：横向偏差（前轮中心到路径的垂距）；
- $k$：增益；$v$：纵向速度。

**两项含义**：
- $\psi$ 项：消除航向误差（对齐路径方向）；
- $\arctan$ 项：消除横向偏差（趋近路径），且 $\arctan$ 限幅避免大偏差时转角爆炸。

**离散处理**：$v\to0$ 时需防止除零（低速限制）。

## 2. 最小可手算例子

**题目**：$\psi=3°,\ e_y=0.5,\ k=1,\ v=10$，求 $\delta$。

**解**：$\arctan(1\times0.5/10)=\arctan(0.05)=2.86°$；$\delta=3°+2.86°=5.86°$。

**易错点**：$e_y$ 用前轮中心（不是后轴）；符号约定；低速除零。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 用后轴中心算 $e_y$ | Stanley 用前轮中心 |
| $\psi$ 与 $\arctan$ 项可互换 | 分工不同（对齐 vs 靠近） |
| $k$ 越大越好 | 过大振荡（见 [[Stanley调参]]） |

## 4. 与后续知识连接

- [[Stanley前馈]]：加前馈（曲率）；
- [[Stanley调参]]：$k$ 整定；
- [[Stanley低速]]、[[Stanley高速]]：工况；
- [[纯跟踪与Stanley控制器]]：综合。

## 5. 检索练习（闭卷）

1. 写出 Stanley 控制律；
2. 计算转向角；
3. 解释两项分工；
4. 与 PP 的差异。

## 6. 通过标准

- 能实现 Stanley；
- 能算转向角；
- 能理解两项语义。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重算转角；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
