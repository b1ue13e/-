"""
高维近重复检测与哈希模块：MinHash 签名矩阵与局部敏感哈希 (LSH)
"""

import hashlib
import numpy as np
from typing import List, Set, Dict, Tuple, Any

class MinHashLSH:
    """
    MinHash + LSH (Locality Sensitive Hashing) 文本近重复检测引擎
    - 特征提取：k-Shingles (字符/词级别)
    - MinHash 签名：使用 K 个伪随机哈希函数 h_i(x) = (a_i * x + b_i) % p
    - LSH 分桶：划分为 b 个 bands，每个 band 包含 r 行 (K = b * r)
    - 理论 S 曲线：P(Collision) = 1 - (1 - s^r)^b
    """
    def __init__(self, num_perm: int = 100, num_bands: int = 25, p: int = 2147483647, seed: int = 42):
        assert num_perm % num_bands == 0, "num_perm 必须能被 num_bands 整除"
        self.num_perm = num_perm
        self.num_bands = num_bands
        self.rows_per_band = num_perm // num_bands
        self.p = p
        
        np.random.seed(seed)
        self.a = np.random.randint(1, self.p - 1, size=self.num_perm, dtype=np.int64)
        self.b = np.random.randint(0, self.p - 1, size=self.num_perm, dtype=np.int64)
        
        # LSH 桶存储：band_idx -> bucket_hash -> list of doc_ids
        self.buckets: List[Dict[str, List[str]]] = [dict() for _ in range(self.num_bands)]
        self.signatures: Dict[str, np.ndarray] = {}

    @staticmethod
    def get_shingles(text: str, k: int = 1) -> Set[str]:
        cleaned = "".join(ch.lower() if ch.isalnum() or ch.isspace() else " " for ch in text)
        words = [w for w in cleaned.split() if w]
        if len(words) < k:
            return {cleaned}
        return {" ".join(words[i:i + k]) for i in range(len(words) - k + 1)}

    @staticmethod
    def jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
        union_len = len(set_a | set_b)
        if union_len == 0:
            return 1.0
        return len(set_a & set_b) / union_len

    @staticmethod
    def _deterministic_hash(s: str) -> int:
        h_str = hashlib.md5(s.encode("utf-8")).hexdigest()
        return int(h_str[:8], 16) & 0x7FFFFFFF

    def compute_minhash_signature(self, shingles: Set[str]) -> np.ndarray:
        if not shingles:
            return np.zeros(self.num_perm, dtype=np.int64)
            
        shingle_hashes = np.array([self._deterministic_hash(s) for s in shingles], dtype=np.int64)
        
        # 矩阵广播计算所有置换的哈希值: (num_perm, num_shingles)
        # H_ij = (a_i * hash_j + b_i) % p
        h_matrix = (self.a[:, None] * shingle_hashes[None, :] + self.b[:, None]) % self.p
        signature = np.min(h_matrix, axis=1)
        return signature

    def insert(self, doc_id: str, shingles: Set[str]):
        sig = self.compute_minhash_signature(shingles)
        self.signatures[doc_id] = sig
        
        # 将签名分划至 b 个 bands
        for band_idx in range(self.num_bands):
            start = band_idx * self.rows_per_band
            end = start + self.rows_per_band
            band_chunk = sig[start:end].tobytes()
            bucket_key = hashlib.md5(band_chunk).hexdigest()
            
            if bucket_key not in self.buckets[band_idx]:
                self.buckets[band_idx][bucket_key] = []
            self.buckets[band_idx][bucket_key].append(doc_id)

    def query_candidates(self, doc_id: str) -> Set[str]:
        if doc_id not in self.signatures:
            return set()
        sig = self.signatures[doc_id]
        candidates = set()
        
        for band_idx in range(self.num_bands):
            start = band_idx * self.rows_per_band
            end = start + self.rows_per_band
            band_chunk = sig[start:end].tobytes()
            bucket_key = hashlib.md5(band_chunk).hexdigest()
            
            matched = self.buckets[band_idx].get(bucket_key, [])
            for cand_id in matched:
                if cand_id != doc_id:
                    candidates.add(cand_id)
                    
        return candidates

    def estimate_similarity(self, doc_a: str, doc_b: str) -> float:
        if doc_a not in self.signatures or doc_b not in self.signatures:
            return 0.0
        sig_a = self.signatures[doc_a]
        sig_b = self.signatures[doc_b]
        return float(np.mean(sig_a == sig_b))
