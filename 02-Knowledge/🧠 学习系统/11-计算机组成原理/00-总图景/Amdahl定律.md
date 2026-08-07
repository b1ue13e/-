---
title: "Amdahl 定律与 Gustafson 定律 (Amdahl's Law)"
type: study
kind: concept
course: "计算机组成原理"
stage_moc: "[[🗺️ 阶段零：总图景]]"
flow: knowledge
tags:
  - 计算机组成原理
  - Amdahl定律
  - 并行计算
  - 加速比
status: completed
created: 2026-07-31
---

# Amdahl 定律与 Gustafson 定律 (Amdahl's Law)

## 1. Amdahl 定律定义与核心公式

**Amdahl 定律 (Amdahl's Law)** 的核心定义是：用于预测系统某一部分优化后，整体系统能获得的理论最大**加速比 (Speedup)** 的定量模型。由 Gene Amdahl 于 1967 年提出，是计算机体系结构中评估部件性能提升性价比的铁律。

**基本性质**：系统的整体加速比受到无法被优化的**串行比例 $f$** 的根本制约。即使将可并行部分无限加速，整体加速比也存在严格的上限 $1/f$。

---

## 2. 形式化推导与 Gustafson 定律

### Amdahl 定律推导
设原始执行时间为 $T_0$，可被加速（并行化）的部分比例为 $p$（$0 \le p \le 1$），不可加速的串行比例为 $f = 1 - p$。若将可加速部分的性能提升至原来的 $k$ 倍，则新的执行时间 $T_{\text{new}}$ 为：

$$T_{\text{new}} = T_0 \cdot (1 - p) + T_0 \cdot \frac{p}{k} = T_0 \cdot \left( (1-p) + \frac{p}{k} 
ight)$$

整体加速比 $S_{\text{latency}}$ 定义为原始时间与新时间之比：

$$S_{\text{latency}} = \frac{T_0}{T_{\text{new}}} = \frac{1}{(1-p) + \dfrac{p}{k}} = \frac{1}{f + \dfrac{1-f}{k}}$$

**理论极限**：当处理器核数 $k \to \infty$ 时：

$$S_{\text{limit}} = \lim_{k \to \infty} \frac{1}{f + \dfrac{1-f}{k}} = \frac{1}{f}$$

**因此**：若系统中有 10% 的串行代码（$f = 0.1$），即使使用无限多个 CPU 核心（$k \to \infty$），最大加速比也绝对无法超过 10 倍。

---

## 3. Amdahl 定律与 Gustafson 定律的区别与对比

| 维度 | Amdahl 定律 | Gustafson 定律 |
|:---|:---|:---|
| **核心假设** | **固定工作量 (Fixed Problem Size)** | **固定执行时间 (Fixed Time)** |
| **视角** | 增加核心数来缩短固定任务时间 | 增加核心数来解决更大规模问题 |
| **加速比公式** | $S = \dfrac{1}{f + \frac{1-f}{k}}$ | $S_{\text{scaled}} = k - f(k-1)$ |
| **极限行为** | 核心数 $k \to \infty$ 时收敛于 $1/f$ | 随着 $k$ 增加可线性扩展 |
| **指导意义** | 强调串行瓶颈的危害 | 强调超算在大规模并行上的优势 |

**局限（误区）**：Amdahl 定律忽略了并行化带来的额外开销（如线程同步、锁争用、通信延迟），实际加速比常在达到峰值后随核心数增加而下降。

关联知识点推荐：[[Roofline模型]]、[[流水线技术]]、[[伪共享]]、[[无锁编程]]。

---

## 4. Python 加速比计算与边界断言自测

```python
import math

def amdahl_speedup(p: float, k: float) -> float:
    """Amdahl 定律: p 为可并行比例, k 为并行加速倍数"""
    assert 0 <= p <= 1, "p 必须在 [0, 1] 范围内"
    assert k > 0, "k 必须大于 0"
    return 1.0 / ((1 - p) + p / k)

def gustafson_speedup(f: float, k: float) -> float:
    """Gustafson 定律: f 为串行比例, k 为核心数"""
    assert 0 <= f <= 1
    return k - f * (k - 1)

if __name__ == "__main__":
    # 自测验证 1: 90% 可并行, 8核处理器
    s8 = amdahl_speedup(0.9, 8)
    expected_s8 = 1.0 / (0.1 + 0.9 / 8)
    assert abs(s8 - expected_s8) < 1e-6

    # 自测验证 2: 极限断言 (无限核心)
    s_inf = amdahl_speedup(0.9, 1e9)
    assert abs(s_inf - 10.0) < 1e-4, f"极限应趋近 10, 得 {s_inf}"

    # 自测验证 3: Gustafson 扩展加速比对照
    g8 = gustafson_speedup(0.1, 8)
    assert abs(g8 - 7.3) < 1e-6
    assert g8 > s8, "Gustafson 加速比应高于 Amdahl"

    # 自测验证 4: 反例 - 无可并行部分 (p=0) 加速比恒等于 1
    s_zero = amdahl_speedup(0.0, 64)
    assert abs(s_zero - 1.0) < 1e-6

    print(f"Amdahl 8核加速比: {s8:.3f}x, 理论极限: {s_inf:.3f}x")
    print(f"Gustafson 8核扩展加速比: {g8:.3f}x")
    print("Amdahl 定律与 Gustafson 定律单元测试全部成功！")
```

---

## 5. 权威参考文献
- Amdahl, G. M. (1967). Validity of the single processor approach to achieving large scale computing capabilities. *AFIPS Conference Proceedings*, 30, 483-485. DOI: https://doi.org/10.1145/1465482.1465560
- Gustafson, J. L. (1988). Reevaluating Amdahl's law. *Communications of the ACM*, 31(5), 532-533. DOI: https://doi.org/10.1145/42411.42415
- Hennessy, J. L., & Patterson, D. A. (2017). *Computer Architecture: A Quantitative Approach* (6th ed.). Morgan Kaufmann. Chapter 1. DOI: https://doi.org/10.1016/C2014-0-03820-2
