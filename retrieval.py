from qdrant_client import QdrantClient
from embedding import load_embedder, embed_chunks
from loading import load_document
from indexing import COLLECTION_NAME

TOP_K = 3

def retrieve_relevant_chunks(query:str, embedder, client:QdrantClient, topk: int = TOP_K) -> list[dict]:
    query_vector = embedder.encode(query).tolist()
    
    search_results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=topk,
        with_payload=True,
    )

    return [{**search_result.payload, "score": round(search_result.score, 4)} for search_result in search_results.points]

if __name__ == "__main__":
    embedder = load_embedder()
    client = QdrantClient(path="/tmp/langchain_qdrant")
    try:
        query = "What is milkyway"
        relevant_chunks = retrieve_relevant_chunks(query, embedder, client)
        print("Relevant_chunks")
        for chunk in relevant_chunks:
            print(f"Score: {chunk['score']}")
            print(f"Content: {chunk['content']}")
    finally:
        client.close()