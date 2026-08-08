---
type: study
topic: "PP算法"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: derivation
concept: ["Pure Pursuit", "横向控制", "几何跟踪"]
prerequisites: ["圆弧逼近", "预瞄距离"]
related: ["PP曲率", "PP转向角", "PP稳定性"]
upstream: ["[[圆弧逼近]]"]
source: "Coulter (1992); PythonRobotics pure_pursuit.py"
tags: [学习, 控制与机器人学, 横向控制]
---

# PP算法（Pure Pursuit）

## 0. 为什么学它

**Pure Pursuit（纯跟踪）**是最经典的几何横向控制器：瞄准前视点、按圆弧跟踪。实现简单、参数少、对路径平滑度不敏感，是低速路径跟踪（AGV、扫地机、赛车线）的默认方案。

## 1. 核心算法

1. 在路径上找**前视点**：距车辆 $l_d$ 的点；
2. 计算前视方位角 $\alpha$（车辆航向与前视方向的夹角）；
3. 由圆弧几何算曲率 $\kappa=\dfrac{2\sin\alpha}{l_d}$；
4. 转向角 $\delta=\arctan(\kappa L)$；
5. 执行，下个周期重复。

**伪代码**：

```
target = find_point_at_distance(path, l_d, vehicle_pose)
alpha = angle_between(vehicle_heading, direction_to(target))
kappa = 2 * sin(alpha) / l_d
delta = atan2(kappa * L, 1)
```

## 2. 最小可手算例子

**题目**：$L=2.5,\ l_d=8,\ \alpha=10°$，求 $\delta$。

**解**：$\kappa=\frac{2\sin10°}{8}=\frac{0.347}{8}=0.0434$；$\delta=\arctan(0.0434\times2.5)=6.2°$。

**易错点**：$\alpha$ 符号（左右）；$l_d$ 过小 → 振荡，过大 → 切弯（见 [[PP稳定性]]）。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 前视点必须在正前方 | 是距车 $l_d$ 的路径点（含侧面） |
| $l_d$ 固定 | 应随 $v$ 增大：$l_d=kv$ |
| 高速也适用 | 高速需增大前视或换动力学法 |

## 4. 与后续知识连接

- [[PP曲率]]、[[PP转向角]]：细节；
- [[PP稳定性]]：前视与稳定；
- [[预瞄距离]]：参数整定；
- [[纯跟踪与Stanley控制器]]：综合对比。

## 5. 检索练习（闭卷）

1. 写出 PP 算法五步；
2. 计算转向角；
3. 说明前视距离作用；
4. 与 Stanley 的区别。

## 6. 通过标准

- 能实现 PP；
- 能算转向角；
- 能整定前视距离。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重写伪代码；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
