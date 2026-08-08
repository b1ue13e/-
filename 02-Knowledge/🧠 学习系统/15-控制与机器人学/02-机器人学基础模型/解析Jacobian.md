---
type: study
topic: "解析Jacobian"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段2-机器人学基础模型]]"
flow: knowledge
kind: derivation
concept: ["解析Jacobian", "欧拉角", "速度映射"]
prerequisites: ["几何Jacobian", "欧拉角"]
related: ["几何Jacobian", "奇异位形"]
upstream: ["[[几何Jacobian]]"]
source: "Modern Robotics (Lynch & Park), Ch.5; Craig Ch.5"
tags: [学习, 控制与机器人学, 机器人学]
---

# 解析Jacobian

## 0. 为什么学它

几何 Jacobian 的角速度 $\omega$ 是物理向量；但任务空间常用**欧拉角及其导数**（如 $\dot\alpha,\dot\beta,\dot\gamma$）来描述末端姿态变化率。**解析 Jacobian** $J_a$ 把 $\dot q$ 映射到"位置 + 欧拉角速率"，便于直接用姿态误差做控制。

## 1. 核心定义

$$X=\begin{pmatrix}p\\\phi\end{pmatrix}\quad(\phi=\text{欧拉角}),\qquad \dot X=J_a(q)\,\dot q.$$

**与几何 J 的关系**：$\omega = E(\phi)\,\dot\phi$（欧拉角速率到角速度的变换矩阵），故

$$J_a = \begin{pmatrix}I&0\\0&E^{-1}(\phi)\end{pmatrix}J.$$

对 ZYX 欧拉角：$E=\begin{pmatrix}0&-\sin\alpha&\cos\alpha\sin\beta\\0&\cos\alpha&\sin\alpha\sin\beta\\1&0&\cos\beta\end{pmatrix}$（具体形式随约定而变）。

## 2. 关键差异

| 项 | 几何 J | 解析 J |
|:---|:---|:---|
| 输出旋转分量 | 角速度 $\omega$（物理向量） | 欧拉角速率 $\dot\phi$ |
| 构造 | 轴向量叉积 | 几何 J 乘 $E^{-1}$ |
| 奇异 | 机械奇异（J 秩亏） | 机械奇异 + 欧拉角奇异（如 $\beta=90°$ 时 $E$ 奇异） |

## 3. 最小可手算例子

**题目**：ZYX 欧拉角，$\beta=90°$ 时 $E$ 是否奇异？

**解**：$E$ 的第 3 列 $\cos\beta=0$，且 $\beta=90°$ 时 $E$ 行列式 $\det E=-\cos\beta=0$ → **奇异**。这正是 [[万向锁]] 在 Jacobian 层面的体现：姿态速率无法唯一映射。

**易错点**：把 $E$ 奇异误当作机械奇异；$E$ 形式随欧拉角约定不同。

## 4. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 解析 J 比几何 J 更"正确" | 两者等价，只是输出坐标系/表示不同 |
| $E$ 形式固定 | 依赖欧拉角约定（ZYX/XYZ…） |
| 忽略欧拉角奇异 | 万向锁附近 $E$ 病态 |

## 5. 与后续知识连接

- [[几何Jacobian]]：基础；
- [[万向锁]]：欧拉角奇异；
- [[奇异位形]]：机械奇异；
- 工程：视觉伺服（image-based）常用解析 J。

## 6. 检索练习（闭卷）

1. 写出 $J_a$ 与 $J$ 的关系；
2. 说明 $E$ 矩阵的作用；
3. 解释解析 J 为何含两类奇异；
4. 何时优先用解析 J。

## 7. 通过标准

- 能由几何 J 构造解析 J；
- 能解释 $E$ 与欧拉角奇异；
- 能区分两类奇异。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重推 $E$ 关系；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
