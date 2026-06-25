# Mini-RAG v1 baseline evaluation

First eval run against the hand-crafted 30-question golden set. The system
under test is the production-shipped Level 1 RAG (retrieval only):

- Parsing: Docling DocumentConverter
- Chunking: paragraph-level via doc_item iteration, with merge rule and size
  safety net
- Embeddings: SPECTER2 (`allenai/specter2_base`, 768-dim, local)
- Vector store: Chroma (50 papers, 7,452 chunks)
- Retrieval: dense top-5 cosine similarity, no reranker, no hybrid
- Generation (eval-only): minimal gpt-4o-mini call with retrieved chunks

## Headline numbers

| Metric | Score | Notes |
|---|---|---|
| Recall@1 | 0.034 | Only ~3% of questions had gold at rank 1 |
| Recall@3 | 0.069 | |
| Recall@5 | 0.103 | ~10% of questions had any gold in top-5 |
| MRR | 0.059 | Average rank of first gold ≈ 17 |
| NDCG@5 | 0.042 | |
| Faithfulness | 0.634 | LLM mostly stays grounded |
| Context precision | 0.293 | LLM judge: ~30% of retrieved chunks are relevant |
| Context recall | 0.169 | ~17% of gold answer is reconstructible from retrieval |
| Answer correctness | 0.267 | |
| Answer relevancy | 0.277 | |

Run elapsed: ~85 seconds. Cost: ~$0.10.

## Per-type breakdown

| Type | n | R@5 | MRR | Faith | Ctx Prec | Ctx Recall | Ans Corr |
|---|---|---|---|---|---|---|---|
| definition | 4 | 0.250 | 0.250 | 0.875 | 0.258 | 0.250 | 0.310 |
| contribution_recall | 3 | 0.333 | 0.167 | 0.619 | 0.326 | 0.417 | 0.451 |
| specific_fact_lookup | 6 | 0.167 | 0.033 | 0.500 | 0.158 | 0.000 | 0.253 |
| methodology | 4 | **0.000** | 0.000 | 0.583 | **0.904** | 0.500 | 0.278 |
| comparison_contrast | 3 | 0.000 | 0.000 | 0.667 | 0.602 | 0.111 | 0.365 |
| table_numerical | 3 | 0.000 | 0.000 | 0.333 | 0.000 | 0.000 | 0.235 |
| equation | 2 | 0.000 | 0.000 | 0.500 | 0.100 | 0.250 | 0.128 |
| cross_paper | 2 | 0.000 | 0.000 | 0.833 | 0.000 | 0.000 | 0.166 |
| multi_hop | 1 | 0.000 | 0.000 | 0.667 | 0.200 | 0.000 | 0.136 |
| vague_ambiguous | 1 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.113 |
| negative_no_answer | 1 | n/a | n/a | 1.000 | 0.000 | 0.000 | 0.157 |

## Findings

### What worked

- **Definitions had the highest MRR (0.250).** Specific terminology in the
  question (e.g. "MAA", "Strategy Planner", "mobility") anchored retrieval to
  chunks that contain the same terms. This is the case where dense semantic
  retrieval works as advertised.

- **Contribution_recall had the highest Recall@5 (0.333).** Paper-name anchors
  plus the phrase "contributions" aligned with content in introduction
  sections that explicitly list contributions.

- **Faithfulness was high everywhere (0.500-1.000).** The eval LLM stayed
  grounded in retrieved context rather than hallucinating. The grounding
  works; retrieval just isn't supplying the right context.

- **Negative_no_answer scored perfect Faithfulness (1.000).** The system
  correctly said "this paper does not discuss agentic AI" for the Thinking
  in Boxes 3D editing paper. Grounding behavior is correct.

### What didn't work

#### Methodology: Ctx Precision 0.904 with Recall@5 0.000

The clearest diagnostic finding. The LLM judge says 90% of retrieved chunks
are relevant to the methodology questions, but our specific `gold_chunk_ids`
weren't in the top-5.

Two possible reads:

- Our gold chunks were too narrow. Methodology often spans multiple chunks
  (overview, specifics, ablations); we marked one paragraph as gold while
  the retriever found a different methodology paragraph that would have
  worked.
- Retrieval prioritizes high-level methodology summaries over the specific
  subsection containing our gold.

Either way, this validates RAGAS's value: context_precision catches the
"relevant chunk retrieved" signal that strict chunk_id matching misses.

Action: review methodology gold_chunk_ids and consider whether to broaden
them (e.g., include 2-3 valid chunks per question instead of one).

#### Table_numerical: 0.000 across the board

Tables came through as markdown via Docling, so the content is in the index.
But dense retrieval cannot match queries like "What is the ASR score..." to
chunks containing "0.165". Specific numerical values carry no semantic signal
that SPECTER2 can use to differentiate them.

This is the canonical case for hybrid retrieval. BM25 would match exact
numerical strings; dense would contribute the surrounding context.

