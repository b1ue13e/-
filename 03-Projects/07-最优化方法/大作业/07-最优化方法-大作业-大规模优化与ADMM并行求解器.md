---
type: project
project_type: homework
course: 07-最优化方法
assignment_id: 07-最优化方法-大作业-01
assignment_level: capstone
assignment_format: project
stage_id: '05'
requires: ["[[最优化方法-增广拉格朗日与ADMM]]", "[[最优化方法-近端梯度与FISTA]]", "[[最优化方法-凸优化与拉格朗日对偶]]"]
source_type: open_source_project_task
created: 2026-08-06
status: ongoing
flow: project
tags:
  - 作业
  - 大作业
  - ADMM
  - 分布式计算
  - 最优化方法
---



# 07-最优化方法-大作业-大规模优化与ADMM并行求解器

> **本期末大作业为《07-最优化方法》课程结课 Capstone 项目**，旨在综合运用阶段 01~05 所学的前置线代、凸分析、对偶理论、近端算子与增广拉格朗日乘子法，手写一个**数据并行分块的共识 ADMM (Consensus ADMM) 大规模 Lasso 优化求解器**，并在多进程环境中审计收敛轨迹与加速比。

---

## 1. 学习目标

1. **分布式算法推导**：将海量数据行切分到 $N$ 个并行节点，推导 Consensus ADMM 下的本地 $x_i$ 更新步、全局全局变量 $z$ 更新步及对偶乘子 $u_i$ 更新步。
2. **手撕分布式求解器**：利用 Python `multiprocessing` 多进程池，实现多卡/多核分布式数据并行计算。
3. **收敛性与残差审计**：计算并画出**原残差 (Primal Residual)** $\|r^k\|_2$ 与 **对偶残差 (Dual Residual)** $\|s^k\|_2$ 的对数下降轨迹，实现自适应惩罚参数 $\rho$ 调整。
4. **与基线对比**：与单进程近端梯度 (FISTA) 及 Scipy/Sklearn 在收敛耗时和大规模特征选择上做性能对比。

---

## 2. 任务边界与知识依赖

## 3. 详细题目与要求

考虑大规模 Lasso 目标：
$$\min_{x} \frac{1}{2} \|A x - b\|_2^2 + \lambda \|x\|_1$$
将数据矩阵 $A \in \mathbf{R}^{M \times n}$ 与观察向量 $b \in \mathbf{R}^M$ 按样本行水平切分为 $N$ 个子块：
$$A = \begin{bmatrix} A_1 \\ A_2 \\ \vdots \\ A_N \end{bmatrix}, \quad b = \begin{bmatrix} b_1 \\ b_2 \\ \vdots \\ b_N \end{bmatrix}$$
每个分块节点维护本地副本 $x_i \in \mathbf{R}^n$，并要求所有本地副本等于全局一致约束 $z \in \mathbf{R}^n$：
$$\min_{x_1, \dots, x_N, z} \sum_{i=1}^N \frac{1}{2} \|A_i x_i - b_i\|_2^2 + \lambda \|z\|_1 \quad \text{s.t.} \quad x_i - z = 0, \ i=1,\dots,N$$

### 💡 迭代更新公式拆解：
1. **$x_i^{k+1}$ 本地并行求解步**（每个 worker 独立求解二次型，可提前预因子化）：
   $$x_i^{k+1} = \left( A_i^T A_i + \rho I \right)^{-1} \left( A_i^T b_i + \rho (z^k - u_i^k) \right)$$
2. **$z^{k+1}$ 中央共识步**（收集所有 $x_i^{k+1} + u_i^k$ 的平均值，应用软阈值算子）：
   $$\bar{x}^{k+1} = \frac{1}{N} \sum_{i=1}^N x_i^{k+1}, \quad \bar{u}^k = \frac{1}{N} \sum_{i=1}^N u_i^k$$
   $$z^{k+1} = \mathbf{S}_{\frac{\lambda}{N \rho}} \left( \bar{x}^{k+1} + \bar{u}^k \right)$$
3. **$u_i^{k+1}$ 对偶乘子更新步**：
   $$u_i^{k+1} = u_i^k + x_i^{k+1} - z^{k+1}$$

---

## 运行环境与依赖

- **Python 环境**：Python 3.10+，包含 `numpy`, `matplotlib`, `multiprocessing`
- **运行命令**：`python capstone_admm_solver.py`

