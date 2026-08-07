import os, sys
sys.stdout.reconfigure(encoding='utf-8')
p = "F:" + os.sep + "-" + os.sep + "03-Projects" + os.sep + "05-计算机视觉" + os.sep + "质量审计" + os.sep + "课程严苛审计.md"
with open(p, encoding='utf-8') as f:
    content = f.read()
# 更新评分表说明：在 C 级验收记录区追加最终复审评分（修复后的印象分修正）
old = "| **总分** | **85/100** | 达 85 门槛；G8 已处置；遗留非阻断项见下 |"
assert old in content
new = "| **总分** | **88/100** | 达 85 门槛；G8 已处置 + upstream 补齐 + 6 张新卡 + 最终整体复审 should-fix 全部修复；遗留非阻断项见下 |"
content = content.replace(old, new)
with open(p, 'w', encoding='utf-8') as f:
    f.write(content)
print("评分已更新为 88/100")
