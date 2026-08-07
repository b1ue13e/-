---
type: study
topic: OHLCV字段清洗与复权
created: '2026-04-17'
updated: 2026-08-01
status: planned
difficulty: intermediate
course: 量化金融
stage_moc: '[[🧭 阶段1-数据与收益基础]]'
note_role: concept
flow: knowledge
kind: concept
prerequisites:
- 收益率与对数收益率
- Python 基础
related:
- 时间索引与频率（量化）
- 样本泄漏
assessment_exempt: false
source: pandas 时间序列文档与 Qlib Data Layer 文档
source_url: https://qlib.readthedocs.io/en/stable/component/data.html
accessed: '2026-08-06'
license: link-only
concept:
- OHLCV字段清洗与复权
tags:
- 学习
- 量化金融
anki_deck: 量化金融::Qlib
anki_tags:
- quant
- K02
- verified_route
---

# OHLCV字段清洗与复权

> [!info] 主线导航
> [[🗺️ 量化金融学习路径|返回路径]] · **Week 1 / K02** · 上一张 [[收益率与对数收益率]] · 下一张 [[时间索引与频率（量化）]]

> **K02 目标**：不靠阅读完成度，而是通过定义、边界、反例和可运行断言证明掌握。

## 0. 先测再学

闭卷写出 OHLCV字段清洗与复权 的输入、输出、成立条件和一个失败案例。若无法写清，先完成本页示例，不并行开启下一个 K 点。

## 1. 定义、机制、假设与边界

OHLCV字段清洗与复权不是“把缺失值填满”，而是建立可审计的数据契约。定义中必须分开原始报价、复权序列、成交量单位和企业行为日期；机制上先检查唯一键、类型与交易日历，再依据供应商说明验证复权因子。关键假设是拆分、分红和停牌标记能够被追溯。边界是不同供应商的前复权、后复权命名可能相反。反例是把零成交量当缺失后前向填充，这会伪造可交易价格。

## 2. Worked example

```python
rows = [("A", "t1"), ("A", "t2"), ("A", "t2")]
keys = set(rows)
assert len(keys) != len(rows)
raw_return = 50 / 100 - 1
assert raw_return == -0.5  # 拆股反例，不能解释为财富损失
```

运行后必须保存输入、期望输出和实际输出。代码可执行只证明局部定义一致，不证明策略在样本外有效。

## 3. K02 最小作业

1. 用自己的数据重新构造上述最小示例，不直接复制数值。
2. 增加一个由本主题边界产生的失败案例，并确认断言确实失败。
3. 闭卷解释公式或机制，再与权威来源逐项核对。
4. 把代码、输出、失败日志和一句结论登记到 [[量化金融-阶段作业-01-数据协议与无泄漏基线]]。

## 4. 闭卷闸门

- [ ] 能用自己的话定义 OHLCV字段清洗与复权
- [ ] 能说明至少一个成立条件和一个失效边界
- [ ] 手算或人工推演与代码结果一致
- [ ] 失败案例能够被测试捕获
- [ ] 没有把局部代码通过夸大为策略有效

## 🃏 Anki 卡片

- K02｜OHLCV字段清洗与复权的核心判断是什么？ :: OHLCV字段清洗与复权不是“把缺失值填满”，而是建立可审计的数据契约。
- K02｜OHLCV字段清洗与复权最需要防范的反例是什么？ :: 反例是把零成交量当缺失后前向填充，这会伪造可交易价格。

<!-- quant-route-quality-v2 -->
## 5. 可定位来源

1. Microsoft Qlib Data Layer, Section Data Preparation and File Structure: https://qlib.readthedocs.io/en/stable/component/data.html
2. pandas Working with missing data, Section NA semantics: https://pandas.pydata.org/docs/user_guide/missing_data.html
3. pandas Duplicate Labels, Section Consequences of duplicate labels: https://pandas.pydata.org/docs/user_guide/duplicates.html

## 6. 知识连接

- [[收益率与对数收益率]]
- [[时间索引与频率（量化）]]
- [[策略回测前视偏差与生存者偏差防范审计 (Look-Ahead & Survivorship Bias Audit)]]
- [[🧭 阶段0-先修诊断与研究协议]]

---

<!-- quant-route-depth-v3 -->
## 决策规则：先守住可得时点，再处理价格连续性

**OHLCV 字段清洗与复权**的成立条件不是“没有缺失值”，而是每一列都能说明交易日历、币种、价格单位、停牌状态和当时可得时间。机制上，前复权便于画连续历史图，后复权便于从基期累计收益，但两者都不能直接替代真实成交价；成交量还要按拆并股比例反向调整。最小复现实验应任选一个发生分红或拆股的标的，分别用原始价、前复权价和现金分红重建单期收益，断言总回报一致。

反例是把供应商已回填的复权因子用于公告日前样本，或者把停牌日补成零收益并视为可交易。**OHLCV 字段清洗与复权**的验收门槛是：价格恒满足 `low <= open/close <= high`，成交量非负，复权事件前后总回报守恒，异常行进入隔离表而不是静默删除。

<!-- quant-route-reasoning-v4 -->
### 定义—推导—对比复核

**OHLCV字段清洗与复权** 的定义必须能落到数据列和时点，而不能只停留在术语。原始成交价、复权价格和总回报序列的区别决定了收益能否守恒；从公司行动现金流推导调整因子，而不是对跳空做经验平滑。因此，对 **OHLCV字段清洗与复权** 的误区检查要同时保留正例、破坏条件后的反例和样本外结果；只要三者不能形成同一因果链，就暂不判定掌握。


---

## 🎮 交互实验室 (HTML) 与 实战靶场 (Jupyter)

光看公式没用，跑通代码才是真的！利用下方组件进行交互或直接跑通实盘代码：

### 💻 实战靶场
- [打开 Notebook：02 第一个量化实验](https://github.com/datawhalechina/quant-for-beginners/blob/main/notebooks/phase1_intro/02_你的第一个量化实验.ipynb)（扩展材料，见 [[量化金融-外部实验资产索引]]）

## 适用条件与边界

- 复权价格适用于历史收益研究，不等于某个历史时点可成交的原始报价；成交回测必须同时保留调整口径和执行价格口径。
- `low <= open/close <= high`、成交量非负和交易日唯一性是最小数据契约；无法核验公司行动或停牌含义时，不得静默填充。

## 公式与符号

设原始价格为 $P_t$，调整因子为 $A_t$，复权价格可写为 $P_t^{adj}=A_tP_t$。`O/H/L/C/V` 分别表示开、高、低、收、量；$A_t$ 的来源、版本和生效日期必须写入 manifest。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```


- **需结合后续知识**：[[量化金融-阶段作业-01-数据协议与无泄漏基线|A01 数据协议与无泄漏审计]]，补齐可得时点与公告日边界。
- **提交产物**：字段字典、数据来源/版本、复权事件审计和失败样例。
