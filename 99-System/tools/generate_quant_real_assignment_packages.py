from __future__ import annotations

import csv
import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(r"f:\-")
PACKAGES_ROOT = ROOT / "03-Projects" / "金融与时序" / "03-量化金融" / "real_assignment_packages"
DATA_ROOT = ROOT / "03-Projects" / "data" / "quant_finance"
GENERATED_AT = "2026-07-31"


PACKAGES = [
    {
        "id": "HW01",
        "slug": "hw01_capm_alpha_beta",
        "title": "CAPM 资产定价与单股 Alpha/Beta 归因",
        "stage": "第一阶段：资产定价与财务量化",
        "timing": "U02 结束后，学生刚完成收益率、超额收益、基准与 CAPM 回归。",
        "prerequisites": ["收益率与对数收益率", "无风险资产与资本市场线", "CAPM 资本资产定价模型"],
        "goals": ["会做单资产 CAPM 回归", "会解释 alpha、beta 与基准", "能做滚动 Beta 基础扩展"],
        "real_files": ["prices.daily.csv", "benchmark.daily.csv", "risk_free.daily.csv"],
        "smoke_files": ["prices.smoke.csv", "benchmark.smoke.csv", "risk_free.smoke.csv"],
        "baseline": "单资产 CAPM + 滚动 Beta",
        "sources": ["Yahoo Finance 或 Stooq 日线价格", "FRED 无风险利率", "Tushare/AKShare 本地替代"],
        "questions": ["你的 alpha 与 beta 分别在说什么？", "滚动 Beta 为什么会变化？", "如果 benchmark 换掉，结论会变化吗？"],
        "next_step": "把 smoke 数据替换成真实市场数据，再补 CAPM 回归和滚动窗口实现。",
    },
    {
        "id": "HW02",
        "slug": "hw02_markowitz_frontier",
        "title": "马科维茨均值-方差有效前沿",
        "stage": "第一阶段：资产定价与财务量化",
        "timing": "U03 结束后，作为第一阶段压舱石作业。",
        "prerequisites": ["收益率与对数收益率", "相关系数、协方差与分散化", "马科维茨均值-方差模型"],
        "goals": ["会估计收益与协方差", "会画有效前沿", "能比较等权、最小方差与切线组合"],
        "real_files": ["asset_returns.daily.csv", "asset_metadata.csv"],
        "smoke_files": ["asset_returns.smoke.csv", "asset_metadata.smoke.csv"],
        "baseline": "等权 vs 最小方差 vs 切线组合",
        "sources": ["Yahoo Finance 多资产日线", "Fama-French 行业组合或 ETF 数据", "Wind/Tushare 本地替代"],
        "questions": ["为什么协方差矩阵决定了最优权重？", "样本内最优和样本外稳定有什么差别？", "为什么需要稳健约束？"],
        "next_step": "把 starter 扩展成真实优化器，并补充权重约束和样本外比较。",
    },
    {
        "id": "HW03",
        "slug": "hw03_fama_macbeth",
        "title": "Fama-MacBeth 跨期横截面风险溢价估计",
        "stage": "第一阶段：资产定价与财务量化",
        "timing": "U04 结束后，学生已经理解时间序列回归与横截面回归的差别。",
        "prerequisites": ["CAPM 资本资产定价模型", "APT 套利定价理论", "Fama-French 三因子模型", "Fama-MacBeth 两步回归法"],
        "goals": ["会做两步回归", "会估计风险溢价", "能谨慎解释统计显著性"],
        "real_files": ["asset_panel.monthly.csv", "factor_panel.monthly.csv"],
        "smoke_files": ["asset_panel.smoke.csv", "factor_panel.smoke.csv"],
        "baseline": "两步回归 + 风险溢价显著性",
        "sources": ["Ken French Data Library", "WRDS/CRSP 资产截面数据", "本地股票池月频收益面板"],
        "questions": ["因子暴露和风险溢价为什么不是同一个东西？", "显著性是否等于可交易性？", "稳健标准误会改写哪些结论？"],
        "next_step": "用真实月频面板替换 smoke 数据，并补足两步回归循环与稳健标准误。",
    },
    {
        "id": "HW04",
        "slug": "hw04_beneish_quality",
        "title": "Beneish M-Score 与财报排雷",
        "stage": "第一阶段：资产定价与财务量化",
        "timing": "U05 结束后，学生已经完成财务报表关系、利润质量和应计项直觉。",
        "prerequisites": ["三大财务报表关系", "ROE 拆解与杜邦分析", "利润表与利润质量", "Beneish M-Score 与 Sloan 应计项因子"],
        "goals": ["会从财报字段构造风险信号", "理解财报发布日期滞后", "能解释误判案例"],
        "real_files": ["financial_statement.panel.csv", "filing_calendar.csv"],
        "smoke_files": ["financial_statement.smoke.csv", "filing_calendar.smoke.csv"],
        "baseline": "Beneish M-Score + 简单质量分层",
        "sources": ["SEC/EDGAR", "巨潮资讯/交易所公告", "Tushare 财务数据"],
        "questions": ["PIT 为什么是这类作业的硬门槛？", "哪些公司会被模型误判？", "财报信号如何影响后续收益或回撤？"],
        "next_step": "把 starter 扩成真实财报字段映射，并加入发布日期过滤逻辑。",
    },
    {
        "id": "HW05",
        "slug": "hw05_black_scholes_hedging",
        "title": "Black-Scholes 定价与动态 Delta 对冲",
        "stage": "第二阶段：时间序列、期权与风控",
        "timing": "U06 结束后，学生已学完期权 payoff、BSM 与 Greeks。",
        "prerequisites": ["远期、期货与期权的区别", "二叉树期权定价模型", "Black-Scholes 期权定价模型", "期权 Greeks"],
        "goals": ["会实现 BSM 定价", "会做离散 Delta 对冲", "能解释对冲误差"],
        "real_files": ["underlying.daily.csv", "option_quotes.daily.csv", "risk_free.daily.csv"],
        "smoke_files": ["underlying.smoke.csv", "option_quotes.smoke.csv", "risk_free.smoke.csv"],
        "baseline": "BSM 闭式 + 离散 Delta 对冲",
        "sources": ["OptionMetrics 或交易所期权数据", "Yahoo Finance 期权链", "国债收益率曲线"],
        "questions": ["对冲误差来自哪里？", "波动率误设会怎样影响结果？", "为什么调仓越频繁也不一定越好？"],
        "next_step": "先把 smoke 路径替换成真实期权与标的行情，再补 Greeks 与对冲模块。",
    },
    {
        "id": "HW06",
        "slug": "hw06_garch_var",
        "title": "GARCH(1,1) 动态波动率与动态 VaR",
        "stage": "第二阶段：时间序列、期权与风控",
        "timing": "U07 结束后，作为第二阶段压舱石作业。",
        "prerequisites": ["收益率序列的风格化事实", "波动率聚集", "ARCH 效应", "GARCH 模型"],
        "goals": ["会拟合 GARCH", "会构造动态 VaR", "会做风险覆盖检验"],
        "real_files": ["returns.daily.csv"],
        "smoke_files": ["returns.smoke.csv"],
        "baseline": "GARCH 条件波动率 + VaR 覆盖检验",
        "sources": ["FRED、Yahoo Finance 或本地指数日线", "交易所指数收益序列"],
        "questions": ["为什么样本内拟合好看不够？", "VaR 命中率在说什么？", "如果分布假设变化，会怎样影响结论？"],
        "next_step": "在真实收益序列上补充 GARCH 拟合、VaR 回测和覆盖检验。",
    },
    {
        "id": "HW07",
        "slug": "hw07_asymmetric_garch",
        "title": "非对称 GARCH 与杠杆效应",
        "stage": "第二阶段：时间序列、期权与风控",
        "timing": "U08 前半段，学生已经做过一次标准 GARCH。",
        "prerequisites": ["GARCH 模型", "非对称 GARCH 模型与杠杆效应"],
        "goals": ["理解 EGARCH/GJR-GARCH 非对称结构", "会比较标准与非对称模型", "会解释新闻响应曲线"],
        "real_files": ["returns.daily.csv"],
        "smoke_files": ["returns.smoke.csv"],
        "baseline": "GARCH vs EGARCH/GJR-GARCH",
        "sources": ["股票指数收益率", "商品或汇率收益率"],
        "questions": ["为什么坏消息更容易放大波动？", "非对称模型比标准模型多解决了什么？", "何时非对称结构并不显著？"],
        "next_step": "在真实收益数据上补模型对照、参数解释和新闻响应曲线。",
    },
    {
        "id": "HW08",
        "slug": "hw08_evt_tail_risk",
        "title": "EVT 与尾部风险外推",
        "stage": "第二阶段：时间序列、期权与风控",
        "timing": "U08 后半段，学生已经体验过常规 VaR 的不足。",
        "prerequisites": ["历史模拟 VaR", "参数法 VaR", "尾部风险", "极值理论 EVT 与 POT 模型"],
        "goals": ["会做 POT/GPD 拟合", "会估计极端 VaR/ES", "会报告门槛敏感性"],
        "real_files": ["returns.daily.csv"],
        "smoke_files": ["returns.smoke.csv"],
        "baseline": "POT 阈值法 + 极端 VaR/ES",
        "sources": ["指数收益序列", "外汇或商品日频收益"],
        "questions": ["门槛为什么是这份作业最危险的自由度？", "极端样本少会如何影响结论？", "EVT 比普通 VaR 多了什么、少了什么？"],
        "next_step": "在真实收益序列上补阈值选择、GPD 拟合与敏感性分析。",
    },
    {
        "id": "HW09",
        "slug": "hw09_volume_dollar_bars",
        "title": "Volume Bars 与 Dollar Bars 采样",
        "stage": "第三阶段：金融 ML、因子与回测",
        "timing": "U09 结束后，作为进入研究工程层的第一份作业。",
        "prerequisites": ["OHLCV 字段清洗与复权", "订单簿数据", "金融微观结构采样棒"],
        "goals": ["会从 tick/成交数据构造 bars", "能比较不同采样方式下的统计性质", "建立数据采样意识"],
        "real_files": ["ticks.csv"],
        "smoke_files": ["ticks.smoke.csv"],
        "baseline": "Volume Bars + Dollar Bars 对照",
        "sources": ["Crypto 逐笔成交", "交易所逐笔样例", "自采 tick 数据"],
        "questions": ["为什么采样方式会改变结论？", "时间 bars 和 dollar bars 各自偏向什么？", "bars 质量如何影响后续标签？"],
        "next_step": "将 smoke tick 替换成真实逐笔数据，并补充 bars 构建与统计对照。",
    },
    {
        "id": "HW10",
        "slug": "hw10_hrp_allocation",
        "title": "HRP 分层风险平价",
        "stage": "第三阶段：金融 ML、因子与回测",
        "timing": "U10 结束后，学生已感受到协方差不稳定。",
        "prerequisites": ["马科维茨均值-方差模型", "相关系数、协方差与分散化", "分层风险平价组合 HRP"],
        "goals": ["会实现 HRP 三步流程", "会与 MPT、等权配置做公平对照", "能解释稳健性差异"],
        "real_files": ["asset_returns.daily.csv", "asset_metadata.csv"],
        "smoke_files": ["asset_returns.smoke.csv", "asset_metadata.smoke.csv"],
        "baseline": "HRP vs MPT vs 1/N",
        "sources": ["多资产 ETF 数据", "行业指数或国家 ETF 池"],
        "questions": ["为什么 HRP 不需要直接求逆？", "样本外稳健比样本内最优更重要吗？", "哪些市场环境下 HRP 也会失败？"],
        "next_step": "用真实多资产收益率补聚类、准对角化和样本外对照。",
    },
    {
        "id": "HW11",
        "slug": "hw11_covariance_denoising",
        "title": "协方差去噪与随机矩阵理论",
        "stage": "第三阶段：金融 ML、因子与回测",
        "timing": "U10-U11 之间，学生已经感受到高维噪声问题。",
        "prerequisites": ["相关系数、协方差与分散化", "协方差去噪与随机矩阵理论 RMT"],
        "goals": ["理解 MP 法则", "会做基础协方差去噪", "能比较去噪前后的配置差异"],
        "real_files": ["asset_returns.daily.csv"],
        "smoke_files": ["asset_returns.smoke.csv"],
        "baseline": "原始协方差 vs 去噪协方差",
        "sources": ["多股票横截面日频收益", "ETF/行业收益矩阵"],
        "questions": ["噪声主导的特征值意味着什么？", "去噪为什么可能有效，也为什么可能失败？", "去噪后最该看哪类样本外指标？"],
        "next_step": "把 smoke 矩阵替换成真实高维收益矩阵，并补谱分析与去噪流程。",
    },
    {
        "id": "HW12",
        "slug": "hw12_cpcv_pbo",
        "title": "CPCV 与 PBO 过拟合审计",
        "stage": "第三阶段：金融 ML、因子与回测",
        "timing": "U11 结束后，作为第三阶段压舱石作业。",
        "prerequisites": ["Purged Group TimeSeries Cross-Validation", "Meta-labeling", "组合过拟合概率 PBO"],
        "goals": ["会做 purging/embargo", "会做 CPCV 审计", "形成先审计再汇报收益的纪律"],
        "real_files": ["strategy_returns.daily.csv", "parameter_grid.csv"],
        "smoke_files": ["strategy_returns.smoke.csv", "parameter_grid.smoke.csv"],
        "baseline": "CPCV + PBO",
        "sources": ["既有策略回测结果", "参数网格实验记录", "自建研究日志导出"],
        "questions": ["为什么普通随机 CV 不适合金融时间序列？", "PBO 改写了你对哪些结果的看法？", "准入规则应该怎样写得更硬？"],
        "next_step": "接入真实策略结果，补时间块切分、purging/embargo 与 PBO 估计。",
    },
    {
        "id": "HW13",
        "slug": "hw13_almgren_chriss",
        "title": "Almgren-Chriss 最优执行",
        "stage": "第四阶段：高频交易与强化学习",
        "timing": "U13 开始，课程从做策略转向如何下单。",
        "prerequisites": ["买卖价差及其微观结构拆解", "市场冲击成本模型与平方根法则", "Implementation Shortfall", "Almgren-Chriss 最优执行轨迹推导"],
        "goals": ["理解成本-风险权衡", "会实现最优拆单轨迹", "能比较匀速执行与最优执行"],
        "real_files": ["parent_order.csv", "liquidity_profile.csv"],
        "smoke_files": ["parent_order.smoke.csv", "liquidity_profile.smoke.csv"],
        "baseline": "TWAP vs Almgren-Chriss",
        "sources": ["自定义 parent order 设定", "日内成交量曲线", "简化订单簿流动性数据"],
        "questions": ["风险厌恶参数如何改变轨迹？", "为什么最优执行不是无条件更便宜？", "流动性曲线不准会造成什么偏差？"],
        "next_step": "把 smoke 设定替换成真实流动性曲线，补执行成本与轨迹求解器。",
    },
    {
        "id": "HW14",
        "slug": "hw14_darkpool_sor",
        "title": "暗池与智能订单路由",
        "stage": "第四阶段：高频交易与强化学习",
        "timing": "U13-U14 之间，学生已经知道执行不是单市场问题。",
        "prerequisites": ["限价订单簿数据与 L1/L2/L3 盘口重建", "买卖价差及其微观结构拆解", "暗池交易与智能订单路由 SOR"],
        "goals": ["会设计简单多市场路由规则", "会把延迟和成交概率纳入执行分析", "理解交易场所异质性"],
        "real_files": ["venue_quotes.csv", "latency_profile.csv"],
        "smoke_files": ["venue_quotes.smoke.csv", "latency_profile.smoke.csv"],
        "baseline": "单市场执行 vs 多市场 SOR",
        "sources": ["多 venue 报价样例", "模拟延迟剖面", "自建 dark/lit 对照数据"],
        "questions": ["为什么路由不是简单选最优价？", "延迟对齐如何改变结果？", "暗池节省点差是否伴随其他代价？"],
        "next_step": "补充真实多 venue 数据或仿真数据，实现路由与延迟分析。",
    },
    {
        "id": "HW15",
        "slug": "hw15_queue_fill_probability",
        "title": "挂单成交概率与队列位置",
        "stage": "第四阶段：高频交易与强化学习",
        "timing": "U14 结束后，学生已经理解订单生命周期和价格优先时间优先。",
        "prerequisites": ["限价订单簿数据与 L1/L2/L3 盘口重建", "买卖价差及其微观结构拆解", "跨市场排队优先权与挂单成交概率"],
        "goals": ["会估计 fill probability", "会解释队列位置与撤单影响", "会比较挂单与吃单成本"],
        "real_files": ["lob_events.csv"],
        "smoke_files": ["lob_events.smoke.csv"],
        "baseline": "基础队列模型 + 成交概率估计",
        "sources": ["订单簿事件流", "盘口更新与成交消息", "仿真撮合日志"],
        "questions": ["为什么挂单不成交本身就是成本？", "撤单行为如何改变 fill probability？", "静态盘口截图为什么不够？"],
        "next_step": "把 smoke 事件流替换成真实盘口事件，并补队列位置与 fill probability 估计器。",
    },
    {
        "id": "HW16",
        "slug": "hw16_finrl_gymnasium",
        "title": "Gymnasium 金融交易环境与 PPO",
        "stage": "第四阶段：高频交易与强化学习",
        "timing": "U15 或 RL 专题启动单元，学生已经建立成本和风险意识。",
        "prerequisites": ["动态下注规模与凯利公式", "动态止损机制与风险平价仓位管理", "强化学习金融交易环境与 MDP 状态-动作空间设计"],
        "goals": ["会封装交易环境", "会设计状态、动作、奖励", "会把成本和风险写进环境"],
        "real_files": ["market_state.daily.csv"],
        "smoke_files": ["market_state.smoke.csv"],
        "baseline": "最小 Gymnasium 环境 + PPO 接口占位",
        "sources": ["标的历史行情", "自定义技术指标面板", "仓位和成本设定"],
        "questions": ["环境设计比模型名字更重要体现在哪里？", "奖励函数如何诱发坏行为？", "训练/评估切分为什么必须分开？"],
        "next_step": "先把环境接口做成最小可运行版本，再逐步加入奖励塑形和评估协议。",
    },
    {
        "id": "HW17",
        "slug": "hw17_qlib_factor_research",
        "title": "Qlib 因子研究与成本敏感回测",
        "stage": "第五阶段：Capstone / 开源工作流",
        "timing": "U15 之后，作为 Capstone 启动包。",
        "prerequisites": ["收益率与对数收益率", "时间序列数据处理", "策略评价指标", "Qlib 工作流与无泄漏审计"],
        "goals": ["会冻结 commit、环境和数据 release", "会搭建朴素 baseline 与 Qlib baseline", "会做含成本样本外回测"],
        "real_files": ["qlib_manifest.json", "workflow_config.yaml", "baseline_protocol.md"],
        "smoke_files": ["qlib_manifest.smoke.csv", "workflow_config.smoke.csv", "baseline_protocol.smoke.csv"],
        "baseline": "等权/朴素信号 vs Qlib LightGBM Alpha158",
        "sources": ["microsoft/qlib", "investment_data 2026-07-27 release", "本地 frozen config 与 lock file"],
        "questions": ["加入成本后哪些结论变化最大？", "哪一处最容易发生泄漏？", "LightGBM 相对朴素 baseline 是否真有稳定增量？"],
        "next_step": "将 smoke 协议替换成真实 commit、manifest 与配置文件，再跑官方 smoke workflow。",
    },
]


