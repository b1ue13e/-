---
type: project
project_type: homework
course: "信号与系统"
assignment_id: "信号与系统-01"
assignment_level: stage
assignment_format: lab
stage_id: "07"
requires: ["[[FFT分解]]", "[[窗函数]]", "[[巴特沃斯]]", "[[离散频谱]]"]
source_type: open_source_project_task
created: 2026-07-29
status: planned
flow: project
tags: [作业, 信号与系统, FFT, 数字滤波器]
---
# 信号与系统 - HW01：FFT 算法与 Butterworth 滤波器

> 🎯 **作业目标**：手写 Cooley-Tukey 快速傅里叶变换 (FFT) 算法，设计 Butterworth 带通数字滤波器，并实现语音信号降噪。

---

## 学习目标
完成本阶段作业后，你应当能够：
- 不依赖高级变换库，自写 Cooley-Tukey 基-2 FFT（含位反转与蝶形运算），并验证其与 numpy.fft 数值一致；
- 用 scipy.signal 设计 IIR Butterworth 带通滤波器，对含噪语音做降噪并量化 SNR 提升；
- （挑战）实现 STFT 与 Griffin-Lim，完成声谱图相位重建；
- 用 pytest 固化核心计算的正确性。

## 任务边界
- 范围内：L1 卷积与时域绘图、L2 手写 FFT、L3 Butterworth 降噪、L4 STFT/相位重建 四级梯度，按需自选目标级。
- 核心算法须自写；允许用 numpy/scipy 做对照基准与滤波器设计接口，但 FFT/卷积核心不得直接调用现成封装替代。
- 语音样本使用公开或合成数据；MIT 6.003 仅作标杆参考，不 redistribut 其原题。
- 不要求：完全复现参考解的每个中间值；处理受限音频版权材料。

## 提交产物
- 可运行 notebook（.ipynb）或脚本（.py），含自写 FFT / 滤波器设计与固定 seed 的复现入口；
- 结果图：FFT 对照、滤波器幅频/相频、降噪前后波形与 SNR、STFT 声谱图（若做 L4）；
- 测试：pytest 用例（如 test_cooley_tukey_fft）通过；简短报告说明复现步骤与结论。

## 验收标准
- L1：卷积时域绘图正确，并验证采样定理。
- L2：相对误差 < 1e-6；手写 FFT 与 numpy.fft 完全吻合，并展示 O(N²) vs O(N log N) 时耗对比。
- L3：信噪比 SNR 提升 ≥ 12 dB。
- L4：STFT + Griffin-Lim 完成频谱图相位重建，可听/可视恢复。
- 综合 Rubric：正确性、可复现性、与库实现一致性、对数值误差的解释。

## 引导自检
提交前自检清单：
- [ ] 手写 FFT 与 numpy.fft 在复数随机输入上误差 < 1e-5？
- [ ] 位反转顺序是否正确（对照 brute-force DFT）？
- [ ] Butterworth 通带/阻带指标是否达到？降噪后 SNR 是否 ≥ 12 dB？
- [ ] pytest 是否全绿？固定 seed 他人能否复现？
常见失败点：位反转索引错导致频谱乱序；FFT 长度非 2 的幂未补零；滤波器系数不稳定（极点出单位圆）。调试：先在小 N、已知答案信号（如单频）上验证 FFT，再上语音。
## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-dsp/hw01_fft_filter.ipynb`
- **开源标杆仓库**：[MIT 6.003 Signals and Systems](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/)
- **核心依赖**：`numpy`, `scipy`, `matplotlib`, `pytest`

---

## 2. 🎯 难度分级（基础 / 进阶 / 综合 / 挑战）

| 梯度级别 | 目标 SNR 提升 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - 基础** | 卷积时域绘图正确 | `numpy` 实现离散卷积与信号时域/频域绘图，验证 Sampling Theorem 采样定理。 |
| 🟡 **L2 - 进阶** | 相对误差 < 1e-6 | **手写 Cooley-Tukey 蝶形 FFT 算法**，对比 $O(N^2)$ DFT 与 $O(N \log N)$ FFT 计算耗时。 |
| 🔴 **L3 - 综合** | 信噪比 SNR 提升 ≥ 12dB | 使用 `scipy.signal` 设计 IIR Butterworth 带通滤波器，并对混合多频噪声的语音信号降噪。 |
| ⭐ **L4 - 挑战** | 频谱图相位恢复 | 实现短时傅里叶变换 (STFT) 与 Griffin-Lim 算法完成声谱图 (Spectrogram) 的音频相位重建。 |

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
