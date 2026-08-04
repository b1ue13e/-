# HW02 Classification 可运行作业包

这是李宏毅 `ML2021 HW02-1 Phoneme Classification` 的本地原创执行包。官方题目、Notebook 和数据保持 `link-only`；本目录只保存自行编写的训练框架、测试、实验记录与提交物。

## 学习目标

在 429 维声学特征上完成 39 类帧级音素分类，并形成完整闭环：

`数据审计 → 分层划分 → 标准化 → MLP baseline → checkpoint → 推理提交 → 混淆矩阵 → 错误分析`

## 目录

```text
hw02_classification/
├── README.md
├── data_card.md
├── rubric.md
├── requirements.txt
├── baseline/README.md
├── reports/report_template.md
├── starter/
│   ├── dataset.py
│   ├── model.py
│   ├── train.py
│   ├── infer.py
│   ├── make_smoke_data.py
│   └── download_official_data.py
└── tests/test_hw02_classification.py
```

## 1. 环境检查

```powershell
python -c "import numpy, torch; print(numpy.__version__, torch.__version__)"
```

## 2. 先跑 smoke 闭环

Smoke 数据与官方任务具有相同的 `429` 维输入和 `39` 类标签，但完全由本地随机生成，不是课程答案。

```powershell
python "03-Projects/projects-ml/hw02_classification/starter/make_smoke_data.py" `
  --output-dir "03-Projects/data/ml_hw02/smoke"

python "03-Projects/projects-ml/hw02_classification/starter/train.py" `
  --data-dir "03-Projects/data/ml_hw02/smoke" `
  --output-dir "03-Projects/projects-ml/hw02_classification/your_outputs/smoke" `
  --epochs 2 --hidden-dims 64 --device cpu

python "03-Projects/projects-ml/hw02_classification/starter/infer.py" `
  --data-dir "03-Projects/data/ml_hw02/smoke" `
  --checkpoint "03-Projects/projects-ml/hw02_classification/your_outputs/smoke/checkpoint.pt" `
  --output "03-Projects/projects-ml/hw02_classification/your_outputs/smoke/prediction.csv" `
  --device cpu
```

## 3. 获取官方数据

先只核验远端文件；不会下载约 355 MB 的压缩包：

```powershell
python "03-Projects/projects-ml/hw02_classification/starter/download_official_data.py" --check-only
```

确认后再下载并安全解压：

```powershell
python "03-Projects/projects-ml/hw02_classification/starter/download_official_data.py"
```

预期目录：

```text
03-Projects/data/ml_hw02/timit_11/
├── train_11.npy
├── train_label_11.npy
└── test_11.npy
```

这些 TIMIT 衍生数组不进入 Git，不得擅自再分发。

## 4. 训练真实 baseline

```powershell
python "03-Projects/projects-ml/hw02_classification/starter/train.py" `
  --data-dir "03-Projects/data/ml_hw02/timit_11" `
  --output-dir "03-Projects/projects-ml/hw02_classification/your_outputs/baseline" `
  --epochs 20 --batch-size 256 --hidden-dims 256,128
```

CPU 试跑可先限制样本量；该结果不能冒充完整 baseline：

```powershell
python "03-Projects/projects-ml/hw02_classification/starter/train.py" `
  --data-dir "03-Projects/data/ml_hw02/timit_11" `
  --output-dir "03-Projects/projects-ml/hw02_classification/your_outputs/pilot" `
  --epochs 1 --max-train-samples 20000 --device cpu
```

训练会生成：

- `checkpoint.pt`
- `metrics.json`
- `history.csv`
- `confusion_matrix.csv`

## 5. 生成提交文件

```powershell
python "03-Projects/projects-ml/hw02_classification/starter/infer.py" `
  --data-dir "03-Projects/data/ml_hw02/timit_11" `
  --checkpoint "03-Projects/projects-ml/hw02_classification/your_outputs/baseline/checkpoint.pt" `
  --output "03-Projects/projects-ml/hw02_classification/your_outputs/baseline/prediction.csv"
```

提交格式严格为：

```csv
Id,Class
0,7
1,12
```

## 6. 自动测试

```powershell
python -m pytest "03-Projects/projects-ml/hw02_classification/tests" -q
```

测试覆盖数据契约、分层切分、模型输出 shape、训练—checkpoint—推理闭环和提交格式。

### 本包验证状态（2026-08-01）

- Python 语法编译：通过；
- 自动测试：`3 passed`；
- 官方远端数据入口：HTTP 200，`372,407,869` bytes；
- 尚未下载约 3 GB 解压数据，也未运行全量 baseline，因此本页没有填写真实课程分数。

## 学术诚信边界

- 官方入口：[ga642381/ML2021-Spring HW02](https://github.com/ga642381/ML2021-Spring/tree/main/HW02)
- 不复制第三方解答或可直接提交的模型权重。
- baseline 数字必须由自己的环境实际运行后写入 `baseline/README.md`。
- 任何数据子集、超参数改动和失败实验都必须在报告中说明。
