"""
08-NLP全栈 大作业 Capstone: 文本误差与召回漏检测审计工具
"""

import numpy as np


def compute_retrieval_metrics(retrieved_doc_ids, ground_truth_doc_ids, k_list=[1, 3, 5]):
    """
    计算检索 Recall@K, Precision@K 与 MRR (Mean Reciprocal Rank)
    """
    gt_set = set(ground_truth_doc_ids)
    metrics = {}
    
    for k in k_list:
        top_k = retrieved_doc_ids[:k]
        hits = len(set(top_k).intersection(gt_set))
        metrics[f"Precision@{k}"] = hits / k
        metrics[f"Recall@{k}"] = hits / len(gt_set) if gt_set else 0.0

    # MRR
    mrr = 0.0
    for rank, doc_id in enumerate(retrieved_doc_ids):
        if doc_id in gt_set:
            mrr = 1.0 / (rank + 1)
            break
    metrics["MRR"] = mrr
    
    return metrics