STARTER_INIT = "from .manifest import load_manifest\n"

STARTER_MANIFEST = """
from __future__ import annotations

import json
from pathlib import Path


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_manifest() -> dict:
    return json.loads((package_root() / "package_manifest.json").read_text(encoding="utf-8"))
"""


STARTER_CHECK = """
from __future__ import annotations

import argparse
import json
from pathlib import Path

from manifest import load_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Check required real-data files.")
    parser.add_argument("--input-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    missing = [name for name in manifest["real_files"] if not (input_dir / name).exists()]
    print(json.dumps({"homework_id": manifest["id"], "input_dir": str(input_dir), "missing_files": missing}, ensure_ascii=False, indent=2))
    if missing:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
"""


STARTER_RUN = """
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from manifest import load_manifest


def summarize_csv(path: Path) -> dict:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return {"file": path.name, "rows": len(rows), "columns": reader.fieldnames or [], "preview": rows[:3]}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run package smoke workflow.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    manifest = load_manifest()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    missing = [name for name in manifest["smoke_files"] if not (input_dir / name).exists()]
    if missing:
        raise SystemExit(f"Missing smoke files: {missing}")

    summaries = [summarize_csv(input_dir / name) for name in manifest["smoke_files"]]
    payload = {
        "homework_id": manifest["id"],
        "title": manifest["title"],
        "stage": manifest["stage"],
        "baseline": manifest["baseline"],
        "summaries": summaries,
    }
    (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "quick_start.md").write_text("\\n".join([
        f"# {manifest['id']} Smoke Run",
        "",
        f"- title: {manifest['title']}",
        f"- input_dir: {input_dir}",
        f"- output_dir: {output_dir}",
        "",
        "## Next Step",
        manifest["next_step"],
    ]), encoding="utf-8")


if __name__ == "__main__":
    main()
"""


TEST_TEMPLATE = """
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_smoke_runner(tmp_path: Path) -> None:
    package_root = Path(__file__).resolve().parents[1]
    workspace_root = package_root.parents[3]
    data_dir = workspace_root / "data" / "quant_finance" / "{slug}"
    output_dir = tmp_path / "outputs"

    subprocess.run([
        sys.executable,
        str(package_root / "starter" / "run.py"),
        "--input-dir",
        str(data_dir),
        "--output-dir",
        str(output_dir),
    ], check=True)

    summary = json.loads((output_dir / "results" / "summary.json").read_text(encoding="utf-8"))
    assert summary["homework_id"] == "{homework_id}"
    assert len(summary["summaries"]) == {smoke_count}
"""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def smoke_rows(file_name: str) -> list[dict[str, str]]:
    if "risk_free" in file_name:
        return [{"date": "2024-01-02", "rf": "0.0001"}, {"date": "2024-01-03", "rf": "0.0001"}, {"date": "2024-01-04", "rf": "0.0001"}]
    if "benchmark" in file_name:
        return [{"date": "2024-01-02", "ticker": "SPY", "close": "100.0", "return": "0.0000"}, {"date": "2024-01-03", "ticker": "SPY", "close": "101.0", "return": "0.0100"}, {"date": "2024-01-04", "ticker": "SPY", "close": "100.5", "return": "-0.0050"}]
    if "prices" in file_name or "underlying" in file_name:
        return [{"date": "2024-01-02", "ticker": "AAA", "close": "100.0", "volume": "1000"}, {"date": "2024-01-03", "ticker": "AAA", "close": "101.0", "volume": "1200"}, {"date": "2024-01-04", "ticker": "AAA", "close": "99.0", "volume": "900"}]
    if "asset_returns" in file_name or "returns" in file_name or "strategy_returns" in file_name:
        return [{"date": "2024-01-02", "asset": "A", "value": "0.010"}, {"date": "2024-01-03", "asset": "A", "value": "-0.006"}, {"date": "2024-01-04", "asset": "B", "value": "0.008"}]
    if "asset_panel" in file_name or "factor_panel" in file_name:
        return [{"date": "2024-01", "asset": "A", "factor_1": "0.10", "target": "0.02"}, {"date": "2024-02", "asset": "A", "factor_1": "0.12", "target": "0.01"}, {"date": "2024-02", "asset": "B", "factor_1": "-0.05", "target": "-0.01"}]
    if "financial_statement" in file_name:
        return [{"ticker": "AAA", "report_date": "2024-03-31", "revenue": "100", "cash_flow": "80", "assets": "300"}, {"ticker": "BBB", "report_date": "2024-03-31", "revenue": "90", "cash_flow": "40", "assets": "250"}, {"ticker": "CCC", "report_date": "2024-03-31", "revenue": "120", "cash_flow": "110", "assets": "500"}]
    if "filing_calendar" in file_name:
        return [{"ticker": "AAA", "filing_date": "2024-04-20"}, {"ticker": "BBB", "filing_date": "2024-04-22"}, {"ticker": "CCC", "filing_date": "2024-04-25"}]
    if "option_quotes" in file_name:
        return [{"date": "2024-01-02", "strike": "100", "maturity": "2024-02-15", "call_price": "3.2", "put_price": "2.8"}, {"date": "2024-01-03", "strike": "100", "maturity": "2024-02-15", "call_price": "3.5", "put_price": "2.5"}, {"date": "2024-01-04", "strike": "100", "maturity": "2024-02-15", "call_price": "2.9", "put_price": "3.1"}]
    if "ticks" in file_name or "lob_events" in file_name:
        return [{"timestamp": "2024-01-02 09:30:00", "price": "100.0", "size": "10", "side": "B"}, {"timestamp": "2024-01-02 09:30:01", "price": "100.1", "size": "12", "side": "S"}, {"timestamp": "2024-01-02 09:30:02", "price": "100.2", "size": "8", "side": "B"}]
    if "metadata" in file_name:
        return [{"asset": "A", "group": "Equity"}, {"asset": "B", "group": "Bond"}, {"asset": "C", "group": "Commodity"}]
    if "parent_order" in file_name:
        return [{"order_id": "1", "qty": "1000", "side": "BUY", "start_time": "09:30:00", "end_time": "10:00:00"}, {"order_id": "2", "qty": "1500", "side": "SELL", "start_time": "10:00:00", "end_time": "10:30:00"}, {"order_id": "3", "qty": "800", "side": "BUY", "start_time": "10:30:00", "end_time": "11:00:00"}]
    if "liquidity_profile" in file_name or "latency_profile" in file_name:
        return [{"bucket": "1", "value": "0.25"}, {"bucket": "2", "value": "0.35"}, {"bucket": "3", "value": "0.40"}]
    if "venue_quotes" in file_name:
        return [{"timestamp": "2024-01-02 09:30:00", "venue": "LIT_A", "bid": "99.9", "ask": "100.1"}, {"timestamp": "2024-01-02 09:30:00", "venue": "DARK_B", "bid": "99.95", "ask": "100.05"}, {"timestamp": "2024-01-02 09:30:01", "venue": "LIT_C", "bid": "99.8", "ask": "100.2"}]
    if "market_state" in file_name:
        return [{"date": "2024-01-02", "feature_1": "0.1", "feature_2": "0.3", "position": "0"}, {"date": "2024-01-03", "feature_1": "0.2", "feature_2": "0.2", "position": "1"}, {"date": "2024-01-04", "feature_1": "-0.1", "feature_2": "0.4", "position": "0"}]
    if "parameter_grid" in file_name:
        return [{"run_id": "1", "param_a": "5", "score": "0.10"}, {"run_id": "2", "param_a": "10", "score": "0.12"}, {"run_id": "3", "param_a": "20", "score": "0.08"}]
    if "qlib_manifest" in file_name:
        return [{"key": "qlib_commit", "value": "b87a2c294d364a33fb739359886acffe8ec907d1"}, {"key": "data_release", "value": "2026-07-27"}, {"key": "provider_uri", "value": "F:/-/03-Projects/data/quant_finance/hw17_qlib_factor_research"}]
    if "workflow_config" in file_name:
        return [{"field": "model", "value": "lightgbm"}, {"field": "dataset", "value": "Alpha158"}, {"field": "split", "value": "train-valid-test"}]
    if "baseline_protocol" in file_name:
        return [{"protocol": "E0", "detail": "equal_weight"}, {"protocol": "E1", "detail": "naive_momentum"}, {"protocol": "E2", "detail": "qlib_lightgbm"}]
    return [{"id": "1", "value": "0.1"}, {"id": "2", "value": "0.2"}, {"id": "3", "value": "0.3"}]


