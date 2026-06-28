# Mini-RAG v4 Retrieval Audit

Per-question retrieval inspection for the v4 run (hybrid + cross-encoder + contextual chunking).

Format per question:
- Question + metrics summary
- Gold info (the chunks marked + the gold answer)
- Top-5 retrieved (chunk_id + section + full text)

Chunk texts now include a contextual prefix:
```
Paper: <title>
Section: <section_heading>

<original chunk text>
```

---

## Q01: specific_fact_lookup

**Question**: What dataset is introduced by SARLO-80?

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=0.50 | AnsCorr=0.10

**Gold chunk_ids**: ['2606.20523::00017']

**Gold answer**:
> The dataset was built from open-access spotlight acquisitions collected by the Umbra satellite constellation and distributed as Sensor Independent Complex Data (SICD). They selected 2,565 SICD scenes covering all continents and diverse environments (urban, rural, coastal, mountainous), with VV or HH polarization, incidence angles ranging from 10° to 70°, and native resolutions from 20 cm to 2 m.

**Gold chunk text(s)**:
- **2606.20523::00017** _(section: 3.1 Source data: UMBRA Collections)_:
  > Paper: SARLO-80: Worldwide Slant SAR Language Optic Dataset 80cm
Section: 3.1 Source data: UMBRA Collections

We built our dataset from open-access spotlight acquisitions collected by the Umbra satellite constellation and distributed as Sensor Independent Complex Data (SICD). SICD products provide complex-valued SAR images (magnitude and phase) together with rich metadata (sampling spacings, scene center point, imaging geometry), which makes them well suited for reproducible preprocessing. We select 2,565 SICD scenes covering all continents and diverse environments (urban, rural, coastal, mountainous) as shown in Figure fig. 1a, with VV or HH polarization, incidence angles ranging from 10 ◦ to 70 ◦ , and native resolutions from 20 cm to 2 m.


**Top-5 retrieved**:

### [1] 2606.20470::00059
_section: 5.1 Jailbreak Prompts Dataset_

> Paper: Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems
Section: 5.1 Jailbreak Prompts Dataset

We evaluate our framework using a subset of 500 highrisk jailbreak prompts drawn from the AdvBench dataset introduced in [1]. These prompts represent a diverse set of illicit and harmful intent queries commonly used as seed prompts in red-teaming aligned language models. The dataset is publicly available 1 and has been adopted in several jailbreak benchmarks and attack evaluations, including PAIR, AutoDAN, and JailbreakBench [3], [6], [26].

### [2] 2606.20482::00062
_section: 7 Conclusion_

> Paper: Your Mouse and Eyes Secretly Leak Your Preference: LLM Alignment using Implicit Feedback from Users
Section: 7 Conclusion

We introduced IFLLM, a dataset pairing webcambased eye-gaze trajectories and mouse movements with explicit preference annotations. The dataset allows us to systematically measure the value of implicit feedback from users for the first time. The users exhibit complicated reading patterns, which are influenced by response length, interface layout, and individual style. Driven by the scrolling need for the long responses, users' mouse movement trajectories carry strong preference signal that text or even eye-gazing data cannot capture and drastically improve the accuracy of reward models and response quality from the resulting aligned LLMs. The effectiveness and accessibility of the mouse movement suggest a natural path toward a selfreinforcing data flywheel driven by ordinary user interactions.

### [3] 2606.20538::00088
_section: 7. Conclusion and Limitations_

> Paper: Multi-Task Bayesian In-Context Learning
Section: 7. Conclusion and Limitations

We introduced Multi-Task Bayesian In-Context Learning , a simple framework that bridges the flexibility and scalability of in-context learning with the principled structure of hierarchical Bayesian inference by representing priors explicitly as in-context dataset prefixes, enabling test-time control over the prior. Empirically, our approach matches oracle Bayesian predictors across diverse prior families, generalizes robustly under out-of-meta-distribution shifts, and achieves orders-of-magnitude faster inference than classical Bayesian baselines. We further demonstrate its practical applicability on a real-world environmental benchmark.

### [4] 2606.20508::00101
_section: A. Additional Experimental Setup Details_

> Paper: What Do Safety-Aligned LLMs Learn From Mixed Compliance Demonstrations?
Section: A. Additional Experimental Setup Details

Harmful compliance demonstration pool setup. Our harmful demonstration prompts are derived from RedTeam-2K, a 2K-query harmful request collection introduced as part of JailBreakV (Luo et al., 2024). Because RedTeam-2K includes heterogeneous sources and varying degrees of explicitness, we first filter the raw request set with GPT-OSS-120B (OpenAI, 2025), used as a judge to retain only requests that are explicitly harmful under the study's threat model. After filtering and generating responses, this harmful pool contains 1,492 harmful compliance demonstrations.

### [5] 2606.20467::00079
_section: 4 Conclusion_

> Paper: Agentic Symbolic Search: Characterizing PDEs Beyond Hand-crafted Expressions, Meshes, and Neural Networks
Section: 4 Conclusion

Several extensions follow naturally from the current framework. The scoring system introduced in Section 2.3 evaluates representations using only equation residuals and public constraints, with no observed solution data. Incorporating observed data as a third scoring signal would extend the method to inverse problems, where the governing equation is partially known and unknown terms or parameters must be recovered from measurements. Because the evaluator structure remains unchanged, this extension requires only an additional score dimension, not a redesign of the search. A second extension is methodological: ablate the specificity of the problem guidance, separating what comes from public mathematical prior knowledge from what is found by outer-loop exploration under weaker prompts. Beyond forward and inverse problems on canonical equations, applying the method to real-world systems introduces further challenges: noisy and partial observations, uncertain or approximate governing equations, and phenomena such as turbulence whose characteristic structures remain open mathematical questions. Finally, the representations produced here are starting points for rigorous analysis: an ansatz that captures the correct scale, exponent, or profile can inform conjectures, guide function-space design, or seed computer-assisted proofs (Wang et al., 2023; Chen and Hou, 2025). Connecting agent-generated representations to formal verification is a natural next step.

---

## Q02: specific_fact_lookup

**Question**: What evaluation metrics does CalTennis use for monocular-to-3D tennis pose estimation?

**Metrics**: R@5=1.00 | R@1=1.00 | MRR=1.00 | CtxP=0.80 | CtxR=0.25 | Faith=1.00 | AnsCorr=0.60

**Gold chunk_ids**: ['2606.20542::00035']

**Gold answer**:
> MPJPE, PA-MPJPE, PVE, translation error, foot work, and stability.

**Gold chunk text(s)**:
- **2606.20542::00035** _(section: 5 Evaluation Metrics)_:
  > Paper: CalTennis: Large Multi-View Tennis Video Dataset and Benchmark of Monocular-to-3D Pose Estimation
Section: 5 Evaluation Metrics

CalTennis uses multi-view video recordings for label-free evaluation of monocular pose estimates: a correct prediction must agree across views, and inter-view disagreement lower-bounds each model's error. In addition to the standard metrics of MPJPE, PA-MPJPE, and PVE [17], we introduce further metrics that capture additional notions of correctness that are relevant for downstream applications.


**Top-5 retrieved**:

### [1] 2606.20542::00035 GOLD HIT
_section: 5 Evaluation Metrics_

> Paper: CalTennis: Large Multi-View Tennis Video Dataset and Benchmark of Monocular-to-3D Pose Estimation
Section: 5 Evaluation Metrics

CalTennis uses multi-view video recordings for label-free evaluation of monocular pose estimates: a correct prediction must agree across views, and inter-view disagreement lower-bounds each model's error. In addition to the standard metrics of MPJPE, PA-MPJPE, and PVE [17], we introduce further metrics that capture additional notions of correctness that are relevant for downstream applications.

### [2] 2606.20542::00016
_section: 1 Introduction_

> Paper: CalTennis: Large Multi-View Tennis Video Dataset and Benchmark of Monocular-to-3D Pose Estimation
Section: 1 Introduction

Evaluation methodology. A label-free framework for evaluating monocular 3D pose estimators using multi-view consistency as a lower bound on error, together with new inconsistency metrics: stability, foot skating, and body shape, that expose failure modes invisible to standard benchmarks.

### [3] 2606.20542::00039
_section: 5 Evaluation Metrics_

> Paper: CalTennis: Large Multi-View Tennis Video Dataset and Benchmark of Monocular-to-3D Pose Estimation
Section: 5 Evaluation Metrics

where Z = TPK foot normalizes across frames, persons, and foot joints k .

### [4] 2606.20542::00001
_section: Abstract_

> Paper: CalTennis: Large Multi-View Tennis Video Dataset and Benchmark of Monocular-to-3D Pose Estimation
Section: Abstract

The Caltech Tennis Dataset (CalTennis) is a large-scale video benchmark for evaluating monocular-to-3D pose estimation in the wild. CalTennis comprises over 11 million frames (51 hours) of tennis practice and match play from 40 players, captured with 2-6 synchronized cameras at 60Hz. It is 10× larger than existing in-the-wild human motion video datasets and 3× larger than existing MOCAPground-truthed datasets, and it is the first large-scale benchmark to provide synchronized multi-view recordings of expert athletic motion. The multi-view setup enables inexpensive, label-free evaluation of monocular-to-3D pose estimation algorithms. We describe a simple, standardized protocol that enables data collection without specialized equipment or expertise, along with fully automated video calibration and synchronization. Benchmarking state-of-the-art monocular-to-3D pose methods on CalTennis, we find that while 3D joint angle recovery is now quite accurate, all models struggle to estimate depth and foot contact consistently. We further propose two novel performance metrics - footwork and stability - as well as qualitatively study body shape inconsistency. These metrics expose previously underexplored failure modes and point to concrete opportunities for improvement in pose estimation and action analysis.

### [5] 2606.20542::00044
_section: 6 Experimental Evaluation_

> Paper: CalTennis: Large Multi-View Tennis Video Dataset and Benchmark of Monocular-to-3D Pose Estimation
Section: 6 Experimental Evaluation

Table 2: Overall Model Performance. We report multi-view consistency of poses estimated by SOTA models run on CalTennis (§6.1). Results are in millimeters ( mm ), except for foot-velocity ( m/s ). We define these metrics in §5. Different models excel at different aspects of motion reconstruction: PromptHMR produces the most consistent translation and pose estimates, whereas WHAMproduces the most consistent foot velocity estimates. All metrics computed on the first 5M frames of CalTennis; full results forthcoming.

---

## Q03: specific_fact_lookup

**Question**: In the Calibrated Mixture-of-Experts under Distribution Shift paper, what is the third takeaway from the experiments?

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=0.67 | AnsCorr=0.09

**Gold chunk_ids**: ['2606.20544::00088']

**Gold answer**:
> Robust filters give better accuracy / calibration trade-off than full re-weighting in several settings.

**Gold chunk text(s)**:
- **2606.20544::00088** _(section: 6.3. Results)_:
  > Paper: Toward Calibrated Mixture-of-Experts Under Distribution Shift
Section: 6.3. Results

Takeaway 3: Robust Filtered gives a better accuracycalibration tradeoff than full reweighting in several settings. The full Robust MoE objective puts additional weight on all high-loss examples, which can improve calibration sharply but may overemphasize examples that are hard for reasons unrelated to routing. This is visible on CIFAR10H and PACS-Art, where Robust MoE lowers hard-subset calibration error but loses accuracy relative to the strongest non-robust classifier. Robust Filtered mitigates this tradeoff by applying the robust term only to routing-relevant examples while retaining an ERM term on the full minibatch. It achieves the best overall CIFAR-10H ECE ( 0 . 013 ), the best CivilComments accuracy ( 0 . 915 ), and the best PACSSketch accuracy ( 0 . 670 ), while maintaining much lower ECE than the non-robust MoE baselines.


**Top-5 retrieved**:

### [1] 2606.20544::00237
_section: E. Additional figures/experiments_

> Paper: Toward Calibrated Mixture-of-Experts Under Distribution Shift
Section: E. Additional figures/experiments

We report reliability diagrams for all methods in Figure E.4, evaluated separately on (a) the full test set and (b) the hard subset of low-agreement images. Panel (a) is an expanded view of Figure 1 that includes per-bin error bars, while panel (b) restricts the same diagnostic to the routing-stressed subset and is the most direct visual evidence for Takeaway 1 in §6: the non-robust baselines concentrate predictions in the highest-confidence bins despite low accuracy on those bins, while the robust methods spread mass over a wider confidence range that more closely tracks the diagonal.

### [2] 2606.20544::00226
_section: D.5. Evaluation protocol_

> Paper: Toward Calibrated Mixture-of-Experts Under Distribution Shift
Section: D.5. Evaluation protocol

The hard-subset notion in CIFAR-10H is the only one of the three that is not directly observable at training time, since human-agreement annotations exist only for the test split.

### [3] 2606.20544::00123
_section: References_

> Paper: Toward Calibrated Mixture-of-Experts Under Distribution Shift
Section: References

Ursula Hébert-Johnson, Michael Kim, Omer Reingold, and Guy Rothblum. Multicalibration: Calibration for the (computationally-identifiable) masses. In International Conference on Machine Learning , pages 1939-1948. PMLR, 2018.

### [4] 2606.20544::00016
_section: 2. Background_

> Paper: Toward Calibrated Mixture-of-Experts Under Distribution Shift
Section: 2. Background

We assume throughout that each expert is calibrated on the view of the data induced by the router so that its prediction can be read as the conditional label frequency on that view. Proper losses such as cross-entropy and the Brier score encourage this kind of expert-level calibration on the training distribution, and related mixture-of-calibrated-experts methods explicitly calibrate experts before combining them (Oksuz et al., 2024; Roschewitz et al., 2025). This is a deliberately favorable assumption for MoEs: by granting calibrated experts, we rule out the simplest explanation for a miscalibrated MoE (unreliable experts) as well as the simplest remedy (calibrating the experts). Our analysis therefore asks what routing and aggregation in particular can or cannot guarantee for the final MoE predictor.

### [5] 2606.20544::00234
_section: E. Additional figures/experiments_

> Paper: Toward Calibrated Mixture-of-Experts Under Distribution Shift
Section: E. Additional figures/experiments

This appendix collects supporting figures for the experiments in §6. For each dataset we provide reliability diagrams for all methods, evaluated both on the full test set and on the dataset's hard subset (§D.5). We close with sensitivity ablations for the robustness parameter η and the warmup horizon.

---

## Q04: specific_fact_lookup

**Question**: What number of user prompts did the team use when generating Diffusion Gemma?

**Metrics**: R@5=1.00 | R@1=1.00 | MRR=1.00 | CtxP=1.00 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.57

**Gold chunk_ids**: ['2606.20560::00045']

**Gold answer**:
> 800.

**Gold chunk text(s)**:
- **2606.20560::00045** _(section: 3.2. What Are the Top Tokens?)_:
  > Paper: How Transparent is DiffusionGemma?
Section: 3.2. What Are the Top Tokens?

We generate DiffusionGemma rollouts on 𝑛 = 800 user prompts from the WildChat dataset (Zhao et al., 2024) up to a maximum of 1024 generated tokens (four canvases) with no early stopping and 𝑇 = 48. At each denoising step 𝑡 and sequence position 𝑖 , we take the results of the softmax in Equation (1) and extract the set of tokens that meet one of the following conditions:


**Top-5 retrieved**:

### [1] 2606.20560::00045 GOLD HIT
_section: 3.2. What Are the Top Tokens?_

> Paper: How Transparent is DiffusionGemma?
Section: 3.2. What Are the Top Tokens?

We generate DiffusionGemma rollouts on 𝑛 = 800 user prompts from the WildChat dataset (Zhao et al., 2024) up to a maximum of 1024 generated tokens (four canvases) with no early stopping and 𝑇 = 48. At each denoising step 𝑡 and sequence position 𝑖 , we take the results of the softmax in Equation (1) and extract the set of tokens that meet one of the following conditions:

### [2] 2606.20560::00077
_section: 5.1.3. Non-autoregressive code generation_

> Paper: How Transparent is DiffusionGemma?
Section: 5.1.3. Non-autoregressive code generation

When DiffusionGemma is asked to produce code, it frequently will not reason chronologically, but will instead approach the problem in discrete chunks. In Figure 9, we show an annotated SummaryView where we prompt DiffusionGemma to write a Python function that returns the longest contiguous subarray of a list of integers.

### [3] 2606.20560::00063
_section: 4. Monitorability_

> Paper: How Transparent is DiffusionGemma?
Section: 4. Monitorability

Figure 5 | DiffusionGemma thinks less than Gemma on all monitorability evaluations. Error bars show 95% confidence intervals of mean number of characters in each model's chain of thought.

### [4] 2606.20560::00113
_section: 7.1. Further Understanding DiffusionGemma's Behavior_

> Paper: How Transparent is DiffusionGemma?
Section: 7.1. Further Understanding DiffusionGemma's Behavior

Model diffing: It might be interesting to apply black-box model diffing tools to DiffusionGemma and Gemma to try to understand the behavioral differences between them (Kempf et al., 2026; Chughtai, 2026).

### [5] 2606.20560::00011
_section: 1. Introduction_

> Paper: How Transparent is DiffusionGemma?
Section: 1. Introduction

Monitorability: Guan et al., 2025 introduce a suite of monitorability evaluations that study the informativeness of a model's chain of thought via the proxy task of monitors' ability to extract said information. In Section 4 we adapt these evaluations and apply them to DiffusionGemma, finding that DiffusionGemma and Gemma 4 are similarly monitorable.

---

## Q05: specific_fact_lookup

**Question**: What metrics does UltraQuant use to characterize serving efficiency for 4-bit KV caching?

**Metrics**: R@5=1.00 | R@1=1.00 | MRR=1.00 | CtxP=0.75 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.92

**Gold chunk_ids**: ['2606.20474::00013']

**Gold answer**:
> Time to first token (TTFT) and time per output token (TPOT).

