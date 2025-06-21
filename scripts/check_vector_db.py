#!/usr/bin/env python3
"""
Check if there's data in the vector database
"""

import chromadb
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "chroma_db")

def check_vector_db():
    """Check vector database contents"""
    
    try:
        # Initialize Chroma client
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        
        # Get collection
        try:
            collection = client.get_collection(name="xavigate_knowledge")
            print(f"Collection 'xavigate_knowledge' found")
            
            # Check count
            count = collection.count()
            print(f"Total documents in collection: {count}")
            
            if count > 0:
                # Get sample documents
                results = collection.peek(limit=3)
                print("\nSample documents:")
                for i, doc_id in enumerate(results['ids']):
                    print(f"\n{i+1}. ID: {doc_id}")
                    if 'documents' in results and i < len(results['documents']):
                        print(f"   Content: {results['documents'][i][:100]}...")
                    if 'metadatas' in results and i < len(results['metadatas']):
                        print(f"   Metadata: {results['metadatas'][i]}")
            else:
                print("\nNo documents found in collection!")
                
        except Exception as e:
            print(f"Collection not found or error accessing it: {e}")
            
            # List all collections
            collections = client.list_collections()
            print(f"\nAvailable collections: {[c.name for c in collections]}")
            
    except Exception as e:
        print(f"Error connecting to ChromaDB: {e}")
        print(f"Check if ChromaDB path exists: {os.path.exists(CHROMA_DB_PATH)}")

if __name__ == "__main__":
    check_vector_db()