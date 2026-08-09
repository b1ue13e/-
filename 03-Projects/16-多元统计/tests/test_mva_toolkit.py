# -*- coding: utf-8 -*-
"""
Scientific and Pedagogical Unit Tests for mva_toolkit.py
Course: 16-多元统计

Verifies statistical accuracy across:
1. Distance & Distribution Diagnostics (Mahalanobis, Mardia Test, Chi-Square Q-Q)
2. Covariance Structure Tests (Box's M, Bartlett, KMO, Ledoit-Wolf)
3. Multivariate Hypothesis Testing (One/Two-Sample Hotelling T^2, MANOVA 4 Statistics)
4. Dimensionality Reduction (PCA, Varimax Factor Analysis, Classical MDS)
5. Classification & Clustering (Fisher LDA, QDA, GMM-EM log-likelihood monotonicity)
6. Association & Correspondence (CCA, Correspondence Analysis)
7. Real-world dataset integration (Swiss Banknotes, UCI Wine)
8. Numerical Safety & Condition Number regularizations
"""
import sys
import os
import pytest
import warnings
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from mva_toolkit import (
    mahalanobis_distance,
    mardia_test,
    chi_square_qq_plot_data,
    box_m_test,
    bartlett_sphericity_test,
    kmo_test,
    ledoit_wolf_shrinkage,
    hotelling_t2_one_sample,
    hotelling_t2_two_sample,
    manova_fit,
    pca_fit,
    varimax_rotation,
    factor_analysis_fit,
    mds_fit,
    lda_fit,
    qda_fit,
    gmm_em_fit,
    cca_fit,
    correspondence_analysis_fit
)
from load_data import load_swiss_banknotes, load_wine_data, load_macro_financial_panel


def test_mahalanobis_and_qq():
    x = np.array([2.0, 3.0])
    mu = np.array([0.0, 0.0])
    cov = np.array([[1.0, 0.5], [0.5, 2.0]])
    d2 = mahalanobis_distance(x, mu, cov)
    inv_cov = np.linalg.inv(cov)
    expected = float(x.T @ inv_cov @ x)
    assert np.isclose(d2, expected)
    
    # Q-Q plot data test
    np.random.seed(42)
    X = np.random.multivariate_normal(mu, cov, size=50)
    qq_data = chi_square_qq_plot_data(X)
    assert len(qq_data["ordered_d2"]) == 50
    assert len(qq_data["theoretical_quantiles"]) == 50
    assert qq_data["df"] == 2


def test_ill_conditioned_cov_regularization():
    # Construct an ill-conditioned covariance matrix (high collinearity)
    cov_ill = np.array([
        [1.0, 0.999999],
        [0.999999, 1.0]
    ])
    x = np.array([1.0, 1.0])
    mu = np.array([0.0, 0.0])
    
    with pytest.warns(RuntimeWarning, match="Ill-conditioned covariance matrix"):
        d2 = mahalanobis_distance(x, mu, cov_ill)
        assert np.isfinite(d2)


def test_mardia_normality():
    np.random.seed(42)
    X_norm = np.random.multivariate_normal([0, 0], np.eye(2), size=200)
    res = mardia_test(X_norm)
    assert res["skewness_p_value"] > 0.01
    assert res["kurtosis_p_value"] > 0.01
    assert "skewness_stat_small_sample" in res


def test_covariance_structure_and_shrinkage():
    np.random.seed(42)
    X1 = np.random.multivariate_normal([0, 0], np.eye(2), size=50)
    X2 = np.random.multivariate_normal([1, 1], np.eye(2), size=50)
    res_box = box_m_test([X1, X2])
    assert res_box["p_value"] > 0.05
    
    cov_high = np.array([
        [1.0, 0.8, 0.7],
        [0.8, 1.0, 0.75],
        [0.7, 0.75, 1.0]
    ])
    X_corr = np.random.multivariate_normal([0, 0, 0], cov_high, size=150)
    res_bart = bartlett_sphericity_test(X_corr)
    assert res_bart["p_value"] < 0.001
    
    res_kmo = kmo_test(X_corr)
    assert res_kmo["kmo_overall"] > 0.65
    
    X_high = np.random.randn(20, 30) # p > n
    res_lw = ledoit_wolf_shrinkage(X_high)
    assert 0.0 <= res_lw["shrinkage_intensity"] <= 1.0
    assert res_lw["shrunk_cov"].shape == (30, 30)
    eigvals = np.linalg.eigvalsh(res_lw["shrunk_cov"])
    assert np.all(eigvals > 0)


