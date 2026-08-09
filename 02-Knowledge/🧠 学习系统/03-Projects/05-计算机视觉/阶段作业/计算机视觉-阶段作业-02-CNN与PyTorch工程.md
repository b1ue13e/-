---
type: project
project_type: homework
course: "05-计算机视觉"
assignment_id: "计算机视觉-HW03"
assignment_level: stage
assignment_format: lab
stage_id: "02"
requires: ["[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/卷积神经网络CNN]]", "[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/批归一化BatchNorm]]", "[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/数据增强与正则化]]", "[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/计算机视觉-训练调试与常见报错]]"]
source_type: official_assignment
created: 2026-08-09
status: planned
flow: project
tags: [作业, 阶段作业, 阶段2]
---

# 计算机视觉-HW03：CNN / BatchNorm / Dropout 与 PyTorch 工程

## 1. 作业身份与来源

- 编号：HW03（stage），CS231n A2 本地化（CNN / BatchNorm / Dropout / PyTorch）。
- 许可：公开课程作业本地化，不复制官方解答。

## 2. 学习目标

完成本作业后，应能：用 PyTorch 从零实现带卷积、空间批归一化、Dropout 的 CNN；理解 **spatial BatchNorm 在 NCHW 上的统计量维度**；用 Torch 自动求导做端到端训练；将 HW01-02 的 NumPy 直觉迁移到框架。

## 3. 任务背景与边界

- 数据集：CIFAR-10（或本地同构子集）。
- 模型：卷积堆叠 + 全连接，中间插入 BatchNorm 与 Dropout。
- 假设：本题**允许并推荐** PyTorch；手写层的 forward/backward 仅作为对照（可用 `torch.nn` 实现主模型）。
- 禁止：直接 `torchvision.models` 现成网络当主模型提交（可用作对照实验）。

## 4. 环境与依赖

- `torch`、`torchvision`、`numpy`、`matplotlib`。
- 运行：`python -m hw03_cnn` 或 `pytest tests/test_hw03.py`（含 BN 前向数值检查）。
- 资源：单卡 CPU/GPU 均可；调试用 `num_train=2000` 子集。

## 5. 稳定题号

1. **Q1 卷积层**：实现 `Conv2d` 前向（im2col 或 `torch.nn.functional.conv2d` 对照），核对输出形状。
2. **Q2 Spatial BatchNorm**：实现训练态（用 batch 均值/方差）与推理态（用滑动平均），验证前向数值一致。
3. **Q3 Dropout**：实现带 `p` 的 Dropout 前向（训练缩放 `/p`）与推理直通，梯度经掩码。
4. **Q4 训练**：组装网络，用 `torch.optim` 训练，目标验证准确率超过 HW02 两层网络基线。

## 6. 提交产物

- `hw03.py` / `hw03.ipynb`、`models.py`：含上述层与训练。
- `report.md`：BN 前后激活分布对比、Dropout 对过拟合影响、最终验证准确率与训练曲线。
- 命令与随机种子（`seed=42`）。

## 7. 验收标准（Rubric）

| 维度 | 满分 | 通过线 |
|:---|:---:|:---:|
| 正确性（Conv/BN/Dropout） | 35 | BN 前向与 `torch.nn.BatchNorm2d` 误差 < 1e-4 |
| 完整性（4 题） | 20 | 三层均自实现且可切换 |
| 解释质量 | 25 | 说清 BN 为什么加速收敛、Dropout 推理为何要缩放 |
| 可复现性 | 20 | 固定种子复现曲线 |

## 8. 引导自检（不泄露答案）

- **检查点 C1**：先用 `torch.nn.BatchNorm2d` 跑通，再写手写版对拍，避免一次错两处。
- **渐进提示 H1**：BN 的 `running_mean` 只在训练态用 `momentum` 更新，推理态不更新。
- **调试 D1**：Loss 不降先查「是否忘了 `model.train()/eval()` 切换 BN/Dropout」。
- **调试 D2**：形状报错先看 conv 的 `padding` 与 `stride` 对输出尺寸公式 `out=(in+2p−k)/s+1`。

## 9. 常见失败

- 把 BatchNorm 用在批大小=1 或推理忘了切 `eval()`，统计量崩溃。
- Dropout 训练期未缩放 `/p`，测试期又重复缩放，准确率异常低。
- 学习率沿用 HW02 的 NumPy 值，PyTorch 默认初始化下过大。

## 10. 提交前自检

- [ ] `pytest tests/test_hw03.py` 通过
- [ ] report 含 BN 分布对比图
- [ ] 未提交官方答案

## 11. 完成后入口

- 复盘：[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/计算机视觉-训练调试与常见报错|训练调试与常见报错]]
- 下一作业：[[计算机视觉-阶段作业-03-迁移学习与可视化|HW04]]
- 阶段 MOC：[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/🧭 阶段2-深度学习内核|阶段2]]
