#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量 Frontmatter 更新工具
用于为 Obsidian 学习笔记批量添加或更新 frontmatter

用法:
    python batch_frontmatter_updater.py [选项]
    
选项:
    --dry-run    预览模式，不实际修改文件
    --missing-only  只为缺失 frontmatter 的文件添加模板，不补写已有 frontmatter
    --path       指定路径（默认：02-Knowledge/🧠 学习系统）
    --template   使用特定模板（stage/topic/note）
"""

import os
import re
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 配置
DEFAULT_PATH = "02-Knowledge/🧠 学习系统"
ENCODING = "utf-8"


def configure_utf8_stdio() -> None:
    """
    Windows PowerShell/cmd 默认可能是 GBK，无法输出 emoji。
    切到 UTF-8 可以避免 UnicodeEncodeError。
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding=ENCODING, errors="replace")
            except Exception:
                pass

# 阶段文件模板 - 用于学习路径的阶段入口文件
STAGE_TEMPLATE = {
    "type": "stage",
    "topic": "",
    "tags": [],
    "created": "{date}",
    "status": "planned",
    "difficulty": "intermediate",
    "concept": [],
    "prerequisites": [],
    "related": [],
    "phase": 0
}

# 主题笔记模板 - 用于具体知识点笔记
TOPIC_TEMPLATE = {
    "type": "study",
    "topic": "",
    "created": "{date}",
    "status": "ongoing",
    "difficulty": "intermediate",
    "concept": [],
    "prerequisites": [],
    "related": [],
    "tags": ["学习"]
}

# 简单笔记模板
NOTE_TEMPLATE = {
    "type": "note",
    "topic": "",
    "created": "{date}",
    "status": "ongoing",
    "tags": ["学习"]
}

INDEX_TEMPLATE = {
    "type": "index",
    "topic": "",
    "created": "{date}",
    "status": "active",
    "tags": ["索引"]
}

BOOK_TEMPLATE = {
    "type": "book",
    "topic": "",
    "created": "{date}",
    "status": "unread",
    "tags": ["书籍", "阅读"]
}

PROMPT_TEMPLATE = {
    "type": "prompt",
    "topic": "",
    "created": "{date}",
    "status": "active",
    "tags": ["prompt"]
}

TEMPLATE_TEMPLATE = {
    "type": "template",
    "topic": "",
    "created": "{date}",
    "status": "active",
    "tags": ["模板"]
}

PROJECT_TEMPLATE = {
    "type": "project",
    "topic": "",
    "created": "{date}",
    "status": "ongoing",
    "difficulty": "advanced",
    "concept": [],
    "prerequisites": [],
    "related": [],
    "tags": ["学习", "项目"]
}


def parse_frontmatter(content: str) -> tuple:
    """
    解析文件的 frontmatter
    返回: (frontmatter_dict, body_content, has_frontmatter, parse_error)
    """
    pattern = r'^\ufeff?---\s*\n(.*?)\n---\s*\n?(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        try:
            fm = yaml.safe_load(match.group(1))
            if fm is not None and not isinstance(fm, dict):
                return {}, match.group(2), True, "frontmatter 不是 YAML 映射"
            return fm or {}, match.group(2), True, None
        except yaml.YAMLError as exc:
            return {}, content, True, str(exc).splitlines()[0]
    
    return {}, content, False, None


def generate_frontmatter(data: Dict) -> str:
    """
    生成 frontmatter 字符串
    """
    # 只清理 None；保留 [] / ""，因为空占位字段也是模板规范的一部分。
    clean_data = {k: v for k, v in data.items() if v is not None}
    return yaml.safe_dump(clean_data, allow_unicode=True, sort_keys=False)


def is_missing_value(value) -> bool:
    """
    判断已有字段是否需要补值；空列表是有效占位，不视为缺失。
    """
    return value is None or value == ""


def update_file_frontmatter(
    file_path: Path,
    template: Dict,
    dry_run: bool = True,
    missing_only: bool = False
) -> str:
    """
    更新单个文件的 frontmatter
    返回: updated / skipped / error
    """
    try:
        content = file_path.read_text(encoding=ENCODING)
        existing_fm, body, has_fm, parse_error = parse_frontmatter(content)

        if parse_error:
            print(f"❌ YAML 错误，已跳过: {file_path} - {parse_error}")
            return "error"

        if missing_only and has_fm:
            print(f"⏭️  跳过 - 已有 frontmatter: {file_path}")
            return "skipped"
        
        # 如果已有 frontmatter，合并而不是覆盖
        if has_fm and existing_fm:
            # 保留现有值，补充缺失的字段
            new_fm = template.copy()
            new_fm.update(existing_fm)
            
            # 确保 created 字段存在
            if "created" not in new_fm or is_missing_value(new_fm["created"]):
                new_fm["created"] = datetime.now().strftime("%Y-%m-%d")

            missing_keys = [
                key for key in new_fm
                if key not in existing_fm or is_missing_value(existing_fm.get(key))
            ]
            if not missing_keys:
                print(f"⏭️  跳过 - 无变化: {file_path}")
                return "skipped"
        else:
            # 新建 frontmatter
            new_fm = template.copy()
            new_fm["created"] = datetime.now().strftime("%Y-%m-%d")
            
            # 从文件名推断 topic
            if "topic" in new_fm and not new_fm["topic"]:
                new_fm["topic"] = file_path.stem.replace("-", " ")
        
        # 生成新的 frontmatter
        fm_str = generate_frontmatter(new_fm)
        new_content = f"---\n{fm_str}---\n\n{body.strip()}\n"

        if new_content == content:
            print(f"⏭️  跳过 - 无变化: {file_path}")
            return "skipped"
        
        if not dry_run:
            file_path.write_text(new_content, encoding=ENCODING)
            print(f"✅ 已更新: {file_path}")
        else:
            print(f"📝 预览 - 将更新: {file_path}")
            print(f"   Frontmatter:\n{fm_str}")
        
        return "updated"
        
    except Exception as e:
        print(f"❌ 错误: {file_path} - {e}")
        return "error"


