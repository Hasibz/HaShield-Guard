import numpy as np

def calculate_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calculates the semantic similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    # Prevent division by zero
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
        
    return dot_product / (norm_vec1 * norm_vec2)

def is_adversarial(prompt_vector: np.ndarray, attack_centroid: np.ndarray, threshold: float = 0.85) -> bool:
    """
    Returns True if the prompt vector is mathematically too close 
    to the known attack cluster.
    """
    similarity = calculate_cosine_similarity(prompt_vector, attack_centroid)
    return similarity >= threshold