**Gold chunk text(s)**:
- **2606.20474::00013** _(section: 3 Agentic Workflow and Concurrency Analysis)_:
  > Paper: UltraQuant: 4-bit KV Caching for Context-Heavy Agents
Section: 3 Agentic Workflow and Concurrency Analysis

Agentic workloads are long-running sessions with a large shared prefix and many shorter follow-up turns. In this setting, compression matters because it increases the number of useful prefixes that remain resident on device. Compression alone, however, does not guarantee better serving outcomes: the overhead introduced by quantization and dequantization can degrade token latency, making end-to-end serving measurement essential. We characterize serving efficiency through two metrics: time-to-first-token (TTFT) and time-per-outputtoken (TPOT).


**Top-5 retrieved**:

### [1] 2606.20474::00013 GOLD HIT
_section: 3 Agentic Workflow and Concurrency Analysis_

> Paper: UltraQuant: 4-bit KV Caching for Context-Heavy Agents
Section: 3 Agentic Workflow and Concurrency Analysis

Agentic workloads are long-running sessions with a large shared prefix and many shorter follow-up turns. In this setting, compression matters because it increases the number of useful prefixes that remain resident on device. Compression alone, however, does not guarantee better serving outcomes: the overhead introduced by quantization and dequantization can degrade token latency, making end-to-end serving measurement essential. We characterize serving efficiency through two metrics: time-to-first-token (TTFT) and time-per-outputtoken (TPOT).

### [2] 2606.20474::00010
_section: 2.3 Serving Systems and Hardware-Native Low Precision_

> Paper: UltraQuant: 4-bit KV Caching for Context-Heavy Agents
Section: 2.3 Serving Systems and Hardware-Native Low Precision

vLLM-style paged serving (Kwon et al., 2023) makes KV-cache residency a systems concern, not only a compression metric. Hardware-native formats such as FP8 already benefit from direct matrixcore support. UltraQuant extends this serving-first lens to 4-bit KV caching by targeting the CDNA4 scaled-F8F6F4 MFMA path, where FP4 operands and UE8M0 scales are consumed by the matrix core itself.

### [3] 2606.20474::00011
_section: 2.3 Serving Systems and Hardware-Native Low Precision_

> Paper: UltraQuant: 4-bit KV Caching for Context-Heavy Agents
Section: 2.3 Serving Systems and Hardware-Native Low Precision

Table 1: Agentic serving results on MiniMax-M2.5, TP = 2 , AMDMI355X, reported as UltraQuant relative to the FP8 KV baseline (higher is better except where noted). The advantage appears in the late rounds, where long per-client prefixes exceed the effective residentcache capacity of FP8: TTFT improves 3 . 47 × and is recovered through cache residency rather than re-prefill.

| Metric                       | UltraQuant vs. FP8 KV   |
|------------------------------|-------------------------|
| P50 TTFT -warm rounds (r2-3) | 0 . 86 × (FP8 faster)   |
| P50 TTFT -late rounds (r4-6) | 3 . 47 ×                |
| P50 TTFT -all rounds         | 2 . 3 ×                 |
| Output throughput            | 1 . 63 ×                |

### [4] 2606.20474::00002
_section: Abstract_

> Paper: UltraQuant: 4-bit KV Caching for Context-Heavy Agents
Section: Abstract

Context-heavy agents place unusual pressure on the key-value (KV) cache: long prefixes are reused across many short turns, while concurrency determines whether the serving system can keep GPUs utilized. We study 4-bit KV-cache compression for this setting, using TurboQuant-style rotation and codebook quantization (Zandieh et al., 2026) as a quality anchor and vLLM FP8 KV caching as the deployment anchor. We report three contributions. First, we frame 4-bit KV caching around multi-round agent workloads where task quality, cache residency, and serving throughput must be measured jointly. Second, we describe the practical design choices needed to make the 4-bit path robust, including asymmetric K/V treatment, Walsh-Hadamard rotation (Walsh, 1923; Hadamard, 1893), QJL removal (Zandieh et al., 2024), and block-scale variants. Third, we present serving optimizations on AMD GPUs, including optimized decode-attention kernels and UltraQuant , an FP4 approximation path that uses FP8 queries, FP4 KV tensors, UE8M0 group scales, and native scaledMFMAsupport on CDNA4. On a long-context, multi-turn agentic workload, UltraQuant cuts P50 time-to-first-token by 3 . 47 × in the cachepressured late rounds ( 2 . 3 × across all rounds) and raises output throughput by 1 . 63 × over the FP8 KV baseline.

### [5] 2606.20474::00034
_section: 7 Performance Results_

> Paper: UltraQuant: 4-bit KV Caching for Context-Heavy Agents
Section: 7 Performance Results

Figure 4: UltraQuant throughput (relative to BF16) vs. BF16, FP8 KV, and Ultra-TQ on MiniMax-M2.5 (TP = 2 , 2 × MI355X).

Figure 5: Median time per output token (relative to BF16) for the MiniMax-M2.5 32K/1K, C =64 , TP = 2 serving configuration.

---

## Q06: specific_fact_lookup

**Question**: In the Calibration Without Comprehension paper on fine-tuning LLMs for vulnerability detection, what is finding two of RQ1?

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=1.00 | AnsCorr=0.11

**Gold chunk_ids**: ['2606.20502::00070']

**Gold answer**:
> Fine-tuning effect is determined by the base model's initial competence.