#### Equation: 0.000 across the board

Confirms the chunker bug we identified earlier. Docling extracted 61 formula
items in 2606.20547 alone, but each had `text: ''` (empty processed text)
with the raw content in `orig`. Our chunker reads `text`, sees empty, drops
the formula silently. Across the entire 50-paper corpus, zero formula chunks
landed in the index.

Action: one-line fix in `tools/ingest/chunking.py` to fall back to
`item.orig` when `item.text` is empty. Requires re-ingestion (~30 min) and
re-population of any equation gold_chunk_ids.

#### Cross_paper + Multi_hop + Comparison_contrast: 0.000 retrieval but high Faithfulness

These categories fundamentally cannot be solved by single-pass dense
retrieval:

- Cross_paper questions ask the system to compare two papers, but a single
  embedding cannot equally serve two distant topics. The retriever picks
  chunks from one paper or thematic chunks that lean toward one side.
- Multi_hop questions require two-step reasoning: find A, then find B about
  A. Single dense retrieval has no decomposition step.
- Comparison_contrast questions about "the difference between X and Y" need
  the system to fetch both X and Y descriptions, often from different
  sections of the same paper.

These are agent-layer responsibilities. A consumer of this RAG (the main
agent) would handle them via:

- Query decomposition: break "compare X and Y" into "describe X" + "describe Y"
- Multi-step retrieval: retrieve A's identity, then formulate query for B
- Result merging: combine partial retrievals into a single answer

Expected eval behavior for these types: they should score low on retrieval
metrics in a RAG-only test. That's the right answer. They're not RAG
failures; they're outside the RAG's scope.

#### Vague_ambiguous: 0.000

"Tell me about image editing" is intentionally vague and tests how the
system handles broad queries. A real consumer would clarify intent before
querying; raw dense retrieval has no clarification mechanism.

This is a query-understanding test, which is also an agent-layer concern.

#### Specific_fact_lookup: only 0.167 Recall@5

Mixed performance. The questions with strong distinctive anchors (Q07 "MAA",
Q15 "HB-FT-LLaMA 2-13B") found their golds. The ones with paper-name anchors
plus generic query terms (Q01 "SARLO-80 dataset") missed because gold chunk
content uses different vocabulary than the question.

This is the vocabulary mismatch problem. Hybrid retrieval would help: BM25
matches the paper name in the question to whatever chunks contain that
paper name (often title/abstract chunks adjacent to the actual answer).
Combined with dense semantic match on the question terms.

## Hypotheses to fixes

| Failure mode | Root cause | Fix |
|---|---|---|
| Vocabulary mismatch (specific_fact_lookup) | Question terms ≠ gold chunk terms | Hybrid retrieval (BM25 + dense via RRF) |
| Needle in haystack within right paper | Dense averages out specific facts | Cross-encoder reranking after retrieval |
| Table values not retrievable | Numbers carry no semantic signal | Hybrid retrieval (BM25 on exact values) |
| Equations missing from index | Chunker drops formulas with empty `text` field | Fall back to `item.orig` in `chunking.py` |
| Multi-hop, cross_paper, comparison_contrast, vague_ambiguous | Single-pass retrieval cannot decompose or compare | Agent-layer query decomposition (outside this RAG) |
| Gold chunks possibly too narrow (methodology) | Single chunk_id marked when multiple would qualify | Review and broaden methodology gold_chunk_ids |

## Next-phase priorities

Ordered by expected lift on the eval set:

1. **Hybrid retrieval (BM25 + dense via RRF).** Single highest-leverage
   change. Would directly lift `specific_fact_lookup`, `table_numerical`,
   `methodology`, `contribution_recall`. Affects roughly 60-70% of the
   questions. The vector DB layer (Chroma) supports adding a BM25 index
   alongside; the retrieval function fuses scores.

2. **Fix chunker formula handling.** Small code change in
   `tools/ingest/chunking.py` (fall back to `item.orig`). Recovers equation
   chunks across all 50 papers. Requires re-ingesting (~30 min) and
   re-populating `gold_chunk_ids` for Q18 and Q19.

3. **Cross-encoder reranking.** After hybrid retrieval returns top-20,
   rerank with a cross-encoder model to push best matches to top-5.
   Improves needle-in-haystack across all types where the right paper is
   found but specific chunk is missed.

4. **Review methodology gold_chunk_ids.** Likely need to broaden them.
   Context precision of 0.904 says retrieval is finding relevant
   methodology content; our golds may be unnecessarily strict.

5. **Document the agent-layer scope for cross_paper / multi_hop /
   comparison_contrast / vague_ambiguous.** These categories should not be
   targeted for RAG-internal improvement; they belong in the main agent
   that consumes this RAG via MCP. Note this in DEVLOG so the writeup is
   honest about scope.

## Run metadata

