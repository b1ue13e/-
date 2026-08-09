"""
06-常微分方程 (ODE) 科学计算与数值求解算法库
=====================================================
包含：
1. 显式单步积分器：Explicit Euler、经典 RK4
2. 自适应步长积分器：Dormand-Prince RK45 (Adaptive Step-Size Integrator)
3. 刚性与非线性隐式求解器：基于 Newton-Raphson 迭代的通用非线性 Backward Euler
4. 动力系统仿真器：Lorenz 3D 混沌吸引子模拟
5. 随机微分方程求解器：Itô 形式 Euler-Maruyama 仿真器
6. 现代神经微分方程 (Neural ODE)：伴随灵敏度方法 (Adjoint Sensitivity Method) 反向传播求导器
"""

from typing import Callable, Optional, Tuple, Union, List
import numpy as np
from numpy.typing import ArrayLike, NDArray

ODEFunc = Callable[[float, NDArray[np.float64]], NDArray[np.float64]]
JacobianFunc = Callable[[float, NDArray[np.float64]], NDArray[np.float64]]


def _validate_t_eval(t_eval: ArrayLike) -> NDArray[np.float64]:
    """验证时间序列单调递增且长度至少为 2"""
    t_arr = np.asarray(t_eval, dtype=np.float64)
    if t_arr.ndim != 1 or len(t_arr) < 2:
        raise ValueError(f"时间序列 t_eval 必须为长度 >= 2 的一维数组，当前形状: {t_arr.shape}")
    dt = np.diff(t_arr)
    if np.any(dt <= 0.0):
        raise ValueError("时间序列 t_eval 必须严格单调递增 (dt > 0)")
    return t_arr


# =========================================================================
# 1. 经典显式求解器 (Explicit Solvers)
# =========================================================================

def solve_euler(f: ODEFunc, y0: ArrayLike, t_eval: ArrayLike) -> NDArray[np.float64]:
    """
    一阶显式欧拉积分器 (Explicit Euler Method)
    
    递推公式:
        y_{n+1} = y_n + dt * f(t_n, y_n)
    理论收敛阶: O(dt)
    """
    t_arr = _validate_t_eval(t_eval)
    y0_arr = np.asarray(y0, dtype=np.float64)
    N = len(t_arr)
    y = np.zeros((N,) + y0_arr.shape, dtype=np.float64)
    y[0] = y0_arr

    for i in range(N - 1):
        dt = t_arr[i + 1] - t_arr[i]
        t = t_arr[i]
        k1 = np.asarray(f(t, y[i]), dtype=np.float64)
        y[i + 1] = y[i] + dt * k1

    return y


