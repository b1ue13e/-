# 17-机器学习 · 项目长期记忆

## 作业体系结构（2026-08-06 确立）

- **唯一规范目录**：`03-Projects/17-机器学习/`。子目录 `课后作业/`（lesson）、`阶段作业/`（stage）、`大作业/`（capstone）即规模层级，不新增第四种。
- **课程主线**：周志华《机器学习》经典 ML 五阶段（基础概念 / 线性模型 / 正则优化 / 树与集成 / 其他方法）。作业按此五阶段对齐。
- **DL 专题支线**：李宏毅 ML2021 深度学习系列（CNN/Transformer/GAN/BERT/自编码器/图神经/RL/元学习等）依赖的 DL 知识卡不在主线内，已整体降级为可选参考，存于 `03-Projects/17-机器学习/专题支线/深度学习/`（`type: reference`，不计入主索引与正式验收）。若纳入正式课程，需先建第 6 阶段「深度学习」并补建对应知识卡，再按 AGENTS §5.5 审查。
- **作业总索引**：`03-Projects/17-机器学习/🧭 课程作业总索引.md`，Dataview 按三个固定子目录查询，不查整棵 `03-Projects/17-机器学习`，以免纳入专题支线。
- **知识卡「学完后可以完成」**：由 Dataview 反查作业 `requires` 自动生成；作业 `requires` 是唯一事实源，知识卡不反写作业链接。
- **旧遗留已清理**：`03-Projects/课程作业/17-机器学习/`（旧 `课程作业总表.md` 等）已迁至 `.recovery-hold/2026-08-06/ml-legacy-coursework/`，消除 preflight 的 `PROJECT_AMBIGUOUS`。
- **未决**：A/B 级独立复审环境不支持 → 课程正式发布未完成。

## DL 专题支线 §5.5 收尾（2026-08-06 续做）

- **已合规项（frontmatter + 链接层 + Round1 优化）**：`assignment_id` 已重编号为 `机器学习-DL-01..14`（避免与主线 01–09 冲突）；`stage_id` 统一为 `专题`；新增 `source_license_status: "待验证"`（上游课程主页无 license 声明，已 WebFetch 核验）；`license` 仅描述本仓库用法；14 份均含「数据/Starter 占位说明」「最低通过门槛」、统一 16 节结构（GNN 已重写对齐）；72 张知识卡反向查询加 `type=project` 过滤。严苛复评 **94/100（A 级，≥90 达标）**。
- **仍递延（历史欠债，需建第 6 阶段「深度学习」根治）**：题目正文为改编原稿未逐题重审；`requires` 暂只能挂经典 ML 卡（DL 专属前置卡未建）；无真实内置数据集/Starter（已诚实标注占位）。这些为有意递延项，不影响 ≥90 结论。
- **preflight 不扫专题支线**：`preflight_course.py` 的 `audit_project` 只查 `课后作业/阶段作业/大作业` 三固定目录，故 14 份 DL `type:reference` 文件不计入 `assignment_files`（主线程仍为 15 份、errors:0/warnings:0）。DL 文件的正文 wikilink 也未被 preflight 校验，需自写脚本扫链接。

## 关键运维事实（避免重复踩坑）

- **Vault 根目录是 `F:/-/`，不是 `F:/`**。`F:/02-Knowledge/🧠 学习系统/17-机器学习` 是根下一份**空/陈旧镜像**；真实课程在 `F:/-/02-Knowledge/🧠 学习系统/17-机器学习`（知识卡）与 `F:/-/03-Projects/17-机器学习`（作业）。运行 `preflight_course.py` 必须用 `--vault "F:/-"`，否则会解析到空镜像报 `LEARNING_PATH_COUNT` / `PROJECT_NOT_RESOLVED`。
- 自写链接校验脚本时，对整棵 `F:/` rglob 极慢（含大量无关目录）；应只扫 `F:/-/02-Knowledge` 与 `F:/-/03-Projects` 两棵树。
