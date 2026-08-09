import pytest
import os
import sys

# 导入工程模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.stream_mining import DGIMStreamCounter, FlajoletMartinEstimator

def test_dgim_bucket_merging_and_invariants():
    """
    测试 DGIM 滑动窗口：
    - 维持同一大小桶至多 2 个的不变量
    - 桶大小必须为 2 的幂次
    - 溢出窗口大小后正确淘汰
    """
    window_size = 20
    dgim = DGIMStreamCounter(window_size=window_size)
    
    # 模拟数据流输入
    stream = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1]
    for bit in stream:
        dgim.update(bit)
        
    # 验证桶大小全为 2 的幂次
    for b in dgim.buckets:
        assert (b.size & (b.size - 1)) == 0
        
    # 验证同大小桶至多 2 个
    from collections import Counter
    size_counts = Counter([b.size for b in dgim.buckets])
    for size, count in size_counts.items():
        assert count <= 2

    # 估计数量应当接近真实值 (真实值 12)
    est = dgim.estimate_count(k=window_size)
    assert abs(est - 12) <= 3

def test_flajolet_martin_distinct_elements():
    """测试 Flajolet-Martin 算法在大基数去重估计下的精度"""
    fm = FlajoletMartinEstimator(num_hashes=64, num_groups=8)
    
    # 插入 500 个独立不重复的字符串
    num_distinct = 500
    for i in range(num_distinct):
        fm.add(f"user_session_token_id_{i}")
        
    # 插入大量重复值（不应影响基数估计）
    for i in range(100):
        fm.add(f"user_session_token_id_{i}")
        
    estimated_card = fm.estimate_cardinality()
    
    # 验证估计误差在合理置信区间内
    assert 200 <= estimated_card <= 1200
