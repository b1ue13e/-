#!/usr/bin/env python3
"""Replace reverted/generic K cards that lack explicit Anki sections."""
from __future__ import annotations

import re
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "02-Knowledge" / "🧠 学习系统" / "03-量化金融"
P1 = runpy.run_path(str(ROOT / "99-System" / "tools" / "upgrade_quant_route_quality.py"))["ITEMS"]
P2 = runpy.run_path(str(ROOT / "99-System" / "tools" / "upgrade_quant_route_quality_k15_k28.py"))["ITEMS"]
ITEMS = {**P1, **P2}
FENCE = chr(96) * 3
HEADING = "## 🃏 Anki 卡片"
A_PAGE = {
    **{f"{i:02d}": "A01-数据协议与无泄漏审计" for i in range(1, 7)},
    **{f"{i:02d}": "A02-E0等权与指数基线" for i in range(7, 11)},
    **{f"{i:02d}": "A03-E1简单连续因子" for i in range(11, 18)},
    **{f"{i:02d}": "A04-E2-Qlib-LightGBM" for i in range(18, 24)},
    **{f"{i:02d}": "A05-成本与稳健性审计" for i in range(24, 29)},
}


def sentence_with(text: str, word: str) -> str:
    for part in re.split(r"(?<=。)", text):
        if word in part:
            return part.strip()
    return text.split("。", 1)[0].strip() + "。"


def main() -> None:
    recovered = []
    for k, (rel, focus, sources, code, links) in ITEMS.items():
        path = Q / rel
        old = path.read_text(encoding="utf-8-sig")
        if HEADING in old:
            continue
        fm = old.split("---", 2)[1] if old.startswith("---") and old.count("---") >= 2 else ""
        created_match = re.search(r"(?m)^created:\s*(.+)$", fm)
        created = created_match.group(1).strip() if created_match else "2026-08-01"
        topic = path.stem
        flow = "sprint" if int(k) <= 6 else "knowledge"
        status = "ongoing" if k == "01" else "planned"
        first = focus.split("。", 1)[0].strip() + "。"
        boundary = sentence_with(focus, "反例")
        source_lines = "\n".join(f"{i}. {s}" for i, s in enumerate(sources, 1))
        link_lines = "\n".join(f"- [[{target}]]" for target in links)
        body = f"""---
type: study
topic: "{topic}"
created: {created}
updated: 2026-08-01
status: {status}
difficulty: intermediate
course: 量化金融
note_role: concept
flow: {flow}
kind: concept
sprint_id: 2026-S01-quant
concept: ["{topic}"]
tags: [学习, 量化金融]
anki_deck: "量化金融::Qlib"
anki_tags: [quant, K{k}, verified_route]
---
# {topic}

> **K{k} 目标**：不靠阅读完成度，而是通过定义、边界、反例和可运行断言证明掌握。

## 0. 先测再学

闭卷写出 {topic} 的输入、输出、成立条件和一个失败案例。若无法写清，先完成本页示例，不并行开启下一个 K 点。

## 1. 定义、机制、假设与边界

{focus}

## 2. Worked example

{FENCE}python
{code}
{FENCE}

运行后必须保存输入、期望输出和实际输出。代码可执行只证明局部定义一致，不证明策略在样本外有效。

## 3. K{k} 最小作业

1. 用自己的数据重新构造上述最小示例，不直接复制数值。
2. 增加一个由本主题边界产生的失败案例，并确认断言确实失败。
3. 闭卷解释公式或机制，再与权威来源逐项核对。
4. 把代码、输出、失败日志和一句结论登记到 [[{A_PAGE[k]}]]。

## 4. 闭卷闸门

- [ ] 能用自己的话定义 {topic}
- [ ] 能说明至少一个成立条件和一个失效边界
- [ ] 手算或人工推演与代码结果一致
- [ ] 失败案例能够被测试捕获
- [ ] 没有把局部代码通过夸大为策略有效

{HEADING}

- K{k}｜{topic}的核心判断是什么？ :: {first}
- K{k}｜{topic}最需要防范的反例是什么？ :: {boundary}

<!-- quant-route-quality-v2 -->
## 5. 可定位来源

{source_lines}

## 6. 知识连接

{link_lines}
"""
        path.write_text(body, encoding="utf-8")
        recovered.append(path.relative_to(ROOT))
    print(f"Recovered {len(recovered)} K cards that lacked explicit Anki sections.")
    for p in recovered:
        print(f"- {p}")


if __name__ == "__main__":
    main()