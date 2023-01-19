import json
import networkx
import networkx as nx
import plotly.graph_objs as go
import argparse
from colour import Color
import dash
import dash_core_components as dcc
import dash_html_components as html

#network = json.load("Data/network_jnode.json")
# Load json file with network (cytoscape format)
with open("Data/network_jnode.json") as file:
    network = json.load(file)
# Create networkx object
G = nx.cytoscape_graph(network)

# Extract coordinates of nodes and add as annotation to the nodes
pos = nx.layout.kamada_kawai_layout(G)

for node in G.nodes:
    G.nodes[node]['pos'] = list(pos[node])

# prepare plotpy scatterplot including coordintes and textual annotation

traceRecode = []
node_trace = go.Scatter(x=[], y=[], hovertext=[], text=[],
                        mode='markers+text', textposition="bottom center",
                        hoverinfo="text", marker={'size': 50, 'color': 'LightSkyBlue'})

# Add annotation to the scatterplot nodes
index=0
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    age = G.nodes[node]["is_age"]
    disease = G.nodes[node]["is_disease"]
    logFC = G.nodes[node]["log2FoldChange"]
    score = G.nodes[node]["score"]
    hovertext = node + " with score : " + str(round(score,3)) + " and Expression: " + str(round(logFC,3)) + "<br>"\
                + "Result: " + age + " and " + disease
    text = node
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['hovertext'] += tuple([hovertext])
    index = index + 1


traceRecode.append(node_trace)

## Now define the edges:


index = 0

for edge in G.edges:
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    trace = go.Scatter(x=tuple([x0, x1, None]), y=tuple([y0, y1, None]),
                       mode='lines',
                       marker=dict(color="black"),
                       line_shape='linear',
                       opacity=0.5,
                       line_width=0.5)
    traceRecode.append(trace)
    index = index + 1


# define layout

figure = {
    "data": traceRecode,
    "layout": go.Layout(title='Interaction network', showlegend=False, hovermode='closest',
                        margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                        xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                        yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                        height=600,
                        clickmode='event+select'
                        )}

## Inizialize dash app
app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=figure)
])

## Run server
app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter