import json
from app.internal.db import db
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

def insert_chunk(source: str, chunks: list[str], vectors: list[list[float]]):
    if len(chunks) != len(vectors):
        raise ValueError("Chunks and vectors must have the same length")
    
    connection = db()

    query = """INSERT INTO nutritions (source, chunk_id, text, embedding) 
    VALUES (%s, %s, %s, %s)"""

    try:
        with connection as c, c.cursor() as cursor:
            for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
                cursor.execute(query, (source, i, chunk, json.dumps(vector)))

            c.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        if connection:
            connection.close()


def get_knn(query: str):
    model = GoogleGenerativeAIEmbeddings(model=settings.GOOGLE_EMBEDDING_MODEL, api_key=settings.GOOGLE_API_KEY)
    query_vector = model.embed_query(query)
    # Implement KNN search logic here

    query_embedding_str = str(list(query_vector))

    connection = db()

    sql_query = f"""
    SELECT text FROM nutritions
    ORDER BY VEC_COSINE_DISTANCE(embedding, '{query_embedding_str}')
    LIMIT {settings.TOP_K};
    """

    relevant_chunks = []
    try:
        with connection as c, c.cursor() as cursor:
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            relevant_chunks = [row[0] for row in rows]
    except Exception as e:
        raise e

    context = "\n\n---\n\n".join(relevant_chunks)
    return context