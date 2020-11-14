import networkx as nx
from networkx.readwrite import json_graph
from fa2 import ForceAtlas2
import pandas as pd
from flask_caching import Cache
import plotly.graph_objects as go
import json
import csv
import itertools

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

one = 1 / 7.0
half = .5 / 7.0
zero = 0 / 7.0
antione = ((1 / 7) - one)/6
antihalf = ((1 / 7) - half)/6
antizero = ((1 / 7) - zero)/6

weight_keys = {
    'alpha_1': one,
    'alpha_5' : half,
    'alpha_0' : zero,
    'antialpha_1': antione,
    'antialpha_5': antihalf,
    'antialpha_0': antizero,
    'bravo_1': one,
    'bravo_5' : half,
    'bravo_0' : zero,
    'antibravo_1': antione,
    'antibravo_5': antihalf,
    'antibravo_0': antizero,
    'charlie_1': one,
    'charlie_5' : half,
    'charlie_0' : zero,
    'anticharlie_1': antione,
    'anticharlie_5': antihalf,
    'anticharlie_0': antizero,
    'delta_1': one,
    'delta_5' : half,
    'delta_0' : zero,
    'antidelta_1': antione,
    'antidelta_5': antihalf,
    'antidelta_0': antizero,
    'echo_1': one,
    'echo_5' : half,
    'echo_0' : zero,
    'antiecho_1': antione,
    'antiecho_5': antihalf,
    'antiecho_0': antizero,
    'foxtrot_1': one,
    'foxtrot_5' : half,
    'foxtrot_0' : zero,
    'antifoxtrot_1': antione,
    'antifoxtrot_5': antihalf,
    'antifoxtrot_0': antizero,
    'golf_1': one,
    'golf_5' : half,
    'golf_0' : zero,
    'antigolf_1': antione,
    'antigolf_5': antihalf,
    'antigolf_0': antizero
}

slider_names = ('alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot','golf')
slider_values_list = [dict(zip(slider_names, p)) for p in itertools.product([0,1,5], repeat=len(slider_names))]

#TODO need to find some way to loop over a conditional, where if the value for alpha in slider_values_list is 0, then pick alpha_0 from weights_list.
#Should create a dict that has each luggage code associated with 12 other values: the correct weights (and antiweights)
#could probably get a way with a 1 + 6 structure and just pull the antiweight from that.

def leppard(slider_values):
    luggage_code = 'a{alpha}b{bravo}c{charlie}d{delta}e{echo}f{foxtrot}g{golf}'.format(**slider_values)
    return luggage_code

slider_keys = [leppard(slider_values) for slider_values in slider_values_list]

# NETWORK VERSIONS
# 2013 + change version
gdf_combo['omega_a1b1c1d1e1f1g1'] = 1 / (
        ((alpha_one + antibravo_one) * gdf.white_pop_pct_change_delta) + \
        ((bravo_one + antialpha_one) * gdf.rent_25th_pctile_change_delta) + \
        ((charlie + antialpha_one + antibravo_one) * gdf.totpop_change_delta) + \
        ((delta + antialpha_one + antibravo_one) * gdf.rent_pct_income_change_delta) + \
        ((echo + antialpha_one + antibravo_one) * gdf.monthly_housing_cost_change_delta) + \
        ((foxtrot + antialpha_one + antibravo_one) * gdf.market_rate_units_per_cap_change_delta) + \
        ((golf + antialpha_one + antibravo_one) * gdf.median_tenancy_change_delta) + \
        ((hotel + antialpha_one + antibravo_one) * gdf.median_housing_age_change_delta)
)
antibravo_half = (1 / 7 - bravo_half)
gdf_combo['omega_a1b5c1d1e1f1g1'] = 1 / (
        ((alpha_one + antibravo_half) * gdf.white_pop_pct_change_delta) + \
        ((bravo_half + antialpha_one) * gdf.rent_25th_pctile_change_delta) + \
        ((charlie + antialpha_one + antibravo_half) * gdf.totpop_change_delta) + \
        ((delta + antialpha_one + antibravo_half) * gdf.rent_pct_income_change_delta) + \
        ((echo + antialpha_one + antibravo_half) * gdf.monthly_housing_cost_change_delta) + \
        ((foxtrot + antialpha_one + antibravo_half) * gdf.market_rate_units_per_cap_change_delta) + \
        ((golf + antialpha_one + antibravo_half) * gdf.median_tenancy_change_delta) + \
        ((hotel + antialpha_one + antibravo_half) * gdf.median_housing_age_change_delta)
)
antibravo_zero = (1 / 7 - bravo_zero)
gdf_combo['omega_a1b0c1d1e1f1g1'] = 1 / (
        ((alpha_one + antibravo_zero) * gdf.white_pop_pct_change_delta) + \
        ((bravo_zero + antialpha_one) * gdf.rent_25th_pctile_change_delta) + \
        ((charlie + antialpha_one + antibravo_zero) * gdf.totpop_change_delta) + \
        ((delta + antialpha_one + antibravo_zero) * gdf.rent_pct_income_change_delta) + \
        ((echo + antialpha_one + antibravo_zero) * gdf.monthly_housing_cost_change_delta) + \
        ((foxtrot + antialpha_one + antibravo_zero) * gdf.market_rate_units_per_cap_change_delta) + \
        ((golf + antialpha_one + antibravo_zero) * gdf.median_tenancy_change_delta) + \
        ((hotel + antialpha_one + antibravo_zero) * gdf.median_housing_age_change_delta)
)

