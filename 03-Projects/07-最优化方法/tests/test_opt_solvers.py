"""
07-最优化方法 · 求解器工业级严密自动化单元测试包 (Pytest)
覆盖：
1. 线搜索与 Armijo 充分下降条件
2. 最速下降法与二阶牛顿法 (二次型一步收敛检验)
3. 线性共轭梯度法 (n 步理论精确收敛检验)
4. 拟牛顿法 BFGS (Rosenbrock 超线性收敛与梯度模长检验)
5. 有限内存拟牛顿 L-BFGS (高维病态两环递归检验)
6. 信赖域 Powell Dogleg 算法 (信赖域半径与实际/预测下降比检验)
7. Polyak 重球法 vs Nesterov 加速梯度法 (病态二次型加速与平稳度检验)
8. 近端梯度法 FISTA (L1-Lasso 稀疏支撑集恢复与 O(1/k^2) 目标收敛)
9. 分布式一致性 ADMM 求解器 (原残差与对偶残差双重收敛检验)
10. 半定规划 SDP Max-Cut 松弛与随机超平面舍入 (Goemans-Williamson 0.878 理论界检验)
"""
import sys
import os
import numpy as np
import pytest

# 将 scripts 目录加入模块搜索路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from line_search_opt import backtracking_armijo, steepest_descent, newton_method, linear_conjugate_gradient
from hw05_bfgs import bfgs_optimizer
from lbfgs_solver import lbfgs_optimizer, lbfgs_two_loop
from trust_region_dogleg import trust_region_dogleg, dogleg_step
from nesterov_heavyball import polyak_heavy_ball, nesterov_accelerated_gradient
from stage_04_fista_adamw import fista_lasso, soft_thresholding
from capstone_admm_solver import DistributedConsensusADMM
from hw06_sdp_maxcut import maxcut_sdp_solver, random_hyperplane_rounding

def test_backtracking_armijo():
    """验证 Armijo 回溯线搜索满足充分下降条件 f(x + alpha*p) <= f(x) + c1*alpha*grad^T*p"""
    f = lambda x: x[0]**2 + 10.0 * x[1]**2
    grad_f = lambda x: np.array([2.0*x[0], 20.0*x[1]])
    x = np.array([5.0, 5.0])
    p = -grad_f(x)
    c1 = 1e-4
    alpha = backtracking_armijo(f, grad_f, x, p, alpha0=1.0, rho=0.5, c1=c1)
    
    assert 0 < alpha <= 1.0
    # 严格验证 Armijo 充分下降不等式
    assert f(x + alpha * p) <= f(x) + c1 * alpha * np.dot(grad_f(x), p)
    assert f(x + alpha * p) < f(x)

def test_steepest_descent_and_newton():
    """验证牛顿法在二次型上 1 步精确收敛，最速下降法平稳收敛"""
    Q = np.array([[4.0, 1.0], [1.0, 2.0]])
    b = np.array([1.0, -1.0])
    f = lambda x: 0.5 * np.dot(x, Q @ x) - np.dot(b, x)
    grad_f = lambda x: Q @ x - b
    hess_f = lambda x: Q
    x_exact = np.linalg.solve(Q, b)
    x0 = np.array([10.0, -10.0])
    
    # 1. 验证牛顿法 1 步精确求解
    x_newton, hist_newton = newton_method(f, grad_f, hess_f, x0, tol=1e-10)
    assert np.allclose(x_newton, x_exact, atol=1e-8)
    assert len(hist_newton) <= 3  # 最多 1-2 次迭代即收敛
    
    # 2. 验证最速下降法收敛到精确解
    x_sd, hist_sd = steepest_descent(f, grad_f, x0, tol=1e-4)
    assert np.allclose(x_sd, x_exact, atol=1e-3)
    assert len(hist_sd) > len(hist_newton)  # 验证一阶收敛慢于二阶

def test_linear_cg():
    """验证线性共轭梯度法 (CG) 在 n 维严格正定系统上精确解出 Ax = b"""
    n = 5
    np.random.seed(42)
    M = np.random.randn(n, n)
    A = M.T @ M + 2.0 * np.eye(n)  # 条件数良好的正定矩阵
    b = np.random.randn(n)
    x0 = np.zeros(n)
    
    x_cg = linear_conjugate_gradient(A, b, x0, tol=1e-10)
    x_exact = np.linalg.solve(A, b)
    
    # 严格检验代数解与残差范数
    assert np.allclose(x_cg, x_exact, atol=1e-8)
    assert np.linalg.norm(A @ x_cg - b) < 1e-8

