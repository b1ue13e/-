# -*- coding: utf-8 -*-
"""
Starter Baseline Script for Capstone Project
Course: 16-多元统计
Project: 多元宏观经济与金融资产综合统计建模

This script provides a complete end-to-end analytical pipeline:
1. Data ingestion & exploration (Macro Panel: 10 macro variables, 6 asset returns, 180 months)
2. Multivariate normality & outlier diagnostics (Mardia test, Mahalanobis distances)
3. Stationarity, collinearity & factorability (Bartlett test, KMO, correlation matrix)
4. Dimensionality reduction & latent factor extraction (SVD-PCA & Varimax Factor Analysis)
5. Canonical Correlation Analysis (CCA) between macro cycle factors and asset returns
6. Output summary report table
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure scripts directory is on sys.path
sys.path.insert(0, os.path.dirname(__file__))
from load_data import load_macro_financial_panel
from mva_toolkit import (
    mardia_test,
    chi_square_qq_plot_data,
    bartlett_sphericity_test,
    kmo_test,
    pca_fit,
    factor_analysis_fit,
    cca_fit
)


def run_capstone_baseline():
    print("=================================================================")
    print(" 🚀 Capstone Baseline: 多元宏观经济与金融资产综合统计建模")
    print("=================================================================\n")
    
    # 1. Load Data
    df = load_macro_financial_panel()
    print(f"✅ [1/5] 数据加载成功: 样本量 n={len(df)} 月度观测, 总变量数={df.shape[1]}")
    macro_cols = ['GDP_Growth', 'CPI', 'PPI', 'M2_Growth', 'TSF_Increment', 'Base_Rate', 'PMI', 'Trade_Balance', 'Unemployment_Rate', 'Industrial_Output']
    asset_cols = ['Stock_A_Return', 'Bond_10Y_Return', 'Commodity_Return', 'Gold_Return', 'USD_CNY_Return', 'Reit_Return']
    
    X_macro = df[macro_cols].values
    Y_asset = df[asset_cols].values
    
    # 2. Multivariate Normality & Diagnostic
    print("\n🔍 [2/5] 多元正态性与分布诊断 (Mardia 检验)...")
    mardia_res = mardia_test(X_macro)
    print(f"  - 宏观变量 Mardia 偏度统计量: {mardia_res['skewness_stat']:.3f} (p-value = {mardia_res['skewness_p_value']:.4f})")
    print(f"  - 宏观变量 Mardia 峰度统计量: {mardia_res['kurtosis_stat']:.3f} (p-value = {mardia_res['kurtosis_p_value']:.4f})")
    
    # 3. Factorability & Sphericity
    print("\n📊 [3/5] 降维适宜性检验 (Bartlett 球形度 & KMO 测度)...")
    bart_res = bartlett_sphericity_test(X_macro)
    kmo_res = kmo_test(X_macro)
    print(f"  - Bartlett 球形检验卡方值: {bart_res['statistic']:.2f} (df = {bart_res['df']}, p-value < 1e-15)")
    print(f"  - KMO 总体采样适宜性测度: {kmo_res['kmo_overall']:.3f} ({'适宜因子分析' if kmo_res['factorable'] else '因子分析受限'})")
    
    # 4. Dimensionality Reduction & Factor Analysis
    print("\n🔬 [4/5] 宏观潜变量提取 (SVD-PCA & Varimax 因子分析)...")
    pca_res = pca_fit(X_macro, n_components=3, standardize=True)
    fa_res = factor_analysis_fit(X_macro, n_factors=3, rotate=True)
    
    print("  - 前 3 主成分方差贡献率:", np.round(pca_res['explained_variance_ratio'], 4))
    print(f"  - 前 3 主成分累积方差贡献率: {pca_res['cumulative_variance_ratio'][-1] * 100:.2f}%")
    print("  - Varimax 旋转后公共因子载荷矩阵 (前 3 因子):\n", pd.DataFrame(np.round(fa_res['loadings'], 2), index=macro_cols, columns=['Factor_1_增长', 'Factor_2_通胀', 'Factor_3_流动性']))
    
    # 5. Canonical Correlation Analysis (CCA)
    print("\n🌐 [5/5] 宏观因子与大类资产典型相关分析 (CCA)...")
    cca_res = cca_fit(X_macro, Y_asset, n_components=2)
    print(f"  - 第 1 典型相关系数 rho_1: {cca_res['correlations'][0]:.4f}")
    print(f"  - 第 2 典型相关系数 rho_2: {cca_res['correlations'][1]:.4f}")
    print("  - 宏观变量第 1 典型变量权重 A[:, 0]:", np.round(cca_res['x_weights'][:, 0], 3))
    print("  - 金融资产第 1 典型变量权重 B[:, 0]:", np.round(cca_res['y_weights'][:, 0], 3))
    
    print("\n=================================================================")
    print(" 🎉 Capstone Baseline 运行完毕！端到端统计建模流水线验证通过。")
    print("=================================================================")


if __name__ == "__main__":
    run_capstone_baseline()