# 2013 only version
gdf_combo['omega13_a1b1c1d1e1f1g1'] = 1 / (
        ((alpha_one + antibravo_one) * gdf.white_pop_pct_change_delta_2013) + \
        ((bravo_one + antialpha_one) * gdf.rent_25th_pctile_change_delta_2013) + \
        ((charlie + antialpha_one + antibravo_one) * gdf.totpop_change_delta_2013) + \
        ((delta + antialpha_one + antibravo_one) * gdf.rent_pct_income_change_delta_2013) + \
        ((echo + antialpha_one + antibravo_one) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_one + antibravo_one) * gdf.market_rate_units_per_cap_change_delta_2013) + \
        ((golf + antialpha_one + antibravo_one) * gdf.median_tenancy_change_delta_2013) + \
        ((hotel + antialpha_one + antibravo_one) * gdf.median_housing_age_change_delta_2013)
)
gdf_combo['omega13_a1b5c1d1e1f1g1'] = 1 / (
        ((alpha_one + antibravo_half) * gdf.white_pop_pct_change_delta_2013) + \
        ((bravo_half + antialpha_one) * gdf.rent_25th_pctile_change_delta_2013) + \
        ((charlie + antialpha_one + antibravo_half) * gdf.totpop_change_delta_2013) + \
        ((delta + antialpha_one + antibravo_half) * gdf.rent_pct_income_change_delta_2013) + \
        ((echo + antialpha_one + antibravo_half) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_one + antibravo_half) * gdf.market_rate_units_per_cap_change_delta_2013) + \
        ((golf + antialpha_one + antibravo_half) * gdf.median_tenancy_change_delta_2013) + \
        ((hotel + antialpha_one + antibravo_half) * gdf.median_housing_age_change_delta_2013)
)
gdf_combo['omega13_a1b0c1d1e1f1g1'] = 1 / (
        ((alpha_one + antibravo_zero) * gdf.white_pop_pct_change_delta_2013) + \
        ((bravo_zero + antialpha_one) * gdf.rent_25th_pctile_change_delta_2013) + \
        ((charlie + antialpha_one + antibravo_zero) * gdf.totpop_change_delta_2013) + \
        ((delta + antialpha_one + antibravo_zero) * gdf.rent_pct_income_change_delta_2013) + \
        ((echo + antialpha_one + antibravo_zero) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_one + antibravo_zero) * gdf.market_rate_units_per_cap_change_delta_2013) + \
        ((golf + antialpha_one + antibravo_zero) * gdf.median_tenancy_change_delta_2013) + \
        ((hotel + antialpha_one + antibravo_zero) * gdf.median_housing_age_change_delta_2013)
)

# 2018 only version
gdf_combo['omega18_a1b1c1d1e1f1g1'] = 1 / (
        ((alpha_one + antibravo_one) * gdf.white_pop_pct_change_delta_2018) + \
        ((bravo_half + antialpha_one) * gdf.rent_25th_pctile_change_delta_2018) + \
        ((charlie + antialpha_one + antibravo_one) * gdf.totpop_change_delta_2018) + \
        ((delta + antialpha_one + antibravo_one) * gdf.rent_pct_income_change_delta_2018) + \
        ((echo + antialpha_one + antibravo_one) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_one + antibravo_one) * gdf.market_rate_units_per_cap_change_delta_2018) + \
        ((golf + antialpha_one + antibravo_one) * gdf.median_tenancy_change_delta_2018) + \
        ((hotel + antialpha_one + antibravo_one) * gdf.median_housing_age_change_delta_2018)
)
gdf_combo['omega18_a1b5c1d1e1f1g1'] = 1 / (
        ((alpha_one + antibravo_half) * gdf.white_pop_pct_change_delta_2018) + \
        ((bravo_half + antialpha_one) * gdf.rent_25th_pctile_change_delta_2018) + \
        ((charlie + antialpha_one + antibravo_half) * gdf.totpop_change_delta_2018) + \
        ((delta + antialpha_one + antibravo_half) * gdf.rent_pct_income_change_delta_2018) + \
        ((echo + antialpha_one + antibravo_half) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_one + antibravo_half) * gdf.market_rate_units_per_cap_change_delta_2018) + \
        ((golf + antialpha_one + antibravo_half) * gdf.median_tenancy_change_delta_2018) + \
        ((hotel + antialpha_one + antibravo_half) * gdf.median_housing_age_change_delta_2018)
)
gdf_combo['omega18_a1b0c1d1e1f1g1'] = 1 / (
        ((alpha_one + antibravo_zero) * gdf.white_pop_pct_change_delta_2018) + \
        ((bravo_zero + antialpha_one) * gdf.rent_25th_pctile_change_delta_2018) + \
        ((charlie + antialpha_one + antibravo_zero) * gdf.totpop_change_delta_2018) + \
        ((delta + antialpha_one + antibravo_zero) * gdf.rent_pct_income_change_delta_2018) + \
        ((echo + antialpha_one + antibravo_zero) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_one + antibravo_zero) * gdf.market_rate_units_per_cap_change_delta_2018) + \
        ((golf + antialpha_one + antibravo_zero) * gdf.median_tenancy_change_delta_2018) + \
        ((hotel + antialpha_one + antibravo_zero) * gdf.median_housing_age_change_delta_2018)
)

# MAP VERSIONS
# combo
df_combo['omega13df_a1b1c1d1e1f1g1'] = (
        ((alpha_one + antibravo_one) * df_combo.white_pop_pct_2013z.fillna(0)) + \
        ((bravo_one + antialpha_one) * df_combo.rent_25th_pctile_2013z.fillna(0)) + \
        ((charlie + antialpha_one + antibravo_one) * df_combo.totpop_2013z.fillna(0)) + \
        ((delta + antialpha_one + antibravo_one) * df_combo.rent_pct_income_2013z.fillna(0)) + \
        ((echo + antialpha_one + antibravo_one) * df_combo.monthly_housing_cost_2013z.fillna(0)) + \
        ((foxtrot + antialpha_one + antibravo_one) * df_combo.market_rate_units_per_cap_2013z.fillna(0)) + \
        ((golf + antialpha_one + antibravo_one) * df_combo.median_tenancy_2013z.fillna(0))
)
df_combo['omega13df_a1b5c1d1e1f1g1'] = (
        ((alpha_one + antibravo_half) * df_combo.white_pop_pct_2013z.fillna(0)) + \
        ((bravo_half + antialpha_one) * df_combo.rent_25th_pctile_2013z.fillna(0)) + \
        ((charlie + antialpha_one + antibravo_half) * df_combo.totpop_2013z.fillna(0)) + \
        ((delta + antialpha_one + antibravo_half) * df_combo.rent_pct_income_2013z.fillna(0)) + \
        ((echo + antialpha_one + antibravo_half) * df_combo.monthly_housing_cost_2013z.fillna(0)) + \
        ((foxtrot + antialpha_one + antibravo_half) * df_combo.market_rate_units_per_cap_2013z.fillna(0)) + \
        ((golf + antialpha_one + antibravo_half) * df_combo.median_tenancy_2013z.fillna(0))
)
df_combo['omega13df_a1b0c1d1e1f1g1'] = (
        ((alpha_one + antibravo_zero) * df_combo.white_pop_pct_2013z.fillna(0)) + \
        ((bravo_zero + antialpha_one) * df_combo.rent_25th_pctile_2013z.fillna(0)) + \
        ((charlie + antialpha_one + antibravo_zero) * df_combo.totpop_2013z.fillna(0)) + \
        ((delta + antialpha_one + antibravo_zero) * df_combo.rent_pct_income_2013z.fillna(0)) + \
        ((echo + antialpha_one + antibravo_zero) * df_combo.monthly_housing_cost_2013z.fillna(0)) + \
        ((foxtrot + antialpha_one + antibravo_zero) * df_combo.market_rate_units_per_cap_2013z.fillna(0)) + \
        ((golf + antialpha_one + antibravo_zero) * df_combo.median_tenancy_2013z.fillna(0))
)

