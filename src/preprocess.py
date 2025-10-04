# src/preprocess.py
import pandas as pd
import re

def clean_text(text):
    """Clean text by removing HTML tags and trimming whitespace."""
    if pd.isna(text):
        return ""
    text = re.sub(r'<.*?>', '', text)  # remove HTML tags
    return text.strip()

def load_and_clean(csv_path="data/publications_with_abstracts.csv"):
    """
    Load CSV of publications, clean text, and ensure columns are standardized.
    Returns a DataFrame ready for search and AI summarization.
    """
    df = pd.read_csv(csv_path)
    
    # Standardize column names
    df.rename(columns={
        'Title': 'title', 
        'Abstract': 'abstract', 
        'Link': 'link'
    }, inplace=True)
    
    # Clean text fields
    df['title'] = df['title'].apply(clean_text)
    df['abstract'] = df['abstract'].apply(lambda x: clean_text(x) or "Abstract not available.")
    
    # Drop duplicates
    df.drop_duplicates(subset=['title'], inplace=True)
    
    return df