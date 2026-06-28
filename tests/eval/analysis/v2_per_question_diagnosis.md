# Mini-RAG v2 per-question diagnosis

Generated from the v2 hybrid run (commit `e4412e9`, config_hash `735da861`). For each of the 30 golden-set questions, this records what actually happened during retrieval and what fix (if any) is the right tool for the failure mode.

**Metric legend**: R@5 = strict-match Recall@5 against gold_chunk_ids. CtxP = RAGAS context_precision (LLM judge: were retrieved chunks relevant?). CtxR = RAGAS context_recall (LLM judge: was gold answer reconstructible?). The gap between R@5 and CtxP/CtxR is the diagnostic: high CtxP with R@5=0 means retrieval found relevant content but in different chunks than we marked as gold.

**Fix categories**:
- **OK**: question already works, no fix needed.
- **CROSS-ENCODER**: right paper is found but the specific best-matching chunk isn't ranked in top-5. Cross-encoder reranking would push the right chunk above the noisier ones.
- **CONTEXTUAL CHUNKING**: the right paper isn't even retrieved because the question's anchor (paper name, acronym) doesn't appear in the gold chunk's text. Prepending paper title + section heading to chunk text before embedding fixes this.
- **AGENT**: out of single-pass-retrieval scope. Multi-hop, cross-paper, vague queries. Needs agent-layer decomposition. Outside the RAG.
- **GOLD-BROADEN**: gold was too narrow; multiple chunks in the same paper could acceptably answer. Considered minor cleanup, not a system fix.

---

## Already working (R@5 = 1.00)

| Q | Type | Question | R@5 | MRR | CtxP | CtxR | What happened | Fix |
|---|---|---|---|---|---|---|---|---|
| Q02 | specific_fact_lookup | CalTennis evaluation metrics | 1.00 | 0.50 | 1.00 | 1.00 | Gold chunk in top-3. "CalTennis" anchor + specific metrics names made it a clean hit on both BM25 and dense. | **OK** |
| Q05 | specific_fact_lookup | UltraQuant serving efficiency metrics | 1.00 | 0.33 | 0.64 | 1.00 | Gold at rank 3. "UltraQuant" anchor + "TTFT/TPOT" specific terms surfaced via BM25. | **OK** |
| Q08 | definition | What does mobility refer to? | 1.00 | 0.50 | 1.00 | 1.00 | Gold at rank 2. Single distinctive term ("mobility") with specific definition chunk. | **OK** |
| Q10 | definition | What is a contagion network? | 1.00 | 0.20 | 0.00 | 0.75 | Gold at rank 5. Defining concept of the paper; hybrid found it but ranked behind related chunks. Cross-encoder would lift MRR. | **OK** (could improve MRR) |
| Q14 | methodology | How does ACE module work? | 1.00 | 0.25 | 0.75 | 1.00 | Gold at rank 4. "ACE" + "Action-based Candidate Evidence" are distinctive enough for hybrid. | **OK** |
| Q18 | equation | Gaussian splatting loss equation | 1.00 | 0.33 | 0.33 | 0.25 | Gold at rank 3. Chunker fix v1.1 put the formula in the chunk; hybrid + "Gaussian splatting" + "VisDom" anchor surfaced it. | **OK** |
| Q22 | contribution_recall | Probabilistic Verification paper contributions | 1.00 | 0.33 | 1.00 | 1.00 | Gold at rank 3. Paper name in question + "contributions" anchored the search. | **OK** |
| Q28 | comparison_contrast | LCB vs Multi-LCB difference | 1.00 | 0.20 | 0.20 | 0.50 | Gold at rank 5. Distinctive acronyms drove the match. Slightly noisy other retrievals (CtxP=0.20) but gold was found. | **OK** |

**8 of 30 questions work as-is.** These set the upper bound on what hybrid retrieval can achieve without additional fixes.

---

## Right paper found, wrong chunk (CROSS-ENCODER targets)

