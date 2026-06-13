# store_data.py

import os
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from data.common_information import common_info_data

load_dotenv()

# ── Koneksi MongoDB Atlas ──────────────────────────────────────────
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["smartshopper"]
collection = db["common_information"]

# ── Load embedding model ───────────────────────────────────────────
# Model ringan, cocok untuk teks Bahasa Indonesia
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def store_documents():
    # Hindari duplikasi: hapus data lama dulu
    collection.delete_many({})
    print("🗑️  Koleksi lama dihapus.")

    documents = []
    for item in common_info_data:
        # Buat embedding dari gabungan question + answer
        text_to_embed = f"{item['question']} {item['answer']}"
        embedding = model.encode(text_to_embed).tolist()

        doc = {
            "category": item["category"],
            "question": item["question"],
            "answer": item["answer"],
            "embedding": embedding,  # Vector untuk RAG retrieval
        }
        documents.append(doc)

    collection.insert_many(documents)
    print(f"✅ {len(documents)} dokumen berhasil disimpan ke MongoDB Atlas.")

if __name__ == "__main__":
    store_documents()