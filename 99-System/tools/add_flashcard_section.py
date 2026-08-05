"""
add_flashcard_section.py
------------------------
给有实质内容的学习笔记批量追加「间隔复习卡片」占位区。

判断逻辑：
- 去掉 frontmatter 后，正文行数 >= MIN_CONTENT_LINES 才算"有内容"
- 已有 #flashcard 标签的跳过（不重复添加）
- 只处理 02-Knowledge/🧠 学习系统/ 下的 .md 文件
- 排除索引、模板、路径图等系统文件（名称以特定 emoji 开头）

用法：
    python tools/add_flashcard_section.py [--dry-run]

    --dry-run  只打印会处理哪些文件，不实际修改
"""

import argparse
import io
import re
import sys
from pathlib import Path

# Windows GBK 终端下强制 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
LEARN_DIR = ROOT / "02-Knowledge/🧠 学习系统"

MIN_CONTENT_LINES = 30  # 正文行数阈值，低于此视为空壳

# 名称前缀判断：这些是系统/索引文件，跳过
SKIP_NAME_PREFIXES = ("🗺️", "🎓", "🧭", "📊", "📋", "🔍", "🕸️", "🔀", "🏷️",
                      "📥", "📚", "🌐", "🎭", "🔄", "🧪", "📄", "📓")

FLASHCARD_BLOCK = """\

---

## 🃏 间隔复习卡片

> 用 **Spaced Repetition** 插件复习。
> 格式：单行卡 `问题 :: 答案`；多行卡：问题 → 空行 → `?` → 空行 → 答案。
> 写卡原则：用自己的话，答案不超过 3 句，每张卡只考一件事。

#flashcard

这个概念解决的核心问题是什么？ :: （填写）

最关键的公式/定义是什么？ :: （填写）

最容易混淆的概念是什么？区别在哪？ :: （填写）
"""


def strip_frontmatter(text: str) -> tuple[str, str]:
    """返回 (frontmatter, body)"""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm = text[: end + 4]
            body = text[end + 4:]
            return fm, body
    return "", text


def has_flashcard(text: str) -> bool:
    return "#flashcard" in text


def content_line_count(body: str) -> int:
    lines = [l for l in body.splitlines() if l.strip()]
    # 排除 markdown 标题行和纯分隔线，只统计实质内容行
    content = [l for l in lines if not re.match(r"^#{1,6}\s", l) and l.strip() != "---"]
    return len(content)


def should_skip(path: Path) -> bool:
    name = path.name
    return any(name.startswith(p) for p in SKIP_NAME_PREFIXES)


def process(dry_run: bool):
    files = list(LEARN_DIR.rglob("*.md"))
    skipped_system = 0
    skipped_shell = 0
    skipped_already = 0
    processed = 0

    for f in sorted(files):
        if should_skip(f):
            skipped_system += 1
            continue

        text = f.read_text(encoding="utf-8")
        fm, body = strip_frontmatter(text)

        if has_flashcard(text):
            skipped_already += 1
            continue

        if content_line_count(body) < MIN_CONTENT_LINES:
            skipped_shell += 1
            continue

        processed += 1
        rel = f.relative_to(ROOT)
        print(f"  [+] {rel}")

        if not dry_run:
            new_text = text.rstrip() + "\n" + FLASHCARD_BLOCK
            f.write_text(new_text, encoding="utf-8")

    print()
    print(f"{'[DRY RUN] ' if dry_run else ''}结果摘要")
    print(f"  {'将处理' if dry_run else '已处理'}：{processed} 篇")
    print(f"  已有闪卡（跳过）：{skipped_already} 篇")
    print(f"  空壳笔记（跳过）：{skipped_shell} 篇")
    print(f"  系统文件（跳过）：{skipped_system} 篇")
    print(f"  合计扫描：{len(files)} 个文件")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量给学习笔记追加闪卡区")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不修改文件")
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN 模式，不会修改任何文件 ===\n")

    process(dry_run=args.dry_run)
