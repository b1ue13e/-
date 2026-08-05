#!/usr/bin/env python3
"""Synchronize derived day/week views from the current Sprint source page.

Storage paths remain unchanged. The Sprint page is the only source of learning
tasks; this script rewrites only the learning-related sections of the 14
existing day plans and the two corresponding week views.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPRINT_PATH = ROOT / "99-System" / "🗓️ 计划执行系统" / "周计划" / "2026-Sprint1-量化金融冲刺计划.md"
DAY_DIR = ROOT / "99-System" / "🗓️ 计划执行系统" / "日计划"
WEEK_DIR = ROOT / "99-System" / "🗓️ 计划执行系统" / "周计划"
SPRINT_ID = "2026-S01-quant"
SPRINT_START = date(2026, 7, 27)
SPRINT_END = date(2026, 8, 9)


def read(path: Path) -> str:
    # utf-8-sig transparently accepts legacy BOM files while returning clean text.
    return path.read_text(encoding="utf-8-sig")


def write_if_changed(path: Path, content: str, check: bool) -> bool:
    old = read(path)
    content = content.rstrip() + "\n"
    if old == content:
        return False
    if not check:
        path.write_text(content, encoding="utf-8", newline="\n")
    return True


def parse_tasks(sprint_text: str) -> dict[int, tuple[bool, str]]:
    pattern = re.compile(r"^- \[([ xX])\] \*\*Day (\d+) \([^)]*\)\*\*：(.*)$", re.MULTILINE)
    tasks = {
        int(day): (mark.lower() == "x", task.strip())
        for mark, day, task in pattern.findall(sprint_text)
    }
    expected = set(range(1, 15))
    if set(tasks) != expected:
        missing = sorted(expected - set(tasks))
        raise RuntimeError(f"Sprint task table is incomplete; missing days: {missing}")
    return tasks


def upsert_frontmatter(text: str, values: dict[str, str]) -> str:
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise RuntimeError("Expected YAML frontmatter")
    header, body = text[4:].split("\n---\n", 1)
    lines = header.splitlines()
    for key, value in values.items():
        replacement = f"{key}: {value}"
        for index, line in enumerate(lines):
            if re.match(rf"^{re.escape(key)}\s*:", line):
                lines[index] = replacement
                break
        else:
            lines.append(replacement)
    block = "---\n" + "\n".join(lines) + "\n---\n"
    return block + body


def day_file(target: date) -> Path:
    matches = sorted(DAY_DIR.glob(f"{target.isoformat()} *.md"))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one day plan for {target}, found {len(matches)}")
    return matches[0]


def replace_between(text: str, start_pattern: str, end_heading: str, replacement: str) -> str:
    pattern = re.compile(
        start_pattern + rf".*?(?=^## (?:[^\r\n]*?[ \t])?{re.escape(end_heading)}[ \t]*$)",
        re.MULTILINE | re.DOTALL,
    )
    updated, count = pattern.subn(replacement.rstrip() + "\n\n", text, count=1)
    if count != 1:
        raise RuntimeError(f"Could not replace section before: {end_heading}")
    return updated


def render_day(text: str, target: date, day_number: int, task_record: tuple[bool, str]) -> str:
    title = next(line for line in text.splitlines() if line.startswith("# "))
    completed, task = task_record
    checkmark = "x" if completed else " "
    task_label = task.rstrip("。")
    proofs = {
        1: "提交收益率、标签、信号形成时点和执行时点口径草案；未通过项明确转入 K01",
        2: "保存固定环境、manifest、qrun 日志和为 0 的退出码，并注明这只证明工具链可用",
        3: "完成 K01 闭卷诊断与 5 个价格的手算；未通过则保持 K01",
        4: "完成 K01 简单/对数收益代码复核与至少一个错误案例",
        5: "完成 K01 累积提取；没有证据不得勾选通过",
        6: "通过 K01：闭卷解释、手算、代码和 A01 证据全部齐全",
        7: "完成 K02 复权合成样例、实际数据口径证据和缺失/停牌规则",
        8: "完成 K03 交易日历、信号日、执行日与测试区间核验",
        9: "完成 K04 多级索引、groupby shift 小样本和跨股票隔离测试",
        10: "完成 K05 rolling(20) 信息窗口、逐项手算和最早可用时间说明",
        11: "完成 K06 四类泄漏辨析、故意泄漏反例和失败测试",
        12: "整合 K01–K06，提交 A01 数据字典、时间协议、复权说明和自动断言",
        13: "完成 K01–K06 累积闭卷测验、错题修复，并从空目录复现 A01",
        14: "完成 A01 答辩与归档；未通过则继续 A01，不启动 A02",
    }
    proof = proofs[day_number]
    learning = f"""{title}

