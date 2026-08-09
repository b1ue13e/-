---
type: project
kind: project
project_type: homework
course: "05-计算机视觉"
assignment_id: "05-计算机视觉-HW01"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[kNN与线性分类器]]", "[[Softmax与SVM损失函数]]", "[[图像分类任务与数据管线]]"]
source_type: official_assignment
source_url: "https://cs231n.stanford.edu/2025/assignments.html"
source_course: "Stanford CS231n 2025 (Assignment 1)"
adapted_from: "CS231n A1 Q1 (kNN) 与 Q3 (Softmax)；本地为原创规格 + 非官方中文版"
license: "link-only；本地作业包为原创规格，官方题目/Starter 不复制"
created: 2026-08-06
updated: 2026-08-08
status: verified
execution_evidence: "2026-08-08 实际执行：pytest test_hw01_cifar10_knn_softmax.py 1 passed（smoke 管线：starter/run.py 在 smoke 数据上跑通 kNN+Softmax 基线，输出 summary.json，knn/softmax 准确率阈值 ≥0.5 通过）；配套 test_prereq_cv.py 6 passed + test_cv_course_integrity.py 1 passed。真实 CIFAR-10 npz 数据未就绪，smoke 阶段验证通过，完整训练待数据落地。"
flow: project
tags: [作业, 计算机视觉, kNN, Softmax]
---

# 05-计算机视觉-课后作业-01-kNN与Softmax线性分类

> 一句话任务：**用 NumPy 从零实现 kNN 分类器与 Softmax 线性分类器，在固定协议下做最小公平对照，并审计失败样本。** 本作业对应 Stanford CS231n 2025 Assignment 1 的 Q1（kNN）与 Q3（Softmax），本地为原创规格，官方题目保持 link-only。

## 📌 作业身份与来源

- **课程**：05-计算机视觉（阶段2 · 图像分类任务与数据管线之后）
- **规模/形态**：`assignment_level: lesson` / `assignment_format: lab`
- **来源**：Stanford CS231n 2025 A1 Q1/Q3（`source_url`，link-only，不复制官方题干）
- **版本**：本地原创规格 v2（2026-08-07 重构：补充详细题目、函数规格、梯度检查与 Rubric 明细）

## 🎯 学习目标

完成后你应能（可验证）：

1. 用向量化 NumPy 实现 kNN 的 L1/L2 距离矩阵与 top-k 投票预测（不写逐样本 for 循环）；
2. 从零实现数值稳定的 Softmax 交叉熵损失与解析梯度，并用中心差分数值梯度验证（相对误差 < 1e-6 量级）；
3. 在固定训练/验证/测试切分与固定随机种子下，报告可复核的 kNN（k 扫描）与 Softmax（学习率/正则扫描）指标；
4. 输出至少 3 个失败样本与类别级准确率表，解释至少一类系统性失败（而非只报最好结果）。

## 📚 所需知识（frontmatter `requires` 为唯一事实源）

| 知识卡 | 本作业用在哪里 |
|:---|:---|
| [[kNN与线性分类器]] | Q2/Q3 距离度量、k 近邻投票原理 |
| [[Softmax与SVM损失函数]] | Q4/Q5 Softmax 损失、解析梯度推导、数值梯度验证 |
| [[图像分类任务与数据管线]] | Q1/Q6 数据切分、预处理、评估协议 |

> 题目级依赖：Q4/Q5 依赖「Softmax与SVM损失函数」的梯度推导小节；Q6 依赖「图像分类任务与数据管线」的固定切分协议。完成 HW01 后再进入 [[05-计算机视觉-课后作业-02-两层网络与反向传播|HW02]]。

## 🚧 任务背景与边界

- **为什么做**：CNN 之前的稳定 baseline（kNN 死记硬背 vs 线性分类总结规律），是后续一切视觉模型的对照基准；手写反向传播前必须先在 Softmax 上把"损失 → 梯度 → 更新"的闭环跑通。
- **输入输出假设**：特征维度 D 与类别数 C 由数据决定；smoke 数据为 3 特征 CSV（`f1,f2,f3` + `label`），真实数据为 `cifar10.train.npz`（(N, 3072) float32 图像展平 + (N,) 标签）与 `label_map.json`。
- **禁止事项**：不得复制第三方实现或官方 Starter 压缩包；不得把 smoke 结果当作正式实验结论；距离矩阵禁止两层 for 循环逐样本实现（允许单层循环扫描 k）。

## 📝 详细题目（稳定题号，按序完成）

### Q1 数据加载与预处理（10 分）

实现 `load_data(train_csv, val_csv)`：

- 返回 `(X_train, y_train, X_val, y_val)`；`X` 形状 `(N, D)` float32，`y` 为标签数组；
- smoke CSV 只取 `f*` 列做特征，丢弃 `id`/`label` 列；
- 真实数据到位后，额外实现 `load_cifar_npz(dir)`：读取 `cifar10.train.npz`/`cifar10.val.npz`（键约定写进代码注释）、`label_map.json`，并将像素归一化到 `[0,1]`（`X / 255.0`）。

