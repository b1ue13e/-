---
title: "信号与系统 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "信号与系统 4-Tier 阶梯作业规范"
course: "信号与系统"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [信号与系统, 4Tier作业, 阶梯作业, 编程实战, PyTest, MIT6003, Oppenheim]
---

# 📻 信号与系统 4-Tier 阶梯作业全景规范说明书 (MIT 6.003 & Oppenheim 范式)

> 本说明书为 **12-信号与系统** 路径（基于 Oppenheim《Signals and Systems》与 MIT 6.003 / Think DSP）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ SciPy / NumPy `fft` 调包 / 基础信号生成 (正弦波, 方波) 与卷积验证
🟡 L2 - Medium Baseline   │ 频域滤波器设计 (低通/高通) / 极零图 (Pole-Zero Plot) 绘制
🔴 L3 - Strong Baseline   │ [核心] 不调用高级 FFT 库，从零手撕 Cooley-Tukey 快速傅里叶变换 (FFT) 与 离散时间卷积算法 (Overlap-Add)
👑 L4 - Boss Baseline     │ 实时流式 DSP (Digital Signal Processing) 处理引擎 / 实现相位声码器 (Phase Vocoder) 变调变速
```

---

## 🎯 信号与系统阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 连续与离散时间信号及线性时不变系统 (LTI Systems)
- **开源溯源**：Oppenheim Ch 1-2 / MIT 6.003 Lec 1-2
- 🟢 **L1**: 生成并可视化阶跃信号、冲激信号、复指数信号。
- 🟡 **L2**: 计算并绘制两个有限长离散信号的卷积和 (Convolution Sum) 结果。
- 🔴 **L3 (手撕核心)**：**手撕 离散时间线性时不变系统 (Discrete-Time LTI) 的状态空间表示法模拟器，以及差分方程求解引擎**。
- 👑 **L4**: 实现多速率信号处理 (Multirate DSP) 中的抽取 (Decimation) 与内插 (Interpolation) 滤波器。

### 2. HW02 - 连续与离散时间傅里叶变换 (CTFT & DTFT)
- **开源溯源**：Oppenheim Ch 3-5 / MIT 6.003 Lec 4-6
- 🟢 **L1**: 使用公式绘制方波与三角波信号的频谱 (幅度谱与相位谱)。
- 🟡 **L2**: 验证傅里叶变换的时移 (Time Shifting) 与频移 (Frequency Shifting) 性质。
- 🔴 **L3 (手撕核心)**：**从零手撕 离散时间傅里叶变换 (DTFT) 计算模块，分析由于窗函数 (Windowing) 引起的频谱泄漏 (Spectral Leakage)**。
- 👑 **L4**: 实现短时傅里叶变换 (STFT) 与频谱图 (Spectrogram) 计算引擎。

### 3. HW03 - 离散傅里叶变换与快速算法 (DFT & FFT)
- **开源溯源**：Oppenheim Ch 8 (from DSP Book) / Think DSP
- 🟢 **L1**: 调用 `scipy.fft` 分析一段真实音频文件的主要频率成分。
- 🟡 **L2**: 比较零填充 (Zero-Padding) 对 DFT 频谱分辨率的影响。
- 🔴 **L3 (手撕核心)**：**手撕 Cooley-Tukey 快速傅里叶变换算法 (Radix-2 FFT，包含位翻转 Bit-Reversal 与 蝶形运算 Butterfly Operations)**。
- 👑 **L4**: 扩展实现高效的二维 FFT (2D-FFT) 用于图像频域滤波。

### 4. HW04 - 采样定理、拉普拉斯与 Z 变换 (Sampling, Laplace & Z-Transform)
- **开源溯源**：Oppenheim Ch 7, 9, 10
- 🟢 **L1**: 模拟信号欠采样引起的混叠 (Aliasing) 现象。
- 🟡 **L2**: 使用 Z 变换极零图判定 IIR 系统的因果性 (Causality) 与稳定性 (Stability)。
- 🔴 **L3 (手撕核心)**：**基于 Z 变换推导结果，手撕 双线性变换 (Bilinear Transform) 算法，将模拟巴特沃斯 (Butterworth) 滤波器转换为数字 IIR 滤波器系数**。
- 👑 **L4**: 实现重叠相加法 (Overlap-Add) 与重叠保留法 (Overlap-Save) 执行大规模长序列的高效频域卷积。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-signals/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-signals/tests/test_hw02_dtft.py
pytest 03-Projects/projects-signals/tests/test_hw03_fft.py
pytest 03-Projects/projects-signals/tests/test_hw04_bilinear.py
```
