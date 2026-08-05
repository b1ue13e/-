from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from textwrap import dedent


ROOT = Path(r"f:\-")
PACKAGES_ROOT = ROOT / "03-Projects" / "课程作业" / "05-计算机视觉" / "real_assignment_packages"
DATA_ROOT = ROOT / "03-Projects" / "data" / "computer_vision"
GENERATED_AT = "2026-08-01"


PACKAGES = [
    {
        "id": "HW01",
        "slug": "hw01_cifar10_knn_softmax",
        "title": "CIFAR-10 kNN 与 Softmax 基线",
        "stage": "第一阶段：视觉分类与实验协议",
        "assigned_when": "U02 结束后，学生刚完成图像数据表示、线性分类和最小评测协议。",
        "prerequisites": [
            "NumPy 向量化",
            "训练/验证/测试切分",
            "距离度量与线性分类",
        ],
        "goals": [
            "会在固定协议下组织 kNN 与 Softmax 基线",
            "会做最小公平对照和失败样本审计",
            "知道为什么 CNN 需要建立在稳定 baseline 之上",
        ],
        "baseline": "kNN + 线性 Softmax",
        "next_step": "把 smoke 特征替换成真实 CIFAR-10 特征或图像张量，再补完整训练与误差分析。",
        "real_files": ["cifar10.train.npz", "cifar10.val.npz", "label_map.json"],
        "smoke_files": ["train.smoke.csv", "val.smoke.csv"],
        "data_dir_name": "hw01_cifar10_knn_softmax",
        "starter_module": "knn_softmax.py",
        "summary_key": "classification_summary",
        "summary_file": "classification_summary.json",
        "report_prompt": "比较 kNN 和 Softmax 的差异，并解释哪些失败样本提示后续需要更强模型。",
    },
    {
        "id": "HW02",
        "slug": "hw02_two_layer_backprop",
        "title": "两层网络与反向传播正确性验证",
        "stage": "第二阶段：训练正确性与调试",
        "assigned_when": "U03 前半段，学生已完成线性基线并学完反向传播、梯度检查和小样本过拟合。",
        "prerequisites": [
            "链式法则与计算图",
            "数值梯度与解析梯度",
            "小样本过拟合测试",
        ],
        "goals": [
            "会独立实现两层网络前向和反向传播",
            "会做梯度检查和过拟合烟雾测试",
            "能区分实现错误、协议错误和调参问题",
        ],
        "baseline": "两层全连接网络 + 梯度检查",
        "next_step": "把 smoke batch 换成真实 CIFAR-10 小批量，再补完整网络训练与日志记录。",
        "real_files": ["cifar10_subset.train.npz", "cifar10_subset.val.npz", "network_config.json"],
        "smoke_files": ["tiny_batch.smoke.csv", "overfit_batch.smoke.csv"],
        "data_dir_name": "hw02_two_layer_backprop",
        "starter_module": "two_layer_net.py",
        "summary_key": "training_summary",
        "summary_file": "training_summary.json",
        "report_prompt": "解释梯度检查、小样本过拟合和正式训练各自验证的是什么。",
    },
    {
        "id": "HW03",
        "slug": "hw03_cnn_training_engineering",
        "title": "小型 CNN 与训练工程",
        "stage": "第三阶段：CNN 训练闭环与日志",
        "assigned_when": "U03 结束后，学生刚完成卷积、池化、数据增强和最小训练循环。",
        "prerequisites": [
            "卷积与池化",
            "优化器与学习率",
            "训练日志与混淆矩阵",
        ],
        "goals": [
            "会组织 CNN 的最小训练、评测和日志闭环",
            "会与 HW01/HW02 的基线做公平对照",
            "会记录训练问题和失败样本",
        ],
        "baseline": "小型 CNN 风格特征 + 线性头",
        "next_step": "把 smoke 图像替换成真实 CIFAR-10 图像张量，再补真实 CNN 训练、增强和误差审计。",
        "real_files": ["cifar10_images.train.npz", "cifar10_images.val.npz", "label_map.json"],
        "smoke_files": ["train.smoke.csv", "val.smoke.csv"],
        "data_dir_name": "hw03_cnn_training_engineering",
        "starter_module": "cnn_pipeline.py",
        "summary_key": "cnn_summary",
        "summary_file": "cnn_summary.json",
        "report_prompt": "解释 CNN 相比 HW01/HW02 的提升、代价，以及当前训练中暴露出的不稳定现象。",
    },
    {
        "id": "HW04",
        "slug": "hw04_transfer_learning_error_analysis",
        "title": "迁移学习与误差分析",
        "stage": "第四阶段：冻结、微调与误差审计",
        "assigned_when": "U04 前半段，学生已完成基础 CNN 训练，并开始比较预训练特征迁移和微调。",
        "prerequisites": [
            "预训练与特征迁移",
            "冻结层与微调策略",
            "类别级误差分析",
        ],
        "goals": [
            "会组织冻结特征与微调的公平对照",
            "会同时报告效果提升与训练成本",
            "会做类别级误差分析和失败审计",
        ],
        "baseline": "预训练 backbone + 冻结头 / 微调对照",
        "next_step": "把 smoke 分数表替换成真实迁移学习训练日志，再补完整 backbone、类别级混淆矩阵与失败样本图库。",
        "real_files": ["cifar10_transfer.train.npz", "cifar10_transfer.val.npz", "label_map.json", "transfer_config.json"],
        "smoke_files": ["train.smoke.csv", "val.smoke.csv"],
        "data_dir_name": "hw04_transfer_learning_error_analysis",
        "starter_module": "transfer_analysis.py",
        "summary_key": "transfer_summary",
        "summary_file": "transfer_summary.json",
        "report_prompt": "比较冻结与微调的差异，并解释哪些类别改善了、哪些类别仍然顽固，以及这是否值得额外成本。",
    },
    {
        "id": "HW05",
        "slug": "hw05_pascal_voc_detection_pkg",
        "title": "Pascal VOC 最小目标检测工程包",
        "stage": "第五阶段：检测工程闭环",
        "assigned_when": "U05 开始时，学生已完成分类与迁移学习分析，开始进入更完整的视觉工程协议。",
        "prerequisites": [
            "边界框与 IoU",
            "NMS 与最小检测评测",
            "训练、评测与可视化入口组织",
        ],
        "goals": [
            "会搭建最小目标检测工程包",
            "会在固定协议下完成训练、评测和可视化闭环",
            "会分析错检、漏检与检测任务边界",
        ],
        "baseline": "最小检测器 + IoU@0.5 评测",
        "next_step": "把 smoke 标注替换成真实 Pascal VOC 子集，再补正式训练配置、日志导出与可视化产物。",
        "real_files": ["voc_annotations.train.json", "voc_annotations.val.json", "detection_config.json", "label_map.json"],
        "smoke_files": ["train.smoke.csv", "val.smoke.csv"],
        "data_dir_name": "hw05_pascal_voc_detection_pkg",
        "starter_module": "detection_pipeline.py",
        "summary_key": "detection_summary",
        "summary_file": "detection_summary.json",
        "report_prompt": "解释当前最小检测工程包能跑通到哪一步，主要失败模式是什么，以及第一步最该改什么。",
    },
    {
        "id": "HW06",
        "slug": "hw06_open_course_project",
        "title": "开放课程项目",
        "stage": "第六阶段：课程综合项目",
        "assigned_when": "课程后段，学生已完成前五份作业，具备最小 baseline、对照、分析与工程组织能力。",
        "prerequisites": [
            "baseline 与改进公平对照",
            "proposal / milestone / final report 结构",
            "失败样本与边界分析",
        ],
        "goals": [
            "会定义一个合适的视觉问题并给出 baseline",
            "会按 proposal -> milestone -> final report 推进项目",
            "会说明项目结论、失败与下一步",
        ],
        "baseline": "课程项目 baseline + 一项清楚的改进尝试",
        "next_step": "把 smoke 计划与结果表替换成真实项目资料，再补正式实验日志、风险追踪和最终报告。",
        "real_files": ["project_manifest.json", "baseline_results.csv", "improvement_results.csv", "risk_log.md"],
        "smoke_files": ["project_plan.smoke.json", "baseline_results.smoke.csv", "improvement_results.smoke.csv"],
        "data_dir_name": "hw06_open_course_project",
        "starter_module": "open_project.py",
        "summary_key": "project_summary",
        "summary_file": "project_summary.json",
        "report_prompt": "说明 baseline 为什么合理、改进是否真的有效，以及项目还缺什么证据才能继续扩题。",
    },
]


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = dedent(content).strip() + "\n"
    if path.suffix == ".md":
        normalized = re.sub(r"(?m)^ {4}", "", normalized)
    path.write_text(normalized, encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def package_manifest(pkg: dict) -> dict:
    return {
        "id": pkg["id"],
        "slug": pkg["slug"],
        "title": pkg["title"],
        "stage": pkg["stage"],
        "generated_at": GENERATED_AT,
        "real_data_dir": str((DATA_ROOT / pkg["data_dir_name"]).resolve()),
        "real_files": pkg["real_files"],
        "smoke_files": pkg["smoke_files"],
        "baseline": pkg["baseline"],
        "next_step": pkg["next_step"],
    }


def build_root_readme() -> str:
    lines = [
        "# Computer Vision Real Assignment Packages",
        "",
        f"- generated_at: {GENERATED_AT}",
        f"- package_count: {len(PACKAGES)}",
        "",
        "## Packages",
    ]
    for pkg in PACKAGES:
        lines.append(f"- `{pkg['id']}` `{pkg['slug']}`: {pkg['title']}")
    lines.extend(
        [
            "",
            "## Standard Contents",
            "",
            "- README.md",
            "- data_card.md",
            "- rubric.md",
            "- faq.md",
            "- submission_checklist.md",
            "- milestones.md",
            "- grader_notes.md",
            "- starter/",
            "- baseline/",
            "- tests/",
            "- reports/",
            "",
            "## Package-specific Extras",
            "",
            "- `HW04` 额外提供 `configs/transfer_protocol_template.json`、训练日志模板与类别误差图库模板",
            "- `HW05` 额外提供真实 VOC 子集配置模板与评测导出模板",
            "- `HW06` 额外提供 `proposal_template.md`、`milestone_template.md`、`ta_grading_template.md`、选题边界与项目风险样例库",
            "",
            "这些包当前采用“真实数据契约 + smoke test + 专题 starter + FAQ + 提交清单 + 里程碑 + 批改说明 + baseline 记录位”的形式，不包含教师最终答案。",
        ]
    )
    return "\n".join(lines)


def extra_readme_section(pkg: dict) -> str:
    sections = {
        "HW04": """
        ## 额外教师资产

        - `configs/transfer_protocol_template.json`：迁移学习正式协议模板
        - `artifacts/templates/training_log_template.csv`：真实训练日志模板
        - `artifacts/templates/class_error_gallery_template.md`：类别级误差图库模板
        """,
        "HW05": """
        ## 额外教师资产

        - `configs/minimal_detector_config.json`：最小检测 smoke 配置
        - `configs/voc2007_tiny_subset.template.json`：真实 VOC 子集配置模板
        - `artifacts/templates/eval_export_template.csv`：评测导出表模板
        - `artifacts/templates/eval_export_readme.md`：评测导出字段说明
        """,
        "HW06": """
        ## 额外教师资产

        - `proposal_template.md`：proposal 模板
        - `milestone_template.md`：milestone 模板
        - `ta_grading_template.md`：助教批改模板
        - `topic_boundary.md`：允许选题 / 不建议选题边界
        - `risk_casebook.md`：项目风险样例库
        """,
    }
    return sections.get(pkg["id"], "")


def build_readme(pkg: dict) -> str:
    smoke_lines = "\n".join(f"- `{name}`" for name in pkg["smoke_files"])
    real_lines = "\n".join(f"- `{name}`" for name in pkg["real_files"])
    prereq_lines = "\n".join(f"- `{item}`" for item in pkg["prerequisites"])
    goal_lines = "\n".join(f"- {item}" for item in pkg["goals"])
    package_dir = PACKAGES_ROOT / pkg["slug"]
    return f"""
    # {pkg["id"]} {pkg["title"]} Real Assignment Package

    这是一份面向学生自做的 `{pkg["id"]}` 真实作业包，不再只是说明页。

    ## 布置时机

    {pkg["assigned_when"]}

    ## 包内结构

    - `starter/`：专题 starter、运行入口与数据检查脚本
    - `baseline/`：baseline 记录位，不提供教师答案
    - `tests/`：最小 smoke test
    - `reports/`：正式报告模板
    - `data_card.md`：真实数据契约与 smoke 数据说明
    - `rubric.md`：评分量表
    - `package_manifest.json`：包元数据和 smoke 文件清单

    ## 前置知识

    {prereq_lines}

    ## 教学目标

    {goal_lines}

    ## 真实数据契约

    预期真实数据目录：

    `{(DATA_ROOT / pkg["data_dir_name"]).resolve()}`

    真实数据到位后，至少应包含：

    {real_lines}

    ## 当前 smoke 数据

    当前包自带最小 smoke 数据，用于验证流程能否跑通：

    {smoke_lines}

    ## 运行方式

    ```bash
    python "{package_dir / 'starter' / 'run.py'}" --input-dir "{DATA_ROOT / pkg["data_dir_name"]}" --output-dir "{package_dir / 'your_outputs'}"
    python "{package_dir / 'starter' / 'check_data.py'}" --input-dir "{DATA_ROOT / pkg["data_dir_name"]}"
    pytest "{package_dir / 'tests'}"
    ```

    ## 当前 baseline 定位

    - 本作业包不附带教师最终答案。
    - `baseline/README.md` 用来记录你的最小 baseline、关键指标和失败案例。
    - 当前 baseline 主题：`{pkg["baseline"]}`

    ## 下一步建议

    {pkg["next_step"]}

    {extra_readme_section(pkg)}
    """


def build_data_card(pkg: dict) -> str:
    real_lines = "\n".join(f"- `{name}`" for name in pkg["real_files"])
    smoke_lines = "\n".join(f"- `{name}`" for name in pkg["smoke_files"])
    return f"""
    # {pkg["id"]} Data Card

    - title: `{pkg["title"]}`
    - stage: `{pkg["stage"]}`
    - generated_at: `{GENERATED_AT}`

    ## 真实数据契约

    数据目录建议固定为：

    `{(DATA_ROOT / pkg["data_dir_name"]).resolve()}`

    预期文件：

    {real_lines}

    ## smoke 数据

    这些数据只用于：

    - 验证 starter 和 tests 跑通
    - 验证文件路径、编码和基本接口
    - 不用于真实研究结论

    smoke 文件：

    {smoke_lines}

    ## 硬约束

    - 不得把 smoke 结果当成正式实验结论
    - 必须在 README 中写清楚真实数据来源、时间区间和许可边界
    - 必须说明是否存在切分污染、标签泄漏或预处理边界问题
    """


def build_rubric(pkg: dict) -> str:
    return f"""
    # {pkg["id"]} Rubric

    | 维度 | 分值 | 评分关注点 |
    |:---|---:|:---|
    | 数据与协议 | 20 | 数据来源、切分、版本与运行协议是否清楚 |
    | baseline 与 starter 完整性 | 20 | 是否基于 `{pkg["baseline"]}` 跑通最小闭环 |
    | 结果与失败分析 | 20 | 是否解释失败案例，而不是只报最好结果 |
    | 工程组织 | 20 | README、目录、命令、输出是否可复核 |
    | 报告质量 | 20 | 是否回答核心问题并写清限制与下一步 |

    **通过线建议：**

    - `75/100` 及以上；
    - 且硬验收项全部通过。
    """


def build_faq(pkg: dict) -> str:
    prereq_lines = "\n".join(f"- 如果对 `{item}` 还不稳，建议先回补再做。" for item in pkg["prerequisites"][:3])
    return f"""
    # {pkg["id"]} FAQ

    ## 1. 这份作业最容易做错什么？

    - 把 smoke 数据当成正式实验结果
    - 只报最好数字，不解释协议和失败案例
    - 忽略公平对照与可复现性

    ## 2. 什么时候说明我还没准备好开始？

    {prereq_lines}

    ## 3. 老师最在意什么？

    - 你是否真正理解 `{pkg["title"]}` 的任务边界
    - 你是否按数据契约和作业协议做事
    - 你是否给出最小 baseline 和失败案例

    ## 4. 老师不希望看到什么？

    - 没有数据来源和切分说明
    - 只有结果，没有方法边界
    - 直接照搬外部实现充当自己的作业
    """


def build_submission_checklist(pkg: dict) -> str:
    real_lines = "\n".join(f"- [ ] 真实数据目录包含 `{name}`" for name in pkg["real_files"])
    return f"""
    # {pkg["id"]} Submission Checklist

    ## 目录与文件

    - [ ] `README.md` 已说明任务、数据、运行方式和结果
    - [ ] `starter/` 保持可运行
    - [ ] `tests/` 至少包含 smoke test
    - [ ] `reports/` 中已填写正式报告
    - [ ] `baseline/README.md` 已记录 baseline 和失败案例

    ## 数据与协议

    {real_lines}
    - [ ] 已写清楚切分方式、预处理与随机种子
    - [ ] 已说明真实数据与 smoke 数据的边界

    ## 结果与解释

    - [ ] 已给出 `{pkg["baseline"]}` 的最小对照
    - [ ] 已解释至少 2 个失败案例或不稳定现象
    - [ ] 已说明本次结论的适用边界
    """


def build_milestones(pkg: dict) -> str:
    goal_lines = "\n".join(f"- {item}" for item in pkg["goals"])
    return f"""
    # {pkg["id"]} Milestones

    ## M0 - 开题前检查

    - 跑通 starter 和 smoke test
    - 确认前置知识是否具备
    - 明确真实数据目录和协议

    ## M1 - 数据与协议冻结

    - 真实数据到位
    - 切分和预处理写入 README
    - 输出目录和命令固定

    ## M2 - Baseline 完成

    - 完成 `{pkg["baseline"]}` 的最小实现
    - 记录关键指标
    - 记录失败案例和异常现象

    ## M3 - 正式交付

    - 完成报告
    - 完成提交清单
    - 确认结果可复现

    ## 这份作业真正希望你增长的能力

    {goal_lines}
    """


def build_grader_notes(pkg: dict) -> str:
    return f"""
    # {pkg["id"]} Grader Notes

    这份说明是老师视角的批改口径，不是学生答案。

    ## 重点看什么

    - 是否真正理解 `{pkg["title"]}` 的任务边界
    - 是否按数据契约和协议完成作业
    - 是否完成 `{pkg["baseline"]}` 并做公平对照
    - 是否能解释结果和失败样本

    ## 明确不看什么

    - 不以最复杂模型为优先
    - 不以最好看结果为唯一评价标准
    - 不要求学生复现完整教师答案

    ## 一票否决项

    - 数据来源不清楚
    - 存在切分污染但未说明
    - 没有 baseline
    - 没有失败案例或边界说明
    """


def build_baseline_readme(pkg: dict) -> str:
    return f"""
    # {pkg["id"]} Baseline Notes

    这里用于记录学生自己的 baseline 结果，不提供教师最终答案。

    建议至少记录：

    - baseline 名称：`{pkg["baseline"]}`
    - 关键指标
    - 失败案例
    - 下一步改进想法
    """


def build_report_template(pkg: dict) -> str:
    return f"""
    # {pkg["id"]} Report Template

    ## 1. 问题与数据

    - 任务定义：
    - 数据来源：
    - 数据切分：
    - 预处理：

    ## 2. Baseline

    - baseline：
    - 关键设置：
    - 结果摘要：

    ## 3. 失败案例与边界

    - 失败案例 1：
    - 失败案例 2：
    - 当前边界：

    ## 4. 结论

    {pkg["report_prompt"]}
    """


def common_manifest_loader() -> str:
    return """
    from __future__ import annotations

    import json
    from pathlib import Path


    def package_root() -> Path:
        return Path(__file__).resolve().parents[1]


    def load_manifest() -> dict:
        return json.loads((package_root() / "package_manifest.json").read_text(encoding="utf-8"))
    """


def common_check_data(pkg: dict) -> str:
    checks = "\n".join(f"    required.append('{name}')" for name in pkg["smoke_files"])
    return f"""
    from __future__ import annotations

    import argparse
    from pathlib import Path


    def main() -> None:
        parser = argparse.ArgumentParser(description="Check smoke data files for {pkg['id']}.")
        parser.add_argument("--input-dir", required=True)
        args = parser.parse_args()

        input_dir = Path(args.input_dir)
        required: list[str] = []
{checks}
        missing = [name for name in required if not (input_dir / name).exists()]
        if missing:
            raise SystemExit("Missing smoke files: " + ", ".join(missing))
        print("smoke_data_ok")


    if __name__ == "__main__":
        main()
    """


def hw01_module() -> str:
    return """
    from __future__ import annotations

    import csv
    from collections import Counter
    from pathlib import Path


    def _read_rows(path: Path) -> list[dict[str, str]]:
        with path.open("r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))


    def _vector(row: dict[str, str]) -> list[float]:
        return [float(row["f1"]), float(row["f2"]), float(row["f3"])]


    def _distance(a: list[float], b: list[float]) -> float:
        return sum((x - y) ** 2 for x, y in zip(a, b))


    def _score_linear(vec: list[float]) -> str:
        scores = {
            "cat": 1.2 * vec[0] + 0.4 * vec[1] - 0.2 * vec[2],
            "dog": 0.3 * vec[0] + 1.1 * vec[1] + 0.2 * vec[2],
            "car": -0.2 * vec[0] + 0.2 * vec[1] + 1.3 * vec[2],
        }
        return max(scores, key=scores.get)


    def evaluate(train_csv: Path, val_csv: Path) -> dict[str, object]:
        train_rows = _read_rows(train_csv)
        val_rows = _read_rows(val_csv)
        knn_correct = 0
        linear_correct = 0
        failures: list[dict[str, str]] = []

        for row in val_rows:
            vec = _vector(row)
            nearest = min(train_rows, key=lambda item: _distance(vec, _vector(item)))
            knn_pred = nearest["label"]
            linear_pred = _score_linear(vec)
            actual = row["label"]
            if knn_pred == actual:
                knn_correct += 1
            if linear_pred == actual:
                linear_correct += 1
            if knn_pred != actual or linear_pred != actual:
                failures.append(
                    {
                        "sample_id": row["id"],
                        "label": actual,
                        "knn_pred": knn_pred,
                        "softmax_pred": linear_pred,
                    }
                )

        label_counts = Counter(row["label"] for row in train_rows)
        return {
            "train_size": len(train_rows),
            "val_size": len(val_rows),
            "label_counts": dict(label_counts),
            "knn_accuracy": round(knn_correct / len(val_rows), 4),
            "softmax_accuracy": round(linear_correct / len(val_rows), 4),
            "failure_examples": failures[:3],
        }
    """


def hw01_run(pkg: dict) -> str:
    return f"""
    from __future__ import annotations

    import argparse
    import json
    from pathlib import Path

    from knn_softmax import evaluate
    from manifest import load_manifest


    def main() -> None:
        parser = argparse.ArgumentParser(description="Run the {pkg['id']} smoke workflow.")
        parser.add_argument("--input-dir", required=True)
        parser.add_argument("--output-dir", required=True)
        args = parser.parse_args()

        manifest = load_manifest()
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir)
        results_dir = output_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        result = evaluate(input_dir / "train.smoke.csv", input_dir / "val.smoke.csv")
        payload = {{
            "homework_id": manifest["id"],
            "title": manifest["title"],
            "stage": manifest["stage"],
            "baseline": manifest["baseline"],
            "{pkg['summary_key']}": result,
        }}
        (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        (results_dir / "{pkg['summary_file']}").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        (output_dir / "quick_start.md").write_text(
            "\\n".join(
                [
                    f"# {{manifest['id']}} Smoke Run",
                    "",
                    f"- train_size: {{result['train_size']}}",
                    f"- val_size: {{result['val_size']}}",
                    f"- knn_accuracy: {{result['knn_accuracy']}}",
                    f"- softmax_accuracy: {{result['softmax_accuracy']}}",
                    "",
                    "## Next Step",
                    manifest["next_step"],
                ]
            ),
            encoding="utf-8",
        )


    if __name__ == "__main__":
        main()
    """


def hw01_test(pkg: dict) -> str:
    return f"""
    from __future__ import annotations

    import json
    import subprocess
    import sys
    from pathlib import Path


    def test_smoke_runner(tmp_path: Path) -> None:
        package_root = Path(__file__).resolve().parents[1]
        manifest = json.loads((package_root / "package_manifest.json").read_text(encoding="utf-8"))
        data_dir = Path(manifest["real_data_dir"])
        output_dir = tmp_path / "outputs"

        subprocess.run(
            [
                sys.executable,
                str(package_root / "starter" / "run.py"),
                "--input-dir",
                str(data_dir),
                "--output-dir",
                str(output_dir),
            ],
            check=True,
        )

        summary = json.loads((output_dir / "results" / "summary.json").read_text(encoding="utf-8"))
        assert summary["homework_id"] == "{pkg['id']}"
        assert summary["classification_summary"]["knn_accuracy"] >= 0.5
        assert summary["classification_summary"]["softmax_accuracy"] >= 0.5
        assert (output_dir / "results" / "{pkg['summary_file']}").exists()
    """


def hw02_module() -> str:
    return """
    from __future__ import annotations

    import csv
    import math
    from copy import deepcopy
    from pathlib import Path


    def _read_rows(path: Path) -> list[dict[str, str]]:
        with path.open("r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))


    def _dataset(path: Path) -> list[tuple[list[float], int]]:
        return [([float(row["x1"]), float(row["x2"])], int(row["label"])) for row in _read_rows(path)]


    def _init_params() -> dict[str, list]:
        return {
            "W1": [[0.20, -0.10, 0.15], [0.05, 0.18, -0.12]],
            "b1": [0.0, 0.0, 0.0],
            "W2": [[0.12, -0.08], [0.10, 0.06], [-0.07, 0.11]],
            "b2": [0.0, 0.0],
        }


    def _relu(values: list[float]) -> list[float]:
        return [v if v > 0 else 0.0 for v in values]


    def _softmax(logits: list[float]) -> list[float]:
        shift = max(logits)
        exps = [math.exp(v - shift) for v in logits]
        total = sum(exps)
        return [v / total for v in exps]


    def _forward(params: dict[str, list], features: list[float]) -> tuple[list[float], list[float], list[float]]:
        hidden_linear = []
        for j in range(3):
            hidden_linear.append(sum(features[i] * params["W1"][i][j] for i in range(2)) + params["b1"][j])
        hidden = _relu(hidden_linear)
        logits = []
        for k in range(2):
            logits.append(sum(hidden[j] * params["W2"][j][k] for j in range(3)) + params["b2"][k])
        return hidden_linear, hidden, logits


    def loss_and_grads(params: dict[str, list], batch: list[tuple[list[float], int]]) -> tuple[float, dict[str, list]]:
        grads = {
            "W1": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            "b1": [0.0, 0.0, 0.0],
            "W2": [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]],
            "b2": [0.0, 0.0],
        }
        loss = 0.0
        for features, label in batch:
            hidden_linear, hidden, logits = _forward(params, features)
            probs = _softmax(logits)
            loss += -math.log(max(probs[label], 1e-12))

            dlogits = probs[:]
            dlogits[label] -= 1.0
            for j in range(3):
                for k in range(2):
                    grads["W2"][j][k] += hidden[j] * dlogits[k]
            for k in range(2):
                grads["b2"][k] += dlogits[k]

            dhidden = []
            for j in range(3):
                dhidden.append(sum(params["W2"][j][k] * dlogits[k] for k in range(2)))
            dhidden_linear = [dhidden[j] if hidden_linear[j] > 0 else 0.0 for j in range(3)]

            for i in range(2):
                for j in range(3):
                    grads["W1"][i][j] += features[i] * dhidden_linear[j]
            for j in range(3):
                grads["b1"][j] += dhidden_linear[j]

        batch_size = float(len(batch))
        for key in ("W1", "W2"):
            for i, row in enumerate(grads[key]):
                for j, value in enumerate(row):
                    grads[key][i][j] = value / batch_size
        for key in ("b1", "b2"):
            grads[key] = [value / batch_size for value in grads[key]]
        return loss / batch_size, grads


    def _apply_step(params: dict[str, list], grads: dict[str, list], learning_rate: float) -> dict[str, list]:
        updated = deepcopy(params)
        for key in ("W1", "W2"):
            for i, row in enumerate(updated[key]):
                for j, value in enumerate(row):
                    updated[key][i][j] = value - learning_rate * grads[key][i][j]
        for key in ("b1", "b2"):
            for i, value in enumerate(updated[key]):
                updated[key][i] = value - learning_rate * grads[key][i]
        return updated


    def numeric_gradient_w2_00(params: dict[str, list], batch: list[tuple[list[float], int]], eps: float = 1e-5) -> float:
        plus = deepcopy(params)
        minus = deepcopy(params)
        plus["W2"][0][0] += eps
        minus["W2"][0][0] -= eps
        plus_loss, _ = loss_and_grads(plus, batch)
        minus_loss, _ = loss_and_grads(minus, batch)
        return (plus_loss - minus_loss) / (2 * eps)


    def run_smoke(tiny_batch_csv: Path, overfit_batch_csv: Path) -> dict[str, object]:
        params = _init_params()
        tiny_batch = _dataset(tiny_batch_csv)
        overfit_batch = _dataset(overfit_batch_csv)

        initial_loss, grads = loss_and_grads(params, tiny_batch)
        numeric = numeric_gradient_w2_00(params, tiny_batch)
        analytic = grads["W2"][0][0]
        updated = _apply_step(params, grads, learning_rate=0.5)
        after_one_step_loss, _ = loss_and_grads(updated, tiny_batch)

        training_params = deepcopy(params)
        history = []
        for _ in range(40):
            current_loss, current_grads = loss_and_grads(training_params, overfit_batch)
            history.append(round(current_loss, 6))
            training_params = _apply_step(training_params, current_grads, learning_rate=0.6)

        return {
            "tiny_batch_size": len(tiny_batch),
            "initial_loss": round(initial_loss, 6),
            "after_one_step_loss": round(after_one_step_loss, 6),
            "numeric_gradient_w2_00": round(numeric, 6),
            "analytic_gradient_w2_00": round(analytic, 6),
            "gradient_diff": round(abs(numeric - analytic), 8),
            "overfit_loss_history_head": history[:5],
            "overfit_final_loss": history[-1],
        }
    """


def hw02_run(pkg: dict) -> str:
    return f"""
    from __future__ import annotations

    import argparse
    import json
    from pathlib import Path

    from manifest import load_manifest
    from two_layer_net import run_smoke


    def main() -> None:
        parser = argparse.ArgumentParser(description="Run the {pkg['id']} smoke workflow.")
        parser.add_argument("--input-dir", required=True)
        parser.add_argument("--output-dir", required=True)
        args = parser.parse_args()

        manifest = load_manifest()
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir)
        results_dir = output_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        result = run_smoke(input_dir / "tiny_batch.smoke.csv", input_dir / "overfit_batch.smoke.csv")
        payload = {{
            "homework_id": manifest["id"],
            "title": manifest["title"],
            "stage": manifest["stage"],
            "baseline": manifest["baseline"],
            "{pkg['summary_key']}": result,
        }}
        (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        (results_dir / "{pkg['summary_file']}").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        (output_dir / "quick_start.md").write_text(
            "\\n".join(
                [
                    f"# {{manifest['id']}} Smoke Run",
                    "",
                    f"- initial_loss: {{result['initial_loss']}}",
                    f"- after_one_step_loss: {{result['after_one_step_loss']}}",
                    f"- gradient_diff: {{result['gradient_diff']}}",
                    f"- overfit_final_loss: {{result['overfit_final_loss']}}",
                    "",
                    "## Next Step",
                    manifest["next_step"],
                ]
            ),
            encoding="utf-8",
        )


    if __name__ == "__main__":
        main()
    """


def hw02_test(pkg: dict) -> str:
    return f"""
    from __future__ import annotations

    import json
    import subprocess
    import sys
    from pathlib import Path


    def test_smoke_runner(tmp_path: Path) -> None:
        package_root = Path(__file__).resolve().parents[1]
        manifest = json.loads((package_root / "package_manifest.json").read_text(encoding="utf-8"))
        data_dir = Path(manifest["real_data_dir"])
        output_dir = tmp_path / "outputs"

        subprocess.run(
            [
                sys.executable,
                str(package_root / "starter" / "run.py"),
                "--input-dir",
                str(data_dir),
                "--output-dir",
                str(output_dir),
            ],
            check=True,
        )

        summary = json.loads((output_dir / "results" / "summary.json").read_text(encoding="utf-8"))
        smoke = summary["training_summary"]
        assert summary["homework_id"] == "{pkg['id']}"
        assert smoke["after_one_step_loss"] < smoke["initial_loss"]
        assert smoke["gradient_diff"] < 1e-4
        assert (output_dir / "results" / "{pkg['summary_file']}").exists()
    """


def hw03_module() -> str:
    return """
    from __future__ import annotations

    import csv
    import math
    from pathlib import Path


    def _read_rows(path: Path) -> list[dict[str, str]]:
        with path.open("r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))


    def _image(row: dict[str, str]) -> list[float]:
        return [float(row[f"p{i}"]) for i in range(16)]


    def _extract_features(image: list[float]) -> list[float]:
        grid = [image[i * 4 : (i + 1) * 4] for i in range(4)]
        left = sum(grid[r][0] + grid[r][1] for r in range(4))
        right = sum(grid[r][2] + grid[r][3] for r in range(4))
        top = sum(grid[0]) + sum(grid[1])
        bottom = sum(grid[2]) + sum(grid[3])
        mean = sum(image) / len(image)
        return [left - right, top - bottom, mean]


    def _dataset(path: Path) -> list[tuple[list[float], int]]:
        rows = _read_rows(path)
        return [(_extract_features(_image(row)), int(row["label"])) for row in rows]


    def _softmax(logits: list[float]) -> list[float]:
        shift = max(logits)
        exps = [math.exp(v - shift) for v in logits]
        total = sum(exps)
        return [v / total for v in exps]


    def _evaluate(weights: list[list[float]], bias: list[float], dataset: list[tuple[list[float], int]]) -> tuple[float, dict[str, int]]:
        correct = 0
        confusion: dict[str, int] = {}
        for features, label in dataset:
            logits = [sum(features[i] * weights[i][k] for i in range(3)) + bias[k] for k in range(2)]
            pred = max(range(2), key=lambda idx: logits[idx])
            if pred == label:
                correct += 1
            confusion[f"{label}->{pred}"] = confusion.get(f"{label}->{pred}", 0) + 1
        return correct / len(dataset), confusion


    def run_smoke(train_csv: Path, val_csv: Path) -> dict[str, object]:
        train_set = _dataset(train_csv)
        val_set = _dataset(val_csv)
        weights = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
        bias = [0.0, 0.0]
        epoch_losses = []

        for _ in range(15):
            total_loss = 0.0
            for features, label in train_set:
                logits = [sum(features[i] * weights[i][k] for i in range(3)) + bias[k] for k in range(2)]
                probs = _softmax(logits)
                total_loss += -math.log(max(probs[label], 1e-12))
                dlogits = probs[:]
                dlogits[label] -= 1.0
                for i in range(3):
                    for k in range(2):
                        weights[i][k] -= 0.05 * features[i] * dlogits[k]
                for k in range(2):
                    bias[k] -= 0.05 * dlogits[k]
            epoch_losses.append(round(total_loss / len(train_set), 6))

        train_accuracy, _ = _evaluate(weights, bias, train_set)
        val_accuracy, confusion = _evaluate(weights, bias, val_set)
        return {
            "train_size": len(train_set),
            "val_size": len(val_set),
            "epoch_losses_head": epoch_losses[:5],
            "final_train_loss": epoch_losses[-1],
            "train_accuracy": round(train_accuracy, 4),
            "val_accuracy": round(val_accuracy, 4),
            "confusion_matrix": confusion,
        }
    """


def hw03_run(pkg: dict) -> str:
    return f"""
    from __future__ import annotations

    import argparse
    import json
    from pathlib import Path

    from cnn_pipeline import run_smoke
    from manifest import load_manifest


    def main() -> None:
        parser = argparse.ArgumentParser(description="Run the {pkg['id']} smoke workflow.")
        parser.add_argument("--input-dir", required=True)
        parser.add_argument("--output-dir", required=True)
        args = parser.parse_args()

        manifest = load_manifest()
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir)
        results_dir = output_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        result = run_smoke(input_dir / "train.smoke.csv", input_dir / "val.smoke.csv")
        payload = {{
            "homework_id": manifest["id"],
            "title": manifest["title"],
            "stage": manifest["stage"],
            "baseline": manifest["baseline"],
            "{pkg['summary_key']}": result,
        }}
        (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        (results_dir / "{pkg['summary_file']}").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        (output_dir / "quick_start.md").write_text(
            "\\n".join(
                [
                    f"# {{manifest['id']}} Smoke Run",
                    "",
                    f"- train_accuracy: {{result['train_accuracy']}}",
                    f"- val_accuracy: {{result['val_accuracy']}}",
                    f"- final_train_loss: {{result['final_train_loss']}}",
                    "",
                    "## Next Step",
                    manifest["next_step"],
                ]
            ),
            encoding="utf-8",
        )


    if __name__ == "__main__":
        main()
    """


def hw03_test(pkg: dict) -> str:
    return f"""
    from __future__ import annotations

    import json
    import subprocess
    import sys
    from pathlib import Path


    def test_smoke_runner(tmp_path: Path) -> None:
        package_root = Path(__file__).resolve().parents[1]
        manifest = json.loads((package_root / "package_manifest.json").read_text(encoding="utf-8"))
        data_dir = Path(manifest["real_data_dir"])
        output_dir = tmp_path / "outputs"

        subprocess.run(
            [
                sys.executable,
                str(package_root / "starter" / "run.py"),
                "--input-dir",
                str(data_dir),
                "--output-dir",
                str(output_dir),
            ],
            check=True,
        )

        summary = json.loads((output_dir / "results" / "summary.json").read_text(encoding="utf-8"))
        smoke = summary["cnn_summary"]
        assert summary["homework_id"] == "{pkg['id']}"
        assert smoke["train_accuracy"] >= 0.5
        assert smoke["val_accuracy"] >= 0.5
        assert (output_dir / "results" / "{pkg['summary_file']}").exists()
    """


def hw04_module() -> str:
    return """
    from __future__ import annotations

    import csv
    from collections import Counter
    from pathlib import Path


    LABELS = ("cat", "dog", "plane")


    def _read_rows(path: Path) -> list[dict[str, str]]:
        with path.open("r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))


    def _predicted_label(row: dict[str, str], prefix: str) -> str:
        scores = {label: float(row[f"{prefix}_{label}"]) for label in LABELS}
        return max(scores, key=scores.get)


    def evaluate(train_csv: Path, val_csv: Path) -> dict[str, object]:
        train_rows = _read_rows(train_csv)
        val_rows = _read_rows(val_csv)
        frozen_correct = 0
        finetune_correct = 0
        per_class: dict[str, dict[str, float]] = {}
        failure_examples: list[dict[str, object]] = []

        for row in val_rows:
            actual = row["label"]
            frozen_pred = _predicted_label(row, "frozen")
            finetune_pred = _predicted_label(row, "finetune")

            stats = per_class.setdefault(actual, {"count": 0, "frozen_correct": 0, "finetune_correct": 0})
            stats["count"] += 1
            if frozen_pred == actual:
                frozen_correct += 1
                stats["frozen_correct"] += 1
            if finetune_pred == actual:
                finetune_correct += 1
                stats["finetune_correct"] += 1
            if frozen_pred != actual or finetune_pred != actual:
                failure_examples.append(
                    {
                        "sample_id": row["id"],
                        "label": actual,
                        "frozen_pred": frozen_pred,
                        "finetune_pred": finetune_pred,
                    }
                )

        per_class_delta: dict[str, float] = {}
        promoted_classes: list[str] = []
        stagnant_classes: list[str] = []
        for label, stats in per_class.items():
            frozen_acc = stats["frozen_correct"] / stats["count"]
            finetune_acc = stats["finetune_correct"] / stats["count"]
            delta = round(finetune_acc - frozen_acc, 4)
            per_class_delta[label] = delta
            if delta > 0:
                promoted_classes.append(label)
            else:
                stagnant_classes.append(label)

        label_counts = Counter(row["label"] for row in train_rows)
        return {
            "train_size": len(train_rows),
            "val_size": len(val_rows),
            "label_counts": dict(label_counts),
            "frozen_accuracy": round(frozen_correct / len(val_rows), 4),
            "finetune_accuracy": round(finetune_correct / len(val_rows), 4),
            "per_class_delta": per_class_delta,
            "promoted_classes": promoted_classes,
            "stagnant_classes": stagnant_classes,
            "cost_ratio": 1.8,
            "failure_examples": failure_examples[:4],
        }
    """


def hw04_run(pkg: dict) -> str:
    return f"""
    from __future__ import annotations

    import argparse
    import json
    from pathlib import Path

    from manifest import load_manifest
    from transfer_analysis import evaluate


    def main() -> None:
        parser = argparse.ArgumentParser(description="Run the {pkg['id']} smoke workflow.")
        parser.add_argument("--input-dir", required=True)
        parser.add_argument("--output-dir", required=True)
        args = parser.parse_args()

        manifest = load_manifest()
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir)
        results_dir = output_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        result = evaluate(input_dir / "train.smoke.csv", input_dir / "val.smoke.csv")
        payload = {{
            "homework_id": manifest["id"],
            "title": manifest["title"],
            "stage": manifest["stage"],
            "baseline": manifest["baseline"],
            "{pkg['summary_key']}": result,
        }}
        (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        (results_dir / "{pkg['summary_file']}").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        (output_dir / "quick_start.md").write_text(
            "\\n".join(
                [
                    f"# {{manifest['id']}} Smoke Run",
                    "",
                    f"- frozen_accuracy: {{result['frozen_accuracy']}}",
                    f"- finetune_accuracy: {{result['finetune_accuracy']}}",
                    f"- promoted_classes: {{', '.join(result['promoted_classes'])}}",
                    f"- cost_ratio: {{result['cost_ratio']}}",
                    "",
                    "## Next Step",
                    manifest["next_step"],
                ]
            ),
            encoding="utf-8",
        )


    if __name__ == "__main__":
        main()
    """


def hw04_test(pkg: dict) -> str:
    return f"""
    from __future__ import annotations

    import json
    import subprocess
    import sys
    from pathlib import Path


    def test_smoke_runner(tmp_path: Path) -> None:
        package_root = Path(__file__).resolve().parents[1]
        manifest = json.loads((package_root / "package_manifest.json").read_text(encoding="utf-8"))
        data_dir = Path(manifest["real_data_dir"])
        output_dir = tmp_path / "outputs"

        subprocess.run(
            [
                sys.executable,
                str(package_root / "starter" / "run.py"),
                "--input-dir",
                str(data_dir),
                "--output-dir",
                str(output_dir),
            ],
            check=True,
        )

        summary = json.loads((output_dir / "results" / "summary.json").read_text(encoding="utf-8"))
        smoke = summary["transfer_summary"]
        assert summary["homework_id"] == "{pkg['id']}"
        assert smoke["finetune_accuracy"] >= smoke["frozen_accuracy"]
        assert len(smoke["promoted_classes"]) >= 1
        assert smoke["cost_ratio"] > 1.0
        assert (package_root / "artifacts" / "templates" / "training_log_template.csv").exists()
        assert (package_root / "artifacts" / "templates" / "class_error_gallery_template.md").exists()
        assert (output_dir / "results" / "{pkg['summary_file']}").exists()
    """


def hw05_module() -> str:
    return """
    from __future__ import annotations

    import csv
    from pathlib import Path


    def _read_rows(path: Path) -> list[dict[str, str]]:
        with path.open("r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))


    def _box(row: dict[str, str], prefix: str) -> tuple[float, float, float, float]:
        return (
            float(row[f"{prefix}_x1"]),
            float(row[f"{prefix}_y1"]),
            float(row[f"{prefix}_x2"]),
            float(row[f"{prefix}_y2"]),
        )


    def _iou(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
        inter_x1 = max(a[0], b[0])
        inter_y1 = max(a[1], b[1])
        inter_x2 = min(a[2], b[2])
        inter_y2 = min(a[3], b[3])
        inter_w = max(0.0, inter_x2 - inter_x1)
        inter_h = max(0.0, inter_y2 - inter_y1)
        inter_area = inter_w * inter_h
        area_a = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
        area_b = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
        union = area_a + area_b - inter_area
        return inter_area / union if union else 0.0


    def run_smoke(train_csv: Path, val_csv: Path) -> dict[str, object]:
        train_rows = _read_rows(train_csv)
        val_rows = _read_rows(val_csv)
        true_positive = 0
        predicted_positive = 0
        ious: list[float] = []
        failure_cases: list[dict[str, object]] = []

        for row in val_rows:
            pred_score = float(row["pred_score"])
            gt_box = _box(row, "gt")
            pred_box = _box(row, "pred")
            iou = _iou(gt_box, pred_box)
            ious.append(round(iou, 4))
            is_positive = pred_score >= 0.5
            if is_positive:
                predicted_positive += 1
            hit = row["label"] == row["pred_label"] and is_positive and iou >= 0.5
            if hit:
                true_positive += 1
            else:
                failure_cases.append(
                    {
                        "image_id": row["image_id"],
                        "label": row["label"],
                        "pred_label": row["pred_label"],
                        "pred_score": pred_score,
                        "iou": round(iou, 4),
                    }
                )

        train_images = len({row["image_id"] for row in train_rows})
        val_images = len({row["image_id"] for row in val_rows})
        return {
            "train_images": train_images,
            "val_images": val_images,
            "precision_at_50": round(true_positive / max(predicted_positive, 1), 4),
            "recall_at_50": round(true_positive / len(val_rows), 4),
            "mean_iou": round(sum(ious) / len(ious), 4),
            "pass_at_iou50": true_positive,
            "failure_cases": failure_cases[:4],
        }
    """


def hw05_run(pkg: dict) -> str:
    return f"""
    from __future__ import annotations

    import argparse
    import json
    from pathlib import Path

    from detection_pipeline import run_smoke
    from manifest import load_manifest


    def main() -> None:
        parser = argparse.ArgumentParser(description="Run the {pkg['id']} smoke workflow.")
        parser.add_argument("--input-dir", required=True)
        parser.add_argument("--output-dir", required=True)
        args = parser.parse_args()

        manifest = load_manifest()
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir)
        results_dir = output_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        result = run_smoke(input_dir / "train.smoke.csv", input_dir / "val.smoke.csv")
        payload = {{
            "homework_id": manifest["id"],
            "title": manifest["title"],
            "stage": manifest["stage"],
            "baseline": manifest["baseline"],
            "{pkg['summary_key']}": result,
        }}
        (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        (results_dir / "{pkg['summary_file']}").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        (output_dir / "quick_start.md").write_text(
            "\\n".join(
                [
                    f"# {{manifest['id']}} Smoke Run",
                    "",
                    f"- precision_at_50: {{result['precision_at_50']}}",
                    f"- recall_at_50: {{result['recall_at_50']}}",
                    f"- mean_iou: {{result['mean_iou']}}",
                    f"- failure_cases: {{len(result['failure_cases'])}}",
                    "",
                    "## Next Step",
                    manifest["next_step"],
                ]
            ),
            encoding="utf-8",
        )


    if __name__ == "__main__":
        main()
    """


def hw05_test(pkg: dict) -> str:
    return f"""
    from __future__ import annotations

    import json
    import subprocess
    import sys
    from pathlib import Path


    def test_smoke_runner(tmp_path: Path) -> None:
        package_root = Path(__file__).resolve().parents[1]
        manifest = json.loads((package_root / "package_manifest.json").read_text(encoding="utf-8"))
        data_dir = Path(manifest["real_data_dir"])
        output_dir = tmp_path / "outputs"

        subprocess.run(
            [
                sys.executable,
                str(package_root / "starter" / "run.py"),
                "--input-dir",
                str(data_dir),
                "--output-dir",
                str(output_dir),
            ],
            check=True,
        )

        summary = json.loads((output_dir / "results" / "summary.json").read_text(encoding="utf-8"))
        smoke = summary["detection_summary"]
        assert summary["homework_id"] == "{pkg['id']}"
        assert smoke["precision_at_50"] >= 0.5
        assert smoke["recall_at_50"] >= 0.5
        assert len(smoke["failure_cases"]) >= 1
        assert (package_root / "configs" / "voc2007_tiny_subset.template.json").exists()
        assert (package_root / "artifacts" / "templates" / "eval_export_template.csv").exists()
        assert (output_dir / "results" / "{pkg['summary_file']}").exists()
    """


def hw06_module() -> str:
    return """
    from __future__ import annotations

    import csv
    import json
    from pathlib import Path


    REQUIRED_FIELDS = ("problem", "dataset", "metric", "baseline", "improvement", "success_threshold", "risks")


    def _scores(path: Path) -> list[float]:
        with path.open("r", encoding="utf-8", newline="") as f:
            return [float(row["score"]) for row in csv.DictReader(f)]


    def run_smoke(plan_json: Path, baseline_csv: Path, improvement_csv: Path) -> dict[str, object]:
        plan = json.loads(plan_json.read_text(encoding="utf-8"))
        baseline_scores = _scores(baseline_csv)
        improvement_scores = _scores(improvement_csv)
        completeness = sum(1 for field in REQUIRED_FIELDS if field in plan and plan[field]) / len(REQUIRED_FIELDS)
        baseline_avg = sum(baseline_scores) / len(baseline_scores)
        improvement_avg = sum(improvement_scores) / len(improvement_scores)
        delta = improvement_avg - baseline_avg
        threshold = float(plan["success_threshold"])
        meets_threshold = improvement_avg >= threshold
        next_decision = "advance_to_final_report" if meets_threshold and delta > 0 else "revise_project_scope"
        return {
            "proposal_completeness": round(completeness, 4),
            "milestone_status": plan.get("milestone_status", "unknown"),
            "baseline_score": round(baseline_avg, 4),
            "improvement_score": round(improvement_avg, 4),
            "delta": round(delta, 4),
            "meets_success_threshold": meets_threshold,
            "next_decision": next_decision,
            "risk_count": len(plan.get("risks", [])),
        }
    """


def hw06_run(pkg: dict) -> str:
    return f"""
    from __future__ import annotations

    import argparse
    import json
    from pathlib import Path

    from manifest import load_manifest
    from open_project import run_smoke


    def main() -> None:
        parser = argparse.ArgumentParser(description="Run the {pkg['id']} smoke workflow.")
        parser.add_argument("--input-dir", required=True)
        parser.add_argument("--output-dir", required=True)
        args = parser.parse_args()

        manifest = load_manifest()
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir)
        results_dir = output_dir / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        result = run_smoke(
            input_dir / "project_plan.smoke.json",
            input_dir / "baseline_results.smoke.csv",
            input_dir / "improvement_results.smoke.csv",
        )
        payload = {{
            "homework_id": manifest["id"],
            "title": manifest["title"],
            "stage": manifest["stage"],
            "baseline": manifest["baseline"],
            "{pkg['summary_key']}": result,
        }}
        (results_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        (results_dir / "{pkg['summary_file']}").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        (output_dir / "quick_start.md").write_text(
            "\\n".join(
                [
                    f"# {{manifest['id']}} Smoke Run",
                    "",
                    f"- proposal_completeness: {{result['proposal_completeness']}}",
                    f"- baseline_score: {{result['baseline_score']}}",
                    f"- improvement_score: {{result['improvement_score']}}",
                    f"- next_decision: {{result['next_decision']}}",
                    "",
                    "## Next Step",
                    manifest["next_step"],
                ]
            ),
            encoding="utf-8",
        )


    if __name__ == "__main__":
        main()
    """


def hw06_test(pkg: dict) -> str:
    return f"""
    from __future__ import annotations

    import json
    import subprocess
    import sys
    from pathlib import Path


    def test_smoke_runner(tmp_path: Path) -> None:
        package_root = Path(__file__).resolve().parents[1]
        manifest = json.loads((package_root / "package_manifest.json").read_text(encoding="utf-8"))
        data_dir = Path(manifest["real_data_dir"])
        output_dir = tmp_path / "outputs"

        subprocess.run(
            [
                sys.executable,
                str(package_root / "starter" / "run.py"),
                "--input-dir",
                str(data_dir),
                "--output-dir",
                str(output_dir),
            ],
            check=True,
        )

        summary = json.loads((output_dir / "results" / "summary.json").read_text(encoding="utf-8"))
        smoke = summary["project_summary"]
        assert summary["homework_id"] == "{pkg['id']}"
        assert smoke["proposal_completeness"] == 1.0
        assert smoke["improvement_score"] > smoke["baseline_score"]
        assert smoke["milestone_status"] == "on_track"
        assert (package_root / "topic_boundary.md").exists()
        assert (package_root / "risk_casebook.md").exists()
        assert (output_dir / "results" / "{pkg['summary_file']}").exists()
    """


def starter_init() -> str:
    return """
    # Package starter exports live in this directory.
    """


def smoke_data_hw01(data_dir: Path) -> None:
    train_rows = [
        {"id": "tr1", "label": "cat", "f1": 0.90, "f2": 0.10, "f3": 0.10},
        {"id": "tr2", "label": "cat", "f1": 0.85, "f2": 0.20, "f3": 0.10},
        {"id": "tr3", "label": "dog", "f1": 0.20, "f2": 0.90, "f3": 0.20},
        {"id": "tr4", "label": "dog", "f1": 0.10, "f2": 0.85, "f3": 0.20},
        {"id": "tr5", "label": "car", "f1": 0.10, "f2": 0.20, "f3": 0.95},
        {"id": "tr6", "label": "car", "f1": 0.15, "f2": 0.15, "f3": 0.90},
    ]
    val_rows = [
        {"id": "va1", "label": "cat", "f1": 0.88, "f2": 0.15, "f3": 0.10},
        {"id": "va2", "label": "dog", "f1": 0.15, "f2": 0.82, "f3": 0.18},
        {"id": "va3", "label": "car", "f1": 0.12, "f2": 0.18, "f3": 0.92},
        {"id": "va4", "label": "cat", "f1": 0.70, "f2": 0.35, "f3": 0.10},
    ]
    write_csv(data_dir / "train.smoke.csv", train_rows, ["id", "label", "f1", "f2", "f3"])
    write_csv(data_dir / "val.smoke.csv", val_rows, ["id", "label", "f1", "f2", "f3"])


def smoke_data_hw02(data_dir: Path) -> None:
    tiny_rows = [
        {"id": "tb1", "label": 0, "x1": 1.0, "x2": 0.0},
        {"id": "tb2", "label": 1, "x1": 0.0, "x2": 1.0},
        {"id": "tb3", "label": 0, "x1": 1.0, "x2": 0.2},
        {"id": "tb4", "label": 1, "x1": 0.1, "x2": 1.0},
    ]
    overfit_rows = [
        {"id": "of1", "label": 0, "x1": 1.0, "x2": 0.0},
        {"id": "of2", "label": 1, "x1": 0.0, "x2": 1.0},
        {"id": "of3", "label": 0, "x1": 0.9, "x2": 0.1},
        {"id": "of4", "label": 1, "x1": 0.1, "x2": 0.9},
    ]
    write_csv(data_dir / "tiny_batch.smoke.csv", tiny_rows, ["id", "label", "x1", "x2"])
    write_csv(data_dir / "overfit_batch.smoke.csv", overfit_rows, ["id", "label", "x1", "x2"])


def smoke_data_hw03(data_dir: Path) -> None:
    def row(sample_id: str, label: int, pixels: list[int]) -> dict[str, object]:
        payload: dict[str, object] = {"id": sample_id, "label": label}
        for i, value in enumerate(pixels):
            payload[f"p{i}"] = value
        return payload

    train_rows = [
        row("tr1", 0, [9, 9, 1, 1, 9, 9, 1, 1, 9, 9, 1, 1, 9, 9, 1, 1]),
        row("tr2", 0, [8, 8, 1, 1, 8, 8, 1, 1, 8, 8, 1, 1, 8, 8, 1, 1]),
        row("tr3", 1, [9, 9, 9, 9, 9, 9, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1]),
        row("tr4", 1, [8, 8, 8, 8, 8, 8, 8, 8, 2, 2, 2, 2, 2, 2, 2, 2]),
    ]
    val_rows = [
        row("va1", 0, [9, 8, 1, 1, 9, 8, 1, 1, 9, 8, 1, 1, 9, 8, 1, 1]),
        row("va2", 1, [8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1]),
        row("va3", 0, [7, 7, 2, 2, 7, 7, 2, 2, 7, 7, 2, 2, 7, 7, 2, 2]),
        row("va4", 1, [9, 9, 9, 9, 8, 8, 8, 8, 2, 2, 2, 2, 1, 1, 1, 1]),
    ]
    fieldnames = ["id", "label"] + [f"p{i}" for i in range(16)]
    write_csv(data_dir / "train.smoke.csv", train_rows, fieldnames)
    write_csv(data_dir / "val.smoke.csv", val_rows, fieldnames)


def smoke_data_hw04(data_dir: Path) -> None:
    train_rows = [
        {"id": "tr1", "label": "cat", "source": "backbone_a"},
        {"id": "tr2", "label": "cat", "source": "backbone_a"},
        {"id": "tr3", "label": "dog", "source": "backbone_a"},
        {"id": "tr4", "label": "dog", "source": "backbone_a"},
        {"id": "tr5", "label": "plane", "source": "backbone_a"},
        {"id": "tr6", "label": "plane", "source": "backbone_a"},
    ]
    val_rows = [
        {"id": "va1", "label": "cat", "frozen_cat": 0.62, "frozen_dog": 0.28, "frozen_plane": 0.10, "finetune_cat": 0.81, "finetune_dog": 0.12, "finetune_plane": 0.07},
        {"id": "va2", "label": "dog", "frozen_cat": 0.44, "frozen_dog": 0.40, "frozen_plane": 0.16, "finetune_cat": 0.15, "finetune_dog": 0.73, "finetune_plane": 0.12},
        {"id": "va3", "label": "plane", "frozen_cat": 0.14, "frozen_dog": 0.21, "frozen_plane": 0.65, "finetune_cat": 0.12, "finetune_dog": 0.18, "finetune_plane": 0.70},
        {"id": "va4", "label": "cat", "frozen_cat": 0.39, "frozen_dog": 0.48, "frozen_plane": 0.13, "finetune_cat": 0.58, "finetune_dog": 0.30, "finetune_plane": 0.12},
        {"id": "va5", "label": "dog", "frozen_cat": 0.31, "frozen_dog": 0.45, "frozen_plane": 0.24, "finetune_cat": 0.19, "finetune_dog": 0.63, "finetune_plane": 0.18},
        {"id": "va6", "label": "plane", "frozen_cat": 0.33, "frozen_dog": 0.18, "frozen_plane": 0.49, "finetune_cat": 0.20, "finetune_dog": 0.16, "finetune_plane": 0.64},
    ]
    write_csv(data_dir / "train.smoke.csv", train_rows, ["id", "label", "source"])
    write_csv(
        data_dir / "val.smoke.csv",
        val_rows,
        ["id", "label", "frozen_cat", "frozen_dog", "frozen_plane", "finetune_cat", "finetune_dog", "finetune_plane"],
    )


def smoke_data_hw05(data_dir: Path) -> None:
    train_rows = [
        {"image_id": "tr1", "label": "cat", "box_count": 1},
        {"image_id": "tr2", "label": "dog", "box_count": 1},
        {"image_id": "tr3", "label": "person", "box_count": 1},
    ]
    val_rows = [
        {"image_id": "va1", "label": "cat", "gt_x1": 10, "gt_y1": 10, "gt_x2": 50, "gt_y2": 50, "pred_label": "cat", "pred_score": 0.92, "pred_x1": 12, "pred_y1": 12, "pred_x2": 48, "pred_y2": 49},
        {"image_id": "va2", "label": "dog", "gt_x1": 20, "gt_y1": 20, "gt_x2": 70, "gt_y2": 70, "pred_label": "dog", "pred_score": 0.88, "pred_x1": 22, "pred_y1": 24, "pred_x2": 66, "pred_y2": 69},
        {"image_id": "va3", "label": "person", "gt_x1": 15, "gt_y1": 12, "gt_x2": 45, "gt_y2": 80, "pred_label": "cat", "pred_score": 0.76, "pred_x1": 16, "pred_y1": 15, "pred_x2": 44, "pred_y2": 78},
        {"image_id": "va4", "label": "dog", "gt_x1": 30, "gt_y1": 30, "gt_x2": 68, "gt_y2": 72, "pred_label": "dog", "pred_score": 0.91, "pred_x1": 31, "pred_y1": 31, "pred_x2": 67, "pred_y2": 71},
    ]
    write_csv(data_dir / "train.smoke.csv", train_rows, ["image_id", "label", "box_count"])
    write_csv(
        data_dir / "val.smoke.csv",
        val_rows,
        ["image_id", "label", "gt_x1", "gt_y1", "gt_x2", "gt_y2", "pred_label", "pred_score", "pred_x1", "pred_y1", "pred_x2", "pred_y2"],
    )


def smoke_data_hw06(data_dir: Path) -> None:
    plan = {
        "problem": "比较轻量 backbone 与数据增强方案在小型视觉任务上的效果。",
        "dataset": "cifar10-mini",
        "metric": "macro_f1",
        "baseline": "小型 CNN",
        "improvement": "加入迁移学习与更稳的增强策略",
        "success_threshold": 0.68,
        "milestone_status": "on_track",
        "risks": ["数据规模偏小", "改进可能只在少数类别生效"],
    }
    baseline_rows = [
        {"fold": "f1", "score": 0.61},
        {"fold": "f2", "score": 0.63},
        {"fold": "f3", "score": 0.62},
    ]
    improvement_rows = [
        {"fold": "f1", "score": 0.70},
        {"fold": "f2", "score": 0.72},
        {"fold": "f3", "score": 0.71},
    ]
    write_json(data_dir / "project_plan.smoke.json", plan)
    write_csv(data_dir / "baseline_results.smoke.csv", baseline_rows, ["fold", "score"])
    write_csv(data_dir / "improvement_results.smoke.csv", improvement_rows, ["fold", "score"])


def build_hw04_transfer_config() -> str:
    return """
    {
      "dataset": "cifar10-transfer-placeholder",
      "backbone": "resnet18",
      "freeze_strategy": "all_backbone",
      "finetune_strategy": "last_block_and_head",
      "metric": "accuracy",
      "notes": "This is a teacher-side protocol template, not a finished experiment config."
    }
    """


def build_hw05_detector_config() -> str:
    return """
    {
      "dataset": "pascal-voc-placeholder",
      "classes": ["cat", "dog", "person"],
      "metric": "IoU@0.5",
      "score_threshold": 0.5,
      "nms_threshold": 0.5,
      "notes": "Replace this smoke config with a real VOC subset config before formal training."
    }
    """


def build_hw05_voc_subset_config() -> str:
    return """
    {
      "dataset": {
        "name": "VOC2007-tiny-subset",
        "source_split": "VOC2007 trainval + test",
        "subset_policy": {
          "classes": ["cat", "dog", "person"],
          "max_train_images_per_class": 40,
          "max_val_images_per_class": 15,
          "allow_multi_label_images": true
        },
        "paths": {
          "jpeg_images": "VOCdevkit/VOC2007/JPEGImages",
          "annotations": "VOCdevkit/VOC2007/Annotations",
          "image_sets_main": "VOCdevkit/VOC2007/ImageSets/Main"
        }
      },
      "train": {
        "batch_size": 4,
        "epochs": 8,
        "optimizer": "sgd",
        "learning_rate": 0.001
      },
      "eval": {
        "metric": "IoU@0.5",
        "score_threshold": 0.5,
        "nms_threshold": 0.5,
        "export_csv": "artifacts/eval/eval_export.csv"
      },
      "notes": "Teacher-side template for a real VOC subset. Freeze exact file lists before formal release."
    }
    """


def build_hw05_eval_export_template() -> str:
    rows = [
        {"image_id": "2007_000001", "split": "val", "class_name": "cat", "gt_count": 1, "pred_count": 1, "tp": 1, "fp": 0, "fn": 0, "best_iou": 0.78, "score_threshold": 0.50, "note": "correct detection"},
        {"image_id": "2007_000002", "split": "val", "class_name": "dog", "gt_count": 1, "pred_count": 2, "tp": 1, "fp": 1, "fn": 0, "best_iou": 0.63, "score_threshold": 0.50, "note": "one extra false positive"},
        {"image_id": "2007_000003", "split": "val", "class_name": "person", "gt_count": 1, "pred_count": 0, "tp": 0, "fp": 0, "fn": 1, "best_iou": 0.00, "score_threshold": 0.50, "note": "missed due to occlusion"},
    ]
    lines = ["image_id,split,class_name,gt_count,pred_count,tp,fp,fn,best_iou,score_threshold,note"]
    for row in rows:
        lines.append(
            ",".join(
                [
                    str(row["image_id"]),
                    str(row["split"]),
                    str(row["class_name"]),
                    str(row["gt_count"]),
                    str(row["pred_count"]),
                    str(row["tp"]),
                    str(row["fp"]),
                    str(row["fn"]),
                    f"{row['best_iou']:.2f}",
                    f"{row['score_threshold']:.2f}",
                    str(row["note"]),
                ]
            )
        )
    return "\n".join(lines)


def build_hw05_eval_export_readme() -> str:
    return """
    # HW05 Evaluation Export Guide

    这个模板用于把 Pascal VOC 子集评测结果导出成可复核的逐图像记录。

    ## 字段说明

    - `image_id`：图像唯一标识
    - `split`：训练 / 验证 / 测试切分
    - `class_name`：当前记录的类别
    - `gt_count`：该类别在当前图像中的真实框数量
    - `pred_count`：该类别在当前图像中的预测框数量
    - `tp / fp / fn`：在固定阈值下的真阳、假阳、漏检数量
    - `best_iou`：最佳匹配框的 IoU
    - `score_threshold`：本次导出采用的分数阈值
    - `note`：人工补充说明，例如遮挡、背景混淆、小目标等

    ## 建议导出时机

    - 每次正式评测后导出一次
    - 更换阈值或 NMS 策略后重新导出
    - 准备写失败案例分析前，先冻结一版导出表
    """


def build_hw04_training_log_template() -> str:
    lines = [
        "epoch,stage,train_loss,val_loss,val_accuracy,learning_rate,elapsed_minutes,notes",
        "1,frozen,1.245,1.102,0.610,0.001000,2.5,head warmup",
        "2,frozen,1.083,0.964,0.655,0.001000,2.4,stable improvement",
        "1,finetune,0.982,0.841,0.702,0.000100,4.1,unfreeze last block",
        "2,finetune,0.901,0.790,0.731,0.000100,4.0,class dog improves",
    ]
    return "\n".join(lines)


def build_hw04_error_gallery_template() -> str:
    return """
    # HW04 Class Error Gallery Template

    > 每个类别至少保留 1 个“冻结失败 -> 微调修复”或“微调仍失败”的例子。

    ## 类别：cat

    - 样本 ID：
    - 冻结预测：
    - 微调预测：
    - 真实标签：
    - 现象说明：
    - 你认为迁移学习帮到了什么：

    ## 类别：dog

    - 样本 ID：
    - 冻结预测：
    - 微调预测：
    - 真实标签：
    - 现象说明：
    - 你认为迁移学习帮到了什么：

    ## 类别：plane

    - 样本 ID：
    - 冻结预测：
    - 微调预测：
    - 真实标签：
    - 现象说明：
    - 你认为迁移学习没有解决什么：
    """


def build_hw06_proposal_template() -> str:
    return """
    # HW06 Proposal Template

    ## 1. 问题定义

    - 我要解决的问题：
    - 为什么值得做：

    ## 2. 数据与评价

    - 数据来源：
    - 切分方式：
    - 核心指标：

    ## 3. Baseline

    - baseline 是什么：
    - 为什么这是合理起点：

    ## 4. 风险

    - 风险 1：
    - 风险 2：

    ## 5. 计划

    - proposal 后一周要完成什么：
    - milestone 前必须跑通什么：
    """


def build_hw06_milestone_template() -> str:
    return """
    # HW06 Milestone Template

    ## 1. 已完成内容

    - 已完成 1：
    - 已完成 2：

    ## 2. 当前结果

    - baseline 当前结果：
    - 改进尝试当前结果：

    ## 3. 阻塞点

    - 阻塞 1：
    - 阻塞 2：

    ## 4. 调整计划

    - 接下来要砍掉什么：
    - 接下来要保留什么：
    """


def build_hw06_ta_grading_template() -> str:
    return """
    # HW06 TA Grading Template

    | 维度 | 满分 | 助教记录 |
    |:---|---:|:---|
    | 问题定义是否清楚 | 20 | |
    | baseline 是否成立 | 20 | |
    | 改进是否有证据 | 20 | |
    | 边界与失败是否真实 | 20 | |
    | proposal / milestone / report 是否一致 | 20 | |

    ## 口头反馈

    - 做得好的地方：
    - 最需要补的一点：
    - 是否建议继续扩题：
    """


def build_hw06_topic_boundary() -> str:
    return """
    # HW06 允许选题 / 不建议选题

    ## 允许选题

    - 小型图像分类改进：有清楚 baseline、数据切分和类别级分析
    - 迁移学习对比：冻结 vs 微调，且有成本记录
    - 最小检测子集实验：有固定 VOC 子集、固定评测协议和失败案例
    - 误差分析型项目：核心目标是解释失败模式，而不是只追最高分

    ## 不建议选题

    - 题目过大：例如“做一个通用自动驾驶系统”
    - 数据和评价协议不清：只有想法，没有可复核指标
    - 没有 baseline：一上来就堆复杂模型
    - 完全依赖外部成品仓库：自己无法解释训练、评测和失败
    - 需要超出当前课程算力预算的大规模实验

    ## 老师批准时重点问什么

    - baseline 是什么？
    - 成功标准是什么？
    - 失败了以后还能交什么证据？
    """


def build_hw06_risk_casebook() -> str:
    return """
    # HW06 项目风险样例库

    ## 风险 1：问题定义过大

    - 表现：题目听起来厉害，但 2 周内没有最小可交付
    - 早期信号：proposal 里没有固定数据、指标和 baseline
    - 缓解动作：砍成一个可复核子问题

    ## 风险 2：只有改进，没有 baseline

    - 表现：学生直接尝试复杂模型，却无法说明是否真的变好
    - 早期信号：milestone 仍没有 baseline 结果表
    - 缓解动作：先冻结 baseline，再谈改进

    ## 风险 3：评测协议漂移

    - 表现：不同实验用了不同切分、不同指标或不同阈值
    - 早期信号：report 里的表格彼此不可比
    - 缓解动作：在 manifest 中锁定协议，并要求导出统一结果表

    ## 风险 4：只展示成功样本

    - 表现：报告里全是漂亮截图，没有失败和边界
    - 早期信号：没有失败案例区
    - 缓解动作：强制至少保留 2 个失败样本与原因说明

    ## 风险 5：实现依赖外部成品

    - 表现：能跑，但学生说不清楚自己改了什么
    - 早期信号：README 只贴仓库链接，没有本地最小入口
    - 缓解动作：要求最小复核入口、关键文件说明和自写实验日志
    """


def extra_package_files(pkg: dict) -> dict[str, str]:
    if pkg["id"] == "HW04":
        return {
            "configs/transfer_protocol_template.json": build_hw04_transfer_config(),
            "artifacts/templates/training_log_template.csv": build_hw04_training_log_template(),
            "artifacts/templates/class_error_gallery_template.md": build_hw04_error_gallery_template(),
        }
    if pkg["id"] == "HW05":
        return {
            "configs/minimal_detector_config.json": build_hw05_detector_config(),
            "configs/voc2007_tiny_subset.template.json": build_hw05_voc_subset_config(),
            "artifacts/templates/eval_export_template.csv": build_hw05_eval_export_template(),
            "artifacts/templates/eval_export_readme.md": build_hw05_eval_export_readme(),
        }
    if pkg["id"] == "HW06":
        return {
            "proposal_template.md": build_hw06_proposal_template(),
            "milestone_template.md": build_hw06_milestone_template(),
            "ta_grading_template.md": build_hw06_ta_grading_template(),
            "topic_boundary.md": build_hw06_topic_boundary(),
            "risk_casebook.md": build_hw06_risk_casebook(),
        }
    return {}


def starter_files(pkg: dict) -> dict[str, str]:
    module_map = {
        "HW01": hw01_module(),
        "HW02": hw02_module(),
        "HW03": hw03_module(),
        "HW04": hw04_module(),
        "HW05": hw05_module(),
        "HW06": hw06_module(),
    }
    run_map = {
        "HW01": hw01_run(pkg),
        "HW02": hw02_run(pkg),
        "HW03": hw03_run(pkg),
        "HW04": hw04_run(pkg),
        "HW05": hw05_run(pkg),
        "HW06": hw06_run(pkg),
    }
    return {
        "__init__.py": starter_init(),
        "manifest.py": common_manifest_loader(),
        "check_data.py": common_check_data(pkg),
        pkg["starter_module"]: module_map[pkg["id"]],
        "run.py": run_map[pkg["id"]],
    }


def test_file(pkg: dict) -> str:
    return {
        "HW01": hw01_test(pkg),
        "HW02": hw02_test(pkg),
        "HW03": hw03_test(pkg),
        "HW04": hw04_test(pkg),
        "HW05": hw05_test(pkg),
        "HW06": hw06_test(pkg),
    }[pkg["id"]]


def generate_package(pkg: dict) -> None:
    package_dir = PACKAGES_ROOT / pkg["slug"]
    data_dir = DATA_ROOT / pkg["data_dir_name"]
    manifest = package_manifest(pkg)

    write_json(package_dir / "package_manifest.json", manifest)
    write_text(package_dir / "README.md", build_readme(pkg))
    write_text(package_dir / "data_card.md", build_data_card(pkg))
    write_text(package_dir / "rubric.md", build_rubric(pkg))
    write_text(package_dir / "faq.md", build_faq(pkg))
    write_text(package_dir / "submission_checklist.md", build_submission_checklist(pkg))
    write_text(package_dir / "milestones.md", build_milestones(pkg))
    write_text(package_dir / "grader_notes.md", build_grader_notes(pkg))
    write_text(package_dir / "baseline" / "README.md", build_baseline_readme(pkg))
    write_text(package_dir / "reports" / "report_template.md", build_report_template(pkg))

    for name, content in starter_files(pkg).items():
        write_text(package_dir / "starter" / name, content)
    write_text(package_dir / "tests" / f"test_{pkg['slug']}.py", test_file(pkg))
    for name, content in extra_package_files(pkg).items():
        write_text(package_dir / name, content)

    if pkg["id"] == "HW01":
        smoke_data_hw01(data_dir)
    elif pkg["id"] == "HW02":
        smoke_data_hw02(data_dir)
    elif pkg["id"] == "HW03":
        smoke_data_hw03(data_dir)
    elif pkg["id"] == "HW04":
        smoke_data_hw04(data_dir)
    elif pkg["id"] == "HW05":
        smoke_data_hw05(data_dir)
    else:
        smoke_data_hw06(data_dir)


def main() -> None:
    PACKAGES_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    write_text(PACKAGES_ROOT / "README.md", build_root_readme())
    for pkg in PACKAGES:
        generate_package(pkg)
    print(f"Generated {len(PACKAGES)} computer vision real assignment packages.")


if __name__ == "__main__":
    main()
