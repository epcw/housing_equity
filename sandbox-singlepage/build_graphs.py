import networkx as nx
from networkx.readwrite import json_graph
from fa2 import ForceAtlas2
import pandas as pd
from flask_caching import Cache
import plotly.graph_objects as go
import json
import csv
import itertools
import numpy

# set root directory for data files
# ROOTBEER = '/home/ubuntu/housing_equity/sandbox-singlepage/' #production
ROOTBEER = ''  # local

# use static csvs instead of rebuilding the dfs in data_prep_tract every time
df = pd.read_csv(ROOTBEER + 'data/df.csv', dtype={"GEOID": str, "TRACT_NUM": str, "YEAR": str})
gdf = pd.read_csv(ROOTBEER + 'data/gdf.csv', dtype={"GEOID_a": str, "GEOID_b": str, "YEAR": str})
df_combo = pd.read_csv(ROOTBEER + 'data/combo_df.csv', dtype={"GEOID": str, "TRACT_NUM": str, "YEAR": str})
gdf_combo = pd.read_csv(ROOTBEER + 'data/combo_gdf.csv',
                        dtype={"GEOID_a": str, "GEOID_b": str, "TRACT_NUM": str, "YEAR": str})
df_mtbaker = pd.read_csv(ROOTBEER + 'data/mtbaker_station_df.csv', dtype={"GEOID": str, "TRACT_NUM": str, "YEAR": str})
gdf_mtbaker = pd.read_csv(ROOTBEER + 'data/mtbaker_station_gdf.csv',
                          dtype={"GEOID_a": str, "GEOID_b": str, "TRACT_NUM": str, "YEAR": str})
df_othello = pd.read_csv(ROOTBEER + 'data/othello_station_df.csv', dtype={"GEOID": str, "TRACT_NUM": str, "YEAR": str})
gdf_othello = pd.read_csv(ROOTBEER + 'data/othello_station_gdf.csv',
                          dtype={"GEOID_a": str, "GEOID_b": str, "TRACT_NUM": str, "YEAR": str})
df_rb = pd.read_csv(ROOTBEER + 'data/rainier_beach_df.csv', dtype={"GEOID": str, "TRACT_NUM": str, "YEAR": str})
gdf_rb = pd.read_csv(ROOTBEER + 'data/rainier_beach_gdf.csv',
                     dtype={"GEOID_a": str, "GEOID_b": str, "TRACT_NUM": str, "YEAR": str})
df_wallingford = pd.read_csv(ROOTBEER + 'data/wallingford_df.csv', dtype={"GEOID": str, "TRACT_NUM": str, "YEAR": str})
gdf_wallingford = pd.read_csv(ROOTBEER + 'data/wallingford_gdf.csv',
                              dtype={"GEOID_a": str, "GEOID_b": str, "TRACT_NUM": str, "YEAR": str})
df['GEOID_long'] = df['GEOID']
df['GEOID'] = df['GEOID'].str.replace("53033", "")
gdf['GEOID_long_a'] = gdf['GEOID_a']
gdf['GEOID_long_b'] = gdf['GEOID_b']
gdf['GEOID_a'] = gdf['GEOID_a'].str.replace("53033", "")
gdf['GEOID_b'] = gdf['GEOID_b'].str.replace("53033", "")
df_rb['GEOID_long'] = df_rb['GEOID']
df_rb['GEOID'] = df_rb['GEOID'].str.replace("53033", "")
gdf_rb['GEOID_long_a'] = gdf_rb['GEOID_a']
gdf_rb['GEOID_long_b'] = gdf_rb['GEOID_b']
gdf_rb['GEOID_a'] = gdf_rb['GEOID_a'].str.replace("53033", "")
gdf_rb['GEOID_b'] = gdf_rb['GEOID_b'].str.replace("53033", "")
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

slider_names = ('alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot','golf')
slider_symbols_list = [dict(zip(slider_names, p)) for p in itertools.product([0,1,5], repeat=len(slider_names))]

def leppard(slider_values):
    luggage_code = 'a{alpha}b{bravo}c{charlie}d{delta}e{echo}f{foxtrot}g{golf}'.format(**slider_values)
    return luggage_code

slider_keys = [leppard(slider_values) for slider_values in slider_symbols_list]

