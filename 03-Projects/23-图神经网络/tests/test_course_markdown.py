from __future__ import annotations

from pathlib import Path


VAULT = Path(__file__).resolve().parents[3]
COURSE = VAULT / "02-Knowledge" / "🧠 学习系统" / "23-图神经网络"


def test_course_has_one_entry_and_four_stage_mocs() -> None:
    assert (COURSE / "🗺️ 图神经网络学习路径.md").exists()
    assert (COURSE / "📚 教材挂载索引.md").exists()
    mocs = sorted(COURSE.glob("0[1-4]-*/🧭 阶段*.md"))
    assert len(mocs) == 4


def test_study_cards_have_required_contract() -> None:
    cards = []
    for path in COURSE.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n") and "\ntype: study\n" in text[:500]:
            cards.append(path)
            frontmatter = text.split("\n---\n", 1)[0]
            for field in ("course:", "stage_moc:", "flow:", "kind:"):
                assert field in frontmatter, f"{path} missing {field}"
            assert "## " in text
            assert "## 8. 学完后可以完成" in text or "## 9. 学完后可以完成" in text or "## 7. 学完后可以完成" in text
    assert len(cards) == 18


def test_project_boundaries_keep_reference_separate_from_learner_submissions() -> None:
    project = VAULT / "03-Projects" / "23-图神经网络"
    assert (project / "reference" / "capstone" / "run.py").exists()
    assert (project / "submission" / "README.md").exists()
    assert not (project / "submission" / "capstone" / "run.py").exists()


def test_stage_worked_examples_are_documented() -> None:
    project = VAULT / "03-Projects" / "23-图神经网络"
    for assignment in ("s01", "s02", "s03", "s04"):
        assert f"starter/run_assignment.py {assignment}" in "\n".join(
            path.read_text(encoding="utf-8")
            for path in (project / "阶段作业").glob("*.md")
        )
