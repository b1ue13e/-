#!/usr/bin/env python3
"""05-计算机视觉 知识卡综合复查脚本（Phase3-3）。

检查项：
1. study 卡 frontmatter 必填字段（type/course/created/status/stage_moc/flow/kind）
2. stage_moc / upstream 链接可解析性
3. 表格行内未转义的 `[[目标|别名]]`（应使用 `\\|`）
4. 空壳/占位检测（文件过小或仅模板结构）
5. 全部 wikilink（含路径链接）可解析性
"""
import os
import re
import sys

BASE = r"F:\-\02-Knowledge\🧠 学习系统\05-计算机视觉"
SKIP_DIRS = {'.归档', '.reasonix', '.recovery-hold', '.pytest_cache', '__pycache__', '.git', '.tmp', '.workbuddy'}

issues = []


def walk_md():
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith('.md'):
                yield os.path.join(root, f)


def parse_fm(content):
    m = re.match(r'^---\n(.*?)\n---', content, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).split('\n'):
        mm = re.match(r'^([A-Za-z_]+):\s*(.*)$', line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip()
    return fm


def resolve(link, cur_dir):
    """返回链接目标是否存在。link 无 [[ ]] 包裹。"""
    target = link.split('|')[0].strip()
    if not target:
        return True
    if target.endswith('.md'):
        target = target[:-3]
    # 全路径链接：相对仓库根 或 课程目录
    if '/' in target:
        cands = [
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(BASE))), target + '.md'),  # F:\-
            os.path.join(BASE, target + '.md'),
        ]
        return any(os.path.exists(c) for c in cands)
    # 短链接：课程目录内递归查找
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if target + '.md' in files:
            return True
    return False


def main():
    files = list(walk_md())
    print(f'共扫描 {len(files)} 个活动 .md 文件\n')

    study_cards = 0
    for path in files:
        rel = os.path.relpath(path, BASE)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        fm = parse_fm(content)
        if fm is None:
            issues.append(f'[frontmatter] 缺失或无法解析: {rel}')
            continue
        if fm.get('type') != 'study':
            # 检查表格转义（所有 md 文件）：未转义的别名竖线（前面无反斜杠）
            for i, line in enumerate(content.split('\n'), 1):
                if line.startswith('|') and re.search(r'\[\[[^\]|]+\](?<!\\)\|[^\]|]+\]\]', line.replace('\\|', '\\x7c')):
                    issues.append(f'[表格转义] {rel}:{i} 未转义别名链接: {line.strip()[:80]}')
            continue
        study_cards += 1
        # study 卡必填字段
        for field in ('type', 'course', 'created', 'status', 'stage_moc', 'flow', 'kind'):
            if field not in fm:
                issues.append(f'[字段缺失] {rel}: {field}')
        # stage_moc 可解析
        sm = fm.get('stage_moc', '')
        links = re.findall(r'\[\[([^\]]+)\]\]', sm)
        for lk in links:
            if not resolve(lk, os.path.dirname(path)):
                issues.append(f'[stage_moc死链] {rel}: {lk}')
        # upstream 可解析
        up = fm.get('upstream', '')
        for lk in re.findall(r'\[\[([^\]]+)\]\]', up):
            if not resolve(lk, os.path.dirname(path)):
                issues.append(f'[upstream死链] {rel}: {lk}')
        # 正文 wikilink 可解析性（跳过 frontmatter 与代码围栏；处理 \\| 转义）
        body = content.split('---', 2)[2] if content.startswith('---') else content
        in_fence = False
        for i, line in enumerate(body.split('\n'), 1):
            if re.match(r'^\s*(```|~~~)', line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for raw in re.findall(r'\[\[([^\]]+)\]\]', line):
                target = re.sub(r'\\\|.*$', '', raw).split('#')[0].strip().removesuffix('.md')
                if not resolve(target, os.path.dirname(path)):
                    issues.append(f'[正文死链] {rel}:{i} [[{raw[:60]}]]')
        # 空壳检测：<1500 字节
        if os.path.getsize(path) < 1500:
            issues.append(f'[疑似空壳] {rel}: {os.path.getsize(path)} 字节')
        # 表格转义（排除已转义的 \|）
        for i, line in enumerate(content.split('\n'), 1):
            if line.startswith('|') and re.search(r'\[\[[^\]|]+\](?<!\\)\|[^\]|]+\]\]', line.replace('\\|', '\\x7c')):
                issues.append(f'[表格转义] {rel}:{i} 未转义别名链接: {line.strip()[:80]}')

    print(f'study 卡数量: {study_cards}')
    if issues:
        print(f'\n发现问题 {len(issues)} 项:')
        for it in issues:
            print('  -', it)
        sys.exit(1)
    else:
        print('\n全部检查通过 ✅')
        sys.exit(0)


if __name__ == '__main__':
    main()