**验收**：`print(X_train.shape, y_train.shape)` 输出与数据一致；空文件抛 `ValueError`。

### Q2 kNN 距离矩阵（15 分）

实现 `compute_distances(X_train, X_val, metric='l2') -> (N_val, N_train)`：

- `l2`：用恒等式 `‖a-b‖² = ‖a‖² + ‖b‖² − 2a·b` 广播实现，开方前用 `np.maximum(..., 0)` 截断负值；
- `l1`：`np.abs(X_val[:, None, :] - X_train[None, :, :]).sum(axis=2)`；
- **手算校验**：`X_train=[[0,0],[1,1]]`，`X_val=[[0,1]]` → l2 与 l1 均得 `[[1.0, 1.0]]`。

**验收**：手算样例一致；在 smoke 数据（6×3）上 `dists.shape == (4, 6)`。

### Q3 kNN 预测（15 分）

实现 `predict_knn(X_train, y_train, X_val, k=3, metric='l2')`：

- 取每个验证样本最近的前 k 个训练标签做多数投票；
- 平局规则：按标签字典序取第一个（确定性输出）；
- 对比 `k ∈ {1, 3, 5}` 在验证集上的准确率。

**验收**：`k=1` 时准确率与"最近邻"直觉一致；smoke 上 `k=3` 达到可复现结果。

### Q4 Softmax 损失与解析梯度（20 分）

实现 `softmax_loss(W, X, y) -> (loss, grad)`：

- 公式：`L = (1/N) Σ_i [-log p_i[y_i]]`，`p_i = softmax(s_i)`，`s_i = X_i W`；
- 解析梯度：`∂L/∂W = (1/N) X^T (P − Y_onehot)`；
- **数值稳定**：每行先减最大 logit（不改变 softmax 结果）；
- 手算样例：`W=[[1,0],[0,1]]`，`X=[[1,0],[0,1]]`，`y=[0,1]` → `loss ≈ 0.3133`。

**验收**：手算样例一致；梯度形状与 `W` 一致。

### Q5 数值梯度验证（15 分）

实现 `numeric_gradient(loss_fn, W, X, y, eps=1e-6)`（中心差分，**用 float64 扰动避免舍入淹没**），并报告梯度检查表：

| W 元素 | 解析梯度 | 数值梯度 | 相对误差 |
|:---|:---|:---|:---|

- 相对误差 `|num−an| / max(1, |num|, |an|)`，阈值 `1e-6` 量级（eps=1e-6 时允许 1e-5 内）；
- smoke 自检：`check_gradient()` 返回最大相对误差，应 `< 1e-6`。

**验收**：梯度检查表所有元素通过阈值；解释"为什么减 max 不影响梯度"。

### Q6 训练与评估协议（15 分）

实现 `train_softmax(X_train, y_train, lr, reg, iters, batch_size, seed)`：

- 固定随机种子（`np.random.default_rng(seed)`）；权重初始化 `W ~ N(0, 0.01)`；
- 每步 `W -= lr * (grad + reg * W)`（L2 正则化梯度并入）；记录损失历史；
- 超参数扫描：`lr ∈ {0.1, 0.5, 1.0}`，`reg ∈ {0, 0.01, 0.1}`，报告验证集准确率表；
- kNN 扫描：`k ∈ {1, 3, 5}`，报告验证集准确率表。

**验收**：记录固定种子与数据版本；两表可复现；给出最优配置与理由。

### Q7 失败样本审计与对照报告（10 分）

- 至少 3 个失败样本（kNN 或 Softmax 至少一个预测错），说明每个样本的预测 vs 真值；
- 类别级准确率表（每个类别的 kNN / Softmax 准确率）；
- 对照报告回答：kNN 与 Softmax 谁更快？谁更准？失败模式差异？为什么？

**验收**：报告含数据来源、切分、种子、限制与下一步（写进 `reports/report_template.md`）。

### 里程碑（可检查的进度拆分）

- **M0** 跑通 `starter/run.py` smoke + `pytest tests/`（包内自检）；
- **M1** Q1-Q3 完成（数据加载 + 距离矩阵 + kNN 预测，手算样例通过）；
- **M2** Q4-Q5 完成（Softmax 损失 + 梯度检查表通过）；
- **M3** Q6-Q7 完成（对照报告 + 失败审计 + `rubric.md` 自评）。

## 🔧 环境与复现

- **依赖**：Python 3.11+、NumPy（`>= 1.24`）；可选 scipy（数值梯度对照，非必需）；真实数据读取可加 PIL/npz。
- **运行命令**：
  ```bash
  python starter/run.py --input-dir <数据目录> --output-dir <输出目录>
  python starter/check_data.py --input-dir <数据目录>
  pytest tests/
  ```
