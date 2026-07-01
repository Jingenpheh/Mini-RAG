# ##############################################################################
# File: storage.py
# Purpose: Vector store writes. Persists chunk records and their pre-computed
#          embeddings into the Chroma collection.
#
# Contents:
#   Functions:
#     store_chunks()           - Write chunks + vectors to the vector store
# ##############################################################################


# Local
from mini_rag import chroma_client
from mini_rag.ingest.schema import Chunk


# ##############################################################################
# Storage
# ##############################################################################


def store_chunks(chunks: list[Chunk], vectors: list[list[float]]) -> int:
    """Persist chunks and their vectors to the Chroma vector store.

    Args:
        chunks (list[Chunk]): Chunk records to store.
        vectors (list[list[float]]): One embedding per chunk, same order.

    Approach:
        Writes through the underlying Chroma collection rather than the
        LangChain wrapper's `add_documents`, because we already computed
        embeddings in the embed stage. Going through the wrapper would
        re-embed on the way in. The wrapper's embedding_function still kicks
        in at retrieval time for query embedding, which is what we want for
        consistency between query and document representations.

        Chunk metadata is flattened to Chroma-safe types by Chunk.to_metadata
        (lists become "; "-joined strings, text and chunk_id excluded).

    Returns:
        int: Number of records written.
    """
    if not chunks:
        return 0
    if len(chunks) != len(vectors):
        raise ValueError(
            f"chunks ({len(chunks)}) and vectors ({len(vectors)}) length mismatch"
        )

    chroma_client.add(
        ids=[c.chunk_id for c in chunks],
        documents=[c.text for c in chunks],
        embeddings=vectors,
        metadatas=[c.to_metadata() for c in chunks],
    )
    return len(chunks)
