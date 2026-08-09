# -*- coding: utf-8 -*-
"""
HW03 规格验证 (skill §7 GOV-6).
目的: 验证 swiss 上 Fisher LDA 一维投影重叠<2% 与 K-Means 轮廓系数∈[0.3,0.7] 自检声明。
LDA 用 mva_toolkit; K-Means/轮廓系数用 scikit-learn (作业环境依赖已声明)。
不提供学生答案。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from load_data import load_swiss_banknotes
from mva_toolkit import lda_fit
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def banner(t): print("\n=== " + t + " ===")

df = load_swiss_banknotes()
cols = ['Length','Left','Right','Bottom','Top','Diagonal']
X = df[cols].values
y = df['Is_Counterfeit'].values

banner("HW03 题目1 自检: Fisher LDA 一维投影重叠 < 2%")
res = lda_fit(X, y)
proj = res['projected'][:, 0]
m0, m1 = proj[y==0].mean(), proj[y==1].mean()
thr = (m0 + m1) / 2
# LDA 投影轴方向(eigenvector sign)任意: 按类均值较大一侧对齐标签, 取两种朝向中较优者
pred_a = (proj > thr).astype(int)          # high -> class 1
pred_b = (proj < thr).astype(int)          # low  -> class 1
acc = max(float((pred_a == y).mean()), float((pred_b == y).mean()))
overlap = 1.0 - acc
print(f"LDA 投影类均值: gen={m0:.2f} fake={m1:.2f} 阈值={thr:.2f}")
print(f"LDA 一维准确率={(1-overlap)*100:.2f}%  重叠={overlap*100:.2f}%")
assert overlap < 0.02, f"重叠 {overlap*100:.2f}% 应 < 2%"

banner("HW03 题目2 自检: K-Means(K=2) 平均轮廓系数 ∈ [0.3, 0.7]")
km = KMeans(n_clusters=2, n_init=10, random_state=0).fit(X)
labels = km.labels_
sil = float(silhouette_score(X, labels))
print(f"KMeans 平均轮廓系数 = {sil:.4f}")
assert 0.3 <= sil <= 0.7, f"轮廓系数 {sil:.4f} 超出 [0.3,0.7]"
print("PASS: LDA 重叠<2%, 轮廓系数∈[0.3,0.7]。")
