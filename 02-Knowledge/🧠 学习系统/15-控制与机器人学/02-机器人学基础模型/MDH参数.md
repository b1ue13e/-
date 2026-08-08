---
type: study
topic: "MDH参数"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段2-机器人学基础模型]]"
flow: knowledge
kind: concept
concept: ["MDH参数", "改进DH", "连杆描述"]
prerequisites: ["DH参数"]
related: ["DH参数", "PUMA560"]
upstream: ["[[DH参数]]"]
source: "机器人学导论 (Craig) Ch.3; Modern Robotics Ch.4"
tags: [学习, 控制与机器人学, 机器人学]
---

# MDH参数

## 0. 为什么学它

Craig 在《机器人学导论》中使用**改进 DH（MDH）**约定，与标准 DH 相比坐标系附着位置不同，矩阵形式也不同。不同教材/库（如 ROS urdf 的某些版本、部分运动学库）混用两套约定——**用错约定是正运动学最常见的错误来源**。

## 1. 核心区别

| 项目 | 标准 DH | 改进 DH（Craig） |
|:---|:---|:---|
| $x_i$ 轴定义 | 沿 $z_{i-1}$ 与 $z_i$ 的公垂线 | 沿 $z_{i-1}$ 与 $z_i$ 的公垂线（附着到 $i-1$ 系） |
| 变换顺序 | 绕 $z_{i-1}$ 转 $\theta_i$、沿 $z_{i-1}$ 移 $d_i$、沿 $x_i$ 移 $a_i$、绕 $x_i$ 转 $\alpha_i$ | 先绕 $x_{i-1}$ 转 $\alpha_{i-1}$、沿 $x_{i-1}$ 移 $a_{i-1}$、绕 $z_i$ 转 $\theta_i$、沿 $z_i$ 移 $d_i$ |
| 矩阵形式 | $T=T_z(\theta)T_z(d)T_x(a)T_x(\alpha)$ 组合 | $T=T_x(\alpha)T_x(a)T_z(\theta)T_z(d)$ 组合 |
| 下标 | $a_i,\alpha_i,d_i,\theta_i$ | $a_{i-1},\alpha_{i-1},d_i,\theta_i$ |

## 2. 改进 DH 变换矩阵

$$T_{i-1,i}=\begin{pmatrix}
\cos\theta_i&-\sin\theta_i&0&a_{i-1}\\
\sin\theta_i\cos\alpha_{i-1}&\cos\theta_i\cos\alpha_{i-1}&-\sin\alpha_{i-1}&-d_i\sin\alpha_{i-1}\\
\sin\theta_i\sin\alpha_{i-1}&\cos\theta_i\sin\alpha_{i-1}&\cos\alpha_{i-1}&d_i\cos\alpha_{i-1}\\
0&0&0&1
\end{pmatrix}$$

## 3. 最小可手算例子

**题目**：对 2R 平面臂用改进 DH 建模。

**解**：$\alpha_0=0, a_0=0$（无扭转/长度），$d_1=d_2=0$：

| $i$ | $a_{i-1}$ | $\alpha_{i-1}$ | $d_i$ | $\theta_i$ |
|:---|:---|:---|:---|:---|
| 1 | 0 | 0 | 0 | $\theta_1$ |
| 2 | $l_1$ | 0 | 0 | $\theta_2$ |

注意与标准 DH 表的**下标不同**：$a_1=l_1$ 在标准 DH 中叫 $a_1$，改进 DH 中叫 $a_1$（表中第 2 行 $a_{1}=l_1$）——两表数值相同但语义下标体系不同，用错即错位。

**易错点**：把标准 DH 参数直接套进改进 DH 矩阵；忽略 $a_{i-1}$ 下标。

## 4. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 两套约定参数混填 | 先确认教材/库用哪套，再建表 |
| 矩阵形式用错 | 标准 DH 与改进 DH 的 $T$ 矩阵不同 |
| 忽略下标差异 | 改进 DH 的 $a,\alpha$ 是 $i-1$ 下标 |

## 5. 与后续知识连接

- [[DH参数]]：标准约定对比；
- [[PUMA560]]：完整实例（按所选约定）；
- [[机械臂DH参数与逆运动学]]：综合大卡；
- 工程：Craig 教材、部分 ROS 库使用改进 DH。

## 6. 检索练习（闭卷）

1. 对比标准 DH 与改进 DH 的三点差异；
2. 写出改进 DH 变换矩阵；
3. 用改进 DH 给 2R 臂建表；
4. 如何判断一个库用的是哪套约定。

## 7. 通过标准

- 能区分两套 DH 约定；
- 能按改进 DH 建表并求正解；
- 能识别用错约定的错误。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后对比两表；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
