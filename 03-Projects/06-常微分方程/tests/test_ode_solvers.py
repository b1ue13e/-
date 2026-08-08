"""
PyTest 单元测试：验证 ODE 求解器、Lorenz 系统、SDE 与 Neural ODE 伴随梯度
包含：
1. 基础精度测试 (Euler & RK4)
2. RK4 四阶收敛阶数定量校验
3. 输入校验与异常边界测试
4. 刚性隐式 Euler 及奇异矩阵处理
5. Lorenz 混沌动力系统
6. SDE Euler-Maruyama 离散求解
7. Neural ODE 伴随灵敏度梯度与有限差分 (Finite Difference) 检验
"""

import os
import sys
import numpy as np
import pytest

# 将 scripts 目录加入 sys.path
scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from ode_solvers import (
    solve_euler,
    solve_rk4,
    solve_backward_euler,
    simulate_lorenz,
    simulate_sde_euler_maruyama,
    SimpleNeuralODEFunc,
    neural_ode_adjoint_gradient
)


def test_euler_accuracy():
    """验证显式 Euler 解指数衰减方程 dy/dt = -y, y(0)=1"""
    f = lambda t, y: -y
    t_eval = np.linspace(0, 1, 101)
    y_num = solve_euler(f, [1.0], t_eval).flatten()
    y_exact = np.exp(-t_eval)

    # 验证最大误差在合理范围内 (O(dt))
    max_err = np.max(np.abs(y_num - y_exact))
    assert max_err < 0.01, f"Euler error too large: {max_err}"


def test_rk4_fourth_order():
    """验证 RK4 算法解谐振子系统的精度"""
    f = lambda t, y: np.array([y[1], -y[0]])
    t_eval = np.linspace(0, 2 * np.pi, 201)
    y0 = np.array([1.0, 0.0])

    y_num = solve_rk4(f, y0, t_eval)
    y1_exact = np.cos(t_eval)

    max_err = np.max(np.abs(y_num[:, 0] - y1_exact))
    assert max_err < 1e-5, f"RK4 error too large: {max_err}"


def test_rk4_quantitative_convergence_rate():
    """定量校验 RK4 算法的 4 阶收敛阶数: Error(h/2) / Error(h) ~ 1/16 = 0.0625"""
    f = lambda t, y: -y
    y0 = np.array([1.0])
    t_end = 1.0

    # Step 1: N = 20 steps (h1 = 0.05)
    t1 = np.linspace(0, t_end, 21)
    y1 = solve_rk4(f, y0, t1).flatten()
    err1 = np.abs(y1[-1] - np.exp(-t_end))

    # Step 2: N = 40 steps (h2 = 0.025)
    t2 = np.linspace(0, t_end, 41)
    y2 = solve_rk4(f, y0, t2).flatten()
    err2 = np.abs(y2[-1] - np.exp(-t_end))

    ratio = err2 / err1
    # 理论比例为 (1/2)^4 = 1/16 = 0.0625
    assert 0.05 < ratio < 0.08, f"RK4 收敛阶数异常，误差比例: {ratio}"


def test_stiff_backward_euler():
    """验证隐式 Euler 解刚性方程 dy/dt = -100 y 的绝对稳定性"""
    A = np.array([[-100.0]])
    t_eval = np.linspace(0, 1, 21)  # dt = 0.05
    y0 = np.array([1.0])

    y_num = solve_backward_euler(A, y0, t_eval).flatten()

    assert not np.any(np.isnan(y_num))
    assert not np.any(np.isinf(y_num))
    assert np.all(np.abs(y_num) <= 1.0)
    assert y_num[-1] < 1e-4


def test_invalid_inputs_and_edge_cases():
    """测试边界与非法输入触发异常"""
    f = lambda t, y: -y
    # 1. 非单调递增时间序列
    with pytest.raises(ValueError, match="严格单调递增"):
        solve_euler(f, [1.0], [0.0, 1.0, 0.5])

    # 2. t_eval 长度不足
    with pytest.raises(ValueError, match="至少包含 2 个元素"):
        solve_rk4(f, [1.0], [0.0])

    # 3. 隐式 Euler 矩阵与初值维度不匹配
    with pytest.raises(ValueError, match="维度"):
        solve_backward_euler(np.eye(2), [1.0], [0.0, 1.0])

    # 4. 隐式 Euler 矩阵奇异抛出异常
    A_singular = np.array([[2.0, 0.0], [0.0, 2.0]])
    t_eval = np.array([0.0, 0.5])  # I - dt*A = I - 0.5*2*I = 0 (奇异)
    with pytest.raises(ValueError, match="奇异不可逆"):
        solve_backward_euler(A_singular, [1.0, 1.0], t_eval)



def test_lorenz_simulation():
    """验证 Lorenz 混沌吸引子仿真"""
    y0 = np.array([1.0, 1.0, 1.0])
    t_eval = np.linspace(0, 10, 1000)
    traj = simulate_lorenz(y0, t_eval)

    assert traj.shape == (1000, 3)
    assert np.all(np.abs(traj) < 100.0)


def test_sde_simulation():
    """验证 SDE Euler-Maruyama 求解几何布朗运动 dy = mu*y*dt + sigma*y*dW"""
    mu = 0.1
    sigma = 0.2
    drift = lambda t, y: mu * y
    diffusion = lambda t, y: sigma * y

    t_eval = np.linspace(0, 1, 501)
    y0 = np.array([100.0])

    y_sim = simulate_sde_euler_maruyama(drift, diffusion, y0, t_eval, seed=42).flatten()
    assert len(y_sim) == 501
    assert y_sim[0] == 100.0
    assert y_sim[-1] > 0  # GBM 保持正性


def test_neural_ode_adjoint_vs_finite_difference():
    """使用有限差分 (Finite Difference) 严格校验 Neural ODE 伴随梯度的正确性"""
    np.random.seed(42)
    dim = 2
    W = np.random.randn(dim, dim) * 0.1
    b = np.zeros(dim)

    ode_func = SimpleNeuralODEFunc(W, b)
    z0 = np.array([1.0, 0.5])
    z_target = np.array([0.0, 0.0])

    loss, dL_dW_adjoint = neural_ode_adjoint_gradient(
        ode_func, z0, z_target, t0=0.0, t1=1.0, num_steps=100
    )

    # 有限差分计算梯度: dL/dW_ij ~ (L(W + eps) - L(W - eps)) / (2 * eps)
    eps = 1e-5
    dL_dW_fd = np.zeros_like(W)

    for i in range(dim):
        for j in range(dim):
            W_plus = W.copy()
            W_plus[i, j] += eps
            ode_func_plus = SimpleNeuralODEFunc(W_plus, b)
            loss_plus, _ = neural_ode_adjoint_gradient(ode_func_plus, z0, z_target, 0.0, 1.0, 100)

            W_minus = W.copy()
            W_minus[i, j] -= eps
            ode_func_minus = SimpleNeuralODEFunc(W_minus, b)
            loss_minus, _ = neural_ode_adjoint_gradient(ode_func_minus, z0, z_target, 0.0, 1.0, 100)

            dL_dW_fd[i, j] = (loss_plus - loss_minus) / (2.0 * eps)

    # 验证伴随梯度与有限差分梯度的相对误差 < 5%
    rel_error = np.linalg.norm(dL_dW_adjoint - dL_dW_fd) / (np.linalg.norm(dL_dW_fd) + 1e-8)
    assert rel_error < 0.05, f"伴随梯度与有限差分偏差过大: {rel_error}"