| Q | Type | Question | R@5 | MRR | CtxP | CtxR | What happened | Fix |
|---|---|---|---|---|---|---|---|---|
| Q03 | specific_fact_lookup | Third takeaway in Calibrated Mixture-of-Experts paper | 0.00 | 0.00 | 0.00 | 0.00 | All 5 retrieved chunks from the right paper, but pulled overview/conclusion content instead of the specific "third takeaway" subsection. | **CROSS-ENCODER** |
| Q06 | specific_fact_lookup | RQ1 finding two in Calibration Without Comprehension | 0.00 | 0.00 | 0.00 | 1.00 | 5/5 right paper. CtxR=1.00 says the gold answer is reconstructible from what was retrieved. Cross-encoder would push the specific "finding two" chunk up. | **CROSS-ENCODER** |
| Q09 | definition | Strategy Planner (Cross-Device Agent Systems) | 0.00 | 0.00 | 1.00 | 1.00 | 5/5 right paper. Perfect CtxP and CtxR. The specific definition chunk (00026) wasn't ranked top-5; closely-adjacent chunks were. | **CROSS-ENCODER** or GOLD-BROADEN |
| Q11 | methodology | Calibration Without Comprehension methodology | 0.00 | 0.00 | 0.87 | 1.00 | 3/5 right paper. Retrieved Introduction, RQ1 setup, RQ2 setup. The specific methodology chunk (00022 = "CWE-Trace assesses...") was not in top-5. | **CROSS-ENCODER** |
| Q12 | methodology | Multi-Qutrit quantum state estimation | 0.00 | 0.00 | 0.70 | 0.00 | 5/5 right paper. Retrieved overview content; specific variational-circuit chunks (00028, 00034) ranked too low. | **CROSS-ENCODER** |
| Q13 | methodology | FreeStyle model training | 0.00 | 0.00 | 0.87 | 1.00 | 4/5 right paper. Cross-encoder would push the specific 2-stage curriculum chunk above the overview chunks. | **CROSS-ENCODER** |
| Q15 | table_numerical | ASR score SR-Scout-30B vs HB-FT-LLaMA2-13B | 0.00 | 0.00 | 0.00 | 0.00 | 5/5 right paper. The full Table 3 markdown IS in chunk 00078 with the value 0.165 visible. Retrieved instead: Table 2 analysis text, Section 5 intro, Table 3 CAPTION (separate chunk). Cross-encoder would see the exact term "HB-FT-LLaMA2-13B" + value in the table chunk and rank it #1. | **CROSS-ENCODER** |
| Q16 | table_numerical | ResNet50 backbone time performance | 0.00 | 0.00 | 0.00 | 0.00 | 4/5 right paper. Table 2 chunk exists but isn't ranking. Similar to Q15. | **CROSS-ENCODER** |
| Q17 | table_numerical | Uniform sampling accuracy in TimeProVe efficiency table | 0.00 | 0.00 | 0.00 | 0.00 | 3/5 right paper. Same table-ranking issue. | **CROSS-ENCODER** |
| Q19 | equation | Cross-batch accumulation equation | 0.00 | 0.00 | 0.42 | 1.00 | 3/5 right paper. CtxR=1.00 says answer is reconstructible. Retrieved design-gap and research-question chunks; missed the actual equation chunk (00043). | **CROSS-ENCODER** |
| Q21 | contribution_recall | Fisher-Geometric Sharpness contributions | 0.00 | 0.00 | 1.00 | 0.75 | 5/5 right paper. CtxP=1.00. Retrieved chunks have the contributions content; gold chunk_ids (00007-00010) closely overlap with what was retrieved. | **GOLD-BROADEN** or **CROSS-ENCODER** |
| Q26 | comparison_contrast | Identity-level vs attribute-level effects on bias | 0.00 | 0.00 | 1.00 | 1.00 | 4/5 right paper. CtxP=CtxR=1.00. Retrieved Abstract + Conclusion + Introduction of the right paper. The specific Results-section chunks (00038, 00041) weren't pulled. | **CROSS-ENCODER** |
| Q27 | comparison_contrast | Egocentric video vs teleoperated robot data for embodied pretraining | 0.00 | 0.00 | 0.95 | 0.00 | 5/5 right paper. CtxP=0.95. The 24%/52.5%/90% number-rich Results chunk wasn't ranked; abstract/conclusion ranked higher. | **CROSS-ENCODER** |

**13 of 30 questions** are clearly cross-encoder territory. R@5 is currently zero on all of them, but CtxP/CtxR show the system is finding relevant content from the right paper; reranking would push the most-precisely-matching chunk to the top.

---

## Wrong paper retrieved (CONTEXTUAL CHUNKING targets)

| Q | Type | Question | R@5 | MRR | CtxP | CtxR | What happened | Fix |
|---|---|---|---|---|---|---|---|---|
| Q01 | specific_fact_lookup | SARLO-80 dataset | 0.00 | 0.00 | 0.00 | 0.00 | 0/5 from gold paper 2606.20523. Retrieved chunks from OTHER papers' dataset sections (COMPAS, jailbreak prompts, IFLLM). The gold chunk says "Umbra Collection" but never says "SARLO-80"; the embedder never linked the query anchor to the answer content. | **CONTEXTUAL CHUNKING** |
| Q04 | specific_fact_lookup | Diffusion Gemma user prompt count | 0.00 | 0.00 | 0.00 | 0.00 | 4/5 right paper. "Diffusion Gemma" anchor worked at the paper level, but the specific "n = 800" chunk has too generic terms ("user prompts", "WildChat") that match many papers. | **CROSS-ENCODER** could help, **CONTEXTUAL CHUNKING** would not move much |
| Q07 | definition | What is MAA? | 0.00 | 0.00 | 0.00 | 0.00 | 0/5 from gold paper 2606.20475. "MAA" alone is too short an acronym; appears across many papers (multi-armed, marginal, etc.). The paper title contains "Marginal Advantage Accumulation" but this isn't in the gold chunk text. Contextual chunking prepending the title would make every chunk in this paper anchored to "Marginal Advantage Accumulation (MAA)". | **CONTEXTUAL CHUNKING** |
| Q20 | contribution_recall | MAA paper's research questions | 0.00 | 0.00 | 0.20 | 0.50 | 2/5 right paper. "MAA" + "research questions" partial match; needs paper-title anchor. | **CONTEXTUAL CHUNKING** + **CROSS-ENCODER** |

