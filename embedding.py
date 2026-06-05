
from sentence_transformers import SentenceTransformer
from chunking import build_chunk_text, word_chunks
from loading import load_document

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def load_embedder() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL)

def embed_chunks(chunks: list[dict], embedder: SentenceTransformer):
    chunk_texts = [build_chunk_text(c) for c in chunks]
    print(f"Embedding {len(chunk_texts)} chunks...")
    embeddings = embedder.encode(chunk_texts, show_progress_bar=True)
    print(f"shape: {embeddings.shape}")
    return embeddings

if __name__ == "__main__":
    raw_text = load_document("animals_milkyway_policies.txt")
    chunks = word_chunks(raw_text)

    embedder = load_embedder()
    embeddings = embed_chunks(chunks, embedder)
    print(f"Total vectors/dimension: {len(embeddings[0])}")
    print(f"Total chunks: {len(embeddings)}")
    print(f"Type of embeddings: {type(embeddings)}")
    print(f"Type of embeddings dtype: {embeddings.dtype}")
    print(f"Type of embeddings[0] dtype: {embeddings[0].dtype}")
