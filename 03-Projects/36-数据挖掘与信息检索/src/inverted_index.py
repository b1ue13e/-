"""
信息检索核心模块：倒排索引构建、Variable Byte 变长字节压缩与 BM25 概率评分
"""

import math
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set, Optional, Any

class VariableByteCodec:
    """
    Variable Byte (VB) 变长字节编码器与 d-gaps 差分压缩
    - 每个字节最高位（MSB, 第 8 位）作为 Continuation Bit（终止位）
    - 0 表示后续仍有字节，1 表示当前是数字的最后一个字节
    - 低 7 位存储数值的二进制有效载荷
    """
    @staticmethod
    def encode_number(num: int) -> bytes:
        if num == 0:
            return bytes([0x80])
        byte_list = []
        while True:
            byte_list.insert(0, num % 128)
            if num < 128:
                break
            num //= 128
        # 将最后一个字节的最高位置 1
        byte_list[-1] += 128
        return bytes(byte_list)

    @staticmethod
    def decode_numbers(stream: bytes) -> List[int]:
        numbers = []
        curr = 0
        for b in stream:
            if b < 128:
                curr = 128 * curr + b
            else:
                curr = 128 * curr + (b - 128)
                numbers.append(curr)
                curr = 0
        return numbers

    @classmethod
    def encode_gaps(cls, doc_ids: List[int]) -> bytes:
        """对单调递增有序的 doc_id 列表计算 d-gaps 并压缩"""
        if not doc_ids:
            return b""
        gaps = [doc_ids[0]]
        for i in range(1, len(doc_ids)):
            gaps.append(doc_ids[i] - doc_ids[i - 1])
        
        encoded = bytearray()
        for g in gaps:
            encoded.extend(cls.encode_number(g))
        return bytes(encoded)

    @classmethod
    def decode_gaps(cls, stream: bytes) -> List[int]:
        """解压 VB 字节流并累加前缀和还原 doc_ids"""
        gaps = cls.decode_numbers(stream)
        if not gaps:
            return []
        doc_ids = [gaps[0]]
        for i in range(1, len(gaps)):
            doc_ids.append(doc_ids[-1] + gaps[i])
        return doc_ids


class BM25Scorer:
    """
    Okapi BM25 概率相关度检索模型 (Robertson-Spärck Jones)
    - 词项饱和度参数 k1: 控制 TF 饱和速度 (默认 1.5)
    - 文档长度归一化参数 b: 控制文档长度惩罚力度 (默认 0.75)
    - IDF(q) = ln( (N - df + 0.5) / (df + 0.5) + 1.0 )
    """
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b

    def idf(self, df: int, total_docs: int) -> float:
        # RSJ 平滑 IDF
        return math.log(1.0 + (total_docs - df + 0.5) / (df + 0.5))

    def score_term(self, tf: int, doc_len: int, avgdl: float, idf_val: float) -> float:
        numerator = tf * (self.k1 + 1.0)
        denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / avgdl))
        return idf_val * (numerator / denominator)


class InvertedIndex:
    """
    生产级内存倒排索引引擎
    - 词项字典 (Dictionary)
    - 倒排链表 (Posting Lists) 支持原始 List 与 VB 压缩 Byte 存储
    - 双指针快速求交 (Two-pointer Intersection)
    - 集成 BM25 语料库评分
    """
    def __init__(self, use_compression: bool = False):
        self.use_compression = use_compression
        self.postings: Dict[str, Any] = defaultdict(list)
        self.term_freqs: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_lengths: Dict[int, int] = {}
        self.doc_map: Dict[int, str] = {}
        self.reverse_doc_map: Dict[str, int] = {}
        self.scorer = BM25Scorer()
        self.next_doc_id = 1

    def tokenize(self, text: str) -> List[str]:
        cleaned = "".join(ch.lower() if ch.isalnum() or ch.isspace() else " " for ch in text)
        return [w for w in cleaned.split() if len(w) > 0]

    def add_document(self, string_id: str, text: str):
        doc_id = self.next_doc_id
        self.next_doc_id += 1
        self.doc_map[doc_id] = string_id
        self.reverse_doc_map[string_id] = doc_id

        tokens = self.tokenize(text)
        self.doc_lengths[doc_id] = len(tokens)
        counts = Counter(tokens)

        for term, freq in counts.items():
            self.postings[term].append(doc_id)
            self.term_freqs[term][doc_id] = freq

    def finalize(self):
        """如果启用了压缩，将所有 postings 压缩为 VB d-gaps 字节流"""
        if self.use_compression:
            compressed_postings = {}
            for term, p_list in self.postings.items():
                p_list_sorted = sorted(list(set(p_list)))
                compressed_postings[term] = VariableByteCodec.encode_gaps(p_list_sorted)
            self.postings = compressed_postings

    def get_postings(self, term: str) -> List[int]:
        term = term.lower()
        if term not in self.postings:
            return []
        if self.use_compression:
            return VariableByteCodec.decode_gaps(self.postings[term])
        return sorted(list(set(self.postings[term])))

    def boolean_and_query(self, terms: List[str]) -> List[str]:
        """双指针线性求交算法 O(L1 + L2)"""
        if not terms:
            return []
        
        postings_lists = [self.get_postings(t) for t in terms]
        # 按倒排链长度升序排列，优先遍历最短链
        postings_lists.sort(key=len)
        
        if not postings_lists or not postings_lists[0]:
            return []
            
        result = postings_lists[0]
        for p_list in postings_lists[1:]:
            intersected = []
            i, j = 0, 0
            while i < len(result) and j < len(p_list):
                if result[i] == p_list[j]:
                    intersected.append(result[i])
                    i += 1
                    j += 1
                elif result[i] < p_list[j]:
                    i += 1
                else:
                    j += 1
            result = intersected
            if not result:
                break
                
        return [self.doc_map[doc_id] for doc_id in result]

    def search_bm25(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        q_tokens = self.tokenize(query)
        if not q_tokens or not self.doc_lengths:
            return []

        total_docs = len(self.doc_lengths)
        avgdl = sum(self.doc_lengths.values()) / total_docs
        scores = defaultdict(float)

        for q in q_tokens:
            posting = self.get_postings(q)
            df = len(posting)
            if df == 0:
                continue
            idf_val = self.scorer.idf(df, total_docs)
            for doc_id in posting:
                tf = self.term_freqs[q].get(doc_id, 0)
                doc_len = self.doc_lengths[doc_id]
                scores[doc_id] += self.scorer.score_term(tf, doc_len, avgdl, idf_val)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [(self.doc_map[doc_id], score) for doc_id, score in ranked[:top_k]]
