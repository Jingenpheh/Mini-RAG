# ##############################################################################
# File: embeddings.py
# Purpose: Embedding stage. Runs the configured embedding model over chunk
#          texts and returns vectors.
#
# Contents:
#   Functions:
#     embed_chunks()           - Compute embeddings for a list of chunks
# ##############################################################################


# Local
from tools.utils import get_embedder
from tools.ingest.schema import Chunk


# ##############################################################################
# Public entry point
# ##############################################################################


def embed_chunks(chunks: list[Chunk]) -> list[list[float]]:
    """Compute embedding vectors for the given chunks.

    Args:
        chunks (list[Chunk]): Chunks to embed.

    Approach:
        Calls the shared embedder singleton from tools.utils so the model
        loads once per process and is reused at retrieval time too. The
        embedder's embed_documents API batches under the hood; returned
        vectors preserve input order so they can be paired with chunks
        positionally by the caller.

    Returns:
        list[list[float]]: One vector per chunk, in the same order. Empty list
            if chunks is empty.
    """
    if not chunks:
        return []
    embedder = get_embedder()
    texts = [c.text for c in chunks]
    return embedder.embed_documents(texts)