**4 of 30 questions** show paper-level vocabulary mismatch. Contextual chunking (prepend `Paper: <title>\nSection: <section>\n\n`) would put the paper name in every chunk's embedded text, fixing the bridging problem.

---

## Out-of-scope for RAG (AGENT-layer)

| Q | Type | Question | R@5 | MRR | CtxP | CtxR | What happened | Fix |
|---|---|---|---|---|---|---|---|---|
| Q23 | negative_no_answer | Does 3D-editing paper discuss agentic AI? | n/a | n/a | 0.00 | 0.00 | Designed-empty gold. Faithfulness 1.00 — system correctly said "this paper does not discuss agentic AI". The retrieval scores are noise; the test passed at the generation layer. | **NO FIX** (intentional) |
| Q24 | vague_ambiguous | Tell me about image editing | 0.00 | 0.00 | 0.25 | 0.00 | 3/5 right paper. Vague query has no anchor; retrieval surfaced loosely-related chunks across papers. Designed to test query-understanding boundary. | **AGENT** (query rewriter) |
| Q25 | multi_hop | Related-work item discussing lottery | 0.00 | 0.00 | 1.00 | 0.00 | 0/5 right paper. "Lottery" matched lottery-themed content across the corpus but didn't anchor to the FID Lottery paper's related-work section. Needs 2-step retrieval. | **AGENT** (query decomposition) |
| Q29 | cross_paper | JanusMesh vs Thinking in Boxes input/output | 0.00 | 0.00 | 0.00 | 0.00 | 1/5 right paper, only Thinking in Boxes retrieved; JanusMesh not pulled. Single dense query cannot equally serve two distant topics. | **AGENT** (decompose into 2 sub-queries) |
| Q30 | cross_paper | JanusMesh vs Thinking in Boxes 3D representations | 0.00 | 0.00 | 0.00 | 0.00 | 0/5 right papers (interestingly retrieved StylisticBias, Calibration, etc.). Cross-paper question can't be served by single retrieval. | **AGENT** (decompose into 2 sub-queries) |

**5 of 30 questions** are out of single-pass RAG scope. Their zero scores are evidence for the agent-layer boundary, not failures to fix at the retrieval layer.

---

## Summary by fix category

| Fix | Q count | Affected questions | Expected lift |
|---|---|---|---|
| **OK (no fix)** | 8 | Q02, Q05, Q08, Q10, Q14, Q18, Q22, Q28 | Already at R@5=1.00 |
| **CROSS-ENCODER** (primary) | 13 | Q03, Q06, Q09, Q11, Q12, Q13, Q15, Q16, Q17, Q19, Q21, Q26, Q27 | These would lift from R@5=0 toward 0.7-0.9, based on the fact that retrieval already finds the right papers and CtxP is high. Single biggest expected eval win. |
| **CONTEXTUAL CHUNKING** (primary) | 2-4 | Q01, Q07 strongly; Q04, Q20 partially | Would lift the wrong-paper cases. Smaller in absolute count but specific. |
| **AGENT (out of scope)** | 5 | Q23, Q24, Q25, Q29, Q30 | No RAG-layer lift expected. These belong in the MCP-consuming agent layer. |

If both fixes were implemented and they each delivered ~70% of their potential lift, the eval would land roughly:

- Currently passing: 8 questions
- Cross-encoder wins: + ~9 questions (out of 13 candidates × 70%)
- Contextual chunking wins: + ~2 questions (out of 3 candidates × 70%)
- Agent-layer: 0 (deferred)

Expected Recall@5: roughly 0.65 (19/30), up from current 0.276.

---

## Implementation order

Based on the table:

1. **Cross-encoder reranking first.** Hits 13 of the 30 questions and has the cleanest mechanism (reranks within already-found candidates). Implementation: ~50 lines added to `tools/retriever.py`, plus a cross-encoder model from `sentence-transformers` (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`, ~80 MB). No re-ingestion needed.

2. **Contextual chunking second.** Hits 2-4 questions. Implementation: ~10 lines in `tools/ingest/chunking.py`, plus CHUNKER_VERSION bump (v2 → v3), re-ingest (~30 min), re-populate gold_chunk_ids (subagent run).

The order is chosen so we measure each lift independently. Both are real fixes, not patches. Each addresses a distinct failure mechanism documented above.

3. **Agent-layer work** is its own initiative, post-MCP. The eval already demonstrates which categories belong there; no further analysis needed at the RAG layer.

---

## Source data

- Eval run: `tests/eval/results.jsonl`, line 7 (run 6, 2026-06-25T16:18:39Z)
- Per-question retrieval audit: `tests/eval/v2_retrieval_audit.md`
- v1 → v1.1 → v2 deltas: `tests/eval/baseline_analysis.md`