def solve_rk4(f: ODEFunc, y0: ArrayLike, t_eval: ArrayLike) -> NDArray[np.float64]:
    """
    经典四阶 Runge-Kutta 积分器 (RK4)
    
    递推公式:
        k1 = f(t_n, y_n)
        k2 = f(t_n + 0.5*dt, y_n + 0.5*dt*k1)
        k3 = f(t_n + 0.5*dt, y_n + 0.5*dt*k2)
        k4 = f(t_n + dt, y_n + dt*k3)
        y_{n+1} = y_n + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)
    理论收敛阶: O(dt^4)
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
        k2 = np.asarray(f(t + 0.5 * dt, yi + 0.5 * dt * k1), dtype=np.float64)
        k3 = np.asarray(f(t + 0.5 * dt, yi + 0.5 * dt * k2), dtype=np.float64)
        k4 = np.asarray(f(t + dt, yi + dt * k3), dtype=np.float64)

        y[i + 1] = yi + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    return y


# =========================================================================
# 2. 自适应步长求解器 (Adaptive Step-Size RK45)
# =========================================================================

def solve_rk45_adaptive(
    f: ODEFunc,
    y0: ArrayLike,
    t_span: Tuple[float, float],
    rtol: float = 1e-6,
    atol: float = 1e-8,
    h_init: Optional[float] = None,
    h_min: float = 1e-12,
    h_max: Optional[float] = None,
    max_steps: int = 100000
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    嵌入式 Dormand-Prince 5(4) 阶自适应步长积分器 (RK45)
    
    根据局部截断误差 (Local Truncation Error) 自动调整积分步长 dt，
    在平缓区域增大步长加速计算，在剧烈变化/奇异区域自动缩小步长保证精度。
    
    参数:
        f: 导数函数 (t: float, y: NDArray) -> NDArray
        y0: 初值向量
        t_span: (t_start, t_end) 积分起止时间
        rtol: 相对误差容限
        atol: 绝对误差容限
        h_init: 初始步长 (若为 None 则根据初值自动选取)
        h_min: 允许的最小步长
        h_max: 允许的最大步长
        max_steps: 最大迭代步数
        
    返回:
        (t_traj, y_traj): 成功积分的时间点与状态轨迹
    """
    t0, tf = float(t_span[0]), float(t_span[1])
    if tf <= t0:
        raise ValueError(f"终止时间 tf={tf} 必须大于起始时间 t0={t0}")

    y0_arr = np.asarray(y0, dtype=np.float64)
    dim = y0_arr.shape

    # Butcher 表系数 (Dormand-Prince)
    c = np.array([0.0, 1.0/5.0, 3.0/10.0, 4.0/5.0, 8.0/9.0, 1.0, 1.0])
    a = [
        [],
        [1.0/5.0],
        [3.0/40.0, 9.0/40.0],
        [44.0/45.0, -56.0/15.0, 32.0/9.0],
        [19372.0/6561.0, -25360.0/2187.0, 64448.0/6561.0, -212.0/729.0],
        [9017.0/3168.0, -355.0/33.0, 46732.0/5247.0, 49.0/176.0, -5103.0/18656.0],
        [35.0/384.0, 0.0, 500.0/1113.0, 125.0/192.0, -2187.0/6784.0, 11.0/84.0]
    ]
    # 5阶解权重 b5
    b5 = np.array([35.0/384.0, 0.0, 500.0/1113.0, 125.0/192.0, -2187.0/6784.0, 11.0/84.0, 0.0])
    # 4阶解权重 b4
    b4 = np.array([5179.0/57600.0, 0.0, 7571.0/16695.0, 393.0/640.0, -92097.0/339200.0, 187.0/2100.0, 1.0/40.0])
    # 误差权重 e = b5 - b4
    e = b5 - b4

    if h_max is None:
        h_max = (tf - t0) / 10.0
    if h_init is None:
        h = min(h_max, (tf - t0) / 100.0)
    else:
        h = min(h_max, max(h_min, float(h_init)))

    t_list = [t0]
    y_list = [y0_arr.copy()]

    t = t0
    y = y0_arr.copy()
    step_count = 0

    while t < tf and step_count < max_steps:
        step_count += 1
        if t + h > tf:
            h = tf - t

        # 计算 7 个阶段的斜率 k
        k: List[NDArray[np.float64]] = []
        for stage in range(7):
            if stage == 0:
                y_stage = y
            else:
                dy = sum(a[stage][j] * k[j] for j in range(stage))
                y_stage = y + h * dy
            t_stage = t + c[stage] * h
            k.append(np.asarray(f(t_stage, y_stage), dtype=np.float64))

        # 5 阶候选解与 4 阶误差估计
        y5 = y + h * sum(b5[j] * k[j] for j in range(7))
        err_vec = h * sum(e[j] * k[j] for j in range(7))

        # 误差标度与范数
        scale = atol + rtol * np.maximum(np.abs(y), np.abs(y5))
        err_ratio = np.max(np.abs(err_vec) / scale)

        if err_ratio <= 1.0:
            # 步长接受
            t = t + h
            y = y5
            t_list.append(t)
            y_list.append(y.copy())

            # 预测下一步长 (安全系数 0.9)
            if err_ratio == 0.0:
                factor = 2.0
            else:
                factor = min(5.0, max(0.2, 0.9 * (1.0 / err_ratio) ** 0.2))
            h = min(h_max, max(h_min, h * factor))
        else:
            # 步长拒绝，缩小重试
            factor = min(0.9, max(0.1, 0.9 * (1.0 / err_ratio) ** 0.25))
            h = max(h_min, h * factor)
            if h <= h_min and t + h == t:
                raise RuntimeError(f"RK45 在 t={t} 步长达到下限 h_min={h_min} 仍无法满足误差容限，系统可能发生刚性爆炸或奇点。")

    return np.array(t_list, dtype=np.float64), np.array(y_list, dtype=np.float64)


