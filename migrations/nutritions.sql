CREATE TABLE IF NOT EXISTS nutritions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    source VARCHAR(255) NOT NULL,
    chunk_id INT NOT NULL,
    text MEDIUMTEXT NOT NULL,
    embedding VECTOR(768) NOT NULL,
)

-- 3) (Opsional tapi disarankan) Aktifkan TiFlash replica & HNSW index
-- Jika table belum punya replica:
ALTER TABLE pdf_chunks SET TIFLASH REPLICA 1; -- wajib sebelum tambah vector index
-- Buat HNSW index (cosine)
CREATE VECTOR INDEX idx_pdf_chunks_embedding
ON pdf_chunks ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;