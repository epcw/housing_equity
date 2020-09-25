import pandas as pd
import geopandas as gp
from geopy import distance
from sklearn.cluster import KMeans

df_rent = pd.read_csv('data/king_blockgrp_rent.csv', dtype={"GEOID": str, "TRACT_NUM": str, "YEAR":str, "BLOCK_GRP":str}) #NOTE: pre-filtered in SQL for King County

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
rdf = pd.read_csv('data/king_blockgrp_race.csv', dtype={"GEOID": str, "TRACT_NUM": str, "YEAR":str, "BLOCK_GRP":str}) #NOTE: pre-filtered in SQL for King County

#filter for year 2013
rdf = rdf[(rdf['YEAR'] == '2013') | (rdf['YEAR'] == '2018') ]

gdf = pd.read_csv('data/wa_king_census_block_groups_distances.csv',
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
housing_df_raw = pd.read_csv('data/king_blockgrp_housing-details.csv', dtype={"DATA":float,"YEAR":str,"TRACT_NUM": str, "BLOCK_GRP": str})

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
housing_age18 = housing_age_df_raw[(housing_age_df_raw['YEAR'] == '2018')]
housing_age18['median_housing_age_2018'] = 2018 - (housing_age18.DATA)
housing_age18 = housing_age18[['GEOID','COUNTY','TRACT_NUM','BLOCK_GRP','median_housing_age_2018']]
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

#merge dataframes to combine the different datasets so that you can calculate it.
minority = df[['GEOID','minority_pop_pct_change']]
gdf = gdf.merge(minority, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'minority_pop_pct_change':'minority_pop_pct_change_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a']]
gdf = gdf.merge(minority, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'minority_pop_pct_change':'minority_pop_pct_change_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b']]

lower_quartile_rent = df[['GEOID','rent_25th_pctile_change']]
gdf = gdf.merge(lower_quartile_rent, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'rent_25th_pctile_change':'rent_25th_pctile_change_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','rent_25th_pctile_change_a']]
gdf = gdf.merge(lower_quartile_rent, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'rent_25th_pctile_change':'rent_25th_pctile_change_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','rent_25th_pctile_change_a','rent_25th_pctile_change_b']]

totpop = df[['GEOID','totpop_change']]
gdf = gdf.merge(totpop, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'totpop_change':'totpop_change_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','rent_25th_pctile_change_a','rent_25th_pctile_change_b','totpop_change_a']]
gdf = gdf.merge(totpop, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'totpop_change':'totpop_change_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','rent_25th_pctile_change_a','rent_25th_pctile_change_b','totpop_change_a','totpop_change_b']]

rent_pct_income = df[['GEOID','rent_pct_income_change']]
gdf = gdf.merge(rent_pct_income, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'rent_pct_income_change':'rent_pct_income_change_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','rent_25th_pctile_change_a','rent_25th_pctile_change_b','totpop_change_a','totpop_change_b','rent_pct_income_change_a']]
gdf = gdf.merge(rent_pct_income, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'rent_pct_income_change':'rent_pct_income_change_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','rent_25th_pctile_change_a','rent_25th_pctile_change_b','totpop_change_a','totpop_change_b','rent_pct_income_change_a','rent_pct_income_change_b']]

affordable_units_per_cap = df[['GEOID','affordable_units_per_cap_change']]
gdf = gdf.merge(affordable_units_per_cap, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'affordable_units_per_cap_change':'affordable_units_per_cap_change_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','rent_25th_pctile_change_a','rent_25th_pctile_change_b','totpop_change_a','totpop_change_b','rent_pct_income_change_a','rent_pct_income_change_b','affordable_units_per_cap_change_a']]
gdf = gdf.merge(affordable_units_per_cap, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'affordable_units_per_cap_change':'affordable_units_per_cap_change_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','rent_25th_pctile_change_a','rent_25th_pctile_change_b','totpop_change_a','totpop_change_b','rent_pct_income_change_a','rent_pct_income_change_b','affordable_units_per_cap_change_a','affordable_units_per_cap_change_b']]

tenancy = df[['GEOID','median_tenancy_change']]
gdf = gdf.merge(tenancy, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'median_tenancy_change':'median_tenancy_change_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','rent_25th_pctile_change_a','rent_25th_pctile_change_b','totpop_change_a','totpop_change_b','rent_pct_income_change_a','rent_pct_income_change_b','affordable_units_per_cap_change_a','affordable_units_per_cap_change_b','median_tenancy_change_a']]
gdf = gdf.merge(tenancy, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'median_tenancy_change':'median_tenancy_change_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','rent_25th_pctile_change_a','rent_25th_pctile_change_b','totpop_change_a','totpop_change_b','rent_pct_income_change_a','rent_pct_income_change_b','affordable_units_per_cap_change_a','affordable_units_per_cap_change_b','median_tenancy_change_a','median_tenancy_change_b']]

housing_age = df[['GEOID','median_housing_age_change']]
gdf = gdf.merge(housing_age, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'median_housing_age_change':'median_housing_age_change_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','rent_25th_pctile_change_a','rent_25th_pctile_change_b','totpop_change_a','totpop_change_b','rent_pct_income_change_a','rent_pct_income_change_b','affordable_units_per_cap_change_a','affordable_units_per_cap_change_b','median_tenancy_change_a','median_tenancy_change_b','median_housing_age_change_a']]
gdf = gdf.merge(housing_age, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'median_housing_age_change':'median_housing_age_change_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','rent_25th_pctile_change_a','rent_25th_pctile_change_b','totpop_change_a','totpop_change_b','rent_pct_income_change_a','rent_pct_income_change_b','affordable_units_per_cap_change_a','affordable_units_per_cap_change_b','median_tenancy_change_a','median_tenancy_change_b','median_housing_age_change_a','median_housing_age_change_b']]

