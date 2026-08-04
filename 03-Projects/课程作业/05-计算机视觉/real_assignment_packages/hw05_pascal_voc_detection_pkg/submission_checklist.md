# HW05 Submission Checklist

## 目录与文件

- [ ] `README.md` 已说明任务、数据、运行方式和结果
- [ ] `starter/` 保持可运行
- [ ] `tests/` 至少包含 smoke test
- [ ] `reports/` 中已填写正式报告
- [ ] `baseline/README.md` 已记录 baseline 和失败案例

## 数据与协议

- [ ] 真实数据目录包含 `voc_annotations.train.json`
- [ ] 真实数据目录包含 `voc_annotations.val.json`
- [ ] 真实数据目录包含 `detection_config.json`
- [ ] 真实数据目录包含 `label_map.json`
- [ ] 已写清楚切分方式、预处理与随机种子
- [ ] 已说明真实数据与 smoke 数据的边界

## 结果与解释

- [ ] 已给出 `最小检测器 + IoU@0.5 评测` 的最小对照
- [ ] 已解释至少 2 个失败案例或不稳定现象
- [ ] 已说明本次结论的适用边界
