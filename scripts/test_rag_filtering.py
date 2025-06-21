#!/usr/bin/env python3
"""
Test RAG Filtering - Compare filtered vs unfiltered search results

This script demonstrates how the intelligent filtering prevents specialized
content (like reintegration documentation) from dominating general queries.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'microservices', 'chat_service'))

from rag_filter import RAGQueryFilter, filter_rag_query


def test_keyword_detection():
    """Test the keyword detection logic"""
    print("=" * 60)
    print("Testing Keyword Detection")
    print("=" * 60)
    
    filter = RAGQueryFilter()
    
    test_queries = [
        # General queries (should NOT trigger reintegration)
        "How do I find a job?",
        "What careers match my skills?",
        "I need career guidance",
        "What is alignment dynamics?",
        "Explain the menu of life",
        
        # Reintegration-specific queries (SHOULD trigger)
        "How do I find a job after prison?",
        "Career options for someone with a criminal record",
        "Employment after incarceration",
        "Reintegration programs available",
        "Second chance after jail"
    ]
    
    for query in test_queries:
        needs_reintegration = filter.needs_reintegration_content(query)
        detected_tags = filter.detect_content_focus(query)
        filter_params = filter.get_filter_params(query)
        
        print(f"\nQuery: '{query}'")
        print(f"  Needs reintegration content: {needs_reintegration}")
        print(f"  Detected focus tags: {detected_tags}")
        print(f"  Filter params: {filter_params}")


def test_content_filtering():
    """Test the content filtering logic"""
    print("\n" + "=" * 60)
    print("Testing Content Filtering")
    print("=" * 60)
    
    filter = RAGQueryFilter()
    
    # Sample chunks that might be returned
    sample_chunks = [
        {
            'title': 'Careers',
            'topic': 'careers',
            'chunk': 'Software developers design and create computer applications...'
        },
        {
            'title': 'Glossary',
            'topic': 'glossary',
            'chunk': 'Alignment Dynamics is a framework for understanding trait expression...'
        },
        {
            'title': 'MN Reintegration',
            'topic': 'mn_reintegration',
            'chunk': 'Finding employment after incarceration can be challenging...'
        },
        {
            'title': 'Menu of Life',
            'topic': 'menu_of_life',
            'chunk': 'The Menu of Life helps you organize different aspects of your life...'
        }
    ]
    
    # Test with general career query
    query = "I need help with my career"
    filter_params = filter.get_filter_params(query)
    
    print(f"\nQuery: '{query}'")
    print(f"Filter params: {filter_params}")
    print("\nFiltering results:")
    
    for chunk in sample_chunks:
        metadata = {
            'tags': chunk['topic'],
            'tag': chunk['topic'],
            'title': chunk['title']
        }
        
        should_filter = filter.should_filter_result(
            chunk['chunk'],
            metadata,
            filter_params
        )
        
        print(f"  {chunk['title']}: {'FILTERED OUT' if should_filter else 'KEPT'}")


def test_real_queries():
    """Test with real-world query examples"""
    print("\n" + "=" * 60)
    print("Testing Real-World Queries")
    print("=" * 60)
    
    real_queries = [
        {
            'query': "I'm feeling burned out at work",
            'expected': 'Should find burnout/problem content, NOT reintegration'
        },
        {
            'query': "What jobs are good for creative people?",
            'expected': 'Should find career content, NOT reintegration'
        },
        {
            'query': "How do I align my traits with my work?",
            'expected': 'Should find alignment dynamics content'
        },
        {
            'query': "Finding work after being released from prison",
            'expected': 'SHOULD find reintegration content'
        },
        {
            'query': "What is a providing trait?",
            'expected': 'Should find glossary content'
        }
    ]
    
    for test in real_queries:
        params = filter_rag_query(test['query'])
        print(f"\nQuery: '{test['query']}'")
        print(f"Expected: {test['expected']}")
        print(f"Filter result: {params}")
        
        # Check if expectations are met
        if 'prison' in test['query'].lower() or 'released' in test['query'].lower():
            if params['exclude_tags']:
                print("  ❌ ERROR: Reintegration content would be filtered!")
        else:
            if not params['exclude_tags']:
                print("  ⚠️  WARNING: Reintegration content NOT filtered")


def main():
    """Run all tests"""
    print("\nRAG Filtering Test Suite")
    print("This demonstrates how specialized content is filtered\n")
    
    test_keyword_detection()
    test_content_filtering()
    test_real_queries()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print("""
The filtering system:
1. Detects when reintegration content IS needed (prison, incarceration keywords)
2. Filters OUT reintegration content for general queries
3. Identifies content focus (careers, glossary, etc.) from query
4. Can be extended with user context flags

This prevents the 32 reintegration document chunks from overwhelming
the 355 general content chunks when users ask general questions.
""")


if __name__ == "__main__":
    main()