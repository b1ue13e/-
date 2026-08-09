# -*- coding: utf-8 -*-
"""
HW02 规格验证 (skill §7 GOV-6).
目的: 验证 wine SVD-PCA 流程可跑, 并核对题面自检声明 (V 正交, 累积方差=1.0, 拐点).
不提供学生答案。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from load_data import load_wine_data
from mva_toolkit import pca_fit

def banner(t): print("\n=== " + t + " ===")

banner("HW02 自检: UCI Wine SVD-PCA")
dw = load_wine_data()
X = dw.drop(columns=['Cultivar']).values
r = pca_fit(X, n_components=13, standardize=True)
V = r['components']

# 正交性 V^T V = I
orth = bool(np.allclose(V.T @ V, np.eye(13), atol=1e-8))
print(f"载荷矩阵 V^T V == I ? {orth}")
assert orth, "主成分载荷应正交归一"

# 全部 13 个主成分累积方差精确等于 1.0
cum = float(r['cumulative_variance_ratio'][-1])
print(f"13 主成分累积方差贡献率 = {cum:.6f}")
assert abs(cum - 1.0) < 1e-6, "全部主成分累积方差应精确为 1.0"

# 拐点 / Kaiser
ev = r['explained_variance_ratio']
eig = r['explained_variance']
n = X.shape[0]
keep = int((eig > 1.0).sum())
print("前 5 主成分方差贡献率:", np.round(ev[:5], 3))
print(f"PC1={ev[0]:.3f} PC2={ev[1]:.3f} PC3={ev[2]:.3f} PC4={ev[3]:.3f}")
print(f"Kaiser 准则(特征值>1): 保留 {keep} 个主成分 (n-1={n-1})")

assert abs(ev.sum() - 1.0) < 1e-6
print(f"PASS: V 正交, 累积方差=1.0, Kaiser 保留 {keep} 个主成分 (拐点约在第 3-4 处)。")
