# HW04 迁移学习与误差分析 Real Assignment Package

这是一份面向学生自做的 `HW04` 真实作业包，不再只是说明页。

## 布置时机

U04 前半段，学生已完成基础 CNN 训练，并开始比较预训练特征迁移和微调。

## 包内结构

- `starter/`：专题 starter、运行入口与数据检查脚本
- `baseline/`：baseline 记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `预训练与特征迁移`
- `冻结层与微调策略`
- `类别级误差分析`

## 教学目标

- 会组织冻结特征与微调的公平对照
- 会同时报告效果提升与训练成本
- 会做类别级误差分析和失败审计

## 真实数据契约

预期真实数据目录：

`F:\-\03-Projects\data\computer_vision\hw04_transfer_learning_error_analysis`

真实数据到位后，至少应包含：

- `cifar10_transfer.train.npz`
- `cifar10_transfer.val.npz`
- `label_map.json`
- `transfer_config.json`

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `train.smoke.csv`
- `val.smoke.csv`

## 运行方式

```bash
python "F:\-\03-Projects\05-计算机视觉\real_assignment_packages\hw04_transfer_learning_error_analysis\starter\run.py" --input-dir "F:\-\03-Projects\data\computer_vision\hw04_transfer_learning_error_analysis" --output-dir "F:\-\03-Projects\05-计算机视觉\real_assignment_packages\hw04_transfer_learning_error_analysis\your_outputs"
python "F:\-\03-Projects\05-计算机视觉\real_assignment_packages\hw04_transfer_learning_error_analysis\starter\check_data.py" --input-dir "F:\-\03-Projects\data\computer_vision\hw04_transfer_learning_error_analysis"
pytest "F:\-\03-Projects\05-计算机视觉\real_assignment_packages\hw04_transfer_learning_error_analysis\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`预训练 backbone + 冻结头 / 微调对照`

## 下一步建议

把 smoke 分数表替换成真实迁移学习训练日志，再补完整 backbone、类别级混淆矩阵与失败样本图库。


    ## 额外教师资产

    - `configs/transfer_protocol_template.json`：迁移学习正式协议模板
    - `artifacts/templates/training_log_template.csv`：真实训练日志模板
    - `artifacts/templates/class_error_gallery_template.md`：类别级误差图库模板