#calculate diff between the two tracts (and take absolute value since sign is meaningless here)
gdf['minority_pop_pct_change_delta'] = (gdf.minority_pop_pct_change_a - gdf.minority_pop_pct_change_b).abs()
gdf['minority_pop_pct_change_delta'] = gdf['minority_pop_pct_change_delta'].fillna(0) #deals with nan in dataframe, which was breaking the network
gdf['rent_25th_pctile_change_delta'] = (gdf.rent_25th_pctile_change_a - gdf.rent_25th_pctile_change_b).abs()
gdf['rent_25th_pctile_change_delta'] = gdf['rent_25th_pctile_change_delta'].fillna(0)
gdf['totpop_change_delta'] = (gdf.totpop_change_a - gdf.totpop_change_b).abs()
gdf['totpop_change_delta'] = gdf['totpop_change_delta'].fillna(0)
gdf['rent_pct_income_change_delta'] = (gdf.rent_pct_income_change_a - gdf.rent_pct_income_change_b).abs()
gdf['rent_pct_income_change_delta'] = gdf['rent_pct_income_change_delta'].fillna(0)
gdf['affordable_units_per_cap_change_delta'] = (gdf.affordable_units_per_cap_change_a - gdf.affordable_units_per_cap_change_b).abs()
gdf['affordable_units_per_cap_change_delta'] = gdf['affordable_units_per_cap_change_delta'].fillna(0)
gdf['median_tenancy_change_delta'] = (gdf.median_tenancy_change_a - gdf.median_tenancy_change_b).abs()
gdf['median_tenancy_change_delta'] = gdf['median_tenancy_change_delta'].fillna(0)
gdf['median_housing_age_change_delta'] = (gdf.median_housing_age_change_a - gdf.median_housing_age_change_b).abs()
gdf['median_housing_age_change_delta'] = gdf['median_housing_age_change_delta'].fillna(0)

#Kmeans clustering
Y = df[['GEOID','rent_25th_pctile_change','minority_pop_pct_change']]
Y = Y[~Y['minority_pop_pct_change'].isnull()]
Y = Y[~Y['rent_25th_pctile_change'].isnull()]
X = Y[['rent_25th_pctile_change','minority_pop_pct_change']]
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
df = df.merge(Y, how='left', left_on=['GEOID','minority_pop_pct_change','rent_25th_pctile_change'], right_on=['GEOID','minority_pop_pct_change','rent_25th_pctile_change'])

grp0 = df[(df['labels'] == 0)]
grp0 = grp0[['COUNTY','TRACT_NUM','BLOCK_GRP','minority_pop_pct_change','rent_25th_pctile_change','labels','d']]
grp0_length = str(grp0.shape)
grp1 = df[(df['labels'] == 1)]
grp1 = grp1[['COUNTY','TRACT_NUM','BLOCK_GRP','minority_pop_pct_change','rent_25th_pctile_change','labels','d']]
grp1_length = str(grp1.shape)

grp2 = df[(df['labels'] == 2)]
grp2 = grp2[['COUNTY','TRACT_NUM','BLOCK_GRP','minority_pop_pct_change','rent_25th_pctile_change','labels','d']]
grp2_length = str(grp2.shape)

grp3 = df[(df['labels'] == 3)]
grp3 = grp3[['COUNTY','TRACT_NUM','BLOCK_GRP','minority_pop_pct_change','rent_25th_pctile_change','labels','d']]
grp3_length = str(grp3.shape)

# TODO: REAL WEIGHTS TO ACCOUNT FOR SCALE OF MEASUREMENTS. MAYBE Z-SCORE EVERYTHING
#weight the edges
alpha = 1/7.0
bravo = 1/7.0
charlie = 1/7.0
delta = 1/7.0
echo = 1/7.0
foxtrot = 1/7.0
golf = 1/7.0

gdf['omega'] = ((alpha * gdf.minority_pop_pct_change_delta) + (bravo * gdf.rent_25th_pctile_change_delta) + (charlie * gdf.totpop_change_delta) + (delta * gdf.rent_pct_income_change_delta) + (echo * gdf.affordable_units_per_cap_change_delta) + (foxtrot * gdf.median_tenancy_change_delta) + (golf * gdf.median_housing_age_change_delta))
gdf['omega'] = gdf['omega'] / gdf['omega'].max() #normalize so edges don't go nuts

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
#df = df.merge(mt, how = 'inner', left_on = ['GEOID'], right_on = ['GEOID10']) #DON'T DO THIS UNTIL CITIES ASSIGNED TO BLOCK GROUPS


#df = df.rename(columns = {'CITYNAME_y':'CITYNAME'})

import itertools

wallingford_gdf = gdf[((gdf['GEOID_a'] == '530330046001') & (gdf['distance'] < 3.000)) | ((gdf['GEOID_b'] == '530330046001') & (gdf['distance'] < 3.000))]
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


#delete unnecessary columns to save memory
#del df['OBJECTID_']
#del df['GEOID10']
#del df['TRACTCE10']
#del gdf['GEOID_x']
#del gdf['GEOID_y']

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