**Gold chunk text(s)**:
- **2606.20502::00070** _(section: B. Finding 2: Fine-Tuning Effect Is Determined by the Base Model's Initial Competence)_:
  > Paper: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software
Section: B. Finding 2: Fine-Tuning Effect Is Determined by the Base Model's Initial Competence

Fine-tuning does not uniformly improve detection; direction and magnitude track the backbone's starting condition. For Qwen3-4B , performance rises by +27 . 5 to +41 . 5 pp because fine-tuning mainly overcomes abstention: coverage increases from 36 . 9% to above 91% , so the apparent gain reflects producing binary verdicts rather than learning transferable vulnerability semantics. For Llama3.1 , fine-tuning is mostly neutral or harmful ( -0 . 2 to -50 . 7 pp), with Devign-FT collapsing to 1 . 3% Overall and 4 . 1% coverage on PBD. For DeepSeek-R1 , fine-tuning consistently degrades detection ( -0 . 6 to -29 . 1 pp on LFD), often amplifying its paranoid prior. The hardest backbone to improve in detection benefits most in RQ2 coarse CWE classification, reinforcing that detection and understanding are weakly coupled.


**Top-5 retrieved**:

### [1] 2606.20502::00098
_section: A. The Backbone's Directional Prior Dominates Fine-Tuning_

> Paper: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software
Section: A. The Backbone's Directional Prior Dominates Fine-Tuning

The near-random accuracy ( ∼ 50% ) observed in RQ1 masks extreme, backbone-determined, and stable directional biases. Two failure modes emerge from DFI analysis:

### [2] 2606.20502::00074
_section: E. Finding 5: Context Depth Is Necessary but Not Sufficient_

> Paper: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software
Section: E. Finding 5: Context Depth Is Necessary but Not Sufficient

RQ1 yields a stronger conclusion than 'accuracy is low': stable directional priors dominate the decision policy, finetuning mainly shifts these priors rather than learning robust, transferable behavior, and neither labeled CWE overlap nor contaminated seen-CVE overlap provides a reliable path to improved detection.

### [3] 2606.20502::00001
_section: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software_

> Paper: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software
Section: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software

Abstract -Whether Large Language Models (LLMs) scoring well on vulnerability benchmarks genuinely reason about security or merely pattern-match on contaminated data remains unresolved. We present CWE-Trace, a framework for LLM vulnerability detection built from 834 manually curated Linux kernel samples spanning 74 Common Weakness Enumerations (CWEs). The framework enforces a strict temporal split (pre2025 historical set / post-cutoff leakage-free set), preserves context-aware vulnerable-patched pairs, and introduces two diagnostic metrics: the Directional Failure Index (DFI) and Hierarchical Distance and Direction (HDD). We evaluate eight vanilla LLMs and 15 LoRA fine-tuned variants across nontargeted detection, targeted detection, and CWE classification. Our analysis yields two key results. First, data contamination provides no measurable advantage. Function-level analysis shows that 84% of nominally contaminated samples carry no usable memorization signal: vulnerable functions are absent or crossmapped across datasets, and ∼ 31% of contaminated samples carry CWE misclassification. Second, backbone directional priors dominate fine-tuning. Models exhibit stable, systematic failure modes (DFI ranging from -85 . 5 to +94 . 8 pp) that persist from historical to post-cutoff data and resist correction. Fine-tuning shifts the output threshold without changing the decision policy. This is calibration without comprehension: output distributions adapt to training data while the underlying security reasoning remains absent. The weakest backbone at binary detection (DeepSeek-R1) gains the most in coarse CWE classification, revealing that detection and understanding are decoupled capabilities. The best detection score reaches only 52 . 1% ( +2 . 1 pp above chance); exact CWE ranking remains below 1 . 3% Top1 accuracy, confirming that current LLMs lack reliable security reasoning for systems software, regardless of fine-tuning strategy.

### [4] 2606.20502::00075
_section: VI. RQ2: CWE-1000 CLASSIFICATION BEFORE AND AFTER FINE-TUNING_

> Paper: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software
Section: VI. RQ2: CWE-1000 CLASSIFICATION BEFORE AND AFTER FINE-TUNING

RQ2 asks whether models can place vulnerabilities into the correct coarse CWE-1000 root family, a weaker target than exact CWE identification, capturing broad security understanding before probing semantic depth in RQ3.

### [5] 2606.20502::00062
_section: IV. EXPERIMENTAL SETUP_

> Paper: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software
Section: IV. EXPERIMENTAL SETUP

RQ1 (Vulnerability Detection Reliability): How reliably do vanilla and fine-tuned models detect vulnerabilities and verify patches, and what roles do directional bias, label-space transfer, and contamination play?

---

## Q07: definition

**Question**: What is MAA?

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=0.50 | AnsCorr=0.12

**Gold chunk_ids**: ['2606.20475::00011']

**Gold answer**:
> Marginal Advantage Accumulation (MAA) for Memory-Driven Agent Self-Evolution. Its core idea is to ground user-perceived 'optimization suggestions' into addressable atomic operations (ops) with invariant identity across batches, and on this basis construct scale-consistent accumulation signals so that evidence of the same op across different batches can be additively aggregated.

**Gold chunk text(s)**:
- **2606.20475::00011** _(section: 1.3 Method Overview and Contributions)_:
  > Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 1.3 Method Overview and Contributions

To address the above gap, we propose Marginal Advantage Accumulation (MAA) for Memory-Driven Agent Self-Evolution. As illustrated in Figure 1, the core idea of MAA is to ground user-perceived 'optimization suggestions' into addressable atomic operations (ops) with invariant identity across batches, and on this basis construct scale-consistent accumulation signals so that evidence of the same op across different batches can be additively aggregated.


**Top-5 retrieved**:

### [1] 2606.20560::00131
_section: 7.4. Model organism research_

> Paper: How Transparent is DiffusionGemma?
Section: 7.4. Model organism research

The model organism research agenda (Hubinger et al., 2023) aims to create controlled examples of dangerous model properties like misalignment and strategic reasoning obfuscation. DiffusionGemma is a promising base model to create interesting model organisms from; for example, we are excited about finetuning DiffusionGemma to reason strategically during denoising steps but hide this reasoning from the final answer or finetuning DiffusionGemma to have reduced CoT monitorability.

### [2] 2606.20538::00022
_section: 4. Multi-Task Bayesian In-Context Learning_

> Paper: Multi-Task Bayesian In-Context Learning
Section: 4. Multi-Task Bayesian In-Context Learning

A major challenge in making in-context learning more Bayesian is the lack of our knowledge of and control over the implicit latent variable Z . This latent variable is implicitly defined and marginalized out as part of the process of in-context learning. Even if we know what this latent variable was, it is unclear what is the best way to represent this latent variable and the prior distribution over it and present it to the in-context learner.

### [3] 2606.20520::00139
_section: 8 System Evaluation_

> Paper: Sovereign Execution Brokers: Enforcing Certificate-Bound Authority in Agentic Control Planes
Section: 8 System Evaluation

RQ3 (Credential Minting Cost): What is the computational and network cost of dynamic scoped credential issuance?

RQ4 (Drift Detection): How does the drift check perform under live state queries, and what is its overhead?

### [4] 2606.20485::00005
_section: Background: what is a many-body system?_

> Paper: Optimal Order of Multi-Agent and General Many-Body Systems
Section: Background: what is a many-body system?

In social systems of multi-agents, we often face the problem of optimization. How much concentration and synchronization of agents' power are optimal? Why market sentiment swings between risk-on and risk-off? What is the trade-off between economic growth and avoiding recession? What determines the outcome of group behavior between crowd-wisdom and crowdmadness? How much should government intervene from top down vs let agents act from bottom up? All these questions lead to, what is the optimal order? Is such optimality absolute (objective) or relative (subjective)?

### [5] 2606.20560::00124
_section: 7.3. Replicating and Extending Chain-of-Thought Work on DiffusionGemma_

> Paper: How Transparent is DiffusionGemma?
Section: 7.3. Replicating and Extending Chain-of-Thought Work on DiffusionGemma

Evaluating controllability: Run the controllability evaluations introduced by Korbak, Balesni, et al. (2025). It may be that DiffusionGemma has much more controllability of its outputs than standard reasoning models do of their reasoning outputs.

---

## Q08: definition

**Question**: What does mobility refer to?

**Metrics**: R@5=1.00 | R@1=1.00 | MRR=1.00 | CtxP=0.87 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.48

**Gold chunk_ids**: ['2606.20485::00079']

**Gold answer**:
> Mobility refers to the ability of agents, resources, information, and influence to change positions within a system over time.

**Gold chunk text(s)**:
- **2606.20485::00079** _(section: Mobility and Viscosity)_:
  > Paper: Optimal Order of Multi-Agent and General Many-Body Systems
Section: Mobility and Viscosity

Mobility refers to the ability of agents, resources, information, and influence to change positions within a system over time. Mobility cannot be inferred from either growth or volatility. In economic systems, mobility may describe the ability of individuals to move across wealth or income ranks [Carroll & Cohen-Kristiansen 2022]. In organizations, mobility reflects the ability of individuals to assume new roles and responsibilities. In knowledge systems, mobility describes the ability of ideas and beliefs to evolve in response to new evidence. More generally, mobility measures the adaptability and flexibility of a system [Lo & Zhang 2024]. A highly productive but immobile system may become incapable of adaptation or self-repair, while a highly mobile system may fail to accumulate sufficient structure and coordination. The optimal system therefore balances productivity, stability, and mobility.


**Top-5 retrieved**:

### [1] 2606.20485::00079 GOLD HIT
_section: Mobility and Viscosity_

> Paper: Optimal Order of Multi-Agent and General Many-Body Systems
Section: Mobility and Viscosity

Mobility refers to the ability of agents, resources, information, and influence to change positions within a system over time. Mobility cannot be inferred from either growth or volatility. In economic systems, mobility may describe the ability of individuals to move across wealth or income ranks [Carroll & Cohen-Kristiansen 2022]. In organizations, mobility reflects the ability of individuals to assume new roles and responsibilities. In knowledge systems, mobility describes the ability of ideas and beliefs to evolve in response to new evidence. More generally, mobility measures the adaptability and flexibility of a system [Lo & Zhang 2024]. A highly productive but immobile system may become incapable of adaptation or self-repair, while a highly mobile system may fail to accumulate sufficient structure and coordination. The optimal system therefore balances productivity, stability, and mobility.

### [2] 2606.20485::00080
_section: Mobility and Viscosity_

> Paper: Optimal Order of Multi-Agent and General Many-Body Systems
Section: Mobility and Viscosity

Mobility (or fluidity) is often modeled as inversely proportional to viscosity. Viscosity represents the resistance of the system to redistribution of power, wealth, influence, or information, which reflects the friction or linkage of agents. One hypothesis of this paper is that viscosity/mobility is related to the strength of feedback interactions 𝐵𝐵 𝑖𝑖 among agents. For example, we can hypothesize viscosity as 𝑉𝑉 = ∑ | 𝐵𝐵 𝑖𝑖 𝑵𝑵 𝒊𝒊=𝟏𝟏 | , mobility is M=1/V .

### [3] 2606.20485::00081
_section: Mobility and Viscosity_

> Paper: Optimal Order of Multi-Agent and General Many-Body Systems
Section: Mobility and Viscosity

A more generic objective function including mobility to maximize is,

𝐺𝐺 = 𝑎𝑎 1 ∗ dW W + 𝑎𝑎2 ∗ 𝜎𝜎 𝑊𝑊 2 + 𝑎𝑎3 ∗ 𝑀𝑀 (24)

### [4] 2606.20485::00113
_section: VI. Conclusions_

> Paper: Optimal Order of Multi-Agent and General Many-Body Systems
Section: VI. Conclusions

Several important questions remain open for future research. These include the empirical measurement of agent response functions, the formal characterization of mobility and adaptability, the relationship between synchronization and systemic fragility, and the development of practical methods for identifying optimal order in real-world systems. Addressing these questions may lead to a deeper understanding of how complex systems grow, adapt, learn, and sustain themselves over time.

### [5] 2606.20506::00217
_section: [Evaluation Criterion]_

> Paper: FreeStyle: Free Control of Style-Content Dual-Reference Generation from Community LoRA Mining
Section: [Evaluation Criterion]

-Color does not refer to surface grain, texture, or line quality.

SHAPE (shape language and form-construction conventions)

-The degree of geometric abstraction or realism, exaggerated

---

## Q09: definition

**Question**: In the Hierarchical Recovery for Cross-Device Agent Systems paper, what is the Strategy Planner?

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=1.00 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.96

**Gold chunk_ids**: ['2606.20487::00026']

**Gold answer**:
> The Strategy Planner is the device-level planner responsible for selecting and revising execution strategies within a single device.

**Gold chunk text(s)**:
- **2606.20487::00026** _(section: 3.4 STRATEGY PLANNER)_:
  > Paper: Beyond Global Replanning: Hierarchical Recovery for Cross-Device Agent Systems
Section: 3.4 STRATEGY PLANNER

The Strategy Planner is the device-level planner responsible for selecting and revising execution strategies within a single device. Similar to interactive agents that choose actions based on recent observations (Yao et al., 2023), it maps the assigned subtask and previous observations to one of three decisions:

S d ( q j , h j , b j , Φ( d )) →{ EXECUTE ( π, x ) , DONE ( y j ) , ESCALATE ( c j ) }


**Top-5 retrieved**:

### [1] 2606.20487::00017
_section: 3.2 HIERARCHICAL REPLANNING OVERVIEW_

> Paper: Beyond Global Replanning: Hierarchical Recovery for Cross-Device Agent Systems
Section: 3.2 HIERARCHICAL REPLANNING OVERVIEW

This hierarchy separates system-level recovery from device-level recovery. The Strategy Planner handles failures that can be resolved within the current device by changing or continuing local strategies, while the Orchestrator intervenes only when device-level feedback indicates that the remaining work requires cross-device reassignment, downstream context revision, or global plan repair.

### [2] 2606.20487::00027
_section: 3.4 STRATEGY PLANNER_

> Paper: Beyond Global Replanning: Hierarchical Recovery for Cross-Device Agent Systems
Section: 3.4 STRATEGY PLANNER

where h j is the local execution history, b j is the remaining local budget, π is the selected strategy, x is the execution instruction sent to the strategy execution agent, y j is the final local result, and c j is the escalation evidence passed upward.

### [3] 2606.20487::00006
_section: 1 INTRODUCTION_

> Paper: Beyond Global Replanning: Hierarchical Recovery for Cross-Device Agent Systems
Section: 1 INTRODUCTION

To address this challenge, we propose H-RePlan , a hierarchical replanning framework for multidevice agents with unified API-CLI-GUI execution. H-RePlan introduces a platform-independent strategy-control abstraction that represents each device by its supported subset of API, CLI, and GUI execution strategies. At the device layer , a Strategy Planner decomposes assigned subtasks, selects execution strategies, and performs local recovery by revising the strategy or instruction when a strategy-level failure occurs. At the system layer , an Orchestrator maintains the cross-device task plan, incorporates failure evidence from devices, and handles device-level failures through reassignment or recovery subtasks.

### [4] 2606.20487::00016
_section: 3.2 HIERARCHICAL REPLANNING OVERVIEW_

> Paper: Beyond Global Replanning: Hierarchical Recovery for Cross-Device Agent Systems
Section: 3.2 HIERARCHICAL REPLANNING OVERVIEW

Figure 2: Overview of H-RePlan's hierarchical replanning loop. The Orchestrator maintains the global plan, while device-level Strategy Planners coordinate API, CLI, and GUI execution agents against heterogeneous environments.

### [5] 2606.20487::00043
_section: 4.2 MAIN RESULTS_

> Paper: Beyond Global Replanning: Hierarchical Recovery for Cross-Device Agent Systems
Section: 4.2 MAIN RESULTS

Figure 4a reveals how hierarchical recovery drives these gains at the device level. We define early escalation as escalation to the Orchestrator within at most two local strategy attempts, and late escalation as escalation after more than two local attempts. As intended, the Strategy Planner mostly contains local faults within the device layer by dynamically pivoting strategies, while global and mixed faults more often trigger early escalation.

---

## Q10: definition

**Question**: What is a contagion network?

**Metrics**: R@5=1.00 | R@1=0.00 | MRR=0.33 | CtxP=1.00 | CtxR=0.75 | Faith=1.00 | AnsCorr=0.44

**Gold chunk_ids**: ['2606.20493::00004', '2606.20493::00005']

**Gold answer**:
> A contagion network describes how evaluator biases propagate across interacting LLM agents through a closed feedback loop where biased judgments from one agent directly shape another agent's subsequent outputs; the paper formalizes this phenomenon as Contagion Networks, where bias can propagate hop-by-hop (e.g., A → B → C) and, if the process iterates, the entire agent network can converge to a single strategy.

**Gold chunk text(s)**:
- **2606.20493::00004** _(section: 1 Introduction)_:
  > Paper: Contagion Networks: Evaluator Bias Propagation in Multi-Agent LLM Systems
Section: 1 Introduction

Consider a concrete scenario: Agent A (GPT-4o) evaluates Agent B 's (DeepSeek) code generation output. GPT-4o, shaped by RLHF training on structured explanations, strongly prefers step-by-step reasoning. This feedback causes DeepSeek to increasingly adopt step-bystep strategies. Now Agent B evaluates Agent C 's (Claude) output-and applies the same step-by-step preference it absorbed from Agent A . Claude, in turn, shifts toward step-by-step. The bias has propagated two hops: A → B → C . If the process iterates, the entire agent network converges to a single strategy, eliminating the very cognitive diversity that multi-agent systems are designed to exploit.

- **2606.20493::00005** _(section: 1 Introduction)_:
  > Paper: Contagion Networks: Evaluator Bias Propagation in Multi-Agent LLM Systems
Section: 1 Introduction

We formalize this phenomenon as Contagion Networks and make the following contributions:


**Top-5 retrieved**:

### [1] 2606.20493::00015
_section: 2.3 Epidemiological Models in AI Systems_

> Paper: Contagion Networks: Evaluator Bias Propagation in Multi-Agent LLM Systems
Section: 2.3 Epidemiological Models in AI Systems

Table 1: Systematic comparison with related phenomena. Contagion Networks is the only framework simultaneously capturing multi-agent, multi-hop propagation dynamics.

### [2] 2606.20493::00069
_section: 6.3 Connection to Cross-Modal Contagion (MM-EPC)_

> Paper: Contagion Networks: Evaluator Bias Propagation in Multi-Agent LLM Systems
Section: 6.3 Connection to Cross-Modal Contagion (MM-EPC)

Together, they define a Γ formalism that spans both agent and modality dimensions, potentially generalizable to a tensor Γ ijk indexed by (evaluator, target, modality).

### [3] 2606.20493::00005 GOLD HIT
_section: 1 Introduction_

> Paper: Contagion Networks: Evaluator Bias Propagation in Multi-Agent LLM Systems
Section: 1 Introduction

We formalize this phenomenon as Contagion Networks and make the following contributions:

### [4] 2606.20493::00066
_section: 6.3 Connection to Cross-Modal Contagion (MM-EPC)_

> Paper: Contagion Networks: Evaluator Bias Propagation in Multi-Agent LLM Systems
Section: 6.3 Connection to Cross-Modal Contagion (MM-EPC)

Our contagion matrix Γ N generalizes the 2 × 2 cross-modal contagion formalism introduced in MM-EPC [1]. While MM-EPC studied bias propagation between text and visual modalities within a single agent, Contagion Networks extend this to arbitrary numbers of agents with arbitrary interaction topologies. The mathematical framework of Γ is identical in both cases, but the domain shifts from modalities to agents .

### [5] 2606.20493::00049
_section: 5.2 Phase 2: Pairwise Contagion_

> Paper: Contagion Networks: Evaluator Bias Propagation in Multi-Agent LLM Systems
Section: 5.2 Phase 2: Pairwise Contagion

Finding 3 (Asymmetric Contagion): Contagion is asymmetric. Agent C (evidencebiased) exerts the strongest outward contagion ( ¯ γ C →· = 0 . 241 ), while Agent A shows the weakest outward effect ( ¯ γ A →· = 0 . 154 ). The C → B pathway produces the highest individual coefficient ( 0 . 304 ± 0 . 068 ).

---

## Q11: methodology

**Question**: In the Calibration Without Comprehension paper, how did they assess each model performance on detecting vulnerabilities in system software?

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=0.80 | CtxR=0.00 | Faith=1.00 | AnsCorr=0.87

**Gold chunk_ids**: ['2606.20502::00022']

**Gold answer**:
> CWE-Trace assesses security reasoning in vanilla and fine-tuned LLMs by extracting high-fidelity Linux kernel vulnerabilities, splitting them into temporal historical (PBD) and leakage-free (LFD) datasets, and evaluating models zero-shot on non-targeted detection, targeted detection, and hierarchical CWE classification using standard accuracy, coverage, DFI, and HDD. DFI quantifies directional decision bias, while HDD measures reasoning depth through shortest-path distance and error direction in the CWE taxonomy.

**Gold chunk text(s)**:
- **2606.20502::00022** _(section: III. METHODOLOGICAL FRAMEWORK)_:
  > Paper: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software
Section: III. METHODOLOGICAL FRAMEWORK

CWE-Trace (Figure 2) assesses security reasoning in vanilla and fine-tuned LLMs. We extract high-fidelity Linux kernel vulnerabilities and split them into temporal splits of historical (PBD) and leakage-free (LFD) datasets, and evaluate models zero-shot on non-targeted detection, targeted detection, and hierarchical CWE classification using standard accuracy, coverage, DFI, and HDD. DFI quantifies directional decision bias, while HDD measures reasoning depth through shortest-path distance and error direction in the CWE taxonomy. Although this study focuses on C/Linux, the framework's extraction pipeline, temporal-split protocol, and evaluation metrics are language-agnostic: the same logic applies directly to any codebase for which commit-level CVE fixes can be retrieved and manually validated. Extension to other languages (e.g., Java, Python) is therefore a straightforward engineering task and constitutes a concrete direction for future work. The goal is to separate broad detection ability from exact semantic diagnosis under a single benchmark.


**Top-5 retrieved**:

### [1] 2606.20502::00079
_section: A. Finding 1: Base Models Reach Moderate Coarse-Level Accuracy but With Macro Disparity_

> Paper: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software
Section: A. Finding 1: Base Models Reach Moderate Coarse-Level Accuracy but With Macro Disparity

TABLE VI VULNERABILITY DETECTION PERFORMANCE (STANDARD ACCURACY, %) ON PBD AND LFD. DFI MEASURES DECISION BIAS (POSITIVE: PARANOID/HIGH-FP; NEGATIVE: SKEPTICAL/HIGH-FN). CGR DENOTES THE EFFECT OF CWE CONTEXT; GEN = LFD -PBD. OVERALL IS THE MEAN OF PBD AVG AND LFD AVG, AND RANK IS BASED ON OVERALL ( 1 = BEST). PER-SECTION MEAN ROWS SUMMARIZE EACH BLOCK; IN THE RANK COLUMN, THEY REPORT THE AVERAGE RANK.

### [2] 2606.20502::00131
_section: REFERENCES_

> Paper: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software
Section: REFERENCES

A. Khare et al. , 'Understanding the effectiveness of large language models in detecting security vulnerabilities,' in 2025 IEEE Conference on Software Testing, Verification and Validation (ICST) . IEEE, 2025, pp. 103-114.

### [3] 2606.20502::00075
_section: VI. RQ2: CWE-1000 CLASSIFICATION BEFORE AND AFTER FINE-TUNING_

> Paper: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software
Section: VI. RQ2: CWE-1000 CLASSIFICATION BEFORE AND AFTER FINE-TUNING

RQ2 asks whether models can place vulnerabilities into the correct coarse CWE-1000 root family, a weaker target than exact CWE identification, capturing broad security understanding before probing semantic depth in RQ3.

### [4] 2606.20502::00062
_section: IV. EXPERIMENTAL SETUP_

> Paper: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software
Section: IV. EXPERIMENTAL SETUP

RQ1 (Vulnerability Detection Reliability): How reliably do vanilla and fine-tuned models detect vulnerabilities and verify patches, and what roles do directional bias, label-space transfer, and contamination play?

### [5] 2606.20502::00012
_section: I. INTRODUCTION_

> Paper: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software
Section: I. INTRODUCTION

Diagnostic metrics. DFI and HDD characterize how models fail beyond aggregate accuracy: DFI decomposes near-random scores into directional bias; HDD measures hierarchical error structure in CWE-1000.

---

## Q12: methodology

**Question**: How does the Multi-Qutrit Entropy Estimation paper estimate the quantum state using their variational quantum algorithm?

**Metrics**: R@5=1.00 | R@1=1.00 | MRR=1.00 | CtxP=1.00 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.95

**Gold chunk_ids**: ['2606.20504::00028', '2606.20504::00034']

**Gold answer**:
> The central idea is to learn a measurement basis in which the entropy can be inferred directly from classical measurement statistics. The variational circuit preserves the intrinsic entropy of the state and seeks a unitary transformation that approximately aligns the computational basis with the eigenbasis of the density matrix; the optimization favors bases that produce maximally non-uniform outcomes, so that p(θ) approximates the eigenvalue spectrum and the resulting measurement entropy provides an estimate of the von Neumann entropy of the quantum state.

**Gold chunk text(s)**:
- **2606.20504::00028** _(section: A. Variational Quantum Algorithm (VQA) Approach)_:
  > Paper: Entropy Estimation in Multi-Qutrit Systems via Variational and Classical Neural Networks
Section: A. Variational Quantum Algorithm (VQA) Approach

The central idea is to learn a measurement basis in which the entropy can be inferred directly from classical measurement statistics. The variational circuit preserves the intrinsic entropy of the state and instead seeks a unitary transformation that approximately aligns the computational basis with the eigenbasis of the density matrix.

- **2606.20504::00034** _(section: A. Variational Quantum Algorithm (VQA) Approach)_:
  > Paper: Entropy Estimation in Multi-Qutrit Systems via Variational and Classical Neural Networks
Section: A. Variational Quantum Algorithm (VQA) Approach

The optimization therefore favors bases that produce maximally non-uniform outcomes. For a fixed state, this occurs when the measurement basis aligns with the eigenbasis of ρ , in which case p ( θ ) approximates the eigenvalue spectrum. The resulting measurement entropy then provides an estimate of the von Neumann entropy of the quantum state.


**Top-5 retrieved**:

### [1] 2606.20504::00034 GOLD HIT
_section: A. Variational Quantum Algorithm (VQA) Approach_

> Paper: Entropy Estimation in Multi-Qutrit Systems via Variational and Classical Neural Networks
Section: A. Variational Quantum Algorithm (VQA) Approach

The optimization therefore favors bases that produce maximally non-uniform outcomes. For a fixed state, this occurs when the measurement basis aligns with the eigenbasis of ρ , in which case p ( θ ) approximates the eigenvalue spectrum. The resulting measurement entropy then provides an estimate of the von Neumann entropy of the quantum state.

### [2] 2606.20504::00028 GOLD HIT
_section: A. Variational Quantum Algorithm (VQA) Approach_

> Paper: Entropy Estimation in Multi-Qutrit Systems via Variational and Classical Neural Networks
Section: A. Variational Quantum Algorithm (VQA) Approach

The central idea is to learn a measurement basis in which the entropy can be inferred directly from classical measurement statistics. The variational circuit preserves the intrinsic entropy of the state and instead seeks a unitary transformation that approximately aligns the computational basis with the eigenbasis of the density matrix.

### [3] 2606.20504::00027
_section: A. Variational Quantum Algorithm (VQA) Approach_

> Paper: Entropy Estimation in Multi-Qutrit Systems via Variational and Classical Neural Networks
Section: A. Variational Quantum Algorithm (VQA) Approach

We develop a variational framework for estimating the von Neumann entropy of multi-qutrit quantum states. While most prior variational approaches focus on qubit systems, extending these ideas to higher-dimensional settings introduces new challenges in circuit design and scalability.

### [4] 2606.20504::00038
_section: A. Variational Quantum Algorithm (VQA) Approach_

> Paper: Entropy Estimation in Multi-Qutrit Systems via Variational and Classical Neural Networks
Section: A. Variational Quantum Algorithm (VQA) Approach

2) Ansatz Design and Parameter Efficiency: A parameter study was conducted to quantify the effect of model capacity on entropy estimation accuracy. Using a fixed reference ansatz and a representative mixed quantum state, the number of trainable parameters was varied by increasing the number of circuit layers.

### [5] 2606.20504::00053
_section: A. Variational Quantum Algorithm (VQA) Approach_

> Paper: Entropy Estimation in Multi-Qutrit Systems via Variational and Classical Neural Networks
Section: A. Variational Quantum Algorithm (VQA) Approach

13

120 trainable parameters, while A8 and A10 contain 117. This controlled design enables systematic comparison of expressibility, parameter distribution, and entanglement structure.

---

## Q13: methodology

**Question**: How does FreeStyle train its style-content dual-reference generation model?

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=1.00 | CtxR=0.00 | Faith=0.00 | AnsCorr=0.14

**Gold chunk_ids**: ['2606.20506::00018']

**Gold answer**:
> They adopt a two-stage curriculum progressing from style-reference generation (Stage 1, trained on style-transfer data) to the harder dual-reference setting (Stage 2, mixing LoRA-mined triplets with style-transfer data). Each stage faces a distinct content-leakage mechanism and employs a corresponding disentanglement strategy: an attention-level enrichment constraint for Stage 1 and frequency-aware RoPE modulation for Stage 2.

**Gold chunk text(s)**:
- **2606.20506::00018** _(section: 3. Method Overview)_:
  > Paper: FreeStyle: Free Control of Style-Content Dual-Reference Generation from Community LoRA Mining
Section: 3. Method Overview

Training (§5). We adopt a two-stage curriculum progressing from style-reference generation (Stage 1, trained on styletransfer data) to the harder dual-reference setting (Stage 2, mixing LoRA-mined triplets with style-transfer data). Each stage faces a distinct content-leakage mechanism and employs a corresponding disentanglement strategy: an attentionlevel enrichment constraint (§5.1) for Stage 1 and frequencyaware RoPE modulation (§5.2) for Stage 2.


**Top-5 retrieved**:

### [1] 2606.20506::00001
_section: FreeStyle: Free Control for Style-Content Dual-Reference Generation from Community LoRA Mining_

