import pandas as pd

def search_publications(df, query):
    mask = df['title'].str.contains(query, case=False, na=False) | df['abstract'].str.contains(query, case=False, na=False)
    return df[mask].head(10)  # return top 10 matches