import pandas as pd
import geopandas as gp
from geopy import distance
from sklearn.cluster import KMeans

df_rent = pd.read_csv('data/king_blockgrp_rent.csv', dtype={"GEOID": str, "TRACT_NUM": str, "YEAR":str, "BLOCK_GRP":str}) #NOTE: pre-filtered in SQL for King County

#filter for 2013
df_rent = df_rent[(df_rent['YEAR'] == '2013')]

#sort median_costs_df by census query, creating new column-sorted dfs instead of rows
df = df_rent[(df_rent['CENSUS_QUERY'] == 'B25071_001E')]
df = df.rename(columns = {'DATA' : 'RENT_AS_PCT_INCOME'})
df = df[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR','RENT_AS_PCT_INCOME']]
costs_df25 = df_rent[(df_rent['CENSUS_QUERY'] == 'B25057_001E')]
costs_df25 = costs_df25.rename(columns = {'DATA' : 'RENT_25PCTILE'})
costs_df25 = costs_df25[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR','RENT_25PCTILE']]
costs_df50 = df_rent[(df_rent['CENSUS_QUERY'] == 'B25058_001E')]
costs_df50 = costs_df50.rename(columns = {'DATA' : 'RENT_50PCTILE'})
costs_df50 = costs_df50[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR','RENT_50PCTILE']]
costs_df75 = df_rent[(df_rent['CENSUS_QUERY'] == 'B25059_001E')]
costs_df75 = costs_df75.rename(columns = {'DATA' : 'RENT_75PCTILE'})
costs_df75 = costs_df75[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR','RENT_75PCTILE']]
df = df.merge(costs_df25, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR']).drop_duplicates()
df = df.merge(costs_df50, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR']).drop_duplicates()
df = df.merge(costs_df75, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR']).drop_duplicates()

#load in race data
rdf = pd.read_csv('data/king_blockgrp_race.csv', dtype={"GEOID": str, "TRACT_NUM": str, "YEAR":str, "BLOCK_GRP":str}) #NOTE: pre-filtered in SQL for King County

#filter for year 2013
rdf = rdf[(rdf['YEAR'] == '2013')]

# TODO: create edges file for census block groups

gdf = pd.read_csv('data/wa_king_census_block_groups_distances.csv',
                   dtype={"block_group_geoid_a": str,"block_group_geoid_b": str})

totpop = rdf[(rdf['CENSUS_QUERY'] == 'B01001_001E')]
totpop = totpop[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA','YEAR']]
totpop = totpop.rename(columns = {'DATA' : 'TOT_POP_2013'})
white = rdf[(rdf['CENSUS_QUERY'] == 'B03002_003E')]
white = white[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA','YEAR']]
white = white.rename(columns = {'DATA' : 'pop_white_nonhisp_only'})
black = rdf[(rdf['CENSUS_QUERY'] == 'B02001_003E')]
black = black[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA','YEAR']]
black = black.rename(columns = {'DATA' : 'pop_black_only'})
native = rdf[(rdf['CENSUS_QUERY'] == 'B02001_004E')]
native = native[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA','YEAR']]
native = native.rename(columns = {'DATA' : 'pop_native_only'})
asian = rdf[(rdf['CENSUS_QUERY'] == 'B02001_005E')]
asian = asian[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA','YEAR']]
asian = asian.rename(columns = {'DATA' : 'pop_asian_only'})
polynesian = rdf[(rdf['CENSUS_QUERY'] == 'B02001_006E')]
polynesian = polynesian[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA','YEAR']]
polynesian = polynesian.rename(columns = {'DATA' : 'pop_polynesian_only'})
latino = rdf[(rdf['CENSUS_QUERY'] == 'B03002_012E')]
latino = latino[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA','YEAR']]
latino = latino.rename(columns = {'DATA' : 'pop_hispanic'})
other = rdf[(rdf['CENSUS_QUERY'] == 'B02001_007E')]
other = other[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA','YEAR']]
other = other.rename(columns = {'DATA' : 'pop_other_only'})
multiracial = rdf[(rdf['CENSUS_QUERY'] == 'B02001_008E')]
multiracial = multiracial[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA','YEAR']]
multiracial = multiracial.rename(columns = {'DATA' : 'pop_multiracial'})
racial = totpop.merge(white, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'])
racial = racial.merge(black, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'])
racial = racial.merge(native, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'])
racial = racial.merge(asian, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'])
racial = racial.merge(polynesian, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'])
racial = racial.merge(latino, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'])
racial = racial.merge(other, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'])
racial = racial.merge(multiracial, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR'])
race_data = racial[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','YEAR','TOT_POP_2013','pop_white_nonhisp_only','pop_black_only','pop_native_only','pop_asian_only','pop_polynesian_only','pop_hispanic','pop_other_only','pop_multiracial']]

df = df.merge(race_data, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP', 'YEAR'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP', 'YEAR']).drop_duplicates()
df['minority_pop'] = df['TOT_POP_2013'] - df['pop_white_nonhisp_only']
df['minority_pop_pct'] = df['minority_pop'] / df['TOT_POP_2013']

gdf = gdf.merge(df[['GEOID']], how='left', left_on='block_group_geoid_a', right_on='GEOID')
gdf = gdf.rename(columns={'block_group_geoid_a':'GEOID_a'})
gdf = gdf.merge(df[['GEOID']], how='left', left_on='block_group_geoid_b', right_on='GEOID')
gdf = gdf.rename(columns={'block_group_geoid_b':'GEOID_b'})

#merge dataframes to combine the different datasets so that you can calculate it.
minority10 = df[['GEOID','minority_pop_pct']]
gdf = gdf.merge(minority10, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'minority_pop_pct':'minority_pop_pct_2010_a'})
gdf = gdf.merge(minority10, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'minority_pop_pct':'minority_pop_pct_2010_b'})

lower_quartile_cost10 = df[['GEOID','RENT_25PCTILE']]
gdf = gdf.merge(lower_quartile_cost10, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'RENT_25PCTILE':'lower_quartile_rent_a'})
gdf = gdf.merge(lower_quartile_cost10, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'RENT_25PCTILE':'lower_quartile_rent_b'})

#calculate diff between the two tracts (and take absolute value since sign is meaningless here)
gdf['minority_pop_pct_delta'] = (gdf.minority_pop_pct_2010_a - gdf.minority_pop_pct_2010_b).abs()
gdf['lower_quartile_rent_delta'] = (gdf.lower_quartile_rent_a - gdf.lower_quartile_rent_b).abs()

#Kmeans clustering
Y = df[['GEOID','RENT_25PCTILE','minority_pop_pct']]
Y = Y[~Y['minority_pop_pct'].isnull()]
Y = Y[~Y['RENT_25PCTILE'].isnull()]
X = Y[['RENT_25PCTILE','minority_pop_pct']]
K = 4
kmeans = KMeans(n_clusters=K, random_state=0).fit(X)
Y['labels'] = kmeans.labels_
c0 = kmeans.cluster_centers_[0]
c1 = kmeans.cluster_centers_[1]
c = pd.DataFrame(kmeans.transform(X), columns=['center_{}'.format(i) for i in range(K)])
for i in range(K):
    Y['center_{}'.format(i)] = c['center_{}'.format(i)]
for i in range(K):
    Y.loc[Y['labels'] == i, 'd'] = Y['center_{}'.format(i)]
#re-merge with df
df = df.merge(Y, how='left', left_on=['GEOID','minority_pop_pct','RENT_25PCTILE'], right_on=['GEOID','minority_pop_pct','RENT_25PCTILE'])

grp0 = df[(df['labels'] == 0)]
grp0 = grp0[['COUNTY','TRACT_NUM','BLOCK_GRP','minority_pop_pct','RENT_25PCTILE','labels','d']]
grp0_length = str(grp0.shape)
grp1 = df[(df['labels'] == 1)]
grp1 = grp1[['COUNTY','TRACT_NUM','BLOCK_GRP','minority_pop_pct','RENT_25PCTILE','labels','d']]
grp1_length = str(grp1.shape)

grp2 = df[(df['labels'] == 2)]
grp2 = grp2[['COUNTY','TRACT_NUM','BLOCK_GRP','minority_pop_pct','RENT_25PCTILE','labels','d']]
grp2_length = str(grp2.shape)

grp3 = df[(df['labels'] == 3)]
grp3 = grp3[['COUNTY','BLOCK_GRP','TRACT_NUM','minority_pop_pct','RENT_25PCTILE','labels','d']]
grp3_length = str(grp3.shape)


# TODO: alpha & omega redef

#alpha time
alpha = .5
gdf['omega'] = (alpha * gdf.minority_pop_pct_delta + (1.0-alpha) * gdf.lower_quartile_rent_delta*10e-03)

#gdf = gdf[gdf['distance'] < 3500] #filter, is only necessary if you need to threshold this and also don't use one of the subset dfs below.

#create cityname df
muni_gdf = gp.read_file('data/shapefiles/Municipal_Boundaries/Municipal_Boundaries.shp')
tract_gdf = gp.read_file('data/shapefiles/KingCountyTracts/kc_tract_10.shp')
t = tract_gdf[['OBJECTID', 'STATEFP10', 'COUNTYFP10', 'TRACTCE10', 'GEOID10', 'geometry']]
m = muni_gdf[['OBJECTID', 'CITYNAME', 'geometry']]
m = m.to_crs(epsg=2926)
#pd.options.display.max_rows = 500
mt = gp.sjoin(t, m, how='left', op='intersects', lsuffix='', rsuffix='_muni')
mt[['GEOID10', 'CITYNAME']]

#merge with cityname df
df = df.merge(mt, how = 'inner', left_on = ['GEOID'], right_on = ['GEOID10'])

#delete unnecessary columns to save memory
del df['OBJECTID_']
del df['GEOID10']
del df['TRACTCE10']
del gdf['GEOID_x']
del gdf['GEOID_y']

#df = df.rename(columns = {'CITYNAME_y':'CITYNAME'})

import itertools

wallingford_gdf = gdf[(gdf['GEOID_a'] == '530330046001') & (gdf['distance'] < 3.500)]
gid_a = list(wallingford_gdf['GEOID_a'].drop_duplicates())
gid_b = list(wallingford_gdf['GEOID_b'].drop_duplicates())

pair_data = {
    'GEOID_a': list(),
    'GEOID_b': list()
}

for ga, gb in itertools.product(gid_a + gid_b, gid_a + gid_b):
    pair_data['GEOID_a'].append(ga)
    pair_data['GEOID_b'].append(gb)

pair_df = pd.DataFrame.from_dict(pair_data)
pair_df = pair_df.merge(gdf, how='left', on=['GEOID_a', 'GEOID_b'])
pair_df = pair_df[~pair_df['distance'].isnull()]

wallingford_gdf = pair_df
wallingford_geoids = list(wallingford_gdf['GEOID_a'].drop_duplicates()) + \
                     list(wallingford_gdf['GEOID_b'].drop_duplicates())
wallingford_df = df[df['GEOID'].isin(wallingford_geoids)]



def get_df(subset='all'):
    subsets = {
        'all': df,
        'wallingford': wallingford_df
    }

    if subset in subsets:
        return subsets[subset]
    else:
        raise('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))


def get_gdf(subset='all'):
    subsets = {
        'all': gdf,
        'wallingford': wallingford_gdf
    }

    if subset in subsets:
        return subsets[subset]
    else:
        raise ('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))
