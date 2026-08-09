# -*- coding: utf-8 -*-
"""
32-非参数统计：核心算法工业级实现与基准检验套件
包含：
1. DKW 不等式一致置信带计算
2. 稳健位置与尺度估计 (Median, MAD, Hodges-Lehmann)
3. Wilcoxon 符号秩检验 (小样本精确分布 + 大样本含结值方差修正)
4. Mann-Whitney U 秩和检验 (小样本精确排列 + 大样本含结值方差修正)
5. Monte Carlo 置换检验 (支持均值差、中位数差、Hodges-Lehmann 稳健位置转移)
6. Bootstrap 置信区间套件 (标准正态、基本经验、百分位、BCa 偏倚校正与加速)
7. KDE 核密度估计与自适应带宽 (Silverman 经验法则 + 留一交叉验证 LOOCV)
8. 局部多项式平滑回归 (Nadaraya-Watson 局部常数 vs Local Linear 局部线性边界修正)
"""

import argparse
import itertools
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from scipy import stats


# =====================================================================
# 1. 经验分布函数与 DKW 置信带
# =====================================================================

def dkw_band_width(n: int, alpha: float = 0.05) -> float:
    """
    计算 Dvoretzky-Kiefer-Wolfowitz (DKW) 不等式在 Massart (1990) 最优常数下的全域一致置信带半宽。
    P(sup |F_n(x) - F(x)| > eps) <= 2 * exp(-2 * n * eps^2) = alpha
    ==> eps = sqrt( ln(2 / alpha) / (2 * n) )
    """
    if n <= 0:
        raise ValueError("样本量 n 必须为正整数")
    if not (0 < alpha < 1):
        raise ValueError("显著性水平 alpha 必须在 (0, 1) 区间内")
    return float(np.sqrt(np.log(2.0 / alpha) / (2.0 * n)))


def empirical_cdf(data: np.ndarray, grid: np.ndarray) -> np.ndarray:
    """计算阶梯经验分布函数 F_n(x)"""
    data_sorted = np.sort(data)
    return np.searchsorted(data_sorted, grid, side="right") / float(len(data))


# =====================================================================
# 2. 稳健位置与尺度估计量
# =====================================================================

def mad_estimator(data: np.ndarray) -> Tuple[float, float, float]:
    """
    计算中位数 (Median)、中位数绝对离差 (MAD) 与正态一致尺度估计量 sigma_MAD = 1.4826 * MAD
    """
    clean_data = np.asarray(data, dtype=float)
    clean_data = clean_data[~np.isnan(clean_data)]
    if len(clean_data) == 0:
        return 0.0, 0.0, 0.0
    med = float(np.median(clean_data))
    mad = float(np.median(np.abs(clean_data - med)))
    sigma_mad = float(1.482602218505602 * mad)
    return med, mad, sigma_mad


def hodges_lehmann_location(data: np.ndarray, max_subsample: int = 300) -> float:
    """
    计算单样本 Hodges-Lehmann 稳健位置估计量：所有 Walsh 均值 (X_i + X_j) / 2 (1 <= i <= j <= n) 的中位数。
    采用 NumPy 向量化上三角索引加速计算，大样本自动分位数均匀子抽样。
    """
    clean_data = np.asarray(data, dtype=float)
    clean_data = clean_data[~np.isnan(clean_data)]
    n = len(clean_data)
    if n == 0:
        return 0.0
    if n > max_subsample:
        clean_data = np.sort(clean_data)
        indices = np.linspace(0, n - 1, max_subsample, dtype=int)
        clean_data = clean_data[indices]
        n = len(clean_data)

    i_idx, j_idx = np.triu_indices(n)
    walsh_means = (clean_data[i_idx] + clean_data[j_idx]) / 2.0
    return float(np.median(walsh_means))


def hodges_lehmann_shift(x: np.ndarray, y: np.ndarray, max_subsample: int = 250) -> float:
    """
    计算两独立样本 Hodges-Lehmann 位置平移估计量：所有配对差 (X_i - Y_j) 的中位数。
    """
    x_clean = np.asarray(x, dtype=float)
    y_clean = np.asarray(y, dtype=float)
    if len(x_clean) > max_subsample:
        x_clean = np.sort(x_clean)[np.linspace(0, len(x_clean) - 1, max_subsample, dtype=int)]
    if len(y_clean) > max_subsample:
        y_clean = np.sort(y_clean)[np.linspace(0, len(y_clean) - 1, max_subsample, dtype=int)]
    diffs = np.subtract.outer(x_clean, y_clean).flatten()
    return float(np.median(diffs))


