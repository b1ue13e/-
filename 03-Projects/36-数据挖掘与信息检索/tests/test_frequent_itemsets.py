import pytest
import os
import sys
import json
from collections import defaultdict

# 导入工程模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.frequent_patterns import AprioriMiner, FPGrowthMiner

def test_apriori_correctness():
    txs = [
        {'A', 'B', 'E'},
        {'B', 'D'},
        {'B', 'C'},
        {'A', 'B', 'D'},
        {'A', 'C'},
        {'A', 'B', 'C'}
    ]
    miner = AprioriMiner(txs, min_sup=2)
    freq = miner.mine()
    
    assert ('A',) in freq and freq[('A',)] == 4
    assert ('B',) in freq and freq[('B',)] == 5
    assert ('A', 'B') in freq and freq[('A', 'B')] == 3
    assert ('A', 'C') in freq and freq[('A', 'C')] == 2
    assert ('B', 'C') in freq and freq[('B', 'C')] == 2

def test_fp_growth_equivalence_with_apriori():
    """验证 FP-Growth 与 Apriori 在多项集挖掘上的数学等价性"""
    txs = [
        {'Bread', 'Milk', 'Butter'},
        {'Bread', 'Diapers', 'Beer', 'Eggs'},
        {'Milk', 'Diapers', 'Beer', 'Cola'},
        {'Bread', 'Milk', 'Diapers', 'Beer'},
        {'Bread', 'Milk', 'Diapers', 'Cola'},
        {'Bread', 'Butter', 'Eggs'},
        {'Milk', 'Diapers', 'Beer', 'Butter'},
        {'Bread', 'Milk', 'Butter', 'Eggs'}
    ]
    min_sup = 3
    
    apriori_miner = AprioriMiner(txs, min_sup=min_sup)
    apriori_freq = apriori_miner.mine()
    
    fpgrowth_miner = FPGrowthMiner(txs, min_sup=min_sup)
    fpgrowth_freq = fpgrowth_miner.mine()
    
    # 验证两种算法找出的频繁项集完全一致
    assert set(apriori_freq.keys()) == set(fpgrowth_freq.keys())
    for itemset in apriori_freq:
        assert apriori_freq[itemset] == fpgrowth_freq[itemset]

def test_support_confidence_lift_and_conviction():
    txs = [
        {'Bread', 'Butter'},
        {'Bread', 'Butter'},
        {'Bread', 'Butter'},
        {'Bread', 'Butter'},
        {'Bread'},
        {'Butter'}
    ]
    miner = AprioriMiner(txs, min_sup=2)
    rules = miner.extract_association_rules(min_confidence=0.5)
    
    assert len(rules) > 0
    rule_bread_butter = next((r for r in rules if r['antecedent'] == ('Bread',) and r['consequent'] == ('Butter',)), None)
    assert rule_bread_butter is not None
    
    # Support(Bread, Butter) = 4/6 = 0.6667
    assert abs(rule_bread_butter['support'] - 4.0 / 6.0) < 1e-5
    # Conf(Bread -> Butter) = 4 / 5 = 0.8
    assert abs(rule_bread_butter['confidence'] - 0.8) < 1e-5
    # Lift(Bread -> Butter) = (4/6) / ( (5/6) * (5/6) ) = 0.6667 / 0.6944 = 0.96
    assert abs(rule_bread_butter['lift'] - (4.0 / 6.0) / ((5.0 / 6.0) * (5.0 / 6.0))) < 1e-5
