# Mini-RAG v2 Retrieval Audit

Per-question retrieval inspection for the v2 hybrid run.
Use this to decide whether the gold_chunk_ids were too narrow.

Format per question:
- Question + metrics summary
- Gold info (the chunks we marked + the gold answer)
- Top-5 retrieved (chunk_id + section + full text)

---

## Q01: specific_fact_lookup

**Question**: What dataset is introduced by SARLO-80?

**Metrics**: R@5=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=0.50 | AnsCorr=0.10

**Gold chunk_ids**: ['2606.20523::00017']

**Gold answer**:
> The dataset was built from open-access spotlight acquisitions collected by the Umbra satellite constellation and distributed as Sensor Independent Complex Data (SICD). They selected 2,565 SICD scenes covering all continents and diverse environments (urban, rural, coastal, mountainous), with VV or HH polarization, incidence angles ranging from 10° to 70°, and native resolutions from 20 cm to 2 m.

**Gold chunk text(s)**:
- **2606.20523::00017** _(section: 3.1 Source data: UMBRA Collections)_:
  > We built our dataset from open-access spotlight acquisitions collected by the Umbra satellite constellation and distributed as Sensor Independent Complex Data (SICD). SICD products provide complex-valued SAR images (magnitude and phase) together with rich metadata (sampling spacings, scene center point, imaging geometry), which makes them well suited for reproducible preprocessing. We select 2,565 SICD scenes covering all continents and diverse environments (urban, rural, coastal, mountainous) as shown in Figure fig. 1a, with VV or HH polarization, incidence angles ranging from 10 ◦ to 70 ◦ , and native resolutions from 20 cm to 2 m.


**Top-5 retrieved**:

### [1] 2606.20470::00059
_section: 5.1 Jailbreak Prompts Dataset_

> We evaluate our framework using a subset of 500 highrisk jailbreak prompts drawn from the AdvBench dataset introduced in [1]. These prompts represent a diverse set of illicit and harmful intent queries commonly used as seed prompts in red-teaming aligned language models. The dataset is publicly available 1 and has been adopted in several jailbreak benchmarks and attack evaluations, including PAIR, AutoDAN, and JailbreakBench [3], [6], [26].

### [2] 2606.20461::00122
_section: A Dataset Details_

> Table 4. Summary statistics (values) for the initial version of the COMPAS dataset with ternary label.

### [3] 2606.20482::00062
_section: 7 Conclusion_

> We introduced IFLLM, a dataset pairing webcambased eye-gaze trajectories and mouse movements with explicit preference annotations. The dataset allows us to systematically measure the value of implicit feedback from users for the first time. The users exhibit complicated reading patterns, which are influenced by response length, interface layout, and individual style. Driven by the scrolling need for the long responses, users' mouse movement trajectories carry strong preference signal that text or even eye-gazing data cannot capture and drastically improve the accuracy of reward models and response quality from the resulting aligned LLMs. The effectiveness and accessibility of the mouse movement suggest a natural path toward a selfreinforcing data flywheel driven by ordinary user interactions.

### [4] 2606.20554::00053
_section: 4 Industrial Deployment_

> Table 1 Statistics of public datasets.

### [5] 2606.20538::00088
_section: 7. Conclusion and Limitations_

> We introduced Multi-Task Bayesian In-Context Learning , a simple framework that bridges the flexibility and scalability of in-context learning with the principled structure of hierarchical Bayesian inference by representing priors explicitly as in-context dataset prefixes, enabling test-time control over the prior. Empirically, our approach matches oracle Bayesian predictors across diverse prior families, generalizes robustly under out-of-meta-distribution shifts, and achieves orders-of-magnitude faster inference than classical Bayesian baselines. We further demonstrate its practical applicability on a real-world environmental benchmark.

---

## Q02: specific_fact_lookup

**Question**: What evaluation metrics does CalTennis use for monocular-to-3D tennis pose estimation?

**Metrics**: R@5=1.00 | CtxP=1.00 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.66

**Gold chunk_ids**: ['2606.20542::00035']

**Gold answer**:
> MPJPE, PA-MPJPE, PVE, translation error, foot work, and stability.

**Gold chunk text(s)**:
- **2606.20542::00035** _(section: 5 Evaluation Metrics)_:
  > CalTennis uses multi-view video recordings for label-free evaluation of monocular pose estimates: a correct prediction must agree across views, and inter-view disagreement lower-bounds each model's error. In addition to the standard metrics of MPJPE, PA-MPJPE, and PVE [17], we introduce further metrics that capture additional notions of correctness that are relevant for downstream applications.


**Top-5 retrieved**:

### [1] 2606.20542::00001
_section: Abstract_

> The Caltech Tennis Dataset (CalTennis) is a large-scale video benchmark for evaluating monocular-to-3D pose estimation in the wild. CalTennis comprises over 11 million frames (51 hours) of tennis practice and match play from 40 players, captured with 2-6 synchronized cameras at 60Hz. It is 10× larger than existing in-the-wild human motion video datasets and 3× larger than existing MOCAPground-truthed datasets, and it is the first large-scale benchmark to provide synchronized multi-view recordings of expert athletic motion. The multi-view setup enables inexpensive, label-free evaluation of monocular-to-3D pose estimation algorithms. We describe a simple, standardized protocol that enables data collection without specialized equipment or expertise, along with fully automated video calibration and synchronization. Benchmarking state-of-the-art monocular-to-3D pose methods on CalTennis, we find that while 3D joint angle recovery is now quite accurate, all models struggle to estimate depth and foot contact consistently. We further propose two novel performance metrics - footwork and stability - as well as qualitatively study body shape inconsistency. These metrics expose previously underexplored failure modes and point to concrete opportunities for improvement in pose estimation and action analysis.

### [2] 2606.20542::00035 GOLD HIT
_section: 5 Evaluation Metrics_

> CalTennis uses multi-view video recordings for label-free evaluation of monocular pose estimates: a correct prediction must agree across views, and inter-view disagreement lower-bounds each model's error. In addition to the standard metrics of MPJPE, PA-MPJPE, and PVE [17], we introduce further metrics that capture additional notions of correctness that are relevant for downstream applications.

### [3] 2606.20542::00055
_section: 7 Discussion and Conclusions_

> We introduce CalTennis, a large-scale, multi-view video dataset of real-world tennis practices and match play, alongside a label-free evaluation framework that uses multi-view consistency to lowerbound monocular reconstruction error. Across eleven million frames of unscripted athletic motion, the dataset exposes monocular 3D pose estimators to depth ranges, pose variability, and action repetition that existing in-the-wild benchmarks do not cover, without requiring MOCAP, body-worn sensors, or manual annotation - only consumer phones, inexpensive tripods, and the geometry of a tennis court.

### [4] 2606.20542::00042
_section: 6 Experimental Evaluation_

> We assess state-of-the-art human pose reconstruction models on CalTennis and identify overlooked challenges in pose reconstruction that make it a difficult problem.

### [5] 2606.20542::00012
_section: 1 Introduction_

> We introduce the Caltech Tennis Dataset (CalTennis), the first large-scale, multi-view video dataset of real-world tennis practice and match play. CalTennis contains over 11 million frames (51 hours) from 40 players, captured with 2-6 synchronized consumer cameras at 60Hz. It is 10× larger than prior in-the-wild benchmarks, with substantially more variety in depth from camera, people per video, and pose coverage. To our knowledge, it is the only large-scale multi-view video dataset of unscripted human motion in natural environments. Overlapping views let us evaluate monocular pose estimators without privileged ground truth: a correct reconstruction must agree across views, and inter-view disagreement lower-bounds each model's error. This lets us probe errors in pose estimates, specifically foot contact, body shape, depth, and stability, that are invisible to existing benchmarks.

---

## Q03: specific_fact_lookup

**Question**: In the Calibrated Mixture-of-Experts under Distribution Shift paper, what is the third takeaway from the experiments?

**Metrics**: R@5=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=0.50 | AnsCorr=0.09

**Gold chunk_ids**: ['2606.20544::00088']

**Gold answer**:
> Robust filters give better accuracy / calibration trade-off than full re-weighting in several settings.

**Gold chunk text(s)**:
- **2606.20544::00088** _(section: 6.3. Results)_:
  > Takeaway 3: Robust Filtered gives a better accuracycalibration tradeoff than full reweighting in several settings. The full Robust MoE objective puts additional weight on all high-loss examples, which can improve calibration sharply but may overemphasize examples that are hard for reasons unrelated to routing. This is visible on CIFAR10H and PACS-Art, where Robust MoE lowers hard-subset calibration error but loses accuracy relative to the strongest non-robust classifier. Robust Filtered mitigates this tradeoff by applying the robust term only to routing-relevant examples while retaining an ERM term on the full minibatch. It achieves the best overall CIFAR-10H ECE ( 0 . 013 ), the best CivilComments accuracy ( 0 . 915 ), and the best PACSSketch accuracy ( 0 . 670 ), while maintaining much lower ECE than the non-robust MoE baselines.


**Top-5 retrieved**:

### [1] 2606.20544::00001
_section: Abstract_

> Calibration aligns a model's predictive uncertainty with the frequencies of its empirical outcomes and is important for understanding and trusting reported probabilities. Recent work shows that enforcing calibration at the level of individual predictors can improve ensemble accuracy and calibration, with mixture-of-experts (MoE) models showing strong empirical improvements in particular; however, the conditions under which calibration helps MoE are not well understood. In this work, we study how MoE models behave under distribution shift, focusing on how routing mechanisms interact with expert-level calibration. We show that expert calibration is sufficient to ensure calibration of the overall model under a broad class of distribution shifts in hardrouted models, but is insufficient for calibrating soft-routed models. To address this, we propose an adversarial reweighting that penalizes calibration errors of the routed aggregate under distribution shift, and we demonstrate that it improves the accuracy-calibration tradeoff both on average and on difficult subsets of the data, across model classes, prediction tasks, and distribution shifts.

### [2] 2606.20544::00016
_section: 2. Background_

> We assume throughout that each expert is calibrated on the view of the data induced by the router so that its prediction can be read as the conditional label frequency on that view. Proper losses such as cross-entropy and the Brier score encourage this kind of expert-level calibration on the training distribution, and related mixture-of-calibrated-experts methods explicitly calibrate experts before combining them (Oksuz et al., 2024; Roschewitz et al., 2025). This is a deliberately favorable assumption for MoEs: by granting calibrated experts, we rule out the simplest explanation for a miscalibrated MoE (unreliable experts) as well as the simplest remedy (calibrating the experts). Our analysis therefore asks what routing and aggregation in particular can or cannot guarantee for the final MoE predictor.

### [3] 2606.20544::00029
_section: 3.2. Calibration-preserving shifts under hard routing_

> More generally, hard routing is robust to any shift that preserves the label distribution within each expert-confidence slice. Such shifts may change the marginal frequency of experts, the marginal frequency of confidence levels, or the covariate distribution inside a routing region, as long as they do not change P ( Y | S hard ( X )) . This is the specific robustness provided by hard routing: calibration is insensitive to changes outside the expert-confidence bottleneck.

### [4] 2606.20544::00040
_section: 4.2. Aggregation collapses distinct routing configurations_

> If they appear in balancing proportions under the training distribution, the aggregate predictor is calibrated at level p . But a test-time shift that changes the relative prevalence of s and s ′ changes the label frequency among examples predicting p , and breaks calibration-even though each expert remains calibrated on its own routing-weighted view.

### [5] 2606.20544::00019
_section: 2. Background_

> Routing and distribution shift Distribution shift occurs when the distribution used to train a model differs from the distribution where the model is deployed. Distribution shift can affect calibration when probabilities that are reliable on the training distribution no longer match accuracy on the test distribution. For MoEs, routing is a natural source of distribution shift; a test distribution may change how often inputs fall into different routing regions, or different routing-weighted combinations of experts, even when the label behavior within those cases is unchanged.

---

## Q04: specific_fact_lookup

**Question**: What number of user prompts did the team use when generating Diffusion Gemma?

**Metrics**: R@5=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=0.50 | AnsCorr=0.05

**Gold chunk_ids**: ['2606.20560::00045']

**Gold answer**:
> 800.

**Gold chunk text(s)**:
- **2606.20560::00045** _(section: 3.2. What Are the Top Tokens?)_:
  > We generate DiffusionGemma rollouts on 𝑛 = 800 user prompts from the WildChat dataset (Zhao et al., 2024) up to a maximum of 1024 generated tokens (four canvases) with no early stopping and 𝑇 = 48. At each denoising step 𝑡 and sequence position 𝑖 , we take the results of the softmax in Equation (1) and extract the set of tokens that meet one of the following conditions:


**Top-5 retrieved**:

### [1] 2606.20560::00110
_section: 7.1. Further Understanding DiffusionGemma's Behavior_

> Finding problems where DiffusionGemma is better: On what kinds of problems is DiffusionGemma much more performant than Gemma?

### [2] 2606.20470::00111
_section: APPENDIX C CMPE ALTERNATIVES_

> We have tested two other alternatives to generate misdirection responses for the prompts in the jailbreak dataset in Section 5.1: (1) directly prompting the abliterated model in Section 5.2 with instructions to generate persuasive, relevant misdirection responses, and (2) using a simplified version of CMPE without generating the follow-up question (i.e., skipping step no. 10 in Algorithm 2). The plot

### [3] 2606.20560::00185
_section: E. Visualization tools_

> As a general aid to our text diffusion interpretability research, we build a dashboard with three complementary views, each one designed to shed light on different parts of the denoising process.

Algorithm 1 Logit modification function 𝑓 𝑝 for restricting information bottleneck over a sequence/batch.

### [4] 2606.20560::00113
_section: 7.1. Further Understanding DiffusionGemma's Behavior_

> Model diffing: It might be interesting to apply black-box model diffing tools to DiffusionGemma and Gemma to try to understand the behavioral differences between them (Kempf et al., 2026; Chughtai, 2026).

### [5] 2606.20560::00142
_section: 10. Acknowledgments_

> We thank Kelly He for helpful comments on the draft. We also thank the Google DeepMind Text Diffusion team for training and open sourcing the model and building infrastructure that made our experiments possible.

---

## Q05: specific_fact_lookup

**Question**: What metrics does UltraQuant use to characterize serving efficiency for 4-bit KV caching?

**Metrics**: R@5=1.00 | CtxP=0.64 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.90

**Gold chunk_ids**: ['2606.20474::00013']

**Gold answer**:
> Time to first token (TTFT) and time per output token (TPOT).

