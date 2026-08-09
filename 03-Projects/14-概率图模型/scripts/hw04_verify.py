# -*- coding: utf-8 -*-
"""课后作业-04 数值题验证脚本（因果推断：关联 vs 干预）。
覆盖：题1 后门调整数值（观测 P(Y=1|X=1) vs 干预 P(Y=1|do(X=1))）。
运行：python hw04_verify.py
"""

print("=" * 60)
print("课后作业-04 数值题验证（因果推断基础）")
print("=" * 60)

# 图: X <- Z -> Y, X -> Y；Z 为混淆。二值变量。
# P(Z=1)=0.5; P(X=1|Z=1)=0.9, P(X=1|Z=0)=0.1
# P(Y=1|X=1,Z=1)=0.6, P(Y=1|X=1,Z=0)=0.4
# P(Y=1|X=0,Z=1)=0.5, P(Y=1|X=0,Z=0)=0.3

PZ1 = 0.5
PX1_g_Z1 = 0.9
PX1_g_Z0 = 0.1
PY1_g_X1Z1 = 0.6
PY1_g_X1Z0 = 0.4
PY1_g_X0Z1 = 0.5
PY1_g_X0Z0 = 0.3

# 1) 观测 P(Y=1 | X=1)
# P(Z=1|X=1) = P(X=1|Z=1)P(Z=1) / P(X=1)
PX1 = PX1_g_Z1 * PZ1 + PX1_g_Z0 * (1 - PZ1)
PZ1_g_X1 = PX1_g_Z1 * PZ1 / PX1
PZ0_g_X1 = 1 - PZ1_g_X1
Pobs = PY1_g_X1Z1 * PZ1_g_X1 + PY1_g_X1Z0 * PZ0_g_X1
print("\n[题1] 观测 P(Y=1|X=1)")
print(f"  P(X=1) = 0.9*0.5 + 0.1*0.5 = {PX1:.4f}  (期望 0.5)")
print(f"  P(Z=1|X=1) = 0.9*0.5/{PX1:.4f} = {PZ1_g_X1:.4f}  (期望 0.9)")
print(f"  P(Y=1|X=1) = 0.6*{PZ1_g_X1:.4f} + 0.4*{PZ0_g_X1:.4f} = {Pobs:.4f}  (期望 ≈0.58)")
assert abs(PX1 - 0.5) < 1e-9
assert abs(PZ1_g_X1 - 0.9) < 1e-9
assert abs(Pobs - 0.58) < 1e-9, f"观测概率应 ≈0.58，实际 {Pobs}"

# 2) 干预 P(Y=1 | do(X=1))：后门调整（以 Z 调整，Z 是唯一混淆父）
Pdo = PY1_g_X1Z1 * PZ1 + PY1_g_X1Z0 * (1 - PZ1)
print("\n[题2] 干预 P(Y=1|do(X=1))（后门调整：按 P(Z) 而非 P(Z|X) 加权）")
print(f"  P(Y=1|do(X=1)) = 0.6*0.5 + 0.4*0.5 = {Pdo:.4f}  (期望 0.5)")
assert abs(Pdo - 0.5) < 1e-9

# 3) 差异来源
print("\n[题3] 对比")
print(f"  观测 {Pobs:.4f} vs 干预 {Pdo:.4f} → 差异 {abs(Pobs-Pdo):.4f}")
print("  差异来源：X=1 使 Z 后验上移（P(Z=1|X=1)=0.9 > 0.5），观测值混入混淆效应；")
print("  干预固定 X 后 Z 不再被 X 影响，按边缘 P(Z) 加权 → 因果效应")
assert Pobs > Pdo, "观测应 > 干预（混淆使 X=1 与高 Y 风险 Z 相关）"

print("\n" + "=" * 60)
print("课后作业-04 数值题验证通过 ✓")
print("=" * 60)