# =========================================================================
# 3. 刚性与非线性隐式求解器 (Implicit Solvers with Newton-Raphson)
# =========================================================================

def _approx_jacobian(f: ODEFunc, t: float, y: NDArray[np.float64], eps: float = 1e-7) -> NDArray[np.float64]:
    """数值有限差分计算雅可比矩阵 df/dy"""
    dim = len(y)
    J = np.zeros((dim, dim), dtype=np.float64)
    f0 = np.asarray(f(t, y), dtype=np.float64)
    for j in range(dim):
        y_pert = y.copy()
        y_pert[j] += eps
        f_pert = np.asarray(f(t, y_pert), dtype=np.float64)
        J[:, j] = (f_pert - f0) / eps
    return J


def solve_backward_euler(
    f: Union[ODEFunc, ArrayLike],
    y0: ArrayLike,
    t_eval: ArrayLike,
    jacobian: Optional[JacobianFunc] = None,
    tol: float = 1e-7,
    max_iter: int = 50
) -> NDArray[np.float64]:
    """
    通用隐式欧拉求解器 (Nonlinear Backward Euler with Newton-Raphson)
    
    支持两类输入：
    1. 线性系统: 若 f 传入 (D, D) 矩阵 A，则直接求解线性方程组 (I - dt * A) y_{n+1} = y_n；
    2. 一般非线性系统: 若 f 传入可调用函数，则使用 Newton-Raphson 迭代求解隐式非线性代数方程:
       G(y_{n+1}) = y_{n+1} - y_n - dt * f(t_{n+1}, y_{n+1}) = 0
       
    理论优势: A-稳定 (A-stable)，可稳定积分高度刚性 (Stiff) 微分方程，无步长稳定性爆炸限制。
    """
    t_arr = _validate_t_eval(t_eval)
    y0_arr = np.asarray(y0, dtype=np.float64)
    is_scalar = (y0_arr.ndim == 0)
    if is_scalar:
        y0_vec = y0_arr.reshape(1)
    else:
        y0_vec = y0_arr

    dim = len(y0_vec)
    N = len(t_arr)
    y = np.zeros((N, dim), dtype=np.float64)
    y[0] = y0_vec
    I = np.eye(dim, dtype=np.float64)

    # 1. 纯线性矩阵快捷分支
    if isinstance(f, (np.ndarray, list)):
        A = np.asarray(f, dtype=np.float64)
        if A.shape != (dim, dim):
            raise ValueError(f"系数矩阵 A 形状 {A.shape} 与初值维度 {dim} 不匹配。")
        for i in range(N - 1):
            dt = t_arr[i + 1] - t_arr[i]
            M = I - dt * A
            try:
                y[i + 1] = np.linalg.solve(M, y[i])
            except np.linalg.LinAlgError as err:
                raise ValueError(f"隐式 Euler 求解失败: 矩阵奇异不可逆 (dt={dt})") from err
        return y.reshape(N) if is_scalar else y

    # 2. 通用非线性系统 Newton-Raphson 迭代分支
    ode_func: ODEFunc = f
    for i in range(N - 1):
        dt = t_arr[i + 1] - t_arr[i]
        t_next = t_arr[i + 1]
        y_curr = y[i]

        # 初始猜测：显式 Euler 步
        f_curr = np.asarray(ode_func(t_arr[i], y_curr), dtype=np.float64).reshape(dim)
        y_next = y_curr + dt * f_curr

        converged = False
        for it in range(max_iter):
            f_next = np.asarray(ode_func(t_next, y_next), dtype=np.float64).reshape(dim)
            G = y_next - y_curr - dt * f_next

            if np.linalg.norm(G, ord=np.inf) < tol:
                converged = True
                break

            # 计算 Jacobian dG/dy = I - dt * df/dy
            if jacobian is not None:
                J_f = np.asarray(jacobian(t_next, y_next), dtype=np.float64).reshape(dim, dim)
            else:
                J_f = _approx_jacobian(ode_func, t_next, y_next)

            dG_dy = I - dt * J_f
            try:
                delta = np.linalg.solve(dG_dy, -G)
            except np.linalg.LinAlgError:
                delta = -G * 0.1  # 奇异降级微步

            y_next = y_next + delta

        if not converged:
            # 达到最大迭代次数仍未满足 tol
            pass

        y[i + 1] = y_next

    return y.reshape(N) if is_scalar else y


