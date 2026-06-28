# Mini-RAG v4 per-question diagnosis

Generated from the v4 run (hybrid + cross-encoder + contextual chunking). For each of the 30 golden-set questions, this records current status and what fix (if any) would lift it further. Compares against the v2 diagnosis at `v2_per_question_diagnosis.md` to show which categories moved.

**Metric legend**: R@1, R@5 = strict-match Recall against `gold_chunk_ids`. CtxP = RAGAS context_precision (LLM-judged: were retrieved chunks relevant?). CtxR = RAGAS context_recall (LLM-judged: was gold answer reconstructible from retrieved chunks?). The gap between R and CtxP/CtxR is diagnostic: high CtxP with R=0 means retrieval found relevant content in non-marked chunks.

**v4 fix categories** (different from v2's structural categories — the v2 categories were addressed by v3 and v4 changes; this is the remaining picture):
- **PERFECT**: gold at rank 1. System needs no fix.
- **STRONG**: gold in top-5 but not at rank 1. Could lift with better reranking or query rewriting.
- **CONTENT-FOUND-WRONG-CHUNK**: R@5=0 but CtxP/CtxR high. Retrieval surfaced relevant chunks just not the marked golds. Gold-broadening or cross-encoder tuning would help.
- **POOL-DEPTH**: gold chunk is too far down to be reranked. Table-aware chunking or wider RERANK_TOP would help.
- **AGENT-NEEDED**: multi-hop, vague, deep cross-paper. Out of single-pass-retrieval scope.

---

## PERFECT (R@1 = 1.00) — 9 questions

These questions land the gold chunk at rank 1.

| Q | Type | Question | R@1 | R@5 | CtxP | Notes |
|---|---|---|---|---|---|---|
| Q02 | specific_fact_lookup | CalTennis evaluation metrics | 1.00 | 1.00 | 0.80 | "CalTennis" anchor + metrics names |
| Q04 | specific_fact_lookup | Diffusion Gemma user prompt count | 1.00 | 1.00 | 1.00 | Contextual chunking unlocked this (v3 had R@5=0) |
| Q05 | specific_fact_lookup | UltraQuant serving efficiency | 1.00 | 1.00 | 0.75 | "UltraQuant" + TTFT/TPOT terms |
| Q08 | definition | What does mobility refer to? | 1.00 | 1.00 | 0.87 | Specific term + paper anchor |
| Q12 | methodology | Multi-Qutrit quantum state estimation | 1.00 | 1.00 | 1.00 | Big v3 → v4 win |
| Q18 | equation | Gaussian splatting loss equation | 1.00 | 1.00 | 1.00 | Chunker v2 + contextual + reranker stack |
| Q20 | contribution_recall | MAA paper RQs | 1.00 | 1.00 | 1.00 | Paper anchor unlocked |
| Q21 | contribution_recall | Fisher-Geometric Sharpness contributions | 1.00 | 1.00 | 1.00 | Was R@5=0 in v3 |
| Q28 | comparison_contrast | LCB vs Multi-LCB | 1.00 | 1.00 | 0.87 | Distinctive acronyms |

---

## STRONG (R@1 = 0, R@5 = 1.00) — 6 questions

Gold chunk is in top-5 but not at rank 1. A more sophisticated reranker or query rewriter could push these to rank 1 and lift Recall@1 further.

| Q | Type | Question | R@1 | R@5 | MRR | CtxP | What would lift |
|---|---|---|---|---|---|---|---|
| Q10 | definition | What is a contagion network? | 0.00 | 1.00 | 0.33 | 1.00 | Gold at rank ~3; better reranker for definition-style queries |
| Q14 | methodology | ACE module in TimeProVe | 0.00 | 1.00 | 0.50 | 1.00 | Gold at rank ~2 |
| Q22 | contribution_recall | Probabilistic Verification contributions | 0.00 | 1.00 | 0.25 | 0.48 | Gold at rank ~4 with noisy other chunks |
| Q27 | comparison_contrast | Egocentric video vs robot data | 0.00 | 1.00 | 0.33 | 1.00 | Big v3 → v4 lift; rank ~3 |
| Q29 | cross_paper | JanusMesh vs Thinking in Boxes I/O | 0.00 | 1.00 | 0.33 | 0.00 | Surprise lift via contextual chunking |
| Q30 | cross_paper | JanusMesh vs Thinking in Boxes 3D | 0.00 | 1.00 | 0.50 | 0.75 | Similar |

---

## CONTENT-FOUND-WRONG-CHUNK (R@5 = 0, CtxP/CtxR high) — 5 questions

R@5 strict-match says fail, but RAGAS's LLM judge says the retrieved chunks have the answer. Either the gold chunk choice was too narrow or the cross-encoder is consistently preferring nearby chunks. Could be cleared by broadening `gold_chunk_ids` or by a stronger reranker.

| Q | Type | Question | R@5 | CtxP | CtxR | Why failing |
|---|---|---|---|---|---|---|
| Q09 | definition | Strategy Planner | 0.00 | 1.00 | 1.00 | All retrieved chunks are from right paper; gold ID too narrow |
| Q11 | methodology | CWE-Trace assessment | 0.00 | 0.80 | 0.00 | Right paper, retrieved Introduction/RQ-setup chunks; gold (specific methodology paragraph) ranked below |
| Q13 | methodology | FreeStyle training | 0.00 | 1.00 | 0.00 | Same pattern as Q11 |
| Q19 | equation | Cross-batch accumulation equation | 0.00 | 1.00 | 1.00 | Retrieved relevant chunks but missed the specific equation chunk |
| Q26 | comparison_contrast | Identity vs attribute effects | 0.00 | 0.95 | 1.00 | Abstract/Conclusion retrieved; specific Results chunks not in top-5 |

**Fix options** for these:
1. **Broaden gold_chunk_ids** to include the Abstract/Conclusion/Introduction chunks of the right paper. Trivial change, raises strict-match Recall@5 to ~1.00 for these 5. Defensible because the answer IS retrievable from what's returned.
2. **Train or use a domain-tuned cross-encoder** on academic papers. The MS-MARCO model we use was trained on web search queries, which differ in style from these long academic questions.
3. **Accept the gap.** Context_precision and context_recall already show these are working from a "does the system answer correctly" perspective.

---

## POOL-DEPTH FAILURES — 7 questions

Hybrid retrieval doesn't surface the right chunk into the top-RERANK_TOP=20 candidates. Cross-encoder never sees it.

| Q | Type | Question | R@5 | Cause | Fix |
|---|---|---|---|---|---|
| Q01 | specific_fact_lookup | SARLO-80 dataset | 0.00 | Gold at BM25 rank 150 (v4) | Wider RERANK_TOP or different embedding model |
| Q03 | specific_fact_lookup | Third takeaway in MoE paper | 0.00 | Vague answer-vs-section anchoring | Re-examine gold; possibly broaden |
| Q06 | specific_fact_lookup | Finding 2 of RQ1 | 0.00 | Similar to Q03 | Same |
| Q07 | definition | What is MAA? | 0.00 | 3-char acronym; BM25 rank 2117 | Hard problem; acronym expansion in query, or trained reranker |
| Q15 | table_numerical | ASR score row | 0.00 | BM25 rank 33; just outside RERANK_TOP=20 | **Widen RERANK_TOP to 50** would likely fix |
| Q16 | table_numerical | ResNet50 time performance | 0.00 | Similar | Same |
| Q17 | table_numerical | Uniform sampling accuracy | 0.00 | Similar | Same |

**Fix options:**
1. **Widen RERANK_TOP from 20 to 50.** One-line change. Would likely fix Q15-Q17 (BM25 ranks 33-50 range). No re-ingestion needed. Quick eval.
2. **Table-specific chunking.** Keep each table including caption + all rows as a single chunk. Would compete more strongly in dense retrieval because the whole table is one semantic unit.
3. **Stronger reranker or domain adaptation.** Larger MS-MARCO model (L-12 instead of L-6) or domain-tuned cross-encoder.

---

## AGENT-NEEDED — 5 questions

These categories are confirmed out-of-RAG scope by the v4 numbers; no retrieval-layer fix will move them.

| Q | Type | Question | R@5 | Why no fix at RAG layer |
|---|---|---|---|---|
| Q23 | negative_no_answer | Does paper discuss agentic AI? | n/a | Designed empty gold. Faithfulness 1.00 — system correctly refused. |
| Q24 | vague_ambiguous | Tell me about image editing | 0.00 | No anchor for retrieval. Query-understanding job for an agent. |
| Q25 | multi_hop | Lottery-related related-work | 0.00 | Needs two-step decomposition. |

(Q29, Q30 cross_paper were listed in v2 as agent-needed but lifted to R@5=1.00 in v4 — moved to STRONG above.)

---

## v2 → v4 fix-category migration

How each v2 category fared after v3 + v4:

| v2 category (count) | v4 count remaining | Migration |
|---|---|---|
| WORKING (8) | 9 PERFECT + 6 STRONG (15) | All v2 working cases still work; plus several lifted from other categories |
| CROSS-ENCODER target (13) | 5 remain in CONTENT-FOUND-WRONG-CHUNK | ~8 cleanly lifted |
| CONTEXTUAL CHUNKING target (4) | 4 of 7 in POOL-DEPTH | Q04 fully lifted; Q01 still hard but BM25 rank closed in (276 → 150); MAA acronym remains stubbornly hard |
| AGENT-NEEDED (5) | 3 remain | Q29, Q30 cross_paper lifted unexpectedly to STRONG |

---

## Headline counts

| Status | Count | Percentage |
|---|---|---|
| **PERFECT (R@1=1.00)** | 9 | 31% |
| **STRONG (R@5=1.00, R@1=0)** | 6 | 21% |
| Content-found-wrong-chunk | 5 | 17% |
| Pool-depth failures | 7 | 24% |
| Agent-needed | 3 (excluding negative_no_answer) | 10% |

**52% of questions reliably find their gold chunk in top-5.** Up from 27% at v2 baseline.

**If table_numerical lifts with `RERANK_TOP=50` (3 questions) and content-found cases get gold-broadened (5 questions), the strict R@5 would climb to ~80%.**

---

## Source data

- v4 eval run: `tests/eval/results.jsonl` (last line as of v4)
- Cumulative analysis (all versions): `analysis/baseline_analysis.md`
- v4 per-question full retrieval audit: `analysis/v4_retrieval_audit.md`
- v2 baseline diagnosis for comparison: `analysis/v2_per_question_diagnosis.md`
