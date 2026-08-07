---
type: study
topic: "约束优化-SQP与投影梯度法"
course: "07-最优化方法"
created: 2026-08-06
status: completed
flow: knowledge
kind: concept
stage_moc: "[[🧭 阶段3-经典数值优化算法]]"
upstream:
  - "[[最优化方法-牛顿法]]"
  - "[[最优化方法-凸优化与拉格朗日对偶]]"
difficulty: advanced
---

# 约束优化：SQP与投影梯度法

## 0. 学习边界
- **类别**：A 类（核心算法框架）
- **判断理由**：在非线性约束优化（Nonlinear Programming, NLP）领域，序列二次规划（SQP）被认为是最高效、最强大的算法之一，尤其是针对中小规模问题。而投影梯度法则是处理简单约束（如非负约束、盒子约束）的最自然扩展，也是许多现代一阶方法（如近端梯度法）的基础。

---
## 1. 这个知识点解决什么问题？
> **我们遇到了什么麻烦**：
当我们面对带有等式或不等式约束的优化问题时：
$$\min_{x} f(x) \quad \text{s.t.} \quad c_i(x) = 0, i \in \mathcal{E}, \quad c_i(x) \ge 0, i \in \mathcal{I}$$
无约束优化的牛顿法或梯度下降法会直接破坏约束条件。我们需要一种机制，不仅能让目标函数下降，还能保证（或逐步逼近）约束的可行性。

---
## 2. 为什么它重要？它有什么用？
- **连接大图景**：它是无约束优化与约束优化之间的桥梁。投影梯度法将梯度下降推广到凸集上；SQP则将牛顿法推广到KKT条件上，通过在每一步求解一个二次规划（QP）子问题来逼近原问题。
- **实际应用场景**：控制理论中的模型预测控制（MPC）、机器人轨迹规划、结构优化、机器学习中的支持向量机（SVM）求解等。
- **高频题型/任务**：推导SQP的子问题形式、证明投影梯度法的收敛性、设计SQP的Merit Function（效益函数）以保证全局收敛。

---
## 3. 学它之前需要哪些前置知识？
1. **[[最优化方法-凸优化与拉格朗日对偶]]**：必须深刻理解KKT条件，因为SQP本质上是对KKT条件求解非线性方程组的牛顿法。
2. **[[最优化方法-线搜索与步长策略]]**：在SQP中，为了保证全局收敛，必须使用Merit Function进行线搜索。

---
## 4. 用直觉语言解释它
> «"这东西其实就像……"»
- **直觉类比/几何图像**：
  - **投影梯度法**：就像在山地（目标函数）中寻找最低点，但你被限制在一个带有栅栏的区域（约束集）。你每次想往山下走（负梯度方向），如果这一步让你跨出了栅栏，你就沿着垂直于栅栏的方向退回到栅栏边缘（投影）。
  - **SQP**：就像你想在一个复杂的曲面和复杂的边界上找最低点，你觉得太难了。于是你在当前点，把目标函数近似成一个“碗”（二次函数），把边界近似成“直线/平面”（线性约束）。在这个简单的“碗和直线”环境中找最低点（QP子问题），走到那儿，再重新近似。
- **为什么很自然**：牛顿法是通过二次模型逼近目标函数，SQP只是顺带把约束也做了线性逼近，从而将非线性规划转化为一系列简单的二次规划。
- **一句话直觉本质**：投影梯度法 = 梯度下降 + 投影；SQP = 目标函数二次泰勒展开 + 约束一阶泰勒展开。

---
## 5. 正式定义、核心公式、符号解释
### 1. 最核心定义
**投影梯度法（Projected Gradient Method）**
用于求解 $\min_{x \in \Omega} f(x)$，其中 $\Omega$ 是闭凸集。迭代公式为：
$$x_{k+1} = \mathcal{P}_{\Omega}(x_k - \alpha_k \nabla f(x_k))$$
其中 $\mathcal{P}_{\Omega}(y) = \arg\min_{x \in \Omega} \|x - y\|_2$ 是投影算子。