> Paper: FreeStyle: Free Control of Style-Content Dual-Reference Generation from Community LoRA Mining
Section: FreeStyle: Free Control for Style-Content Dual-Reference Generation from Community LoRA Mining

Figure 1. Overview of FreeStyle . 1 We collect community-created style and content LoRAs from multiple platforms and automatically compose them through standardized workflows. 2 The resulting FreeStyle dataset contains diverse style-content image triplets spanning multiple base models, artistic styles, and subject categories. 3 FreeStyle enables both style transfer and style-subject controllable image generation across a broad range of visual domains.

### [2] 2606.20506::00039
_section: 5.1. Attention Constraint for Style-Reference Generation_

> Paper: FreeStyle: Free Control of Style-Content Dual-Reference Generation from Community LoRA Mining
Section: 5.1. Attention Constraint for Style-Reference Generation

Here E g = 1 means group g is attended to exactly in proportion to its size; E g > 1 indicates enrichment (the group draws more attention than its size warrants); and E g < 1 indicates suppression. Because the score factors out group size, it places groups of different sizes on equal footing while still resolving how attention shifts along both the denoising and depth axes.

### [3] 2606.20506::00092
_section: 8. Discussion and Conclusion_

> Paper: FreeStyle: Free Control of Style-Content Dual-Reference Generation from Community LoRA Mining
Section: 8. Discussion and Conclusion

Figure 6. Qualitative Comparison on Style-reference ( SRef ) Generation. Our model achieves faithful stylistic alignment while avoiding the structural artifacts and semantic leakage observed in competing baselines.

### [4] 2606.20506::00098
_section: 8. Discussion and Conclusion_

> Paper: FreeStyle: Free Control of Style-Content Dual-Reference Generation from Community LoRA Mining
Section: 8. Discussion and Conclusion

Table 4. Dataset Ablation on the SRef Benchmark . Both models use the same architecture and training setup; only the data source differs.

### [5] 2606.20506::00028
_section: 2. Generation of Rich and Effective Reference Images._

> Paper: FreeStyle: Free Control of Style-Content Dual-Reference Generation from Community LoRA Mining
Section: 2. Generation of Rich and Effective Reference Images.

Figure 3. Overview of the FreeStyle Data Construction Pipeline . 1 Single-LoRA Models Filtering. Community content and style LoRAs are collected and curated to build a high-quality LoRA repository. 2 Single-LoRA Results Filtering. Representative reference images are identified through metadata analysis and generation-based validation. 3 Dual-LoRA Pairs Filtering. Compatible content-style LoRA pairs are selected and combined to construct high-quality content-style triplets.

---

## Q14: methodology

**Question**: How does the ACE (Action-based Candidate Evidence) module work?

**Metrics**: R@5=1.00 | R@1=0.00 | MRR=0.50 | CtxP=1.00 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.92

**Gold chunk_ids**: ['2606.20561::00019']

**Gold answer**:
> ACE serves as the lightweight component of TIMEPROVE. Its objective is to transform a long video into a compact temporal action representation that can be leveraged to generate candidate answer hypotheses before invoking an expensive VLM. ACE consists of two submodules: (i) Action Detector, which performs a single pass over the video to temporally localize actions, and (ii) Query-conditioned Proposal Generator, which employs an edge LLM to reason over the localized actions and produce query-conditioned candidate answers along with corresponding evidence windows.

**Gold chunk text(s)**:
- **2606.20561::00019** _(section: 3.1 Action-based Candidate Evidence (ACE))_:
  > Paper: TimeProVe: Propose, then Verify for Efficient Long Video Temporal Reasoning in Activities of Daily Living
Section: 3.1 Action-based Candidate Evidence (ACE)

ACE serves as the lightweight component of TIMEPROVE. Its objective is to transform a long video into a compact temporal action representation that can be leveraged to generate candidate answer hypotheses before invoking an expensive VLM. ACE consists of two submodules: (i) Action Detector , which performs a single pass over the video to temporally localize actions, and (ii) Query- conditioned Proposal Generator , which employs an edge LLM to reason over the localized actions and produce query-conditioned candidate answers along with corresponding evidence windows.


**Top-5 retrieved**:

### [1] 2606.20561::00009
_section: 1 Introduction_

> Paper: TimeProVe: Propose, then Verify for Efficient Long Video Temporal Reasoning in Activities of Daily Living
Section: 1 Introduction

We design the Action-based Candidate Evidence (ACE) module, the first module of its kind to transform detected actions into query-conditioned answer-evidence candidates through lightweight LLM reasoning and structured reranking.

### [2] 2606.20561::00019 GOLD HIT
_section: 3.1 Action-based Candidate Evidence (ACE)_

> Paper: TimeProVe: Propose, then Verify for Efficient Long Video Temporal Reasoning in Activities of Daily Living
Section: 3.1 Action-based Candidate Evidence (ACE)

ACE serves as the lightweight component of TIMEPROVE. Its objective is to transform a long video into a compact temporal action representation that can be leveraged to generate candidate answer hypotheses before invoking an expensive VLM. ACE consists of two submodules: (i) Action Detector , which performs a single pass over the video to temporally localize actions, and (ii) Query- conditioned Proposal Generator , which employs an edge LLM to reason over the localized actions and produce query-conditioned candidate answers along with corresponding evidence windows.

### [3] 2606.20561::00142
_section: Local Action-based Candidate Evidence (ACE)_

> Paper: TimeProVe: Propose, then Verify for Efficient Long Video Temporal Reasoning in Activities of Daily Living
Section: Local Action-based Candidate Evidence (ACE)

Thus each question is paired with supporting intervals { [ s j , e j ] } m q j =1 . Some questions require a single localized event, while others require multiple intervals, such as verifying that one action occurs after another. These annotations are aimed to distinguish models that merely answer correctly from those that actually retrieve the relevant evidence.

### [4] 2606.20561::00126
_section: A TIMEPROVE's robustness to noisy Action Priors_

> Paper: TimeProVe: Propose, then Verify for Efficient Long Video Temporal Reasoning in Activities of Daily Living
Section: A TIMEPROVE's robustness to noisy Action Priors

Since TIMEPROVE uses the ACE module to construct candidate evidence windows from an action timeline, it is important to understand the sensitivity of the framework to imperfect action detection. We therefore evaluate TIMEPROVE under corrupted event timelines. Starting from the detected timeline A = { ( c i , s i , e i ) } N i =1 , we introduce two types of perturbations at increasing noise levels. For label noise , we randomly replace the action labels c i of a fraction p of events with labels sampled from the remaining action vocabulary, while keeping their temporal boundaries fixed. For boundary noise , we perturb each event boundary as ˜ s i = s i + ϵ s i and ˜ e i = e i + ϵ e i , where

### [5] 2606.20561::00018
_section: 3 Method_

> Paper: TimeProVe: Propose, then Verify for Efficient Long Video Temporal Reasoning in Activities of Daily Living
Section: 3 Method

Therefore, rather than processing the entire video or repeatedly invoking the VLM across many candidate temporal segments, our goal is to identify a small set of candidate windows W = { w k = [ s k , e k ] } K k =1 , where e k -s k ≪ L , and verify only the most promising evidence. Consequently, we propose the T ime-aware P roposal and V erification F ramework, TIMEPROVE, a cost-efficient framework for LVQA. As shown in Figure 2, TIMEPROVE consists of two main components: (i) an Action-based Candidate Evidence (ACE) Module , which operates over the full video using lightweight models to obtain query-conditioned candidate hypotheses, and (ii) a Temporal Verifier , which performs fine-grained verification only on short RGB clips selected by ACE. This design assigns broad temporal proposal generation to lightweight computation, reserving expensive VLM inference for targeted visual verification.

---

## Q15: table_numerical

**Question**: What is the ASR score when the Defender is SR Scout 30B and the Attacker is HB-FT-LLaMA 2-13B Attempts?

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=0.00 | AnsCorr=0.50

**Gold chunk_ids**: ['2606.20470::00078']

**Gold answer**:
> 0.165

**Gold chunk text(s)**:
- **2606.20470::00078** _(section: 5.5 ASR Evaluation & Comparison)_:
  > Paper: Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems
Section: 5.5 ASR Evaluation & Comparison

TABLE 3: Sample-averaged simulated ASR upper bound under the CMPE-based detect-and-misdirect strategy for N = 100 homogeneous i.i.d. attack attempts with K = 1 . For each prompt, ASR is computed using per-sample judge error estimates including γ A , and the table reports the average across all 500 prompts.

| Defender ↓ / Attacker →   | SR-OSS-120B   | SR-Scout-30B   | PAIR-OSS-120B   | HB-FT-LLaMA2-13B   | LLaMA-Guard-3-8B   | GPTFuzz-RoBERTa   |
|---------------------------|---------------|----------------|-----------------|--------------------|--------------------|-------------------|
| SR-OSS-120B               | 0 . 004       | 0 . 005        | 0 . 005         | 0 . 007            | 0 . 003            | 0 . 005           |
| SR-Scout-30B              | 0 . 124       | 0 . 049        | 0 . 094         | 0 . 165            | 0 . 074            | 0 . 084           |
| PAIR-OSS-120B             | 0 . 028       | 0 . 023        | 0 . 007         | 0 . 025            | 0 . 005            | 0 . 017           |
| HB-FT-LLaMA2-13B          | 0 . 077       | 0 . 064        | 0 . 052         | 0 . 001            | 0 . 046            | 0 . 039           |
| LLaMA-Guard-3-8B          | 0 . 098       | 0 . 075        | 0 . 063         | 0 . 126            | 0 . 000            | 0 . 039           |


**Top-5 retrieved**:

### [1] 2606.20470::00065
_section: 5.3 Judge Models_

> Paper: Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems
Section: 5.3 Judge Models

Classifier Judges: HB-FT-LLaMA2-13B (HarmBench Fine-Tuned) [28], GPTFuzz-RoBERTa [2], [10], and Llama-Guard-3-8B [29] are classifier-style judges used to detect harmful content or unsafe prompt-response behavior. GPTFuzz-RoBERTa also produces confidence scores p ∈ [0 , 1] , which we incorporate into normalized harmfulness scores.

### [2] 2606.20470::00072
_section: 5.5 ASR Evaluation & Comparison_

> Paper: Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems
Section: 5.5 ASR Evaluation & Comparison

Table 2 reports the detect-and-block baseline for N = 100 attacker attempts and verification budget K = 1 , where misdirection is absent and γ A = 0 . Table 3 reports the corresponding CMPE-based detect-and-misdirect case using the estimated misdirection-induced false-positive rates. The baseline results show high simulated ASR upper bounds across many attacker-defender configurations, with several values approaching 1 . In contrast, CMPE substantially reduces the estimated ASR upper bound across the same configurations, often by one to two orders of magnitude.

### [3] 2606.20470::00071
_section: 5.5 ASR Evaluation & Comparison_

> Paper: Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems
Section: 5.5 ASR Evaluation & Comparison

Using the per-sample judge error estimates from Section 5.4, we compute a simulated maximum ASR upper bound for each attacker-defender judge pair under the homogeneous i.i.d. special case of our analysis. For each of the 500 jailbreak prompts, we compute a per-sample ASR bound using the corresponding per-sample estimates of β D , β A according to (25) and, when applicable, γ A . We then average the resulting ASR values across all prompts. Therefore, the ASR values in Tables 2 and 3 are not obtained by directly substituting the aggregate error rates in Table 1; the aggregate rates are reported only to summarize judge behavior.

### [4] 2606.20470::00077
_section: 5.5 ASR Evaluation & Comparison_

> Paper: Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems
Section: 5.5 ASR Evaluation & Comparison

TABLE 2: Sample-averaged simulated ASR upper bound under the detect-and-block strategy for N = 100 homogeneous i.i.d. attack attempts with K = 1 . For each prompt, ASR is computed using per-sample judge error estimates with γ A = 0 , and the table reports the average across all 500 prompts.

### [5] 2606.20470::00079
_section: 5.5 ASR Evaluation & Comparison_

> Paper: Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems
Section: 5.5 ASR Evaluation & Comparison

TABLE 3: Sample-averaged simulated ASR upper bound under the CMPE-based detect-and-misdirect strategy for N = 100 homogeneous i.i.d. attack attempts with K = 1 . For each prompt, ASR is computed using per-sample judge error estimates including γ A , and the table reports the average across all 500 prompts.

---

## Q16: table_numerical

**Question**: In the Fast Human Attention Prediction paper on fixation-guided active perception, what is the time performance of the ResNet50 backbone?

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=1.00 | AnsCorr=0.06

**Gold chunk_ids**: ['2606.20491::00050']

**Gold answer**:
> 7.39 ms

**Gold chunk text(s)**:
- **2606.20491::00050** _(section: C. Backbone Ablations)_:
  > Paper: Fast Human Attention Prediction for Fixation-guided Active Perception in Autonomous Navigation
Section: C. Backbone Ablations

| Backbone              | ScanMatch ↑   |   Time (ms) ↓ |   #Params (M) ↓ |   GFLOPs ↓ |
|-----------------------|---------------|---------------|-----------------|------------|
| VGG19+DeepLabV3       | 0.47 (0.10)   |         17.43 |          195.41 |      99.81 |
| Resnet50+DeepLabV3    | 0.46 (0.10)   |         14.32 |            77.4 |       69.8 |
| MobilenetV3+DeepLabV3 | 0.48 (0.11)   |         13.80 |           57.25 |      62.07 |
| Resnet50              | 0.46 (0.11)   |          7.39 |           35.39 |       8.33 |
| MobilenetV3           | 0.47 (0.11)   |          6.84 |           15.24 |       0.61 |
| DINOv3                | 0.48 (0.11))  |         15.65 |           90.15 |      33.38 |
| DINOv3(VIT-S)         | 0.47 (0.11)   |         10.02 |           26.04 |       8.45 |
| DINOv3(VIT-S)*        | 0.48 (0.11)   |          8.76 |           31.35 |       8.49 |


**Top-5 retrieved**:

### [1] 2606.20491::00053
_section: C. Backbone Ablations_

> Paper: Fast Human Attention Prediction for Fixation-guided Active Perception in Autonomous Navigation
Section: C. Backbone Ablations

Overall, all backbones achieve similar performance on the ScanMatch score, while the major difference is in computational cost. The backbone variants without DeeplabV3 provide less inference time and reduced computational costs. Among all evaluated backbones, MobileNetV3 is the most efficient in terms of computational cost and inference speed, as it is specifically designed for mobile and embedded devices [28]. Therefore, MobileNetV3 is selected as the backbone for our model.

### [2] 2606.20491::00046
_section: C. Backbone Ablations_

> Paper: Fast Human Attention Prediction for Fixation-guided Active Perception in Autonomous Navigation
Section: C. Backbone Ablations

We evaluate the impact of the feature extraction backbone by comparing different alternative architectures. Specifically, we begin with the backbone configuration used in tSPMNet [12], which combines VGG19 with a DeepLabV3 [40] segmentation module. We first replace VGG19 [41] with ResNet50 as it has shown better perfomance with reduced computational costs [42], and with MobileNetV3 [28] to obtain a more lightweight variant. In addition, we examine the effect of removing the DeepLabV3 module to further reduce the complexity of the model.

### [3] 2606.20491::00052
_section: C. Backbone Ablations_

> Paper: Fast Human Attention Prediction for Fixation-guided Active Perception in Autonomous Navigation
Section: C. Backbone Ablations

Table II summarizes the comparison between the abovementioned backbone variants in terms of performance (ScanMatch score) and computational costs. The ScanMatch metric is chosen as it is a widely used metric in the literature [10], [12], [30], [38]. The rest of the model is kept unchanged across all comparisons.

### [4] 2606.20491::00048
_section: C. Backbone Ablations_

> Paper: Fast Human Attention Prediction for Fixation-guided Active Perception in Autonomous Navigation
Section: C. Backbone Ablations

For all the above-mentioned backbones, the pretrained models were finetuned during training on the OSIE dataset, except for (a) all DINOv3 backbones which were frozen, and (b) the first half of VGG19 which was frozen as described in [12]. For the model variants using DeepLabV3, the extracted segmentation masks are concatenated with the BACKBONE COMPARISON: PERFORMANCE VS. COMPUTATIONAL COST.

### [5] 2606.20491::00021
_section: Liquid Neural Network (CfC)_

> Paper: Fast Human Attention Prediction for Fixation-guided Active Perception in Autonomous Navigation
Section: Liquid Neural Network (CfC)

where σ ( · ) denotes the sigmoid activation, and ∆ t represents the elapsed time between fixations obtained from the groundtruth fixation durations.

---

## Q17: table_numerical

**Question**: What is the accuracy of the uniform sampling method in the efficiency-comparison table for TimeProVe against LVQA baselines?

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=1.00 | AnsCorr=0.44

**Gold chunk_ids**: ['2606.20561::00055']

**Gold answer**:
> 34.7

**Gold chunk text(s)**:
- **2606.20561::00055** _(section: 5.3 System Diagnosis)_:
  > Paper: TimeProVe: Propose, then Verify for Efficient Long Video Temporal Reasoning in Activities of Daily Living
Section: 5.3 System Diagnosis

| Method           |   Acc. |   # Calls |   Dur. |   Lat. |
|------------------|--------|-----------|--------|--------|
| Caption-Based    |   24.7 |      16.8 | 1004.8 |   55.0 |
| Uniform Sampling |   34.7 |      16.8 | 1004.8 |   27.0 |
| Full-Video       |   35.0 |       1.0 |  180.0 |   17.6 |
| Retrieval-Based  |   33.9 |       7.0 |   10.0 |   35.0 |
| TIMEPROVE        |   44.8 |       8.3 |  123.6 |   18.7 |


**Top-5 retrieved**:

### [1] 2606.20561::00051
_section: 5.3 System Diagnosis_

> Paper: TimeProVe: Propose, then Verify for Efficient Long Video Temporal Reasoning in Activities of Daily Living
Section: 5.3 System Diagnosis

