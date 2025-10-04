# src/search.py
def search_publications(df, query):
    """Return filtered publications based on keyword in title or abstract."""
    mask = df['Title'].str.contains(query, case=False, na=False) | df['Abstract'].str.contains(query, case=False, na=False)
    return df[mask]