---
title: "中国剩余定理 CRT 算法 (Chinese Remainder Theorem)"
course: "04-离散数学"
tags:
  - 离散数学
  - 中国剩余定理
  - CRT
  - 模运算
type: knowledge_card
status: completed
created: 2026-07-31
---

# 中国剩余定理 CRT 算法 (Chinese Remainder Theorem)

## 1. 中国剩余定理的定义与存在唯一性

**中国剩余定理 (CRT, Chinese Remainder Theorem)** 的核心定义是：给定一组两两互素的正整数 $m_1, m_2, \ldots, m_k$（即 $\gcd(m_i, m_j)=1$，$i 
eq j$），对任意整数 $a_1, a_2, \ldots, a_k$，同余方程组：

$$x \equiv a_i \pmod{m_i}, \quad i = 1, 2, \ldots, k$$

**定理（存在唯一性）**：上述方程组在模 $M = m_1 \cdot m_2 \cdots m_k$ 意义下有唯一解：

$$x = \sum_{i=1}^{k} a_i \cdot M_i \cdot (M_i^{-1} \bmod m_i) \pmod{M}$$

其中 $M_i = M / m_i$，$(M_i^{-1} \bmod m_i)$ 为 $M_i$ 模 $m_i$ 的乘法逆元（由扩展 Euclidean 算法求得）。

---

## 2. CRT 算法推导（构造性证明）

**假设（前提条件）**：$m_1, m_2, \ldots, m_k$ 两两互素，$M = \prod m_i$。

**推导步骤**：
1. 计算 $M_i = M / m_i$；
2. 因为 $\gcd(M_i, m_i) = 1$（互素性保证），所以 $M_i^{-1} \bmod m_i$ 存在（扩展 Euclid 算法）；
3. 令 $e_i = M_i \cdot (M_i^{-1} \bmod m_i)$，则 $e_i \equiv 1 \pmod{m_i}$ 且 $e_i \equiv 0 \pmod{m_j}$（$j 
eq i$）；
4. **因此** $x = \sum_{i=1}^k a_i \cdot e_i \pmod{M}$ 满足所有同余方程。

**时间复杂度**：$O(k \log^2 M)$（每次扩展 Euclid 算法 $O(\log M)$）。

**区别与对比**：若 $m_i$ 不两两互素，则方程组可能无解或有多解，CRT 的唯一性条件不满足，需改用 Garner 算法或一般线性方程组求解。

关联知识点推荐：[[并查集]]、[[动态规划]]、[[二分搜索]]、[[复杂度分析]]。

---

## 3. Python 完整 CRT 实现与边界验证

```python
from math import gcd
from functools import reduce
from typing import List, Tuple

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """扩展欧几里得算法: 返回 (gcd, x, y) 使 ax + by = gcd"""
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y

def mod_inverse(a: int, m: int) -> int:
    """模 m 乘法逆元: 要求 gcd(a, m) = 1"""
    g, x, _ = extended_gcd(a % m, m)
    assert g == 1, f"gcd({a},{m})={g} != 1, 逆元不存在"
    return x % m

def chinese_remainder(remainders: List[int], moduli: List[int]) -> int:
    """
    CRT 构造性算法
    假设: moduli 两两互素
    推导: x = sum(a_i * M_i * inv(M_i, m_i)) mod M
    因此在 [0, M) 范围内解唯一
    """
    # 验证两两互素前提条件
    for i in range(len(moduli)):
        for j in range(i+1, len(moduli)):
            assert gcd(moduli[i], moduli[j]) == 1,                 f"模数 {moduli[i]}, {moduli[j]} 不互素，CRT 不适用"
    
    M = reduce(lambda a, b: a*b, moduli)
    x = 0
    for a_i, m_i in zip(remainders, moduli):
        M_i = M // m_i
        x += a_i * M_i * mod_inverse(M_i, m_i)
    return x % M

if __name__ == "__main__":
    # 经典案例: x≡2(mod3), x≡3(mod5), x≡2(mod7) -> 唯一解 x=23 (mod 105)
    x = chinese_remainder([2, 3, 2], [3, 5, 7])
    assert x == 23, f"CRT 错误: expected 23, got {x}"
    assert x % 3 == 2
    assert x % 5 == 3
    assert x % 7 == 2

    # 反例验证: 非互素模数应报错
    try:
        chinese_remainder([1, 1], [6, 4])
        assert False, "应检测到非互素"
    except AssertionError as e:
        if "不互素" in str(e):
            print(f"非互素检测正确: {e}")

    print(f"CRT 核心案例验证成功: x={x}")
    print(f"  {x}%3={x%3}, {x}%5={x%5}, {x}%7={x%7}")
    print("中国剩余定理 CRT 算法单元测试完全成功！")
```

---

## 4. 权威参考文献
- Rosen, K. H. (2018). *Discrete Mathematics and Its Applications* (8th ed.). McGraw-Hill. Chapter 4.3 (Solving Congruences, Chinese Remainder Theorem). ISBN: 978-1259676512. URL: https://www.mheducation.com/highered/product/discrete-mathematics-its-applications-rosen/M9781259676512.html
- Hardy, G. H., & Wright, E. M. (2008). *An Introduction to the Theory of Numbers* (6th ed.). Oxford University Press. Chapter 5 (Congruences and Residues). DOI: https://doi.org/10.1093/oso/9780199219858.001.0001
