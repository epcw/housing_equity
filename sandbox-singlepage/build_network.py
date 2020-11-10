import networkx as nx
from fa2 import ForceAtlas2
import pandas as pd
from flask_caching import Cache
import plotly.graph_objects as go
import json

#set root directory for data files
#ROOTBEER = '/home/ubuntu/housing_equity/sandbox-singlepage/' #production
ROOTBEER = '' #local

with open(ROOTBEER + 'data/washingtongeo.json','r') as GeoJSON:
    tracts = json.load(GeoJSON)

#use static csvs instead of rebuilding the dfs in data_prep_tract every time
df = pd.read_csv(ROOTBEER + 'data/df.csv', dtype={"GEOID": str,"TRACT_NUM": str,"YEAR":str})
gdf = pd.read_csv(ROOTBEER + 'data/gdf.csv', dtype={"GEOID_a": str, "GEOID_b": str,"YEAR":str})
df_combo = pd.read_csv(ROOTBEER + 'data/combo_df.csv', dtype={"GEOID": str,"TRACT_NUM": str,"YEAR":str})
gdf_combo = pd.read_csv(ROOTBEER + 'data/combo_gdf.csv', dtype={"GEOID_a": str, "GEOID_b": str,"TRACT_NUM": str,"YEAR":str})
df_mtbaker = pd.read_csv(ROOTBEER + 'data/mtbaker_station_df.csv', dtype={"GEOID": str,"TRACT_NUM": str,"YEAR":str})
gdf_mtbaker = pd.read_csv(ROOTBEER + 'data/mtbaker_station_gdf.csv', dtype={"GEOID_a": str, "GEOID_b": str,"TRACT_NUM": str,"YEAR":str})
df_othello = pd.read_csv(ROOTBEER + 'data/othello_station_df.csv', dtype={"GEOID": str,"TRACT_NUM": str,"YEAR":str})
gdf_othello = pd.read_csv(ROOTBEER + 'data/othello_station_gdf.csv', dtype={"GEOID_a": str, "GEOID_b": str,"TRACT_NUM": str,"YEAR":str})
df_rb = pd.read_csv(ROOTBEER + 'data/rainier_beach_df.csv', dtype={"GEOID": str,"TRACT_NUM": str,"YEAR":str})
gdf_rb = pd.read_csv(ROOTBEER + 'data/rainier_beach_gdf.csv', dtype={"GEOID_a": str, "GEOID_b": str,"TRACT_NUM": str,"YEAR":str})
df_wallingford = pd.read_csv(ROOTBEER + 'data/wallingford_df.csv', dtype={"GEOID": str,"TRACT_NUM": str,"YEAR":str})
gdf_wallingford = pd.read_csv(ROOTBEER + 'data/wallingford_gdf.csv', dtype={"GEOID_a": str, "GEOID_b": str,"TRACT_NUM": str,"YEAR":str})
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
antialpha_one = (1/7 - alpha_one)
gdf_combo['omega_a1b1c1d1e1f1g1'] = 1/(
        (alpha_one * gdf.white_pop_pct_change_delta) + \
        ((bravo + antialpha_one) * gdf.rent_25th_pctile_change_delta) + \
        ((charlie + antialpha_one) * gdf.totpop_change_delta) + \
        ((delta + antialpha_one) * gdf.rent_pct_income_change_delta) + \
        ((echo + antialpha_one) * gdf.monthly_housing_cost_change_delta) + \
        ((foxtrot + antialpha_one) * gdf.market_rate_units_per_cap_change_delta) + \
        ((golf + antialpha_one) * gdf.median_tenancy_change_delta) + \
        ((hotel + antialpha_one) * gdf.median_housing_age_change_delta)
)

