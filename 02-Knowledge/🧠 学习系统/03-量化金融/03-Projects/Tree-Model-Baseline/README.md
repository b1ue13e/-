---
type: project
topic: "Week 8 树模型时间序列基线"
created: 2026-08-05
status: active
progress: 100%
tags: [项目, 量化金融, 树模型, 时间序列验证]
flow: project
source: "scikit-learn DecisionTreeRegressor；冻结时间切分"
---

# Week 8：树模型时间序列基线

本包将 [[树模型基线]] 从“集合不相交断言”升级为真实训练流程：训练集拟合、验证集选择树深、训练加验证重拟合、测试集一次性评价，并与均值预测比较。

## 数据契约

CSV 必须包含 `date,target` 以及至少一个以 `feature_` 开头的数值特征。特征必须在信号时点可得，`target` 必须位于未来；本包无法替你证明字段的经济可得时点。

## 运行

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python src/tree_baseline.py --output artifacts
```

真实 CSV：

```powershell
python src/tree_baseline.py --input path/to/features.csv --output artifacts --depths 2 3 4
```

输出 `artifacts/tree_metrics.json` 与 `artifacts/test_predictions.csv`。

## 完成标准

- [ ] 保存训练、验证、测试的日期边界，三者严格不相交。
- [ ] 树深只由验证集选择，测试集不得参与调参。
- [ ] 报告验证 MSE、测试 MSE、均值基线 MSE 和特征重要性。
- [ ] 改变测试目标后，所选深度与训练后模型结构不变。
- [ ] 不把演示数据上的非线性拟合写成真实 Alpha。

