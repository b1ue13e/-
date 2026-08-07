# HW05 Pascal VOC 最小目标检测工程包 Real Assignment Package

这是一份面向学生自做的 `HW05` 真实作业包，不再只是说明页。

## 布置时机

U05 开始时，学生已完成分类与迁移学习分析，开始进入更完整的视觉工程协议。

## 包内结构

- `starter/`：专题 starter、运行入口与数据检查脚本
- `baseline/`：baseline 记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `边界框与 IoU`
- `NMS 与最小检测评测`
- `训练、评测与可视化入口组织`

## 教学目标

- 会搭建最小目标检测工程包
- 会在固定协议下完成训练、评测和可视化闭环
- 会分析错检、漏检与检测任务边界

## 真实数据契约

预期真实数据目录：

`F:\-\03-Projects\data\computer_vision\hw05_pascal_voc_detection_pkg`

真实数据到位后，至少应包含：

- `voc_annotations.train.json`
- `voc_annotations.val.json`
- `detection_config.json`
- `label_map.json`

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `train.smoke.csv`
- `val.smoke.csv`

## 运行方式

```bash
python "F:\-\03-Projects\05-计算机视觉\real_assignment_packages\hw05_pascal_voc_detection_pkg\starter\run.py" --input-dir "F:\-\03-Projects\data\computer_vision\hw05_pascal_voc_detection_pkg" --output-dir "F:\-\03-Projects\05-计算机视觉\real_assignment_packages\hw05_pascal_voc_detection_pkg\your_outputs"
python "F:\-\03-Projects\05-计算机视觉\real_assignment_packages\hw05_pascal_voc_detection_pkg\starter\check_data.py" --input-dir "F:\-\03-Projects\data\computer_vision\hw05_pascal_voc_detection_pkg"
pytest "F:\-\03-Projects\05-计算机视觉\real_assignment_packages\hw05_pascal_voc_detection_pkg\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`最小检测器 + IoU@0.5 评测`

## 下一步建议

把 smoke 标注替换成真实 Pascal VOC 子集，再补正式训练配置、日志导出与可视化产物。


    ## 额外教师资产

    - `configs/minimal_detector_config.json`：最小检测 smoke 配置
    - `configs/voc2007_tiny_subset.template.json`：真实 VOC 子集配置模板
    - `artifacts/templates/eval_export_template.csv`：评测导出表模板
    - `artifacts/templates/eval_export_readme.md`：评测导出字段说明
