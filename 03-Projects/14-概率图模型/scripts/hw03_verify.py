# -*- coding: utf-8 -*-
"""课后作业-03 数值题验证脚本（只读验证题目答案正确性，不替代学习者作答）。
覆盖：题1 BN MLE 频率 / 题2 Laplace 平滑 / 题3 MRF theta / 题4 GMM EM 一步。
运行：python hw03_verify.py
"""
import numpy as np
from math import exp, log

print("=" * 60)
print("课后作业-03 数值题验证（参数学习与 EM）")
print("=" * 60)

# ---------- 题 1：BN MLE ----------
print("\n[题1] BN A->B MLE（数据: (1,1)x2,(1,0)x2,(0,1)x1,(0,0)x3）")
data = [(1,1)]*2 + [(1,0)]*2 + [(0,1)]*1 + [(0,0)]*3
N = len(data)
nA1 = sum(1 for a,_ in data if a==1)
nA0 = N - nA1
nB1A1 = sum(1 for a,b in data if a==1 and b==1)
nB0A1 = sum(1 for a,b in data if a==1 and b==0)
nB1A0 = sum(1 for a,b in data if a==0 and b==1)
nB0A0 = sum(1 for a,b in data if a==0 and b==0)
PA1 = nA1 / N
PB1A1 = nB1A1 / (nB1A1 + nB0A1)
PB1A0 = nB1A0 / (nB1A0 + nB0A0)
print(f"  P(A=1) = {nA1}/{N} = {PA1:.4f}  (期望 4/8=0.5)")
print(f"  P(B=1|A=1) = {nB1A1}/{nB1A1+nB0A1} = {PB1A1:.4f}  (期望 2/4=0.5)")
print(f"  P(B=1|A=0) = {nB1A0}/{nB1A0+nB0A0} = {PB1A0:.4f}  (期望 1/4=0.25)")
assert abs(PA1 - 0.5) < 1e-9, "P(A=1) 应 = 0.5"
assert abs(PB1A1 - 0.5) < 1e-9, "P(B=1|A=1) 应 = 0.5"
assert abs(PB1A0 - 0.25) < 1e-9, "P(B=1|A=0) 应 = 0.25"
print("  自由参数 = 1 + 2 = 3  ✓")

# ---------- 题 2：Laplace 平滑 ----------
print("\n[题2] Laplace 平滑 (alpha=1)")
PA1_s = (nA1 + 1) / (N + 2)
PB1A1_s = (nB1A1 + 1) / (nB1A1 + nB0A1 + 2)
PB1A0_s = (nB1A0 + 1) / (nB1A0 + nB0A0 + 2)
print(f"  P(A=1)平滑 = {PA1_s:.4f}  (期望 (4+1)/10=0.5)")
print(f"  P(B=1|A=1)平滑 = {PB1A1_s:.4f}  (期望 (2+1)/6≈0.5)")
print(f"  P(B=1|A=0)平滑 = {PB1A0_s:.4f}  (期望 (1+1)/6≈0.3333)")
diff_mle = abs(PB1A1 - PB1A0)
diff_s = abs(PB1A1_s - PB1A0_s)
print(f"  MLE 差异 |{PB1A1:.4f}-{PB1A0:.4f}|={diff_mle:.4f} vs 平滑差异 {diff_s:.4f} → 平滑缩小差异")
assert abs(PA1_s - 0.5) < 1e-9
assert abs(PB1A1_s - 0.5) < 1e-9
assert abs(PB1A0_s - 1/3) < 1e-9

# ---------- 题 3：MRF theta ----------
print("\n[题3] MRF P(x1,x2) ∝ exp(theta*1[x1=x2])，数据 (1,1)x2,(1,0)x1")
# 数据期望 E[f] = (2*1 + 1*0)/3 = 2/3
E_data = (2*1 + 1*0) / 3
print(f"  数据期望 E[f] = {E_data:.4f}  (期望 2/3)")
# 模型期望 E[f] = P(x1=x2) = (e^theta + e^theta)/(Z) 其中 Z = e^theta*2 + 2
# 令梯度 0: E_data - E_model = 0 → E_model = 2/3
# E_model = 2e^theta / (2e^theta + 2) = e^theta/(e^theta+1) = 2/3 → e^theta = 2 → theta = ln2
theta = log(2)
E_model = exp(theta) / (exp(theta) + 1)
print(f"  e^theta = {exp(theta):.4f}  (期望 2)")
print(f"  模型期望 E_model = {E_model:.4f}  (期望 2/3)")
print(f"  theta = ln2 = {theta:.4f}")
assert abs(exp(theta) - 2) < 1e-9
assert abs(E_model - 2/3) < 1e-9
assert abs(theta - log(2)) < 1e-9

# ---------- 题 4：GMM EM 一步 ----------
print("\n[题4] GMM EM 一步（数据 {0,4}，init pi=(0.5,0.5), mu=(-1,3), sigma2=(1,1)）")
x = np.array([0.0, 4.0])
pi = np.array([0.5, 0.5])
mu = np.array([-1.0, 3.0])
var = np.array([1.0, 1.0])
# E 步：责任
def gauss_pdf(v, m, vv):
    return (1.0 / np.sqrt(2*np.pi*vv)) * np.exp(-0.5*(v-m)**2/vv)
gamma = np.zeros((2, 2))
for t in range(2):
    for k in range(2):
        gamma[t, k] = pi[k] * gauss_pdf(x[t], mu[k], var[k])
    gamma[t] /= gamma[t].sum()
print(f"  gamma[0] (x=0) = [{gamma[0,0]:.6f}, {gamma[0,1]:.6f}]  (gamma_11=gamma[0,0])")
print(f"  gamma[1] (x=4) = [{gamma[1,0]:.6f}, {gamma[1,1]:.6f}]")
# 手算 gamma_11: p(x=0|N(-1,1)) = 1/sqrt(2pi)*exp(-0.5*1) = 0.24197; p(x=0|N(3,1)) = 1/sqrt(2pi)*exp(-4.5)=4.43e-4
g11 = gauss_pdf(0.0, -1.0, 1.0)
g12 = gauss_pdf(0.0, 3.0, 1.0)
gamma11_manual = (0.5*g11) / (0.5*g11 + 0.5*g12)
print(f"  手算 gamma_11 = {gamma11_manual:.6f}  (期望 ≈0.982)")
assert gamma[0,0] > 0.97, "gamma_11 应接近 1（样本0 远在分量1 附近）"
assert abs(gamma[0,0] - gamma11_manual) < 1e-9
# M 步：更新 mu, pi
Nk = gamma.sum(axis=0)
pi_new = Nk / Nk.sum()
mu_new = np.zeros(2)
for k in range(2):
    mu_new[k] = (gamma[:, k] @ x) / Nk[k]
print(f"  pi_new = [{pi_new[0]:.6f}, {pi_new[1]:.6f}]")
print(f"  mu_new = [{mu_new[0]:.6f}, {mu_new[1]:.6f}]")
print(f"  收敛方向：mu1 从 -1 向 {mu_new[0]:.3f}（样本0 主导），mu2 从 3 向 {mu_new[1]:.3f}（样本4 主导）")
assert 0.4 < pi_new[0] < 0.6, "pi_1 应接近 0.5（两样本责任不对称但总量接近）"
assert mu_new[1] > 3.8, "mu2 应接近 4（样本4 几乎全归分量2）"

print("\n" + "=" * 60)
print("课后作业-03 全部数值题验证通过 ✓")
print("=" * 60)
