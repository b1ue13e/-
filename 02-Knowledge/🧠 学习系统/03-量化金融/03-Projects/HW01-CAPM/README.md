---
type: project
topic: "HW01 CAPM 与 Alpha 检验实验包"
created: 2026-08-05
status: active
progress: 100%
tags: [项目, 量化金融, HW01, CAPM]
flow: project
source: "CAPM 单因子 OLS；课程 HW01 规格"
---

# HW01：CAPM 与 Alpha 检验实验包

本包将资产超额收益对市场超额收益的 OLS 回归落成可复现基线。它不把显著 Alpha 当作盈利保证，也不替代作业说明书中的闭卷矩阵推导。

## 数据契约

CSV 至少包含：`date, asset_return, market_return`。收益必须使用同一频率和同一现金流口径；`date` 若提供，必须唯一、升序。

## 运行

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python src/capm_lab.py --output artifacts
```

演示模式生成固定种子的合成收益；真实 CSV 使用：

```powershell
python src/capm_lab.py --input path/to/returns.csv --output artifacts --train-fraction 0.8
```

输出 `artifacts/metrics.json` 和 `artifacts/test_predictions.csv`。模型只在训练切分拟合，测试切分只用于最终评价。

## 完成标准

- [ ] 闭卷写出 $R_i-R_f=\alpha+\beta(R_m-R_f)+\epsilon$ 与矩阵 OLS 解。
- [ ] 报告 Alpha、Beta、标准误、t 值、$R^2$ 和测试 MSE。
- [ ] 与“训练集平均收益”基线比较，不能只报告模型自身结果。
- [ ] 解释市场代理、无风险利率、样本区间和统计显著性的边界。

