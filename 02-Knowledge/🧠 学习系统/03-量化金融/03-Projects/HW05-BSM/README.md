---
type: project
topic: "HW05 Black-Scholes 与动态对冲实验包"
created: 2026-08-05
status: active
progress: 100%
tags: [项目, 量化金融, HW05, Black-Scholes]
flow: project
source: "Black-Scholes 基准公式；课程内 HW05 规格"
---

# HW05：Black-Scholes 与动态对冲实验包

本包对应 [[[支线任务] HW05-BSM期权定价与对冲]]，提供可复现的数值基线，不包含市场数据，也不声称 Black–Scholes 假设在真实市场成立。

## 环境

```powershell
python -m pip install -r requirements.txt
```

依赖：Python 3.10+、NumPy、SciPy。

## 测试

```powershell
python -m unittest discover -s tests -v
```

测试覆盖：

- 数值锚点 $d_2=-0.326551$ 与看涨价格；
- 看涨-看跌平价；
- 看涨价格对波动率的单调性；
- 对偶采样蒙特卡洛按“每对反变量 payoff 的均值”计算标准误，并落在统计误差范围内；
- 加入交易成本后，复制组合平均对冲误差变差。

## 生成实验产物

```powershell
python src/bsm_lab.py --output artifacts --paths 50000 --hedge-paths 10000 --hedge-steps 52 --seed 42
```

输出 `artifacts/metrics.json`，记录闭式价格、蒙特卡洛标准误和离散对冲误差。固定种子只用于复现，正式报告必须补充多种子敏感性分析。

## 完成标准

- [ ] 全部测试通过。
- [ ] 闭卷推导 Delta 对冲到 PDE，不只会调用函数。
- [ ] 报告蒙特卡洛估计、标准误和与闭式解的偏差。
- [ ] 比较至少两种调仓频率与一种交易成本。
- [ ] 说明常数波动率、连续交易、无跳跃和欧式行权边界。
