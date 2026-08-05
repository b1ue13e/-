---
type: project
topic: "MIT 6.7960 Homework 2 逐题知识点映射"
created: 2026-08-05
status: active
progress: 0%
tags: [项目, 45-生成式AI基础与Prompt工程, MIT-OCW, HW02]
flow: project
kind: moc
source: "MIT OCW 6.7960 Deep Learning Fall 2024 Homework 2, CC BY-NC-SA 4.0"
---

# MIT 6.7960 Homework 2 逐题知识点映射

> [!info] [打开官方 HW2 PDF](https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/mit6_7960_f24_hw2.pdf)。本页不复制题面或答案；HW2 是优化、归纳偏置与 GNN 扩展，不是 Prompt 入门硬门槛。

| 题号 | 官方主题摘要 | 必需知识 | 对应补救/迁移 |
| :---: | :--- | :--- | :--- |
| Q1 | 对偶范数 | 范数、Hölder 不等式 | [[深度学习数学-对偶范数谱范数PowerIteration与最速下降]] |
| Q2 | 最速下降的对偶形式 | 约束优化、对偶 | [[深度学习数学-对偶范数谱范数PowerIteration与最速下降]] |
| Q3 | $\ell_p$ 范数下最速下降 | $p/q$ 对偶、取等方向 | [[深度学习数学-对偶范数谱范数PowerIteration与最速下降]] |
| Q4 | 谱范数下最速下降 | SVD、谱/核范数对偶 | [[深度学习数学-对偶范数谱范数PowerIteration与最速下降]] |
| Q5 Bonus | 线性预测平方损失界 | 范数界、泛化 | [[深度学习数学-对偶范数谱范数PowerIteration与最速下降]]（Bonus 延伸） |
| Q6 | 高斯矩阵谱范数实验 | 随机矩阵、Power iteration、受控重复 | [[深度学习数学-对偶范数谱范数PowerIteration与最速下降]] |
| Q7 | 正交矩阵谱范数 | 正交性、奇异值 | [[深度学习数学-对偶范数谱范数PowerIteration与最速下降]] |
| Q8 | Power iteration | 主奇异值、收敛条件 | [[深度学习数学-对偶范数谱范数PowerIteration与最速下降]] |
| Q9 | 宽度间学习率迁移 | 参数化、方差 scale | [[深度学习工程-宽度缩放WeightDecay卷积与受控比较]] |
| Q10 Optional | steeper descent | 优化方向比较 | 最优化扩展 |
| Q11 | weight decay | 正则化、AdamW | [[深度学习工程-宽度缩放WeightDecay卷积与受控比较]]、[[训练优化-交叉熵AdamW调度梯度裁剪与检查点]] |
| Q12 | CNN 架构实现 | 卷积、shape、参数量 | [[深度学习工程-宽度缩放WeightDecay卷积与受控比较]] |
| Q13 | 训练与评估代码 | train/eval、单 batch、指标 | [[深度学习工程-宽度缩放WeightDecay卷积与受控比较]]、[[深度学习工程-PyTorch张量自动微分与训练循环]] |
| Q14 | 架构比较 | 公平对照、参数/FLOP、归纳偏置 | [[深度学习工程-宽度缩放WeightDecay卷积与受控比较]] |
| Q15 | 通用聚合函数 | 集合不变性、聚合碰撞 | [[图表示学习-不变聚合消息传递与手性边界]] |
| Q16 | MP-GNN 表达能力 | 消息传递、1-WL 边界 | [[图表示学习-不变聚合消息传递与手性边界]] |
| Q17 | 手性与图表示限制 | 对称性、三维反射、不可辨识 | [[图表示学习-不变聚合消息传递与手性边界]] |
| Q18 | 分子性质预测 | 图/3D 特征、回归评估、split | [[图表示学习-不变聚合消息传递与手性边界]] |

## 与本课程的关系

- **作业所需但非 Prompt 核心**：Q1–Q11 支撑训练优化；Q12–Q18 支撑归纳偏置与图数据。
- **Prompt/生成式 AI 迁移重点**：Q9、Q11、Q14，分别训练 scaling、优化器和受控比较意识。
- 完整答案只写在个人作业仓，不写入本导航页。

## Gate 与补救

- Q1–Q8：必须能手算一个 $\ell_p$ 最速方向、证明正交矩阵谱范数并让 Power iteration 通过 2×2 参考例。
- Q9–Q14：CNN 先通过 shape/参数量/单 batch 测试；架构比较必须报告参数与 FLOP。
- Q15–Q18：必须构造一种聚合碰撞和一个手性信息缺失解释，再进入分子预测。
