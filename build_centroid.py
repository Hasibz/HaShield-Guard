from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import numpy as np
import os
os.makedirs(os.path.dirname(save_path), exist_ok=True)
print("\n--- HaShield Centroid Builder ---")

# 1. Load the real-world dataset from Hugging Face
print("1. Downloading TrustAIRLab Jailbreak Dataset...")
# We use the 2023_12_25 split as shown in your screenshot
ds = load_dataset("TrustAIRLab/in-the-wild-jailbreak-prompts", "jailbreak_2023_12_25")

# Extract the actual prompts (Assuming they are in the 'train' split under the 'prompt' column)
# We limit to 1000 prompts for the first run so it doesn't take an hour on your CPU
prompts = ds['train']['prompt'][:1000] 
print(f"-> Successfully loaded {len(prompts)} real-world attack prompts.")

# 2. Load the embedding model
print("\n2. Loading Embedding Model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 3. Calculate embeddings for all 1000 prompts
print("\n3. Encoding prompts to vectors (This may take 1-3 minutes...)")
attack_vectors = model.encode(prompts, show_progress_bar=True)

# 4. Save the ENTIRE matrix of attack vectors, not just the average
print("\n4. Saving the Vector Matrix...")
save_path = "hashield/models/attack_vectors.npy"
np.save(save_path, attack_vectors)

print(f"\n[SUCCESS] Matrix of {len(attack_vectors)} vectors saved to: {save_path}")
print("HaShield will now use K-Nearest Neighbors for zero-day detection!")