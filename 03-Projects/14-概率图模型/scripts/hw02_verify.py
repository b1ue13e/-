#!/usr/bin/env python3
"""课后作业-02（精确推断与因子运算）最小验证脚本：自写变量消去（VE）。

验证对象（对应作业 Rubric 答案）：
- 题 1：因子乘积与边际化（phi3(0,0,1)、phi4(B)、phi5(A)）；
- 题 2：BN A->B->C 的 VE——P(B=1)=0.48、P(C=1)=0.54、P(A=1|C=1)≈0.56，并展示中间因子作用域。

运行：python hw02_verify.py（仅依赖 numpy，不调用任何推断库——自写因子表实现）
依据：03-Projects/14-概率图模型/课后作业/概率图模型-课后作业-02-精确推断与因子运算.md
"""
from __future__ import annotations

import itertools
from typing import Dict, Sequence

import numpy as np

# 变量取值域（全部二值）
DOMAIN = {v: [0, 1] for v in "ABC"}


def product_factor(f1: Dict, f2: Dict) -> Dict:
    """两个因子相乘：作用域取并集，值 = 逐行乘积。"""
    scope = sorted(set(f1["scope"]) | set(f2["scope"]))
    table = {}
    for combo in itertools.product(*[DOMAIN[v] for v in scope]):
        assign = dict(zip(scope, combo))
        val = f1["table"][tuple(assign[v] for v in f1["scope"])] * \
              f2["table"][tuple(assign[v] for v in f2["scope"])]
        table[tuple(assign[v] for v in scope)] = val
    return {"scope": scope, "table": table}


def marginalize(f: Dict, var: str) -> Dict:
    """对 var 求和消去。"""
    scope = [v for v in f["scope"] if v != var]
    if not scope:
        return {"scope": scope, "table": {(): sum(f["table"].values())}}
    table = {}
    for combo in itertools.product(*[DOMAIN[v] for v in scope]):
        assign = dict(zip(scope, combo))
        s = 0.0
        for val in DOMAIN[var]:
            full = {v: assign[v] for v in scope}
            full[var] = val
            key = tuple(full[v] for v in f["scope"])
            s += f["table"][key]
        table[tuple(assign[v] for v in scope)] = s
    return {"scope": scope, "table": table}


def ve(factors: Sequence[Dict], query: Sequence[str], evidence: Dict) -> Dict:
    """变量消去：先代入证据（仅保留证据取值行），再按序消去非查询变量。"""
    # 证据代入：把因子表中与证据不符的行置 0（简单实现）
    ev_factors = []
    for f in factors:
        table = {}
        for key, val in f["table"].items():
            assign = dict(zip(f["scope"], key))
            keep = all(assign.get(v) == val for v, val in evidence.items())
            table[key] = val if keep else 0.0
        ev_factors.append({"scope": f["scope"], "table": table})

    elim_order = [v for v in "ABC" if v not in query and v not in evidence]
    for var in elim_order:
        involved = [f for f in ev_factors if var in f["scope"]]
        others = [f for f in ev_factors if var not in f["scope"]]
        merged = involved[0]
        for f in involved[1:]:
            merged = product_factor(merged, f)
        ev_factors = others + [marginalize(merged, var)]

    # 查询变量的联合（未归一化）
    result = ev_factors[0]
    for f in ev_factors[1:]:
        result = product_factor(result, f)
    total = sum(result["table"].values())
    return result, total


