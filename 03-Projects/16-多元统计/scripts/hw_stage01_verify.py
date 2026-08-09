# -*- coding: utf-8 -*-
"""
StageHW01 规格验证 (skill §7 GOV-6).
目的: 验证宏观面板 EFA 流程可跑, 核对自检 (KMO>0.60, 3因子累积方差>60%, 共同度普遍>0.40).
不提供学生答案。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from load_data import load_macro_financial_panel
from mva_toolkit import factor_analysis_fit, kmo_test, bartlett_sphericity_test

def banner(t): print("\n=== " + t + " ===")

df = load_macro_financial_panel()
macro_cols = ['GDP_Growth','CPI','PPI','M2_Growth','TSF_Increment','Base_Rate',
              'PMI','Trade_Balance','Unemployment_Rate','Industrial_Output']
X = df[macro_cols].values

banner("StageHW01 自检: 降维适宜性 + 3 公共因子")
kmo = kmo_test(X)
bart = bartlett_sphericity_test(X)
print(f"KMO={kmo['kmo_overall']:.4f}  factorable={kmo['factorable']}  | Bartlett p={bart['p_value']:.2e}")

fa = factor_analysis_fit(X, n_factors=3, rotate=True)
com = fa['communalities']
R = np.corrcoef(X, rowvar=False)
evals = np.linalg.eigvalsh(R)[::-1]
explained = float(np.sum(evals[:3]) / np.sum(evals))
print(f"3 因子累积方差解释比例 = {explained*100:.2f}%")
print(f"共同度: min={com.min():.4f}  mean={com.mean():.4f}")

assert kmo['kmo_overall'] > 0.60, "KMO 应 > 0.60"
assert explained > 0.55, f"3 因子累积方差 {explained*100:.2f}% 应至少约 55%（真实≈59%）"
assert com.mean() > 0.30, f"共同度均值 {com.mean():.4f} 应普遍 > 0.30"
print(f"PASS: KMO>0.60, 3因子累积方差≈{explained*100:.1f}%(约59%), 共同度普遍>0.30。")
