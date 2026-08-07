---
type: project
kind: project
project_type: homework
course: "05-计算机视觉"
assignment_id: "05-计算机视觉-HW05"
assignment_level: stage
assignment_format: project
stage_id: "03"
requires: ["[[目标检测RCNN与YOLO]]", "[[IoU与NMS]]", "[[计算机视觉-FPN]]", "[[迁移学习与微调]]"]
source_type: official_assignment
source_url: "https://cs231n.stanford.edu/2025/assignments.html"
source_course: "Stanford CS231n 2025 / D2L Detection"
license: "link-only；本地作业包为原创规格，官方题目/Starter 不复制"
created: 2026-08-06
status: planned
flow: project
tags: [作业, 计算机视觉, 目标检测, Pascal VOC]
---

# 05-计算机视觉-阶段作业-03-目标检测PascalVOC

## 📋 任务描述与学习目标

搭建最小目标检测工程包：在 Pascal VOC 子集上完成数据加载、IoU/NMS 实现、检测模型训练与评测闭环，并分析错检、漏检与任务边界。

学完本阶段作业后你应该能：

- 实现 IoU 计算与 NMS，并解释其评测语义；
- 在固定协议下完成训练、评测与可视化闭环；
- 分析错检/漏检案例，说明检测任务的边界条件。

## 🎯 任务分层要求（基础 / 进阶 / 综合）

### 基础要求
- [ ] 用 `starter/` 跑通 VOC 数据加载与 smoke 评测
- [ ] 实现 IoU 与 NMS（NumPy/PyTorch）

### 进阶要求
- [ ] 训练一个最小检测模型（微调预训练骨干）并报告 mAP
- [ ] 输出检测可视化（PR 曲线或样例图）

### 综合要求
- [ ] 错检/漏检分析：至少一个失败模式 + 任务边界说明
- [ ] 完成 `rubric.md` 自评与提交清单

## 🔧 环境与复现

- 依赖：Python 3.11+、PyTorch、torchvision（`fasterrcnn_resnet50_fpn` 或等价骨干，版本以 `package_manifest.json` 为准）
- 真实数据目录：`F:\-\03-Projects\data\computer_vision\hw05_pascal_voc_detection_pkg`（需 `voc_annotations.train.json` / `voc_annotations.val.json`）
- 运行命令、数据契约、配置与 artifacts 详见包内 `README.md` / `data_card.md` / `configs/`

## 📦 提交产物

- [ ] 数据加载、IoU/NMS 实现与测试
- [ ] 训练脚本、评测输出与 mAP 记录
- [ ] 检测可视化与错检/漏检分析报告（`reports/`）
- [ ] `baseline/README.md`：最小 baseline 记录

## ✅ 验收标准与 Rubric

- 包内 `rubric.md` 为评分量表；`tests/` 为 smoke 验收
- 硬验收：IoU/NMS 数值正确；评测协议固定；报告含失败模式分析
- 不得复制第三方答案；官方作业保持 `link-only`

## 🔍 引导与自检

- 先在小样本上验证 IoU/NMS 数值正确性，再上全量数据
- 常见失败：类别标签偏移、NMS 阈值语义错误、评测时数据增强泄漏
- 提交前清单见 `submission_checklist.md`；常见问题见 `faq.md`

## 🔗 知识依赖与后续

- 前置知识卡：`目标检测RCNN与YOLO`、`IoU与NMS`、`FPN`、`迁移学习与微调`（frontmatter `requires` 为唯一事实源）
- 完成后进入阶段4-5 的开放课程项目（[[05-计算机视觉-大作业-开放课程项目|大作业：开放课程项目]]）
- 作业包：[[README|HW05 真实作业包]]
