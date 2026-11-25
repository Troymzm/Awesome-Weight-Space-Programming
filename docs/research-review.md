# WSP 文献检索与覆盖复核

检索范围以 **2026-11-25** 为截止日。中英文索引分别见 [中文 README](../README.zh-CN.md) 和 [英文 README](../README.md)。[BibTeX](../references.bib) 提供目录中的 arXiv 记录及两篇起点报告。研究结果来自链接中的论文或原始报告，本仓库核对引用和实验口径。

## 问题与纳入范围

本次调研关注四个问题。通用模型能从参数中读出哪些信息？它能修复已有能力还是写入新的计算？生成的修改能否持久、迁移或组合？什么样的评测能区分这些结果及其替代解释？

- **直接研究**纳入权重读取、修改、构造与验证，以及能够产出可执行权重程序的工作。纳入独立复现、可复核的负结果和带实验的作者报告。
- **相邻研究**收录编译、权重表示、约束修复、权重算术及条件生成方面的技术先例与对照。用前向响应检索模型的行为探针、专门训练的读取器和生成器，以及由数值求解器拟合更新的混合方法，均注明各自的输入和更新机制。
- **记录单位**为独立研究或资源。同一论文的版本、镜像和代码归入一个条目。arXiv 日期为首次提交日期，修订稿链接固定到核验版本。首次提交与公开公告采用不同的时间口径，靠近截止日的候选另核对公告。会议录用、研讨会、预印本、作者报告、复现仓库和工具分别标注。 [arXiv 公布日程](https://info.arxiv.org/help/availability.html)
- **来源**优先使用会议论文页、正式出版记录、arXiv、作者项目页和官方代码。综述和公开聚合目录用于找候选，论文描述回到一手来源。标题、链接和状态逐条核对。重点争议和基准另核对方法、实验或局限段落。普通条目根据摘要或作者项目说明进行索引。

## 检索过程

| 检索轮次 | 实际查询词或组合 | 筛选重点 |
| --- | --- | --- |
| 术语和入口 | `"weight-space programming"`，`"weight space programming" neural weights`，`"weight-space programming" site:arxiv.org/abs OR site:openreview.net` | 确定术语来源，定位早期论文及作者报告。 |
| 操作与变体 | `"LLM-written" "weights" site:arxiv.org`，`"weight programming" "write weights"`，`"self-WSP"`，`"weight space" gradient-free repair neural compilation` | 补入规则编译、读权重、修复、自编辑、能力写入及多种参数访问方式。 |
| 评测和复现 | `"WeightBench"`，`"IWIBench"`，`"weight-space programming" independent replication`，`weight-space programming blind diagnosis deployment fault` | 检查无反馈与有限反馈设置、保留指标、公开复现、匹配随机扰动及黑盒对照。 |
| 技术先例 | `Tracr Injection Neural Decompiling Cajal`，`predict neural network accuracy from weights`，`weight-space interpretability parameter decomposition`，`ROME MEMIT AlphaEdit sequential collapse`，`NNrepair APRNN SynFlow`，`Git Re-Basin TIES DARE hypernetwork` | 按关联纳入编译、表示、修复、合并和生成的代表工作。 |
| 日期与引文补漏 | `"weight-space programming" after:2026-11-21 before:2026-11-26`，`"weight-space programming" "November 24, 2026" OR "November 25, 2026"`，重点论文参考文献与公开目录的交叉筛选 | 查近期发表、术语异名、跨域应用与还未被论文索引的技术报告。 |

检索使用通用网页与学术论文索引，回到 arXiv、OpenReview、PMLR、NeurIPS、ACL Anthology、SIGPLAN、出版社及作者页核验。交叉检查了三份公开目录和近期主题索引，作为补漏入口。arXiv 网页的批量查询曾超时，使用站点限定检索和逐篇 arXiv 记录补查。 [组织方式参考](https://github.com/Zehong-Wang/Awesome-Weight-Space-Learning) · [公开目录一](https://github.com/mrtrunghieu1/awesome-weight-space-programming) · [公开目录二](https://github.com/SajjadPSavoji/awesome-weight-space-programming) · [公开目录三](https://github.com/Boom5426/Awesome-Weight-Space-Programming) · [近期主题索引](https://thelatestinai.com/topics/weight-space-programming)

## 证据与写作口径

| 研究问题 | 可以引用的结果 | 比较时应保留的条件 |
| --- | --- | --- |
| 权重读取是否提供了额外信息？ | 一些小模型的结构线索和局部计算可以被恢复，但对完整功能的推断会受数据集先验、输入层线索及参数化形式影响。模拟临床网络实验报告，在所测任务上，有计算工具的黑盒与白盒诊断表现相近。 | 匹配参数访问以外的信息量，加入架构元数据、未训练权重、隐藏单元重排、函数等价变换或固定输入的前向探针作为对照。 [视觉审计](https://arxiv.org/abs/2611.05798v2) · [输入层复现](https://arxiv.org/abs/2611.21449) · [黑盒与白盒](https://arxiv.org/abs/2611.07847v2) · [ProbeGen](https://proceedings.iclr.cc/paper_files/paper/2025/hash/2aab8a76c7e761b66eccaca0927787de-Abstract-Conference.html) |
| 规则编译与从少量观测学习有何差异？ | 明确的规则或算法可以写成小型策略或循环 Transformer 的权重。在未公开游戏的实验中，按相同规则编写的 Python 策略仍是强对照。 | 写清规则、架构、样例和模拟器的可见性。对已知规范用可执行程序作对照，对统计学习用样本量匹配的拟合方法作对照。 [未公开游戏实验](https://arxiv.org/abs/2611.16981) · [结构化数据](https://arxiv.org/abs/2611.19292v3) · [LoopedWSP](https://mbzuai-oryx.github.io/LoopedWSP/) |
| 编辑是在修复故障还是安装新能力？ | Qwen 抗循环研究和 Keel 测量了答案完成、推理长度或准确率等结果。视觉语言模型的部分植入故障留下了可用于定位的低位精度痕迹。WeightCode 还测试了新任务、已测原有能力的保留，以及在五个同架构、独立训练的 ViT-Lite 上重跑程序。 | 分别报告完成率和完成后的准确率。核对故障来源、参数精度与保留测试。WeightCode 的复用比较使用每个目标自己的带标签示例，证据适用于所测的同架构检查点。 [空间推理对照](https://arxiv.org/abs/2611.27089) · [Keel](https://arxiv.org/abs/2611.25257) · [精度控制](https://arxiv.org/abs/2611.23615v2) · [WeightCode](https://arxiv.org/html/2611.25476v1#S4.SS3) |
| 自修改和反馈循环能否稳定获益？ | Self-WSP 的乱序张量目录实验中，预算匹配的随机搜索在 GSM8K 上与自编辑表现相近，在 MATH500 上较弱。后续有序目录实验采用了不同的接口。具身模拟中，所测家族的四个规模中只有 27B 模型保留了成功编辑。 | 报告筛选规则、全部轨迹、空改动比例与前向预算。区分程序如何生成、修正量如何拟合与是否对目标模型反向传播。WeightLoop 拟合修正量时使用正则化最小二乘或 L-BFGS，HypoLoop 的部分对照还通过原生网络使用 Adam。 [Self-WSP](https://arxiv.org/html/2611.28833v1#S5) · [具身自编辑](https://arxiv.org/abs/2611.31117) · [WeightLoop](https://arxiv.org/html/2611.07319v2#S3) · [HypoLoop](https://arxiv.org/html/2611.23718v1#S3) |
| 自动化的增益来自哪里？ | 已知部署故障的修复中，专用脚本接近代理，代理在脚本未覆盖的故障上更有优势。检测编辑和 Global MMLU Tagalog 测试各自的匹配随机对照均未显示明确的 LLM 编辑优势。扩散编辑的预注册重写流程未超过强基线。 | 报告随机扰动匹配的结构、幅度与预算。区分程序生成、系数拟合、搜索与打分，并注明预注册及探索性指标。 [视觉故障](https://arxiv.org/abs/2611.28781) · [YOLO26](https://arxiv.org/abs/2611.17789) · [Filipino 对照](https://huggingface.co/blog/Neurips-2026-MLIntern-Repro/the-weight-space-programming-illusion-gradient-fre) · [扩散编辑](https://arxiv.org/abs/2611.22228) |

### 基准复核

| 资源 | 实验口径 | 引用限制 |
| --- | --- | --- |
| [WeightBench](https://arxiv.org/html/2611.18553v1#S3) | 五轨共登记 42 项任务，目标约为 2K–7B 参数。READ 轨禁止目标模型前向执行。默认难度下 39 项通过有效性门槛，42 项中有 21 项的参考解使用与智能体相同的权限。 | GPT-6.1-sol 的结果须与其他模型的共同 38 项比较。采样次数与部分运行环境有差异，无有效提交和待人工复核的隔离运行记为 0。旋转、置换与新种子用于缓解污染。 [有效性门槛与参考解](https://arxiv.org/html/2611.18553v1#S5.SS2) |
| [IWIBench](https://arxiv.org/html/2611.08647v1#S3) | 在同一个 Gemma 3 4B IT 目标上，10 种编辑器配置各评测同一批 30 个选定开发集 episode，覆盖 10 个任务族。按任务族等权汇总归一化目标增益与对照项保留率的乘积。 | 保留率的分母仅包含原始检查点答对的对照项。结果适用于所测检查点、任务和工具预算。 [评分细则](https://arxiv.org/html/2611.08647v1#S3.SS2) |
| [Vision WSP / ERT](https://arxiv.org/abs/2611.26408) | 研究按留出图像评价重新标注及纠错，记录编辑成功和模型性能副作用。 | 同时改变目标模型的训练方案。比较结果包含目标对编辑的准备程度，仓库只列可核实的项目页。 |
| [WSPBench](https://www.wspbench.com/) | 公开测试版区分纯权重、张量分析和限额行为探针。已公布的开发集对照包含 6 项无工具读取与写入任务和 18 次会话。 | 公开对照没有修复任务，也没有计划中的隐藏评测结果。 |

### 论文定位和优先对照

- 研究**普适的权重读取**时，专门训练的读取器和行为探针提供两类对照。可在函数等价的不同参数化上比较语义诊断，同时加入元数据与等预算黑盒基线。 [Weight Oracles](https://arxiv.org/abs/2610.07334) · [函数保持审计](https://arxiv.org/abs/2611.05798v2) · [黑盒对照](https://arxiv.org/abs/2611.07847v2)
- 研究**可移植的能力安装**时，WeightCode 已测试同架构跨检查点重算和顺序安装。Tracr 和 Program-as-Weights 提供不同的编译对照，Doc-to-LoRA 可对照上下文写入权重的训练式方案。进一步比较时可分别控制训练种子、架构、任务顺序与保留成本。 [WeightCode](https://arxiv.org/html/2611.25476v1#S4.SS3) · [Tracr](https://papers.nips.cc/paper_files/paper/2023/hash/771155abaae744e08576f1f3b4b7ac0d-Abstract-Conference.html) · [Program-as-Weights](https://arxiv.org/abs/2607.02512v2) · [Doc-to-LoRA](https://proceedings.mlr.press/v306/charakorn26a.html)
- 研究**自改进或多轮维护**时，应把持久参数修改、临时运行时干预和训练得到的更新规则当作三种条件。以每轮事先规定的保留约束、候选总数和新任务评估检验可持续性。 [Self-WSP](https://arxiv.org/abs/2611.28833) · [W-ISA](https://arxiv.org/abs/2611.13232) · [Fast weights](https://proceedings.mlr.press/v162/irie22b.html)

## 独立补漏与筛选记录

- **术语覆盖**补入了 10 月的 *Weight Oracles*、更早的规则编译和参数分解，以及 11 月下旬的公开候选。把含有 “weight programming” 但仅修改运行时状态或依赖专用生成器的论文收在相邻研究。
- **证据覆盖**补入了重跑、无收益、未通过验证、精度泄露、只恢复完成率等结果。对未来发布或作者正在开发的资源保留状态。
- **版本核对**使用了 [Function-Preserving Audits v2](https://arxiv.org/abs/2611.05798v2)、[游戏任务 v4](https://arxiv.org/abs/2611.09271v4)、[结构化数据 v3](https://arxiv.org/abs/2611.19292v3) 和 [ICL 写入 v2](https://arxiv.org/abs/2611.26841v2)。原始 Sparks 的 alphaXiv 条目归入作者报告。作者说明了 WSP 概念允许用梯度获取信息或实施修改，原报告实验对梯度另有限制。 [作者回应](https://rikiyat.github.io/blog/weight-space-programming/#response-to-comments)
- **候选排除**包括已撤回的 [Diffusion Super-Resolution](https://arxiv.org/abs/2611.18690)，只有技术猜想的 [Image-Restoration Conjectures](https://arxiv.org/abs/2611.04268)，以及超出截止日期的 [WSPNest 发布](https://atharva-naik.github.io/wspnest/)。传统合并、优化和超网络采用代表性筛选，以免大方向的常规论文淹没直接研究。

arXiv 11 月分类月表的末轮筛选补入了植入故障上的固定投影对照，以及从会话激活生成持久适配器的训练式对照。 [语言模型修复](https://arxiv.org/abs/2611.25613v2) · [参数记忆](https://arxiv.org/abs/2611.20759)

本索引覆盖截至截止日可查证的主要研究线索。数据库索引延迟、非正式材料的可发现性以及相邻方向的代表性筛选都会影响覆盖范围。

## 第二轮审计与修订

- **证据口径。** ProbeGen 和 ProbeLog 依赖目标模型的前向响应。WeightLoop 包含数值拟合步骤，检测器重参数化使用大语言模型做离线诊断与算子构造。重新核对了 WeightBench 的任务门槛、参考解权限、IWIBench 的保留率分母，以及 Self-WSP 的随机搜索比较。 [ProbeLog](https://arxiv.org/abs/2502.09619) · [检测器原文](https://arxiv.org/html/2611.29882v1) · [WeightBench](https://arxiv.org/html/2611.18553v1#S5.SS2)
- **出版与版本。** 对照了复核前 64 条 arXiv 记录的题名和 BibTeX 作者。将 Adaptive Neural Compilation 和 Neural Decompiling 补记到正式出版记录，区分 TracrBench、Weight Oracles 等的研讨会状态，固定了重要修订版本。部分出版社或 DOI 链接的读取受限，使用会议页、作者页或 arXiv 补核。 [NeurIPS 2016](https://papers.nips.cc/paper_files/paper/2016/hash/f0adc8838f4bdedde4ec2cfad0515589-Abstract.html) · [ANNPR 2024](https://link.springer.com/chapter/10.1007/978-3-031-71602-7_3) · [ICML 2024 研讨会](https://icml2024mi.pages.dev/posters)
- **检索补漏。** 在已有检索式上补查 `"rewriting its weights"` 等异名、arXiv 的 `cs.AI / cs.LG / cs.CL / cs.CV / cs.RO` 的 11 月分类列表分页，以及代表工作引文。增补了 Keel、工具使用与答案提交的分析、公开随机扰动对照和相关编译与生成先例。社区复现保留其报告或仓库身份。 [Keel](https://arxiv.org/abs/2611.25257) · [工具使用分析](https://arxiv.org/abs/2611.20566) · [AdderBoard](https://github.com/anadim/AdderBoard)