**序列二次规划（SQP）**
针对一般NLP问题，每一步在 $x_k$ 处求解如下 QP 子问题获得搜索方向 $p_k$：
$$\min_{p} \frac{1}{2} p^T \nabla_{xx}^2 \mathcal{L}(x_k, \lambda_k) p + \nabla f(x_k)^T p$$
$$\text{s.t.} \quad \nabla c_i(x_k)^T p + c_i(x_k) = 0, \quad i \in \mathcal{E}$$
$$\quad \quad \nabla c_i(x_k)^T p + c_i(x_k) \ge 0, \quad i \in \mathcal{I}$$
其中 $\mathcal{L}(x, \lambda) = f(x) - \sum \lambda_i c_i(x)$ 是拉格朗日函数。

### 2. 核心公式
- **有效集（Active Set）**：$\mathcal{A}(x) = \{i \in \mathcal{I} \mid c_i(x) = 0\} \cup \mathcal{E}$
- **Merit Function（例如 $\ell_1$ 惩罚函数）**：
  $$\phi_1(x; \mu) = f(x) + \mu \sum_{i \in \mathcal{E}} |c_i(x)| + \mu \sum_{i \in \mathcal{I}} [c_i(x)]^-$$
  其中 $[z]^- = \max(0, -z)$。用于线搜索评估步长。

### 3. 符号说明表
| 符号 | 含义 | 备注 |
|---|---|---|
| $\Omega$ | 可行域（约束集） | 在投影方法中要求是凸集 |
| $\mathcal{P}_{\Omega}$ | 投影算子 | 寻找凸集中距离目标最近的点 |
| $p_k$ | SQP中的搜索方向 | 通过求解局部QP得到 |
| $\nabla_{xx}^2 \mathcal{L}$ | 海森矩阵 | 目标与约束的联合曲率 |

### 4. 常见变体与适用条件
- 如果海森矩阵难以计算，可以使用 BFGS 更新近似海森矩阵，称为 **拟牛顿SQP**。

---
## 6. 推导思路和思想来源
### 投影梯度法的推导
- **最初困难**：梯度下降的一步 $x_k - \alpha_k \nabla f(x_k)$ 可能会跑出可行域。
- **关键"转念"**：跑出去了就“拉回来”。在欧氏距离下，拉回来的操作就是投影。
- **数学等价性**：当步长很小时，这等价于在可行域内寻找一个方向，使得该方向与负梯度方向的夹角最小。

### SQP的推导（基于等式约束）
- **牛顿法解KKT**：对于只含有等式约束 $c(x)=0$ 的问题，KKT条件为：
  $$F(x, \lambda) = \begin{bmatrix} \nabla f(x) - J(x)^T \lambda \\ c(x) \end{bmatrix} = 0$$
  对此非线性方程组应用牛顿法，计算雅可比矩阵：
  $$F'(x, \lambda) = \begin{bmatrix} \nabla_{xx}^2 \mathcal{L} & -J(x)^T \\ J(x) & 0 \end{bmatrix}$$
  牛顿步 $\begin{bmatrix} p \\ p_\lambda \end{bmatrix}$ 满足：
  $$\begin{bmatrix} \nabla_{xx}^2 \mathcal{L} & -J(x)^T \\ J(x) & 0 \end{bmatrix} \begin{bmatrix} p \\ p_\lambda \end{bmatrix} = -\begin{bmatrix} \nabla f(x) - J(x)^T \lambda \\ c(x) \end{bmatrix}$$
- **重写为QP**：可以证明，上述牛顿系统的解 $p$ 正是以下等式约束二次规划的解：
  $$\min_p \frac{1}{2} p^T \nabla_{xx}^2 \mathcal{L} p + \nabla f(x)^T p \quad \text{s.t.} \quad J(x)p + c(x) = 0$$
