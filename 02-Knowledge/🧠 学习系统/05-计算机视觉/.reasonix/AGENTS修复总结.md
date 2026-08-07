---
type: index
topic: "05-计算机视觉 AGENTS.md 修复总结"
course: "05-计算机视觉"
created: 2026-08-06
status: active
flow: project
kind: moc
tags: [审计, 治理, 计算机视觉]
---

# AGENTS.md 全面修复总结：05-计算机视觉

> **修复日期**：2026-08-06
> **修复范围**：02-Knowledge/05-计算机视觉 全部知识卡和 MOC
> **验收等级**：C 级

---

## 修复清单

### Phase 1: Frontmatter 批量修复（55 文件，101 处编辑）

| # | 修复项 | 影响文件 | 状态 |
|:---:|---|---|:---:|
| 1 | course 编码检查 | 63 文件 | ✅ 无需修复（终端渲染误判） |
| 2 | 添加 stage_moc 字段 | 55 张 study 卡 | ✅ 已修复 |
| 3 | 移除静态 downstream | 14 张卡 | ✅ 已修复 |
| 4 | 清理 upstream（移除阶段 MOC） | 14 张卡 | ✅ 已修复 |
| 5 | 移除冗余 assessment_exempt:false | 16 张卡 | ✅ 已修复 |

### Phase 2: Dataview 派生查询

| # | 修复项 | 影响文件 | 状态 |
|:---:|---|---|:---:|
| 6 | 添加下游知识查询 | 55 张卡 | ✅ 已添加 |
| 7 | 添加可完成作业查询 | 55 张卡 | ✅ 已添加 |

### Phase 3: MOC 与导航

| # | 检查项 | 结果 |
|:---:|---|---|
| 8 | 阶段 MOC 表格 wikilink 转义 | ✅ 已合规（无别名链接） |
| 9 | 教材挂载索引管道转义 | ✅ 已转义（前期修复） |
| 10 | 阶段 MOC 作业映射去重 | ✅ 无重复映射 |
| 11 | 课程学习路径导航 | ✅ 导航完整 |

### Phase 4: 归档治理

| # | 检查项 | 结果 |
|:---:|---|---|
| 12 | 空壳文件归档 | ✅ 113 个空壳已归档 |
| 13 | 迁移待办文档 | ✅ 已记录迁移计划 |

---

## 第二轮修复（2026-08-06，AGENTS.md 全面修复优化）

### Phase 1: 作业资产资格审计与清退

| # | 修复项 | 结果 |
|:---:|---|---|
| 1 | 4Tier 说明书 §5.5 审查 | 评分 40/100（<70）→ 清退；价值由 real_assignment_packages 承接 |
| 2 | 17 个占位项目资格审计 | 全部为模板口号（21/100）→ 直接清退 |
| 3 | 快照与恢复安全 | 155 文件 → `.recovery-hold/2026-08-06/05-计算机视觉/`，md5 抽查一致 |
| 4 | 107 处静态死链引用清理 | 92 行脚本删除（54 文件）+ 阶段5 MOC 手工 9 处 + 分隔线整理 |

### Phase 2: 作业体系迁移到 03-Projects/05-计算机视觉/

| # | 修复项 | 结果 |
|:---:|---|---|
| 5 | 新结构创建 | 🧭 课程作业总索引 / 课后作业 / 阶段作业 / 大作业 / 质量审计 / data / scripts / tests |
| 6 | 资产归位 | real_assignment_packages（6 包）整体迁入；capstone 规范命名入大作业/ |
| 7 | 作业 frontmatter | 7 份作业补齐 assignment_id/level/format/stage_id/requires/source_type；requires 21 个知识卡链接全可解析 |
| 8 | 总索引 | 旧课程作业总表 → 🧭 课程作业总索引.md（Dataview 派生看板 + 三级清单） |
| 9 | 旧目录移除 | 03-Projects/课程作业/05-计算机视觉/ 清空删除 |

### Phase 3: 课程导航与知识卡

| # | 修复项 | 结果 |
|:---:|---|---|
| 10 | 学习路径 | 3 处作业链接改指新总索引；开源作业源地图死链删除；阶段0 状态 ✅ |
| 11 | 教材挂载索引 | 2 处链接更新至新结构 |
| 12 | 阶段0 前置 MOC | 补充 §5.1 复用原则 + 诊断入口/最低标准 + 补学顺序 |
| 13 | 空数组清理 | prerequisites: [] 2 处删除 |

### Phase 4: 验证