def build_readme(pkg: dict) -> str:
    prereq = "\n".join(f"- `{item}`" for item in pkg["prerequisites"])
    goals = "\n".join(f"- {item}" for item in pkg["goals"])
    real_files = "\n".join(f"- `{name}`" for name in pkg["real_files"])
    smoke_files = "\n".join(f"- `{name}`" for name in pkg["smoke_files"])
    sources = "\n".join(f"- {item}" for item in pkg["sources"])
    return f"""
    # {pkg["id"]} {pkg["title"]} Real Assignment Package

    这是一份面向学生自做的 `{pkg["id"]}` 真实作业包，不再只是说明页。

    ## 布置时机

    {pkg["timing"]}

    ## 包内结构

    - `starter/`：最小可运行骨架，负责检查数据契约并跑通 smoke workflow
    - `baseline/`：baseline 结果记录位，不提供教师答案
    - `tests/`：最小 smoke test
    - `reports/`：正式报告模板
    - `data_card.md`：真实数据契约与 smoke 数据说明
    - `rubric.md`：评分量表
    - `package_manifest.json`：包元数据和 smoke 文件清单

    ## 前置知识

    {prereq}

    ## 教学目标

    {goals}

    ## 真实数据契约

    预期真实数据目录：

    `{DATA_ROOT / pkg["slug"]}`

    真实数据到位后，至少应包含：

    {real_files}

    可优先使用的数据来源：

    {sources}

    ## 当前 smoke 数据

    当前包自带最小 smoke 数据，用于验证流程能否跑通：

    {smoke_files}

    ## 运行方式

    ```bash
    python "{PACKAGES_ROOT / pkg["slug"] / "starter" / "run.py"}" --input-dir "{DATA_ROOT / pkg["slug"]}" --output-dir "{PACKAGES_ROOT / pkg["slug"] / "your_outputs"}"
    python "{PACKAGES_ROOT / pkg["slug"] / "starter" / "check_data.py"}" --input-dir "{DATA_ROOT / pkg["slug"]}"
    pytest "{PACKAGES_ROOT / pkg["slug"] / "tests"}"
    ```

    ## 当前 baseline 定位

    - 本作业包不附带教师最终答案。
    - `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
    - 当前 baseline 主题：`{pkg["baseline"]}`

    ## 下一步建议

    {pkg["next_step"]}
    """


