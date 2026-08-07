import os
import sys
import glob
import re
import yaml
from pathlib import Path
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = Path("F:/-")
KNOWLEDGE_DIR = VAULT_ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统"

if not KNOWLEDGE_DIR.exists():
    KNOWLEDGE_DIR = VAULT_ROOT / "02-Knowledge/🧠 学习系统"

audit_results = []
course_stats = defaultdict(lambda: {"total": 0, "sum_score": 0, "scores": []})
WIKILINK_RE = re.compile(r'\[\[([^\]\|]+)(?:\|[^\]]+)?\]\]')

def score_note(file_path):
    score = 0
    breakdown = {}
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        return None

    # 1. Frontmatter (10 pts)
    fm_score = 0
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                data = yaml.safe_load(parts[1])
                if isinstance(data, dict):
                    fm_score += 4
                    if any(k in data for k in ["title", "name", "h1"]): fm_score += 2
                    if any(k in data for k in ["tags", "tag"]): fm_score += 2
                    if any(k in data for k in ["course", "category", "subject", "type"]): fm_score += 2
            except:
                fm_score = 2
    breakdown["frontmatter"] = fm_score
    score += fm_score

    # 2. Intuitive Mental Model & Problem Context (15 pts)
    mm_score = 0
    if any(kw in content for kw in ["麻烦", "背景", "为什么", "心智模型", "直觉", "背景与动机", "类比"]):
        mm_score += 8
    if any(kw in content for kw in ["其实就像", "比喻", "Q&A", "问答"]):
        mm_score += 7
    breakdown["mental_model"] = mm_score
    score += mm_score

    # 3. Formal Definition & Math Derivation (25 pts)
    math_score = 0
    has_inline_math = bool(re.search(r'\$[^\$]+\$', content))
    has_block_math = bool(re.search(r'\$\$[^\$]+\$\$', content))
    if has_block_math:
        math_score += 10
    elif has_inline_math:
        math_score += 5
        
    if any(kw in content for kw in ["符号", "对照表", "Symbol", "定义"]):
        math_score += 7
    if any(kw in content for kw in ["推导", "证明", "梯度", "损失", "最小化", "最大化", "Derivation"]):
        math_score += 8
    breakdown["math"] = math_score
    score += math_score

    # 4. Code Implementation & Tensor Shape Tracing (25 pts)
    code_score = 0
    has_code = "```python" in content or "```" in content
    if has_code:
        code_score += 10
        if any(kw in content for kw in ["shape", "Shape", "维度", "B, T, D", "batch_size"]):
            code_score += 8
        if "assert" in content or "print(" in content or "return" in content:
            code_score += 7
    breakdown["code"] = code_score
    score += code_score

    # 5. Knowledge Connections & Self-Test (15 pts)
    conn_score = 0
    wikilinks = WIKILINK_RE.findall(content)
    if len(wikilinks) >= 3:
        conn_score += 8
    elif len(wikilinks) >= 1:
        conn_score += 4
        
    if any(kw in content for kw in ["闭卷", "自查", "思考题", "Checklist", "测试", "复盘"]):
        conn_score += 7
    breakdown["connections"] = conn_score
    score += conn_score

    # 6. Misconceptions & Comparison Matrix (10 pts)
    matrix_score = 0
    if "|" in content and "-|-" in content:
        matrix_score += 5
    if any(kw in content for kw in ["误区", "坑", "注意", "对比", "WARNING", "CAUTION", "易错"]):
        matrix_score += 5
    breakdown["misconceptions"] = matrix_score
    score += matrix_score

    return {
        "file": str(file_path),
        "name": file_path.stem,
        "score": score,
        "breakdown": breakdown
    }

all_md_files = list(KNOWLEDGE_DIR.rglob("*.md"))

for f_path in all_md_files:
    res = score_note(f_path)
    if res:
        audit_results.append(res)
        rel_parts = f_path.relative_to(KNOWLEDGE_DIR).parts
        subject = rel_parts[0] if len(rel_parts) > 1 else "根目录"
        course_stats[subject]["total"] += 1
        course_stats[subject]["sum_score"] += res["score"]
        course_stats[subject]["scores"].append(res["score"])

audit_results.sort(key=lambda x: x["score"], reverse=True)
REPORT_PATH = VAULT_ROOT / "knowledge_notes_strict_audit_round1.md"

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("# 🏆 第一轮修复后全量超严苛打分与质量诊断报告\n\n")
    total_notes = len(audit_results)
    avg_total_score = sum(r["score"] for r in audit_results) / total_notes if total_notes else 0
    
    f.write(f"- **评估笔记总量**：{total_notes} 篇知识点笔记\n")
    f.write(f"- **第一轮全局平均得分**：**{avg_total_score:.1f} / 100 分**\n")
    
    g_excellent = len([r for r in audit_results if r["score"] >= 90])
    g_good = len([r for r in audit_results if 80 <= r["score"] < 90])
    g_fair = len([r for r in audit_results if 60 <= r["score"] < 80])
    g_poor = len([r for r in audit_results if r["score"] < 60])
    
    f.write("\n## 📊 轮次 1 得分区间分布\n")
    f.write(f"- 🌟 **卓越 (90 - 100 分)**：{g_excellent} 篇 ({(g_excellent/total_notes*100):.1f}%)\n")
    f.write(f"- 🟢 **良好 (80 - 89 分)**：{g_good} 篇 ({(g_good/total_notes*100):.1f}%)\n")
    f.write(f"- 🟡 **合格 (60 - 79 分)**：{g_fair} 篇 ({(g_fair/total_notes*100):.1f}%)\n")
    f.write(f"- 🔴 **待优化 (< 60 分)**：{g_poor} 篇 ({(g_poor/total_notes*100):.1f}%)\n")

    f.write("\n## 📚 各学科/课程轮次 1 得分排行\n")
    f.write("| 学科/课程 | 笔记数量 | 平均得分 | 质量评级 |\n")
    f.write("|:---|---:|---:|:---| \n")
    
    sorted_courses = sorted(course_stats.items(), key=lambda x: (x[1]["sum_score"]/x[1]["total"] if x[1]["total"] else 0), reverse=True)
    for course, st in sorted_courses:
        avg = st["sum_score"] / st["total"] if st["total"] else 0
        grade = "🌟 顶尖" if avg >= 95 else "🟢 优秀" if avg >= 85 else "🟡 一般"
        f.write(f"| **{course}** | {st['total']} | **{avg:.1f}** | {grade} |\n")

print(f"Round 1 Audit Complete! Avg score: {avg_total_score:.1f}")
