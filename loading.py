import pathlib

def load_document(filepath: str) -> str:
    path = pathlib.Path(filepath)
    if not path.exists():
        raise FileNotFoundError(
            print(f"File not found in {path.resolve}\n")
        )
    return path.read_text(encoding="utf-8")

if __name__ == "__main__":
    raw_text = load_document("animals_milkyway_policies.txt")
    print(f"Polcices Loaded, it has {len(raw_text)} characters")
    print(raw_text[:400])
    