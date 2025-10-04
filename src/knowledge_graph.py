# src/knowledge_graph.py
import networkx as nx
from pyvis.network import Network

def build_graph(df, top_keywords=5):
    """
    Build a knowledge graph from publications.
    Nodes: publications and top keywords from titles
    Edges: publication -> keywords
    """
    G = nx.Graph()
    
    for _, row in df.iterrows():
        pub_node = row['title']
        G.add_node(pub_node, label=row['title'], url=row['link'], color='lightblue')
        
        # Extract keywords from title (simple split for demo; can use NLP for real keywords)
        keywords = row['title'].split()[:top_keywords]
        for kw in keywords:
            G.add_node(kw, label=kw, color='orange')
            G.add_edge(pub_node, kw)
    
    return G

def visualize_graph(G, output_file="assets/graph.html"):
    """
    Generate an interactive HTML graph visualization using pyvis.
    """
    net = Network(height="750px", width="100%", notebook=False)
    net.from_nx(G)
    net.show(output_file)