import streamlit as st
import pandas as pd
from src.preprocess import load_and_clean
from src.knowledge_graph import visualize_graph
import streamlit.components.v1 as components

# --- Local build_graph function ---
def build_graph(df):
    import networkx as nx
    G = nx.Graph()
    for _, row in df.iterrows():
        pub_node = row['title']
        G.add_node(pub_node, type='publication')
        if 'keywords' in row and row['keywords']:
            for kw in row['keywords'].split(','):
                kw_node = kw.strip()
                G.add_node(kw_node, type='keyword')
                G.add_edge(pub_node, kw_node)
    return G

st.set_page_config(page_title="NASA Bio Explorer Knowledge Graph", page_icon="📊", layout="wide")

# --- Banner / Header ---
st.image("assets/nasa_logo.png", width=150)
st.title("📊 NASA Bio Explorer Knowledge Graph")
st.markdown("Explore relationships between NASA space biology publications with an interactive knowledge graph.")

# --- Load Data ---
@st.cache_data
def load_data():
    return load_and_clean("data/publications_with_abstracts.csv")

df = load_data()

# --- Sidebar ---
with st.sidebar:
    st.title("Knowledge Graph Settings")
    query = st.text_input("Enter keyword to filter publications")
    max_results = st.slider("Max publications to include", 1, 50, 20)

# --- Filter publications ---
if query:
    filtered_df = df[
        df['title'].str.contains(query, case=False, na=False) |
        df['abstract'].str.contains(query, case=False, na=False)
    ]
else:
    filtered_df = df.copy()

filtered_df = filtered_df.head(max_results)

# --- Display filtered publications ---
st.subheader(f"Filtered Publications ({len(filtered_df)})")
for idx, row in filtered_df.iterrows():
    with st.expander(f"[{row['title']}]({row['link']})", expanded=False):
        st.markdown(f"**Abstract:** {row['abstract'][:500]}{'...' if len(row['abstract']) > 500 else ''}")

st.markdown("---")

# --- Knowledge Graph ---
if st.button("Generate Knowledge Graph"):
    with st.spinner("Building knowledge graph..."):
        G = build_graph(filtered_df)
        # Use updated visualize_graph that writes HTML safely
        visualize_graph(G, "assets/graph.html")
    st.success("Knowledge graph generated!")

    # Embed HTML directly in Streamlit
    try:
        with open("assets/graph.html", "r", encoding="utf-8") as f:
            html_data = f.read()
        components.html(html_data, height=750, scrolling=True)
    except FileNotFoundError:
        st.error("Graph HTML file not found. Please check the assets folder.")