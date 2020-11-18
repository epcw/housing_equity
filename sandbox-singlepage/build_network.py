import networkx as nx
from networkx.readwrite import json_graph
import pandas as pd
import plotly.express as px
from flask_caching import Cache
import plotly.graph_objects as go
import json
import glob
import os
import itertools

#set root directory for data files
#ROOTBEER = '/home/ubuntu/housing_equity/sandbox-singlepage/' #production
ROOTBEER = '' #local

network_dir = os.path.join(ROOTBEER + 'data/network/')
maps_dir = os.path.join(ROOTBEER + 'data/maps/')

#set a map center (for maps only, obviously)
the_bounty = {"lat": 47.6615392, "lon": -122.3446507}
pikes_place = {"lat": 47.6145537,"lon": -122.3497373}

with open(ROOTBEER + 'data/washingtongeo.json','r') as GeoJSON:
    tracts = json.load(GeoJSON)

df_combo = pd.read_csv(ROOTBEER + 'data/df_combo.csv', dtype={"GEOID": str,"TRACT_NUM": str,"YEAR":str})

#master loop function for slider variables
slider_names = ('alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot','golf') #IF YOU CHANGE THIS, also change the networkx_var dict inside update_network below. And don't forget to add a slider in the HTML.
slider_values_list = [dict(zip(slider_names, p)) for p in itertools.product([0,1,5], repeat=len(slider_names))]

def leppard(slider_values):
    luggage_code = 'a{alpha}b{bravo}c{charlie}d{delta}e{echo}f{foxtrot}g{golf}'.format(**slider_values)
    return luggage_code

slider_keys = [leppard(slider_values) for slider_values in slider_values_list]

#if 'a0b0c0d0e0f0g0' in slider_keys:
#    slider_keys.remove('a0b0c0d0e0f0g0')

for slider in slider_keys:
    print('exporting maps for ' + slider)
    fig4 = px.choropleth_mapbox(df_combo,
                                geojson=tracts,
                                locations=df_combo['GEOID_long'],
                                featureidkey='properties.GEOID',
                                color=df_combo['omegadf_{key}'.format(key=slider)],
                                opacity=0.7,
                                color_continuous_scale='RdYlGn_r')
    fig4.update_layout(mapbox_style="open-street-map",
                       mapbox_zoom=10.5,
                       mapbox_center=pikes_place)
    with open(os.path.join(maps_dir, 'fig4_{key}.json'.format(key=slider)), 'w') as map_file4:
        fig4.write_json(map_file4)

    fig3 = px.scatter(df_combo,
                      x='omega13df_{key}'.format(key=slider),
                      y='omega18df_{key}'.format(key=slider),
                      color='neighborhood',
                      text='GEOID'
                      )
    fig3.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )
    #  update_yaxes(
    #    range=[-1.5, 1.5]
    # )
    # fig3.update_xaxes(
    #    range=[-1.5, 1.5]
    # )
    fig3.update_traces(textposition="middle right")

    # can set axis ratios, as well
    # fig.update_yaxes(
    #    scaleanchor = "x",
    #    scaleratio = 1,
    #  )
    #

    fig3.update_traces(marker=dict(size=20))
    # Add Diagonal Line so you can see movement btw 2013 and 2018
    fig3.add_shape(
        type="line",
        x0=-5,
        y0=-5,
        x1=5,
        y1=5,
        line=dict(
            color="MediumPurple",
            width=4,
            dash="dash",
        )
    )
    with open(os.path.join(maps_dir, 'fig3_{key}.json'.format(key=slider)), 'w') as map_file3:
        fig3.write_json(map_file3)

    fig5 = px.choropleth_mapbox(df_combo,
                                geojson=tracts,
                                locations=df_combo['GEOID_long'],
                                featureidkey='properties.GEOID',
                                color=df_combo['omega13df_{key}'.format(key=slider)],
                                opacity=0.7,
                                color_continuous_scale='RdYlGn_r')
    fig5.update_layout(mapbox_style="open-street-map",
                       mapbox_zoom=10.5,
                       mapbox_center=pikes_place)
    fig6 = px.choropleth_mapbox(df_combo,
                                geojson=tracts,
                                locations=df_combo['GEOID_long'],
                                featureidkey='properties.GEOID',
                                color=df_combo['omega18df_{key}'.format(key=slider)],
                                opacity=0.7,
                                color_continuous_scale='RdYlGn_r')
    fig6.update_layout(mapbox_style="open-street-map",
                       mapbox_zoom=10.5,
                       mapbox_center=pikes_place)
    with open(os.path.join(maps_dir, 'fig5_{key}.json'.format(key=slider)), 'w') as map_file5:
        fig5.write_json(map_file5)
        
    with open(os.path.join(maps_dir, 'fig6_{key}.json'.format(key=slider)), 'w') as map_file6:
        fig6.write_json(map_file6)

'''
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

#from build_network import get_nodes, get_edges
for graph_name in graphs_dict:
    key = str(graph_name).lstrip('G2018_')


colorsIndex = {'wallingford':'#ef553b','rainier_beach':'#636efa'}  #manually assign colors
colors = df_combo['neighborhood'].map(colorsIndex)

print('adding nodes and edges to graphs')
for graph_name in graphs_dict:
    key = str(graph_name).lstrip('G2018_')
    print('creating graph objects for ' + graph_name)
    node_trace2018 = go.Scatter(
        x=[],
        y=[],
        mode='markers+text',  # make markers+text to show labels
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
    edge_trace2018 = go.Scatter(
        x=[],
        y=[],
        line=dict(width=1, color='#c6c6c6'),
        hoverinfo='text',
        mode='lines'
    )
    print('building edges for ' + graph_name)
    for edge in graphs_dict[graph_name].edges():
        x0, y0 = graphs_dict[graph_name].nodes[edge[0]]['pos']
        x1, y1 = graphs_dict[graph_name].nodes[edge[1]]['pos']
        edge_trace2018['x'] += tuple([x0, x1, None])
        edge_trace2018['y'] += tuple([y0, y1, None])

    print('building nodes for ' + graph_name)
    for node in graphs_dict[graph_name].nodes():
        x, y = graphs_dict[graph_name].nodes[node]['pos']
        print(graph_name + ' ' + node + ' x')
        node_trace2018['x'] += tuple([x])
        print(graph_name + ' ' + node + ' y')
        node_trace2018['y'] += tuple([y])
        print(graph_name + ' ' + node + ' text')
        node_trace2018.text = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  # tract version
        print(graph_name + ' ' + node + ' markers')
        node_trace2018.marker.color = colors
        node_trace2018.marker.size = (1.5 + df_combo.omega18) * 20

#    node_adjacencies = []
#   for node, adjacencies in enumerate(graphs_dict[graph_name].items().adjacency()):
#        node_adjacencies.append(len(adjacencies[1]))

    fig = go.Figure(data=[edge_trace2018,node_trace2018],
                    layout=go.Layout(
                        title='',
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    with open(os.path.join(network_dir, 'network_{key}.json'.format(key=key)), 'w') as network_file:
        fig.write_json(network_file)


#node_adjacencies = {}
#for graph_name in graphs_dict:
#    key = str(graph_name).lstrip('G2018_')
#    node_adjacencies[key] = []
#    for node, adjacencies in enumerate(graphs_dict[graph].items().adjacency()):
#        node_adjacencies[key].append(len(adjacencies[1]))
'''
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

'''
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
