---
type: project
topic: "时间序列 Capstone 评分示例与失败案例"
course: "时间序列分析"
created: 2026-08-05
updated: 2026-08-05
status: completed
progress: 100%
flow: project
kind: example
tags: [项目, 时间序列, Capstone, 评分样例, 失败案例]
source_lesson: "[[L09-滚动预测与模型评估]]"
---

# Capstone｜评分示例与失败案例

> 本页是教学样例，不是用户真实业务结论。优秀案例使用固定种子的合成月度数据，代码已于 2026-08-05 实际运行；数值只用于演示报告证据链。

## A. 合格案例：季节序列一步滚动预测

### 1. 任务契约

| 字段 | 冻结值 |
|---|---|
| 预测对象 | 合成月度需求，单位：件 |
| 预测原点 | 每月结束后，已获得当月完整值 |
| horizon | 1 个月 |
| 主要指标 | MAE；RMSE 为辅助 |
| 区间 | 80% 与 95% |
| 基线 | last-value naïve、seasonal naïve($m=12$) |
| 候选 | AutoReg，lags=[1,12]，线性趋势 |
| 验证 | 起点 132–179，共 48 个 expanding-window 预测 |

### 2. 数据生成

$$y_t=50+0.04t+4\sin(2\pi t/12)+\varepsilon_t,
\qquad \varepsilon_t\sim N(0,1.2^2).$$

固定随机种子 `20260805`，总长度 180。这里公开生成机制，是为了让教学结果可复核；真实项目不能因为“知道答案”而跳过诊断。

### 3. 可复现实验

```python
import numpy as np
from statsmodels.tsa.ar_model import AutoReg

rng = np.random.default_rng(20260805)
n = 180
t = np.arange(n)
y = 50 + 0.04 * t + 4 * np.sin(2 * np.pi * t / 12) + rng.normal(0, 1.2, n)
start = 132

truth, seasonal, last, ar = [], [], [], []
lo80, hi80, lo95, hi95 = [], [], [], []

for origin in range(start, n):
    train = y[:origin]
    fit = AutoReg(train, lags=[1, 12], trend="ct", old_names=False).fit()
    prediction = fit.get_prediction(start=origin, end=origin, dynamic=False)

    truth.append(y[origin])
    seasonal.append(y[origin - 12])
    last.append(y[origin - 1])
    ar.append(float(prediction.predicted_mean[0]))

    ci80 = np.asarray(prediction.conf_int(alpha=0.20))[0]
    ci95 = np.asarray(prediction.conf_int(alpha=0.05))[0]
    lo80.append(ci80[0]); hi80.append(ci80[1])
    lo95.append(ci95[0]); hi95.append(ci95[1])

truth = np.asarray(truth)
def metrics(pred):
    pred = np.asarray(pred)
    return np.mean(np.abs(truth - pred)), np.sqrt(np.mean((truth - pred) ** 2))

print("seasonal", metrics(seasonal))
print("ar", metrics(ar))
print("last", metrics(last))
print("80 coverage/width", np.mean((truth >= lo80) & (truth <= hi80)), np.mean(np.asarray(hi80) - lo80))
print("95 coverage/width", np.mean((truth >= lo95) & (truth <= hi95)), np.mean(np.asarray(hi95) - lo95))
```

### 4. 已验证输出

| 模型 | MAE | RMSE |
|---|---:|---:|
| seasonal naïve | 1.613 | 2.001 |
| AutoReg(1,12)+trend | **1.344** | **1.713** |
| last-value naïve | 1.732 | 2.234 |

| 区间 | 经验覆盖率 | 平均宽度 |
|---|---:|---:|
| 80% | 83.3% | 4.076 |
| 95% | 93.8% | 6.234 |

AutoReg 相对 seasonal naïve 的 MAE 改善约 16.7%。该结论只适用于固定生成机制、一步预测和这 48 个起点；不能外推到真实销售、多步 horizon 或结构突变。

### 4.1 多 horizon 扩展

为了公平比较 $h=1,3,6$，下面让三个 horizon 使用同一组 43 个预测原点，并将原点步进固定为 1。每个 horizon 单独统计点误差与区间校准。

