"""
22-概率论与数理统计 工业级数理统计与推断计算引擎
提供严谨的极大似然估计 (含 Fisher 观测信息矩阵与标准误)、BCa 非参数重抽样、
单因素 ANOVA、多重检验 FDR 控制与多元线性回归推断。
"""

import numpy as np
import scipy.stats as stats
from scipy.optimize import minimize
from scipy.special import gammaln


# ==========================================
# 1. 贝叶斯与概率逆向推断模块
# ==========================================

def bayes_posterior_calc(prior: float, sensitivity: float, false_positive: float) -> float:
    """
    计算二元事件的贝叶斯后验概率 P(D | T+)
    """
    prior = float(np.clip(prior, 1e-12, 1.0 - 1e-12))
    sens = float(np.clip(sensitivity, 1e-12, 1.0))
    fp = float(np.clip(false_positive, 0.0, 1.0))
    
    numerator = prior * sens
    denominator = numerator + (1.0 - prior) * fp
    if denominator <= 0:
        return 0.0
    return float(numerator / denominator)


def bayes_discrete_table_update(priors: np.ndarray, likelihoods: np.ndarray) -> np.ndarray:
    """
    多假设离散贝叶斯信念更新 (使用 Log-Sum-Exp 避免数值下溢)
    """
    priors = np.asarray(priors, dtype=float)
    likelihoods = np.asarray(likelihoods, dtype=float)
    assert len(priors) == len(likelihoods), "先验与似然维度必须一致"
    
    log_unnorm = np.log(np.clip(priors, 1e-15, None)) + np.log(np.clip(likelihoods, 1e-15, None))
    max_log = np.max(log_unnorm)
    unnorm = np.exp(log_unnorm - max_log)
    posteriors = unnorm / np.sum(unnorm)
    return posteriors


# ==========================================
# 2. 极大似然估计 (MLE) 与信息矩阵推断
# ==========================================

