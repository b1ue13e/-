"""
海量流数据挖掘算法模块：DGIM 滑动窗口计数与 Flajolet-Martin 基数估计
"""

import hashlib
import math
from typing import List, Tuple, Dict, Any, Optional

class DGIMBucket:
    def __init__(self, size: int, timestamp: int):
        self.size = size  # 必须是 2 的幂次: 1, 2, 4, 8...
        self.timestamp = timestamp


class DGIMStreamCounter:
    """
    DGIM (Datar-Gionis-Indyk-Motwani) 滑动窗口二进制流 1 计数器
    - 空间复杂度: O(log^2 N)
    - 规则 1: 桶的大小必须是 2 的整数次幂
    - 规则 2: 对于任意大小的桶，最多允许存在 2 个（当出现第 3 个相同大小的桶时，最旧的两个桶合并为一个 2 倍大小的桶）
    - 规则 3: 超出滑动窗口大小 N 的桶自动过期淘汰
    """
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.current_time = 0
        self.buckets: List[DGIMBucket] = []

    def update(self, bit: int):
        self.current_time += 1
        if bit != 1:
            return
            
        # 1. 插入新桶 (大小为 1)
        self.buckets.insert(0, DGIMBucket(1, self.current_time))
        
        # 2. 检查并合并桶 (维持任意大小至多 2 个桶的不变量)
        idx = 0
        while idx < len(self.buckets) - 2:
            # 检查是否有 3 个相同大小的桶
            if (self.buckets[idx].size == self.buckets[idx + 1].size == self.buckets[idx + 2].size):
                # 合并最旧的两个桶 (即 idx+1 和 idx+2)
                merged_size = self.buckets[idx + 1].size * 2
                merged_time = self.buckets[idx + 2].timestamp
                # 弹出旧桶并插入新合并桶
                self.buckets.pop(idx + 2)
                self.buckets.pop(idx + 1)
                self.buckets.insert(idx + 1, DGIMBucket(merged_size, merged_time))
                # 检查合并后是否会触发下一级连续合并
                idx += 1
            else:
                idx += 1
                
        # 3. 淘汰超出窗口大小的过期桶
        expire_time = self.current_time - self.window_size
        self.buckets = [b for b in self.buckets if b.timestamp > expire_time]

    def estimate_count(self, k: Optional[int] = None) -> int:
        """
        估算最近 k 个时间步长内的 1 的数量 (默认 k = window_size)
        - 累加完全包含在查询范围内的桶的大小
        - 对跨越边界的最旧桶，按一半大小估计 (b.size / 2)
        """
        if not self.buckets:
            return 0
            
        if k is None or k > self.window_size:
            k = self.window_size
            
        threshold_time = self.current_time - k
        total_count = 0
        last_bucket = None
        
        for b in self.buckets:
            if b.timestamp > threshold_time:
                total_count += b.size
                last_bucket = b
            else:
                last_bucket = b
                break
                
        if last_bucket is not None and last_bucket.timestamp <= threshold_time:
            total_count += last_bucket.size // 2
            
        return total_count


class FlajoletMartinEstimator:
    r"""
    Flajolet-Martin (FM) 基数估计器 (Distinct Elements Count)
    - 确定性 MD5 加盐映射
    - 计算尾随二进制 0 的最大长度 R = max \rho(h(x))
    - 理论估计值: E[2^R] = \phi * N，其中修正因子 \phi \approx 0.77351
    - 支持多哈希函数分桶 (Bucket Averaging) 减小方差
    """
    PHI = 0.77351

    def __init__(self, num_hashes: int = 64, num_groups: int = 8):
        self.num_hashes = num_hashes
        self.num_groups = num_groups
        self.p = 2147483647
        self.salts = [f"fm_salt_{i}_" for i in range(num_hashes)]
        self.max_trailing_zeros = [0] * num_hashes

    @staticmethod
    def trailing_zeros(val: int) -> int:
        if val == 0:
            return 32
        count = 0
        while (val & 1) == 0:
            count += 1
            val >>= 1
        return count

    def _hash_item(self, item: str, salt: str) -> int:
        h_str = hashlib.md5((salt + item).encode("utf-8")).hexdigest()
        return int(h_str[:8], 16) & 0x7FFFFFFF

    def add(self, item: str):
        for i, salt in enumerate(self.salts):
            h_val = self._hash_item(item, salt)
            tz = self.trailing_zeros(h_val)
            if tz > self.max_trailing_zeros[i]:
                self.max_trailing_zeros[i] = tz

    def estimate_cardinality(self) -> float:
        hashes_per_group = self.num_hashes // self.num_groups
        group_estimates = []
        
        for g in range(self.num_groups):
            group_r = self.max_trailing_zeros[g * hashes_per_group:(g + 1) * hashes_per_group]
            # 组内算术平均 R
            avg_r = sum(group_r) / len(group_r)
            group_est = (2.0 ** avg_r) / self.PHI
            group_estimates.append(group_est)
            
        # 所有组的中位数作为最终估计
        group_estimates.sort()
        mid = len(group_estimates) // 2
        if len(group_estimates) % 2 == 1:
            return group_estimates[mid]
        else:
            return (group_estimates[mid - 1] + group_estimates[mid]) / 2.0