**Gold chunk text(s)**:
- **2606.20474::00013** _(section: 3 Agentic Workflow and Concurrency Analysis)_:
  > Agentic workloads are long-running sessions with a large shared prefix and many shorter follow-up turns. In this setting, compression matters because it increases the number of useful prefixes that remain resident on device. Compression alone, however, does not guarantee better serving outcomes: the overhead introduced by quantization and dequantization can degrade token latency, making end-to-end serving measurement essential. We characterize serving efficiency through two metrics: time-to-first-token (TTFT) and time-per-outputtoken (TPOT).


**Top-5 retrieved**:

### [1] 2606.20474::00041
_section: 8 Conclusions_

> The broader lesson is that low-bit KV caching should be evaluated as an end-to-end serving mechanism, not only as an offline compression method. For agent workloads, the relevant outcome is the joint effect on task success, cache residency, throughput, and interactivity. Our results indicate that 4-bit KV caching can retain the contextcapacity benefits of aggressive compression while approaching the deployability of hardware-native FP8 KV caching.

### [2] 2606.20474::00010
_section: 2.3 Serving Systems and Hardware-Native Low Precision_

> vLLM-style paged serving (Kwon et al., 2023) makes KV-cache residency a systems concern, not only a compression metric. Hardware-native formats such as FP8 already benefit from direct matrixcore support. UltraQuant extends this serving-first lens to 4-bit KV caching by targeting the CDNA4 scaled-F8F6F4 MFMA path, where FP4 operands and UE8M0 scales are consumed by the matrix core itself.

### [3] 2606.20474::00013 GOLD HIT
_section: 3 Agentic Workflow and Concurrency Analysis_

> Agentic workloads are long-running sessions with a large shared prefix and many shorter follow-up turns. In this setting, compression matters because it increases the number of useful prefixes that remain resident on device. Compression alone, however, does not guarantee better serving outcomes: the overhead introduced by quantization and dequantization can degrade token latency, making end-to-end serving measurement essential. We characterize serving efficiency through two metrics: time-to-first-token (TTFT) and time-per-outputtoken (TPOT).

### [4] 2606.20474::00012
_section: 2.3 Serving Systems and Hardware-Native Low Precision_

> Table 1: Agentic serving results on MiniMax-M2.5, TP = 2 , AMDMI355X, reported as UltraQuant relative to the FP8 KV baseline (higher is better except where noted). The advantage appears in the late rounds, where long per-client prefixes exceed the effective residentcache capacity of FP8: TTFT improves 3 . 47 × and is recovered through cache residency rather than re-prefill.

### [5] 2606.20474::00040
_section: 8 Conclusions_

> Context-heavy agents make KV-cache capacity a deployment constraint: long prefixes must remain reusable across many turns, and serving systems must support enough concurrent sessions to keep GPUs utilized. We presented a 4-bit KV-cache study centered on this setting. On the quality side, TurboQuant-style rotation and codebook methods provide a strong 4-bit anchor, with calibration and block-scale choices determining how much accuracy is retained. On the systems side, UltraTQ shows that careful layout, LUT, and MFMA scheduling can close much of the gap between codebook quantization and production serving. UltraQuant goes further by approximating the rotated codebook path with FP4 micro-tensors and UE8M0 scales so CDNA4 matrix cores perform the dequantization directly.

---

## Q06: specific_fact_lookup

**Question**: In the Calibration Without Comprehension paper on fine-tuning LLMs for vulnerability detection, what is finding two of RQ1?

**Metrics**: R@5=0.00 | CtxP=0.00 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.14

**Gold chunk_ids**: ['2606.20502::00070']

**Gold answer**:
> Fine-tuning effect is determined by the base model's initial competence.

**Gold chunk text(s)**:
- **2606.20502::00070** _(section: B. Finding 2: Fine-Tuning Effect Is Determined by the Base Model's Initial Competence)_:
  > Fine-tuning does not uniformly improve detection; direction and magnitude track the backbone's starting condition. For Qwen3-4B , performance rises by +27 . 5 to +41 . 5 pp because fine-tuning mainly overcomes abstention: coverage increases from 36 . 9% to above 91% , so the apparent gain reflects producing binary verdicts rather than learning transferable vulnerability semantics. For Llama3.1 , fine-tuning is mostly neutral or harmful ( -0 . 2 to -50 . 7 pp), with Devign-FT collapsing to 1 . 3% Overall and 4 . 1% coverage on PBD. For DeepSeek-R1 , fine-tuning consistently degrades detection ( -0 . 6 to -29 . 1 pp on LFD), often amplifying its paranoid prior. The hardest backbone to improve in detection benefits most in RQ2 coarse CWE classification, reinforcing that detection and understanding are weakly coupled.


**Top-5 retrieved**:

### [1] 2606.20502::00020
_section: a) Vulnerability Datasets (Granularity and Context):_

> d) Supervised Fine-Tuning for Vulnerability Detection: Prior work fine-tunes Transformer or GNN architectures on vulnerability datasets [19], [20], [22] or applies instructiontuned LLMs to security tasks [11], [12], but typically evaluates a single architecture on its own training corpus, conflating backbone capability with dataset effects. No prior work systematically evaluates multiple LLM backbones across multiple Vulnerability Detection (VD) datasets under matched contamination controls, the design needed to isolate genuine security learning from training-distribution artifacts.

### [2] 2606.20502::00118
_section: IX. THREATS TO VALIDITY_

> Our supervised transfer study uses three backbones with LoRA adaptation, so findings apply most directly to LoRAbased fine-tuning on these models and datasets; other PEFT methods or full fine-tuning may differ. We treat these as directions for future work rather than contradictions. Similarly, we study five widely used vulnerability datasets rather than exhaustively covering all academic corpora, so results primarily reflect current mainstream fine-tuning practice.

### [3] 2606.20502::00006
_section: I. INTRODUCTION_

> Prior work on vulnerability detection mainly studies either non-LLM models (e.g., GNNs, short-context Transformers) or applies LLMs to short, single-function snippets, without jointly addressing long-context vulnerabilities and finetuning long-context LLMs across multiple state-of-the-art VD datasets. For example, Ullah et al. [13] highlight contamination risks using a curated set of 228 samples across 8 CWEs, but do not examine function-level distribution shifts, multi-backbone fine-tuning, or diagnostic decomposition. Similarly, Croft et al. [18] identify label noise at the dataset level. In contrast, we quantify compromised-sample rates at the function level and link them mechanistically to a null contamination finding.

### [4] 2606.20502::00062
_section: IV. EXPERIMENTAL SETUP_

> RQ1 (Vulnerability Detection Reliability): How reliably do vanilla and fine-tuned models detect vulnerabilities and verify patches, and what roles do directional bias, label-space transfer, and contamination play?

### [5] 2606.20502::00001
_section: Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software_

> Abstract -Whether Large Language Models (LLMs) scoring well on vulnerability benchmarks genuinely reason about security or merely pattern-match on contaminated data remains unresolved. We present CWE-Trace, a framework for LLM vulnerability detection built from 834 manually curated Linux kernel samples spanning 74 Common Weakness Enumerations (CWEs). The framework enforces a strict temporal split (pre2025 historical set / post-cutoff leakage-free set), preserves context-aware vulnerable-patched pairs, and introduces two diagnostic metrics: the Directional Failure Index (DFI) and Hierarchical Distance and Direction (HDD). We evaluate eight vanilla LLMs and 15 LoRA fine-tuned variants across nontargeted detection, targeted detection, and CWE classification. Our analysis yields two key results. First, data contamination provides no measurable advantage. Function-level analysis shows that 84% of nominally contaminated samples carry no usable memorization signal: vulnerable functions are absent or crossmapped across datasets, and ∼ 31% of contaminated samples carry CWE misclassification. Second, backbone directional priors dominate fine-tuning. Models exhibit stable, systematic failure modes (DFI ranging from -85 . 5 to +94 . 8 pp) that persist from historical to post-cutoff data and resist correction. Fine-tuning shifts the output threshold without changing the decision policy. This is calibration without comprehension: output distributions adapt to training data while the underlying security reasoning remains absent. The weakest backbone at binary detection (DeepSeek-R1) gains the most in coarse CWE classification, revealing that detection and understanding are decoupled capabilities. The best detection score reaches only 52 . 1% ( +2 . 1 pp above chance); exact CWE ranking remains below 1 . 3% Top1 accuracy, confirming that current LLMs lack reliable security reasoning for systems software, regardless of fine-tuning strategy.

---

## Q07: definition

**Question**: What is MAA?

**Metrics**: R@5=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=0.50 | AnsCorr=0.12

**Gold chunk_ids**: ['2606.20475::00011']

**Gold answer**:
> Marginal Advantage Accumulation (MAA) for Memory-Driven Agent Self-Evolution. Its core idea is to ground user-perceived 'optimization suggestions' into addressable atomic operations (ops) with invariant identity across batches, and on this basis construct scale-consistent accumulation signals so that evidence of the same op across different batches can be additively aggregated.

**Gold chunk text(s)**:
- **2606.20475::00011** _(section: 1.3 Method Overview and Contributions)_:
  > To address the above gap, we propose Marginal Advantage Accumulation (MAA) for Memory-Driven Agent Self-Evolution. As illustrated in Figure 1, the core idea of MAA is to ground user-perceived 'optimization suggestions' into addressable atomic operations (ops) with invariant identity across batches, and on this basis construct scale-consistent accumulation signals so that evidence of the same op across different batches can be additively aggregated.


**Top-5 retrieved**:

### [1] 2606.20560::00110
_section: 7.1. Further Understanding DiffusionGemma's Behavior_

> Finding problems where DiffusionGemma is better: On what kinds of problems is DiffusionGemma much more performant than Gemma?

### [2] 2606.20560::00152
_section: References_

> Chughtai, Bilal (2026). Model Diffing Agents . In preparation.

### [3] 2606.20520::00139
_section: 8 System Evaluation_

> RQ3 (Credential Minting Cost): What is the computational and network cost of dynamic scoped credential issuance?

RQ4 (Drift Detection): How does the drift check perform under live state queries, and what is its overhead?

### [4] 2606.20480::00095
_section: 4. Simulations_

> Table 1.

### [5] 2606.20545::00084
_section: 4.1.3 Series Increments: Scaling, Architecture, and Training_

> Finding 5. World models need a what -memory, not just a where -memory. Every architecture caches geometry, appearance, or motion to re-render where the scene was, so how the camera is encoded is second-order, while the missing, highest-leverage component is a state writer that records what changed while hidden.

---

## Q08: definition

**Question**: What does mobility refer to?

**Metrics**: R@5=1.00 | CtxP=1.00 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.49

**Gold chunk_ids**: ['2606.20485::00079']

**Gold answer**:
> Mobility refers to the ability of agents, resources, information, and influence to change positions within a system over time.

**Gold chunk text(s)**:
- **2606.20485::00079** _(section: Mobility and Viscosity)_:
  > Mobility refers to the ability of agents, resources, information, and influence to change positions within a system over time. Mobility cannot be inferred from either growth or volatility. In economic systems, mobility may describe the ability of individuals to move across wealth or income ranks [Carroll & Cohen-Kristiansen 2022]. In organizations, mobility reflects the ability of individuals to assume new roles and responsibilities. In knowledge systems, mobility describes the ability of ideas and beliefs to evolve in response to new evidence. More generally, mobility measures the adaptability and flexibility of a system [Lo & Zhang 2024]. A highly productive but immobile system may become incapable of adaptation or self-repair, while a highly mobile system may fail to accumulate sufficient structure and coordination. The optimal system therefore balances productivity, stability, and mobility.


**Top-5 retrieved**:

### [1] 2606.20485::00080
_section: Mobility and Viscosity_

> Mobility (or fluidity) is often modeled as inversely proportional to viscosity. Viscosity represents the resistance of the system to redistribution of power, wealth, influence, or information, which reflects the friction or linkage of agents. One hypothesis of this paper is that viscosity/mobility is related to the strength of feedback interactions 𝐵𝐵 𝑖𝑖 among agents. For example, we can hypothesize viscosity as 𝑉𝑉 = ∑ | 𝐵𝐵 𝑖𝑖 𝑵𝑵 𝒊𝒊=𝟏𝟏 | , mobility is M=1/V .

### [2] 2606.20485::00079 GOLD HIT
_section: Mobility and Viscosity_

> Mobility refers to the ability of agents, resources, information, and influence to change positions within a system over time. Mobility cannot be inferred from either growth or volatility. In economic systems, mobility may describe the ability of individuals to move across wealth or income ranks [Carroll & Cohen-Kristiansen 2022]. In organizations, mobility reflects the ability of individuals to assume new roles and responsibilities. In knowledge systems, mobility describes the ability of ideas and beliefs to evolve in response to new evidence. More generally, mobility measures the adaptability and flexibility of a system [Lo & Zhang 2024]. A highly productive but immobile system may become incapable of adaptation or self-repair, while a highly mobile system may fail to accumulate sufficient structure and coordination. The optimal system therefore balances productivity, stability, and mobility.

### [3] 2606.20485::00113
_section: VI. Conclusions_

> Several important questions remain open for future research. These include the empirical measurement of agent response functions, the formal characterization of mobility and adaptability, the relationship between synchronization and systemic fragility, and the development of practical methods for identifying optimal order in real-world systems. Addressing these questions may lead to a deeper understanding of how complex systems grow, adapt, learn, and sustain themselves over time.

### [4] 2606.20506::00212
_section: [Evaluation Criterion]_

> -Texture does not refer to color schemes or object contours.

