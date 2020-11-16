import networkx as nx
from networkx.readwrite import json_graph
import pandas as pd
from flask_caching import Cache
import plotly.graph_objects as go
import json
import glob
import os

#set root directory for data files
#ROOTBEER = '/home/ubuntu/housing_equity/sandbox-singlepage/' #production
ROOTBEER = '' #local

with open(ROOTBEER + 'data/washingtongeo.json','r') as GeoJSON:
    tracts = json.load(GeoJSON)

#set directory for graph jsons
json_dir = ROOTBEER + 'data/json/*'
graphs_dict = {} #set a dictionary to hold graphs
for file in glob.iglob(json_dir):
    with open (file) as json_file:
        graph_name = os.path.basename(file)
        graph_name = graph_name.rstrip('.json')
        graph = json.load(json_file)
        graphs_dict[graph_name] = json_graph.node_link_graph(graph) #sets a value that consists of the networkx graph

#loop over graph_dict to write all the variables for the graph
#for graph_name, graph in graphs_dict.items():
#    exec(graph_name + '=graph')

node_trace2018 = {}
edge_trace2018 = {}

df_combo = pd.read_csv(ROOTBEER + 'data/df_combo.csv', dtype={"GEOID": str,"TRACT_NUM": str,"YEAR":str})

#from build_network import get_nodes, get_edges

for graph in graphs_dict:
    key = str(graph).lstrip('G2018_')
    node_trace2018[key] = go.Scatter(
    x=[],
    y=[],
    mode='markers+text',  #make markers+text to show labels
    text=[],
    hoverinfo='text',
    customdata=df_combo['GEOID'],
    marker=dict(
        showscale=False,
        colorscale='YlGnBu',
        reversescale=False,
        color=[],
        size=20,
        opacity=0.8,
        colorbar=dict(
            thickness=10,
            title='COLOR GROUP BY CENSUS TRACT NUMBER',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)
    ),
    showlegend=True,
    marker_line_width=1
    )
    edge_trace2018[key] = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
    )

colorsIndex = {'wallingford':'#ef553b','rainier_beach':'#636efa'}  #manually assign colors
colors = df_combo['neighborhood'].map(colorsIndex)

for graph in graphs_dict:
    key = str(graph).lstrip('G2018_')
    for edge in graphs_dict[graph].edges():
        x0, y0 = graphs_dict[graph].nodes[edge[0]]['pos']
        x1, y1 = graphs_dict[graph].nodes[edge[1]]['pos']
        edge_trace2018[key]['x'] += tuple([x0, x1, None])
        edge_trace2018[key]['y'] += tuple([y0, y1, None])
    for node in graphs_dict[graph].nodes():
        x, y = graphs_dict[graph].nodes[node]['pos']
        node_trace2018[key]['x'] += tuple([x])
        node_trace2018[key]['y'] += tuple([y])
        node_trace2018[key].text = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  # tract version
        node_trace2018[key].marker.color = colors
        node_trace2018[key].marker.size = (1.5 + df_combo.omega18) * 20

'''
#plot this bad boy
#edge_trace = go.Scatter(
#    x=[],
#    y=[],
#    line=dict(width=1,color='#c6c6c6'),
#    hoverinfo='text',
#    mode='lines'
#)


edge_trace2018_a1b1c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
)

edge_trace2018_a1b5c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
)

edge_trace2018_a1b0c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
)

edge_trace2018_a5b1c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
)

edge_trace2018_a5b5c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
)

edge_trace2018_a5b0c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
)

edge_trace2018_a0b1c1d1e1f1g1= go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
)

edge_trace2018_a0b5c1d1e1f1g1= go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
)

edge_trace2018_a0b0c1d1e1f1g1= go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
)
'''
#for edge in G.edges():
#    x0, y0 = G.nodes[edge[0]]['pos']
#    x1, y1 = G.nodes[edge[1]]['pos']
#    edge_trace['x'] += tuple([x0, x1, None])
#    edge_trace['y'] += tuple([y0, y1, None])

