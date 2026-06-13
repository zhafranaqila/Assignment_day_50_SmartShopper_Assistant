# tools/common_information_tool.py

import os
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from google.adk.tools import FunctionTool
from dotenv import load_dotenv

load_dotenv()

# ── Koneksi MongoDB & Model ────────────────────────────────────────
client = MongoClient(os.getenv("MONGODB_URI"))
collection = client["smartshopper"]["common_information"]
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# ── Fungsi Retrieval ───────────────────────────────────────────────
def retrieve_common_information(query: str) -> str:
    """
    Retrieve jawaban untuk pertanyaan umum seputar e-commerce
    seperti pengiriman, pembelian, refund, akun, dan promo.

    Args:
        query: Pertanyaan dari user

    Returns:
        Jawaban relevan berdasarkan data common information
    """
    # Buat embedding dari query user
    query_embedding = model.encode(query).tolist()

    # Ambil semua dokumen dari MongoDB
    documents = list(collection.find({}, {"_id": 0, "question": 1, "answer": 1, "embedding": 1}))

    # Hitung cosine similarity manual
    import numpy as np

    def cosine_similarity(a, b):
        a, b = np.array(a), np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    # Ranking dokumen berdasarkan similarity
    scored = []
    for doc in documents:
        score = cosine_similarity(query_embedding, doc["embedding"])
        scored.append((score, doc))

    # Ambil top 3 dokumen paling relevan
    top_docs = sorted(scored, key=lambda x: x[0], reverse=True)[:3]

    # Susun konteks untuk jawaban
    context = "\n\n".join([
        f"Q: {doc['question']}\nA: {doc['answer']}"
        for _, doc in top_docs
    ])

    return f"Berdasarkan informasi yang tersedia:\n\n{context}"

# ── Bungkus jadi FunctionTool ──────────────────────────────────────
common_info_tool = FunctionTool(retrieve_common_information)