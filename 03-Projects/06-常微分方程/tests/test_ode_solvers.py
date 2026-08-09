"""
常微分方程 (ODE) 科学计算与求解器自动化测试套件
=====================================================
覆盖:
1. Explicit Euler 1阶理论收敛率测试
2. RK4 4阶理论收敛阶定量网格收敛性分析 (Grid Refinement Study)
3. RK45 自适应步长积分器在瞬态急剧变化区间的动态步长缩放测试
4. 通用隐式 Euler 非线性刚性系统 (Nonlinear Stiff ODE with Newton-Raphson) 稳定性测试
5. Lorenz 3D 混沌动力系统蝴蝶吸引子形态与有界性测试
6. SDE Euler-Maruyama 随机模拟均值与统计特性检验
7. Neural ODE 伴随状态法梯度 vs 双边有限差分数值梯度定量比对 (< 1% 相对误差)
8. 异常输入边界条件测试
"""

import os
import sys
import pytest
import numpy as np

# 将 scripts 路径加入模块导入搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.abspath(os.path.join(current_dir, "..", "scripts"))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from ode_solvers import (
    solve_euler,
    solve_rk4,
    solve_rk45_adaptive,
    solve_backward_euler,
    simulate_lorenz,
    simulate_sde_euler_maruyama,
    SimpleNeuralODEFunc,
    neural_ode_adjoint_gradient,
)


# =========================================================================
# 1. 显式求解器收敛阶测试
# =========================================================================

def test_euler_accuracy():
    """显式 Euler 法在指数衰减模型 y' = -y, y(0)=1 上的 1 阶精度验证"""
    f = lambda t, y: -y
    t_eval_coarse = np.linspace(0, 1, 21)   # dt = 0.05
    t_eval_fine = np.linspace(0, 1, 41)     # dt = 0.025

    y_coarse = solve_euler(f, 1.0, t_eval_coarse)
    y_fine = solve_euler(f, 1.0, t_eval_fine)

    exact = np.exp(-1.0)
    err_coarse = abs(y_coarse[-1] - exact)
    err_fine = abs(y_fine[-1] - exact)

    # 步长减半，1 阶误差应减半 (比率接近 0.5)
    ratio = err_fine / err_coarse
    assert 0.45 < ratio < 0.55, f"Euler 收敛比率异常: {ratio}"


def test_rk4_accuracy_and_convergence_rate():
    """经典 RK4 在简谐振子 y'' + y = 0 上的 4 阶收敛阶定量网格加密验证"""
    # 状态向量 z = [y, y'] -> z' = [y', -y]
    f = lambda t, z: np.array([z[1], -z[0]], dtype=np.float64)
    z0 = np.array([1.0, 0.0])  # y(0)=1, y'(0)=0 -> 精确解 y(t)=cos(t)

    t_eval_coarse = np.linspace(0, np.pi, 21)   # dt = pi/20
    t_eval_fine = np.linspace(0, np.pi, 41)     # dt = pi/40

    z_coarse = solve_rk4(f, z0, t_eval_coarse)
    z_fine = solve_rk4(f, z0, t_eval_fine)

    exact_terminal = np.array([np.cos(np.pi), -np.sin(np.pi)])  # [-1, 0]
    err_coarse = np.linalg.norm(z_coarse[-1] - exact_terminal)
    err_fine = np.linalg.norm(z_fine[-1] - exact_terminal)

    # 步长减半，4 阶误差应缩小约 (1/2)^4 = 0.0625
    ratio = err_fine / err_coarse
    assert 0.05 < ratio < 0.08, f"RK4 4 阶收敛比率异常: {ratio}"


# =========================================================================
# 2. 自适应步长 RK45 测试
# =========================================================================