> **Sprint 1（Day {day_number}/14）**：单主题主攻量化金融。学习任务派生自 [[99-System/🗓️ 计划执行系统/周计划/2026-Sprint1-量化金融冲刺计划|唯一 Sprint 任务源]]，本页不再并行安排其他主攻科目。

> [!important] 今日边界
> 只完成量化金融主攻、Anki 到期 FSRS 卡片与健康维护；不跨天补账，不临时切换学科。

## 🎯 80% 深度主攻（90–150 分钟）

- [{checkmark}] **量化金融**：{task_label}
  - 执行入口：[[02-Knowledge/🧠 学习系统/03-量化金融/🚀 Qlib项目执行入口|Qlib 项目执行入口]]
  - 路线：[[02-Knowledge/🧠 学习系统/03-量化金融/🧩 Qlib 项目知识点—作业—验收路线图|K01–K28 掌握路线]]
  - Sprint：[[99-System/🗓️ 计划执行系统/周计划/2026-Sprint1-量化金融冲刺计划|2026-S01-quant]]
  - 今日验收：{proof}。

## 🔄 20% Anki FSRS 间隔维护（最多 30 分钟）

- [ ] 打开 Anki 的 `量化金融::Sprint 1` 牌组，完成全部到期卡；最多 30 分钟或 50 张。
- [ ] 对选择 `Again` 的概念，在原笔记标记 `flow: review`、`weak: true`、`weak_since: {target.isoformat()}`。
- [ ] 没有到期卡时直接结束，不额外制造复习任务。

## 🧠 闭卷提取与验证

- [ ] 不看正文，用自己的话回答：今天的方法解决什么问题？
- [ ] 写出关键假设、公式或流程，并说明一个失效边界。
- [ ] 用题目、代码或结果图验证，不以“笔记写完”作为完成标准。"""

    text = replace_between(
        text,
        rf"^{re.escape(title)}\s*$",
        "雅思词汇",
        learning,
    )

    index = """## 学习索引挂载

- 主攻：量化金融
- 当前行动：[[02-Knowledge/🧠 学习系统/03-量化金融/🚀 Qlib项目执行入口|Qlib 项目执行入口]]
- 路线：[[02-Knowledge/🧠 学习系统/03-量化金融/🧩 Qlib 项目知识点—作业—验收路线图|K01–K28 掌握路线]]
- Sprint：[[99-System/🗓️ 计划执行系统/周计划/2026-Sprint1-量化金融冲刺计划|2026-S01-quant]]
- 当前身份：`flow: sprint`"""
    text = replace_between(text, r"^## 学习索引挂载\s*$", "当日收束", index)

    close = f"""## 当日收束

