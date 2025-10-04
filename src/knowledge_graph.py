import networkx as nx
from pyvis.network import Network
from rake_nltk import Rake

def build_graph(df):
    G = nx.Graph()
    rake = Rake()
    for _, row in df.iterrows():
        pub_node = row['title']
        G.add_node(pub_node, type='publication', color='#97c2fc', size=20)
        abstract = row.get('abstract', '')
        if abstract:
            rake.extract_keywords_from_text(abstract)
            keywords = [kw for kw, score in rake.get_ranked_phrases_with_scores()[:5]]
            for kw in keywords:
                G.add_node(kw, type='keyword', color='#FFA500', size=15)
                G.add_edge(pub_node, kw)
    return G

def visualize_graph(G, output_file="assets/graph.html"):
    net = Network(height="750px", width="100%", notebook=False)

    # Apply node attributes from the graph
    for n, attr in G.nodes(data=True):
        attr.setdefault('color', '#97c2fc')
        attr.setdefault('size', 15)

    net.from_nx(G)
    net.show_buttons(filter_=['physics'])
    net.write_html(output_file, open_browser=False)