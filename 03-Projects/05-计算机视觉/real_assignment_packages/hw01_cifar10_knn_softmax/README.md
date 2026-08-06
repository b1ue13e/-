# HW01 CIFAR-10 kNN 与 Softmax 基线 Real Assignment Package

这是一份面向学生自做的 `HW01` 真实作业包，不再只是说明页。

## 布置时机

U02 结束后，学生刚完成图像数据表示、线性分类和最小评测协议。

## 包内结构

- `starter/`：专题 starter、运行入口与数据检查脚本
- `baseline/`：baseline 记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `NumPy 向量化`
- `训练/验证/测试切分`
- `距离度量与线性分类`

## 教学目标

- 会在固定协议下组织 kNN 与 Softmax 基线
- 会做最小公平对照和失败样本审计
- 知道为什么 CNN 需要建立在稳定 baseline 之上

## 真实数据契约

预期真实数据目录：

`F:\-\03-Projects\data\computer_vision\hw01_cifar10_knn_softmax`

真实数据到位后，至少应包含：

- `cifar10.train.npz`
- `cifar10.val.npz`
- `label_map.json`

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `train.smoke.csv`
- `val.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\课程作业\05-计算机视觉\real_assignment_packages\hw01_cifar10_knn_softmax\starter\run.py" --input-dir "f:\-\03-Projects\data\computer_vision\hw01_cifar10_knn_softmax" --output-dir "f:\-\03-Projects\课程作业\05-计算机视觉\real_assignment_packages\hw01_cifar10_knn_softmax\your_outputs"
python "f:\-\03-Projects\课程作业\05-计算机视觉\real_assignment_packages\hw01_cifar10_knn_softmax\starter\check_data.py" --input-dir "f:\-\03-Projects\data\computer_vision\hw01_cifar10_knn_softmax"
pytest "f:\-\03-Projects\课程作业\05-计算机视觉\real_assignment_packages\hw01_cifar10_knn_softmax\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`kNN + 线性 Softmax`

## 下一步建议

把 smoke 特征替换成真实 CIFAR-10 特征或图像张量，再补完整训练与误差分析。
