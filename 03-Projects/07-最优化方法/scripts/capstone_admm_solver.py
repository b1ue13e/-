"""
07-最优化方法 · 期末 Capstone 大作业: Consensus ADMM 并行与分布式求解器
支持：多 Worker 块状分布式更新、Consensus 变量一致性投影、L1/L2 正则化软阈值、严格原残差/对偶残差检验
"""
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def soft_thresholding(v, kappa):
    """软阈值算子 S_kappa(v) = sign(v) * max(|v| - kappa, 0)"""
    return np.sign(v) * np.maximum(np.abs(v) - kappa, 0.0)

def local_x_update(args):
    """Worker 节点本地求解 x_i: argmin 0.5 ||A_i x_i - b_i||_2^2 + (rho/2) ||x_i - z + u_i||_2^2"""
    A_i, b_i, z, u_i, rho, inv_matrix = args
    rhs = A_i.T @ b_i + rho * (z - u_i)
    x_i_next = inv_matrix @ rhs
    return x_i_next

class DistributedConsensusADMM:
    """
    分布式一致性 ADMM (Consensus ADMM) 求解器:
    min sum_{i=1}^N (0.5 ||A_i x_i - b_i||_2^2) + lambda * ||z||_1
    s.t. x_i - z = 0, i = 1, ..., N
    """
    def __init__(self, num_workers=2, rho=1.0, lmbda=0.1, use_threads=True):
        self.num_workers = num_workers
        self.rho = rho
        self.lmbda = lmbda
        self.use_threads = use_threads
        
    def fit(self, A, b, max_iters=100, tol_primal=1e-3, tol_dual=1e-3):
        """
        运行分布式 ADMM 迭代求解
        """
        M, n = A.shape
        N = self.num_workers
        block_size = M // N
        
        A_blocks = [A[i*block_size:(i+1)*block_size] for i in range(N)]
        b_blocks = [b[i*block_size:(i+1)*block_size] for i in range(N)]
        inv_matrices = [np.linalg.inv(A_i.T @ A_i + self.rho * np.eye(n)) for A_i in A_blocks]
        
        x_blocks = [np.zeros(n) for _ in range(N)]
        u_blocks = [np.zeros(n) for _ in range(N)]
        z = np.zeros(n)
        
        primal_residuals = []
        dual_residuals = []
        objective_history = []
        
        executor = ThreadPoolExecutor(max_workers=N) if self.use_threads else None
        
        for k in range(max_iters):
            tasks = [(A_blocks[i], b_blocks[i], z, u_blocks[i], self.rho, inv_matrices[i]) for i in range(N)]
            
            if self.use_threads and executor is not None:
                x_blocks = list(executor.map(local_x_update, tasks))
            else:
                x_blocks = [local_x_update(t) for t in tasks]
            
            x_bar = np.mean(x_blocks, axis=0)
            u_bar = np.mean(u_blocks, axis=0)
            
            # 全局变量 z 更新 (带有 L1 软阈值正则化)
            z_next = soft_thresholding(x_bar + u_bar, self.lmbda / (N * self.rho))
            
            # 对偶变量 u_i 更新
            for i in range(N):
                u_blocks[i] += x_blocks[i] - z_next
                
            # 原残差 r_k 与对偶残差 s_k
            r_k = np.sqrt(sum(np.linalg.norm(x_i - z_next)**2 for x_i in x_blocks))
            s_k = np.sqrt(N) * self.rho * np.linalg.norm(z_next - z)
            
            primal_residuals.append(float(r_k))
            dual_residuals.append(float(s_k))
            
            # 计算总目标函数值: 0.5 ||A z - b||_2^2 + lambda * ||z||_1
            obj_val = 0.5 * np.linalg.norm(A @ z_next - b)**2 + self.lmbda * np.sum(np.abs(z_next))
            objective_history.append(float(obj_val))
            
            z = z_next
            if r_k < tol_primal and s_k < tol_dual:
                break
                
        if executor is not None:
            executor.shutdown(wait=False)
            
        return z, primal_residuals, dual_residuals, objective_history