#2013 only version
gdf_combo['omega13_a1b1c1d1e1f1g1'] = 1/(
        (alpha_one * gdf.white_pop_pct_change_delta_2013) + \
        ((bravo + antialpha_one) * gdf.rent_25th_pctile_change_delta_2013) + \
        ((charlie + antialpha_one) * gdf.totpop_change_delta_2013) + \
        ((delta + antialpha_one) * gdf.rent_pct_income_change_delta_2013) + \
        ((echo + antialpha_one) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_one) * gdf.market_rate_units_per_cap_change_delta_2013) + \
        ((golf + antialpha_one) * gdf.median_tenancy_change_delta_2013) + \
        ((hotel + antialpha_one) * gdf.median_housing_age_change_delta_2013)
)

#2018 only version
gdf_combo['omega18_a1b1c1d1e1f1g1'] = 1/(
        (alpha_one * gdf.white_pop_pct_change_delta_2018) + \
        ((bravo + antialpha_one) * gdf.rent_25th_pctile_change_delta_2018) + \
        ((charlie + antialpha_one) * gdf.totpop_change_delta_2018) + \
        ((delta + antialpha_one) * gdf.rent_pct_income_change_delta_2018) + \
        ((echo + antialpha_one) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_one) * gdf.market_rate_units_per_cap_change_delta_2018) + \
        ((golf + antialpha_one) * gdf.median_tenancy_change_delta_2018) + \
        ((hotel + antialpha_one) * gdf.median_housing_age_change_delta_2018)
)

#MAP VERSIONS
#combo
df_combo['omega13df_a1b1c1d1e1f1g1'] = (
        (alpha_one * df_combo.white_pop_pct_2013z.fillna(0)) + \
        ((bravo + antialpha_one) * df_combo.rent_25th_pctile_2013z.fillna(0)) + \
        ((charlie + antialpha_one) * df_combo.totpop_2013z.fillna(0)) + \
        ((delta + antialpha_one) * df_combo.rent_pct_income_2013z.fillna(0)) + \
        ((echo + antialpha_one) * df_combo.monthly_housing_cost_2013z.fillna(0)) + \
        ((foxtrot + antialpha_one) * df_combo.market_rate_units_per_cap_2013z.fillna(0)) + \
        ((golf + antialpha_one) * df_combo.median_tenancy_2013z.fillna(0))
)

df_combo['omega18df_a1b1c1d1e1f1g1'] = (
        (alpha_one * df_combo.white_pop_pct_2018z.fillna(0)) + \
        ((bravo + antialpha_one) * df_combo.rent_25th_pctile_2018z.fillna(0)) + \
        ((charlie + antialpha_one) * df_combo.totpop_2018z.fillna(0)) + \
        ((delta + antialpha_one) * df_combo.rent_pct_income_2018z.fillna(0)) + \
        ((echo + antialpha_one) * df_combo.monthly_housing_cost_2018z.fillna(0)) + \
        ((foxtrot + antialpha_one) * df_combo.market_rate_units_per_cap_2018z.fillna(0)) + \
        ((golf + antialpha_one) * df_combo.median_tenancy_2018z.fillna(0))
)
df_combo['omegadf_a1b1c1d1e1f1g1'] = df_combo.omega18df_a1b1c1d1e1f1g1 - df_combo.omega13df_a1b1c1d1e1f1g1

antialpha_half = (1/7 - alpha_half)
gdf_combo['omega_a5b1c1d1e1f1g1'] = 1/(
        (alpha_half * gdf.white_pop_pct_change_delta) + \
        ((bravo + antialpha_half) * gdf.rent_25th_pctile_change_delta) + \
        ((charlie + antialpha_half) * gdf.totpop_change_delta) + \
        ((delta + antialpha_half) * gdf.rent_pct_income_change_delta) + \
        ((echo + antialpha_half) * gdf.monthly_housing_cost_change_delta) + \
        ((foxtrot + antialpha_half) * gdf.market_rate_units_per_cap_change_delta) + \
        ((golf + antialpha_half) * gdf.median_tenancy_change_delta) + \
        ((hotel + antialpha_half) * gdf.median_housing_age_change_delta)
)