class MLEFitter:
    """
    连续分布参数极大似然估计器
    输出最优参数、最大对数似然、AIC/BIC、Fisher 观测信息矩阵与参数渐近标准误
    """
    
    @staticmethod
    def fit_normal(data: np.ndarray) -> dict:
        data = np.asarray(data, dtype=float)
        n = len(data)
        mu_hat = float(np.mean(data))
        sigma2_hat = float(np.mean((data - mu_hat) ** 2)) # MLE 无偏方差前系数为 1/n
        sigma_hat = float(np.sqrt(sigma2_hat))
        
        log_lik = -0.5 * n * np.log(2.0 * np.pi * sigma2_hat) - 0.5 * n
        aic = 2 * 2 - 2 * log_lik
        bic = 2 * np.log(n) - 2 * log_lik
        
        # Fisher 观测信息矩阵: diag(n/sigma^2, n/(2*sigma^4))
        se_mu = float(sigma_hat / np.sqrt(n))
        se_sigma2 = float(sigma2_hat * np.sqrt(2.0 / n))
        
        return {
            "model": "Normal",
            "params": {"mu": mu_hat, "sigma2": sigma2_hat, "sigma": sigma_hat},
            "log_lik": float(log_lik),
            "aic": float(aic),
            "bic": float(bic),
            "se": {"mu": se_mu, "sigma2": se_sigma2},
            "cov_matrix": np.diag([se_mu ** 2, se_sigma2 ** 2])
        }

    @staticmethod
    def fit_lognormal(data: np.ndarray) -> dict:
        data = np.asarray(data, dtype=float)
        assert np.all(data > 0), "对数正态数据必须严格为正"
        n = len(data)
        log_data = np.log(data)
        
        mu_hat = float(np.mean(log_data))
        sigma2_hat = float(np.mean((log_data - mu_hat) ** 2))
        sigma_hat = float(np.sqrt(sigma2_hat))
        
        log_lik = -np.sum(log_data) - 0.5 * n * np.log(2.0 * np.pi * sigma2_hat) - 0.5 * n
        aic = 2 * 2 - 2 * log_lik
        bic = 2 * np.log(n) - 2 * log_lik
        
        se_mu = float(sigma_hat / np.sqrt(n))
        se_sigma2 = float(sigma2_hat * np.sqrt(2.0 / n))
        
        return {
            "model": "Lognormal",
            "params": {"mu_log": mu_hat, "sigma2_log": sigma2_hat, "sigma_log": sigma_hat},
            "log_lik": float(log_lik),
            "aic": float(aic),
            "bic": float(bic),
            "se": {"mu_log": se_mu, "sigma2_log": se_sigma2}
        }

    @staticmethod
    def fit_gamma(data: np.ndarray) -> dict:
        data = np.asarray(data, dtype=float)
        assert np.all(data > 0), "Gamma 数据必须严格为正"
        n = len(data)
        mean_x = float(np.mean(data))
        var_x = float(np.var(data, ddof=1))
        
        # 矩估计初值
        alpha_init = max(0.1, (mean_x ** 2) / max(1e-6, var_x))
        beta_init = max(0.1, mean_x / max(1e-6, var_x)) # Rate 参数: pdf ~ x^{a-1} e^{-b x}
        
        sum_x = float(np.sum(data))
        sum_log_x = float(np.sum(np.log(data)))
        
        def neg_log_lik(params):
            a, b = params
            if a <= 1e-6 or b <= 1e-6:
                return 1e12
            ll = n * (a * np.log(b) - gammaln(a)) + (a - 1.0) * sum_log_x - b * sum_x
            return -ll

        res = minimize(
            neg_log_lik,
            [alpha_init, beta_init],
            method='L-BFGS-B',
            bounds=[(1e-5, None), (1e-5, None)]
        )
        if not res.success:
            raise RuntimeError(f"Gamma MLE optimization failed: {res.message}")
            
        alpha_hat, beta_hat = float(res.x[0]), float(res.x[1])
        log_lik = -float(res.fun)
        aic = 2 * 2 - 2 * log_lik
        bic = 2 * np.log(n) - 2 * log_lik
        
        # 数值 Hessian 矩阵近似计算标准误
        eps = 1e-4
        h = np.zeros((2, 2))
        p = np.array([alpha_hat, beta_hat])
        for i in range(2):
            for j in range(2):
                p_pp = p.copy(); p_pp[i] += eps; p_pp[j] += eps
                p_pm = p.copy(); p_pm[i] += eps; p_pm[j] -= eps
                p_mp = p.copy(); p_mp[i] -= eps; p_mp[j] += eps
                p_mm = p.copy(); p_mm[i] -= eps; p_mm[j] -= eps
                h[i, j] = (neg_log_lik(p_pp) - neg_log_lik(p_pm) - neg_log_lik(p_mp) + neg_log_lik(p_mm)) / (4 * eps * eps)
        try:
            cov_mat = np.linalg.inv(h)
            se_alpha = float(np.sqrt(max(1e-10, cov_mat[0, 0])))
            se_beta = float(np.sqrt(max(1e-10, cov_mat[1, 1])))
        except Exception as err:
            raise RuntimeError(f"Hessian 观测信息矩阵计算逆矩阵失败: {err}")

        return {
            "model": "Gamma",
            "params": {"alpha": alpha_hat, "beta": beta_hat, "scale": 1.0 / beta_hat},
            "log_lik": float(log_lik),
            "aic": float(aic),
            "bic": float(bic),
            "se": {"alpha": se_alpha, "beta": se_beta},
            "cov_matrix": cov_mat
        }


# ==========================================
# 3. 非参数 Bootstrap 与 BCa 稳健区间
# ==========================================

def bootstrap_percentile_ci(
    data: np.ndarray,
    stat_func=np.median,
    n_boot: int = 2000,
    alpha: float = 0.05,
    random_state: int = 42
) -> tuple[float, float, float]:
    """
    标准百分位数 Bootstrap 置信区间
    返回: (ci_lower, ci_upper, boot_se)
    """
    data = np.asarray(data, dtype=float)
    n = len(data)
    rng = np.random.default_rng(random_state)
    
    boot_indices = rng.integers(0, n, size=(n_boot, n))
    boot_samples = data[boot_indices]
    boot_stats = np.apply_along_axis(stat_func, 1, boot_samples)
    
    ci_lower = float(np.percentile(boot_stats, 100 * (alpha / 2.0)))
    ci_upper = float(np.percentile(boot_stats, 100 * (1.0 - alpha / 2.0)))
    boot_se = float(np.std(boot_stats, ddof=1))
    
    return ci_lower, ci_upper, boot_se


