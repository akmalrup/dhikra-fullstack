import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Paths
EMBEDDINGS_PATH = "data/embeddings.npy"
METADATA_PATH = "data/ayah_metadata.pkl"

# Load once
#print("Loading embeddings...")
embeddings = np.load(EMBEDDINGS_PATH)
with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)

#print("Embeddings + metadata loaded.")
model = SentenceTransformer("all-MiniLM-L6-v2")


def find_most_similar_ayah(transcript, top_k=3, surah_filter=None):
    """
    Finds the most similar ayah(s) to the input transcript.

    Args:
        transcript (str): Whisper-generated English text
        top_k (int): Number of matches to return
        surah_filter (int or None): If set, restricts matching to a specific surah

    Returns:
        List[dict]: Top-k ayahs with similarity scores
    """

    if surah_filter is not None:
        metadata_filtered = [m for m in metadata if m["surah"] == surah_filter]
        embedding_subset = [embeddings[i] for i, m in enumerate(metadata) if m["surah"] == surah_filter]
    else:
        metadata_filtered = metadata
        embedding_subset = embeddings

    if len(embedding_subset) == 0:
        print(f"No ayahs found for Surah {surah_filter}")
        return []

    query_embedding = model.encode([transcript])[0]
    scores = cosine_similarity([query_embedding], embedding_subset)[0]

    top_indices = np.argsort(scores)[::-1][:top_k]
    results = []

    for i in top_indices:
        match = metadata_filtered[i].copy()
        match["similarity"] = scores[i]
        results.append(match)

    return results
