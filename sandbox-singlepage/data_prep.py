import pandas as pd
import geopandas as gp
from geopy import distance
from sklearn.cluster import KMeans

df = pd.read_csv('data/housing_prepped.csv', dtype={"GEOID": str,"TRACT_NUM": str})

#filter for King County
df = df[(df['COUNTY'] == 'King')]

rdf = pd.read_csv('data/race-data.csv', dtype={"TRACT_NUM": str, "YEAR": str})

#filter for King County 2010
rdf = rdf[(rdf['COUNTY'] == 'King') & (rdf['YEAR'] == '2010')]

#create GEOID
rdf['GEOID'] = '53033' + rdf['TRACT_NUM']

gdf = pd.read_csv('data/washingtongeo_dist.csv',
                   dtype={"TRACTCE_a": str,"TRACTCE_b": str})

white = rdf[(rdf['CENSUS_QUERY'] == 'B03002_003E')]
white = white[['GEOID','COUNTY','TRACT_NUM','DATA']]
white = white.rename(columns = {'DATA' : 'pop_white_nonhisp_only'})
black = rdf[(rdf['CENSUS_QUERY'] == 'B02001_003E')]
black = black[['GEOID','COUNTY','TRACT_NUM','DATA']]
black = black.rename(columns = {'DATA' : 'pop_black_only'})
native = rdf[(rdf['CENSUS_QUERY'] == 'B02001_004E')]
native = native[['GEOID','COUNTY','TRACT_NUM','DATA']]
native = native.rename(columns = {'DATA' : 'pop_native_only'})
asian = rdf[(rdf['CENSUS_QUERY'] == 'B02001_005E')]
asian = asian[['GEOID','COUNTY','TRACT_NUM','DATA']]
asian = asian.rename(columns = {'DATA' : 'pop_asian_only'})
polynesian = rdf[(rdf['CENSUS_QUERY'] == 'B02001_006E')]
polynesian = polynesian[['GEOID','COUNTY','TRACT_NUM','DATA']]
polynesian = polynesian.rename(columns = {'DATA' : 'pop_polynesian_only'})
latino = rdf[(rdf['CENSUS_QUERY'] == 'B03002_012E')]
latino = latino[['GEOID','COUNTY','TRACT_NUM','DATA']]
latino = latino.rename(columns = {'DATA' : 'pop_hispanic'})
other = rdf[(rdf['CENSUS_QUERY'] == 'B02001_007E')]
other = other[['GEOID','COUNTY','TRACT_NUM','DATA']]
other = other.rename(columns = {'DATA' : 'pop_other_only'})
multiracial = rdf[(rdf['CENSUS_QUERY'] == 'B02001_008E')]
multiracial = multiracial[['GEOID','COUNTY','TRACT_NUM','DATA']]
multiracial = multiracial.rename(columns = {'DATA' : 'pop_multiracial'})
racial = white.merge(black, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial = racial.merge(native, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial = racial.merge(asian, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial = racial.merge(polynesian, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial = racial.merge(latino, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial = racial.merge(other, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial = racial.merge(multiracial, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
race_data = racial[['GEOID','COUNTY','TRACT_NUM','pop_white_nonhisp_only','pop_black_only','pop_native_only','pop_asian_only','pop_polynesian_only','pop_hispanic','pop_other_only','pop_multiracial']]

df = df.merge(race_data, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
df['minority_pop'] = df['TOT_POP_2010'] - df['pop_white_nonhisp_only']
df['minority_pop_pct'] = df['pop_white_nonhisp_only'] / df['TOT_POP_2010']

gdf = gdf.merge(df[['TRACT_NUM','GEOID']], how='left', left_on='TRACTCE_a', right_on='TRACT_NUM')
gdf = gdf.rename(columns={'GEOID':'GEOID_a'})
gdf = gdf.merge(df[['TRACT_NUM','GEOID']], how='left', left_on='TRACTCE_b', right_on='TRACT_NUM')
gdf = gdf.rename(columns={'GEOID':'GEOID_b'})

#merge dataframes to combine the different datasets so that you can calculate it.
minority10 = df[['GEOID','minority_pop_pct']]
gdf = gdf.merge(minority10, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'minority_pop_pct':'minority_pop_pct_2010_a'})
gdf = gdf.merge(minority10, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'minority_pop_pct':'minority_pop_pct_2010_b'})

#calculate diff between the two tracts (and take absolute value since sign is meaningless here)
gdf['minority_pop_pct_delta'] = (gdf.minority_pop_pct_2010_a - gdf.minority_pop_pct_2010_b).abs()

#delete unnecessary columns to save memory
del gdf['TRACT_NUM_x']
del gdf['TRACT_NUM_y']
del gdf['GEOID_x']
del gdf['GEOID_y']

#Kmeans clustering
Y = df[['GEOID','TWENTY_PCTILE_2010','minority_pop_pct']]
Y = Y[~Y['minority_pop_pct'].isnull()]
Y = Y[~Y['TWENTY_PCTILE_2010'].isnull()]
X = Y[['TWENTY_PCTILE_2010','minority_pop_pct']]
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
df = df.merge(Y, how='left', left_on=['GEOID','minority_pop_pct','TWENTY_PCTILE_2010'], right_on=['GEOID','minority_pop_pct','TWENTY_PCTILE_2010'])

grp0 = df[(df['labels'] == 0)]
grp0 = grp0[['COUNTY','TRACT_NUM','minority_pop_pct','TWENTY_PCTILE_2010','labels','d']]
grp0_length = str(grp0.shape)
grp1 = df[(df['labels'] == 1)]
grp1 = grp1[['COUNTY','TRACT_NUM','minority_pop_pct','TWENTY_PCTILE_2010','labels','d']]
grp1_length = str(grp1.shape)

grp2 = df[(df['labels'] == 2)]
grp2 = grp2[['COUNTY','TRACT_NUM','minority_pop_pct','TWENTY_PCTILE_2010','labels','d']]
grp2_length = str(grp2.shape)

grp3 = df[(df['labels'] == 3)]
grp3 = grp3[['COUNTY','TRACT_NUM','minority_pop_pct','TWENTY_PCTILE_2010','labels','d']]
grp3_length = str(grp3.shape)

#alpha time
alpha = .5
gdf['omega'] = (alpha * gdf.minority_pop_pct_delta + (1.0-alpha) * gdf.distance*10e-04)

gdf = gdf[gdf['distance'] < 3500]

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
#df = df.rename(columns = {'CITYNAME_y':'CITYNAME'})

import itertools

wallingford_gdf = gdf[(gdf['GEOID_a'] == '53033004600') & (gdf['distance'] < 3500)]
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



# TODO: alpha & omega redef

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
