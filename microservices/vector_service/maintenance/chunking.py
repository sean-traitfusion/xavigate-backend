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
    # Parse path components
    path_obj = Path(path)
    ext = path_obj.suffix
    folder = path_obj.parent.name
    filename = path_obj.stem
    
    print(f"📂 File being chunked: {path}")
    print(f"🧭 Parsed folder = {folder}, filename = {filename}")

    # Load content based on file type
    if ext == ".docx":
        texts = load_docx_texts(path)
    elif ext == ".jsonl":
        texts = load_jsonl_texts(path)
    elif ext == ".md":
        texts = load_md_texts(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # Create base chunks
    base_chunks = chunk_texts(texts)

    # Normalize filename for pattern matching
    normalized_name = filename.lower().replace("-", "").replace("_", "").replace(" ", "")
    print(f"🧩 Normalized name: {normalized_name}")

    # Determine type and tags based on folder and filename
    if folder == "alignment_dynamics":
        type_ = "alignment_module"
        tags = ["alignment_dynamics"]
        
        if "mapper" in normalized_name:
            tags.extend(["alignment_mapper", "practice_tool"])
            print(f"✅ Tagged as alignment_mapper")
        elif "realigner" in normalized_name:
            tags.extend(["realigner_module", "recovery_tool", "sequel_to_mapper"])
            print(f"✅ Tagged as realigner_module")
        elif "unblocking" in normalized_name:
            tags.extend(["unblocking_module", "stuckness", "energetic_reset", "practice_tool"])
            print(f"✅ Tagged as unblocking_module")
        else:
            tags.append("misc_alignment")
            print(f"⚠️ Tagged as misc_alignment")
    
    elif folder == "methods":
        type_ = "method"
        if "menu" in normalized_name:
            tags = ["menu_of_life", "method"]
            print(f"✅ Tagged as menu_of_life")
        elif "task" in normalized_name:
            tags = ["task_trait_alignment", "method"]
            print(f"✅ Tagged as task_trait_alignment")
        else:
            tags = ["method"]
            print(f"✅ Tagged as generic method")
    
    elif folder == "problems":
        type_ = "problem"
        tags = ["burnout", "problem", "focus_areas"]
        print(f"✅ Tagged as problem")
    
    elif folder == "programs":
        type_ = "program" 
        tags = ["mn_reintegration", "program"]
        print(f"✅ Tagged as program")
    
    elif folder == "glossary":
        type_ = "glossary"
        tags = ["glossary"]
        print(f"✅ Tagged as glossary")
    
    else:
        type_ = "uncategorized"
        tags = ["uncategorized"]
        print(f"⚠️ Tagged as uncategorized")

    # Debug output
    print(f"📎 Final tags: {tags}")
    print(f"🏷️ Final type: {type_}")

    # Create enriched chunks - each chunk gets its own copy of the metadata
    enriched_chunks = []
    for chunk in base_chunks:
        enriched_chunk = {
            "content": chunk["content"],
            "metadata": {
                "source": filename.lower().replace(" ", "_").replace("-", "_"),
                "type": type_,
                "tags": tags.copy(),  # Important: create a copy of tags for each chunk
            },
            "chunk_index": chunk["chunk_index"],
            "tokens": chunk["tokens"],
        }
        enriched_chunks.append(enriched_chunk)
    
    print(f"✅ Created {len(enriched_chunks)} chunks")
    return enriched_chunks

if __name__ == "__main__":
    chunks = prepare_chunks("data/alignment_dynamics/Re-Aligner Module.md")
    print(json.dumps(chunks[0], indent=2))