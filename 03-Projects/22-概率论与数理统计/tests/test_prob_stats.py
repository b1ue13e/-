"""
22-概率论与数理统计 全量严苛自动化单元测试套件
验证贝叶斯推断、极大似然求解、BCa Bootstrap、ANOVA 方差分解、FDR 多重校正
以及真实世界厚尾偏态数据集 (financial_loss_or_delay_data.csv) 端到端推断流水线。
"""

import os
import sys
import numpy as np
import pandas as pd
import pytest
import scipy.stats as stats

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.stats_solver import (
    bayes_posterior_calc,
    bayes_discrete_table_update,
    MLEFitter,
    bootstrap_percentile_ci,
    bootstrap_bca_ci,
    one_way_anova,
    benjamini_hochberg_fdr,
    linear_regression_fit,
)
import scripts.starter_code as starter_code


def test_starter_code_contracts():
    """验证学习者 Starter Code 骨架契约与全量完成度接口测试"""
    # 1. 三门问题接口契约
    stay_win, switch_win = starter_code.monte_carlo_monty_hall(n_sim=50_000)
    assert abs(stay_win - 1.0 / 3.0) < 0.02
    assert abs(switch_win - 2.0 / 3.0) < 0.02

    # 2. 二元信道接口契约
    p_y1, post_x1 = starter_code.simulate_binary_symmetric_channel(n_sim=100_000)
    assert 0 < p_y1 < 1.0
    assert 0 < post_x1 < 1.0

    # 3. CLT 模拟契约
    clt_res = starter_code.central_limit_theorem_simulation(sample_sizes=[2, 30])
    assert abs(clt_res[30]["skewness"]) < abs(clt_res[2]["skewness"]) # 偏度向 0 衰减

    # 4. Fisher CRLB 契约
    crlb_val = starter_code.calculate_fishers_exact_crlb("normal_mean", theta=2.0, n=100)
    assert abs(crlb_val - 0.01) < 1e-6



def test_bayes_inference():
    """测试二元贝叶斯与多假设离散更新"""
    # 1. 罕见病基率谬误
    prior = 0.001
    sens = 0.99
    fp = 0.01
    post = bayes_posterior_calc(prior, sens, fp)
    theory_post = (0.001 * 0.99) / (0.001 * 0.99 + 0.999 * 0.01)
    assert abs(post - theory_post) < 1e-6
    assert abs(post - 0.0901639) < 1e-4

    # 2. 多假设更新
    priors = np.array([0.5, 0.3, 0.2])
    likelihoods = np.array([0.1, 0.8, 0.4])
    post_table = bayes_discrete_table_update(priors, likelihoods)
    expected_unnorm = priors * likelihoods
    expected_post = expected_unnorm / np.sum(expected_unnorm)
    assert np.allclose(post_table, expected_post, atol=1e-6)
    assert abs(np.sum(post_table) - 1.0) < 1e-6


def test_mle_fitter_normal_gamma_lognormal():
    """测试参数估计器在正态、对数正态与 Gamma 分布上的 MLE 与信息矩阵"""
    np.random.seed(42)
    n = 2000
    
    # 1. 正态总体
    true_mu, true_sigma = 5.0, 2.0
    norm_data = np.random.normal(true_mu, true_sigma, size=n)
    res_norm = MLEFitter.fit_normal(norm_data)
    assert abs(res_norm["params"]["mu"] - true_mu) < 0.1
    assert abs(res_norm["params"]["sigma"] - true_sigma) < 0.1
    assert res_norm["se"]["mu"] > 0
    assert res_norm["aic"] > 0

    # 2. Gamma 总体
    true_alpha, true_beta = 4.0, 2.0 # shape=4, rate=2, scale=0.5
    gamma_data = np.random.gamma(shape=true_alpha, scale=1.0 / true_beta, size=n)
    res_gamma = MLEFitter.fit_gamma(gamma_data)
    assert abs(res_gamma["params"]["alpha"] - true_alpha) < 0.3
    assert abs(res_gamma["params"]["beta"] - true_beta) < 0.3
    assert res_gamma["se"]["alpha"] > 0

    # 3. 对数正态总体
    lognorm_data = np.random.lognormal(mean=1.5, sigma=0.5, size=n)
    res_lognorm = MLEFitter.fit_lognormal(lognorm_data)
    assert abs(res_lognorm["params"]["mu_log"] - 1.5) < 0.05
    assert abs(res_lognorm["params"]["sigma_log"] - 0.5) < 0.05


def test_bca_bootstrap_ci_coverage():
    """测试非参数 BCa Bootstrap 与 Percentile Bootstrap 在偏态统计量上的置信区间"""
    np.random.seed(42)
    n = 150
    # 偏态数据 (指数分布 Exp(1))
    exp_data = np.random.exponential(scale=1.0, size=n)
    true_median = np.log(2.0) # ~0.6931
    
    ci_low_p, ci_high_p, se_p = bootstrap_percentile_ci(exp_data, stat_func=np.median, n_boot=1000)
    ci_low_bca, ci_high_bca, se_bca = bootstrap_bca_ci(exp_data, stat_func=np.median, n_boot=1000)
    
    assert ci_low_p < true_median < ci_high_p
    assert ci_low_bca < true_median < ci_high_bca
    assert ci_low_bca < ci_high_bca
    assert se_bca > 0


