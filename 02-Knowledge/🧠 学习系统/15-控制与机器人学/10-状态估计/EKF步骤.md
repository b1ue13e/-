---
type: study
topic: "EKF步骤"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-09
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段10-状态估计]]"
flow: knowledge
kind: concept
concept: ["EKF算法", "递推步骤"]
prerequisites: ["EKF非线性状态估计", "线性化", "雅可比计算"]
related: ["预测步", "更新步", "局部线性化"]
upstream:
  - "[[EKF非线性状态估计]]"
  - "[[线性化]]"
source: "Probabilistic Robotics (Thrun et al.) Ch.3 [待验证]；PythonRobotics ekf_localization.py"
tags: [学习, 控制与机器人学, 状态估计]
---

# EKF步骤

## 0. 为什么学它

"EKF 是什么"与"EKF 怎么跑"是两件事。本卡给出 EKF 的**完整可执行算法**：初始化后，"非线性预测 + 雅可比计算 + 线性更新"循环往复。它是从理论公式到代码实现的桥梁——照着这张卡的九步流程，就能写出 `ekf_localization.py` 那样的可运行滤波器。

## 1. 完整算法（九步循环）

**初始化**：$\hat{\mathbf{x}}_0, P_0$

**循环 $k = 0, 1, 2, \dots$**：

### 预测步（时间更新，每个控制周期都执行）
1. 状态传播：$\hat{\mathbf{x}}_{k+1}^- = f(\hat{\mathbf{x}}_k, \mathbf{u}_k)$
2. 计算雅可比：$F_k = \left.\partial f/\partial \mathbf{x}\right|_{\hat{\mathbf{x}}_k}$
3. 协方差传播：$P_{k+1}^- = F_k P_k F_k^\top + Q$

### 更新步（测量更新，有测量时才执行）
4. 预测测量：$\hat{\mathbf{z}} = h(\hat{\mathbf{x}}_{k+1}^-)$
5. 计算雅可比：$H_k = \left.\partial h/\partial \mathbf{x}\right|_{\hat{\mathbf{x}}^-}$
6. 新息：$r = \mathbf{z}_k - \hat{\mathbf{z}}$
7. 增益：$K = P^- H_k^\top (H_k P^- H_k^\top + R)^{-1}$
8. 状态更新：$\hat{\mathbf{x}}^+ = \hat{\mathbf{x}}^- + K r$
9. 协方差更新：$P^+ = (I - K H_k) P^-$

## 2. 与 KF 的结构对应

| KF | EKF |
|:---|:---|
| $A\hat{\mathbf{x}}$ | $f(\hat{\mathbf{x}})$ |
| $A$ | $F_k$（雅可比） |
| $H\hat{\mathbf{x}}$ | $h(\hat{\mathbf{x}})$ |
| $H$ | $H_k$（雅可比） |

**结构完全一致，只是用雅可比替换系统矩阵**——这就是"扩展（Extended）"的含义。

## 3. 工程注意

| 注意 | 说明 |
|:---|:---|
| 雅可比精度 | 解析优于数值差分（见 [[雅可比计算\|雅可比计算]]） |
| 测量缺失 | 只跑预测步（配合 [[采样率差异\|采样率差异]]） |
| 发散监控 | 新息检验、卡方门限（见 [[故障检测\|故障检测]]） |

## 4. 最小可手算例子（一步完整 EKF）

**题目**：一维系统 $f(x)=x$（匀速），$h(x)=x^2$，$Q=0.1, R=4$。$\hat{x}_0=2$，$P_0=1$，测量 $z=5$。

**解**：
- 步骤 1-3（预测）：$\hat{x}^- = 2$，$F = 1$，$P^- = 1 \times 1 \times 1 + 0.1 = 1.1$；
- 步骤 4-5：$\hat{z} = 2^2 = 4$，$H = 4$；
- 步骤 6：$r = 5 - 4 = 1$；
- 步骤 7：$K = \frac{1.1 \times 4}{4 \times 1.1 \times 4 + 4} = \frac{4.4}{21.6} \approx 0.204$；
- 步骤 8-9：$\hat{x}^+ = 2 + 0.204 \times 1 = 2.204$，$P^+ = (1 - 0.204 \times 4) \times 1.1 \approx 0.202$。

**解读**：九步完整走完一轮"预测-更新"；测量 $z=5$ 对应 $x \approx \pm 2.24$，估计向正方向修正到 2.204，$P$ 从 1.1 缩到 0.20。

## 5. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| "每步都必须更新" | 无测量时只跑预测步（步骤 1-3） |
| "$F$ 算一次就行" | 每步在当前估计处重算（状态变了，切线要重画） |
| "先更新再预测" | 顺序固定：预测 →（有测量才）更新 |
| "协方差公式抄 KF 的 $A$" | 用 $F_k$ 且预测均值用 $f$ 而非 $A\hat{x}$ |

## 6. 检索练习（闭卷）

1. 默写 EKF 九步流程；
2. 完成手算例子（换 $z=4.5$ 重算）；
3. 说出 EKF 与 KF 的四组结构对应；
4. 无测量时 EKF 只跑哪几步？

## 7. 通过标准

- 能默写并执行 EKF 九步；
- 能手算一步完整 EKF 迭代；
- 能对照 KF 说出四组差异；
- 能设计"测量缺失时"的运行策略。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：把九步流程与 `ekf_localization.py` 的代码逐行对应；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；
- 关联：[[雅可比计算\|雅可比计算]]、[[局部线性化\|局部线性化]]。
