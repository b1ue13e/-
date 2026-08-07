---
type: study
topic: NumPy信号
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: advanced
concept: 
prerequisites: []
related: []
tags: 
course: "信号与系统"
flow: knowledge
stage_moc: "[[🚀 第八阶段：工程实现]]"
kind: concept
assessment_exempt: true
sources:
  - "Think DSP Ch.1-7（numpy 基础）"
  - "NumPy 官方文档：numpy.fft"
  - "SciPy Lecture Notes"
assessment_exempt_reason: "软件/环境参考页，非可验收知识点卡"

upstream:
  - "[[离散信号]]"
  - "[[线性卷积]]"
---
# NumPy信号

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🚀 第八阶段：工程实现]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：Python 工具链
- 这张卡要回答的问题：用 NumPy 处理信号的基础操作有哪些？
- 阶段目标：掌握用 numpy 生成/表示信号、做 FFT、卷积，作为信号实验的底座。

## 对应教材（真实出处）
- Think DSP Ch.1-7（numpy 基础）
- NumPy 官方文档：numpy.fft
- SciPy Lecture Notes

## 一句话定义
> NumPy 提供数组化信号：np.linspace 造时间轴、np.sin/cos 造波、np.fft.fft/ifft 做变换、np.convolve 做卷积，是 Think DSP 的实验底座。

## 从学习内容上要抓什么
- 数组即信号，向量化避免循环。
- np.fft 默认未 fftshift，负频在后半。
- np.convolve(mode='same'/'full') 控输出长度。

## 核心内容
### 1. 基本定义与直觉
NumPy 把信号变成「一排数」，所有运算都在这排数上并行飞过——比逐个点循环快几个数量级。

### 2. 公式 / 机制 / 流程
$$X=np.fft.fft(x);\quad y=np.convolve(x,h,'full')$$

### 3. 一个最小例子
t=np.linspace(0,1,1000); x=np.sin(2*np.pi*50*t); X=np.fft.fft(x)。

### 4. 常见误区
- 忘记 fftshift 导致频谱左右颠倒。
- convolve 模式选错使长度不符预期。

## 和其他笔记的关系
- 前置：[[离散信号]]
- 前置：[[DFT线性]]
- 相关：[[SciPy信号]]
- 相关：[[Matplotlib信号]]
- 相关：[[线性卷积]]
- 返回阶段索引：[[🚀 第八阶段：工程实现]]

## 最小自测
- [ ] 列举 NumPy 信号常用函数。
- [ ] 为何要 fftshift？
- [ ] np.convolve 的 mode 有何区别？

*创建于：2026-04-18 · 更新于：2026-08-06*
