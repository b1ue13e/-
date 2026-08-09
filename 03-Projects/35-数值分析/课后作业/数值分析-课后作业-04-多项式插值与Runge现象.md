---
type: project
project_type: homework
course: "数值分析"
assignment_id: "数值分析-HW04"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[02-插值积分与逼近/数值分析-多项式插值与Chebyshev节点|数值分析-多项式插值与Chebyshev节点]]"]
source_type: official_assignment
created: 2026-08-08
updated: 2026-08-08
status: active
flow: project
tags: [作业, 课后作业, 数值分析, 多项式插值, Runge现象, Chebyshev节点]
---

# 数值分析-课后作业-04-多项式插值与Runge现象

> 对齐官方源：**MIT 18.330 Problem Set 2 (Polynomial & Chebyshev Interpolation)** 与 **FNC Chapter 4**

---

## 1. 学习目标与动机
- 复现经典 Runge 震荡现象并测量等距插值算子的 Lebesgue 常数爆炸；
- 独立编写基于 Chebyshev 零点节点的重心拉格朗日第二型（Barycentric Form II）插值器；
- 验证 Chebyshev 插值在解析函数上的指数级谱收敛性。

---

## 2. 任务边界与输入输出
- **输入**：目标测试函数 $f(x) = \frac{1}{1 + 25x^2}$，区间 $[-1, 1]$，节点数量 $N \in [5, 50]$。
- **输出**：在 1000 个密集评估点上的最大范数误差 $\|f - P_N\|_\infty$ 对比表与对数收敛曲线。

---

## 3. 详细实验任务与算法规范

### 任务 1：等距多项式插值发散复现
使用等距节点 $x_j = -1 + \frac{2j}{N}$，观察随着 $N$ 从 5 增加至 30 时，插值多项式在端点 $x \approx \pm 1$ 处的剧烈震荡现象。

### 任务 2：Chebyshev 零点重心插值器
实现类 `BarycentricChebyshevInterpolator`，利用权重 $w_k = (-1)^k \sin\left( \frac{2k+1}{2N} \pi \right)$ 在 $O(N)$ 复杂度下评估任意点函数值。

### 任务 3：误差收敛阶双对数分析
记录两种节点配置下误差随 $N$ 的变化趋势，绘制 $\log_{10}(\text{Error})$ 对 $N$ 散点图。

---

## 4. 提交产物与代码规范
- 代码文件：`03-Projects/35-数值分析/scripts/hw04_interpolation_runge.py`
- 自动化测试：集成至 `03-Projects/35-数值分析/tests/test_numerical_analysis.py`

---

## 5. 验收标准（Rubric）

| 验收维度 | 达标分 | 满分要点 |
| :--- | :---: | :--- |
| **Runge 发散复现** | 30 | 等距插值在 $N=25$ 时端点误差大于 $10^2$ 并正确捕获发散 |
| **Chebyshev 重心实现** | 40 | 重心算法在 $N=25$ 时最大误差小于 $10^{-3}$，在 $N=50$ 时小于 $10^{-7}$ |
| **向后稳定性与无除零** | 30 | 评估点精确命中插值节点时通过短路逻辑保证精确等于 $f(x_k)$ |

---

## 6. 引导自检与易错陷阱
- **陷阱**：在评估点接近插值节点时，直接相除可能出现 `0/0` 导致 `NaN`，必须添加匹配保护。

---

## 7. Starter Code 与可执行基线

```python
import numpy as np

def chebyshev_nodes(n):
    k = np.arange(n)
    return np.cos((2 * k + 1) / (2 * n) * np.pi)
```
