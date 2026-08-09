---
type: study
topic: "Python建模与数据切分"
course: "30-应用回归分析"
created: 2026-08-09
updated: 2026-08-09
status: ongoing
stage_moc: "[[🧭 应用回归分析-前置知识]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: [Python, 数据切分, 数据泄漏]
upstream: ["[[应用回归分析-概率统计与矩阵最小前置]]"]
source: "scikit-learn 1.8.0 本地运行接口"
source_url: "https://scikit-learn.org/stable/"
accessed: 2026-08-09
license: "BSD-3-Clause（包元数据待复核）"
tags: [学习, 应用回归分析, 前置知识, Python]
---

# 应用回归分析：Python 建模与数据切分

## 本课程需要什么

你需要能固定随机种子、区分训练集和测试集、把预处理放进 `Pipeline`，并保存可复现指标。复杂软件工程不属于本卡范围。

## 无泄漏原则

测试集代表尚未发生的未来数据。任何从数据估计的步骤，包括均值、标准差、缺失值填补、特征选择和超参数选择，都不得提前看到测试集。交叉验证时，这些步骤还必须在每个训练折内部重新拟合。

```python
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = Pipeline([
    ("scale", StandardScaler()),
    ("regressor", Ridge(alpha=1.0)),
])
model.fit(X_train, y_train)
prediction = model.predict(X_test)
rmse = root_mean_squared_error(y_test, prediction)
assert rmse > 0
print(f"test_rmse={rmse:.3f}")
```

## 实验协议

1. 先冻结问题定义、目标变量和主指标。
2. 划分训练集与测试集；测试集封存。
3. 在训练集内部交叉验证和选择超参数。
4. 固定最终方案后，在测试集上评价一次。
5. 保存环境版本、随机种子、数据来源和失败结果。

## 输入、输出与调试

进入建模前先检查四类契约：

- **形状**：`X` 必须是二维的样本乘特征矩阵，`y` 的长度与样本数一致。
- **索引**：切分后训练与测试索引不得相交；特征与目标索引必须对齐。
- **类型**：数值列、类别列和日期列必须显式识别，不能依赖偶然的字符串转数值。
- **输出**：至少保存模型身份、随机种子、训练/测试行数、主指标和逐样本预测。

遇到结果异常时按以下顺序排查：先确认目标定义和切分索引，再检查 Pipeline 中的步骤，最后检查模型参数。不要一看到分数差就扩大参数搜索；很多失败来自目标泄漏、索引错位或单位错误。

## 最小变式实验

1. 把随机种子从 42 改为 43，记录测试样本和 RMSE 如何变化。
2. 保持种子 42，分别运行带标准化和不带标准化的 Ridge。
3. 打印训练与测试索引交集，断言其为空。
4. 故意在全数据上拟合标准化器，画出错误数据流，再改回 Pipeline。

变式实验的目标不是找到更好分数，而是确认你能观察到协议改变带来的后果。

## 常见错误

- 在切分前对全数据标准化。
- 反复查看测试集并据此选择模型。
- 只报告最好的一次随机切分。
- 把训练 $R^2$ 当成泛化能力。

## 闭卷验收

- 改写一段“全量标准化后再 CV”的错误代码，使预处理进入 `Pipeline`。
- 解释验证集、交叉验证折和最终测试集各自承担什么职责。
- 连续运行上面的示例两次，确认相同随机种子得到相同 RMSE。

通过标准：三项均完成，且能在不看笔记的情况下画出“原始数据 → 训练/测试切分 → 训练折内预处理 → 模型选择 → 一次测试评价”的数据流。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
