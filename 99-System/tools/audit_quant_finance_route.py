#!/usr/bin/env python3
"""Audit the canonical quant-finance learning execution chain."""
from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
QUANT = ROOT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"
PROJECT = ROOT / "03-Projects" / "金融与时序" / "03-量化金融" / "Qlib因子研究"
KEY_PAGES = [
    QUANT / "🧩 Qlib 项目知识点—作业—验收路线图.md",
    QUANT / "🚀 Qlib项目执行入口.md",
    QUANT / "🧠 量化金融李宏毅式实战作业总索引.md",
    QUANT / "🗺️ 量化金融学习路径.md",
    ROOT / "01-Active Sprint" / "🚀 Active Sprint.md",
    ROOT / "99-System" / "🗓️ 计划执行系统" / "周计划" / "2026-Sprint1-量化金融冲刺计划.md",
    PROJECT / "00-Qlib项目总看板.md",
]
SKIP_DIRS = {".git", ".obsidian", ".recovery-hold", ".tmp", "tmp", "🗄️ 归档", "书籍资源", ".venv", "site-packages"}
LINK_RE = re.compile(r"(?<!!)\[\[([^\]]+)\]\]")


def markdown_files() -> list[Path]:
    paths: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".tmp")]
        for filename in filenames:
            if filename.endswith(".md"):
                paths.append(Path(dirpath) / filename)
    return paths


def audit_links(pages: list[Path], all_md: list[Path]) -> list[str]:
    errors: list[str] = []
    stems: dict[str, list[Path]] = defaultdict(list)
    for path in all_md:
        stems[path.stem].append(path)
    for path in pages:
        text = path.read_text(encoding="utf-8-sig")
        for match in LINK_RE.finditer(text):
            target = match.group(1).split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/").rstrip("/")
            if not target:
                continue
            direct = []
            for base in (path.parent, ROOT):
                candidate = base.joinpath(*target.split("/"))
                if candidate.suffix.lower() not in {".md", ".pdf"}:
                    candidate = candidate.with_suffix(".md")
                if candidate.exists():
                    direct.append(candidate)
            name = Path(target).name.removesuffix(".md")
            if not direct and not stems.get(name):
                errors.append(f"broken link in {path.relative_to(ROOT)}: {target}")
            if "/" not in target and len(stems.get(name, [])) > 1:
                errors.append(f"ambiguous basename link in {path.relative_to(ROOT)}: {target}")
    return errors


def main() -> int:
    errors: list[str] = []
    for path in KEY_PAGES:
        if not path.exists():
            errors.append(f"missing key page: {path.relative_to(ROOT)}")
    for name in [
        "A01-数据协议与无泄漏审计.md",
        "A02-E0等权与指数基线.md",
        "A03-E1简单连续因子.md",
        "A04-E2-Qlib-LightGBM.md",
        "A05-成本与稳健性审计.md",
        "A06-复现报告与答辩.md",
        "Quant-Factor-And-Arbitrage-Engine.md",
    ]:
        if not (PROJECT / name).exists():
            errors.append(f"missing project page: {name}")

    if all(path.exists() for path in KEY_PAGES):
        errors.extend(audit_links(KEY_PAGES, markdown_files()))

    route = QUANT / "🧩 Qlib 项目知识点—作业—验收路线图.md"
    if route.exists():
        rows = re.findall(r"^\| K(\d{2}) \|", route.read_text(encoding="utf-8-sig"), re.MULTILINE)
        expected = [f"{i:02d}" for i in range(1, 29)]
        if rows != expected:
            errors.append(f"K rows are not exactly K01-K28: {rows}")

    for path in [KEY_PAGES[0], KEY_PAGES[1], KEY_PAGES[4], KEY_PAGES[6]]:
        if path.exists() and "K01" not in path.read_text(encoding="utf-8-sig"):
            errors.append(f"current K pointer missing K01: {path.relative_to(ROOT)}")

    stale_days = list(QUANT.glob("20??-??-?? *日计划.md"))
    if stale_days:
        errors.append(f"stale day plans in knowledge folder: {len(stale_days)}")
    if (QUANT / "🚀 Active Sprint.md").exists():
        errors.append("duplicate Active Sprint remains in quant folder")

    if errors:
        print(f"Quant route audit failed with {len(errors)} issue(s):")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Quant route audit passed: canonical links, K01-K28, A01-A06, current pointer, and folder hygiene are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
