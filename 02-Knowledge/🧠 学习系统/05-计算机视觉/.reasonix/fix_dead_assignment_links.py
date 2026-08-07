#!/usr/bin/env python3
"""05-计算机视觉：删除指向不存在作业文件/占位项目的静态死链引用。

背景：课程知识卡与阶段 MOC 中人工维护了大量指向
`03-Projects/课程作业/05-计算机视觉/课后作业/...`、`课后习题/...`、
`阶段作业/...`、`大作业/...` 的静态链接，这些目标文件从未创建
（或已清退），全部为死链；且静态作业反链违反「作业—知识关系唯一
事实源为作业 requires」的规则，可完成作业应由知识卡尾部 Dataview
派生查询提供。

处理范围：课程活动目录下所有 .md（排除 .归档/.reasonix/.recovery-hold）。
跳过文件：🗺️ 学习路径、📚 教材挂载索引、🏭 第五阶段 MOC（手工编辑，
其中含需要保留并改路径的链接）。
保留行：含「课程作业总表」或「项目-CIFAR-10分类与失败样本审计」的行
（这两个文件存在，路径迁移后由手工更新）。
"""
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY_RUN = "--dry-run" in sys.argv
TARGET = "03-Projects/课程作业/05-计算机视觉/"
KEEP = ("课程作业总表", "项目-CIFAR-10分类与失败样本审计")
SKIP_FILES = (
    "🗺️ 计算机视觉学习路径.md",
    "📚 教材挂载索引.md",
    "🏭 第五阶段：专业深化与工程落地.md",
)
SKIP_DIRS = {".归档", ".reasonix", ".recovery-hold", ".pytest_cache", "__pycache__", ".git"}

STATS = {"files": 0, "lines_deleted": 0, "empty_sections": 0, "dashes_fixed": 0}


def clean_section_headers(lines):
    """删除内容为空的 '## 🧪 学完本节后可完成的作业' 小节标题。"""
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## 🧪 学完本节后可完成的作业"):
            # 向后看：标题之后直到下一个 '##' 或 EOF，若只剩空行/分隔线则删除标题
            j = i + 1
            only_empty = True
            while j < len(lines):
                nxt = lines[j]
                if nxt.startswith("## ") or nxt.startswith("# "):
                    break
                if nxt.strip() not in ("", "---"):
                    only_empty = False
                    break
                j += 1
            if only_empty:
                STATS["empty_sections"] += 1
                i += 1  # 跳过标题行
                continue
        result.append(line)
        i += 1
    return result


def collapse_dashes(lines):
    """将连续的 '---' 行压缩为一个。"""
    result = []
    prev_dash = False
    for line in lines:
        if line.strip() == "---":
            if prev_dash:
                STATS["dashes_fixed"] += 1
                continue
            prev_dash = True
        else:
            prev_dash = False
        result.append(line)
    return result


def process_file(path, rel):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original_lines = content.split("\n")
    lines = [l for l in original_lines if not (TARGET in l and not any(k in l for k in KEEP))]
    deleted = len(original_lines) - len(lines)
    if deleted == 0:
        return
    STATS["files"] += 1
    STATS["lines_deleted"] += deleted
    lines = clean_section_headers(lines)
    lines = collapse_dashes(lines)
    if not DRY_RUN:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("\n".join(lines))
    print(f"  [{rel}] 删除 {deleted} 行" + (f"，空小节 {STATS['empty_sections']}" if STATS["empty_sections"] else ""))


def main():
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".md"):
                continue
            if f in SKIP_FILES:
                continue
            process_file(os.path.join(root, f), os.path.relpath(os.path.join(root, f), BASE))
    print(f"\n统计：{STATS['files']} 个文件，删除 {STATS['lines_deleted']} 行，"
          f"清理空小节 {STATS['empty_sections']} 处，压缩分隔线 {STATS['dashes_fixed']} 处")


if __name__ == "__main__":
    main()
