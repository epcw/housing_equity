import networkx as nx
from fa2 import ForceAtlas2
import pandas as pd

#TRACT VERSION
import data_prep_tract
df = data_prep_tract.get_df()
gdf = data_prep_tract.get_gdf()
df_wallingford = data_prep_tract.get_df(subset='wallingford')
gdf_wallingford = data_prep_tract.get_gdf(subset='wallingford')
df_rb = data_prep_tract.get_df(subset='rainier_beach')
gdf_rb = data_prep_tract.get_gdf(subset='rainier_beach')
df_combo = data_prep_tract.get_df(subset='combo')
gdf_combo = data_prep_tract.get_gdf(subset='combo')
#df_mtbaker = data_prep_tract.get_df(subset='mtbaker_station')
#gdf_mtbaker = data_prep_tract.get_gdf(subset='mtbaker_station')
#df_othello = data_prep_tract.get_df(subset='othello_station')
#gdf_othello = data_prep_tract.get_gdf(subset='othello_station')
df_rb['GEOID_long'] = df_rb['GEOID']
df_rb['GEOID'] = df_rb['GEOID'].str.replace("53033", "")
gdf_rb['GEOID_long_a'] = gdf_rb['GEOID_a']
gdf_rb['GEOID_long_b'] = gdf_rb['GEOID_b']
gdf_rb['GEOID_a'] = gdf_rb['GEOID_a'].str.replace("53033", "")
gdf_rb['GEOID_b'] = gdf_rb['GEOID_b'].str.replace("53033", "")
#df_mtbaker['GEOID_long'] = df_mtbaker['GEOID']
#df_mtbaker['GEOID'] = df_mtbaker['GEOID'].str.replace("53033", "")
#gdf_mtbaker['GEOID_long_a'] = gdf_mtbaker['GEOID_a']
#gdf_mtbaker['GEOID_long_b'] = gdf_mtbaker['GEOID_b']
#gdf_mtbaker['GEOID_a'] = gdf_mtbaker['GEOID_a'].str.replace("53033", "")
#gdf_mtbaker['GEOID_b'] = gdf_mtbaker['GEOID_b'].str.replace("53033", "")
#df_othello['GEOID_long'] = df_othello['GEOID']
#df_othello['GEOID'] = df_othello['GEOID'].str.replace("53033", "")
#gdf_othello['GEOID_long_a'] = gdf_othello['GEOID_a']
#gdf_othello['GEOID_long_b'] = gdf_othello['GEOID_b']
#gdf_othello['GEOID_a'] = gdf_othello['GEOID_a'].str.replace("53033", "")
#gdf_othello['GEOID_b'] = gdf_othello['GEOID_b'].str.replace("53033", "")
df['GEOID_long'] = df['GEOID']
df['GEOID'] = df['GEOID'].str.replace("53033", "")
gdf['GEOID_long_a'] = gdf['GEOID_a']
gdf['GEOID_long_b'] = gdf['GEOID_b']
gdf['GEOID_a'] = gdf['GEOID_a'].str.replace("53033", "")
gdf['GEOID_b'] = gdf['GEOID_b'].str.replace("53033", "")
df_wallingford['GEOID_long'] = df_wallingford['GEOID']
df_wallingford['GEOID'] = df_wallingford['GEOID'].str.replace("53033", "")
gdf_wallingford['GEOID_long_a'] = gdf_wallingford['GEOID_a']
gdf_wallingford['GEOID_long_b'] = gdf_wallingford['GEOID_b']
gdf_wallingford['GEOID_a'] = gdf_wallingford['GEOID_a'].str.replace("53033", "")
gdf_wallingford['GEOID_b'] = gdf_wallingford['GEOID_b'].str.replace("53033", "")
df_combo['GEOID_long'] = df_combo['GEOID']
df_combo['GEOID'] = df_combo['GEOID'].str.replace("53033", "")
gdf_combo['GEOID_long_a'] = gdf_combo['GEOID_a']
gdf_combo['GEOID_long_b'] = gdf_combo['GEOID_b']
gdf_combo['GEOID_a'] = gdf_combo['GEOID_a'].str.replace("53033", "")
gdf_combo['GEOID_b'] = gdf_combo['GEOID_b'].str.replace("53033", "")


