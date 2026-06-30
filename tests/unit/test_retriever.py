"""Pin RRF fusion math from mini_rag.retriever.

The fusion logic is the single deterministic step between hybrid retrieval
and reranking. Tests use small synthetic rank dicts (no model, no Chroma).
"""

import math


def test_rrf_fuse_combines_ranks_from_both_retrievers():
    from mini_rag.retriever import _rrf_fuse, _RRF_K
    dense = {"a": 1, "b": 2, "c": 3}
    bm25 = {"a": 2, "c": 1, "d": 3}
    scores = _rrf_fuse(dense, bm25, k=_RRF_K)

    # Every id from either retriever is present
    assert set(scores) == {"a", "b", "c", "d"}

    # 'a' appears in both at decent rank: should score highest
    # 'c' appears in both, top of bm25: should also score high
    # 'b' and 'd' each appear in one: should score lower
    assert scores["a"] > scores["b"]
    assert scores["c"] > scores["d"]


def test_rrf_fuse_uses_documented_formula():
    from mini_rag.retriever import _rrf_fuse
    dense = {"x": 1}
    bm25 = {"x": 1}
    scores = _rrf_fuse(dense, bm25, k=60)
    # Both retrievers rank "x" at position 1, so score = 2 * 1/(60+1)
    assert math.isclose(scores["x"], 2.0 / 61.0)


def test_rrf_fuse_handles_id_in_only_one_retriever():
    from mini_rag.retriever import _rrf_fuse
    dense = {"only_dense": 1}
    bm25 = {}
    scores = _rrf_fuse(dense, bm25, k=60)
    # Missing-side contribution must be ~0 (rank treated as infinity)
    assert math.isclose(scores["only_dense"], 1.0 / 61.0, abs_tol=1e-9)


def test_rrf_fuse_ranks_top_at_rank_1_above_id_at_rank_20():
    from mini_rag.retriever import _rrf_fuse, _RRF_K
    dense = {"top": 1, "deep": 20}
    bm25 = {}
    scores = _rrf_fuse(dense, bm25, k=_RRF_K)
    assert scores["top"] > scores["deep"]


def test_rrf_fuse_with_empty_inputs_returns_empty_dict():
    from mini_rag.retriever import _rrf_fuse
    assert _rrf_fuse({}, {}, k=60) == {}
