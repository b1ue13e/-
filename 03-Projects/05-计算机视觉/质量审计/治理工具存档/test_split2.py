# -*- coding: utf-8 -*-
"""验证修正后的 split_link_body（别名含 / 场景）"""
import re

RENAME = {'GoogLeNet': '计算机视觉-GoogLeNet', 'MLP': '计算机视觉-MLP', 'SIFT': '计算机视觉-SIFT'}

def split_link_body(body):
    m = re.match(r'^(.*?)(\\\||\|)(.*)$', body)
    if m and m.group(1):
        name_part, alias = m.group(1), m.group(2) + m.group(3)
    else:
        name_part, alias = body, ''
    prefix = ''
    name = name_part
    if '/' in name_part:
        prefix, name = name_part.rsplit('/', 1)
        prefix += '/'
    return prefix, name, alias

def repl(m):
    inner = m.group(0)[2:-2]
    prefix, name, alias = split_link_body(inner)
    if name in RENAME:
        return '[[' + prefix + RENAME[name] + alias + ']]'
    return m.group(0)

tests = [
    '[[GoogLeNet|GoogLeNet / Inception]]',
    '[[MLP]]',
    '[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/SIFT\\|进入]]',
    '[[🏗️ 第一阶段：底层基石\\|第一阶段]]',
    '[[SIFT]]',
]
for t in tests:
    out = re.sub(r'\[\[[^\[\]]+?\]\]', repl, t)
    print(f'{t}')
    print(f'  -> {out}')
    print()