'''
for edge in G2018_a1b1c1d1e1f1g1.edges():
    x0, y0 = G2018_a1b1c1d1e1f1g1.nodes[edge[0]]['pos2018_a1b1c1d1e1f1g1']
    x1, y1 = G2018_a1b1c1d1e1f1g1.nodes[edge[1]]['pos2018_a1b1c1d1e1f1g1']
    edge_trace2018_a1b1c1d1e1f1g1['x'] += tuple([x0, x1, None])
    edge_trace2018_a1b1c1d1e1f1g1['y'] += tuple([y0, y1, None])

for edge in G2018_a1b5c1d1e1f1g1.edges():
    x0, y0 = G2018_a1b5c1d1e1f1g1.nodes[edge[0]]['pos2018_a1b5c1d1e1f1g1']
    x1, y1 = G2018_a1b5c1d1e1f1g1.nodes[edge[1]]['pos2018_a1b5c1d1e1f1g1']
    edge_trace2018_a1b5c1d1e1f1g1['x'] += tuple([x0, x1, None])
    edge_trace2018_a1b5c1d1e1f1g1['y'] += tuple([y0, y1, None])

for edge in G2018_a1b0c1d1e1f1g1.edges():
    x0, y0 = G2018_a1b0c1d1e1f1g1.nodes[edge[0]]['pos2018_a1b0c1d1e1f1g1']
    x1, y1 = G2018_a1b0c1d1e1f1g1.nodes[edge[1]]['pos2018_a1b0c1d1e1f1g1']
    edge_trace2018_a1b0c1d1e1f1g1['x'] += tuple([x0, x1, None])
    edge_trace2018_a1b0c1d1e1f1g1['y'] += tuple([y0, y1, None])

for edge in G2018_a5b1c1d1e1f1g1.edges():
    x0, y0 = G2018_a5b1c1d1e1f1g1.nodes[edge[0]]['pos2018_a5b1c1d1e1f1g1']
    x1, y1 = G2018_a5b1c1d1e1f1g1.nodes[edge[1]]['pos2018_a5b1c1d1e1f1g1']
    edge_trace2018_a5b1c1d1e1f1g1['x'] += tuple([x0, x1, None])
    edge_trace2018_a5b1c1d1e1f1g1['y'] += tuple([y0, y1, None])

for edge in G2018_a5b5c1d1e1f1g1.edges():
    x0, y0 = G2018_a5b5c1d1e1f1g1.nodes[edge[0]]['pos2018_a5b5c1d1e1f1g1']
    x1, y1 = G2018_a5b5c1d1e1f1g1.nodes[edge[1]]['pos2018_a5b5c1d1e1f1g1']
    edge_trace2018_a5b5c1d1e1f1g1['x'] += tuple([x0, x1, None])
    edge_trace2018_a5b5c1d1e1f1g1['y'] += tuple([y0, y1, None])

for edge in G2018_a5b0c1d1e1f1g1.edges():
    x0, y0 = G2018_a5b0c1d1e1f1g1.nodes[edge[0]]['pos2018_a5b0c1d1e1f1g1']
    x1, y1 = G2018_a5b0c1d1e1f1g1.nodes[edge[1]]['pos2018_a5b0c1d1e1f1g1']
    edge_trace2018_a5b0c1d1e1f1g1['x'] += tuple([x0, x1, None])
    edge_trace2018_a5b0c1d1e1f1g1['y'] += tuple([y0, y1, None])

for edge in G2018_a0b1c1d1e1f1g1.edges():
    x0, y0 = G2018_a0b1c1d1e1f1g1.nodes[edge[0]]['pos2018_a0b1c1d1e1f1g1']
    x1, y1 = G2018_a0b1c1d1e1f1g1.nodes[edge[1]]['pos2018_a0b1c1d1e1f1g1']
    edge_trace2018_a0b1c1d1e1f1g1['x'] += tuple([x0, x1, None])
    edge_trace2018_a0b1c1d1e1f1g1['y'] += tuple([y0, y1, None])

for edge in G2018_a0b5c1d1e1f1g1.edges():
    x0, y0 = G2018_a0b5c1d1e1f1g1.nodes[edge[0]]['pos2018_a0b5c1d1e1f1g1']
    x1, y1 = G2018_a0b5c1d1e1f1g1.nodes[edge[1]]['pos2018_a0b5c1d1e1f1g1']
    edge_trace2018_a0b5c1d1e1f1g1['x'] += tuple([x0, x1, None])
    edge_trace2018_a0b5c1d1e1f1g1['y'] += tuple([y0, y1, None])

for edge in G2018_a0b0c1d1e1f1g1.edges():
    x0, y0 = G2018_a0b0c1d1e1f1g1.nodes[edge[0]]['pos2018_a0b0c1d1e1f1g1']
    x1, y1 = G2018_a0b0c1d1e1f1g1.nodes[edge[1]]['pos2018_a0b0c1d1e1f1g1']
    edge_trace2018_a0b0c1d1e1f1g1['x'] += tuple([x0, x1, None])
    edge_trace2018_a0b0c1d1e1f1g1['y'] += tuple([y0, y1, None])

#node_trace = go.Scatter(
#    x=[],
#    y=[],
#    mode='markers+text', #make markers+text to show labels
#    text=[],
#    hoverinfo='text',
#    customdata=df_combo['GEOID'],
#    marker=dict(
#        showscale=False,
#        colorscale='Edge',
#        reversescale=False,
#        color=[],
#        size=20,
#        opacity=0.8,
#        colorbar=dict(
#            thickness=10,
#            title='COLOR GROUP BY CENSUS TRACT NUMBER',
#            xanchor='left',
#            titleside='right'
#        ),
#        line=dict(width=0)
#    ),
#    showlegend=True,
#    marker_line_width=1
#)

'''
'''
node_trace2018_a1b1c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
   mode='markers+text',  #make markers+text to show labels
    text=[],
    hoverinfo='text',
    customdata=df_combo['GEOID'],
    marker=dict(
        showscale=False,
        colorscale='YlGnBu',
        reversescale=False,
        color=[],
        size=20,
        opacity=0.8,
        colorbar=dict(
            thickness=10,
            title='COLOR GROUP BY CENSUS TRACT NUMBER',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)
    ),
    showlegend=True,
    marker_line_width=1
)

node_trace2018_a1b5c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
   mode='markers+text',  #make markers+text to show labels
    text=[],
    hoverinfo='text',
    customdata=df_combo['GEOID'],
    marker=dict(
        showscale=False,
        colorscale='YlGnBu',
        reversescale=False,
        color=[],
        size=20,
        opacity=0.8,
        colorbar=dict(
            thickness=10,
            title='COLOR GROUP BY CENSUS TRACT NUMBER',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)
    ),
    showlegend=True,
    marker_line_width=1
)

node_trace2018_a1b0c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
   mode='markers+text',  #make markers+text to show labels
    text=[],
    hoverinfo='text',
    customdata=df_combo['GEOID'],
    marker=dict(
        showscale=False,
        colorscale='YlGnBu',
        reversescale=False,
        color=[],
        size=20,
        opacity=0.8,
        colorbar=dict(
            thickness=10,
            title='COLOR GROUP BY CENSUS TRACT NUMBER',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)
    ),
    showlegend=True,
    marker_line_width=1
)

node_trace2018_a5b1c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
   mode='markers+text',  #make markers+text to show labels
    text=[],
    hoverinfo='text',
    customdata=df_combo['GEOID'],
    marker=dict(
        showscale=False,
        colorscale='YlGnBu',
        reversescale=False,
        color=[],
        size=20,
        opacity=0.8,
        colorbar=dict(
            thickness=10,
            title='COLOR GROUP BY CENSUS TRACT NUMBER',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)
    ),
    showlegend=True,
    marker_line_width=1
)

node_trace2018_a5b5c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
   mode='markers+text',  #make markers+text to show labels
    text=[],
    hoverinfo='text',
    customdata=df_combo['GEOID'],
    marker=dict(
        showscale=False,
        colorscale='YlGnBu',
        reversescale=False,
        color=[],
        size=20,
        opacity=0.8,
        colorbar=dict(
            thickness=10,
            title='COLOR GROUP BY CENSUS TRACT NUMBER',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)
    ),
    showlegend=True,
    marker_line_width=1
)

node_trace2018_a5b0c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
   mode='markers+text',  #make markers+text to show labels
    text=[],
    hoverinfo='text',
    customdata=df_combo['GEOID'],
    marker=dict(
        showscale=False,
        colorscale='YlGnBu',
        reversescale=False,
        color=[],
        size=20,
        opacity=0.8,
        colorbar=dict(
            thickness=10,
            title='COLOR GROUP BY CENSUS TRACT NUMBER',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)
    ),
    showlegend=True,
    marker_line_width=1
)

node_trace2018_a0b1c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
   mode='markers+text',  #make markers+text to show labels
    text=[],
    hoverinfo='text',
    customdata=df_combo['GEOID'],
    marker=dict(
        showscale=False,
        colorscale='YlGnBu',
        reversescale=False,
        color=[],
        size=20,
        opacity=0.8,
        colorbar=dict(
            thickness=10,
            title='COLOR GROUP BY CENSUS TRACT NUMBER',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)
    ),
    showlegend=True,
    marker_line_width=1
)

node_trace2018_a0b5c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
   mode='markers+text',  #make markers+text to show labels
    text=[],
    hoverinfo='text',
    customdata=df_combo['GEOID'],
    marker=dict(
        showscale=False,
        colorscale='YlGnBu',
        reversescale=False,
        color=[],
        size=20,
        opacity=0.8,
        colorbar=dict(
            thickness=10,
            title='COLOR GROUP BY CENSUS TRACT NUMBER',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)
    ),
    showlegend=True,
    marker_line_width=1
)

node_trace2018_a0b0c1d1e1f1g1 = go.Scatter(
    x=[],
    y=[],
   mode='markers+text',  #make markers+text to show labels
    text=[],
    hoverinfo='text',
    customdata=df_combo['GEOID'],
    marker=dict(
        showscale=False,
        colorscale='YlGnBu',
        reversescale=False,
        color=[],
        size=20,
        opacity=0.8,
        colorbar=dict(
            thickness=10,
            title='COLOR GROUP BY CENSUS TRACT NUMBER',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)
    ),
    showlegend=True,
    marker_line_width=1
)
#for node in G.nodes():
#    x, y = G.nodes[node]['pos']
#    node_trace['x'] += tuple([x])
#    node_trace['y'] += tuple([y])


for node in G2018_a1b1c1d1e1f1g1.nodes():
    x, y = G2018_a1b1c1d1e1f1g1.nodes[node]['pos2018_a1b1c1d1e1f1g1']
    node_trace2018_a1b1c1d1e1f1g1['x'] += tuple([x])
    node_trace2018_a1b1c1d1e1f1g1['y'] += tuple([y])

for node in G2018_a1b5c1d1e1f1g1.nodes():
    x, y = G2018_a1b5c1d1e1f1g1.nodes[node]['pos2018_a1b5c1d1e1f1g1']
    node_trace2018_a1b5c1d1e1f1g1['x'] += tuple([x])
    node_trace2018_a1b5c1d1e1f1g1['y'] += tuple([y])

for node in G2018_a1b0c1d1e1f1g1.nodes():
    x, y = G2018_a1b0c1d1e1f1g1.nodes[node]['pos2018_a1b0c1d1e1f1g1']
    node_trace2018_a1b0c1d1e1f1g1['x'] += tuple([x])
    node_trace2018_a1b0c1d1e1f1g1['y'] += tuple([y])

for node in G2018_a5b1c1d1e1f1g1.nodes():
    x, y = G2018_a5b1c1d1e1f1g1.nodes[node]['pos2018_a5b1c1d1e1f1g1']
    node_trace2018_a5b1c1d1e1f1g1['x'] += tuple([x])
    node_trace2018_a5b1c1d1e1f1g1['y'] += tuple([y])

for node in G2018_a5b5c1d1e1f1g1.nodes():
    x, y = G2018_a5b5c1d1e1f1g1.nodes[node]['pos2018_a5b5c1d1e1f1g1']
    node_trace2018_a5b5c1d1e1f1g1['x'] += tuple([x])
    node_trace2018_a5b5c1d1e1f1g1['y'] += tuple([y])

for node in G2018_a5b0c1d1e1f1g1.nodes():
    x, y = G2018_a5b0c1d1e1f1g1.nodes[node]['pos2018_a5b0c1d1e1f1g1']
    node_trace2018_a5b0c1d1e1f1g1['x'] += tuple([x])
    node_trace2018_a5b0c1d1e1f1g1['y'] += tuple([y])

for node in G2018_a0b1c1d1e1f1g1.nodes():
    x, y = G2018_a0b1c1d1e1f1g1.nodes[node]['pos2018_a0b1c1d1e1f1g1']
    node_trace2018_a0b1c1d1e1f1g1['x'] += tuple([x])
    node_trace2018_a0b1c1d1e1f1g1['y'] += tuple([y])

for node in G2018_a0b5c1d1e1f1g1.nodes():
    x, y = G2018_a0b5c1d1e1f1g1.nodes[node]['pos2018_a0b5c1d1e1f1g1']
    node_trace2018_a0b5c1d1e1f1g1['x'] += tuple([x])
    node_trace2018_a0b5c1d1e1f1g1['y'] += tuple([y])

for node in G2018_a0b0c1d1e1f1g1.nodes():
    x, y = G2018_a0b0c1d1e1f1g1.nodes[node]['pos2018_a0b0c1d1e1f1g1']
    node_trace2018_a0b0c1d1e1f1g1['x'] += tuple([x])
    node_trace2018_a0b0c1d1e1f1g1['y'] += tuple([y])

'''
node_adjacencies = {}
for graph in graphs_dict:
    key = str(graph).lstrip('G2018_')
    node_adjacencies[key] = []
    for node, adjacencies in enumerate(graphs_dict[graph].adjacency()):
        node_adjacencies[key].append(len(adjacencies[1]))