def test_rk45_adaptive_step_size():
    """验证 RK45 在含快速瞬态过渡的模型上自动调整步长并高精度拟合"""
    # 模型: y' = -20*(y - cos(t)) - sin(t), 初值 y(0) = 0
    # 在 t 接近 0 处具有快速指数瞬态，随后进入平滑的 cos(t) 轨道
    f = lambda t, y: -20.0 * (y - np.cos(t)) - np.sin(t)
    exact_func = lambda t: np.cos(t) - np.exp(-20.0 * t)

    t_span = (0.0, 3.0)
    t_traj, y_traj = solve_rk45_adaptive(f, 0.0, t_span, rtol=1e-5, atol=1e-7)

    assert len(t_traj) >= 10, "自适应轨迹采样点数过少"
    assert t_traj[-1] == pytest.approx(3.0, abs=1e-5)

    # 检查瞬态区域步长远小于稳态平缓区域步长
    dt_arr = np.diff(t_traj)
    dt_transient = np.min(dt_arr[:5])
    dt_smooth = np.max(dt_arr[len(dt_arr)//2:])
    assert dt_transient < dt_smooth, f"自适应步长未能检测瞬态变化: min_dt={dt_transient}, max_dt={dt_smooth}"

    # 轨迹与解析解的全局最大误差严格低于容差
    exact_vals = exact_func(t_traj)
    max_err = np.max(np.abs(y_traj - exact_vals))
    assert max_err < 5e-4, f"RK45 最大全局误差超出预期: {max_err}"


# =========================================================================
# 3. 非线性刚性隐式求解器测试
# =========================================================================

def test_backward_euler_linear_and_nonlinear_stiff():
    """验证隐式 Euler 求解器在线性与高度非线性刚性系统中的无条件稳定性"""
    # 1. 线性极度刚性系统 dy/dt = -500 * y, 初值 y(0)=1
    # 显式 Euler 当 dt > 2/500 = 0.004 时将爆炸，隐式 Euler 在 dt=0.05 下依然稳定衰减
    dt_large = 0.05
    t_eval = np.linspace(0, 1.0, 21)
    A = np.array([[-500.0]])
    y_lin = solve_backward_euler(A, np.array([1.0]), t_eval)

    assert y_lin[-1, 0] == pytest.approx(0.0, abs=1e-4)
    assert not np.any(np.isnan(y_lin))

    # 2. 非线性刚性系统: dy/dt = -50 * (y^3 - y), 初值 y(0) = 0.5
    # 注意动力学分析: y=0 为不稳定鞍点/斥子 (f'(0)=+50)，y=1 为稳定吸引子 (f'(1)=-100)
    # 利用 Newton-Raphson 隐式求解，初值 y(0)=0.5 将平滑稳定收敛至稳定吸引子 y=1.0
    f_nonlinear = lambda t, y: -50.0 * (y**3 - y)
    y_nonlin = solve_backward_euler(f_nonlinear, 0.5, t_eval, tol=1e-8)

    assert not np.any(np.isnan(y_nonlin))
    assert abs(y_nonlin[-1] - 1.0) < 0.05, f"非线性刚性求解器未正确收敛至稳定吸引子 y=1: terminal={y_nonlin[-1]}"


# =========================================================================
# 4. Lorenz 混沌动力系统测试
# =========================================================================

def test_lorenz_chaotic_trajectory():
    """验证 Lorenz 混沌吸引子生成与轨迹物理有界性"""
    t_eval = np.linspace(0, 20, 2001)
    y0 = [1.0, 1.0, 1.0]

    traj = simulate_lorenz(y0, t_eval)

    assert traj.shape == (2001, 3)
    assert not np.any(np.isnan(traj))
    # 经典 Lorenz 吸引子在空间中有界: |x|<30, |y|<40, 0<z<60
    assert np.all(np.abs(traj[:, 0]) < 35.0)
    assert np.all(np.abs(traj[:, 1]) < 45.0)
    assert np.all((traj[:, 2] > -5.0) & (traj[:, 2] < 65.0))


# =========================================================================
# 5. SDE 随机微分方程仿真测试
# =========================================================================

def test_sde_euler_maruyama():
    """验证几何布朗运动 (GBM) 的 Euler-Maruyama 统计平均与理论预期对齐"""
    # dS = mu * S * dt + sigma * S * dW, 初值 S0 = 1.0
    mu = 0.1
    sigma = 0.2
    drift = lambda t, S: mu * S
    diffusion = lambda t, S: sigma * S

    t_eval = np.linspace(0, 1.0, 101)

    # 运行多条随机轨迹验证系综均值 E[S(t)] = S0 * exp(mu * t)
    num_paths = 200
    terminal_vals = []
    for i in range(num_paths):
        path = simulate_sde_euler_maruyama(drift, diffusion, 1.0, t_eval, seed=i)
        terminal_vals.append(path[-1])

    mean_terminal = np.mean(terminal_vals)
    theoretical_mean = np.exp(mu * 1.0)  # exp(0.1) ~ 1.105

    # 统计均值应落在理论值 5% 误差范围内
    assert abs(mean_terminal - theoretical_mean) < 0.08, f"SDE 系综均值偏离理论值: {mean_terminal} vs {theoretical_mean}"


# =========================================================================
# 6. Neural ODE 伴随灵敏度求导 vs 有限差分定量测试
# =========================================================================

def test_neural_ode_adjoint_vs_finite_difference():
    """验证伴随状态法计算的 Neural ODE 权重梯度与双边有限差分梯度的相对误差 < 1%"""
    np.random.seed(42)
    dim = 2
    W_init = np.random.randn(dim, dim) * 0.5
    b_init = np.zeros(dim)

    ode_func = SimpleNeuralODEFunc(W_init, b_init)
    z0 = np.array([1.0, -0.5])
    z_target = np.array([0.2, 0.8])

    loss_adjoint, grad_adjoint = neural_ode_adjoint_gradient(
        ode_func, z0, z_target, t0=0.0, t1=1.0, num_steps=200
    )

    # 计算双边有限差分数值梯度 (Finite Difference)
    eps = 1e-5
    grad_fd = np.zeros_like(W_init)

    for i in range(dim):
        for j in range(dim):
            W_pos = W_init.copy()
            W_pos[i, j] += eps
            func_pos = SimpleNeuralODEFunc(W_pos, b_init)
            loss_pos, _ = neural_ode_adjoint_gradient(func_pos, z0, z_target, t0=0.0, t1=1.0, num_steps=200)

            W_neg = W_init.copy()
            W_neg[i, j] -= eps
            func_neg = SimpleNeuralODEFunc(W_neg, b_init)
            loss_neg, _ = neural_ode_adjoint_gradient(func_neg, z0, z_target, t0=0.0, t1=1.0, num_steps=200)

            grad_fd[i, j] = (loss_pos - loss_neg) / (2.0 * eps)

    # 计算两者的相对误差范数: ||G_adjoint - G_fd|| / (||G_fd|| + 1e-8)
    rel_error = np.linalg.norm(grad_adjoint - grad_fd) / (np.linalg.norm(grad_fd) + 1e-8)
    assert rel_error < 0.01, f"Neural ODE 伴随梯度与有限差分相对误差超出 1%: {rel_error}"


# =========================================================================
# 7. 异常输入边界测试
# =========================================================================

def test_invalid_inputs():
    """验证时间序列非单调及形状不匹配时的异常捕获"""
    f = lambda t, y: y
    with pytest.raises(ValueError, match="严格单调递增"):
        solve_euler(f, 1.0, [1.0, 0.5, 2.0])

    with pytest.raises(ValueError, match="长度 >= 2"):
        solve_rk4(f, 1.0, [1.0])

    with pytest.raises(ValueError, match="终止时间"):
        solve_rk45_adaptive(f, 1.0, (2.0, 1.0))
