
from loading import load_document

CHUNK_SIZE = 50

def word_chunks(text: str, chunk_size: int = CHUNK_SIZE) -> list[dict]:
    clean_lines = []
    for line in text.splitlines():
        line = line.strip().lstrip("#").strip()
        if line:
            clean_lines.append(line)
        
        words = " ".join(clean_lines).split()
        chunks = []
    for i in range(0, len(words), chunk_size):
        content = " ".join(words[i : i + chunk_size])
        chunks.append({
            "chunk_index": len(chunks),
            "content": content,
        })
    return chunks

def build_chunk_text(chunk: dict) -> str:
    return chunk["content"]

if __name__ == "__main__":
    text = load_document("animals_milkyway_policies.txt")
    chunks = word_chunks(text)

    print(f"Total Chucnks: {len(chunks)}")
    print(build_chunk_text(chunks[0]))

    



