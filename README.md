# Awesome-Weight-Space-Programming

English · [简体中文](README.zh-CN.md)

A curated research index for **weight-space programming (WSP)**. It covers work that reads neural-network weights, repairs a trained model, writes weights from a specification, or installs reusable computations through parameter edits.

**Coverage through 2026-11-25.** [Search and evidence review (中文)](docs/research-review.md) · [BibTeX](references.bib) · [Contributing](CONTRIBUTING.md)

## Scope

Direct WSP studies give a programmer access to model parameters and ask it to infer or implement a computation. Many use a general-purpose language model with tools. Others use explicitly specified weight programs. The catalog distinguishes literal tensor access, programmatic tensor access, and behavioral feedback. Gradient use is a separate property of the protocol. An edit can use no backpropagation while still fitting coefficients or selecting candidates with labeled feedback. [Sparks and its author response](https://rikiyat.github.io/blog/weight-space-programming/#response-to-comments)

The foundations include dedicated weight readers, behavioral probes, compilers, editors with numerical fitting, and trained weight generators. These studies provide precedents and experimental comparators. Publication status appears alongside contribution type. arXiv dates denote first submission.

## Contents

- [Start here](#start-here)
- [Direct WSP](#direct-wsp)
  - [Read and diagnose](#read-and-diagnose)
  - [Repair and adapt](#repair-and-adapt)
  - [Write and compile](#write-and-compile)
  - [Install and compose](#install-and-compose)
  - [Self-editing and iterative feedback](#self-editing-and-iterative-feedback)
- [Benchmarks](#benchmarks)
- [Replications and controls](#replications-and-controls)
- [Tools and runtimes](#tools-and-runtimes)
- [Foundations and adjacent work](#foundations-and-adjacent-work)
  - [Program-to-weight compilers](#program-to-weight-compilers)
  - [Weight-space reading and interpretability](#weight-space-reading-and-interpretability)
  - [Behavioral probing comparators](#behavioral-probing-comparators)
  - [Related model editing](#related-model-editing)
  - [Model editing, verification and repair](#model-editing-verification-and-repair)
  - [Weight composition and learned generation](#weight-composition-and-learned-generation)
  - [Related benchmarks and model zoos](#related-benchmarks-and-model-zoos)
- [Applications](#applications)

## Start here

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights](https://rikiyat.github.io/blog/weight-space-programming/) | Author report · 2026-11-02 | Empirical study | Introduces the contemporary term through eight read, repair and write experiments. Access to code and feedback varies by experiment. [Logs](https://github.com/RikiyaT/lm_understand-logs) |

- For systematic evaluation and failure cases, read WeightBench alongside the independent paper on rule compilation and input-layer cues. [WeightBench](https://arxiv.org/abs/2611.18553) · [Independent replication](https://arxiv.org/abs/2611.21449)
- For persistent capability installation, start with WeightCode and compare its experimental setting with prompt-derived edits in the ICL study. [WeightCode](https://arxiv.org/abs/2611.25476) · [ICL write-in](https://arxiv.org/abs/2611.26841v2)
- For the boundaries of the field, compare program-to-weight compilation with the survey taxonomy of weight-space learning. [Tracr](https://papers.nips.cc/paper_files/paper/2023/hash/771155abaae744e08576f1f3b4b7ac0d-Abstract-Conference.html) · [Weight-space learning survey](https://arxiv.org/abs/2603.10090)

## Direct WSP

### Read and diagnose

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [Function-Preserving Audits of Visual Weight Readers](https://arxiv.org/abs/2611.05798v2) | arXiv preprint · 2026-11-04 · v2 | Empirical study | Uses function-preserving neural-field transformations to test whether weight readers track the function or its parameterization. |
| [Weight-space programming for auditing clinical decision networks](https://arxiv.org/abs/2611.05341) | arXiv preprint · 2026-11-03 | Empirical study | Audits and repairs planted rule failures in small clinical decision networks, with limitations on clearing healthy networks. |
| [Weight-Space Reading](https://www.alphaxiv.org/abs/2611.weight-space-reading-language-models) | Author report · 2026-11 | Empirical study | Compares tensor access with descriptions of matched edits when predicting their effects. The report finds no conclusive self-reading advantage. [Code](https://github.com/suayptalha/wsr) |

### Repair and adapt

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [Can LLMs Debug Robots by Editing Their Weights?](https://arxiv.org/abs/2611.09376) | arXiv preprint · 2026-11-06 | Empirical study | Tests lexical grounding repairs in a robot policy using bounded simulator feedback. Other editing sessions largely fail to yield validated gains. |
| [Repairing Robot Policies with Weight Space Programming](https://jstranghoener.github.io/blog/robotic-weight-space-programming/) | Author report · 2026-11-11 | Empirical study | Tests repair of a simulated manipulation policy under distribution shift. Gains on held-out episodes with a fixed goal did not transfer to a held-out goal. |
| [Distilling Instructions into Weights: Closed-Form Edits Fix a Robot Policy's Misreading](https://arxiv.org/abs/2611.11894) | arXiv preprint · 2026-11-09 | Method + benchmark | Distills an effective instruction rephrasing into a robot policy with a closed-form edit and evaluates with paired held-out seeds. |
| [Mixed Signals: Weight-Space Programming for EEG and ECG](https://arxiv.org/abs/2611.13758) | arXiv preprint · 2026-11-10 | Empirical study | Tests direct construction and repair of small EEG and ECG classifiers under different data and feedback conditions. |
| [Training Vision Models for LLM-Driven Weight-Space Programming](https://arxiv.org/abs/2611.26408) | arXiv preprint · 2026-11-19 | Method + benchmark | Compares training recipes that prepare vision targets for later closed-form edits, measuring held-out efficacy and side effects. [Project](https://viscom.uni-ulm.de/wsp/) |
| [Keel: A Frontier Model Teaches a Vision-Language Model by Rewriting Its Weights](https://arxiv.org/abs/2611.25257) | arXiv preprint · 2026-11-18 | Method | Uses multimodal diagnostics and screened persistent edits to address reasoning loops in Qwen3.5-0.8B and 2B, measuring loop frequency, answer length and accuracy. |
| [Weight-space programming and mechanistic interpretability for model editing in particle physics](https://arxiv.org/abs/2611.27079) | arXiv preprint · 2026-11-20 | Empirical study | Compares agent edits with sparse-autoencoder-guided repair of a particle-physics jet classifier under a restricted query budget. |
| [Can a Frontier LLM Repair a Quantized Network by Tool-Free Weight-Space Programming?](https://arxiv.org/abs/2611.33031v1) | arXiv preprint · 2026-11-24 · v1 | Empirical study | Studies model repair or adaptation through parameter changes. |
| [Reading, Writing and Repairing Game-Theoretic Policies in Weight Space](https://arxiv.org/abs/2611.31979v1) | arXiv preprint · 2026-11-24 · v1 | Empirical study | Studies model repair or adaptation through parameter changes. |
| [Sparks of Weight-Space Programming for Robot Foundation Models](https://arxiv.org/abs/2611.31715v1) | arXiv preprint · 2026-11-24 · v1 | Empirical study | Studies model repair or adaptation through parameter changes. |
| [TowerBridge: Bridging the Dual-Encoder Modality Gap via Weight-Space Programming](https://arxiv.org/abs/2611.31233v1) | arXiv preprint · 2026-11-23 · v1 | Empirical study | Studies model repair or adaptation through parameter changes. |
| [Weight Coding: Evolving Web-Scale Recommenders through Direct Weight Edits with LLM Agents](https://arxiv.org/abs/2611.29613v1) | arXiv preprint · 2026-11-22 · v1 | Empirical study | Studies model repair or adaptation through parameter changes. |
| [Autonomous Parameter Surgery: How LLMs Implant Selective Backdoors into Language Models](https://arxiv.org/abs/2611.27920v1) | arXiv preprint · 2026-11-20 · v1 | Empirical study | Studies model repair or adaptation through parameter changes. |
| [Gradient-Free Few-Shot Adaptation of Vision Models via Agentic Coding](https://arxiv.org/abs/2611.28105v1) | arXiv preprint · 2026-11-17 · v1 | Empirical study | Studies model repair or adaptation through parameter changes. |

### Write and compile

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [Interpretable weight-space programming builds transparent transformers and brain encoding models](https://arxiv.org/abs/2611.18114) | arXiv preprint · 2026-11-13 | Method | Builds interpretable models with agent-authored parameters and analytic features, including language and brain encoding experiments. |
| [Compiling Known Rules into Compact Neural Agents: Weight-Space Programming on Unseen Games](https://arxiv.org/abs/2611.16981) | arXiv preprint · 2026-11-12 | Method + benchmark | Uses private game families to test rule-to-policy compilation with held-out levels and stronger Python-agent comparators. [Code](https://github.com/JensLehmann/weight-space-programming-games) |
| [Weight-Space Programming Doesn't Need Transformers](https://arxiv.org/abs/2611.22055) | arXiv preprint · 2026-11-17 | Empirical study | Compares fixed-target architecture with unrestricted design. Editors prefer sparse associative tables in the tested workloads. |
| [Zero-Shot Weight-Space Programming for Prediction and Classification of Target Variables in Structured Datasets](https://arxiv.org/abs/2611.19292v3) | arXiv preprint · 2026-11-14 · v3 | Empirical study | Asks an LLM to specify literal parameters from labeled tabular examples, with no execution before submission. |
| [Zero-Shot Weight-Space Programming Across a Difficulty-Graded Ladder of Two-Player Games](https://arxiv.org/abs/2611.09271v4) | arXiv preprint · 2026-11-06 · v4 | Empirical study | Evaluates direct weight writing for a ladder of two-player games with increasing strategic complexity. |
| [Can a Language Model Write the Weights? An Empirical Study of LLM-Written Scoring Networks for Column Generation and MILP Branching, with a Bus-Driver Scheduling Application](https://arxiv.org/abs/2611.09559) | arXiv preprint · 2026-11-06 | Empirical study | Evaluates LLM-written scoring networks for column generation and mixed-integer branching against solver and hand-designed baselines. |
| [Weight-Space Programming for Medical Imaging: Do We Still Need Training Data?](https://arxiv.org/abs/2611.12066) | arXiv preprint · 2026-11-09 | Empirical study | Constructs small medical image models without training data and compares against supervised models on MedMNIST. |
| [Physics2Weight: Direct Neural Network Architecture and Weight Generation from Physical Laws Using Large Language Models](https://arxiv.org/abs/2611.12954) | arXiv preprint · 2026-11-07 | Method | Uses PDE structure to generate a neural architecture and its weights. Nonlinear cases bound the scope of the demonstration. |
| [Weight-Space Programming of Variational Quantum Circuits: Large Language Models Write Quantum Circuit Parameters Without an Optimizer](https://arxiv.org/abs/2611.11537) | arXiv preprint · 2026-11-08 | Empirical study | Extends direct parameter writing to variational quantum circuits and evaluates across multiple quantum objectives. |
| [Weight-Space Programming of Policies and Their Verification via Model Checking](https://arxiv.org/abs/2611.11604) | arXiv preprint · 2026-11-08 | Method | Combines policy synthesis in weight space with model checking to assess formal reachability guarantees. |
| [Weight-space programming for tractor guidance controller: large language models natively write neural network weights that steer a real tractor](https://arxiv.org/abs/2611.21958) | arXiv preprint · 2026-11-16 | Empirical study | Programs a compact neural steering controller and evaluates it in simulation and a physical tractor experiment. |
| [Weight-Space Programming for Materials Science](https://arxiv.org/abs/2611.22013) | arXiv preprint · 2026-11-17 | Empirical study | Turns domain knowledge into weights for materials-property ranking without labeled training examples. |
| [Looped Weight-Space Programming: LLM-Written Transformers for Long Algorithmic Reasoning](https://mbzuai-oryx.github.io/LoopedWSP/) | Author report · 2026-11-23 | Empirical study | Programs looped Transformer weights for specified algorithms, including maze search, and compares with trained models and direct prompting. [Code](https://github.com/mbzuai-oryx/LoopedWSP) |
| [PAWP-TTS: Phoneme-Aware Weight Programming for Compact Bilingual English-Nepali Speech Synthesis](https://arxiv.org/abs/2611.29455v1) | arXiv preprint · 2026-11-22 · v1 | Empirical study | Studies the construction of executable network weights. |

### Install and compose

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [WeightCode: Installing New Capabilities into Neural Networks via Weight-Space Programming](https://arxiv.org/abs/2611.25476) | arXiv preprint · 2026-11-19 | Method | Synthesizes reusable programs that add computations and tests retention and sequential installation. Reuse experiments rerun programs on independently trained ViT-Lites of the same architecture. [Code](https://github.com/Gen-Verse/WeightCode) |
| [Weight-Space Programming Writes In-Context Learning and Matches Fine-Tuning in Language Models](https://arxiv.org/abs/2611.26841v2) | arXiv preprint · 2026-11-19 · v2 | Empirical study | Writes activation contrasts from in-context examples into weights. Matched-data comparisons and wording shifts qualify apparent parity with fine-tuning. [Code](https://github.com/y3nk0/weight-space-programming-study) |
| [Weights & Caches: LLMs Can Program Tabular Foundation Models](https://arxiv.org/abs/2611.20174) | arXiv preprint · 2026-11-15 | Empirical study | Programs a small tabular foundation model and repairs a pretrained checkpoint. A separate branch edits only the KV cache. |

### Self-editing and iterative feedback

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [Language Models Can Rewrite Their Own Weights](https://arxiv.org/abs/2611.21885v2) | arXiv preprint · 2026-11-16 · v2 | Empirical study | A 27B model edits its own checkpoint using graded examples and forward feedback, with tests of repeated edits and corruption recovery. |
| [Self-WSP: Can Language Models Improve Themselves Through Weight-Space Programming?](https://arxiv.org/abs/2611.28833) | arXiv preprint · 2026-11-21 | Empirical study | Uses the same 0.8B model as editor and solver, with edits selected on practice questions. Under a matched budget in the shuffled-interface comparison, random search is comparable on GSM8K and falls short on MATH500. |
| [Self-Upgrading Embodied Agents](https://arxiv.org/abs/2611.31117) | arXiv preprint · 2026-11-23 | Empirical study | Tests task-to-task self-editing in a household simulator. Of four sizes tested, the 27B model is the one that retains a successful edit. |

## Benchmarks

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [WeightBench: Evaluating Language Models as Weight-Space Programmers](https://arxiv.org/abs/2611.18553) | arXiv preprint · 2026-11-13 | Benchmark | Registers 42 tasks in five tracks, including infeasibility detection and systems constraints. In the paper, 39 meet the validity gate at default difficulty. [Code and leaderboard](https://github.com/Aayush-Marasini/WeightBench) |
| [IWIBench: Evaluating Gradient-Free Model Driven Intra-weight Injection](https://arxiv.org/abs/2611.08647) | arXiv preprint · 2026-11-05 | Benchmark | Tests gradient-free edits on a fixed Gemma 3 4B IT checkpoint. The score combines normalized target gain with retention on baseline-correct control items. [Project](https://hcltech-robotics.github.io/iwibench/) · [Code](https://github.com/HCLTech-robotics/iwibench) |
| [TrojanMaxxing: One-shotting VLM Backdoors with Weight-Space Programming](https://arxiv.org/abs/2611.27425v1) | arXiv preprint · 2026-11-20 · v1 | Benchmark | Proposes or studies evaluation tasks for weight-space programming. |

WeightBench varies access, feedback and reference-solution privileges by task. IWIBench reports target gains and retention on specified controls for one target checkpoint. See the [benchmark review](docs/research-review.md#基准复核) for comparison details.

## Replications and controls

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [Exploring Weight-Space Programming: Capabilities, Generalization, and Limitations](https://arxiv.org/abs/2611.09382) | arXiv preprint · 2026-11-06 | Empirical study | Studies multiple editing trajectories with development and held-out scoring, documenting both accepted gains and unchanged checkpoints. [Project](https://wsp-scope.github.io/) |
| [Can an LLM Actually Reason and Program about Neural Network's Weights or is it just memorization on steroids? Exploring "Weight-Space Programming"](https://arxiv.org/abs/2611.08070) | arXiv preprint · 2026-11-05 | Empirical study | Separates tractable local weight calculations from semantic diagnoses driven by familiar dataset priors. |
| [Replicating and Extending Weight-Space Programming: Frontier LLMs Compile Programs into Weights and Read Input Layers](https://arxiv.org/abs/2611.21449) | arXiv preprint · 2026-11-16 | Empirical study | Replicates policy writing on Breakout and modified variants, and uses newly designed games to test whether weight reading recovers input layout or game rules. |
| [Same Fix, Different Weights: Replicating Weight-Space Programming with Claude](https://arxiv.org/abs/2611.20953) | arXiv preprint · 2026-11-16 | Empirical study | Uses permutation and untrained-network controls and reproduces anti-loop behavior with a different edit mechanism. [Code](https://github.com/Cenrax/weight-space-programming-claude) |
| [Computation, not weight access: large language models as auditors of clinical prediction networks](https://arxiv.org/abs/2611.07847v2) | arXiv preprint · 2026-11-05 · v2 | Empirical study | Separates text-only, white-box and black-box auditing of synthetic clinical networks and includes scripted controls. |
| [Just sort it! A note on the LP behind rank-one anti-loop edits](https://arxiv.org/abs/2611.21432) | arXiv preprint · 2026-11-16 | Analysis | Provides a simple sorting baseline for the optimization subproblem of an anti-loop update with a fixed direction. |
| [Can a Linear Program Do Weight-Space Programming?](https://nathan.rs/posts/weight-space-lp/) | Author report · 2026-11-09 | Empirical study | Tests a linear program as a direct baseline for a Qwen anti-loop weight edit. |
| [Weight Space Programming for Vision Language Model Repair](https://arxiv.org/abs/2611.23615v2) | arXiv preprint · 2026-11-17 · v2 | Empirical study | Shows that low-bit artifacts help identify planted VLM faults. Rounding the weights removes most unaided recovery in the tested case. |
| [Writing Weights or Training Them? Spatial Reasoning through Weight-Space Programming and Low-Rank Adaptation](https://arxiv.org/abs/2611.27089) | arXiv preprint · 2026-11-20 | Empirical study | Distinguishes restoration of answer completion from targeted spatial adaptation and measures interference on nearby tasks. |
| [Can Large Language Models Optimize Pretrained Neural Network Weights? A Multi-Phase Empirical Evaluation of Gradient-Free Editing in YOLO26 Object Detection](https://arxiv.org/abs/2611.17789) | arXiv preprint · 2026-11-13 | Empirical study | Tests direct detection-model edits against budget-matched random search and finds no established advantage for LLM guidance. |
| [Where Does a Weight-Editing Agent Help? Blind Diagnosis and Repair of Deployment Faults in Vision Models](https://arxiv.org/abs/2611.28781) | arXiv preprint · 2026-11-21 | Empirical study | Compares a blind vision repair agent with fault-specific scripts and checks its diagnostic advantage on faults outside the script library. |
| [Can an LLM Repair a Language Model in Weight Space Without Gradient Training?](https://arxiv.org/abs/2611.25613v2) | arXiv preprint · 2026-11-19 · v2 | Empirical study | Uses fixed projections and matched-budget black-box search to test what adaptive edit selection adds on planted Transformer faults. |
| [Weight-Space Programming Changes How an LLM Uses Python for Computational Biology](https://arxiv.org/abs/2611.20566) | arXiv preprint · 2026-11-16 | Empirical study | Examines changes in Python tool use after editing a small language model and distinguishes corrected computations from improved answer completion. |
| [Can LLMs Write Backdoors? An Empirical Security Study of Weight-Space Programming](https://arxiv.org/abs/2611.17395) | arXiv preprint · 2026-11-12 | Empirical study | Studies checkpoint integrity in WSP experiments, with implications for behavior-preservation tests and provenance checks. |
| [What Did Astra’s Edit Actually Do?](https://xxlya.github.io/editlens/) | Research report · 2026-11 | Empirical study | Audits the public anti-loop patch using behavior and mechanistic analysis. |
| [Rethinking Weight-Space Programming: Re-running the experiments with baselines and controls](https://zhangyiqun018.github.io/rethinking-weight-space-programming/) | Reproduction report · 2026-11 | Empirical study | Reruns selected read and write experiments with added baselines and controls. [Code](https://github.com/ZhangYiqun018/rethinking-weight-space-programming) |
| [Re-running “Sparks of Weight-Space Programming”](https://github.com/shapor/weight-space-experiments) | Reproduction repository · 2026-11 | Empirical study | Adds blind reading runs, independent scoring and a non-thinking mode comparison for the Qwen patch. |
| [The Weight-Space Programming Illusion: Gradient-Free Weight Edits Did Not Beat Random Noise on Filipino](https://huggingface.co/blog/Neurips-2026-MLIntern-Repro/the-weight-space-programming-illusion-gradient-fre) | Community report · 2026-11-22 | Empirical study | On the Global MMLU Tagalog subset of FilBench, targeted edits across three small models did not beat perturbations matched for structure and magnitude. |
| [Can an LLM Program the Weights of a Lewam - Robot Policy?](https://huggingface.co/blog/herooooooooo/can-an-llm-program-the-weights-of-a-lewam-robot-po) | Community report · 2026-11-17 | Empirical study | Evaluates LeWAM edits on 300 fresh simulator starts and reports no established success gain over the unedited policy. |

## Tools and runtimes

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [W-ISA: Transactional Execution of Weight-Space Intervention Programs](https://arxiv.org/abs/2611.13232) | arXiv preprint · 2026-11-09 | System/tool | Defines typed weight interventions with transactional execution, restoration and replay. [Code](https://github.com/eax/w-isa) |
| [NCP: Verifier-Guided Optimization of Weight-Space Control Policies](https://arxiv.org/abs/2611.13236) | arXiv preprint · 2026-11-09 | System/tool | Adds telemetry and admission rules to transactional interventions, and reports an experiment in which all candidates were rejected. |
| [OpenWSP](https://github.com/openwsp/openwsp) | Software project | System/tool | Provides checkpoint inspection, editing and versioning utilities. The project publishes an independent rerun of the Sparks Qwen edit. [Replication results](https://github.com/openwsp/openwsp/blob/main/replications/exp8/results/live-runs/codex-20261103/math500/summary.json) |
| [weightspace](https://github.com/leofmarciano/weightspace) | Software project | System/tool | Provides Python interfaces for agent-driven reading, fixing and writing target weights. |
| [WSP-Gym](https://github.com/emeraldant/WSP-Gym) | Software project | System/tool | Provides small synthetic tasks for testing weight-space operations. |
| [WSPBench](https://www.wspbench.com/) | Public beta benchmark | Benchmark | Distinguishes access tiers and reports a development comparison on six no-tool reading and writing tasks. |
| [SafeTensors](https://github.com/safetensors/safetensors) | File format | System/tool | Provides tensor serialization for distributing checkpoints and parameter patches. |

## Foundations and adjacent work

These works provide ways to compile programs, analyze weights, construct baselines, and account for the training or fitting that precedes a weight artifact.

### Program-to-weight compilers

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [Thinking Like Transformers](https://proceedings.mlr.press/v139/weiss21a.html) | ICML 2021 | Method | Introduces RASP for expressing sequence computations in attention and feed-forward primitives. |
| [Tracr: Compiled Transformers as a Laboratory for Interpretability](https://papers.nips.cc/paper_files/paper/2023/hash/771155abaae744e08576f1f3b4b7ac0d-Abstract-Conference.html) | NeurIPS 2023 | System/tool | Compiles RASP programs into decoder-only weights with known circuits. [Code](https://github.com/google-deepmind/tracr) |
| [ALTA: Compiler-Based Analysis of Transformers](https://arxiv.org/abs/2410.18077v2) | TMLR 2025 · arXiv v2 | System/tool | Compiles looping programs into Universal Transformer weights. [Code](https://github.com/google-deepmind/alta) |
| [Tracr-Injection: Distilling Algorithms into Pre-trained Language Models](https://aclanthology.org/2025.findings-acl.146/) | Findings of ACL 2025 | Method | Transfers compiled algorithms into pretrained models by distilling outputs and internal traces. |
| [Neural Decompiling of Tracr Transformers](https://link.springer.com/chapter/10.1007/978-3-031-71602-7_3) | ANNPR Workshop 2024 proceedings | Method + benchmark | Learns to reconstruct RASP from synthetic program and weight pairs. [arXiv](https://arxiv.org/abs/2410.00061) |
| [Learning to Compile Programs to Neural Networks](https://proceedings.mlr.press/v235/weber24b.html) | ICML 2024 | Method | Trains a compiler that turns program text into neural surrogate weights, decoupling surrogate generation from execution. [arXiv](https://arxiv.org/abs/2407.15078) |
| [Attention is Turing-Complete](https://jmlr.org/papers/v22/20-302.html) | JMLR 2021 | Theory/proof | Constructs hard-attention weights that implement a Turing machine under formal assumptions. |
| [Compiling to Linear Neurons](https://popl26.sigplan.org/details/POPL-2026-popl-research-papers/37/Compiling-to-Linear-Neurons) | POPL 2026 | Theory/proof | Compiles discrete conditionals into differentiable linear neurons with correctness guarantees. |
| [Compiling to Recurrent Neurons](https://pldi26.sigplan.org/details/pldi-2026-papers/102/Compiling-to-Recurrent-Neurons) | PLDI 2026 | Theory/proof | Extends the compilation approach to iteration using recurrent neurons. |
| [Linear Transformers Are Secretly Fast Weight Programmers](https://proceedings.mlr.press/v139/schlag21a.html) | ICML 2021 | Theory/proof | Relates linear attention to dynamically written fast-weight memories inside a network. |
| [A CPU Inside an LLM: Zero-Gradient Compilation of Exact Circuits into Pretrained Weights](https://arxiv.org/abs/2611.26450) | arXiv preprint · 2026-11-19 | Method | Uses a purpose-built analytical compiler to graft arithmetic and Boolean circuits into pretrained LMs, with architecture and numerical requirements. |
| [Looped Transformers as Programmable Computers](https://proceedings.mlr.press/v202/giannou23a.html) | ICML 2023 | Theory/proof | Constructs constant-depth looped Transformers that execute iterative programs. |
| [Knowledge-based artificial neural networks](https://www.sciencedirect.com/science/article/abs/pii/0004370294901058) | Artificial Intelligence 1994 | Method | Translates domain rules into a network and refines the resulting model from examples. |
| [Adaptive Neural Compilation](https://papers.nips.cc/paper_files/paper/2016/hash/f0adc8838f4bdedde4ec2cfad0515589-Abstract.html) | NeurIPS 2016 | Method | Compiles a low-level program into a differentiable representation and optimizes it for a target input distribution. [arXiv v2](https://arxiv.org/abs/1605.07969v2) |

### Weight-space reading and interpretability

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html) | Author report 2021 | Analysis | Uses QK and OV weight compositions to analyze circuits in attention-only transformers. |
| [Classifying the classifier: dissecting the weight space of neural networks](https://arxiv.org/abs/2002.05688) | ECAI 2020 | Method | Trains weight-based probes to infer properties of the training setup and releases the Neural Weight Space snapshot dataset. [Proceedings DOI](https://doi.org/10.3233/FAIA200209) |
| [Predicting Neural Network Accuracy from Weights](https://arxiv.org/abs/2002.11448v4) | arXiv preprint · 2020 · v4 | Method | Uses trained predictors to estimate network performance from weight statistics. |
| [Equivariant Architectures for Learning in Deep Weight Spaces](https://proceedings.mlr.press/v202/navon23a.html) | ICML 2023 | Method | Processes MLP parameters with layers that respect hidden-neuron permutations. |
| [Permutation Equivariant Neural Functionals](https://proceedings.neurips.cc/paper_files/paper/2023/hash/4e9d8aeeab6120c3c83ccf95d4c211d3-Abstract-Conference.html) | NeurIPS 2023 | Method | Constructs permutation-equivariant mappings over network weights. |
| [Graph Neural Networks for Learning Equivariant Representations of Neural Networks](https://proceedings.iclr.cc/paper_files/paper/2024/hash/c592fc7e6207f82560ed45fece8d6937-Abstract-Conference.html) | ICLR 2024 | Method | Represents neural parameters as graphs so representations can respect weight symmetries. |
| [Interpreting the Weight Space of Customized Diffusion Models](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f85364507054c257959c2011c28bfc0d-Abstract-Conference.html) | NeurIPS 2024 | Method + benchmark | Analyzes personalized diffusion-model deltas and releases weight collections. [Code](https://github.com/snap-research/weights2weights) |
| [Weight Oracles: Reading Neural Network Weights with Language Models](https://arxiv.org/abs/2610.07334) | arXiv preprint · 2026-10-05 · NeuralArtifacts workshop spotlight acceptance | Method + benchmark | Trains weight-conditioned language models to answer questions about small networks, a learned comparator for general-purpose agents. |
| [Auto Weight-Space Programming (Part 1): Defining the Problem and Initial Experiments](https://atharva-naik.github.io/blog/awsp-part-1/) | Author report · 2026-11 | Empirical study | Studies trained self-reading on a small behavioral-choice task. This is supporting evidence for reading under weight access. [Code](https://github.com/atharva-naik/auto-weight-space-programming) |
| [Interpretability in Parameter Space: Minimizing Mechanistic Description Length with Attribution-based Parameter Decomposition](https://arxiv.org/abs/2501.14926v4) | arXiv preprint · 2025 · v4 | Method | Learns a decomposition into parameter components to recover mechanisms in controlled networks. |
| [Targeted Recovery of Weight-Space Mechanisms From Neural Networks](https://arxiv.org/abs/2607.13047) | ICML Mechanistic Interpretability Workshop 2026 | Method | Learns components that preserve computation on specified inputs while a catch-all component handles other inputs. |
| [Learning Trajectories Leave Decodable Traces in Neural Network Weight Space and Internal Representations](https://arxiv.org/abs/2611.24782v2) | arXiv preprint · 2026-11-18 · v2 | Empirical study | Tests identification of initialization and task order from trained networks. Results distinguish decoding aspects of training history from reconstructing the trajectory. |

### Behavioral probing comparators

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [Deep Linear Probe Generators for Weight Space Learning](https://proceedings.iclr.cc/paper_files/paper/2025/hash/2aab8a76c7e761b66eccaca0927787de-Abstract-Conference.html) | ICLR 2025 | Method | Learns input probes with a shared deep-linear generator and predicts model properties from the target's forward responses. |
| [Can this Model Also Recognize Dogs? Zero-Shot Model Search from Weights](https://arxiv.org/abs/2502.09619) | ICLR Weight Space Learning Workshop 2025 | Method | Retrieves classifiers by capability using logit responses to fixed probe inputs. [Workshop listing](https://weight-space-learning.github.io/papers) |

### Related model editing

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [HypoLoop: Revising Weight-Editing Plans from Scientific Feedback](https://arxiv.org/abs/2611.23718) | arXiv preprint · 2026-11-18 | Method | Revises scientific editing plans from sequential feedback. Numerical fitters compute the updates, with gradient-based variants included. |
| [WeightLoop: Weight-Space Programming with Experimental Feedback](https://arxiv.org/abs/2611.07319v2) | arXiv preprint · 2026-11-05 · v2 | Method | An agent specifies an update program. Regularized least squares or L-BFGS fits corrections from experimental feedback, and the validated edits are saved. |
| [What Does Weight-Space Programming Add to Diffusion Editing? Program Construction versus Score-Guided Refinement](https://arxiv.org/abs/2611.22228) | arXiv preprint · 2026-11-17 | Empirical study | Separates agent-authored diffusion edit programs from numerical coefficient fitting. Its preregistered rewrite pipeline shows no advantage over a strong comparator. |
| [Tree-Ising: Repairing Language Models with Bit-Level Ising Edits](https://arxiv.org/abs/2611.14210) | arXiv preprint · 2026-11-10 | Method | Uses discrete weight edits to repair language-model behavior and serves as a non-agent comparator. |
| [SWEET: Mitigating Spurious Feature Reliance in LLM Reasoning via Weight Editing](https://arxiv.org/abs/2611.10974) | arXiv preprint · 2026-11-07 | Method | Localizes spurious reasoning features using counterfactual activations and edits weights with a prescribed algorithm. |
| [Reparameterizing Your Object Detectors for Weight Space Programming](https://arxiv.org/abs/2611.29882) | arXiv preprint · 2026-11-23 | Method | Uses an LLM agent for offline structural diagnosis and operator synthesis. Deterministic reparameterization and numerical calibration then run without LLM calls. |
| [Can AI Mature a Model's Geometry? Training-Free Weight Baking in LLMs](https://arxiv.org/abs/2611.21310) | arXiv preprint · 2026-11-16 | Method | An analyst proposes a geometric transformation from weight-derived summaries. Ridge regression writes the parameter update. |
| [Can Weight-Space Programming Alter Learned Ethical Priorities?](https://arxiv.org/abs/2611.24330) | arXiv preprint · 2026-11-18 | Empirical study | Tests fixed, architecture-guided edits to the fitted readout of a concept-supervised model on a synthetic trade-off task and checks factual and behavioral preservation. |

### Model editing, verification and repair

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [Locating and Editing Factual Associations in GPT](https://proceedings.neurips.cc/paper_files/paper/2022/hash/6f1d43d5a82a37e89b0665b33bf3a182-Abstract-Conference.html) | NeurIPS 2022 | Method + benchmark | Uses causal tracing to motivate rank-one factual updates and introduces CounterFact. |
| [Mass-Editing Memory in a Transformer](https://arxiv.org/abs/2210.07229v2) | ICLR 2023 · arXiv v2 | Method | Extends causal factual editing across layers and larger batches of associations. |
| [AlphaEdit: Null-Space Constrained Knowledge Editing for Language Models](https://proceedings.iclr.cc/paper_files/paper/2025/hash/29c8c615b3187ee995029284702d3f43-Abstract-Conference.html) | ICLR 2025 | Method | Projects edits into a null space derived from representations of knowledge to retain. |
| [Rebuilding ROME : Resolving Model Collapse during Sequential Model Editing](https://aclanthology.org/2024.emnlp-main.1210/) | EMNLP 2024 | Method | Studies sequential factual editing failures and changes the implementation to improve stability. |
| [Provable Repair of Deep Neural Networks](https://pldi21.sigplan.org/details/pldi-2021-papers/39/Provable-Repair-of-Deep-Neural-Networks) | PLDI 2021 | Method | Solves for weight corrections that satisfy output specifications for supported networks. |
| [NNrepair: Constraint-Based Repair of Neural Network Classifiers](https://link.springer.com/chapter/10.1007/978-3-030-81685-8_1) | CAV 2021 | Method | Uses failing and passing inputs to localize suspect parameters and solve for a repair. |
| [Architecture-Preserving Provable Repair of Deep Neural Networks](https://pldi23.sigplan.org/details/pldi-2023-pldi/19/Architecture-Preserving-Provable-Repair-of-Deep-Neural-Networks) | PLDI 2023 | Method | Solves behavioral specifications over input polytopes while preserving the target architecture. [Code](https://github.com/95616ARG/APRNN) |
| [Pruning neural networks without any data by iteratively conserving synaptic flow](https://proceedings.neurips.cc/paper/2020/hash/46a4378f835dc8040c8057beb6a2da52-Abstract.html) | NeurIPS 2020 | Method | A data-free pruning-at-initialization comparator whose pruning scores use gradients. |

### Weight composition and learned generation

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [Editing Models with Task Arithmetic](https://arxiv.org/abs/2212.04089v3) | ICLR 2023 · arXiv v3 | Method | Adds and negates deltas derived from fine-tuned checkpoints. [Code](https://github.com/mlfoundations/task_vectors) |
| [Git Re-Basin: Merging Models modulo Permutation Symmetries](https://arxiv.org/abs/2209.04836v6) | ICLR 2023 · arXiv v6 | Method | Aligns permutation-equivalent units before combining checkpoints. |
| [TIES-Merging: Resolving Interference When Merging Models](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1644c9af28ab7916874f6fd6228a9bcf-Abstract-Conference.html) | NeurIPS 2023 | Method | Resolves sign conflicts and filters small changes in task deltas. |
| [Language Models are Super Mario: Absorbing Abilities from Homologous Models as a Free Lunch](https://proceedings.mlr.press/v235/yu24p.html) | ICML 2024 | Method | Sparsifies and rescales fine-tuning deltas before merging related models. |
| [HyperNetworks](https://research.google/pubs/hypernetworks-2/) | ICLR 2017 | Method | Uses a learned network to produce another network's weights. |
| [Drag-and-Drop LLMs: Zero-Shot Prompt-to-Weights](https://proceedings.neurips.cc/paper_files/paper/2025/hash/e15b6539e6d61aab5dee4593222ba40e-Abstract-Conference.html) | NeurIPS 2025 | Method | Uses a trained hypernetwork to generate task-conditioned adaptation weights. |
| [LoRAGen: Structure-Aware Weight Space Learning for LoRA Generation](https://proceedings.iclr.cc/paper_files/paper/2026/hash/fc7c087b5e965075c8946b9ff57e3d64-Abstract-Conference.html) | ICLR 2026 | Method | Generates language-conditioned LoRA parameters via a learned latent diffusion model. |
| [Program-as-Weights: A Programming Paradigm for Fuzzy Functions](https://arxiv.org/abs/2607.02512v2) | Accepted to NeurIPS 2026 · camera-ready v2 | Method + benchmark | Trains a compiler on FuzzyBench to translate fuzzy function specifications into adapters for a frozen interpreter. |
| [NeuronGen: Neural Network Parameter Generation via Large Language Models](https://arxiv.org/abs/2505.12470v3) | arXiv preprint · 2025-05-18 · v3 | Method | Uses checkpoint supervision and instruction tuning to train a language model to emit target-network parameters. |
| [Text-to-LoRA: Instant Transformer Adaption](https://proceedings.mlr.press/v267/charakorn25a.html) | ICML 2025 | Method | Trains a hypernetwork to generate LoRA weights from task descriptions. |
| [Doc-to-LoRA: Learning to Instantly Internalize Contexts](https://proceedings.mlr.press/v306/charakorn26a.html) | ICML 2026 | Method | Learns to map a context to a LoRA adapter for a fixed target model. It is a trained-generation comparator for writing context into weights. |
| [A Modern Self-Referential Weight Matrix That Learns to Modify Itself](https://proceedings.mlr.press/v162/irie22b.html) | ICML 2022 | Method | Learns a runtime update rule for fast weights within the target network. |
| [Towards Autoregressive Neural Network Parameter Generation](https://arxiv.org/abs/2611.25538) | arXiv preprint · 2026-11-19 | Method | Trains a tokenizer over pretrained weight tensors and generates weight tokens autoregressively. |
| [Instant Weight-Space Consolidation for Long-Term Memory in LLMs](https://arxiv.org/abs/2611.20759) | arXiv preprint · 2026-11-16 | Method | Uses a trained recurrent hypernetwork to consolidate conversation activations into a persistent adapter at inference time. |

### Related benchmarks and model zoos

| Work | Publication or project status | Type | Relevance |
| --- | --- | --- | --- |
| [TracrBench: Generating Interpretability Testbeds with Large Language Models](https://arxiv.org/abs/2409.13714) | ICML Mechanistic Interpretability Workshop 2024 | Benchmark | Provides compiled test models with known procedural structure for interpretation. [Workshop listing](https://icml2024mi.pages.dev/posters) |
| [MQuAKE: Assessing Knowledge Editing in Language Models via Multi-Hop Questions](https://aclanthology.org/2023.emnlp-main.971/) | EMNLP 2023 | Benchmark | Tests whether an edit propagates to multi-hop questions that depend on the revised fact. |
| [Evaluating the Ripple Effects of Knowledge Editing in Language Models](https://aclanthology.org/2024.tacl-1.16/) | TACL 2024 | Benchmark | Measures changes to related facts that follow from an edit. |
| [Model Zoos: A Dataset of Diverse Populations of Neural Network Models](https://proceedings.neurips.cc/paper_files/paper/2022/hash/f94d5edb5c01715d879693ddbfdc1b98-Abstract-Datasets_and_Benchmarks.html) | NeurIPS Datasets and Benchmarks 2022 | Benchmark | Provides trained checkpoint populations for weight-level analysis. |
| [Implicit Zoo: A Large-Scale Dataset of Neural Implicit Functions for 2D Images and 3D Scenes](https://proceedings.neurips.cc/paper_files/paper/2024/hash/a1aa1edb47567545a4b037a95d658e6f-Abstract-Datasets_and_Benchmarks_Track.html) | NeurIPS Datasets and Benchmarks 2024 | Benchmark | Provides neural-field parameter collections for 2D and 3D signals. |
| [AdderBoard](https://github.com/anadim/AdderBoard) | Benchmark project | Benchmark | Tracks hand-coded and trained small Transformers in separate divisions on held-out addition problems. |

## Applications

| Domain | Representative starting points |
| --- | --- |
| Language and reasoning | [ICL write-in](https://arxiv.org/abs/2611.26841v2), [spatial reasoning](https://arxiv.org/abs/2611.27089), [self-rewriting](https://arxiv.org/abs/2611.21885v2) |
| Games and control | [Unseen games](https://arxiv.org/abs/2611.16981), [model-checked policies](https://arxiv.org/abs/2611.11604), [field steering](https://arxiv.org/abs/2611.21958) |
| Robotics | [Lexical grounding](https://arxiv.org/abs/2611.09376), [instruction distillation](https://arxiv.org/abs/2611.11894), [embodied self-editing](https://arxiv.org/abs/2611.31117) |
| Vision and multimodal models | [Vision editability](https://arxiv.org/abs/2611.26408), [deployment faults](https://arxiv.org/abs/2611.28781), [VLM fault controls](https://arxiv.org/abs/2611.23615v2), [diffusion edits](https://arxiv.org/abs/2611.22228) |
| Tabular and optimization | [Tabular foundation models](https://arxiv.org/abs/2611.20174), [literal parameter generation](https://arxiv.org/abs/2611.19292v3), [optimization scorers](https://arxiv.org/abs/2611.09559) |
| Scientific models | [Brain encoding](https://arxiv.org/abs/2611.18114), [EEG and ECG](https://arxiv.org/abs/2611.13758), [particle physics](https://arxiv.org/abs/2611.27079), [PDEs](https://arxiv.org/abs/2611.12954), [experimental feedback](https://arxiv.org/abs/2611.07319v2) |
