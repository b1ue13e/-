---
title: "量化金融-实战起航-本地环境配置与依赖(requirements)"
type: study
topic: "环境配置"
created: "2026-08-04"
status: active
difficulty: beginner
stage: "Level 0"
tags: [学习, 量化金融, 环境配置, Python]
nav_level: 2
nav_prev: "量化金融-启蒙-主观交易与量化交易的本质区别"
nav_next: "数据排雷指南：复权、生存者偏差与未来函数"
---


# 💻 量化实战起航：本地环境配置与依赖 (Dependency Hell 防坑指南)

## 0. 先判断它值不值得深挖
- **类别**：**A+ 类（基建必读）**
- **判断理由**：如果你直接复制本知识库里的 `arch` 或 `statsmodels` 代码到本地裸 Python 环境运行，你只会收获满屏红色的 `ModuleNotFoundError`。这是所有新手的“环境配置地狱”。

## 1. 为什么我们需要独立的环境？
在量化金融实战中，不同的模型依赖不同版本的库（例如 `yfinance` 接口经常变动，`arch` 库对 numpy 版本有要求）。
如果你不建立虚拟环境（Virtual Environment），你的电脑很快就会变成一个互相冲突的垃圾场。

## 2. 核心依赖清单 (requirements.txt)
> 请在你的项目根目录下，新建一个 `requirements.txt` 文件，并将以下内容复制进去：

```text
# 核心数据科学库
pandas>=1.5.0
numpy>=1.22.0
scipy>=1.9.0

# 绘图与可视化
matplotlib>=3.6.0
seaborn>=0.12.0

# 量化金融专门库
yfinance>=0.2.18      # 雅虎财经数据下载（回测基石）
arch>=5.3.0           # GARCH 波动率模型专用库
statsmodels>=0.13.5   # OLS回归、CAPM、Fama-French建模
scikit-learn>=1.2.0   # 机器学习基座

# 开发与交互环境
jupyterlab>=3.5.0     # 强烈建议使用 Jupyter 运行代码
notebook>=6.5.2
```

## 3. 一键安装指南 (Cheat Sheet)

### 步骤 A：创建虚拟环境 (强烈建议使用 Conda)
打开终端 (Terminal 或 Anaconda Prompt)，执行：
```bash
conda create -n quant_env python=3.10
conda activate quant_env
```

### 步骤 B：批量安装所有依赖
确保你在终端中已经进入了包含 `requirements.txt` 的文件夹，然后执行：
```bash
pip install -r requirements.txt
```

### 步骤 C：启动实验室
```bash
jupyter lab
```
*当浏览器自动弹开，看到左侧的文件目录时，恭喜你，你已经拥有了和华尔街量化研究员一样的初级火器装备！现在可以去复制《均线策略》或《GARCH模型》里的代码，按下 `Shift+Enter` 尽情开火了。*
\n

---
> 🧭 **自动导航 (Dataview Engine)**

```dataview
TABLE WITHOUT ID 
  "⬅️ [[" + nav_prev + "]]" AS "上一课", 
  "🏠 [[🗺️ 量化金融全栈终极框架 (Academic + AFML + HFT)|回到主干]]" AS "主菜单", 
  "➡️ [[" + nav_next + "]]" AS "下一课"
WHERE file.path = this.file.path
```
