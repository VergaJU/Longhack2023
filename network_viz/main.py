import json
import pandas as pd
import networkx
import networkx as nx
import plotly.graph_objs as go
import argparse
from colour import Color
import dash
from dash import dcc, dash_table
from dash import html
from textwrap import dedent as d
from html.parser import HTMLParser

parser = argparse.ArgumentParser(description="Network representation with Plotly and Dash")
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument("-i", "--input_network",
                           help="json containing the network in cytoscape format")
requiredNamed.add_argument("-d", "--dataframe",
                           help="annotated dataframe from network analysis")

# GeneName, logFC
args = parser.parse_args()

network_json = args.input_network
scored_genes = args.dataframe


## Add arguments with file paths
# import the css template, and pass the css template into dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "AGen-iNET"
server = app.server

percentile=[0, 100]

# Load results with scores and annotation

df = pd.read_csv(scored_genes)
df1 = df[["GeneName", "score"]].sort_values("score", ascending=False)
df1["score"] = round(df["score"],3)


# Load json file with network (cytoscape format)
with open(network_json) as file:
    network = json.load(file)

# Create networkx object
G1 = nx.cytoscape_graph(network)

def network_graph(percRange):
    # filter by range
    selected_nodes = [n for n,v in G1.nodes(data=True) if v["percentile"] <= percRange[1] and v['percentile'] > percRange[0]]
    G = G1.subgraph(selected_nodes)

    # Extract coordinates of nodes and add as annotation to the nodes
    pos = nx.layout.kamada_kawai_layout(G)


    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])

    # prepare plotpy scatterplot including coordintes and textual annotation
    traceRecode = []
    node_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], marker_symbol=[],
                            opacity=1,
                            mode='markers', textposition="bottom center",
                            hoverinfo="text", marker={'size': [],
                                                      'color': [],
                                                      'line': dict(color=[], width=[]),
                                                      'opacity': 1})


    # Add annotation to the scatterplot nodes
    index=0
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        age = G.nodes[node]["is_age"]
        if age == "Age related":
            symbol = "diamond"
        else:
            symbol = "circle"
        disease = G.nodes[node]["is_disease"]
        if disease == "Disease related":
            color = "red"
        else:
            color = "blue"
        variant = G.nodes[node]["is_variant"]
        if variant == "Variant related to Age AND Disease":
            border = "black"
        elif variant == "Variant NOT related to Age AND Disease":
            border = "yellow"
        else :
            border = "green"
        drug = G.nodes[node]["drugs"]
        logFC = G.nodes[node]["logFC"]
        score = G.nodes[node]["score"]
        hovertext = node + ":\nScore: " + str(round(score,3)) + "\nExpression: " + str(round(logFC,3)) + "\n"\
                    + age + "\n" + disease
        node_trace["marker"]["size"] += tuple([score*50])
        node_trace["marker"]["color"] += tuple([color])
        node_trace["marker"]["line"]["color"] += tuple([border])
        node_trace["marker"]["line"]["width"] += tuple([score*5])
        node_trace["text"] += tuple(["\n".join(drug)])
        node_trace["marker_symbol"] += tuple([symbol])
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
        "layout": go.Layout(title='Modern problems require modern solutions',
                            showlegend=False, hovermode='closest',
                            margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                            xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            height=600,
                            clickmode='event+select'
                            )}
    return figure


# styles: for right side hover/click component
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    #########################Title
    html.Div([html.H1(html.Img(id='logo', src=app.get_asset_url("logo_horizontal.png"), height="100"))],
             className="row",
             style={'textAlign': "center"}),
    #############################################################################################define the row
    html.Div(
        className="row",
        children=[
            html.Div(
                className="two columns",
                children=[
                    ##############################################left side two input components
                    dcc.Markdown(d("""
                            **Percentile scores**
                            
                            Slide the bar to define which nodes visualize.
                            """)),
                    html.Div(
                        className="twelve columns",
                        children=[
                            dcc.RangeSlider(
                                id='my-range-slider',
                                min=0,
                                max=100,
                                step=10,
                                value=[0, 100],
                                marks={
                                    10: {'label': '10'},
                                    20: {'label': '20'},
                                    30: {'label': '30'},
                                    40: {'label': '40'},
                                    50: {'label': '50'},
                                    60: {'label': '60'},
                                    70: {'label': '70'},
                                    80: {'label': '80'},
                                    90: {'label': '90'},
                                    100: {'label': '100'}
                                }
                            ),
                            html.Br(),
                            html.Div(id='output-container-range-slider')
                        ],
                        style={'height': '80'}
                    ),
                    html.Div(
                        className="twelve columns",
                        children=[
                            dcc.Markdown(d("""
                            **Biomarkers**
                            """)),
                            dash_table.DataTable(df1.to_dict("records"),
                                                 [{"name": i, "id": i} for i in df1.columns])]
                    )
                ]
            ),
            ############################################middle graph component
            html.Div(
                className="eight columns",
                children=[dcc.Graph(id="my-graph",
                                    figure=network_graph(percentile))],
            ),
            #########################################right side two output component
            html.Div(
                className="two columns",
                children=[
                    html.Div(
                        className='twelve columns',
                        children=[
                            dcc.Markdown(d("""
                            **Gene Info**
                            """)),
                            html.Pre(id='hover-data', style=styles['pre'])
                        ],
                            style={'height': '150px'}),
                    html.Div(
                        className='twelve columns',
                        children=[
                            dcc.Markdown(d("""
                            **Drugs Info**
                            """)),
                            html.Pre(id='click-data', style=styles['pre'])
                        ],
                        style={'height': '150px'}),
                    html.Div(
                        className='twelve columns',
                        children=[
                            dcc.Markdown(d("""
                            **Legend**
                            """)),
                            html.Img(id='legend', src=app.get_asset_url("Legend.png"), height="200")
                        ],
                        style={'height': '200px'}),
                ]
            )
        ]
    )
])

class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, data):
        self.text += data



###################################callback for left side components
@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    YEAR = value
    return network_graph(value)
################################callback for right side components
@app.callback(
    dash.dependencies.Output('hover-data', 'children'),
    [dash.dependencies.Input('my-graph', 'hoverData')])
def display_hover_data(hoverData):
    f = HTMLFilter()
    f.feed(hoverData['points'][0]['hovertext'])
    return f.text


@app.callback(
    dash.dependencies.Output('click-data', 'children'),
    [dash.dependencies.Input('my-graph', 'clickData')])
def display_click_data(clickData):
    f = HTMLFilter()
    f.feed(clickData['points'][0]['text'])
    return f.text



if __name__ == '__main__':
    app.run_server(debug=True)