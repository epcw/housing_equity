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

#set directory for graph_name jsons
json_dir = ROOTBEER + 'data/json/*'
graphs_dict = {} #set a dictionary to hold graphs
for file in glob.iglob(json_dir):
    with open (file) as json_file:
        graph_name = os.path.basename(file)
        graph_name = graph_name.rstrip('.json')
        graph = json.load(json_file)
        graphs_dict[graph_name] = json_graph.node_link_graph(graph) #sets a value that consists of the networkx graph

print('loading graph files')
#loop over graph_dict to write all the variables for the graph
#for graph_name_name, graph in graphs_dict.items():
#    exec(graph_name + '=graph')

node_trace2018 = {}
edge_trace2018 = {}

df_combo = pd.read_csv(ROOTBEER + 'data/df_combo.csv', dtype={"GEOID": str,"TRACT_NUM": str,"YEAR":str})

#from build_network import get_nodes, get_edges
print('creating graph objects')
for graph_name in graphs_dict:
    key = str(graph_name).lstrip('G2018_')
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

network_dir = os.path.join(ROOTBEER + 'data/network/')

print('adding nodes and edges to graphs')
for graph_name in graphs_dict:
    key = str(graph_name).lstrip('G2018_')
    print('building edges for ' + graph_name)
    for edge in graphs_dict[graph_name].edges():
        x0, y0 = graphs_dict[graph_name].nodes[edge[0]]['pos']
        x1, y1 = graphs_dict[graph_name].nodes[edge[1]]['pos']
        edge_trace2018[key]['x'] += tuple([x0, x1, None])
        edge_trace2018[key]['y'] += tuple([y0, y1, None])

    print('building nodes for ' + graph_name)
    for node in graphs_dict[graph_name].nodes():
        x, y = graphs_dict[graph_name].nodes[node]['pos']
        print(graph_name + ' ' + node + ' x')
        node_trace2018[key]['x'] += tuple([x])
        print(graph_name + ' ' + node + ' y')
        node_trace2018[key]['y'] += tuple([y])
        print(graph_name + ' ' + node + ' text')
        node_trace2018[key].text = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  # tract version
        print(graph_name + ' ' + node + ' markers')
        node_trace2018[key].marker.color = colors
        node_trace2018[key].marker.size = (1.5 + df_combo.omega18) * 20

    with open(os.path.join(network_dir, 'node_trace_2018{key}'.format(key=key)), 'w') as node_trace_file:
        node_trace2018[key].write_json(node_trace_file)

    with open(os.path.join(network_dir, 'edge_trace_2018{key}'.format(key=key)), 'w') as edge_trace_file:
        edge_trace2018[key].write_json(edge_trace_file)

    break

print('calculating adjacencies')

node_adjacencies = {}
for graph_name in graphs_dict:
    key = str(graph_name).lstrip('G2018_')
    node_adjacencies[key] = []
    for node, adjacencies in enumerate(graphs_dict[graph].adjacency()):
        node_adjacencies[key].append(len(adjacencies[1]))

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
