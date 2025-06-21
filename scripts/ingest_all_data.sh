#!/bin/bash

echo "=============================================="
echo "Xavigate Full Data Ingestion Script"
echo "=============================================="

# Function to run command in docker
run_in_docker() {
    docker exec xavigate_vector_service bash -c "$1"
}

# Step 1: Clear existing data
echo ""
echo "Step 1: Clearing existing ChromaDB data..."
run_in_docker "rm -rf /app/chroma_db/*"

# Step 2: Run chunking for all documents
echo ""
echo "Step 2: Chunking documents..."
run_in_docker "cd /app/maintenance && python bulk_chunk_all.py /app/docs/kb"

# Step 3: Ingest glossary
echo ""
echo "Step 3: Ingesting glossary..."
run_in_docker "cd /app/maintenance && python ingest_glossary.py"

# Step 4: Ingest career chunks directly
echo ""
echo "Step 4: Ingesting career chunks..."
run_in_docker "cd /app/maintenance && python -c \"
import json
import sys
import os
from pathlib import Path
sys.path.append('/app')
from maintenance.embeddings import get_embedding
from chromadb import PersistentClient
from uuid import uuid4

# Initialize ChromaDB
client = PersistentClient(path='/app/chroma_db')
collection = client.get_or_create_collection(name='xavigate_knowledge')

# Load career chunks
careers_file = Path('/app/docs/kb/careers/mn_careers_chunks.jsonl')
if careers_file.exists():
    print(f'Loading career chunks from {careers_file}')
    chunks_added = 0
    
    with open(careers_file, 'r') as f:
        for line in f:
            try:
                chunk = json.loads(line.strip())
                content = chunk.get('text', '')
                if content:
                    embedding = get_embedding(content)
                    metadata = {
                        'title': chunk.get('title', 'Career'),
                        'type': 'career',
                        'tags': 'careers minnesota',
                        'tag': 'careers',
                        'source': 'mn_careers_chunks.jsonl'
                    }
                    collection.add(
                        documents=[content],
                        metadatas=[metadata],
                        ids=[str(uuid4())],
                        embeddings=[embedding]
                    )
                    chunks_added += 1
                    if chunks_added % 50 == 0:
                        print(f'Progress: {chunks_added} career chunks added')
            except Exception as e:
                print(f'Error processing career chunk: {e}')
                continue
    
    print(f'✅ Added {chunks_added} career chunks')
else:
    print('⚠️ Career chunks file not found')
\""

# Step 5: Ingest other document chunks
echo ""
echo "Step 5: Ingesting other document chunks..."
run_in_docker "cd /app/maintenance && python -c \"
import json
import sys
import os
from pathlib import Path
sys.path.append('/app')
from maintenance.embeddings import get_embedding
from chromadb import PersistentClient
from uuid import uuid4

# Initialize ChromaDB
client = PersistentClient(path='/app/chroma_db')
collection = client.get_or_create_collection(name='xavigate_knowledge')

# Process bulk chunks but skip career data
chunks_file = Path('/app/maintenance/bulk_chunks_all.jsonl')
if chunks_file.exists():
    print(f'Loading chunks from {chunks_file}')
    chunks_added = 0
    
    with open(chunks_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                # Skip empty lines
                if not line.strip():
                    continue
                    
                chunk = json.loads(line.strip())
                
                # Skip career chunks (already processed)
                if 'careers' in chunk.get('metadata', {}).get('source', '').lower():
                    continue
                
                content = chunk.get('content', chunk.get('text', ''))
                if content:
                    embedding = get_embedding(content)
                    metadata = chunk.get('metadata', {})
                    
                    # Ensure required fields
                    if 'tags' in metadata and isinstance(metadata['tags'], list):
                        metadata['tags'] = ' '.join(metadata['tags'])
                        metadata['tag'] = metadata['tags'].split()[0] if metadata['tags'] else 'uncategorized'
                    
                    collection.add(
                        documents=[content],
                        metadatas=[metadata],
                        ids=[str(uuid4())],
                        embeddings=[embedding]
                    )
                    chunks_added += 1
                    if chunks_added % 10 == 0:
                        print(f'Progress: {chunks_added} document chunks added')
            except json.JSONDecodeError as e:
                # Skip malformed lines silently
                continue
            except Exception as e:
                print(f'Error on line {line_num}: {e}')
                continue
    
    print(f'✅ Added {chunks_added} document chunks')
else:
    print('⚠️ Bulk chunks file not found')
\""

# Step 6: Verify ingestion
echo ""
echo "Step 6: Verifying ingestion..."
run_in_docker "cd /app && python -c \"
from chromadb import PersistentClient

client = PersistentClient(path='/app/chroma_db')
collection = client.get_or_create_collection(name='xavigate_knowledge')

count = collection.count()
print(f'\\n✅ Total documents in collection: {count}')

if count > 0:
    # Get sample data
    sample = collection.get(limit=5)
    print(f'\\nSample documents:')
    for i, (doc, meta) in enumerate(zip(sample['documents'], sample['metadatas'])):
        print(f'  {i+1}. {meta.get(\"title\", \"Unknown\")} - Tags: {meta.get(\"tags\", \"none\")}')
        print(f'     Content preview: {doc[:100]}...')
\""

echo ""
echo "=============================================="
echo "Ingestion complete!"
echo "=============================================="