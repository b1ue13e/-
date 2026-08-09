"""Eight-Schools Hierarchical Model & Shrinkage Analysis (Pure NumPy & Diagnostics).

Demonstrates:
- Analytical Partial Pooling Shrinkage factors B_j = sigma_j^2 / (sigma_j^2 + tau^2)
- Centered vs Non-Centered Parameterization sampling & Divergence tracking
- Posterior recovery on the classical Eight Schools SAT dataset
"""
import os
import csv
from typing import Dict, Tuple
import numpy as np


def load_eight_schools_csv(filepath: str = None) -> Tuple[list, np.ndarray, np.ndarray]:
    """读取 Eight Schools 数据集."""
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), "..", "data", "eight_schools.csv")
    schools = []
    y = []
    sigma = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            schools.append(row["school"])
            y.append(float(row["estimate_y"]))
            sigma.append(float(row["std_error_sigma"]))
    return schools, np.array(y, dtype=np.float64), np.array(sigma, dtype=np.float64)


def compute_analytical_shrinkage(
    y_obs: np.ndarray,
    sigma_obs: np.ndarray,
    mu: float,
    tau: float
) -> Dict[str, np.ndarray]:
    """在给定超参数 (mu, tau) 下解析计算各校收缩因子与后验条件均值."""
    var_obs = sigma_obs**2
    var_tau = max(tau**2, 1e-8)
    
    # 收缩因子 B_j in [0, 1]
    shrinkage_b = var_obs / (var_obs + var_tau)
    # 后验条件均值: (1 - B_j) * y_j + B_j * mu
    theta_post = (1.0 - shrinkage_b) * y_obs + shrinkage_b * mu
    # 后验条件方差: 1 / (1/sigma^2 + 1/tau^2) = (sigma^2 * tau^2) / (sigma^2 + tau^2)
    post_var = (var_obs * var_tau) / (var_obs + var_tau)
    
    return {
        "shrinkage_b": shrinkage_b,
        "theta_post_mean": theta_post,
        "theta_post_sd": np.sqrt(post_var)
    }


def non_centered_log_posterior(
    params: np.ndarray,
    y_obs: np.ndarray,
    sigma_obs: np.ndarray
) -> float:
    """非中心化后验对数密度: params = [mu, log_tau, theta_offset_0, ..., theta_offset_7]."""
    mu = params[0]
    log_tau = params[1]
    tau = np.exp(log_tau)
    theta_offset = params[2:]
    
    # 1. 超先验
    lp_mu = -0.5 * (mu / 10.0)**2 - np.log(10.0 * np.sqrt(2 * np.pi))
    # log_tau 对应的 HalfNormal(10) 先验带雅可比变换
    lp_tau = -0.5 * (tau / 10.0)**2 + log_tau  # Jacobian |d tau / d log_tau| = tau
    
    # 2. 标准正态先验: theta_offset ~ N(0, 1)
    lp_offsets = -0.5 * np.sum(theta_offset**2)
    
    # 3. 确定性重构与似然
    theta = mu + tau * theta_offset
    lp_lik = -0.5 * np.sum(((y_obs - theta) / sigma_obs)**2) - np.sum(np.log(sigma_obs * np.sqrt(2 * np.pi)))
    
    return float(lp_mu + lp_tau + lp_offsets + lp_lik)


