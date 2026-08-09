# -*- coding: utf-8 -*-
"""课后作业-05 数值题验证脚本（HMM 前向/后向/Viterbi）。
覆盖：题1 前向算法 / 题2 Viterbi 解码 / 题3 Baum-Welch 的 gamma_1(1)。
运行：python hw05_verify.py
"""
import numpy as np

print("=" * 60)
print("课后作业-05 数值题验证（HMM 三大问题）")
print("=" * 60)

# HMM: S={1,2}, O={0,1}, T=2, pi=(0.5,0.5)
# A = [[0.7,0.3],[0.4,0.6]], b1(0)=0.9,b1(1)=0.1; b2(0)=0.2,b2(1)=0.8
# O = (0, 1)
pi = np.array([0.5, 0.5])
A = np.array([[0.7, 0.3], [0.4, 0.6]])
B = np.array([[0.9, 0.1], [0.2, 0.8]])  # 行=状态, 列=观测 {0,1}
O = np.array([0, 1])
T, N = 2, 2

# ---------- 题 1：前向算法 ----------
alpha = np.zeros((T, N))
alpha[0] = pi * B[:, O[0]]
print("\n[题1] 前向算法")
print(f"  alpha_1 = [{alpha[0,0]:.6f}, {alpha[0,1]:.6f}]")
print(f"    手算: alpha_1(1)=0.5*0.9=0.45, alpha_1(2)=0.5*0.2=0.10")
for t in range(1, T):
    alpha[t] = (alpha[t-1] @ A) * B[:, O[t]]
print(f"  alpha_2 = [{alpha[1,0]:.6f}, {alpha[1,1]:.6f}]")
# 手算 alpha_2(1) = [0.45*0.7 + 0.10*0.4]*b1(1) = [0.315+0.04]*0.1 = 0.0355
# 手算 alpha_2(2) = [0.45*0.3 + 0.10*0.6]*b2(1) = [0.135+0.06]*0.8 = 0.156
print(f"    手算: alpha_2(1)=(0.45*0.7+0.10*0.4)*0.1=0.0355, alpha_2(2)=(0.45*0.3+0.10*0.6)*0.8=0.156")
P_O = alpha[T-1].sum()
print(f"  P(O|lambda) = {P_O:.6f}  (期望 0.0355+0.156=0.1915)")
assert abs(alpha[0,0] - 0.45) < 1e-9
assert abs(alpha[0,1] - 0.10) < 1e-9
assert abs(alpha[1,0] - 0.0355) < 1e-9
assert abs(alpha[1,1] - 0.156) < 1e-9
assert abs(P_O - 0.1915) < 1e-9

# ---------- 题 2：Viterbi ----------
print("\n[题2] Viterbi 解码")
delta = np.zeros((T, N))
psi = np.zeros((T, N), dtype=int)
delta[0] = pi * B[:, O[0]]
for t in range(1, T):
    for j in range(N):
        tmp = delta[t-1] * A[:, j]
        psi[t, j] = int(np.argmax(tmp))
        delta[t, j] = np.max(tmp) * B[j, O[t]]
print(f"  delta_1 = [{delta[0,0]:.6f}, {delta[0,1]:.6f}]")
print(f"  delta_2 = [{delta[1,0]:.6f}, {delta[1,1]:.6f}]  psi_2 = [{psi[1,0]}, {psi[1,1]}]")
# 手算: delta_2(1) = max(0.45*0.7, 0.10*0.4)*0.1 = max(0.315,0.04)*0.1 = 0.0315, psi=1
# 手算: delta_2(2) = max(0.45*0.3, 0.10*0.6)*0.8 = max(0.135,0.06)*0.8 = 0.108, psi=1
P_star = delta[T-1].max()
q2 = int(np.argmax(delta[T-1]))
q1 = int(psi[1, q2])
print(f"  P* = {P_star:.6f}  (期望 max(0.0315,0.108)=0.108)")
print(f"  最优路径 q = ({q1+1}, {q2+1})  (期望 (1,2))")
assert abs(delta[1,0] - 0.0315) < 1e-9
assert abs(delta[1,1] - 0.108) < 1e-9
assert abs(P_star - 0.108) < 1e-9
assert (q1 == 0 and q2 == 1), "最优路径应为 (1,2)"
assert P_star <= P_O, "P* (0.108) <= P(O) (0.1915)：解码概率 ≤ 总概率"

# ---------- 题 3：Baum-Welch 后向 + gamma_1(1) ----------
print("\n[题3] 后向算法 + gamma_1(1)")
beta = np.zeros((T, N))
beta[T-1] = 1.0
for t in range(T-2, -1, -1):
    beta[t] = (A * B[:, O[t+1]]) @ beta[t+1]
print(f"  beta_1 = [{beta[0,0]:.6f}, {beta[0,1]:.6f}]")
# 手算: beta_1(1) = sum_j A[1,j]*B[j,O2]*beta_2(j) = 0.7*0.1*1 + 0.3*0.8*1 = 0.07+0.24=0.31
# 手算: beta_1(2) = 0.4*0.1*1 + 0.6*0.8*1 = 0.04+0.48=0.52
gamma1 = alpha[0] * beta[0] / P_O
print(f"  gamma_1(1) = {gamma1[0]:.6f}  (期望 0.45*0.31/0.1915 ≈ 0.7285)")
assert abs(beta[0,0] - 0.31) < 1e-9
assert abs(beta[0,1] - 0.52) < 1e-9
assert abs(gamma1[0] - 0.45*0.31/0.1915) < 1e-9

print("\n" + "=" * 60)
print("课后作业-05 全部数值题验证通过 ✓")
print("=" * 60)
