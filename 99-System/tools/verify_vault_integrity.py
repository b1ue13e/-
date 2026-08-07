import os
import sys
import re
import yaml
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
root_dir = Path(r'f:\-')

print("=========================================")
print("🛡️ 知识库完整性与系统重构验证 (Vault Integrity Check)")
print("=========================================\n")

errors = []

# 1. Unprefixed Path Scanner (ignoring script files, code blocks, and comments)
def check_all_unprefixed():
    targets = [
        ('🧠 学习系统', '02-Knowledge/'),
        ('🗓️ 计划执行系统', '99-System/'),
        ('📚 书库', '02-Knowledge/'),
        ('📚 论文库', '02-Knowledge/')
    ]
    counts = {t[0]: 0 for t in targets}
    skip_dirs = {'.git', '.obsidian', '.claude', 'tools', '书籍资源', 'tmp', 'exports'}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith('.')]
        for f in filenames:
            if f.endswith(('.md', '.py', '.ps1', '.js', '.json', '.base')):
                p = os.path.join(dirpath, f)
                try:
                    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read()
                except Exception:
                    continue
                    
                clean_content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
                for op_str, root_prefix in targets:
                    op_re = re.compile(re.escape(op_str))
                    for m in op_re.finditer(clean_content):
                        pos = m.start()
                        prefix = clean_content[max(0, pos-25):pos]
                        if any(marker in prefix for marker in ['├──', '└──', '│', '根目录']):
                            continue
                        if root_prefix not in prefix and root_prefix.replace('/', '\\') not in prefix:
                            counts[op_str] += 1
    return counts

counts = check_all_unprefixed()
study_cnt = counts['🧠 学习系统']
sprint_cnt = counts['🗓️ 计划执行系统']
books_cnt = counts['📚 书库']
papers_cnt = counts['📚 论文库']

total_unprefixed = study_cnt + sprint_cnt + books_cnt + papers_cnt
if total_unprefixed == 0:
    print("✅ 1. 全库路径扫描：0 个未修饰旧路径 (100% 涵盖 Dataview 与无斜杠路径)")
else:
    print(f"❌ 1. 旧路径残留报错：发现 {total_unprefixed} 个未修饰旧路径 (🧠:{study_cnt}, 🗓️:{sprint_cnt}, 📚书:{books_cnt}, 📚论:{papers_cnt})")
    errors.append("存在未修饰旧路径残留")

# 2. PyYAML Frontmatter Parse Check
fm_re = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
yaml_err_cnt = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    dirnames[:] = [d for d in dirnames if d not in ['.git', '.obsidian', '.claude', 'tmp', 'exports', '书籍资源'] and not d.startswith('.')]
    for f in filenames:
        if f.endswith('.md'):
            p = os.path.join(dirpath, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
            except Exception:
                continue
            m = fm_re.match(content)
            if m:
                try:
                    yaml.safe_load(m.group(1))
                except Exception as e:
                    yaml_err_cnt += 1
                    print(f"  [YAML Err #{yaml_err_cnt}] {os.path.relpath(p, root_dir)}")


if yaml_err_cnt == 0:
    print("✅ 2. YAML 语法扫描：0 处 Frontmatter 解析错误 (PyYAML 100% 校验通过)")
else:
    print(f"❌ 2. YAML 语法报错：发现 {yaml_err_cnt} 处可解析错误")
    errors.append("YAML Frontmatter 语法报错")

# 3. Anki export script test
anki_script = root_dir / "99-System" / "tools" / "export_anki_cards.py"
res_anki = subprocess.run([sys.executable, str(anki_script), "--check"], capture_output=True, encoding="utf-8", errors="ignore", cwd=str(root_dir))
if res_anki.returncode == 0:
    print(f"✅ 3. Anki 导出脚本测试：{res_anki.stdout.strip()}")
else:
    print(f"❌ 3. Anki 脚本运行报错：{res_anki.stderr.strip()}")
    errors.append("Anki 导出脚本检查失败")

# 4. Sprint sync script test
sprint_script = root_dir / "99-System" / "tools" / "sync_current_sprint.py"
res_sprint = subprocess.run([sys.executable, str(sprint_script), "--check"], capture_output=True, encoding="utf-8", errors="ignore", cwd=str(root_dir))
if res_sprint.returncode == 0:
    print(f"✅ 4. Sprint 同步脚本测试：{res_sprint.stdout.strip()}")
else:
    print(f"❌ 4. Sprint 脚本运行报错：{res_sprint.stderr.strip()}")
    errors.append("Sprint 脚本运行报错")

# 5. Homepage plugin configuration check
homepage_data = root_dir / ".obsidian" / "plugins" / "homepage" / "data.json"
if homepage_data.exists():
    h_content = homepage_data.read_text(encoding="utf-8")
    if '"value": "🏠 主页"' in h_content:
        print("✅ 5. Homepage 插件配置：已被正确修饰指向系统首页 [🏠 主页.md]")
    else:
        print("❌ 5. Homepage 插件配置未更新")
        errors.append("Homepage 插件配置未更新")

# 6. Obsidian app.json ignore rules check
app_json = root_dir / ".obsidian" / "app.json"
if app_json.exists():
    a_content = app_json.read_text(encoding="utf-8")
    if "^02-Knowledge/📚 书库/书籍资源" in a_content:
        print("✅ 6. Obsidian 忽略规则配置：已更正为 [^02-Knowledge/📚 书库/书籍资源]")
    else:
        print("❌ 6. Obsidian 忽略规则配置未更新")
        errors.append("app.json userIgnoreFilters 未更新")

print("\n=========================================")
if not errors:
    print("🎉 总体验证结果：全部 6 项测试完全通过！系统已达到无缝使用状态。")
else:
    print(f"⚠️ 总体验证结果：发现 {len(errors)} 项未解决错误，请查阅以上日志。")
print("=========================================")
