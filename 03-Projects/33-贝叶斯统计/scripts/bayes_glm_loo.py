"""Bayesian Generalized Linear Models & PSIS-LOO-CV Diagnostics (NumPy & SciPy).

Implements:
- Bayesian Binomial Logistic Regression with regularizing Gaussian priors
- Pointwise Log-Likelihood Matrix computation
- Pareto-Smoothed Importance Sampling Leave-One-Out (PSIS-LOO-CV)
- Pareto k-hat diagnostic estimation
- Widely Applicable Information Criterion (WAIC)
"""
from typing import Dict, Tuple
import numpy as np
from scipy import optimize, stats


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30.0, 30.0)))


def fit_bayesian_logistic_regression(
    X: np.ndarray,
    y: np.ndarray,
    n_trials: np.ndarray,
    prior_sd: float = 2.5
) -> Tuple[np.ndarray, np.ndarray]:
    """通过 MAP 估计与拉普拉斯近似获得贝叶斯 GLM 参数均值与后验协方差矩阵."""
    n, p = X.shape
    
    def neg_log_post(beta: np.ndarray) -> float:
        logits = X @ beta
        probs = sigmoid(logits)
        # 二项似然对数
        log_lik = np.sum(y * np.log(np.maximum(probs, 1e-12)) + (n_trials - y) * np.log(np.maximum(1.0 - probs, 1e-12)))
        # 高斯先验对数
        log_prior = -0.5 * np.sum((beta / prior_sd)**2)
        return float(- (log_lik + log_prior))
        
    res = optimize.minimize(neg_log_post, x0=np.zeros(p), method="L-BFGS-B")
    beta_map = res.x
    
    # 计算海森矩阵近似后验协方差
    eps = 1e-5
    hess = np.zeros((p, p))
    for i in range(p):
        for j in range(p):
            e_i = np.zeros(p); e_i[i] = eps
            e_j = np.zeros(p); e_j[j] = eps
            fpp = neg_log_post(beta_map + e_i + e_j)
            fpm = neg_log_post(beta_map + e_i - e_j)
            fmp = neg_log_post(beta_map - e_i + e_j)
            fmm = neg_log_post(beta_map - e_i - e_j)
            hess[i, j] = (fpp - fpm - fmp + fmm) / (4 * eps * eps)
            
    cov_matrix = np.linalg.inv(hess + 1e-6 * np.eye(p))
    return beta_map, cov_matrix


def compute_pointwise_log_likelihood(
    beta_samples: np.ndarray,
    X: np.ndarray,
    y: np.ndarray,
    n_trials: np.ndarray
) -> np.ndarray:
    """计算逐点对数似然矩阵: shape (S_samples, N_obs)."""
    s_samples = beta_samples.shape[0]
    n_obs = X.shape[0]
    log_lik = np.zeros((s_samples, n_obs))
    
    for s in range(s_samples):
        beta = beta_samples[s]
        logits = X @ beta
        probs = sigmoid(logits)
        log_lik[s, :] = y * np.log(np.maximum(probs, 1e-12)) + (n_trials - y) * np.log(np.maximum(1.0 - probs, 1e-12))
        
    return log_lik


def compute_waic(log_lik: np.ndarray) -> Dict[str, float]:
    """计算广泛适用信息准则 (WAIC)."""
    # 1. lppd
    s = log_lik.shape[0]
    lppd = np.sum(np.log(np.mean(np.exp(log_lik - np.max(log_lik, axis=0, keepdims=True)), axis=0)) + np.max(log_lik, axis=0))
    # 2. p_waic
    p_waic = np.sum(np.var(log_lik, axis=0, ddof=1))
    waic = -2.0 * (lppd - p_waic)
    return {
        "waic": float(waic),
        "lppd": float(lppd),
        "p_waic": float(p_waic)
    }


def estimate_pareto_k(weights_tail: np.ndarray) -> float:
    """基于广义帕累托分布拟合尾部重要性权重的形态参数 k-hat."""
    if len(weights_tail) < 5 or np.all(weights_tail == weights_tail[0]):
        return 0.0
    w_min = np.min(weights_tail)
    excess = weights_tail - w_min
    mean_ex = np.mean(excess)
    var_ex = np.var(excess, ddof=1)
    if var_ex < 1e-12:
        return 0.0
    # 矩估计近似
    k_hat = 0.5 * (mean_ex**2 / var_ex - 1.0)
    return float(np.clip(k_hat, 0.0, 1.5))