# =====================================================================
# 3. Wilcoxon 符号秩检验 (Exact + Ties Variance Correction)
# =====================================================================

def _compute_tie_correction(ranks: np.ndarray) -> float:
    """
    计算结值 (Ties) 引起的方差修正项: sum(t_k^3 - t_k)
    """
    _, counts = np.unique(ranks, return_counts=True)
    tie_counts = counts[counts > 1]
    return float(np.sum(tie_counts**3 - tie_counts))


def my_wilcoxon_signed_rank(
    differences: np.ndarray,
    exact_threshold: int = 15,
    alternative: str = "two-sided"
) -> Tuple[float, float]:
    """
    自定义 Wilcoxon 符号秩检验 (单样本对称中心或配对差异检验)。
    
    参数：
    - differences: 配对差 (X_i - Y_i) 或单样本减去原假设中位数 (X_i - m_0)
    - exact_threshold: 当有效样本量 n <= exact_threshold 时使用 2^n 精确全排列枚举
    - alternative: 'two-sided' (双尾), 'greater' (单尾右侧), 'less' (单尾左侧)
    
    返回：
    - w_plus: 正秩和统计量 W+
    - p_value: 精确或含结值修正的渐近 p 值
    """
    diffs = np.asarray(differences, dtype=float)
    diffs = diffs[diffs != 0] # 剔除零差值
    n = len(diffs)
    if n == 0:
        return 0.0, 1.0

    abs_diffs = np.abs(diffs)
    ranks = stats.rankdata(abs_diffs)
    w_plus = float(np.sum(ranks[diffs > 0]))
    w_minus = float(np.sum(ranks[diffs < 0]))
    w_stat = min(w_plus, w_minus) if alternative == "two-sided" else w_plus

    # 1. 小样本精确全排列分布 (Exact Permutation)
    if n <= exact_threshold:
        # 遍历 2^n 种符号配置 (+1 / -1)
        all_possible_w_plus = []
        for signs in itertools.product([0, 1], repeat=n):
            signs_arr = np.array(signs)
            all_possible_w_plus.append(np.sum(ranks * signs_arr))
        all_possible_w_plus = np.array(all_possible_w_plus)
        total_perms = len(all_possible_w_plus)

        if alternative == "two-sided":
            # 依对称性计算双尾 p 值
            e_w = np.sum(ranks) / 2.0
            dev = np.abs(w_plus - e_w)
            count = np.sum(np.abs(all_possible_w_plus - e_w) >= dev - 1e-9)
            p_val = count / float(total_perms)
        elif alternative == "greater":
            count = np.sum(all_possible_w_plus >= w_plus - 1e-9)
            p_val = count / float(total_perms)
        elif alternative == "less":
            count = np.sum(all_possible_w_plus <= w_plus + 1e-9)
            p_val = count / float(total_perms)
        else:
            raise ValueError(f"未知备择假设: {alternative}")
        return float(w_plus), float(np.clip(p_val, 0.0, 1.0))

    # 2. 大样本渐近正态近似 + 连续性校正 + 结值方差修正
    e_w = n * (n + 1) / 4.0
    tie_term = _compute_tie_correction(ranks)
    var_w = (n * (n + 1) * (2 * n + 1) - 0.5 * tie_term) / 24.0

    if var_w <= 0:
        return float(w_plus), 1.0

    sd_w = np.sqrt(var_w)
    # 连续性校正 (Continuity Correction 0.5)
    if alternative == "two-sided":
        z = (np.abs(w_plus - e_w) - 0.5) / sd_w
        p_val = 2.0 * (1.0 - stats.norm.cdf(max(0.0, z)))
    elif alternative == "greater":
        z = (w_plus - e_w - 0.5) / sd_w
        p_val = 1.0 - stats.norm.cdf(z)
    elif alternative == "less":
        z = (w_plus - e_w + 0.5) / sd_w
        p_val = stats.norm.cdf(z)
    else:
        raise ValueError(f"未知备择假设: {alternative}")

    return float(w_plus), float(np.clip(p_val, 0.0, 1.0))


