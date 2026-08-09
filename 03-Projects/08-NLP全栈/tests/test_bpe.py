"""
课后作业 02: 子词分词与 BPE 算法 单元测试
"""
import pytest

class BPETokenizer:
    def __init__(self, vocab_size: int = 100):
        self.vocab_size = vocab_size
        self.merges = {}
        self.vocab = set()

    def get_stats(self, ids_list):
        counts = {}
        for ids in ids_list:
            for pair in zip(ids[:-1], ids[1:]):
                counts[pair] = counts.get(pair, 0) + 1
        return counts

    def merge(self, ids_list, pair, idx):
        new_ids_list = []
        for ids in ids_list:
            new_ids = []
            i = 0
            while i < len(ids):
                if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
                    new_ids.append(idx)
                    i += 2
                else:
                    new_ids.append(ids[i])
                    i += 1
            new_ids_list.append(new_ids)
        return new_ids_list

    def train(self, texts, num_merges: int = 10):
        ids_list = [list(text.encode("utf-8")) for text in texts]
        curr_idx = 256
        for _ in range(num_merges):
            stats = self.get_stats(ids_list)
            if not stats:
                break
            best_pair = max(stats, key=stats.get)
            self.merges[best_pair] = curr_idx
            ids_list = self.merge(ids_list, best_pair, curr_idx)
            curr_idx += 1
        return self.merges

def test_bpe_tokenizer_training():
    tokenizer = BPETokenizer()
    corpus = ["hug", "hug", "hugs", "hugger"]
    merges = tokenizer.train(corpus, num_merges=3)
    
    assert len(merges) > 0, "BPE 应该成功学习到至少一个 merge 规则"
    assert any(idx >= 256 for idx in merges.values()), "合并后的 token ID 应该大于 255"

def test_bpe_frequency_count():
    tokenizer = BPETokenizer()
    ids_list = [[104, 117, 103], [104, 117, 103]] # "hug", "hug" in ASCII
    stats = tokenizer.get_stats(ids_list)
    
    assert stats[(104, 117)] == 2, "pair (h, u) 的频次计算结果应为 2"
    assert stats[(117, 103)] == 2, "pair (u, g) 的频次计算结果应为 2"