Efficiency Analysis. Table 3 highlights the accuracy-efficiency tradeoff among LVQA methods. Caption-based and uniform-sampling methods process much longer video duration through repeated VLM calls, yet remain less accurate. In contrast, full-video inference has low latency but its comparable accuracy shows that exposing the VLM to more video frames does not necessarily yield better reasoning when evidence is sparse. Retrieval-based selection is efficient in processed duration, but its low performance suggests that generic retrieval often misses action-relevant evidence. In contrast, TIMEPROVE achieves the best accuracy with minimal latency overhead, because ACE narrows the search before VLM verification. This shows that the key efficiency gain is not merely reducing calls or duration in isolation, but selecting clips that are likely to contain the answer.

### [2] 2606.20561::00054
_section: 5.3 System Diagnosis_

> Paper: TimeProVe: Propose, then Verify for Efficient Long Video Temporal Reasoning in Activities of Daily Living
Section: 5.3 System Diagnosis

Table 3: Efficiency comparison of TIMEPROVE with LVQA baselines.

### [3] 2606.20561::00042
_section: 4 OPENTSUBENCH (OTB)_

> Paper: TimeProVe: Propose, then Verify for Efficient Long Video Temporal Reasoning in Activities of Daily Living
Section: 4 OPENTSUBENCH (OTB)

LVQA is most useful when a model can not only answer a question, but also identify the temporal evidence that supports the answer. This requirement is especially important for ADL, where the relevant evidence may occupy only a few seconds within a long, visually redundant recording. Existing LVQA benchmarks often emphasize multiplechoice evaluation, report aggregate accuracy without diagnostic breakdowns, or omit precise temporal evidence. As a result, they make it difficult to evaluate whether a model is genuinely grounded or merely producing the right answer from language priors or dataset biases.

### [4] 2606.20561::00059
_section: 5.4 Generalization to Temporal Grounding_

> Paper: TimeProVe: Propose, then Verify for Efficient Long Video Temporal Reasoning in Activities of Daily Living
Section: 5.4 Generalization to Temporal Grounding

Although TIMEPROVE is specifically designed for open-ended LVQA, its intermediate representation, i.e., localized evidence window from ACE, is inherently temporal. This makes it natural to ask whether the same mechanism can transfer to temporal grounding, where the task is to localize the interval corresponding to a language query. We evaluate this on Charades-STA in Table 4. Comple- mentary to LVQA, Charades-STA evaluates short, free-form temporal grounding rather than openended reasoning over long ADL videos. Accordingly, TIMEPROVE with only the Action Detector is limited at stricter IoU thresholds, since action detectors provide event-level segments rather than the fine boundary alignment required by temporal grounding. Nevertheless, this variant remains competitive with several general video-language grounding models, suggesting that action timelines provide useful temporal structure even beyond the target LVQA setting. Notably, while strong baselines such as TimeSuite and Time-R1 achieve competitive performance on CHARADES-STA, they substantially underperform on OTB, highlighting the challenges posed by temporally grounded reasoning in long ADL videos.

### [5] 2606.20561::00048
_section: 5.2 Comparison with State-of-the-Art_

> Paper: TimeProVe: Propose, then Verify for Efficient Long Video Temporal Reasoning in Activities of Daily Living
Section: 5.2 Comparison with State-of-the-Art

In Table 1, we compare TIMEPROVE with two families of methods, supervised fine-tuned (SFT) VLMs and agentic VLM-based frameworks. Among SFT-based methods, VideoLLaMA3 achieves the lowest performance, while temporal grounding models such as TimeChat, VTimeLLM, Time-R1, and TimeSuite improve performance on specific categories through timeaware instruction tuning but remain limited overall. Interestingly, TIMEPROVE with VLMA3 as the verifier achieves stronger overall performance. Using Gemma4-2B in ACE, TIMEPROVE achieves an improvement of 14 . 7% over the baseline with the same VLMA3 as Temporal Verifier. With Qwen27B in ACE, TIMEPROVE achieves further improvement of 5 . 4% , with gains across temporal positioning, compositional actions, and long-horizon sparse evidence.

---

## Q18: equation

**Question**: What is the proposed loss equation for Gaussian splatting in VisDom?

**Metrics**: R@5=1.00 | R@1=1.00 | MRR=1.00 | CtxP=1.00 | CtxR=0.25 | Faith=1.00 | AnsCorr=0.92

**Gold chunk_ids**: ['2606.20531::00027', '2606.20531::00028']

**Gold answer**:
> The proposed loss is L_ours = L_base + λ_2 L_mask + λ_3 L_i (Equation 2), where L_base is the 3DGS-GO base loss, L_mask is the binary cross-entropy loss between the given and rendered masks, and L_i = -(1 - M_i) log(1 - M̂_i) is a visibility penalty that penalizes Gaussians appearing opaque in regions outside the visual hull when rendered from interpolated camera views (with masks M_i obtained by rendering the visual hull from these novel views).

**Gold chunk text(s)**:
- **2606.20531::00027** _(section: 4.3 VisDom Constraint for Sparse NVS)_:
  > Paper: VisDom: Sparse Novel View Synthesis with Visible Domain Constraint
Section: 4.3 VisDom Constraint for Sparse NVS

Gaussian Splatting Gaussian splatting [9] (3DGS) is a 3D scene representation based on 3D Gaussian learned per scene. As the representation is explicit, bounding the near and far planes, as with NeRFs, is no longer an option. However, we use our visible domain-constrained visual hull to regularize 3DGS in two ways. Firstly, we initialize the 3DGS reconstruction, similar to existing works [17,29], with the visual hull obtained with the algorithm as described in section 4.2. Secondly, we interpolate between the camera poses of the training set and enforce a visibility constraint on the new views. As discussed in section 4.1, we can identify 3D regions where Gaussians are not expected due to the visual hull. Therefore, we enforce the mask loss on unoccupied pixels in the unseen views, refining the reconstruction by adjusting the Gaussians' opacities. This ensures that the reconstructed Gaussians are inside our visual domain-constrained visual hull. The proposed loss looks as follows

L ours = L base + λ 2 L mask + λ 3 L i , (2)

- **2606.20531::00028** _(section: 4.3 VisDom Constraint for Sparse NVS)_:
  > Paper: VisDom: Sparse Novel View Synthesis with Visible Domain Constraint
Section: 4.3 VisDom Constraint for Sparse NVS

where L i = -(1 -M i ) log(1 -ˆ M i ) penalizes Gaussians that appear opaque in regions outside the visual hull when rendered from interpolated camera views. Here, masks M i are obtained by rendering our visual hull from these novel views. L base and L mask are the loss of the base method (3DGS-GO) and the binary cross-entropy loss between the given and the rendered masks, respectively.


**Top-5 retrieved**:

### [1] 2606.20531::00027 GOLD HIT
_section: 4.3 VisDom Constraint for Sparse NVS_

> Paper: VisDom: Sparse Novel View Synthesis with Visible Domain Constraint
Section: 4.3 VisDom Constraint for Sparse NVS

Gaussian Splatting Gaussian splatting [9] (3DGS) is a 3D scene representation based on 3D Gaussian learned per scene. As the representation is explicit, bounding the near and far planes, as with NeRFs, is no longer an option. However, we use our visible domain-constrained visual hull to regularize 3DGS in two ways. Firstly, we initialize the 3DGS reconstruction, similar to existing works [17,29], with the visual hull obtained with the algorithm as described in section 4.2. Secondly, we interpolate between the camera poses of the training set and enforce a visibility constraint on the new views. As discussed in section 4.1, we can identify 3D regions where Gaussians are not expected due to the visual hull. Therefore, we enforce the mask loss on unoccupied pixels in the unseen views, refining the reconstruction by adjusting the Gaussians' opacities. This ensures that the reconstructed Gaussians are inside our visual domain-constrained visual hull. The proposed loss looks as follows

L ours = L base + λ 2 L mask + λ 3 L i , (2)

### [2] 2606.20531::00091
_section: A.2 Gaussian Splatting_

> Paper: VisDom: Sparse Novel View Synthesis with Visible Domain Constraint
Section: A.2 Gaussian Splatting

3D Gaussian Splatting (3DGS) [9] is a real-time neural rendering technique that represents a 3D scene using Gaussian primitives comprising properties such as position µ , opacity α , covariance Σ , and color c . Unlike NeRFs [18], which rely on volumetric sampling and expensive ray marching, 3DGS directly projects and renders Gaussians in a differentiable way using alpha compositing (given a pixel p in eq. (4)), enabling fast and high-quality reconstruction. In this work, we deal with the final rendered image ˆ C and the rendered alpha channel w i ,

ˆ C ( p ) = ∑ i w i c i , where w i = α i i -1 ∏ j =1 (1 -α j ) . (4)

### [3] 2606.20531::00024
_section: 4.3 VisDom Constraint for Sparse NVS_

> Paper: VisDom: Sparse Novel View Synthesis with Visible Domain Constraint
Section: 4.3 VisDom Constraint for Sparse NVS

We propose to regularize reconstruction methods using a robust version of the visual hull. For readers unfamiliar with the underlying representations, we provide concise overviews of NeRFs [18] and 3D Gaussian Splatting (3DGS) [9] in the supplementary material.

### [4] 2606.20531::00077
_section: References_

> Paper: VisDom: Sparse Novel View Synthesis with Visible Domain Constraint
Section: References

Wu, J., Li, R., Zhu, Y., Guo, R., Sun, J., Zhang, Y.: Sparse2dgs: Geometryprioritized gaussian splatting for surface reconstruction from sparse views. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 1130711316 (2025)

### [5] 2606.20531::00061
_section: References_

> Paper: VisDom: Sparse Novel View Synthesis with Visible Domain Constraint
Section: References

Kerbl, B., Kopanas, G., Leimk¨ uhler, T., Drettakis, G.: 3d gaussian splatting for real-time radiance field rendering. ACM Transactions on Graphics 42 (4) (July 2023), https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/

---

## Q19: equation

**Question**: What is the equation for cross-batch accumulation?

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=1.00 | CtxR=1.00 | Faith=0.50 | AnsCorr=0.14

**Gold chunk_ids**: ['2606.20475::00043', '2606.20475::00044']

**Gold answer**:
> Cross-batch accumulation aggregates multiple marginal advantages δ_{k,t} of the same op across multiple batches into a stable accumulation quantity, using exponential moving average (EMA) as the default accumulation operator in recursive form: m_{k,t} = β m_{k,t-1} + (1 - β) δ_{k,t}, m̂_{k,t} = m_{k,t} / (1 - β^{t_k}) (Equation 5), where t_k is the cumulative number of updates op k has participated in and the denominator (1 - β^{t_k}) is the bias correction term.

**Gold chunk text(s)**:
- **2606.20475::00043** _(section: 3.3.1 Accumulation Operator and EMA Instance)_:
  > Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 3.3.1 Accumulation Operator and EMA Instance

Cross-batch accumulation aggregates multiple marginal advantages 𝛿 𝑘,𝑡 of the same op across multiple batches (the differential signal of op 𝑘 at step 𝑡 ) into a stable accumulation quantity, allowing positive and negative evidence to cancel and consistent directions to be amplified. We choose exponential moving average (EMA) as the default accumulation operator, with the recursive form:

𝑚 𝑘,𝑡 = 𝛽 𝑚 𝑘,𝑡 -1 + ( 1 -𝛽 ) 𝛿 𝑘,𝑡 , ˆ 𝑚 𝑘,𝑡 = 𝑚 𝑘,𝑡 1 -𝛽 𝑡 𝑘 (5)

- **2606.20475::00044** _(section: 3.3.1 Accumulation Operator and EMA Instance)_:
  > Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 3.3.1 Accumulation Operator and EMA Instance

where 𝑡 𝑘 is the cumulative number of updates op 𝑘 has participated in, and the denominator is the bias correction term. When 𝛿 𝑘,𝜏 signs are consistent across different batches, the magnitude of the accumulation quantity grows with steps; when signs alternate, positive-negative cancellation causes the accumulation quantity to trend toward zero. EMA simultaneously smooths residual amplitude noise from differencing, and through exponential weighting causes recent consistent-direction evidence to quickly dominate the accumulation quantity, accelerating ranking convergence.


**Top-5 retrieved**:

### [1] 2606.20475::00009
_section: 1.2 Design Gaps in Batch-Style Trace Distillation_

> Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 1.2 Design Gaps in Batch-Style Trace Distillation

Cross-batch comparability (Comparability) : Different batches have varying task distributions; the signals produced by the same operation across batches must share a consistent scale to enable meaningful additive accumulation. If signals are dominated by batch-specific characteristics rather than the true effect of the operation, cross-batch aggregation becomes meaningless.

### [2] 2606.20475::00053
_section: 4.1 Research Questions_

> Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 4.1 Research Questions

RQ2: Layer-by-layer ablation of cross-batch accumulation signals. Through stepwise ablation from Reactive Update to Abs-score EMA, Counting𝛿 EMA, and finally Continuous𝛿 EMA, we sequentially verify the necessity of cross-batch accumulation, the irreplaceability of differential construction, and the additional gains of continuous amplitude for ranking.

### [3] 2606.20475::00008
_section: 1.2 Design Gaps in Batch-Style Trace Distillation_

> Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 1.2 Design Gaps in Batch-Style Trace Distillation

Cross-batch identity alignment (Alignability) : The system must be able to identify semantically equivalent operations across different batches and merge them into the same accumulation unit. Without stable tracking of the same operation, cross-batch evidence accumulation is impossible.

### [4] 2606.20475::00010
_section: 1.2 Design Gaps in Batch-Style Trace Distillation_

> Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 1.2 Design Gaps in Batch-Style Trace Distillation

These two requirements reveal the fundamental distinction between step-local edit selection (ordinal selection on the current batch) and cross-batch edit accumulation (stateful evidence aggregation across batches): ranking or preference signals suffice for the former but cannot support the latter due to the absence of the above two properties. No existing method provides a design layer satisfying both requirements, and this deficiency worsens with increasing task complexity-when task distribution differences are large and trajectories are long, the value of cross-batch evidence accumulation becomes particularly significant.

### [5] 2606.20475::00007
_section: 1.2 Design Gaps in Batch-Style Trace Distillation_

> Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 1.2 Design Gaps in Batch-Style Trace Distillation

The essence of the problem is that existing methods lack a cross-batch evidence accumulation mechanism. To fill this design gap, an accumulation mechanism must satisfy two structural requirements:

---

## Q20: contribution_recall

**Question**: What research questions does the Marginal Advantage Accumulation (MAA) paper focus on?

**Metrics**: R@5=1.00 | R@1=1.00 | MRR=1.00 | CtxP=1.00 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.95

**Gold chunk_ids**: ['2606.20475::00052', '2606.20475::00053', '2606.20475::00054', '2606.20475::00055']

**Gold answer**:
> Four research questions: RQ1 end-to-end effectiveness of MAA against baselines under same data split and inference budget; RQ2 layer-by-layer ablation of cross-batch accumulation signals from Reactive Update to Abs-score EMA, Counting-δ EMA, and Continuous-δ EMA; RQ3 sign mechanism diagnosis of whether the direction of differential δ is consistent under perturbation and aligned with true rollout gain; RQ4 diagnostic analysis of whether reactive update degenerates in long-term training and whether MAA's evidence cancellation mechanism is functioning.

**Gold chunk text(s)**:
- **2606.20475::00052** _(section: 4.1 Research Questions)_:
  > Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 4.1 Research Questions

RQ1: End-to-end effectiveness. Does the complete MAA bring stable task benefits compared to the frozen (no memory) baseline, single-shot distillation, reactive update, offline distillation method Trace2Skill, and online method SkillOpt, under the same data split, same outer validation protocol, and similar inference budget?

- **2606.20475::00053** _(section: 4.1 Research Questions)_:
  > Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 4.1 Research Questions

RQ2: Layer-by-layer ablation of cross-batch accumulation signals. Through stepwise ablation from Reactive Update to Abs-score EMA, Counting𝛿 EMA, and finally Continuous𝛿 EMA, we sequentially verify the necessity of cross-batch accumulation, the irreplaceability of differential construction, and the additional gains of continuous amplitude for ranking.

- **2606.20475::00054** _(section: 4.1 Research Questions)_:
  > Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 4.1 Research Questions

RQ3: Sign mechanism diagnosis. Is the direction of differential 𝛿 highly consistent under perturbation despite limited robustness of differential amplitude 𝛿 , and is the alignment with the true rollout gain direction significantly above chance?

- **2606.20475::00055** _(section: 4.1 Research Questions)_:
  > Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 4.1 Research Questions

RQ4: Diagnostic analysis. Doesreactive update degenerate in long-term training due to accumulating harmful ops? Is MAA's evidence cancellation mechanism actually functioning?


**Top-5 retrieved**:

### [1] 2606.20475::00052 GOLD HIT
_section: 4.1 Research Questions_

> Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 4.1 Research Questions

RQ1: End-to-end effectiveness. Does the complete MAA bring stable task benefits compared to the frozen (no memory) baseline, single-shot distillation, reactive update, offline distillation method Trace2Skill, and online method SkillOpt, under the same data split, same outer validation protocol, and similar inference budget?

### [2] 2606.20475::00055 GOLD HIT
_section: 4.1 Research Questions_

> Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 4.1 Research Questions

RQ4: Diagnostic analysis. Doesreactive update degenerate in long-term training due to accumulating harmful ops? Is MAA's evidence cancellation mechanism actually functioning?

### [3] 2606.20475::00051
_section: 4.1 Research Questions_

> Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 4.1 Research Questions

Experiments in this section revolve around four research questions.

### [4] 2606.20475::00053 GOLD HIT
_section: 4.1 Research Questions_

> Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 4.1 Research Questions

RQ2: Layer-by-layer ablation of cross-batch accumulation signals. Through stepwise ablation from Reactive Update to Abs-score EMA, Counting𝛿 EMA, and finally Continuous𝛿 EMA, we sequentially verify the necessity of cross-batch accumulation, the irreplaceability of differential construction, and the additional gains of continuous amplitude for ranking.

