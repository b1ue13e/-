---
type: study
topic: "非线性车辆MPC"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-08
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段9-MPC深入]]"
flow: knowledge
kind: concept
concept: ["NMPC", "非线性优化"]
prerequisites: ["线性车辆MPC", "非线性预测"]
related: ["非线性预测", "线性车辆MPC", "显式MPC"]
upstream: ["[[09-MPC深入/线性车辆MPC]]", "[[09-MPC深入/非线性预测]]"]
source: "acados/CasADi 文档；车辆 NMPC 文献"
tags: [学习, 控制与机器人学, MPC]
---

# 非线性车辆MPC

> **一句话**：直接用非线性车辆模型做预测控制（NMPC）——大偏差、极限工况（漂移、紧急避障）下线性 MPC 失效时，NMPC 能救场，但计算代价大。

## 0. 为什么学它

线性 MPC 在正常工作点足够，但大航向偏差、漂移、紧急避障时线性化误差爆炸。NMPC 直接用非线性模型（含魔术公式轮胎）预测——精度高但求解难，本卡讲清何时需要与如何求解。

## 1. 何时需要 NMPC

| 场景 | 线性 MPC | NMPC |
|:---|:---|:---|
| 正常跟踪 | ✅ | 杀鸡用牛刀 |
| 大航向偏差 | ❌ 线性化失效 | ✅ |
| 漂移/极限 | ❌ | ✅（轮胎非线性） |
| 紧急避障 | 勉强 | ✅ |

## 2. 问题形式

$$\min_u \sum \ell(\mathbf{x}_k, \mathbf{u}_k) \quad \text{s.t.} \quad \mathbf{x}_{k+1} = f(\mathbf{x}_k, \mathbf{u}_k), \; \mathbf{x} \in \mathcal{X}, \; u \in \mathcal{U}$$

$f$：非线性车辆模型（自行车 + 魔术公式轮胎，见[[魔术公式]]/[[车辆动力学]]）。

## 3. 求解方法

| 方法 | 思路 |
|:---|:---|
| 序贯二次规划（SQP） | 每迭代线性化 → 子 QP |
| 实时迭代（RTI） | 每步只做一次 SQP 迭代（热启动） |
| 直接配点/打靶 | 离散化为 NLP 求解 |
| acados/CasADi | 现代高效 NMPC 框架 |

## 4. 关键难点

- **非凸性**：多局部最优，初值敏感 → 热启动至关重要（见[[热启动]]）；
- **计算量**：每周期解 NLP，实时压力大；
- **实现复杂度**：雅可比/黑塞计算、求解器集成。

## 5. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| NMPC 总是更好 | 正常工况线性 MPC 足够，NMPC 成本高 |
| NMPC 一定能实时 | 需 RTI/代码生成（见[[MPC代码生成]]）才可部署 |
| 线性 MPC 可随意替代 NMPC | 极限工况线性化失效，NMPC 不可替代 |

## 6. 工程取舍

- 先线性 MPC 打底，必要时 NMPC 增强；
- 或：线性 MPC + 约束/限幅兜底（工程主流）；
- 硬件升级（高性能 ECU）时 NMPC 才可行。

## 7. 检索练习（闭卷）

1. 说明 NMPC 适用边界；
2. 列出求解方法；
3. 说明工程取舍。

## 8. 通过标准

- 能判断何时用 NMPC；
- 能选择求解方法；
- 能说明工程部署。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；下次复习：与[[线性车辆MPC]]对照。
