import re, glob

files = [f for f in glob.glob('**/*.md', recursive=True) if '.workbuddy' not in f]
total_fix = 0
for fp in files:
    with open(fp, 'r', encoding='utf-8', errors='replace', newline='') as fh:
        t = fh.read()
    orig = t
    # 1. 修复 \rho -> CR/换行 + ho_k 或 ho  (含 $ 后 CR 情况)
    t, n1 = re.subn(r'\$([\r\n\s])+ho_k', '$\u005crho_k', t)
    t, n2 = re.subn(r'\$([\r\n\s])+ho([\s\\])', '$\u005crho\\2', t)
    # 2. 修复 \nabla -> 换行 + abla（行首裸 abla 前无反斜杠）
    t, n3 = re.subn(r'(?<=\n)abla(?=[ f_{^]|$)', '\u005c\u005cnabla', t)
    # 3. 修复 CR+ho 残留（任意位置）
    t, n4 = re.subn('\x0dho', '\u005crho', t)
    # 4. 合并拆行：行首 \nabla/\rho 且上一行以 $ 或空格/逗号/反斜杠结尾
    if n1 + n2 + n3 + n4 > 0:
        lines = t.split('\n')
        out = []
        for i, ln in enumerate(lines):
            if i > 0 and re.match(r'^\\(nabla|rho)', ln):
                prev = out[-1] if out else lines[i-1]
                dc = prev.count('$')
                if dc % 2 == 1 or prev.rstrip().endswith((' ', '\\', ',')):
                    out[-1] = prev + ln
                    total_fix += 1
                    continue
            out.append(ln)
        t = '\n'.join(out)
    if t != orig:
        with open(fp, 'w', encoding='utf-8', newline='') as fh:
            fh.write(t)
        print(f'修复: {fp} (rho:{n1+n2+n4}, nabla:{n3})')
print('完成，总合并:', total_fix)
