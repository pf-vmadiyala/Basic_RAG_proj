import os
from dotenv import load_dotenv
from groq import Groq
from embedding import load_embedder
from indexing import COLLECTION_NAME
from qdrant_client import QdrantClient
from retrieval import retrieve_relevant_chunks

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model = os.getenv("GROQ_MODEL")
embedder = load_embedder()

SYSTEM_PROMPT = """You are a helpful HR assistant.
                Answer the user's question using ONLY the context provided below.
                If the context does not contain enough information, say so — do not make things up.
                Always cite the section name when referencing specific information."""

def build_context(retrieve_relevant_chunks: list[dict]) -> str:
    parts = []
    for i, chunks in enumerate(retrieve_relevant_chunks, 1):
        parts.append(f"[Source {i}]\n{chunks['content']}")
    return "\n\n".join(parts)


def rag_pipeline(query: str, embedder, client: QdrantClient, top_k: int=5) -> tuple[str, str]:

    
    client = QdrantClient(path="/tmp/langchain_qdrant")
    try:
        relevant_chunks = retrieve_relevant_chunks(query, embedder, client, top_k)
        if not relevant_chunks:
            return "No relevant information found", ""
        
        context = build_context(relevant_chunks)

        groq_client = Groq()
        user_message = f"Context:\n{context}\nQuedtion: {query}"

        groq_response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system", 
                    "content" : SYSTEM_PROMPT
                },
                {
                    "role": "user", 
                    "content": user_message
                },
            ],
            temperature= 0.2
        )
        return groq_response.choices[0].message.content, context
    
    finally:
        client.close()

if __name__ == "__main__":
    query = "What are the policies on leaves?"
    print(f"Quedtion: {query}")
    response, context = rag_pipeline(query, embedder, client)
    print("\n" + "="*50 + "\n")
    print("AI Response:")
    print(response)
    print("\n" + "="*50 + "\n")
    print("Context:")
    print(context)
        
