# HW01 Regression Real Assignment Package

这是一份面向学生自做的 `HW01 Regression` 作业包，不再只是说明页。

当前包内已经落地：

- `starter/`：数据读取、训练入口、推理入口的骨架
- `baseline/`：baseline 目标记录，不提供教师答案
- `tests/`：最小接口与提交格式检查
- `reports/`：学生报告模板
- `data_card.md`：数据契约与当前样例说明
- `feature_notes.md`：93 个特征的结构说明
- `rubric.md`：评分细则

## 目录结构

```text
hw01_regression/
├── README.md
├── data_card.md
├── feature_notes.md
├── rubric.md
├── starter/
│   ├── __init__.py
│   ├── dataset.py
│   ├── download_official_data.py
│   ├── model.py
│   ├── train.py
│   └── infer.py
├── baseline/
│   └── README.md
├── tests/
│   └── test_hw01_regression.py
└── reports/
    └── report_template.md
```

## 数据位置

当前作业包使用的本地数据路径：

- `F:\-\03-Projects\data\ml_hw01\covid.train.csv`
- `F:\-\03-Projects\data\ml_hw01\covid.test.csv`
- `F:\-\03-Projects\data\ml_hw01\sample_submission.csv`

说明：

- 当前默认文件已经切换为 `李宏毅 ML 2021 HW01` 官方真实数据：
  - `covid.train.csv`：2700 行，95 列
  - `covid.test.csv`：893 行，94 列
- 当前仓库同时保留了 `smoke` 备份数据，专门用于最小自动测试：
  - `covid.train.smoke.csv`
  - `covid.test.smoke.csv`
  - `sample_submission.smoke.csv`
- 官方下载来源使用课程公开 Google Drive 文件 ID：
  - train: `19CCyCgJrUxtvgZF53vnctJiOJ23T5mqF`
  - test: `1CE240jLm2npU-tdz81-oVKEF3T2yfT1O`

## 运行方式

### 1. 检查数据与启动 starter

```bash
python "F:\-\03-Projects\projects-ml\hw01_regression\starter\train.py" --train-csv "F:\-\03-Projects\data\ml_hw01\covid.train.csv" --output-dir "F:\-\03-Projects\projects-ml\hw01_regression\your_outputs" --valid-ratio 0.25 --seed 42
```

如果需要重新下载官方数据：

```bash
python "F:\-\03-Projects\projects-ml\hw01_regression\starter\download_official_data.py"
```

### 2. 生成提交模板

```bash
python "F:\-\03-Projects\projects-ml\hw01_regression\starter\infer.py" --test-csv "F:\-\03-Projects\data\ml_hw01\covid.test.csv" --checkpoint "F:\-\03-Projects\projects-ml\hw01_regression\your_outputs\checkpoint.pt" --output "F:\-\03-Projects\projects-ml\hw01_regression\your_outputs\pred.csv"
```

### 3. 跑测试

```bash
pytest "F:\-\03-Projects\projects-ml\hw01_regression\tests\test_hw01_regression.py"
```

## 目前 baseline 定位

- 本作业包不再附带教师实现。
- `baseline/README.md` 只记录目标和你的结果。
- 你需要自己完成：
  - 特征处理
  - 模型实现
  - 训练循环
  - checkpoint 保存
  - 提交文件生成

## 下一步建议

1. 先读 `feature_notes.md`
2. 自己做第一版 ridge 或 MLP
3. 把结果回填到 `baseline/README.md`
4. 用 `reports/report_template.md` 写实验记录
