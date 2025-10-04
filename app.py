# app.py
import streamlit as st
import pandas as pd
from src.preprocess import load_and_clean
from src.search import search_publications
from src.knowledge_graph import build_graph, visualize_graph
from src.summarizer import summarize_with_openai, summarize_with_ollama

st.set_page_config(page_title="NASA Bio Explorer", layout="wide")

st.title("🚀 NASA Bio Explorer Dashboard")
st.markdown("Explore NASA space biology publications with AI-powered summaries and interactive visualizations.")

# --- Load Data ---
@st.cache_data
def load_data():
    return load_and_clean("data/publications_with_abstracts.csv")

df = load_data()

# --- Sidebar: Search ---
st.sidebar.header("Search & Summarize")
query = st.sidebar.text_input("Enter keyword to search publications")
ai_choice = st.sidebar.radio("Summarization AI", ["OpenAI", "Ollama"])
max_results = st.sidebar.slider("Max results to display", 1, 20, 5)

# --- Filter Publications ---
if query:
    # Filter publications by keyword in title or abstract
    filtered_df = df[
        df['title'].str.contains(query, case=False, na=False) |
        df['abstract'].str.contains(query, case=False, na=False)
    ]
else:
    filtered_df = df.copy()

st.subheader(f"Showing {min(len(filtered_df), max_results)} publications")

for idx, row in filtered_df.head(max_results).iterrows():
    st.markdown(f"**[{row['title']}]({row['link']})**")
    
    # Generate and display AI summary of the full abstract
    with st.spinner("Generating summary..."):
        if ai_choice == "OpenAI":
            summary = summarize_with_openai(row['title'], row['abstract'])
        else:
            summary = summarize_with_ollama(row['title'], row['abstract'])
    st.markdown(f"**Summary:** {summary}")
    
    # Follow-up Q&A box
    question = st.text_area(f"Ask a question about this publication:", key=f"q_{idx}")
    if question:
        with st.spinner("Generating answer..."):
            if ai_choice == "OpenAI":
                answer = summarize_with_openai(question, row['abstract'])
            else:
                answer = summarize_with_ollama(question, row['abstract'])
        st.markdown(f"**Answer:** {answer}")

# --- Knowledge Graph ---
st.subheader("📊 Knowledge Graph")
if st.button("Generate Knowledge Graph"):
    G = build_graph(filtered_df)
    visualize_graph(G, "assets/graph.html")
    st.markdown("Interactive graph saved to `assets/graph.html`. Open it in your browser to explore.")