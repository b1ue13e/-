---
type: study
topic: "Python 与表格数据最小桥接"
course: "时间序列分析"
created: 2026-08-06
status: ongoing
stage_moc: "[[🧭 阶段0-前置知识]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["Python 基础", "表格数据"]
source: "Python 3 tutorial; pandas Getting Started tutorials"
source_url: "https://docs.python.org/3/tutorial/; https://pandas.pydata.org/docs/getting_started/intro_tutorials/"
accessed: 2026-08-06
license: "Python 文档 PSF License；pandas 文档许可边界以官方页面为准，本地仅保存最小原创桥接说明。"
tags: [学习, 时间序列分析, 前置知识, Python]
---

# 时间序列分析｜Python 与表格数据最小桥接

## 本课程需要什么

只要求你能运行 Python 文件、读取一张小表、查看列和缺失值，并理解“一行是一条观测、一列是一个变量”。本卡不讲完整 Python 语法、面向对象或软件工程。

## 最小规则

- `list` 保存有顺序的值；`dict` 保存键值对；`DataFrame` 是带行列标签的二维表。
- `df["value"]` 选择一列；`df.loc[...]` 按标签选择；`df.iloc[...]` 按位置选择。
- `isna()` 标记缺失；`sort_values()` 排序；不要在看见异常时直接删除，先说明业务含义。
- 脚本应包含固定输入、明确输出和断言，避免只在 Notebook 的隐藏状态下运行。

## 最小可运行例子

依赖：Python 3、`pandas`。

```python
from io import StringIO
import pandas as pd

raw = StringIO("""date,value
2025-02-01,12
2025-01-01,10
2025-03-01,
""")

frame = pd.read_csv(raw, parse_dates=["date"])
frame = frame.sort_values("date")

assert list(frame.columns) == ["date", "value"]
assert frame["date"].is_monotonic_increasing
assert int(frame["value"].isna().sum()) == 1
print(frame)
```

预期：日期按一月至三月排列，三月的 `value` 是缺失值；三条断言通过。

## 常见错误

1. 把字符串日期直接按字面处理，却没有验证解析结果。
2. 用 `dropna()` 静默删除缺失期，使时间间隔发生变化。
3. 修改表格后不检查行数、列名和排序。
4. 只保存输出截图，不保存生成输出的代码与环境版本。

## 与本课程的连接

完成本卡后，你应能运行[[时间序列分析-描述统计与相关性最小桥接]]中的小例子，并为[[L00-环境与时间索引]]准备一张可信表格。

## 检索练习与通过标准

- [ ] 不看笔记说出 `loc` 与 `iloc` 的区别。
- [ ] 独立读取 3 行 CSV，完成日期解析、排序和缺失计数。
- [ ] 给脚本增加“日期唯一”的断言，并构造一个使断言失败的重复日期例子。

三项都能独立完成，才算通过。

## 下游与作业

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