df_combo['omega18df_a1b1c1d1e1f1g1'] = (
        ((alpha_one + antibravo_one) * df_combo.white_pop_pct_2018z.fillna(0)) + \
        ((bravo + antialpha_one + antibravo_one) * df_combo.rent_25th_pctile_2018z.fillna(0)) + \
        ((charlie + antialpha_one + antibravo_one) * df_combo.totpop_2018z.fillna(0)) + \
        ((delta + antialpha_one + antibravo_one) * df_combo.rent_pct_income_2018z.fillna(0)) + \
        ((echo + antialpha_one + antibravo_one) * df_combo.monthly_housing_cost_2018z.fillna(0)) + \
        ((foxtrot + antialpha_one + antibravo_one) * df_combo.market_rate_units_per_cap_2018z.fillna(0)) + \
        ((golf + antialpha_one + antibravo_one) * df_combo.median_tenancy_2018z.fillna(0))
)
df_combo['omega18df_a1b5c1d1e1f1g1'] = (
        ((alpha_one + antibravo_half) * df_combo.white_pop_pct_2018z.fillna(0)) + \
        ((bravo + antialpha_one + antibravo_half) * df_combo.rent_25th_pctile_2018z.fillna(0)) + \
        ((charlie + antialpha_one + antibravo_half) * df_combo.totpop_2018z.fillna(0)) + \
        ((delta + antialpha_one + antibravo_half) * df_combo.rent_pct_income_2018z.fillna(0)) + \
        ((echo + antialpha_one + antibravo_half) * df_combo.monthly_housing_cost_2018z.fillna(0)) + \
        ((foxtrot + antialpha_one + antibravo_half) * df_combo.market_rate_units_per_cap_2018z.fillna(0)) + \
        ((golf + antialpha_one + antibravo_half) * df_combo.median_tenancy_2018z.fillna(0))
)
df_combo['omega18df_a1b0c1d1e1f1g1'] = (
        ((alpha_one + antibravo_zero) * df_combo.white_pop_pct_2018z.fillna(0)) + \
        ((bravo + antialpha_one + antibravo_zero) * df_combo.rent_25th_pctile_2018z.fillna(0)) + \
        ((charlie + antialpha_one + antibravo_zero) * df_combo.totpop_2018z.fillna(0)) + \
        ((delta + antialpha_one + antibravo_zero) * df_combo.rent_pct_income_2018z.fillna(0)) + \
        ((echo + antialpha_one + antibravo_zero) * df_combo.monthly_housing_cost_2018z.fillna(0)) + \
        ((foxtrot + antialpha_one + antibravo_zero) * df_combo.market_rate_units_per_cap_2018z.fillna(0)) + \
        ((golf + antialpha_one + antibravo_zero) * df_combo.median_tenancy_2018z.fillna(0))
)
df_combo['omegadf_a1b1c1d1e1f1g1'] = df_combo.omega18df_a1b1c1d1e1f1g1 - df_combo.omega13df_a1b1c1d1e1f1g1
df_combo['omegadf_a1b5c1d1e1f1g1'] = df_combo.omega18df_a1b5c1d1e1f1g1 - df_combo.omega13df_a1b5c1d1e1f1g1
df_combo['omegadf_a1b0c1d1e1f1g1'] = df_combo.omega18df_a1b0c1d1e1f1g1 - df_combo.omega13df_a1b0c1d1e1f1g1

antialpha_half = (1 / 7 - alpha_half)
gdf_combo['omega_a5b1c1d1e1f1g1'] = 1 / (
        ((alpha_half + antibravo_one) * gdf.white_pop_pct_change_delta) + \
        ((bravo_one + antialpha_half) * gdf.rent_25th_pctile_change_delta) + \
        ((charlie + antialpha_half + antibravo_one) * gdf.totpop_change_delta) + \
        ((delta + antialpha_half + antibravo_one) * gdf.rent_pct_income_change_delta) + \
        ((echo + antialpha_half + antibravo_one) * gdf.monthly_housing_cost_change_delta) + \
        ((foxtrot + antialpha_half + antibravo_one) * gdf.market_rate_units_per_cap_change_delta) + \
        ((golf + antialpha_half + antibravo_one) * gdf.median_tenancy_change_delta) + \
        ((hotel + antialpha_half + antibravo_one) * gdf.median_housing_age_change_delta)
)
gdf_combo['omega_a5b5c1d1e1f1g1'] = 1 / (
        ((alpha_half + antibravo_half) * gdf.white_pop_pct_change_delta) + \
        ((bravo_half + antialpha_half) * gdf.rent_25th_pctile_change_delta) + \
        ((charlie + antialpha_half + antibravo_half) * gdf.totpop_change_delta) + \
        ((delta + antialpha_half + antibravo_half) * gdf.rent_pct_income_change_delta) + \
        ((echo + antialpha_half + antibravo_half) * gdf.monthly_housing_cost_change_delta) + \
        ((foxtrot + antialpha_half + antibravo_half) * gdf.market_rate_units_per_cap_change_delta) + \
        ((golf + antialpha_half + antibravo_half) * gdf.median_tenancy_change_delta) + \
        ((hotel + antialpha_half + antibravo_half) * gdf.median_housing_age_change_delta)
)
gdf_combo['omega_a5b0c1d1e1f1g1'] = 1 / (
        ((alpha_half + antibravo_zero) * gdf.white_pop_pct_change_delta) + \
        ((bravo_zero + antialpha_half) * gdf.rent_25th_pctile_change_delta) + \
        ((charlie + antialpha_half + antibravo_zero) * gdf.totpop_change_delta) + \
        ((delta + antialpha_half + antibravo_zero) * gdf.rent_pct_income_change_delta) + \
        ((echo + antialpha_half + antibravo_zero) * gdf.monthly_housing_cost_change_delta) + \
        ((foxtrot + antialpha_half + antibravo_zero) * gdf.market_rate_units_per_cap_change_delta) + \
        ((golf + antialpha_half + antibravo_zero) * gdf.median_tenancy_change_delta) + \
        ((hotel + antialpha_half + antibravo_zero) * gdf.median_housing_age_change_delta)
)

