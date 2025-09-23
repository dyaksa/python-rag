# Essentials RAG - PDF Question Answering System

## 📋 Overview

Essentials RAG adalah sistem Retrieval-Augmented Generation (RAG) yang memungkinkan Anda untuk mengunggah dokumen PDF dan mengajukan pertanyaan tentang kontennya. Sistem ini menggunakan Google Generative AI untuk embedding dan language model, dengan database vector untuk pencarian similarity.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PDF Upload    │────│   Text Chunking  │────│   Embeddings    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                         │
                                ▼                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query    │────│   Vector Search  │────│   Database      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                         │
        ▼                         ▼
┌─────────────────┐    ┌──────────────────┐
│   LLM Answer    │◄───│   Context RAG    │
└─────────────────┘    └──────────────────┘
```

## 🚀 Features

- **PDF Document Ingestion**: Upload dan proses dokumen PDF
- **Intelligent Text Chunking**: Pembagian teks dengan overlap untuk konteks yang lebih baik
- **Vector Embeddings**: Menggunakan Google Generative AI embedding model
- **Similarity Search**: Pencarian berbasis cosine similarity
- **Question Answering**: RAG-based QA menggunakan Google Gemini
- **RESTful API**: Flask-based web API
- **Database Integration**: Dukungan vector database dengan TiDB

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **AI/ML**:
  - Google Generative AI (Gemini)
  - Langchain
  - Vector embeddings
- **Database**: TiDB dengan vector support
- **PDF Processing**: PyPDF
- **Text Processing**: Tiktoken

## 📁 Project Structure

```
essentials-rag/
├── app.py                      # Entry point aplikasi
├── requirements.txt            # Dependencies Python
├── Makefile                   # Build commands
├── .env.example              # Template environment variables
├── migrations/
│   └── nutritions.sql        # Database schema
└── app/
    ├── adapters/             # External integrations
    │   ├── embbedings.py     # Google AI embeddings
    │   ├── pdf_reader.py     # PDF text extraction
    │   └── tokenizer.py      # Text chunking
    ├── bootstrap/
    │   └── app_bootstrap.py  # Flask app factory
    ├── controller/
    │   └── ingest_controller.py # API endpoints
    ├── core/
    │   └── config.py         # Configuration management
    ├── internal/
    │   └── db.py            # Database connection
    ├── repositories/
    │   └── chunk_repository.py # Data access layer
    └── usecases/
        └── ingest_pdf_usecase.py # Business logic
```

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8+
- MySQL/TiDB dengan vector support
- Google AI API Key

### 1. Clone Repository

```bash
git clone <repository-url>
cd essentials-rag
```

### 2. Setup Virtual Environment

```bash
# Menggunakan Makefile
make venv

# Atau manual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 3. Database Setup

1. Buat database baru di MySQL/TiDB
2. Jalankan migration:

```bash
mysql -h <host> -u <user> -p <database> < migrations/nutritions.sql
```

### 4. Environment Configuration

```bash
cp .env.example .env
```

Edit file `.env` dengan konfigurasi Anda:

```bash
# Application Settings
APP_NAME=Essentials RAG
APP_VERSION=1.0.0
APP_PORT=5000
DEBUG=true

# Google AI Configuration
GOOGLE_API_KEY=your_google_ai_api_key
GOOGLE_LLM_MODEL=gemini-pro
GOOGLE_EMBEDDING_MODEL=text-embedding-004

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name

# RAG Settings
MAX_CHUNK_TOKENS=500
OVERLAP_TOKENS=50
TOP_K=5

# Optional: Langsmith Tracing
LANGSMITH_TRACING=false
LANGSMITH_API_KEY=your_langsmith_key
```

## 🎯 Usage

### 1. Start the Application

```bash
python app.py
```

Server akan berjalan di `http://localhost:5000`

### 2. API Endpoints

#### Upload PDF Document

```bash
POST /api/ingest/upload
```

**Parameters:**

- `file`: PDF file (multipart/form-data)
- `source`: Document source name (optional)
- `max_tokens`: Maximum tokens per chunk (default: 500)
- `overlap_tokens`: Overlap between chunks (default: 50)

**Example:**

```bash
curl -X POST \
  http://localhost:5000/api/ingest/upload \
  -F "file=@document.pdf" \
  -F "source=nutrition_guide" \
  -F "max_tokens=400" \
  -F "overlap_tokens=40"
```

**Response:**

```json
{
  "message": "Document ingested successfully",
  "chunks_count": 25,
  "source": "nutrition_guide"
}
```

#### Ask Question

```bash
POST /api/ingest/ask
```

**Request Body:**

```json
{
  "ask": "Apa itu protein?"
}
```

**Example:**

```bash
curl -X POST \
  http://localhost:5000/api/ingest/ask \
  -H "Content-Type: application/json" \
  -d '{"ask": "Apa manfaat vitamin C?"}'
```

**Response:**

```json
{
  "answer": "Vitamin C memiliki berbagai manfaat untuk kesehatan..."
}
```

## 🔧 Configuration

### RAG Parameters

- **MAX_CHUNK_TOKENS**: Ukuran maksimal setiap chunk teks (default: 500)
- **OVERLAP_TOKENS**: Overlap antar chunk untuk konteks (default: 50)
- **TOP_K**: Jumlah chunk yang diambil untuk context (default: 5)

### Google AI Models

- **Embedding Model**: `text-embedding-004`
- **Language Model**: `gemini-pro`

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**: Pastikan semua dependencies terinstall

```bash
pip install -r requirements.txt
```

2. **Database Connection Error**: Periksa konfigurasi database di `.env`

3. **Google AI API Error**: Pastikan API key valid dan memiliki quota

4. **Memory Issues**: Kurangi `MAX_CHUNK_TOKENS` untuk dokumen besar

### Error Examples

```python
# TypeError: float() argument must be a string or a real number, not 'list'
# Solution: Update GoogleGenerativeAIEmbeddings parameter dari 'google_api_key' ke 'api_key'

# ValueError: Expected a callable type for func
# Solution: Pastikan semua import dan parameter function benar
```

## 📊 Performance Tips

1. **Chunk Size**: Sesuaikan `MAX_CHUNK_TOKENS` berdasarkan domain dokumen
2. **Overlap**: Gunakan overlap 10-20% dari chunk size untuk konteks optimal
3. **Database**: Gunakan vector index untuk performa pencarian
4. **Caching**: Implementasi caching untuk query yang sering digunakan

## 🤝 Contributing

1. Fork repository
2. Buat feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buat Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Support

- **Issues**: [GitHub Issues](link-to-issues)
- **Documentation**: [Wiki](link-to-wiki)
- **Email**: support@example.com

---

**Built with ❤️ using Google Generative AI and Langchain**
