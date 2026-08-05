from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from textwrap import dedent


ROOT = Path(r"f:\-")
SOURCE = ROOT / "99-System" / "tools" / "generate_quant_real_assignment_packages.py"


def load_generation_module():
    spec = importlib.util.spec_from_file_location("quant_pkg_gen", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load package generator from {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = dedent(content).strip() + "\n"
    normalized = re.sub(r"(?m)^ {4}", "", normalized)
    path.write_text(normalized, encoding="utf-8")


def build_faq(pkg: dict) -> str:
    prereq = "\n".join(f"- 我如果对 `{item}` 还不稳，需要先回去补一遍再开始。" for item in pkg["prerequisites"][:3])
    return f"""
    # {pkg["id"]} FAQ

    ## 1. 这份作业最容易做错什么？

    - 把 smoke 数据跑通，当成正式实验结果。
    - 直接汇报最好看的数字，不解释协议、边界和失败案例。
    - 忽略时间切分、交易成本、发布日期或采样口径。

    ## 2. 什么时候说明我还没准备好开做？

    {prereq}

    ## 3. 我需要做得和论文一样复杂吗？

    不需要。先完成最小 baseline、最小报告和最小复现链路，再决定要不要加复杂方法。

    ## 4. 老师最在意什么？

    - 你是不是真的理解 `{pkg["title"]}` 解决的金融问题。
    - 你是否按数据契约和作业协议做事。
    - 你是否给出公平 baseline，而不是只展示最好结果。

    ## 5. 老师不希望看到什么？

    - 没有数据来源、没有时间区间、没有协议说明。
    - 只有结果，没有方法边界。
    - 拿现成开源结果直接替代自己的实验过程。
    """


def build_submission_checklist(pkg: dict) -> str:
    real_files = "\n".join(f"- [ ] 真实数据目录包含 `{name}`" for name in pkg["real_files"])
    return f"""
    # {pkg["id"]} Submission Checklist

    提交前，请逐项自查：

    ## 目录与文件

    - [ ] `README` 已说明问题、方法、数据来源和运行方式
    - [ ] `starter/` 保持可运行
    - [ ] `tests/` 至少包含 smoke test
    - [ ] `reports/` 中已填写正式报告
    - [ ] `baseline/README.md` 已记录 baseline 和失败案例

    ## 数据与协议

    {real_files}
    - [ ] 已写清楚时间区间、切分方式和是否存在未来信息
    - [ ] 已说明复权、采样、成本或发布日期口径

    ## 结果与解释

    - [ ] 已给出 `{pkg["baseline"]}` 的公平对照
    - [ ] 已解释至少 2 个失败案例或不稳定现象
    - [ ] 已说明本次结论的适用边界

    ## 最后检查

    - [ ] 结果可以在新目录重新运行
    - [ ] smoke test 通过
    - [ ] 没有把 smoke 结果当正式结论
    """


def build_milestones(pkg: dict) -> str:
    goals = "\n".join(f"- {goal}" for goal in pkg["goals"])
    return f"""
    # {pkg["id"]} Milestones

    ## M0 - 开题前检查

    - 明确作业题目：`{pkg["title"]}`
    - 确认前置知识是否具备
    - 跑通 starter 和 smoke test

    ## M1 - 数据与协议冻结

    - 真实数据到位
    - 口径说明写入 README
    - 训练 / 验证 / 测试或样本内 / 样本外切分固定

    ## M2 - Baseline 完成

    - 完成最小 baseline：`{pkg["baseline"]}`
    - 记录关键指标
    - 记录失败案例和异常现象

    ## M3 - 正式交付

    - 完成报告
    - 完成提交清单
    - 确认能复现

    ## 这份作业真正希望你增长的能力

    {goals}
    """


def build_grader_notes(pkg: dict) -> str:
    questions = "\n".join(f"- {q}" for q in pkg["questions"][:3])
    return f"""
    # {pkg["id"]} Grader Notes

    这份说明是老师视角的批改口径，不是学生答案。

    ## 重点看什么

    - 是否真正理解 `{pkg["title"]}` 的任务边界
    - 是否按数据契约和协议完成作业
    - 是否完成 `{pkg["baseline"]}` 并做公平对照
    - 是否能解释结果而不是只堆数字

    ## 明确不看什么

    - 不以最复杂模型为优先
    - 不以最好看结果为唯一评价标准
    - 不要求学生复现外部论文的全部细节

    ## 批改时建议追问的问题

    {questions}

    ## 一票否决项

    - 数据来源不清楚
    - 存在明显未来信息但未说明
    - 没有 baseline
    - 没有失败案例或边界说明
    """


def main() -> None:
    module = load_generation_module()
    packages_root: Path = module.PACKAGES_ROOT
    for pkg in module.PACKAGES:
        package_dir = packages_root / pkg["slug"]
        write_text(package_dir / "faq.md", build_faq(pkg))
        write_text(package_dir / "submission_checklist.md", build_submission_checklist(pkg))
        write_text(package_dir / "milestones.md", build_milestones(pkg))
        write_text(package_dir / "grader_notes.md", build_grader_notes(pkg))
    print(f"Augmented teacher materials for {len(module.PACKAGES)} packages.")


if __name__ == "__main__":
    main()
