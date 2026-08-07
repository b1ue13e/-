# 15-控制与机器人学 项目长期记忆

## 课程身份

- 正式路线编号：`15-控制与机器人学`，入口 `🗺️ 控制与机器人学学习路径.md`，已在 `99-System/tools/audit_course_execution_routes.py` 注册。
- 知识目录：`02-Knowledge/🧠 学习系统/15-控制与机器人学/`（11 阶段 + 00-前置知识 + 知识地图）。
- 项目目录：`03-Projects/系统与硬件/15-控制与机器人学/`（课后作业/阶段作业/大作业/质量审计）。

## 来源架构（2026-08-06 确定）

- 主 Spine：Modern Robotics（Lynch & Park）+ PythonRobotics（实践），Co-Spine：Modern Control Engineering（Ogata），Supplement：MIT 6.832 Underactuated、Probabilistic Robotics。详见教材挂载索引。

## 结构约定（重构后）

- 阶段 MOC 必须命名 `🧭 阶段N-名称.md`（预检脚本以 `🧭*.md` 识别）；知识卡归入具体阶段目录，根目录不堆放知识卡。
- 作业唯一事实源在 03-Projects `🧭 课程作业总索引.md`；作业 `requires` 关联已教授知识卡。
- 前置复用跨课程卡（高代/概率/Python），不重复建卡；前置 MOC：`00-前置知识/🧭 控制与机器人学-前置知识.md`。

## 执行状态（断点）

- 2026-08-06 完成 B0-B5（结构治理 + 前置 + 学习路径 + 阶段1 全部 20 卡），checkpoint `515daa4`。
- 待续：B6-B9 阶段 2-11 逐卡生产（约 293 张占位卡）、HW02-HW06 作业、B10 全量验证与 A/B 级正式验收。
- 唯一执行清单：`03-Projects/系统与硬件/15-控制与机器人学/质量审计/课程重构执行清单.md`。

## 环境经验

- Windows 中文/emoji 文件名带 VS16 变体选择符与全角冒号，重命名须用 pathlib glob + 正则。
- 审计脚本 `audit_course_execution_routes.py` 第 126 行存在历史路径拼接 bug（全仓 FAIL 属工具噪声）。
- 运行仓库 Python 审计需先装 pyyaml（venv：`C:\Users\DELL\.workbuddy\binaries\python\envs\default`）。