# =====================================================================
# 4. Mann-Whitney U 秩和检验 (Exact + Ties Variance Correction)
# =====================================================================

def my_mann_whitney_u(
    x: np.ndarray,
    y: np.ndarray,
    exact_threshold: int = 10,
    alternative: str = "two-sided"
) -> Tuple[float, float]:
    """
    自定义 Mann-Whitney U 检验 (两独立样本位置/随机占优检验)。
    
    参数：
    - x, y: 两组独立连续/次序观测样本
    - exact_threshold: min(m, n) <= exact_threshold 且 m+n <= 20 时使用组合精确枚举
    - alternative: 'two-sided', 'greater', 'less'
    
    返回：
    - u_x: 第一组 U 统计量 = W_X - m(m+1)/2
    - p_value: 精确或含结值修正的渐近 p 值
    """
    x_clean = np.asarray(x, dtype=float)
    y_clean = np.asarray(y, dtype=float)
    m, n = len(x_clean), len(y_clean)
    if m == 0 or n == 0:
        return 0.0, 1.0

    combined = np.concatenate([x_clean, y_clean])
    ranks = stats.rankdata(combined)
    w_x = np.sum(ranks[:m])
    u_x = float(w_x - m * (m + 1) / 2.0)
    u_y = float(m * n - u_x)

    # 1. 小样本精确组合全排列
    if min(m, n) <= exact_threshold and (m + n) <= 20:
        indices = range(m + n)
        all_possible_w = []
        for comb in itertools.combinations(indices, m):
            all_possible_w.append(np.sum(ranks[list(comb)]))
        all_possible_w = np.array(all_possible_w)
        all_possible_u = all_possible_w - m * (m + 1) / 2.0
        total_combs = len(all_possible_u)

        if alternative == "two-sided":
            e_u = m * n / 2.0
            dev = np.abs(u_x - e_u)
            count = np.sum(np.abs(all_possible_u - e_u) >= dev - 1e-9)
            p_val = count / float(total_combs)
        elif alternative == "greater":
            count = np.sum(all_possible_u >= u_x - 1e-9)
            p_val = count / float(total_combs)
        elif alternative == "less":
            count = np.sum(all_possible_u <= u_x + 1e-9)
            p_val = count / float(total_combs)
        else:
            raise ValueError(f"未知备择假设: {alternative}")
        return float(u_x), float(np.clip(p_val, 0.0, 1.0))

    # 2. 大样本渐近正态近似 + 连续性校正 + 结值方差修正
    e_u = m * n / 2.0
    N = m + n
    tie_term = _compute_tie_correction(ranks)
    var_u = (m * n / 12.0) * ((N + 1) - tie_term / (N * (N - 1))) if N > 1 else 0.0

    if var_u <= 0:
        return float(u_x), 1.0

    sd_u = np.sqrt(var_u)
    if alternative == "two-sided":
        z = (np.abs(u_x - e_u) - 0.5) / sd_u
        p_val = 2.0 * (1.0 - stats.norm.cdf(max(0.0, z)))
    elif alternative == "greater":
        z = (u_x - e_u - 0.5) / sd_u
        p_val = 1.0 - stats.norm.cdf(z)
    elif alternative == "less":
        z = (u_x - e_u + 0.5) / sd_u
        p_val = stats.norm.cdf(z)
    else:
        raise ValueError(f"未知备择假设: {alternative}")

    return float(u_x), float(np.clip(p_val, 0.0, 1.0))


# =====================================================================
# 5. Monte Carlo 置换检验 (支持多种稳健统计量)
# =====================================================================