### [5] 2606.20475::00054 GOLD HIT
_section: 4.1 Research Questions_

> Paper: Marginal Advantage Accumulation for Memory-Driven Agent Self-Evolution
Section: 4.1 Research Questions

RQ3: Sign mechanism diagnosis. Is the direction of differential 𝛿 highly consistent under perturbation despite limited robustness of differential amplitude 𝛿 , and is the alignment with the true rollout gain direction significantly above chance?

---

## Q21: contribution_recall

**Question**: What are the contributions of the Fisher-Geometric Sharpness paper on SGD implicit bias toward flat minima?

**Metrics**: R@5=1.00 | R@1=1.00 | MRR=1.00 | CtxP=1.00 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.97

**Gold chunk_ids**: ['2606.20469::00007', '2606.20469::00008', '2606.20469::00009', '2606.20469::00010']

**Gold answer**:
> The paper defines Riemannian sharpness on the statistical manifold and shows its invariance under reparametrization (Lemma 1); derives the local stationary distribution of the mini-batch SGD SDE and proves that it assigns exponentially greater mass to Riemannian-flat minima (Theorem 1, Corollary 1); establishes a PAC-Bayes generalization bound explicitly controlled by Riemannian sharpness (Corollary 2); and provides empirical validation on MNIST and CIFAR-10 confirming that Riemannian sharpness tracks generalization across optimizers, batch sizes, and learning rates in ways that Euclidean sharpness does not.

**Gold chunk text(s)**:
- **2606.20469::00007** _(section: Contributions)_:
  > Paper: Fisher-Geometric Sharpness and the Implicit Bias of SGD toward Flat Minima
Section: Contributions

We have defined Riemannian sharpness on the statistical manifold and showed its invariance under reparametrization (Lemma 1), attempting to resolve the fundamental critique of Dinh et al. [2017].

We are explicit about the gap between the theoretical invariance of S R (which holds for the true FIM) and its empirical estimator (which is not exactly invariant; see Section 6.5).

- **2606.20469::00008** _(section: Contributions)_:
  > Paper: Fisher-Geometric Sharpness and the Implicit Bias of SGD toward Flat Minima
Section: Contributions

We have derived the local stationary distribution of the mini-batch SGD SDE and then proved that it assigns exponentially greater mass to Riemannian-flat minima (Theorem 1, Corollary 1).

We have established a PAC-Bayes generalization bound that is explicitly controlled by Riemannian sharpness (Corollary 2) which formally links flatness to test performance.

- **2606.20469::00009** _(section: Contributions)_:
  > Paper: Fisher-Geometric Sharpness and the Implicit Bias of SGD toward Flat Minima
Section: Contributions

We have provided empirical validation on MNIST and CIFAR-10, confirming that Riemannian sharpness tracks generalization across optimizers, batch sizes, and learning rates in ways that Euclidean sharpness does not.

- **2606.20469::00010** _(section: Contributions)_:
  > Paper: Fisher-Geometric Sharpness and the Implicit Bias of SGD toward Flat Minima
Section: Contributions

Unlike prior work Jang et al. [2022], Kristiadi et al. [2023] which establishes reparametrization invariance in isolation, this work is the first to unify invariant sharpness with the SGD stationary distribution and a PAC-Bayes generalization bound in a single framework.


**Top-5 retrieved**:

### [1] 2606.20469::00007 GOLD HIT
_section: Contributions_

> Paper: Fisher-Geometric Sharpness and the Implicit Bias of SGD toward Flat Minima
Section: Contributions

We have defined Riemannian sharpness on the statistical manifold and showed its invariance under reparametrization (Lemma 1), attempting to resolve the fundamental critique of Dinh et al. [2017].

We are explicit about the gap between the theoretical invariance of S R (which holds for the true FIM) and its empirical estimator (which is not exactly invariant; see Section 6.5).

### [2] 2606.20469::00009 GOLD HIT
_section: Contributions_

> Paper: Fisher-Geometric Sharpness and the Implicit Bias of SGD toward Flat Minima
Section: Contributions

We have provided empirical validation on MNIST and CIFAR-10, confirming that Riemannian sharpness tracks generalization across optimizers, batch sizes, and learning rates in ways that Euclidean sharpness does not.

### [3] 2606.20469::00008 GOLD HIT
_section: Contributions_

> Paper: Fisher-Geometric Sharpness and the Implicit Bias of SGD toward Flat Minima
Section: Contributions

We have derived the local stationary distribution of the mini-batch SGD SDE and then proved that it assigns exponentially greater mass to Riemannian-flat minima (Theorem 1, Corollary 1).

We have established a PAC-Bayes generalization bound that is explicitly controlled by Riemannian sharpness (Corollary 2) which formally links flatness to test performance.

### [4] 2606.20469::00010 GOLD HIT
_section: Contributions_

> Paper: Fisher-Geometric Sharpness and the Implicit Bias of SGD toward Flat Minima
Section: Contributions

Unlike prior work Jang et al. [2022], Kristiadi et al. [2023] which establishes reparametrization invariance in isolation, this work is the first to unify invariant sharpness with the SGD stationary distribution and a PAC-Bayes generalization bound in a single framework.

### [5] 2606.20469::00164
_section: References_

> Paper: Fisher-Geometric Sharpness and the Implicit Bias of SGD toward Flat Minima
Section: References

S. Nacson, K. Ravikumar, N. Srebro, and D. Soudry. Implicit bias of SGD for diagonal linear networks: A provable benefit of stochasticity. In Advances in Neural Information Processing Systems (NeurIPS) , 2022.

---

## Q22: contribution_recall

**Question**: What are the contributions of the Efficient and Sound Probabilistic Verification for AI Agents paper?

**Metrics**: R@5=1.00 | R@1=0.00 | MRR=0.25 | CtxP=0.48 | CtxR=0.75 | Faith=1.00 | AnsCorr=0.32

**Gold chunk_ids**: ['2606.20510::00010', '2606.20510::00012', '2606.20510::00013', '2606.20510::00014']

**Gold answer**:
> The contributions are: (1) identifying security risks in deterministic verification engines in ambiguous agent environments and introducing a model for probabilistic verification; (2) modeling multi-step agent trajectories via Datalog derivation graphs and formalizing the computation of worst-case policy violation risk as an exact LP; (3) introducing a polynomially-sized SDP relaxation that tracks second-order moments to efficiently approximate risk at runtime, with a formal proof of soundness as a strict upper bound on execution risk; and (4) evaluating the framework across terminal agent benchmarks, demonstrating that the relaxation effectively balances the security-utility tradeoff with low computational overhead.

**Gold chunk text(s)**:
- **2606.20510::00010** _(section: 1. Introduction)_:
  > Paper: Efficient and Sound Probabilistic Verification for AI Agents
Section: 1. Introduction

We identify security risks in deterministic verification engines in ambiguous agent environments and introduce a model for probabilistic verification.

We model multi-step agent trajectories via Datalog derivation graphs and formalize the compu-

- **2606.20510::00012** _(section: 1. Introduction)_:
  > Paper: Efficient and Sound Probabilistic Verification for AI Agents
Section: 1. Introduction

tation of worst-case policy violation risk as an exact LP.

- **2606.20510::00013** _(section: 1. Introduction)_:
  > Paper: Efficient and Sound Probabilistic Verification for AI Agents
Section: 1. Introduction

Weintroduce a polynomially-sized SDP relaxation that tracks second-order moments to efficiently approximate risk at runtime, and we formally prove its soundness as a strict upper bound on execution risk.

- **2606.20510::00014** _(section: 1. Introduction)_:
  > Paper: Efficient and Sound Probabilistic Verification for AI Agents
Section: 1. Introduction

Weevaluate our framework across terminal agent benchmarks, demonstrating that our relaxation effectively balances the security-utility tradeoff with low computational overhead.


**Top-5 retrieved**:

### [1] 2606.20510::00009
_section: 1. Introduction_

> Paper: Efficient and Sound Probabilistic Verification for AI Agents
Section: 1. Introduction

In summary, our key contributions are as follows:

### [2] 2606.20510::00056
_section: 3.3. Compiling Datalog Trajectories to a DAG_

> Paper: Efficient and Sound Probabilistic Verification for AI Agents
Section: 3.3. Compiling Datalog Trajectories to a DAG

Data merging. Next, the agent combines the contents of b.txt and the redacted intermediate file, representing a Merge transition:

### [3] 2606.20510::00001
_section: Efficient and Sound Probabilistic Verification for AI Agents_

> Paper: Efficient and Sound Probabilistic Verification for AI Agents
Section: Efficient and Sound Probabilistic Verification for AI Agents

Securing AI agents that operate in complex digital environments has become a critical need, and runtime monitoring approaches that formulate and enforce policies expressed in a formal language like Datalog offer a promising solution. However, existing approaches are restricted to deterministic policies. In many practical applications of AI agents, there is a need to enforce security policies in the face of ambiguity, leading to probabilistic predicates or state transitions (for example, a declassifier or Personally Identifiable Information (PII) detector that has some failure probability on each invocation). Furthermore, in many such applications, one cannot easily make the independence assumptions necessary to invoke prior work on probabilistic inference in Datalog. We address this by introducing a sound and efficient framework for such verification based on distributionally robust optimization, computing sound upper bounds on the probability of policy violation regardless of possible correlations between predicates. On standard benchmarks for terminal and tool calling agents, we demonstrate that our approach outperforms prior art and improves the security-utility trade-off while ensuring rigorous bounds on the probability of policy violation.

### [4] 2606.20510::00014 GOLD HIT
_section: 1. Introduction_

> Paper: Efficient and Sound Probabilistic Verification for AI Agents
Section: 1. Introduction

Weevaluate our framework across terminal agent benchmarks, demonstrating that our relaxation effectively balances the security-utility tradeoff with low computational overhead.

### [5] 2606.20510::00100
_section: 5.1. Benchmarks_

> Paper: Efficient and Sound Probabilistic Verification for AI Agents
Section: 5.1. Benchmarks

We evaluated our framework across a diverse suite of agentic safety and probabilistic logic programming tasks designed to test scalability, multi-turn security enforcement, and resilience to correlated inputs.

---

## Q23: negative_no_answer

**Question**: Does this paper discuss anything about agentic AI?

**Metrics**: R@5=n/a | R@1=n/a | MRR=n/a | CtxP=0.00 | CtxR=0.00 | Faith=1.00 | AnsCorr=0.17

**Gold chunk_ids**: []

**Gold answer**:
> No, this paper does not discuss agentic AI. It is about 3D editing in real images.

**Gold chunk text(s)**:
(intentionally empty - negative_no_answer)

**Top-5 retrieved**:

### [1] 2606.20470::00008
_section: 1 INTRODUCTION_

> Paper: Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems
Section: 1 INTRODUCTION

Section 7 situates this work relative to recent activedefense approaches. Section 8 concludes the paper by discussing deployment implications and future directions for integrating misdirection into agentic security architectures. Overall, the paper contributes a probabilistic analysis of model-guided attack dynamics, a detect-and-misdirect defense strategy that bounds attacker success by degrading automated evaluation, and a practical CMPE instantiation validated through both judge-based ASR simulations and end-to-end attack-framework experiments. These results support a defense perspective in which limiting the quality of attacker feedback can be as important as blocking malicious outputs in autonomous AI systems.

### [2] 2606.20470::00000
_section: Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems_

> Paper: Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems
Section: Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems

Reza Soosahabi, Vivek Namsani Application & Threat Intelligence Research Center Keysight Technologies Inc., USA

✦

### [3] 2606.20470::00054
_section: 4 CONTEXTUAL MISDIRECTION VIA PROGRESSIVE ENGAGEMENT AGAINST JAILBREAK ATTACKS_

> Paper: Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems
Section: 4 CONTEXTUAL MISDIRECTION VIA PROGRESSIVE ENGAGEMENT AGAINST JAILBREAK ATTACKS

6: w ← SHUFFLE ( w )

7: ˜ p ← JOIN ( w )

### [4] 2606.20470::00055
_section: 4 CONTEXTUAL MISDIRECTION VIA PROGRESSIVE ENGAGEMENT AGAINST JAILBREAK ATTACKS_

> Paper: Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems
Section: 4 CONTEXTUAL MISDIRECTION VIA PROGRESSIVE ENGAGEMENT AGAINST JAILBREAK ATTACKS

8:

s

ctx

←

M

(

expand text

,

˜

p, N

e

)

▷

expand to

≈

N

e

words

9:

(3) Follow-up question

### [5] 2606.20512::00121
_section: 8 Discussion_

> Paper: Probe-and-Refine Tuning of Repository Guidance for Coding Agents
Section: 8 Discussion

Instruction quality as a first-order variable. The central claim of this paper is that the quality of the instructions given to a coding agent is a first-order determinant of its reliability, comparable in magnitude to choices about model capability or step budget within a fixed scaffold. This reframes a question that has received surprisingly little systematic attention: while models, context windows, and scaffolds have all been subject to careful ablation, the content of the agent's own instructions has rarely been varied or optimized. Guidance does not improve the quality of the changes the agent makes (precision is constant at ∼ 59%), but, as the budget experiment shows (Section 6), it is what makes additional steps productive at all. The 42 % of instances resistant to all three conditions at the any-trial threshold are unlikely to be reached by guidance improvements alone; these appear to require stronger reasoning or longer context rather than better localization.

---

## Q24: vague_ambiguous

**Question**: Tell me about image editing.

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=1.00 | CtxR=0.25 | Faith=0.00 | AnsCorr=0.09

**Gold chunk_ids**: ['2606.20556::00003', '2606.20556::00004']

**Gold answer**:
> The paper introduces 'Thinking in Boxes', a system for 3D editing in real images. The user specifies an edit by placing a 3D box around an object in the input image and a second box where they want the object to end up; a learned procedure maps this pair of boxes into the internal representation of a generator, producing the edited image. The same procedure handles translation, rotation, occlusion, and viewpoint changes and is learned once for all manipulations, not retrained or optimized per image. To ground transformations in scene appearance, the method introduces a depth-aligned planar floor as a global reference frame.

**Gold chunk text(s)**:
- **2606.20556::00003** _(section: Source Image Abstract)_:
  > Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: Source Image Abstract

Rotation Scaling Rotation Large 3D Transformations Source Primitive Text and 2D-conditioning interfaces provide weak, ambiguous control over spatial transformations in image editing - particularly under large object motions and camera changes. Prior work has used 3D primitives such as boxes, but only as loose conditioning signals indicating approximate object location rather than specifying the transformation. We instead use 3D boxes as structured specifications: the user provides the input and output boxes of the edit, casting editing as a well-posed geometry problem. This 'thinking in boxes' interface, where each box face is colorcoded to convey 3D orientation, gives precise control over translation, rotation, scaling, and viewpoint changes in real images while preserving scene and object identity, and recovering previously unseen object regions. To ground transformations in scene appearance, we introduce a depth-aligned planar floor as a global reference frame, shaded with depth-aware cues. Conditioned on this structure, an image generator produces consistent results under large transformations. Trained in two stages - on synthetic multi-object scenes and a small set of real-world videos from Objectron - the system generalizes to complex, in-the-wild real images. Our method operates directly on real photographs and substantially outperforms recent state-of-the-art methods on large 3D edits.

- **2606.20556::00004** _(section: 1 Introduction)_:
  > Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: 1 Introduction

We present a system that lets a user manipulate a simple, abstracted representation of the objects in an image, and turns those manipulations into edits of the image itself. The user specifies an edit by placing a 3D box around an object in the input image and a second box where they want the object to end up; a learned procedure maps this pair of boxes into the internal representation of a generator, producing the edited image. The same procedure handles translation, rotation, occlusion, and viewpoint changes and is learned once for all manipulations - not retrained or optimized per image.


**Top-5 retrieved**:

### [1] 2606.20556::00062
_section: References_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: References

Omri Avrahami, Or Patashnik, Ohad Fried, Egor Nemchinov, Kfir Aberman, Dani Lischinski, and Daniel Cohen-Or. Stable flow: Vital layers for training-free image editing. In Proceedings of the Computer Vision and Pattern Recognition Conference , pages 7877-7888, 2025.

### [2] 2606.20556::00084
_section: References_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: References

Ziqi Jiang, Zhen Wang, and Long Chen. Clipdrag: Combining text-based and drag-based instructions for image editing. In International Conference on Learning Representations , volume 2025, pages 5237-5253, 2025.

### [3] 2606.20556::00093
_section: References_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: References

Oscar Michel, Anand Bhattad, Eli VanderBilt, Ranjay Krishna, Aniruddha Kembhavi, and Tanmay Gupta. Object 3dit: Language-guided 3d-aware image editing. Advances in Neural Information Processing Systems , 36:3497-3516, 2023.

### [4] 2606.20556::00094
_section: References_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: References

Oscar Michel, Anand Bhattad, Eli VanderBilt, Ranjay Krishna, Aniruddha Kembhavi, and Tanmay Gupta. Object 3dit: Language-guided 3d-aware image editing. Advances in Neural Information Processing Systems , 36:3497-3516, 2023.

### [5] 2606.20556::00121
_section: References_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: References

Yicheng Xiao, Wenhu Zhang, Lin Song, Yukang Chen, Wenbo Li, Nan Jiang, Tianhe Ren, Haokun Lin, Wei Huang, Haoyang Huang, et al. Spatialedit: Benchmarking fine-grained image spatial editing. arXiv preprint arXiv:2604.04911 , 2026.

---

## Q25: multi_hop

**Question**: Which related-work itemwas shared in this paper that discusses lottery, and what does it say?

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=0.58 | CtxR=0.00 | Faith=0.00 | AnsCorr=0.05

**Gold chunk_ids**: ['2606.20536::00017']

