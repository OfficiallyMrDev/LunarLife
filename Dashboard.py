# app.py
import streamlit as st
import pandas as pd
from src.preprocess import load_and_clean
from src.search import search_publications
from src.knowledge_graph import build_graph, visualize_graph
from src.summarizer import summarize

st.set_page_config(page_title="LunarLife", page_icon="🚀", layout="wide")

# --- Banner with logo/header image ---
st.image("assets/logorm.png", width=150)
st.title("Project LunarLife ")
st.markdown("Explore NASA space biology publications with AI-powered summaries and interactive visualizations.")

# --- Load Data ---
@st.cache_data
def load_data():
    return load_and_clean("data/publications_with_abstracts.csv")

df = load_data()

# --- Sidebar: Search & Settings ---
with st.sidebar:
    with st.expander("Search Publications", expanded=True):
        query = st.text_input("Enter keyword to search publications")
    with st.expander("Summarization Settings", expanded=True):
        ai_choice = st.selectbox("Summarization AI", ["OpenAI", "Ollama"])
        max_results = st.slider("Max results to display", 1, 20, 5)
        include_results_conclusion = st.checkbox("Include Results and Conclusion in summary", value=True)

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
    badge = "" if include_results_conclusion else ""
    expander_label = f"[{row['title']}]({row['link']}) {badge}"
    with st.expander(expander_label, expanded=False):
        combined_text = row['abstract']
        if include_results_conclusion:
            combined_text += f" {row.get('results', '')} {row.get('conclusion', '')}"
        combined_text = combined_text.strip()[:2000]  # Truncate to max 2000 characters
        
        # Generate and display AI summary of the full abstract + optional results + conclusion
        with st.spinner("Generating summary..."):
            prompt_text = f"Please summarize the following publication in three sections: Introduction, Results, Conclusion.\nTitle: {row['title']}\nContent: {combined_text}"
            summary = summarize(row['title'], prompt_text, ai_choice.lower())
        st.markdown("**Summary:**")
        st.code(summary)
        
        # Follow-up Q&A box
        question = st.text_area(f"Ask a question about this publication:", key=f"q_{idx}")
        if question:
            with st.spinner("Generating answer..."):
                combined_question_text = f"{question} {combined_text}".strip()[:2000]  # Truncate to max 2000 characters
                answer = summarize(question, combined_text, ai_choice.lower())
            st.markdown("**Answer:**")
            st.code(answer)
    st.markdown("---")