'''
#BLOCK GROUP VERSION
import data_prep_blockgrp
df = data_prep_blockgrp.get_df()
gdf = data_prep_blockgrp.get_gdf()
df_wallingford = data_prep_blockgrp.get_df(subset='wallingford')
gdf_wallingford = data_prep_blockgrp.get_gdf(subset='wallingford')
df_rb = data_prep_blockgrp.get_df(subset='rainier_beach')
gdf_rb = data_prep_blockgrp.get_gdf(subset='rainier_beach')
df_mtbaker = data_prep_blockgrp.get_df(subset='mtbaker_station')
gdf_mtbaker = data_prep_blockgrp.get_gdf(subset='mtbaker_station')
df_othello = data_prep_blockgrp.get_df(subset='othello_station')
gdf_othello = data_prep_blockgrp.get_gdf(subset='othello_station')
df_rb['GEOID_long'] = df_rb['GEOID']
df_rb['GEOID'] = df_rb['GEOID'].str.replace("53033", "")
gdf_rb['GEOID_long_a'] = gdf_rb['GEOID_a']
gdf_rb['GEOID_long_b'] = gdf_rb['GEOID_b']
gdf_rb['GEOID_a'] = gdf_rb['GEOID_a'].str.replace("53033", "")
gdf_rb['GEOID_b'] = gdf_rb['GEOID_b'].str.replace("53033", "")
df_mtbaker['GEOID_long'] = df_mtbaker['GEOID']
df_mtbaker['GEOID'] = df_mtbaker['GEOID'].str.replace("53033", "")
gdf_mtbaker['GEOID_long_a'] = gdf_mtbaker['GEOID_a']
gdf_mtbaker['GEOID_long_b'] = gdf_mtbaker['GEOID_b']
gdf_mtbaker['GEOID_a'] = gdf_mtbaker['GEOID_a'].str.replace("53033", "")
gdf_mtbaker['GEOID_b'] = gdf_mtbaker['GEOID_b'].str.replace("53033", "")
df_othello['GEOID_long'] = df_othello['GEOID']
df_othello['GEOID'] = df_othello['GEOID'].str.replace("53033", "")
gdf_othello['GEOID_long_a'] = gdf_othello['GEOID_a']
gdf_othello['GEOID_long_b'] = gdf_othello['GEOID_b']
gdf_othello['GEOID_a'] = gdf_othello['GEOID_a'].str.replace("53033", "")
gdf_othello['GEOID_b'] = gdf_othello['GEOID_b'].str.replace("53033", "")
df['GEOID_long'] = df['GEOID']
df['GEOID'] = df['GEOID'].str.replace("53033", "")
gdf['GEOID_long_a'] = gdf['GEOID_a']
gdf['GEOID_long_b'] = gdf['GEOID_b']
gdf['GEOID_a'] = gdf['GEOID_a'].str.replace("53033", "")
gdf['GEOID_b'] = gdf['GEOID_b'].str.replace("53033", "")
df_wallingford['GEOID_long'] = df_wallingford['GEOID']
df_wallingford['GEOID'] = df_wallingford['GEOID'].str.replace("53033", "")
gdf_wallingford['GEOID_long_a'] = gdf_wallingford['GEOID_a']
gdf_wallingford['GEOID_long_b'] = gdf_wallingford['GEOID_b']
gdf_wallingford['GEOID_a'] = gdf_wallingford['GEOID_a'].str.replace("53033", "")
gdf_wallingford['GEOID_b'] = gdf_wallingford['GEOID_b'].str.replace("53033", "")


from data_prep_blockgrp import block_grp_geoids
'''

#PLOT
node_list = list(set(df_combo['GEOID']))
#G = nx.Graph()
G2018 = nx.Graph()


'''
#normal version (no cache)
forceatlas2 = ForceAtlas2(
                        # Behavior alternatives
                        outboundAttractionDistribution=False,  # Dissuade hubs
                        linLogMode=False,  # NOT IMPLEMENTED
                        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                        edgeWeightInfluence=5.0,

                        # Performance
                        jitterTolerance=1.0,  # Tolerance
                        barnesHutOptimize=True,
                        barnesHutTheta=1.2,
                        multiThreaded=False,  # NOT IMPLEMENTED

                        # Tuning
                        scalingRatio=2,
                        strongGravityMode=True,
                        gravity=20.0,

                        # Log
                        verbose=True)
'''