def bootstrap_bca_ci(
    data: np.ndarray,
    stat_func=np.median,
    n_boot: int = 2000,
    alpha: float = 0.05,
    random_state: int = 42
) -> tuple[float, float, float]:
    """
    偏差校正与加速 (BCa) Bootstrap 置信区间 (应对偏态与厚尾统计量)
    """
    data = np.asarray(data, dtype=float)
    n = len(data)
    theta_hat = stat_func(data)
    rng = np.random.default_rng(random_state)
    
    # 1. Bootstrap 重抽样
    boot_indices = rng.integers(0, n, size=(n_boot, n))
    boot_samples = data[boot_indices]
    boot_stats = np.apply_along_axis(stat_func, 1, boot_samples)
    boot_se = float(np.std(boot_stats, ddof=1))
    
    # 2. 偏差校正参数 z0
    prop_less = np.mean(boot_stats < theta_hat)
    prop_less = np.clip(prop_less, 1e-5, 1.0 - 1e-5)
    z0 = stats.norm.ppf(prop_less)
    
    # 3. 加速度参数 a (Jackknife 留一法近似)
    jackknife_stats = np.zeros(n)
    for i in range(n):
        jk_data = np.delete(data, i)
        jackknife_stats[i] = stat_func(jk_data)
    jk_mean = np.mean(jackknife_stats)
    diff = jk_mean - jackknife_stats
    
    denom = 6.0 * (np.sum(diff ** 2) ** 1.5)
    if denom == 0:
        a = 0.0
    else:
        a = float(np.sum(diff ** 3) / denom)
    
    # 4. 调整分位数 alpha1 与 alpha2
    z_alpha_low = stats.norm.ppf(alpha / 2.0)
    z_alpha_high = stats.norm.ppf(1.0 - alpha / 2.0)
    
    def adjust_q(z_alpha):
        denom_q = 1.0 - a * (z0 + z_alpha)
        if abs(denom_q) < 1e-8:
            denom_q = 1e-8
        adj_z = z0 + (z0 + z_alpha) / denom_q
        return float(stats.norm.cdf(adj_z))
    
    q_low = np.clip(adjust_q(z_alpha_low), 1e-4, 1.0 - 1e-4)
    q_high = np.clip(adjust_q(z_alpha_high), 1e-4, 1.0 - 1e-4)
    
    ci_lower = float(np.percentile(boot_stats, 100 * q_low))
    ci_upper = float(np.percentile(boot_stats, 100 * q_high))
    
    return ci_lower, ci_upper, boot_se


# ==========================================
# 4. 假设检验、方差分析与多重校正 (FDR)
# ==========================================

def one_way_anova(groups: list[np.ndarray]) -> dict:
    """
    单因素方差分析 (One-way ANOVA) 求解引擎与效应量计算
    """
    k = len(groups)
    assert k >= 2, "ANOVA 需要至少 2 个组"
    
    group_lens = [len(g) for g in groups]
    N = sum(group_lens)
    all_data = np.concatenate(groups)
    grand_mean = float(np.mean(all_data))
    
    group_means = [float(np.mean(g)) for g in groups]
    
    ssb = sum(n_i * (m_i - grand_mean) ** 2 for n_i, m_i in zip(group_lens, group_means))
    ssw = sum(np.sum((g - np.mean(g)) ** 2) for g in groups)
    sst = np.sum((all_data - grand_mean) ** 2)
    
    df_between = k - 1
    df_within = N - k
    
    msb = ssb / df_between
    msw = ssw / df_within
    
    f_stat = msb / max(1e-12, msw)
    p_val = float(1.0 - stats.f.cdf(f_stat, df_between, df_within))
    eta_squared = float(ssb / max(1e-12, sst)) # 效应量
    
    return {
        "SST": float(sst),
        "SSB": float(ssb),
        "SSW": float(ssw),
        "df_between": df_between,
        "df_within": df_within,
        "MSB": float(msb),
        "MSW": float(msw),
        "F_stat": float(f_stat),
        "p_val": p_val,
        "eta_squared": eta_squared
    }


