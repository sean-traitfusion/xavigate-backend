"""
RAG Query Filtering Module

This module provides intelligent filtering for RAG queries to prevent specialized
content (like reintegration documentation) from dominating general search results.
"""

from typing import List, Dict, Set, Optional
import re


class RAGQueryFilter:
    """Intelligent query filtering for RAG searches"""
    
    def __init__(self):
        # Keywords that indicate reintegration/prison content is relevant
        self.reintegration_keywords = {
            'prison', 'incarceration', 'incarcerated', 'jail', 'felon', 'felony',
            'criminal', 'conviction', 'parole', 'probation', 'reentry', 're-entry',
            'reintegration', 'released', 'inmate', 'correctional', 'justice system',
            'record', 'background check', 'expungement', 'halfway house'
        }
        
        # Keywords for specific content types
        self.content_keywords = {
            'careers': {
                'career', 'job', 'work', 'employment', 'profession', 'occupation',
                'salary', 'hire', 'hiring', 'interview', 'resume', 'cv', 'skills'
            },
            'glossary': {
                'what is', 'define', 'definition', 'meaning', 'glossary', 'term',
                'concept', 'explain'
            },
            'alignment_dynamics': {
                'alignment', 'dynamics', 'mapper', 'realigner', 'unblocking',
                'trait', 'expression', 'pattern'
            },
            'menu_of_life': {
                'menu of life', 'appetizer', 'main course', 'dessert', 'life menu'
            },
            'task_trait_alignment': {
                'task trait', 'trait alignment', 'task alignment'
            },
            'problem': {
                'burnout', 'stress', 'overwhelm', 'problem', 'issue', 'challenge',
                'struggle', 'difficulty'
            }
        }
        
        # Keywords that indicate NON-career life questions
        self.life_context_keywords = {
            'relationship': {'relationship', 'partner', 'spouse', 'marriage', 'dating', 'love'},
            'workplace_dynamics': {'boss', 'manager', 'coworker', 'colleague', 'team', 'conflict'},
            'personal_growth': {'bored', 'unfulfilled', 'purpose', 'meaning', 'passion', 'fulfillment'},
            'creativity': {'creative', 'artistic', 'express', 'imagination', 'create'},
            'emotional': {'feeling', 'emotion', 'mood', 'anxiety', 'depression', 'happy', 'sad'},
            'social': {'friend', 'social', 'lonely', 'connection', 'community'},
            'family': {'family', 'parent', 'child', 'sibling', 'relative'}
        }
        
        # Default tags to exclude unless specifically relevant
        self.default_exclude_tags = {'mn_reintegration', 'reintegration'}
        
    def needs_reintegration_content(self, query: str) -> bool:
        """Check if query indicates user needs reintegration content"""
        query_lower = query.lower()
        
        # Check for explicit reintegration keywords
        for keyword in self.reintegration_keywords:
            if keyword in query_lower:
                return True
        
        # Check for phrases that might indicate this context
        reintegration_phrases = [
            'getting out', 'second chance', 'fresh start after',
            'rebuilding', 'starting over'
        ]
        
        for phrase in reintegration_phrases:
            if phrase in query_lower:
                # Additional context check
                if any(word in query_lower for word in ['prison', 'jail', 'release']):
                    return True
        
        return False
    
    def detect_content_focus(self, query: str) -> Set[str]:
        """Detect which content types are most relevant to the query"""
        query_lower = query.lower()
        detected_tags = set()
        
        # First check if this is a life/relationship query (non-career)
        is_life_query = False
        life_contexts = []
        
        for context, keywords in self.life_context_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    is_life_query = True
                    life_contexts.append(context)
                    break
        
        # Check each content type
        for content_type, keywords in self.content_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    detected_tags.add(content_type)
                    break
        
        # Special handling for life queries
        if is_life_query:
            # For workplace dynamics, we want glossary/alignment, NOT career descriptions
            if 'workplace_dynamics' in life_contexts and 'careers' in detected_tags:
                detected_tags.remove('careers')
                detected_tags.update(['glossary', 'alignment_dynamics', 'problem'])
            
            # For personal growth/creativity, prioritize alignment and glossary
            if any(ctx in life_contexts for ctx in ['personal_growth', 'creativity', 'emotional']):
                detected_tags.update(['glossary', 'alignment_dynamics', 'menu_of_life'])
                # Remove careers unless explicitly job-related
                if 'careers' in detected_tags and not any(
                    kw in query_lower for kw in ['job', 'career', 'profession']
                ):
                    detected_tags.remove('careers')
        
        # If no specific content detected, use appropriate defaults
        if not detected_tags:
            if is_life_query:
                # For life queries, default to glossary and alignment content
                detected_tags = {'glossary', 'alignment_dynamics', 'menu_of_life'}
            else:
                # For general queries, include careers
                detected_tags = {'careers', 'glossary', 'alignment_dynamics'}
        
        return detected_tags
    
    def get_filter_params(self, query: str, user_context: Optional[Dict] = None) -> Dict:
        """
        Generate filter parameters for RAG query
        
        Args:
            query: The user's search query
            user_context: Optional context about the user (could include flags like 'needs_reintegration')
            
        Returns:
            Dict with 'tags' to include and 'exclude_tags' to filter out
        """
        # Check if reintegration content is needed
        include_reintegration = self.needs_reintegration_content(query)
        
        # Override based on user context if provided
        if user_context and user_context.get('needs_reintegration'):
            include_reintegration = True
        
        # Detect content focus
        focus_tags = self.detect_content_focus(query)
        
        # Build filter parameters
        filter_params = {
            'tags': list(focus_tags),
            'exclude_tags': list(self.default_exclude_tags) if not include_reintegration else []
        }
        
        # Special handling for career queries
        if 'careers' in focus_tags and not include_reintegration:
            # Explicitly exclude reintegration-focused career content
            filter_params['exclude_content_patterns'] = [
                'incarceration', 'prison', 'criminal record', 'felony'
            ]
        
        # Add flag to help with post-filtering
        filter_params['is_life_query'] = any(
            keyword in query.lower() 
            for keyword_set in self.life_context_keywords.values() 
            for keyword in keyword_set
        )
        
        return filter_params
    
    def should_filter_result(self, chunk_text: str, chunk_metadata: Dict, 
                           filter_params: Dict) -> bool:
        """
        Check if a specific chunk should be filtered out
        
        Args:
            chunk_text: The text content of the chunk
            chunk_metadata: Metadata associated with the chunk
            filter_params: Filter parameters from get_filter_params
            
        Returns:
            True if chunk should be filtered out, False otherwise
        """
        # Check excluded tags
        chunk_tags = set(chunk_metadata.get('tags', '').split())
        chunk_tags.add(chunk_metadata.get('tag', ''))
        
        for exclude_tag in filter_params.get('exclude_tags', []):
            if exclude_tag in chunk_tags:
                return True
        
        # Check content patterns to exclude
        exclude_patterns = filter_params.get('exclude_content_patterns', [])
        chunk_lower = chunk_text.lower()
        
        for pattern in exclude_patterns:
            if pattern in chunk_lower:
                return True
        
        # Special filtering for life queries to reduce career spam
        if filter_params.get('is_life_query') and 'career' in chunk_tags:
            # For life queries, filter out pure career descriptions
            # unless they're about workplace dynamics or soft skills
            career_description_patterns = [
                'description:', 'nature scores:', 'gross bodily:', 'fine bodily:',
                'salary:', 'education required:', 'job duties:'
            ]
            
            if any(pattern in chunk_lower for pattern in career_description_patterns):
                # This looks like a career description, not life advice
                return True
        
        return False
    
    def rerank_results(self, results: List[Dict], query: str, 
                      filter_params: Dict) -> List[Dict]:
        """
        Re-rank results to deprioritize specialized content unless relevant
        
        Args:
            results: List of search results
            query: Original query
            filter_params: Filter parameters used
            
        Returns:
            Re-ranked results
        """
        # Separate results into tiers
        primary_results = []
        secondary_results = []
        
        for result in results:
            # Check if this is specialized content
            is_specialized = False
            
            # Check for reintegration content
            if 'reintegration' in result.get('title', '').lower():
                is_specialized = True
            if 'mn_reintegration' in result.get('metadata', {}).get('tags', ''):
                is_specialized = True
                
            # If specialized content isn't needed, deprioritize it
            if is_specialized and filter_params.get('exclude_tags'):
                secondary_results.append(result)
            else:
                primary_results.append(result)
        
        # Return primary results first, then secondary
        return primary_results + secondary_results


# Convenience function for use in chat service
def filter_rag_query(query: str, user_context: Optional[Dict] = None) -> Dict:
    """
    Generate RAG filter parameters for a query
    
    Args:
        query: User's search query
        user_context: Optional user context
        
    Returns:
        Filter parameters dict
    """
    filter = RAGQueryFilter()
    return filter.get_filter_params(query, user_context)