def build_data_card(pkg: dict) -> str:
    real_files = "\n".join(f"- `{name}`" for name in pkg["real_files"])
    smoke_files = "\n".join(f"- `{name}`" for name in pkg["smoke_files"])
    sources = "\n".join(f"- {item}" for item in pkg["sources"])
    return f"""
    # {pkg["id"]} Data Card

    - title: `{pkg["title"]}`
    - stage: `{pkg["stage"]}`
    - generated_at: `{GENERATED_AT}`

    ## 真实数据契约

    数据目录建议固定为：

    `{DATA_ROOT / pkg["slug"]}`

    预期文件：

    {real_files}

    推荐来源：

    {sources}

    ## smoke 数据

    这些数据只用于：

    - 验证 starter 和 tests 跑通
    - 验证文件路径、编码和基本接口
    - 不用于真实研究结论

    smoke 文件：

    {smoke_files}

    ## 硬约束

    - 不得把 smoke 结果当成正式实验结论
    - 必须在 README 中写清楚真实数据来源、时间区间和许可边界
    - 必须说明是否存在未来信息、复权或对齐问题
    """


def build_rubric(pkg: dict) -> str:
    return f"""
    # {pkg["id"]} Rubric

    | 维度 | 分值 | 说明 |
    |:---|---:|:---|
    | 问题理解 | 20 | 是否真正理解 `{pkg["title"]}` 的金融问题 |
    | 数据与协议 | 20 | 数据口径、时间切分、PIT/无泄漏说明是否清楚 |
    | Baseline | 20 | 是否给出公平 baseline，并完成对照 |
    | 分析解释 | 20 | 是否解释结果、失败案例和边界 |
    | 工程与复现 | 20 | 目录、脚本、测试、报告是否完整可复现 |

    ## 不通过条件

    - 无法说明数据来源和时间区间
    - 无 smoke test 或 starter 无法运行
    - 没有 baseline 或只有最好结果没有失败案例
    - 报告没有解释方法边界

    ## 本作业特别强调

    `{pkg["baseline"]}`
    """


