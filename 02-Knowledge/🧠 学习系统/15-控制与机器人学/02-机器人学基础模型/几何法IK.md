---
type: study
topic: "几何法IK"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段2-机器人学基础模型]]"
flow: knowledge
kind: derivation
concept: ["几何法IK", "逆运动学", "平面分解"]
prerequisites: ["解析逆运动学", "DH参数"]
related: ["数值IK", "IK多解"]
upstream: ["[[02-机器人学基础模型/解析逆运动学]]"]
source: "Modern Robotics (Lynch & Park), Ch.6; Craig Ch.4"
tags: [学习, 控制与机器人学, 机器人学]
---

# 几何法IK

## 0. 为什么学它

对平面/简单构型机械臂，用**几何关系 + 三角学**直接求关节角，比代数消元更直观、更快。它是解析逆运动学的直觉入口，也是理解高维机械臂"解耦"思想的起点。

## 1. 核心方法

把机械臂投影到平面，把 IK 问题转化为**三角形/多边形几何问题**：

- 2R 臂：由余弦定理求 $\theta_2$，由角度差求 $\theta_1$；
- 含偏置的臂：先几何求腕心，再逐关节分解；
- 球腕：位置解用几何（臂），姿态解用欧拉角分解（腕）。

## 2. 最小可手算例子（2R 平面臂几何解）

**题目**：$l_1=l_2=1$，目标 $(x,y)=(1,0)$，求关节角。

**解**：$r=\sqrt{x^2+y^2}=1$。$\cos\theta_2=\frac{r^2-l_1^2-l_2^2}{2l_1l_2}=\frac{1-1-1}{2}=-0.5$ → $\theta_2=\pm120^\circ$。
$\theta_1=\text{atan2}(y,x)-\text{atan2}(l_2\sin\theta_2,\ l_1+l_2\cos\theta_2)$：
- $\theta_2=+120^\circ$：$\sin=0.866,\cos=-0.5$ → $\text{atan2}(0.866,\ 1-0.5=0.5)=60^\circ$ → $\theta_1=0-60=-60^\circ$；
- $\theta_2=-120^\circ$：$\theta_1=+60^\circ$。

两组解 $(−60°,+120°)$ 与 $(+60°,−120°)$——肘上/肘下。

**易错点**：$\text{atan2}$ 的象限；多解都要保留。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 几何法只适合 2R | 平面化 + 解耦后可推广到 6DOF 臂 |
| 只取一组合理解 | 多解需按关节限位/奇异/能耗选择 |
| 忽略不可达 | $r>l_1+l_2$ 或 $r<\lvert l_1-l_2\rvert$ 时无解 |

## 4. 与后续知识连接

- [[解析逆运动学]]：一般化框架；
- [[数值IK]]：无法解析时的替代；
- [[IK多解]]：解的枚举与选择；
- [[机械臂DH参数与逆运动学]]：综合。

## 5. 检索练习（闭卷）

1. 用几何法重解 2R 臂 $\theta_2$；
2. 说明 $\text{atan2}$ 的作用；
3. 判断 $(x,y)=(3,0)$（$l_1=l_2=1$）是否可达；
4. 几何法如何扩展到球腕臂。

## 6. 通过标准

- 能用余弦定理/atan2 解 2R IK；
- 能判断可达性与多解；
- 能理解平面化解耦思想。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重解 2R；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