# =========================================================================
# 4. 动力系统仿真器 (Lorenz Attractor)
# =========================================================================

def lorenz_deriv(
    t: float,
    state: ArrayLike,
    sigma: float = 10.0,
    rho: float = 28.0,
    beta: float = 8.0 / 3.0
) -> NDArray[np.float64]:
    """
    Lorenz 3D 经典非线性混沌动力系统:
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
    """使用经典 RK4 积分生成 Lorenz 混沌轨迹"""
    f = lambda t, y: lorenz_deriv(t, y, sigma=sigma, rho=rho, beta=beta)
    return solve_rk4(f, y0, t_eval)


# =========================================================================
# 5. 随机微分方程仿真器 (SDE Euler-Maruyama)
# =========================================================================

def simulate_sde_euler_maruyama(
    drift: ODEFunc,
    diffusion: ODEFunc,
    y0: ArrayLike,
    t_eval: ArrayLike,
    seed: Optional[int] = 42
) -> NDArray[np.float64]:
    """
    Itô 形式 SDE Euler-Maruyama 离散积分器:
        dy = a(t, y) dt + b(t, y) dW
    其中布朗运动微元 dW ~ Normal(0, sqrt(dt))
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


# =========================================================================
# 6. 神经微分方程 (Neural ODE) 伴随灵敏度反向传播
# =========================================================================

class SimpleNeuralODEFunc:
    """
    参数化单层 Neural ODE 动力函数: f(t, z; W, b) = tanh(W z + b)
    包含前向映射、关于状态 z 的解析 Jacobian 以及关于权重 W 的张量导数。
    """
    def __init__(self, weight: ArrayLike, bias: ArrayLike) -> None:
        self.W = np.asarray(weight, dtype=np.float64)
        self.b = np.asarray(bias, dtype=np.float64)

        if self.W.ndim != 2 or self.W.shape[0] != self.W.shape[1]:
            raise ValueError(f"权重矩阵 W 必须为方阵，当前形状: {self.W.shape}")
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
        """df/dW 3阶张量，形状为 (dim, dim, dim)"""
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
    使用伴随灵敏度方法 (Adjoint Sensitivity Method) 反向积分计算 Loss 关于参数 W 的全梯度
    
    数学原理:
        Loss = 0.5 * ||z(t1) - z_target||^2
        伴随状态 a(t) = dL / dz(t)
        伴随微分方程: da/dt = - a(t)^T @ (df/dz)
        参数梯度: dL/dW = - int_{t1}^{t0} a(t)^T @ (df/dW) dt
    """
    if num_steps < 2:
        raise ValueError("积分步数 num_steps 必须 >= 2")

    t_eval = np.linspace(t0, t1, num_steps)
    dt = t_eval[1] - t_eval[0]
    z0_arr = np.asarray(z0, dtype=np.float64)
    z_target_arr = np.asarray(z_target, dtype=np.float64)

    # 1. 前向积分求解状态轨迹
    f = lambda t, z: ode_func.forward(t, z)
    z_traj = solve_rk4(f, z0_arr, t_eval)

    z_terminal = z_traj[-1]
    loss = float(0.5 * np.sum((z_terminal - z_target_arr)**2))

    # 2. 终端边界条件 a(t1) = dLoss / dz(t1) = z(t1) - z_target
    a_t = z_terminal - z_target_arr
    dL_dW = np.zeros_like(ode_func.W, dtype=np.float64)

    # 3. 反向伴随积分 (从 t1 逆向积分到 t0)
    for i in range(num_steps - 1, 0, -1):
        t = t_eval[i]
        z = z_traj[i]

        J_z = ode_func.jacobian_z(t, z)
        J_W = ode_func.jacobian_W(t, z)

        # 梯度的黎曼积分累加: a(t)^T @ (df/dW) * dt
        grad_step = np.einsum('i,ijk->jk', a_t, J_W)
        dL_dW += grad_step * dt

        # 伴随状态逆向更新
        da_dt = - np.dot(J_z.T, a_t)
        a_t = a_t - dt * da_dt

    return loss, dL_dW