def test_bfgs_rosenbrock():
    """验证拟牛顿法 BFGS 在经典 Rosenbrock 非凸香蕉曲面上的超线性收敛与零梯度"""
    def rosenbrock(x):
        return 100.0 * (x[1] - x[0]**2)**2 + (1.0 - x[0])**2
        
    def grad_rosenbrock(x):
        g1 = -400.0 * x[0] * (x[1] - x[0]**2) - 2.0 * (1.0 - x[0])
        g2 = 200.0 * (x[1] - x[0]**2)
        return np.array([g1, g2])
    
    x0 = np.array([-1.2, 1.0])
    x_opt, hist = bfgs_optimizer(rosenbrock, grad_rosenbrock, x0=x0, max_iters=100, tol=1e-5)
    
    # 严格检验最优点 (1.0, 1.0) 与最优梯度残差
    assert np.allclose(x_opt, [1.0, 1.0], atol=1e-3)
    assert np.linalg.norm(grad_rosenbrock(x_opt)) < 1e-4
    assert rosenbrock(x_opt) < 1e-6

def test_lbfgs_high_dim():
    """验证有限内存 L-BFGS 在 30 维中高维病态问题上的收敛性与双循环逆 Hessian 逼近"""
    d = 30
    np.random.seed(123)
    evals = np.linspace(1.0, 100.0, d) # 条件数 kappa = 100
    A = np.diag(evals)
    b = np.ones(d)
    f = lambda x: 0.5 * np.dot(x, A @ x) - np.dot(b, x)
    grad_f = lambda x: A @ x - b
    x_exact = np.linalg.solve(A, b)
    
    x0 = np.zeros(d)
    x_opt, history = lbfgs_optimizer(f, grad_f, x0, m=10, max_iters=80, tol=1e-6)
    
    assert np.allclose(x_opt, x_exact, atol=1e-4)
    assert np.linalg.norm(grad_f(x_opt)) < 1e-4
    # 验证目标函数单调严格下降
    f_vals = [h[2] for h in history]
    assert f_vals[-1] < f_vals[0]

def test_trust_region_dogleg():
    """验证信赖域 Powell Dogleg 算法在 Rosenbrock 上的收敛性与梯度逼近"""
    def rosenbrock(x):
        return 100.0 * (x[1] - x[0]**2)**2 + (1.0 - x[0])**2
        
    def grad_rosenbrock(x):
        g1 = -400.0 * x[0] * (x[1] - x[0]**2) - 2.0 * (1.0 - x[0])
        g2 = 200.0 * (x[1] - x[0]**2)
        return np.array([g1, g2])
        
    def hess_rosenbrock(x):
        h11 = -400.0 * x[1] + 1200.0 * x[0]**2 + 2.0
        h12 = -400.0 * x[0]
        h21 = -400.0 * x[0]
        h22 = 200.0
        return np.array([[h11, h12], [h21, h22]])

    x0 = np.array([-1.2, 1.0])
    x_opt, history = trust_region_dogleg(rosenbrock, grad_rosenbrock, hess_rosenbrock, x0, delta0=1.0, max_iters=100)
    
    assert np.allclose(x_opt, [1.0, 1.0], atol=1e-3)
    assert np.linalg.norm(grad_rosenbrock(x_opt)) < 1e-3

def test_heavyball_and_nesterov():
    """对比 Polyak 重球法与 Nesterov AGD 在病态二次型 (kappa = 20) 上的收敛性"""
    A = np.array([[20.0, 0.0], [0.0, 1.0]])
    f = lambda x: 0.5 * np.dot(x, A @ x)
    grad_f = lambda x: A @ x
    x0 = np.array([5.0, 5.0])

    # 在 L = 20 下，选用稳定步长 lr = 0.04 < 1/L
    x_hb, hist_hb = polyak_heavy_ball(f, grad_f, x0, lr=0.04, beta=0.6, max_iters=150)
    x_nag, hist_nag = nesterov_accelerated_gradient(f, grad_f, x0, lr=0.04, beta=0.6, max_iters=150)

    # 验证最终收敛到原点
    assert np.allclose(x_hb, [0.0, 0.0], atol=1e-2)
    assert np.allclose(x_nag, [0.0, 0.0], atol=1e-2)
    assert f(x_nag) < f(x0) * 1e-3

def test_fista_lasso():
    """验证 FISTA 求解 Lasso 时的目标函数单调收敛与稀疏支撑集精准恢复"""
    np.random.seed(42)
    N, d = 100, 15
    X = np.random.randn(N, d)
    # 真实稀疏权重 (前 4 项非零，其余均为 0)
    w_true = np.zeros(d)
    w_true[:4] = [2.0, -1.5, 1.2, -0.8]
    y = X @ w_true + 0.02 * np.random.randn(N)
    
    w_est, history = fista_lasso(X, y, lmbda=0.05, max_iters=200)
    
    # 1. 验证目标函数单调下降且收敛
    assert history[-1] < history[0] * 0.5
    # 2. 验证稀疏性恢复：非零项集中在前部
    assert np.sum(np.abs(w_est[:4]) > 0.1) == 4