- Timestamp: 2026-06-24T16:06:52Z
- Pipeline commit: fddb1f9
- Config hash: 3f45ab14
- Embedding model: allenai/specter2_base (768-dim)
- Eval LLM: gpt-4o-mini (temp 0)
- RAGAS judge: gpt-4o-mini (temp 0)
- RAGAS embedder: text-embedding-3-small
- Elapsed: ~85 seconds
- Sample size: 30 of 30 questions
- Result record: `tests/eval/results.jsonl` (first line)

---

# Mini-RAG v1.1: chunker fix (formula extraction)

Single change vs v1: when a `FormulaItem` has empty `text`, fall back to
`item.orig`. Recovers formula content across the corpus that v1 silently
dropped. CHUNKER_VERSION bumped to 2; config_hash invalidated existing
chunks; full re-ingest produced 7,631 chunks (vs 7,452 in v1).

## Comparison vs v1

| Metric | v1 | v1.1 | Δ |
|---|---|---|---|
| Recall@1 | 0.034 | 0.034 | 0.000 |
| Recall@3 | 0.069 | 0.069 | 0.000 |
| Recall@5 | 0.103 | 0.103 | 0.000 |
| MRR | 0.059 | 0.059 | 0.000 |
| NDCG@5 | 0.042 | 0.043 | +0.001 |
| Faithfulness | 0.634 | 0.643 | +0.009 |
| Answer correctness | 0.267 | 0.282 | +0.015 |
| Answer relevancy | 0.277 | 0.278 | +0.001 |
| Context precision | 0.293 | 0.286 | -0.007 |
| Context recall | 0.169 | 0.203 | **+0.034** |

## Equation type specifically

| Metric | v1 | v1.1 |
|---|---|---|
| Recall@5 | 0.000 | 0.000 |
| Context precision | 0.100 | 0.000 |
| Context recall | 0.250 | 0.500 |
| Faithfulness | 0.500 | 0.500 |
| Answer correctness | 0.128 | 0.126 |

## Findings

### The fix landed: formula content is now in the index

Verified directly: chunk `2606.20531::00027` (Q18 gold) now ends with
`L_ours = L_base + λ_2 L_mask + λ_3 L_i, (2)`, and chunk
`2606.20475::00043` (Q19 gold) now contains the cross-batch EMA recursive
formula `m_{k,t} = β m_{k,t-1} + (1−β) δ_{k,t}` with bias correction. In
v1 these were dropped because docling's `FormulaItem.text` was empty even
though `.orig` had the content. The chunker now reads `.orig` as fallback.

### But retrieval did not improve

Equation Recall@5 stayed at 0.000. The formulas are present in the chunks
but dense retrieval can't rank them at the top for queries like "What is
the proposed loss equation for Gaussian splatting in VisDom?" Two reasons:

- Math symbols don't carry strong semantic signal in SPECTER2 (it wasn't
  trained on equation tokens).
- Query terms "equation" and "loss" semantically match many chunks across
  many papers, so dense retrieval surfaces near-misses from other papers
  before the right chunk in the right paper.

This is the predicted limitation of pure dense retrieval on math content.
The fix was necessary (you can't retrieve content that isn't indexed), but
not sufficient. Hybrid retrieval is required to actually leverage it.

### Context recall lift (+0.034 overall, +0.250 on equation type) is the real signal

Recall@k can't move if retrieval returns the same chunks. But context_recall
asks RAGAS's LLM judge "can the gold answer be reconstructed from the
retrieved chunks?" Even though the retrieved chunks haven't changed in
rank, they now CONTAIN more relevant content (formula text appended to
preceding text chunks). The judge sees this and scores higher.

This validates the fix landed where intended. The next phase (hybrid
retrieval) will let Recall@k catch up by actually finding these chunks.

### Q26 effective content fix (subagent finding, not visible in metrics)

When re-populating gold_chunk_ids, the subagent noticed Q26's original
gold chunks (00037, 00040) pointed at short table-caption chunks. In v2,
the substantive identity-vs-attribute findings live in adjacent chunks
(00038, 00041). The subagent corrected these. Result: a more
representative gold-set entry, even without metric movement.

## Conclusion: proceed to hybrid retrieval (v2)

The chunker fix is a necessary scaffolding change with limited direct
metric impact. Its value is unlocked by hybrid retrieval, which can
match queries like "equation for X" against the literal term "X" in the
chunk (where the formula now lives) via BM25. Single-dim signal: dense
alone cannot bridge "math query" to "math chunk"; BM25 + dense via RRF
should.

## v1.1 run metadata

- Timestamp: 2026-06-25T14:29:46Z
- Pipeline commit: 70fd59b
- Config hash: 735da861 (changed from v1's 3f45ab14 due to CHUNKER_VERSION bump)
- Chunks total: 7,631 (vs 7,452 in v1)
- Gold chunk id updates: 9 of 30 entries
- Q18, Q19 answer text enriched with extracted formulas
- Elapsed: ~120 seconds
- Result record: `tests/eval/results.jsonl` (second line)
