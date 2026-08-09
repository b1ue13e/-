---
type: project
project_type: homework
course: "05-计算机视觉"
assignment_id: "计算机视觉-HW01"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/kNN与线性分类器]]", "[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/Softmax与SVM损失函数]]", "[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/反向传播与计算图]]", "[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/梯度下降CV]]"]
source_type: official_assignment
created: 2026-08-09
status: planned
flow: project
tags: [作业, 课后作业, 阶段2]
---

# 计算机视觉-HW01：kNN / SVM / Softmax 与反向传播

## 1. 作业身份与来源

- 编号：HW01（lesson）
- 本地化自：Stanford CS231n Assignment 1（kNN / SVM / Softmax / Two-Layer Net / Backprop），按本路径知识顺序裁剪与中文本地化。
- 许可：CS231n 作业以课程公开许可发布；本库仅翻译题面、改写同构任务，**不复制官方解答**。
- 改编关系：原 A1 拆分成本库 HW01（kNN/SVM/Softmax/反向传播）+ HW02（两层网络与训练）。

## 2. 学习目标

完成本作业后，应能：用纯 NumPy 实现并对比 kNN、SVM 多类铰链损失、Softmax 交叉熵三类分类器；手动推导两层网络对权重的梯度并用数值梯度验证；理解「数据预处理（均值归零）」对距离/梯度类方法的影响。

## 3. 任务背景与边界

- 数据集：CIFAR-10 子集（课程提供 `cifar10_utils.py`  loader，或本地同构小数据集）。
- 输入输出：输入为展平图像矩阵 `X (N, D)`，标签 `y (N,)`；输出为预测 `y_pred` 与损失/准确率。
- 假设：仅用 NumPy，禁止在本题直接使用 PyTorch `autograd`（HW03 才引入）；允许用 `np.dot`、`broadcasting`。
- 禁止：直接调用 `sklearn` 的 KNeighbors/SVC 完成主任务（可在「常见失败」环节做对照实验）。

## 4. 环境与依赖

- Python ≥ 3.9，依赖 `numpy`、`matplotlib`。
- 运行：`python -m hw01_knn_svm` 或 `pytest tests/test_hw01.py`。
- 资源约束：CIFAR-10 全量约 170 MB；调试期可先用 1000 样本子集（`num_train=1000`）。

## 5. 稳定题号

1. **Q1 kNN**：实现 L2 距离矩阵（禁止显式三重循环，用广播或 `(a-b)^2` 展开）；做 5-fold 交叉验证选 k。
2. **Q2 线性分类器**：实现 SVM 多类铰链损失 `+ 1/N Σ max(0, s_j - s_yi + Δ)` 与 Softmax 交叉熵 `−log(e^{s_yi}/Σe^{s_j})`，含 L2 正则项。
3. **Q3 梯度**：对两层网络 `f = W2·max(0, W1·x+b1)+b2` 解析推导 `∂L/∂W1, ∂L/∂W2`，并与中心差分数值梯度在容差 `1e-6` 内一致。
4. **Q4 训练**：用 SGD 联合训练 W1/W2/b1/b2，记录训练/验证损失曲线。

## 6. 提交产物

- `hw01.py` / `hw01.ipynb`：含上述实现与干净输出。
- `report.md`：kNN 交叉验证表、SVM vs Softmax 验证准确率对比、梯度检查通过截图、损失曲线。
- 运行命令与随机种子（`seed=42`）。

## 7. 验收标准（Rubric）

| 维度 | 满分 | 通过线 |
|:---|:---:|:---:|
| 正确性（距离/损失/梯度实现） | 40 | 数值梯度与解析梯度误差 < 1e-5 |
| 完整性（4 题全做） | 20 | 4 题均有可运行代码 |
| 解释质量（report 分析） | 25 | 说清 kNN 慢/内存大、SVM 与 Softmax 决策边界差异 |
| 可复现性（种子/命令） | 15 | 他人按命令复现曲线 |

## 8. 引导自检（不泄露答案）

- **检查点 C1**：先写 `compute_distances_no_loops` 后用小规模 `N=3` 与朴素循环版对拍，误差应为 0。
- **渐进提示 H1**：SVM 梯度别忘「对正确类 `s_yi` 也要反向贡献」；先固定 `Δ=1` 再调。
- **调试 D1**：若 Softmax 出现 `nan`，先对 `s_j` 做 `-max(s)` 平移（数值稳定），再想为什么。
- **调试 D2**：梯度检查不通过时，优先怀疑 `ReLU` 在 0 处次梯度与广播维度，而非公式。

## 9. 常见失败

- 忘记对训练集做**均值归零**（用训练集均值，不能在测试集上算），导致距离类方法失效。
- 数值梯度步长 `h` 过大（用 `1e-5` 量级中心差分）。
- 把 `N` 与 `D` 维度写反，矩阵乘形状对不上。

## 10. 提交前自检

- [ ] `pytest tests/test_hw01.py` 全绿（含梯度检查）
- [ ] report 含 4 张必需图表
- [ ] 未提交任何官方答案文本

## 11. 完成后入口

- 复盘：[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/反向传播与计算图|反向传播与计算图]]
- 下一作业：[[计算机视觉-课后作业-02-两层网络与训练|HW02]]
- 阶段 MOC：[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/🧭 阶段2-深度学习内核|阶段2]]
