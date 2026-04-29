---
type: index
topic: "PyTorch课程代码索引"
created: 2026-04-28
status: active
tags: [索引, 学习, 深度学习, PyTorch, 课程代码]
source: "E:/deeplearning"
---
# 📦 PyTorch课程代码索引

> 来源：`E:\deeplearning`
> 导入策略：保留 notebook、CSV、图片和小型运行数据；额外生成 JupyMD 兼容 Markdown；跳过重复 `.zip`、`.ipynb_checkpoints` 和大型预训练 `.pth` 权重。

---

## 📚 章节入口

| 章节 | 主题 | Obsidian / JupyMD 版 | 原 Notebook | 数据/说明 | 对应知识路径 |
|:---|:---|:---|:---|:---|:---|
| 第2章 | PyTorch 与数学基础 | [[课程代码-PyTorch实战/02-PyTorch与数学基础/深度学习第二章\|打开 Markdown]] | [[课程代码-PyTorch实战/02-PyTorch与数学基础/深度学习第二章.ipynb\|ipynb]] | 无外部数据 | [[09-高等代数/🗺️ 高等代数学习路径\|高等代数]] · [[28-数学分析/🗺️ 数学分析学习路径\|数学分析]] · [[05-计算机视觉/02-深度学习内核/PyTorchModule\|PyTorch Module]] |
| 第3章 | PyTorch 基本概念：张量、激活函数、损失函数、优化器 | [[课程代码-PyTorch实战/03-PyTorch基本概念/深度学习第三章\|打开 Markdown]] | [[课程代码-PyTorch实战/03-PyTorch基本概念/深度学习第三章.ipynb\|ipynb]] | `data/img1.jpeg` | [[05-计算机视觉/02-深度学习内核/激活函数CV\|激活函数]] · [[05-计算机视觉/02-深度学习内核/MSE损失\|MSE损失]] · [[05-计算机视觉/02-深度学习内核/交叉熵损失\|交叉熵损失]] · [[05-计算机视觉/02-深度学习内核/PyTorchOptimizer\|PyTorch Optimizer]] |
| 第4章 | 深度神经网络：MLP、CNN、RNN/LSTM/GRU、股票趋势预测 | [[课程代码-PyTorch实战/04-PyTorch深度神经网络/深度学习第四章\|打开 Markdown]] | [[课程代码-PyTorch实战/04-PyTorch深度神经网络/深度学习第四章.ipynb\|ipynb]] | [[课程代码-PyTorch实战/04-PyTorch深度神经网络/大模型权重说明\|大模型权重说明]] | [[05-计算机视觉/02-深度学习内核/MLP\|MLP]] · [[05-计算机视觉/02-深度学习内核/ResNet\|ResNet]] · [[08-NLP全栈/03-深度学习NLP基础/RNN结构\|RNN]] · [[02-时间序列分析/05-机器学习与深度学习进阶/LSTM与GRU\|LSTM与GRU]] |
| 第5章 | PyTorch 数值建模：回归、聚类、PCA、交叉验证 | [[课程代码-PyTorch实战/05-PyTorch数值建模/深度学习第五章\|打开 Markdown]] | [[课程代码-PyTorch实战/05-PyTorch数值建模/深度学习第五章.ipynb\|ipynb]] | `train.csv` / `test.csv` / `plant.csv` / `region.csv` | [[17-机器学习/02-线性模型/线性回归\|线性回归]] · [[17-机器学习/05-其他方法/原型聚类\|K-Means/原型聚类]] · [[17-机器学习/05-其他方法/主成分分析\|PCA主成分分析]] · [[17-机器学习/01-基础概念/数据集划分与交叉验证\|交叉验证]] |

---

## 🧭 推荐学习顺序

1. 先走 [[../🎭 深度学习总入口\|深度学习总入口]] 的“最短主线”。
2. 用第2章补 PyTorch 数学操作和自动求导前置。
3. 用第3章补张量、激活、损失、优化器。
4. 用第4章把 MLP / CNN / RNN / LSTM / GRU 串起来。
5. 用第5章把深度学习工具接回回归、聚类、PCA、交叉验证等经典机器学习任务。

---

## ⚠️ 关于运行方式

这些 Markdown 保留普通 `python` 代码块，供 JupyMD 使用本地 Python 解释器运行。

- 请在 JupyMD 设置中把 `Python interpreter` 指向本地 Python。
- 该 Python 环境需要安装 `torch` / `torchvision` / `jupytext` / `matplotlib` 等依赖。
- 如果要完整复现实验：仍建议打开对应原 `.ipynb`，用 Jupyter / JupyterLab 运行。

## 🧪 运行环境提示

这些 notebook 主要依赖：

- `torch`
- `torchvision`
- `numpy`
- `pandas`
- `matplotlib`
- `scikit-learn`
- `tqdm`
- `kmeans_pytorch`（第五章聚类部分可能需要）

如果只是阅读，不需要安装环境；如果要运行，建议在单独虚拟环境中打开 notebook。

---

## 📦 导入清单

| 类型 | 处理方式 |
|:---|:---|
| `.ipynb` | 已导入第2-5章主 notebook，并生成同名 `.md` 兼容版 |
| 图片 / CSV / 输出图片 | 已按章节复制到对应 `data/` / `assets/` 目录 |
| `lstm.pth` | 体积小，已随第四章数据保留 |
| 大型预训练 `.pth` | 未复制，见 [[课程代码-PyTorch实战/04-PyTorch深度神经网络/大模型权重说明\|大模型权重说明]] |
| `.zip` | 未复制，源目录已有解压版本，避免重复 |
| `.ipynb_checkpoints` | 未复制，避免 Jupyter 缓存污染知识库 |

---

## 🔗 回到入口

- [[../🎭 深度学习总入口\|🎭 深度学习总入口]]
- [[../🎓 学习入口\|🎓 学习入口]]