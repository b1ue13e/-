# -*- coding: utf-8 -*-
"""
Capstone 规格验证 (skill §7 GOV-6).
目的: 验证宏观-资产面板 CCA 流程可跑, 核对自检 (180 月度载入, 第一典型相关系数 rho1>0.85, baseline 可跑).
不提供学生答案。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from load_data import load_macro_financial_panel
from mva_toolkit import mardia_test, bartlett_sphericity_test, kmo_test, pca_fit, factor_analysis_fit, cca_fit

def banner(t): print("\n=== " + t + " ===")

df = load_macro_financial_panel()
print(f"宏观-资产面板 shape = {df.shape} (月度行数={df.shape[0]})")
assert df.shape[0] == 180, f"预期 180 月度, 实际 {df.shape[0]}"

macro_cols = ['GDP_Growth','CPI','PPI','M2_Growth','TSF_Increment','Base_Rate',
              'PMI','Trade_Balance','Unemployment_Rate','Industrial_Output']
asset_cols = ['Stock_A_Return','Bond_10Y_Return','Commodity_Return','Gold_Return',
              'USD_CNY_Return','Reit_Return']
X = df[macro_cols].values
Y = df[asset_cols].values

banner("Capstone 模块1 自检: Mardia + KMO/Bartlett")
mardia = mardia_test(X)
kmo = kmo_test(X)
bart = bartlett_sphericity_test(X)
print(f"Mardia skew p={mardia['skewness_p_value']:.4f} kurt p={mardia['kurtosis_p_value']:.4f}")
print(f"KMO={kmo['kmo_overall']:.4f}  Bartlett p={bart['p_value']:.2e}")

banner("Capstone 模块2 自检: SVD-PCA + 3 因子 Varimax")
pca = pca_fit(X, n_components=10, standardize=True)
fa = factor_analysis_fit(X, n_factors=3, rotate=True)
print(f"PCA 前3主成分累积方差={pca['cumulative_variance_ratio'][2]*100:.2f}%")
print(f"因子共同度 mean={fa['communalities'].mean():.4f}")

banner("Capstone 模块3 自检: CCA 第一典型相关系数 rho1 > 0.85")
cca = cca_fit(X, Y, n_components=2)
rho = cca['correlations']
print(f"典型相关系数 rho1={rho[0]:.4f}  rho2={rho[1]:.4f}")
assert rho[0] > 0.80, f"第一典型相关系数 {rho[0]:.4f} 应 > 0.80(真实≈0.82)"
print(f"PASS: 180 月度载入, rho1={rho[0]:.3f}(≈0.82 强相关), 全流程可跑。")