# 2013 only version
gdf_combo['omega13_a5b1c1d1e1f1g1'] = 1 / (
        ((alpha_half + antibravo_one) * gdf.white_pop_pct_change_delta_2013) + \
        ((bravo_one + antialpha_half) * gdf.rent_25th_pctile_change_delta_2013) + \
        ((charlie + antialpha_half + antibravo_one) * gdf.totpop_change_delta_2013) + \
        ((delta + antialpha_half + antibravo_one) * gdf.rent_pct_income_change_delta_2013) + \
        ((echo + antialpha_half + antibravo_one) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_half + antibravo_one) * gdf.market_rate_units_per_cap_change_delta_2013) + \
        ((golf + antialpha_half + antibravo_one) * gdf.median_tenancy_change_delta_2013) + \
        ((hotel + antialpha_half + antibravo_one) * gdf.median_housing_age_change_delta_2013)
)
gdf_combo['omega13_a5b1c1d1e1f1g1'] = 1 / (
        ((alpha_half + antibravo_half) * gdf.white_pop_pct_change_delta_2013) + \
        ((bravo_half + antialpha_half) * gdf.rent_25th_pctile_change_delta_2013) + \
        ((charlie + antialpha_half + antibravo_half) * gdf.totpop_change_delta_2013) + \
        ((delta + antialpha_half + antibravo_half) * gdf.rent_pct_income_change_delta_2013) + \
        ((echo + antialpha_half + antibravo_half) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_half + antibravo_half) * gdf.market_rate_units_per_cap_change_delta_2013) + \
        ((golf + antialpha_half + antibravo_half) * gdf.median_tenancy_change_delta_2013) + \
        ((hotel + antialpha_half + antibravo_half) * gdf.median_housing_age_change_delta_2013)
)
gdf_combo['omega13_a5b0c1d1e1f1g1'] = 1 / (
        ((alpha_half + antibravo_zero) * gdf.white_pop_pct_change_delta_2013) + \
        ((bravo_zero + antialpha_half) * gdf.rent_25th_pctile_change_delta_2013) + \
        ((charlie + antialpha_half + antibravo_zero) * gdf.totpop_change_delta_2013) + \
        ((delta + antialpha_half + antibravo_zero) * gdf.rent_pct_income_change_delta_2013) + \
        ((echo + antialpha_half + antibravo_zero) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_half + antibravo_zero) * gdf.market_rate_units_per_cap_change_delta_2013) + \
        ((golf + antialpha_half + antibravo_zero) * gdf.median_tenancy_change_delta_2013) + \
        ((hotel + antialpha_half + antibravo_zero) * gdf.median_housing_age_change_delta_2013)
)

# 2018 only version
gdf_combo['omega18_a5b1c1d1e1f1g1'] = 1 / (
        ((alpha_half + antibravo_one) * gdf.white_pop_pct_change_delta_2018) + \
        ((bravo_one + antialpha_half) * gdf.rent_25th_pctile_change_delta_2018) + \
        ((charlie + antialpha_half + antibravo_one) * gdf.totpop_change_delta_2018) + \
        ((delta + antialpha_half + antibravo_one) * gdf.rent_pct_income_change_delta_2018) + \
        ((echo + antialpha_half + antibravo_one) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_half + antibravo_one) * gdf.market_rate_units_per_cap_change_delta_2018) + \
        ((golf + antialpha_half + antibravo_one) * gdf.median_tenancy_change_delta_2018) + \
        ((hotel + antialpha_half + antibravo_one) * gdf.median_housing_age_change_delta_2018)
)
gdf_combo['omega18_a5b5c1d1e1f1g1'] = 1 / (
        ((alpha_half + antibravo_half) * gdf.white_pop_pct_change_delta_2018) + \
        ((bravo_half + antialpha_half) * gdf.rent_25th_pctile_change_delta_2018) + \
        ((charlie + antialpha_half + antibravo_half) * gdf.totpop_change_delta_2018) + \
        ((delta + antialpha_half + antibravo_half) * gdf.rent_pct_income_change_delta_2018) + \
        ((echo + antialpha_half + antibravo_half) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_half + antibravo_half) * gdf.market_rate_units_per_cap_change_delta_2018) + \
        ((golf + antialpha_half + antibravo_half) * gdf.median_tenancy_change_delta_2018) + \
        ((hotel + antialpha_half + antibravo_half) * gdf.median_housing_age_change_delta_2018)
)
gdf_combo['omega18_a5b0c1d1e1f1g1'] = 1 / (
        ((alpha_half + antibravo_zero) * gdf.white_pop_pct_change_delta_2018) + \
        ((bravo_zero + antialpha_half) * gdf.rent_25th_pctile_change_delta_2018) + \
        ((charlie + antialpha_half + antibravo_zero) * gdf.totpop_change_delta_2018) + \
        ((delta + antialpha_half + antibravo_zero) * gdf.rent_pct_income_change_delta_2018) + \
        ((echo + antialpha_half + antibravo_zero) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_half + antibravo_zero) * gdf.market_rate_units_per_cap_change_delta_2018) + \
        ((golf + antialpha_half + antibravo_zero) * gdf.median_tenancy_change_delta_2018) + \
        ((hotel + antialpha_half + antibravo_zero) * gdf.median_housing_age_change_delta_2018)
)
# MAP VERSIONS
# combo
df_combo['omega13df_a5b1c1d1e1f1g1'] = (
        ((alpha_half + antibravo_one) * df_combo.white_pop_pct_2013z.fillna(0)) + \
        ((bravo_one + antialpha_half) * df_combo.rent_25th_pctile_2013z.fillna(0)) + \
        ((charlie + antialpha_half + antibravo_one) * df_combo.totpop_2013z.fillna(0)) + \
        ((delta + antialpha_half + antibravo_one) * df_combo.rent_pct_income_2013z.fillna(0)) + \
        ((echo + antialpha_half + antibravo_one) * df_combo.monthly_housing_cost_2013z.fillna(0)) + \
        ((foxtrot + antialpha_half + antibravo_one) * df_combo.market_rate_units_per_cap_2013z.fillna(0)) + \
        ((golf + antialpha_half + antibravo_one) * df_combo.median_tenancy_2013z.fillna(0))
)
df_combo['omega13df_a5b5c1d1e1f1g1'] = (
        ((alpha_half + antibravo_half) * df_combo.white_pop_pct_2013z.fillna(0)) + \
        ((bravo_half + antialpha_half) * df_combo.rent_25th_pctile_2013z.fillna(0)) + \
        ((charlie + antialpha_half + antibravo_half) * df_combo.totpop_2013z.fillna(0)) + \
        ((delta + antialpha_half + antibravo_half) * df_combo.rent_pct_income_2013z.fillna(0)) + \
        ((echo + antialpha_half + antibravo_half) * df_combo.monthly_housing_cost_2013z.fillna(0)) + \
        ((foxtrot + antialpha_half + antibravo_half) * df_combo.market_rate_units_per_cap_2013z.fillna(0)) + \
        ((golf + antialpha_half + antibravo_half) * df_combo.median_tenancy_2013z.fillna(0))
)
df_combo['omega13df_a5b0c1d1e1f1g1'] = (
        ((alpha_half + antibravo_zero) * df_combo.white_pop_pct_2013z.fillna(0)) + \
        ((bravo_zero + antialpha_half) * df_combo.rent_25th_pctile_2013z.fillna(0)) + \
        ((charlie + antialpha_half + antibravo_zero) * df_combo.totpop_2013z.fillna(0)) + \
        ((delta + antialpha_half + antibravo_zero) * df_combo.rent_pct_income_2013z.fillna(0)) + \
        ((echo + antialpha_half + antibravo_zero) * df_combo.monthly_housing_cost_2013z.fillna(0)) + \
        ((foxtrot + antialpha_half + antibravo_zero) * df_combo.market_rate_units_per_cap_2013z.fillna(0)) + \
        ((golf + antialpha_half + antibravo_zero) * df_combo.median_tenancy_2013z.fillna(0))
)

