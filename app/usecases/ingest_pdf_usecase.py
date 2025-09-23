from app.adapters.pdf_reader import extract_text_from_pdf
from app.adapters.tokenizer import chunk_text
from app.adapters.embbedings import embed_batch
from app.repositories.chunk_repository import insert_chunk, get_knn
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings

def ingest_pdf_stream(stream, source: str, max_tokens: int, overlap_tokens: int):
    # Extract text from PDF stream
    text = extract_text_from_pdf(stream)
    
    # Chunk the text
    chunks = chunk_text(text, max_tokens=max_tokens, overlap=overlap_tokens)
    
    # Generate embeddings for the chunks
    embeddings = embed_batch(chunks)
    
    # Insert chunks and their embeddings into the database
    insert_chunk(source, chunks, embeddings)

def query_knn(query: str):
    template = """Jawablah pertanyaan pengguna dengan jelas dan ringkas hanya berdasarkan konteks berikut:
    Konteks:
    {context}
    Jika konteks tidak cukup untuk menjawab, katakan "Maaf, saya tidak tahu."
    Pertanyaan: {question}
    Jawaban:
    """
    prompt = ChatPromptTemplate.from_template(template)
    custom_retriever = RunnableLambda(
        lambda x: {"context": get_knn(x["question"])}
    )

    rag_chain = (
        {"context": custom_retriever, "question": RunnablePassthrough()}
        | prompt
        | GoogleGenerativeAI(model=settings.GOOGLE_LLM_MODEL, google_api_key=settings.GOOGLE_API_KEY)
        | StrOutputParser()
    )

    return rag_chain