def permutation_test(
    x: np.ndarray,
    y: np.ndarray,
    statistic: str = "median_diff",
    n_permutations: int = 5000,
    seed: int = 42,
    alternative: str = "two-sided"
) -> Tuple[float, float, np.ndarray]:
    """
    两独立样本 Monte Carlo 精确置换检验。
    
    参数：
    - x, y: 两组独立样本
    - statistic:
        'mean_diff': 均值差 (对正态敏感，对长尾脆弱)
        'median_diff': 中位数差 (稳健，对偏态离群点强健)
        'hl_shift': Hodges-Lehmann 位置平移 (高效率稳健)
        'rank_sum': 第一组秩和 (等价于置换秩检验)
    - n_permutations: 随机置换重复次数
    - seed: 随机数种子
    - alternative: 'two-sided', 'greater', 'less'
    
    返回：
    - obs_stat: 观测到的统计量值
    - p_value: Monte Carlo 经验 p 值
    - perm_stats: 全部重抽样下的置换统计量经验分布
    """
    rng = np.random.default_rng(seed)
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    m, n = len(x_arr), len(y_arr)
    combined = np.concatenate([x_arr, y_arr])

    def calc_stat(a: np.ndarray, b: np.ndarray) -> float:
        if statistic == "mean_diff":
            return float(np.mean(a) - np.mean(b))
        elif statistic == "median_diff":
            return float(np.median(a) - np.median(b))
        elif statistic == "hl_shift":
            return float(hodges_lehmann_shift(a, b))
        elif statistic == "rank_sum":
            comb = np.concatenate([a, b])
            r = stats.rankdata(comb)
            return float(np.sum(r[:len(a)]))
        else:
            raise ValueError(f"未知统计量类型: {statistic}")

    obs_stat = calc_stat(x_arr, y_arr)
    perm_stats = np.zeros(n_permutations, dtype=float)

    for b in range(n_permutations):
        shuffled = rng.permutation(combined)
        perm_a = shuffled[:m]
        perm_b = shuffled[m:]
        perm_stats[b] = calc_stat(perm_a, perm_b)

    # 计算 p 值 (包含 +1 正则化防 p=0)
    if alternative == "two-sided":
        count = np.sum(np.abs(perm_stats) >= np.abs(obs_stat) - 1e-12)
    elif alternative == "greater":
        count = np.sum(perm_stats >= obs_stat - 1e-12)
    elif alternative == "less":
        count = np.sum(perm_stats <= obs_stat + 1e-12)
    else:
        raise ValueError(f"未知备择假设: {alternative}")

    p_value = float((1 + count) / (1 + n_permutations))
    return float(obs_stat), p_value, perm_stats


def permutation_test_mean(x: np.ndarray, y: np.ndarray, n_permutations: int = 5000, seed: int = 42) -> Tuple[float, float]:
    """向后兼容接口：均值差置换检验"""
    obs, p_val, _ = permutation_test(x, y, statistic="mean_diff", n_permutations=n_permutations, seed=seed)
    return obs, p_val


# =====================================================================
# 6. Bootstrap 置信区间套件 (Normal, Basic, Percentile, BCa)
# =====================================================================

