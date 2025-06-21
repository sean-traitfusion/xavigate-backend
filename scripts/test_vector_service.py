#!/usr/bin/env python3
"""
Comprehensive Test Script for Xavigate Vector Service

This script tests all aspects of the vector service to ensure it's
functioning correctly after cleanup and ingestion.

Tests include:
1. Service health check
2. Search functionality
3. Collection verification
4. Integration with chat service
5. Performance benchmarks

Usage:
    python test_vector_service.py [--verbose]
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
import httpx
from typing import List, Dict, Any
import statistics

# Configuration
VECTOR_SERVICE_URL = os.getenv("VECTOR_SERVICE_URL", "http://localhost:8017")
CHAT_SERVICE_URL = os.getenv("CHAT_SERVICE_URL", "http://localhost:8015")

# Test data
TEST_QUERIES = [
    # Knowledge base queries
    {"query": "alignment dynamics", "expected_tags": ["alignment_mapper", "realigner_module"]},
    {"query": "menu of life", "expected_tags": ["menu_of_life"]},
    {"query": "glossary", "expected_tags": ["glossary"]},
    {"query": "careers minnesota", "expected_tags": ["careers", "minnesota"]},
    {"query": "task trait alignment", "expected_tags": ["task_trait_alignment"]},
    {"query": "burnout", "expected_tags": ["burnout", "problem"]},
    {"query": "reintegration program", "expected_tags": ["mn_reintegration", "program"]},
    
    # Edge cases
    {"query": "xyz123nonexistent", "expected_tags": []},  # Should return results but maybe not relevant
    {"query": "", "expected_tags": []},  # Empty query
    {"query": "a", "expected_tags": []},  # Single character
]


class VectorServiceTester:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "details": []
        }
        
    def log(self, message: str, level: str = "INFO"):
        """Log a message with formatting"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        symbols = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "TEST": "🧪"
        }
        symbol = symbols.get(level, "•")
        print(f"[{timestamp}] {symbol} {message}")
        
    def add_result(self, test_name: str, passed: bool, message: str = "", warning: bool = False):
        """Add a test result"""
        if passed and not warning:
            self.results["passed"] += 1
            if self.verbose:
                self.log(f"{test_name}: {message}", "SUCCESS")
        elif warning:
            self.results["warnings"] += 1
            self.log(f"{test_name}: {message}", "WARNING")
        else:
            self.results["failed"] += 1
            self.log(f"{test_name}: {message}", "ERROR")
            
        self.results["details"].append({
            "test": test_name,
            "passed": passed,
            "message": message,
            "warning": warning
        })
    
    def test_health(self):
        """Test 1: Service Health Check"""
        self.log("Testing service health...", "TEST")
        
        try:
            response = httpx.get(f"{VECTOR_SERVICE_URL}/health", timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                self.add_result("Health Check", True, f"Service healthy: {data}")
            else:
                self.add_result("Health Check", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.add_result("Health Check", False, f"Connection failed: {e}")
    
    def test_search_functionality(self):
        """Test 2: Search Functionality"""
        self.log("Testing search functionality...", "TEST")
        
        for test_case in TEST_QUERIES:
            query = test_case["query"]
            expected_tags = test_case["expected_tags"]
            
            try:
                response = httpx.post(
                    f"{VECTOR_SERVICE_URL}/search",
                    json={"query": query, "top_k": 5},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    results = response.json()
                    
                    # Check if we got results
                    if isinstance(results, list) and len(results) > 0:
                        # Check for expected tags in results
                        found_tags = set()
                        for result in results:
                            if "metadata" in result and "tags" in result["metadata"]:
                                found_tags.update(result["metadata"]["tags"])
                        
                        if expected_tags:
                            matching_tags = set(expected_tags) & found_tags
                            if matching_tags:
                                self.add_result(
                                    f"Search '{query}'", 
                                    True, 
                                    f"Found {len(results)} results with tags: {matching_tags}"
                                )
                            else:
                                self.add_result(
                                    f"Search '{query}'", 
                                    False, 
                                    f"Expected tags {expected_tags} not found. Found: {found_tags}"
                                )
                        else:
                            # For edge cases, just check that we handled them gracefully
                            self.add_result(
                                f"Search '{query}'", 
                                True, 
                                f"Handled gracefully with {len(results)} results"
                            )
                    else:
                        if not expected_tags:  # Edge case queries might return no results
                            self.add_result(f"Search '{query}'", True, "No results (expected for edge case)")
                        else:
                            self.add_result(f"Search '{query}'", False, "No results returned")
                else:
                    self.add_result(f"Search '{query}'", False, f"Status {response.status_code}")
                    
            except Exception as e:
                self.add_result(f"Search '{query}'", False, f"Error: {e}")
    
    def test_collection_info(self):
        """Test 3: Collection Verification"""
        self.log("Testing collection information...", "TEST")
        
        try:
            response = httpx.get(f"{VECTOR_SERVICE_URL}/debug/chromadb", timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                
                # Check collection name
                if data.get("collection_name") == "xavigate_knowledge":
                    self.add_result("Collection Name", True, "Using correct collection: xavigate_knowledge")
                else:
                    self.add_result("Collection Name", False, f"Wrong collection: {data.get('collection_name')}")
                
                # Check document count
                count = data.get("count", 0)
                if count > 0:
                    self.add_result("Document Count", True, f"Collection has {count} documents")
                else:
                    self.add_result("Document Count", False, "Collection is empty")
                
                # Check metadata structure
                if "sample_metadata" in data and data["sample_metadata"]:
                    self.add_result("Metadata Structure", True, "Metadata present and structured correctly")
                    
                    # Verify tag diversity
                    all_tags = set()
                    for metadata in data["sample_metadata"]:
                        if "tags" in metadata:
                            all_tags.update(metadata["tags"])
                    
                    if len(all_tags) >= 5:
                        self.add_result("Tag Diversity", True, f"Found {len(all_tags)} unique tags")
                    else:
                        self.add_result("Tag Diversity", False, f"Low tag diversity: {all_tags}")
                else:
                    self.add_result("Metadata Structure", False, "No metadata found")
                    
            else:
                self.add_result("Collection Info", False, f"Status {response.status_code}")
                
        except Exception as e:
            self.add_result("Collection Info", False, f"Error: {e}")
    
    def test_performance(self):
        """Test 4: Performance Benchmarks"""
        self.log("Testing search performance...", "TEST")
        
        query_times = []
        test_query = "alignment dynamics"
        
        try:
            # Warm up
            httpx.post(f"{VECTOR_SERVICE_URL}/search", json={"query": test_query, "top_k": 5})
            
            # Run multiple queries
            for i in range(10):
                start_time = time.time()
                response = httpx.post(
                    f"{VECTOR_SERVICE_URL}/search",
                    json={"query": test_query, "top_k": 5},
                    timeout=10.0
                )
                end_time = time.time()
                
                if response.status_code == 200:
                    query_times.append((end_time - start_time) * 1000)  # Convert to ms
            
            if query_times:
                avg_time = statistics.mean(query_times)
                p95_time = sorted(query_times)[int(len(query_times) * 0.95)]
                
                if avg_time < 100:  # Less than 100ms average
                    self.add_result("Performance", True, f"Avg: {avg_time:.2f}ms, P95: {p95_time:.2f}ms")
                elif avg_time < 500:  # Less than 500ms
                    self.add_result("Performance", True, f"Avg: {avg_time:.2f}ms, P95: {p95_time:.2f}ms", warning=True)
                else:
                    self.add_result("Performance", False, f"Slow: Avg {avg_time:.2f}ms")
            else:
                self.add_result("Performance", False, "Could not measure performance")
                
        except Exception as e:
            self.add_result("Performance", False, f"Error: {e}")
    
    def test_chat_integration(self):
        """Test 5: Chat Service Integration"""
        self.log("Testing chat service integration...", "TEST")
        
        # Skip if chat service URL not configured
        if CHAT_SERVICE_URL == "http://localhost:8015":
            try:
                # Quick check if chat service is running
                httpx.get(f"{CHAT_SERVICE_URL}/health", timeout=2.0)
            except:
                self.add_result("Chat Integration", True, "Skipped (chat service not running)", warning=True)
                return
        
        try:
            # Test chat request with RAG
            chat_request = {
                "userId": "test-user",
                "username": "test_user",
                "fullName": "Test User",
                "traitScores": {f"trait_{i}": 5.0 for i in range(19)},
                "message": "What is alignment dynamics?",
                "sessionId": "test-session"
            }
            
            response = httpx.post(
                f"{CHAT_SERVICE_URL}/query",
                json=chat_request,
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if sources were returned
                if "sources" in data and len(data["sources"]) > 0:
                    self.add_result("Chat RAG Integration", True, f"Chat returned {len(data['sources'])} sources")
                else:
                    self.add_result("Chat RAG Integration", False, "No RAG sources in chat response")
                    
            else:
                self.add_result("Chat Integration", False, f"Status {response.status_code}")
                
        except Exception as e:
            self.add_result("Chat Integration", False, f"Error: {e}")
    
    def test_error_handling(self):
        """Test 6: Error Handling"""
        self.log("Testing error handling...", "TEST")
        
        # Test invalid request
        try:
            response = httpx.post(
                f"{VECTOR_SERVICE_URL}/search",
                json={"invalid": "request"},
                timeout=5.0
            )
            
            if 400 <= response.status_code < 500:
                self.add_result("Error Handling", True, "Properly handles invalid requests")
            else:
                self.add_result("Error Handling", False, f"Unexpected status for invalid request: {response.status_code}")
                
        except Exception as e:
            self.add_result("Error Handling", False, f"Error: {e}")
    
    def run_all_tests(self):
        """Run all tests"""
        self.log("Starting Vector Service Test Suite", "INFO")
        self.log(f"Vector Service URL: {VECTOR_SERVICE_URL}", "INFO")
        
        print("\n" + "="*60)
        
        # Run tests
        self.test_health()
        self.test_search_functionality()
        self.test_collection_info()
        self.test_performance()
        self.test_chat_integration()
        self.test_error_handling()
        
        # Summary
        print("\n" + "="*60)
        self.log("Test Summary", "INFO")
        print("="*60)
        
        total = self.results["passed"] + self.results["failed"]
        success_rate = (self.results["passed"] / total * 100) if total > 0 else 0
        
        self.log(f"Passed: {self.results['passed']}", "SUCCESS")
        self.log(f"Failed: {self.results['failed']}", "ERROR" if self.results["failed"] > 0 else "INFO")
        self.log(f"Warnings: {self.results['warnings']}", "WARNING" if self.results["warnings"] > 0 else "INFO")
        self.log(f"Success Rate: {success_rate:.1f}%", "INFO")
        
        # Detailed failures
        if self.results["failed"] > 0:
            print("\nFailed Tests:")
            for detail in self.results["details"]:
                if not detail["passed"] and not detail["warning"]:
                    print(f"  - {detail['test']}: {detail['message']}")
        
        return self.results["failed"] == 0


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Test Xavigate vector service")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    tester = VectorServiceTester(verbose=args.verbose)
    success = tester.run_all_tests()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())