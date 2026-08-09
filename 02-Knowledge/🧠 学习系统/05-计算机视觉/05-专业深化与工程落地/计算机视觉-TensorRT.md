---
type: study
course: "05-计算机视觉"
topic: "TensorRT 推理优化与部署"
created: 2026-08-06
updated: 2026-08-06
status: ongoing
difficulty: intermediate
concept: ["TensorRT", "推理优化", "INT8量化", "模型部署", "CUDA"]
prerequisites: ["模型量化", "卷积神经网络CNN", "优化器SGD到Adam"]
upstream: ["[[模型量化]]", "[[卷积神经网络CNN]]"]
related: ["ONNXRuntime", "模型剪枝", "知识蒸馏"]
flow: knowledge
stage_moc: "[[🧭 阶段5-专业深化与工程落地]]"
kind: concept
source: "NVIDIA TensorRT 官方文档（docs.nvidia.com/deeplearning/tensorrt）；Leyuan Wang et al. TensorRT 技术报告"
tags: [学习, 计算机视觉, TensorRT, 推理优化, 部署]
---

# TensorRT：推理优化与部署

## 0. 学习边界

- **值得**：TensorRT 是 NVIDIA GPU 上推理部署的事实标准（TensorFlow/PyTorch 后端、自动驾驶、云服务都用它）；理解其优化原理（图优化 + 精度校准 + 层融合）对任何 GPU 推理任务都有价值。
- **不值得**：如果部署在非 NVIDIA 硬件（手机/ARM/Intel），TensorRT 不适用，应看 ONNXRuntime / OpenVINO / TFLite。

## 1. 这个知识点解决什么问题？

**问题**：训练好的模型（PyTorch/TensorFlow）直接推理很慢——算子粒度细（小 kernel 启动开销大）、默认 float32、没有利用 GPU 特性。

**TensorRT 的答案**：把训练模型**编译成针对目标 GPU 优化的推理引擎（engine）**，通过四类优化：
1. **图优化与层融合**（kernel fusion）：把相邻算子合并（Conv+Bias+ReLU → 单 kernel），减少内存访问与 kernel 启动。
2. **精度校准（INT8/FP16）**：在精度损失可控下用更低精度。
3. **显存优化**：内存复用、减少拷贝。
4. **自动调优（tactic selection）**：为每个算子选最优 CUDA kernel（不同 GPU 不同）。

## 2. 为什么它重要？它有什么用？

- **性能**：典型 2-5 倍加速（FP16），INT8 再翻倍；ResNet-50 在 T4 上 FP16 可达 ~4000 img/s。
- **生态**：PyTorch（torch-tensorrt）、ONNX（trtexec）、TensorFlow（TF-TRT）都能接入。
- **工业标准**：自动驾驶（NVIDIA DRIVE）、云推理（Triton Inference Server）、游戏（DLSS）都用 TensorRT。
- **注意**：engine 与 GPU 架构绑定（T4 的 engine 不能直接跑在 A100），且是闭源 SDK（非开源，需从 NVIDIA 下载）。

## 3. 学它之前需要哪些前置知识？

1. **[[模型量化]]**：INT8 量化的原理（scale/zero-point、校准集）是 TensorRT INT8 的基础。
2. **[[卷积神经网络CNN|CNN 结构]]**：熟悉 Conv/BN/ReLU 等算子才能理解层融合。
3. **基本部署概念**：ONNX 中间格式、batch 大小、动态 shape。

## 4. 用直觉语言解释它

训练模型像一本"词典"：每个词条（算子）都写得清清楚楚，但查起来慢（多次翻页）。TensorRT 像把词典重新排版成"速查手册"：
- 把常用搭配（Conv+Bias+ReLU）合成一个词条 → 少翻几页（kernel fusion）。
- 把繁体字换成简体（FP32→FP16/INT8）→ 每页更薄（精度降低）。
- 针对你的书架（GPU）定制排版 → 你的手册和别人的不同（engine 与 GPU 绑定）。

## 5. 正式定义、核心公式、符号解释

