---
type: project
topic: "Quant-Factor-And-Arbitrage-Engine"
created: 2026-07-28
updated: 2026-08-01
status: active
progress: 3%
flow: project
kind: project
domain: quant-finance
focus: now
sprint_id: 2026-S01-quant
tags: [项目, PoW, 量化金融, Qlib, 因子研究]
---

# Quant-Factor-And-Arbitrage-Engine

## 项目目标

建立一条可复现、无前视、含成本、样本外可解释的因子研究与回测工作流。复杂模型必须与朴素基线使用相同数据、区间、成本和组合规则。

## 当前真实状态

| 项目 | 状态 |
|:---|:---:|
| 官方 Qlib 工具链烟雾测试 | completed |
| K01–K06 | not started / current K01 |
| A01 数据协议 | active |
| A02–A06 | locked |
| 自己的 E0/E1/E2 公平对照 | not started |
| HW17 总验收 | locked |

> 烟雾测试退出码为 0 只证明工具链可用，不代表知识、基线或研究结论已经完成。

## 核心交付

1. 可复现协议：代码 commit、环境、数据 release、切分。
2. 公平基线：E0 等权/指数、E1 简单因子、E2 Qlib LightGBM。
3. 成本敏感回测：gross/net、换手、回撤、基准对照。
4. 无泄漏与失败审计：时间协议、偏差清单、失败案例和未知项。
5. 复现报告：新目录可重跑，结论边界清楚。

## 导航

- [[🚀 Qlib项目执行入口|Qlib 项目执行入口]]
- [[00-Qlib项目总看板|项目总看板]]
- [[A01-数据协议与无泄漏审计|A01 数据协议与无泄漏审计]]
- [[🧩 Qlib 项目知识点—作业—验收路线图|知识点—作业—验收路线图]]
- [[量化金融-大作业-Qlib因子研究与成本敏感回测|综合作业规格]]
