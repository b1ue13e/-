"""
07-最优化方法 求解器全量自动化单元测试包 (Pytest)
包含经典一阶、线搜索、二阶、拟牛顿 (BFGS/L-BFGS)、信赖域 (Dogleg)、动量/Nesterov (NAG)、FISTA 与 ADMM
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
    f = lambda x: x[0]**2 + 10.0 * x[1]**2
    grad_f = lambda x: np.array([2*x[0], 20.0*x[1]])
    x = np.array([10.0, 10.0])
    p = -grad_f(x)
    alpha = backtracking_armijo(f, grad_f, x, p)
    assert 0 < alpha <= 1.0
    assert f(x + alpha * p) < f(x)

def test_steepest_descent_and_newton():
    f = lambda x: 0.5 * x[0]**2 + 5.0 * x[1]**2
    grad_f = lambda x: np.array([x[0], 10.0*x[1]])
    hess_f = lambda x: np.array([[1.0, 0.0], [0.0, 10.0]])
    x0 = [10.0, 10.0]
    
    x_sd, _ = steepest_descent(f, grad_f, x0, tol=1e-4)
    assert np.allclose(x_sd, [0.0, 0.0], atol=1e-3)
    
    x_newton, _ = newton_method(f, grad_f, hess_f, x0, tol=1e-4)
    assert np.allclose(x_newton, [0.0, 0.0], atol=1e-3)

def test_linear_cg():
    A = np.array([[4.0, 1.0], [1.0, 3.0]])
    b = np.array([1.0, 2.0])
    x0 = [0.0, 0.0]
    x_cg = linear_conjugate_gradient(A, b, x0)
    x_exact = np.linalg.solve(A, b)
    assert np.allclose(x_cg, x_exact, atol=1e-5)

def test_bfgs_rosenbrock():
    def rosenbrock(x):
        return 100.0 * (x[1] - x[0]**2)**2 + (1.0 - x[0])**2
    def grad_rosenbrock(x):
        g1 = -400.0 * x[0] * (x[1] - x[0]**2) - 2.0 * (1.0 - x[0])
        g2 = 200.0 * (x[1] - x[0]**2)
        return np.array([g1, g2])
    
    x_opt, _ = bfgs_optimizer(rosenbrock, grad_rosenbrock, x0=[-1.2, 1.0], max_iters=100)
    assert np.allclose(x_opt, [1.0, 1.0], atol=1e-2)

def test_lbfgs_high_dim():
    # 测试 L-BFGS 在 10 维二次型问题上的收敛性与双循环递归
    d = 10
    A = np.diag(np.linspace(1.0, 20.0, d))
    b = np.ones(d)
    f = lambda x: 0.5 * np.dot(x, A @ x) - np.dot(b, x)
    grad_f = lambda x: A @ x - b
    
    x0 = np.zeros(d)
    x_opt, history = lbfgs_optimizer(f, grad_f, x0, m=5, max_iters=50, tol=1e-5)
    x_exact = np.linalg.solve(A, b)
    assert np.allclose(x_opt, x_exact, atol=1e-4)
    assert history[-1][2] < 1e-4

def test_trust_region_dogleg():
    # 测试 信赖域 Powell Dogleg 在 Rosenbrock 函数上的收敛性
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

    x0 = [-1.2, 1.0]
    x_opt, history = trust_region_dogleg(rosenbrock, grad_rosenbrock, hess_rosenbrock, x0, delta0=1.0, max_iters=100)
    assert np.allclose(x_opt, [1.0, 1.0], atol=1e-2)
    assert history[-1][2] < 1e-3

def test_heavyball_and_nesterov():
    # 测试 Polyak 重球法与 Nesterov AGD 在病态二次型上的收敛比对
    A = np.array([[10.0, 0.0], [0.0, 1.0]]) # 条件数 kappa = 10
    f = lambda x: 0.5 * np.dot(x, A @ x)
    grad_f = lambda x: A @ x
    x0 = [10.0, 10.0]

    x_hb, hist_hb = polyak_heavy_ball(f, grad_f, x0, lr=0.1, beta=0.6, max_iters=100)
    x_nag, hist_nag = nesterov_accelerated_gradient(f, grad_f, x0, lr=0.1, beta=0.6, max_iters=100)

    assert np.allclose(x_hb, [0.0, 0.0], atol=1e-2)
    assert np.allclose(x_nag, [0.0, 0.0], atol=1e-2)

def test_fista_lasso():
    np.random.seed(42)
    N, d = 100, 10
    X = np.random.randn(N, d)
    w_true = np.array([2.0, -1.5, 0, 0, 1.0, 0, 0, 0, 0, 0])
    y = X @ w_true + 0.05 * np.random.randn(N)
    
    w_est, history = fista_lasso(X, y, lmbda=0.1, max_iters=150)
    assert history[-1] < history[0]
    assert np.sum(np.abs(w_est) > 1e-3) <= 5

def test_consensus_admm():
    np.random.seed(42)
    M, n = 200, 20
    A = np.random.randn(M, n)
    w_true = np.zeros(n)
    w_true[:5] = [1.0, -1.0, 2.0, -2.0, 1.5]
    b = A @ w_true + 0.1 * np.random.randn(M)
    
    admm = DistributedConsensusADMM(num_workers=2, rho=1.0, lmbda=0.2)
    z, primal_r, dual_r = admm.fit(A, b, max_iters=30)
    assert len(primal_r) > 0
    assert np.sum(np.abs(z) > 1e-2) <= 10

def test_maxcut_sdp_solver():
    # 测试 Max-Cut SDP 松弛与随机超平面剪切
    np.random.seed(42)
    n = 6
    W = np.array([
        [0, 2, 1, 0, 0, 0],
        [2, 0, 3, 1, 0, 0],
        [1, 3, 0, 2, 1, 0],
        [0, 1, 2, 0, 4, 1],
        [0, 0, 1, 4, 0, 2],
        [0, 0, 0, 1, 2, 0]
    ], dtype=float)
    
    X_opt, sdp_val = maxcut_sdp_solver(W)
    assert X_opt is not None
    assert X_opt.shape == (n, n)
    assert np.allclose(np.diag(X_opt), 1.0, atol=1e-3)
    assert sdp_val > 0
    
    best_cut = random_hyperplane_rounding(X_opt, num_cuts=20)
    assert best_cut is not None
    assert len(best_cut) == n