#2013 only version
gdf_combo['omega13_a5b1c1d1e1f1g1'] = 1/(
        (alpha_half * gdf.white_pop_pct_change_delta_2013) + \
        ((bravo + antialpha_half) * gdf.rent_25th_pctile_change_delta_2013) + \
        ((charlie + antialpha_half) * gdf.totpop_change_delta_2013) + \
        ((delta + antialpha_half) * gdf.rent_pct_income_change_delta_2013) + \
        ((echo + antialpha_half) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_half) * gdf.market_rate_units_per_cap_change_delta_2013) + \
        ((golf + antialpha_half) * gdf.median_tenancy_change_delta_2013) + \
        ((hotel + antialpha_half) * gdf.median_housing_age_change_delta_2013)
)

#2018 only version
gdf_combo['omega18_a5b1c1d1e1f1g1'] = 1/(
        (alpha_half * gdf.white_pop_pct_change_delta_2018) + \
        ((bravo + antialpha_half) * gdf.rent_25th_pctile_change_delta_2018) + \
        ((charlie + antialpha_half) * gdf.totpop_change_delta_2018) + \
        ((delta + antialpha_half) * gdf.rent_pct_income_change_delta_2018) + \
        ((echo + antialpha_half) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_half) * gdf.market_rate_units_per_cap_change_delta_2018) + \
        ((golf + antialpha_half) * gdf.median_tenancy_change_delta_2018) + \
        ((hotel + antialpha_half) * gdf.median_housing_age_change_delta_2018)
)

#MAP VERSIONS
#combo
df_combo['omega13df_a5b1c1d1e1f1g1'] = (
        (alpha_half * df_combo.white_pop_pct_2013z.fillna(0)) + \
        ((bravo + antialpha_half) * df_combo.rent_25th_pctile_2013z.fillna(0)) + \
        ((charlie + antialpha_half) * df_combo.totpop_2013z.fillna(0)) + \
        ((delta + antialpha_half) * df_combo.rent_pct_income_2013z.fillna(0)) + \
        ((echo + antialpha_half) * df_combo.monthly_housing_cost_2013z.fillna(0)) + \
        ((foxtrot + antialpha_half) * df_combo.market_rate_units_per_cap_2013z.fillna(0)) + \
        ((golf + antialpha_half) * df_combo.median_tenancy_2013z.fillna(0))
)

df_combo['omega18df_a5b1c1d1e1f1g1'] = (
        (alpha_half * df_combo.white_pop_pct_2018z.fillna(0)) + \
        ((bravo + antialpha_half) * df_combo.rent_25th_pctile_2018z.fillna(0)) + \
        ((charlie + antialpha_half) * df_combo.totpop_2018z.fillna(0)) + \
        ((delta + antialpha_half) * df_combo.rent_pct_income_2018z.fillna(0)) + \
        ((echo + antialpha_half) * df_combo.monthly_housing_cost_2018z.fillna(0)) + \
        ((foxtrot + antialpha_half) * df_combo.market_rate_units_per_cap_2018z.fillna(0)) + \
        ((golf + antialpha_half) * df_combo.median_tenancy_2018z.fillna(0))
)
df_combo['omegadf_a5b1c1d1e1f1g1'] = df_combo.omega18df_a5b1c1d1e1f1g1 - df_combo.omega13df_a5b1c1d1e1f1g1

antialpha_zero = (1/7 - alpha_zero)
gdf_combo['omega_a0b1c1d1e1f1g1'] = 1/(
        (alpha_zero * gdf.white_pop_pct_change_delta) + \
        ((bravo + antialpha_half) * gdf.rent_25th_pctile_change_delta) + \
        ((charlie + antialpha_half) * gdf.totpop_change_delta) + \
        ((delta + antialpha_half) * gdf.rent_pct_income_change_delta) + \
        ((echo + antialpha_half) * gdf.monthly_housing_cost_change_delta) + \
        ((foxtrot + antialpha_half) * gdf.market_rate_units_per_cap_change_delta) + \
        ((golf + antialpha_half) * gdf.median_tenancy_change_delta) + \
        ((hotel + antialpha_half) * gdf.median_housing_age_change_delta)
)

