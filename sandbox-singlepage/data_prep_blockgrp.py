import pandas as pd
import geopandas as gp
from geopy import distance
import json
import os
import numpy as np

#set root directory for data files
#ROOTDIR = '/home/ubuntu/housing_equity/sandbox-singlepage/data' #production
ROOTDIR = os.path.join(os.getenv('EPCW_DROPBOX'), 'Projects/housing_equity/sandbox-singlepage/data')
# ROOTDIR = '' #local

#read in shapefile (needs to be in GeoJSON format)
#with open('/home/ubuntu/dash/data/washingtongeo.json','r') as GeoJSON:
with open(os.path.join(ROOTDIR, 'wa_king_census_block_groups.geojson'),'r') as GeoJSON:
    block_grp_geoids = json.load(GeoJSON)

df_rent = pd.read_csv(os.path.join(ROOTDIR, 'king_blockgrp_rent.csv'), dtype={"GEOID": str, "TRACT_NUM": str, "YEAR":str, "BLOCK_GRP":str}) #NOTE: pre-filtered in SQL for King County

#filter for 2013
df_rent = df_rent[(df_rent['YEAR'] == '2013') | (df_rent['YEAR'] == '2018')]

#sort median_costs_df by census query, creating new column-sorted dfs instead of rows
df13 = df_rent[(df_rent['YEAR'] == '2013')]
dfrent_13 = df13[(df13['CENSUS_QUERY'] == 'B25071_001E')]
dfrent_13 = dfrent_13.rename(columns = {'DATA' : 'RENT_AS_PCT_INCOME_2013'})
dfrent_13 = dfrent_13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','RENT_AS_PCT_INCOME_2013']]
costs_df25_13 = df13[(df13['CENSUS_QUERY'] == 'B25057_001E')]
costs_df25_13 = costs_df25_13.rename(columns = {'DATA' : 'RENT_25PCTILE_2013'})
costs_df25_13 = costs_df25_13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','RENT_25PCTILE_2013']]
costs_df50_13 = df13[(df13['CENSUS_QUERY'] == 'B25058_001E')]
costs_df50_13 = costs_df50_13.rename(columns = {'DATA' : 'RENT_50PCTILE_2013'})
costs_df50_13 = costs_df50_13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','RENT_50PCTILE_2013']]
costs_df75_13 = df13[(df13['CENSUS_QUERY'] == 'B25059_001E')]
costs_df75_13 = costs_df75_13.rename(columns = {'DATA' : 'RENT_75PCTILE_2013'})
costs_df75_13 = costs_df75_13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','RENT_75PCTILE_2013']]
df13 = dfrent_13.merge(costs_df25_13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP']).drop_duplicates()
df13 = df13.merge(costs_df50_13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP']).drop_duplicates()
df13 = df13.merge(costs_df75_13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP']).drop_duplicates()

df18 = df_rent[(df_rent['YEAR'] == '2018')]
dfrent_18 = df18[(df18['CENSUS_QUERY'] == 'B25071_001E')]
dfrent_18 = dfrent_18.rename(columns = {'DATA' : 'RENT_AS_PCT_INCOME_2018'})
dfrent_18 = dfrent_18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','RENT_AS_PCT_INCOME_2018']]
costs_df25_18 = df18[(df18['CENSUS_QUERY'] == 'B25057_001E')]
costs_df25_18 = costs_df25_18.rename(columns = {'DATA' : 'RENT_25PCTILE_2018'})
costs_df25_18 = costs_df25_18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','RENT_25PCTILE_2018']]
costs_df50_18 = df18[(df18['CENSUS_QUERY'] == 'B25058_001E')]
costs_df50_18 = costs_df50_18.rename(columns = {'DATA' : 'RENT_50PCTILE_2018'})
costs_df50_18 = costs_df50_18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','RENT_50PCTILE_2018']]
costs_df75_18 = df18[(df18['CENSUS_QUERY'] == 'B25059_001E')]
costs_df75_18 = costs_df75_18.rename(columns = {'DATA' : 'RENT_75PCTILE_2018'})
costs_df75_18 = costs_df75_18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','RENT_75PCTILE_2018']]
df18 = dfrent_18.merge(costs_df25_18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP']).drop_duplicates()
df18 = df18.merge(costs_df50_18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP']).drop_duplicates()
df18 = df18.merge(costs_df75_18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP']).drop_duplicates()

df = df13 = df13.merge(df18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP']).drop_duplicates()

#load in race data
rdf = pd.read_csv(os.path.join(ROOTDIR, 'king_blockgrp_race.csv'), dtype={"GEOID": str, "TRACT_NUM": str, "YEAR":str, "BLOCK_GRP":str}) #NOTE: pre-filtered in SQL for King County

#filter for year 2013
rdf = rdf[(rdf['YEAR'] == '2013') | (rdf['YEAR'] == '2018') ]

gdf = pd.read_csv(os.path.join(ROOTDIR, 'wa_king_census_block_groups_distances.csv'),
                   dtype={"block_group_geoid_a": str,"block_group_geoid_b": str})

rdf13 = rdf[(rdf['YEAR'] == '2013')]
totpop_13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B01001_001E')]
totpop_13 = totpop_13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA','YEAR']]
totpop_13 = totpop_13.rename(columns = {'DATA' : 'TOT_POP_2013'})
white_13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B03002_003E')]
white_13 = white_13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
white_13 = white_13.rename(columns = {'DATA' : 'pop_white_nonhisp_only_2013'})
black_13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B02001_003E')]
black_13 = black_13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
black_13 = black_13.rename(columns = {'DATA' : 'pop_black_only_2013'})
native_13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B02001_004E')]
native_13 = native_13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
native_13 = native_13.rename(columns = {'DATA' : 'pop_native_only_2013'})
asian_13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B02001_005E')]
asian_13 = asian_13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
asian_13 = asian_13.rename(columns = {'DATA' : 'pop_asian_only_2013'})
polynesian_13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B02001_006E')]
polynesian_13 = polynesian_13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
polynesian_13 = polynesian_13.rename(columns = {'DATA' : 'pop_polynesian_only_2013'})
latino_13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B03002_012E')]
latino_13 = latino_13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
latino_13 = latino_13.rename(columns = {'DATA' : 'pop_hispanic_2013'})
other_13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B02001_007E')]
other_13 = other_13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
other_13 = other_13.rename(columns = {'DATA' : 'pop_other_only_2013'})
multiracial_13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B02001_008E')]
multiracial_13 = multiracial_13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
multiracial_13 = multiracial_13.rename(columns = {'DATA' : 'pop_multiracial_2013'})
racial13 = totpop_13.merge(white_13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial13 = racial13.merge(black_13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial13 = racial13.merge(native_13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial13 = racial13.merge(asian_13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial13 = racial13.merge(polynesian_13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial13 = racial13.merge(latino_13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial13 = racial13.merge(other_13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial13 = racial13.merge(multiracial_13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
race_data13 = racial13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','TOT_POP_2013','pop_white_nonhisp_only_2013','pop_black_only_2013','pop_native_only_2013','pop_asian_only_2013','pop_polynesian_only_2013','pop_hispanic_2013','pop_other_only_2013','pop_multiracial_2013']]

rdf18 = rdf[(rdf['YEAR'] == '2018')]
totpop_18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B01001_001E')]
totpop_18 = totpop_18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA','YEAR']]
totpop_18 = totpop_18.rename(columns = {'DATA' : 'TOT_POP_2018'})
white_18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B03002_003E')]
white_18 = white_18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
white_18 = white_18.rename(columns = {'DATA' : 'pop_white_nonhisp_only_2018'})
black_18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_003E')]
black_18 = black_18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
black_18 = black_18.rename(columns = {'DATA' : 'pop_black_only_2018'})
native_18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_004E')]
native_18 = native_18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
native_18 = native_18.rename(columns = {'DATA' : 'pop_native_only_2018'})
asian_18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_005E')]
asian_18 = asian_18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
asian_18 = asian_18.rename(columns = {'DATA' : 'pop_asian_only_2018'})
polynesian_18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_006E')]
polynesian_18 = polynesian_18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
polynesian_18 = polynesian_18.rename(columns = {'DATA' : 'pop_polynesian_only_2018'})
latino_18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B03002_012E')]
latino_18 = latino_18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
latino_18 = latino_18.rename(columns = {'DATA' : 'pop_hispanic_2018'})
other_18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_007E')]
other_18 = other_18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
other_18 = other_18.rename(columns = {'DATA' : 'pop_other_only_2018'})
multiracial_18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_008E')]
multiracial_18 = multiracial_18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','DATA']]
multiracial_18 = multiracial_18.rename(columns = {'DATA' : 'pop_multiracial_2018'})
racial18 = totpop_18.merge(white_18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial18 = racial18.merge(black_18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial18 = racial18.merge(native_18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial18 = racial18.merge(asian_18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial18 = racial18.merge(polynesian_18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial18 = racial18.merge(latino_18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial18 = racial18.merge(other_18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
racial18 = racial18.merge(multiracial_18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
race_data18 = racial18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','TOT_POP_2018','pop_white_nonhisp_only_2018','pop_black_only_2018','pop_native_only_2018','pop_asian_only_2018','pop_polynesian_only_2018','pop_hispanic_2018','pop_other_only_2018','pop_multiracial_2018']]
race_data = race_data13.merge(race_data18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP']).drop_duplicates()

df = df.merge(race_data, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP']).drop_duplicates()
df['minority_pop_2013'] = df['TOT_POP_2013'] - df['pop_white_nonhisp_only_2013']
df['minority_pop_pct_2013'] = df['minority_pop_2013'] / df['TOT_POP_2013']
df['minority_pop_2018'] = df['TOT_POP_2018'] - df['pop_white_nonhisp_only_2018']
df['minority_pop_pct_2018'] = df['minority_pop_2018'] / df['TOT_POP_2018']

#bring in affordable housing data
housing_df_raw = pd.read_csv(os.path.join(ROOTDIR, 'king_blockgrp_housing-details.csv'), dtype={"DATA":float,"YEAR":str,"TRACT_NUM": str, "BLOCK_GRP": str})

#create geoid
housing_df_raw['GEOID'] = '53033' + housing_df_raw['TRACT_NUM'] + housing_df_raw['BLOCK_GRP']

#Aggregate unit data (rows in original housing_df_raw are counts of units under 100/mo, 200/mo, 300/mo, etc.
affordable_df_raw = housing_df_raw[(housing_df_raw['CENSUS_QUERY'] == 'B25063_003E') | (housing_df_raw['CENSUS_QUERY'] == 'B25063_004E') | (housing_df_raw['CENSUS_QUERY'] == 'B25063_005E') | (housing_df_raw['CENSUS_QUERY'] == 'B25063_006E') | (housing_df_raw['CENSUS_QUERY'] == 'B25063_007E') | (housing_df_raw['CENSUS_QUERY'] == 'B25063_008E') | (housing_df_raw['CENSUS_QUERY'] == 'B25063_009E') | (housing_df_raw['CENSUS_QUERY'] == 'B25063_010E') | (housing_df_raw['CENSUS_QUERY'] == 'B25063_011E') | (housing_df_raw['CENSUS_QUERY'] == 'B25063_012E') | (housing_df_raw['CENSUS_QUERY'] == 'B25063_013E')]
affordable_df = affordable_df_raw[['COUNTY','TRACT_NUM','BLOCK_GRP','GEOID','YEAR']]

affordable_data13 = affordable_df_raw[(affordable_df_raw['YEAR'] == '2013')]
affordable_data13 = affordable_data13.groupby(['GEOID']).sum().reset_index()
affordable_df = affordable_df.merge(affordable_data13, how='left', left_on=['GEOID'], right_on=['GEOID'])
affordable_df = affordable_df[['COUNTY','TRACT_NUM','BLOCK_GRP','GEOID','DATA']]
affordable_df = affordable_df.rename(columns = {'DATA' : 'sub_600_units_2013'})
affordable_data18 = affordable_df_raw[(affordable_df_raw['YEAR'] == '2018')]
affordable_data18 = affordable_data18.groupby(['GEOID']).sum().reset_index()
affordable_df = affordable_df.merge(affordable_data18, how='left', left_on=['GEOID'], right_on=['GEOID']).drop_duplicates()
affordable_df = affordable_df[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','sub_600_units_2013','DATA']]
affordable_df = affordable_df.rename(columns = {'DATA' : 'sub_600_units_2018'})
df = df.merge(affordable_df, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
df['sub_600_units_per_capita_2013'] = df['sub_600_units_2013']/df['TOT_POP_2013']
df['sub_600_units_per_capita_2018'] = df['sub_600_units_2018']/df['TOT_POP_2018']

#Tenancy data
tenancy_df_raw = housing_df_raw[(housing_df_raw['CENSUS_QUERY'] == 'B25039_001E')]
tenancy13 = tenancy_df_raw[(tenancy_df_raw['YEAR'] == '2013')]
tenancy13['median_tenancy_2013'] = 2013 - (tenancy13.DATA)
tenancy13 = tenancy13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','median_tenancy_2013']]
tenancy18 = tenancy_df_raw[(tenancy_df_raw['YEAR'] == '2018')]
tenancy18['median_tenancy_2018'] = 2018 - (tenancy18.DATA)
tenancy18 = tenancy18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','median_tenancy_2018']]
df = df.merge(tenancy13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
df = df.merge(tenancy18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])

#housing age data
housing_age_df_raw = housing_df_raw[(housing_df_raw['CENSUS_QUERY'] == 'B25035_001E')]
housing_age13 = housing_age_df_raw[(housing_age_df_raw['YEAR'] == '2013')]
housing_age13['median_housing_age_2013'] = 2013 - (housing_age13.DATA)
housing_age13 = housing_age13[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','median_housing_age_2013']]
housing_age13.loc[housing_age13.median_housing_age_2013 > 100, 'median_housing_age_2013'] = None #corrects for the census having "2018" as an answer to some of these
housing_age18 = housing_age_df_raw[(housing_age_df_raw['YEAR'] == '2018')]
housing_age18['median_housing_age_2018'] = 2018 - (housing_age18.DATA)
housing_age18 = housing_age18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','median_housing_age_2018']]
housing_age18.loc[housing_age18.median_housing_age_2018 > 100, 'median_housing_age_2018'] = None #corrects for the census having "2018" as an answer to some of these

df = df.merge(housing_age13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])
df = df.merge(housing_age18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'], right_on = ['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP'])

gdf = gdf.merge(df[['GEOID']], how='left', left_on='block_group_geoid_a', right_on='GEOID')
gdf = gdf.rename(columns={'block_group_geoid_a':'GEOID_a'})
gdf = gdf.merge(df[['GEOID']], how='left', left_on='block_group_geoid_b', right_on='GEOID')
gdf = gdf.rename(columns={'block_group_geoid_b':'GEOID_b'})

df['minority_pop_pct_change'] = (df.minority_pop_pct_2018 - df.minority_pop_pct_2013)
df['rent_25th_pctile_change'] = (df.RENT_25PCTILE_2018 - df.RENT_25PCTILE_2013)
df['totpop_change'] = (df.TOT_POP_2018 - df.TOT_POP_2013)
df['rent_pct_income_change'] = (df.RENT_AS_PCT_INCOME_2018 - df.RENT_AS_PCT_INCOME_2013)
df['affordable_units_per_cap_change'] = (df.sub_600_units_per_capita_2018 - df.sub_600_units_per_capita_2013)
df['median_tenancy_change'] = (df.median_tenancy_2018 - df.median_tenancy_2013)
df['median_housing_age_change'] = (df.median_housing_age_2018 - df.median_housing_age_2013)

#CONVERT ALL CHANGES TO Z-SCORE SO YOU CAN COMPARE THEM
df['minority_pop_pct_change'] = (df.minority_pop_pct_change - df.minority_pop_pct_change.mean())/df.minority_pop_pct_change.std()
df['rent_25th_pctile_change'] = (df.rent_25th_pctile_change - df.rent_25th_pctile_change.mean())/df.rent_25th_pctile_change.std()
df['totpop_change'] = (df.totpop_change - df.totpop_change.mean())/df.totpop_change.std()
df['rent_pct_income_change'] = (df.rent_pct_income_change - df.rent_pct_income_change.mean())/df.rent_pct_income_change.std()
df['affordable_units_per_cap_change'] = (df.affordable_units_per_cap_change - df.affordable_units_per_cap_change.mean())/df.affordable_units_per_cap_change.std()
df['median_tenancy_change'] = (df.median_tenancy_change - df.median_tenancy_change.mean())/df.median_tenancy_change.std()
df['median_housing_age_change'] = (df.median_housing_age_change - df.median_housing_age_change.mean())/df.median_housing_age_change.std()

#CONVERT 2013 numbers to z-score for comparison
df['minority_pop_pct_2013z'] = (df.minority_pop_pct_2013 - df.minority_pop_pct_2013.mean())/df.minority_pop_pct_2013.std()
df['rent_25th_pctile_2013z'] = (df.RENT_25PCTILE_2013 - df.RENT_25PCTILE_2013.mean())/df.RENT_25PCTILE_2013.std()
df['totpop_2013z'] = (df.TOT_POP_2013 - df.TOT_POP_2013.mean())/df.TOT_POP_2013.std()
df['rent_pct_income_2013z'] = (df.RENT_AS_PCT_INCOME_2013 - df.RENT_AS_PCT_INCOME_2013.mean())/df.RENT_AS_PCT_INCOME_2013.std()
df['affordable_units_per_cap_2013z'] = (df.sub_600_units_per_capita_2013 - df.sub_600_units_per_capita_2013.mean())/df.sub_600_units_per_capita_2013.std()
df['median_tenancy_2013z'] = (df.median_tenancy_2013 - df.median_tenancy_2013.mean())/df.median_tenancy_2013.std()
df['median_housing_age_2013z'] = (df.median_housing_age_2013 - df.median_housing_age_2013.mean())/df.median_housing_age_2013.std()

#CONVERT 2018 numbers to z-score for comparison
df['minority_pop_pct_2018z'] = (df.minority_pop_pct_2018 - df.minority_pop_pct_2018.mean())/df.minority_pop_pct_2018.std()
df['rent_25th_pctile_2018z'] = (df.RENT_25PCTILE_2018 - df.RENT_25PCTILE_2018.mean())/df.RENT_25PCTILE_2018.std()
df['totpop_2018z'] = (df.TOT_POP_2018 - df.TOT_POP_2018.mean())/df.TOT_POP_2018.std()
df['rent_pct_income_2018z'] = (df.RENT_AS_PCT_INCOME_2018 - df.RENT_AS_PCT_INCOME_2018.mean())/df.RENT_AS_PCT_INCOME_2018.std()
df['affordable_units_per_cap_2018z'] = (df.sub_600_units_per_capita_2018 - df.sub_600_units_per_capita_2018.mean())/df.sub_600_units_per_capita_2018.std()
df['median_tenancy_2018z'] = (df.median_tenancy_2018 - df.median_tenancy_2018.mean())/df.median_tenancy_2018.std()
df['median_housing_age_2018z'] = (df.median_housing_age_2018 - df.median_housing_age_2018.mean())/df.median_housing_age_2018.std()

#merge dataframes to combine the different datasets so that you can calculate it.
minority = df[['GEOID','minority_pop_pct_change','minority_pop_pct_2013z','minority_pop_pct_2018z']]
gdf = gdf.merge(minority, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'minority_pop_pct_change':'minority_pop_pct_change_a'})
gdf = gdf.rename(columns = {'minority_pop_pct_2013z':'minority_pop_pct_2013z_a'})
gdf = gdf.rename(columns = {'minority_pop_pct_2018z':'minority_pop_pct_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_2013z_a','minority_pop_pct_2018z_a']]
gdf = gdf.merge(minority, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'minority_pop_pct_change':'minority_pop_pct_change_b'})
gdf = gdf.rename(columns = {'minority_pop_pct_2013z':'minority_pop_pct_2013z_b'})
gdf = gdf.rename(columns = {'minority_pop_pct_2018z':'minority_pop_pct_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b']]

lower_quartile_rent = df[['GEOID','rent_25th_pctile_change','rent_25th_pctile_2013z','rent_25th_pctile_2018z']]
gdf = gdf.merge(lower_quartile_rent, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'rent_25th_pctile_change':'rent_25th_pctile_change_a'})
gdf = gdf.rename(columns = {'rent_25th_pctile_2013z':'rent_25th_pctile_2013z_a'})
gdf = gdf.rename(columns = {'rent_25th_pctile_2018z':'rent_25th_pctile_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a']]
gdf = gdf.merge(lower_quartile_rent, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'rent_25th_pctile_change':'rent_25th_pctile_change_b'})
gdf = gdf.rename(columns = {'rent_25th_pctile_2013z':'rent_25th_pctile_2013z_b'})
gdf = gdf.rename(columns = {'rent_25th_pctile_2018z':'rent_25th_pctile_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b']]

totpop = df[['GEOID','totpop_change','totpop_2013z','totpop_2018z']]
gdf = gdf.merge(totpop, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'totpop_change':'totpop_change_a'})
gdf = gdf.rename(columns = {'totpop_2013z':'totpop_2013z_a'})
gdf = gdf.rename(columns = {'totpop_2018z':'totpop_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a']]
gdf = gdf.merge(totpop, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'totpop_change':'totpop_change_b'})
gdf = gdf.rename(columns = {'totpop_2013z':'totpop_2013z_b'})
gdf = gdf.rename(columns = {'totpop_2018z':'totpop_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b']]

rent_pct_income = df[['GEOID','rent_pct_income_change','rent_pct_income_2013z','rent_pct_income_2018z']]
gdf = gdf.merge(rent_pct_income, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'rent_pct_income_change':'rent_pct_income_change_a'})
gdf = gdf.rename(columns = {'rent_pct_income_2013z':'rent_pct_income_2013z_a'})
gdf = gdf.rename(columns = {'rent_pct_income_2018z':'rent_pct_income_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a']]
gdf = gdf.merge(rent_pct_income, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'rent_pct_income_change':'rent_pct_income_change_b'})
gdf = gdf.rename(columns = {'rent_pct_income_2013z':'rent_pct_income_2013z_b'})
gdf = gdf.rename(columns = {'rent_pct_income_2018z':'rent_pct_income_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b']]

affordable_units_per_cap = df[['GEOID','affordable_units_per_cap_change','affordable_units_per_cap_2013z','affordable_units_per_cap_2018z']]
gdf = gdf.merge(affordable_units_per_cap, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'affordable_units_per_cap_change':'affordable_units_per_cap_change_a'})
gdf = gdf.rename(columns = {'affordable_units_per_cap_2013z':'affordable_units_per_cap_2013z_a'})
gdf = gdf.rename(columns = {'affordable_units_per_cap_2018z':'affordable_units_per_cap_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a']]
gdf = gdf.merge(affordable_units_per_cap, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'affordable_units_per_cap_change':'affordable_units_per_cap_change_b'})
gdf = gdf.rename(columns = {'affordable_units_per_cap_2013z':'affordable_units_per_cap_2013z_b'})
gdf = gdf.rename(columns = {'affordable_units_per_cap_2018z':'affordable_units_per_cap_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a','affordable_units_per_cap_change_b','affordable_units_per_cap_2013z_b','affordable_units_per_cap_2018z_b']]

tenancy = df[['GEOID','median_tenancy_change','median_tenancy_2013z','median_tenancy_2018z']]
gdf = gdf.merge(tenancy, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'median_tenancy_change':'median_tenancy_change_a'})
gdf = gdf.rename(columns = {'median_tenancy_2013z':'median_tenancy_2013z_a'})
gdf = gdf.rename(columns = {'median_tenancy_2018z':'median_tenancy_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a','affordable_units_per_cap_change_b','affordable_units_per_cap_2013z_b','affordable_units_per_cap_2018z_b','median_tenancy_change_a','median_tenancy_2013z_a','median_tenancy_2018z_a']]
gdf = gdf.merge(tenancy, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'median_tenancy_change':'median_tenancy_change_b'})
gdf = gdf.rename(columns = {'median_tenancy_2013z':'median_tenancy_2013z_b'})
gdf = gdf.rename(columns = {'median_tenancy_2018z':'median_tenancy_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a','affordable_units_per_cap_change_b','affordable_units_per_cap_2013z_b','affordable_units_per_cap_2018z_b','median_tenancy_change_a','median_tenancy_2013z_a','median_tenancy_2018z_a','median_tenancy_change_b','median_tenancy_2013z_b','median_tenancy_2018z_b']]

housing_age = df[['GEOID','median_housing_age_change','median_housing_age_2013z','median_housing_age_2018z']]
gdf = gdf.merge(housing_age, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'median_housing_age_change':'median_housing_age_change_a'})
gdf = gdf.rename(columns = {'median_housing_age_2013z':'median_housing_age_2013z_a'})
gdf = gdf.rename(columns = {'median_housing_age_2018z':'median_housing_age_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a','affordable_units_per_cap_change_b','affordable_units_per_cap_2013z_b','affordable_units_per_cap_2018z_b','median_tenancy_change_a','median_tenancy_2013z_a','median_tenancy_2018z_a','median_tenancy_change_b','median_tenancy_2013z_b','median_tenancy_2018z_b','median_housing_age_change_a','median_housing_age_2013z_a','median_housing_age_2018z_a']]
gdf = gdf.merge(housing_age, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'median_housing_age_change':'median_housing_age_change_b'})
gdf = gdf.rename(columns = {'median_housing_age_2013z':'median_housing_age_2013z_b'})
gdf = gdf.rename(columns = {'median_housing_age_2018z':'median_housing_age_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a','affordable_units_per_cap_change_b','affordable_units_per_cap_2013z_b','affordable_units_per_cap_2018z_b','median_tenancy_change_a','median_tenancy_2013z_a','median_tenancy_2018z_a','median_tenancy_change_b','median_tenancy_2013z_b','median_tenancy_2018z_b','median_housing_age_change_a','median_housing_age_2013z_a','median_housing_age_2018z_a','median_housing_age_change_b','median_housing_age_2013z_b','median_housing_age_2018z_b']]


# omicron = 1/3 #this is the vectored weighting factor of starting point (omicron) vs change (1-omicron)
omicron = 1.0

#calculate diff between the two tracts (and take absolute value since sign is meaningless here) - Delta taking into account starting point (2013) and change.
gdf['minority_pop_pct_change_delta'] = ((((1-omicron) * gdf.minority_pop_pct_change_a) + (omicron * gdf.minority_pop_pct_2013z_a)) - (((1-omicron) * gdf.minority_pop_pct_change_b) + (omicron * gdf.minority_pop_pct_2013z_b))).abs()
gdf['minority_pop_pct_change_delta'] = gdf['minority_pop_pct_change_delta'].fillna(0) #deals with nan in dataframe, which was breaking the network
gdf['rent_25th_pctile_change_delta'] = ((((1-omicron) * gdf.rent_25th_pctile_change_a) + (omicron * gdf.rent_25th_pctile_2013z_a)) - (((1-omicron) * gdf.rent_25th_pctile_change_b) + (omicron * gdf.rent_25th_pctile_2013z_b))).abs()
gdf['rent_25th_pctile_change_delta'] = gdf['rent_25th_pctile_change_delta'].fillna(0)
gdf['totpop_change_delta'] = ((((1-omicron) * gdf.totpop_change_a) + (omicron * gdf.totpop_2013z_a)) - (((1-omicron) * gdf.totpop_change_b) + (omicron * gdf.totpop_2013z_b))).abs()
gdf['totpop_change_delta'] = gdf['totpop_change_delta'].fillna(0)
gdf['rent_pct_income_change_delta'] = ((((1-omicron) * gdf.rent_pct_income_change_a) + (omicron * gdf.rent_pct_income_2013z_a)) - (((1-omicron) * gdf.rent_pct_income_change_b) + (omicron * gdf.rent_pct_income_2013z_b))).abs()
gdf['rent_pct_income_change_delta'] = gdf['rent_pct_income_change_delta'].fillna(0)
gdf['affordable_units_per_cap_change_delta'] = ((((1-omicron) * gdf.affordable_units_per_cap_change_a) + (omicron * gdf.affordable_units_per_cap_2013z_a)) - (((1-omicron) * gdf.affordable_units_per_cap_change_b) + (omicron * gdf.affordable_units_per_cap_2013z_b))).abs()
gdf['affordable_units_per_cap_change_delta'] = gdf['affordable_units_per_cap_change_delta'].fillna(0)
gdf['median_tenancy_change_delta'] = ((((1-omicron) * gdf.median_tenancy_change_a) + (omicron * gdf.median_tenancy_2013z_a)) - (((1-omicron) * gdf.median_tenancy_change_b) + (omicron * gdf.median_tenancy_2013z_b))).abs()
gdf['median_tenancy_change_delta'] = gdf['median_tenancy_change_delta'].fillna(0)
gdf['median_housing_age_change_delta'] = ((((1-omicron) * gdf.median_housing_age_change_a) + (omicron * gdf.median_housing_age_2013z_a)) - (((1-omicron) * gdf.median_housing_age_change_b) + (omicron * gdf.median_housing_age_2013z_b))).abs()
gdf['median_housing_age_change_delta'] = gdf['median_housing_age_change_delta'].fillna(0)

#Delta in 2013 (without taking into account change)
gdf['minority_pop_pct_change_delta_2013'] = ((gdf.minority_pop_pct_2013z_a) - (gdf.minority_pop_pct_2013z_b)).abs()
gdf['minority_pop_pct_change_delta_2013'] = gdf['minority_pop_pct_change_delta_2013'].fillna(0) #deals with nan in dataframe, which was breaking the network
gdf['rent_25th_pctile_change_delta_2013'] = ((gdf.rent_25th_pctile_2013z_a) - (gdf.rent_25th_pctile_2013z_b)).abs()
gdf['rent_25th_pctile_change_delta_2013'] = gdf['rent_25th_pctile_change_delta_2013'].fillna(0)
gdf['totpop_change_delta_2013'] = ((gdf.totpop_2013z_a) - (gdf.totpop_2013z_b)).abs()
gdf['totpop_change_delta_2013'] = gdf['totpop_change_delta_2013'].fillna(0)
gdf['rent_pct_income_change_delta_2013'] = ((gdf.rent_pct_income_2013z_a) - (gdf.rent_pct_income_2013z_b)).abs()
gdf['rent_pct_income_change_delta_2013'] = gdf['rent_pct_income_change_delta_2013'].fillna(0)
gdf['affordable_units_per_cap_change_delta_2013'] = ((gdf.affordable_units_per_cap_2013z_a) - (gdf.affordable_units_per_cap_2013z_b)).abs()
gdf['affordable_units_per_cap_change_delta_2013'] = gdf['affordable_units_per_cap_change_delta_2013'].fillna(0)
gdf['median_tenancy_change_delta_2013'] = ((gdf.median_tenancy_2013z_a) - (gdf.median_tenancy_2013z_b)).abs()
gdf['median_tenancy_change_delta_2013'] = gdf['median_tenancy_change_delta_2013'].fillna(0)
gdf['median_housing_age_change_delta_2013'] = ((gdf.median_housing_age_2013z_a) - (gdf.median_housing_age_2013z_b)).abs()
gdf['median_housing_age_change_delta_2013'] = gdf['median_housing_age_change_delta_2013'].fillna(0)

#Delta in 2018 (without taking into account change)
gdf['minority_pop_pct_change_delta_2018'] = (gdf.minority_pop_pct_2018z_a) - (gdf.minority_pop_pct_2018z_b).abs()
gdf['minority_pop_pct_change_delta_2018'] = gdf['minority_pop_pct_change_delta_2018'].fillna(0) #deals with nan in dataframe, which was breaking the network
gdf['rent_25th_pctile_change_delta_2018'] = (gdf.rent_25th_pctile_2018z_a) - (gdf.rent_25th_pctile_2018z_b).abs()
gdf['rent_25th_pctile_change_delta_2018'] = gdf['rent_25th_pctile_change_delta_2018'].fillna(0)
gdf['totpop_change_delta_2018'] = (gdf.totpop_2018z_a) - (gdf.totpop_2018z_b).abs()
gdf['totpop_change_delta_2018'] = gdf['totpop_change_delta_2018'].fillna(0)
gdf['rent_pct_income_change_delta_2018'] = (gdf.rent_pct_income_2018z_a) - (gdf.rent_pct_income_2018z_b).abs()
gdf['rent_pct_income_change_delta_2018'] = gdf['rent_pct_income_change_delta_2018'].fillna(0)
gdf['affordable_units_per_cap_change_delta_2018'] = (gdf.affordable_units_per_cap_2018z_a) - (gdf.affordable_units_per_cap_2018z_b).abs()
gdf['affordable_units_per_cap_change_delta_2018'] = gdf['affordable_units_per_cap_change_delta_2018'].fillna(0)
gdf['median_tenancy_change_delta_2018'] = (gdf.median_tenancy_2018z_a) - (gdf.median_tenancy_2018z_b).abs()
gdf['median_tenancy_change_delta_2018'] = gdf['median_tenancy_change_delta_2018'].fillna(0)
gdf['median_housing_age_change_delta_2018'] = (gdf.median_housing_age_2018z_a) - (gdf.median_housing_age_2018z_b).abs()
gdf['median_housing_age_change_delta_2018'] = gdf['median_housing_age_change_delta_2018'].fillna(0)


#weight the edges
weights = [
    1,
    0,
    0,
    0,
    0,
    0,
    0
]

z = np.sum(weights)
weights = [ wi/z for wi in weights ]

alpha, bravo, charlie, delta, echo, foxtrot, golf = weights

threshold = -0.5

#2013 + change version
gdf['omega'] = (
        -(alpha * gdf.minority_pop_pct_change_delta) + \
        (bravo * gdf.rent_25th_pctile_change_delta) + \
        (charlie * gdf.totpop_change_delta) + \
        (delta * gdf.rent_pct_income_change_delta) + \
        -(echo * gdf.affordable_units_per_cap_change_delta) + \
        -(foxtrot * gdf.median_tenancy_change_delta) + \
        (golf * gdf.median_housing_age_change_delta)
)

#gdf.loc[gdf.omega < 0, 'omega'] = None #corrects for the census having "2018" as an answer to some of these
gdf = gdf[(gdf['omega'] >= threshold)]

#2013 only version
gdf['omega13'] = (
        -(alpha * gdf.minority_pop_pct_change_delta_2013) + \
        (bravo * gdf.rent_25th_pctile_change_delta_2013) + \
        (charlie * gdf.totpop_change_delta_2013) + \
        (delta * gdf.rent_pct_income_change_delta_2013) + \
        -(echo * gdf.affordable_units_per_cap_change_delta_2013) + \
        -(foxtrot * gdf.median_tenancy_change_delta_2013) + \
        (golf * gdf.median_housing_age_change_delta_2013)
)
gdf = gdf[(gdf['omega13'] >= threshold)]

#2018 only version
gdf['omega18'] = (
        -(alpha * gdf.minority_pop_pct_change_delta_2018) + \
        (bravo * gdf.rent_25th_pctile_change_delta_2018) + \
        (charlie * gdf.totpop_change_delta_2018) + \
        (delta * gdf.rent_pct_income_change_delta_2018) + \
        -(echo * gdf.affordable_units_per_cap_change_delta_2018) + \
        -(foxtrot * gdf.median_tenancy_change_delta_2018) + \
        (golf * gdf.median_housing_age_change_delta_2018)
)
gdf = gdf[(gdf['omega18'] >= threshold)]

#tester for bar graph of just geoid_a
gdf['omega_bar'] = (
        -(alpha * (((1-omicron) * gdf.minority_pop_pct_change_a) + (omicron * gdf.minority_pop_pct_2013z_a))) + \
        (bravo * (((1-omicron) * gdf.rent_25th_pctile_change_a) + (omicron * gdf.rent_25th_pctile_2013z_a))) + \
        (charlie * (((1-omicron) * gdf.totpop_change_a) + (omicron * gdf.totpop_2013z_a))) + \
        (delta * (((1-omicron) * gdf.rent_pct_income_change_a) + (omicron * gdf.rent_pct_income_2013z_a))) + \
        -(echo * (((1-omicron) * gdf.affordable_units_per_cap_change_a) + (omicron * gdf.affordable_units_per_cap_2013z_a))) + \
        -(foxtrot * (((1-omicron) * gdf.median_tenancy_change_a) + (omicron * gdf.median_tenancy_2013z_a))) + \
        (golf * (((1-omicron) * gdf.median_housing_age_change_a) + (omicron * gdf.median_housing_age_2013z_a)))
)
gdf['omega_bar'] = gdf['omega_bar'].fillna(0) #deals with nan in dataframe, which was breaking the network
gdf = gdf[(gdf['omega_bar'] >= threshold)]


#gdf.loc[gdf.omega < 0, 'omega'] = None #corrects for the census having "2018" as an answer to some of these
gdf = gdf[(gdf['omega'] >= threshold)]

#gdf['omega'] = gdf['omega'] / gdf['omega'].max() #normalize so edges don't go nuts

#gdf = gdf[gdf['distance'] < 3500] #filter, is only necessary if you need to threshold this and also don't use one of the subset dfs below.

#create cityname df
muni_gdf = gp.read_file(os.path.join(ROOTDIR, 'shapefiles/Municipal_Boundaries/Municipal_Boundaries.shp'))
tract_gdf = gp.read_file(os.path.join(ROOTDIR, 'shapefiles/KingCountyTracts/kc_tract_10.shp'))
t = tract_gdf[['OBJECTID', 'STATEFP10', 'COUNTYFP10', 'TRACTCE10', 'GEOID10', 'geometry']]
m = muni_gdf[['OBJECTID', 'CITYNAME', 'geometry']]
m = m.to_crs(epsg=2926)
#pd.options.display.max_rows = 500
mt = gp.sjoin(t, m, how='left', op='intersects', lsuffix='', rsuffix='_muni')
mt[['GEOID10', 'CITYNAME']]

#merge with cityname df
#df = df.merge(mt, how = 'inner', left_on = ['GEOID'], right_on = ['GEOID10']) #DON'T DO THIS UNTIL CITIES ASSIGNED TO BLOCK GROUPS


#df = df.rename(columns = {'CITYNAME_y':'CITYNAME'})

import itertools

#create mtbaker_station_df & mtbaker_station_gdf
mtbaker_station_gdf = gdf[((gdf['GEOID_a'] == '530330100011') & (gdf['distance'] < 1.500)) | ((gdf['GEOID_b'] == '530330100011') & (gdf['distance'] < 1.500))]
mtbaker_station_gid_a = list(mtbaker_station_gdf['GEOID_a'].drop_duplicates())
mtbaker_station_gid_b = list(mtbaker_station_gdf['GEOID_b'].drop_duplicates())

mtbaker_station_pair_data = {
    'GEOID_a': list(),
    'GEOID_b': list()
}

for ga, gb in itertools.product(mtbaker_station_gid_a + mtbaker_station_gid_b, mtbaker_station_gid_a + mtbaker_station_gid_b):
    mtbaker_station_pair_data['GEOID_a'].append(ga)
    mtbaker_station_pair_data['GEOID_b'].append(gb)

mtbaker_station_pair_df = pd.DataFrame.from_dict(mtbaker_station_pair_data)
mtbaker_station_pair_df = mtbaker_station_pair_df.merge(gdf, how='left', on=['GEOID_a', 'GEOID_b'])
mtbaker_station_pair_df = mtbaker_station_pair_df[~mtbaker_station_pair_df['distance'].isnull()]

mtbaker_station_gdf = mtbaker_station_pair_df
mtbaker_station_geoids = list(mtbaker_station_gdf['GEOID_a'].drop_duplicates()) + \
                     list(mtbaker_station_gdf['GEOID_b'].drop_duplicates())
mtbaker_station_df = df[df['GEOID'].isin(mtbaker_station_geoids)]
mtbaker_station_df['neighborhood'] = 'mtbaker_station'

#create othello_station_df & othello_station_gdf
othello_station_gdf = gdf[((gdf['GEOID_a'] == '530330110012') & (gdf['distance'] < 1.500)) | ((gdf['GEOID_b'] == '530330110012') & (gdf['distance'] < 1.500))]
othello_station_gid_a = list(othello_station_gdf['GEOID_a'].drop_duplicates())
othello_station_gid_b = list(othello_station_gdf['GEOID_b'].drop_duplicates())

othello_station_pair_data = {
    'GEOID_a': list(),
    'GEOID_b': list()
}

for ga, gb in itertools.product(othello_station_gid_a + othello_station_gid_b, othello_station_gid_a + othello_station_gid_b):
    othello_station_pair_data['GEOID_a'].append(ga)
    othello_station_pair_data['GEOID_b'].append(gb)

othello_station_pair_df = pd.DataFrame.from_dict(othello_station_pair_data)
othello_station_pair_df = othello_station_pair_df.merge(gdf, how='left', on=['GEOID_a', 'GEOID_b'])
othello_station_pair_df = othello_station_pair_df[~othello_station_pair_df['distance'].isnull()]

othello_station_gdf = othello_station_pair_df
othello_station_geoids = list(othello_station_gdf['GEOID_a'].drop_duplicates()) + \
                     list(othello_station_gdf['GEOID_b'].drop_duplicates())
othello_station_df = df[df['GEOID'].isin(othello_station_geoids)]
othello_station_df['neighborhood'] = 'othello_station'

#create rainier_beach_df & rainier_beach_gdf
rainier_beach_gdf = gdf[((gdf['GEOID_a'] == '530330117001') & (gdf['distance'] < 2)) | ((gdf['GEOID_b'] == '530330117001') & (gdf['distance'] < 2))]
rainier_beach_gid_a = list(rainier_beach_gdf['GEOID_a'].drop_duplicates())
rainier_beach_gid_b = list(rainier_beach_gdf['GEOID_b'].drop_duplicates())

rainier_beach_pair_data = {
    'GEOID_a': list(),
    'GEOID_b': list()
}

for ga, gb in itertools.product(rainier_beach_gid_a + rainier_beach_gid_b, rainier_beach_gid_a + rainier_beach_gid_b):
    rainier_beach_pair_data['GEOID_a'].append(ga)
    rainier_beach_pair_data['GEOID_b'].append(gb)

rainier_beach_pair_df = pd.DataFrame.from_dict(rainier_beach_pair_data)
rainier_beach_pair_df = rainier_beach_pair_df.merge(gdf, how='left', on=['GEOID_a', 'GEOID_b'])
rainier_beach_pair_df = rainier_beach_pair_df[~rainier_beach_pair_df['distance'].isnull()]

rainier_beach_gdf = rainier_beach_pair_df
rainier_beach_geoids = list(rainier_beach_gdf['GEOID_a'].drop_duplicates()) + \
                     list(rainier_beach_gdf['GEOID_b'].drop_duplicates())
rainier_beach_df = df[df['GEOID'].isin(rainier_beach_geoids)]
rainier_beach_df['neighborhood'] = 'rainier_beach'

#create wallingford_df & wallingford_gdf
wallingford_gdf = gdf[((gdf['GEOID_a'] == '530330046001') & (gdf['distance'] < 3.000)) | ((gdf['GEOID_b'] == '530330046001') & (gdf['distance'] < 3.000))]
wallingford_gid_a = list(wallingford_gdf['GEOID_a'].drop_duplicates())
wallingford_gid_b = list(wallingford_gdf['GEOID_b'].drop_duplicates())

wallingford_pair_data = {
    'GEOID_a': list(),
    'GEOID_b': list()
}

for ga, gb in itertools.product(wallingford_gid_a + wallingford_gid_b, wallingford_gid_a + wallingford_gid_b):
    wallingford_pair_data['GEOID_a'].append(ga)
    wallingford_pair_data['GEOID_b'].append(gb)

wallingford_pair_df = pd.DataFrame.from_dict(wallingford_pair_data)
wallingford_pair_df = wallingford_pair_df.merge(gdf, how='left', on=['GEOID_a', 'GEOID_b'])
wallingford_pair_df = wallingford_pair_df[~wallingford_pair_df['distance'].isnull()]

wallingford_gdf = wallingford_pair_df
wallingford_geoids = list(wallingford_gdf['GEOID_a'].drop_duplicates()) + \
                     list(wallingford_gdf['GEOID_b'].drop_duplicates())
wallingford_df = df[df['GEOID'].isin(wallingford_geoids)]
wallingford_df['neighborhood'] = 'wallingford'

def get_df(subset='all'):
    subsets = {
        'all': df,
        'mtbaker_station': mtbaker_station_df,
        'othello_station': othello_station_df,
        'rainier_beach': rainier_beach_df,
        'wallingford': wallingford_df
    }

    if subset in subsets:
        return subsets[subset]
    else:
        raise('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))


def get_gdf(subset='all'):
    subsets = {
        'all': gdf,
        'mtbaker_station': mtbaker_station_gdf,
        'othello_station': othello_station_gdf,
        'rainier_beach': rainier_beach_gdf,
        'wallingford': wallingford_gdf
    }

    if subset in subsets:
        return subsets[subset]
    else:
        raise ('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))