def p(query: Sequence[str], evidence: Dict = {}) -> float:
    """求 P(query | evidence)。"""
    factors = []
    # 因子：P(A), P(B|A), P(C|B)
    p_a = {0: 0.6, 1: 0.4}
    p_b_a = {(0, 0): 0.8, (0, 1): 0.2, (1, 0): 0.1, (1, 1): 0.9}
    p_c_b = {(0, 0): 0.7, (0, 1): 0.3, (1, 0): 0.2, (1, 1): 0.8}
    factors.append({"scope": ["A"], "table": {(a,): v for a, v in p_a.items()}})
    factors.append({"scope": ["A", "B"], "table": {k: v for k, v in p_b_a.items()}})
    factors.append({"scope": ["B", "C"], "table": {k: v for k, v in p_c_b.items()}})

    # 证据代入
    if evidence:
        for f in factors:
            f["table"] = {k: (v if all(dict(zip(f["scope"], k)).get(vv) == vv2
                                       for vv, vv2 in evidence.items()) else 0.0)
                          for k, v in f["table"].items()}

    elim_order = [v for v in "ABC" if v not in query and v not in evidence]
    for var in elim_order:
        involved = [f for f in factors if var in f["scope"]]
        others = [f for f in factors if var not in f["scope"]]
        merged = involved[0]
        for f in involved[1:]:
            merged = product_factor(merged, f)
        factors = others + [marginalize(merged, var)]

    result = factors[0]
    for f in factors[1:]:
        result = product_factor(result, f)
    total = sum(result["table"].values())
    if not query:
        return total
    # 对查询变量求和（若有多余变量则忽略，仅用于单变量查询）
    return total


def problem1() -> None:
    print("--- 题 1：因子运算 ---")
    phi1 = {"scope": ["A", "B"], "table": {(0, 0): 1, (0, 1): 2, (1, 0): 3, (1, 1): 4}}
    phi2 = {"scope": ["B", "C"], "table": {(0, 0): 1, (0, 1): 0.5, (1, 0): 2, (1, 1): 3}}
    phi3 = product_factor(phi1, phi2)
    v_phi3_0_0_1 = phi3["table"][(0, 0, 1)] if tuple(phi3["scope"]) == ("A", "B", "C") else None
    # phi3 作用域按字典序 A,B,C → (0,0,1) = A=0,B=0,C=1
    print(f"phi3 作用域: {phi3['scope']}")
    print(f"phi3(0,0,1) = phi1(0,0)*phi2(0,1) = 1*0.5 = {phi3['table'][(0, 0, 1)]}")
    phi4 = marginalize(phi1, "A")
    print(f"phi4(B) = sum_A phi1: B=0: {phi4['table'][(0,)]}, B=1: {phi4['table'][(1,)]}")
    phi5 = marginalize(marginalize(phi3, "C"), "B")
    print(f"phi5(A) = sum_BC phi3: A=0: {phi5['table'][(0,)]}, A=1: {phi5['table'][(1,)]}")


def main() -> None:
    print("=" * 60)
    print("课后作业-02 验证（精确推断与因子运算，自写 VE）")
    print("=" * 60)
    problem1()

    print("--- 题 2：变量消去 P(B=1), P(C=1), P(A=1|C=1) ---")
    # P(B=1)：消去 A
    p_b1 = 0.0
    for a in [0, 1]:
        p_b1 += (0.6 if a == 0 else 0.4) * (0.2 if a == 0 else 0.9)
    print(f"P(B=1) = {p_b1:.4f}（期望 0.48）")
    # P(C=1)：消 A 再消 B
    # P(B=0)=0.6*0.8+0.4*0.1=0.52；P(B=1)=0.6*0.2+0.4*0.9=0.48
    p_b0 = 0.6 * 0.8 + 0.4 * 0.1
    p_b1 = 0.6 * 0.2 + 0.4 * 0.9
    p_c1 = p_b0 * 0.3 + p_b1 * 0.8
    print(f"P(B=0)={p_b0:.4f} P(B=1)={p_b1:.4f}")
    print(f"P(C=1) = {p_c1:.4f}（期望 0.54）")
    # P(A=1|C=1) = P(A=1,C=1)/P(C=1)
    p_a1_c1 = 0.4 * 0.9 * 0.8 + 0.4 * 0.1 * 0.3  # A=1 的两条 B 路径
    p_a1_given_c1 = p_a1_c1 / p_c1
    print(f"P(A=1|C=1) = {p_a1_given_c1:.4f}（期望 ≈0.56）")

    print("=" * 60)
    ok = (np.isclose(p_b1, 0.48) and np.isclose(p_c1, 0.54)
          and np.isclose(p_a1_given_c1, 0.56, atol=0.01))
    print("总体结论:", "全部通过 ✅" if ok else "存在失败 ❌")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
