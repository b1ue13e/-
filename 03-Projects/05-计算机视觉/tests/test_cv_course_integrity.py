"""pytest 包装：05-计算机视觉 知识卡综合复查（Phase3-3）。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_links_cv as v  # noqa: E402


def test_cv_course_integrity():
    """55 张 study 卡 frontmatter/stage_moc/upstream/空壳/表格转义全部合规。"""
    files = list(v.walk_md())
    assert len(files) >= 60, f"活动 md 文件数异常: {len(files)}"
    problems = []
    study_cards = 0
    for path in files:
        rel = os.path.relpath(path, v.BASE)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        fm = v.parse_fm(content)
        if fm is None:
            problems.append(f'frontmatter 缺失: {rel}')
            continue
        if fm.get('type') != 'study':
            for i, line in enumerate(content.split('\n'), 1):
                if line.startswith('|') and v.re.search(
                        r'\[\[[^\]|]+\](?<!\\)\|[^\]|]+\]\]', line.replace('\\|', '\\x7c')):
                    problems.append(f'表格未转义别名 {rel}:{i}')
            continue
        study_cards += 1
        for field in ('type', 'course', 'created', 'status', 'stage_moc', 'flow', 'kind'):
            if field not in fm:
                problems.append(f'{rel} 缺字段 {field}')
        for lk in v.re.findall(r'\[\[([^\]]+)\]\]', fm.get('stage_moc', '')):
            if not v.resolve(lk, os.path.dirname(path)):
                problems.append(f'{rel} stage_moc 死链 {lk}')
        for lk in v.re.findall(r'\[\[([^\]]+)\]\]', fm.get('upstream', '')):
            if not v.resolve(lk, os.path.dirname(path)):
                problems.append(f'{rel} upstream 死链 {lk}')
        if os.path.getsize(path) < 1500:
            problems.append(f'{rel} 疑似空壳')
        for i, line in enumerate(content.split('\n'), 1):
            if line.startswith('|') and v.re.search(
                    r'\[\[[^\]|]+\](?<!\\)\|[^\]|]+\]\]', line.replace('\\|', '\\x7c')):
                problems.append(f'表格未转义别名 {rel}:{i}')
    assert study_cards == 55, f"study 卡数量异常: {study_cards}"
    assert not problems, f"发现问题 {len(problems)} 项:\n" + "\n".join(problems[:30])
