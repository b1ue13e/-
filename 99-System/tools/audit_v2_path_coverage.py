#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_v2_path_coverage.py
审计 33 条核心/扩展学习路径的 V2 规范（开源主线 + 阶段实验 + 100分 Rubric）覆盖情况。
"""

import os
import sys
from pathlib import Path

# 设置 UTF-8 输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

VAULT_ROOT = Path(r"F:\-")
LEARNING_SYS_DIR = VAULT_ROOT / "02-Knowledge" / "🧠 学习系统"

CORE_PATHS = [
    "01-社交网络挖掘", "02-时间序列分析", "03-量化金融", "04-离散数学", "05-计算机视觉",
    "06-常微分方程", "07-最优化方法", "08-NLP全栈", "09-高等代数", "10-数据结构与算法",
    "11-计算机组成原理", "12-信号与系统", "13-强化学习", "14-概率图模型", "15-控制与机器人学",
    "16-多元统计", "17-机器学习", "22-概率论与数理统计", "23-图神经网络", "24-随机过程",
    "25-测度论", "26-实变函数", "27-泛函分析", "28-数学分析", "29-运筹学",
    "30-应用回归分析", "31-属性数据分析", "32-非参数统计", "33-贝叶斯统计", "34-偏微分方程",
    "35-数值分析", "36-数据挖掘与信息检索", "37-复变函数"
]

def audit_path(path_name):
    path_dir = LEARNING_SYS_DIR / path_name
    index_file = path_dir / "📚 教材挂载索引.md"
    
    if not index_file.exists():
        return {
            "name": path_name,
            "exists": False,
            "has_spine": False,
            "has_plan": False,
            "has_stage_exp": False,
            "has_rubric": False,
            "v2_compliant": False,
            "status": "❌ 缺失教材挂载索引"
        }
    
    try:
        content = index_file.read_text(encoding="utf-8")
    except Exception as e:
        return {
            "name": path_name,
            "exists": True,
            "has_spine": False,
            "has_plan": False,
            "has_stage_exp": False,
            "has_rubric": False,
            "v2_compliant": False,
            "status": f"❌ 读取错误: {e}"
        }
    
    has_spine = "spine_source:" in content or "spine_source :" in content
    has_plan = "## 🧭 开源自学执行方案" in content
    has_stage_exp = ("阶段" in content and ("Lab" in content or "实验" in content or "产出" in content or "验收" in content))
    has_rubric = "100 分 Rubric" in content or "100分 Rubric" in content or "Rubric" in content
    
    is_v2 = has_spine and has_plan and has_stage_exp and has_rubric
    
    missing_items = []
    if not has_spine: missing_items.append("spine_source")
    if not has_plan: missing_items.append("开源执行方案")
    if not has_stage_exp: missing_items.append("阶段实验/Lab")
    if not has_rubric: missing_items.append("Rubric")
    
    status = "✅ V2 完整规范" if is_v2 else f"⚠️ V1 结构 (缺失: {', '.join(missing_items)})"
    
    return {
        "name": path_name,
        "exists": True,
        "has_spine": has_spine,
        "has_plan": has_plan,
        "has_stage_exp": has_stage_exp,
        "has_rubric": has_rubric,
        "v2_compliant": is_v2,
        "status": status
    }

def main():
    results = [audit_path(name) for name in CORE_PATHS]
    v2_count = sum(1 for r in results if r["v2_compliant"])
    total_count = len(CORE_PATHS)
    rate = (v2_count / total_count) * 100 if total_count > 0 else 0
    
    print(f"=" * 80)
    print(f"📊 33 条学习路径 V2 规范覆盖审计报告")
    print(f"=" * 80)
    print(f"覆盖率: {rate:.1f}% ({v2_count}/{total_count} 已升级为 V2 规范)")
    print(f"-" * 80)
    
    for r in results:
        print(f"{r['name']:<24} | {r['status']}")
    
    print(f"=" * 80)
    return 0

if __name__ == "__main__":
    sys.exit(main())
