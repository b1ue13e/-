# HW01 Data Card

## 数据任务

- 任务类型：监督学习回归
- 目标：根据过去 3 天的结构化调查特征预测第 3 天 `tested_positive`
- 当前默认数据：`李宏毅 ML 2021 HW01 官方真实数据`

## 当前字段契约

### 训练集 `covid.train.csv`

| 字段 | 含义 | 类型 |
|:---|:---|:---|
| `id` | 样本编号 | 整数 |
| 第 1-93 列特征 | 40 个州 one-hot + 3 天调查特征拼接 | 浮点数 |
| 最后一列 `tested_positive` | 回归目标 | 浮点数 |

### 测试集 `covid.test.csv`

| 字段 | 含义 | 类型 |
|:---|:---|:---|
| `id` | 样本编号 | 整数 |
| 第 1-93 列特征 | 40 个州 one-hot + 3 天调查特征拼接 | 浮点数 |

### 提交文件 `sample_submission.csv`

| 字段 | 含义 |
|:---|:---|
| `id` | 样本编号 |
| `tested_positive` | 预测值 |

## 官方数据规模与结构

- 训练集：`2700` 行，`95` 列
- 测试集：`893` 行，`94` 列
- 训练集列结构：
  - `id`
  - `93` 个输入特征
  - 最后一列目标 `tested_positive`
- 测试集列结构：
  - `id`
  - `93` 个输入特征

## 当前本地双数据层

### 1. 默认真实数据

- `covid.train.csv`
- `covid.test.csv`
- `sample_submission.csv`

### 2. 最小测试数据

- `covid.train.smoke.csv`
- `covid.test.smoke.csv`
- `sample_submission.smoke.csv`

用途：

1. 真实数据负责 baseline 与正式实验
2. smoke 数据负责自动测试与最小回归校验

## 接入官方数据时必须保持不变的部分

1. 文件名：
   - `covid.train.csv`
   - `covid.test.csv`
   - `sample_submission.csv`
2. `id` 字段存在
3. 训练集最后一列是 `tested_positive`
4. 测试集不带目标列
5. 提交文件列名为 `id,tested_positive`

## 已知限制

- 当前 baseline 只是最小 ridge baseline，不代表课程 strong baseline。
- 代码目前按列位置读取真实 CSV，是为了兼容官方重复列名字段。
- smoke 数据只能验证流程，不能替代真实实验结论。
