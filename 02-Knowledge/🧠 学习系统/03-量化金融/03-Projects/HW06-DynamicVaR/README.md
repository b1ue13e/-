---
type: project
topic: "HW06 动态 VaR 与覆盖率检验实验包"
created: 2026-08-05
status: active
progress: 100%
tags: [项目, 量化金融, HW06, VaR]
flow: project
source: "滚动参数法与历史模拟 VaR；Kupiec 无条件覆盖检验"
---

# HW06：动态 VaR 与覆盖率检验实验包

本包提供两个严格滞后的动态风险基线：滚动正态参数法 VaR 与滚动历史模拟 VaR，并在冻结测试期执行 Kupiec 无条件覆盖检验。

## 口径

- 输入收益率使用小数：`-0.02` 表示亏损 `2%`。
- VaR 输出为正的损失阈值；当 `-return > VaR` 时记为一次违约。
- 每个测试日的预测只使用该日前 `window` 个收益率。
- Kupiec 只检验违约比例，不检验违约是否聚集，也不证明尾部模型完全正确。

## 运行

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python src/dynamic_var.py --output artifacts --confidence 0.99 --window 60
```

真实 CSV 必须包含 `date,return`：

```powershell
python src/dynamic_var.py --input path/to/returns.csv --output artifacts
```

输出 `artifacts/var_metrics.json` 与 `artifacts/var_forecasts.csv`。

## 完成标准

- [ ] 手算一组参数法 VaR，解释置信水平、持有期和收益单位。
- [ ] 验证测试期首个预测只使用训练期末尾窗口。
- [ ] 报告两种方法的违约次数、违约率、Kupiec LR 与 p 值。
- [ ] 解释“未拒绝覆盖率”不等于模型准确，更不等于资产安全。

