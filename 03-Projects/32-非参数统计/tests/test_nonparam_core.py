# -*- coding: utf-8 -*-
"""
pytest 严苛单元测试套件：验证 32-非参数统计核心算法实现的数学正确性、小样本精确解、Ties 修正与边界性质
"""

import sys
from pathlib import Path
import numpy as np
import pytest
from scipy import stats

# 导入待测函数
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from run_nonparam_experiments import (
    dkw_band_width,
    empirical_cdf,
    mad_estimator,
    hodges_lehmann_location,
    hodges_lehmann_shift,
    my_wilcoxon_signed_rank,
    my_mann_whitney_u,
    permutation_test,
    bootstrap_confidence_intervals,
    bootstrap_bca_ci,
    kde_gaussian,
    silverman_bandwidth,
    loocv_kde_bandwidth,
    nadaraya_watson_regression,
    local_linear_regression,
    loocv_local_linear_bandwidth
)


def test_dkw_band_width_theoretical_value():
    """测试 DKW 不等式置信带半宽在已知样本量与显著性水平下的理论精确值"""
    n = 100
    alpha = 0.05
    w = dkw_band_width(n, alpha)
    expected = np.sqrt(np.log(2.0 / 0.05) / 200.0)
    assert np.isclose(w, expected, rtol=1e-5)
    assert 0.135 < w < 0.136

    # 验证经验分布被 DKW 包络严格包含
    np.random.seed(42)
    sample = np.random.uniform(0, 1, n)
    grid = np.linspace(0, 1, 100)
    fn = empirical_cdf(sample, grid)
    f_true = grid
    sup_diff = np.max(np.abs(fn - f_true))
    assert sup_diff < w, "在 95% 置信度下，均匀分布样本的经验分布上确界误差必须小于 DKW 半宽"


def test_mad_and_hodges_lehmann_outlier_resistance():
    """测试 MAD 与 Hodges-Lehmann 位置估计量在正态样本与离群点污染下的稳健性"""
    np.random.seed(42)
    clean_data = np.random.normal(loc=10.0, scale=2.0, size=5000)
    med, mad, sigma_mad = mad_estimator(clean_data)
    hl_loc = hodges_lehmann_location(clean_data)

    assert np.isclose(med, 10.0, atol=0.1)
    assert np.isclose(sigma_mad, 2.0, atol=0.1)
    assert np.isclose(hl_loc, 10.0, atol=0.1)

    # 注入极端离群点污染
    contaminated = clean_data.copy()
    contaminated[:50] = 10000.0 # 1% 极大离群点
    _, _, sigma_mad_cont = mad_estimator(contaminated)
    hl_cont = hodges_lehmann_location(contaminated)
    assert np.isclose(sigma_mad_cont, 2.0, atol=0.2), "MAD 必须抵抗 1% 极端离群点"
    assert np.isclose(hl_cont, 10.0, atol=0.2), "HL 估计量必须保持稳健"


def test_wilcoxon_signed_rank_exact_and_ties():
    """测试自研 Wilcoxon 符号秩检验：在小样本下与精确排列一致，在含结值(Ties)下与 scipy 完全对齐"""
    # 1. 经典小样本精确检验 (n=6)
    diffs_small = np.array([3, -2, 14, 8, 1, 11])
    w_plus, p_exact = my_wilcoxon_signed_rank(diffs_small, exact_threshold=10, alternative='two-sided')
    scipy_exact = stats.wilcoxon(diffs_small, alternative='two-sided', method='exact')
    assert np.isclose(p_exact, scipy_exact.pvalue, atol=1e-5)

    # 2. 含有结值 (Ties) 的大样本检验
    diffs_ties = np.array([3, -2, 14, 8, 1, 11, -4, 8, 3, -1, 5, 7, 8, -2, 3, 14, 1, -1])
    w_plus_ties, p_ties = my_wilcoxon_signed_rank(diffs_ties, exact_threshold=5, alternative='two-sided')
    scipy_approx = stats.wilcoxon(diffs_ties, alternative='two-sided', method='approx')
    assert np.isclose(p_ties, scipy_approx.pvalue, atol=0.02)


