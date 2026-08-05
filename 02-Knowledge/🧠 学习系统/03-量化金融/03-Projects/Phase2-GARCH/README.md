---
type: project
topic: "Phase 2 GARCH 波动率预测实验包"
created: 2026-08-05
status: active
progress: 100%
tags: [项目, 量化金融, GARCH, 波动率]
flow: project
source: "GARCH(1,1) Gaussian quasi-maximum likelihood；课程 Phase 2 规格"
---

# Phase 2：GARCH 波动率预测实验包

本包把 [[量化金融-波动率-GARCH家族模型]] 落成可运行的纵向实验：确定性模拟数据、GARCH(1,1) 极大似然估计、冻结时间切分、一步样本外预测、滚动方差基线和 QLIKE 比较。

## 口径

- 收益率使用**百分数单位**：`1.0` 表示 `1%`，不是 `100%`。
- 演示数据来自已知参数的 GARCH 过程，只用于验证实现，不代表 AAPL。
- 测试集只用于最终逐步预测；每次预测仅使用此前已经观察到的收益。
- 若 CSV 提供 `date` 列，输出会保留测试日期；否则使用 `observation_index`。
- 均值方程为常数均值，均值只在训练切分上估计；优化失败会阻断 JSON/CSV 产物写入。
- QLIKE 越低越好，但单个样本上的优势不证明模型在真实市场稳定有效。

## 环境与测试

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

测试覆盖：参数约束、条件方差为正、未来数据不改写训练估计、样本外预测长度与产物生成。

## 运行演示

```powershell
python src/garch_lab.py --output artifacts --seed 42
```

输出：

- `artifacts/phase2_metrics.json`
- `artifacts/phase2_forecasts.csv`

## 使用自己的收益率 CSV

CSV 必须包含 `return` 列，并使用百分数单位：

```powershell
python src/garch_lab.py --input path/to/returns.csv --output artifacts --train-fraction 0.8 --rolling-window 20
```

真实数据报告还必须记录标的、收益口径、复权定义、样本区间和异常值处理。

## 完成标准

- [ ] 全部测试通过，优化器报告成功收敛。
- [ ] 写出 $\sigma_t^2=\omega+\alpha\epsilon_{t-1}^2+\beta\sigma_{t-1}^2$，并解释三个参数。
- [ ] 验证 $\omega>0$、$\alpha,\beta\ge0$、$\alpha+\beta<1$。
- [ ] 只报告冻结测试集的 GARCH 与滚动方差 QLIKE。
- [ ] 保存一个失败案例，例如把小数收益误当成百分数或反之。
- [ ] 不把模拟数据结果写成 AAPL 实证结论。
