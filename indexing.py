from loading import load_document
from embedding import load_embedder, embed_chunks
from chunking import word_chunks
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

COLLECTION_NAME = "milkyway_animals_policies_embeddings"

def create_collection( chunks: list[dict], embeddings, client:QdrantClient, dim: int):
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size = dim,
            distance=Distance.COSINE,
        )
    )

    points = [
        PointStruct(
            id = idx,
            vector=embedding.tolist(),
            payload = {"content": chunk["content"]},
        )
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings))
    ]

    result = client.upsert(
        collection_name = COLLECTION_NAME,
        points = points,
        wait = True,
    )

    print(f"Indexed {len(points)} Points Status: {result.status}")
    print("Points indexed successfully!")
    
    info = client.get_collection(COLLECTION_NAME)
    print(f" Collection Status: {info.status}")
    print(f" Points Count: {info.points_count}")
    print(f"Vector config: {info.config.params.vectors}")
    print(f"Dimensions: {info.config.params.vectors.size}")
    print(f"Distance: {info.config.params.vectors.distance}")

    
    # return result

if __name__ == "__main__":
    text = load_document("animals_milkyway_policies.txt")
    chunks = word_chunks(text)
    embedder = load_embedder()
    embeddings = embed_chunks(chunks, embedder)
    
    client = QdrantClient(path="/tmp/langchain_qdrant")
    try:
        create_collection(chunks, embeddings, client, dim = embedder.get_embedding_dimension())
    finally:
        client.close()