#2013 only version
gdf_combo['omega13_a0b1c1d1e1f1g1'] = 1/(
        (alpha_zero * gdf.white_pop_pct_change_delta_2013) + \
        ((bravo + antialpha_half) * gdf.rent_25th_pctile_change_delta_2013) + \
        ((charlie + antialpha_half) * gdf.totpop_change_delta_2013) + \
        ((delta + antialpha_half) * gdf.rent_pct_income_change_delta_2013) + \
        ((echo + antialpha_half) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_half) * gdf.market_rate_units_per_cap_change_delta_2013) + \
        ((golf + antialpha_half) * gdf.median_tenancy_change_delta_2013) + \
        ((hotel + antialpha_half) * gdf.median_housing_age_change_delta_2013)
)

#2018 only version
gdf_combo['omega18_a0b1c1d1e1f1g1'] = 1/(
        (alpha_zero * gdf.white_pop_pct_change_delta_2018) + \
        ((bravo + antialpha_half) * gdf.rent_25th_pctile_change_delta_2018) + \
        ((charlie + antialpha_half) * gdf.totpop_change_delta_2018) + \
        ((delta + antialpha_half) * gdf.rent_pct_income_change_delta_2018) + \
        ((echo + antialpha_half) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_half) * gdf.market_rate_units_per_cap_change_delta_2018) + \
        ((golf + antialpha_half) * gdf.median_tenancy_change_delta_2018) + \
        ((hotel + antialpha_half) * gdf.median_housing_age_change_delta_2018)
)

#MAP VERSIONS
#combo
df_combo['omega13df_a0b1c1d1e1f1g1'] = (
        (alpha_half * df_combo.white_pop_pct_2013z.fillna(0)) + \
        ((bravo + antialpha_half) * df_combo.rent_25th_pctile_2013z.fillna(0)) + \
        ((charlie + antialpha_half) * df_combo.totpop_2013z.fillna(0)) + \
        ((delta + antialpha_half) * df_combo.rent_pct_income_2013z.fillna(0)) + \
        ((echo + antialpha_half) * df_combo.monthly_housing_cost_2013z.fillna(0)) + \
        ((foxtrot + antialpha_half) * df_combo.market_rate_units_per_cap_2013z.fillna(0)) + \
        ((golf + antialpha_half) * df_combo.median_tenancy_2013z.fillna(0))
)

df_combo['omega18df_a0b1c1d1e1f1g1'] = (
        (alpha_half * df_combo.white_pop_pct_2018z.fillna(0)) + \
        ((bravo + antialpha_half) * df_combo.rent_25th_pctile_2018z.fillna(0)) + \
        ((charlie + antialpha_half) * df_combo.totpop_2018z.fillna(0)) + \
        ((delta + antialpha_half) * df_combo.rent_pct_income_2018z.fillna(0)) + \
        ((echo + antialpha_half) * df_combo.monthly_housing_cost_2018z.fillna(0)) + \
        ((foxtrot + antialpha_half) * df_combo.market_rate_units_per_cap_2018z.fillna(0)) + \
        ((golf + antialpha_half) * df_combo.median_tenancy_2018z.fillna(0))
)
df_combo['omegadf_a0b1c1d1e1f1g1'] = df_combo.omega18df_a0b1c1d1e1f1g1 - df_combo.omega13df_a0b1c1d1e1f1g1

#PLOT
node_list = list(set(df_combo['GEOID']))
#G = nx.Graph()
G2018_a1b1c1d1e1f1g1 = nx.Graph()
G2018_a5b1c1d1e1f1g1 = nx.Graph()
G2018_a0b1c1d1e1f1g1 = nx.Graph()


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
    G2018_a1b1c1d1e1f1g1.add_node(i)
    G2018_a5b1c1d1e1f1g1.add_node(i)
    G2018_a0b1c1d1e1f1g1.add_node(i)

#Build the Edge list for the network graph for 2013
for i, row in gdf_combo.iterrows():
#    G.add_weighted_edges_from([(row['GEOID_a'],row['GEOID_b'],row['omega13'])])
    G2018_a1b1c1d1e1f1g1.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_a1b1c1d1e1f1g1'])])
    G2018_a5b1c1d1e1f1g1.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_a5b1c1d1e1f1g1'])])
    G2018_a0b1c1d1e1f1g1.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_a0b1c1d1e1f1g1'])])
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

