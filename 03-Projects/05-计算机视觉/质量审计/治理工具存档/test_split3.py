# -*- coding: utf-8 -*-
"""调试 split_link_body"""
import re

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

for body in [
    '🏗️ 第一阶段：底层基石\\|第一阶段',
    'GoogLeNet|GoogLeNet / Inception',
    'MLP',
]:
    print(repr(body))
    print('  ->', split_link_body(body))
