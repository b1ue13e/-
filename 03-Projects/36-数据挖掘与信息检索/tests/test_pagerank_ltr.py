import pytest
import os
import sys
import numpy as np

# 导入工程模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.learning_to_rank import PageRank, RankNetNumPy

def test_pagerank_convergence_and_authority():
    # 5 节点图：0 -> 1, 2; 1 -> 2; 2 -> 0; 3 -> 2; 4 为悬空节点
    adj = np.array([
        [0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]  # Dangling node
    ], dtype=float)
    
    pr_engine = PageRank(d=0.85)
    pr = pr_engine.fit_predict(adj)
    
    assert np.sum(pr) == pytest.approx(1.0, abs=1e-5)
    # 节点 2 被多个入边指向，权重显著最高
    assert pr[2] == np.max(pr)
    assert pr[2] > pr[0] > pr[1]

def test_ranknet_pairwise_optimization_and_ranking_convergence():
    # 生成合成排序特征：高相关文档在特征第 0 维和第 1 维具有显著正权重
    np.random.seed(101)
    n_pairs = 100
    dim = 4
    
    # x_better 具有更高的潜在相关度分数
    x_better = np.random.randn(n_pairs, dim) + 1.0
    x_worse = np.random.randn(n_pairs, dim) - 1.0
    
    ranknet = RankNetNumPy(input_dim=dim, hidden_dim=6, lr=0.1)
    
    initial_loss = ranknet.train_step(x_better, x_worse, target=1.0)
    
    # 训练 50 个 step
    losses = [initial_loss]
    for _ in range(50):
        l = ranknet.train_step(x_better, x_worse, target=1.0)
        losses.append(l)
        
    # 验证 Pairwise 交叉熵损失有效下降
    assert losses[-1] < losses[0]
    
    # 验证模型预测得分：x_better 显著高于 x_worse
    scores_better = ranknet.forward(x_better)
    scores_worse = ranknet.forward(x_worse)
    assert np.mean(scores_better > scores_worse) >= 0.95
