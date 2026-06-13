# Assignment-day-50--SmartShopper-Assistant

Repositori ini berisi implementasi AI Agent untuk asisten belanja e-commerce menggunakan Google ADK, Gemini, dan MongoDB Atlas. 

Sistem ini dirancang untuk membedakan secara otomatis (*routing*) antara pertanyaan spesifik produk (dijawab langsung oleh LLM) dan pertanyaan operasional/kebijakan toko (diselesaikan menggunakan mekanisme RAG).

## 📂 Struktur Proyek

```text
├── data/
│   └── common_information.py      # Dataset mentah kebijakan e-commerce
├── tools/
│   └── common_information_tool.py # Fungsi retrieval RAG & Cosine Similarity
├── .gitignore                     # Memastikan file .env tidak ter-upload
├── agent.py                       # Inisialisasi Google ADK Agent & system prompt
├── main.py                        # Script runner utama untuk interaksi chat
├── store_data.py                  # Script untuk generate embedding & push ke MongoDB
└── requirements.txt               # Dependensi library python
