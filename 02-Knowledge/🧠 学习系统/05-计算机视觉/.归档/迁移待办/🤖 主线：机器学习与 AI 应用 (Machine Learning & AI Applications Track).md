---
topic: "主线-机器学习与AI应用"
type: index
kind: moc
flow: knowledge
track: "机器学习与AI应用"
status: active
created: 2026-07-30
updated: 2026-07-30
tags:
  - MOC
  - 主线
  - 机器学习
  - 深度学习
  - AI应用
  - 知识网络
---

# 🤖 主线：机器学习与 AI 应用 (Machine Learning & AI Applications Track)

> 🧭 **主线宗旨**：整合经典机器学习、概率图模型、强化学习以及计算机视觉 (CV)、自然语言处理 (NLP)、图神经网络 (GNN) 与数据挖掘等前沿应用。严格收拢通用 ML/DL 算法主卡，构建从监督/无监督基础到多模态与序贯决策的现代化 AI 知识网络。

---

## 🗺️ 8 门子线路径逻辑递进图

```mermaid
flowchart TD
    subgraph 机器学习与概率结构底座
        ML0["[[🗺️ 机器学习学习路径\|17-机器学习]]<br/>(SVM, 树模型, SGD, 神经网络基础)"]
        ML0 --> PGM["[[🗺️ 概率图模型学习路径|14-概率图模型]]<br/>(Bayesian Network, CRF, Variational Inference)"]
        ML0 --> RL["[[🗺️ 强化学习学习路径|13-强化学习]]<br/>(MDP, Q-Learning, Policy Gradient, PPO)"]
    end

    subgraph 领域应用与感知专题
        ML0 --> CV["[[🗺️ 计算机视觉学习路径|05-计算机视觉]]<br/>(CNN, ResNet, YOLO, ViT, Diffusion)"]
        ML0 --> NLP["[[🗺️ NLP全栈学习路径\|08-NLP全栈]]<br/>(RNN, Transformer, BERT, LLM Pretraining)"]
        ML0 --> GNN["[[🗺️ 图神经网络学习路径\|23-图神经网络]]<br/>(Message Passing, GCN, GAT, GraphSAGE)"]
    end

    subgraph 数据挖掘与网络分析
        ML0 --> DM["[[🗺️ 数据挖掘与信息检索学习路径\|36-数据挖掘与信息检索]]<br/>(Vector Search, BM25, PageRank, 推荐系统)"]
        GNN & DM --> SNM["[[🗺️ 社交网络挖掘学习路径|01-社交网络挖掘]]<br/>(社区发现, 链路预测, 传播模型)"]
    end
```

---

## 🔑 全库唯一 Master 概念卡

通用机器学习算法与深度学习核心架构统一收拢至 `17-机器学习` 与 `08-NLP全栈` 中的 canonical 主卡：

1. **梯度下降与反向传播**：[[反向传播算法BP]] ($\frac{\partial \mathcal{L}}{\partial \mathbf{W}}$)
2. **Transformer 自注意力机制**：[[Transformer自注意力机制]] ($\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$)
3. **马尔可夫决策过程 MDP**：[[马尔可夫决策过程MDP]] ($\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$)
4. **图卷积与消息传递**：[[图卷积网络GCN]] ($\mathbf{H}^{(l+1)} = \sigma\left(\tilde{\mathbf{D}}^{-\frac{1}{2}} \tilde{\mathbf{A}} \tilde{\mathbf{D}}^{-\frac{1}{2}} \mathbf{H}^{(l)} \mathbf{W}^{(l)}\right)$)
5. **KL 散度与变分推断**：[[KL散度]] ($D_{\text{KL}}(P || Q)$)

---

## 📊 包含子路径看板 (Dataview)

```dataview
TABLE course AS "课程名称", status AS "状态", importance AS "优先级", updated AS "最近更新"
FROM "02-Knowledge/🧠 学习系统"
WHERE type = "index" AND track = "机器学习与AI应用"
SORT file.name ASC
```

---

*主线更新时间：2026-07-30 | 状态：active*
