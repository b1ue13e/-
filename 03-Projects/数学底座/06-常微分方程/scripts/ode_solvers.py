"""
常微分方程 (ODE) 数值求解器与仿真算法库

包含：
1. 显式 Euler & 经典 4 阶 Runge-Kutta (RK4) 求解器
2. 隐式 Euler 刚性系统求解器
3. Lorenz 混沌动力学系统仿真
4. 随机微分方程 (SDE) Euler-Maruyama 求解器
5. 神经微分方程 (Neural ODE) 伴随灵敏度 (Adjoint Sensitivity) 梯度求解器
"""

from typing import Callable, Tuple, Union, Optional
import numpy as np
from numpy.typing import NDArray

ArrayLike = Union[float, list, tuple, NDArray[np.float64]]
ODEFunc = Callable[[float, NDArray[np.float64]], NDArray[np.float64]]


def _validate_t_eval(t_eval: ArrayLike) -> NDArray[np.float64]:
    """校验并转换评估时间序列，确保单调递增且长度 >= 2"""
    t_arr = np.asarray(t_eval, dtype=np.float64)
    if t_arr.ndim != 1 or len(t_arr) < 2:
        raise ValueError("t_eval 必须为至少包含 2 个元素的一维数组/列表。")
    dt = np.diff(t_arr)
    if np.any(dt <= 0):
        raise ValueError("t_eval 必须为严格单调递增的时间序列。")
    return t_arr


# ==========================================
# 1. 基础 ODE 求解器 (Explicit & Implicit)
# ==========================================

def solve_euler(f: ODEFunc, y0: ArrayLike, t_eval: ArrayLike) -> NDArray[np.float64]:
    """
    显式 Euler 法求解器: dy/dt = f(t, y)

    公式:
        y_{n+1} = y_n + dt * f(t_n, y_n)

    参数:
        f: 导数函数，签名 (t: float, y: NDArray) -> NDArray
        y0: 初值状态向量或标量
        t_eval: 评估时间节点序列

    返回:
        NDArray: 形状为 (len(t_eval), *y0.shape) 的数值解轨迹
    """
    t_arr = _validate_t_eval(t_eval)
    y0_arr = np.asarray(y0, dtype=np.float64)
    N = len(t_arr)
    y = np.zeros((N,) + y0_arr.shape, dtype=np.float64)
    y[0] = y0_arr

    for i in range(N - 1):
        dt = t_arr[i + 1] - t_arr[i]
        f_val = np.asarray(f(t_arr[i], y[i]), dtype=np.float64)
        if f_val.shape != y0_arr.shape:
            raise ValueError(f"导数函数 f 输出形状 {f_val.shape} 与初值 y0 形状 {y0_arr.shape} 不匹配。")
        y[i + 1] = y[i] + dt * f_val

    return y


def solve_rk4(f: ODEFunc, y0: ArrayLike, t_eval: ArrayLike) -> NDArray[np.float64]:
    """
    经典 4 阶 Runge-Kutta (RK4) 求解器: dy/dt = f(t, y)

    公式:
        k1 = f(t_n, y_n)
        k2 = f(t_n + dt/2, y_n + dt/2 * k1)
        k3 = f(t_n + dt/2, y_n + dt/2 * k2)
        k4 = f(t_n + dt, y_n + dt * k3)
        y_{n+1} = y_n + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)

    参数:
        f: 导数函数，签名 (t: float, y: NDArray) -> NDArray
        y0: 初值状态向量或标量
        t_eval: 评估时间节点序列

    返回:
        NDArray: 形状为 (len(t_eval), *y0.shape) 的 4 阶数值解轨迹
    """
    t_arr = _validate_t_eval(t_eval)
    y0_arr = np.asarray(y0, dtype=np.float64)
    N = len(t_arr)
    y = np.zeros((N,) + y0_arr.shape, dtype=np.float64)
    y[0] = y0_arr

    for i in range(N - 1):
        t = t_arr[i]
        dt = t_arr[i + 1] - t
        yi = y[i]

        k1 = np.asarray(f(t, yi), dtype=np.float64)
        if k1.shape != y0_arr.shape:
            raise ValueError(f"导数函数 f 输出形状 {k1.shape} 与初值 y0 形状 {y0_arr.shape} 不匹配。")

        k2 = np.asarray(f(t + 0.5 * dt, yi + 0.5 * dt * k1), dtype=np.float64)
        k3 = np.asarray(f(t + 0.5 * dt, yi + 0.5 * dt * k2), dtype=np.float64)
        k4 = np.asarray(f(t + dt, yi + dt * k3), dtype=np.float64)

        y[i + 1] = yi + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    return y


