# Awesome-Weight-Space-Programming

简体中文 · [English](README.md)

本仓库整理**权重空间编程（Weight-Space Programming，WSP）**的研究资源，涵盖神经网络权重读取、训练后模型修复、按任务规范编写权重，以及通过参数编辑写入可复用的计算。

**收录截至 2026 年 11 月 25 日。** [中文检索与证据复核](docs/research-review.md) · [BibTeX 引用](references.bib) · [贡献指南](CONTRIBUTING.md)

## 收录范围

直接 WSP 研究让编程者访问模型参数，以推断或实现特定计算。许多研究使用配备工具的通用语言模型，也有研究采用明确规定的权重程序。目录区分直接读取张量数值、通过代码访问张量和获取模型行为反馈。梯度使用情况是另一项实验条件。即使编辑过程不使用反向传播，也可能利用带标签的反馈拟合系数或筛选候选修改。 [Sparks 原始报告与作者回应](https://rikiyat.github.io/blog/weight-space-programming/#response-to-comments)

基础与相关工作可作为技术先例或实验基线，其中包括专用读取器、行为探针、编译器、带数值拟合的编辑方法和训练式权重生成器。条目同时标出发表状态和贡献类型。arXiv 日期为首次提交日期。

## 目录

- [入门导读](#入门导读)
- [直接权重空间编程](#直接权重空间编程)
  - [读取与诊断](#读取与诊断)
  - [修复与适配](#修复与适配)
  - [编写与编译](#编写与编译)
  - [能力写入与组合](#能力写入与组合)
  - [自编辑与迭代反馈](#自编辑与迭代反馈)
- [评测基准](#评测基准)
- [复现与对照实验](#复现与对照实验)
- [工具与运行时](#工具与运行时)
- [基础与相关工作](#基础与相关工作)
  - [程序到权重的编译](#程序到权重的编译)
  - [权重读取与可解释性](#权重读取与可解释性)
  - [行为探针对照](#行为探针对照)
  - [相关模型编辑方法](#相关模型编辑方法)
  - [模型编辑验证与修复](#模型编辑验证与修复)
  - [权重组合与学习式生成](#权重组合与学习式生成)
  - [相关基准与模型库](#相关基准与模型库)
- [应用领域](#应用领域)

## 入门导读

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights](https://rikiyat.github.io/blog/weight-space-programming/) | 作者报告 · 2026-11-02 | 实证研究 | 通过八项读取、修复和写入实验介绍权重空间编程。各实验的代码访问和反馈条件不同。 [实验日志](https://github.com/RikiyaT/lm_understand-logs) |

- 系统评测与失败案例可从 WeightBench 入手，并结合独立复现了解规则编译与输入层线索。 [WeightBench](https://arxiv.org/abs/2611.18553) · [独立复现](https://arxiv.org/abs/2611.21449)
- 持久能力写入可先读 WeightCode，再对照 ICL 研究中从上下文示例导出的编辑。 [WeightCode](https://arxiv.org/abs/2611.25476) · [将 ICL 写入权重](https://arxiv.org/abs/2611.26841v2)
- 了解领域边界时，可以对照程序到权重的编译与权重空间学习综述的分类。 [Tracr](https://papers.nips.cc/paper_files/paper/2023/hash/771155abaae744e08576f1f3b4b7ac0d-Abstract-Conference.html) · [权重空间学习综述](https://arxiv.org/abs/2603.10090)

## 直接权重空间编程

### 读取与诊断

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [Function-Preserving Audits of Visual Weight Readers](https://arxiv.org/abs/2611.05798v2) | arXiv 预印本 · 2026-11-04 · v2 | 实证研究 | 用保持神经场函数不变的变换，检验权重读取器识别的是函数本身还是其参数化形式。 |
| [Weight-space programming for auditing clinical decision networks](https://arxiv.org/abs/2611.05341) | arXiv 预印本 · 2026-11-03 | 实证研究 | 在小型临床决策网络中审计和修复人为植入的规则故障。识别无故障网络仍有局限。 |
| [Weight-Space Reading](https://www.alphaxiv.org/abs/2611.weight-space-reading-language-models) | 作者报告 · 2026-11 | 实证研究 | 比较直接访问张量与读取配对编辑的文字描述这两种条件下的效果预测。实验尚无法确定读取自身权重是否有优势。 [代码](https://github.com/suayptalha/wsr) |

### 修复与适配

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [Can LLMs Debug Robots by Editing Their Weights?](https://arxiv.org/abs/2611.09376) | arXiv 预印本 · 2026-11-06 | 实证研究 | 在模拟器反馈预算受限的条件下修复机器人策略对指令词汇的理解。其他编辑实验大多未取得经验证的收益。 |
| [Repairing Robot Policies with Weight Space Programming](https://jstranghoener.github.io/blog/robotic-weight-space-programming/) | 作者报告 · 2026-11-11 | 实证研究 | 测试分布偏移下的仿真操作策略修复。同一目标的留出回合上取得的收益未迁移到留出的新目标。 |
| [Distilling Instructions into Weights: Closed-Form Edits Fix a Robot Policy's Misreading](https://arxiv.org/abs/2611.11894) | arXiv 预印本 · 2026-11-09 | 方法与基准 | 用闭式编辑将有效的指令改写蒸馏进机器人策略，并使用配对的留出随机种子评估。 |
| [Mixed Signals: Weight-Space Programming for EEG and ECG](https://arxiv.org/abs/2611.13758) | arXiv 预印本 · 2026-11-10 | 实证研究 | 在不同数据和反馈条件下，测试直接构造和修复小型脑电（EEG）与心电（ECG）分类器。 |
| [Training Vision Models for LLM-Driven Weight-Space Programming](https://arxiv.org/abs/2611.26408) | arXiv 预印本 · 2026-11-19 | 方法与基准 | 比较多种面向后续闭式编辑的视觉模型训练方案，并在留出集上评估效果与副作用。 [项目页](https://viscom.uni-ulm.de/wsp/) |
| [Keel: A Frontier Model Teaches a Vision-Language Model by Rewriting Its Weights](https://arxiv.org/abs/2611.25257) | arXiv 预印本 · 2026-11-18 | 方法 | 用多模态诊断和经筛选的持久编辑修复 Qwen3.5-0.8B 与 2B 的推理循环，并评估循环频率、答案长度和准确率。 |
| [Weight-space programming and mechanistic interpretability for model editing in particle physics](https://arxiv.org/abs/2611.27079) | arXiv 预印本 · 2026-11-20 | 实证研究 | 在查询预算受限的条件下，比较智能体编辑和稀疏自编码器引导的方法对粒子物理喷注分类器的修复效果。 |
| [Can a Frontier LLM Repair a Quantized Network by Tool-Free Weight-Space Programming?](https://arxiv.org/abs/2611.33031v1) | arXiv 预印本 · 2026-11-24 · v1 | 实证研究 | 研究通过参数修改进行模型修复或适配。 |
| [Reading, Writing and Repairing Game-Theoretic Policies in Weight Space](https://arxiv.org/abs/2611.31979v1) | arXiv 预印本 · 2026-11-24 · v1 | 实证研究 | 研究通过参数修改进行模型修复或适配。 |
| [Sparks of Weight-Space Programming for Robot Foundation Models](https://arxiv.org/abs/2611.31715v1) | arXiv 预印本 · 2026-11-24 · v1 | 实证研究 | 研究通过参数修改进行模型修复或适配。 |
| [TowerBridge: Bridging the Dual-Encoder Modality Gap via Weight-Space Programming](https://arxiv.org/abs/2611.31233v1) | arXiv 预印本 · 2026-11-23 · v1 | 实证研究 | 研究通过参数修改进行模型修复或适配。 |
| [Weight Coding: Evolving Web-Scale Recommenders through Direct Weight Edits with LLM Agents](https://arxiv.org/abs/2611.29613v1) | arXiv 预印本 · 2026-11-22 · v1 | 实证研究 | 研究通过参数修改进行模型修复或适配。 |
| [Autonomous Parameter Surgery: How LLMs Implant Selective Backdoors into Language Models](https://arxiv.org/abs/2611.27920v1) | arXiv 预印本 · 2026-11-20 · v1 | 实证研究 | 研究通过参数修改进行模型修复或适配。 |
| [Gradient-Free Few-Shot Adaptation of Vision Models via Agentic Coding](https://arxiv.org/abs/2611.28105v1) | arXiv 预印本 · 2026-11-17 · v1 | 实证研究 | 研究通过参数修改进行模型修复或适配。 |

### 编写与编译

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [Interpretable weight-space programming builds transparent transformers and brain encoding models](https://arxiv.org/abs/2611.18114) | arXiv 预印本 · 2026-11-13 | 方法 | 用智能体编写的参数和解析构造的特征构建可解释模型，涵盖语言与脑编码实验。 |
| [Compiling Known Rules into Compact Neural Agents: Weight-Space Programming on Unseen Games](https://arxiv.org/abs/2611.16981) | arXiv 预印本 · 2026-11-12 | 方法与基准 | 在未公开的游戏族和留出关卡上检验从规则到策略的编译，并与表现更强的 Python 智能体比较。 [代码](https://github.com/JensLehmann/weight-space-programming-games) |
| [Weight-Space Programming Doesn't Need Transformers](https://arxiv.org/abs/2611.22055) | arXiv 预印本 · 2026-11-17 | 实证研究 | 比较固定目标架构与自由设计架构。编辑器在所测任务中偏向选择稀疏关联表。 |
| [Zero-Shot Weight-Space Programming for Prediction and Classification of Target Variables in Structured Datasets](https://arxiv.org/abs/2611.19292v3) | arXiv 预印本 · 2026-11-14 · v3 | 实证研究 | 让大语言模型根据带标签的表格样例直接给出参数数值，提交前不运行目标网络。 |
| [Zero-Shot Weight-Space Programming Across a Difficulty-Graded Ladder of Two-Player Games](https://arxiv.org/abs/2611.09271v4) | arXiv 预印本 · 2026-11-06 · v4 | 实证研究 | 在策略复杂度逐级递增的双人游戏中评估直接写入权重。 |
| [Can a Language Model Write the Weights? An Empirical Study of LLM-Written Scoring Networks for Column Generation and MILP Branching, with a Bus-Driver Scheduling Application](https://arxiv.org/abs/2611.09559) | arXiv 预印本 · 2026-11-06 | 实证研究 | 评估由大语言模型为列生成和混合整数规划分支编写的评分网络，并与求解器及人工设计的基线比较。 |
| [Weight-Space Programming for Medical Imaging: Do We Still Need Training Data?](https://arxiv.org/abs/2611.12066) | arXiv 预印本 · 2026-11-09 | 实证研究 | 在没有训练数据的条件下构建小型医学影像模型，并在 MedMNIST 上与监督训练的模型比较。 |
| [Physics2Weight: Direct Neural Network Architecture and Weight Generation from Physical Laws Using Large Language Models](https://arxiv.org/abs/2611.12954) | arXiv 预印本 · 2026-11-07 | 方法 | 利用偏微分方程（PDE）的结构生成网络架构及权重。非线性算例显示了该方法的适用边界。 |
| [Weight-Space Programming of Variational Quantum Circuits: Large Language Models Write Quantum Circuit Parameters Without an Optimizer](https://arxiv.org/abs/2611.11537) | arXiv 预印本 · 2026-11-08 | 实证研究 | 将直接写入参数扩展到变分量子线路，并在多个量子计算目标上进行评估。 |
| [Weight-Space Programming of Policies and Their Verification via Model Checking](https://arxiv.org/abs/2611.11604) | arXiv 预印本 · 2026-11-08 | 方法 | 结合权重空间中的策略合成与模型检验，评估形式化的可达性保证。 |
| [Weight-space programming for tractor guidance controller: large language models natively write neural network weights that steer a real tractor](https://arxiv.org/abs/2611.21958) | arXiv 预印本 · 2026-11-16 | 实证研究 | 编写紧凑的神经网络转向控制器，并在仿真环境和真实拖拉机上评估。 |
| [Weight-Space Programming for Materials Science](https://arxiv.org/abs/2611.22013) | arXiv 预印本 · 2026-11-17 | 实证研究 | 将领域知识转化为用于材料属性排序的权重，过程无需带标签的训练样例。 |
| [Looped Weight-Space Programming: LLM-Written Transformers for Long Algorithmic Reasoning](https://mbzuai-oryx.github.io/LoopedWSP/) | 作者报告 · 2026-11-23 | 实证研究 | 为迷宫搜索等指定算法编写循环 Transformer 权重，并与经过训练的模型及直接提示大语言模型的做法比较。 [代码](https://github.com/mbzuai-oryx/LoopedWSP) |
| [PAWP-TTS: Phoneme-Aware Weight Programming for Compact Bilingual English-Nepali Speech Synthesis](https://arxiv.org/abs/2611.29455v1) | arXiv 预印本 · 2026-11-22 · v1 | 实证研究 | 研究如何构造可执行的网络权重。 |

### 能力写入与组合

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [WeightCode: Installing New Capabilities into Neural Networks via Weight-Space Programming](https://arxiv.org/abs/2611.25476) | arXiv 预印本 · 2026-11-19 | 方法 | 合成可复用的程序写入新计算，并测试原能力保留和连续写入。复用实验在同架构、独立训练的 ViT-Lite 上重新运行程序。 [代码](https://github.com/Gen-Verse/WeightCode) |
| [Weight-Space Programming Writes In-Context Learning and Matches Fine-Tuning in Language Models](https://arxiv.org/abs/2611.26841v2) | arXiv 预印本 · 2026-11-19 · v2 | 实证研究 | 将上下文示例引起的激活差异写入权重。数据匹配与措辞变化实验进一步限定了与微调表现相近的条件。 [代码](https://github.com/y3nk0/weight-space-programming-study) |
| [Weights & Caches: LLMs Can Program Tabular Foundation Models](https://arxiv.org/abs/2611.20174) | arXiv 预印本 · 2026-11-15 | 实证研究 | 编写小型表格基础模型并修复预训练检查点。另有一组实验只编辑 KV 缓存。 |

### 自编辑与迭代反馈

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [Language Models Can Rewrite Their Own Weights](https://arxiv.org/abs/2611.21885v2) | arXiv 预印本 · 2026-11-16 · v2 | 实证研究 | 让 270 亿参数模型利用带评分的样例和前向反馈编辑自身检查点，并测试重复编辑与损坏恢复。 |
| [Self-WSP: Can Language Models Improve Themselves Through Weight-Space Programming?](https://arxiv.org/abs/2611.28833) | arXiv 预印本 · 2026-11-21 | 实证研究 | 用同一个 8 亿参数模型编辑与求解，通过练习题筛选修改。在张量目录乱序且预算匹配的对照中，随机搜索在 GSM8K 上表现相近，在 MATH500 上落后。 |
| [Self-Upgrading Embodied Agents](https://arxiv.org/abs/2611.31117) | arXiv 预印本 · 2026-11-23 | 实证研究 | 在家庭环境模拟器中测试跨任务自编辑。所测四种模型规模中，270 亿参数版本保留了一次成功编辑。 |

## 评测基准

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [WeightBench: Evaluating Language Models as Weight-Space Programmers](https://arxiv.org/abs/2611.18553) | arXiv 预印本 · 2026-11-13 | 基准 | 五个评测轨道共登记 42 项任务，包括判断编辑是否可行以及满足系统资源约束。论文中有 39 项在默认难度下通过有效性门槛。 [代码与排行榜](https://github.com/Aayush-Marasini/WeightBench) |
| [IWIBench: Evaluating Gradient-Free Model Driven Intra-weight Injection](https://arxiv.org/abs/2611.08647) | arXiv 预印本 · 2026-11-05 | 基准 | 在固定的 Gemma 3 4B IT 检查点上测试无梯度编辑。评分结合归一化目标增益与原模型答对的对照项保留率。 [项目页](https://hcltech-robotics.github.io/iwibench/) · [代码](https://github.com/HCLTech-robotics/iwibench) |
| [TrojanMaxxing: One-shotting VLM Backdoors with Weight-Space Programming](https://arxiv.org/abs/2611.27425v1) | arXiv 预印本 · 2026-11-20 · v1 | 基准 | 提出或研究用于评估权重空间编程的任务。 |

WeightBench 按任务设定参数访问和反馈权限，参考解的权限也随任务而变。IWIBench 在单一目标检查点上衡量目标增益及指定对照项的保留率。比较分数前可查阅[基准复核](docs/research-review.md#基准复核)。

## 复现与对照实验

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [Exploring Weight-Space Programming: Capabilities, Generalization, and Limitations](https://arxiv.org/abs/2611.09382) | arXiv 预印本 · 2026-11-06 | 实证研究 | 用开发集和留出集对多条编辑轨迹评分，记录验证通过的收益和最终保留原检查点的情况。 [项目页](https://wsp-scope.github.io/) |
| [Can an LLM Actually Reason and Program about Neural Network's Weights or is it just memorization on steroids? Exploring "Weight-Space Programming"](https://arxiv.org/abs/2611.08070) | arXiv 预印本 · 2026-11-05 | 实证研究 | 区分可处理的局部权重计算与依赖熟悉数据集先验的语义诊断。 |
| [Replicating and Extending Weight-Space Programming: Frontier LLMs Compile Programs into Weights and Read Input Layers](https://arxiv.org/abs/2611.21449) | arXiv 预印本 · 2026-11-16 | 实证研究 | 在 Breakout 及其修改版上复现策略编写，并用新设计的游戏检验权重读取能否识别输入布局与游戏规则。 |
| [Same Fix, Different Weights: Replicating Weight-Space Programming with Claude](https://arxiv.org/abs/2611.20953) | arXiv 预印本 · 2026-11-16 | 实证研究 | 采用置换和未训练网络作为对照，并用不同的编辑机制复现抑制循环的效果。 [代码](https://github.com/Cenrax/weight-space-programming-claude) |
| [Computation, not weight access: large language models as auditors of clinical prediction networks](https://arxiv.org/abs/2611.07847v2) | arXiv 预印本 · 2026-11-05 · v2 | 实证研究 | 在合成临床网络上分别测试纯文本、白盒和黑盒审计，并加入脚本对照。 |
| [Just sort it! A note on the LP behind rank-one anti-loop edits](https://arxiv.org/abs/2611.21432) | arXiv 预印本 · 2026-11-16 | 分析 | 为方向固定的秩一抗循环更新中的优化子问题提供简单的排序基线。 |
| [Can a Linear Program Do Weight-Space Programming?](https://nathan.rs/posts/weight-space-lp/) | 作者报告 · 2026-11-09 | 实证研究 | 用线性规划作为 Qwen 抗循环权重编辑的直接对照。 |
| [Weight Space Programming for Vision Language Model Repair](https://arxiv.org/abs/2611.23615v2) | arXiv 预印本 · 2026-11-17 · v2 | 实证研究 | 低位数值痕迹有助于识别人为植入的视觉语言模型故障。在该实验中，对权重舍入后，大部分无辅助修复效果消失。 |
| [Writing Weights or Training Them? Spatial Reasoning through Weight-Space Programming and Low-Rank Adaptation](https://arxiv.org/abs/2611.27089) | arXiv 预印本 · 2026-11-20 | 实证研究 | 区分恢复答题完成能力与针对空间推理任务的专门适配，并测量对相近任务的干扰。 |
| [Can Large Language Models Optimize Pretrained Neural Network Weights? A Multi-Phase Empirical Evaluation of Gradient-Free Editing in YOLO26 Object Detection](https://arxiv.org/abs/2611.17789) | arXiv 预印本 · 2026-11-13 | 实证研究 | 将目标检测模型的直接编辑与预算匹配的随机搜索比较，未发现大语言模型引导的明确优势。 |
| [Where Does a Weight-Editing Agent Help? Blind Diagnosis and Repair of Deployment Faults in Vision Models](https://arxiv.org/abs/2611.28781) | arXiv 预印本 · 2026-11-21 | 实证研究 | 将盲测的视觉模型修复智能体与针对特定故障的脚本比较，并检验智能体在脚本库未覆盖故障上的诊断优势。 |
| [Can an LLM Repair a Language Model in Weight Space Without Gradient Training?](https://arxiv.org/abs/2611.25613v2) | arXiv 预印本 · 2026-11-19 · v2 | 实证研究 | 利用固定投影与预算匹配的黑盒搜索，检验自适应选择编辑方法能为人为植入的 Transformer 故障带来多少修复收益。 |
| [Weight-Space Programming Changes How an LLM Uses Python for Computational Biology](https://arxiv.org/abs/2611.20566) | arXiv 预印本 · 2026-11-16 | 实证研究 | 考察小型语言模型编辑后使用 Python 工具的变化，区分计算纠正与答案完成率提高。 |
| [Can LLMs Write Backdoors? An Empirical Security Study of Weight-Space Programming](https://arxiv.org/abs/2611.17395) | arXiv 预印本 · 2026-11-12 | 实证研究 | 研究 WSP 实验中的检查点完整性，为行为保留测试与来源核查提供参考。 |
| [What Did Astra’s Edit Actually Do?](https://xxlya.github.io/editlens/) | 研究报告 · 2026-11 | 实证研究 | 通过行为测试与机制分析审计公开发布的抗循环补丁。 |
| [Rethinking Weight-Space Programming: Re-running the experiments with baselines and controls](https://zhangyiqun018.github.io/rethinking-weight-space-programming/) | 复现报告 · 2026-11 | 实证研究 | 为选定的读取和写入实验补充基线与对照后重新运行。 [代码](https://github.com/ZhangYiqun018/rethinking-weight-space-programming) |
| [Re-running “Sparks of Weight-Space Programming”](https://github.com/shapor/weight-space-experiments) | 复现仓库 · 2026-11 | 实证研究 | 增加盲测读取实验和独立评分，并为 Qwen 补丁加入非思考模式对照。 |
| [The Weight-Space Programming Illusion: Gradient-Free Weight Edits Did Not Beat Random Noise on Filipino](https://huggingface.co/blog/Neurips-2026-MLIntern-Repro/the-weight-space-programming-illusion-gradient-fre) | 社区报告 · 2026-11-22 | 实证研究 | 在 FilBench 的 Global MMLU Tagalog 子集上，对三个小型模型进行的定向编辑均未优于结构和幅度匹配的随机扰动。 |
| [Can an LLM Program the Weights of a Lewam - Robot Policy?](https://huggingface.co/blog/herooooooooo/can-an-llm-program-the-weights-of-a-lewam-robot-po) | 社区报告 · 2026-11-17 | 实证研究 | 在 300 个仿真留出起点上评估 LeWAM 编辑，未发现相对于原策略有明确的成功率增益。 |

## 工具与运行时

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [W-ISA: Transactional Execution of Weight-Space Intervention Programs](https://arxiv.org/abs/2611.13232) | arXiv 预印本 · 2026-11-09 | 系统与工具 | 定义带类型约束的权重干预，支持事务式执行、恢复和重放。 [代码](https://github.com/eax/w-isa) |
| [NCP: Verifier-Guided Optimization of Weight-Space Control Policies](https://arxiv.org/abs/2611.13236) | arXiv 预印本 · 2026-11-09 | 系统与工具 | 为事务式干预增加运行监测与准入规则，并报告一项所有候选干预均未通过准入的实验。 |
| [OpenWSP](https://github.com/openwsp/openwsp) | 软件项目 | 系统与工具 | 提供检查点查看、编辑和版本管理工具，并公开独立重跑 Sparks Qwen 编辑实验的结果。 [复现结果](https://github.com/openwsp/openwsp/blob/main/replications/exp8/results/live-runs/codex-20261103/math500/summary.json) |
| [weightspace](https://github.com/leofmarciano/weightspace) | 软件项目 | 系统与工具 | 提供 Python 接口，支持由智能体读取、修复和写入目标模型权重。 |
| [WSP-Gym](https://github.com/emeraldant/WSP-Gym) | 软件项目 | 系统与工具 | 提供用于测试权重空间操作的小型合成任务。 |
| [WSPBench](https://www.wspbench.com/) | 公开测试版基准 | 基准 | 区分不同的访问条件，并公开六项无工具读取与写入任务的开发集对照结果。 |
| [SafeTensors](https://github.com/safetensors/safetensors) | 文件格式 | 系统与工具 | 提供用于分发模型检查点与参数补丁的张量序列化格式。 |

## 基础与相关工作

这些工作涵盖程序编译、权重分析和实验基线，也帮助区分权重产物背后的训练与参数拟合。

### 程序到权重的编译

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [Thinking Like Transformers](https://proceedings.mlr.press/v139/weiss21a.html) | ICML 2021 | 方法 | 提出 RASP，用注意力和前馈运算的基本组件表达序列计算。 |
| [Tracr: Compiled Transformers as a Laboratory for Interpretability](https://papers.nips.cc/paper_files/paper/2023/hash/771155abaae744e08576f1f3b4b7ac0d-Abstract-Conference.html) | NeurIPS 2023 | 系统与工具 | 将 RASP 程序编译为仅含解码器的 Transformer 权重，所得电路结构已知。 [代码](https://github.com/google-deepmind/tracr) |
| [ALTA: Compiler-Based Analysis of Transformers](https://arxiv.org/abs/2410.18077v2) | TMLR 2025 · arXiv v2 | 系统与工具 | 将循环程序编译为 Universal Transformer 的权重。 [代码](https://github.com/google-deepmind/alta) |
| [Tracr-Injection: Distilling Algorithms into Pre-trained Language Models](https://aclanthology.org/2025.findings-acl.146/) | Findings of ACL 2025 | 方法 | 通过蒸馏输出和中间执行轨迹，将编译后的算法迁移到预训练模型。 |
| [Neural Decompiling of Tracr Transformers](https://link.springer.com/chapter/10.1007/978-3-031-71602-7_3) | ANNPR 研讨会论文集 2024 | 方法与基准 | 从合成的程序与权重配对数据中学习重建 RASP 程序。 [arXiv](https://arxiv.org/abs/2410.00061) |
| [Learning to Compile Programs to Neural Networks](https://proceedings.mlr.press/v235/weber24b.html) | ICML 2024 | 方法 | 训练编译器将程序文本转换为神经代理模型的权重，使模型生成与执行分离。 [arXiv](https://arxiv.org/abs/2407.15078) |
| [Attention is Turing-Complete](https://jmlr.org/papers/v22/20-302.html) | JMLR 2021 | 理论与证明 | 在给定形式化假设下，构造能够模拟图灵机的硬注意力权重。 |
| [Compiling to Linear Neurons](https://popl26.sigplan.org/details/POPL-2026-popl-research-papers/37/Compiling-to-Linear-Neurons) | POPL 2026 | 理论与证明 | 将离散条件分支编译为可微的线性神经元，并给出正确性保证。 |
| [Compiling to Recurrent Neurons](https://pldi26.sigplan.org/details/pldi-2026-papers/102/Compiling-to-Recurrent-Neurons) | PLDI 2026 | 理论与证明 | 用循环神经元将编译方法扩展到迭代程序。 |
| [Linear Transformers Are Secretly Fast Weight Programmers](https://proceedings.mlr.press/v139/schlag21a.html) | ICML 2021 | 理论与证明 | 建立线性注意力与网络内部动态写入的快权重记忆之间的联系。 |
| [A CPU Inside an LLM: Zero-Gradient Compilation of Exact Circuits into Pretrained Weights](https://arxiv.org/abs/2611.26450) | arXiv 预印本 · 2026-11-19 | 方法 | 用专门设计的解析编译器将算术和布尔电路嵌入预训练语言模型，并说明架构与数值条件。 |
| [Looped Transformers as Programmable Computers](https://proceedings.mlr.press/v202/giannou23a.html) | ICML 2023 | 理论与证明 | 构造能执行迭代程序的常数深度循环 Transformer。 |
| [Knowledge-based artificial neural networks](https://www.sciencedirect.com/science/article/abs/pii/0004370294901058) | Artificial Intelligence 1994 | 方法 | 将领域规则转换为神经网络，再用样例进一步调整模型。 |
| [Adaptive Neural Compilation](https://papers.nips.cc/paper_files/paper/2016/hash/f0adc8838f4bdedde4ec2cfad0515589-Abstract.html) | NeurIPS 2016 | 方法 | 将低级程序编译为可微表示，并针对目标输入分布优化程序。 [arXiv v2](https://arxiv.org/abs/1605.07969v2) |

### 权重读取与可解释性

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html) | 作者报告 2021 | 分析 | 通过组合 QK 和 OV 权重分析纯注意力 Transformer 的计算电路。 |
| [Classifying the classifier: dissecting the weight space of neural networks](https://arxiv.org/abs/2002.05688) | ECAI 2020 | 方法 | 训练基于权重的探针来推断训练设置，并发布 Neural Weight Space 权重快照数据集。 [论文集 DOI](https://doi.org/10.3233/FAIA200209) |
| [Predicting Neural Network Accuracy from Weights](https://arxiv.org/abs/2002.11448v4) | arXiv 预印本 · 2020 · v4 | 方法 | 用训练得到的预测器从权重统计量估计网络性能。 |
| [Equivariant Architectures for Learning in Deep Weight Spaces](https://proceedings.mlr.press/v202/navon23a.html) | ICML 2023 | 方法 | 用对隐藏神经元置换等变的网络层处理多层感知机参数。 |
| [Permutation Equivariant Neural Functionals](https://proceedings.neurips.cc/paper_files/paper/2023/hash/4e9d8aeeab6120c3c83ccf95d4c211d3-Abstract-Conference.html) | NeurIPS 2023 | 方法 | 构造作用于网络权重的置换等变映射。 |
| [Graph Neural Networks for Learning Equivariant Representations of Neural Networks](https://proceedings.iclr.cc/paper_files/paper/2024/hash/c592fc7e6207f82560ed45fece8d6937-Abstract-Conference.html) | ICLR 2024 | 方法 | 把神经网络参数表示成图，使所得表示能够反映权重的对称性。 |
| [Interpreting the Weight Space of Customized Diffusion Models](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f85364507054c257959c2011c28bfc0d-Abstract-Conference.html) | NeurIPS 2024 | 方法与基准 | 分析个性化扩散模型的权重增量，并发布权重数据集。 [代码](https://github.com/snap-research/weights2weights) |
| [Weight Oracles: Reading Neural Network Weights with Language Models](https://arxiv.org/abs/2610.07334) | arXiv 预印本 · 2026-10-05 · NeuralArtifacts 研讨会 Spotlight 录用 | 方法与基准 | 训练以权重为条件的语言模型，回答关于小型网络的问题，为通用智能体提供训练式对照。 |
| [Auto Weight-Space Programming (Part 1): Defining the Problem and Initial Experiments](https://atharva-naik.github.io/blog/awsp-part-1/) | 作者报告 · 2026-11 | 实证研究 | 在小规模行为选择任务上研究经过训练的模型如何读取自身权重，为参数访问条件下的权重读取提供证据。 [代码](https://github.com/atharva-naik/auto-weight-space-programming) |
| [Interpretability in Parameter Space: Minimizing Mechanistic Description Length with Attribution-based Parameter Decomposition](https://arxiv.org/abs/2501.14926v4) | arXiv 预印本 · 2025 · v4 | 方法 | 学习将参数分解为多个组件，以恢复受控网络中的计算机制。 |
| [Targeted Recovery of Weight-Space Mechanisms From Neural Networks](https://arxiv.org/abs/2607.13047) | ICML 机制可解释性研讨会 2026 | 方法 | 学习在指定输入上保留原计算的参数组件，并用一个兜底组件处理其余输入。 |
| [Learning Trajectories Leave Decodable Traces in Neural Network Weight Space and Internal Representations](https://arxiv.org/abs/2611.24782v2) | arXiv 预印本 · 2026-11-18 · v2 | 实证研究 | 测试从训练后的网络辨认初始化与任务顺序，区分解码部分训练历史与重建完整轨迹。 |

### 行为探针对照

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [Deep Linear Probe Generators for Weight Space Learning](https://proceedings.iclr.cc/paper_files/paper/2025/hash/2aab8a76c7e761b66eccaca0927787de-Abstract-Conference.html) | ICLR 2025 | 方法 | 用共享的深度线性生成器学习输入探针，再根据目标模型的前向响应预测其属性。 |
| [Can this Model Also Recognize Dogs? Zero-Shot Model Search from Weights](https://arxiv.org/abs/2502.09619) | ICLR 权重空间学习研讨会 2025 | 方法 | 根据固定探针输入的 logit 响应，按能力检索分类器。 [研讨会论文列表](https://weight-space-learning.github.io/papers) |

### 相关模型编辑方法

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [HypoLoop: Revising Weight-Editing Plans from Scientific Feedback](https://arxiv.org/abs/2611.23718) | arXiv 预印本 · 2026-11-18 | 方法 | 根据连续收到的实验反馈修订科学模型的编辑方案，由数值求解器计算参数更新，部分变体使用梯度。 |
| [WeightLoop: Weight-Space Programming with Experimental Feedback](https://arxiv.org/abs/2611.07319v2) | arXiv 预印本 · 2026-11-05 · v2 | 方法 | 由智能体编写更新程序，再用正则化最小二乘或 L-BFGS 根据实验反馈拟合修正量并保存通过验证的编辑。 |
| [What Does Weight-Space Programming Add to Diffusion Editing? Program Construction versus Score-Guided Refinement](https://arxiv.org/abs/2611.22228) | arXiv 预印本 · 2026-11-17 | 实证研究 | 区分智能体编写扩散模型编辑程序与数值拟合系数两个阶段。预注册的重写流程未优于强基线。 |
| [Tree-Ising: Repairing Language Models with Bit-Level Ising Edits](https://arxiv.org/abs/2611.14210) | arXiv 预印本 · 2026-11-10 | 方法 | 通过离散权重编辑修复语言模型行为，为智能体方法提供算法对照。 |
| [SWEET: Mitigating Spurious Feature Reliance in LLM Reasoning via Weight Editing](https://arxiv.org/abs/2611.10974) | arXiv 预印本 · 2026-11-07 | 方法 | 用反事实激活定位推理依赖的伪相关特征，再按预先定义的算法编辑权重。 |
| [Reparameterizing Your Object Detectors for Weight Space Programming](https://arxiv.org/abs/2611.29882) | arXiv 预印本 · 2026-11-23 | 方法 | 离线阶段用大语言模型智能体诊断结构并构造算子，后续重参数化和数值校准按确定性流程执行，无需调用大语言模型。 |
| [Can AI Mature a Model's Geometry? Training-Free Weight Baking in LLMs](https://arxiv.org/abs/2611.21310) | arXiv 预印本 · 2026-11-16 | 方法 | 分析模型根据从权重导出的摘要提出几何变换，随后用岭回归写入参数更新。 |
| [Can Weight-Space Programming Alter Learned Ethical Priorities?](https://arxiv.org/abs/2611.24330) | arXiv 预印本 · 2026-11-18 | 实证研究 | 在合成权衡任务上，按预先指定的架构规则编辑概念监督模型已拟合的读出权重，并检查事实准确率与相近行为是否保留。 |

### 模型编辑验证与修复

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [Locating and Editing Factual Associations in GPT](https://proceedings.neurips.cc/paper_files/paper/2022/hash/6f1d43d5a82a37e89b0665b33bf3a182-Abstract-Conference.html) | NeurIPS 2022 | 方法与基准 | 通过因果追踪确定事实编辑的秩一更新，并推出 CounterFact 基准。 |
| [Mass-Editing Memory in a Transformer](https://arxiv.org/abs/2210.07229v2) | ICLR 2023 · arXiv v2 | 方法 | 将基于因果定位的事实编辑扩展到多个网络层和更大批次的事实关联。 |
| [AlphaEdit: Null-Space Constrained Knowledge Editing for Language Models](https://proceedings.iclr.cc/paper_files/paper/2025/hash/29c8c615b3187ee995029284702d3f43-Abstract-Conference.html) | ICLR 2025 | 方法 | 根据需要保留的知识表示确定零空间，并将编辑更新投影到其中。 |
| [Rebuilding ROME : Resolving Model Collapse during Sequential Model Editing](https://aclanthology.org/2024.emnlp-main.1210/) | EMNLP 2024 | 方法 | 研究连续事实编辑过程中的失效，并通过修改实现提高稳定性。 |
| [Provable Repair of Deep Neural Networks](https://pldi21.sigplan.org/details/pldi-2021-papers/39/Provable-Repair-of-Deep-Neural-Networks) | PLDI 2021 | 方法 | 求解满足输出规范的权重修正，并适用于论文所覆盖的网络结构。 |
| [NNrepair: Constraint-Based Repair of Neural Network Classifiers](https://link.springer.com/chapter/10.1007/978-3-030-81685-8_1) | CAV 2021 | 方法 | 用通过和未通过测试的输入定位可疑参数，再通过约束求解生成修复补丁。 |
| [Architecture-Preserving Provable Repair of Deep Neural Networks](https://pldi23.sigplan.org/details/pldi-2023-pldi/19/Architecture-Preserving-Provable-Repair-of-Deep-Neural-Networks) | PLDI 2023 | 方法 | 在保持目标架构的条件下求解权重更新，使模型满足定义在输入多面体上的行为规范。 [代码](https://github.com/95616ARG/APRNN) |
| [Pruning neural networks without any data by iteratively conserving synaptic flow](https://proceedings.neurips.cc/paper/2020/hash/46a4378f835dc8040c8057beb6a2da52-Abstract.html) | NeurIPS 2020 | 方法 | 提供无数据的初始化剪枝对照，其剪枝评分使用梯度。 |

### 权重组合与学习式生成

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [Editing Models with Task Arithmetic](https://arxiv.org/abs/2212.04089v3) | ICLR 2023 · arXiv v3 | 方法 | 对从微调检查点提取的权重增量执行加法与取负操作。 [代码](https://github.com/mlfoundations/task_vectors) |
| [Git Re-Basin: Merging Models modulo Permutation Symmetries](https://arxiv.org/abs/2209.04836v6) | ICLR 2023 · arXiv v6 | 方法 | 合并检查点之前，先对齐在置换下功能等价的神经单元。 |
| [TIES-Merging: Resolving Interference When Merging Models](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1644c9af28ab7916874f6fd6228a9bcf-Abstract-Conference.html) | NeurIPS 2023 | 方法 | 合并任务向量时处理符号冲突，并过滤幅度较小的变化。 |
| [Language Models are Super Mario: Absorbing Abilities from Homologous Models as a Free Lunch](https://proceedings.mlr.press/v235/yu24p.html) | ICML 2024 | 方法 | 先稀疏化并重新缩放微调增量，再合并同源模型。 |
| [HyperNetworks](https://research.google/pubs/hypernetworks-2/) | ICLR 2017 | 方法 | 训练一个网络来生成另一个网络的权重。 |
| [Drag-and-Drop LLMs: Zero-Shot Prompt-to-Weights](https://proceedings.neurips.cc/paper_files/paper/2025/hash/e15b6539e6d61aab5dee4593222ba40e-Abstract-Conference.html) | NeurIPS 2025 | 方法 | 用训练后的超网络根据任务提示生成适配权重。 |
| [LoRAGen: Structure-Aware Weight Space Learning for LoRA Generation](https://proceedings.iclr.cc/paper_files/paper/2026/hash/fc7c087b5e965075c8946b9ff57e3d64-Abstract-Conference.html) | ICLR 2026 | 方法 | 通过训练得到的潜空间扩散模型，按语言条件生成 LoRA 参数。 |
| [Program-as-Weights: A Programming Paradigm for Fuzzy Functions](https://arxiv.org/abs/2607.02512v2) | NeurIPS 2026 录用 · 最终稿 v2 | 方法与基准 | 在 FuzzyBench 上训练编译器，将模糊函数的规范转换为供冻结解释器使用的适配器。 |
| [NeuronGen: Neural Network Parameter Generation via Large Language Models](https://arxiv.org/abs/2505.12470v3) | arXiv 预印本 · 2025-05-18 · v3 | 方法 | 利用模型检查点监督与指令微调，训练语言模型输出目标网络参数。 |
| [Text-to-LoRA: Instant Transformer Adaption](https://proceedings.mlr.press/v267/charakorn25a.html) | ICML 2025 | 方法 | 训练超网络根据任务描述生成 LoRA 权重。 |
| [Doc-to-LoRA: Learning to Instantly Internalize Contexts](https://proceedings.mlr.press/v306/charakorn26a.html) | ICML 2026 | 方法 | 学习为固定的目标模型将上下文映射为 LoRA 适配器，可作为将上下文写入权重的训练式对照。 |
| [A Modern Self-Referential Weight Matrix That Learns to Modify Itself](https://proceedings.mlr.press/v162/irie22b.html) | ICML 2022 | 方法 | 学习目标网络内部快权重的运行时更新规则。 |
| [Towards Autoregressive Neural Network Parameter Generation](https://arxiv.org/abs/2611.25538) | arXiv 预印本 · 2026-11-19 | 方法 | 基于预训练权重张量训练分词器，并自回归地生成权重词元。 |
| [Instant Weight-Space Consolidation for Long-Term Memory in LLMs](https://arxiv.org/abs/2611.20759) | arXiv 预印本 · 2026-11-16 | 方法 | 在推理时用训练后的循环超网络将会话激活整合为持久适配器。 |

### 相关基准与模型库

| 研究或资源 | 发表或项目状态 | 类型 | 主要内容 |
| --- | --- | --- | --- |
| [TracrBench: Generating Interpretability Testbeds with Large Language Models](https://arxiv.org/abs/2409.13714) | ICML 机制可解释性研讨会 2024 | 基准 | 提供经编译得到且程序结构已知的测试模型，用于评价解释方法。 [研讨会论文列表](https://icml2024mi.pages.dev/posters) |
| [MQuAKE: Assessing Knowledge Editing in Language Models via Multi-Hop Questions](https://aclanthology.org/2023.emnlp-main.971/) | EMNLP 2023 | 基准 | 检验事实编辑是否传播到依赖该事实的多跳问题。 |
| [Evaluating the Ripple Effects of Knowledge Editing in Language Models](https://aclanthology.org/2024.tacl-1.16/) | TACL 2024 | 基准 | 测量知识编辑对关联事实产生的变化。 |
| [Model Zoos: A Dataset of Diverse Populations of Neural Network Models](https://proceedings.neurips.cc/paper_files/paper/2022/hash/f94d5edb5c01715d879693ddbfdc1b98-Abstract-Datasets_and_Benchmarks.html) | NeurIPS 数据集与基准赛道 2022 | 基准 | 提供成组的训练后模型检查点，用于权重层面的分析。 |
| [Implicit Zoo: A Large-Scale Dataset of Neural Implicit Functions for 2D Images and 3D Scenes](https://proceedings.neurips.cc/paper_files/paper/2024/hash/a1aa1edb47567545a4b037a95d658e6f-Abstract-Datasets_and_Benchmarks_Track.html) | NeurIPS 数据集与基准赛道 2024 | 基准 | 提供一组表示二维和三维信号的神经场参数。 |
| [AdderBoard](https://github.com/anadim/AdderBoard) | 基准项目 | 基准 | 用留出的加法题评测小型 Transformer，按手写权重与训练所得权重分别排名。 |

## 应用领域

| 领域 | 代表性工作 |
| --- | --- |
| 语言与推理 | [将 ICL 写入权重](https://arxiv.org/abs/2611.26841v2)、[空间推理](https://arxiv.org/abs/2611.27089)、[权重自改写](https://arxiv.org/abs/2611.21885v2) |
| 游戏与控制 | [未见游戏](https://arxiv.org/abs/2611.16981)、[策略模型检验](https://arxiv.org/abs/2611.11604)、[实地转向控制](https://arxiv.org/abs/2611.21958) |
| 机器人 | [词汇语义落地](https://arxiv.org/abs/2611.09376)、[指令蒸馏](https://arxiv.org/abs/2611.11894)、[具身智能体自编辑](https://arxiv.org/abs/2611.31117) |
| 视觉与多模态模型 | [视觉模型可编辑性](https://arxiv.org/abs/2611.26408)、[部署故障](https://arxiv.org/abs/2611.28781)、[视觉语言模型故障对照](https://arxiv.org/abs/2611.23615v2)、[扩散模型编辑](https://arxiv.org/abs/2611.22228) |
| 表格数据与优化 | [表格基础模型](https://arxiv.org/abs/2611.20174)、[直接给出参数数值](https://arxiv.org/abs/2611.19292v3)、[优化用评分模型](https://arxiv.org/abs/2611.09559) |
| 科学模型 | [脑编码](https://arxiv.org/abs/2611.18114)、[脑电与心电](https://arxiv.org/abs/2611.13758)、[粒子物理](https://arxiv.org/abs/2611.27079)、[偏微分方程](https://arxiv.org/abs/2611.12954)、[实验反馈](https://arxiv.org/abs/2611.07319v2) |