pos2018_a1b1c1d1e1f1g1 = forceatlas2.forceatlas2_networkx_layout(G2018_a1b1c1d1e1f1g1,pos=None, iterations=1000)

for n, p in pos2018_a1b1c1d1e1f1g1.items():
    G2018_a1b1c1d1e1f1g1.nodes[n]['pos2018_a1b1c1d1e1f1g1'] = p

pos2018_a5b1c1d1e1f1g1 = forceatlas2.forceatlas2_networkx_layout(G2018_a5b1c1d1e1f1g1,pos=None, iterations=1000)

for n, p in pos2018_a5b1c1d1e1f1g1.items():
    G2018_a5b1c1d1e1f1g1.nodes[n]['pos2018_a5b1c1d1e1f1g1'] = p

pos2018_a0b1c1d1e1f1g1 = forceatlas2.forceatlas2_networkx_layout(G2018_a0b1c1d1e1f1g1,pos=None, iterations=1000)

for n, p in pos2018_a0b1c1d1e1f1g1.items():
    G2018_a0b1c1d1e1f1g1.nodes[n]['pos2018_a0b1c1d1e1f1g1'] = p

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

edge_trace2018_a5b1c1d1e1f1g1 = go.Scatter(
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

#for edge in G.edges():
#    x0, y0 = G.nodes[edge[0]]['pos']
#    x1, y1 = G.nodes[edge[1]]['pos']
#    edge_trace['x'] += tuple([x0, x1, None])
#    edge_trace['y'] += tuple([y0, y1, None])


for edge in G2018_a1b1c1d1e1f1g1.edges():
    x0, y0 = G2018_a1b1c1d1e1f1g1.nodes[edge[0]]['pos2018_a1b1c1d1e1f1g1']
    x1, y1 = G2018_a1b1c1d1e1f1g1.nodes[edge[1]]['pos2018_a1b1c1d1e1f1g1']
    edge_trace2018_a1b1c1d1e1f1g1['x'] += tuple([x0, x1, None])
    edge_trace2018_a1b1c1d1e1f1g1['y'] += tuple([y0, y1, None])

for edge in G2018_a5b1c1d1e1f1g1.edges():
    x0, y0 = G2018_a5b1c1d1e1f1g1.nodes[edge[0]]['pos2018_a5b1c1d1e1f1g1']
    x1, y1 = G2018_a5b1c1d1e1f1g1.nodes[edge[1]]['pos2018_a5b1c1d1e1f1g1']
    edge_trace2018_a5b1c1d1e1f1g1['x'] += tuple([x0, x1, None])
    edge_trace2018_a5b1c1d1e1f1g1['y'] += tuple([y0, y1, None])

for edge in G2018_a0b1c1d1e1f1g1.edges():
    x0, y0 = G2018_a0b1c1d1e1f1g1.nodes[edge[0]]['pos2018_a0b1c1d1e1f1g1']
    x1, y1 = G2018_a0b1c1d1e1f1g1.nodes[edge[1]]['pos2018_a0b1c1d1e1f1g1']
    edge_trace2018_a0b1c1d1e1f1g1['x'] += tuple([x0, x1, None])
    edge_trace2018_a0b1c1d1e1f1g1['y'] += tuple([y0, y1, None])

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

#for node in G.nodes():
#    x, y = G.nodes[node]['pos']
#    node_trace['x'] += tuple([x])
#    node_trace['y'] += tuple([y])


for node in G2018_a1b1c1d1e1f1g1.nodes():
    x, y = G2018_a1b1c1d1e1f1g1.nodes[node]['pos2018_a1b1c1d1e1f1g1']
    node_trace2018_a1b1c1d1e1f1g1['x'] += tuple([x])
    node_trace2018_a1b1c1d1e1f1g1['y'] += tuple([y])

for node in G2018_a5b1c1d1e1f1g1.nodes():
    x, y = G2018_a5b1c1d1e1f1g1.nodes[node]['pos2018_a5b1c1d1e1f1g1']
    node_trace2018_a5b1c1d1e1f1g1['x'] += tuple([x])
    node_trace2018_a5b1c1d1e1f1g1['y'] += tuple([y])

for node in G2018_a0b1c1d1e1f1g1.nodes():
    x, y = G2018_a0b1c1d1e1f1g1.nodes[node]['pos2018_a0b1c1d1e1f1g1']
    node_trace2018_a0b1c1d1e1f1g1['x'] += tuple([x])
    node_trace2018_a0b1c1d1e1f1g1['y'] += tuple([y])

#node_adjacencies = []
node_adjacencies2018_a1b1c1d1e1f1g1 = []
node_adjacencies2018_a5b1c1d1e1f1g1 = []
node_adjacencies2018_a0b1c1d1e1f1g1 = []

#for node, adjacencies in enumerate(G.adjacency()):
#    node_adjacencies.append(len(adjacencies[1]))


for node, adjacencies in enumerate(G2018_a1b1c1d1e1f1g1.adjacency()):
    node_adjacencies2018_a1b1c1d1e1f1g1.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018_a5b1c1d1e1f1g1.adjacency()):
    node_adjacencies2018_a5b1c1d1e1f1g1.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018_a0b1c1d1e1f1g1.adjacency()):
    node_adjacencies2018_a0b1c1d1e1f1g1.append(len(adjacencies[1]))

