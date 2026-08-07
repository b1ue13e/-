#!/usr/bin/env python3
"""Normalize quant-finance cards and attach canonical assessment links."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
COURSE = ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统" / "03-量化金融"
PROJECT = ROOT / "03-Projects" / "金融与时序" / "03-量化金融"
SNAPSHOT = ROOT / ".recovery-hold" / "2026-08-06" / "quant-finance-comprehensive"
TODAY = "2026-08-06"


STAGES = {
    "00-前置知识": ("00", "量化金融先修与研究协议"),
    "01-夯实基础": ("01", "量化金融数据、收益与组合基础"),
    "02-量化核心技能": ("02", "量化金融定价、时序、因子与风险"),
    "04-深入精通": ("04", "量化金融微观结构、执行与强化学习"),
}


EXEMPT_NAMES = {
    "量化金融-符号与术语速查.md": "术语与符号参考页，不作为独立知识验收单元。",
    "量化金融-本地环境配置与依赖.md": "环境说明页，只服务于代码运行前置。",
    "量化金融-外部实验资产索引.md": "外部实验来源索引，只登记资产与边界。",
    "量化金融-跨课程依赖与出口.md": "跨课程依赖参考页，不承担课程顺序导航。",
    "量化金融-全栈资产地图.md": "完成主线后的资产查阅索引，不作为独立知识卡。",
    "量化金融错题漏洞入口 (Quant Finance Pitfalls).md": "错题与弱点聚合页，具体验收在链接的知识卡和作业中完成。",
    "ML 如何规范地进入金融建模常见题型.md": "题型导航页，不作为独立概念卡。",
    "夯实基础常见题型 (量化金融基石).md": "题型导航页，不作为独立概念卡。",
    "RL 交易实验常见题型.md": "题型导航页，不作为独立概念卡。",
}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return {}, normalized
    parts = normalized.split("---", 2)
    if len(parts) != 3:
        return {}, normalized
    data = yaml.safe_load(parts[1])
    return (data if isinstance(data, dict) else {}), parts[2].lstrip("\n")


def clean_title(value: str) -> str:
    title = re.sub(r"^\d{2}-", "", value)
    title = title.replace("🧠 ", "").strip()
    return title


def source_fields(data: dict, body: str) -> tuple[str, str, str]:
    source = data.get("source") or data.get("source_course")
    source_url = data.get("source_url")
    license_name = data.get("license")
    sources = data.get("sources")
    if not source and isinstance(sources, list) and sources:
        item = sources[0]
        if isinstance(item, dict):
            source = item.get("title")
            source_url = source_url or item.get("url")
            license_name = license_name or item.get("license")
    if not source:
        source = "本课程历史知识卡；原始来源 [待验证]"
    if not source_url or not str(source_url).startswith(("http://", "https://")):
        url_match = re.search(r"https?://[^\s)>\]]+", body)
        source_url = url_match.group(0) if url_match else "[待验证]"
    if not license_name:
        license_name = "link-only；正文为本地学习整理"
    return str(source), str(source_url), str(license_name)


def assignment_for(path: Path) -> tuple[str, str]:
    name = path.stem.lower()
    if path.parent.name == "00-前置知识":
        return (
            "03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-01-线性代数与概率基础",
            "先修检查与基础手算",
        )
    rules = [
        (("capm", "beta", "alpha", "资本资产"), "01", "CAPM与Alpha检验"),
        (("马科维茨", "有效前沿", "black-litterman", "协方差", "组合分散"), "02", "马科维茨有效前沿"),
        (("fama", "hml", "qmj", "因子", "roe", "wacc", "财务", "ebitda", "beneish", "杜邦"), "03", "Fama-MacBeth回归"),
        (("black-scholes", "期权", "希腊", "greek", "伊藤", "sde", "蒙特卡洛"), "05", "Black-Scholes定价与对冲"),
        (("garch", "波动率", "acf", "pacf", "单位根", "adf", "协整", "johansen", "平稳"), "06", "GARCH波动率与动态VaR"),
        (("evt", "var", "cvar", "es", "尾部", "极值"), "08", "EVT尾部风险"),
        (("bars", "采样", "vpin", "订单流", "盘口", "l1", "l2", "l3"), "09", "信息驱动采样"),
        (("hrp", "风险平价", "marchenko", "rmt", "去噪"), "10", "HRP资产配置"),
        (("pbo", "cpcv", "purged", "过拟合", "验证", "泄漏", "回测"), "12", "CPCV与PBO审计"),
        (("almgren", "twap", "vwap", "implementation shortfall", "冲击成本", "最优执行"), "13", "Almgren-Chriss最优执行"),
        (("暗池", "sor", "路由"), "14", "暗池与智能订单路由"),
        (("队列", "挂单", "限价订单簿", "做市商", "价差", "价格发现"), "15", "盘口队列与挂单概率"),
        (("mdp", "奖励", "强化学习", "gym", "ppo", "风险约束", "交易环境", "贝尔曼", "hjb", "merton"), "16", "金融交易环境与PPO"),
        (("qlib", "树模型", "meta-label", "策略评价", "夏普", "最大回撤", "趋势", "均值回归", "配对交易", "凯利", "止损"), "17", "Qlib因子研究与成本敏感回测"),
    ]
    for keys, number, title in rules:
        if any(key in name for key in keys):
            if int(number) <= 8:
                target = f"03-Projects/金融与时序/03-量化金融/课后作业/量化金融-课后作业-{number}-{title}"
            elif int(number) <= 16:
                stage = "03" if int(number) <= 12 else "04"
                target = f"03-Projects/金融与时序/03-量化金融/阶段作业/量化金融-阶段作业-{stage}-{title}"
            else:
                target = "03-Projects/金融与时序/03-量化金融/大作业/量化金融-大作业-Qlib因子研究与成本敏感回测"
            return target, title
    return (
        "03-Projects/金融与时序/03-量化金融/大作业/量化金融-大作业-Qlib因子研究与成本敏感回测",
        "Capstone 综合迁移任务",
    )


def ensure_h1(body: str, title: str) -> str:
    lines = body.splitlines()
    h1_indexes = [index for index, line in enumerate(lines) if line.startswith("# ")]
    if not h1_indexes:
        return f"# {title}\n\n{body.lstrip()}"
    lines[h1_indexes[0]] = f"# {title}"
    for index in h1_indexes[1:]:
        lines[index] = "## " + lines[index][2:]
    return "\n".join(lines)


def assessment_section(path: Path, target: str, label: str) -> str:
    return f'''## 🧪 学完本节后可完成的作业

- **可完成**：[[{target}|{label}]]。
- **为什么现在能做**：本卡已经提供该任务需要的定义、公式、条件或实现边界；若任务还依赖后续知识，先完成对应阶段 MOC 中排在本卡之后的知识卡。
- **提交产物**：闭卷定义/推导、一个可复查计算或代码结果、一个失败案例，以及对适用边界的说明。
'''


def render(path: Path, text: str) -> str:
    data, body = parse_frontmatter(text)
    title = clean_title(str(data.get("topic") or data.get("title") or path.stem))
    is_moc = path.name.startswith("🧭 阶段") or path.name in EXEMPT_NAMES or data.get("kind") == "moc"
    if path.name.startswith("🧭 阶段"):
        data.update({"type": "index", "kind": "moc", "flow": "knowledge"})
    elif path.name in EXEMPT_NAMES:
        data.update({"type": "index", "kind": "moc", "flow": "knowledge"})
    else:
        data.update({"type": "study", "kind": data.get("kind") if data.get("kind") in {"concept", "derivation", "problem-type", "mistake"} else "concept", "flow": data.get("flow") if data.get("flow") in {"sprint", "review"} else "knowledge"})
    data["topic"] = title
    data["course"] = "量化金融"
    data["created"] = str(data.get("created") or TODAY).replace("{date}", TODAY)
    data["status"] = data.get("status") if data.get("status") in {"planned", "ongoing", "completed"} else "planned"
    data["difficulty"] = data.get("difficulty") if data.get("difficulty") in {"beginner", "intermediate", "advanced"} else "intermediate"
    for field in ("concept", "prerequisites", "related"):
        value = data.get(field, [])
        data[field] = value if isinstance(value, list) else ([] if value in (None, "") else [str(value)])
    data["tags"] = data.get("tags") if isinstance(data.get("tags"), list) else ["学习", "量化金融"]
    source, source_url, license_name = source_fields(data, body)
    data["source"] = source
    data["source_url"] = source_url
    data["accessed"] = TODAY
    data["license"] = license_name
    if path.name in EXEMPT_NAMES:
        data["assessment_exempt"] = True
        data["assessment_exempt_reason"] = EXEMPT_NAMES[path.name]
    else:
        data["assessment_exempt"] = False
        data.pop("assessment_exempt_reason", None)
    body = ensure_h1(body, title)
    if not is_moc and "## 🧪 学完本节后可完成的作业" not in body:
        target, label = assignment_for(path)
        body = body.rstrip() + "\n\n" + assessment_section(path, target, label)
    frontmatter = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000).strip()
    return f"---\n{frontmatter}\n---\n\n{body.strip()}\n"


def files() -> list[Path]:
    paths: list[Path] = []
    for directory in STAGES:
        folder = COURSE / directory
        if folder.exists():
            paths.extend(sorted(folder.glob("*.md")))
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.apply and not SNAPSHOT.exists():
        raise SystemExit(f"Missing recovery snapshot: {SNAPSHOT}")
    changes = []
    for path in files():
        old = path.read_text(encoding="utf-8-sig")
        new = render(path, old)
        if new != old.replace("\r\n", "\n"):
            changes.append((path, new))
    print(f"mode={'apply' if args.apply else 'dry-run'}")
    print(f"files={len(files())}")
    print(f"changes={len(changes)}")
    for path, _ in changes:
        print(f"EDIT\t{path.relative_to(ROOT)}")
    if not args.apply:
        return 0
    for path, new in changes:
        path.write_text(new, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