def value_code(symbol):
    if symbol == 1:
        value = 1
    elif symbol == 5:
        value = 0.5
    elif symbol == 0:
        value = 0
    else:
        raise ValueError
    return value

def normalize(x):
    try:
        z = 1.0/(numpy.sum(x))
    except ZeroDivisionError:
        z = 1.0/len(x)
    return z

slider_values_list = [symbol for symbol in slider_symbols_list]
'''
# NETWORK VERSIONS
# 2013 + change version
print ('calculating network 2013 v 2018 dfs')
for symbols in slider_symbols_list:
    key = leppard(symbols)
    values_dict = dict([(name, value_code(symbol)) for name, symbol in symbols.items()])
    z = normalize(list(values_dict.values()))
    gdf_combo['omega_{key}'.format(key=key)] = 1.0 / ( z * (
        (values_dict['alpha'] * gdf.white_pop_pct_change_delta) + \
        (values_dict['bravo'] * gdf.rent_25th_pctile_change_delta) + \
        (values_dict['charlie'] * gdf.totpop_change_delta) + \
        (values_dict['delta'] * gdf.rent_pct_income_change_delta) + \
        (values_dict['echo'] * gdf.monthly_housing_cost_change_delta) + \
        (values_dict['foxtrot'] * gdf.market_rate_units_per_cap_change_delta) + \
        (values_dict['golf'] * gdf.median_tenancy_change_delta)
        )
    )
print ('calculating network 2013 dfs')
# 2013 only version
for symbols in slider_symbols_list:
    key = leppard(symbols)
    values_dict = dict([(name, value_code(symbol)) for name, symbol in symbols.items()])
    z = normalize(list(values_dict.values()))
    gdf_combo['omega13_{key}'.format(key=key)] = 1.0 / ( z * (
        (values_dict['alpha'] * gdf.white_pop_pct_change_delta_2013) + \
        (values_dict['bravo'] * gdf.rent_25th_pctile_change_delta_2013) + \
        (values_dict['charlie'] * gdf.totpop_change_delta_2013) + \
        (values_dict['delta'] * gdf.rent_pct_income_change_delta_2013) + \
        (values_dict['echo'] * gdf.monthly_housing_cost_change_delta) + \
        (values_dict['foxtrot'] * gdf.market_rate_units_per_cap_change_delta_2013) + \
        (values_dict['golf'] *gdf.median_housing_age_change_delta_2013)
        )
    )

print ('calculating network 2018 dfs')
# 2018 only version
for symbols in slider_symbols_list:
    key = leppard(symbols)
    values_dict = dict([(name, value_code(symbol)) for name, symbol in symbols.items()])
    z = normalize(list(values_dict.values()))
    gdf_combo['omega18_{key}'.format(key=key)] = 1.0 / ( z * (
        (values_dict['alpha'] * gdf.white_pop_pct_change_delta_2018) + \
        (values_dict['bravo'] * gdf.rent_25th_pctile_change_delta_2018) + \
        (values_dict['charlie'] * gdf.totpop_change_delta_2018) + \
        (values_dict['delta'] * gdf.rent_pct_income_change_delta_2018) + \
        (values_dict['echo'] * gdf.monthly_housing_cost_change_delta) + \
        (values_dict['foxtrot'] * gdf.market_rate_units_per_cap_change_delta_2018) + \
        (values_dict['golf'] *gdf.median_housing_age_change_delta_2018)
        )
    )
'''
df_new = df_combo[['GEOID','GEOID_long','COUNTY','TRACT_NUM','neighborhood']]
# MAP VERSIONS
# combo
print ('calculating 2013 dfs')
for symbols in slider_symbols_list:
    key = leppard(symbols)
    values_dict = dict([(name, value_code(symbol)) for name, symbol in symbols.items()])
    z = normalize(list(values_dict.values()))
    df_new['omega13df_{key}'.format(key=key)] = 1.0 / ( z * (
        (values_dict['alpha'] * df_combo.white_pop_pct_2013z.fillna(0)) + \
        (values_dict['bravo'] * df_combo.rent_25th_pctile_2013z.fillna(0)) + \
        (values_dict['charlie'] * df_combo.totpop_2013z.fillna(0)) + \
        (values_dict['delta'] * df_combo.rent_pct_income_2013z.fillna(0)) + \
        (values_dict['echo'] * df_combo.monthly_housing_cost_2013z.fillna(0)) + \
        (values_dict['foxtrot'] * df_combo.market_rate_units_per_cap_2013z.fillna(0)) + \
        (values_dict['golf'] * df_combo.median_tenancy_2013z.fillna(0))
        )
    )
