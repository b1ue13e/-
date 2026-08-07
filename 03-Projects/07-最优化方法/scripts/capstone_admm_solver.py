"""
07-最优化方法 · 期末 Capstone 大作业: Consensus ADMM 并行求解器
"""
import numpy as np
import multiprocessing as mp

def soft_thresholding(v, kappa):
    """软阈值算子 S_kappa(v)"""
    return np.sign(v) * np.maximum(np.abs(v) - kappa, 0.0)

def local_x_update(args):
    """Worker 节点本地求解 x_i"""
    A_i, b_i, z, u_i, rho, inv_matrix = args
    rhs = A_i.T @ b_i + rho * (z - u_i)
    x_i_next = inv_matrix @ rhs
    return x_i_next

class DistributedConsensusADMM:
    def __init__(self, num_workers=2, rho=1.0, lmbda=0.1):
        self.num_workers = num_workers
        self.rho = rho
        self.lmbda = lmbda
        
    def fit(self, A, b, max_iters=50, tol=1e-4):
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
        
        pool = mp.Pool(processes=N)
        for _ in range(max_iters):
            tasks = [(A_blocks[i], b_blocks[i], z, u_blocks[i], self.rho, inv_matrices[i]) for i in range(N)]
            x_blocks = pool.map(local_x_update, tasks)
            
            x_bar = np.mean(x_blocks, axis=0)
            u_bar = np.mean(u_blocks, axis=0)
            z_next = soft_thresholding(x_bar + u_bar, self.lmbda / (N * self.rho))
            
            for i in range(N):
                u_blocks[i] += x_blocks[i] - z_next
                
            r_k = np.sqrt(sum(np.linalg.norm(x_i - z_next)**2 for x_i in x_blocks))
            s_k = np.sqrt(N) * self.rho * np.linalg.norm(z_next - z)
            
            primal_residuals.append(r_k)
            dual_residuals.append(s_k)
            
            z = z_next
            if r_k < tol and s_k < tol:
                break
                
        pool.close()
        pool.join()
        return z, primal_residuals, dual_residuals