def build_baseline(pkg: dict) -> str:
    return f"""
    # {pkg["id"]} Baseline Log

    ## 最小 baseline 目标

    {pkg["baseline"]}

    ## 你需要回填的内容

    - 数据版本：
    - 时间区间：
    - 基线方法：
    - 关键指标：
    - 与更复杂方法的差异：
    - 失败案例：
    - 下一步改进：
    """


def build_report(pkg: dict) -> str:
    questions = "\n".join(f"- {q}" for q in pkg["questions"])
    return f"""
    # {pkg["id"]} Report Template

    ## 1. 作业目标

    说明本作业要解决的金融问题，以及你为什么选择当前 baseline。

    ## 2. 数据与协议

    - 数据来源
    - 时间区间
    - 训练/验证/测试切分
    - 成本口径或执行假设

    ## 3. 方法

    说明你实现的方法、参数和公平对照对象。

    ## 4. 结果

    - 核心指标
    - 图表
    - 与 baseline 的对照

    ## 5. 失败案例与边界

    至少写 2 个失败案例或不稳定现象。

    ## 6. 复盘问题

    {questions}
    """


def manifest(pkg: dict) -> dict:
    return {
        "id": pkg["id"],
        "slug": pkg["slug"],
        "title": pkg["title"],
        "stage": pkg["stage"],
        "generated_at": GENERATED_AT,
        "real_data_dir": str(DATA_ROOT / pkg["slug"]),
        "real_files": pkg["real_files"],
        "smoke_files": pkg["smoke_files"],
        "baseline": pkg["baseline"],
        "next_step": pkg["next_step"],
    }