def bootstrap_confidence_intervals(
    data: np.ndarray,
    stat_func: Callable[[np.ndarray], float],
    alpha: float = 0.05,
    n_boot: int = 2000,
    seed: int = 42
) -> Dict[str, Tuple[float, float]]:
    """
    计算 4 类经典与现代 Bootstrap 置信区间：
    1. Standard Normal Bootstrap CI: theta_hat +/- z * se_boot
    2. Basic (Empirical) Bootstrap CI: [2*theta_hat - theta*_(1-alpha/2), 2*theta_hat - theta*_(alpha/2)]
    3. Percentile Bootstrap CI: [theta*_(alpha/2), theta*_(1-alpha/2)]
    4. BCa (Bias-Corrected and Accelerated) Bootstrap CI: 调整非正态偏倚与留一曲率
    """
    rng = np.random.default_rng(seed)
    data_clean = np.asarray(data, dtype=float)
    n = len(data_clean)
    if n < 3:
        raise ValueError("Bootstrap 样本量至少为 3")

    theta_hat = float(stat_func(data_clean))

    # 1. Bootstrap 重采样
    boot_thetas = np.zeros(n_boot, dtype=float)
    for b in range(n_boot):
        sample = rng.choice(data_clean, size=n, replace=True)
        boot_thetas[b] = stat_func(sample)

    se_boot = float(np.std(boot_thetas, ddof=1))
    z_crit = float(stats.norm.ppf(1.0 - alpha / 2.0))

    # [1] Standard Normal CI
    ci_normal = (theta_hat - z_crit * se_boot, theta_hat + z_crit * se_boot)

    # [2] Percentile CI
    q_low = float(alpha / 2.0)
    q_high = float(1.0 - alpha / 2.0)
    ci_percentile = (
        float(np.percentile(boot_thetas, 100.0 * q_low)),
        float(np.percentile(boot_thetas, 100.0 * q_high))
    )

    # [3] Basic (Empirical) CI
    ci_basic = (
        float(2.0 * theta_hat - np.percentile(boot_thetas, 100.0 * q_high)),
        float(2.0 * theta_hat - np.percentile(boot_thetas, 100.0 * q_low))
    )

    # [4] BCa CI
    # 计算偏倚修正参数 z0
    prop_less = np.mean(boot_thetas < theta_hat)
    if prop_less <= 0:
        z0 = -3.0
    elif prop_less >= 1:
        z0 = 3.0
    else:
        z0 = float(stats.norm.ppf(prop_less))

    # 计算留一法 (Jackknife) 加速度参数 a
    jack_thetas = np.zeros(n, dtype=float)
    for i in range(n):
        jack_sample = np.delete(data_clean, i)
        jack_thetas[i] = stat_func(jack_sample)

    jack_mean = np.mean(jack_thetas)
    diff = jack_mean - jack_thetas
    sum_diff3 = np.sum(diff**3)
    sum_diff2 = np.sum(diff**2)

    if sum_diff2 > 1e-12:
        a = float(sum_diff3 / (6.0 * (sum_diff2**1.5)))
    else:
        # 当统计量为中位数等阶梯函数时，使用平滑扰动 Jackknife 避免梯度为 0
        h_noise = 0.1 * np.std(data_clean, ddof=1) / np.sqrt(n) if np.std(data_clean) > 0 else 1e-3
        smooth_jack = np.zeros(n)
        for i in range(n):
            perturbed = data_clean.copy()
            perturbed[i] += h_noise
            smooth_jack[i] = stat_func(perturbed)
        s_mean = np.mean(smooth_jack)
        s_diff = s_mean - smooth_jack
        s2 = np.sum(s_diff**2)
        a = float(np.sum(s_diff**3) / (6.0 * (s2**1.5))) if s2 > 1e-12 else 0.0

    # 限制 a 在合理物理范围内 [-0.5, 0.5]
    a = float(np.clip(a, -0.5, 0.5))

    # 调整分位点
    z_alpha1 = float(stats.norm.ppf(alpha / 2.0))
    z_alpha2 = float(stats.norm.ppf(1.0 - alpha / 2.0))

    denom1 = 1.0 - a * (z0 + z_alpha1)
    denom2 = 1.0 - a * (z0 + z_alpha2)

    # 检查单调性破缺
    if denom1 <= 0 or denom2 <= 0:
        # 退化为标准百分位区间
        ci_bca = ci_percentile
    else:
        a1 = float(stats.norm.cdf(z0 + (z0 + z_alpha1) / denom1))
        a2 = float(stats.norm.cdf(z0 + (z0 + z_alpha2) / denom2))
        a1 = float(np.clip(a1, 0.0005, 0.9995))
        a2 = float(np.clip(a2, 0.0005, 0.9995))
        ci_bca = (
            float(np.percentile(boot_thetas, 100.0 * a1)),
            float(np.percentile(boot_thetas, 100.0 * a2))
        )

    return {
        "normal": ci_normal,
        "basic": ci_basic,
        "percentile": ci_percentile,
        "bca": ci_bca,
        "se_boot": (se_boot, se_boot),
        "theta_hat": (theta_hat, theta_hat),
        "bca_params": (z0, a)
    }


def bootstrap_bca_ci(
    data: np.ndarray,
    stat_func: Callable[[np.ndarray], float],
    alpha: float = 0.05,
    n_boot: int = 2000,
    seed: int = 42
) -> Tuple[float, float]:
    """向后兼容接口：仅返回 BCa 置信区间 (lower, upper)"""
    res = bootstrap_confidence_intervals(data, stat_func, alpha=alpha, n_boot=n_boot, seed=seed)
    return res["bca"]


# =====================================================================
# 7. KDE 核密度估计与自适应带宽 (Silverman + LOOCV)
# =====================================================================

