#!/usr/bin/env python3
"""
Test Suite for Life/Non-Career Queries

This script tests how well the RAG system handles various life topics
beyond career advice, ensuring career content doesn't dominate.
"""

import sys
import os
import json
import httpx
from typing import Dict, List

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'microservices', 'chat_service'))
from rag_filter import RAGQueryFilter, filter_rag_query

# Configuration
VECTOR_SERVICE_URL = os.getenv("VECTOR_SERVICE_URL", "http://localhost:8017")


def test_query(query: str, expected_context: str) -> Dict:
    """Test a single query and analyze results"""
    print(f"\n{'='*60}")
    print(f"Query: '{query}'")
    print(f"Expected context: {expected_context}")
    print("-" * 60)
    
    # Get filter params
    filter_params = filter_rag_query(query)
    print(f"Filter params: {filter_params}")
    
    # Make vector search request
    try:
        response = httpx.post(
            f"{VECTOR_SERVICE_URL}/search",
            json={"query": query, "top_k": 5},
            timeout=10.0
        )
        
        if response.status_code == 200:
            results = response.json()
            
            # Analyze results
            topic_counts = {}
            for result in results:
                topic = result.get('topic', 'unknown')
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
            print(f"\nResults by topic:")
            for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  {topic}: {count}")
            
            # Show sample results
            print(f"\nTop 3 results:")
            for i, result in enumerate(results[:3]):
                title = result.get('title', 'Unknown')
                chunk = result.get('chunk', '')[:150]
                print(f"\n{i+1}. [{result.get('topic')}] {title}")
                print(f"   {chunk}...")
            
            return {
                'query': query,
                'expected': expected_context,
                'results': results,
                'topic_counts': topic_counts
            }
        else:
            print(f"Error: Status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None


def run_test_suite():
    """Run comprehensive test suite for life queries"""
    print("\nXavigate Life Query Test Suite")
    print("Testing non-career life alignment queries\n")
    
    test_cases = [
        # Workplace relationships (not career advice)
        {
            'query': "How do I deal with a difficult boss?",
            'expected': "Workplace dynamics, interpersonal skills, NOT job descriptions"
        },
        {
            'query': "My coworker is always negative and bringing me down",
            'expected': "Interpersonal dynamics, emotional boundaries"
        },
        
        # Personal relationships
        {
            'query': "I'm having trouble connecting with my partner",
            'expected': "Relationship dynamics, interpersonal traits"
        },
        {
            'query': "How can I be a better friend?",
            'expected': "Social traits, interpersonal skills"
        },
        
        # Personal growth and fulfillment
        {
            'query': "I feel bored and unfulfilled with life",
            'expected': "Life alignment, purpose, trait expression"
        },
        {
            'query': "How do I find my passion and purpose?",
            'expected': "Alignment dynamics, self-discovery"
        },
        
        # Creativity and expression
        {
            'query': "I want to express my creative side more",
            'expected': "Creative traits, expression methods"
        },
        {
            'query': "How can I be more imaginative?",
            'expected': "Creative traits, imagination"
        },
        
        # Emotional and mental well-being
        {
            'query': "I'm feeling overwhelmed and stressed",
            'expected': "Stress management, trait balance"
        },
        {
            'query': "How do I manage my anxiety?",
            'expected': "Emotional regulation, trait management"
        },
        
        # Life balance
        {
            'query': "How do I balance work and personal life?",
            'expected': "Life balance, menu of life concept"
        },
        {
            'query': "I need more fun and play in my life",
            'expected': "Life balance, trait expression"
        },
        
        # Family dynamics
        {
            'query': "How can I improve my relationship with my parents?",
            'expected': "Family dynamics, interpersonal traits"
        },
        
        # Social connections
        {
            'query': "I feel lonely and disconnected",
            'expected': "Social traits, connection strategies"
        },
        
        # Pure career query for comparison
        {
            'query': "What careers match my skills?",
            'expected': "Career descriptions and matches"
        }
    ]
    
    results = []
    career_dominated = 0
    balanced_results = 0
    
    for test_case in test_cases:
        result = test_query(test_case['query'], test_case['expected'])
        if result:
            results.append(result)
            
            # Check if career content dominates
            career_count = result['topic_counts'].get('career', 0)
            total_count = sum(result['topic_counts'].values())
            
            if career_count > total_count * 0.6:  # More than 60% career
                career_dominated += 1
                print("\n⚠️  WARNING: Career content dominates this query!")
            else:
                balanced_results += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print("="*60)
    print(f"Total queries tested: {len(test_cases)}")
    print(f"Balanced results: {balanced_results}")
    print(f"Career-dominated results: {career_dominated}")
    print(f"Success rate: {balanced_results/len(test_cases)*100:.1f}%")
    
    # Specific insights
    print("\nKey Insights:")
    print("1. Life context queries should return glossary and alignment content")
    print("2. Career descriptions should be filtered for non-career queries")
    print("3. The filtering helps focus on trait expression and life alignment")
    
    return results


def test_filter_effectiveness():
    """Test how well the filter identifies life queries"""
    print("\n" + "="*60)
    print("Testing Filter Effectiveness")
    print("="*60)
    
    rag_filter = RAGQueryFilter()
    
    test_queries = [
        "dealing with difficult boss",
        "relationship problems",
        "feeling unfulfilled",
        "express creativity",
        "find a new job",  # Should still be career
        "manage stress at work",
        "connect with friends"
    ]
    
    for query in test_queries:
        params = filter_rag_query(query)
        is_life = params.get('is_life_query', False)
        tags = params.get('tags', [])
        
        print(f"\nQuery: '{query}'")
        print(f"  Is life query: {is_life}")
        print(f"  Tags: {tags}")
        print(f"  Will filter careers: {'careers' not in tags or is_life}")


if __name__ == "__main__":
    # Run the test suite
    test_filter_effectiveness()
    results = run_test_suite()
    
    print("\n" + "="*60)
    print("Test Complete!")
    print("="*60)