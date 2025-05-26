import os
from chromadb import PersistentClient
from uuid import uuid4

# Use same client type as API - ensure absolute path
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "/app/chroma_db")
client = PersistentClient(path=CHROMA_DB_PATH)

print("✅ ChromaDB client initialized")

def store_embeddings(embedded_chunks):
    """Store embeddings in ChromaDB with verification"""
    if not embedded_chunks:
        print("⚠️  No chunks to store")
        return 0
    
    print(f"🧠 Storing {len(embedded_chunks)} embeddings...")
    
    collection = client.get_or_create_collection(
        name="xavigate_knowledge",
        embedding_function=None
    )
    
    # Check initial count
    initial_count = collection.count()
    print(f"📊 Initial collection count: {initial_count}")
    
    successful_adds = 0
    
    for i, chunk in enumerate(embedded_chunks):
        try:
            # Minimal debug for first few chunks
            if i < 3:
                print(f"➡️ Chunk {i+1}: {len(chunk['content'])} chars, {len(chunk['embedding'])} dims")
            
            collection.add(
                documents=[chunk["content"]],
                embeddings=[chunk["embedding"]],
                metadatas=[chunk["metadata"]],
                ids=[chunk.get("id", str(uuid4()))],
            )
            
            successful_adds += 1
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"🟢 Progress: {i+1}/{len(embedded_chunks)} chunks added")
                
        except Exception as e:
            print(f"❌ Error storing chunk {chunk.get('id', 'unknown')}: {e}")
    
    # Verify final count
    final_count = collection.count()
    added_count = final_count - initial_count
    
    print(f"✅ Storage complete!")
    print(f"📊 Successfully processed: {successful_adds}/{len(embedded_chunks)} chunks")
    print(f"📊 Collection count: {initial_count} → {final_count} (+{added_count})")
    
    if added_count != successful_adds:
        print("⚠️  Warning: Count mismatch - some data may not have persisted!")
    
    return successful_adds

def verify_collection():
    """Verify collection state and return count"""
    collection = client.get_or_create_collection(
        name="xavigate_knowledge",
        embedding_function=None
    )
    
    count = collection.count()
    print(f"🔍 Current collection count: {count}")
    
    if count > 0:
        # Sample some data
        sample = collection.get(limit=3)
        print(f"📄 Sample IDs: {sample['ids']}")
        
        # Check for glossary items specifically
        try:
            glossary_sample = collection.get(
                where={"tag": "glossary"},
                limit=3
            )
            glossary_count = len(glossary_sample['ids'])
            print(f"📚 Glossary items: {glossary_count}")
        except:
            print("📚 Could not filter glossary items")
    
    return count

if __name__ == "__main__":
    # Test the collection
    print("🧪 Testing collection...")
    verify_collection()