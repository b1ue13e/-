# HW01 Feature Notes

## 总体结构

官方 `covid.train.csv` 的输入一共 `93` 个特征，目标列是最后一列 `tested_positive`。

输入可以理解成：

1. `40` 维州 one-hot
2. `Day 1` 的 `18` 个调查特征
3. `Day 2` 的 `18` 个调查特征
4. `Day 3` 的前 `17` 个调查特征

原因是：

- 训练集最后一列标签就是 `Day 3` 的 `tested_positive`
- 所以输入部分只保留 `Day 3` 的前 17 个特征，不再包含最后那个目标值

## 40 个州 one-hot

`AL, AK, AZ, AR, CA, CO, CT, FL, GA, ID, IL, IN, IA, KS, KY, LA, MD, MA, MI, MN, MS, MO, NE, NV, NJ, NM, NY, NC, OH, OK, OR, PA, RI, SC, TX, UT, VA, WA, WV, WI`

## 每日调查特征

每个完整日块包含下面 18 个特征：

`cli, ili, hh_cmnty_cli, nohh_cmnty_cli, wearing_mask, travel_outside_state, work_outside_home, shop, restaurant, spent_time, large_event, public_transit, anxious, depressed, felt_isolated, worried_become_ill, worried_finances, tested_positive`

## 对 HW01 最有用的理解

1. 这不是普通的“静态表格回归”，而是把连续 3 天信息拼成一个样本。
2. `Day 3` 的最后目标值不能当输入特征。
3. 如果你做特征选择，可以优先比较：
   - 只用 `Day 3` 的 17 个非目标特征
   - 用 `Day 2 + Day 3`
   - 用全部 `93` 个特征
4. 州 one-hot 可能带来明显增益，因为不同州的疫情基线差异很大。

## 可以继续做的特征实验

- 只保留 `Day 3` 特征
- 去掉州 one-hot 做对照
- 用相关系数筛一版特征
- 比较 `all features` vs `selected features`
