import os
import shutil

original_symlink = getattr(os, "symlink", None)
def symlink_wrapper(src, dst, *args, **kwargs):
    if not os.path.isabs(src):
        src = os.path.join(os.path.dirname(dst), src)
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
os.symlink = symlink_wrapper

import pandas as pd

from dotenv import load_dotenv
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()

# -----------------------------
# Configuration
# -----------------------------

CSV_PATH = r"E:\Calorie calculator\data\Indian_Food_Nutrition_Processed.csv"
COLLECTION_NAME = "indian_foods"

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv(CSV_PATH)

print(f"Loaded {len(df)} food records.")

# -----------------------------
# Convert rows to Documents
# -----------------------------

documents = []

for _, row in df.iterrows():

    text = f"""
Food: {row['Food']}
Calories: {row['Calories (kcal)']} kcal
Protein: {row['Protein (g)']} g
Carbohydrates: {row['Carbohydrates (g)']} g
Fat: {row['Fats (g)']} g
Fibre: {row['Fibre (g)']} g
"""

    documents.append(
        Document(
            page_content=text.strip(),
            metadata={
                "food": row["Food"]
            }
        )
    )

print(f"Created {len(documents)} documents.")

# -----------------------------
# Connect to Qdrant
# -----------------------------

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    check_compatibility=False
)

client.set_model("sentence-transformers/all-MiniLM-L6-v2")
client.set_sparse_model("prithivida/Splade_PP_en_v1")

# Recreate collection to ensure dense + sparse setup
if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(COLLECTION_NAME)

print("Uploading vectors to Qdrant using fastembed (Dense + Sparse)...")

client.add(
    collection_name=COLLECTION_NAME,
    documents=[doc.page_content for doc in documents],
    metadata=[
        {
            "text": doc.page_content,
            "food": doc.metadata["food"],
        } 
        for doc in documents
    ],
    ids=[i for i in range(len(documents))]
)

print("Food data successfully uploaded to Qdrant.")
print(f"Total vectors: {len(documents)}")