---
title: "信号与系统-题型-FFT算法与Butterworth滤波器手撕阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "信号与系统作业"
course: "12-信号与系统"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: intermediate
importance: A
concept: ["信号处理", "FFT算法", "数字滤波器"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/12-信号与系统/🗺️ 信号与系统学习路径|信号与系统学习路径]]"]
related: ["[[常微分方程-题型-相平面分析与Lyapunov函数阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/12-信号与系统/🗺️ 信号与系统学习路径|信号与系统学习路径]]"]
downstream: []
tags: [学习, 12-信号与系统, 作业, 实战, 阶梯作业]
aliases: ["DSP-HW01-FFT与滤波器作业"]
---

# 信号与系统 - HW01：FFT 算法与 Butterworth 滤波器手撕阶梯作业

> 🎯 **作业目标**：手写 Cooley-Tukey 快速傅里叶变换 (FFT) 算法，设计 Butterworth 带通数字滤波器，并实现语音信号降噪。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-dsp/hw01_fft_filter.ipynb`
- **开源标杆仓库**：[MIT 6.003 Signals and Systems](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/)
- **核心依赖**：`numpy`, `scipy`, `matplotlib`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 SNR 提升 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 卷积时域绘图正确 | `numpy` 实现离散卷积与信号时域/频域绘图，验证 Sampling Theorem 采样定理。 |
| 🟡 **L2 - Medium Baseline** | 相对误差 < 1e-6 | **手写 Cooley-Tukey 蝶形 FFT 算法**，对比 $O(N^2)$ DFT 与 $O(N \log N)$ FFT 计算耗时。 |
| 🔴 **L3 - Strong Baseline** | 信噪比 SNR 提升 ≥ 12dB | 使用 `scipy.signal` 设计 IIR Butterworth 带通滤波器，并对混合多频噪声的语音信号降噪。 |
| 👑 **L4 - Boss Baseline** | 频谱图相位恢复 | 实现短时傅里叶变换 (STFT) 与 Griffin-Lim 算法完成声谱图 (Spectrogram) 的音频相位重建。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_cooley_tukey_fft():
    from dsp_solvers import manual_fft
    x = np.random.randn(1024) + 1j * np.random.randn(1024)
    
    my_fft = manual_fft(x)
    np_fft = np.fft.fft(x)
    
    np.testing.assert_allclose(my_fft, np_fft, atol=1e-5, err_msg="手写 FFT 结果必须与 numpy.fft.fft 完全吻合")
```

---

## 🃏 Anki 卡片

- Q: 为什么 Cooley-Tukey 快速傅里叶变换 (FFT) 能将计算复杂度从 $O(N^2)$ 降低到 $O(N \log N)$？
- A: FFT 利用了旋转因子 $W_N^k$ 的周期性与对称性 ($W_N^{k+N/2} = -W_N^k$)，采用分治法 (Divide and Conquer) 将 $N$ 点 DFT 递归拆分为偶数项与奇数项两个 $N/2$ 点 DFT，通过蝶形运算复用计算中间值。