- **推广到不等式**：将不等式约束的一阶泰勒展开 $c_i(x) + \nabla c_i(x)^T p \ge 0$ 加入QP子问题，这就是现代SQP的基础。

---
## 7. 例子：基础 → 中等 → 实际应用
### 例子 1：基础例子（可手算）
求 $\min x_1^2 + x_2^2$ s.t. $x_1 + x_2 \ge 2$。
**投影梯度法**：设初始点 $(0,0)$。$\nabla f = (0,0)$，投影到半平面。
实际上，用SQP，在任意点展开。因为目标已经是二次的，约束是线性的，SQP在第一步就求解原问题，一步收敛到最优解 $(1,1)$。

### 例子 2：中等例子（SQP与Merit Function）
由于非线性约束，QP的解可能导致目标函数上升。通过 $\phi_1(x; \mu)$，如果 $\mu$ 足够大（$\mu \ge \|\lambda\|_\infty$），QP方向 $p$ 是 $\phi_1$ 的下降方向。这样就可以用常规的回溯线搜索找到合适的步长 $\alpha$。

### 例子 3：实际应用（Python代码示例：投影梯度法解Box约束）
```python
import numpy as np

def projected_gradient_descent(f_grad, proj_operator, x0, lr=0.1, max_iter=100):
    x = np.array(x0, dtype=float)
    for i in range(max_iter):
        grad = f_grad(x)
        x_new = proj_operator(x - lr * grad)
        if np.linalg.norm(x_new - x) < 1e-6:
            break
        x = x_new
    return x

# 最小化 (x1-3)^2 + (x2-4)^2, 约束在 [-1, 1]x[-1, 1] 盒子内
def grad(x):
    return 2 * (x - np.array([3.0, 4.0]))

def box_proj(x):
    return np.clip(x, -1.0, 1.0)

x_opt = projected_gradient_descent(grad, box_proj, [0, 0])
print("Optimal x:", x_opt) # 应当为 [1.0, 1.0]
```

---
## 8. 常见误区和易混概念
### 误区 1：SQP子问题总是可行的。
**错**。线性化的不等式约束可能相互矛盾（例如，原约束是可行域，但某一点处的线性切线产生空集）。解决办法是引入“松弛变量”（Elastic mode）或者使用信赖域方法。
### 概念对比表
| 方法 | 核心机制 | 适用约束类型 | 优点 |
|---|---|---|---|
| 投影梯度法 | 一阶梯度+直接投影 | 简单凸集（盒子、球） | 计算极其廉价 |
| 罚函数法 | 修改目标函数 | 任何约束 | 简单，但病态严重 |
| 内点法 | 障碍函数+牛顿法 | 大规模不等式 | 处理不等式能力强 |
| SQP | QP子问题 | 中小规模复杂约束 | 收敛极快（局部二次收敛） |

---
## 9. 相关知识点与 Obsidian 双链建议
- **上游依赖**：[[最优化方法-凸优化与拉格朗日对偶]]、[[最优化方法-拟牛顿法BFGS]]。
- **下游延伸**：[[最优化方法-罚函数法与障碍法]]、[[最优化方法-内点法原理]]。
- **横向关联**：与[[最优化方法-内点法原理]]竞争，常常在NLP求解器中提供两种选择。

---
## 10. 闭卷复现任务
- [ ] 默写投影算子的定义。
- [ ] 推导等式约束下，KKT条件的牛顿方程等价于QP子问题。
- [ ] 写出带有L1 Merit Function的SQP算法基本流程。

---
## 11. 自测题：5 道
> [!question]- 1. 投影梯度法要求可行域 $\Omega$ 必须是什么类型的集合？为什么？
> 必须是闭凸集。闭合性保证最近点存在；凸性保证最近点（投影）唯一，且投影算子是非扩张的（$\|P(x)-P(y)\| \le \|x-y\|$），这是证明算法收敛的关键。