def run_eight_schools_non_centered_mcmc(
    y_obs: np.ndarray,
    sigma_obs: np.ndarray,
    n_samples: int = 3000,
    seed: int = 42
) -> Dict[str, np.ndarray]:
    """运行非中心化 MCMC 采样."""
    rng = np.random.RandomState(seed)
    n_schools = len(y_obs)
    # 参数维度: mu (1) + log_tau (1) + theta_offset (8) = 10 维
    dim = 2 + n_schools
    current = np.zeros(dim)
    current[0] = np.mean(y_obs)  # mu init
    current[1] = np.log(5.0)     # log_tau init
    
    current_lp = non_centered_log_posterior(current, y_obs, sigma_obs)
    
    samples = np.zeros((n_samples, dim))
    proposal_scale = np.array([1.2, 0.4] + [0.8] * n_schools)
    
    for i in range(n_samples):
        prop = current + rng.normal(0.0, proposal_scale)
        prop_lp = non_centered_log_posterior(prop, y_obs, sigma_obs)
        
        log_alpha = prop_lp - current_lp
        if np.log(rng.uniform(0.0, 1.0)) < log_alpha:
            current = prop
            current_lp = prop_lp
        samples[i] = current
        
    # 弃去前 1000 步 burn-in
    post_samples = samples[1000:]
    mu_draws = post_samples[:, 0]
    tau_draws = np.exp(post_samples[:, 1])
    theta_offset_draws = post_samples[:, 2:]
    
    # 重构真实的 theta
    theta_draws = mu_draws[:, None] + tau_draws[:, None] * theta_offset_draws
    
    return {
        "mu": mu_draws,
        "tau": tau_draws,
        "theta": theta_draws
    }


def simulate_neals_funnel(n_samples: int = 2000, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """生成经典 Neal's Funnel 数据: y ~ N(0, 3^2), x_i ~ N(0, exp(y/2)^2)."""
    rng = np.random.RandomState(seed)
    y = rng.normal(0.0, 3.0, size=n_samples)
    scale = np.exp(y / 2.0)
    x = rng.normal(0.0, scale)
    return x, y


def detect_funnel_divergences(
    x_samples: np.ndarray,
    y_samples: np.ndarray,
    energy_threshold: float = 10.0
) -> Dict[str, object]:
    """检测漏斗颈部 (y < -2) 的数值不稳定与能量偏离 (Divergence Proxy)."""
    in_neck = y_samples < -2.0
    # 在漏斗颈部，极高曲率导致梯度爆炸，近似为势能急剧变化
    implied_scale = np.exp(y_samples / 2.0)
    # 标度残差与散度判据
    divergence_mask = in_neck & (np.abs(x_samples) > 2.5 * implied_scale)
    divergence_count = int(np.sum(divergence_mask))
    
    return {
        "total_samples": len(y_samples),
        "in_neck_count": int(np.sum(in_neck)),
        "divergence_count": divergence_count,
        "divergence_rate": float(divergence_count / len(y_samples))
    }


def get_eight_schools_pymc_code() -> str:
    """提供工业级 PyMC 5.x + ArviZ 标准非中心化层次模型代码模板."""
    return '''import pymc as pm
import arviz as az
import numpy as np

# 数据: Eight Schools SAT 辅导提分
y_obs = np.array([28.0, 8.0, -3.0, 7.0, -1.0, 1.0, 18.0, 12.0])
sigma_obs = np.array([15.0, 10.0, 16.0, 11.0, 9.0, 11.0, 10.0, 18.0])

with pm.Model(coords={"school": [f"School_{i}" for i in range(8)]}) as non_centered_model:
    # 1. 超先验
    mu = pm.Normal("mu", mu=0.0, sigma=10.0)
    tau = pm.HalfNormal("tau", sigma=10.0)
    
    # 2. 非中心化基础变量
    theta_offset = pm.Normal("theta_offset", mu=0.0, sigma=1.0, dims="school")
    
    # 3. 确定性重构真实的组别均值 (Deterministic Transform)
    theta = pm.Deterministic("theta", mu + tau * theta_offset, dims="school")
    
    # 4. 观测似然
    y = pm.Normal("y", mu=theta, sigma=sigma_obs, observed=y_obs, dims="school")
    
    # 5. NUTS 采样与收敛诊断
    idata = pm.sample(draws=2000, tune=1000, target_accept=0.95, chains=4, random_seed=42)
    
    # 6. ArviZ 收敛诊断
    summary = az.summary(idata, var_names=["mu", "tau", "theta"])
    divergences = idata.sample_stats.diverging.sum().item()
    print(f"Total Divergences: {divergences}")
'''

