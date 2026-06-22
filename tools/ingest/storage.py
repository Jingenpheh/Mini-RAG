# ##############################################################################
# File: storage.py
# Purpose: Vector store writes. Phase 3 stub. Will write chunk records and
#          their embeddings into Chroma.
#
# Contents:
#   Functions:
#     store_chunks()           - Persist chunks + vectors to the vector store
# ##############################################################################


# Local
from tools.ingest.schema import Chunk


# ##############################################################################
# Storage (stub)
# ##############################################################################


def store_chunks(chunks: list[Chunk], vectors: list[list[float]]) -> int:
    """Persist chunks and their vectors to the vector store.

    Args:
        chunks (list[Chunk]): Chunk records to store.
        vectors (list[list[float]]): One embedding per chunk, same order.

    Approach:
        Phase 3 will get the Chroma collection from tools.utils.get_vector_store
        and call collection.add(ids=, documents=, embeddings=, metadatas=) with
        the chunk_id, text, vector, and to_metadata() of each chunk. The stub
        is a no-op so the pipeline can be exercised end-to-end during
        development.

    Returns:
        int: Number of records written. Currently 0.
    """
    return 0
