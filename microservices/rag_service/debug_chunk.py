from pathlib import Path
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_jsonl_texts(path: str):
    lines = Path(path).read_text().splitlines()
    texts = []
    for line in lines:
        entry = json.loads(line)
        if 'text' in entry:
            texts.append(entry['text'])
    return texts

def chunk_texts(texts):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="text-embedding-3-small",
        chunk_size=700,
        chunk_overlap=100,
    )
    print(f"Loaded {len(texts)} base texts")
    joined = "\n".join(texts)
    chunks = splitter.split_text(joined)
    print(f"Split into {len(chunks)} chunks")
    print("Sample chunk:", chunks[0] if chunks else "None")

if __name__ == "__main__":
    texts = load_jsonl_texts("docs/kb/glossary/glossary.jsonl")
    chunk_texts(texts)