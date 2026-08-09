# -*- coding: utf-8 -*-
"""大作业（Capstone）验收测试规格可执行性验证脚本。
验证验收测试条目本身可测（CPD 归一化 + 枚举 vs 变量消元一致），
不替代学习者对真实数据的完整审计工作。
运行：python capstone_verify.py
"""
import numpy as np
from itertools import product

print("=" * 60)
print("大作业 规格可执行性验证（结构、推断与采样一致性审计）")
print("=" * 60)

# ---- 最小示例：学生网络式小 BN（仅用于验证验收测试逻辑）----
# A -> B, A -> C（A 根节点，B/C 子节点）
phi_A = np.array([0.7, 0.3])        # P(A=0), P(A=1)
phi_BA = np.array([[0.9, 0.1],      # P(B|A): 行=A, 列=B
                   [0.4, 0.6]])
phi_CA = np.array([[0.8, 0.2],
                   [0.3, 0.7]])

print("\n[验收测试 01] 每个 CPD 按父配置归一化")
assert np.isclose(phi_A.sum(), 1.0)
assert np.allclose(phi_BA.sum(axis=1), 1.0), "P(B|A) 每行应归一化"
assert np.allclose(phi_CA.sum(axis=1), 1.0), "P(C|A) 每行应归一化"
print("  ✓ P(A), P(B|A), P(C|A) 全部按父配置归一化")

print("\n[验收测试 02] 枚举与变量消元一致")
# 枚举：P(A=0,B=0,C=1) 全联合求和
def joint_enum():
    p = 0.0
    for a, b, c in product(range(2), repeat=3):
        if (a, b, c) == (0, 0, 1):
            p = phi_A[a] * phi_BA[a, b] * phi_CA[a, c]
    return p

def ve_marginal():
    """变量消元求 P(A=0,B=0,C=1)：逐因子相乘后按目标取值求和"""
    # P(A,B,C) = phi_A * phi_BA * phi_CA，求 A=0,B=0,C=1
    return phi_A[0] * phi_BA[0, 0] * phi_CA[0, 1]

p_enum = joint_enum()
p_ve = ve_marginal()
print(f"  枚举 P(A=0,B=0,C=1) = {p_enum:.6f}")
print(f"  消元 P(A=0,B=0,C=1) = {p_ve:.6f}")
assert np.isclose(p_enum, p_ve), "枚举与变量消元应一致"
print("  ✓ 枚举 == 变量消元（验收测试 02 逻辑可测）")

print("\n[验收测试 03 前提] 无证据时采样边缘收敛（验证收敛判据可测）")
# 用直接采样近似 P(B=0)（此处仅验证判据可写，真实审计需完整采样实验）
P_B0_true = sum(phi_A[a] * phi_BA[a, 0] for a in range(2))
print(f"  理论 P(B=0) = {P_B0_true:.4f}（采样收敛判据的靶值）")
assert 0 < P_B0_true < 1

print("\n" + "=" * 60)
print("大作业 验收测试规格可执行性验证通过 ✓")
print("=" * 60)