print ('calculating 2018 dfs')
for symbols in slider_symbols_list:
    key = leppard(symbols)
    values_dict = dict([(name, value_code(symbol)) for name, symbol in symbols.items()])
    z = normalize(list(values_dict.values()))
    df_new['omega18df_{key}'.format(key=key)] = 1.0 / ( z * (
        (values_dict['alpha'] * df_combo.white_pop_pct_2018z.fillna(0)) + \
        (values_dict['bravo'] * df_combo.rent_25th_pctile_2018z.fillna(0)) + \
        (values_dict['charlie'] * df_combo.totpop_2018z.fillna(0)) + \
        (values_dict['delta'] * df_combo.rent_pct_income_2018z.fillna(0)) + \
        (values_dict['echo'] * df_combo.monthly_housing_cost_2018z.fillna(0)) + \
        (values_dict['foxtrot'] * df_combo.market_rate_units_per_cap_2018z.fillna(0)) + \
        (values_dict['golf'] * df_combo.median_tenancy_2018z.fillna(0))
        )
    )
print ('calculating 2013 v 2018 dfs')
for symbols in slider_symbols_list:
    key = leppard(symbols)
    values_dict = dict([(name, value_code(symbol)) for name, symbol in symbols.items()])
    z = normalize(list(values_dict.values()))
    df_new['omegadf_{key}'.format(key=key)] = df_new['omega18df_{key}'.format(key=key)] - df_new['omega13df_{key}'.format(key=key)]


#export df_combo for maps
df_new_filename = ROOTBEER + 'data/df_combo.csv'
df_new.to_csv(df_new_filename, index = False, quotechar='"',quoting=csv.QUOTE_ALL)

slider_keys = [leppard(symbols) for symbols in slider_symbols_list]
'''
# PLOT
node_list = list(set(df_combo['GEOID']))

graph_list = {}
print('creating graph objects')
for slider in slider_keys:
    graph_list['G2018_' + str(slider)] = nx.Graph()

# normal version (no cache)
forceatlas2 = ForceAtlas2(
    # Behavior alternatives
    outboundAttractionDistribution=False,  # Dissuade hubs
    linLogMode=False,  # NOT IMPLEMENTED
    adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
    edgeWeightInfluence=2,  # SUPER IMPORTANT - sets edge weights and distance between connected nodes

    # Performance
    jitterTolerance=1.0,  # Tolerance
    barnesHutOptimize=True,  # works better with this than the default
    barnesHutTheta=8.7,  # set around here seems like the right balance for this project
    multiThreaded=False,  # NOT IMPLEMENTED

    # Tuning
    scalingRatio=12,
    strongGravityMode=False,
    gravity=0.00100000,  # this prevents unconnected nodes from flying away due to node repulsion

    # Log
    verbose=False)

print('Adding nodes to network')
for i in node_list:
    for graph in graph_list:
        graph_list[graph].add_node(i)

print('building network edges')
# Build the Edge list for the network graph for 2013
for i, row in gdf_combo.iterrows():
    for graph in graph_list:
        key = str(graph).lstrip('G2018_')
        graph_list[graph].add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_{key}'.format(key=key)])])
'''
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
'''
# NON-CACHE-USING VERSION
print('applying forceatlas2 algorithm to netowrk')
for graph in graph_list:
    pos = forceatlas2.forceatlas2_networkx_layout(graph_list[graph], pos = None, iterations = 1000)
    for n,p in pos.items():
        graph_list[graph].nodes[n]['pos'] = p

print('exporting networks to json files')
# export to json
json_dict = {}
for graph in graph_list:
    json_dict[str(graph)] = json_graph.node_link_data(graph_list[graph])
  #  json_dict['G2018_{key}'] = json_graph.node_link_data(G2018_{key}).format(key=key)

for name, value in json_dict.items():
    filename = ROOTBEER + 'data/json/' + name + '.json'
    with open(filename, 'w') as outfile:
        json.dump(value, outfile)
'''