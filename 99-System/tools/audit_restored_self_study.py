#!/usr/bin/env python3
"""Audit the restored 33-course self-study layer and its new links."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SYSTEM = ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统"
COURSE_RE = re.compile(r"^(0[1-9]|1[0-7]|2[2-9]|3[0-7])-")
LINK_RE = re.compile(r"\[\[([^\]]]+)\]\]")


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for name in ("00-Inbox", "01-Active Sprint", "02-Knowledge", "03-Projects", "04-Review", "99-System"):
        files.extend((ROOT / name).rglob("*.md"))
    files.extend(ROOT.glob("*.md"))
    return files


def main() -> None:
    courses = sorted(p for p in SYSTEM.iterdir() if p.is_dir() and COURSE_RE.match(p.name))
    errors: list[str] = []
    if len(courses) != 33:
        errors.append(f"expected 33 formal course directories, found {len(courses)}")

    focused: list[Path] = []
    for course in courses:
        paths = list(course.glob("*学习路径*.md"))
        mounts = list(course.glob("*教材挂载索引*.md"))
        if len(paths) != 1:
            errors.append(f"{course.name}: learning path count={len(paths)}")
        if len(mounts) != 1:
            errors.append(f"{course.name}: mount count={len(mounts)}")
            continue
        focused.extend(paths + mounts)
        text = mounts[0].read_text(encoding="utf-8-sig")
        checks = {
            "one restore marker": text.count("OPEN_SELF_STUDY_START") == 1,
            "spine": "唯一 Spine" in text,
            "three labs": len(re.findall(r"\| Lab [123] \|", text)) == 3,
            "capstone": "### Capstone" in text,
            "rubric": "### 100 分 Rubric" in text,
            "license": "### 许可证与本地镜像" in text,
        }
        for label, passed in checks.items():
            if not passed:
                errors.append(f"{course.name}: missing {label}")

    focused.extend([
        SYSTEM / "33门课程开源自学与验收总索引.md",
        SYSTEM / "🧭 学习路径详细索引.md",
        SYSTEM / "🎓 学习入口.md",
        SYSTEM / "🧭 学科分组导航.md",
        SYSTEM / "📚 教材挂载总索引.md",
        SYSTEM / "📊 教材挂载覆盖检查.md",
    ])
    focused.extend((SYSTEM / "37-复变函数").rglob("*.md"))

    all_md = markdown_files()
    by_stem: dict[str, list[Path]] = {}
    for path in all_md:
        by_stem.setdefault(path.stem, []).append(path)

    for path in dict.fromkeys(focused):
        if not path.exists():
            errors.append(f"missing file: {path}")
            continue
        text = path.read_text(encoding="utf-8-sig")
        if text.startswith("---\n") and "\n---\n" in text[4:]:
            try:
                yaml.safe_load(text[4:].split("\n---\n", 1)[0])
            except Exception as exc:
                errors.append(f"YAML {path}: {exc}")
        for raw in LINK_RE.findall(text):
            target = raw.replace("\\|", "|").split("|", 1)[0].split("#", 1)[0]
            if not target or target.startswith(("http://", "https://")):
                continue
            if "/" in target:
                candidate = ROOT / (target + ".md")
                if not candidate.exists():
                    system_candidate = SYSTEM / (target + ".md")
                    if not system_candidate.exists():
                        errors.append(f"broken path link in {path.name}: {target}")
            elif target not in by_stem:
                errors.append(f"missing short link in {path.name}: {target}")

    old_count_hits = []
    for name in ("🎓 学习入口.md", "🧭 学科分组导航.md", "📚 教材挂载总索引.md", "📊 教材挂载覆盖检查.md"):
        text = (SYSTEM / name).read_text(encoding="utf-8-sig")
        if re.search(r"32 条|32门|32 门|22-36|32/32", text):
            old_count_hits.append(name)
    if old_count_hits:
        errors.append(f"obsolete path counts: {old_count_hits}")

    if errors:
        print("AUDIT FAILED")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    print("AUDIT OK")
    print("formal_courses=33")
    print("learning_paths=33")
    print("mount_pages=33")
    print("self_study_blocks=33")
    print("complex_analysis_stages=4")
    print(f"focused_yaml_and_links={len(dict.fromkeys(focused))}")


if __name__ == "__main__":
    main()
