"""
频繁模式挖掘算法模块：Apriori 先验剪枝与 FP-Growth 条件模式基
"""

from collections import defaultdict, Counter
from typing import List, Set, Dict, Tuple, Optional, Any
import itertools

class AprioriMiner:
    """
    Apriori 频繁项集挖掘引擎
    - Join 步：连接 (k-1)-项集生成候选 k-项集 C_k
    - Prune 步：验证 C_k 的所有 (k-1) 子集是否均为频繁项集
    - 规则导出：计算 Support, Confidence, Lift, Conviction
    """
    def __init__(self, transactions: List[Set[str]], min_sup: int):
        self.transactions = [set(t) for t in transactions]
        self.num_tx = len(self.transactions)
        self.min_sup = min_sup
        self.frequent_itemsets: Dict[Tuple[str, ...], int] = {}

    def find_frequent_1_itemsets(self) -> Dict[Tuple[str, ...], int]:
        counts = defaultdict(int)
        for t in self.transactions:
            for item in t:
                counts[(item,)] += 1
        l1 = {k: v for k, v in counts.items() if v >= self.min_sup}
        return l1

    def generate_candidates_k(self, l_prev: List[Tuple[str, ...]], k: int) -> List[Tuple[str, ...]]:
        candidates = []
        n = len(l_prev)
        for i in range(n):
            for j in range(i + 1, n):
                t1, t2 = l_prev[i], l_prev[j]
                if t1[:k - 2] == t2[:k - 2]:
                    candidate = tuple(sorted(set(t1) | set(t2)))
                    # Prune step: check all (k-1) subsets
                    subsets = [candidate[:idx] + candidate[idx + 1:] for idx in range(len(candidate))]
                    if all(sub in l_prev for sub in subsets):
                        candidates.append(candidate)
        return candidates

    def mine(self) -> Dict[Tuple[str, ...], int]:
        l_current = self.find_frequent_1_itemsets()
        self.frequent_itemsets = dict(l_current)
        
        k = 2
        while l_current:
            l_prev_list = sorted(list(l_current.keys()))
            c_k = self.generate_candidates_k(l_prev_list, k)
            
            c_counts = defaultdict(int)
            for c in c_k:
                c_set = set(c)
                for t in self.transactions:
                    if c_set.issubset(t):
                        c_counts[c] += 1
                        
            l_current = {k_item: v for k_item, v in c_counts.items() if v >= self.min_sup}
            self.frequent_itemsets.update(l_current)
            k += 1
            
        return self.frequent_itemsets

    def extract_association_rules(self, min_confidence: float = 0.5) -> List[Dict[str, Any]]:
        if not self.frequent_itemsets:
            self.mine()
            
        rules = []
        for itemset, sup_count in self.frequent_itemsets.items():
            if len(itemset) < 2:
                continue
            itemset_set = set(itemset)
            sup_xy = sup_count / self.num_tx
            
            # 生成所有可能的真前件
            for r in range(1, len(itemset)):
                for antecedent_tuple in itertools.combinations(itemset, r):
                    antecedent = set(antecedent_tuple)
                    consequent = itemset_set - antecedent
                    
                    ant_key = tuple(sorted(antecedent))
                    con_key = tuple(sorted(consequent))
                    
                    sup_x = self.frequent_itemsets.get(ant_key, 0) / self.num_tx
                    sup_y = self.frequent_itemsets.get(con_key, 0) / self.num_tx
                    
                    if sup_x == 0:
                        continue
                    confidence = sup_xy / sup_x
                    if confidence >= min_confidence:
                        lift = (sup_xy / (sup_x * sup_y)) if sup_y > 0 else 0.0
                        conviction = ((1.0 - sup_y) / (1.0 - confidence)) if (1.0 - confidence) > 1e-9 else float('inf')
                        
                        rules.append({
                            "antecedent": ant_key,
                            "consequent": con_key,
                            "support": sup_xy,
                            "confidence": confidence,
                            "lift": lift,
                            "conviction": conviction,
                        })
        return rules