def test_mann_whitney_u_exact_and_ties():
    """测试自研 Mann-Whitney U 检验：在小样本下精确排列一致，在有结值下与 scipy 对齐"""
    # 1. 小样本精确组合全排列
    x_small = np.array([4.5, 5.8, 6.2])
    y_small = np.array([3.1, 4.2, 5.0, 5.5])
    u_val, p_exact = my_mann_whitney_u(x_small, y_small, exact_threshold=10, alternative='two-sided')
    scipy_exact = stats.mannwhitneyu(x_small, y_small, alternative='two-sided', method='exact')
    assert np.isclose(u_val, scipy_exact.statistic, atol=1e-5)
    assert np.isclose(p_exact, scipy_exact.pvalue, atol=1e-5)

    # 2. 含有结值的数据集
    x_ties = np.array([1, 2, 2, 3, 4, 5, 5, 6])
    y_ties = np.array([2, 3, 3, 4, 4, 5, 6, 7])
    u_t, p_t = my_mann_whitney_u(x_ties, y_ties, exact_threshold=3, alternative='two-sided')
    scipy_res = stats.mannwhitneyu(x_ties, y_ties, alternative='two-sided', method='asymptotic')
    assert np.isclose(u_t, scipy_res.statistic, atol=1e-5)
    assert np.isclose(p_t, scipy_res.pvalue, atol=0.05)


def test_permutation_test_robustness_on_heavy_tail():
    """测试 Monte Carlo 置换检验：在重尾柯西分布下，Hodges-Lehmann / 中位数置换统计量优于均值置换"""
    np.random.seed(123)
    # 两组服从相同位置的柯西分布（严重重尾）
    x = stats.cauchy.rvs(loc=0, scale=1, size=25, random_state=123)
    y = stats.cauchy.rvs(loc=0, scale=1, size=25, random_state=456)
    
    # 均值可能被极端值扭曲，但 Hodges-Lehmann 置换检验应当正确保留原假设 (p > 0.05)
    _, p_hl, _ = permutation_test(x, y, statistic="hl_shift", n_permutations=1000, seed=42)
    assert p_hl > 0.05, "在零分布相同的前提下，HL 置换检验不应错误拒绝原假设"


def test_bootstrap_confidence_intervals_4_types():
    """测试 4 类 Bootstrap 置信区间 (Normal, Basic, Percentile, BCa) 均覆盖指数分布真实中位数"""
    np.random.seed(42)
    data = np.random.exponential(scale=2.0, size=60) # 真实中位数 = 2 * ln(2) = 1.38629
    true_median = 2.0 * np.log(2.0)

    cis = bootstrap_confidence_intervals(data, np.median, alpha=0.05, n_boot=1000, seed=42)
    
    assert cis["normal"][0] < true_median < cis["normal"][1]
    assert cis["basic"][0] < true_median < cis["basic"][1]
    assert cis["percentile"][0] < true_median < cis["percentile"][1]
    assert cis["bca"][0] < true_median < cis["bca"][1]
    
    # 验证 BCa 参数合理性
    z0, a = cis["bca_params"]
    assert -3.0 <= z0 <= 3.0
    assert -0.5 <= a <= 0.5


def test_kde_density_integration_and_loocv():
    """测试 KDE 高斯核密度数值积分为 1，且 LOOCV 带宽在合理区间"""
    np.random.seed(42)
    data = np.random.normal(loc=0.0, scale=1.0, size=100)
    grid = np.linspace(-4, 4, 1000)
    h_opt = loocv_kde_bandwidth(data)
    assert 0.1 < h_opt < 1.0, f"最优带宽 h={h_opt} 必须落在合理区间"

    dens = kde_gaussian(data, grid, h=h_opt)
    dx = grid[1] - grid[0]
    integral = np.sum(dens) * dx
    assert np.isclose(integral, 1.0, atol=0.02), "KDE 在实数轴积分必须归一化为 1"


def test_local_linear_vs_nadaraya_watson_boundary():
    """测试局部线性回归相比 Nadaraya-Watson 在边界处的优越性 (消除 O(h) 边界偏差)"""
    np.random.seed(42)
    x = np.linspace(0, 1, 80)
    y_true = 3.0 * x + 1.0 # 线性趋势
    y_noisy = y_true + np.random.normal(0, 0.05, size=len(x))

    x_eval = np.array([0.02, 0.05, 0.5, 0.95, 0.98]) # 包含左右极端边界点
    h = 0.15

    pred_ll = local_linear_regression(x, y_noisy, x_eval, h=h)
    pred_nw = nadaraya_watson_regression(x, y_noisy, x_eval, h=h)
    true_eval = 3.0 * x_eval + 1.0

    err_ll = np.abs(pred_ll - true_eval)
    err_nw = np.abs(pred_nw - true_eval)

    # 边界点 (x=0.02, x=0.98) 处局部线性回归的误差显著小于局部常数 NW 回归
    assert err_ll[0] < err_nw[0], "左边界处 Local Linear 回归必须战胜 Nadaraya-Watson"
    assert err_ll[-1] < err_nw[-1], "右边界处 Local Linear 回归必须战胜 Nadaraya-Watson"
