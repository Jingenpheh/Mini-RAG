# ##############################################################################
# File: embeddings.py
# Purpose: Embedding stage. Phase 3 stub. Will call the embedding model on
#          chunk texts and return vectors.
#
# Contents:
#   Functions:
#     embed_chunks()           - Compute embeddings for a list of chunks (stub)
# ##############################################################################


# Local
from tools.ingest.schema import Chunk


# ##############################################################################
# Embedding (stub)
# ##############################################################################


def embed_chunks(chunks: list[Chunk]) -> list[list[float]]:
    """Compute embedding vectors for the given chunks.

    Args:
        chunks (list[Chunk]): Chunks to embed.

    Approach:
        Phase 3 will call OpenAI's text-embedding-3-small via
        langchain-openai's OpenAIEmbeddings, batching as needed. The current
        stub returns empty lists so the rest of the pipeline can be exercised
        end-to-end during development.

    Returns:
        list[list[float]]: One vector per chunk, in the same order. Currently
            returns a list of empty lists.
    """
    return [[] for _ in chunks]
