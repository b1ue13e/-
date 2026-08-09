from __future__ import annotations


def _validate(labels: list[int], scores: list[float]) -> None:
    if len(labels) != len(scores) or not labels:
        raise ValueError("labels and scores must be non-empty and have equal length")
    if set(labels) != {0, 1}:
        raise ValueError("labels must contain both binary classes")


def roc_auc(labels: list[int], scores: list[float]) -> float:
    _validate(labels, scores)
    ranked = sorted(zip(scores, labels), key=lambda item: item[0])
    positive_rank_sum = 0.0
    index = 0
    while index < len(ranked):
        end = index + 1
        while end < len(ranked) and ranked[end][0] == ranked[index][0]:
            end += 1
        average_rank = (index + 1 + end) / 2.0
        positive_rank_sum += average_rank * sum(label for _, label in ranked[index:end])
        index = end
    positives = sum(labels)
    negatives = len(labels) - positives
    return (
        positive_rank_sum - positives * (positives + 1) / 2.0
    ) / (positives * negatives)


def average_precision(labels: list[int], scores: list[float]) -> float:
    _validate(labels, scores)
    ranked = sorted(zip(scores, labels), key=lambda item: item[0], reverse=True)
    positives = sum(labels)
    true_positive = 0
    seen = 0
    previous_recall = 0.0
    area = 0.0
    index = 0
    while index < len(ranked):
        end = index + 1
        while end < len(ranked) and ranked[end][0] == ranked[index][0]:
            end += 1
        group = ranked[index:end]
        true_positive += sum(label for _, label in group)
        seen += len(group)
        recall = true_positive / positives
        precision = true_positive / seen
        area += (recall - previous_recall) * precision
        previous_recall = recall
        index = end
    return area


def precision_at_k(labels: list[int], scores: list[float], k: int) -> float:
    _validate(labels, scores)
    if not 0 < k <= len(labels):
        raise ValueError("k must be within the candidate count")
    order = sorted(range(len(scores)), key=lambda index: (-scores[index], index))
    return sum(labels[index] for index in order[:k]) / k

