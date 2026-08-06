# HW06 开放课程项目 Real Assignment Package

这是一份面向学生自做的 `HW06` 真实作业包，不再只是说明页。

## 布置时机

课程后段，学生已完成前五份作业，具备最小 baseline、对照、分析与工程组织能力。

## 包内结构

- `starter/`：专题 starter、运行入口与数据检查脚本
- `baseline/`：baseline 记录位，不提供教师答案
- `tests/`：最小 smoke test
- `reports/`：正式报告模板
- `data_card.md`：真实数据契约与 smoke 数据说明
- `rubric.md`：评分量表
- `package_manifest.json`：包元数据和 smoke 文件清单

## 前置知识

- `baseline 与改进公平对照`
- `proposal / milestone / final report 结构`
- `失败样本与边界分析`

## 教学目标

- 会定义一个合适的视觉问题并给出 baseline
- 会按 proposal -> milestone -> final report 推进项目
- 会说明项目结论、失败与下一步

## 真实数据契约

预期真实数据目录：

`F:\-\03-Projects\data\computer_vision\hw06_open_course_project`

真实数据到位后，至少应包含：

- `project_manifest.json`
- `baseline_results.csv`
- `improvement_results.csv`
- `risk_log.md`

## 当前 smoke 数据

当前包自带最小 smoke 数据，用于验证流程能否跑通：

- `project_plan.smoke.json`
- `baseline_results.smoke.csv`
- `improvement_results.smoke.csv`

## 运行方式

```bash
python "f:\-\03-Projects\课程作业\05-计算机视觉\real_assignment_packages\hw06_open_course_project\starter\run.py" --input-dir "f:\-\03-Projects\data\computer_vision\hw06_open_course_project" --output-dir "f:\-\03-Projects\课程作业\05-计算机视觉\real_assignment_packages\hw06_open_course_project\your_outputs"
python "f:\-\03-Projects\课程作业\05-计算机视觉\real_assignment_packages\hw06_open_course_project\starter\check_data.py" --input-dir "f:\-\03-Projects\data\computer_vision\hw06_open_course_project"
pytest "f:\-\03-Projects\课程作业\05-计算机视觉\real_assignment_packages\hw06_open_course_project\tests"
```

## 当前 baseline 定位

- 本作业包不附带教师最终答案。
- `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
- 当前 baseline 主题：`课程项目 baseline + 一项清楚的改进尝试`

## 下一步建议

把 smoke 计划与结果表替换成真实项目资料，再补正式实验日志、风险追踪和最终报告。


    ## 额外教师资产

    - `proposal_template.md`：proposal 模板
    - `milestone_template.md`：milestone 模板
    - `ta_grading_template.md`：助教批改模板
    - `topic_boundary.md`：允许选题 / 不建议选题边界
    - `risk_casebook.md`：项目风险样例库
