import networkx as nx
from fa2 import ForceAtlas2
import pandas as pd
from flask_caching import Cache
import plotly.graph_objects as go


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

#weight the edges
alpha_one = 1/7.0
alpha_half = .5/7.0
alpha_zero = 0/7.0
bravo = 1/7.0
charlie = 1/7.0
delta = 1/7.0
echo = 1/7.0
foxtrot = 1/7.0
golf = 1/7.0
hotel = 0

#NETWORK VERSIONS
#2013 + change version
alpha = alpha_one
antialpha = (1/7 - alpha)
gdf_combo['omega_alpha_one'] = 1/(
        (alpha * gdf.white_pop_pct_change_delta) + \
        ((bravo + antialpha) * gdf.rent_25th_pctile_change_delta) + \
        ((charlie + antialpha) * gdf.totpop_change_delta) + \
        ((delta + antialpha) * gdf.rent_pct_income_change_delta) + \
        ((echo + antialpha) * gdf.monthly_housing_cost_change_delta) + \
        ((foxtrot + antialpha) * gdf.market_rate_units_per_cap_change_delta) + \
        ((golf + antialpha) * gdf.median_tenancy_change_delta) + \
        ((hotel + antialpha) * gdf.median_housing_age_change_delta)
)

#2013 only version
gdf_combo['omega13_alpha_one'] = 1/(
        (alpha_one * gdf.white_pop_pct_change_delta_2013) + \
        ((bravo + antialpha) * gdf.rent_25th_pctile_change_delta_2013) + \
        ((charlie + antialpha) * gdf.totpop_change_delta_2013) + \
        ((delta + antialpha) * gdf.rent_pct_income_change_delta_2013) + \
        ((echo + antialpha) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha) * gdf.market_rate_units_per_cap_change_delta_2013) + \
        ((golf + antialpha) * gdf.median_tenancy_change_delta_2013) + \
        ((hotel + antialpha) * gdf.median_housing_age_change_delta_2013)
)

#2018 only version
gdf_combo['omega18_alpha_one'] = 1/(
        (alpha_one * gdf.white_pop_pct_change_delta_2018) + \
        ((bravo + antialpha) * gdf.rent_25th_pctile_change_delta_2018) + \
        ((charlie + antialpha) * gdf.totpop_change_delta_2018) + \
        ((delta + antialpha) * gdf.rent_pct_income_change_delta_2018) + \
        ((echo + antialpha) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha) * gdf.market_rate_units_per_cap_change_delta_2018) + \
        ((golf + antialpha) * gdf.median_tenancy_change_delta_2018) + \
        ((hotel + antialpha) * gdf.median_housing_age_change_delta_2018)
)

#PLOT
node_list = list(set(df_combo['GEOID']))
#G = nx.Graph()
G2018 = nx.Graph()
G2018_half = nx.Graph()
G2018_zero = nx.Graph()


#normal version (no cache)
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



for i in node_list:
#    G.add_node(i)
    G2018.add_node(i)
    G2018_half.add_node(i)
    G2018_zero.add_node(i)

#Build the Edge list for the network graph for 2013
for i, row in gdf_combo.iterrows():
#    G.add_weighted_edges_from([(row['GEOID_a'],row['GEOID_b'],row['omega13'])])
    G2018.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_alpha_one'])])
    G2018_half.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_alpha_one'])])
    G2018_zero.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_alpha_one'])])
'''
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

def pos2018_half():
    return query_forceatlas2().forceatlas2_networkx_layout(G2018_half, pos=None, iterations=1000)

def pos2018_zero():
    return query_forceatlas2().forceatlas2_networkx_layout(G2018_zero, pos=None, iterations=1000)

#for n, p in pos().items():
#    G.nodes[n]['pos'] = p


for n, p in pos2018().items():
    G2018.nodes[n]['pos'] = p

for n, p in pos2018_half().items():
    G2018_half.nodes[n]['pos'] = p

for n, p in pos2018_zero().items():
    G2018_zero.nodes[n]['pos'] = p

'''
#NON-CACHE-USING VERSION
#pos = forceatlas2.forceatlas2_networkx_layout(G,pos=None, iterations=1000)

#for n, p in pos.items():
#    G.nodes[n]['pos'] = p

pos2018 = forceatlas2.forceatlas2_networkx_layout(G2018,pos=None, iterations=1000)

for n, p in pos2018.items():
    G2018.nodes[n]['pos2018'] = p

pos2018_half = forceatlas2.forceatlas2_networkx_layout(G2018_half,pos=None, iterations=1000)

