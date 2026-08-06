---
type: study
topic: "PP曲率"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: derivation
concept: ["Pure Pursuit", "曲率", "几何跟踪"]
prerequisites: ["PP算法", "圆弧逼近"]
related: ["PP算法", "PP转向角"]
upstream: ["[[06-横向控制/PP算法]]"]
source: "Pure Pursuit 文献; PythonRobotics"
tags: [学习, 控制与机器人学, 横向控制]
---

# PP曲率

## 0. 为什么学它

Pure Pursuit 的"核心计算"就是**前视点曲率 $\kappa$**：它把车辆-前视点几何转成所需的转弯弯度。理解 $\kappa$ 公式的推导与量纲，才能正确实现与整定 PP。

## 1. 核心公式

**PP 曲率**：

$$\kappa=\frac{2\sin\alpha}{l_d},$$

- $\alpha$：车辆航向与前视方向夹角；
- $l_d$：前视距离。

**推导**（圆弧几何）：前视弦长 $l_d$，车辆转弯半径 $R$，由弦-切角关系 $\sin\alpha=\frac{l_d}{2R}=\frac{\kappa l_d}{2}$ 反解。

**极限检查**：
- $\alpha=0$（正对前视点）：$\kappa=0$ 直线行驶 ✓；
- $l_d\to0$：$\kappa$ 巨大（激进转向）；
- $\alpha$ 大：曲率大，急转弯。

## 2. 最小可手算例子

**题目**：$l_d=10,\ \alpha=20°$，求 $\kappa$ 与半径 $R$。

**解**：$\kappa=\frac{2\sin20°}{10}=0.0684$；$R=1/\kappa=14.6$ m。

**易错点**：$\alpha$ 用弧度；$l_d$ 与 $\kappa$ 量纲（m⁻¹）。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 曲率与 $l_d$ 成正比 | 反比（$l_d$ 大 → 缓弯） |
| $\alpha=0$ 也转弯 | 正对时直线 |
| 忽略符号 | $\alpha$ 符号决定左右转 |

## 4. 与后续知识连接

- [[PP算法]]：主流程；
- [[PP转向角]]：$\delta$ 计算；
- [[圆弧逼近]]：几何来源。

## 5. 检索练习（闭卷）

1. 写出 PP 曲率公式；
2. 计算 $\kappa,R$；
3. 极限检查三情形；
4. 与 $l_d$ 的关系。

## 6. 通过标准

- 能推/用曲率公式；
- 能做极限检查；
- 能理解量纲。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重算曲率；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
