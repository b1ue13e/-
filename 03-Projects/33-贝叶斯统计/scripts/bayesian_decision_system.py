"""End-to-End Bayesian Decision Analysis & Asymmetric Loss Optimization (Capstone Suite).

Implements:
- Asymmetric LinEx (Linear-Exponential) loss function & analytical closed form
- Quantile / Pinball Check loss function for asymmetric inventory/risk
- Full Posterior Vectorized Expected Loss Minimization over MCMC matrices
- High-stakes Business Decision Matrix: Lending default vs Approval payoff
- Comparison between Naive Plug-in Estimation and Bayesian Risk Minimization
"""
from typing import Callable, Dict, Tuple
import numpy as np


def linex_loss(theta: np.ndarray, a: float, b: float = 1.0, c: float = 2.0) -> np.ndarray:
    """LinEx 损失函数: L(theta, a) = b * (exp(c*(a - theta)) - c*(a - theta) - 1)."""
    delta = a - theta
    scaled = np.clip(c * delta, -50.0, 50.0)
    return b * (np.exp(scaled) - scaled - 1.0)


def quantile_check_loss(theta: np.ndarray, a: float, tau: float = 0.90) -> np.ndarray:
    """分位数 Check 损失函数 (Pinball Loss): (theta - a) * (tau - I(theta < a)).
    
    其后验期望最小化解为后验分布的 tau-分位数: a* = F^{-1}(tau | y).
    """
    diff = theta - a
    # 当 theta < a 时为 1, 否则为 0
    indicator = (diff < 0.0).astype(np.float64)
    return diff * (tau - indicator)


def solve_bayesian_expected_loss(
    posterior_samples: np.ndarray,
    loss_fn: Callable[[np.ndarray, float], np.ndarray],
    action_grid: np.ndarray
) -> Tuple[float, float, np.ndarray]:
    """通过全后验矩阵向量化计算期望损失曲面，输出最优行动 a* 与最小期望损失."""
    expected_losses = np.zeros_like(action_grid)
    for i, a_val in enumerate(action_grid):
        losses = loss_fn(posterior_samples, a_val)
        expected_losses[i] = float(np.mean(losses))
        
    best_idx = np.argmin(expected_losses)
    best_action = float(action_grid[best_idx])
    min_expected_loss = float(expected_losses[best_idx])
    return best_action, min_expected_loss, expected_losses


def analytical_linex_optimal_action(posterior_samples: np.ndarray, c: float = 2.0) -> float:
    """LinEx 损失的最优解析解: a* = - (1/c) * ln( E[exp(-c * theta) | y] )."""
    neg_scaled = np.clip(-c * posterior_samples, -50.0, 50.0)
    exp_mean = np.mean(np.exp(neg_scaled))
    a_star = - (1.0 / c) * np.log(max(exp_mean, 1e-12))
    return float(a_star)


def evaluate_lending_decision_policy(
    default_prob_samples: np.ndarray,
    loan_amount: float = 10000.0,
    interest_profit: float = 1200.0,
    loss_given_default: float = 8000.0,
    threshold_grid: np.ndarray = None
) -> Dict[str, float]:
    """评估金融信贷场景下不同放贷阈值的全后验期望收益与尾部破产风险."""
    if threshold_grid is None:
        threshold_grid = np.linspace(0.01, 0.30, 100)
        
    expected_profits = []
    tail_var_losses = []  # 95% 极端损失
    
    for th in threshold_grid:
        net_payoff = (1.0 - default_prob_samples) * interest_profit - default_prob_samples * loss_given_default
        selected_payoffs = np.where(default_prob_samples < th, net_payoff, 0.0)
        
        expected_profits.append(float(np.mean(selected_payoffs)))
        tail_var_losses.append(float(np.percentile(selected_payoffs, 5)))
        
    best_idx = np.argmax(expected_profits)
    best_threshold = float(threshold_grid[best_idx])
    max_expected_profit = float(expected_profits[best_idx])
    
    return {
        "best_approval_threshold": best_threshold,
        "max_expected_profit": max_expected_profit,
        "tail_5pct_payoff_at_opt": float(tail_var_losses[best_idx])
    }
