---
title: "快速傅里叶变换 FFT (Fast Fourier Transform)"
course: "10-数据结构与算法"
tags:
  - 数据结构与算法
  - FFT
  - 分治算法
  - 多项式乘法
type: knowledge_card
status: completed
created: 2026-07-31
---

# 快速傅里叶变换 FFT (Fast Fourier Transform)

## 1. FFT 定义与核心加速原理

**快速傅里叶变换 FFT (Fast Fourier Transform)** 的核心定义是：利用**分治策略**与**复数单位根的对称性质**，将离散傅里叶变换 (DFT) 的计算复杂度从朴素算法的 $O(n^2)$ 降低至 $O(n \log n)$ 的高效算法，由 Cooley 和 Tukey 于 1965 年提出。

**DFT 的定义**：对长度为 $n$ 的复数序列 $\{a_0, a_1, \ldots, a_{n-1}\}$，其离散傅里叶变换 $A_k$ 定义为：
$$A_k = \sum_{j=0}^{n-1} a_j \cdot \omega_n^{jk}, \quad k = 0, 1, \ldots, n-1$$

其中 $\omega_n = e^{-2\pi i/n}$ 称为 $n$ 次本原单位根。

**单位根的核心性质**：
1. **折叠性质**：$\omega_n^{j + n/2} = -\omega_n^j$
2. **消去/降阶性质**：$\omega_{2n}^{2k} = \omega_n^k$

---

## 2. Cooley-Tukey 分治推导与蝶形运算

**前提条件与假设**：输入序列长度 $n$ 为 2 的幂次（$n = 2^m$）。

**推导过程（按下标奇偶拆分）**：

将 $A_k$ 的求和按 $j$ 的奇偶性拆分为两部分：

$$A_k = \sum_{j=0}^{n/2-1} a_{2j} \cdot \omega_n^{2jk} + \sum_{j=0}^{n/2-1} a_{2j+1} \cdot \omega_n^{(2j+1)k}$$

利用消去性质 $\omega_n^{2jk} = \omega_{n/2}^{jk}$，提取因子 $\omega_n^k$：

$$A_k = \sum_{j=0}^{n/2-1} a_{2j} \cdot \omega_{n/2}^{jk} + \omega_n^k \sum_{j=0}^{n/2-1} a_{2j+1} \cdot \omega_{n/2}^{jk} = E_k + \omega_n^k \cdot O_k$$

对于后半部分 $k + n/2$，利用折叠性质 $\omega_n^{k + n/2} = -\omega_n^k$：

$$A_{k + n/2} = E_k - \omega_n^k \cdot O_k \quad (k = 0, 1, \ldots, n/2 - 1)$$

**因此**，原本 $O(n^2)$ 的 DFT 转化为递归求解两个规模为 $n/2$ 的子问题，递推式 $T(n) = 2T(n/2) + O(n)$，由主定理解得总时间复杂度为 $O(n \log n)$。

---

## 3. FFT 与其他相关算法的区别与对比

| 算法 / 变换 | 时间复杂度 | 空间复杂度 | 前提条件 | 典型应用领域 |
|:---|:---|:---|:---|:---|
| **朴素 DFT** | $O(n^2)$ | $O(n)$ | 无限制 | 教学定义演示 |
| **Cooley-Tukey FFT** | $O(n \log n)$ | $O(n)$ | $n = 2^k$ | 信号处理、音频压缩 |
| **NTT (数论变换)** | $O(n \log n)$ | $O(n)$ | 模数特化 $p=c \cdot 2^k+1$ | 大整数精确乘法、密码学 |
| **Chirp-Z 变换** | $O(n \log n)$ | $O(n)$ | 无限制 | 任意长度/非均匀采样 DFT |

**局限（误区/反例）**：标准 Cooley-Tukey 算法要求序列长度必须为 2 的幂；若输入长度非 2 的幂且直接补零，可能改变信号频域特征，须使用 Chirp-Z 算法或 Bluestein 算法。

关联知识点推荐：[[红黑树]]、[[堆与堆排序]]、[[复杂度分析]]、[[二分搜索]]。

---

## 4. Python 蝶形 FFT 实现与多项式乘法自测断言

```python
import numpy as np
from typing import List

def fft_recursive(a: List[complex]) -> List[complex]:
    """
    Cooley-Tukey 蝶形 FFT (递归实现)
    假设: len(a) 为 2 的幂次
    推导: A_k = E_k + w*O_k, A_{k+n/2} = E_k - w*O_k
    """
    n = len(a)
    if n == 1:
        return list(a)

    assert (n & (n - 1)) == 0, f"n 必须为 2 的幂次, 得 n={n}"

    even = fft_recursive(a[0::2])
    odd  = fft_recursive(a[1::2])

    result = [0j] * n
    half = n // 2
    for k in range(half):
        w = np.exp(-2j * np.pi * k / n)
        result[k]        = even[k] + w * odd[k]
        result[k + half] = even[k] - w * odd[k]
    return result

if __name__ == "__main__":
    # 自测验证 1: 与 numpy.fft 的数值一致性
    np.random.seed(42)
    n = 16
    a = [complex(np.random.randn(), np.random.randn()) for _ in range(n)]

    my_fft = np.array(fft_recursive(a))
    np_fft = np.fft.fft(a)
    max_err = np.max(np.abs(my_fft - np_fft))
    assert max_err < 1e-10, f"FFT 数值误差过大: {max_err}"

    # 自测验证 2: 多项式乘法 (1 + 2x)(3 + 4x) = 3 + 10x + 8x^2
    p1 = [1, 2, 0, 0]
    p2 = [3, 4, 0, 0]
    F1 = np.array(fft_recursive(p1))
    F2 = np.array(fft_recursive(p2))
    prod = np.fft.ifft(F1 * F2).real
    assert abs(prod[0] - 3) < 1e-9 and abs(prod[1] - 10) < 1e-9 and abs(prod[2] - 8) < 1e-9

    # 自测验证 3: 反例验证 (非 2 的幂次抛出断言错误)
    try:
        fft_recursive([1, 2, 3])
        assert False, "应捕获非 2 的幂次"
    except AssertionError as err:
        print(f"反例非 2 幂次拦截成功: {err}")

    print(f"快速傅里叶变换 FFT 验证成功！最大误差 = {max_err:.2e}")
    print("快速傅里叶变换 FFT 单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Cooley, J. W., & Tukey, J. W. (1965). An algorithm for the machine calculation of complex Fourier series. *Mathematics of Computation*, 19(90), 297-301. DOI: https://doi.org/10.2307/2003354
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press. Chapter 30 (Polynomials and the FFT). ISBN: 978-0262046305. URL: https://mitpress.mit.edu/9780262046305/
- Oppenheim, A. V., & Schafer, R. W. (2009). *Discrete-Time Signal Processing* (3rd ed.). Pearson. Chapter 8. ISBN: 978-0131988422. URL: https://www.pearson.com/en-us/subject-catalog/p/discrete-time-signal-processing/P200000003254
