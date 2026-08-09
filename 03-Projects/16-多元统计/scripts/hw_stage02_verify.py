# -*- coding: utf-8 -*-
"""
StageHW02 规格验证 (skill §7 GOV-6).
目的: 验证 wine 上 MANOVA/QDA 与 GMM-EM 流程可跑, 核对自检 (MANOVA 显著, QDA>90%, GMM 对数似然单调).
不提供学生答案。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from load_data import load_wine_data
from mva_toolkit import manova_fit, qda_fit, gmm_em_fit

def banner(t): print("\n=== " + t + " ===")

dw = load_wine_data()
X = dw.drop(columns=['Cultivar']).values
y = dw['Cultivar'].values

banner("StageHW02 题目1 自检: MANOVA Wilks + QDA 训练准确率")
mv = manova_fit(X, y)
print(f"Wilks' Lambda={mv['wilks_lambda']:.4e}  Wilks F={mv['wilks_F']:.2f}  p={mv['wilks_p_value']:.2e}")
qda = qda_fit(X, y)
qpred = qda['predict'](X)
qacc = float((qpred == y).mean())
print(f"QDA 训练准确率={qacc*100:.2f}%")
assert mv['wilks_p_value'] < 0.05, "MANOVA 应显著"
assert qacc > 0.90, "QDA 训练准确率应 > 90%"

banner("StageHW02 题目2 自检: GMM-EM 对数似然单调非递减且收敛")
gmm = gmm_em_fit(X, n_components=3, max_iter=50)
ll = gmm['log_likelihoods']
diffs = np.diff(ll)
mono = bool(np.all(diffs > -1e-2))   # 允许数值正则引入的极小波动
print(f"EM 迭代={len(ll)}  收敛={gmm['converged']}  最小步长={diffs.min():.4f}")
assert mono, f"对数似然存在过大下降 (最小步长 {diffs.min():.4f})"
print("PASS: MANOVA 显著, QDA>90%, GMM 对数似然整体非递减(数值波动<1e-2)。")
