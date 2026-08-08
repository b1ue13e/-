---
type: study
topic: "ICR"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段3-移动机器人与车辆模型]]"
flow: knowledge
kind: concept
concept: ["ICR", "瞬时旋转中心", "运动学"]
prerequisites: ["差分驱动", "线速度", "角速度"]
related: ["差分驱动", "阿克曼几何", "单轮车模型"]
upstream: ["[[差分驱动]]"]
source: "Modern Robotics (Lynch & Park), Ch.13; 经典运动学"
tags: [学习, 控制与机器人学, 移动机器人]
---

# ICR（瞬时旋转中心）

## 0. 为什么学它

任意刚体平面运动，在每一瞬间都等价于绕某一点（**瞬时旋转中心 ICR**）做圆周运动。ICR 把"速度 + 角速度"统一成"绕一个点旋转"，是理解差分驱动、阿克曼转向、全向轮的几何统一视角。

## 1. 核心定义

**ICR**：刚体上瞬时速度为零的点。刚体任意点的速度 = 绕 ICR 的圆周速度：

$$v_p = \omega \times (p - p_{ICR}).$$

对机器人（线速度 $v$、角速度 $\omega$），ICR 在机器人坐标系中的位置：

$$p_{ICR}=\left(0,\ \frac{v}{\omega}\right)\quad(\text{沿 y 轴，距离 }v/\omega).$$

- $v/\omega > 0$：ICR 在左侧；
- $v=0$：原地旋转，ICR 在自身位置；
- $\omega=0$：直线运动，ICR 在无穷远。

## 2. 最小可手算例子

**题目**：机器人 $v=1$ m/s、$\omega=0.5$ rad/s，求 ICR 位置与转弯半径。

**解**：转弯半径 $R=\frac{v}{\omega}=\frac{1}{0.5}=2$ m；ICR 在机器人坐标系 $(0,2)$ 处。机器人绕该点以 2m 半径做圆周运动。

**易错点**：ICR 随 $v,\omega$ 变化（瞬时）；$\omega\to0$ 时 ICR 趋于无穷。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| ICR 是固定点 | 瞬时点，随运动变化 |
| 直线运动有 ICR 在原点 | $\omega=0$ 时 ICR 在无穷远 |
| 忽略 $v/\omega$ 符号 | 符号决定转向方向 |

## 4. 与后续知识连接

- [[差分驱动]]：$v,\omega\to$ ICR；
- [[阿克曼几何]]：四轮转向的 ICR 唯一性约束；
- [[单轮车模型]]：ICR 的简化；
- 工程：圆弧路径跟踪、曲率控制。

## 5. 检索练习（闭卷）

1. 写出 ICR 位置公式；
2. 求 $v=2,\omega=1$ 的转弯半径；
3. 说明原地旋转与直线的 ICR；
4. ICR 如何统一差分与阿克曼转向。

## 6. 通过标准

- 能由 $v,\omega$ 求 ICR 与半径；
- 能解释 ICR 的瞬时性；
- 能理解其几何统一作用。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重算 ICR；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
