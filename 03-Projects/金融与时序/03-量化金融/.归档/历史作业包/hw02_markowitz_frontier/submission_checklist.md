# HW02 Submission Checklist

提交前，请逐项自查：

## 目录与文件

- [ ] `README` 已说明问题、方法、数据来源和运行方式
- [ ] `starter/` 保持可运行
- [ ] `tests/` 至少包含 smoke test
- [ ] `reports/` 中已填写正式报告
- [ ] `baseline/README.md` 已记录 baseline 和失败案例

## 数据与协议

- [ ] 真实数据目录包含 `asset_returns.daily.csv`
- [ ] 真实数据目录包含 `asset_metadata.csv`
- [ ] 已写清楚时间区间、切分方式和是否存在未来信息
- [ ] 已说明复权、采样、成本或发布日期口径

## 结果与解释

- [ ] 已给出 `等权 vs 最小方差 vs 切线组合` 的公平对照
- [ ] 已解释至少 2 个失败案例或不稳定现象
- [ ] 已说明本次结论的适用边界

## 最后检查

- [ ] 结果可以在新目录重新运行
- [ ] smoke test 通过
- [ ] 没有把 smoke 结果当正式结论
