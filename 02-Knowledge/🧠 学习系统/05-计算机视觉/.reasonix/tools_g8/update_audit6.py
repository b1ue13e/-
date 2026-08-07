import os, sys
sys.stdout.reconfigure(encoding='utf-8')
p = "F:" + os.sep + "-" + os.sep + "03-Projects" + os.sep + "05-计算机视觉" + os.sep + "质量审计" + os.sep + "课程严苛审计.md"
with open(p, encoding='utf-8') as f:
    content = f.read()
marker = "### 2026-08-06 交付检查轮（追加）"
assert marker in content
addition = """**最终整体复审（review 子代理，全课程验收级）与修复**
- 复审印象分 78/100（未达 85），发现并修复 4 项 should-fix + 3 项 minor：
  - upstream 环：感知机→前向传播→MLP 三元环、图像滤波↔傅里叶双向环、计算图依赖倒置 → 已断环，拓扑检测 61 卡无环
  - MOC 漏列已建卡：阶段2 漏列 7 卡（CNN/kNN/Softmax/优化器/学习率/权重初始化/数据管线）、阶段4 漏列 2 卡（Saliency/自监督总卡）、阶段5 漏列 1 卡（相机标定）→ 已补齐，61 卡 100% 在 MOC 中
  - 教材挂载索引作业单元数 5→7（与实际 7 份作业一致）
  - minor：2 卡 prerequisites 旧名（Softmax分类器→Softmax与SVM损失函数）、计算图 prerequisites 去下游
- 复核验证：pytest 1 passed；JSON 69 文件 963 wikilink 断链 0 歧义 0；死链 0；verify_queries 61/61
- 复审通过项确认：61 卡 frontmatter/stage_moc/upstream 全合规、4 起点卡省略正确、无空壳、无静态 downstream、作业 requires 全可解析、覆盖矩阵未夸大

"""
content = content.replace(marker, addition + marker, 1)
with open(p, 'w', encoding='utf-8') as f:
    f.write(content)
print("治理清单最终复审记录已追加")
