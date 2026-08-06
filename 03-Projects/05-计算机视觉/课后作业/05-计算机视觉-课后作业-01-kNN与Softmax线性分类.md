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
license: "link-only；本地作业包为原创规格，官方题目/Starter 不复制"
created: 2026-08-06
status: planned
flow: project
tags: [作业, 计算机视觉, kNN, Softmax]
---

# 05-计算机视觉-课后作业-01-kNN与Softmax线性分类

## 📋 任务描述与学习目标

基于 CIFAR-10 子集，在固定协议下组织 kNN 与 Softmax 线性分类基线：实现距离矩阵、kNN 预测、Softmax 损失与梯度，完成最小公平对照和失败样本审计。

学完本节（阶段2 图像分类知识卡）后，你应该能：

- 用 NumPy 实现 kNN 的 L1/L2 距离矩阵与投票预测；
- 从零实现 Softmax 交叉熵损失与解析梯度（数值梯度验证）；
- 在固定训练/验证/测试切分下报告可复核的指标，并分析至少一类失败样本。

## 🎯 任务分层要求（基础 / 进阶 / 综合）

### 基础要求
- [ ] 用 `starter/run.py` 跑通 smoke 数据流程（输入输出可复核）
- [ ] 实现 kNN 距离矩阵（L1/L2）与 top-k 投票
- [ ] 实现 Softmax 损失 `L_i = -log(softmax(f)_{y_i})` 与梯度 `p_k - 1(y_i=k)`

### 进阶要求
- [ ] 用数值梯度（`scipy` 或手写中心差分）验证解析梯度
- [ ] 调优超参数（k、学习率、正则强度）并报告验证集曲线

### 综合要求
- [ ] 写一份最小对照报告：kNN vs Softmax 的准确率、速度与失败样本差异
- [ ] 完成 `submission_checklist.md` 与 `rubric.md` 自评

## 🔧 环境与复现

- 依赖：Python 3.11+、NumPy（`starter/` 内脚本仅依赖 numpy）
- 真实数据目录：`F:\-\03-Projects\data\computer_vision\hw01_cifar10_knn_softmax`（需 `cifar10.train.npz` / `cifar10.val.npz` / `label_map.json`；未到位时使用包内 smoke 数据）
- 运行命令与数据契约详见包内 `README.md`、`data_card.md`
- 固定随机种子并记录版本，结果可复现

## 📦 提交产物

- [ ] 实现代码（`starter/` 下新增或修改的模块）
- [ ] 运行日志与最小测试输出
- [ ] `reports/report_template.md` 填写的对照报告
- [ ] `baseline/README.md` 记录最小 baseline 与失败案例

## ✅ 验收标准与 Rubric

- 包内 `rubric.md` 为评分量表；`tests/test_hw01_cifar10_knn_softmax.py` 为 smoke 验收
- 硬验收：固定输入下测试通过；距离矩阵与梯度数值正确；报告含至少一个失败样本分析
- 不得复制第三方答案；官方作业保持 `link-only`

## 🔍 引导与自检

- 先跑 `check_data.py` 确认数据契约，再写算法
- 常见失败：距离矩阵形状错误、Softmax 数值溢出（建议减去最大值）、梯度忘记除以 N
- 提交前清单见 `submission_checklist.md`；里程碑与常见问题见 `milestones.md` / `faq.md`

## 🔗 知识依赖与后续

- 前置知识卡：`kNN与线性分类器`、`Softmax与SVM损失函数`、`图像分类任务与数据管线`（frontmatter `requires` 为唯一事实源）
- 完成后进入 [[05-计算机视觉-课后作业-02-两层网络与反向传播|HW02：两层网络与反向传播]]
- 作业包：[[README|HW01 真实作业包]]
