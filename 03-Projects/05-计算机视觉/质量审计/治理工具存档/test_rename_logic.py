# -*- coding: utf-8 -*-
"""验证 b10_execute_rename.py 的替换逻辑"""
import re

RENAME = {'MLP': '计算机视觉-MLP', 'SIFT': '计算机视觉-SIFT', '🏗️ 第一阶段：底层基石': '🧭 阶段1-底层基石'}

def split_link_body(body):
    prefix, rest = '', body
    if '/' in body:
        prefix, rest = body.rsplit('/', 1)
        prefix += '/'
    m = re.match(r'^(.*?)(\\\||\|)(.*)$', rest)
    alias = ''
    name = rest
    if m and m.group(1):
        name, alias = m.group(1), m.group(2) + m.group(3)
    return prefix, name, alias

def repl(m):
    inner = m.group(0)[2:-2]
    prefix, name, alias = split_link_body(inner)
    if name in RENAME:
        return '[[' + prefix + RENAME[name] + alias + ']]'
    return m.group(0)

def replace_in_text(content):
    out_lines = []
    in_fence = False
    for line in content.split('\n'):
        if line.strip().startswith('```'):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue
        newline = re.sub(r'\[\[[^\[\]]+?\]\]', repl, line)
        out_lines.append(newline)
    return '\n'.join(out_lines)

tests = [
    '[[MLP]]',
    '[[MLP|多层感知机]]',
    '[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/SIFT|进入]]',
    '[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/SIFT\\|进入]]',
    '[[🏗️ 第一阶段：底层基石]]',
    '[[🏗️ 第一阶段：底层基石\\|第一阶段]]',
    '文本中的 [[MLP]] 和 [[Softmax与SVM损失函数]] 应保留后者',
    '```\n[[MLP]] 代码围栏内不替换\n```\n[[MLP]] 围栏外替换',
    '| 行 | 链接 |\n|:---|:---|\n| A | [[SIFT\\|SIFT特征]] |',
]
for t in tests:
    out = replace_in_text(t)
    print(f'IN : {t}')
    print(f'OUT: {out}')
    print()