def solve_backward_euler(f_linear_A: ArrayLike, y0: ArrayLike, t_eval: ArrayLike) -> NDArray[np.float64]:
    """
    隐式 Euler 法（针对线性刚性系统 dy/dt = A y）

    公式:
        (I - dt * A) y_{n+1} = y_n  =>  y_{n+1} = (I - dt * A)^{-1} y_n

    参数:
        f_linear_A: 线性系统系数矩阵 A，形状 (D, D)
        y0: 初值状态向量，形状 (D,)
        t_eval: 评估时间节点序列

    异常:
        ValueError: 矩阵 (I - dt * A) 奇异不可逆时抛出
    """
    t_arr = _validate_t_eval(t_eval)
    A = np.asarray(f_linear_A, dtype=np.float64)
    y0_arr = np.asarray(y0, dtype=np.float64)

    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError(f"线性系统系数矩阵 A 必须为方阵，当前形状: {A.shape}")

    dim = len(y0_arr)
    if A.shape[0] != dim:
        raise ValueError(f"矩阵 A 维度 ({A.shape[0]}) 与初值 y0 维度 ({dim}) 不一致。")

    N = len(t_arr)
    y = np.zeros((N, dim), dtype=np.float64)
    y[0] = y0_arr
    I = np.eye(dim, dtype=np.float64)

    for i in range(N - 1):
        dt = t_arr[i + 1] - t_arr[i]
        M = I - dt * A
        try:
            y[i + 1] = np.linalg.solve(M, y[i])
        except np.linalg.LinAlgError as err:
            raise ValueError(f"隐式 Euler 求解失败: 矩阵 (I - dt * A) 在步长 dt={dt} 时奇异不可逆。") from err

    return y


# ==========================================
# 2. Lorenz 混沌动力系统
# ==========================================

def lorenz_deriv(
    t: float,
    state: ArrayLike,
    sigma: float = 10.0,
    rho: float = 28.0,
    beta: float = 8.0 / 3.0
) -> NDArray[np.float64]:
    """
    Lorenz 吸引子三维非线性微分方程组：
        dx/dt = sigma * (y - x)
        dy/dt = x * (rho - z) - y
        dz/dt = x * y - beta * z
    """
    st = np.asarray(state, dtype=np.float64)
    if st.shape != (3,):
        raise ValueError(f"Lorenz 系统状态向量形状必须为 (3,)，当前形状: {st.shape}")

    x, y, z = st
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return np.array([dxdt, dydt, dzdt], dtype=np.float64)


def simulate_lorenz(
    y0: ArrayLike,
    t_eval: ArrayLike,
    sigma: float = 10.0,
    rho: float = 28.0,
    beta: float = 8.0 / 3.0
) -> NDArray[np.float64]:
    """使用 RK4 求解模拟 Lorenz 混沌轨迹"""
    f = lambda t, y: lorenz_deriv(t, y, sigma=sigma, rho=rho, beta=beta)
    return solve_rk4(f, y0, t_eval)


# ==========================================
# 3. 随机微分方程 (SDE) 求解器
# ==========================================

def simulate_sde_euler_maruyama(
    drift: ODEFunc,
    diffusion: ODEFunc,
    y0: ArrayLike,
    t_eval: ArrayLike,
    seed: Optional[int] = 42
) -> NDArray[np.float64]:
    """
    SDE Euler-Maruyama 离散求解器:
        dy = a(t, y) dt + b(t, y) dW
        其中 dW ~ Normal(0, sqrt(dt))
    """
    if seed is not None:
        np.random.seed(seed)

    t_arr = _validate_t_eval(t_eval)
    y0_arr = np.asarray(y0, dtype=np.float64)
    N = len(t_arr)
    y = np.zeros((N,) + y0_arr.shape, dtype=np.float64)
    y[0] = y0_arr

    for i in range(N - 1):
        dt = t_arr[i + 1] - t_arr[i]
        dW = np.random.normal(0.0, np.sqrt(dt), size=y0_arr.shape)
        t = t_arr[i]
        yi = y[i]

        drift_val = np.asarray(drift(t, yi), dtype=np.float64)
        diff_val = np.asarray(diffusion(t, yi), dtype=np.float64)

        y[i + 1] = yi + drift_val * dt + diff_val * dW

    return y