def test_one_way_anova_and_fdr():
    """测试单因素 ANOVA 平方和守恒性与 Benjamini-Hochberg FDR 校正"""
    np.random.seed(42)
    g1 = np.random.normal(10.0, 1.5, size=30)
    g2 = np.random.normal(12.0, 1.5, size=35)
    g3 = np.random.normal(15.0, 1.5, size=40)
    
    anova_res = one_way_anova([g1, g2, g3])
    # 检验平方和守恒: SST = SSB + SSW
    assert abs(anova_res["SST"] - (anova_res["SSB"] + anova_res["SSW"])) < 1e-5
    assert anova_res["p_val"] < 1e-4 # 三组均值有显著差异
    assert 0 < anova_res["eta_squared"] < 1.0

    # 测试 FDR 校正
    p_vals = np.array([0.001, 0.008, 0.035, 0.045, 0.12, 0.45, 0.89])
    rejected, adj_p = benjamini_hochberg_fdr(p_vals, alpha=0.05)
    assert rejected[0] and rejected[1]
    assert not rejected[-1]
    assert np.all(np.diff(adj_p[np.argsort(p_vals)]) >= -1e-12) # 调整后 p 值保序


def test_ols_linear_regression_matrix_inference():
    """测试多维 OLS 解析解、高斯-马尔可夫 BLUE 统计推断与残差诊断"""
    np.random.seed(42)
    n = 200
    X_raw = np.random.randn(n, 3)
    X = np.column_stack([np.ones(n), X_raw])
    true_beta = np.array([3.0, 1.5, -2.0, 0.8])
    noise = np.random.normal(0, 0.5, size=n)
    y = X @ true_beta + noise
    
    reg = linear_regression_fit(X, y)
    assert np.allclose(reg["beta_hat"], true_beta, atol=0.15)
    assert reg["R2"] > 0.90
    assert reg["Adj_R2"] > 0.90
    assert reg["F_pval"] < 1e-5
    assert len(reg["p_vals"]) == 4
    assert np.all(reg["p_vals"] < 0.01) # 所有真系数均显著拒绝原假设
    assert len(reg["VIF"]) == 3
    assert np.all(np.array(reg["VIF"]) < 5.0) # 无共线性


def test_real_world_capstone_dataset_pipeline():
    """端到端测试真实世界厚尾偏态数据集 (financial_loss_or_delay_data.csv) 推断全流程"""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "financial_loss_or_delay_data.csv")
    assert os.path.exists(data_path), f"真实数据集文件不存在: {data_path}"
    
    df = pd.read_csv(data_path)
    assert len(df) == 1000
    assert "latency_ms" in df.columns
    
    latency = df["latency_ms"].values
    # 1. EDA 四阶矩检验偏态
    skew = stats.skew(latency)
    kurt = stats.kurtosis(latency)
    assert skew > 1.0, f"真实数据应当呈现明显右偏, 实际为 {skew:.2f}"
    assert kurt > 3.0, f"真实数据应当展现尖峰厚尾特征, 实际为 {kurt:.2f}"
    
    # 2. 多模型 MLE 拟合与 AIC 对比 (正态 vs Gamma vs 对数正态)
    res_norm = MLEFitter.fit_normal(latency)
    res_gamma = MLEFitter.fit_gamma(latency)
    res_lognorm = MLEFitter.fit_lognormal(latency)
    
    # 对数正态 / Gamma 应显著击败正态分布
    assert res_lognorm["aic"] < res_norm["aic"]
    assert res_gamma["aic"] < res_norm["aic"]
    
    # 3. BCa Bootstrap 计算极端分位数 (95% 分位数)
    q95_func = lambda x: np.percentile(x, 95)
    ci_low, ci_high, se_q95 = bootstrap_bca_ci(latency, stat_func=q95_func, n_boot=1000, alpha=0.05)
    sample_q95 = float(np.percentile(latency, 95))
    assert ci_low <= sample_q95 <= ci_high
    
    # 4. 多元回归建模
    X_mat = np.column_stack([
        np.ones(len(df)),
        df["request_volume"].values,
        df["server_load"].values,
        df["system_tier"].values,
        df["is_peak_hour"].values
    ])
    y_vec = np.log(df["latency_ms"].values) # 对数响应变量
    reg_res = linear_regression_fit(X_mat, y_vec)
    
    assert reg_res["R2"] > 0.40
    assert reg_res["F_pval"] < 1e-10
    # request_volume 和 server_load 系数应显著为正
    assert reg_res["beta_hat"][1] > 0
    assert reg_res["beta_hat"][2] > 0


def test_ols_singular_matrix_error():
    """测试当回归自变量存在完全多重共线性（矩阵不可逆）时抛出显式异常"""
    X_singular = np.array([
        [1.0, 2.0, 4.0],
        [1.0, 3.0, 6.0],
        [1.0, 4.0, 8.0],
        [1.0, 5.0, 10.0]
    ])  # n=4, p=3, 列 2 与列 3 线性相关 (2 * col 2 = col 3)
    y = np.array([5.0, 7.0, 9.0, 11.0])
    with pytest.raises((ValueError, RuntimeError, AssertionError, np.linalg.LinAlgError)):
        linear_regression_fit(X_singular, y)



def test_crlb_invalid_inputs():
    """测试 Starter Code 中 CRLB 参数异常值的保护边界"""
    with pytest.raises(ValueError):
        starter_code.calculate_fishers_exact_crlb("normal_mean", theta=1.0, n=-5)
    with pytest.raises(ValueError):
        starter_code.calculate_fishers_exact_crlb("unknown_family", theta=1.0, n=10)

