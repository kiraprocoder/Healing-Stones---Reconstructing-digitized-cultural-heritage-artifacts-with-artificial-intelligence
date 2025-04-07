import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the match graph JSON
with open("match_graph.json", "r") as f:
    data = json.load(f)

G = nx.Graph()

# Add nodes and edges from the list
for source, target, weight in data:
    G.add_node(source)
    G.add_node(target)
    G.add_edge(source, target, weight=weight)

# Define layout
pos = nx.spring_layout(G, k=0.5, iterations=100, seed=42)

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=800, node_color="#87CEEB", edgecolors='black', linewidths=0.8)

# Draw edges with thicker lines
nx.draw_networkx_edges(G, pos, width=2.0, edge_color="#888")

# Draw labels with larger font
nx.draw_networkx_labels(G, pos, font_size=10, font_color="#333")

# Optionally draw edge weights
# edge_labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

# Final layout adjustments
plt.axis('off')
plt.title("Mayan Stele Fragment Graph", fontsize=14)
plt.tight_layout()
plt.show()