class FPNode:
    """FP-Tree 节点定义"""
    def __init__(self, item: str, count: int, parent: Optional['FPNode']):
        self.item = item
        self.count = count
        self.parent = parent
        self.children: Dict[str, 'FPNode'] = {}
        self.node_link: Optional['FPNode'] = None


class FPGrowthMiner:
    """
    FP-Growth 频繁项集挖掘引擎
    - 构建紧凑前缀树 FP-Tree 与项头表 Header Table
    - 自底向上提取条件模式基 (Conditional Pattern Bases)
    - 递归构建条件 FP-Tree，避免庞大的候选集生成开销
    """
    def __init__(self, transactions: List[Set[str]], min_sup: int):
        self.transactions = [set(t) for t in transactions]
        self.min_sup = min_sup
        self.frequent_itemsets: Dict[Tuple[str, ...], int] = {}

    def build_tree(self, transactions: List[List[str]], item_counts: Dict[str, int]) -> Tuple[FPNode, Dict[str, Optional[FPNode]]]:
        root = FPNode("null", 1, None)
        header_table: Dict[str, Optional[FPNode]] = {item: None for item in item_counts}

        for tx in transactions:
            # 仅保留频繁项并按全局频次降序排列
            filtered_items = [item for item in tx if item in item_counts]
            filtered_items.sort(key=lambda x: (item_counts[x], x), reverse=True)
            
            curr_node = root
            for item in filtered_items:
                if item in curr_node.children:
                    curr_node.children[item].count += 1
                else:
                    new_node = FPNode(item, 1, curr_node)
                    curr_node.children[item] = new_node
                    
                    # 维护项头表链表
                    if header_table[item] is None:
                        header_table[item] = new_node
                    else:
                        ptr = header_table[item]
                        while ptr.node_link is not None:
                            ptr = ptr.node_link
                        ptr.node_link = new_node
                curr_node = curr_node.children[item]
                
        return root, header_table

    def mine_tree(self, header_table: Dict[str, Optional[FPNode]], prefix: List[str]):
        # 按频次升序遍历项头表中的项
        sorted_items = sorted(header_table.keys(), key=lambda x: sum(self._get_counts(header_table[x])))
        
        for item in sorted_items:
            new_prefix = prefix + [item]
            itemset = tuple(sorted(new_prefix))
            support = sum(self._get_counts(header_table[item]))
            if support >= self.min_sup:
                self.frequent_itemsets[itemset] = support
                
                # 抽取条件模式基
                cond_patt_bases = []
                ptr = header_table[item]
                while ptr is not None:
                    path = []
                    curr = ptr.parent
                    while curr is not None and curr.item != "null":
                        path.append(curr.item)
                        curr = curr.parent
                    for _ in range(ptr.count):
                        if path:
                            cond_patt_bases.append(path)
                    ptr = ptr.node_link
                    
                # 统计条件模式基中项的频次
                cond_counts = defaultdict(int)
                for path in cond_patt_bases:
                    for p_item in path:
                        cond_counts[p_item] += 1
                cond_counts = {k: v for k, v in cond_counts.items() if v >= self.min_sup}
                
                if cond_counts:
                    _, cond_header = self.build_tree(cond_patt_bases, cond_counts)
                    self.mine_tree(cond_header, new_prefix)

    def _get_counts(self, node: Optional[FPNode]) -> List[int]:
        counts = []
        curr = node
        while curr is not None:
            counts.append(curr.count)
            curr = curr.node_link
        return counts

    def mine(self) -> Dict[Tuple[str, ...], int]:
        counts = defaultdict(int)
        for t in self.transactions:
            for item in t:
                counts[item] += 1
        freq_1 = {k: v for k, v in counts.items() if v >= self.min_sup}
        if not freq_1:
            return {}
            
        root, header_table = self.build_tree([[item for item in t] for t in self.transactions], freq_1)
        self.frequent_itemsets = {}
        self.mine_tree(header_table, [])
        return self.frequent_itemsets