| # | 检查项 | 结果 |
|:---:|---|---|
| 14 | pytest 知识卡完整性 | `pytest tests/` 1 passed（55 张卡 frontmatter/stage_moc/upstream/空壳/表格转义） |
| 15 | verify_links_and_paths | 03-Projects 作业文件断链 0；课程内 657 条历史链接欠债记录 G8 |
| 16 | scan_placeholders | 0 空壳 |
| 17 | 作业目录审计工具 | 旧结构工具报错 = 工具噪声（G9） |
| 18 | 课程严苛审计 | 质量审计/课程严苛审计.md：G1-G9 治理清单 + C 级验收 82/100 |

---

## 验证结果（第二轮）

- **study 卡总数**：55，frontmatter/stage_moc/upstream/空壳/表格转义全部合规（`pytest tests/` 1 passed）
- **作业体系**：03-Projects/05-计算机视觉/ 新结构 + 7 份规范作业 + 6 作业包；作业文件断链 0
- **历史链接欠债**：657 条记录至治理清单 G8（本轮未批量处理）
- **工具噪声**：audit_course_homework_catalogs/audit_formal_homework_packs 对新结构报错（G9）

---

## 交付检查轮补充（2026-08-06）

- 全库索引修复：`33门课程完整作业包索引.md` / `33门课程正式作业索引.md` 05 行路径更新至新结构；全库旧路径残留清零
- 阶段1-4 MOC「阶段验收与作业」空小节 → Dataview 派生查询（5 个 MOC 全覆盖）
- `audit_course_execution_routes.py`：学习路径补「开源自学执行方案」链接（9 项 FAIL 修复 1 项，其余 8 项记录 G10）
- MOC 注册表（开放教材主线注册表/挂载总地图/来源白名单）引用核对一致
- `verify_queries.py`：55/55 张 study 卡含 upstream/requires 派生查询
- 学习路径/教材挂载索引 `updated` 字段更新至 2026-08-06
- 清理：`.reasonix/tmp`、`.pytest_cache`、`__pycache__`、`.pyc` 清零

## 第三轮补充（2026-08-06，G8 链接欠债全面修复）

- **G8 处置**：733 处死链 / 312 个唯一目标全部处理 → 复扫死链 0
  - 替换 581 处（相对路径规范化、旧概念名映射、跨课程映射、书库 PDF→书籍笔记、归档空壳→正式卡）
  - 去链接 102 处（计划性概念保留文字）；表格 ⬜ 规划行 159 处转纯文本占位
  - 脚本修正：围栏跳过、`\\|` 转义识别、回写 bug、RELPATH 抢占反向修复
- **MOC 一致性**：LoRA 状态 ⬜→✅；阶段0 补「阶段验收与作业」小节；12 个 MOC 链接/列数全合规
- **验证**：verify_links_and_paths 63 文件 836 wikilink 断链 0 歧义 0；pytest 1 passed；verify_links_cv 全部通过
- 治理清单同步：`课程严苛审计.md` G8 → ✅ 已处理

## 交付检查轮补充（2026-08-06，第二轮）

- **全库索引**：33门课程完整作业包索引 L37 / 正式作业索引 L33 05 行指向新结构 ✅；`33门课程开源自学与验收总索引` L72 G4 残留死链（`🧭 计算机视觉开源作业源地图`）→ 改指学习路径；该索引其余 9 处断链均为其他课程框架页死链（历史欠债，记录 G6 类不处理）
- **MOC 注册表**：开放教材主线注册表 L33 / 挂载总地图 L28 / 来源白名单 L35 对 05 引用一致可解析（JSON 3 文件 77 链接仅 2 处时间序列分析死链，非本课程）
- **派生查询**：`verify_queries.py` 55/55 study 卡含 upstream/requires 派生查询
- **G10 状态**：③ 学习路径执行方案链接 ✅ 已修；①教材挂载索引 frontmatter 字段 + ②执行区术语为全库统一模板版本问题（抽查 08-NLP全栈/17-机器学习/03-量化金融 同样缺失），仅记录
- **清理**：tests/.pytest_cache、__pycache__、课程根缓存删除；`.reasonix/tmp`（35 文件）清空，8 个核心修复脚本归档至 `.reasonix/tools_g8/`；清理后 pytest 1 passed
- 治理清单与验收记录已同步（G8 → ✅、评分 85/100、复审修复记录归档）

## 第四轮补充（2026-08-06，upstream 补齐 + 高优先级概念建卡）

- **upstream 字段补齐**：42 张无 upstream 卡逐卡分析 §3 前置 → 38 张补全（完整路径 wikilink），4 张起点卡省略；51+4=55 张全合规（AGENTS.md §3）
- **高优先级概念建卡（6 张）**：DETR、知识蒸馏（阶段3）；DeiT、CLIP 独立卡（阶段4）；TensorRT、目标跟踪（阶段5）——均按模板 0-13 章节完整编写（9.6-11KB）
- **MOC 与覆盖矩阵**：6 行 ⬜→✅ 回填；覆盖矩阵更新（阶段3 65%、阶段4 60%、阶段5 45%）；study 卡 55→61
- **验证**：pytest 1 passed（断言更新为 ≥55）；JSON 69 文件 948 wikilink 断链 0 歧义 0；死链扫描 0；verify_queries 61/61
- 治理清单第四轮记录已归档

