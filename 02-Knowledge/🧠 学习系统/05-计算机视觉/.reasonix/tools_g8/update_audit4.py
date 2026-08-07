import os, sys
sys.stdout.reconfigure(encoding='utf-8')
p = "F:" + os.sep + "-" + os.sep + "03-Projects" + os.sep + "05-计算机视觉" + os.sep + "质量审计" + os.sep + "课程严苛审计.md"
with open(p, encoding='utf-8') as f:
    content = f.read()

# 追加第四轮修复记录（放在 "### 2026-08-06 交付检查轮（追加）" 之前）
marker = "### 2026-08-06 交付检查轮（追加）"
assert marker in content
addition = """### 2026-08-06 第四轮：upstream 补齐 + 高优先级概念建卡（C 级，非独立复审）

**upstream 字段补齐（AGENTS.md §3 合规）**
- 审计发现：55 张 study 卡中 42 张无 upstream 数组（约 20 张正文 §3 有明确前置但未声明），违反"存在直接前置时 upstream 必须非空"
- 逐卡分析 §3 前置声明后补全 38 张（直接前置，完整路径 wikilink），4 张真正起点卡（线性代数基础CV/图像表示/梯度下降CV/概率分布CV）保持省略
- 幂等修复：去除映射表重复项、修正 upstream 元素 `[[ ]]` 包裹格式
- 结果：51 张含 upstream + 4 张起点省略 = 55 张全合规；pytest 与 verify_links_cv 通过

**高优先级概念建卡（覆盖矩阵缺口，逐卡编写）**
- 新增 6 张 study 卡（按深度学习模板 0-13 章节完整编写，9.6-11KB）：
  - 阶段3：DETR（Carion 2020）、知识蒸馏（Hinton 2015）
  - 阶段4：DeiT（Touvron 2021）、CLIP 独立卡（Radford 2021）
  - 阶段5：TensorRT（NVIDIA 文档）、目标跟踪（SORT/DeepSORT）
- 每张含：问题动机/正式定义/公式推导/基础+中等+应用例子/误区表/闭卷复现/5 道自测/派生查询
- 阶段 MOC 6 行 ⬜→✅ 回填；覆盖矩阵更新（阶段3 55%→65%、阶段4 50%→60%、阶段5 30%→45%）
- study 卡 55 → 61；测试断言 `== 55` → `>= 55`（新增卡属正常演化）

**验证**
- pytest 1 passed（61 卡 frontmatter/stage_moc/upstream/空壳/表格转义全合规）
- verify_links_and_paths JSON：69 文件 948 wikilink 断链 0 歧义 0
- 精确扫描死链 0；verify_queries 61/61 派生查询

"""
content = content.replace(marker, addition + marker, 1)
with open(p, 'w', encoding='utf-8') as f:
    f.write(content)
print("治理清单第四轮记录已追加")
