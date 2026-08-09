import pytest
import os
import sys
import json

# 将工程源码路径加入 Python 模块搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.frequent_patterns import AprioriMiner
from src.inverted_index import InvertedIndex, BM25Scorer

def test_apriori_1_itemsets():
    transactions = [
        {'Bread', 'Milk', 'Butter'},
        {'Bread', 'Diapers', 'Beer'},
        {'Milk', 'Diapers', 'Beer'},
        {'Bread', 'Milk', 'Diapers'},
        {'Bread', 'Milk', 'Butter'}
    ]
    miner = AprioriMiner(transactions, min_sup=2)
    freq = miner.mine()
    
    assert ('Bread',) in freq
    assert freq[('Bread',)] == 4
    assert freq[('Milk',)] == 4
    assert freq[('Diapers',)] == 3
    assert ('Bread', 'Milk') in freq

def test_bm25_scoring():
    index = InvertedIndex(use_compression=False)
    index.add_document("doc1", "Data mining and knowledge discovery in large databases")
    index.add_document("doc2", "Information retrieval and search engine ranking models")
    index.add_document("doc3", "Probabilistic BM25 model for text retrieval and ranking")
    
    results = index.search_bm25("BM25 retrieval ranking", top_k=2)
    assert len(results) > 0
    top_doc, top_score = results[0]
    assert top_doc == "doc3"
    assert top_score > 0.0

if __name__ == "__main__":
    test_apriori_1_itemsets()
    test_bm25_scoring()
    print("All integration tests passed successfully!")
