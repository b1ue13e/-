---
type: study
topic: "几何Jacobian"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段2-机器人学基础模型]]"
flow: knowledge
kind: derivation
concept: ["几何Jacobian", "速度映射", "奇异位形"]
prerequisites: ["速度传递", "角速度", "线速度"]
related: ["解析Jacobian", "奇异位形", "力映射"]
upstream: ["[[02-机器人学基础模型/速度传递]]"]
source: "Modern Robotics (Lynch & Park), Ch.5"
tags: [学习, 控制与机器人学, 机器人学]
---

# 几何Jacobian

## 0. 为什么学它

**Jacobian** $J(q)$ 是机器人学最重要的线性化工具：它把关节速度映射到末端速度 $V=J(q)\dot q$，把末端力映射到关节力矩 $\tau=J^\top F$。奇异位形分析、速度控制、静力学、可操作性全部建立在它之上。

## 1. 核心定义

**几何 Jacobian**（6×n）：末端速度旋量 = $J\dot q$，

$$V=\begin{pmatrix}\omega\\v\end{pmatrix}=J(q)\,\dot q,\qquad J=\begin{bmatrix}J_\omega\\J_v\end{bmatrix}.$$

**第 $i$ 列**（关节 $i$ 为单位速度时末端的角/线速度）：
- 旋转关节：$J_{\omega,i}=\hat z_{i-1}$，$J_{v,i}=\hat z_{i-1}\times (p_{end}-p_{i-1})$；
- 移动关节：$J_{\omega,i}=0$，$J_{v,i}=\hat z_{i-1}$。

其中 $\hat z_{i-1}$ 为关节轴单位向量（基座系），$p_{i-1}$ 为关节原点（基座系）。

## 2. 最小可手算例子（2R 平面臂）

**题目**：求 2R 臂几何 Jacobian（$l_1=l_2=1$，平面运动，姿态仅绕 z）。

**解**：$J_\omega=\begin{bmatrix}1&1\end{bmatrix}$（两旋转关节均绕 z）。
$J_v=\begin{bmatrix}-\sin\theta_1&-\sin(\theta_1+\theta_2)\\ \cos\theta_1&\cos(\theta_1+\theta_2)\end{bmatrix}$（由 $v=J_v\dot q$ 推导或速度传递读取）。

验证 $V=J\dot q$ 与 [[速度传递]] 结果一致 ✓。

**易错点**：$J_v$ 的叉积方向与 $p_{end}-p_{i-1}$ 的相对位置；列顺序与关节顺序对应。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| Jacobian 是方阵 | 一般 $6\times n$（冗余 $n>6$、欠驱动 $n<6$） |
| 与解析 Jacobian 混淆 | 几何 J 直接由轴/位置构造，不依赖姿态参数化 |
| 忽略奇异 | $\det(JJ^\top)=0$ 时速度映射退化 |

## 4. 与后续知识连接

- [[解析Jacobian]]：姿态用欧拉角时的变体；
- [[奇异位形]]：$J$ 秩亏；
- [[力映射]]：$\tau=J^\top F$；
- [[可操作性]]：$\sqrt{\det(JJ^\top)}$；
- [[数值IK]]：伪逆迭代。

## 5. 检索练习（闭卷）

1. 写出几何 J 每列公式（旋转/移动关节）；
2. 构造 2R 臂 J；
3. 说明 $J$ 的尺寸与奇异条件；
4. 区分几何与解析 Jacobian。

## 6. 通过标准

- 能构造任意臂的几何 J；
- 能验证 $V=J\dot q$；
- 能由 J 判断奇异与可操作性。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重构造 2R J；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