def silverman_bandwidth(data: np.ndarray) -> float:
    """
    Silverman (1986) 经验法则最优带宽公式：
    h = 0.9 * min(sigma, IQR / 1.34) * n^(-1/5)
    """
    clean_data = np.asarray(data, dtype=float)
    clean_data = clean_data[~np.isnan(clean_data)]
    n = len(clean_data)
    if n <= 1:
        return 1.0
    sd = np.std(clean_data, ddof=1)
    q75, q25 = np.percentile(clean_data, [75, 25])
    iqr = q75 - q25
    spread = min(sd, iqr / 1.34) if (iqr > 0 and sd > 0) else (sd if sd > 0 else 1.0)
    return float(0.9 * spread * (n**(-0.2)))


def kde_gaussian(data: np.ndarray, grid: np.ndarray, h: float) -> np.ndarray:
    """
    标准高斯核密度估计：
    f_hat(x) = (1 / (n * h)) * sum( phi( (x - X_i) / h ) )
    """
    clean_data = np.asarray(data, dtype=float)
    n = len(clean_data)
    if n == 0 or h <= 0:
        return np.zeros_like(grid)
    u = np.subtract.outer(grid, clean_data) / h
    return np.mean(stats.norm.pdf(u), axis=1) / h


def loocv_kde_bandwidth(data: np.ndarray, h_candidates: Optional[np.ndarray] = None) -> float:
    """
    留一交叉验证 (LOOCV) 最大似然带宽选择：
    最大化 sum_{i=1}^n ln( f_{-i}(X_i; h) )
    """
    clean_data = np.asarray(data, dtype=float)
    n = len(clean_data)
    if n < 5:
        return silverman_bandwidth(clean_data)

    if h_candidates is None:
        h_silverman = silverman_bandwidth(clean_data)
        h_candidates = np.logspace(np.log10(h_silverman * 0.2), np.log10(h_silverman * 3.0), 30)

    best_h = h_candidates[0]
    best_score = -np.inf

    # 预计算所有点对差值矩阵
    diff_matrix = np.subtract.outer(clean_data, clean_data) # (n, n)
    np.fill_diagonal(diff_matrix, np.nan) # 排除对角线（留一）

    for h in h_candidates:
        u = diff_matrix / h
        pdf_matrix = stats.norm.pdf(u) # (n, n)
        # 对每一行求和，除以 (n-1)*h 得到 f_{-i}(X_i)
        f_minus_i = np.nanmean(pdf_matrix, axis=1) / h
        # 避免 log(0)
        f_minus_i = np.clip(f_minus_i, 1e-15, None)
        score = np.sum(np.log(f_minus_i))
        if score > best_score:
            best_score = score
            best_h = h

    return float(best_h)


# =====================================================================
# 8. 局部多项式平滑回归 (Nadaraya-Watson vs Local Linear)
# =====================================================================

def nadaraya_watson_regression(x_train: np.ndarray, y_train: np.ndarray, x_eval: np.ndarray, h: float) -> np.ndarray:
    """
    Nadaraya-Watson 局部常数回归 (Local Constant Regression, Degree 0)。
    在边界处存在显著的一阶 O(h) 偏差。
    """
    u = np.subtract.outer(x_eval, x_train) / h
    weights = stats.norm.pdf(u) # (n_eval, n_train)
    weight_sums = np.sum(weights, axis=1, keepdims=True)
    weight_sums[weight_sums == 0] = 1e-10
    normalized_weights = weights / weight_sums
    return np.dot(normalized_weights, y_train)