**核心概念**：
- **Engine（引擎）**：编译产物，绑定特定 GPU 架构与输入 shape，是部署交付物（.engine 文件）。
- **Builder**：构建引擎的配置器（batch、精度、工作空间、DLA 等）。
- **Tactic（策略）**：同一算子的不同 CUDA 实现，builder 通过 benchmarking 选择最优。

**主要优化技术**：

1. **层融合（Layer Fusion）**：
   - Conv + BN + ReLU → 单个 kernel（推理时 BN 可折叠进 Conv 权重）。
   - BN 折叠公式：$\hat{y} = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}}\gamma + \beta$ 可并入 $W' = \frac{\gamma}{\sqrt{\sigma^2+\epsilon}}W$，$b' = \frac{\gamma(b-\mu)}{\sqrt{\sigma^2+\epsilon}} + \beta$。

2. **精度模式**：
   - FP16：半精度，A100/T4 上吞吐翻倍，通常精度损失 <0.5%。
   - INT8：每张量量化 $\hat{x} = \text{round}(x / s)$，$s = \frac{x_{\max}}{127}$（对称量化）。需要**校准集**确定动态范围（默认 entropy calibration，最小化信息损失）。

3. **动态 shape / 显存优化**：输入 batch 动态、内存池复用。

4. **kernel auto-tuning**：builder 对每个算子跑多种 CUDA 实现，选延迟最低的（build 时间长，运行快）。

**INT8 校准（calibration）**：
$$
s = \frac{\max(|x|)}{\text{Q}_{\max}}
$$
校准集通常是验证集子集（如 500-1000 张），前向收集激活分布，确定每层 scale；entropy calibration 选使 KL 散度最小的阈值。

### 5.5 跨平台推理工具对比（ONNX Runtime / OpenVINO / MNN / NCNN）

TensorRT 是 **NVIDIA GPU 专用**的极致推理引擎；实际部署常按硬件选型：

| 工具 | 平台/硬件 | 特点 | 适用 |
|:---|:---|:---|:---|
| **ONNX Runtime** | 跨平台（CPU/GPU/移动端） | 开放标准 ONNX 模型直接推理；CPU 上也有优化；生态最广 | 通用部署、跨框架互转 |
| **OpenVINO** | Intel CPU/GPU/VPU | Intel 硬件深度优化，CPU 推理显著加速 | Intel 服务器/边缘设备 |
| **TensorRT** | NVIDIA GPU | 延迟最低、INT8/FP16 支持最好，但 engine 与 GPU 绑定 | GPU 服务器/车端 Orin |
| **MNN**（阿里） | 移动端（ARM CPU/GPU/NPU） | 移动端性能优化、模型压缩（量化/裁剪） | 手机 App 推理 |
| **NCNN**（腾讯） | 移动端/嵌入式 | 轻量、无第三方依赖、推理快速 | 手机/嵌入式 Linux |

**选型路径**：先导出 ONNX（通用中间格式）→ 按目标硬件选择推理后端（GPU→TensorRT、Intel CPU→OpenVINO、手机→MNN/NCNN）；量化与算子兼容性（算子不支持时回退到 CPU 实现）是常见坑。

## 6. 推导思路和思想来源

1. **为什么推理与训练不同**：训练需要反向传播（保留中间激活），推理只有前向（可融合、可低精度）；训练框架优化目标是吞吐（大 batch 训练），推理优化目标是延迟（单 batch 快速响应）。
2. **为什么 BN 可折叠**：推理时 BN 的 $\mu, \sigma$ 固定（无 batch 统计更新），可并入 Conv 权重——训练框架保留 BN 是必要的，推理合并后省一次 kernel。
3. **为什么 INT8 可行**：神经网络权重/激活分布集中，对称量化 + 校准能保持大部分信息；深度学习社区经验表明 INT8 精度损失通常 1-3%。
4. **为什么 engine 与 GPU 绑定**：kernel 选择（tactic）依赖 GPU 的 SM 数量、寄存器、张量核能力；换 GPU 需重新 build。

## 7. 例子：基础 → 中等 → 实际应用

**基础例子（BN 折叠）**：
Conv 权重 $W$、BN 参数 $\mu=0.5, \sigma^2=0.25, \gamma=2, \beta=0$：
- 折叠后 $W' = \frac{2}{\sqrt{0.25+1e-5}} W \approx \frac{2}{0.5}W = 4W$，$b' = \frac{2(0-0.5)}{0.5} = -2$
- 推理时 Conv+BN 变成单 Conv（+ReLU 融合）。