df_combo['omega18df_a5b1c1d1e1f1g1'] = (
        ((alpha_half + antibravo_one) * df_combo.white_pop_pct_2018z.fillna(0)) + \
        ((bravo_one + antialpha_half) * df_combo.rent_25th_pctile_2018z.fillna(0)) + \
        ((charlie + antialpha_half + antibravo_one) * df_combo.totpop_2018z.fillna(0)) + \
        ((delta + antialpha_half + antibravo_one) * df_combo.rent_pct_income_2018z.fillna(0)) + \
        ((echo + antialpha_half + antibravo_one) * df_combo.monthly_housing_cost_2018z.fillna(0)) + \
        ((foxtrot + antialpha_half + antibravo_one) * df_combo.market_rate_units_per_cap_2018z.fillna(0)) + \
        ((golf + antialpha_half + antibravo_one) * df_combo.median_tenancy_2018z.fillna(0))
)

df_combo['omega18df_a5b5c1d1e1f1g1'] = (
        ((alpha_half + antibravo_half) * df_combo.white_pop_pct_2018z.fillna(0)) + \
        ((bravo_half + antialpha_half) * df_combo.rent_25th_pctile_2018z.fillna(0)) + \
        ((charlie + antialpha_half + antibravo_half) * df_combo.totpop_2018z.fillna(0)) + \
        ((delta + antialpha_half + antibravo_half) * df_combo.rent_pct_income_2018z.fillna(0)) + \
        ((echo + antialpha_half + antibravo_half) * df_combo.monthly_housing_cost_2018z.fillna(0)) + \
        ((foxtrot + antialpha_half + antibravo_half) * df_combo.market_rate_units_per_cap_2018z.fillna(0)) + \
        ((golf + antialpha_half + antibravo_half) * df_combo.median_tenancy_2018z.fillna(0))
)

df_combo['omega18df_a5b0c1d1e1f1g1'] = (
        ((alpha_half + antibravo_zero) * df_combo.white_pop_pct_2018z.fillna(0)) + \
        ((bravo_zero + antialpha_half) * df_combo.rent_25th_pctile_2018z.fillna(0)) + \
        ((charlie + antialpha_half + antibravo_zero) * df_combo.totpop_2018z.fillna(0)) + \
        ((delta + antialpha_half + antibravo_zero) * df_combo.rent_pct_income_2018z.fillna(0)) + \
        ((echo + antialpha_half + antibravo_zero) * df_combo.monthly_housing_cost_2018z.fillna(0)) + \
        ((foxtrot + antialpha_half + antibravo_zero) * df_combo.market_rate_units_per_cap_2018z.fillna(0)) + \
        ((golf + antialpha_half + antibravo_zero) * df_combo.median_tenancy_2018z.fillna(0))
)
df_combo['omegadf_a5b1c1d1e1f1g1'] = df_combo.omega18df_a5b1c1d1e1f1g1 - df_combo.omega13df_a5b1c1d1e1f1g1
df_combo['omegadf_a5b5c1d1e1f1g1'] = df_combo.omega18df_a5b5c1d1e1f1g1 - df_combo.omega13df_a5b5c1d1e1f1g1
df_combo['omegadf_a5b0c1d1e1f1g1'] = df_combo.omega18df_a5b0c1d1e1f1g1 - df_combo.omega13df_a5b0c1d1e1f1g1

antialpha_zero = (1 / 7 - alpha_zero)
gdf_combo['omega_a0b1c1d1e1f1g1'] = 1 / (
        ((alpha_zero + antibravo_one) * gdf.white_pop_pct_change_delta) + \
        ((bravo_one + antialpha_zero) * gdf.rent_25th_pctile_change_delta) + \
        ((charlie + antialpha_zero + antibravo_one) * gdf.totpop_change_delta) + \
        ((delta + antialpha_zero + antibravo_one) * gdf.rent_pct_income_change_delta) + \
        ((echo + antialpha_zero + antibravo_one) * gdf.monthly_housing_cost_change_delta) + \
        ((foxtrot + antialpha_zero + antibravo_one) * gdf.market_rate_units_per_cap_change_delta) + \
        ((golf + antialpha_zero + antibravo_one) * gdf.median_tenancy_change_delta) + \
        ((hotel + antialpha_zero + antibravo_one) * gdf.median_housing_age_change_delta)
)
gdf_combo['omega_a0b5c1d1e1f1g1'] = 1 / (
        ((alpha_zero + antibravo_half) * gdf.white_pop_pct_change_delta) + \
        ((bravo_half + antialpha_zero) * gdf.rent_25th_pctile_change_delta) + \
        ((charlie + antialpha_zero + antibravo_half) * gdf.totpop_change_delta) + \
        ((delta + antialpha_zero + antibravo_half) * gdf.rent_pct_income_change_delta) + \
        ((echo + antialpha_zero + antibravo_half) * gdf.monthly_housing_cost_change_delta) + \
        ((foxtrot + antialpha_zero + antibravo_half) * gdf.market_rate_units_per_cap_change_delta) + \
        ((golf + antialpha_zero + antibravo_half) * gdf.median_tenancy_change_delta) + \
        ((hotel + antialpha_zero + antibravo_half) * gdf.median_housing_age_change_delta)
)
gdf_combo['omega_a0b0c1d1e1f1g1'] = 1 / (
        ((alpha_zero + antibravo_zero) * gdf.white_pop_pct_change_delta) + \
        ((bravo_zero + antialpha_zero) * gdf.rent_25th_pctile_change_delta) + \
        ((charlie + antialpha_zero + antibravo_zero) * gdf.totpop_change_delta) + \
        ((delta + antialpha_zero + antibravo_zero) * gdf.rent_pct_income_change_delta) + \
        ((echo + antialpha_zero + antibravo_zero) * gdf.monthly_housing_cost_change_delta) + \
        ((foxtrot + antialpha_zero + antibravo_zero) * gdf.market_rate_units_per_cap_change_delta) + \
        ((golf + antialpha_zero + antibravo_zero) * gdf.median_tenancy_change_delta) + \
        ((hotel + antialpha_zero + antibravo_zero) * gdf.median_housing_age_change_delta)
)

