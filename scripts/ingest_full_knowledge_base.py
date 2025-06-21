#!/usr/bin/env python3
"""
Full Knowledge Base Ingestion Pipeline for Xavigate Vector Service

This script performs a complete ingestion of all knowledge base documents
into the vector database (ChromaDB) with the xavigate_knowledge collection.

Steps:
1. Clear existing data (optional)
2. Convert raw documents to chunks
3. Ingest glossary
4. Ingest document chunks
5. Verify ingestion

Usage:
    python ingest_full_knowledge_base.py [--clear-existing]
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
import httpx

# Add the maintenance directory to Python path
BACKEND_ROOT = Path(__file__).parent.parent
MAINTENANCE_DIR = BACKEND_ROOT / "microservices" / "vector_service" / "maintenance"
sys.path.insert(0, str(MAINTENANCE_DIR))

# Configuration
KB_DIR = BACKEND_ROOT / "docs" / "kb"
VECTOR_SERVICE_URL = os.getenv("VECTOR_SERVICE_URL", "http://localhost:8017")


def print_header(message):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f" {message}")
    print(f"{'='*60}\n")


def print_status(message, status="INFO"):
    """Print a status message with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status_symbols = {
        "INFO": "ℹ️",
        "SUCCESS": "✅",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "PROCESSING": "⏳"
    }
    symbol = status_symbols.get(status, "•")
    print(f"[{timestamp}] {symbol} {message}")


def check_vector_service():
    """Check if vector service is accessible"""
    try:
        response = httpx.get(f"{VECTOR_SERVICE_URL}/health")
        if response.status_code == 200:
            print_status("Vector service is running", "SUCCESS")
            return True
        else:
            print_status(f"Vector service returned status {response.status_code}", "ERROR")
            return False
    except Exception as e:
        print_status(f"Cannot connect to vector service: {e}", "ERROR")
        return False


def clear_existing_data():
    """Clear existing ChromaDB data"""
    print_status("Clearing existing ChromaDB data...", "PROCESSING")
    
    chroma_dir = BACKEND_ROOT / "microservices" / "vector_service" / "chroma_db"
    if chroma_dir.exists():
        import shutil
        shutil.rmtree(chroma_dir)
        print_status("Cleared existing ChromaDB data", "SUCCESS")
    else:
        print_status("No existing ChromaDB data found", "INFO")