**中等例子（部署流程）**：
```
PyTorch 模型 → export ONNX → trtexec --onnx=model.onnx --fp16 --int8 --calib=calib.ptq → model.engine
运行：load engine → 分配输入输出 buffer → enqueue → 取结果
```
- ResNet-50 onnx 直接跑（T4）：~1.8ms/图
- TensorRT FP16：~0.9ms/图
- TensorRT INT8：~0.5ms/图
（数字为示意量级，实际取决于 GPU/批大小。）

**实际应用**：
- **自动驾驶**：DRIVE 平台 TensorRT 推理多摄像头感知。
- **云推理**：Triton 用 TensorRT 后端服务批量请求。
- **视频分析**：实时行人检测/人脸识别服务（INT8 部署）。

## 8. 常见误区和易混概念

| 误区 | 澄清 |
|:---|:---|
| "TensorRT 是开源的" | 不是：闭源 SDK，从 NVIDIA 官网/apt 获取（Developer 账号），但免费 |
| "engine 可跨 GPU 使用" | 不能：绑定 GPU 架构（compute capability）与输入 shape，换卡/换 shape 需重新 build |
| "TensorRT 自动量化无损失" | 不是：INT8 有精度损失，需校准集 + 精度验证（eval 对比） |
| "训练模型 = 部署模型" | 不同：部署要导出（ONNX/engine），且推理优化会牺牲灵活性（动态 shape 受限） |
| 与 [[02-Knowledge/🧠 学习系统/05-计算机视觉/05-专业深化与工程落地/模型量化\|模型量化]] 混淆 | 量化是"精度降低"的通用概念（可用 PyTorch QAT/ONNX 量化）；TensorRT 是"GPU 推理优化框架"，INT8 量化是它的一个功能 |

## 9. 相关知识点与 Obsidian 双链建议

- 上游：[[模型量化]]、[[卷积神经网络CNN|CNN]]
- 平行：[[模型剪枝]]、[[知识蒸馏]]（可组合的压缩方法）
- 替代：ONNXRuntime（跨硬件）、OpenVINO（Intel）

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 10. 闭卷复现任务

1. 手写 BN 折叠公式：给定 Conv+BN 参数，写出折叠后的 $W', b'$（10 分钟）。
2. 画 TensorRT 部署流水线：PyTorch → ONNX → trtexec（FP16/INT8+校准）→ engine → 推理（5 分钟）。
3. 解释为什么 engine 与 GPU 绑定，以及 INT8 需要校准集的原因（5 分钟）。

## 11. 自测题：5 道

- #自测题/基础 1. TensorRT 的交付物是什么？（编译后的 engine 文件，绑定 GPU 架构）
- #自测题/基础 2. 列举三类 TensorRT 优化（层融合 / INT8/FP16 精度 / kernel auto-tuning）
- #自测题/中等 3. INT8 量化需要什么额外数据？（校准集，用于确定激活的动态范围/scale）
- #自测题/中等 4. 为什么推理时 BN 可以折叠进 Conv？（推理时 BN 统计量固定，无 batch 更新）
- #自测题/较难 5. 为什么同一个 engine 不能在 T4 和 A100 之间复用？（tactic/kernel 选择依赖 GPU 计算能力，需重新 build）

## 12. 我的主动回忆区

> 填完并闭卷复述后打勾：
- [ ] 我能画出 TensorRT 部署流水线
- [ ] 我能默写 BN 折叠公式
- [ ] 我能解释 INT8 校准的意义

## 13. 给 Obsidian 的归档建议

- 与 [[模型量化|模型量化卡]] 关联：量化原理在那边，TensorRT 是它的工程落地。
- 阶段5 MOC 中它对应"模型部署 → 推理优化"板块。

## 学完后可以完成

> 下列作业在 `requires` 中引用了本卡，由 Dataview 实时派生（非人工维护反向链接）：

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

本卡另以前置「🧪 自测题」与闭卷复现作为形成性验收。

## 🔗 知识图谱

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