def benjamini_hochberg_fdr(p_values: np.ndarray, alpha: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
    """
    Benjamini-Hochberg (BH) 错误发现率 (FDR) 多重检验控制算法
    返回: (rejected_mask, adjusted_p_values)
    """
    p_vals = np.asarray(p_values, dtype=float)
    m = len(p_vals)
    sorted_indices = np.argsort(p_vals)
    sorted_p = p_vals[sorted_indices]
    
    # 计算调整 p 值
    adj_p = np.zeros(m)
    adj_p[-1] = sorted_p[-1]
    for i in range(m - 2, -1, -1):
        rank = i + 1
        adj_p[i] = min(adj_p[i + 1], sorted_p[i] * m / rank)
    adj_p = np.clip(adj_p, 0.0, 1.0)
    
    # 恢复原序列
    original_adj_p = np.zeros(m)
    original_adj_p[sorted_indices] = adj_p
    
    rejected = original_adj_p <= alpha
    return rejected, original_adj_p


# ==========================================
# 5. 多元线性回归与统计推断 (OLS)
# ==========================================

def linear_regression_fit(X: np.ndarray, y: np.ndarray) -> dict:
    """
    多元线性回归普通最小二乘法 (OLS) 解析解、假设推断与残差诊断
    """
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n, p = X.shape
    assert n > p, f"样本量 n ({n}) 必须大于特征数 p ({p})"
    
    XtX = X.T @ X
    XtX_inv = np.linalg.inv(XtX)
    beta_hat = XtX_inv @ X.T @ y
    
    y_pred = X @ beta_hat
    residuals = y - y_pred
    sse = float(np.sum(residuals ** 2))
    
    df_resid = n - p
    sigma2_hat = float(sse / df_resid)
    cov_beta = sigma2_hat * XtX_inv
    se_beta = np.sqrt(np.diag(cov_beta))
    
    t_stats = beta_hat / se_beta
    p_vals = 2.0 * (1.0 - stats.t.cdf(np.abs(t_stats), df=df_resid))
    
    sst = float(np.sum((y - np.mean(y)) ** 2))
    r2 = float(1.0 - (sse / max(1e-12, sst)))
    adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / df_resid)
    
    # 整体 F 检验
    ssr = sst - sse
    df_model = p - 1
    if df_model > 0 and sse > 0:
        f_stat = float((ssr / df_model) / (sse / df_resid))
        f_pval = float(1.0 - stats.f.cdf(f_stat, df_model, df_resid))
    else:
        f_stat, f_pval = 0.0, 1.0

    # 方差膨胀因子 (VIF) 诊断多重共线性
    vif = []
    if p > 1:
        corr_matrix = np.corrcoef(X[:, 1:], rowvar=False) if p > 2 else np.array([[1.0]])
        if p > 2:
            try:
                inv_corr = np.linalg.inv(corr_matrix)
                vif = [float(inv_corr[i, i]) for i in range(p - 1)]
            except Exception:
                vif = [float("inf")] * (p - 1)
        else:
            vif = [1.0]

    # Jarque-Bera 残差正态性检验
    skew = float(stats.skew(residuals))
    kurt = float(stats.kurtosis(residuals)) # excess kurtosis
    jb_stat = float((n / 6.0) * (skew ** 2 + 0.25 * (kurt ** 2)))
    jb_pval = float(1.0 - stats.chi2.cdf(jb_stat, df=2))

    return {
        "beta_hat": beta_hat,
        "se_beta": se_beta,
        "t_stats": t_stats,
        "p_vals": p_vals,
        "sigma2_hat": sigma2_hat,
        "R2": r2,
        "Adj_R2": adj_r2,
        "F_stat": f_stat,
        "F_pval": f_pval,
        "residuals": residuals,
        "VIF": vif,
        "JB_stat": jb_stat,
        "JB_pval": jb_pval
    }
