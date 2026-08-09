---
type: study
topic: "Lasso回归与坐标下降"
course: "30-应用回归分析"
created: 2026-08-09
updated: 2026-08-09
status: ongoing
stage_moc: "[[🧭 阶段3-正则化非线性与广义模型]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: [Lasso, L1正则化, 坐标下降]
prerequisites: [岭回归, 标准化, 凸优化直觉]
related: [自变量选择, 岭回归]
upstream: ["[[岭迹分析]]"]
source: "ISLP Ch. 6：The Lasso"
source_url: "https://www.statlearning.com/"
accessed: 2026-08-09
license: "link-only；具体许可 [待验证]"
tags: [学习, 应用回归分析, 正则化]
---

# 应用回归分析：Lasso 回归与坐标下降

## 目标函数

Lasso 在平方损失上加入 L1 惩罚：

$$
\hat\beta_\lambda
=\arg\min_\beta
\left\{
\frac{1}{2n}\lVert y-X\beta\rVert_2^2
+\lambda\lVert\beta\rVert_1
\right\}.
$$

特征应在训练折内部标准化，截距通常不惩罚。L1 约束的尖角使部分系数可以恰好为零，但被选中不等于获得了无偏或因果解释。

## 软阈值与坐标下降

固定其余坐标，只更新第 $j$ 个系数。对标准化列，更新可写为

$$
\beta_j\leftarrow
\frac{S\left(\frac{1}{n}x_j^Tr_j,\lambda\right)}
{\frac{1}{n}x_j^Tx_j},
\qquad
S(z,\lambda)=\operatorname{sign}(z)\max(\lvert z\rvert-\lambda,0),
$$

其中 $r_j=y-\sum_{k\ne j}x_k\beta_k$。分子落入阈值区间时，系数直接变为零。

## 算法骨架

1. 在当前训练折内中心化响应并标准化特征。
2. 初始化系数和截距。
3. 依次更新每个坐标，维护部分残差。
4. 当目标函数变化或最大坐标变化小于容差时停止。
5. 用训练集内部 CV 选择 $\lambda$，再在测试集评价一次。

## 与 Ridge 的区别

| 问题 | Ridge | Lasso |
| :--- | :--- | :--- |
| 惩罚 | L2 | L1 |
| 典型结果 | 连续收缩 | 收缩并产生稀疏解 |
| 高相关特征 | 倾向共同保留 | 可能不稳定地选其中一个 |
| 主要风险 | 解释有偏 | 选择不稳定、选择后推断困难 |

## 最小验证代码

```python
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = Pipeline([
    ('scale', StandardScaler()),
    ('lasso', Lasso(max_iter=20000)),
])
search = GridSearchCV(
    model,
    {'lasso__alpha': np.logspace(-3, 2, 30)},
    scoring='neg_root_mean_squared_error',
    cv=5,
)
search.fit(X_train, y_train)
coef = search.best_estimator_.named_steps['lasso'].coef_
print(search.best_params_)
print('nonzero=', int(np.count_nonzero(coef)))
print('negative_test_rmse=', search.score(X_test, y_test))
```

## 常见错误

- 用测试集选择 $\lambda$。
- 在 CV 外标准化。
- 把一次切分中的非零变量当作稳定结论。
- 忽略高相关特征之间的选择替代性。
- 用 Lasso 选择后直接套普通 OLS p 值而不说明选择后推断问题。

## 闭卷验收

1. 写出软阈值算子并解释何时输出零。
2. 手算一次单坐标更新。
3. 用重复 CV 比较变量选择稳定性。
4. 说明 Lasso 稀疏性和科学可解释性之间的区别。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