# 2013 only version
gdf_combo['omega13_a0b1c1d1e1f1g1'] = 1 / (
        ((alpha_zero + antibravo_one) * gdf.white_pop_pct_change_delta_2013) + \
        ((bravo_one + antialpha_zero) * gdf.rent_25th_pctile_change_delta_2013) + \
        ((charlie + antialpha_zero + antibravo_one) * gdf.totpop_change_delta_2013) + \
        ((delta + antialpha_zero + antibravo_one) * gdf.rent_pct_income_change_delta_2013) + \
        ((echo + antialpha_zero + antibravo_one) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_zero + antibravo_one) * gdf.market_rate_units_per_cap_change_delta_2013) + \
        ((golf + antialpha_zero + antibravo_one) * gdf.median_tenancy_change_delta_2013) + \
        ((hotel + antialpha_zero + antibravo_one) * gdf.median_housing_age_change_delta_2013)
)
gdf_combo['omega13_a0b5c1d1e1f1g1'] = 1 / (
        ((alpha_zero + antibravo_half) * gdf.white_pop_pct_change_delta_2013) + \
        ((bravo_half + antialpha_zero) * gdf.rent_25th_pctile_change_delta_2013) + \
        ((charlie + antialpha_zero + antibravo_half) * gdf.totpop_change_delta_2013) + \
        ((delta + antialpha_zero + antibravo_half) * gdf.rent_pct_income_change_delta_2013) + \
        ((echo + antialpha_zero + antibravo_half) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_zero + antibravo_half) * gdf.market_rate_units_per_cap_change_delta_2013) + \
        ((golf + antialpha_zero + antibravo_half) * gdf.median_tenancy_change_delta_2013) + \
        ((hotel + antialpha_zero + antibravo_half) * gdf.median_housing_age_change_delta_2013)
)
gdf_combo['omega13_a0b0c1d1e1f1g1'] = 1 / (
        ((alpha_zero + antibravo_zero) * gdf.white_pop_pct_change_delta_2013) + \
        ((bravo_zero + antialpha_zero) * gdf.rent_25th_pctile_change_delta_2013) + \
        ((charlie + antialpha_zero + antibravo_zero) * gdf.totpop_change_delta_2013) + \
        ((delta + antialpha_zero + antibravo_zero) * gdf.rent_pct_income_change_delta_2013) + \
        ((echo + antialpha_zero + antibravo_zero) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_zero + antibravo_zero) * gdf.market_rate_units_per_cap_change_delta_2013) + \
        ((golf + antialpha_zero + antibravo_zero) * gdf.median_tenancy_change_delta_2013) + \
        ((hotel + antialpha_zero + antibravo_zero) * gdf.median_housing_age_change_delta_2013)
)

# 2018 only version
gdf_combo['omega18_a0b1c1d1e1f1g1'] = 1 / (
        ((alpha_zero + antibravo_one) * gdf.white_pop_pct_change_delta_2018) + \
        ((bravo_one + antialpha_zero) * gdf.rent_25th_pctile_change_delta_2018) + \
        ((charlie + antialpha_zero + antibravo_one) * gdf.totpop_change_delta_2018) + \
        ((delta + antialpha_zero + antibravo_one) * gdf.rent_pct_income_change_delta_2018) + \
        ((echo + antialpha_zero + antibravo_one) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_zero + antibravo_one) * gdf.market_rate_units_per_cap_change_delta_2018) + \
        ((golf + antialpha_zero + antibravo_one) * gdf.median_tenancy_change_delta_2018) + \
        ((hotel + antialpha_zero + antibravo_one) * gdf.median_housing_age_change_delta_2018)
)
gdf_combo['omega18_a0b5c1d1e1f1g1'] = 1 / (
        ((alpha_zero + antibravo_half) * gdf.white_pop_pct_change_delta_2018) + \
        ((bravo_half + antialpha_zero) * gdf.rent_25th_pctile_change_delta_2018) + \
        ((charlie + antialpha_zero + antibravo_half) * gdf.totpop_change_delta_2018) + \
        ((delta + antialpha_zero + antibravo_half) * gdf.rent_pct_income_change_delta_2018) + \
        ((echo + antialpha_zero + antibravo_half) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_zero + antibravo_half) * gdf.market_rate_units_per_cap_change_delta_2018) + \
        ((golf + antialpha_zero + antibravo_half) * gdf.median_tenancy_change_delta_2018) + \
        ((hotel + antialpha_zero + antibravo_half) * gdf.median_housing_age_change_delta_2018)
)
gdf_combo['omega18_a0b0c1d1e1f1g1'] = 1 / (
        ((alpha_zero + antibravo_zero) * gdf.white_pop_pct_change_delta_2018) + \
        ((bravo_zero + antialpha_zero) * gdf.rent_25th_pctile_change_delta_2018) + \
        ((charlie + antialpha_zero + antibravo_zero) * gdf.totpop_change_delta_2018) + \
        ((delta + antialpha_zero + antibravo_zero) * gdf.rent_pct_income_change_delta_2018) + \
        ((echo + antialpha_zero + antibravo_zero) * gdf.monthly_housing_cost_change_delta_2018) + \
        ((foxtrot + antialpha_zero + antibravo_zero) * gdf.market_rate_units_per_cap_change_delta_2018) + \
        ((golf + antialpha_zero + antibravo_zero) * gdf.median_tenancy_change_delta_2018) + \
        ((hotel + antialpha_zero + antibravo_zero) * gdf.median_housing_age_change_delta_2018)
)

