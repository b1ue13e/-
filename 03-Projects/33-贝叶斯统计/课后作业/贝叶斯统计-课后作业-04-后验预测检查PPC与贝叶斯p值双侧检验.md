---
type: project
project_type: homework
course: "贝叶斯统计"
assignment_id: "贝叶斯统计-04"
assignment_level: lesson
assignment_format: problem-set
stage_id: "04"
requires:
  - "[[贝叶斯统计-后验预测检查与模型校准]]"
  - "[[贝叶斯统计-信息准则与模型比较]]"
source_type: local_integration_task
created: 2026-08-08
status: planned
flow: project
tags: [作业, 课后作业, 贝叶斯统计, PPC, 后验预测, 贝叶斯p值]
---

# 贝叶斯统计-课后作业-04-后验预测检查PPC与贝叶斯p值双侧检验

> 所属阶段：[[04-决策与实践/🧭 阶段4-决策与实践|阶段4：决策与实践]]

---

## 1. 学习目标与任务定位
1. **掌握后验预测检查 (PPC)** 蒙特卡洛全期望仿真生成机制 $y^{\text{rep}}$；
2. **掌握设计业务定制检验统计量 $T(y)$** 并计算贝叶斯 $p$ 值（$\hat{p}_B$）；
3. **编写 Python 自动化诊断代码** 评估模型在均值、极值与方差维度的校准度。

---

## 2. 任务边界与执行环境
- **任务规模**：课后推导与检验实验（`lesson` 规模）；
- **执行环境**：Python 3.10+ / NumPy / SciPy，核心脚本位于 `03-Projects/33-贝叶斯统计/scripts/bayes_glm_loo.py`；
- **自动化测试**：`03-Projects/33-贝叶斯统计/tests/test_bayes_glm_loo.py`。

---

## 3. 详细题目与公式推导

### 题目 1：贝叶斯 $p$ 值数学定义与判据 (Problem 1)
1. 给定观测数据 $y$ 与后验采样生成的 $S$ 套复制数据集 $\{y^{\text{rep},(s)}\}_{s=1}^S$，写出贝叶斯 $p$ 值的蒙特卡洛估计式：
   $$\hat{p}_B = \frac{1}{S} \sum_{s=1}^S I\left(T(y^{\text{rep},(s)}) \ge T(y)\right)$$
2. 证明当 $\hat{p}_B \approx 0.50$ 时表示完美校准，而 $\hat{p}_B < 0.05$ 或 $\hat{p}_B > 0.95$ 表示模型存在严重系统性系统失真（如未建模过离散或厚尾）。

### 题目 2：多统计量综合校准实验 (Problem 2)
1. 针对二项/逻辑回归模型，分别选择 $T_1(y) = \text{mean}(y)$、$T_2(y) = \max(y)$、$T_3(y) = \text{Var}(y)$；
2. 编写 Python 函数自动化计算三个统计量的贝叶斯 $p$ 值；
3. 验证模型在均值与方差维度均处于 $[0.05, 0.95]$ 的置信接受域。

---

## 4. 提交产物清单
1. 包含 PPC 生成与贝叶斯 $p$ 值计算的 Python 函数实现；
2. 检验统计量极值分析与模型校准判断报告；
3. 单元测试全部通过的验证结果。

---

## 5. 验收标准与 Rubric
- **满分 (10分)**：完整写出检验统计量与极值积分公式，代码正确计算 $\hat{p}_B$ 并全量通过单元测试；
- **及格 (6–9分)**：完成 PPC 计算但对非对称极值检验统计量的选取说明不足；
- **不合格 (<6分)**：未实现复制数据生成或代码报错。

---

## 6. 引导与自检
- [ ] 为什么频率学派的 $p$ 值服从均匀分布 $U(0, 1)$，而保守的贝叶斯 $p$ 值往往向中心 0.5 集中？
- [ ] 运行单元测试确认代码合规：`python -m unittest 03-Projects/33-贝叶斯统计/tests/test_bayes_glm_loo.py`。

