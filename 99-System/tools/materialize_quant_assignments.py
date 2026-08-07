#!/usr/bin/env python3
"""Materialize canonical quant-finance assignment pages from package manifests."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
COURSE = ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统" / "03-量化金融"
PROJECT = ROOT / "03-Projects" / "金融与时序" / "03-量化金融"
PACKAGES = PROJECT / "real_assignment_packages"
SNAPSHOT = ROOT / ".recovery-hold" / "2026-08-06" / "quant-finance-comprehensive"


CONFIG = {
    "01": {"type": "课后作业", "stage": "01", "title": "CAPM与Alpha检验", "source_type": "local_integration_task", "sources": "QuantEcon Asset Pricing lectures；Georgia Tech ML4T 只作验收参照", "knowledge": ["01-夯实基础/收益率与对数收益率", "02-量化核心技能/CAPM 资本资产定价模型", "02-量化核心技能/相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)"], "lab": "validated_labs/HW01-CAPM"},
    "02": {"type": "课后作业", "stage": "01", "title": "马科维茨有效前沿", "source_type": "local_integration_task", "sources": "QuantEcon portfolio/asset-pricing materials；本地数值实现", "knowledge": ["01-夯实基础/马科维茨有效前沿", "02-量化核心技能/相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)"], "lab": None},
    "03": {"type": "课后作业", "stage": "01", "title": "Fama-MacBeth回归", "source_type": "local_integration_task", "sources": "公开资产定价教材与本地实现；精确课程题号 [待验证]", "knowledge": ["02-量化核心技能/Fama-MacBeth 两步回归法 (Fama-MacBeth Two-Step Regression)", "02-量化核心技能/Fama-French三因子模型"], "lab": None},
    "04": {"type": "课后作业", "stage": "01", "title": "Beneish-M-Score财报排雷", "source_type": "local_integration_task", "sources": "Beneish M-Score 公开论文线索与本地财务数据任务；数据许可按来源核验", "knowledge": ["01-夯实基础/三大财务报表钩稽关系 (Interrelationship of Financial Statements)", "02-量化核心技能/Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)"], "lab": None},
    "05": {"type": "课后作业", "stage": "02", "title": "Black-Scholes定价与对冲", "source_type": "local_integration_task", "sources": "MIT OCW 18.S096 PS8-PS9 主题；Hull 教材本地参考", "knowledge": ["04-深入精通/量化金融-随机过程-伊藤引理与随机微分方程", "02-量化核心技能/Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)", "02-量化核心技能/期权希腊字母 (Option Greeks_ Delta, Gamma, Theta, Vega, Rho)"], "lab": "validated_labs/HW05-BSM"},
    "06": {"type": "课后作业", "stage": "02", "title": "GARCH波动率与动态VaR", "source_type": "local_integration_task", "sources": "MIT OCW 18.S096 PS4-PS5 主题；本地 GARCH/VaR 实验", "knowledge": ["02-量化核心技能/量化金融-波动率-GARCH家族模型", "02-量化核心技能/参数法VaR（方差-协方差法）", "02-量化核心技能/历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)"], "lab": "validated_labs/Phase2-GARCH"},
    "07": {"type": "课后作业", "stage": "02", "title": "非对称GARCH", "source_type": "local_integration_task", "sources": "公开 GARCH 教材与本地实现；精确课程题号 [待验证]", "knowledge": ["02-量化核心技能/非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)", "02-量化核心技能/量化金融-波动率-GARCH家族模型"], "lab": None},
    "08": {"type": "课后作业", "stage": "02", "title": "EVT尾部风险", "source_type": "local_integration_task", "sources": "公开 EVT 教材与本地风险任务；精确课程题号 [待验证]", "knowledge": ["02-量化核心技能/极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)", "02-量化核心技能/量化金融-风险管理-期望损失分解与ES理论"], "lab": None},
    "09": {"type": "阶段作业", "stage": "03", "title": "信息驱动采样", "source_type": "local_integration_task", "sources": "公开金融机器学习材料与本地采样引擎；来源许可 [待验证]", "knowledge": ["02-量化核心技能/Volume Bars与Dollar Bars信息驱动采样 (Information-Driven Bars)", "04-深入精通/金融微观结构采样棒 (Financial Data Bars_ Volume, Dollar & Imbalance Bars in AFML)"], "lab": None},
    "10": {"type": "阶段作业", "stage": "03", "title": "HRP资产配置", "source_type": "local_integration_task", "sources": "公开 HRP 方法材料与本地实现；来源许可 [待验证]", "knowledge": ["04-深入精通/HRP分层风险平价", "04-深入精通/Marchenko-Pastur定理", "02-量化核心技能/协方差去噪与随机矩阵理论 RMT (Covariance Denoising & Marchenko-Pastur Law in AFML)"], "lab": None},
    "11": {"type": "阶段作业", "stage": "03", "title": "协方差去噪", "source_type": "local_integration_task", "sources": "公开随机矩阵理论材料与本地实现；来源许可 [待验证]", "knowledge": ["04-深入精通/Marchenko-Pastur定理", "02-量化核心技能/协方差去噪与随机矩阵理论 RMT (Covariance Denoising & Marchenko-Pastur Law in AFML)"], "lab": None},
    "12": {"type": "阶段作业", "stage": "03", "title": "CPCV与PBO审计", "source_type": "local_integration_task", "sources": "公开金融机器学习验证材料与本地审计任务；来源许可 [待验证]", "knowledge": ["04-深入精通/Purged Group TimeSeries Cross-Validation 净化交叉验证 (Purged Group K-Fold CV)", "02-量化核心技能/PBO回测过拟合概率与Deflated Sharpe Ratio (Probability of Backtest Overfitting)", "02-量化核心技能/时间序列验证"], "lab": None},
    "13": {"type": "阶段作业", "stage": "04", "title": "Almgren-Chriss最优执行", "source_type": "local_integration_task", "sources": "Almgren-Chriss 方法公开论文线索与本地实现；再分发许可 [待验证]", "knowledge": ["04-深入精通/Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型", "04-深入精通/Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)"], "lab": None},
    "14": {"type": "阶段作业", "stage": "04", "title": "暗池与智能订单路由", "source_type": "local_integration_task", "sources": "公开市场微观结构材料与本地路由任务；数据许可 [待验证]", "knowledge": ["04-深入精通/量化金融-执行策略-暗池撮合与SOR智能路由", "02-量化核心技能/订单类型与交易所连续竞价撮合机制 (Order Types & Continuous Double Auction)"], "lab": None},
    "15": {"type": "阶段作业", "stage": "04", "title": "盘口队列与挂单概率", "source_type": "local_integration_task", "sources": "公开限价订单簿材料与本地队列仿真；数据许可 [待验证]", "knowledge": ["04-深入精通/跨市场排队优先权与挂单成交概率 (Queue Position & Fill Probability in High-Frequency Trading)", "04-深入精通/限价订单簿数据与 L1_L2_L3 盘口重建 (Limit Order Book Data & Reconstructing L1_L2_L3)"], "lab": None},
    "16": {"type": "阶段作业", "stage": "04", "title": "金融交易环境与PPO", "source_type": "open_source_project_task", "sources": "FinRL / Gymnasium 开源项目任务；具体 commit 与许可证见提交 manifest", "knowledge": ["04-深入精通/强化学习金融交易环境与 MDP 状态-动作空间设计 (Gym-Finance & MDP in Financial RL)", "02-量化核心技能/金融MDP设计与奖励函数工程 (Financial MDP & Reward Engineering)", "04-深入精通/风险约束下的RL"], "lab": None},
    "17": {"type": "大作业", "stage": "05", "title": "Qlib因子研究与成本敏感回测", "source_type": "open_source_project_task", "sources": "Microsoft Qlib 官方仓库与本地 A01-A06 集成任务", "knowledge": ["02-量化核心技能/Qlib回测工作流(Qlib Workflow)", "02-量化核心技能/样本泄漏", "02-量化核心技能/回测框架与无泄漏实验", "02-量化核心技能/策略评价指标"], "lab": "Qlib因子研究"},
}


def assignment_path(number: str, cfg: dict[str, object]) -> Path:
    kind = str(cfg["type"])
    title = str(cfg["title"])
    if kind == "课后作业":
        return PROJECT / kind / f"量化金融-课后作业-{number}-{title}.md"
    if kind == "阶段作业":
        return PROJECT / kind / f"量化金融-阶段作业-{cfg['stage']}-{title}.md"
    return PROJECT / kind / f"量化金融-大作业-{title}.md"


def wikilinks(items: list[str]) -> str:
    return "\n".join(f"- [[02-Knowledge/🧠 学习系统/03-量化金融/{item}|{Path(item).name}]]" for item in items)


def package_readme(number: str) -> str:
    package = next(PACKAGES.glob(f"hw{number}_*"))
    return (package / "README.md").read_text(encoding="utf-8-sig")


def render(number: str, cfg: dict[str, object]) -> str:
    package = next(PACKAGES.glob(f"hw{number}_*"))
    manifest = json.loads((package / "package_manifest.json").read_text(encoding="utf-8-sig"))
    source_url = {
        "16": "https://github.com/AI4Finance-Foundation/FinRL",
        "17": "https://github.com/microsoft/qlib",
    }.get(number, "[待验证]")
    license_name = {"16": "Apache-2.0（以固定 commit 为准）", "17": "MIT（Qlib 代码）"}.get(number, "[待验证]")
    package_link = f"03-Projects/金融与时序/03-量化金融/real_assignment_packages/{manifest['slug']}/README"
    lab = cfg.get("lab")
    lab_line = f"- **成熟实现/证据**：`03-Projects/金融与时序/03-量化金融/{lab}/`\n" if lab else ""
    return f'''---
type: project
topic: "{manifest['title']}"
course: "量化金融"
created: 2026-08-06
status: active
progress: 0%
tags: [项目, 量化金融, {cfg['type']}]
flow: project
kind: project
project_type: homework
homework_id: HW{number}
assignment_type: {cfg['type']}
source_type: {cfg['source_type']}
source_url: "{source_url}"
accessed: 2026-08-06
license: "{license_name}"
solution_visibility: private
---

# 量化金融-{cfg['type']}-{number}-{cfg['title']}

## 1. 作业身份与来源边界

- **所属阶段**：{manifest['stage']}。
- **来源贡献**：{cfg['sources']}。
- **本地改动**：把来源主题转成可复现的数据协议、基线、测试与报告任务；不复制官方答案。
- **成熟度**：当前 canonical 页面与配套包支持 smoke 验证；真实数据结论必须使用 `--mode real`、保存数据 manifest 并通过正式测试。

## 2. 学习目标

完成后，学习者应能：

1. 解释 `{manifest['title']}` 的问题、假设和适用边界；
2. 运行可复现基线并保存输入、参数、输出与失败案例；
3. 用专题指标而非单一收益数字判定方法是否成立；
4. 区分 smoke 工程证据与真实市场证据。

## 3. 所需知识

{wikilinks(list(cfg['knowledge']))}

允许使用 Python、NumPy、Pandas、SciPy、statsmodels、scikit-learn 及包内依赖；使用额外库必须锁定版本。禁止使用测试期调参、未来数据、未记录的手工清洗和可直接提交的第三方答案。

## 4. 任务背景与边界

以 `{manifest['baseline']}` 为最小对照。所有结论必须绑定数据版本、时间区间、频率、随机种子与执行成本。若真实数据或许可暂不可得，允许使用包内 smoke 数据完成工程自检，但报告标题和结论必须明确标为“smoke”，不得外推为市场实证。

## 5. 详细题目

### 题 1：协议冻结与失败样例

写出数据字典、输入/输出 schema、信息可得时间和禁止事项。构造至少一个必然失败输入，并证明测试能够拒绝它。

### 题 2：朴素基线

先运行 `{manifest['baseline']}`，保存参数、环境、运行命令和原始指标。不得在看到测试结果后修改切分边界。

### 题 3：专题实现

在包内 starter 基础上完成本专题核心算法；为关键公式、数值不变量或时间约束增加至少三个测试，其中至少一个为反例。

### 题 4：稳健性与边界

完成至少一项参数扰动、一项数据扰动和一个失败案例。解释哪些结论仍成立、哪些只对当前输入成立。

### 题 5：报告与复现

在干净输出目录重跑，生成 `summary.json`、专题产物、测试日志和 800-1500 字报告。报告必须区分 smoke、真实数据、样本内和样本外结果。

## 6. 环境与复现

- **Python**：3.11；依赖以包内代码导入和提交的 lock file 为准。
- **随机种子**：涉及随机算法时固定为 `42`，并报告多种子结果或解释为何不适用。
- **硬件**：默认 CPU；若使用 GPU，记录型号、显存和运行时间。
- **预计运行**：smoke 低于 1 分钟；真实模式范围由数据量决定，提交时记录实测时间。
- **入口**：[[{package_link}|HW{number} 配套代码包]]。
{lab_line}- **模式**：`python starter/run.py --mode smoke|real --input-dir <dir> --output-dir <dir>`。

## 7. 提交产物

- `README.md`：问题、数据、方法、运行命令和边界；
- `environment.txt` 或 lock file；
- `data_manifest.json`：来源、许可、校验值、时间区间和 schema；
- `src/` 或完成后的 `starter/`；
- `tests/`：正常、失败、边界测试；
- `artifacts/summary.json` 与专题产物；
- `failure_log.md`；
- `report.md`。

## 8. 验收标准与 Rubric

| 维度 | 分值 | 专题证据 |
| :--- | ---: | :--- |
| 数据、来源与复现 | 20 | manifest、许可边界、环境、命令和输入输出齐全 |
| 方法正确性 | 25 | 核心公式/算法与至少三个专题测试一致 |
| 基线与公平比较 | 20 | 先有朴素基线，切分、成本和样本完全同口径 |
| 稳健性与失败分析 | 20 | 参数/数据扰动、失败案例和边界解释齐全 |
| 报告与工程质量 | 15 | 产物可重跑、结论不过度外推、目录完整 |

**通过线**：总分不低于 75，且方法正确性不低于 18；正式模式缺数据 manifest、存在泄漏或核心测试失败时直接不通过。

## 9. 引导与自检

- 先预测 smoke 输出结构，再运行；输出异常时先检查 schema 和时间排序。
- 指标过好时优先检查泄漏、成本、重复样本和测试集调参。
- 无法复现时冻结解释器、输入校验值、随机种子和工作目录后逐项排查。
- 提交前确认报告没有把 smoke 结果、局部代码通过或单一好年份写成策略有效。

## 10. 知识反链与后续

- 本作业所需知识见第 3 节；对应阶段 MOC 将本页作为阶段出口。
- 完成后回到 [[03-Projects/金融与时序/03-量化金融/🧭 课程作业总索引|课程作业总索引]] 更新状态。
- HW01-HW08 进入阶段综合任务；HW09-HW16 为阶段综合任务；HW17 完成后进入 A01-A06 复现与答辩。
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.apply and not SNAPSHOT.exists():
        raise SystemExit(f"Missing recovery snapshot: {SNAPSHOT}")
    outputs = [(assignment_path(number, cfg), render(number, cfg)) for number, cfg in CONFIG.items()]
    conflicts = [path for path, _ in outputs if path.exists()]
    if conflicts and not args.apply:
        for path in conflicts:
            print(f"OVERWRITE\t{path.relative_to(ROOT)}")
    print(f"mode={'apply' if args.apply else 'dry-run'}")
    print(f"assignments={len(outputs)}")
    for path, _ in outputs:
        print(f"WRITE\t{path.relative_to(ROOT)}")
    if not args.apply:
        return 0
    for path, text in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