def run_chunking():
    """Run the bulk chunking process"""
    print_header("Step 1: Chunking Documents")
    
    # Change to maintenance directory
    os.chdir(MAINTENANCE_DIR)
    
    # Run bulk_chunk_all.py
    print_status("Running bulk chunking script...", "PROCESSING")
    result = subprocess.run(
        [sys.executable, "bulk_chunk_all.py", str(KB_DIR)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_status("Document chunking completed", "SUCCESS")
        
        # Check if output file was created
        output_file = MAINTENANCE_DIR / "bulk_chunks_all_cleaned.jsonl"
        if output_file.exists():
            with open(output_file, 'r') as f:
                chunk_count = sum(1 for _ in f)
            print_status(f"Created {chunk_count} chunks", "INFO")
        else:
            print_status("Warning: No chunks file created", "WARNING")
            return False
    else:
        print_status(f"Chunking failed: {result.stderr}", "ERROR")
        return False
    
    return True


def ingest_glossary():
    """Ingest glossary data"""
    print_header("Step 2: Ingesting Glossary")
    
    os.chdir(MAINTENANCE_DIR)
    
    # First, convert CSV to JSONL if needed
    glossary_csv = KB_DIR / "glossary" / "glossary.csv"
    glossary_jsonl = KB_DIR / "glossary" / "glossary.jsonl"
    
    if glossary_csv.exists() and not glossary_jsonl.exists():
        print_status("Converting glossary CSV to JSONL...", "PROCESSING")
        result = subprocess.run(
            [sys.executable, "convert_glossary_csv_to_jsonl.py"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print_status(f"Glossary conversion failed: {result.stderr}", "ERROR")
            return False
    
    # Ingest glossary
    print_status("Ingesting glossary entries...", "PROCESSING")
    result = subprocess.run(
        [sys.executable, "ingest_glossary.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_status("Glossary ingestion completed", "SUCCESS")
        if result.stdout:
            # Extract count from output if available
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if "ingested" in line.lower():
                    print_status(line.strip(), "INFO")
    else:
        print_status(f"Glossary ingestion failed: {result.stderr}", "ERROR")
        return False
    
    return True


def ingest_chunks():
    """Ingest document chunks"""
    print_header("Step 3: Ingesting Document Chunks")
    
    os.chdir(MAINTENANCE_DIR)
    
    print_status("Ingesting document chunks...", "PROCESSING")
    result = subprocess.run(
        [sys.executable, "ingest_chunks.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_status("Document chunk ingestion completed", "SUCCESS")
        if result.stdout:
            # Extract count from output if available
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if "ingested" in line.lower() or "processed" in line.lower():
                    print_status(line.strip(), "INFO")
    else:
        print_status(f"Chunk ingestion failed: {result.stderr}", "ERROR")
        return False
    
    return True


def verify_ingestion():
    """Verify the ingestion by testing vector search"""
    print_header("Step 4: Verifying Ingestion")
    
    test_queries = [
        "alignment dynamics",
        "glossary",
        "career",
        "menu of life",
        "Minnesota"
    ]
    
    success_count = 0
    
    for query in test_queries:
        try:
            response = httpx.post(
                f"{VECTOR_SERVICE_URL}/search",
                json={"query": query, "top_k": 3},
                timeout=10.0
            )
            
            if response.status_code == 200:
                results = response.json()
                if results and len(results) > 0:
                    print_status(f"Query '{query}': Found {len(results)} results", "SUCCESS")
                    success_count += 1
                else:
                    print_status(f"Query '{query}': No results found", "WARNING")
            else:
                print_status(f"Query '{query}': Failed with status {response.status_code}", "ERROR")
                
        except Exception as e:
            print_status(f"Query '{query}': Error - {e}", "ERROR")
    
    print_status(f"Verification complete: {success_count}/{len(test_queries)} queries successful", 
                 "SUCCESS" if success_count == len(test_queries) else "WARNING")
    
    return success_count > 0


def get_collection_stats():
    """Get statistics about the ingested collection"""
    print_header("Collection Statistics")
    
    try:
        # Try to get debug info from vector service
        response = httpx.get(f"{VECTOR_SERVICE_URL}/debug/chromadb")
        if response.status_code == 200:
            data = response.json()
            print_status(f"Collection: {data.get('collection_name', 'Unknown')}", "INFO")
            print_status(f"Total documents: {data.get('count', 'Unknown')}", "INFO")
            
            if 'sample_metadata' in data and data['sample_metadata']:
                print_status("Sample metadata tags:", "INFO")
                for metadata in data['sample_metadata'][:5]:
                    tags = metadata.get('tags', [])
                    if tags:
                        print(f"  - {', '.join(tags)}")
    except Exception as e:
        print_status(f"Could not get collection stats: {e}", "WARNING")


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Ingest full knowledge base into vector service")
    parser.add_argument(
        "--clear-existing",
        action="store_true",
        help="Clear existing ChromaDB data before ingestion"
    )
    parser.add_argument(
        "--skip-verification",
        action="store_true",
        help="Skip verification step"
    )
    args = parser.parse_args()
    
    print_header("Xavigate Knowledge Base Ingestion Pipeline")
    print_status(f"Knowledge Base Directory: {KB_DIR}", "INFO")
    print_status(f"Vector Service URL: {VECTOR_SERVICE_URL}", "INFO")
    
    # Check if running in Docker or local
    if os.path.exists("/.dockerenv"):
        print_status("Running inside Docker container", "INFO")
    else:
        print_status("Running locally", "INFO")
    
    # Check vector service
    if not check_vector_service():
        print_status("Please ensure the vector service is running", "ERROR")
        print_status("For local development: cd microservices/vector_service && python main.py", "INFO")
        print_status("For Docker: docker-compose up vector_service", "INFO")
        return 1
    
    # Clear existing data if requested
    if args.clear_existing:
        clear_existing_data()
    
    # Run ingestion pipeline
    success = True
    
    if not run_chunking():
        success = False
    
    if success and not ingest_glossary():
        success = False
    
    if success and not ingest_chunks():
        success = False
    
    # Verify ingestion
    if success and not args.skip_verification:
        if not verify_ingestion():
            print_status("Verification showed potential issues", "WARNING")
    
    # Show statistics
    if success:
        get_collection_stats()
    
    # Final status
    print_header("Ingestion Pipeline Complete")
    if success:
        print_status("All steps completed successfully!", "SUCCESS")
        print_status("The vector service is now ready to serve queries", "INFO")
        return 0
    else:
        print_status("Some steps failed. Please check the errors above.", "ERROR")
        return 1


if __name__ == "__main__":
    sys.exit(main())