```python
import numpy as np
from statsmodels.tsa.ar_model import AutoReg

rng = np.random.default_rng(20260805)
n = 180
t = np.arange(n)
y = 50 + 0.04 * t + 4 * np.sin(2 * np.pi * t / 12) + rng.normal(0, 1.2, n)
start = 132
horizons = (1, 3, 6)
records = {
    h: {name: [] for name in (
        "truth", "seasonal", "last", "ar", "lo80", "hi80", "lo95", "hi95"
    )}
    for h in horizons
}

for origin in range(start, n - max(horizons) + 1):
    train = y[:origin]
    fit = AutoReg(train, lags=[1, 12], trend="ct", old_names=False).fit()
    prediction = fit.get_prediction(
        start=origin, end=origin + max(horizons) - 1, dynamic=False
    )
    means = np.asarray(prediction.predicted_mean)
    ci80 = np.asarray(prediction.conf_int(alpha=0.20))
    ci95 = np.asarray(prediction.conf_int(alpha=0.05))

    for h in horizons:
        idx = origin + h - 1
        r = records[h]
        r["truth"].append(y[idx])
        r["seasonal"].append(y[idx - 12])
        r["last"].append(y[origin - 1])
        r["ar"].append(means[h - 1])
        r["lo80"].append(ci80[h - 1, 0]); r["hi80"].append(ci80[h - 1, 1])
        r["lo95"].append(ci95[h - 1, 0]); r["hi95"].append(ci95[h - 1, 1])

for h in horizons:
    r = {name: np.asarray(values) for name, values in records[h].items()}
    print("h", h, "origins", len(r["truth"]))
    for name in ("seasonal", "ar", "last"):
        error = r["truth"] - r[name]
        print(name, f"MAE={np.mean(np.abs(error)):.3f}",
              f"RMSE={np.sqrt(np.mean(error ** 2)):.3f}")
    for level in ("80", "95"):
        lo, hi = r["lo" + level], r["hi" + level]
        coverage = np.mean((r["truth"] >= lo) & (r["truth"] <= hi))
        print(level, f"coverage={100 * coverage:.1f}%",
              f"width={np.mean(hi - lo):.3f}")
```

| horizon | 模型 | MAE | RMSE |
|---:|---|---:|---:|
| 1 | seasonal naïve | 1.588 | 1.998 |
| 1 | AutoReg(1,12)+trend | **1.356** | **1.728** |
| 1 | last-value naïve | 1.735 | 2.259 |
| 3 | seasonal naïve | 1.587 | 2.001 |
| 3 | AutoReg(1,12)+trend | **1.316** | **1.684** |
| 3 | last-value naïve | 3.917 | 4.421 |
| 6 | seasonal naïve | 1.673 | 2.074 |
| 6 | AutoReg(1,12)+trend | **1.381** | **1.751** |
| 6 | last-value naïve | 5.450 | 6.212 |

| horizon | 80% 覆盖率 / 宽度 | 95% 覆盖率 / 宽度 |
|---:|---:|---:|
| 1 | 86.0% / 4.079 | 93.0% / 6.238 |
| 3 | 81.4% / 4.175 | 93.0% / 6.385 |
| 6 | 79.1% / 4.175 | 93.0% / 6.386 |

这里 AutoReg 在三个 horizon 都优于两条基线，但这是合成机制下的结果。last-value 基线随 horizon 变差，说明基线也必须与业务 horizon 匹配；区间覆盖率则要与名义水平、宽度和有限原点数一起解释。

### 5. 失败窗口

AutoReg 绝对误差最大的三个零基索引为 158、139、147。合成数据没有业务事件可调查，因此只能报告为随机创新极端值；真实项目必须回到时间线核实异常、制度变化与数据问题。

### 6. Rubric 评分：88/100

| 维度 | 得分 | 扣分原因 |
|---|---:|---|
| 数据、环境与复现 | 19/20 | 未锁定完整包版本文件 |
| 方法正确性 | 23/25 | 未展示参数/根与残差四联图 |
| 基线与公平比较 | 20/20 | 两个朴素基线、相同起点 |
| 评估、消融与误差 | 18/20 | 已比较 $h=1,3,6$，但未比较固定 rolling window 或跨折校准 |
| 报告与边界 | 8/15 | 合成数据无业务决策和真实失败机制 |

**结论**：方法闭环合格，可作为代码与表格格式参考；不能直接作为真实 Capstone 提交。

## B. 失败案例：分数漂亮但协议无效

### 提交摘要

1. 对全量数据插值、标准化并生成居中滚动均值；
2. 随机 80/20 切分；
3. 只训练 Transformer 与 LSTM；
4. 根据测试集挑选窗口、horizon 和最优随机种子；
5. 只报告最优测试 RMSE，不提供 naïve 基线；
6. 删除三个最大误差窗口后重新计算；
7. 用注意力权重声称促销“导致”销量增长。

### 一票否决

| 错误 | 为什么结果无效 | 最小修复 |
|---|---|---|
| 全样本预处理 | 未来分布进入训练 | 每个滚动窗口内拟合 |
| 居中滚动均值 | 使用未来邻域 | 只用预测原点前 trailing window |
| 随机切分 | 训练看到未来状态 | 按时间滚动起点 |
| 反复看测试调参 | 测试成为验证集 | 重新封存未见测试段 |
| 无朴素基线 | 无法判断复杂度价值 | 加 naïve/seasonal naïve |
| 删除失败窗口 | 系统性低估风险 | 保留并调查 |
| 注意力作因果 | 预测关联不等于因果 | 删除因果表述或另做识别设计 |

### Rubric 评分：24/100，不通过

- 数据、环境与复现：4/20
- 方法正确性：5/25
- 基线与公平比较：0/20
- 评估、消融与误差：3/20
- 报告与边界：12/15

即使提交者声称 RMSE 很低，也不记录该数值，因为评估协议已经泄漏，分数没有可解释性。修复后必须从未被查看的新测试段重新评估。

## 使用出口

- 作业规范：[[HW09-滚动预测与完整建模报告]]
- 教师答案：[[HW01-HW09-参考答案与错误诊断#HW09｜滚动预测与完整建模报告]]
- 实现项目：[[项目-时间序列预测与漂移监控]]
