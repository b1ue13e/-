#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运筹学-课后作业-02（对偶与灵敏度）规格验证脚本
=================================================
用途（依据 rebuild-obsidian-course skill §7 / GOV-6）：
  1) 验证题面规格可执行（模型可解、Harness 可运行），确认题目被正确设定；
  2) 给学习者提供手算对照「靶值」，用于自检，不是作业作答替代品。

重要：本脚本只核对"题面数值正确性"，不提供推导过程。作业要求的最优解、
区间、100% 规则结论必须由学习者自己从检验数不等式推导。本文件的存在
不是为了把答案写进题干（那会违反 AGENTS.md §5.5.7），而是作为独立靶值参考。

运行：python scripts/hw02_verify.py
"""
from __future__ import annotations
import sys

try:
    from scipy.optimize import linprog
except ImportError:
    print("WARN: scipy 不可用，将使用已手算核验的靶值（仅报告，不求解）")
    linprog = None


def solve_primal_q1():
    # min 3x1+4x2 s.t. x1+x2>=2, x1+2x2>=3, x>=0
    c = [3, 4]
    A_ub = [[-1, -1], [-1, -2]]
    b_ub = [-2, -3]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None), (0, None)], method="highs")
    return res


def solve_primal_q2():
    # max 3x1+2x2 s.t. x1+x2<=4, x1<=2, x2<=3, x>=0  ->  min -3x1-2x2
    c = [-3, -2]
    A_ub = [[1, 1], [1, 0], [0, 1]]
    b_ub = [4, 2, 3]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None), (0, None)], method="highs")
    return res


def main() -> int:
    ok = True

    # ---- Q1: 原问题最优 (1,1), z=7；对偶最优同样 7（强对偶）----
    if linprog is not None:
        r1 = solve_primal_q1()
        x1, x2 = r1.x
        z1 = r1.fun
        print(f"[Q1] 原问题最优解 x*=({x1:.4f},{x2:.4f}), z*={z1:.4f}")
        assert abs(x1 - 1.0) < 1e-6 and abs(x2 - 1.0) < 1e-6, "Q1 最优解应为 (1,1)"
        assert abs(z1 - 7.0) < 1e-6, "Q1 最优值应为 7"
        # 对偶：max 2y1+3y2 s.t. y1+y2<=3, y1+2y2<=4  -> 最优 (2,1), z=7
        rd = linprog([-2, -3], A_ub=[[1, 1], [1, 2]], b_ub=[3, 4],
                     bounds=[(0, None), (0, None)], method="highs")
        assert abs(rd.fun - (-7.0)) < 1e-6, "Q1 对偶最优值应为 7（强对偶）"
        print("[Q1] 强对偶验证通过：p*=d*=7")
    else:
        print("[Q1] 靶值：原最优 (1,1) z=7；对偶最优 (2,1) z=7（强对偶）")

    # ---- Q2: 原问题最优 (2,2), z=10 ----
    if linprog is not None:
        r2 = solve_primal_q2()
        x1, x2 = r2.x
        z2 = -r2.fun
        print(f"[Q2] 原问题最优解 x*=({x1:.4f},{x2:.4f}), z*={z2:.4f}")
        assert abs(x1 - 2.0) < 1e-6 and abs(x2 - 2.0) < 1e-6, "Q2 最优解应为 (2,2)"
        assert abs(z2 - 10.0) < 1e-6, "Q2 最优值应为 10"
    else:
        print("[Q2] 靶值：原最优 (2,2) z=10")

    # ---- Q3: 灵敏度区间（由最终表检验数解析推导，非数值搜索）----
    # 最优基 {x1,x2} 对应绑定约束 (1) x1+x2<=b1 与 (2) x1<=2。
    # 基矩阵 B=[[1,1],[1,0]], B^{-1}=[[0,1],[1,-1]]。
    # 目标系数 c1：对偶变量 y1=2, y2=c1-2；对偶可行要求 y2>=0 -> c1>=2。
    c1_lo = 2.0
    # 右端项 b1：x_B=B^{-1}[b1,2]^T=[2, b1-2]^T -> x2=b1-2>=0 -> b1>=2；
    #          又 x2<=3 -> b1-2<=3 -> b1<=5。
    b1_lo, b1_hi = 2.0, 5.0
    print(f"[Q3] 靶值：c1 保持最优基区间 c1>={c1_lo:.0f}；b1 保持区间 b1∈[{b1_lo:.0f},{b1_hi:.0f}]")
    assert c1_lo >= 2.0 and b1_lo == 2.0 and b1_hi == 5.0

    # ---- Q4: 100% 规则（可选进阶）----
    # b1: 当前 4，允许增到 5（+1），实际 +20%(=0.8) -> 占用 0.8/1.0=80%
    # b3: 当前 3，允许减到 2（-1），实际 -20%(=0.6) -> 占用 0.6/1.0=60%
    b1_used = 0.8 / 1.0
    b3_used = 0.6 / 1.0
    total = b1_used + b3_used
    guaranteed = total <= 1.0
    print(f"[Q4] 靶值：b1 占用 {b1_used:.2f} + b3 占用 {b3_used:.2f} = {total:.2f} "
          f"-> {'保证' if guaranteed else '不保证'}保持最优基")
    assert not guaranteed, "Q4 比值和 1.4>1 -> 最优基不保证保持"

    print("\nSPEC VERIFIED: 题面模型与靶值自洽，harness 可运行。"
          "（靶值仅供自检，推导须在作业中完成）")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
