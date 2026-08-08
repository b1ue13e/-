---
type: study
topic: "Frenet转换"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-08
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段8-轨迹与路径跟踪]]"
flow: knowledge
kind: concept
concept: ["坐标变换", "最近点投影"]
prerequisites: ["参考线", "s坐标", "d坐标"]
related: ["Frenet横向", "Frenet纵向", "Frenet误差"]
upstream: ["[[参考线]]", "[[s坐标]]", "[[d坐标]]"]
source: "Werling et al. Frenet 框架论文；PythonRobotics frenet_optimal_trajectory（MIT）"
tags: [学习, 控制与机器人学, Frenet]
---

# Frenet转换

> **一句话**：笛卡尔坐标 $(x,y)$ 与 Frenet 坐标 $(s,d)$ 互转，核心是"找最近投影点"。

## 0. 为什么学它

传感器给的是笛卡尔坐标，规划器在 Frenet 系里工作，控制器又要吃笛卡尔参考——**每一次规划迭代都要在两套坐标间来回切换**。转换公式里的速度分解与奇异条件，直接决定轨迹采样是否可信。

## 1. 笛卡尔 → Frenet（正变换）

**第 1 步：找投影点**。求解最近点：

$$s^* = \arg\min_s \lVert \mathbf{p} - \mathbf{r}(s) \rVert$$

工程上：离散搜索 + 牛顿迭代精化。

**第 2 步：算横向偏差**：

$$d = (\mathbf{p} - \mathbf{r}(s^*)) \cdot \mathbf{n}(s^*)$$

**第 3 步：纵向速度分解**（需要 $\dot{s}, \dot{d}$）：

$$\dot{s} = \frac{v\cos(\theta - \theta_r)}{1 - \kappa_r d}, \qquad \dot{d} = v\sin(\theta - \theta_r)$$

其中 $\theta$：车航向，$\theta_r$：参考线切线角。

## 2. Frenet → 笛卡尔（逆变换）

$$\mathbf{p} = \mathbf{r}(s) + d\,\mathbf{n}(s)$$

航向与曲率修正：

$$\theta = \theta_r + \arctan\left( \frac{\dot{d}}{\dot{s}} \right)$$

$$\kappa = \frac{\kappa_r + \frac{d''}{(1-\kappa_r d)^2}}{\sqrt{1+(d'/\dot{s})^2}} \cdot \text{修正}$$

## 3. 高阶量换算

给定 $d, d', d''$（对 $s$ 的导数）与参考线 $\kappa_r$：

$$\dot{d} = d' \dot{s}, \qquad \ddot{d} = d'' \dot{s}^2 + d' \ddot{s}$$

$$v = \sqrt{\dot{s}^2 + \dot{d}^2}$$

## 4. 最小可手算例子（正变换）

**题目**：参考线为 x 轴（$\theta_r = 0, \kappa_r = 0$），车在 $(3, 4)$，航向 $\theta = 90°$，车速 $v = 5$。求 $(s, d, \dot{s}, \dot{d})$。

**步骤**：
1. 投影点 $(3,0)$ → $s = 3$，$d = 4$；
2. $\dot{s} = \dfrac{v\cos(\theta-\theta_r)}{1 - 0} = 5\cos90° = 0$；$\dot{d} = 5\sin90° = 5$；
3. 含义：车垂直于参考线行驶——纵向不前进、横向远离，$v = \sqrt{0^2+5^2} = 5$ ✓。

**对照**：若 $\theta = 0°$，则 $\dot{s}=5,\ \dot{d}=0$——车沿参考线走，$d$ 不变。

## 5. 奇异点

- $1 - \kappa_r d = 0$：点在参考线曲率圆心 → 转换发散（远离参考线时易发生）；
- 投影不唯一：参考线曲率大或点距参考线远时，多个局部最近点。

## 6. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 把 $s$ 直接取为 $x$ | 仅在参考线为平行 x 轴的直线时成立 |
| 忽略 $1-\kappa_r d$ 分母 | 弯道+大偏移时该因子显著，忽略会算错 $\dot{s}$ |
| 高曲率区暴力投影 | 应做多起点投影并选距离最小者，避免局部次优 |

## 7. 检索练习（闭卷）

1. 写出正变换三步与速度分解公式；
2. 手算：参考线为 x 轴，$(3,4)$、$\theta=90°$、$v=5$ 的 $(s,d,\dot{s},\dot{d})$；
3. 说明奇异条件 $1-\kappa_r d=0$ 的物理含义。

## 8. 通过标准

- 能完成笛卡尔 ↔ Frenet 互转（含速度分解）；
- 能识别并解释奇异条件；
- 能说明逆变换的曲率修正。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；下次复习：重做一次正变换手算。