for n, p in pos2018_half.items():
    G2018_half.nodes[n]['pos2018_half'] = p

pos2018_zero = forceatlas2.forceatlas2_networkx_layout(G2018_zero,pos=None, iterations=1000)

for n, p in pos2018_zero.items():
    G2018_zero.nodes[n]['pos2018_zero'] = p

#plot this bad boy
#edge_trace = go.Scatter(
#    x=[],
#    y=[],
#    line=dict(width=1,color='#c6c6c6'),
#    hoverinfo='text',
#    mode='lines'
#)

edge_trace2018_one = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
)

edge_trace2018_half = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
)

edge_trace2018_zero= go.Scatter(
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
    x0, y0 = G2018.nodes[edge[0]]['pos2018']
    x1, y1 = G2018.nodes[edge[1]]['pos2018']
    edge_trace2018_one['x'] += tuple([x0, x1, None])
    edge_trace2018_one['y'] += tuple([y0, y1, None])

for edge in G2018_half.edges():
    x0, y0 = G2018_half.nodes[edge[0]]['pos2018_half']
    x1, y1 = G2018_half.nodes[edge[1]]['pos2018_half']
    edge_trace2018_half['x'] += tuple([x0, x1, None])
    edge_trace2018_half['y'] += tuple([y0, y1, None])

for edge in G2018_zero.edges():
    x0, y0 = G2018_zero.nodes[edge[0]]['pos2018_zero']
    x1, y1 = G2018_zero.nodes[edge[1]]['pos2018_zero']
    edge_trace2018_zero['x'] += tuple([x0, x1, None])
    edge_trace2018_zero['y'] += tuple([y0, y1, None])

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


node_trace2018_one = go.Scatter(
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

node_trace2018_half = go.Scatter(
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

node_trace2018_zero = go.Scatter(
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
    x, y = G2018.nodes[node]['pos2018']
    node_trace2018_one['x'] += tuple([x])
    node_trace2018_one['y'] += tuple([y])

for node in G2018_half.nodes():
    x, y = G2018_half.nodes[node]['pos2018_half']
    node_trace2018_half['x'] += tuple([x])
    node_trace2018_half['y'] += tuple([y])

for node in G2018_zero.nodes():
    x, y = G2018_zero.nodes[node]['pos2018_zero']
    node_trace2018_zero['x'] += tuple([x])
    node_trace2018_zero['y'] += tuple([y])

#node_adjacencies = []
node_adjacencies2018_one = []
node_adjacencies2018_half = []
node_adjacencies2018_zero = []


#for node, adjacencies in enumerate(G.adjacency()):
#    node_adjacencies.append(len(adjacencies[1]))


for node, adjacencies in enumerate(G2018.adjacency()):
    node_adjacencies2018_one.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018_half.adjacency()):
    node_adjacencies2018_half.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018_zero.adjacency()):
    node_adjacencies2018_zero.append(len(adjacencies[1]))

#for node in G.nodes():
#    node_label = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version


for node in G2018.nodes():
    node_label2018_one = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

for node in G2018_half.nodes():
    node_label2018_half = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

for node in G2018_zero.nodes():
    node_label2018_zero = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

df_combo['tract_index'] = df_combo['TRACT_NUM'].astype(int)

#node_trace.marker.color = df_combo['tract_index']
#node_trace.marker.size = node_adjacencies
#node_trace.text = node_label

colorsIndex = {'wallingford':'#ef553b','rainier_beach':'#636efa'}  #manually assign colors
colors = df_combo['neighborhood'].map(colorsIndex)
node_trace2018_one.marker.color = colors
node_trace2018_half.marker.color = colors
node_trace2018_zero.marker.color = colors
#node_trace2018.marker.color = df_combo['neighborhood_index'].astype(int)
node_trace2018_one.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_one.text = node_label2018_one
node_trace2018_half.marker.size = (1.5 + df_combo.omega18) * 20 #TODO FIX DF VERSIONS OF OMEGA AS WELL - RESPONSIVE SLIDER IF POSSIBLE
node_trace2018_half.text = node_label2018_half
node_trace2018_zero.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_zero.text = node_label2018_zero

def get_nodes(subset='one'):
    subsets = {
        'one': node_trace2018_one,
        'half': node_trace2018_half,
        'zero': node_trace2018_zero
    }

    if subset in subsets:
        return subsets[subset]
    else:
        raise('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))


def get_edges(subset='one'):
    subsets = {
        'one': edge_trace2018_one,
        'half': edge_trace2018_half,
        'zero': edge_trace2018_zero
    }

    if subset in subsets:
        return subsets[subset]
    else:
        raise ('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))
