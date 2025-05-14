from pathlib import Path
from typing import List, Dict, Optional
import json
import docx
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_docx_texts(path: str) -> List[str]:
    doc = docx.Document(path)
    texts = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            texts.append(text)
    return texts

def load_jsonl_texts(path: str) -> List[str]:
    lines = Path(path).read_text().splitlines()
    texts = []
    for line in lines:
        entry = json.loads(line)
        if "text" in entry:
            texts.append(entry["text"])
        elif "term" in entry and "definition" in entry:
            texts.append(f"{entry['term']}: {entry['definition']}")
    return texts

def load_md_texts(path: str) -> List[str]:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    texts = [line.strip() for line in lines if line.strip()]
    return texts


def chunk_texts(texts: List[str], chunk_size=700, chunk_overlap=100) -> List[Dict]:
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="text-embedding-3-small",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    joined_text = "\n".join(texts)
    chunks = splitter.split_text(joined_text)
    return [{"chunk_index": i, "content": chunk, "tokens": len(chunk.split())} for i, chunk in enumerate(chunks)]

def prepare_chunks(path: str) -> List[Dict]:
    ext = Path(path).suffix
    folder = Path(path).parent.name
    filename = Path(path).stem

    # Load content
    if ext == ".docx":
        texts = load_docx_texts(path)
    elif ext == ".jsonl":
        texts = load_jsonl_texts(path)
    elif ext == ".md":
        texts = load_md_texts(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    base_chunks = chunk_texts(texts)

    # Set type based on folder
    if folder == "methods":
        type_ = "method"
    elif folder == "problems":
        type_ = "problem"
    elif folder == "programs":
        type_ = "program"
    elif folder == "glossary":
        type_ = "glossary"
    elif folder == "alignment_dynamics":
        type_ = "alignment_module"
    else:
        type_ = "unknown"

    # Custom metadata for AD modules
    tags = []
    if folder == "alignment_dynamics":
        tags.append("alignment_dynamics")

        name = filename.lower().replace("-", "").replace("_", "").replace(" ", "")
        if "mapper" in name:
            tags += ["alignment_mapper", "practice_tool"]
        elif "realigner" in name:
            tags += ["realigner_module", "recovery_tool", "sequel_to_mapper"]
        elif "unblocking" in name:
            tags += ["unblocking_module", "stuckness", "energetic_reset", "practice_tool"]
        else:
            tags.append("misc_alignment")

    enriched_chunks = []
    for chunk in base_chunks:
        metadata = {
            "source": filename.lower().replace(" ", "_"),
            "type": type_,
            "tags": tags,
        }

        enriched_chunks.append({
            "content": chunk["content"],
            "metadata": metadata,
            "chunk_index": chunk["chunk_index"],
            "tokens": chunk["tokens"],
        })

    return enriched_chunks

if __name__ == "__main__":
    chunks = prepare_chunks("data/alignment_dynamics/Re-Aligner Module.md")
    print(json.dumps(chunks[0], indent=2))