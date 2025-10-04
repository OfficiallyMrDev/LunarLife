import networkx as nx
import matplotlib.pyplot as plt

def build_knowledge_graph(df):
    G = nx.Graph()
    for _, row in df.head(50).iterrows():  # limit to first 50 for demo
        title = row['title']
        keywords = str(row.get('keywords', '')).split(',')
        for kw in keywords:
            G.add_node(title, type="paper")
            G.add_node(kw.strip(), type="keyword")
            G.add_edge(title, kw.strip())

    fig, ax = plt.subplots(figsize=(10,6))
    nx.draw(G, with_labels=True, node_size=500, font_size=8, ax=ax)
    return fig