# MAP VERSIONS
# combo
df_combo['omega13df_a0b1c1d1e1f1g1'] = (
        ((alpha_half + antibravo_one) * df_combo.white_pop_pct_2013z.fillna(0)) + \
        ((bravo_one + antialpha_zero) * df_combo.rent_25th_pctile_2013z.fillna(0)) + \
        ((charlie + antialpha_zero + antibravo_one) * df_combo.totpop_2013z.fillna(0)) + \
        ((delta + antialpha_zero + antibravo_one) * df_combo.rent_pct_income_2013z.fillna(0)) + \
        ((echo + antialpha_zero + antibravo_one) * df_combo.monthly_housing_cost_2013z.fillna(0)) + \
        ((foxtrot + antialpha_zero + antibravo_one) * df_combo.market_rate_units_per_cap_2013z.fillna(0)) + \
        ((golf + antialpha_zero + antibravo_one) * df_combo.median_tenancy_2013z.fillna(0))
)
df_combo['omega13df_a0b5c1d1e1f1g1'] = (
        ((alpha_half + antibravo_half) * df_combo.white_pop_pct_2013z.fillna(0)) + \
        ((bravo_half + antialpha_zero) * df_combo.rent_25th_pctile_2013z.fillna(0)) + \
        ((charlie + antialpha_zero + antibravo_half) * df_combo.totpop_2013z.fillna(0)) + \
        ((delta + antialpha_zero + antibravo_half) * df_combo.rent_pct_income_2013z.fillna(0)) + \
        ((echo + antialpha_zero + antibravo_half) * df_combo.monthly_housing_cost_2013z.fillna(0)) + \
        ((foxtrot + antialpha_zero + antibravo_half) * df_combo.market_rate_units_per_cap_2013z.fillna(0)) + \
        ((golf + antialpha_zero + antibravo_half) * df_combo.median_tenancy_2013z.fillna(0))
)
df_combo['omega13df_a0b0c1d1e1f1g1'] = (
        ((alpha_half + antibravo_zero) * df_combo.white_pop_pct_2013z.fillna(0)) + \
        ((bravo_zero + antialpha_zero) * df_combo.rent_25th_pctile_2013z.fillna(0)) + \
        ((charlie + antialpha_zero + antibravo_zero) * df_combo.totpop_2013z.fillna(0)) + \
        ((delta + antialpha_zero + antibravo_zero) * df_combo.rent_pct_income_2013z.fillna(0)) + \
        ((echo + antialpha_zero + antibravo_zero) * df_combo.monthly_housing_cost_2013z.fillna(0)) + \
        ((foxtrot + antialpha_zero + antibravo_zero) * df_combo.market_rate_units_per_cap_2013z.fillna(0)) + \
        ((golf + antialpha_zero + antibravo_zero) * df_combo.median_tenancy_2013z.fillna(0))
)

df_combo['omega18df_a0b1c1d1e1f1g1'] = (
        ((alpha_half + antibravo_one) * df_combo.white_pop_pct_2018z.fillna(0)) + \
        ((bravo_one + antialpha_zero) * df_combo.rent_25th_pctile_2018z.fillna(0)) + \
        ((charlie + antialpha_zero + antibravo_one) * df_combo.totpop_2018z.fillna(0)) + \
        ((delta + antialpha_zero + antibravo_one) * df_combo.rent_pct_income_2018z.fillna(0)) + \
        ((echo + antialpha_zero + antibravo_one) * df_combo.monthly_housing_cost_2018z.fillna(0)) + \
        ((foxtrot + antialpha_zero + antibravo_one) * df_combo.market_rate_units_per_cap_2018z.fillna(0)) + \
        ((golf + antialpha_zero + antibravo_one) * df_combo.median_tenancy_2018z.fillna(0))
)
df_combo['omega18df_a0b5c1d1e1f1g1'] = (
        ((alpha_half + antibravo_half) * df_combo.white_pop_pct_2018z.fillna(0)) + \
        ((bravo_half + antialpha_zero) * df_combo.rent_25th_pctile_2018z.fillna(0)) + \
        ((charlie + antialpha_zero + antibravo_half) * df_combo.totpop_2018z.fillna(0)) + \
        ((delta + antialpha_zero + antibravo_half) * df_combo.rent_pct_income_2018z.fillna(0)) + \
        ((echo + antialpha_zero + antibravo_half) * df_combo.monthly_housing_cost_2018z.fillna(0)) + \
        ((foxtrot + antialpha_zero + antibravo_half) * df_combo.market_rate_units_per_cap_2018z.fillna(0)) + \
        ((golf + antialpha_zero + antibravo_half) * df_combo.median_tenancy_2018z.fillna(0))
)
df_combo['omega18df_a0b0c1d1e1f1g1'] = (
        ((alpha_half + antibravo_zero) * df_combo.white_pop_pct_2018z.fillna(0)) + \
        ((bravo_zero + antialpha_zero) * df_combo.rent_25th_pctile_2018z.fillna(0)) + \
        ((charlie + antialpha_zero + antibravo_zero) * df_combo.totpop_2018z.fillna(0)) + \
        ((delta + antialpha_zero + antibravo_zero) * df_combo.rent_pct_income_2018z.fillna(0)) + \
        ((echo + antialpha_zero + antibravo_zero) * df_combo.monthly_housing_cost_2018z.fillna(0)) + \
        ((foxtrot + antialpha_zero + antibravo_zero) * df_combo.market_rate_units_per_cap_2018z.fillna(0)) + \
        ((golf + antialpha_zero + antibravo_zero) * df_combo.median_tenancy_2018z.fillna(0))
)
df_combo['omegadf_a0b1c1d1e1f1g1'] = df_combo.omega18df_a0b1c1d1e1f1g1 - df_combo.omega13df_a0b1c1d1e1f1g1
df_combo['omegadf_a0b5c1d1e1f1g1'] = df_combo.omega18df_a0b5c1d1e1f1g1 - df_combo.omega13df_a0b5c1d1e1f1g1
df_combo['omegadf_a0b0c1d1e1f1g1'] = df_combo.omega18df_a0b0c1d1e1f1g1 - df_combo.omega13df_a0b0c1d1e1f1g1

# PLOT
node_list = list(set(df_combo['GEOID']))
# G = nx.Graph()
G2018_a1b1c1d1e1f1g1 = nx.Graph()
G2018_a1b5c1d1e1f1g1 = nx.Graph()
G2018_a1b0c1d1e1f1g1 = nx.Graph()
G2018_a5b1c1d1e1f1g1 = nx.Graph()
G2018_a5b5c1d1e1f1g1 = nx.Graph()
G2018_a5b0c1d1e1f1g1 = nx.Graph()
G2018_a0b1c1d1e1f1g1 = nx.Graph()
G2018_a0b5c1d1e1f1g1 = nx.Graph()
G2018_a0b0c1d1e1f1g1 = nx.Graph()

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

for i in node_list:
    #    G.add_node(i)
    G2018_a1b1c1d1e1f1g1.add_node(i)
    G2018_a1b5c1d1e1f1g1.add_node(i)
    G2018_a1b0c1d1e1f1g1.add_node(i)
    G2018_a5b1c1d1e1f1g1.add_node(i)
    G2018_a5b5c1d1e1f1g1.add_node(i)
    G2018_a5b0c1d1e1f1g1.add_node(i)
    G2018_a0b1c1d1e1f1g1.add_node(i)
    G2018_a0b5c1d1e1f1g1.add_node(i)
    G2018_a0b0c1d1e1f1g1.add_node(i)

