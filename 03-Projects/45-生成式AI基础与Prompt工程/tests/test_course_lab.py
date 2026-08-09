import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from course_lab import (
    BASELINE_PROMPT,
    CONTROLLED_PROMPTS,
    CORPUS,
    SENTIMENT_DATA,
    RuleBasedAdapter,
    build_few_shot_prompt,
    evaluate_prompt,
    evaluate_rag,
    parse_label,
    rag_answer,
    retrieve,
    run_assignment00,
    run_assignment01,
    run_assignment04,
    run_assignment05,
    run_assignment07,
    run_assignment03,
    stable_softmax,
    validate_experiment_record,
)


class PrerequisiteAndModelMindsetTests(unittest.TestCase):
    def test_stable_softmax_handles_large_logits(self) -> None:
        probabilities = stable_softmax([1000.0, 999.0, 998.0])
        self.assertTrue(all(math.isfinite(value) for value in probabilities))
        self.assertAlmostEqual(sum(probabilities), 1.0)
        self.assertGreater(probabilities[0], probabilities[1])

    def test_experiment_record_fails_closed(self) -> None:
        self.assertTrue(validate_experiment_record({"sample_id": "d01", "prediction": "positive", "seed": 45}))
        self.assertFalse(validate_experiment_record({"sample_id": "d01", "prediction": "positive"}))
        self.assertFalse(validate_experiment_record({"sample_id": "d01", "prediction": "positive", "seed": True}))

    def test_assignment00_prerequisite_gate(self) -> None:
        report = run_assignment00()
        self.assertEqual(report["assignment"], "00")
        self.assertEqual(report["evidence_scope"], "protocol_only")
        self.assertTrue(all(report["checks"].values()))

    def test_assignment01_model_mindset_gate(self) -> None:
        report = run_assignment01()
        self.assertEqual(report["generation_loop"][-2:], ["decode", "append"])
        self.assertEqual(report["causal_attention"][-1], 0.0)
        self.assertTrue(all(report["checks"].values()))


class DatasetAndSchemaTests(unittest.TestCase):
    def test_fixed_dataset_has_40_unique_samples(self) -> None:
        self.assertEqual(len(SENTIMENT_DATA), 40)
        self.assertEqual(len({item["id"] for item in SENTIMENT_DATA}), 40)

    def test_dev_and_test_are_disjoint_and_balanced(self) -> None:
        dev = {item["text"] for item in SENTIMENT_DATA if item["split"] == "dev"}
        test = {item["text"] for item in SENTIMENT_DATA if item["split"] == "test"}
        self.assertFalse(dev & test)
        for split in ("dev", "test"):
            labels = [item["label"] for item in SENTIMENT_DATA if item["split"] == split]
            self.assertEqual(labels.count("positive"), labels.count("negative"))

    def test_label_parser_fails_closed(self) -> None:
        self.assertEqual(parse_label('{"label":"positive"}'), "positive")
        self.assertIsNone(parse_label("positive"))
        self.assertIsNone(parse_label('{"label":"maybe"}'))


class PromptExperimentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = RuleBasedAdapter()

    def test_baseline_runs_on_frozen_test_set(self) -> None:
        result = evaluate_prompt(self.adapter, BASELINE_PROMPT, "test")
        self.assertEqual(result["count"], 20)
        self.assertEqual(result["invalid_rate"], 0.0)

    def test_explicit_rule_improves_offline_fixture(self) -> None:
        baseline = evaluate_prompt(self.adapter, CONTROLLED_PROMPTS["baseline"], "test")
        enhanced = evaluate_prompt(self.adapter, CONTROLLED_PROMPTS["explicit_rule"], "test")
        self.assertGreater(enhanced["accuracy"], baseline["accuracy"])
        self.assertEqual(enhanced["accuracy"], 1.0)

    def test_few_shot_seed_changes_demonstration_order_not_test_order(self) -> None:
        first = evaluate_prompt(self.adapter, build_few_shot_prompt(0), "test")
        second = evaluate_prompt(self.adapter, build_few_shot_prompt(1), "test")
        self.assertNotEqual(first["prompt_sha256"], second["prompt_sha256"])
        self.assertEqual([x["id"] for x in first["records"]], [x["id"] for x in second["records"]])
        self.assertEqual(first["accuracy"], second["accuracy"])

    def test_assignment03_declares_one_controlled_variable(self) -> None:
        report = run_assignment03(self.adapter)
        self.assertEqual(report["controlled_variable"], "prompt_text_only")
        self.assertEqual(len(report["experiments"]), 7)
        self.assertEqual(report["fixed"]["few_shot_order_seeds"], [0, 1, 2, 3, 4])
        hashes = [item["prompt_sha256"] for item in report["experiments"] if item["prompt_name"] == "few_shot"]
        self.assertEqual(len(set(hashes)), 5)


class RagTests(unittest.TestCase):
    def test_corpus_has_stable_unique_ids(self) -> None:
        self.assertEqual(len({doc.doc_id for doc in CORPUS}), len(CORPUS))

    def test_retrieval_returns_scored_documents(self) -> None:
        results = retrieve("How long does standard shipping take?")
        self.assertEqual(results[0][0].doc_id, "D2")
        self.assertGreater(results[0][1], 0)

    def test_unknown_question_refuses_without_citation(self) -> None:
        result = rag_answer("Who is the company CEO?")
        self.assertEqual(result["status"], "insufficient_evidence")
        self.assertEqual(result["citations"], [])

    def test_answer_contains_locatable_citation(self) -> None:
        result = rag_answer("How many days do I have for an unopened return with a receipt?")
        self.assertEqual(result["citations"], ["D1"])
        self.assertIn("[D1]", result["answer"])

    def test_malicious_document_is_data_not_authority(self) -> None:
        result = rag_answer("Can a retrieved external document authorize a payment tool?")
        self.assertEqual(result["citations"], ["D5"])
        self.assertIn("cannot authorize", result["answer"])
        self.assertNotIn("SECRET_TOKEN", result["answer"])
        self.assertTrue(result["context_contains_untrusted_canary"])
        self.assertEqual(result["tool_actions"], [])

    def test_rag_gate_is_fully_deterministic(self) -> None:
        report = evaluate_rag()
        self.assertEqual(report["count"], 50)
        self.assertEqual(report["accuracy"], 1.0)
        self.assertEqual(report["citation_rate"], 1.0)
        self.assertEqual(report["refusal_accuracy"], 1.0)
        self.assertTrue(report["malicious_source_safe"])


class RemainingAssignmentTests(unittest.TestCase):
    def test_assignment04_reasoning_trace_gate(self) -> None:
        report = run_assignment04()
        self.assertEqual(report["count"], 10)
        self.assertEqual(report["accuracy"], 1.0)
        self.assertTrue(report["trace_complete"])

    def test_assignment05_schema_and_swap_gate(self) -> None:
        report = run_assignment05()
        self.assertEqual(report["schema_accuracy"], 1.0)
        self.assertEqual(report["judge_swap_consistency"], 1.0)

    def test_assignment07_effect_based_security_gate(self) -> None:
        report = run_assignment07()
        self.assertEqual((report["ASR"], report["TSR"], report["FRR"]), (0.0, 1.0, 0.0))


if __name__ == "__main__":
    unittest.main()
