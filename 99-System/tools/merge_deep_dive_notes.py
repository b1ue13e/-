import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

deep_dive_files = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    if any(x in dirpath for x in ['.git', '.obsidian', '.claude']): continue
    for f in filenames:
        if f.endswith('-深挖.md'):
            deep_dive_files.append(os.path.join(dirpath, f))

print(f"Found {len(deep_dive_files)} *-深挖.md notes to merge.")

link_replacements = {}
merged_count = 0

for deep_path in deep_dive_files:
    deep_name = os.path.basename(deep_path)
    main_name = deep_name.replace('-深挖.md', '.md')
    main_path = os.path.join(os.path.dirname(deep_path), main_name)
    
    deep_stem = deep_name.replace('.md', '')
    main_stem = main_name.replace('.md', '')
    link_replacements[deep_stem] = main_stem
    
    if not os.path.exists(main_path):
        print(f"⚠️ Main card does not exist for {deep_name}: expected {main_path}")
        continue
        
    # Read deep dive note
    with open(deep_path, 'r', encoding='utf-8', errors='ignore') as f:
        deep_content = f.read()
        
    # Strip frontmatter from deep dive
    deep_body = re.sub(r'^---.*?---\s*\n?', '', deep_content, flags=re.DOTALL).strip()
    # Strip H1 heading from deep dive body if present
    deep_body = re.sub(r'^#\s+.*?\n+', '', deep_body).strip()
    
    # Read main card
    with open(main_path, 'r', encoding='utf-8', errors='ignore') as f:
        main_content = f.read()
        
    # Append deep dive content to main card if not already appended
    if "## 💡 深度拓展与推导" not in main_content and len(deep_body) > 50:
        merged_main = main_content.rstrip() + "\n\n---\n\n## 💡 深度拓展与推导\n\n" + deep_body + "\n"
    else:
        merged_main = main_content
        
    # Write merged main card
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(merged_main)
        
    # Delete deep dive file
    os.remove(deep_path)
    print(f"✅ [合并与擦除] {deep_name} -> {main_name}")
    merged_count += 1

print(f"\nSuccessfully merged and removed {merged_count} deep dive notes.")

# Replace vault-wide wikilinks to deep dive notes
print("\nUpdating vault-wide wikilinks...")
updated_links_cnt = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    if any(x in dirpath for x in ['.git', '.obsidian', '.claude']): continue
    for f in filenames:
        if f.endswith(('.md', '.json', '.py')):
            p = os.path.join(dirpath, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
            except Exception: continue
            
            new_c = content
            for deep_s, main_s in link_replacements.items():
                new_c = new_c.replace(f"[[{deep_s}]]", f"[[{main_s}]]")
                new_c = new_c.replace(f"[[{deep_s}|", f"[[{main_s}|")
                
            if new_c != content:
                with open(p, 'w', encoding='utf-8') as fp:
                    fp.write(new_c)
                updated_links_cnt += 1

print(f"Updated wikilinks in {updated_links_cnt} files.")