**Gold answer**:
> The lottery-ticket hypothesis (Frankle & Carbin) is referenced in the 'Why runs differ' related-work subsection. It is invoked, alongside the loss-landscape view of Fort et al., to argue that stochastic gradient descent visits a discretely diverse set of basins, amplified by initialisation, batch order, and adaptive optimisers.

**Gold chunk text(s)**:
- **2606.20536::00017** _(section: 2 Related Work)_:
  > Paper: The FID Lottery: Quantifying Hidden Randomness in Generative-Model Evaluation
Section: 2 Related Work

Why runs differ. The lottery-ticket hypothesis [30, 31] and the loss-landscape view of Fort et al. [29] argue that the stochastic gradient descent visits a discretely diverse set of basins, amplified by initialisation [32, 35], batch order, and adaptive optimisers [53]. Architectures [36, 93, 23] change basin geometry but not multiplicity. Nagarajan and Kolter [69] formalise why these gaps are intrinsic, while Wenzel et al. [95], Jordan [45] exploit them for uncertainty quantification. Zhang et al. [99] show diffusion models are unusually well-behaved at the function level. We add that near-identical noise-to-image maps still yield percent-level FID fluctuations.


**Top-5 retrieved**:

### [1] 2606.20536::00168
_section: C Companion summary tables_

> Paper: The FID Lottery: Quantifying Hidden Randomness in Generative-Model Evaluation
Section: C Companion summary tables

The figures of the main paper carry the qualitative argument. The three tables below consolidate the headline numbers behind them so they can be looked up in one place.

### [2] 2606.20536::00067
_section: References_

> Paper: The FID Lottery: Quantifying Hidden Randomness in Generative-Model Evaluation
Section: References

Shane Barratt and Rishi Sharma. A note on the inception score. arXiv preprint arXiv:1801.01973 , 2018.

### [3] 2606.20536::00130
_section: References_

> Paper: The FID Lottery: Quantifying Hidden Randomness in Generative-Model Evaluation
Section: References

Edward Raff. A step toward quantifying independently reproducible machine learning research. In Advances in Neural Information Processing Systems 32 (NeurIPS) , 2019.

### [4] 2606.20508::00012
_section: 2. Related Work_

> Paper: What Do Safety-Aligned LLMs Learn From Mixed Compliance Demonstrations?
Section: 2. Related Work

Mechanistic and Bayesian accounts of context-induced behavior change. Several recent papers provide mechanistic and theoretical accounts of ICL that motivate our hypotheses. Xie et al. (2022) explain ICL as implicit Bayesian inference over a latent concept shared across the prompt, while Hendel et al. (2023) argue that ICL often compresses demonstrations into a query-agnostic task vector. On the behavior-control side, Choi & Li (2024) show that in-context examples can steer high-level personas, and Bigelow et al. (2025) propose a unifying Bayesian account in which incontext examples accumulate evidence over latent concepts while activation steering shifts priors. Our paper operationalizes this perspective in the safety domain: we test whether benign and harmful compliance demonstrations accumulate along a single 'comply' dimension or along more specific latent beliefs about whether harmful requests should be answered.

### [5] 2606.20502::00014
_section: I. INTRODUCTION_

> Paper: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software
Section: I. INTRODUCTION

The paper is structured as follows: §II reviews related work; §III presents methodology; §IV details setup; §V-§VII analyze results; §VIII discusses implications; §IX states threats; and §X concludes.

---

## Q26: comparison_contrast

**Question**: What is the difference between identity-level effects and attribute-level effects on bias in MLLMs?

**Metrics**: R@5=0.00 | R@1=0.00 | MRR=0.00 | CtxP=0.95 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.91

**Gold chunk_ids**: ['2606.20527::00038', '2606.20527::00041']

**Gold answer**:
> Identity-level effects are dominated by age and body type; attribute-level effects are dominated by fashion style and other visual cues. About 15 attributes account for ~80% of total variation.