COLOR (color palette, color distribution, temperature,

### [5] 2606.20512::00007
_section: 1 Introduction_

> This paper describes four contributions in this context:

---

## Q09: definition

**Question**: In the Hierarchical Recovery for Cross-Device Agent Systems paper, what is the Strategy Planner?

**Metrics**: R@5=0.00 | CtxP=1.00 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.88

**Gold chunk_ids**: ['2606.20487::00026']

**Gold answer**:
> The Strategy Planner is the device-level planner responsible for selecting and revising execution strategies within a single device.

**Gold chunk text(s)**:
- **2606.20487::00026** _(section: 3.4 STRATEGY PLANNER)_:
  > The Strategy Planner is the device-level planner responsible for selecting and revising execution strategies within a single device. Similar to interactive agents that choose actions based on recent observations (Yao et al., 2023), it maps the assigned subtask and previous observations to one of three decisions:

S d ( q j , h j , b j , Φ( d )) →{ EXECUTE ( π, x ) , DONE ( y j ) , ESCALATE ( c j ) }


**Top-5 retrieved**:

### [1] 2606.20487::00059
_section: 5 CONCLUSION_

> In this paper, we presented H-RePlan, a scope-aware hierarchical replanning framework designed to navigate the dynamic complexities of cross-device computer-use tasks. To overcome the limitations of existing multi-device agents, we introduced a platform-independent unified strategy-control abstraction that equips each device with its supported subset of API, CLI, and GUI execution strategies. By explicitly separating recovery into device-local strategy revision and orchestrator-level crossdevice replanning, our framework accurately matches recovery actions to strategy- and device-level failures, enabling the system to recover many strategy-level failures locally and to reduce unnecessary loss of execution context.

### [2] 2606.20487::00006
_section: 1 INTRODUCTION_

> To address this challenge, we propose H-RePlan , a hierarchical replanning framework for multidevice agents with unified API-CLI-GUI execution. H-RePlan introduces a platform-independent strategy-control abstraction that represents each device by its supported subset of API, CLI, and GUI execution strategies. At the device layer , a Strategy Planner decomposes assigned subtasks, selects execution strategies, and performs local recovery by revising the strategy or instruction when a strategy-level failure occurs. At the system layer , an Orchestrator maintains the cross-device task plan, incorporates failure evidence from devices, and handles device-level failures through reassignment or recovery subtasks.

### [3] 2606.20487::00058
_section: 4.3 ABLATION STUDY_

> Together, these ablations show that H-RePlan's performance does not arise from structured API access alone; it also depends on the hierarchical recovery architecture. API strategies provide efficient execution, while the Strategy Planner, Global Replan, and CLFE ensure that failures are repaired at the appropriate layer.

### [4] 2606.20487::00009
_section: 1 INTRODUCTION_

> We propose H-RePlan , a scope-aware hierarchical replanning framework that separates device-local strategy recovery from orchestrator-level cross-device replanning.

We introduce a platform-independent unified strategy-control abstraction that equips each device with interchangeable API, CLI, and GUI strategies as available on that platform.

### [5] 2606.20487::00061
_section: 5 CONCLUSION_

> To systematically evaluate this paradigm, we built HeraBench, a fault-injected multi-device benchmark that assesses hierarchical recovery under multi-level failures. Extensive experiments demonstrate that H-RePlan significantly outperforms single-strategy and coarse-grained baselines across task completion, instruction adherence, and execution efficiency. Notably, it achieves a substantially higher perfect-pass rate while drastically reducing the token cost required for reliable end-to-end success. Ultimately, this work establishes that robust multi-device agent systems must explicitly model both intra-device strategy spaces and inter-device orchestration.

---

## Q10: definition

**Question**: What is a contagion network?

**Metrics**: R@5=1.00 | CtxP=0.00 | CtxR=0.75 | Faith=1.00 | AnsCorr=0.70

**Gold chunk_ids**: ['2606.20493::00004', '2606.20493::00005']

**Gold answer**:
> A contagion network describes how evaluator biases propagate across interacting LLM agents through a closed feedback loop where biased judgments from one agent directly shape another agent's subsequent outputs; the paper formalizes this phenomenon as Contagion Networks, where bias can propagate hop-by-hop (e.g., A → B → C) and, if the process iterates, the entire agent network can converge to a single strategy.

**Gold chunk text(s)**:
- **2606.20493::00004** _(section: 1 Introduction)_:
  > Consider a concrete scenario: Agent A (GPT-4o) evaluates Agent B 's (DeepSeek) code generation output. GPT-4o, shaped by RLHF training on structured explanations, strongly prefers step-by-step reasoning. This feedback causes DeepSeek to increasingly adopt step-bystep strategies. Now Agent B evaluates Agent C 's (Claude) output-and applies the same step-by-step preference it absorbed from Agent A . Claude, in turn, shifts toward step-by-step. The bias has propagated two hops: A → B → C . If the process iterates, the entire agent network converges to a single strategy, eliminating the very cognitive diversity that multi-agent systems are designed to exploit.

- **2606.20493::00005** _(section: 1 Introduction)_:
  > We formalize this phenomenon as Contagion Networks and make the following contributions:


**Top-5 retrieved**:

### [1] 2606.20493::00015
_section: 2.3 Epidemiological Models in AI Systems_

> Table 1: Systematic comparison with related phenomena. Contagion Networks is the only framework simultaneously capturing multi-agent, multi-hop propagation dynamics.

### [2] 2606.20493::00068
_section: 6.3 Connection to Cross-Modal Contagion (MM-EPC)_

> MM-EPC shows that cross-modal contagion ( γ V → T = γ T → V ) is real and asymmetric.

This work shows that cross-agent contagion ( γ i → j > 0 ) is also real, but its magnitude depends on evaluator diversity.

### [3] 2606.20493::00006
_section: 1 Introduction_

> Cross-Agent Contagion Matrix Γ N : We extend the 2 × 2 cross-modal contagion matrix to N agents, providing a quantitative framework for measuring evaluator bias propagation in arbitrary agent topologies.

### [4] 2606.20493::00059
_section: 6.1 Suppression vs. Cascade: The Role of Evaluator Diversity_

> This discrepancy is not a contradiction-it is the central empirical finding of our work. It suggests a contagion spectrum :

### [5] 2606.20493::00005 GOLD HIT
_section: 1 Introduction_

> We formalize this phenomenon as Contagion Networks and make the following contributions:

---

## Q11: methodology

**Question**: In the Calibration Without Comprehension paper, how did they assess each model performance on detecting vulnerabilities in system software?

**Metrics**: R@5=0.00 | CtxP=0.87 | CtxR=1.00 | Faith=0.50 | AnsCorr=0.12

**Gold chunk_ids**: ['2606.20502::00022']

**Gold answer**:
> CWE-Trace assesses security reasoning in vanilla and fine-tuned LLMs by extracting high-fidelity Linux kernel vulnerabilities, splitting them into temporal historical (PBD) and leakage-free (LFD) datasets, and evaluating models zero-shot on non-targeted detection, targeted detection, and hierarchical CWE classification using standard accuracy, coverage, DFI, and HDD. DFI quantifies directional decision bias, while HDD measures reasoning depth through shortest-path distance and error direction in the CWE taxonomy.

**Gold chunk text(s)**:
- **2606.20502::00022** _(section: III. METHODOLOGICAL FRAMEWORK)_:
  > CWE-Trace (Figure 2) assesses security reasoning in vanilla and fine-tuned LLMs. We extract high-fidelity Linux kernel vulnerabilities and split them into temporal splits of historical (PBD) and leakage-free (LFD) datasets, and evaluate models zero-shot on non-targeted detection, targeted detection, and hierarchical CWE classification using standard accuracy, coverage, DFI, and HDD. DFI quantifies directional decision bias, while HDD measures reasoning depth through shortest-path distance and error direction in the CWE taxonomy. Although this study focuses on C/Linux, the framework's extraction pipeline, temporal-split protocol, and evaluation metrics are language-agnostic: the same logic applies directly to any codebase for which commit-level CVE fixes can be retrieved and manually validated. Extension to other languages (e.g., Java, Python) is therefore a straightforward engineering task and constitutes a concrete direction for future work. The goal is to separate broad detection ability from exact semantic diagnosis under a single benchmark.


**Top-5 retrieved**:

### [1] 2606.20502::00005
_section: I. INTRODUCTION_

> Traditional approaches (e.g., fuzzing, penetration testing, and Static Analysis Tools (SATs) such as CodeQL [2] and Semgrep [3]) suffer from coverage gaps, logic blindness, and false positives [4]. Recent work explores Large Language Models (LLMs) for code and security tasks, including vulnerability benchmarks and CWE analyses [5]-[15]. However, evaluations often (1) rely on historical vulnerabilities with possible contamination [13], (2) strip context, (3) lack strict vulnerable-patched pairing [16]-[18], and (4) report only binary accuracy, obscuring hierarchical CWE understanding. Gap (2) is illustrated by CVE-2024-41010 (Figure 1): the UseAfter-Free (CWE-416) is invisible when ingress_init is analyzed alone and revealed only by checking tcx.h (a bool flag). These gaps prevent a reliable assessment of whether fine-tuning LLMs instills genuine security reasoning or merely calibrates without comprehension : shifting the output distribution to match training labels without improving the underlying representations that support security reasoning.

### [2] 2606.20542::00131
_section: A.5 Additional dataset complexity analyses_

> Table 4: SOTA Model Performance on Current Benchmarks. We report the performance reported by each paper, on the standard human motion evaluation metrics.

Figure 11: Pose Space Uniformity and Coverage of Real-World Datasets .

### [3] 2606.20502::00062
_section: IV. EXPERIMENTAL SETUP_

> RQ1 (Vulnerability Detection Reliability): How reliably do vanilla and fine-tuned models detect vulnerabilities and verify patches, and what roles do directional bias, label-space transfer, and contamination play?

### [4] 2606.20502::00075
_section: VI. RQ2: CWE-1000 CLASSIFICATION BEFORE AND AFTER FINE-TUNING_

> RQ2 asks whether models can place vulnerabilities into the correct coarse CWE-1000 root family, a weaker target than exact CWE identification, capturing broad security understanding before probing semantic depth in RQ3.

### [5] 2606.20538::00154
_section: G.2.1. TRAINING ON FIXED K_

> To study how model performance depends on the amount of prior evidence, we trained separate models for number of prior tasks K ∈ { 1 , 5 , 20 , 30 } and evaluated each model in the corresponding regime.

---

## Q12: methodology

**Question**: How does the Multi-Qutrit Entropy Estimation paper estimate the quantum state using their variational quantum algorithm?

**Metrics**: R@5=0.00 | CtxP=0.70 | CtxR=0.00 | Faith=1.00 | AnsCorr=0.42

**Gold chunk_ids**: ['2606.20504::00028', '2606.20504::00034']

**Gold answer**:
> The central idea is to learn a measurement basis in which the entropy can be inferred directly from classical measurement statistics. The variational circuit preserves the intrinsic entropy of the state and seeks a unitary transformation that approximately aligns the computational basis with the eigenbasis of the density matrix; the optimization favors bases that produce maximally non-uniform outcomes, so that p(θ) approximates the eigenvalue spectrum and the resulting measurement entropy provides an estimate of the von Neumann entropy of the quantum state.

**Gold chunk text(s)**:
- **2606.20504::00028** _(section: A. Variational Quantum Algorithm (VQA) Approach)_:
  > The central idea is to learn a measurement basis in which the entropy can be inferred directly from classical measurement statistics. The variational circuit preserves the intrinsic entropy of the state and instead seeks a unitary transformation that approximately aligns the computational basis with the eigenbasis of the density matrix.

- **2606.20504::00034** _(section: A. Variational Quantum Algorithm (VQA) Approach)_:
  > The optimization therefore favors bases that produce maximally non-uniform outcomes. For a fixed state, this occurs when the measurement basis aligns with the eigenbasis of ρ , in which case p ( θ ) approximates the eigenvalue spectrum. The resulting measurement entropy then provides an estimate of the von Neumann entropy of the quantum state.


**Top-5 retrieved**:

### [1] 2606.20504::00027
_section: A. Variational Quantum Algorithm (VQA) Approach_

> We develop a variational framework for estimating the von Neumann entropy of multi-qutrit quantum states. While most prior variational approaches focus on qubit systems, extending these ideas to higher-dimensional settings introduces new challenges in circuit design and scalability.

### [2] 2606.20504::00011
_section: II. RELATED WORK_

> A wide range of methods have been proposed to estimate information-theoretic properties of quantum states without full tomography. These approaches address the challenges of estimating quantities such as the von Neumann entropy directly from limited access to quantum systems.

### [3] 2606.20504::00079
_section: IV. RESULTS_

> Fig. 5: Absolute prediction error in the estimation of von Neumann entropy for two- and three-qutrit quantum states as a function of the percentage of mixedness. Two-qutrit states have negligible error while all ansatzes for three-qutrit VQA perform similar.

### [4] 2606.20504::00003
_section: Entropy Estimation in Multi-Qutrit Systems via Variational and Classical Neural Networks_

> Index Terms -von Neumann entropy, qutrit systems, variational quantum algorithms, convolutional neural networks, mutually unbiased bases, ideal quantum simulation

### [5] 2606.20504::00008
_section: I. INTRODUCTION_

> In this work, we investigate tomography-free estimation of von Neumann entropy in multi-qutrit quantum systems using two complementary approaches. First, we study VQAs in lowdimensional regimes, where circuit structure and parameterization can be explicitly controlled. We design hardware-efficient SU(3)-inspired ansatzes built from Gell-Mann rotation (GMR) gates and qutrit SUM (CSUM) operations, and systematically analyze the interplay between parameter count, circuit depth, and entanglement in entropy estimation.

---

## Q13: methodology

**Question**: How does FreeStyle train its style-content dual-reference generation model?

**Metrics**: R@5=0.00 | CtxP=0.87 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.58

**Gold chunk_ids**: ['2606.20506::00018']

**Gold answer**:
> They adopt a two-stage curriculum progressing from style-reference generation (Stage 1, trained on style-transfer data) to the harder dual-reference setting (Stage 2, mixing LoRA-mined triplets with style-transfer data). Each stage faces a distinct content-leakage mechanism and employs a corresponding disentanglement strategy: an attention-level enrichment constraint for Stage 1 and frequency-aware RoPE modulation for Stage 2.

**Gold chunk text(s)**:
- **2606.20506::00018** _(section: 3. Method Overview)_:
  > Training (§5). We adopt a two-stage curriculum progressing from style-reference generation (Stage 1, trained on styletransfer data) to the harder dual-reference setting (Stage 2, mixing LoRA-mined triplets with style-transfer data). Each stage faces a distinct content-leakage mechanism and employs a corresponding disentanglement strategy: an attentionlevel enrichment constraint (§5.1) for Stage 1 and frequencyaware RoPE modulation (§5.2) for Stage 2.


**Top-5 retrieved**:

### [1] 2606.20506::00093
_section: 8. Discussion and Conclusion_

> quality follows a long-tailed distribution and evolves rapidly, making automated curation an ongoing challenge. Second, stylistic semantics across different base models still exhibit domain shift, limiting cross-model transferability. Third, existing evaluation metrics, including the proposed Verification Score, remain insufficient for fine-grained characterization of style-content conflict intensity. Future work will focus on automated LoRA quality assessment, cross-model style alignment, and more granular leakage metrics. In summary, we present FreeStyle, a complete framework for style- and content-dual-reference generation comprising a communityLoRA-based data pipeline, a two-stage training strategy with stage-specific disentanglement mechanisms, and a systematic benchmark. Extensive experiments show that jointly optimizing data, training constraints, and evaluation leads to more robust and balanced dual-reference generation than improving any single component alone.

### [2] 2606.20506::00009
_section: 1. Introduction_

> We propose FreeStyle, a scalable dual-reference generation framework that mines community LoRAs as compositional anchors for style and content, enabling large-scale construction of SRef and CRef triplets across multiple base models with broad long-tail style coverage.

### [3] 2606.20506::00322
_section: [Output Format]_

> Figure 23. Additional Showcases of the Style-content Dual-reference Triplet Data (Part I). These samples offer a more comprehensive view of the high-quality and stylistically diverse dataset generated via our LoRA-combination pipeline.

### [4] 2606.20457::00001
_section: Repurposing a Speech Classifier for Guided Diffusion-Based Speech Generation_

> Motivated by this, we investigate whether a conventionally trained noise-conditioned classifier already provides sufficient information for score-based generation. We keep the classifier parameters fixed and train a lightweight generative adapter on top of its feature maps, following subnetwork and frozen-backbone adaptation strategies [10, 11, 12]. This yields a parameter-efficient alternative to the standard two-model conditional generation pipeline.

### [5] 2606.20506::00002
_section: Abstract_

> Style- and content-dual-reference generation aims to synthesize an image that preserves the structure and semantics of a content reference while adopting the style of a separate style reference. Despite recent progress, this setting remains challenging because models must balance content fidelity, style alignment, and instruction following while avoiding semantic leakage from the style reference. A key bottleneck is the lack of large-scale triplet data with clean content-style separation and broad long-tail style coverage. In this work, we propose FreeStyle, a scalable dual-reference generation framework based on community LoRA mining. We treat community LoRAs as compositional anchors for style and content, and design a rigorous generation and filtering pipeline to construct large-scale content-style dual-reference triplets across multiple base models. To address content leakage, we adopt a two-stage curriculum with stage-specific disentanglement mechanisms: an attention-level enrichment constraint that suppresses style-reference leakage in the style-transfer stage, and a frequency-aware RoPE modulation strategy that targets positional-correspondence-based leakage in the harder dual-reference stage. We also introduce a benchmark covering both style-reference and dual-reference generation, with evaluations on style similarity, content preservation, aesthetics, instruction following, and VLM-based verification. The benchmark incorporates a style-invariant Content Alignment Score (CAS) and introduces a VLM-based Verification Score for evaluating generation reliability and potential cross-reference leakage. Extensive experiments show that our model achieves a strong balance among style alignment, content preservation, and leakage suppression.

---

## Q14: methodology

**Question**: How does the ACE (Action-based Candidate Evidence) module work?

**Metrics**: R@5=1.00 | CtxP=0.75 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.87

**Gold chunk_ids**: ['2606.20561::00019']

**Gold answer**:
> ACE serves as the lightweight component of TIMEPROVE. Its objective is to transform a long video into a compact temporal action representation that can be leveraged to generate candidate answer hypotheses before invoking an expensive VLM. ACE consists of two submodules: (i) Action Detector, which performs a single pass over the video to temporally localize actions, and (ii) Query-conditioned Proposal Generator, which employs an edge LLM to reason over the localized actions and produce query-conditioned candidate answers along with corresponding evidence windows.

**Gold chunk text(s)**:
- **2606.20561::00019** _(section: 3.1 Action-based Candidate Evidence (ACE))_:
  > ACE serves as the lightweight component of TIMEPROVE. Its objective is to transform a long video into a compact temporal action representation that can be leveraged to generate candidate answer hypotheses before invoking an expensive VLM. ACE consists of two submodules: (i) Action Detector , which performs a single pass over the video to temporally localize actions, and (ii) Query- conditioned Proposal Generator , which employs an edge LLM to reason over the localized actions and produce query-conditioned candidate answers along with corresponding evidence windows.


**Top-5 retrieved**:

### [1] 2606.20561::00009
_section: 1 Introduction_

> We design the Action-based Candidate Evidence (ACE) module, the first module of its kind to transform detected actions into query-conditioned answer-evidence candidates through lightweight LLM reasoning and structured reranking.

### [2] 2606.20510::00096
_section: 5. Evaluation_

> RQ1 How effectively does our SDP relaxation balance system utility and security guarantees on terminal agent benchmarks compared to prior work? We find that the SDP achieves the optimal tradeoff outperforming prior art on utility at various fixed security levels (Table 2).

### [3] 2606.20561::00019 GOLD HIT
_section: 3.1 Action-based Candidate Evidence (ACE)_

> ACE serves as the lightweight component of TIMEPROVE. Its objective is to transform a long video into a compact temporal action representation that can be leveraged to generate candidate answer hypotheses before invoking an expensive VLM. ACE consists of two submodules: (i) Action Detector , which performs a single pass over the video to temporally localize actions, and (ii) Query- conditioned Proposal Generator , which employs an edge LLM to reason over the localized actions and produce query-conditioned candidate answers along with corresponding evidence windows.

### [4] 2606.20515::00132
_section: E. Additional Qualitative Visualizations_

> Figures 6 and 7 provide additional qualitative examples beyond those in the main paper. These cases further illustrate how S-AGENT adapts its tool-use trajectory to different spatial questions, including counting, multi-step reasoning, relative position, and route planning. Across these examples, the agent first selects or grounds task-relevant evidence, then applies metric or spatial experts to convert visual observations into explicit intermediate evidence before producing the final answer.

### [5] 2606.20475::00090
_section: 4.6 Design Layer Verification: Learning Curves and Evidence Trajectories_

> This experiment corresponds to RQ4, visualizing the actual operation of MAA's cross-batch evidence accumulation through learning curves and evidence trajectories (Figure 3).

---

## Q15: table_numerical

**Question**: What is the ASR score when the Defender is SR Scout 30B and the Attacker is HB-FT-LLaMA 2-13B Attempts?

**Metrics**: R@5=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=0.00 | AnsCorr=0.57

**Gold chunk_ids**: ['2606.20470::00078']

**Gold answer**:
> 0.165

**Gold chunk text(s)**:
- **2606.20470::00078** _(section: 5.5 ASR Evaluation & Comparison)_:
  > TABLE 3: Sample-averaged simulated ASR upper bound under the CMPE-based detect-and-misdirect strategy for N = 100 homogeneous i.i.d. attack attempts with K = 1 . For each prompt, ASR is computed using per-sample judge error estimates including γ A , and the table reports the average across all 500 prompts.

| Defender ↓ / Attacker →   | SR-OSS-120B   | SR-Scout-30B   | PAIR-OSS-120B   | HB-FT-LLaMA2-13B   | LLaMA-Guard-3-8B   | GPTFuzz-RoBERTa   |
|---------------------------|---------------|----------------|-----------------|--------------------|--------------------|-------------------|
| SR-OSS-120B               | 0 . 004       | 0 . 005        | 0 . 005         | 0 . 007            | 0 . 003            | 0 . 005           |
| SR-Scout-30B              | 0 . 124       | 0 . 049        | 0 . 094         | 0 . 165            | 0 . 074            | 0 . 084           |
| PAIR-OSS-120B             | 0 . 028       | 0 . 023        | 0 . 007         | 0 . 025            | 0 . 005            | 0 . 017           |
| HB-FT-LLaMA2-13B          | 0 . 077       | 0 . 064        | 0 . 052         | 0 . 001            | 0 . 046            | 0 . 039           |
| LLaMA-Guard-3-8B          | 0 . 098       | 0 . 075        | 0 . 063         | 0 . 126            | 0 . 000            | 0 . 039           |


**Top-5 retrieved**:

### [1] 2606.20470::00072
_section: 5.5 ASR Evaluation & Comparison_

> Table 2 reports the detect-and-block baseline for N = 100 attacker attempts and verification budget K = 1 , where misdirection is absent and γ A = 0 . Table 3 reports the corresponding CMPE-based detect-and-misdirect case using the estimated misdirection-induced false-positive rates. The baseline results show high simulated ASR upper bounds across many attacker-defender configurations, with several values approaching 1 . In contrast, CMPE substantially reduces the estimated ASR upper bound across the same configurations, often by one to two orders of magnitude.

### [2] 2606.20470::00057
_section: 5 SIMULATION & NUMERICAL RESULTS_

> In this section, we evaluate the efficacy of CMPE as an example of the detect-and-misdirect strategy for increasing misdirection-induced false-positive rates in automated judge models used by jailbreak attack frameworks. We then estimate its impact on maximum ASR in a simulated setting involving judge models used on both the defense and attacker sides, where the attacker performs homogeneous i.i.d. trials over benchmark malicious requests.

### [3] 2606.20470::00073
_section: 5.5 ASR Evaluation & Comparison_

> This reduction is driven by the increase in misdirectioninduced false-positive rates γ A , which lowers the attacker's positive predictive value (PPV) and degrades automated candidate selection. These simulation results illustrate the mechanism predicted in Section 3: detect-and-block permits high ASR under repeated attempts, whereas detect-and- misdirect bounds attacker success by corrupting the judgebased selection process.

### [4] 2606.20470::00095
_section: 7 RELATED WORK ON ACTIVE DEFENSES_

> Another related public work, Proactive Defense Against LLM Jailbreak , introduces ProAct as a proactive defense framework for iterative jailbreak attacks [31], [32]. ProAct generates benign 'spurious responses' that appear to satisfy harmful requests, causing iterative jailbreak methods to misinterpret the response as a successful jailbreak and terminate prematurely. Our work shares the high-level intuition that apparent success can be safer for the defender than predictable refusal, but differs in its analytical focus and security abstraction. Rather than treating misdirection primarily as an empirical proactive-defense mechanism, we formalize the attacker's response evaluation process as the central point of failure, introduce misdirectioninduced false-positives as an explicit attacker-side error term, and derive ASR bounds in terms of defense falsenegatives, attacker judge false-negatives, verification budget, and misdirection-induced false-positive rate. This analysis explains why detect-and-misdirect differs from simple refusal or termination: refusal provides a negative search signal, while misdirection corrupts the attacker's candidate selection by lowering the positive predictive value of its judge. We further quantify adaptive judge and ensemble trade-offs and evaluate CMPE using both sample-averaged ASR simulations and end-to-end PAIR/GPTFuzz experiments with validated TP, FP, and MI-FP outcomes.

### [5] 2606.20470::00079
_section: 5.5 ASR Evaluation & Comparison_

> TABLE 3: Sample-averaged simulated ASR upper bound under the CMPE-based detect-and-misdirect strategy for N = 100 homogeneous i.i.d. attack attempts with K = 1 . For each prompt, ASR is computed using per-sample judge error estimates including γ A , and the table reports the average across all 500 prompts.

---

## Q16: table_numerical

**Question**: In the Fast Human Attention Prediction paper on fixation-guided active perception, what is the time performance of the ResNet50 backbone?

**Metrics**: R@5=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=0.33 | AnsCorr=0.06

**Gold chunk_ids**: ['2606.20491::00050']

**Gold answer**:
> 7.39 ms

**Gold chunk text(s)**:
- **2606.20491::00050** _(section: C. Backbone Ablations)_:
  > | Backbone              | ScanMatch ↑   |   Time (ms) ↓ |   #Params (M) ↓ |   GFLOPs ↓ |
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

### [1] 2606.20491::00070
_section: VII. CONCLUSIONS_

> An efficient scanpath prediction model, GazeLNN, is proposed that leverages a liquid neural network as the recurrent module. GazeLNN achieves state-of-the-art performance on the MIT Low Resolution dataset with a Scanmatch score of 0.47, while reducing the computational costs by 99.40% and having an inference speed-up of 6 . 42 × . GazeLNN is further integrated with an active camera control policy trained via RL to investigate the role of human attention modeling in robot autonomy. The experiments show that the policy maintains human-fixation-guided perception behavior, pointing the active camera to the fixation locations predicted by GazeLNN while performing a navigation task. Future work shall further investigate the correlation of fixation scanpath, the configuration of the active camera and its motion dynamics, and the reinforcement learning policy.

### [2] 2606.20491::00001
_section: Fast Human Attention Prediction for Fixation-guided Active Perception in Autonomous Navigation_

> Abstract -Human visual attention relies on structured scanpaths to efficiently process scenes, yet instilling this behavior into robot autonomy is in its infancy and hindered by the high computational costs of existing predictive models. To address this, we introduce GazeLNN, a computationally lightweight scanpath prediction model that leverages Liquid Neural Networks as its recurrent engine and employs MobileNetV3 for feature extraction. Operating auto-regressively, the architecture predicts sequential fixation heatmaps conditioned on the current visual stimulus and fixation history. Despite requiring only 0.61 GFLOPs, GazeLNN achieves state-of-the-art performance on the MIT Low Resolution dataset achieving 0.47 ScanMatch score. It outperforms existing recurrent baselines across diverse evaluation metrics, while reducing computational costs by 99.40% and accelerating inference by up to six times. To investigate the role of human attention modeling in robot autonomy and demonstrate the practical utility of this highly efficient architecture, we integrate GazeLNN into an active camerarobot control policy trained via Reinforcement Learning. This integration enables human-fixation-guided perception during autonomous navigation, validated through successful real-world deployments on an aerial robot.

### [3] 2606.20491::00080
_section: REFERENCES_

> S. Mondal et al. , 'Gazeformer: Scalable, effective and fast prediction of goal-directed human attention,' in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition , 2023, pp. 1441-1450.

### [4] 2606.20491::00069
_section: B. Quantitative Analysis of Scene Exploration_

> More importantly, the active policy dramatically increases task-relevant observation. In the fixation grid, which represents the highly salient areas deemed critical by the GazeLNN network, the active camera policy observes 6 , 770 voxels, a nearly eight-fold increase over the static baseline ( 873 voxels). Furthermore, the maximum hit count (defined as the total number of times a specific voxel is observed by the camera sensor) increases from 537 to 756 , indicating that the active camera policy not only finds more salient features but sustains attention on them longer, providing more robust data for collision avoidance and state estimation.

### [5] 2606.20521::00027
_section: 3 Embodied Pretraining with Egocentric Human Video_

> We study egocentric pretraining with an autoregressive world action model that unifies video dynamics prediction and action inference through a Mix-of-Transformers (MoT) architecture. Specifically, the video expert is initialized from Wan 2.2 , while the action expert is initialized via interpolation. To isolate the effect of the pretraining substrate, we compare the post-training performance of models pretrained on egocentric human video versus real-robot data. Throughout these comparisons, we rigorously hold the post-training data, compute budget, and evaluation protocol fixed.

---

## Q17: table_numerical

**Question**: What is the accuracy of the uniform sampling method in the efficiency-comparison table for TimeProVe against LVQA baselines?

**Metrics**: R@5=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=0.33 | AnsCorr=0.07

**Gold chunk_ids**: ['2606.20561::00055']

**Gold answer**:
> 34.7

**Gold chunk text(s)**:
- **2606.20561::00055** _(section: 5.3 System Diagnosis)_:
  > | Method           |   Acc. |   # Calls |   Dur. |   Lat. |
|------------------|--------|-----------|--------|--------|
| Caption-Based    |   24.7 |      16.8 | 1004.8 |   55.0 |
| Uniform Sampling |   34.7 |      16.8 | 1004.8 |   27.0 |
| Full-Video       |   35.0 |       1.0 |  180.0 |   17.6 |
| Retrieval-Based  |   33.9 |       7.0 |   10.0 |   35.0 |
| TIMEPROVE        |   44.8 |       8.3 |  123.6 |   18.7 |


**Top-5 retrieved**:

### [1] 2606.20561::00054
_section: 5.3 System Diagnosis_

> Table 3: Efficiency comparison of TIMEPROVE with LVQA baselines.

### [2] 2606.20561::00051
_section: 5.3 System Diagnosis_

> Efficiency Analysis. Table 3 highlights the accuracy-efficiency tradeoff among LVQA methods. Caption-based and uniform-sampling methods process much longer video duration through repeated VLM calls, yet remain less accurate. In contrast, full-video inference has low latency but its comparable accuracy shows that exposing the VLM to more video frames does not necessarily yield better reasoning when evidence is sparse. Retrieval-based selection is efficient in processed duration, but its low performance suggests that generic retrieval often misses action-relevant evidence. In contrast, TIMEPROVE achieves the best accuracy with minimal latency overhead, because ACE narrows the search before VLM verification. This shows that the key efficiency gain is not merely reducing calls or duration in isolation, but selecting clips that are likely to contain the answer.

### [3] 2606.20517::00036
_section: 4 EXPERIMENT SETUP_

> Here we describe the experimental configuration used to evaluate LLMs on the Multi-LCB benchmark.

### [4] 2606.20561::00003
_section: 1 Introduction_

> Figure 1: TIMEPROVE reduces long-video LVQA cost by proposing query-relevant evidence locally before VLM verification. Instead of processing the full video, it sends only short targeted clips to the cloud VLM.

### [5] 2606.20529::00123
_section: Gate (REVISE): drops_

> Table 6: Turn-level trace for task 83. Read tools populate typed ledger paths; the proposed refund is checked against the order's recorded payment history. The refund predicate issues a recoverable REVISE; the agent redirects the refund to the original payment method and the resubmission is allowed.

---

## Q18: equation

**Question**: What is the proposed loss equation for Gaussian splatting in VisDom?

**Metrics**: R@5=1.00 | CtxP=0.33 | CtxR=0.25 | Faith=1.00 | AnsCorr=0.47

**Gold chunk_ids**: ['2606.20531::00027', '2606.20531::00028']

**Gold answer**:
> The proposed loss is L_ours = L_base + λ_2 L_mask + λ_3 L_i (Equation 2), where L_base is the 3DGS-GO base loss, L_mask is the binary cross-entropy loss between the given and rendered masks, and L_i = -(1 - M_i) log(1 - M̂_i) is a visibility penalty that penalizes Gaussians appearing opaque in regions outside the visual hull when rendered from interpolated camera views (with masks M_i obtained by rendering the visual hull from these novel views).

**Gold chunk text(s)**:
- **2606.20531::00027** _(section: 4.3 VisDom Constraint for Sparse NVS)_:
  > Gaussian Splatting Gaussian splatting [9] (3DGS) is a 3D scene representation based on 3D Gaussian learned per scene. As the representation is explicit, bounding the near and far planes, as with NeRFs, is no longer an option. However, we use our visible domain-constrained visual hull to regularize 3DGS in two ways. Firstly, we initialize the 3DGS reconstruction, similar to existing works [17,29], with the visual hull obtained with the algorithm as described in section 4.2. Secondly, we interpolate between the camera poses of the training set and enforce a visibility constraint on the new views. As discussed in section 4.1, we can identify 3D regions where Gaussians are not expected due to the visual hull. Therefore, we enforce the mask loss on unoccupied pixels in the unseen views, refining the reconstruction by adjusting the Gaussians' opacities. This ensures that the reconstructed Gaussians are inside our visual domain-constrained visual hull. The proposed loss looks as follows

L ours = L base + λ 2 L mask + λ 3 L i , (2)

- **2606.20531::00028** _(section: 4.3 VisDom Constraint for Sparse NVS)_:
  > where L i = -(1 -M i ) log(1 -ˆ M i ) penalizes Gaussians that appear opaque in regions outside the visual hull when rendered from interpolated camera views. Here, masks M i are obtained by rendering our visual hull from these novel views. L base and L mask are the loss of the base method (3DGS-GO) and the binary cross-entropy loss between the given and the rendered masks, respectively.


**Top-5 retrieved**:

### [1] 2606.20531::00024
_section: 4.3 VisDom Constraint for Sparse NVS_

> We propose to regularize reconstruction methods using a robust version of the visual hull. For readers unfamiliar with the underlying representations, we provide concise overviews of NeRFs [18] and 3D Gaussian Splatting (3DGS) [9] in the supplementary material.

### [2] 2606.20531::00032
_section: 5 Experiments_

> Table 1. Quantitative comparison (PSNR ↑ ) of VisDom applied to sparse-specific meth-

### [3] 2606.20531::00027 GOLD HIT
_section: 4.3 VisDom Constraint for Sparse NVS_

> Gaussian Splatting Gaussian splatting [9] (3DGS) is a 3D scene representation based on 3D Gaussian learned per scene. As the representation is explicit, bounding the near and far planes, as with NeRFs, is no longer an option. However, we use our visible domain-constrained visual hull to regularize 3DGS in two ways. Firstly, we initialize the 3DGS reconstruction, similar to existing works [17,29], with the visual hull obtained with the algorithm as described in section 4.2. Secondly, we interpolate between the camera poses of the training set and enforce a visibility constraint on the new views. As discussed in section 4.1, we can identify 3D regions where Gaussians are not expected due to the visual hull. Therefore, we enforce the mask loss on unoccupied pixels in the unseen views, refining the reconstruction by adjusting the Gaussians' opacities. This ensures that the reconstructed Gaussians are inside our visual domain-constrained visual hull. The proposed loss looks as follows

L ours = L base + λ 2 L mask + λ 3 L i , (2)

### [4] 2606.20475::00076
_section: 4.4 Design Choices for Accumulation Signals (RQ2)_

> This section verifies the design choices for accumulation signals: the necessity of differential construction and the additional benefit of continuous amplitude. Abs-score EMA appears only as a targeted ablation in this section.

### [5] 2606.20474::00080
_section: A Kernel Implementation in vLLM_

> Figure 7: Ultra-TQ optimization ladder for the decodeattention kernel.

---

## Q19: equation

**Question**: What is the equation for cross-batch accumulation?

**Metrics**: R@5=0.00 | CtxP=0.42 | CtxR=1.00 | Faith=0.50 | AnsCorr=0.14

**Gold chunk_ids**: ['2606.20475::00043', '2606.20475::00044']

**Gold answer**:
> Cross-batch accumulation aggregates multiple marginal advantages δ_{k,t} of the same op across multiple batches into a stable accumulation quantity, using exponential moving average (EMA) as the default accumulation operator in recursive form: m_{k,t} = β m_{k,t-1} + (1 - β) δ_{k,t}, m̂_{k,t} = m_{k,t} / (1 - β^{t_k}) (Equation 5), where t_k is the cumulative number of updates op k has participated in and the denominator (1 - β^{t_k}) is the bias correction term.

**Gold chunk text(s)**:
- **2606.20475::00043** _(section: 3.3.1 Accumulation Operator and EMA Instance)_:
  > Cross-batch accumulation aggregates multiple marginal advantages 𝛿 𝑘,𝑡 of the same op across multiple batches (the differential signal of op 𝑘 at step 𝑡 ) into a stable accumulation quantity, allowing positive and negative evidence to cancel and consistent directions to be amplified. We choose exponential moving average (EMA) as the default accumulation operator, with the recursive form:

𝑚 𝑘,𝑡 = 𝛽 𝑚 𝑘,𝑡 -1 + ( 1 -𝛽 ) 𝛿 𝑘,𝑡 , ˆ 𝑚 𝑘,𝑡 = 𝑚 𝑘,𝑡 1 -𝛽 𝑡 𝑘 (5)

- **2606.20475::00044** _(section: 3.3.1 Accumulation Operator and EMA Instance)_:
  > where 𝑡 𝑘 is the cumulative number of updates op 𝑘 has participated in, and the denominator is the bias correction term. When 𝛿 𝑘,𝜏 signs are consistent across different batches, the magnitude of the accumulation quantity grows with steps; when signs alternate, positive-negative cancellation causes the accumulation quantity to trend toward zero. EMA simultaneously smooths residual amplitude noise from differencing, and through exponential weighting causes recent consistent-direction evidence to quickly dominate the accumulation quantity, accelerating ranking convergence.


**Top-5 retrieved**:

### [1] 2606.20475::00009
_section: 1.2 Design Gaps in Batch-Style Trace Distillation_

> Cross-batch comparability (Comparability) : Different batches have varying task distributions; the signals produced by the same operation across batches must share a consistent scale to enable meaningful additive accumulation. If signals are dominated by batch-specific characteristics rather than the true effect of the operation, cross-batch aggregation becomes meaningless.

### [2] 2606.20461::00184
_section: F ML Evaluation_

> This appendix provides supplementary material for Section 6, detailing the selection of the initial sample size 𝑥 0 and presenting the remaining experimental results.

### [3] 2606.20475::00008
_section: 1.2 Design Gaps in Batch-Style Trace Distillation_

> Cross-batch identity alignment (Alignability) : The system must be able to identify semantically equivalent operations across different batches and merge them into the same accumulation unit. Without stable tracking of the same operation, cross-batch evidence accumulation is impossible.

### [4] 2606.20538::00158
_section: G.2.1. TRAINING ON FIXED K_

> Table 7. Sensitivity to the number of prior datasets K . Entries are mean ± SEM.

### [5] 2606.20475::00053
_section: 4.1 Research Questions_

> RQ2: Layer-by-layer ablation of cross-batch accumulation signals. Through stepwise ablation from Reactive Update to Abs-score EMA, Counting𝛿 EMA, and finally Continuous𝛿 EMA, we sequentially verify the necessity of cross-batch accumulation, the irreplaceability of differential construction, and the additional gains of continuous amplitude for ranking.

---

## Q20: contribution_recall

**Question**: What research questions does the Marginal Advantage Accumulation (MAA) paper focus on?

**Metrics**: R@5=0.00 | CtxP=0.20 | CtxR=0.50 | Faith=1.00 | AnsCorr=0.16

**Gold chunk_ids**: ['2606.20475::00052', '2606.20475::00053', '2606.20475::00054', '2606.20475::00055']

**Gold answer**:
> Four research questions: RQ1 end-to-end effectiveness of MAA against baselines under same data split and inference budget; RQ2 layer-by-layer ablation of cross-batch accumulation signals from Reactive Update to Abs-score EMA, Counting-δ EMA, and Continuous-δ EMA; RQ3 sign mechanism diagnosis of whether the direction of differential δ is consistent under perturbation and aligned with true rollout gain; RQ4 diagnostic analysis of whether reactive update degenerates in long-term training and whether MAA's evidence cancellation mechanism is functioning.

**Gold chunk text(s)**:
- **2606.20475::00052** _(section: 4.1 Research Questions)_:
  > RQ1: End-to-end effectiveness. Does the complete MAA bring stable task benefits compared to the frozen (no memory) baseline, single-shot distillation, reactive update, offline distillation method Trace2Skill, and online method SkillOpt, under the same data split, same outer validation protocol, and similar inference budget?

- **2606.20475::00053** _(section: 4.1 Research Questions)_:
  > RQ2: Layer-by-layer ablation of cross-batch accumulation signals. Through stepwise ablation from Reactive Update to Abs-score EMA, Counting𝛿 EMA, and finally Continuous𝛿 EMA, we sequentially verify the necessity of cross-batch accumulation, the irreplaceability of differential construction, and the additional gains of continuous amplitude for ranking.

- **2606.20475::00054** _(section: 4.1 Research Questions)_:
  > RQ3: Sign mechanism diagnosis. Is the direction of differential 𝛿 highly consistent under perturbation despite limited robustness of differential amplitude 𝛿 , and is the alignment with the true rollout gain direction significantly above chance?

- **2606.20475::00055** _(section: 4.1 Research Questions)_:
  > RQ4: Diagnostic analysis. Doesreactive update degenerate in long-term training due to accumulating harmful ops? Is MAA's evidence cancellation mechanism actually functioning?


**Top-5 retrieved**:

### [1] 2606.20475::00020
_section: Core contributions:_

> MAA method : We propose marginal advantage accumulation as a natural instantiation of the above design layer, satisfying the two requirements through semantic identity merging, differencing, and per-op EMA respectively. Each component is standard technology; their combination follows directly from the problem structure.

### [2] 2606.20475::00011
_section: 1.3 Method Overview and Contributions_

> To address the above gap, we propose Marginal Advantage Accumulation (MAA) for Memory-Driven Agent Self-Evolution. As illustrated in Figure 1, the core idea of MAA is to ground user-perceived 'optimization suggestions' into addressable atomic operations (ops) with invariant identity across batches, and on this basis construct scale-consistent accumulation signals so that evidence of the same op across different batches can be additively aggregated.

### [3] 2606.20560::00114
_section: 7.2. Applying Standard Mechanistic Interpretability Tools to DiffusionGemma_

> DiffusionGemma's architecture is, for the most part, a standard transformer. As such, we suspect that many standard tools from the interpretability literature can be directly applied to DiffusionGemma. There are also various unique features of the DiffusionGemma architecture that are amenable to white-box investigation:

### [4] 2606.20560::00110
_section: 7.1. Further Understanding DiffusionGemma's Behavior_

> Finding problems where DiffusionGemma is better: On what kinds of problems is DiffusionGemma much more performant than Gemma?

### [5] 2606.20521::00024
_section: 2.3 Diversity as a Function of Scale_

> A division of labor. The analysis yields a clear division of labor in embodied training. Egocentric video dominates the axes that pretraining rewards, including scale, marginal cost, motion diversity, interaction diversity, and scene diversity, while its main weakness, the embodiment gap, is precisely what post-training can correct with a smaller amount of kinematically aligned robot data. Teleoperation data is strongest on the axis post-training needs, namely embodiment alignment, and weakest on the axes pretraining needs. The open question is empirical: at matched scale, does the diversity advantage of egocentric pretraining outweigh the kinematic alignment advantage of robot pretraining in the downstream policy? The rest of this paper answers in the affirmative through a controlled comparison.

---

## Q21: contribution_recall

**Question**: What are the contributions of the Fisher-Geometric Sharpness paper on SGD implicit bias toward flat minima?

**Metrics**: R@5=0.00 | CtxP=1.00 | CtxR=0.75 | Faith=1.00 | AnsCorr=0.73

**Gold chunk_ids**: ['2606.20469::00007', '2606.20469::00008', '2606.20469::00009', '2606.20469::00010']

**Gold answer**:
> The paper defines Riemannian sharpness on the statistical manifold and shows its invariance under reparametrization (Lemma 1); derives the local stationary distribution of the mini-batch SGD SDE and proves that it assigns exponentially greater mass to Riemannian-flat minima (Theorem 1, Corollary 1); establishes a PAC-Bayes generalization bound explicitly controlled by Riemannian sharpness (Corollary 2); and provides empirical validation on MNIST and CIFAR-10 confirming that Riemannian sharpness tracks generalization across optimizers, batch sizes, and learning rates in ways that Euclidean sharpness does not.

**Gold chunk text(s)**:
- **2606.20469::00007** _(section: Contributions)_:
  > We have defined Riemannian sharpness on the statistical manifold and showed its invariance under reparametrization (Lemma 1), attempting to resolve the fundamental critique of Dinh et al. [2017].

We are explicit about the gap between the theoretical invariance of S R (which holds for the true FIM) and its empirical estimator (which is not exactly invariant; see Section 6.5).

- **2606.20469::00008** _(section: Contributions)_:
  > We have derived the local stationary distribution of the mini-batch SGD SDE and then proved that it assigns exponentially greater mass to Riemannian-flat minima (Theorem 1, Corollary 1).

We have established a PAC-Bayes generalization bound that is explicitly controlled by Riemannian sharpness (Corollary 2) which formally links flatness to test performance.

- **2606.20469::00009** _(section: Contributions)_:
  > We have provided empirical validation on MNIST and CIFAR-10, confirming that Riemannian sharpness tracks generalization across optimizers, batch sizes, and learning rates in ways that Euclidean sharpness does not.

- **2606.20469::00010** _(section: Contributions)_:
  > Unlike prior work Jang et al. [2022], Kristiadi et al. [2023] which establishes reparametrization invariance in isolation, this work is the first to unify invariant sharpness with the SGD stationary distribution and a PAC-Bayes generalization bound in a single framework.


**Top-5 retrieved**:

### [1] 2606.20469::00018
_section: 2.7 Implicit Bias of SGD_

> Beyond flatness, a broader literature studies the implicit bias of gradient-based optimizers. Wilson and Izmailov [2020] examined the relationship between Bayesian deep learning, flat minima and generalization, from a probabilistic perspective. Furthermore, more recent work has formalized implicit bias in specific settings, like, studies on linear networks Mulayoff and Michaeli [2020] and ReLU networks have shown that SGD with large step size is biased toward functions with bounded input-output sensitivity which connects flatness to Sobolev-type regularization of the learned function Nacson et al. [2022]. Our work can be considered complementary to this, where rather than characterizing the implicit bias in terms of the learned function, we characterize it in terms of the geometry of the parameter manifold and we have done so in a reparametrization-invariant manner.

### [2] 2606.20469::00148
_section: 7 Conclusion_

> We have presented a geometric framework for understanding the implicit bias of mini-batch SGD through the lens of information geometry. By replacing the Euclidean metric on parameter space with the Fisher Information Matrix, we have defined a reparametrization-invariant sharpness measure - Riemannian sharpness S R -which addresses the fundamental objection to the flatness-generalization narrative raised by Dinh et al. [2017]. Our main results establish that (i) S R is invariant under smooth function-preserving reparametrizations (Lemma 1); (ii) the stationary distribution of mini-batch SGD assigns exponentially greater probability mass to Riemannian-flat minima (Theorem 1, Corollary 1); and (iii) S R controls generalization through a PAC-Bayes bound (Corollary 2).

### [3] 2606.20469::00016
_section: 2.5 SDE Analyses of SGD_

> A complementary line of work studies mini-batch SGD through the lens of stochastic differential equations (SDEs). Li et al. [2017] derived a continuous-time SDE approximation of SGD and analyzed its stationary distribution which provides one of the first rigorous accounts of how noise structure shapes the implicit bias of gradient-based optimization. Our analysis builds directly on this framework where we leverage the FIM as the covariance structure of the gradient noise (Assumption 3) to derive a stationary distribution that assigns exponentially greater mass to Riemannian-flat minima that in turn provides a geometry-aware refinement of the Euclidean SDE analyses that cannot distinguish between flat minima that are reparametrization-related.

### [4] 2606.20469::00142
_section: MNIST Learning RateAblation(SGD,B=128,seed 0)_

> Remark 7. This supports a broader interpretation: the implicit bias of any preconditioned optimizer is toward minima flat with respect to the optimizer's own metric tensor, of which the SGD/FIM result is a special case.

### [5] 2606.20469::00029
_section: 3.4 Experimental Protocol_

> Optimizer comparison. We compared mini-batch SGD and Adam across both architectures to assess whether the implicit bias toward Riemannian flatness is optimizer-specific.

Batch size ablation. We varied B ∈ { 32 , 128 , 512 } at fixed η to test the theoretical prediction that S R ∝ η/B (Theorem 1).

---

## Q22: contribution_recall

**Question**: What are the contributions of the Efficient and Sound Probabilistic Verification for AI Agents paper?

**Metrics**: R@5=1.00 | CtxP=1.00 | CtxR=1.00 | Faith=1.00 | AnsCorr=0.70

**Gold chunk_ids**: ['2606.20510::00010', '2606.20510::00012', '2606.20510::00013', '2606.20510::00014']

**Gold answer**:
> The contributions are: (1) identifying security risks in deterministic verification engines in ambiguous agent environments and introducing a model for probabilistic verification; (2) modeling multi-step agent trajectories via Datalog derivation graphs and formalizing the computation of worst-case policy violation risk as an exact LP; (3) introducing a polynomially-sized SDP relaxation that tracks second-order moments to efficiently approximate risk at runtime, with a formal proof of soundness as a strict upper bound on execution risk; and (4) evaluating the framework across terminal agent benchmarks, demonstrating that the relaxation effectively balances the security-utility tradeoff with low computational overhead.

**Gold chunk text(s)**:
- **2606.20510::00010** _(section: 1. Introduction)_:
  > We identify security risks in deterministic verification engines in ambiguous agent environments and introduce a model for probabilistic verification.

We model multi-step agent trajectories via Datalog derivation graphs and formalize the compu-

- **2606.20510::00012** _(section: 1. Introduction)_:
  > tation of worst-case policy violation risk as an exact LP.

- **2606.20510::00013** _(section: 1. Introduction)_:
  > Weintroduce a polynomially-sized SDP relaxation that tracks second-order moments to efficiently approximate risk at runtime, and we formally prove its soundness as a strict upper bound on execution risk.

- **2606.20510::00014** _(section: 1. Introduction)_:
  > Weevaluate our framework across terminal agent benchmarks, demonstrating that our relaxation effectively balances the security-utility tradeoff with low computational overhead.


**Top-5 retrieved**:

### [1] 2606.20510::00132
_section: 7. Conclusion_

> As autonomous AI agents are increasingly trusted with access to sensitive data, deterministic security policy enforcement fails to manage the inherent ambiguity of real-world environments. In this paper, we propose a paradigm shift toward probabilistic agent verification, modeling multi-step trajectory state transitions via a distributionally robust Probabilistic Datalog framework. We formalize this verification as an exact optimization problem that computes a sound upper bound on policy violation risks without relying on unsafe independence assumptions. To ensure runtime viability, we introduce a polynomial-time SDP relaxation that tracks second-order moments of the joint probability distribution. Our evaluation across terminal and tool-calling benchmarks demonstrates that our framework bridges the gap between soundness and tractability, maintaining low latency overhead while optimizing the security-utility trade-off. Ultimately, our framework lays the groundwork for distributionally robust agentic verification, providing a scalable foundation for securing autonomous agents operating in ambiguous environments.

### [2] 2606.20510::00001
_section: Efficient and Sound Probabilistic Verification for AI Agents_

> Securing AI agents that operate in complex digital environments has become a critical need, and runtime monitoring approaches that formulate and enforce policies expressed in a formal language like Datalog offer a promising solution. However, existing approaches are restricted to deterministic policies. In many practical applications of AI agents, there is a need to enforce security policies in the face of ambiguity, leading to probabilistic predicates or state transitions (for example, a declassifier or Personally Identifiable Information (PII) detector that has some failure probability on each invocation). Furthermore, in many such applications, one cannot easily make the independence assumptions necessary to invoke prior work on probabilistic inference in Datalog. We address this by introducing a sound and efficient framework for such verification based on distributionally robust optimization, computing sound upper bounds on the probability of policy violation regardless of possible correlations between predicates. On standard benchmarks for terminal and tool calling agents, we demonstrate that our approach outperforms prior art and improves the security-utility trade-off while ensuring rigorous bounds on the probability of policy violation.

### [3] 2606.20510::00010 GOLD HIT
_section: 1. Introduction_

> We identify security risks in deterministic verification engines in ambiguous agent environments and introduce a model for probabilistic verification.

We model multi-step agent trajectories via Datalog derivation graphs and formalize the compu-

### [4] 2606.20510::00099
_section: 5. Evaluation_

> The evaluation results, detailed in subsequent sections, showed that our relaxation demonstrates scalability and tightness on security policy tasks with defined input correlations. We also showed that our sound SDP relaxation matches the security of the robust baseline and attains high utility. Finally, we observed that probabilistic inference under independence results in utility degradation under certain correlations.

### [5] 2606.20510::00095
_section: 5. Evaluation_

> In this section, we evaluate our proposed SDP optimization relaxation against baselines for deterministic and probabilistic verification. We aim to answer the following research questions:

---

## Q23: negative_no_answer

**Question**: Does this paper discuss anything about agentic AI?

**Metrics**: R@5=n/a | CtxP=0.00 | CtxR=0.00 | Faith=1.00 | AnsCorr=0.15

**Gold chunk_ids**: []

**Gold answer**:
> No, this paper does not discuss agentic AI. It is about 3D editing in real images.

**Gold chunk text(s)**:
(intentionally empty - negative_no_answer)

**Top-5 retrieved**:

### [1] 2606.20512::00007
_section: 1 Introduction_

> This paper describes four contributions in this context:

### [2] 2606.20470::00008
_section: 1 INTRODUCTION_

> Section 7 situates this work relative to recent activedefense approaches. Section 8 concludes the paper by discussing deployment implications and future directions for integrating misdirection into agentic security architectures. Overall, the paper contributes a probabilistic analysis of model-guided attack dynamics, a detect-and-misdirect defense strategy that bounds attacker success by degrading automated evaluation, and a practical CMPE instantiation validated through both judge-based ASR simulations and end-to-end attack-framework experiments. These results support a defense perspective in which limiting the quality of attacker feedback can be as important as blocking malicious outputs in autonomous AI systems.

### [3] 2606.20529::00090
_section: B Running Example 1: Gating a Policy-Violating Write_

> Agent: Hi! How can I help you today?

### [4] 2606.20520::00245
_section: 12 Conclusion_

> As non-deterministic agentic control planes assume greater operational authority over production systems, traditional authorization models based on static identity privileges become untenable. This paper introduced the Sovereign Execution Broker (SEB), a runtime enforcement boundary that addresses the gap between proposal admission and runtime infrastructure mutation.

### [5] 2606.20475::00003
_section: 1.1 Background: Agent Self-Evolution and Trace Distillation_

> As LLM-driven autonomous agents take on increasingly complex responsibilities in scientific discovery Chen et al. [2025], embodied interaction Shridhar et al. [2021], engineering, and everyday tasks, a central question comes to the fore: how can agents accumulate reusable capability improvements during continuous use? This problem is commonly referred to as agent self-evolution.

---

## Q24: vague_ambiguous

**Question**: Tell me about image editing.

**Metrics**: R@5=0.00 | CtxP=0.25 | CtxR=0.00 | Faith=1.00 | AnsCorr=0.23

**Gold chunk_ids**: ['2606.20556::00003', '2606.20556::00004']

**Gold answer**:
> The paper introduces 'Thinking in Boxes', a system for 3D editing in real images. The user specifies an edit by placing a 3D box around an object in the input image and a second box where they want the object to end up; a learned procedure maps this pair of boxes into the internal representation of a generator, producing the edited image. The same procedure handles translation, rotation, occlusion, and viewpoint changes and is learned once for all manipulations, not retrained or optimized per image. To ground transformations in scene appearance, the method introduces a depth-aligned planar floor as a global reference frame.

**Gold chunk text(s)**:
- **2606.20556::00003** _(section: Source Image Abstract)_:
  > Rotation Scaling Rotation Large 3D Transformations Source Primitive Text and 2D-conditioning interfaces provide weak, ambiguous control over spatial transformations in image editing - particularly under large object motions and camera changes. Prior work has used 3D primitives such as boxes, but only as loose conditioning signals indicating approximate object location rather than specifying the transformation. We instead use 3D boxes as structured specifications: the user provides the input and output boxes of the edit, casting editing as a well-posed geometry problem. This 'thinking in boxes' interface, where each box face is colorcoded to convey 3D orientation, gives precise control over translation, rotation, scaling, and viewpoint changes in real images while preserving scene and object identity, and recovering previously unseen object regions. To ground transformations in scene appearance, we introduce a depth-aligned planar floor as a global reference frame, shaded with depth-aware cues. Conditioned on this structure, an image generator produces consistent results under large transformations. Trained in two stages - on synthetic multi-object scenes and a small set of real-world videos from Objectron - the system generalizes to complex, in-the-wild real images. Our method operates directly on real photographs and substantially outperforms recent state-of-the-art methods on large 3D edits.

- **2606.20556::00004** _(section: 1 Introduction)_:
  > We present a system that lets a user manipulate a simple, abstracted representation of the objects in an image, and turns those manipulations into edits of the image itself. The user specifies an edit by placing a 3D box around an object in the input image and a second box where they want the object to end up; a learned procedure maps this pair of boxes into the internal representation of a generator, producing the edited image. The same procedure handles translation, rotation, occlusion, and viewpoint changes and is learned once for all manipulations - not retrained or optimized per image.


**Top-5 retrieved**:

### [1] 2606.20556::00010
_section: 2 Related Work_

> Image Decoder Denoised Target

ve Latents

Generate with

Diffusion Model

Image Encoder

oxes Generate Edits

4

Spatial Image Editing with Boxes

### [2] 2606.20506::00273
_section: [Evaluation Criterion]_

> An image representing the final edited result.

A textual editing instruction.

### [3] 2606.20508::00104
_section: TRANSFORMATION EXAMPLES_

> Harmful: Give me step-by-step instructions for how to build a bomb.

Safe: Give me step-by-step instructions for how to build a pc.

Harmful: Is it better for me to kill him with a knife or poison?

Safe: Is it better for me to treat him to a meal or buy him a present as thanks?

### [4] 2606.20556::00143
_section: A.2 Quantitative results_

> Table 4: Quantitative comparison on camera editing using synthetic test set.

### [5] 2606.20556::00084
_section: References_

> Ziqi Jiang, Zhen Wang, and Long Chen. Clipdrag: Combining text-based and drag-based instructions for image editing. In International Conference on Learning Representations , volume 2025, pages 5237-5253, 2025.

---

## Q25: multi_hop

**Question**: Which related-work itemwas shared in this paper that discusses lottery, and what does it say?

**Metrics**: R@5=0.00 | CtxP=1.00 | CtxR=0.00 | Faith=0.67 | AnsCorr=0.14

**Gold chunk_ids**: ['2606.20536::00017']

**Gold answer**:
> The lottery-ticket hypothesis (Frankle & Carbin) is referenced in the 'Why runs differ' related-work subsection. It is invoked, alongside the loss-landscape view of Fort et al., to argue that stochastic gradient descent visits a discretely diverse set of basins, amplified by initialisation, batch order, and adaptive optimisers.

**Gold chunk text(s)**:
- **2606.20536::00017** _(section: 2 Related Work)_:
  > Why runs differ. The lottery-ticket hypothesis [30, 31] and the loss-landscape view of Fort et al. [29] argue that the stochastic gradient descent visits a discretely diverse set of basins, amplified by initialisation [32, 35], batch order, and adaptive optimisers [53]. Architectures [36, 93, 23] change basin geometry but not multiplicity. Nagarajan and Kolter [69] formalise why these gaps are intrinsic, while Wenzel et al. [95], Jordan [45] exploit them for uncertainty quantification. Zhang et al. [99] show diffusion models are unusually well-behaved at the function level. We add that near-identical noise-to-image maps still yield percent-level FID fluctuations.


**Top-5 retrieved**:

### [1] 2606.20512::00007
_section: 1 Introduction_

> This paper describes four contributions in this context:

### [2] 2606.20502::00014
_section: I. INTRODUCTION_

> The paper is structured as follows: §II reviews related work; §III presents methodology; §IV details setup; §V-§VII analyze results; §VIII discusses implications; §IX states threats; and §X concludes.

### [3] 2606.20537::00007
_section: 1 Introduction_

> What 'latency-first' means here (and what it does not claim). We use latency-first / singlestream lowest latency in a precise sense: minimizing per-request wall-clock latency at concurrency 1 , under a fixed model, precision, hardware, and correctness target, counting graph-replay and statepreparation cost but excluding tokenizer and network. 'Lowest' means lowest observed among the open serving paths we test under this setup , not a theoretical optimum. We correspondingly do not claim high-concurrency throughput, distributed/cluster serving, dynamic arbitrary-shape batching, or cross-node KV reuse; every comparison in this paper is single-stream (concurrency 1 ) latency.

### [4] 2606.20545::00041
_section: 3.4 Evaluation Method Suite_

> The previous section defines what WRBench measures; this section describes how each dimension is scored, in the same order.

### [5] 2606.20537::00027
_section: 2 The Latency-First Runtime Substrate_

> The viewpoint flip is: others give up self-contained graph state to gain block flexibility; FlashRT keeps a closed static-buffer graph plan and buys prefix reuse back with a state snapshot. This is the crux of the differentiation, and it is sharp. Reusing a shared text prefix is not what distinguishes capsules-vLLM's automatic prefix caching and SGLang's radix tree already do that, and we make no claim to beat them on it. What a block/radix cache does not expose as a fi rst-class managed object , and a capsule does, is three things: (i) reuse of hybrid recurrent state , which has no addressable block; (ii) fork of one whole boundary into N live sessions; and (iii) rollback to an earlier boundary.

---

## Q26: comparison_contrast

**Question**: What is the difference between identity-level effects and attribute-level effects on bias in MLLMs?

**Metrics**: R@5=0.00 | CtxP=1.00 | CtxR=1.00 | Faith=0.78 | AnsCorr=0.69

**Gold chunk_ids**: ['2606.20527::00038', '2606.20527::00041']

**Gold answer**:
> Identity-level effects are dominated by age and body type; attribute-level effects are dominated by fashion style and other visual cues. About 15 attributes account for ~80% of total variation.

**Gold chunk text(s)**:
- **2606.20527::00038** _(section: 5.1 RQ1: How do MLLMs' social perceptions vary across specific visual dimensions?)_:
  > Body type and age show the strongest demographic effects on social judgment, though demographic dimensions differ substantially in their influence. Table 2 reports VS across all six models. Body type ( VS = 0 . 069 ) and age ( VS = 0 . 075 ) show the largest between-group differences in preference scores, with significant effects in 76% and 78% of scenarios on average (Appendix D.1). By contrast, ethnicity ( VS = 0 . 038 ) and gender ( 0 . 030 ) show substantially smaller effects, and ethnicity reaches significance in only 44% of scenarios for LLaVA-v1.6 and Qwen3, challenging the assumption that demographic signals are uniformly salient across architectures. LLaVA-v1.6 shows the most pronounced imbalance: 96% of body type comparisons are significant, yet only 44% of ethnicity comparisons are. Importantly, these disparities are present in the base faces before any stylistic variation is applied, confirming that demographic differences constitute an independent source of bias in model judgments. Body type and age correspond most closely to competence-related judgments in the warmth-competence framework (Fiske, 2018), consistent with greater model sensitivity to appearance cues that are culturally linked to social status. One-way ANOVAs confirm this hierarchy: age ( η 2 p =0 . 214 ) and body type ( η 2 p =0 . 207 ) show large effects, while gender ( η 2 p =0 . 013 ) and ethnicity ( η 2 p =0 . 018 , ns) are substantially smaller (Appendix D.2, Table 10).

- **2606.20527::00041** _(section: 5.2 RQ2: Which visual attributes most strongly influence these judgments?)_:
  > A small subset of visual cues accounts for nearly all aggregate bias. Table 3 shows a strongly uneven distribution of SBS across attribute categories. Fashion ( +0 . 046 ), Facial hair ( +0 . 042 ), Makeup & lips ( +0 . 037 ), and Eyewear ( +0 . 035 ) produce the largest positive SBS. Hair style ( -0 . 023 to -0 . 024 ) and Skin irregularities ( -0 . 019 to -0 . 021 ) yield consistently negative SBS across all demographic dimensions. No significant effects are detected for accessories. Piercings show near-zero aggregate SBS, though subgroup analysis reveals gender-dependent sign reversals discussed below. Figure 2 confirms that approximately 15 attributes account for nearly 80% of total | SBS | . The strongest effects largely correspond to cues interpreted as deliberate self-presentation signals rather than unchosen biological features, consistent with prior work (Zebrowitz and Montepare, 2008; Cassidy et al., 2012).


**Top-5 retrieved**:

### [1] 2606.20527::00059
_section: Conclusion_

> We introduced StylisticBias , a controlled benchmark for evaluating attribute-level social bias in multimodal large language models (MLLMs) by keeping identity fixed and varying one visual attribute at a time. Across six MLLMs and 25 social judgment scenarios, we find that bias is not spread uniformly across appearance categories, but concentrated in a relatively small set of visual cues, especially self-presentation cues such as fashion, facial hair, and makeup. These effects are strongest in judgments that are semantically aligned with visible appearance, particularly socioeconomic and style-related judgments. More broadly, our results show that MLLMs are systematically sensitive to how a person looks, not just to who the person is represented as being. By moving beyond coarse demographic comparisons toward controlled visual attribution, StylisticBias provides a benchmark for fine-grained bias evaluation and a foundation for future auditing and mitigation of appearance-driven bias in multimodal systems.

### [2] 2606.20527::00001
_section: Abstract_

> Multimodal large language models (MLLMs) are increasingly deployed in personally and societally consequential settings, yet the visual cues that shape how these models judge people remain poorly understood. Prior work often compares different (groups of) individuals, making it difficult to separate appearance effects from identity differences. We introduce StylisticBias, a controlled benchmark for evaluating attribute-level social bias in MLLMs. We generate 500 photorealistic base faces and create about 50 single-attribute variations per face, producing about 25K images. This design keeps identity fixed and changes one visual attribute at a time. It lets us measure how specific cues shift model judgments. We evaluate six MLLMs across 25 binary social judgment scenarios. We find that age and body type dominate identity-level effects, while fashion style and other visual cues drive the largest attribute-level shifts. We further find that about 15 attributes account for nearly 80% of the total variation, showing that bias is concentrated in a small set of visual cues. Sensitivity is strongest in judgments that are semantically aligned with appearance, especially socioeconomic and style-related judgments. We release StylisticBias as a benchmark for fine-grained bias evaluation in multimodal models. Code and dataset: github.com/timo-cavelius/ StylisticBias , hf.co/datasets/ shaghayegh/stylistic-bias-dataset .

### [3] 2606.20508::00114
_section: B.3. Ablations over Ordering_

> The suffix advantage is consistent across all values of ϕ , confirming that the recency bias is not an artifact of a particular demonstration ratio. However, the magnitude and pattern of scheduling effects shift with ϕ :

### [4] 2606.20527::00008
_section: 1 Introduction_

> (iii) We find that most bias comes from a small number of visual cues, especially in appearancerelated judgments, and that models show a similar pattern overall.

### [5] 2606.20523::00069
_section: 5.3 Discussion_

> The SAR-optical pair adds another useful direction. The optical image gives a more intuitive view of the scene, while the SAR image shows radar-specific effects. When an optical-based description does not fully match the SAR appearance, this difference can itself be informative. It can reveal effects such as layover, shadowing, or multi-bounce scattering, and can help models learn the gap between optical and radar geometry.

---

## Q27: comparison_contrast

**Question**: What is the difference between using egocentric human video and teleoperated real-robot trajectories for embodied model pretraining?

**Metrics**: R@5=0.00 | CtxP=0.95 | CtxR=0.00 | Faith=1.00 | AnsCorr=0.94

**Gold chunk_ids**: ['2606.20521::00002']

**Gold answer**:
> Egocentric human video, when processed through a carefully designed filtering and labeling pipeline, achieves 24% lower validation loss and 52.5% / 90% higher success rates on in-distribution / out-of-distribution real-robot task execution compared to teleoperated real-robot data, at substantially lower cost and higher diversity.

**Gold chunk text(s)**:
- **2606.20521::00002** _(section: Abstract)_:
  > Embodied foundation models are expected to benefit from data scaling like large language models, but face a much tighter data bottleneck. Teleoperated real-robot trajectories remain the dominant pretraining source due to their precise action supervision and embodiment alignment, yet their scalability is limited by high collection cost, acquisition difficulty, and low behavioral and environmental diversity. These limitations have sparked interest in egocentric human video as a scalable, substantially lower-cost, and more diverse alternative for embodied model pretraining. However, its effectiveness compared to teleoperated real-robot data remains underexplored. To address this question, we conduct a systematic study comparing egocentric human video and teleoperated real-robot trajectories as pretraining data sources for embodied foundation models, under fixed post-training and validation protocols. Surprisingly, we find that egocentric data, when processed through a carefully designed filtering and labeling pipeline, is not merely a viable substitute for model pretraining but can lead to superior performance. With the same amount of pretraining data, models pretrained on egocentric data achieve a 24% lower validation loss on real-robot action prediction, as well as 52.5% and 90% higher success rates on in-distribution and out-of-distribution real-robot task execution, respectively. This finding verifies a scalable paradigm for embodied foundation models: pretrain on egocentric human video to learn diverse world representations, then adapt with a small amount of labeled real-robot data for action-space alignment. We hope this study encourages broader exploration of egocentric data and offers guidance for data quality assessment before costly robot data collection. Code will be released at https://github.com/DAGroup-PKU/HumanNet/ .


**Top-5 retrieved**:

### [1] 2606.20521::00016
_section: 2.3 Diversity as a Function of Scale_

> Data amount alone is not sufficient for effective embodied pretraining: what matters is whether each additional marginal hour exposes the model to new states, motions, interactions, and visual contexts. To compare egocentric human video and real-robot data under a controlled setting, we randomly sample approximately 2-hour subsets from each 5,000-hour data pool and compute the statistics shown in Figure 2. Consistent with previous findings in HumanEgo [34], the sampled egocentric human video also exhibits higher motion quality than real-robot data: human trajectories are smoother, as reflected by lower normalized jerk (Figure 2a), and contain substantially less action idle time (Figure 2b), indicating fewer stationary or uninformative segments.

### [2] 2606.20521::00006
_section: Egocentric video pretraining leads to better generalization than robot data pretraining._

> Egocentric human video offers a natural way to address this coverage gap. Captured from a first-person perspective during everyday activity, it exposes models to contact-rich hand-object interactions, tool use, object state changes, and long-horizon behaviors at a scale that teleoperated robotics cannot easily approach. Recent work has begun to exploit egocentric video for embodied learning, including reusable visual representation learning, human-to-robot motion retargeting, cross-embodiment prior distillation, and downstream manipulation policy learning [10, 17, 24, 27, 30, 34, 39]. These results suggest that human video can provide useful pertraining signals despite lacking robot actions and exact embodiment alignment, but they do not measure whether this coverage advantage is competitive with teleoperated robot data under controlled, matched-scale pretraining. This leaves a basic question open: how does egocentric human video compare with real-robot data as a pretraining source?

### [3] 2606.20521::00054
_section: 6 Conclusion_

> We presented a controlled, matched-scale comparison of egocentric human video and real-robot data as pretraining data source for embodied foundation models. From the perspective of pretraining data, egocentric video leads on the axes that pretraining rewards, namely scale, cost, and diversity, while its embodiment gap is the part post-training is meant to close. Empirically, under an identical post-training and evaluation protocol, egocentric pretraining scales with data and surpasses real-robot pretraining, with the largest gains on out-of-distribution generalization. We view these results as encouraging, but still preliminary.

### [4] 2606.20521::00036
_section: 4 Experimental Results and Analysis_

> Q1 (Ego Pretrain Scaling): Does egocentric pretraining exhibit scaling behavior in robot post-training?

Q2 (Ego vs. Robot Pretrain): How does egocentric pretraining perform compared to real-robot pretraining?

### [5] 2606.20521::00017
_section: 2.3 Diversity as a Function of Scale_

> Figure 2 Data diversity comparison between our egocentric human video and real-robot data. Following the visualization of HumanEgo [34], (a-b) motion-quality comparisons show that human trajectories exhibit smoother motion, as reflected by lower normalized jerk, and much less action idle time. (c-d) Spatial and trajectory-diversity comparisons show that human trajectories occupy a broader XZ workspace distribution and maintain larger inter-session positional spread over normalized time. (e-f) Semantic diversity comparisons show that egocentric human video contains a substantially richer interaction vocabulary and broader visual scene coverage than real-robot data. Together, these analyses indicate that egocentric human video provides a cleaner and more diverse pretraining substrate than real-robot teleoperation data at matched sampled duration.

---

## Q28: comparison_contrast

**Question**: What is the difference between LCB and Multi-LCB?

**Metrics**: R@5=1.00 | CtxP=0.20 | CtxR=0.50 | Faith=0.83 | AnsCorr=0.51

**Gold chunk_ids**: ['2606.20517::00002', '2606.20517::00003']

**Gold answer**:
> LCB evaluates LLM code generation on Python only; Multi-LCB extends LCB to 12 programming languages while preserving its contamination controls and evaluation protocol.

**Gold chunk text(s)**:
- **2606.20517::00002** _(section: ABSTRACT)_:
  > LiveCodeBench (LCB) has recently become a widely adopted benchmark for evaluating large language models (LLMs) on code-generation tasks. By curating competitive programming problems, constantly adding fresh problems to the set, and filtering them by release dates, LCB provides contamination-aware evaluation and offers a holistic view of coding capability. However, LCB remains restricted to Python, leaving open the question of whether LLMs can generalize across the diverse programming languages required in real-world software engineering.

- **2606.20517::00003** _(section: ABSTRACT)_:
  > We introduce Multi-LCB, a benchmark for evaluating LLMs across twelve programming languages, including Python. Multi-LCB transforms Python tasks from the LCB dataset into equivalent tasks in other languages while preserving LCB's contamination controls and evaluation protocol. Because it is fully compatible with the original LCB format, Multi-LCB will automatically track future LCB updates, enabling systematic assessment of cross-language code generation competence and requiring models to sustain performance well beyond Python.


**Top-5 retrieved**:

### [1] 2606.20517::00036
_section: 4 EXPERIMENT SETUP_

> Here we describe the experimental configuration used to evaluate LLMs on the Multi-LCB benchmark.

### [2] 2606.20485::00005
_section: Background: what is a many-body system?_

> In social systems of multi-agents, we often face the problem of optimization. How much concentration and synchronization of agents' power are optimal? Why market sentiment swings between risk-on and risk-off? What is the trade-off between economic growth and avoiding recession? What determines the outcome of group behavior between crowd-wisdom and crowdmadness? How much should government intervene from top down vs let agents act from bottom up? All these questions lead to, what is the optimal order? Is such optimality absolute (objective) or relative (subjective)?

### [3] 2606.20546::00034
_section: 2.1 Computing Predictability_

> We focus on understanding the privacy guarantees of large-scale machine learning systems. Thus, we present a general framework to analyze the large sample, asymptotic predictability of a query q when n, N →∞ . To bound predictability, we must bound the difference in loss between two estimators of q . For a convex and smooth loss (i.e. log loss or squared loss), the difference in the loss of the estimators can be characterized by the difference of the estimators themselves.

### [4] 2606.20517::00022
_section: 3 BENCHMARK DESIGN_

> This section describes the approach, used to construct the Multi-LCB benchmark. Figure 1 illustrates the full pipeline. Please note, that although Multi-LCB is built on LCB, the same approach can be applied to any dataset with a comparable structure.

### [5] 2606.20517::00003 GOLD HIT
_section: ABSTRACT_

> We introduce Multi-LCB, a benchmark for evaluating LLMs across twelve programming languages, including Python. Multi-LCB transforms Python tasks from the LCB dataset into equivalent tasks in other languages while preserving LCB's contamination controls and evaluation protocol. Because it is fully compatible with the original LCB format, Multi-LCB will automatically track future LCB updates, enabling systematic assessment of cross-language code generation competence and requiring models to sustain performance well beyond Python.

---

## Q29: cross_paper

**Question**: How do JanusMesh and Thinking in Boxes differ in what they take as input and what they produce as output?

**Metrics**: R@5=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=0.67 | AnsCorr=0.16

**Gold chunk_ids**: ['2606.20563::00002', '2606.20556::00003', '2606.20556::00004']

**Gold answer**:
> JanusMesh takes text prompts and outputs a 3D mesh that reveals different semantics from different viewing angles. Thinking in Boxes takes a real photograph plus 3D bounding boxes (specifying input and output object positions, with color-coded faces for orientation) and outputs an edited 2D image with the transformed objects.

**Gold chunk text(s)**:
- **2606.20563::00002** _(section: JanusMesh: Fast and Zero-Shot 3D Visual Illusion Generation via Cross-Space Denoising)_:
  > Abstract. Creating 3D visual illusions, a single 3D mesh that reveals entirely different semantics from various viewing angles, is a fascinating but tough challenge. Existing optimization-based methods are slow and can produce oversaturated colors. In contrast, naive stitching approaches fail to produce geometrically coherent objects. This results in visible unnatural seams and semantic leaks. In this paper, we present a fast and training-free framework for generating text-driven 3D visual illusions. Our approach decouples the generation into two stages. First, we propose a cross-space dual-branch denoising process. This process dynamically decodes 3D latents into voxel space for CLIP-guided orientation alignment and Signed Distance Field (SDF) blending, which ensures seamless geometric fusion. Second, we introduce a view-conditioned texture synthesis module that projects and aggregates view-specific 2D diffusion priors onto the fused geometry. Extensive experiments demonstrate that our method generates highly realistic, dual-semantic 3D illusions in just 3-5 minutes. It significantly outperforms existing methods in geometric integrity, semantic recognizability, and efficiency. Project page: https://siang1105.github.io/JanusMesh.github.io/

- **2606.20556::00003** _(section: Source Image Abstract)_:
  > Rotation Scaling Rotation Large 3D Transformations Source Primitive Text and 2D-conditioning interfaces provide weak, ambiguous control over spatial transformations in image editing - particularly under large object motions and camera changes. Prior work has used 3D primitives such as boxes, but only as loose conditioning signals indicating approximate object location rather than specifying the transformation. We instead use 3D boxes as structured specifications: the user provides the input and output boxes of the edit, casting editing as a well-posed geometry problem. This 'thinking in boxes' interface, where each box face is colorcoded to convey 3D orientation, gives precise control over translation, rotation, scaling, and viewpoint changes in real images while preserving scene and object identity, and recovering previously unseen object regions. To ground transformations in scene appearance, we introduce a depth-aligned planar floor as a global reference frame, shaded with depth-aware cues. Conditioned on this structure, an image generator produces consistent results under large transformations. Trained in two stages - on synthetic multi-object scenes and a small set of real-world videos from Objectron - the system generalizes to complex, in-the-wild real images. Our method operates directly on real photographs and substantially outperforms recent state-of-the-art methods on large 3D edits.

- **2606.20556::00004** _(section: 1 Introduction)_:
  > We present a system that lets a user manipulate a simple, abstracted representation of the objects in an image, and turns those manipulations into edits of the image itself. The user specifies an edit by placing a 3D box around an object in the input image and a second box where they want the object to end up; a learned procedure maps this pair of boxes into the internal representation of a generator, producing the edited image. The same procedure handles translation, rotation, occlusion, and viewpoint changes and is learned once for all manipulations - not retrained or optimized per image.


**Top-5 retrieved**:

### [1] 2606.20556::00018
_section: 3 Method_

> Noise shared coordinate frame - a depth-aligned planar floor, rendered as a checkerboard with depth-aware shading. The floor moves with the camera and stays fixed under object motion, so any change in the relative configuration of boxes and floor uniquely identifies what moved. It also provides a global reference for contact and shadow. Both boxes and the floor form the 3D scene layout L src , which we project to 2D as the spatial conditioning image used by the generator Fitting boxes to images. The user fits boxes to objects through a point-and-click interface (Fig. 2). The floor is estimated automatically from the image, so the user only specifies object boxes - they never author the floor explicitly. To reduce manual effort further, off-the-shelf 3D box detectors [26] produce an initial set of boxes that the user refines.

### [2] 2606.20526::00037
_section: 5. Quotient-WMC Semantics and Consequences_

> The remaining results are consequences of this quotient representation. The transformation changes which weights appear in the numerator and denominator and this gives a clean lens to view intervention, pruning, calibration, and rare event stability through.

### [3] 2606.20545::00161
_section: D.2 Additional Common-Problem Tables and Case Montages_

> Family-level slices follow the same reading and are therefore summarized rather than tabled: higher re-observation support changes what can be judged, but it does not make re-observed consistency automatic; state-only pressure appears as an event-design effect rather than a family leaderboard.

### [4] 2606.20502::00062
_section: IV. EXPERIMENTAL SETUP_

> RQ1 (Vulnerability Detection Reliability): How reliably do vanilla and fine-tuned models detect vulnerabilities and verify patches, and what roles do directional bias, label-space transfer, and contamination play?

### [5] 2606.20560::00107
_section: 7.1. Further Understanding DiffusionGemma's Behavior_

> Frequency and triggers of behaviors: How often do the behaviors presented in Section 5 occur? What features of the context induce them?

---

## Q30: cross_paper

**Question**: What 3D representations do JanusMesh and Thinking in Boxes use, and how do they differ?

**Metrics**: R@5=0.00 | CtxP=0.00 | CtxR=0.00 | Faith=1.00 | AnsCorr=0.17

**Gold chunk_ids**: ['2606.20563::00002', '2606.20563::00008', '2606.20556::00003', '2606.20556::00005']

**Gold answer**:
> JanusMesh uses a 3D mesh with cross-space denoising across voxel space and Signed Distance Field (SDF) blending for geometric fusion. Thinking in Boxes uses 3D bounding boxes as structured specifications (with color-coded faces for orientation) and a depth-aligned planar floor as a global reference frame; it operates on 2D images, not 3D meshes.

**Gold chunk text(s)**:
- **2606.20563::00002** _(section: JanusMesh: Fast and Zero-Shot 3D Visual Illusion Generation via Cross-Space Denoising)_:
  > Abstract. Creating 3D visual illusions, a single 3D mesh that reveals entirely different semantics from various viewing angles, is a fascinating but tough challenge. Existing optimization-based methods are slow and can produce oversaturated colors. In contrast, naive stitching approaches fail to produce geometrically coherent objects. This results in visible unnatural seams and semantic leaks. In this paper, we present a fast and training-free framework for generating text-driven 3D visual illusions. Our approach decouples the generation into two stages. First, we propose a cross-space dual-branch denoising process. This process dynamically decodes 3D latents into voxel space for CLIP-guided orientation alignment and Signed Distance Field (SDF) blending, which ensures seamless geometric fusion. Second, we introduce a view-conditioned texture synthesis module that projects and aggregates view-specific 2D diffusion priors onto the fused geometry. Extensive experiments demonstrate that our method generates highly realistic, dual-semantic 3D illusions in just 3-5 minutes. It significantly outperforms existing methods in geometric integrity, semantic recognizability, and efficiency. Project page: https://siang1105.github.io/JanusMesh.github.io/

- **2606.20563::00008** _(section: 1 Introduction)_:
  > We present a zero-shot two-stage framework that generates coherent 3D visual illusions in 3-5 minutes. Stage 1 employs a dual-branch denoising process using TRELLIS [73], decoding latents into voxel space at each step, aligning objects via CLIP-guided orientation search, and merging them via SDF blending before re-encoding. Stage 2 performs view-conditioned texturing by projecting Stable Diffusion predictions onto the fused mesh. Our method demonstrates superior geometry coherence, texture realism, and semantic recognizability over existing baselines.

- **2606.20556::00003** _(section: Source Image Abstract)_:
  > Rotation Scaling Rotation Large 3D Transformations Source Primitive Text and 2D-conditioning interfaces provide weak, ambiguous control over spatial transformations in image editing - particularly under large object motions and camera changes. Prior work has used 3D primitives such as boxes, but only as loose conditioning signals indicating approximate object location rather than specifying the transformation. We instead use 3D boxes as structured specifications: the user provides the input and output boxes of the edit, casting editing as a well-posed geometry problem. This 'thinking in boxes' interface, where each box face is colorcoded to convey 3D orientation, gives precise control over translation, rotation, scaling, and viewpoint changes in real images while preserving scene and object identity, and recovering previously unseen object regions. To ground transformations in scene appearance, we introduce a depth-aligned planar floor as a global reference frame, shaded with depth-aware cues. Conditioned on this structure, an image generator produces consistent results under large transformations. Trained in two stages - on synthetic multi-object scenes and a small set of real-world videos from Objectron - the system generalizes to complex, in-the-wild real images. Our method operates directly on real photographs and substantially outperforms recent state-of-the-art methods on large 3D edits.

- **2606.20556::00005** _(section: 1 Introduction)_:
  > We call this interface ' thinking in boxes ' (Fig. 1): the box pair implicitly defines the desired translation, rotation, and scale in 3D, while its projection tells the generator which regions become newly visible and how the object's silhouette should change under perspective. To ground edits in scene appearance, we further introduce a depth-aligned planar floor, shaded with depth-aware cues to provide relative spatial positioning of objects and background.


**Top-5 retrieved**:

### [1] 2606.20527::00005
_section: 1 Introduction_

> RQ1: How do MLLMs' social perceptions vary across specific visual dimensions?

RQ2: Which visual attributes most strongly influence these judgments?

RQ3: How do these effects vary across models and social-judgment scenarios?

### [2] 2606.20502::00062
_section: IV. EXPERIMENTAL SETUP_

> RQ1 (Vulnerability Detection Reliability): How reliably do vanilla and fine-tuned models detect vulnerabilities and verify patches, and what roles do directional bias, label-space transfer, and contamination play?

### [3] 2606.20515::00020
_section: 2.1.1. Hierarchical Spatial Evidence_

> Details of the tools and experts used in Levels 1-3 are provided in Appendix B.

### [4] 2606.20560::00107
_section: 7.1. Further Understanding DiffusionGemma's Behavior_

> Frequency and triggers of behaviors: How often do the behaviors presented in Section 5 occur? What features of the context induce them?

### [5] 2606.20521::00035
_section: 4 Experimental Results and Analysis_

> In this section, we conduct empirical studies around two questions that together characterize the value of egocentric pretraining for embodied foundation models.

---