def detect_template_type(file_path: Path) -> Dict:
    """
    根据文件路径和名称自动检测模板类型
    """
    name = file_path.name
    path_str = str(file_path)

    if "模板" in name:
        template = TEMPLATE_TEMPLATE.copy()
        template["topic"] = file_path.stem
        return template

    if "prompt" in path_str.lower():
        template = PROMPT_TEMPLATE.copy()
        template["topic"] = file_path.stem
        return template

    if any(keyword in name for keyword in ["学习路径", "主页", "入口", "索引", "使用指南", "知识地图"]):
        template = INDEX_TEMPLATE.copy()
        template["topic"] = file_path.stem
        return template

    if "02-Knowledge/📚 书库" in path_str:
        template = BOOK_TEMPLATE.copy()
        template["topic"] = file_path.stem
        return template
    
    # 阶段文件：路径包含“阶段/板块”
    if "阶段" in name or "板块" in name:
        template = STAGE_TEMPLATE.copy()
        template["topic"] = file_path.stem
        # 尝试提取阶段编号
        match = re.search(r'(\d+)', name)
        if match:
            template["phase"] = int(match.group(1))
        return template

    if "项目" in name or "实战" in path_str:
        template = PROJECT_TEMPLATE.copy()
        template["topic"] = file_path.stem
        return template
    
    # 主题笔记：在阶段目录内的具体笔记
    if any(x in path_str for x in ["01-", "02-", "03-", "04-", "05-", "06-"]):
        template = TOPIC_TEMPLATE.copy()
        template["topic"] = file_path.stem
        return template
    
    # 默认简单模板
    return NOTE_TEMPLATE.copy()


def scan_and_update(directory: str, dry_run: bool = True, missing_only: bool = False) -> Dict:
    """
    扫描目录并更新 frontmatter
    返回统计信息
    """
    stats = {
        "total": 0,
        "updated": 0,
        "skipped": 0,
        "errors": 0
    }
    
    base_path = Path(directory)
    if not base_path.exists():
        print(f"❌ 路径不存在: {directory}")
        return stats
    
    md_files = list(base_path.rglob("*.md"))
    
    print(f"🔍 发现 {len(md_files)} 个 Markdown 文件")
    print(f"{'='*60}")
    
    for file_path in md_files:
        # 跳过某些系统文件
        if file_path.name.startswith("."):
            continue
            
        stats["total"] += 1
        
        # 自动检测模板类型
        template = detect_template_type(file_path)
        
        # 更新文件
        result = update_file_frontmatter(file_path, template, dry_run, missing_only)
        if result == "updated":
            stats["updated"] += 1
        elif result == "skipped":
            stats["skipped"] += 1
        else:
            stats["errors"] += 1
    
    return stats


def print_stats(stats: Dict):
    """
    打印统计信息
    """
    print(f"\n{'='*60}")
    print("📊 处理统计:")
    print(f"   总计文件: {stats['total']}")
    print(f"   已更新: {stats['updated']}")
    print(f"   已跳过: {stats['skipped']}")
    print(f"   错误: {stats['errors']}")


def main():
    """
    主函数
    """
    configure_utf8_stdio()

    args = sys.argv[1:]
    
    dry_run = "--dry-run" in args
    missing_only = "--missing-only" in args
    
    # 解析路径参数
    path = DEFAULT_PATH
    if "--path" in args:
        idx = args.index("--path")
        if idx + 1 < len(args):
            path = args[idx + 1]
    
    print("🚀 Frontmatter 批量更新工具")
    print(f"📁 目标路径: {path}")
    print(f"🔧 模式: {'预览' if dry_run else '实际更新'}")
    print(f"🎯 范围: {'仅缺失 frontmatter' if missing_only else '缺失与缺字段'}")
    print(f"{'='*60}\n")
    
    stats = scan_and_update(path, dry_run, missing_only)
    print_stats(stats)
    
    if dry_run:
        print("\n💡 这是预览模式，移除 --dry-run 参数以实际更新文件")


if __name__ == "__main__":
    main()
