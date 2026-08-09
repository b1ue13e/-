---
type: project
project_type: homework
course: "贝叶斯统计"
assignment_id: "贝叶斯统计-03"
assignment_level: lesson
assignment_format: lab
stage_id: "03"
requires:
  - "[[贝叶斯统计-层次模型与部分汇聚收缩机制]]"
  - "[[贝叶斯统计-PyMC概率编程工作流与参数推断]]"
source_type: local_integration_task
created: 2026-08-08
status: planned
flow: project
tags: [作业, 课后作业, 贝叶斯统计, Neal漏斗, 非中心化, 散度诊断]
---

# 贝叶斯统计-课后作业-03-Neal漏斗分歧诊断与非中心化参数化实验

> 所属阶段：[[03-层次模型与回归/🧭 阶段3-层次模型与回归|阶段3：层次模型与回归]]

---

## 1. 学习目标与任务定位
1. **掌握层次模型中组间方差参数导致的极端漏斗几何曲率**（Neal's Funnel）；
2. **掌握非中心化参数化 (Non-Centered Parameterization)** 确定性坐标变换代数机理；
3. **编写 Python 散度检测器与 PyMC 5.x 非中心化模型代码**，将数值 Divergence 降为 0。

---

## 2. 任务边界与执行环境
- **任务规模**：课后实验与诊断任务（`lesson` 规模）；
- **执行环境**：Python 3.10+ / NumPy / SciPy，核心脚本位于 `03-Projects/33-贝叶斯统计/scripts/hierarchical_shrinkage.py`；
- **自动化测试**：`03-Projects/33-贝叶斯统计/tests/test_hierarchical_shrinkage.py`。

---

## 3. 详细实验题目与步骤

### 题目 1：Neal 漏斗模拟与几何病态分析 (Lab 1)
1. 编写函数生成 Neal 漏斗分布样本：$y \sim \mathcal{N}(0, 3^2), \quad x_i \sim \mathcal{N}(0, \exp(y/2)^2)$；
2. 观察在 $y < -2$ 区域，条件标准差 $\sigma(x \mid y) = \exp(y/2)$ 的压缩幅度；
3. 解释为什么步长固定的 Leapfrog 辛积分器在此处必然发生数值飞逸。

### 题目 2：非中心化坐标变换 (Lab 2)
1. 令 $\tilde{x}_i \sim \mathcal{N}(0, 1)$，推导 $x_i = \exp(y/2) \cdot \tilde{x}_i$ 的联合密度；
2. 证明在新坐标系 $(\tilde{x}, y)$ 下，目标分布解耦为完全独立的正态流形，曲率处处均匀；
3. 编写代码验证非中心化表示能够实现 100% 自由探索而无采样散度。

---

## 4. 提交产物清单
1. 位于 `scripts/hierarchical_shrinkage.py` 的漏斗生成与散度检测函数实现；
2. 包含中心化与非中心化后验采样散点图对比的实验日志；
3. 单元测试全部通过的验证结果。

---

## 5. 验收标准与 Rubric
- **满分 (10分)**：完整写出非中心化代数推导，Python 诊断函数准确检测散度并全量通过自动化单元测试；
- **及格 (6–9分)**：完成参数化对比与代码运行，但对曲率爆炸原因阐述不完整；
- **不合格 (<6分)**：未完成坐标变换推导或测试失败。

---

## 6. 引导与自检
- [ ] 为什么在数据量极大（$N \to \infty$）时，中心化参数化反而优于非中心化参数化？
- [ ] 运行单元测试确认代码合规：`python -m unittest 03-Projects/33-贝叶斯统计/tests/test_hierarchical_shrinkage.py`。