- [{checkmark}] Day {day_number} 的量化金融验收物是否真实存在？
- [ ] Anki 到期 FSRS 卡片是否完成，`Again` 是否已经标记薄弱点？
- [ ] 雅思、训练和饮食是否完成或如实记录？
- [ ] 明天只接续 Sprint Day {min(day_number + 1, 14)}，不加入新的主攻科目？"""
    text = replace_between(text, r"^## 当日收束\s*$", "导航", close)

    if "所属 Sprint：" not in text:
        marker = f"- 所属周：[[99-System/🗓️ 计划执行系统/周计划/2026-W{target.isocalendar().week:02d} 周计划|2026-W{target.isocalendar().week:02d} 周计划]]"
        sprint_link = "\n- 所属 Sprint：[[99-System/🗓️ 计划执行系统/周计划/2026-Sprint1-量化金融冲刺计划|2026-S01-quant]]"
        if marker in text:
            text = text.replace(marker, marker + sprint_link, 1)
        else:
            text = text.replace("## 导航\n", "## 导航\n\n" + sprint_link.lstrip() + "\n", 1)

    return upsert_frontmatter(
        text,
        {
            "updated": "2026-07-29",
            "phase": f'"Sprint 1：量化金融 (Day {day_number})"',
            "flow": "sprint",
            "sprint": "current",
            "sprint_id": SPRINT_ID,
            "sprint_day": str(day_number),
            "source_of_truth": "false",
            "tags": "[学习, 规划, 日计划, 量化金融, Quant, FSRS, 雅思, 减脂, 训练]",
        },
    )


def render_week(text: str, week_number: int, dates: list[date], tasks: dict[int, tuple[bool, str]]) -> str:
    title = next(line for line in text.splitlines() if line.startswith("# "))
    start_day = (dates[0] - SPRINT_START).days + 1
    end_day = (dates[-1] - SPRINT_START).days + 1
    rows = []
    for target in dates:
        day_number = (target - SPRINT_START).days + 1
        day_plan = day_file(target)
        label = day_plan.stem
        completed, task = tasks[day_number]
        status = "✅ " if completed else ""
        rows.append(
            f"| {target.isoformat()} | Day {day_number} | {status}{task} | "
            f"[[99-System/🗓️ 计划执行系统/日计划/{label}|进入]] |"
        )
    derived = f"""{title}

> 本周只负责展示 [[99-System/🗓️ 计划执行系统/周计划/2026-Sprint1-量化金融冲刺计划|量化金融 Sprint]] 的 Day {start_day}–{end_day}，不再独立安排其他学习主线。

> [!important] 唯一任务源
> 学习任务如需调整，只修改 Sprint 页面，再运行 `python 99-System/tools/sync_current_sprint.py`。

## 本周目标

- [ ] 完成量化金融 Sprint Day {start_day}–{end_day} 的每日验收物。
- [ ] 每天只处理 Anki 到期 FSRS 卡片，`Again` 概念进入 [[04-Review/04-🔁 Review|薄弱点队列]]。
- [ ] 保留雅思、训练和饮食维护，但不新增第二主攻学科。

## 每日入口

| 日期 | Sprint | 唯一学习主线 | 日计划 |
|:--|:--:|:--|:--|
{chr(10).join(rows)}

## 周末验收

- [ ] 每天至少有一项可检查的笔记、题目、代码或报告产出。
- [ ] 在周记的“本周薄弱点”登记所有 `Again` 概念。
- [ ] 未完成任务只在量化金融 Sprint 内顺延，不切换科目。"""

    text = replace_between(
        text,
        rf"^{re.escape(title)}\s*$",
        "本周训练与饮食复盘",
        derived,
    )
    return upsert_frontmatter(
        text,
        {
            "updated": "2026-07-29",
            "flow": "sprint",
            "sprint": "current",
            "sprint_id": SPRINT_ID,
            "source_of_truth": "false",
            "tags": "[学习, 规划, 周计划, 量化金融, Quant, FSRS, 雅思, 减脂, 训练]",
        },
    )


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Synchronize derived Sprint views.")
    parser.add_argument("--check", action="store_true", help="Report drift without writing files")
    args = parser.parse_args()

    tasks = parse_tasks(read(SPRINT_PATH))
    changed: list[Path] = []

    for offset in range((SPRINT_END - SPRINT_START).days + 1):
        target = SPRINT_START + timedelta(days=offset)
        path = day_file(target)
        rendered = render_day(read(path), target, offset + 1, tasks[offset + 1])
        if write_if_changed(path, rendered, args.check):
            changed.append(path)

    weeks = {
        31: [SPRINT_START + timedelta(days=i) for i in range(7)],
        32: [SPRINT_START + timedelta(days=i) for i in range(7, 14)],
    }
    for week_number, dates in weeks.items():
        path = WEEK_DIR / f"2026-W{week_number:02d} 周计划.md"
        rendered = render_week(read(path), week_number, dates, tasks)
        if write_if_changed(path, rendered, args.check):
            changed.append(path)

    if changed:
        action = "Would update" if args.check else "Updated"
        print(f"{action} {len(changed)} files:")
        for path in changed:
            print(f"- {path.relative_to(ROOT)}")
        return 1 if args.check else 0

    print("Sprint-derived day/week views are synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



