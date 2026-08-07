---
type: index
topic: "生成式AI基础与Prompt工程学习路径"
created: 2026-08-05
status: active
flow: knowledge
kind: moc
tags: [索引, 学习路径, 生成式AI, Prompt工程]
source: "MIT OCW 6.7960 Deep Learning Fall 2024; Stanford CS336 Spring 2025; Stanford CS324 Winter 2022/2023; CMU 17-630 public syllabus reference"
---

# 🗺️ 生成式 AI 基础与 Prompt 工程学习路径

> 目标不是背“万能提示词”，而是能解释模型为何这样输出、把模糊需求写成可验收规格、用实验比较提示方案，并为幻觉、注入和不确定性设计防线。

## 课程来源与使用边界

| 角色 | 公开课程 | 本课程用途 |
| :--- | :--- | :--- |
| 开放教材主线 | [MIT OCW 6.7960 Deep Learning](https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/)（CC BY-NC-SA 4.0） | 深度学习、Transformer、VAE/GAN/扩散与公开作业 |
| 开源实现主线 | [Stanford CS336 Spring 2025](https://cs336.stanford.edu/spring2025/) 与 MIT License A1-A4 仓库 | Tokenizer、Transformer、训练、推理、数据与 Scaling |
| Prompt 实验主线 | [Stanford CS324](https://stanford-cs324.github.io/winter2022/) 与 [2023 Intro Assignment](https://stanford-cs324.github.io/winter2023/assignment/) | Prompt 基线、模型比较与 LLM 评测实验；只链接公开材料 |
| Prompt 目录参考 | [CMU 17-630](https://www.cs.cmu.edu/~breaux/prompting/schedule.html) | ICL、CoT、RAG、评测、注入等知识顺序；页面有版权，不复制题面 |

> 本库只链接公开页面并写原创学习笔记，不转载未明确开放授权的答案。CMU 17-630 页面只公开作业名称时，映射页会明确标注“自学改编任务”，不冒充官方题面。

## 小白入口与学习节奏

先读 [[🧭 课程学习与认知支架]]，按“示范→补全→独立迁移”学习。小白建议 14 周、每周 7–9 小时；具备完整先修者可压缩到 10 周。

1. [[课程前置-Python-JSON测试与实验复现]]：自测至少 4/5。
2. [[课程前置-概率向量与Softmax最小补丁]]：自测至少 4/5。
3. 若做 MIT HW1：[[课程前置-神经网络数学-凸性几何链式法则与优化]]。
4. MIT HW1/PyTorch 分支：[[神经网络表达-ReLU分段线性逻辑门与泛化]]、[[深度学习工程-PyTorch张量自动微分与训练循环]]。
5. CS336 分支：[[Tokenizer工程-Unicode字节与BPE训练]]、[[训练优化-交叉熵AdamW调度梯度裁剪与检查点]]。
6. MIT HW5 分支：[[生成模型数学-高斯KL重参数化与扩散后验]]。
7. [[生成式AI-基础-概率生成Token与能力边界]]。
8. [[Prompt工程-需求-任务规格与结构化输出]]。
9. [[Prompt评测-实验-指标数据集与误差分析]]。
10. [[Prompt工程-上下文学习-示例选择与提示敏感性]]。

> 先评测、后优化示例，避免“ICL 依赖评测、评测又排在 ICL 后”的循环。两张前置卡任一未通过，只做作业 00，不直接进入 MIT/CS336 实现。

## 阶段一：模型心智模型

> 深度学习官方作业不是 Prompt 入门的隐含门槛：只走 Prompt 主线者读概念卡和微型实验；要完成 MIT/CS336 官方实现者必须先通过 ReLU、PyTorch、BPE、训练优化与高斯扩散五条先修 Gate。

| 类型 | 主题卡 | 作业作用 |
| :---: | :--- | :--- |
| 必需 | [[生成式AI-基础-概率生成Token与能力边界]] | 解释 Token、条件概率、上下文和幻觉来源 |
| 必需 | [[Transformer与大语言模型-架构-Transformer工作原理]] | 理解注意力、因果 Mask 与上下文依赖 |
| 必需 | [[Transformer与大语言模型-训练-GPT与自回归语言模型]] | 理解预训练目标、下一 Token 预测与 ICL 基础 |
| 必需 | [[生成控制-解码-温度Top-k与Top-p]] | 控制确定性、创造性和重复 |
| 全面 | [[生成式AI-模型家族-VAE-GAN与扩散模型]] | 覆盖文本之外的主流生成范式 |
| 全面 | [[生成式AI-多模态-条件生成与基础模型]] | 理解文本、图像与跨模态条件生成 |
| 全面 | [[模型适配-对齐-SFT-RLHF与DPO]] | 判断 Prompt、RAG、微调、对齐的边界 |

### 官方实现作业的工程卡

| 作业分支 | 必读主题卡 | 可开始官方代码的 Gate |
| :--- | :--- | :--- |
| MIT HW1 | [[神经网络表达-ReLU分段线性逻辑门与泛化]]、[[深度学习工程-PyTorch张量自动微分与训练循环]] | 逻辑门真值表、有限差分、单 batch 过拟合 |
| MIT HW2 | [[深度学习数学-对偶范数谱范数PowerIteration与最速下降]]、[[深度学习工程-宽度缩放WeightDecay卷积与受控比较]]、[[图表示学习-不变聚合消息传递与手性边界]] | 范数最速方向、谱估计、CNN shape、聚合碰撞与手性边界 |
| Stanford CS336 A1 | [[Tokenizer工程-Unicode字节与BPE训练]]、[[Transformer工程-RMSNorm-SwiGLU-RoPE与资源核算]]、[[训练优化-交叉熵AdamW调度梯度裁剪与检查点]] | Unicode round-trip、BPE 确定性、RMSNorm/RoPE、资源核算、标量 AdamW、恢复等价 |
| MIT HW4 | [[表征学习-对比损失表示几何双编码器与自编码器]] | InfoNCE 手算、温度/归一化、增强与重建边界 |
| MIT HW5 | [[生成模型数学-高斯KL重参数化与扩散后验]]、[[深度学习工程-PyTorch张量自动微分与训练循环]] | 闭式 KL、扩散后验、shape/梯度测试 |

## 阶段二：Prompt 需求表达

| 类型 | 主题卡 | 作业作用 |
| :---: | :--- | :--- |
| 必需 | [[Prompt工程-需求-任务规格与结构化输出]] | 把目标转成输入、规则、输出和验收条件 |
| 必需 | [[Prompt工程-方法-指令示例推理与约束]] | Prompt 方法总览与策略选择 |
| 必需 | [[Prompt工程-上下文学习-示例选择与提示敏感性]] | 设计 Few-shot 示例并控制顺序偏差 |
| 必需 | [[Prompt工程-推理-任务分解自一致性与验证]] | 处理多步任务并引入外部验证 |

## 阶段三：增强、评测与可靠性

| 类型 | 主题卡 | 作业作用 |
| :---: | :--- | :--- |
| 必需 | [[Prompt增强-RAG-检索生成与可追溯回答]] | 让回答基于给定资料并提供来源 |
| 必需 | [[Prompt评测-实验-指标数据集与误差分析]] | 固定数据集、指标和消融实验 |
| 全面 | [[Prompt评测-LLMJudge-偏置校准与人工复核]] | 正确使用模型评审并识别位置/长度偏置 |
| 必需 | [[生成式AI-可靠性-幻觉校准与事实核验]] | 区分未知、冲突和错误引用 |
| 必需 | [[Prompt工程-安全-提示注入与分层防护]] | 防御不可信上下文和越权请求 |

## 官方作业与知识覆盖

### 官方逐题/逐节导航

- MIT OCW：[[MIT-6.7960-HW01-逐题知识点映射]]、[[MIT-6.7960-HW02-逐题知识点映射]]、[[MIT-6.7960-HW03-逐节知识点映射]]、[[MIT-6.7960-HW04-逐题知识点映射]]、[[MIT-6.7960-HW05-逐题知识点映射]]。
- Stanford CS336：[[Stanford-CS336-A1-逐节知识点映射]]。
- Stanford CS324（仅链接导航）：[[Stanford-CS324-Prompt作业逐节导航]]。

### 本课程原创教学作业

作业 02/03/06 的可运行 starter、固定数据、adapter、runner 和自动 Gate 位于 `03-Projects/45-生成式AI基础与Prompt工程/starter/`。

| 作业 | 属性 | 最小知识集 | 映射 |
| :--- | :--- | :--- | :--- |
| 作业 0 环境与数学诊断 | 本课程原创 | Python、softmax、交叉熵、随机种子 | [[生成式AI与Prompt工程-作业00-环境与数学诊断]] |
| 作业 1 生成模型与 Transformer | 参考 MIT/CS336 的本地小规模原创实验 | 生成模型、Token、Transformer、解码 | [[生成式AI与Prompt工程-作业01-生成模型与Transformer实验]] |
| 作业 2 Prompt 基线与模型比较 | 参考 CS324 能力目标的原创实验 | Zero/Few-shot、任务定义、模型差异 | [[生成式AI与Prompt工程-作业02-Prompt基线与模型比较]] |
| 作业 3 Prompt 受控实验 | 借鉴 CS324 P1 交付结构的原创实验 | 数据切分、消融、错误分析 | [[生成式AI与Prompt工程-作业03-Prompt受控实验]] |
| 作业 4 推理与任务分解 | 基于公开讲义原创 | Direct/CoT/自一致性/分解 | [[生成式AI与Prompt工程-作业04-推理与任务分解]] |
| 作业 5 结构化输出与 Judge | 基于公开评测讲义原创 | Schema、Judge 偏置、人工复核 | [[生成式AI与Prompt工程-作业05-结构化输出与LLMJudge]] |
| 作业 6 RAG Prompt 增强 | 基于公开 RAG 讲义原创 | 检索、引用、忠实度、注入 | [[生成式AI与Prompt工程-作业06-RAGPrompt增强]] |
| 作业 7 红队与防御 | Berkeley/CMU 公开安全主题原创 | 注入、泄漏、威胁模型、Guardrail | [[生成式AI与Prompt工程-作业07-红队安全与可靠性]] |
| 结课项目 | MIT/CS324 项目交付结构 | 完整 Prompt 系统与可复现报告 | [[生成式AI与Prompt工程-结课项目]] |

## 全面知识点边界

- **本课必须掌握**：条件生成、Token/上下文、Transformer、自回归、解码、需求规格、ICL、分解、RAG、评测、幻觉、注入。
- **理解但不要求重训练大模型**：数据清洗、Scaling Laws、分布式训练、RLHF/DPO、多模态训练。
- **转入下一课程**：工具执行、状态机、长期记忆、多智能体与 Agent 评测进入 [[🗺️ AI-Agent工程-学习路径|AI Agent 工程学习路径]]。

## 闭卷结课验收

- [ ] 能画出“需求 → Prompt → 模型 → 校验 → 反馈”的闭环。
- [ ] 能对同一任务比较 Zero-shot、Few-shot、分解和 RAG 四种方案。
- [ ] 能建立至少 30 条固定评测样本并报告均值、失败类型和成本。
- [ ] 能解释 Prompt 注入为何是信任边界问题，而不是一句“忽略攻击”能解决。
- [ ] 能说清何时继续 Prompt、何时用 RAG、何时微调、何时交给 Agent。