# ==========================================
# 4. 神经微分方程 (Neural ODE) 伴随灵敏度法
# ==========================================

class SimpleNeuralODEFunc:
    """
    简单单层 Neural ODE 函数: f(t, z; W, b) = tanh(W z + b)
    包含前向映射及其关于状态 z 和参数 W 的 Exact Jacobian 矩阵计算。
    """
    def __init__(self, weight: ArrayLike, bias: ArrayLike) -> None:
        self.W = np.asarray(weight, dtype=np.float64)
        self.b = np.asarray(bias, dtype=np.float64)

        if self.W.ndim != 2 or self.W.shape[0] != self.W.shape[1]:
            raise ValueError("权重矩阵 W 必须为二次方阵。")
        if self.b.shape != (self.W.shape[0],):
            raise ValueError(f"偏置 b 维度 {self.b.shape} 与 W 维度 {self.W.shape[0]} 不匹配。")

    def forward(self, t: float, z: NDArray[np.float64]) -> NDArray[np.float64]:
        """前向求值 f(t, z) = tanh(W z + b)"""
        return np.tanh(np.dot(self.W, z) + self.b)

    def jacobian_z(self, t: float, z: NDArray[np.float64]) -> NDArray[np.float64]:
        """df/dz = diag(1 - tanh^2(W z + b)) @ W"""
        val = np.tanh(np.dot(self.W, z) + self.b)
        dtanh = 1.0 - val**2
        return np.diag(dtanh) @ self.W

    def jacobian_W(self, t: float, z: NDArray[np.float64]) -> NDArray[np.float64]:
        """df/dW 3阶雅可比张量，形状为 (dim, dim, dim)"""
        val = np.tanh(np.dot(self.W, z) + self.b)
        dtanh = 1.0 - val**2
        dim = len(z)
        df_dW = np.zeros((dim, dim, dim), dtype=np.float64)
        for i in range(dim):
            df_dW[i, i, :] = dtanh[i] * z
        return df_dW


def neural_ode_adjoint_gradient(
    ode_func: SimpleNeuralODEFunc,
    z0: ArrayLike,
    z_target: ArrayLike,
    t0: float,
    t1: float,
    num_steps: int = 100
) -> Tuple[float, NDArray[np.float64]]:
    """
    使用伴随灵敏度方法 (Adjoint Sensitivity Method) 反向积分计算 Loss 关于 W 的梯度

    Loss 定义:
        L = 0.5 * ||z(t1) - z_target||^2

    伴随状态:
        a(t) = dL / dz(t)
        da/dt = - a(t)^T @ (df/dz)
        dL/dW = - int_{t0}^{t1} a(t)^T @ (df/dW) dt

    返回:
        Tuple[float, NDArray]: (loss_val, dL_dW)
    """
    if num_steps < 2:
        raise ValueError("num_steps 必须 >= 2。")

    t_eval = np.linspace(t0, t1, num_steps)
    dt = t_eval[1] - t_eval[0]
    z0_arr = np.asarray(z0, dtype=np.float64)
    z_target_arr = np.asarray(z_target, dtype=np.float64)

    # 1. 前向轨迹解
    f = lambda t, z: ode_func.forward(t, z)
    z_traj = solve_rk4(f, z0_arr, t_eval)

    z_terminal = z_traj[-1]
    loss = float(0.5 * np.sum((z_terminal - z_target_arr)**2))

    # 2. 终端伴随状态 a(t1) = dLoss / dz(t1)
    a_t = z_terminal - z_target_arr
    dL_dW = np.zeros_like(ode_func.W, dtype=np.float64)

    # 3. 反向伴随积分
    for i in range(num_steps - 1, 0, -1):
        t = t_eval[i]
        z = z_traj[i]

        J_z = ode_func.jacobian_z(t, z)
        J_W = ode_func.jacobian_W(t, z)

        grad_W_step = np.einsum('i,ijk->jk', a_t, J_W)
        dL_dW += grad_W_step * dt

        da_dt = - np.dot(J_z.T, a_t)
        a_t = a_t - dt * da_dt

    return loss, dL_dW

