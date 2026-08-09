"""
22-概率论与数理统计 学习者实践 Starter Code 参考实现与骨架模板
提供作业编程练习的函数接口定义、类型注解与完成实现，支持自动化契约测试。
"""

import numpy as np
import scipy.stats as stats


def monte_carlo_monty_hall(n_sim: int = 100_000, random_seed: int = 42) -> tuple[float, float]:
    """
    【课后作业 01 练习 1】
    三门问题 (Monty Hall) 蒙特卡洛仿真
    返回: (win_rate_stay, win_rate_switch)
    """
    np.random.seed(random_seed)
    # 1. 真实奖品所在的门 (0, 1, 2)
    car_doors = np.random.randint(0, 3, size=n_sim)
    # 2. 参赛者初始选择的门 (假设恒选择 0 号门)
    player_choices = np.zeros(n_sim, dtype=int)
    
    # 3. 统计不换门中奖率
    win_stay = (player_choices == car_doors).mean()
    
    # 4. 换门策略：主持人打开一扇有山羊的门后，换门必然选中剩余那一扇门
    # 若初始选对(1/3)，换门必输；若初始选错(2/3)，主持人帮你排除了唯一的坏门，换门必赢！
    win_switch = (player_choices != car_doors).mean()
    
    return float(win_stay), float(win_switch)


def simulate_binary_symmetric_channel(
    n_sim: int = 500_000,
    prior_1: float = 0.4,
    p_0_to_1: float = 0.05,
    p_1_to_0: float = 0.08,
    random_seed: int = 42
) -> tuple[float, float]:
    """
    【课后作业 01 练习 2】
    二元信道传输后验概率模拟
    返回: (simulated_p_y1, simulated_posterior_x1_given_y1)
    """
    np.random.seed(random_seed)
    # 1. 产生发送信号 X in {0, 1}
    X = (np.random.rand(n_sim) < prior_1).astype(int)
    
    # 2. 生成接收信号 Y
    Y = np.zeros(n_sim, dtype=int)
    # X=0 时以 p_0_to_1 翻转为 1
    flip_0 = (X == 0) & (np.random.rand(n_sim) < p_0_to_1)
    Y[flip_0] = 1
    # X=1 时以 (1 - p_1_to_0) 保持为 1
    keep_1 = (X == 1) & (np.random.rand(n_sim) >= p_1_to_0)
    Y[keep_1] = 1
    
    # 3. 边缘概率 P(Y=1) 与后验概率 P(X=1 | Y=1)
    p_y1 = float(Y.mean())
    y1_mask = (Y == 1)
    posterior_x1 = float(X[y1_mask].mean()) if y1_mask.sum() > 0 else 0.0
    
    return p_y1, posterior_x1


def central_limit_theorem_simulation(
    dist_name: str = "exponential",
    sample_sizes: list[int] = [2, 5, 30, 100],
    n_trials: int = 10_000,
    random_seed: int = 42
) -> dict[int, dict[str, float]]:
    """
    【课后作业 02 练习 2】
    中心极限定理 (CLT) 渐近正态性收敛模拟
    返回各样本量 n 下标准化均值的均值、方差、偏度与超额峰度
    """
    np.random.seed(random_seed)
    results = {}
    
    if dist_name == "exponential":
        # Exp(lambda=1): mu=1, sigma=1
        mu, sigma = 1.0, 1.0
        draw_fn = lambda n, trials: np.random.exponential(scale=1.0, size=(trials, n))
    elif dist_name == "uniform":
        # Unif(0, 1): mu=0.5, sigma=1/sqrt(12)
        mu, sigma = 0.5, 1.0 / np.sqrt(12.0)
        draw_fn = lambda n, trials: np.random.uniform(0.0, 1.0, size=(trials, n))
    else:
        raise ValueError(f"不支持的分布族: {dist_name}")
        
    for n in sample_sizes:
        samples = draw_fn(n, n_trials) # shape: (n_trials, n)
        sample_means = samples.mean(axis=1)
        z_n = np.sqrt(n) * (sample_means - mu) / sigma
        
        results[n] = {
            "mean": float(np.mean(z_n)),
            "var": float(np.var(z_n)),
            "skewness": float(stats.skew(z_n)),
            "kurtosis": float(stats.kurtosis(z_n))
        }
        
    return results


def calculate_fishers_exact_crlb(dist_type: str, theta: float, n: int) -> float:
    """
    【阶段作业 01 练习 2】
    计算常见分布族参数的理论 Fisher 信息量与 Cramér-Rao 方差下界 (CRLB)
    """
    if n <= 0:
        raise ValueError("样本容量 n 必须为正整数")
    if theta <= 0:
        raise ValueError("参数 theta 必须为正数")
        
    if dist_type == "normal_mean":
        # X ~ N(theta, sigma^2=1), I(theta) = 1, CRLB = 1/n
        return 1.0 / n
    elif dist_type == "exponential_rate":
        # X ~ Exp(lambda=theta), I(theta) = 1/theta^2, CRLB = theta^2 / n
        return (theta ** 2) / n
    elif dist_type == "poisson_lambda":
        # X ~ Pois(lambda=theta), I(theta) = 1/theta, CRLB = theta / n
        return theta / n
    else:
        raise ValueError(f"未知分布族类型: {dist_type}")

