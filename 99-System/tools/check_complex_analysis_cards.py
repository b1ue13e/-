#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 37-复变函数 14 张知识点卡是否完整遵循数学证明模板结构。
验证项：
  1. frontmatter 存在且含 proof_mode: true
  2. 模板的 14 个二级标题（## 0. 到 ## 13.）全部存在
  3. 文件非空、无「待补充/TODO/占位」占位标记
退出码：0=全部通过；1=存在失败项
"""
import re
import sys
from pathlib import Path

BASE = Path(r"F:\-\02-Knowledge\🧠 学习系统\37-复变函数")
TEMPLATE_SECTIONS = [
    "## 0. ", "## 1. ", "## 2. ", "## 3. ", "## 4. ", "## 5. ", "## 6. ",
    "## 7. ", "## 8. ", "## 9. ", "## 10. ", "## 11. ", "## 12. ", "## 13. ",
]
PLACEHOLDER = re.compile(r"待补充|待补全|TODO|TBD|占位|暂无内容|未完成")
SKIP_NAMES = ("📘", "📗", "📙", "📕", "📋", "📚", "🗺️")

failures = []
checked = 0
for f in sorted(BASE.rglob("*.md")):
    if f.name.startswith(SKIP_NAMES):
        continue
    txt = f.read_text(encoding="utf-8")
    checked += 1
    # 1. frontmatter + proof_mode
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    if not m:
        failures.append(f"{f.name}: 无 frontmatter")
    elif "proof_mode: true" not in m.group(1):
        failures.append(f"{f.name}: 缺 proof_mode: true")
    # 2. 模板 14 节
    missing = [s for s in TEMPLATE_SECTIONS if s not in txt]
    if missing:
        failures.append(f"{f.name}: 缺节 {missing}")
    # 3. 占位标记
    if PLACEHOLDER.search(txt):
        failures.append(f"{f.name}: 含占位标记")

print(f"检查 {checked} 张卡")
if failures:
    for x in failures:
        print(f"[FAIL] {x}")
    print(f"=== RESULT: {len(failures)} 项失败 ===")
    sys.exit(1)
print("=== RESULT: ALL PASS ===")