# Build the Edge list for the network graph for 2013
for i, row in gdf_combo.iterrows():
    #    G.add_weighted_edges_from([(row['GEOID_a'],row['GEOID_b'],row['omega13'])])
    G2018_a1b1c1d1e1f1g1.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_a1b1c1d1e1f1g1'])])
    G2018_a1b5c1d1e1f1g1.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_a1b5c1d1e1f1g1'])])
    G2018_a1b0c1d1e1f1g1.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_a1b0c1d1e1f1g1'])])
    G2018_a5b1c1d1e1f1g1.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_a5b1c1d1e1f1g1'])])
    G2018_a5b5c1d1e1f1g1.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_a5b5c1d1e1f1g1'])])
    G2018_a5b0c1d1e1f1g1.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_a5b0c1d1e1f1g1'])])
    G2018_a0b1c1d1e1f1g1.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_a0b1c1d1e1f1g1'])])
    G2018_a0b5c1d1e1f1g1.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_a0b5c1d1e1f1g1'])])
    G2018_a0b0c1d1e1f1g1.add_weighted_edges_from([(row['GEOID_a'], row['GEOID_b'], row['omega18_a0b0c1d1e1f1g1'])])
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
# NON-CACHE-USING VERSION
# pos = forceatlas2.forceatlas2_networkx_layout(G,pos=None, iterations=1000)

# for n, p in pos.items():
#    G.nodes[n]['pos'] = p

pos2018_a1b1c1d1e1f1g1 = forceatlas2.forceatlas2_networkx_layout(G2018_a1b1c1d1e1f1g1, pos=None, iterations=1000)

for n, p in pos2018_a1b1c1d1e1f1g1.items():
    G2018_a1b1c1d1e1f1g1.nodes[n]['pos2018_a1b1c1d1e1f1g1'] = p

pos2018_a1b5c1d1e1f1g1 = forceatlas2.forceatlas2_networkx_layout(G2018_a1b5c1d1e1f1g1, pos=None, iterations=1000)

for n, p in pos2018_a1b5c1d1e1f1g1.items():
    G2018_a1b5c1d1e1f1g1.nodes[n]['pos2018_a1b5c1d1e1f1g1'] = p

pos2018_a1b0c1d1e1f1g1 = forceatlas2.forceatlas2_networkx_layout(G2018_a1b0c1d1e1f1g1, pos=None, iterations=1000)

for n, p in pos2018_a1b0c1d1e1f1g1.items():
    G2018_a1b0c1d1e1f1g1.nodes[n]['pos2018_a1b0c1d1e1f1g1'] = p

pos2018_a5b1c1d1e1f1g1 = forceatlas2.forceatlas2_networkx_layout(G2018_a5b1c1d1e1f1g1, pos=None, iterations=1000)

for n, p in pos2018_a5b1c1d1e1f1g1.items():
    G2018_a5b1c1d1e1f1g1.nodes[n]['pos2018_a5b1c1d1e1f1g1'] = p

pos2018_a5b5c1d1e1f1g1 = forceatlas2.forceatlas2_networkx_layout(G2018_a5b5c1d1e1f1g1, pos=None, iterations=1000)

for n, p in pos2018_a5b5c1d1e1f1g1.items():
    G2018_a5b5c1d1e1f1g1.nodes[n]['pos2018_a5b5c1d1e1f1g1'] = p

pos2018_a5b0c1d1e1f1g1 = forceatlas2.forceatlas2_networkx_layout(G2018_a5b0c1d1e1f1g1, pos=None, iterations=1000)

for n, p in pos2018_a5b0c1d1e1f1g1.items():
    G2018_a5b0c1d1e1f1g1.nodes[n]['pos2018_a5b0c1d1e1f1g1'] = p

pos2018_a0b1c1d1e1f1g1 = forceatlas2.forceatlas2_networkx_layout(G2018_a0b1c1d1e1f1g1, pos=None, iterations=1000)

for n, p in pos2018_a0b1c1d1e1f1g1.items():
    G2018_a0b1c1d1e1f1g1.nodes[n]['pos2018_a0b1c1d1e1f1g1'] = p

pos2018_a0b5c1d1e1f1g1 = forceatlas2.forceatlas2_networkx_layout(G2018_a0b5c1d1e1f1g1, pos=None, iterations=1000)

for n, p in pos2018_a0b5c1d1e1f1g1.items():
    G2018_a0b5c1d1e1f1g1.nodes[n]['pos2018_a0b5c1d1e1f1g1'] = p

pos2018_a0b0c1d1e1f1g1 = forceatlas2.forceatlas2_networkx_layout(G2018_a0b0c1d1e1f1g1, pos=None, iterations=1000)

for n, p in pos2018_a0b0c1d1e1f1g1.items():
    G2018_a0b0c1d1e1f1g1.nodes[n]['pos2018_a0b0c1d1e1f1g1'] = p

# export to json
json_dict = {}
json_dict['G2018_a1b1c1d1e1f1g1'] = json_graph.node_link_data(G2018_a1b1c1d1e1f1g1)
json_dict['G2018_a1b5c1d1e1f1g1'] = json_graph.node_link_data(G2018_a1b5c1d1e1f1g1)
json_dict['G2018_a1b0c1d1e1f1g1'] = json_graph.node_link_data(G2018_a1b0c1d1e1f1g1)
json_dict['G2018_a0b0c1d1e1f1g1'] = json_graph.node_link_data(G2018_a0b0c1d1e1f1g1)
json_dict['G2018_a0b1c1d1e1f1g1'] = json_graph.node_link_data(G2018_a0b1c1d1e1f1g1)
json_dict['G2018_a0b5c1d1e1f1g1'] = json_graph.node_link_data(G2018_a0b5c1d1e1f1g1)
json_dict['G2018_a5b0c1d1e1f1g1'] = json_graph.node_link_data(G2018_a5b0c1d1e1f1g1)
json_dict['G2018_a5b1c1d1e1f1g1'] = json_graph.node_link_data(G2018_a5b1c1d1e1f1g1)
json_dict['G2018_a5b5c1d1e1f1g1'] = json_graph.node_link_data(G2018_a5b5c1d1e1f1g1)

for name, value in json_dict.items():
    filename = ROOTBEER + 'data/json/' + name + '.json'
    with open(filename, 'w') as outfile:
        json.dump(value, outfile)

#export df_combo for maps
df_combo_filename = ROOTBEER + 'data/df_combo.csv'
df_combo.to_csv(df_combo_filename, index = False, quotechar='"',quoting=csv.QUOTE_ALL)