## 第四轮交付检查补充（2026-08-06）

- **独立复审（review 子代理）**：结论 pass 可发布，无 blocker/should-fix；3 处 minor 全部修复：
  - 阶段5 知识蒸馏行 ⬜→✅ 指向阶段3 知识蒸馏卡；阶段3 U-Net 行 ⬜→✅ 指向语义分割与UNet
  - CLIP upstream 补 Softmax与SVM损失函数（§3 声明但遗漏）
- **MOC 一致性扫描**：额外修复 2 处（阶段2 几何变换→几何变换CV、阶段3 迁移学习→迁移学习与微调）；确认 LeNet/Panoptic FPN 无对应卡保持 ⬜ 正确
- **复审确认**：6 张新卡公式无误（匈牙利匹配/InfoNCE/温度softmax/BN折叠）、upstream 全部指向真实直接前置、文件 UTF-8 完好（grep 乱码为环境 GBK 显示缺陷非文件损坏）
- **最终验证**：pytest 1 passed；verify_links_cv 61 卡通过；死链 0；verify_queries 61/61；upstream 覆盖 57 含 + 4 起点省略 = 61 张全合规；MOC 断链 0、表格列数一致
- 清理：tests 缓存删除；.reasonix/tools_g8/ 保留 15 个修复脚本归档

## 最终整体复审（2026-08-06，全课程验收级）

- **review 子代理整体复审**：印象分 78/100 → 修复 should-fix 后 **88/100（达 85 门槛）**
- **4 项 should-fix 修复**：
  - upstream 环：感知机三元环（→线性代数/梯度下降）、图像滤波↔傅里叶双向环、计算图依赖倒置 → 拓扑检测 61 卡无环
  - MOC 漏列 10 张已建卡：阶段2 七卡（CNN/kNN/Softmax/优化器/学习率/权重初始化/数据管线）、阶段4 两卡、阶段5 一卡 → 61 卡 100% MOC 覆盖
  - 教材挂载索引作业单元数 5→7；2 卡 prerequisites 旧名修正
- **minor 收尾**：Transformer prerequisites 卡名规范化、6 文件进度条口径（计入 ongoing）、CIFAR-10 project_type 位置统一、学习路径图例补 🔒
- **最终验证**：pytest 1 passed；JSON 69 文件 963 wikilink 断链 0 歧义 0；死链 0；verify_queries 61/61
- **7 个检查点提交**：cc7ce59 → 0d24706 → 07a6c65 → 226a786 → dc50993 → b1b322b → 3e6326c
- 注：C 级复审（当前环境无独立模型，A/B 级需独立会话/模型环境）

---

## 验证结果（第一轮）

- **study 卡总数**：55
- **缺失 stage_moc**：0
- **残留 static downstream**：0
- **包含 Dataview 查询**：55/55

---

## AGENTS.md 合规状态

| 规则条款 | 状态 |
|:---|:---:|
| §3: stage_moc 必填 | ✅ |
| §2: downstream 反向查询 | ✅ |
| §3: upstream 不含阶段 MOC | ✅ |
| §3: 不写无信息量默认值 | ✅ |
| §2: 知识卡可用派生视图 | ✅ |
| §2: 课程学习路径只维护有序阶段 | ✅ |
| §5.3: 归档目录排除 | ✅ |

---

## 已知限制

- 审计工具 scan_frontmatter.py 硬编码 ROOT 为 tools 目录，无法从课程目录调用
- audit_course_homework_catalogs.py / audit_formal_homework_packs.py 硬编码旧结构 `03-Projects/课程作业/`，对已迁移的新结构 `03-Projects/<课程>/` 报 missing catalog（G9，待全库工具统一适配）
- audit_course_execution_routes.py 对 05-计算机视觉 剩余 8 项 FAIL：教材挂载索引 frontmatter 缺 `resource_policy_version/spine_url/spine_mirror_policy` 且 updated 非 2026-07-28、执行区缺 Spine 声明/最小证据/强验证/失败条件术语（G10，全库统一模板版本问题；学习路径执行链接已补）
- 教材挂载索引中 `\\|` 双反斜杠转义为前期脚本产物，Obsidian 内渲染正常
- 课程知识卡正文 657 处历史链接欠债（相对路径风格 + 计划性概念短链接）记录于治理清单 G8，未在本轮批量处理

---

*报告生成：2026-08-06*