> [!question]- 2. SQP 为什么需要 Merit Function？
> 因为在带有约束的非线性优化中，我们面临“减小目标函数”和“减小约束违反度”两个可能冲突的目标。Merit Function（效益函数）将这两者结合成一个标量函数，用于在迭代中评估当前步是否真的带来了“整体进步”，并用于线搜索决定步长。

> [!question]- 3. 为什么等式约束SQP子问题中的海森矩阵是拉格朗日函数的海森矩阵，而不是目标函数的海森矩阵？
> 因为在约束流形上，目标函数的曲率不足以描述问题的局部性质，约束曲面的弯曲（曲率）也会影响最优解的位置。拉格朗日函数的海森矩阵 $\nabla^2_{xx} \mathcal{L}$ 正是结合了目标和约束曲率的正确二阶导数。

> [!question]- 4. 在 SQP 中如果发生 Maratos 效应，指的是什么问题？
> Maratos效应是指：在靠近最优解时，一个完全接受全步长的牛顿步（能带来超线性收敛），由于其在约束流形上的二次弯曲，使得 Merit Function 反而上升，从而被线搜索拒绝。这会破坏SQP的快收敛性。常用二阶校正（Second-order correction）或非单调线搜索来克服。

> [!question]- 5. 简述有效集法（Active Set Method）在约束优化中的作用。
> 对于不等式约束问题，在最优点处，只有一部分不等式是取等号的（即有效约束）。有效集法通过在迭代过程中动态猜测哪些约束是有效的，将不等式约束问题转化为只含等式约束的子问题来求解。

---
## 12. 我的主动回忆区
### 我的闭卷复述
### 我的推导复现
### 我的错误与卡点
### 下次复习日期
2026-08-12

---
## 13. 给 Obsidian 的归档建议
归入 `07-最优化方法/非线性规划` 文件夹，确保与 KKT 条件和内点法的笔记建立紧密的双向链接。

## ⚠️ 常见陷阱与避坑指南

> [!CAUTION]
> 1. **SQP 二次子问题不兼容 (Infeasible QP Subproblem)**：在序列二次规划 (SQP) 中，当原非线性约束剧烈弯曲时，对约束进行线性化得到的 QP 子问题可行域可能为空。需引入松弛变量（如 $S\ell_1QP$ 策略）。
> 2. **投影梯度法的算子复杂度**：投影梯度法要求向可行域 $\Omega$ 的投影算子 $\Pi_\Omega(x)$ 极易计算（例如超矩形、球体）。如果可行域本身极其复杂，求解投影算子本身就是一个二次规划，导致算法效率低下。

## 🃏 Anki 卡片

Q: 序列二次规划 (SQP, Sequential Quadratic Programming) 每步迭代的核心思想是什么？
A: 在当前迭代点 $x_k$ 处，构造拉格朗日函数的二次近似目标，并将非线性约束局部线性化，从而解出一个二次规划 (QP) 子问题，取其解作为搜索方向 $d_k$。
<!-- id: opt-sqp-01 -->

Q: 投影梯度法 (Projected Gradient Descent) 的更新公式及其适用条件是什么？
A: 更新公式为 $x_{k+1} = \Pi_\Omega \left( x_k - \alpha_k \nabla f(x_k) 
ight)$。适用条件：可行域 $\Omega$ 必须为闭凸集，且向 $\Omega$ 的欧氏投影算子 $\Pi_\Omega$ 具有闭式解或高度高效的算法。
<!-- id: opt-sqp-02 -->


---
Q: 序列二次规划 (SQP) 的基本思想是什么？
A: 在每步迭代中构造并求解拉格朗日函数的二次规划（QP）子问题，直接逼近非线性约束优化的 KKT 点。
<!-- id: opt-sqp-03 -->

## 学完后可以完成


```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
