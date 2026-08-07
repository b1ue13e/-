"""
08-NLP全栈 阶段作业 01: Beam Search 束搜索解码器实现
"""

import torch
import torch.nn.functional as F


def beam_search_decode(model_step_fn, start_token: int, end_token: int, beam_width: int = 3, max_len: int = 20):
    """
    束搜索解码算法
    model_step_fn: callable(input_token, hidden) -> (logits [1, V], next_hidden)
    returns: best_sequence (List[int]), best_score (float)
    """
    # 存 (tokens, cumulative_log_prob, hidden_state)
    beams = [([start_token], 0.0, None)]
    completed = []

    for _ in range(max_len):
        candidates = []
        for seq, score, hidden in beams:
            if seq[-1] == end_token:
                completed.append((seq, score))
                continue
                
            last_token = seq[-1]
            logits, next_hidden = model_step_fn(last_token, hidden)
            log_probs = F.log_softmax(logits, dim=-1).squeeze(0) # [V]
            
            topk_log_probs, topk_indices = torch.topk(log_probs, beam_width)
            for k in range(beam_width):
                token = topk_indices[k].item()
                prob = topk_log_probs[k].item()
                candidates.append((seq + [token], score + prob, next_hidden))

        if not candidates:
            break

        # 选出 Top beam_width 个候选
        candidates.sort(key=lambda x: x[1], reverse=True)
        beams = candidates[:beam_width]

        # 提前终止条件
        if len(completed) >= beam_width:
            break

    # 包含未遇到 EOS 的剩余 Beams
    for seq, score, _ in beams:
        completed.append((seq, score))

    completed.sort(key=lambda x: x[1] / len(x[0]), reverse=True) # 按长度归一化分数排序
    return completed[0][0], completed[0][1]