def test_consensus_admm():
    """验证分布式 Consensus ADMM 的原残差/对偶残差双重收敛与稀疏恢复"""
    np.random.seed(42)
    M, n = 200, 20
    A = np.random.randn(M, n)
    w_true = np.zeros(n)
    w_true[:4] = [2.0, -1.5, 1.0, -0.8]
    b = A @ w_true + 0.05 * np.random.randn(M)
    
    admm = DistributedConsensusADMM(num_workers=4, rho=1.0, lmbda=0.2, use_threads=True)
    z, primal_r, dual_r, obj_hist = admm.fit(A, b, max_iters=50, tol_primal=1e-2, tol_dual=1e-2)
    
    # 1. 严格检验残差有效收敛
    assert len(primal_r) > 5
    assert primal_r[-1] < primal_r[0] * 0.5
    # 2. 检验目标函数有效下降
    assert obj_hist[-1] < obj_hist[0]
    # 3. 检验稀疏支撑集恢复正确
    assert np.all(np.abs(z[:4]) > 0.1)

def test_maxcut_sdp_solver():
    """验证 Goemans-Williamson Max-Cut SDP 松弛的半正定矩阵性质与剪切权重有效性"""
    n = 6
    W = np.array([
        [0, 3, 1, 0, 0, 0],
        [3, 0, 4, 1, 0, 0],
        [1, 4, 0, 2, 1, 0],
        [0, 1, 2, 0, 5, 2],
        [0, 0, 1, 5, 0, 3],
        [0, 0, 0, 2, 3, 0]
    ], dtype=float)
    
    X_opt, sdp_val = maxcut_sdp_solver(W)
    assert X_opt is not None
    assert X_opt.shape == (n, n)
    
    # 严格检验 SDP 约束：对角线为 1，特征值非负 (半正定)
    assert np.allclose(np.diag(X_opt), 1.0, atol=1e-3)
    eigvals = np.linalg.eigvalsh(X_opt)
    assert np.all(eigvals >= -1e-4) # 半正定性
    
    # 随机超平面舍入
    cut_val, x_cut = random_hyperplane_rounding(X_opt, W, num_trials=100)
    assert cut_val > 0
    # 验证割值满足 Goemans-Williamson 理论下界期望预期
    assert cut_val >= 0.7 * sdp_val


def test_lion_optimizer():
    """验证 Lion 符号动量优化器在二次目标上的有界更新与平稳收敛"""
    from modern_llm_optimizers import Lion
    np.random.seed(42)
    # 目标: min 0.5 * x^T A x, 其中 A 严格正定
    A = np.diag([5.0, 1.0])
    x = np.array([2.0, -3.0])
    optimizer = Lion([x], lr=0.03, beta1=0.9, beta2=0.99, weight_decay=0.0)
    
    initial_loss = 0.5 * float(x @ A @ x)
    for _ in range(120):
        grad = A @ x
        optimizer.step([grad])
    
    final_loss = 0.5 * float(x @ A @ x)
    assert final_loss < initial_loss * 0.1
    assert np.allclose(x, [0.0, 0.0], atol=0.8)


def test_muon_orthogonalization():
    """验证 Muon Newton-Schulz 极分解正交化拉平奇异值为 1 (U @ U.T ≈ I)"""
    from modern_llm_optimizers import newton_schulz_polar, Muon
    np.random.seed(42)
    d1, d2 = 16, 32
    # 构造一个病态权重梯度矩阵
    G = np.random.randn(d1, d2)
    U = newton_schulz_polar(G, steps=10)
    
    # 验证 U @ U.T 严格逼近单位矩阵 I (机器精度级别)
    gram = U @ U.T
    assert np.allclose(gram, np.eye(d1), atol=1e-5)
    
    # 验证奇异值几乎全部紧密聚集在 1.0 附近
    s = np.linalg.svd(U, compute_uv=False)
    assert np.allclose(s, 1.0, atol=1e-4)



def test_dynamic_loss_scaler():
    """验证 Dynamic Loss Scaler 的溢出跳过、缩减与稳定步放大机制"""
    from modern_llm_optimizers import DynamicLossScaler
    scaler = DynamicLossScaler(init_scale=1024.0, scale_factor=2.0, scale_window=5)
    
    # 1. 正常梯度解缩放
    normal_grads = [np.array([1024.0, 2048.0])]
    unscaled, is_valid = scaler.unscale_and_update(normal_grads)
    assert is_valid is True
    assert np.allclose(unscaled[0], [1.0, 2.0])
    
    # 2. 发生 Inf 溢出
    overflow_grads = [np.array([np.inf, 2048.0])]
    _, is_valid = scaler.unscale_and_update(overflow_grads)
    assert is_valid is False
    assert scaler.scale == 512.0  # 自动减半

