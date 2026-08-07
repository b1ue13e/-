#!/usr/bin/env python3
"""课后作业-01（表示与条件独立）最小验证脚本。

验证对象（对应作业 Rubric 答案）：
- 题 1：菱形 BN 的链式分解参数计数（答案 9）与 P(A=1,B=1,C=1,D=1)；
- 题 3：两变量 MRF 的配分函数 Z=9、P(X1=1)=6/9、P(X1=1|X2=0)=4/6、势函数整体缩放不变性。

运行：python hw01_verify.py（仅依赖 numpy）
依据：03-Projects/14-概率图模型/课后作业/概率图模型-课后作业-01-表示与条件独立.md
"""
from __future__ import annotations

import numpy as np


def problem1_diamond_bn() -> dict:
    """题 1：A->B, A->C, B->D, C->D，全二值。"""
    # 自由参数计数：每张 CPT = 父组合数 × (取值数-1)
    params = {"P(A)": 1, "P(B|A)": 2, "P(C|A)": 2, "P(D|B,C)": 4}
    total = sum(params.values())

    # 手算联合 P(A=1,B=1,C=1,D=1)
    p_a = 0.5
    p_b_given_a = 0.8   # P(B=1|A=1)
    p_c_given_a = 0.7   # P(C=1|A=1)
    p_d_given_bc = 0.9  # P(D=1|B=1,C=1)
    joint = p_a * p_b_given_a * p_c_given_a * p_d_given_bc

    return {"param_count": total, "expected_param_count": 9,
            "P(A=1,B=1,C=1,D=1)": joint, "expected_joint": 0.5 * 0.8 * 0.7 * 0.9}


def problem3_mrf() -> dict:
    """题 3：两变量 MRF，psi(0,0)=1, psi(0,1)=2, psi(1,0)=2, psi(1,1)=4。"""
    psi = np.array([[1.0, 2.0], [2.0, 4.0]])
    Z = psi.sum()
    # 边缘 P(X1=1) = (psi(1,0)+psi(1,1))/Z
    p_x1_1 = (psi[1, 0] + psi[1, 1]) / Z
    # 条件 P(X1=1|X2=0) = psi(1,0)/(psi(0,0)+psi(1,0))
    p_x1_given_x2_0 = psi[1, 0] / (psi[0, 0] + psi[1, 0])
    # 势函数整体乘 3：联合不变（Z 也乘 3）
    psi3 = psi * 3.0
    Z3 = psi3.sum()
    p_x1_1_scaled = (psi3[1, 0] + psi3[1, 1]) / Z3

    return {"Z": Z, "expected_Z": 9,
            "P(X1=1)": p_x1_1, "expected_P(X1=1)": 6 / 9,
            "P(X1=1|X2=0)": p_x1_given_x2_0, "expected_cond": 4 / 6,
            "scaled_Z": Z3, "scaled_P(X1=1)": p_x1_1_scaled,
            "scale_invariant": np.isclose(p_x1_1_scaled, p_x1_1)}


def check(name: str, got: float, expected: float) -> None:
    ok = np.isclose(got, expected)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got={got:.6f} expected={expected:.6f}")


def main() -> None:
    print("=" * 60)
    print("课后作业-01 验证（表示与条件独立）")
    print("=" * 60)

    r1 = problem1_diamond_bn()
    check("题1 参数计数", r1["param_count"], r1["expected_param_count"])
    check("题1 P(A=1,B=1,C=1,D=1)", r1["P(A=1,B=1,C=1,D=1)"], r1["expected_joint"])

    r3 = problem3_mrf()
    check("题3 Z", r3["Z"], r3["expected_Z"])
    check("题3 P(X1=1)", r3["P(X1=1)"], r3["expected_P(X1=1)"])
    check("题3 P(X1=1|X2=0)", r3["P(X1=1|X2=0)"], r3["expected_cond"])
    check("题3 缩放后 P(X1=1) 不变", r3["scaled_P(X1=1)"], r3["P(X1=1)"])
    print(f"题3 缩放后 Z = {r3['scaled_Z']:.1f}（同步放大 3 倍，联合分布不变）")

    print("=" * 60)
    all_pass = (np.isclose(r1["param_count"], r1["expected_param_count"])
                and np.isclose(r1["P(A=1,B=1,C=1,D=1)"], r1["expected_joint"])
                and np.isclose(r3["Z"], r3["expected_Z"])
                and np.isclose(r3["P(X1=1)"], r3["expected_P(X1=1)"])
                and np.isclose(r3["P(X1=1|X2=0)"], r3["expected_cond"])
                and r3["scale_invariant"])
    print("总体结论:", "全部通过 ✅" if all_pass else "存在失败 ❌")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
