# app.py
import streamlit as st
import pandas as pd
import re
from src.preprocess import load_and_clean
from src.search import search_publications
from src.summarizer import summarize

st.set_page_config(page_title="LunarLife", page_icon="🚀", layout="wide")

# --- Banner with logo/header image ---
st.title("Summarizer")
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
        filter_category = st.selectbox("Select filter category", ["None", "Organism", "Experiment Type", "Mission Relevance"])
        filter_value = None
        if filter_category == "Organism":
            filter_value = st.selectbox("Select organism", ["All", "Mice", "Plants", "Cells", "Other"])
        elif filter_category == "Experiment Type":
            filter_value = st.selectbox("Select experiment type", ["All", "Genomics", "Bone", "Immune", "Radiation", "Other"])
        elif filter_category == "Mission Relevance":
            filter_value = st.selectbox("Select mission relevance", ["All", "ISS", "Bion-M1", "Shuttle", "Other"])
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

# Apply single-category filters (use metadata columns if available, otherwise fallback to pattern search in abstract)
if filter_category != "None" and filter_value and filter_value != "All":
    # Prefer explicit metadata columns if they exist
    col_map = {
        'Organism': 'organism',
        'Experiment Type': 'experiment_type',
        'Mission Relevance': 'mission'
    }
    col = col_map.get(filter_category)
    if col in filtered_df.columns:
        # Use the metadata column for filtering (case-insensitive contains)
        filtered_df = filtered_df[filtered_df[col].astype(str).str.contains(str(filter_value), case=False, na=False)]
    else:
        # Fallback: map high-level choices to likely keywords and search the abstract
        patterns = {
            'Organism': {
                'Mice': ['mouse', 'mice'],
                'Plants': ['plant', 'plants', 'arabidopsis'],
                'Cells': ['cell', 'cells', 'cell line'],
                'Other': []
            },
            'Experiment Type': {
                'Genomics': ['genom'],
                'Bone': ['bone', 'osteop'],
                'Immune': ['immune', 'immuno'],
                'Radiation': ['radiat', 'ioniz'],
                'Other': []
            },
            'Mission Relevance': {
                'ISS': ['ISS', 'international space station', 'space station'],
                'Bion-M1': ['Bion-M1', 'Bion-M 1', 'bion m1'],
                'Shuttle': ['Shuttle', 'space shuttle'],
                'Other': []
            }
        }
        pats = patterns.get(filter_category, {}).get(filter_value, [])
        if pats:
            regex = '|'.join([re.escape(p) for p in pats])
            filtered_df = filtered_df[filtered_df['abstract'].str.contains(regex, case=False, na=False)]
        else:
            # No specific mapping for this value; do not apply extra filtering
            pass

st.subheader(f"Showing {min(len(filtered_df), max_results)} publications")

for idx, row in filtered_df.head(max_results).iterrows():
    badge = ""
    if include_results_conclusion:
        badge = " - Includes Results & Conclusion"
    expander_label = f"[{row['title']}]({row['link']}){badge}"
    with st.expander(expander_label, expanded=False):
        combined_text = row['abstract']
        if include_results_conclusion:
            combined_text += f" {row.get('results', '')} {row.get('conclusion', '')}"
        combined_text = combined_text.strip()[:2000]  # Truncate to max 2000 characters

        if st.button("Generate Summary", key=f"btn_{idx}"):
            with st.spinner("Generating summary..."):
                prompt_text = f"Please summarize the following publication in three sections: Introduction, Results, Conclusion.\nTitle: {row['title']}\nContent: {combined_text}"
                summary = summarize(row['title'], prompt_text, ai_choice.lower())
                st.markdown("**Summary:**")
                st.code(summary)

            question = st.text_area(f"Ask a question about this publication:", key=f"q_{idx}")
            if question:
                with st.spinner("Generating answer..."):
                    combined_question_text = f"{question} {combined_text}".strip()[:2000]
                    answer = summarize(question, combined_text, ai_choice.lower())
                st.markdown("**Answer:**")
                st.code(answer)
    st.markdown("---")
