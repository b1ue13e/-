# HW03 小型 CNN 与训练工程 Real Assignment Package

这是一份面向学生自做的 `HW03` 真实作业包，不再只是说明页。

## 布置时机

U03 结束后，学生刚完成卷积、池化、数据增强和最小训练循环。

## 包内结构

- `starter/`：专题 starter、运行入口与数据检查脚本
- `baseline/`：baseline 记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `卷积与池化`
- `优化器与学习率`
- `训练日志与混淆矩阵`

## 教学目标

- 会组织 CNN 的最小训练、评测和日志闭环
- 会与 HW01/HW02 的基线做公平对照
- 会记录训练问题和失败样本

## 真实数据契约

预期真实数据目录：

`F:\-\03-Projects\data\computer_vision\hw03_cnn_training_engineering`

真实数据到位后，至少应包含：

- `cifar10_images.train.npz`
- `cifar10_images.val.npz`
- `label_map.json`

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `train.smoke.csv`
- `val.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\课程作业\05-计算机视觉\real_assignment_packages\hw03_cnn_training_engineering\starter\run.py" --input-dir "f:\-\03-Projects\data\computer_vision\hw03_cnn_training_engineering" --output-dir "f:\-\03-Projects\课程作业\05-计算机视觉\real_assignment_packages\hw03_cnn_training_engineering\your_outputs"
python "f:\-\03-Projects\课程作业\05-计算机视觉\real_assignment_packages\hw03_cnn_training_engineering\starter\check_data.py" --input-dir "f:\-\03-Projects\data\computer_vision\hw03_cnn_training_engineering"
pytest "f:\-\03-Projects\课程作业\05-计算机视觉\real_assignment_packages\hw03_cnn_training_engineering\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`小型 CNN 风格特征 + 线性头`

## 下一步建议

把 smoke 图像替换成真实 CIFAR-10 图像张量，再补真实 CNN 训练、增强和误差审计。