'''
node_adjacencies2018_a1b1c1d1e1f1g1 = []
node_adjacencies2018_a1b5c1d1e1f1g1 = []
node_adjacencies2018_a1b0c1d1e1f1g1 = []
node_adjacencies2018_a5b1c1d1e1f1g1 = []
node_adjacencies2018_a5b5c1d1e1f1g1 = []
node_adjacencies2018_a5b0c1d1e1f1g1 = []
node_adjacencies2018_a0b1c1d1e1f1g1 = []
node_adjacencies2018_a0b5c1d1e1f1g1 = []
node_adjacencies2018_a0b0c1d1e1f1g1 = []
#for node, adjacencies in enumerate(G.adjacency()):
#    node_adjacencies.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018_a1b1c1d1e1f1g1.adjacency()):
    node_adjacencies2018_a1b1c1d1e1f1g1.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018_a1b5c1d1e1f1g1.adjacency()):
    node_adjacencies2018_a1b5c1d1e1f1g1.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018_a1b0c1d1e1f1g1.adjacency()):
    node_adjacencies2018_a1b0c1d1e1f1g1.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018_a5b1c1d1e1f1g1.adjacency()):
    node_adjacencies2018_a5b1c1d1e1f1g1.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018_a5b5c1d1e1f1g1.adjacency()):
    node_adjacencies2018_a5b5c1d1e1f1g1.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018_a5b0c1d1e1f1g1.adjacency()):
    node_adjacencies2018_a5b0c1d1e1f1g1.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018_a0b1c1d1e1f1g1.adjacency()):
    node_adjacencies2018_a0b1c1d1e1f1g1.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018_a0b5c1d1e1f1g1.adjacency()):
    node_adjacencies2018_a0b5c1d1e1f1g1.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018_a0b0c1d1e1f1g1.adjacency()):
    node_adjacencies2018_a0b0c1d1e1f1g1.append(len(adjacencies[1]))


#for node in G.nodes():
#    node_label = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

for node in G2018_a1b1c1d1e1f1g1.nodes():
    node_label2018_a1b1c1d1e1f1g1 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

for node in G2018_a1b5c1d1e1f1g1.nodes():
    node_label2018_a1b5c1d1e1f1g1 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

for node in G2018_a1b0c1d1e1f1g1.nodes():
    node_label2018_a1b0c1d1e1f1g1 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

for node in G2018_a5b1c1d1e1f1g1.nodes():
    node_label2018_a5b1c1d1e1f1g1 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

for node in G2018_a5b5c1d1e1f1g1.nodes():
    node_label2018_a5b5c1d1e1f1g1 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

for node in G2018_a5b0c1d1e1f1g1.nodes():
    node_label2018_a5b0c1d1e1f1g1 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

for node in G2018_a0b1c1d1e1f1g1.nodes():
    node_label2018_a0b1c1d1e1f1g1 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

for node in G2018_a0b5c1d1e1f1g1.nodes():
    node_label2018_a0b5c1d1e1f1g1 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

for node in G2018_a0b0c1d1e1f1g1.nodes():
    node_label2018_a0b0c1d1e1f1g1 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

df_combo['tract_index'] = df_combo['TRACT_NUM'].astype(int)

#node_trace.marker.color = df_combo['tract_index']
#node_trace.marker.size = node_adjacencies
#node_trace.text = node_label

colorsIndex = {'wallingford':'#ef553b','rainier_beach':'#636efa'}  #manually assign colors
colors = df_combo['neighborhood'].map(colorsIndex)
node_trace2018_a1b1c1d1e1f1g1.marker.color = colors
node_trace2018_a1b5c1d1e1f1g1.marker.color = colors
node_trace2018_a1b0c1d1e1f1g1.marker.color = colors
node_trace2018_a5b1c1d1e1f1g1.marker.color = colors
node_trace2018_a5b5c1d1e1f1g1.marker.color = colors
node_trace2018_a5b0c1d1e1f1g1.marker.color = colors
node_trace2018_a0b1c1d1e1f1g1.marker.color = colors
node_trace2018_a0b5c1d1e1f1g1.marker.color = colors
node_trace2018_a0b0c1d1e1f1g1.marker.color = colors
#node_trace2018.marker.color = df_combo['neighborhood_index'].astype(int)
node_trace2018_a1b1c1d1e1f1g1.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_a1b1c1d1e1f1g1.text = node_label2018_a1b1c1d1e1f1g1
node_trace2018_a1b5c1d1e1f1g1.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_a1b5c1d1e1f1g1.text = node_label2018_a1b5c1d1e1f1g1
node_trace2018_a1b0c1d1e1f1g1.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_a1b0c1d1e1f1g1.text = node_label2018_a1b0c1d1e1f1g1
node_trace2018_a5b1c1d1e1f1g1.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_a5b1c1d1e1f1g1.text = node_label2018_a5b1c1d1e1f1g1
node_trace2018_a5b5c1d1e1f1g1.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_a5b5c1d1e1f1g1.text = node_label2018_a5b5c1d1e1f1g1
node_trace2018_a5b0c1d1e1f1g1.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_a5b0c1d1e1f1g1.text = node_label2018_a5b0c1d1e1f1g1
node_trace2018_a0b1c1d1e1f1g1.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_a0b1c1d1e1f1g1.text = node_label2018_a0b1c1d1e1f1g1
node_trace2018_a0b5c1d1e1f1g1.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_a0b5c1d1e1f1g1.text = node_label2018_a0b5c1d1e1f1g1
node_trace2018_a0b0c1d1e1f1g1.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_a0b0c1d1e1f1g1.text = node_label2018_a0b0c1d1e1f1g1
'''
def get_nodes(subset='a1b1c1d1e1f1g1'):
    subsets = {}
    for node_trace in node_trace2018:
        key = str(node_trace)
        subset[key] = node_trace2018[node_trace]

    if subset in subsets:
        return subsets[subset]
    else:
        raise('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))


def get_edges(subset='a1b1c1d1e1f1g1'):
    for edge_trace in edge_trace2018:
        key = str(edge_trace)
        subset[key] = edge_trace2018[edge_trace]

    if subset in subsets:
        return subsets[subset]
    else:
        raise ('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))


def get_maps(subset='one'):
    subsets = {
        'one': df_combo,
        'half': df_combo,
        'zero': df_combo
    }

    if subset in subsets:
        return subsets[subset]
    else:
        raise ('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))