#for node in G.nodes():
#    node_label = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version


for node in G2018_a1b1c1d1e1f1g1.nodes():
    node_label2018_a1b1c1d1e1f1g1 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

for node in G2018_a5b1c1d1e1f1g1.nodes():
    node_label2018_a5b1c1d1e1f1g1 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

for node in G2018_a0b1c1d1e1f1g1.nodes():
    node_label2018_a0b1c1d1e1f1g1 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"]  #tract version

df_combo['tract_index'] = df_combo['TRACT_NUM'].astype(int)

#node_trace.marker.color = df_combo['tract_index']
#node_trace.marker.size = node_adjacencies
#node_trace.text = node_label

colorsIndex = {'wallingford':'#ef553b','rainier_beach':'#636efa'}  #manually assign colors
colors = df_combo['neighborhood'].map(colorsIndex)
node_trace2018_a1b1c1d1e1f1g1.marker.color = colors
node_trace2018_a5b1c1d1e1f1g1.marker.color = colors
node_trace2018_a0b1c1d1e1f1g1.marker.color = colors
#node_trace2018.marker.color = df_combo['neighborhood_index'].astype(int)
node_trace2018_a1b1c1d1e1f1g1.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_a1b1c1d1e1f1g1.text = node_label2018_a1b1c1d1e1f1g1
node_trace2018_a5b1c1d1e1f1g1.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_a5b1c1d1e1f1g1.text = node_label2018_a5b1c1d1e1f1g1
node_trace2018_a0b1c1d1e1f1g1.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018_a0b1c1d1e1f1g1.text = node_label2018_a0b1c1d1e1f1g1

def get_nodes(subset='a1b1c1d1e1f1g1'):
    subsets = {
        'a1b1c1d1e1f1g1': node_trace2018_a1b1c1d1e1f1g1,
        'a5b1c1d1e1f1g1': node_trace2018_a5b1c1d1e1f1g1,
        'a0b1c1d1e1f1g1': node_trace2018_a0b1c1d1e1f1g1
    }

    if subset in subsets:
        return subsets[subset]
    else:
        raise('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))


def get_edges(subset='a1b1c1d1e1f1g1'):
    subsets = {
        'a1b1c1d1e1f1g1': edge_trace2018_a1b1c1d1e1f1g1,
        'a5b1c1d1e1f1g1': edge_trace2018_a5b1c1d1e1f1g1,
        'a0b1c1d1e1f1g1': edge_trace2018_a0b1c1d1e1f1g1
    }

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
