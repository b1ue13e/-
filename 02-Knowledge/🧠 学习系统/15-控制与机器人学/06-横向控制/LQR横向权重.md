---
type: study
topic: "LQR横向权重"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: problem-type
concept: ["LQR横向", "权重", "误差权衡"]
prerequisites: ["LQR横向状态", "LQR代价函数"]
related: ["LQR横向状态", "LQR横向增益"]
upstream: ["[[LQR横向状态]]"]
source: "自动驾驶横向控制工程实践; PythonRobotics"
tags: [学习, 控制与机器人学, 横向控制]
---

# LQR横向权重

## 0. 为什么学它

横向 LQR 的 $Q,R$ 决定"快速纠偏 vs 平顺转向"的权衡。**LQR 横向权重**给出面向路径跟踪的权重选择方法（$e_y$ 权重、$e_\psi$ 权重、转向权重），让控制器"该硬时硬、该柔时柔"。

## 1. 权重设计与直觉

**权重矩阵**（对角常用）：$Q=\text{diag}(q_{ey},\ q_{\dot ey},\ q_{e\psi},\ q_{\dot e\psi})$，$R=[r_\delta]$。

| 权重 | 惩罚对象 | 调大效果 |
|:---|:---|:---|
| $q_{ey}$ | 横向偏差 | 更快归线，但转向剧烈 |
| $q_{e\psi}$ | 航向误差 | 车头更贴路径方向 |
| $q_{\dot e\psi}$ | 横摆速率 | 抑制转向抖动 |
| $r_\delta$ | 转向角 | 平顺省力，偏差变大 |

**初值**（Bryson）：按量级 $q_{ey}=1/e_{y,max}^2$ 等。

**工程倾向**：$q_{ey}$ 与 $q_{e\psi}$ 同量级，$r_\delta$ 决定"贴线 vs 平顺"——乘坐舒适性常要求 $r_\delta$ 较大。

## 2. 最小可手算例子（决策练习）

**题目**：跟踪"急贴线但平顺"，如何设权重？

**解**：$q_{ey}$ 中等（要收敛）、$q_{e\psi}$ 中等、$q_{\dot e\psi}$ 较大（抑制抖振）、$r_\delta$ 较大（转向温和）——牺牲一点精度换平顺。

**易错点**：$r_\delta$ 过大则弯道偏差大；只调单一权重忽略耦合。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| $Q$ 越大越好 | 过大转向饱和 |
| 权重与速度无关 | 高速宜降低偏差权重防抖 |
| 忽略 $q_{\dot e\psi}$ | 横摆抑制项影响舒适性 |

## 4. 与后续知识连接

- [[LQR横向增益]]：结果；
- [[LQR代价函数]]：权重原理；
- [[LQR调参]]：一般流程。

## 5. 检索练习（闭卷）

1. 列出横向权重及效果；
2. 给"平顺优先"设权重；
3. 说明 Bryson 初值；
4. 速度对权重的影响。

## 6. 通过标准

- 能设横向权重；
- 能权衡贴线/平顺；
- 能验证闭环。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重设权重；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
