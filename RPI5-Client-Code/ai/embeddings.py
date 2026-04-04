"""
Embeddings module — generates vector embeddings for prompts.
Stub implementation for the demo. In production, this would use
a local sentence-transformer or similar model.
"""
from logger import logger


def generate_embedding(text: str) -> list:
    """
    Generate a simple hash-based pseudo-embedding for demo purposes.
    In production, use a real model like sentence-transformers.
    """
    # Simple character-frequency based vector (128 dims)
    vec = [0.0] * 128
    for i, char in enumerate(text.lower()):
        idx = ord(char) % 128
        vec[idx] += 1.0

    # Normalize
    magnitude = sum(v ** 2 for v in vec) ** 0.5
    if magnitude > 0:
        vec = [v / magnitude for v in vec]

    logger.debug(f"Generated embedding for '{text[:30]}...' ({len(vec)} dims)")
    return vec


def cosine_similarity(vec_a: list, vec_b: list) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = sum(a ** 2 for a in vec_a) ** 0.5
    mag_b = sum(b ** 2 for b in vec_b) ** 0.5
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)
