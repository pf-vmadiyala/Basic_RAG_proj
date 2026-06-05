from qdrant_client import QdrantClient

COLLECTION_NAME = "milkyway_animals_policies_embeddings"

def verify():
    client = QdrantClient(path="/tmp/langchain_qdrant")
    try:
        # 1. Check if collection exists
        exists = client.collection_exists(COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' exists: {exists}")
        if not exists:
            return

        # 2. Get collection info
        info = client.get_collection(COLLECTION_NAME)
        print(f"Collection status: {info.status}")
        print(f"Points count: {info.points_count}")
        
        # 3. Retrieve some points
        print("\nRetrieving first 3 indexed points:")
        points, _ = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=3,
            with_payload=True,
            with_vectors=False
        )
        
        for p in points:
            print(f"- Point ID: {p.id}")
            print(f"  Content: {p.payload.get('content', '')[:120]}...")
            
    finally:
        client.close()

if __name__ == "__main__":
    verify()
