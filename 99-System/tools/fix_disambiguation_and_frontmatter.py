import os
import re

vault_dir = r'f:\-\02-Knowledge\🧠 学习系统'

print("=== STARTING DISAMBIGUATION & FRONTMATTER MISMATCH FIXES ===")

# -------------------------------------------------------------
# 任务三：修复同名入口卡文件名冲突（中国剩余定理、最近点对问题）
# -------------------------------------------------------------
# 1. 中国剩余定理 (DSA 侧改名)
dsa_crt_old = os.path.join(vault_dir, r'10-数据结构与算法\05-算法思想进阶\中国剩余定理.md')
dsa_crt_new = os.path.join(vault_dir, r'10-数据结构与算法\05-算法思想进阶\中国剩余定理-CRT算法.md')
if os.path.exists(dsa_crt_old):
    with open(dsa_crt_old, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('title: "中国剩余定理"', 'title: "中国剩余定理-CRT算法"')
    c = c.replace('# 中国剩余定理', '# 中国剩余定理-CRT算法')
    with open(dsa_crt_new, 'w', encoding='utf-8') as f:
        f.write(c)
    os.remove(dsa_crt_old)
    print("Fixed 同名冲突: 中国剩余定理.md -> 中国剩余定理-CRT算法.md")

# 2. 最近点对问题 (DSA 进阶侧改名)
dsa_cp_old = os.path.join(vault_dir, r'10-数据结构与算法\05-算法思想进阶\最近点对问题.md')
dsa_cp_new = os.path.join(vault_dir, r'10-数据结构与算法\05-算法思想进阶\最近点对问题-分治进阶.md')
if os.path.exists(dsa_cp_old):
    with open(dsa_cp_old, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('title: "最近点对问题-分治应用"', 'title: "最近点对问题-分治进阶"')
    c = c.replace('# 最近点对问题-分治应用', '# 最近点对问题-分治进阶')
    with open(dsa_cp_new, 'w', encoding='utf-8') as f:
        f.write(c)
    os.remove(dsa_cp_old)
    print("Fixed 同名冲突: 05-最近点对问题.md -> 最近点对问题-分治进阶.md")

# -------------------------------------------------------------
# 任务二：同名异义词消歧 (重命名与 Frontmatter/H1 修正)
# -------------------------------------------------------------
disambiguation_rules = [
    ("差分.md", "02-时间序列分析", "差分-时间序列.md", "差分-时间序列"),
    ("差分.md", "10-数据结构与算法", "差分-数组算法.md", "差分-数组算法"),
    ("稳定性.md", "17-机器学习", "稳定性-机器学习.md", "稳定性-机器学习"),
    ("稳定性.md", "29-运筹学", "稳定性-匹配理论.md", "稳定性-匹配理论"),
    ("稳定性.md", "04-离散数学", "稳定性-匹配理论.md", "稳定性-匹配理论"),
    ("绝对连续.md", "25-测度论", "绝对连续-测度.md", "绝对连续-测度"),
    ("绝对连续.md", "26-实变函数", "绝对连续-函数.md", "绝对连续-函数"),
    ("Taylor展开.md", "37-复变函数", "Taylor展开-复变函数.md", "Taylor展开-复变函数"),
    ("Taylor 展开.md", "37-复变函数", "Taylor展开-复变函数.md", "Taylor展开-复变函数"),
    ("分布观点.md", "25-测度论", "分布-广义函数.md", "分布-广义函数"),
    ("分布观点.md", "34-偏微分方程", "弱导数-分布观点.md", "弱导数-分布观点"),
]

for old_name, path_keyword, new_name, new_title in disambiguation_rules:
    for root, dirs, files in os.walk(vault_dir):
        if old_name in files and path_keyword in root:
            old_fp = os.path.join(root, old_name)
            new_fp = os.path.join(root, new_name)
            try:
                with open(old_fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                content = re.sub(r'title:\s*".*?"', f'title: "{new_title}"', content)
                content = re.sub(r'topic:\s*".*?"', f'topic: "{new_title}"', content)
                with open(new_fp, 'w', encoding='utf-8') as f:
                    f.write(content)
                if old_fp != new_fp:
                    os.remove(old_fp)
                print(f"Disambiguated: {old_name} in {path_keyword} -> {new_name}")
            except Exception as e:
                print(f"Error disambiguating {old_fp}: {e}")

# -------------------------------------------------------------
# 任务四：修补复制/Frontmatter 错配与 H1 标题错位
# -------------------------------------------------------------
fixed_mismatch = 0
fixed_h1 = 0

for root, dirs, files in os.walk(vault_dir):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                original_content = content
                title_name = f.replace('.md', '')
                
                # 1. 修复 组合优化ML.md 的 topic
                if f == '组合优化ML.md' and 'topic: "类型系统验证"' in content:
                    content = content.replace('topic: "类型系统验证"', 'topic: "组合优化ML"')
                    fixed_mismatch += 1
                    
                # 2. 修复 图嵌入ML.md 的 topic
                if f == '图嵌入ML.md' and 'topic: "同态加密"' in content:
                    content = content.replace('topic: "同态加密"', 'topic: "图嵌入ML"')
                    fixed_mismatch += 1

                # 3. 修复 34-偏微分方程 下 topic 共享同名错配
                if '34-偏微分方程' in root and 'topic:' in content:
                    # 匹配并用当前真实文件名更新 topic
                    content = re.sub(r'topic:\s*".*?"', f'topic: "{title_name}"', content)

                # 4. 修复 H1 标题被 "0. 先判断它值不值得深挖" 盖住的错位问题
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        yaml_part = parts[1]
                        body_part = parts[2]
                        
                        # 检查 body 的第一行一级标题是否错写为了 # 0. 先判断...
                        lines = body_part.strip().split('\n')
                        if lines and lines[0].startswith('# 0.'):
                            lines[0] = f'# {title_name}\n\n### 0. 先判断它值不值得深挖'
                            new_body = '\n'.join(lines)
                            content = '---' + yaml_part + '\n---\n\n' + new_body
                            fixed_h1 += 1

                if content != original_content:
                    with open(fp, 'w', encoding='utf-8') as file:
                        file.write(content)
            except Exception as e:
                pass

print(f"Fixed Topic Mismatches: {fixed_mismatch}")
print(f"Fixed H1 Title Overlays: {fixed_h1}")
print("=== DISAMBIGUATION & FRONTMATTER FIXES COMPLETED SUCCESSFULLY ===")
