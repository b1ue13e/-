# 图神经网络课程项目

这个项目目录是课程作业、Starter Code、测试和运行证据的唯一事实源。知识定义和学习顺序位于 `02-Knowledge/🧠 学习系统/23-图神经网络/`。

## 环境

已验证环境：Python 3.11.9、PyTorch 2.12.1+cpu、NetworkX 3.6.1、NumPy 2.4.6。主线不需要 CUDA、PyG 或外部下载。

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
python starter/run_assignment.py s01 --output artifacts/starter-s01 --epochs 40 --seeds 42
python starter/run_assignment.py s02 --output artifacts/starter-s02 --epochs 40 --seeds 7 42 2026
python starter/run_assignment.py s03 --output artifacts/starter-s03 --epochs 40 --seeds 7
python starter/run_assignment.py s04 --output artifacts/starter-s04
python reference/capstone/run.py --config reference/capstone/config.json --output artifacts/capstone-reference
python -m pytest -q reference/capstone/tests
```

精确复现本机已验证环境时使用 `requirements-lock.txt`；`requirements.txt` 保留兼容版本范围，供 CPU 环境安装。

## 交付结构

- `课后作业/`：前置诊断、图表示/随机游走、消息传递/GCN 手算；
- `阶段作业/`：节点嵌入与谱基线、三模型对照、自监督、结构扩展边界；
- `大作业/`：小图节点分类与消息传递消融；
- `reference/capstone/`：可执行 reference submission，用于验证 capstone 规格，不代表学习者提交；
- `submission/`：学习者自己的提交目录，不与 reference 共用路径；
- `starter/gnn_course/`：确定性 toy 图、MLP/GCN/GraphSAGE/GAT、batch 子图采样、split manifest 和训练套件；
- `starter/run_assignment.py`：S01-S04 的可运行 worked example，不代替学习者提交；
- `tests/`：数据契约、split、模型形状、排列等变性、训练更新和 Markdown 契约；
- `artifacts/starter-s01/` 至 `artifacts/starter-s04/`：四个阶段 worked example 的实际运行产物；
- `artifacts/capstone-reference/`：120 节点 contextual SBM 上的 26 次 reference 运行，含基线、模型对照、分层 batch fanout、深度 1/4 和特征消融。

## 证据边界

toy 图只有 12 个节点，标签与社区结构相关；它只用于快速验证 API 和形状。reference capstone 使用 120 节点、固定 split 的 contextual SBM，仍是 synthetic transductive 证据，不是 OGB/CS224W 成绩、inductive 泛化或真实业务结论。任何外部数据实验必须另建 manifest，记录数据版本、许可、官方 split/evaluator 和资源。

## Reference 结果边界

`artifacts/capstone-reference/summary.json` 记录了 26 次运行。当前 reference 中，label propagation 在这份合成图上达到 `1.0` test accuracy，GCN depth 4 也达到 `1.0`；这不是模型排名结论，而是课程要求学习者保留并解释“复杂模型没有稳定赢”的证据。所有结果都只支持当前数据生成过程、split、seed 和训练预算。

## 从哪里开始

先打开 [[图神经网络-课后作业-00-前置诊断与环境自检]]，通过后再按课程学习路径推进。作业总览：[[03-Projects/23-图神经网络/🧭 课程作业总索引]]。