def test_hotelling_t2_empirical():
    df_bank = load_swiss_banknotes()
    cols = ['Length', 'Left', 'Right', 'Bottom', 'Top', 'Diagonal']
    X_gen = df_bank[df_bank['Is_Counterfeit'] == 0][cols].values
    X_fake = df_bank[df_bank['Is_Counterfeit'] == 1][cols].values
    
    res = hotelling_t2_two_sample(X_gen, X_fake)
    assert res["F_stat"] > 50.0
    assert res["p_value"] < 1e-5
    assert res["df1"] == 6
    assert res["df2"] == 193


def test_manova_wine():
    df_wine = load_wine_data()
    feature_cols = [c for c in df_wine.columns if c != 'Cultivar']
    X = df_wine[feature_cols].values
    y = df_wine['Cultivar'].values
    
    res = manova_fit(X, y)
    assert res["wilks_lambda"] < 0.1
    assert res["wilks_p_value"] < 1e-5
    assert res["pillai_trace"] > 1.0
    assert res["roys_largest_root"] > 0


def test_pca_and_factor_analysis():
    df_wine = load_wine_data()
    feature_cols = [c for c in df_wine.columns if c != 'Cultivar']
    X = df_wine[feature_cols].values
    
    res_pca_full = pca_fit(X, n_components=13, standardize=True)
    assert res_pca_full["components"].shape == (13, 13)
    assert np.isclose(np.sum(res_pca_full["explained_variance_ratio"]), 1.0, atol=1e-3)
    assert "whitened" in res_pca_full
    
    res_pca = pca_fit(X, n_components=3, standardize=True)
    assert res_pca["components"].shape == (3, 13)
    assert res_pca["cumulative_variance_ratio"][-1] > 0.65
    
    res_fa = factor_analysis_fit(X, n_factors=3, rotate=True)
    assert res_fa["loadings"].shape == (13, 3)
    assert np.all(res_fa["communalities"] >= 0)
    assert np.all(res_fa["communalities"] <= 1.0)


def test_mds_metric():
    D = np.array([
        [0.0, 3.0, 5.0],
        [3.0, 0.0, 2.0],
        [5.0, 2.0, 0.0]
    ])
    res = mds_fit(D, n_components=1)
    coords = res["coordinates"]
    reconstructed_d = np.abs(coords[0, 0] - coords[1, 0])
    assert np.isclose(reconstructed_d, 3.0, atol=1e-3)


def test_lda_and_qda_classification():
    df_bank = load_swiss_banknotes()
    cols = ['Length', 'Left', 'Right', 'Bottom', 'Top', 'Diagonal']
    X = df_bank[cols].values
    y = df_bank['Is_Counterfeit'].values
    
    res_lda = lda_fit(X, y)
    assert res_lda["W"].shape == (6, 1)
    
    res_qda = qda_fit(X, y)
    preds = res_qda["predict"](X)
    acc = np.mean(preds == y)
    assert acc > 0.95


def test_gmm_em_monotonicity():
    np.random.seed(42)
    X1 = np.random.multivariate_normal([-2, -2], np.eye(2)*0.5, size=40)
    X2 = np.random.multivariate_normal([3, 3], np.eye(2)*0.5, size=40)
    X = np.vstack([X1, X2])
    
    res = gmm_em_fit(X, n_components=2, max_iter=30)
    lls = res["log_likelihoods"]
    for i in range(1, len(lls)):
        assert lls[i] >= lls[i-1] - 1e-4


def test_cca_and_correspondence_analysis():
    df_macro = load_macro_financial_panel()
    macro_cols = ['GDP_Growth', 'CPI', 'PPI', 'M2_Growth', 'PMI']
    asset_cols = ['Stock_A_Return', 'Bond_10Y_Return', 'Commodity_Return']
    
    X = df_macro[macro_cols].values
    Y = df_macro[asset_cols].values
    
    res_cca = cca_fit(X, Y, n_components=2)
    assert len(res_cca["correlations"]) == 2
    assert res_cca["correlations"][0] >= res_cca["correlations"][1]
    assert np.all(res_cca["correlations"] <= 1.0)
    
    contingency = np.array([
        [60, 20, 10],
        [30, 50, 40],
        [10, 30, 80]
    ])
    res_ca = correspondence_analysis_fit(contingency, n_components=2)
    assert res_ca["total_inertia"] > 0
    assert len(res_ca["explained_inertia_ratio"]) == 2
    assert np.isclose(np.sum(res_ca["explained_inertia_ratio"]), 1.0, atol=1e-3)
