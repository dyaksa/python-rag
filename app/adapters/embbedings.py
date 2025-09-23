from __future__ import annotations
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

def embbed_text(text: str) -> list[float]:
    """Mengembalikan embedding (1x768) untuk teks."""
    model = GoogleGenerativeAIEmbeddings(model=settings.GOOGLE_EMBEDDING_MODEL, api_key=settings.GOOGLE_API_KEY)
    embedding = model.embed_query(text)
    return embedding

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Mengembalikan list embedding (Nx768) untuk list teks."""
    if not texts:
        return []
    
    all_embeddings = []

    for i in range(0, len(texts), 16):
        batch = texts[i:i + 16]
        model = GoogleGenerativeAIEmbeddings(model=settings.GOOGLE_EMBEDDING_MODEL, api_key=settings.GOOGLE_API_KEY)
        batch_embeddings = model.embed_documents(batch)
        if i == 0:
            all_embeddings = batch_embeddings
        else:
            all_embeddings.extend(batch_embeddings)
    
    return all_embeddings
    