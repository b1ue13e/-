# -*- coding: utf-8 -*-
"""
HW01 规格验证 (skill §7 GOV-6).
目的: 验证作业规格可被执行(Harness 可跑), 并核对题面自检声明与真实计算。
不提供学生答案, 仅做规格可执行性与数值一致性核查。
"""
import sys, os, warnings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from load_data import load_swiss_banknotes
from mva_toolkit import hotelling_t2_two_sample, mardia_test

def banner(t): print("\n=== " + t + " ===")

# ---- 题目2 自检: swiss 两样本 Hotelling T^2 自由度 ----
banner("HW01 题目2 自检: swiss 两样本 Hotelling T^2 (df1=6, df2=193)")
df = load_swiss_banknotes()
cols = ['Length','Left','Right','Bottom','Top','Diagonal']
Xg = df[df['Is_Counterfeit']==0][cols].values
Xc = df[df['Is_Counterfeit']==1][cols].values
res = hotelling_t2_two_sample(Xg, Xc)
print(f"T2={res['T2']:.2f}  F={res['F_stat']:.2f}  df1={res['df1']}  df2={res['df2']}  p={res['p_value']:.2e}")
assert res['df1'] == 6, "df1 应为 6"
assert res['df2'] == 193, f"df2 应为 193, 实际 {res['df2']}"
assert res['p_value'] < 1e-9
print("PASS: df1=6, df2=193, p<1e-9")

# ---- Mardia 正态性诊断 ----
banner("HW01 题目2 自检: Mardia 正态性 (真钞 100 样本)")
mg = mardia_test(Xg)
print(f"skew p={mg['skewness_p_value']:.4f}  kurt p={mg['kurtosis_p_value']:.4f}  (仅报告, 不阈值断言)")

# ---- 题目1 玩具数据奇异性核查 ----
banner("HW01 题目1: 玩具数据 S_pooled 奇异性核查 (规格注意事项)")
G1 = np.array([[1,2],[2,3],[3,4]], float)
G2 = np.array([[4,5],[5,6],[6,7]], float)
m1, m2 = G1.mean(0), G2.mean(0)
S1 = np.cov(G1, rowvar=False, ddof=1)
S2 = np.cov(G2, rowvar=False, ddof=1)
Sp = ((2)*S1 + (2)*S2) / 4
cond = float(np.linalg.cond(Sp))
print(f"mean1={m1}  mean2={m2}")
print(f"S_pooled=\n{Sp}")
print(f"S_pooled 条件数 = {cond:.2e}  => 奇异, 逆矩阵不存在")
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    r = hotelling_t2_two_sample(G1, G2)
print(f"mva_toolkit 岭正则化 T2 = {r['T2']:.4f} (退化数据经正则化可得的参考值)")
assert cond > 1e10, "预期共线玩具数据导致 S_pooled 奇异"
print("SPEC NOTE: 题面要求'手算 S_pooled^{-1}', 但给定玩具数据完全共线 -> S_pooled 奇异, 逆不存在;")
print("           仅正则化 T2=13.5 可得。建议作者扰动玩具数据或显式改用广义逆。")

print("\n[HW01 verify] swiss df PASS; 玩具数据退化已记录(规格需作者决定: 扰动数据或改用广义逆)。")
