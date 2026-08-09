# 社交网络挖掘课程项目

本目录是课程作业、合成数据、运行入口和验收证据的唯一项目源。知识卡位于 `02-Knowledge/🧠 学习系统/01-社交网络挖掘/`。

## 环境

- Python 3.11+
- 普通 CPU 即可运行课程 fixture 与 smoke test
- 基础依赖见 `requirements.txt`

```powershell
python -m pip install -r requirements.txt
```

## 首次运行

```powershell
python scripts/generate_course_data.py --output data/generated --seed 42
python scripts/course_smoke.py --output artifacts/preflight
python starter/run_baseline.py --events data/generated/temporal_edges.csv --output artifacts/starter-synthetic
python -m pytest -q
```

预期结果：

- `data/generated/generation_manifest.json` 记录种子、文件哈希和行数；
- `artifacts/preflight/smoke_report.json` 记录 Python、NumPy、NetworkX 版本和图不变量；
- `artifacts/starter-synthetic/` 包含真实可运行的切分 manifest、传统基线预测和指标；
- 测试验证生成确定性、无标签泄漏、时间切分、传统基线、阶段 oracle、Markdown 契约和全部知识卡代码。

## Capstone 真实数据

合成 fixture 只用于协议预检。正式 Capstone 必须运行 SocioPatterns High School 2013 真实数据轨道：

```powershell
python scripts/fetch_public_network.py --output data/external/high-school-2013
python starter/run_baseline.py --events data/external/high-school-2013/temporal_edges.csv --undirected --output artifacts/starter-real
```

下载脚本固定官方 SHA-256，并生成包含 `CC BY-NC-SA 3.0`、引用、匿名化和语义边界的 manifest。

## 学习顺序

1. 从知识库的 `🗺️ 社交网络挖掘学习路径.md` 进入。
2. 完成前置诊断与 `课后作业/SNA-L00`。
3. 每阶段先完成知识卡中的手算、渐隐练习和闭卷检索，再完成同 `stage_id` 的阶段综合作业。
4. 阶段 4 冻结的 split 必须被阶段 6 和 Capstone 复用。
5. 学习者实现统一放入 `submission/`，运行产物放入 `artifacts/`；不要修改生成器伪造作业结果。

## 目录职责

| 路径 | 职责 |
| :--- | :--- |
| `课后作业/` | 前置诊断与环境自检；阶段形成性练习保留在知识卡内 |
| `阶段作业/` | 多知识点综合实验 |
| `大作业/` | 跨阶段 Capstone |
| `scripts/` | 数据 fixture 和课程 smoke test |
| `starter/` | 可运行的阶段 oracle、数据契约、时间切分和链接预测基线 |
| `tests/` | 课程提供代码的回归测试 |
| `data/generated/` | 可删除并重建的合成数据 |
| `data/external/` | 本地下载的真实数据；不得提交上游压缩包 |
| `submission/` | 学习者自己的代码、推导和报告 |
| `artifacts/` | 运行日志、表格、图片和校验结果 |
| `质量审计/` | 重构执行清单和唯一严苛审计 |

## 复现规则

- 所有命令从本目录执行，不使用本机绝对路径。
- 数据或协议改变时生成新的 manifest，不覆盖旧证据。
- 正式结果必须保留全部随机种子和失败运行。
- 正式 Capstone 依赖必做真实数据；外部下载失败时只能完成合成预检，不能宣布课程完成。
- 任何额外数据扩展都必须记录 URL、访问日期、许可和 SHA-256。
