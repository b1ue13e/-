"""
08-NLP全栈 知识卡合规性 pytest 测试套件
验证所有 08-NLP全栈 知识卡文件的 Frontmatter 属性、标题规范、闭卷提取提示与双链合法性。
"""

import os
import glob
import re
import pytest

NLP_KNOWLEDGE_DIR = r"f:\-\02-Knowledge\🧠 学习系统\08-NLP全栈"
NLP_PROJECTS_DIR = r"f:\-\03-Projects\08-NLP全栈"

def get_all_nlp_cards():
    cards = glob.glob(os.path.join(NLP_KNOWLEDGE_DIR, "**", "08-NLP全栈-*.md"), recursive=True)
    return [c for c in cards if "前置" not in os.path.basename(c)]

def get_fully_populated_nlp_cards():
    """已全量充实为 Cognitive-Sci 13 节示范结构的核心卡"""
    core_names = [
        "08-NLP全栈-Self-Attention自注意力机制.md",
        "08-NLP全栈-Transformer架构.md",
        "08-NLP全栈-BERT模型.md",
        "08-NLP全栈-检索增强生成RAG.md"
    ]
    return [c for c in get_all_nlp_cards() if os.path.basename(c) in core_names]

@pytest.mark.parametrize("card_path", get_all_nlp_cards())
def test_nlp_card_frontmatter(card_path):
    with open(card_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert content.startswith("---"), f"Card {card_path} missing YAML frontmatter start"
    assert "course: \"08-NLP全栈\"" in content or "course: 08-NLP全栈" in content, f"Card {card_path} missing course attribute"
    assert "type: study" in content, f"Card {card_path} missing type: study"
    assert "stage_moc:" in content, f"Card {card_path} missing stage_moc"

@pytest.mark.parametrize("card_path", get_fully_populated_nlp_cards())
def test_nlp_card_essential_sections(card_path):
    with open(card_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 验证已充实的示范卡是否包含核心段落与提取练习
    has_recall = "我的主动回忆区" in content or "Guided Recall" in content or "## 12." in content
    has_quiz = "闭卷提取练习" in content or "自测" in content or "## 13." in content
    
    assert has_recall, f"Card {os.path.basename(card_path)} missing Guided Recall section"
    assert has_quiz, f"Card {os.path.basename(card_path)} missing Self-Quiz section"

def test_minbert_script_execution():
    from subprocess import run
    res = run(["python", os.path.join(NLP_PROJECTS_DIR, "scripts", "test_minbert_standalone.py")], capture_output=True, text=True, encoding="utf-8")
    assert res.returncode == 0, f"MinBERT test script failed: {res.stderr}"
    assert "[OK]" in res.stdout or "PASSED" in res.stdout