**Gold chunk text(s)**:
- **2606.20527::00038** _(section: 5.1 RQ1: How do MLLMs' social perceptions vary across specific visual dimensions?)_:
  > Paper: StylisticBias: A Few Human Visual Cues Drive Most Social Biases in MLLMs
Section: 5.1 RQ1: How do MLLMs' social perceptions vary across specific visual dimensions?

Body type and age show the strongest demographic effects on social judgment, though demographic dimensions differ substantially in their influence. Table 2 reports VS across all six models. Body type ( VS = 0 . 069 ) and age ( VS = 0 . 075 ) show the largest between-group differences in preference scores, with significant effects in 76% and 78% of scenarios on average (Appendix D.1). By contrast, ethnicity ( VS = 0 . 038 ) and gender ( 0 . 030 ) show substantially smaller effects, and ethnicity reaches significance in only 44% of scenarios for LLaVA-v1.6 and Qwen3, challenging the assumption that demographic signals are uniformly salient across architectures. LLaVA-v1.6 shows the most pronounced imbalance: 96% of body type comparisons are significant, yet only 44% of ethnicity comparisons are. Importantly, these disparities are present in the base faces before any stylistic variation is applied, confirming that demographic differences constitute an independent source of bias in model judgments. Body type and age correspond most closely to competence-related judgments in the warmth-competence framework (Fiske, 2018), consistent with greater model sensitivity to appearance cues that are culturally linked to social status. One-way ANOVAs confirm this hierarchy: age ( η 2 p =0 . 214 ) and body type ( η 2 p =0 . 207 ) show large effects, while gender ( η 2 p =0 . 013 ) and ethnicity ( η 2 p =0 . 018 , ns) are substantially smaller (Appendix D.2, Table 10).

- **2606.20527::00041** _(section: 5.2 RQ2: Which visual attributes most strongly influence these judgments?)_:
  > Paper: StylisticBias: A Few Human Visual Cues Drive Most Social Biases in MLLMs
Section: 5.2 RQ2: Which visual attributes most strongly influence these judgments?

A small subset of visual cues accounts for nearly all aggregate bias. Table 3 shows a strongly uneven distribution of SBS across attribute categories. Fashion ( +0 . 046 ), Facial hair ( +0 . 042 ), Makeup & lips ( +0 . 037 ), and Eyewear ( +0 . 035 ) produce the largest positive SBS. Hair style ( -0 . 023 to -0 . 024 ) and Skin irregularities ( -0 . 019 to -0 . 021 ) yield consistently negative SBS across all demographic dimensions. No significant effects are detected for accessories. Piercings show near-zero aggregate SBS, though subgroup analysis reveals gender-dependent sign reversals discussed below. Figure 2 confirms that approximately 15 attributes account for nearly 80% of total | SBS | . The strongest effects largely correspond to cues interpreted as deliberate self-presentation signals rather than unchosen biological features, consistent with prior work (Zebrowitz and Montepare, 2008; Cassidy et al., 2012).


**Top-5 retrieved**:

### [1] 2606.20527::00001
_section: Abstract_

> Paper: StylisticBias: A Few Human Visual Cues Drive Most Social Biases in MLLMs
Section: Abstract

Multimodal large language models (MLLMs) are increasingly deployed in personally and societally consequential settings, yet the visual cues that shape how these models judge people remain poorly understood. Prior work often compares different (groups of) individuals, making it difficult to separate appearance effects from identity differences. We introduce StylisticBias, a controlled benchmark for evaluating attribute-level social bias in MLLMs. We generate 500 photorealistic base faces and create about 50 single-attribute variations per face, producing about 25K images. This design keeps identity fixed and changes one visual attribute at a time. It lets us measure how specific cues shift model judgments. We evaluate six MLLMs across 25 binary social judgment scenarios. We find that age and body type dominate identity-level effects, while fashion style and other visual cues drive the largest attribute-level shifts. We further find that about 15 attributes account for nearly 80% of the total variation, showing that bias is concentrated in a small set of visual cues. Sensitivity is strongest in judgments that are semantically aligned with appearance, especially socioeconomic and style-related judgments. We release StylisticBias as a benchmark for fine-grained bias evaluation in multimodal models. Code and dataset: github.com/timo-cavelius/ StylisticBias , hf.co/datasets/ shaghayegh/stylistic-bias-dataset .

### [2] 2606.20527::00059
_section: Conclusion_

> Paper: StylisticBias: A Few Human Visual Cues Drive Most Social Biases in MLLMs
Section: Conclusion

We introduced StylisticBias , a controlled benchmark for evaluating attribute-level social bias in multimodal large language models (MLLMs) by keeping identity fixed and varying one visual attribute at a time. Across six MLLMs and 25 social judgment scenarios, we find that bias is not spread uniformly across appearance categories, but concentrated in a relatively small set of visual cues, especially self-presentation cues such as fashion, facial hair, and makeup. These effects are strongest in judgments that are semantically aligned with visible appearance, particularly socioeconomic and style-related judgments. More broadly, our results show that MLLMs are systematically sensitive to how a person looks, not just to who the person is represented as being. By moving beyond coarse demographic comparisons toward controlled visual attribution, StylisticBias provides a benchmark for fine-grained bias evaluation and a foundation for future auditing and mitigation of appearance-driven bias in multimodal systems.

### [3] 2606.20527::00057
_section: Models share a common bias structure but differ in effect magnitude._

> Paper: StylisticBias: A Few Human Visual Cues Drive Most Social Biases in MLLMs
Section: Models share a common bias structure but differ in effect magnitude.

Table 5: Per-model variation effects. SBS and Cohen's d are face-level estimates.

Figure 5: Gemma-3 vs. Gemma-4 mean ∆ per scenario, colored by judgment category ( r = 0 . 75 , slope = 0 . 39 ).

### [4] 2606.20527::00042
_section: 5.2 RQ2: Which visual attributes most strongly influence these judgments?_

> Paper: StylisticBias: A Few Human Visual Cues Drive Most Social Biases in MLLMs
Section: 5.2 RQ2: Which visual attributes most strongly influence these judgments?

Note that clothing variations use full-body portraits rather than the head-and-shoulders framing used for all other attributes (Appendix B.3). Fashion effects should be interpreted with this difference in visual context in mind.

### [5] 2606.20527::00054
_section: 5.3 RQ3: How do these effects vary across models and social-judgment scenarios?_

> Paper: StylisticBias: A Few Human Visual Cues Drive Most Social Biases in MLLMs
Section: 5.3 RQ3: How do these effects vary across models and social-judgment scenarios?

Figure 4: Mean SBS ( x -axis) vs. mean | SBS | ( y -axis) for each of the 25 scenarios, with bootstrap 95% CI (face-level).

---

## Q27: comparison_contrast

**Question**: What is the difference between using egocentric human video and teleoperated real-robot trajectories for embodied model pretraining?

**Metrics**: R@5=1.00 | R@1=0.00 | MRR=0.33 | CtxP=1.00 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.37

**Gold chunk_ids**: ['2606.20521::00002']

**Gold answer**:
> Egocentric human video, when processed through a carefully designed filtering and labeling pipeline, achieves 24% lower validation loss and 52.5% / 90% higher success rates on in-distribution / out-of-distribution real-robot task execution compared to teleoperated real-robot data, at substantially lower cost and higher diversity.

**Gold chunk text(s)**:
- **2606.20521::00002** _(section: Abstract)_:
  > Paper: HumanScale: Egocentric Human Video Can Outperform Real-Robot Data for Embodied Pretraining
Section: Abstract

Embodied foundation models are expected to benefit from data scaling like large language models, but face a much tighter data bottleneck. Teleoperated real-robot trajectories remain the dominant pretraining source due to their precise action supervision and embodiment alignment, yet their scalability is limited by high collection cost, acquisition difficulty, and low behavioral and environmental diversity. These limitations have sparked interest in egocentric human video as a scalable, substantially lower-cost, and more diverse alternative for embodied model pretraining. However, its effectiveness compared to teleoperated real-robot data remains underexplored. To address this question, we conduct a systematic study comparing egocentric human video and teleoperated real-robot trajectories as pretraining data sources for embodied foundation models, under fixed post-training and validation protocols. Surprisingly, we find that egocentric data, when processed through a carefully designed filtering and labeling pipeline, is not merely a viable substitute for model pretraining but can lead to superior performance. With the same amount of pretraining data, models pretrained on egocentric data achieve a 24% lower validation loss on real-robot action prediction, as well as 52.5% and 90% higher success rates on in-distribution and out-of-distribution real-robot task execution, respectively. This finding verifies a scalable paradigm for embodied foundation models: pretrain on egocentric human video to learn diverse world representations, then adapt with a small amount of labeled real-robot data for action-space alignment. We hope this study encourages broader exploration of egocentric data and offers guidance for data quality assessment before costly robot data collection. Code will be released at https://github.com/DAGroup-PKU/HumanNet/ .


**Top-5 retrieved**:

### [1] 2606.20521::00043
_section: 4.2 Egocentric Pretraining Generalizes Better than Robot Pretraining_

> Paper: HumanScale: Egocentric Human Video Can Outperform Real-Robot Data for Embodied Pretraining
Section: 4.2 Egocentric Pretraining Generalizes Better than Robot Pretraining

Diversity and information density. As analyzed in Section 2, egocentric data is intrinsically more diverse and covers a far wider range of tasks, objects, and backgrounds than teleoperated robot data, which is collected in a bounded set of laboratory setups. Matching the two sources by hours further understates this advantage, since an hour of egocentric video contains far more and cleaner trajectories than an hour of robot teleoperation. In our 100-hour recipe, for instance, the egocentric data comprises roughly 45,000 trajectories, whereas the real-robot data contains only about 8,000, as teleoperation is slowed by long idle intervals and the comparatively slow motion of the robot arm. Each hour of teleoperated data therefore carries substantially less information and offers little advantage as a pretraining source.

### [2] 2606.20521::00004
_section: Egocentric video pretraining leads to better generalization than robot data pretraining._

> Paper: HumanScale: Egocentric Human Video Can Outperform Real-Robot Data for Embodied Pretraining
Section: Egocentric video pretraining leads to better generalization than robot data pretraining.

Figure 1 Egocentric human video leads to stronger generalization than robot data for embodied pretraining. Left: Egocentric human video offers massive accessible scale ( ∼ 10 6 hours), low collection cost, and open-world diversity, but provides only pseudo action labels from human hand retargeting. Teleoperated robot data provides precise action labels yet is limited in scale ( ∼ 10 4 public hours), costly to collect, and limited scene diversity. Middle: We compare egocentric video pretraining with real robot data pretraining using the same world-action model (WAM). Both pretrained models are post-trained on the same real-robot dataset and evaluated on both seen and unseen AgiBot tasks. Right: On out-of-distribution evaluations, egocentric pretraining exhibits clear scaling behavior, while real-robot pretraining saturates earlier. Real-world rollouts further show that ego-pretrained policies maintain high success rates under unseen-object shifts, whereas the no-pretraining baseline collapses.

### [3] 2606.20521::00002 GOLD HIT
_section: Abstract_

> Paper: HumanScale: Egocentric Human Video Can Outperform Real-Robot Data for Embodied Pretraining
Section: Abstract

Embodied foundation models are expected to benefit from data scaling like large language models, but face a much tighter data bottleneck. Teleoperated real-robot trajectories remain the dominant pretraining source due to their precise action supervision and embodiment alignment, yet their scalability is limited by high collection cost, acquisition difficulty, and low behavioral and environmental diversity. These limitations have sparked interest in egocentric human video as a scalable, substantially lower-cost, and more diverse alternative for embodied model pretraining. However, its effectiveness compared to teleoperated real-robot data remains underexplored. To address this question, we conduct a systematic study comparing egocentric human video and teleoperated real-robot trajectories as pretraining data sources for embodied foundation models, under fixed post-training and validation protocols. Surprisingly, we find that egocentric data, when processed through a carefully designed filtering and labeling pipeline, is not merely a viable substitute for model pretraining but can lead to superior performance. With the same amount of pretraining data, models pretrained on egocentric data achieve a 24% lower validation loss on real-robot action prediction, as well as 52.5% and 90% higher success rates on in-distribution and out-of-distribution real-robot task execution, respectively. This finding verifies a scalable paradigm for embodied foundation models: pretrain on egocentric human video to learn diverse world representations, then adapt with a small amount of labeled real-robot data for action-space alignment. We hope this study encourages broader exploration of egocentric data and offers guidance for data quality assessment before costly robot data collection. Code will be released at https://github.com/DAGroup-PKU/HumanNet/ .

### [4] 2606.20521::00011
_section: Egocentric video pretraining leads to better generalization than robot data pretraining._

> Paper: HumanScale: Egocentric Human Video Can Outperform Real-Robot Data for Embodied Pretraining
Section: Egocentric video pretraining leads to better generalization than robot data pretraining.

Egocentric pretraining improves downstream generalization over real-robot pretraining. At matched scale and under the same pretraining-post-training protocol, egocentric pretraining achieves stronger performance than real-robot pretraining, with the largest gains on unseen tasks.

### [5] 2606.20521::00009
_section: Egocentric video pretraining leads to better generalization than robot data pretraining._

> Paper: HumanScale: Egocentric Human Video Can Outperform Real-Robot Data for Embodied Pretraining
Section: Egocentric video pretraining leads to better generalization than robot data pretraining.

Egocentric pretraining scales consistently. As the amount of egocentric pretraining data increases from

---

## Q28: comparison_contrast

**Question**: What is the difference between LCB and Multi-LCB?

**Metrics**: R@5=1.00 | R@1=1.00 | MRR=1.00 | CtxP=0.87 | CtxR=1.00 | Faith=0.83 | AnsCorr=0.71

**Gold chunk_ids**: ['2606.20517::00002', '2606.20517::00003']

**Gold answer**:
> LCB evaluates LLM code generation on Python only; Multi-LCB extends LCB to 12 programming languages while preserving its contamination controls and evaluation protocol.

**Gold chunk text(s)**:
- **2606.20517::00002** _(section: ABSTRACT)_:
  > Paper: Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages
Section: ABSTRACT

LiveCodeBench (LCB) has recently become a widely adopted benchmark for evaluating large language models (LLMs) on code-generation tasks. By curating competitive programming problems, constantly adding fresh problems to the set, and filtering them by release dates, LCB provides contamination-aware evaluation and offers a holistic view of coding capability. However, LCB remains restricted to Python, leaving open the question of whether LLMs can generalize across the diverse programming languages required in real-world software engineering.

- **2606.20517::00003** _(section: ABSTRACT)_:
  > Paper: Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages
Section: ABSTRACT

We introduce Multi-LCB, a benchmark for evaluating LLMs across twelve programming languages, including Python. Multi-LCB transforms Python tasks from the LCB dataset into equivalent tasks in other languages while preserving LCB's contamination controls and evaluation protocol. Because it is fully compatible with the original LCB format, Multi-LCB will automatically track future LCB updates, enabling systematic assessment of cross-language code generation competence and requiring models to sustain performance well beyond Python.


**Top-5 retrieved**:

### [1] 2606.20517::00003 GOLD HIT
_section: ABSTRACT_

> Paper: Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages
Section: ABSTRACT

We introduce Multi-LCB, a benchmark for evaluating LLMs across twelve programming languages, including Python. Multi-LCB transforms Python tasks from the LCB dataset into equivalent tasks in other languages while preserving LCB's contamination controls and evaluation protocol. Because it is fully compatible with the original LCB format, Multi-LCB will automatically track future LCB updates, enabling systematic assessment of cross-language code generation competence and requiring models to sustain performance well beyond Python.

### [2] 2606.20517::00002 GOLD HIT
_section: ABSTRACT_

> Paper: Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages
Section: ABSTRACT

LiveCodeBench (LCB) has recently become a widely adopted benchmark for evaluating large language models (LLMs) on code-generation tasks. By curating competitive programming problems, constantly adding fresh problems to the set, and filtering them by release dates, LCB provides contamination-aware evaluation and offers a holistic view of coding capability. However, LCB remains restricted to Python, leaving open the question of whether LLMs can generalize across the diverse programming languages required in real-world software engineering.

### [3] 2606.20517::00022
_section: 3 BENCHMARK DESIGN_

> Paper: Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages
Section: 3 BENCHMARK DESIGN

This section describes the approach, used to construct the Multi-LCB benchmark. Figure 1 illustrates the full pipeline. Please note, that although Multi-LCB is built on LCB, the same approach can be applied to any dataset with a comparable structure.

### [4] 2606.20517::00165
_section: F.3 PERFORMANCE ON THE MULTI-LCB (JUL 2024-MAY 2025 SUBSET)_

> Paper: Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages
Section: F.3 PERFORMANCE ON THE MULTI-LCB (JUL 2024-MAY 2025 SUBSET)

Table 13: Performance results on Multi-LCB tasks from July 2024 till May 2025. Scores represent the Pass@1 (%) metric (higher is better). (* - reasoning mode)

### [5] 2606.20517::00024
_section: 3 BENCHMARK DESIGN_

> Paper: Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages
Section: 3 BENCHMARK DESIGN

To construct Multi-LCB, we load the desired version of the LCB code generation dataset from Hugging Face, retrieving Python problems and their metadata. We convert every release of LCB code generation dataset without modification, preserving all tasks from three competitive-programming platforms: LeetCode, AtCoder, and Codeforces. Each task includes a natural language description, input/output examples, and contest release date for contamination-aware filtering. Test conversion is applied only to LeetCode's functional format tasks to ensure unified STDIN/STDOUT evaluation. Details about platforms and temporal distribution appear in the Appendix D.1.

---

## Q29: cross_paper

**Question**: How do JanusMesh and Thinking in Boxes differ in what they take as input and what they produce as output?

**Metrics**: R@5=1.00 | R@1=0.00 | MRR=0.33 | CtxP=0.00 | CtxR=0.00 | Faith=0.67 | AnsCorr=0.16

**Gold chunk_ids**: ['2606.20563::00002', '2606.20556::00003', '2606.20556::00004']

**Gold answer**:
> JanusMesh takes text prompts and outputs a 3D mesh that reveals different semantics from different viewing angles. Thinking in Boxes takes a real photograph plus 3D bounding boxes (specifying input and output object positions, with color-coded faces for orientation) and outputs an edited 2D image with the transformed objects.

**Gold chunk text(s)**:
- **2606.20563::00002** _(section: JanusMesh: Fast and Zero-Shot 3D Visual Illusion Generation via Cross-Space Denoising)_:
  > Paper: JanusMesh: Fast and Zero-Shot 3D Visual Illusion Generation via Cross-Space Denoising
Section: JanusMesh: Fast and Zero-Shot 3D Visual Illusion Generation via Cross-Space Denoising

Abstract. Creating 3D visual illusions, a single 3D mesh that reveals entirely different semantics from various viewing angles, is a fascinating but tough challenge. Existing optimization-based methods are slow and can produce oversaturated colors. In contrast, naive stitching approaches fail to produce geometrically coherent objects. This results in visible unnatural seams and semantic leaks. In this paper, we present a fast and training-free framework for generating text-driven 3D visual illusions. Our approach decouples the generation into two stages. First, we propose a cross-space dual-branch denoising process. This process dynamically decodes 3D latents into voxel space for CLIP-guided orientation alignment and Signed Distance Field (SDF) blending, which ensures seamless geometric fusion. Second, we introduce a view-conditioned texture synthesis module that projects and aggregates view-specific 2D diffusion priors onto the fused geometry. Extensive experiments demonstrate that our method generates highly realistic, dual-semantic 3D illusions in just 3-5 minutes. It significantly outperforms existing methods in geometric integrity, semantic recognizability, and efficiency. Project page: https://siang1105.github.io/JanusMesh.github.io/

- **2606.20556::00003** _(section: Source Image Abstract)_:
  > Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: Source Image Abstract

Rotation Scaling Rotation Large 3D Transformations Source Primitive Text and 2D-conditioning interfaces provide weak, ambiguous control over spatial transformations in image editing - particularly under large object motions and camera changes. Prior work has used 3D primitives such as boxes, but only as loose conditioning signals indicating approximate object location rather than specifying the transformation. We instead use 3D boxes as structured specifications: the user provides the input and output boxes of the edit, casting editing as a well-posed geometry problem. This 'thinking in boxes' interface, where each box face is colorcoded to convey 3D orientation, gives precise control over translation, rotation, scaling, and viewpoint changes in real images while preserving scene and object identity, and recovering previously unseen object regions. To ground transformations in scene appearance, we introduce a depth-aligned planar floor as a global reference frame, shaded with depth-aware cues. Conditioned on this structure, an image generator produces consistent results under large transformations. Trained in two stages - on synthetic multi-object scenes and a small set of real-world videos from Objectron - the system generalizes to complex, in-the-wild real images. Our method operates directly on real photographs and substantially outperforms recent state-of-the-art methods on large 3D edits.

- **2606.20556::00004** _(section: 1 Introduction)_:
  > Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: 1 Introduction

We present a system that lets a user manipulate a simple, abstracted representation of the objects in an image, and turns those manipulations into edits of the image itself. The user specifies an edit by placing a 3D box around an object in the input image and a second box where they want the object to end up; a learned procedure maps this pair of boxes into the internal representation of a generator, producing the edited image. The same procedure handles translation, rotation, occlusion, and viewpoint changes and is learned once for all manipulations - not retrained or optimized per image.


**Top-5 retrieved**:

### [1] 2606.20556::00165
_section: E User Study Setup_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: E User Study Setup

Figure 21: Participants are shown the input image, source and target 3D layouts, and two candidate edited outputs (A and B). They are asked to select the output that best preserves the edited object's appearance and identity (e.g., foreground, background details) with respect to the original input image. Example questions with explanations are provided to familiarize participants with the evaluation protocol.

### [2] 2606.20556::00016
_section: 3 Method_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: 3 Method

Scene layout. The input to our method - a set of boxes in two configurations - has to tell the generator unambiguously what edit to perform. The mapping from the source configuration to the target configuration must have a single interpretation. Boxes alone do not satisfy this: a leftward shift of every box can equally indicate that the objects moved left or that the camera panned right, and the generator has no way to choose. We resolve the ambiguity by anchoring the boxes in a

### [3] 2606.20556::00004 GOLD HIT
_section: 1 Introduction_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: 1 Introduction

We present a system that lets a user manipulate a simple, abstracted representation of the objects in an image, and turns those manipulations into edits of the image itself. The user specifies an edit by placing a 3D box around an object in the input image and a second box where they want the object to end up; a learned procedure maps this pair of boxes into the internal representation of a generator, producing the edited image. The same procedure handles translation, rotation, occlusion, and viewpoint changes and is learned once for all manipulations - not retrained or optimized per image.

### [4] 2606.20556::00018
_section: 3 Method_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: 3 Method

Noise shared coordinate frame - a depth-aligned planar floor, rendered as a checkerboard with depth-aware shading. The floor moves with the camera and stays fixed under object motion, so any change in the relative configuration of boxes and floor uniquely identifies what moved. It also provides a global reference for contact and shadow. Both boxes and the floor form the 3D scene layout L src , which we project to 2D as the spatial conditioning image used by the generator Fitting boxes to images. The user fits boxes to objects through a point-and-click interface (Fig. 2). The floor is estimated automatically from the image, so the user only specifies object boxes - they never author the floor explicitly. To reduce manual effort further, off-the-shelf 3D box detectors [26] produce an initial set of boxes that the user refines.

### [5] 2606.20560::00123
_section: 7.3. Replicating and Extending Chain-of-Thought Work on DiffusionGemma_

> Paper: How Transparent is DiffusionGemma?
Section: 7.3. Replicating and Extending Chain-of-Thought Work on DiffusionGemma

There has been significant effort on understanding how understandable, faithful, controllable, and monitorable long chains of thought in autoregressive transformer language models are. One could imagine replicating this work for the outputs of DiffusionGemma, both for a single canvas and across multiple canvases. For instance:

---

## Q30: cross_paper

**Question**: What 3D representations do JanusMesh and Thinking in Boxes use, and how do they differ?

**Metrics**: R@5=1.00 | R@1=0.00 | MRR=0.50 | CtxP=0.75 | CtxR=0.00 | Faith=1.00 | AnsCorr=0.18

**Gold chunk_ids**: ['2606.20563::00002', '2606.20563::00008', '2606.20556::00003', '2606.20556::00005']

**Gold answer**:
> JanusMesh uses a 3D mesh with cross-space denoising across voxel space and Signed Distance Field (SDF) blending for geometric fusion. Thinking in Boxes uses 3D bounding boxes as structured specifications (with color-coded faces for orientation) and a depth-aligned planar floor as a global reference frame; it operates on 2D images, not 3D meshes.

**Gold chunk text(s)**:
- **2606.20563::00002** _(section: JanusMesh: Fast and Zero-Shot 3D Visual Illusion Generation via Cross-Space Denoising)_:
  > Paper: JanusMesh: Fast and Zero-Shot 3D Visual Illusion Generation via Cross-Space Denoising
Section: JanusMesh: Fast and Zero-Shot 3D Visual Illusion Generation via Cross-Space Denoising

Abstract. Creating 3D visual illusions, a single 3D mesh that reveals entirely different semantics from various viewing angles, is a fascinating but tough challenge. Existing optimization-based methods are slow and can produce oversaturated colors. In contrast, naive stitching approaches fail to produce geometrically coherent objects. This results in visible unnatural seams and semantic leaks. In this paper, we present a fast and training-free framework for generating text-driven 3D visual illusions. Our approach decouples the generation into two stages. First, we propose a cross-space dual-branch denoising process. This process dynamically decodes 3D latents into voxel space for CLIP-guided orientation alignment and Signed Distance Field (SDF) blending, which ensures seamless geometric fusion. Second, we introduce a view-conditioned texture synthesis module that projects and aggregates view-specific 2D diffusion priors onto the fused geometry. Extensive experiments demonstrate that our method generates highly realistic, dual-semantic 3D illusions in just 3-5 minutes. It significantly outperforms existing methods in geometric integrity, semantic recognizability, and efficiency. Project page: https://siang1105.github.io/JanusMesh.github.io/

- **2606.20563::00008** _(section: 1 Introduction)_:
  > Paper: JanusMesh: Fast and Zero-Shot 3D Visual Illusion Generation via Cross-Space Denoising
Section: 1 Introduction

We present a zero-shot two-stage framework that generates coherent 3D visual illusions in 3-5 minutes. Stage 1 employs a dual-branch denoising process using TRELLIS [73], decoding latents into voxel space at each step, aligning objects via CLIP-guided orientation search, and merging them via SDF blending before re-encoding. Stage 2 performs view-conditioned texturing by projecting Stable Diffusion predictions onto the fused mesh. Our method demonstrates superior geometry coherence, texture realism, and semantic recognizability over existing baselines.

- **2606.20556::00003** _(section: Source Image Abstract)_:
  > Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: Source Image Abstract

Rotation Scaling Rotation Large 3D Transformations Source Primitive Text and 2D-conditioning interfaces provide weak, ambiguous control over spatial transformations in image editing - particularly under large object motions and camera changes. Prior work has used 3D primitives such as boxes, but only as loose conditioning signals indicating approximate object location rather than specifying the transformation. We instead use 3D boxes as structured specifications: the user provides the input and output boxes of the edit, casting editing as a well-posed geometry problem. This 'thinking in boxes' interface, where each box face is colorcoded to convey 3D orientation, gives precise control over translation, rotation, scaling, and viewpoint changes in real images while preserving scene and object identity, and recovering previously unseen object regions. To ground transformations in scene appearance, we introduce a depth-aligned planar floor as a global reference frame, shaded with depth-aware cues. Conditioned on this structure, an image generator produces consistent results under large transformations. Trained in two stages - on synthetic multi-object scenes and a small set of real-world videos from Objectron - the system generalizes to complex, in-the-wild real images. Our method operates directly on real photographs and substantially outperforms recent state-of-the-art methods on large 3D edits.

- **2606.20556::00005** _(section: 1 Introduction)_:
  > Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: 1 Introduction

We call this interface ' thinking in boxes ' (Fig. 1): the box pair implicitly defines the desired translation, rotation, and scale in 3D, while its projection tells the generator which regions become newly visible and how the object's silhouette should change under perspective. To ground edits in scene appearance, we further introduce a depth-aligned planar floor, shaded with depth-aware cues to provide relative spatial positioning of objects and background.


**Top-5 retrieved**:

### [1] 2606.20556::00008
_section: 1 Introduction_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: 1 Introduction

Several recent methods aim to fill this gap, each with significant tradeoffs in the choice of input representation. One line uses per-object latent representations [64, 18] that work well in restricted domains - driving scenes, household objects - but transfer poorly to in-the-wild photos. A second line uses depth as the 3D representation, lifting diffusion activations or attention maps to 3D via the depth proxy [50, 42, 5]; this supports 3D edits on real images without retraining, but the depth-only representation is brittle under large transformations and significant disocclusion, and the methods require per-image inversion or optimization. A third line uses detailed 3D primitives - meshes or convex blocks [60, 14] - applies the edit in image or depth space, and uses diffusion as a final cleanup pass; this paradigm has so far been shown on generated images rather than real photographs [60]. We propose a different choice. Boxes at the object level and a depth-aligned floor at the scene level forms a minimal representation - the user only places and moves boxes - and structurally complete: boxes encode object pose and visibility, the floor encodes the scene geometry and disambiguates the object from the camera motion. Given that representation, a generator trained once on the source-target pair renders large 3D edits, including substantial rotations and disocclusions, on in-the-wild photographs.

### [2] 2606.20556::00005 GOLD HIT
_section: 1 Introduction_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: 1 Introduction

We call this interface ' thinking in boxes ' (Fig. 1): the box pair implicitly defines the desired translation, rotation, and scale in 3D, while its projection tells the generator which regions become newly visible and how the object's silhouette should change under perspective. To ground edits in scene appearance, we further introduce a depth-aligned planar floor, shaded with depth-aware cues to provide relative spatial positioning of objects and background.

### [3] 2606.20556::00002
_section: Thinking in Boxes: 3D Editing in Real Images Made Easy_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: Thinking in Boxes: 3D Editing in Real Images Made Easy

Figure 1: Thinking in boxes. Given a single source image (bottom left), the user fits 3D boxes around objects of interest, anchored on a depth-aligned floor (top left). Editing the boxes drives the corresponding edit in the image: from left to right, translation, rotation, combined translation and rotation, and a camera viewpoint change. The bottles' and helmets' appearance is preserved across all four edits, including regions of the object not visible in the source - note the back of the bottle and side view of the helmet revealed under rotation. Note that all qualitative figures are real images.

### [4] 2606.20556::00018
_section: 3 Method_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: 3 Method

Noise shared coordinate frame - a depth-aligned planar floor, rendered as a checkerboard with depth-aware shading. The floor moves with the camera and stays fixed under object motion, so any change in the relative configuration of boxes and floor uniquely identifies what moved. It also provides a global reference for contact and shadow. Both boxes and the floor form the 3D scene layout L src , which we project to 2D as the spatial conditioning image used by the generator Fitting boxes to images. The user fits boxes to objects through a point-and-click interface (Fig. 2). The floor is estimated automatically from the image, so the user only specifies object boxes - they never author the floor explicitly. To reduce manual effort further, off-the-shelf 3D box detectors [26] produce an initial set of boxes that the user refines.

### [5] 2606.20556::00011
_section: 2 Related Work_

> Paper: Thinking in Boxes: 3D Editing in Real Images Made Easy
Section: 2 Related Work

Concatenate Spatially Figure 2: Editing Pipeline. (1) Users provide a real source image and (2) fit 3D boxes to the objects within the scene using a point-and-click interface. (3) The boxes can be manipulated in 3D space, allowing for scaling, rotation, translation, and camera moves. Both the source and target box layouts are projected into 2D and serve, alongside the source image, as inputs to an image editing model [34]. (4) The model generates an edit that respects the underlying scene geometry and follows the user's layout. In this example, the car on the left is moved forward with the rest of the scene preserved.

---