```python
import numpy as np
import multiprocessing as mp
import time
import matplotlib.pyplot as plt

def soft_thresholding(v, kappa):
    """软阈值算子 S_kappa(v)"""
    return np.sign(v) * np.maximum(np.abs(v) - kappa, 0.0)

def local_x_update(args):
    """Worker 节点本地求解 x_i"""
    A_i, b_i, z, u_i, rho, inv_matrix = args
    # 利用预计算的 (A_i^T A_i + rho*I)^-1 加速求解
    rhs = A_i.T @ b_i + rho * (z - u_i)
    x_i_next = inv_matrix @ rhs
    return x_i_next

class DistributedConsensusADMM:
    def __init__(self, num_workers=4, rho=1.0, lmbda=0.1):
        self.num_workers = num_workers
        self.rho = rho
        self.lmbda = lmbda
        
    def fit(self, A, b, max_iters=100, tol=1e-4):
        M, n = A.shape
        N = self.num_workers
        
        # 数据分块
        block_size = M // N
        A_blocks = [A[i*block_size:(i+1)*block_size] for i in range(N)]
        b_blocks = [b[i*block_size:(i+1)*block_size] for i in range(N)]
        
        # 预计算缓存因子以避免重复逆运算
        inv_matrices = [np.linalg.inv(A_i.T @ A_i + self.rho * np.eye(n)) for A_i in A_blocks]
        
        # 初始化状态变量
        x_blocks = [np.zeros(n) for _ in range(N)]
        u_blocks = [np.zeros(n) for _ in range(N)]
        z = np.zeros(n)
        
        primal_residuals = []
        dual_residuals = []
        
        pool = mp.Pool(processes=N)
        start_time = time.time()
        
        for k in range(max_iters):
            # 1. 并行更新 x_i
            tasks = [(A_blocks[i], b_blocks[i], z, u_blocks[i], self.rho, inv_matrices[i]) for i in range(N)]
            x_blocks = pool.map(local_x_update, tasks)
            
            # 2. 中央聚合共识更新 z
            x_bar = np.mean(x_blocks, axis=0)
            u_bar = np.mean(u_blocks, axis=0)
            z_next = soft_thresholding(x_bar + u_bar, self.lmbda / (N * self.rho))
            
            # 3. 对偶更新 u_i
            for i in range(N):
                u_blocks[i] += x_blocks[i] - z_next
                
            # 4. 计算残差
            r_k = np.sqrt(sum(np.linalg.norm(x_i - z_next)**2 for x_i in x_blocks)) # 原残差
            s_k = np.sqrt(N) * self.rho * np.linalg.norm(z_next - z)                 # 对偶残差
            
            primal_residuals.append(r_k)
            dual_residuals.append(s_k)
            
            z = z_next
            if r_k < tol and s_k < tol:
                print(f"ADMM 在第 {k} 次迭代提前收敛！")
                break
                
        pool.close()
        pool.join()
        elapsed = time.time() - start_time
        
        return z, primal_residuals, dual_residuals, elapsed

# 真实仿真与校验
if __name__ == '__main__':
    # 模拟合成大规模数据 M=5000, n=200
    np.random.seed(42)
    M, n = 5000, 200
    A = np.random.randn(M, n)
    # 真实稀疏系数
    w_true = np.zeros(n)
    w_true[:20] = np.random.randn(20) # 只有前 20 个特征非零
    b = A @ w_true + 0.1 * np.random.randn(M)
    
    admm = DistributedConsensusADMM(num_workers=4, rho=2.0, lmbda=0.5)
    w_pred, r_res, s_res, cost_time = admm.fit(A, b, max_iters=80)
    
    print(f"并行计算总耗时: {cost_time:.3f} 秒")
    print(f"预测向量的稀疏度 (L0 范数): {np.sum(np.abs(w_pred) > 1e-3)}")
    
    # 画出原残差与对偶残差的收敛折线
    plt.figure(figsize=(8, 5))
    plt.semilogy(r_res, label='Primal Residual ||r^k||_2')
    plt.semilogy(s_res, label='Dual Residual ||s^k||_2')
    plt.xlabel('Iteration')
    plt.ylabel('Residual Norm')
    plt.title('Consensus ADMM Residual Convergence')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # 检验断言
    assert len(r_res) > 0, "算法未运行！"
    assert np.sum(np.abs(w_pred) > 1e-3) <= 50, "稀疏特征选择不满足要求！"
```

---

## 提交产物与格式

### 1. 提交文件
- `capstone_admm_solver.py`
- 大作业实验与分析报告 `ADMM_Report.pdf`

### 2. 100 分制期末 Rubric 评分细则

| 维度 | 分值 | 评价标准与交付物要求 |
|:---|:---:|:---|
| **算法推导报告** | 25 分 | - 完整推导 Consensus ADMM 各更新步，详细阐述原残差与对偶残差表达式（25分）。 |
| **代码与多进程架构** | 30 分 | - 成功实现 Python `multiprocessing` 并行 Worker 求解（20分）；<br>- 正确实现矩阵预因子化（Inv Precomputation）性能优化（10分）。 |
| **收敛性与残差审计** | 25 分 | - 画出双残差（Primal & Dual Residuals）对数收敛曲线（15分）；<br>- 探究不同参数 $\rho$ 对收敛速度的影响分析（10分）。 |
| **实验对比与拓展** | 10 分 | - 在真实/高维数据上对比单进程求解器，给出性能加速比。 |
| **工程文档与复现** | 10 分 | - 代码结构清晰，带有可流畅运行的示例脚本。 |


---

## 6. 引导提示与自检

- 检查梯度与 Hessian 计算公式推导。
- 验证凸性与约束条件可行性。


---

## 7. 来源与后续入口

- **来源**：EE364A / Numerical Optimization。
- **后续入口**：参见阶段 MOC 与课程总索引。
