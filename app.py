import streamlit as st
import pandas as pd
from src.summarizer import summarize_publication
from src.search import search_publications
from src.knowledge_graph import build_knowledge_graph

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/publications.csv")

df = load_data()

# Sidebar navigation
st.sidebar.title("🚀 NASA Bio Explorer")
section = st.sidebar.radio("Navigate", ["Home", "Search & Explore", "Knowledge Graph"])

# --- Home Page ---
if section == "Home":
    st.title("🌌 NASA Bio Explorer Dashboard")
    st.write("""
    Welcome to NASA Bio Explorer!  
    This interactive tool summarizes 600+ NASA space biology publications, 
    helping scientists, mission planners, and enthusiasts explore the impact of 
    decades of space bioscience research.
    """)

# --- Search & Explore ---
elif section == "Search & Explore":
    st.header("🔍 Explore Publications")
    query = st.text_input("Enter keywords (e.g., radiation, plants, immune system)")
    if query:
        results = search_publications(df, query)
        for _, row in results.iterrows():
            st.subheader(row['title'])
            st.write(f"**Authors:** {row['authors']}")
            st.write(f"**Year:** {row['year']}")
            st.write(summarize_publication(row['abstract']))

# --- Knowledge Graph ---
elif section == "Knowledge Graph":
    st.header("🧠 Knowledge Graph of NASA Bioscience")
    fig = build_knowledge_graph(df)
    st.pyplot(fig)