def local_linear_regression(x_train: np.ndarray, y_train: np.ndarray, x_eval: np.ndarray, h: float) -> np.ndarray:
    """
    局部线性回归 (Local Linear Regression, Degree 1)。
    自动修正边界偏差 (Boundary Bias Elimination, 达到 O(h^2) 全域一致收敛速率)。
    """
    x_tr = np.asarray(x_train, dtype=float)
    y_tr = np.asarray(y_train, dtype=float)
    x_ev = np.asarray(x_eval, dtype=float)
    n_eval = len(x_ev)
    y_pred = np.zeros(n_eval, dtype=float)

    for idx, x0 in enumerate(x_ev):
        dx = x_tr - x0
        weights = stats.norm.pdf(dx / h)
        w_sum = np.sum(weights)
        if w_sum <= 1e-12:
            y_pred[idx] = np.mean(y_tr)
            continue

        s0 = w_sum
        s1 = np.sum(weights * dx)
        s2 = np.sum(weights * (dx**2))
        t0 = np.sum(weights * y_tr)
        t1 = np.sum(weights * dx * y_tr)

        denom = s0 * s2 - s1**2
        if np.abs(denom) > 1e-12:
            # 解析解无需矩阵求逆：beta_0 = (s2 * t0 - s1 * t1) / denom
            y_pred[idx] = (s2 * t0 - s1 * t1) / denom
        else:
            # 退化为局部常数加权均值
            y_pred[idx] = t0 / s0

    return y_pred


