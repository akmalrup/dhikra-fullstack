import pandas as pd
import numpy as np
import os
import pickle
from sentence_transformers import SentenceTransformer

# Paths
DATASET_PATH = "data/ayah_dataset.csv"
EMBEDDINGS_PATH = "data/embeddings.npy"
METADATA_PATH = "data/ayah_metadata.pkl"

# Load ayah data
df = pd.read_csv(DATASET_PATH)
texts = df["english_text"].tolist()

# Load sentence-transformer model
print("🔄 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
print("🔁 Generating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)

# Save embeddings to .npy
np.save(EMBEDDINGS_PATH, embeddings)
print(f"Saved embeddings to {EMBEDDINGS_PATH}")

# Save metadata (so we can map embeddings back to ayahs)
metadata = df[["surah", "ayah", "arabic_text", "english_text"]].to_dict(orient="records")
with open(METADATA_PATH, "wb") as f:
    pickle.dump(metadata, f)
print(f"Saved metadata to {METADATA_PATH}")
