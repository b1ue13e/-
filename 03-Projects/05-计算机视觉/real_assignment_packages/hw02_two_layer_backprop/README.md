# HW02 两层网络与反向传播正确性验证 Real Assignment Package

这是一份面向学生自做的 `HW02` 真实作业包，不再只是说明页。

## 布置时机

U03 前半段，学生已完成线性基线并学完反向传播、梯度检查和小样本过拟合。

## 包内结构

- `starter/`：专题 starter、运行入口与数据检查脚本
- `baseline/`：baseline 记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `链式法则与计算图`
- `数值梯度与解析梯度`
- `小样本过拟合测试`

## 教学目标

- 会独立实现两层网络前向和反向传播
- 会做梯度检查和过拟合烟雾测试
- 能区分实现错误、协议错误和调参问题

## 真实数据契约

预期真实数据目录：

`F:\-\03-Projects\data\computer_vision\hw02_two_layer_backprop`

真实数据到位后，至少应包含：

- `cifar10_subset.train.npz`
- `cifar10_subset.val.npz`
- `network_config.json`

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `tiny_batch.smoke.csv`
- `overfit_batch.smoke.csv`

## 运行方式

```bash
python "F:\-\03-Projects\05-计算机视觉\real_assignment_packages\hw02_two_layer_backprop\starter\run.py" --input-dir "F:\-\03-Projects\data\computer_vision\hw02_two_layer_backprop" --output-dir "F:\-\03-Projects\05-计算机视觉\real_assignment_packages\hw02_two_layer_backprop\your_outputs"
python "F:\-\03-Projects\05-计算机视觉\real_assignment_packages\hw02_two_layer_backprop\starter\check_data.py" --input-dir "F:\-\03-Projects\data\computer_vision\hw02_two_layer_backprop"
pytest "F:\-\03-Projects\05-计算机视觉\real_assignment_packages\hw02_two_layer_backprop\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`两层全连接网络 + 梯度检查`

## 下一步建议

把 smoke batch 换成真实 CIFAR-10 小批量，再补完整网络训练与日志记录。
