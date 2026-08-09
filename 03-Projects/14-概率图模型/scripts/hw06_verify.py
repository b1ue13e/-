# -*- coding: utf-8 -*-
"""课后作业-06 数值题验证脚本（VAE 高斯 KL / 重参数化）。
覆盖：题2 高斯 KL 手算（二维）+ 重参数化 z = mu + sigma*eps。
运行：python hw06_verify.py
"""
import numpy as np
from math import log

print("=" * 60)
print("课后作业-06 数值题验证（VAE 与主题模型）")
print("=" * 60)

# ---------- 题 2：高斯 KL ----------
print("\n[题2] KL(N(mu,sigma^2) || N(0,1)) = 0.5*(mu^2 + sigma^2 - 1 - log sigma^2)")

def gauss_kl(mu, var):
    return 0.5 * (mu**2 + var - 1 - log(var))

# 一维验证
kl1 = gauss_kl(0.5, 2.0)
print(f"  KL(N(0.5,2)||N(0,1)) = {kl1:.6f}")
# 手算: 0.5*(0.25 + 2 - 1 - log 2) = 0.5*(1.25 - 0.693147) = 0.5*0.556853 = 0.278426
assert abs(kl1 - 0.5*(0.25+2-1-log(2))) < 1e-9
assert abs(kl1 - 0.278426) < 1e-4

# 二维（独立分解求和）：mu=(0.5,1.0), sigma^2=(2.0,1.0)
mu = np.array([0.5, 1.0])
var = np.array([2.0, 1.0])
kl_2d = sum(gauss_kl(m, v) for m, v in zip(mu, var))
print(f"  KL(二维) = {kl_2d:.6f}")
# 手算: dim1=0.278426, dim2=0.5*(1+1-1-log1)=0.5*1=0.5 → 总和 0.778426
kl_dim2 = 0.5 * (1.0 + 1.0 - 1 - log(1.0))  # = 0.5
print(f"    手算: dim1={gauss_kl(0.5,2.0):.6f} + dim2={kl_dim2:.4f} = {kl_2d:.6f}")
assert abs(kl_2d - (0.278426 + 0.5)) < 1e-4

# ---------- 题 2（续）：重参数化 ----------
print("\n[题2续] 重参数化 z = mu + sigma*eps")
mu_r = 1.0
sigma_r = 0.5
eps = 0.8
z = mu_r + sigma_r * eps
print(f"  z = {mu_r} + {sigma_r}*{eps} = {z:.4f}  (期望 1.4)")
assert abs(z - 1.4) < 1e-9
print("  z 对 mu,sigma 可微 → ELBO 可反向传播求梯度（对比评分函数估计的方差）✓")

print("\n" + "=" * 60)
print("课后作业-06 数值题验证通过 ✓")
print("=" * 60)