def generate_package(pkg: dict) -> None:
    package_dir = PACKAGES_ROOT / pkg["slug"]
    data_dir = DATA_ROOT / pkg["slug"]
    package_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    write_text(package_dir / "README.md", build_readme(pkg))
    write_text(package_dir / "data_card.md", build_data_card(pkg))
    write_text(package_dir / "rubric.md", build_rubric(pkg))
    write_text(package_dir / "baseline" / "README.md", build_baseline(pkg))
    write_text(package_dir / "reports" / "report_template.md", build_report(pkg))
    write_text(package_dir / "starter" / "__init__.py", STARTER_INIT)
    write_text(package_dir / "starter" / "manifest.py", STARTER_MANIFEST)
    write_text(package_dir / "starter" / "check_data.py", STARTER_CHECK)
    write_text(package_dir / "starter" / "run.py", STARTER_RUN)
    write_text(package_dir / "tests" / f"test_{pkg['slug']}.py", TEST_TEMPLATE.format(slug=pkg["slug"], homework_id=pkg["id"], smoke_count=len(pkg["smoke_files"])))
    (package_dir / "package_manifest.json").write_text(json.dumps(manifest(pkg), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for name in pkg["smoke_files"]:
        write_csv(data_dir / name, smoke_rows(name))

    write_text(
        data_dir / "README.md",
        f"""
        # {pkg["id"]} Smoke Data

        - package: `{pkg["slug"]}`
        - generated_at: `{GENERATED_AT}`
        - do_not_use_for_final_conclusion: `true`
        """,
    )


def build_root_readme() -> str:
    lines = [
        "# Quant Finance Real Assignment Packages",
        "",
        f"- generated_at: {GENERATED_AT}",
        f"- package_count: {len(PACKAGES)}",
        "",
        "## Packages",
    ]
    for pkg in PACKAGES:
        lines.append(f"- `{pkg['id']}` `{pkg['slug']}`: {pkg['title']}")
    lines.extend(
        [
            "",
            "## Standard Contents",
            "",
            "- README.md",
            "- data_card.md",
            "- rubric.md",
            "- starter/",
            "- baseline/",
            "- tests/",
            "- reports/",
            "",
            "这些包当前采用“真实数据契约 + smoke test + starter skeleton + baseline 记录位”的形式，不包含教师最终答案。",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    PACKAGES_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    write_text(PACKAGES_ROOT / "README.md", build_root_readme())
    for pkg in PACKAGES:
        generate_package(pkg)
    print(f"Generated {len(PACKAGES)} quant finance real assignment packages.")


if __name__ == "__main__":
    main()
