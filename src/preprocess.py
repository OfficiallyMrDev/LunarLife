# src/preprocess.py
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'<.*?>', '', text)  # remove HTML tags
    return text.strip()

def load_and_clean(csv_path="data/publications_with_abstracts.csv"):
    """
    Load CSV of publications, clean text, and ensure columns are standardized.
    """
    df = pd.read_csv(csv_path)
    df.rename(columns={'Title':'title', 'Abstract':'abstract', 'Link':'link'}, inplace=True)
    
    df['title'] = df['title'].apply(clean_text)
    df['abstract'] = df['abstract'].apply(lambda x: clean_text(x) or "Abstract not available.")
    
    df.drop_duplicates(subset=['title'], inplace=True)
    df.fillna({"abstract":"Abstract not available."}, inplace=True)
    
    # Add columns for results and conclusion
    df['results'] = ""
    df['conclusion'] = ""
    
    return df

def extract_results_conclusion(url):
    """
    Fetch the publication HTML and extract Results and Conclusion sections.
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        results = ""
        conclusion = ""
        
        for heading in soup.find_all(['h2','h3']):
            section_title = heading.get_text().strip().lower()
            content = ""
            for sibling in heading.find_next_siblings():
                if sibling.name in ['h2','h3']:
                    break
                content += sibling.get_text(separator=" ", strip=True) + " "
            if "result" in section_title:
                results += content
            if "conclusion" in section_title or "discussion" in section_title:
                conclusion += content
        
        return results.strip(), conclusion.strip()
    
    except Exception as e:
        return "", ""