for i in node_list:
#    G.add_node(i)
    G2018.add_node(i)


#Build the Edge list for the network graph for 2013
for i, row in gdf_combo.iterrows():
#    G.add_weighted_edges_from([(row['GEOID_a'],row['GEOID_b'],row['omega13'])])
    G2018.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18'])])


#CACHE-USING VERSION
@cache.memoize(timeout=TIMEOUT)
def query_forceatlas2():
    forceatlas2 = ForceAtlas2(
                            # Behavior alternatives
                            outboundAttractionDistribution=False,  # Dissuade hubs
                            linLogMode=False,  # NOT IMPLEMENTED
                            adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                            edgeWeightInfluence=2,  #SUPER IMPORTANT - sets edge weights and distance between connected nodes

                            # Performance
                            jitterTolerance=1.0,  # Tolerance
                            barnesHutOptimize=True,  #works better with this than the default
                            barnesHutTheta=8.7,  #set around here seems like the right balance for this project
                            multiThreaded=False,  # NOT IMPLEMENTED

                            # Tuning
                            scalingRatio=12,
                            strongGravityMode=False,
                            gravity=0.00100000,  #this prevents unconnected nodes from flying away due to node repulsion

                            # Log
                            verbose=False)
    return forceatlas2


#def pos():
#    return query_forceatlas2().forceatlas2_networkx_layout(G, pos=None, iterations=1000)


def pos2018():
    return query_forceatlas2().forceatlas2_networkx_layout(G2018, pos=None, iterations=1000)


#for n, p in pos().items():
#    G.nodes[n]['pos'] = p


for n, p in pos2018().items():
    G2018.nodes[n]['pos'] = p


'''
#NON-CACHE-USING VERSION
pos = forceatlas2.forceatlas2_networkx_layout(G,pos=None, iterations=1000)


for n, p in pos.items():
    G.nodes[n]['pos'] = p
'''


#plot this bad boy
#edge_trace = go.Scatter(
#    x=[],
#    y=[],
#    line=dict(width=1,color='#c6c6c6'),
#    hoverinfo='text',
#    mode='lines'
#)


edge_trace2018 = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
)

#for edge in G.edges():
#    x0, y0 = G.nodes[edge[0]]['pos']
#    x1, y1 = G.nodes[edge[1]]['pos']
#    edge_trace['x'] += tuple([x0, x1, None])
#    edge_trace['y'] += tuple([y0, y1, None])


for edge in G2018.edges():
    x0, y0 = G2018.nodes[edge[0]]['pos']
    x1, y1 = G2018.nodes[edge[1]]['pos']
    edge_trace2018['x'] += tuple([x0, x1, None])
    edge_trace2018['y'] += tuple([y0, y1, None])


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


node_trace2018 = go.Scatter(
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


for node in G2018.nodes():
    x, y = G2018.nodes[node]['pos']
    node_trace2018['x'] += tuple([x])
    node_trace2018['y'] += tuple([y])


#node_adjacencies = []
node_adjacencies2018 = []


#for node, adjacencies in enumerate(G.adjacency()):
#    node_adjacencies.append(len(adjacencies[1]))


for node, adjacencies in enumerate(G2018.adjacency()):
    node_adjacencies2018.append(len(adjacencies[1]))


#for node in G.nodes():
#    node_label = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version


for node in G2018.nodes():
    node_label2018 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version


df_combo['tract_index'] = df_combo['TRACT_NUM'].astype(int)


#node_trace.marker.color = df_combo['tract_index']
#node_trace.marker.size = node_adjacencies
#node_trace.text = node_label


colorsIndex = {'wallingford':'#ef553b','rainier_beach':'#636efa'}  #manually assign colors
colors = df_combo['neighborhood'].map(colorsIndex)
node_trace2018.marker.color = colors
#node_trace2018.marker.color = df_combo['neighborhood_index'].astype(int)
node_trace2018.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018.text = node_label2018

def get_node_trace(subset='all'):
    subsets = {
        'all': node_df,
    }

    if subset in subsets:
        return subsets[subset]
    else:
        raise('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))


def get_node_trace(subset='all'):
    subsets = {
        'all': edge_df,
    }

    if subset in subsets:
        return subsets[subset]
    else:
        raise ('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))
