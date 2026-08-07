from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = REPO_ROOT / "02-Knowledge" / "🧠 学习系统" / "02-时间序列分析"
EXCLUDED_PARTS = {".tmp", ".reasonix", ".recovery-hold"}

ASSESSMENT_BLOCKS = {
    "时间序列的定义.md": """
## 检索练习与通过标准

闭卷写出时间序列、随机过程样本路径、截面数据和面板数据的区别，并用一个含重复日期的三行表说明为什么排序和信息时钟属于数据契约。通过标准：定义无循环论证，能指出重复日期、乱序和未来值各自破坏的假设。
""",
    "时间索引与频率.md": """
## 检索练习与通过标准

给一张含缺月、重复时间戳和混合时区的表，先手工列出问题，再写出检查频率、排序、重复和缺失的最小代码。通过标准：不在全样本上静默插值，能说明重采样改变了什么信息边界，并输出可复核的异常清单。
""",
    "基础认知层常见题型.md": """
## 检索练习与通过标准

闭卷完成三道变式：识别趋势/季节/噪声、判断随机游走是否平稳、区分真实零和缺失。通过标准：每题先给图形或机制证据，再给结论；不得只凭口诀或单个检验 p 值。
""",
    "建模与诊断层常见题型.md": """
## 检索练习与通过标准

对两个 ARIMA 候选计算同口径 AICc，解释 Ljung–Box 的自由度，并写出一次“收敛但样本外失败”的否决链。通过标准：能区分拟合、残差诊断和滚动预测三种证据，不把更小 AICc 写成最终胜出。
""",
    "机器学习与深度学习进阶常见题型.md": """
## 检索练习与通过标准

审查一个含 `center=True`、随机 K 折和未来窗口统计量的特征工程片段，逐行标记泄漏点并给出时间滚动替代方案。通过标准：能写出预测原点、可用信息集合和至少一项无泄漏断言。
""",
    "模型识别.md": """
## 检索练习与通过标准

从一组给定 ACF/PACF 草图提出不超过三个候选，随后为每个候选写出根、收敛、残差和滚动验证的淘汰条件。通过标准：候选提名与最终选择分离，能解释“ACF/PACF 截尾口诀”失效的至少一个原因。
""",
    "经典模型层常见题型.md": """
## 检索练习与通过标准

分别构造一个 AR(1)、MA(1) 和 SARIMA 的最小辨析题，写出参数、周期、冲击传播和适用边界。通过标准：至少一个题目包含反例，且答案能区分模型形式与移动平均平滑。
""",
    "统计基础层常见题型.md": """
## 检索练习与通过标准

闭卷推导 MA(1) 的方差、lag-1 协方差和可逆性条件，再判断一个 AR(2) 的根是否满足平稳要求。通过标准：符号、白噪声条件和根的判定方向无误，能指出初始条件的作用。
""",
    "综合模拟题真题复盘.md": """
## 检索练习与通过标准

限时口述一个从任务定义到滚动评估的完整流程，并针对“模型残差合格但预测输给基线”写出复盘记录。通过标准：包含数据契约、候选、诊断、样本外指标、失败窗口和下一步回流入口。
""",
}


DERIVED_VIEW = """
## 学完后可以完成

完成本卡后，使用下面的派生视图定位下游知识和可执行验收入口；作业关系只维护在作业的 `requires` 字段。

### 派生视图

### 下游知识

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

### 可完成作业

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
"""

FPP3_LINK_ONLY = 'license: "截至 2026-08-07 未发现适用于教材正文/题目的开放再分发许可；link-only，仅保留原创释义与章节定位。"'
ASSESSMENT_SENTENCE = "完成本卡后，使用下面的派生视图定位下游知识和可执行验收入口；作业关系只维护在作业的 `requires` 字段。"


def split_document(text: str) -> tuple[str, str] | None:
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    return match.groups() if match else None


def repair(path: Path) -> bool:
    text = path.read_text(encoding="utf-8-sig")
    parts = split_document(text)
    if parts is None:
        return False
    frontmatter, body = parts
    if not re.search(r"^type:\s*study\s*$", frontmatter, re.MULTILINE):
        return False
    changed = False
    if not re.search(r"^## 学完后可以完成\s*$", body, re.MULTILINE):
        body = re.sub(
            r"^## 派生视图\s*$",
            "## 学完后可以完成\n\n完成本卡后，使用下面的派生视图定位下游知识和可执行验收入口；作业关系只维护在作业的 `requires` 字段。\n\n### 派生视图",
            body,
            count=1,
            flags=re.MULTILINE,
        )
        if "## 学完后可以完成" not in body:
            body = body.rstrip() + "\n\n" + DERIVED_VIEW.strip() + "\n"
        changed = True
    duplicate_heading = re.compile(r"^### 学完后可以完成\s*\n(?:\n完成本卡后，使用下面的派生视图定位下游知识和可执行验收入口；作业关系只维护在作业的 `requires` 字段。\s*)?", re.MULTILINE)
    deduplicated = duplicate_heading.sub("", body)
    if deduplicated != body:
        body = deduplicated
        changed = True
    repeated_sentence = f"{ASSESSMENT_SENTENCE}\n\n{ASSESSMENT_SENTENCE}"
    while repeated_sentence in body:
        body = body.replace(repeated_sentence, ASSESSMENT_SENTENCE)
        changed = True
    if not re.search(r"^### 派生视图\s*$", body, re.MULTILINE):
        body = body.rstrip() + "\n\n" + DERIVED_VIEW.strip() + "\n"
        changed = True
    block = ASSESSMENT_BLOCKS.get(path.name)
    if block and "## 检索练习与通过标准" not in body:
        insertion = body.find("## 学完后可以完成")
        if insertion >= 0:
            body = body[:insertion] + block.strip() + "\n\n" + body[insertion:]
        else:
            body = body.rstrip() + "\n\n" + block.strip() + "\n"
        changed = True
    if "otexts.com" in text:
        updated_frontmatter = frontmatter
        for stale_license in (
            'license: "CC BY-NC-SA 4.0"',
            'license: "official-free"',
            'license: "official-free online"',
            'license: "[待验证]；课程页公开访问，正文再分发边界待核验；本卡仅保存原创释义与链接。"',
        ):
            updated_frontmatter = updated_frontmatter.replace(stale_license, FPP3_LINK_ONLY)
        updated_frontmatter = updated_frontmatter.replace('source_type: "official-free-textbook"', 'source_type: open-textbook')
        if "link-only" not in updated_frontmatter:
            updated_frontmatter = updated_frontmatter.rstrip() + "\nsource_license: \"截至 2026-08-07 未发现适用于 FPP3 教材正文/题目的开放再分发许可；link-only，仅保留原创释义与章节定位。\""
        if updated_frontmatter != frontmatter:
            frontmatter = updated_frontmatter
            changed = True
    if changed:
        path.write_text(f"---\n{frontmatter}\n---\n{body.lstrip()}\n", encoding="utf-8")
    return changed


def main() -> int:
    changed = 0
    for path in sorted(COURSE_ROOT.rglob("*.md")):
        if EXCLUDED_PARTS.intersection(path.parts):
            continue
        if repair(path):
            changed += 1
            # Windows terminals may expose a GBK stdout even though vault paths are UTF-8.
            print(str(path.relative_to(REPO_ROOT)).encode("unicode_escape").decode("ascii"))
    print(f"changed_files={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