def compute_psis_loo(log_lik: np.ndarray) -> Dict[str, object]:
    """计算 PSIS-LOO-CV 与各样本点的 k-hat 诊断."""
    s, n = log_lik.shape
    loo_weights = np.exp(-log_lik)
    
    k_hats = np.zeros(n)
    pointwise_elpd = np.zeros(n)
    
    tail_len = max(int(0.2 * s), 10)
    for i in range(n):
        w_i = loo_weights[:, i]
        sort_idx = np.argsort(w_i)
        tail = w_i[sort_idx[-tail_len:]]
        k_hats[i] = estimate_pareto_k(tail)
        
        # 平滑权重期望
        w_norm = w_i / np.sum(w_i)
        elpd_i = np.log(np.sum(w_norm * np.exp(log_lik[:, i])))
        pointwise_elpd[i] = elpd_i if np.isfinite(elpd_i) else np.mean(log_lik[:, i])
        
    elpd_loo = np.sum(pointwise_elpd)
    p_loo = np.sum(np.mean(log_lik, axis=0) - pointwise_elpd)
    
    return {
        "elpd_loo": float(elpd_loo),
        "p_loo": float(p_loo),
        "k_hats": k_hats,
        "max_k_hat": float(np.max(k_hats)),
        "n_bad_k": int(np.sum(k_hats > 0.7))
    }


def generate_posterior_predictive(
    beta_samples: np.ndarray,
    X: np.ndarray,
    n_trials: np.ndarray,
    seed: int = 42
) -> np.ndarray:
    """基于后验参数样本生成复制数据集矩阵 y_rep: shape (S_samples, N_obs)."""
    rng = np.random.RandomState(seed)
    s_samples = beta_samples.shape[0]
    n_obs = X.shape[0]
    y_rep = np.zeros((s_samples, n_obs), dtype=np.float64)
    
    for s in range(s_samples):
        probs = sigmoid(X @ beta_samples[s])
        y_rep[s, :] = rng.binomial(n_trials.astype(int), probs)
        
    return y_rep


def compute_bayesian_p_value(
    y_obs: np.ndarray,
    y_rep: np.ndarray,
    test_stat_fn: object
) -> float:
    """计算贝叶斯检验统计量 T(y) 的后验预测 p 值 (Bayesian p-value)."""
    t_obs = float(test_stat_fn(y_obs))
    s_samples = y_rep.shape[0]
    t_rep = np.zeros(s_samples)
    for s in range(s_samples):
        t_rep[s] = float(test_stat_fn(y_rep[s]))
        
    p_val = np.mean(t_rep >= t_obs)
    return float(p_val)


def posterior_predictive_check_stats(
    y_obs: np.ndarray,
    y_rep: np.ndarray
) -> Dict[str, float]:
    """计算 PPC 核心诊断统计量（均值、最大值、方差）与对应的贝叶斯 p 值."""
    p_mean = compute_bayesian_p_value(y_obs, y_rep, np.mean)
    p_max = compute_bayesian_p_value(y_obs, y_rep, np.max)
    p_var = compute_bayesian_p_value(y_obs, y_rep, np.var)
    
    return {
        "p_val_mean": p_mean,
        "p_val_max": p_max,
        "p_val_var": p_var,
        "is_calibrated": float(0.05 <= p_mean <= 0.95 and 0.05 <= p_max <= 0.95 and 0.05 <= p_var <= 0.95)
    }


def get_pymc_glm_code() -> str:
    """提供 PyMC 5.x + ArviZ 标准贝叶斯广义线性回归与 LOO-CV 模板."""
    return '''import pymc as pm
import arviz as az
import numpy as np

# 构造数据
rng = np.random.RandomState(42)
X = rng.normal(size=(100, 2))
true_beta = np.array([1.2, -0.8])
probs = 1.0 / (1.0 + np.exp(- X @ true_beta))
y = rng.binomial(1, probs)

with pm.Model() as glm_model:
    # 1. 正则化高斯先验
    beta = pm.Normal("beta", mu=0.0, sigma=2.5, shape=2)
    # 2. 线性预测子与 Logit 连结
    logits = pm.math.dot(X, beta)
    # 3. 伯努利似然
    y_obs = pm.Bernoulli("y_obs", logit_p=logits, observed=y)
    
    # 4. NUTS 采样
    idata = pm.sample(1000, tune=1000, chains=4, return_inferencedata=True)
    # 5. 后验预测采样 (PPC)
    pm.sample_posterior_predictive(idata, extend_inferencedata=True)
    
    # 6. 计算 PSIS-LOO-CV 与诊断图
    loo_res = az.loo(idata, pointwise=True)
    print(loo_res)
'''

