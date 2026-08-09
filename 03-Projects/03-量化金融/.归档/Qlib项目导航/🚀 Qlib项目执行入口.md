---
type: index
topic: "Qlib 项目执行入口"
course: "量化金融"
created: 2026-08-06
status: active
flow: project
kind: moc
assessment_exempt: true
assessment_exempt_reason: "项目执行导航；知识与作业验收由课程阶段 MOC、作业文件和实验包承担。"
source: "Microsoft Qlib 官方仓库与本地作业包"
source_url: "https://github.com/microsoft/qlib"
accessed: 2026-08-06
license: "Qlib MIT；行情数据按来源单独核验"
tags: [索引, 项目, 量化金融, Qlib]
---
# Qlib 项目执行入口

本入口把知识学习、阶段作业和可运行实验包串成一条证据链。当前从 `K01` 和 `A01` 开始；任何 `smoke` 结果都不等同于策略有效。

## 执行顺序

1. [[🧩 Qlib 项目知识点—作业—验收路线图|知识点—作业—验收路线图]]：按 K01–K28 解锁。
2. [[00-Qlib项目总看板|项目总看板]]：记录当前 K、A 阶段和证据状态。
3. [[A01-数据协议与无泄漏审计|A01 数据协议与无泄漏审计]]：先冻结数据、时间和可得性协议。
4. `real_assignment_packages/`：运行对应实验包测试并保存报告，不提交受限数据或答案。
5. [[量化金融-大作业-Qlib因子研究与成本敏感回测|Qlib 因子研究大作业]]：完成 A01–A06 后进行综合验收。

## 运行边界

- 代码版本、数据 release、环境和随机种子必须写入报告。
- 未核验的行情许可写为 `unknown` 或 `blocked`，不得写成 `pass`。
- 结果同时报告 gross、net、基准、换手和成本；测试集不得用于选择。
