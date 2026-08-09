# 课程 Starter

本目录提供可运行的数据契约、时间切分、负采样、五个传统链接预测基线和评价指标。它负责消除环境与协议起步成本，不包含阶段报告、表示学习、消融或 Capstone 结论。

```powershell
python scripts/generate_course_data.py --output data/generated --seed 42
python starter/run_stage_baseline.py --stage 01 --data-dir data/generated --output artifacts/starter-stage01
python starter/run_stage_baseline.py --stage 02 --data-dir data/generated --output artifacts/starter-stage02
python starter/run_stage_baseline.py --stage 03 --data-dir data/generated --output artifacts/starter-stage03
python starter/run_stage_baseline.py --stage 05 --data-dir data/generated --output artifacts/starter-stage05
python starter/run_baseline.py --events data/generated/temporal_edges.csv --output artifacts/starter-synthetic
python -m pytest -q
```

真实数据轨道先运行 `scripts/fetch_public_network.py`，再把生成的 `temporal_edges.csv` 传给同一入口并显式添加 `--undirected`。`split_manifest.json`、`predictions.csv` 和 `metrics.json` 是后续阶段必须复用的协议证据。
