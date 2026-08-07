---
type: project
project_type: homework
course: "量化金融"
assignment_id: "QF-ST04-01"
assignment_level: stage
assignment_format: lab
stage_id: "04"
requires: ["[[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型]]"]
source_type: local_integration_task
source: "real_assignment_packages/hw13_almgren_chriss"
source_url: "[[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw13_almgren_chriss/README|HW13 可执行作业包]]"
license: "Repository-authored"
created: 2026-08-06
status: active
flow: project
tags: [作业, 量化金融]
---
# 量化金融-阶段作业-04-Almgren-Chriss最优执行

## 学习目标

完成 [[03-Projects/金融与时序/03-量化金融/real_assignment_packages/hw13_almgren_chriss/README|HW13 可执行作业包]]：实现风险中性与风险厌恶执行轨迹，分解临时/永久冲击和风险项；与 TWAP 比较成本分布，并对流动性、波动率和期限做敏感性分析。

## 任务边界

- 实现风险中性与风险厌恶的 Almgren–Chriss 轨迹，并与 TWAP 比较；不把简化冲击模型当作真实交易成本报价。
- 临时/永久冲击、风险厌恶、波动率、流动性和期限的单位必须在协议中固定。

## 提交产物

- 校验库存单调归零、单位和成本符号，运行基线与测试。
- 提交轨迹、成本-风险前沿、情景表和模型限制。评分：推导/实现 30，边界 20，对照 20，解释 20，可复现性 10。

## 验收标准

- 库存终点、轨迹单调性、成本符号和边界测试通过。
- 至少改变一个流动性/波动率/期限参数，并解释成本-风险前沿变化。

## 引导自检

- [ ] 先核对库存、时间和价格单位。
- [ ] 再与 TWAP 基线比较总成本与风险。
- [ ] 最后运行敏感性分析并记录模型失效边界。

## 运行证据与失败判定

- 提交单位表、库存轨迹、逐期交易量、临时/永久冲击成本、风险项和 TWAP 对照。
- 期末库存不为零、成交量为负、价格与波动单位混用或总成本分解不闭合时，判定为失败。
- 改变风险厌恶、波动率和冲击参数复跑，并明确在哪些参数区间模型不再可信。

## 最小复现工作流

1. 阅读作业包说明、数据卡与 Rubric，冻结股数、时间单位、波动率、临时/永久冲击、期限和风险厌恶。
2. 运行数据检查与 TWAP 基线，先用小网格手算库存递推和成本分解，再运行最优轨迹。
3. 保存每期交易量、剩余库存、期望成本、风险项和总目标值；库存守恒与期末清零必须自动断言。
4. 运行全部测试并记录命令、退出码和失败用例；不得通过改变单位或忽略冲击项制造更优结果。
5. 报告把模型推导、数值实现、基线比较、敏感性和失效边界分别映射到评分证据。

**最低通过判据**：库存守恒、期末清零和成本分解全部可复算；最优轨迹与 TWAP 在相同订单、期限和冲击模型下比较，并完整报告参数敏感性与失效区间。


