---
type: project
topic: "AAPL Capstone Phase 1"
created: 2026-08-05
status: active
progress: 100%
tags: [项目, 量化金融, Capstone, 基线]
flow: project
source: "本地确定性演示数据或用户提供的公开行情 CSV"
---

# AAPL Capstone Phase 1：无泄漏基线

这是 [[Capstone-统一标的贯穿实战项目|AAPL 贯穿式项目]] 的第一个可执行切片。它验证数据契约、信号滞后、交易成本、最大回撤和产物保存，不声称演示数据具有投资意义。

## 环境

- Python 3.10+
- `numpy`
- `pandas`

```powershell
python -m pip install -r requirements.txt
```

## 运行测试

```powershell
python -m unittest discover -s tests -v
```

测试覆盖：正常运行、重复日期拒绝、未来价格不改写过去结果、持仓严格滞后信号。

## 运行演示基线

```powershell
python src/phase1_baseline.py --output artifacts
```

演示模式生成固定价格序列，输出：

- `artifacts/metrics.json`
- `artifacts/equity_curve.csv`

## 使用自己的 CSV

CSV 必须包含 `date,adj_close`，日期唯一且严格升序，价格为正且无缺失：

```powershell
python src/phase1_baseline.py --input path/to/aapl.csv --output artifacts --fast-window 20 --slow-window 60 --cost-bps 10
```

使用真实数据时，在报告中记录数据提供方、下载时间、查询参数、复权定义与研究区间。脚本不会静默排序或填充错误数据。

## 通过标准

- [ ] 全部测试通过。
- [ ] 能解释为何持仓使用上一期信号。
- [ ] 能说明演示数据与真实 AAPL 结论的区别。
- [ ] `metrics.json` 中的成本参数与报告一致。
