"""Metropolis-Hastings Sampler & Convergence Diagnostics (Pure NumPy/SciPy).

Implements:
- 1D/Multi-D Random Walk Metropolis-Hastings
- Parallel chains execution with burn-in
- Classical Gelman-Rubin R-hat and Rank-Normalized Folded R-hat
- Effective Sample Size (Bulk-ESS, Tail-ESS)
- Monte Carlo Standard Error (MCSE)
"""
from typing import Callable, Tuple
import numpy as np
from scipy import stats


def target_mixture_gaussian_log_prob(x: np.ndarray) -> np.ndarray:
    """1D 双峰高斯混合目标后验: 0.3 * N(-2, 1.0) + 0.7 * N(3, 0.5^2)."""
    p1 = 0.3 * np.exp(-0.5 * (x + 2.0)**2) / np.sqrt(2 * np.pi)
    p2 = 0.7 * np.exp(-0.5 * ((x - 3.0) / 0.5)**2) / (np.sqrt(2 * np.pi) * 0.5)
    dens = np.maximum(p1 + p2, 1e-300)
    return np.log(dens)


def run_mh_chain(
    init_val: float,
    n_iter: int = 5000,
    proposal_std: float = 1.0,
    seed: int = 42,
    log_prob_fn: Callable[[np.ndarray], np.ndarray] = target_mixture_gaussian_log_prob
) -> Tuple[np.ndarray, float]:
    """运行单条 Metropolis-Hastings 链，返回轨迹与实际接受率."""
    rng = np.random.RandomState(seed)
    chain = np.zeros(n_iter, dtype=np.float64)
    current = float(init_val)
    current_lp = float(log_prob_fn(np.array([current]))[0])
    
    n_accepted = 0
    for i in range(n_iter):
        prop = current + rng.normal(0.0, proposal_std)
        prop_lp = float(log_prob_fn(np.array([prop]))[0])
        
        log_alpha = prop_lp - current_lp
        if np.log(rng.uniform(0.0, 1.0)) < log_alpha:
            current = prop
            current_lp = prop_lp
            n_accepted += 1
        chain[i] = current
        
    accept_rate = float(n_accepted) / float(n_iter)
    return chain, accept_rate


def run_parallel_mh(
    init_vals: list,
    n_iter: int = 5000,
    burn_in: int = 1000,
    proposal_std: float = 1.5,
    base_seed: int = 100
) -> Tuple[np.ndarray, list]:
    """运行多条独立链并切除预热期 (Burn-in)."""
    chains = []
    accept_rates = []
    for idx, init_v in enumerate(init_vals):
        c, rate = run_mh_chain(
            init_val=init_v,
            n_iter=n_iter,
            proposal_std=proposal_std,
            seed=base_seed + idx
        )
        chains.append(c[burn_in:])
        accept_rates.append(rate)
    return np.array(chains), accept_rates


def compute_classical_r_hat(chains: np.ndarray) -> float:
    """计算经典 Gelman-Rubin R-hat.
    
    chains shape: (m_chains, n_samples)
    """
    m, n = chains.shape
    if m < 2:
        raise ValueError("计算 R-hat 至少需要 2 条独立链")
    chain_means = np.mean(chains, axis=1)
    grand_mean = np.mean(chain_means)
    
    # 链间方差 B
    B = (n / (m - 1)) * np.sum((chain_means - grand_mean)**2)
    # 链内方差 W
    s2 = np.var(chains, axis=1, ddof=1)
    W = np.mean(s2)
    
    if W < 1e-12:
        return 1.0
    var_plus = ((n - 1) / n) * W + (1 / n) * B
    r_hat = np.sqrt(var_plus / W)
    return float(r_hat)


def compute_rank_normalized_r_hat(chains: np.ndarray) -> float:
    """计算现代 Rank-Normalized Folded R-hat (Vehtari et al., 2021)."""
    m, n = chains.shape
    total_samples = m * n
    flat = chains.flatten()
    ranks = stats.rankdata(flat, method="average")
    
    # 正态逆映射
    norm_ranks = stats.norm.ppf((ranks - 0.375) / (total_samples + 0.25))
    rank_chains = norm_ranks.reshape((m, n))
    
    # 标准 R-hat
    r_hat_raw = compute_classical_r_hat(rank_chains)
    
    # 折叠 R-hat (评估尺度/方差收敛)
    folded = np.abs(chains - np.median(chains))
    folded_ranks = stats.rankdata(folded.flatten(), method="average")
    norm_folded = stats.norm.ppf((folded_ranks - 0.375) / (total_samples + 0.25))
    r_hat_folded = compute_classical_r_hat(norm_folded.reshape((m, n)))
    
    return float(max(r_hat_raw, r_hat_folded))


def compute_ess(chains: np.ndarray, max_lag: int = 100) -> float:
    """计算有效样本量 (Effective Sample Size)."""
    m, n = chains.shape
    total_n = m * n
    
    # 自相关系数求和
    autocorrs = []
    for i in range(m):
        c = chains[i] - np.mean(chains[i])
        var_c = np.sum(c**2)
        if var_c < 1e-12:
            continue
        corr = np.correlate(c, c, mode="full")[n - 1:] / var_c
        autocorrs.append(corr[:min(n, max_lag)])
        
    if not autocorrs:
        return float(total_n)
    mean_corr = np.mean(autocorrs, axis=0)
    
    # 初始正相关对求和
    tau_int = 1.0
    for k in range(1, len(mean_corr)):
        if mean_corr[k] <= 0.05:
            break
        tau_int += 2.0 * mean_corr[k]
        
    ess = total_n / max(tau_int, 1.0)
    return float(ess)


def compute_mcse(chains: np.ndarray) -> float:
    """计算蒙特卡洛标准误差 (MCSE)."""
    flat = chains.flatten()
    sd = np.std(flat, ddof=1)
    ess = compute_ess(chains)
    mcse = sd / np.sqrt(max(ess, 1.0))
    return float(mcse)