- **数据入口**：smoke 在 `F:\-\03-Projects\data\computer_vision\hw01_cifar10_knn_softmax\`；真实 CIFAR-10 子集同目录（未到位时用 smoke 完成 M0-M2，M3 需真实数据）。
- **固定随机种子**：训练与切分全部固定 `seed`，在报告与 README 记录 NumPy/Python 版本。
- **预计运行范围**：smoke 全流程 < 30 秒；真实数据（5000 训练样本 × 500 验证）距离矩阵 < 2 分钟（内存 < 1 GB）。

## 📦 提交产物

1. `starter/` 下新增/修改的模块（Q1-Q6 实现）；
2. `tests/` 至少保留 smoke test，鼓励补 Q2/Q4/Q5 的最小单测；
3. `reports/report_template.md` 填写的对照报告（Q7）；
4. `baseline/README.md` 记录最小 baseline 指标与失败案例；
5. `submission_checklist.md` 逐项勾选。

## ✅ 验收标准与 Rubric（100 分，≥75 通过）

| 题目 | 分值 | 满分行为 | 部分得分 | 不得分 |
|:---|:---:|:---|:---|:---|
| Q1 数据加载 | 10 | 接口正确、空文件报错、真实 npz 适配注释完整 | 接口正确但缺真实数据适配 | 无法加载 smoke |
| Q2 距离矩阵 | 15 | 向量化、手算样例一致、l1/l2 均实现 | 仅 l2 且手算一致 | 逐样本 for 循环或结果错误 |
| Q3 kNN 预测 | 15 | top-k 投票 + 平局确定性 + k 扫描表 | 投票正确无 k 扫描 | 预测错误 |
| Q4 Softmax | 20 | 公式/梯度正确 + 数值稳定 + 手算一致 | 公式正确但未减 max（溢出风险） | 梯度错误 |
| Q5 梯度检查 | 15 | 全元素通过阈值 + 解释减 max | 通过但未解释 | 未做或不过 |
| Q6 训练协议 | 15 | 固定种子 + 双扫描表 + 最优配置理由 | 单组超参无扫描 | 不可复现 |
| Q7 报告审计 | 10 | ≥3 失败样本 + 类别级表 + 对照结论 | 有失败样本无类别级分析 | 只报最好结果 |

> 硬验收（一票否决）：`pytest tests/` 通过；梯度检查通过；报告含至少一个失败样本分析；不得复制第三方答案。

## 🔍 引导与自检

**递进提示（不泄露答案）**：
1. 距离矩阵先从 3×3 手算开始，再对照你的实现输出；
2. Softmax 梯度用"概率 − one-hot"直觉记忆：`dL/ds = p − y_onehot`；
3. 梯度检查失败时，先查"是否忘了除 N"、"X 是否含偏置列"、"减 max 是否只作用在 exp 前"；
4. 数值梯度扰动用 float64：`0.1 + 1e-6` 在 float32 中会损失有效位。

**常见失败与调试方向**：

| 现象 | 可能原因 | 调试方向 |
|:---|:---|:---|
| `dists` 形状 `(N_train, N_val)` 反了 | 广播维度写反 | 检查 `X_val[:, None, :] - X_train[None, :, :]` |
| loss 为 `nan` | softmax 未减 max | `scores -= scores.max(axis=1, keepdims=True)` |
| 梯度检查相对误差 > 1e-4 | 未除 N / 正则梯度重复计入 | 检查 `grad / N` 与 `reg*W` 只加一次 |
| kNN 极慢 | 两层 for 循环 | 用广播一次算出距离矩阵 |
| 训练 loss 不下降 | lr 过大/过小 | 扫描 `lr ∈ {0.1, 0.5, 1.0}` |

**提交前清单**（对应 `submission_checklist.md`）：代码可运行、种子固定、两表齐全、≥3 失败样本、README 写清数据与限制。

## 🔁 任务层次与复盘

- **基础要求**：Q1-Q5（数据加载 → 距离矩阵 → kNN → Softmax → 梯度检查）；
- **进阶要求**：Q6 超参数扫描 + Q7 类别级失败审计（主任务完成前不做也行，但完成主任务不依赖它们）；
- **可选进阶（不占完成门槛）**：mini-batch Softmax、kNN 用 KD-Tree/scipy 加速、混淆矩阵热力图；
- **复盘入口**：完成后对比知识卡「Softmax与SVM损失函数」的梯度推导闭卷重推一遍；将失败样本记入 [[04-Review]] 复习队列；`rubric.md` 自评 < 75 时回到对应题目补做。
- **进入 HW02 的条件**：`pytest` 通过 + Rubric ≥ 75 + 梯度检查表通过。

## 🔗 知识依赖与后续

- 前置：[[kNN与线性分类器]]、[[Softmax与SVM损失函数]]、[[图像分类任务与数据管线]]（frontmatter `requires` 为唯一事实源）
- 下一站：[[05-计算机视觉-课后作业-02-两层网络与反向传播|HW02：两层网络与反向传播]]（把"损失→梯度→更新"闭环从线性推广到两层网络）
- 作业包：[[README|HW01 真实作业包]]（starter / tests / rubric / data_card / faq / milestones）