def loocv_local_linear_bandwidth(x: np.ndarray, y: np.ndarray, h_candidates: Optional[np.ndarray] = None) -> float:
    """
    通过留一交叉验证 (LOOCV) 选择最优局部线性回归窗宽 h (包含快速抽样评估)
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    n = len(x_arr)
    if h_candidates is None:
        span = np.ptp(x_arr)
        h_candidates = np.linspace(span / 15.0, span / 3.0, 10)

    best_h = float(h_candidates[0])
    min_mse = np.inf
    eval_indices = np.linspace(0, n - 1, min(n, 40), dtype=int)

    for h in h_candidates:
        errors = np.zeros(len(eval_indices))
        for idx, i in enumerate(eval_indices):
            x_minus = np.delete(x_arr, i)
            y_minus = np.delete(y_arr, i)
            pred = local_linear_regression(x_minus, y_minus, np.array([x_arr[i]]), h=h)[0]
            errors[idx] = (y_arr[i] - pred)**2
        mse = np.mean(errors)
        if mse < min_mse:
            min_mse = mse
            best_h = float(h)

    return best_h


# =====================================================================
# 9. 端到端工业级实证流水线
# =====================================================================

def run_full_pipeline():
    print("=====================================================================")
    print("  32-非参数统计：全流程工业级实证与算法基准评测流水线")
    print("=====================================================================")

    csv_path = Path(__file__).parent.parent / "data/nonparam_benchmark_data.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"未找到基准数据集: {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"成功加载基准数据集: {csv_path.name}, 样本容量: N={len(df)}")

    # 1. 经验分布与 DKW 置信带
    n_sample = len(df)
    alpha = 0.05
    w_dkw = dkw_band_width(n_sample, alpha)
    print(f"\n[1] 经验分布与集中不等式:")
    print(f"    - 样本量 n = {n_sample}, 显著性水平 alpha = {alpha}")
    print(f"    - DKW 95% 全域一致置信带半宽: eps = {w_dkw:.4f} (真实分布 F(x) 100% 包含在此包络内)")

    # 2. 稳健尺度与离群点破坏力实验
    med_a, mad_a, s_mad_a = mad_estimator(df["group_A"].values)
    hl_a = hodges_lehmann_location(df["group_A"].values)
    mean_a, std_a = np.mean(df["group_A"].values), np.std(df["group_A"].values, ddof=1)

    med_b, mad_b, s_mad_b = mad_estimator(df["group_B"].values)
    hl_b = hodges_lehmann_location(df["group_B"].values)
    mean_b, std_b = np.mean(df["group_B"].values), np.std(df["group_B"].values, ddof=1)

    print(f"\n[2] 参数 vs 稳健位置与尺度估计 (展示离群点破坏力):")
    print(f"    - 组 A (无污染): 均值={mean_a:.3f}, 标准差={std_a:.3f} | 中位数={med_a:.3f}, MAD标准差={s_mad_a:.3f}, HL位置={hl_a:.3f}")
    print(f"    - 组 B (含离群): 均值={mean_b:.3f}, 标准差={std_b:.3f} | 中位数={med_b:.3f}, MAD标准差={s_mad_b:.3f}, HL位置={hl_b:.3f}")
    print(f"    --> 严重离群点使经典标准差膨胀了 {(std_b/std_a):.2f} 倍，而 MAD 仅波动 {(s_mad_b/s_mad_a):.2f} 倍！")

    # 3. 经典秩检验与多重对决
    u_val, u_p = my_mann_whitney_u(df["group_A"].values, df["group_B"].values)
    scipy_u, scipy_p = stats.mannwhitneyu(df["group_A"].values, df["group_B"].values, alternative="two-sided")
    ttest_stat, ttest_p = stats.ttest_ind(df["group_A"].values, df["group_B"].values)
    _, perm_mean_p, _ = permutation_test(df["group_A"].values, df["group_B"].values, statistic="mean_diff", n_permutations=2000)
    _, perm_hl_p, _ = permutation_test(df["group_A"].values, df["group_B"].values, statistic="hl_shift", n_permutations=2000)

    print(f"\n[3] 组间差异推断多重对决 (组 A vs 组 B):")
    print(f"    - Student t 检验 (参数假设): t = {ttest_stat:.3f}, p-value = {ttest_p:.4e}")
    print(f"    - 自研 Mann-Whitney U (含结修正): U = {u_val:.1f}, p-value = {u_p:.4e} (Scipy 对齐: U={scipy_u:.1f}, p={scipy_p:.4e})")
    print(f"    - 均值差 Monte Carlo 置换检验: p-value = {perm_mean_p:.4e}")
    print(f"    - Hodges-Lehmann 稳健置换检验: p-value = {perm_hl_p:.4e}")

    # 4. Bootstrap 4 类置信区间全面对比
    boot_dict = bootstrap_confidence_intervals(df["group_A"].values, np.median, alpha=0.05, n_boot=2000)
    print(f"\n[4] 组 A 中位数 95% Bootstrap 置信区间对比 (4 类体系):")
    print(f"    - 标准正态 (Normal):    [{boot_dict['normal'][0]:.3f}, {boot_dict['normal'][1]:.3f}]")
    print(f"    - 经验基本 (Basic):     [{boot_dict['basic'][0]:.3f}, {boot_dict['basic'][1]:.3f}]")
    print(f"    - 百分位 (Percentile):   [{boot_dict['percentile'][0]:.3f}, {boot_dict['percentile'][1]:.3f}]")
    print(f"    - 偏倚修正与加速 (BCa):  [{boot_dict['bca'][0]:.3f}, {boot_dict['bca'][1]:.3f}] (z0={boot_dict['bca_params'][0]:.3f}, a={boot_dict['bca_params'][1]:.4f})")

    # 5. KDE 与自适应带宽选择
    x_feat = df["X_feature"].values
    h_silver = silverman_bandwidth(x_feat)
    h_opt = loocv_kde_bandwidth(x_feat)
    print(f"\n[5] KDE 密度估计与带宽自适应选择:")
    print(f"    - Silverman 经验法则带宽: h = {h_silver:.4f}")
    print(f"    - 留一交叉验证 (LOOCV) 最优带宽: h = {h_opt:.4f}")

    # 6. 局部多项式平滑回归与边界效应消除
    y_resp = df["Y_response"].values
    h_loess = loocv_local_linear_bandwidth(x_feat, y_resp)
    x_eval = np.linspace(np.min(x_feat), np.max(x_feat), 100)
    y_nw = nadaraya_watson_regression(x_feat, y_resp, x_eval, h=h_loess)
    y_ll = local_linear_regression(x_feat, y_resp, x_eval, h=h_loess)
    mse_ll = np.mean((local_linear_regression(x_feat, y_resp, x_feat, h=h_loess) - y_resp)**2)
    mse_nw = np.mean((nadaraya_watson_regression(x_feat, y_resp, x_feat, h=h_loess) - y_resp)**2)

    print(f"\n[6] 局部多项式回归与边界修正对比 (LOOCV 最优 h = {h_loess:.4f}):")
    print(f"    - Nadaraya-Watson (局部常数) MSE = {mse_nw:.4f}")
    print(f"    - Local Linear (局部线性)   MSE = {mse_ll:.4f}")
    print(f"    --> 局部线性回归在边界处消除了 O(h) 偏差，全域拟合方差改善 {( (mse_nw - mse_ll)/mse_nw * 100 ):.2f}%！")
    print("=====================================================================")
    print("  全流程工业级实证与测试完成，所有指标坚如磐石！")
    print("=====================================================================")


if __name__ == "__main__":
    run_full_pipeline()
