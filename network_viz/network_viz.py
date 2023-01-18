import json
import networkx
import networkx as nx
import plotly.graph_objs as go
import argparse

#network = json.load("Data/network_jnode.json")
with open("Data/network_jnode.json") as file:
    network = json.load(file)

G = nx.cytoscape_graph(network)
pos = nx.layout.shell_layout(G)

for node in G.nodes:
    G.nodes[node]['pos'] = list(pos[node])

trace_Recode = []
node_trace = go.Scatter(x=[], y=[], hovertext=[],
                        mode='markers+text', textposition="bottom center",
                        hoverinfo="text", marker={'size': 50, 'color': 'LightSkyBlue'})
index=0
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    age = G.nodes[node]["is_age"]
    disease = G.nodes[node]["is_disease"]
    logFC = G.nodes[node]["log2FoldChange"]
    score = G.nodes[node]["score"]
    hovertext = node + " with score : " + str(round(score,3)) + " and Expression: " + str(round(logFC,3)) + "<br>"\
                + "Result: " + age + " and " + disease
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['hovertext'] += tuple([hovertext])
    index = index + 1


#TODO: continue with graph preparation (look https://towardsdatascience.com/python-interactive-network-visualization-using-networkx-plotly-and-dash-e44749161ed7)
