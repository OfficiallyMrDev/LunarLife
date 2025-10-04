# src/search.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import re

def preprocess_text(text: str) -> str:
    """Preprocess text for improved search."""
    if pd.isna(text):
        return ""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def get_relevant_keywords(text: str) -> List[str]:
    """Extract relevant keywords from text."""
    # Common scientific/space biology terms to boost
    domain_keywords = {
        'microgravity', 'radiation', 'spaceflight', 'zero gravity', 
        'astronaut', 'cosmic', 'space', 'lunar', 'mars', 'mission',
        'experiment', 'study', 'research', 'analysis', 'data',
        'biology', 'medical', 'health', 'physiology', 'genetics'
    }
    
    words = set(text.lower().split())
    return list(words.intersection(domain_keywords))

def calculate_relevance_score(row: pd.Series, query: str, vectorizer: TfidfVectorizer) -> float:
    """Calculate relevance score based on text similarity and other factors."""
    # Combine text fields with different weights
    text = (
        (row['title'] + " ") * 2 +  # Title has double weight
        (row['abstract'] + " ")     # Abstract has normal weight
    )
    
    # Calculate TF-IDF similarity
    query_vec = vectorizer.transform([query])
    text_vec = vectorizer.transform([text])
    similarity = cosine_similarity(query_vec, text_vec)[0][0]
    
    # Boost score based on metadata matches
    boost = 1.0
    if query.lower() in str(row['organism']).lower():
        boost += 0.3
    if query.lower() in str(row['experiment_type']).lower():
        boost += 0.3
    if query.lower() in str(row['mission']).lower():
        boost += 0.4
        
    return similarity * boost

def search_publications(df: pd.DataFrame, query: str, 
                       filters: Dict[str, str] = None) -> pd.DataFrame:
    """
    Enhanced search function with relevance scoring and filtering.
    
    Args:
        df: DataFrame containing publications
        query: Search query string
        filters: Dictionary of filters (e.g., {'organism': 'mice', 'experiment_type': 'radiation'})
    
    Returns:
        DataFrame of matched publications, sorted by relevance
    """
    if not query.strip():
        return df
    
    # Preprocess the query
    processed_query = preprocess_text(query)
    
    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=10000
    )
    
    # Fit vectorizer on corpus
    corpus = df['title'].fillna('') + ' ' + df['abstract'].fillna('')
    vectorizer.fit(corpus)
    
    # Calculate relevance scores
    df['relevance_score'] = df.apply(
        lambda row: calculate_relevance_score(row, processed_query, vectorizer),
        axis=1
    )
    
    # Apply filters if provided
    if filters:
        for key, value in filters.items():
            if value and value.lower() != 'all':
                df = df[df[key].str.lower() == value.lower()]
    
    # Filter results with non-zero relevance and sort
    results = df[df['relevance_score'] > 0].sort_values(
        'relevance_score', ascending=False
    ).copy()
    
    # Add match highlights
    def highlight_matches(text, query_terms):
        highlighted = text
        for term in query_terms:
            pattern = re.compile(f'({term})', re.IGNORECASE)
            highlighted = pattern.sub(r'**\1**', highlighted)
        return highlighted
    
    query_terms = processed_query.split()
    results['highlighted_title'] = results['title'].apply(
        lambda x: highlight_matches(x, query_terms)
    )
    results['highlighted_abstract'] = results['abstract'].apply(
        lambda x: highlight_matches(x, query_terms)
    )
    
    return results[['title', 'abstract', 'link', 'organism', 
                   'experiment_type', 'mission', 'relevance_score',
                   'highlighted_title', 'highlighted_abstract']]