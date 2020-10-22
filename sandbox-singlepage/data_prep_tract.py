import pandas as pd
import re
import csv
import json

#set root directory for data files
#ROOTBEER = '/home/ubuntu/housing_equity/sandbox-singlepage/' #production
ROOTBEER = '' #local

with open(ROOTBEER + 'data/washingtongeo.json','r') as GeoJSON:
    tracts = json.load(GeoJSON)

df_raw = pd.read_csv(ROOTBEER + 'data/totalpop-tract.csv', dtype={"GEOID": str,"TRACT_NUM": str,"YEAR":str})
df13_raw = df_raw[(df_raw['YEAR'] == '2013')]
df13_raw = df13_raw.rename(columns = {'DATA' : 'TOT_POP_2013'})
df13_raw = df13_raw[['GEOID','COUNTY','TRACT_NUM','TOT_POP_2013']]
df18_raw = df_raw[(df_raw['YEAR'] == '2018')]
df18_raw = df18_raw.rename(columns = {'DATA' : 'TOT_POP_2018'})
df18_raw = df18_raw[['GEOID','COUNTY','TRACT_NUM','TOT_POP_2018']]
df = df13_raw.merge(df18_raw, how='left', left_on=['GEOID','COUNTY','TRACT_NUM'], right_on=['GEOID','COUNTY','TRACT_NUM'])

#bring in affordable housing data
housing_df_raw = pd.read_csv(ROOTBEER + 'data/affordable_housing_units-allyears-tract.csv', dtype={"TRACT_NUM": str,"YEAR":str,"GEOID":str}) #prefiltered for King County
housing_df_totalunits = pd.read_csv(ROOTBEER + 'data/totalunits-tracts.csv', dtype={"TRACT_NUM": str,"YEAR":str,"GEOID":str}) #prefiltered for King County

#filter for Year
housing_df13 = housing_df_raw[(housing_df_raw['YEAR'] == '2013')]
housing_df18 = housing_df_raw[(housing_df_raw['YEAR'] == '2018')]
housingtotal_df13 = housing_df_totalunits[(housing_df_totalunits['YEAR'] == '2013')]
housingtotal_df18 = housing_df_totalunits[(housing_df_totalunits['YEAR'] == '2018')]

#Aggregate unit data (rows in original housing_df_raw are counts of units under 100/mo, 200/mo, 300/mo, etc.
housing_data13 = housing_df13.groupby(['GEOID','TRACT_NUM','COUNTY']).sum().reset_index()
housing_data13 = housing_data13.rename(columns = {'DATA' : 'sub_600_per_mo_housing_units_2013'})
housing_data18 = housing_df18.groupby(['GEOID','TRACT_NUM','COUNTY']).sum().reset_index()
housing_data18 = housing_data18.rename(columns = {'DATA' : 'sub_600_per_mo_housing_units_2018'})
housingtotal_df13 = housingtotal_df13.rename(columns = {'DATA' : 'total_housing_units_2013'})
housingtotal_df18 = housingtotal_df18.rename(columns = {'DATA' : 'total_housing_units_2018'})
housing_df = housing_data13.merge(housing_data18, how='left', left_on=['GEOID','TRACT_NUM','COUNTY'], right_on=['GEOID','TRACT_NUM','COUNTY'])
housing_df = housing_df.merge(housingtotal_df13, how='left', left_on=['GEOID','TRACT_NUM','COUNTY'], right_on=['GEOID','TRACT_NUM','COUNTY'])
housing_df = housing_df.merge(housingtotal_df18, how='left', left_on=['GEOID','TRACT_NUM','COUNTY'], right_on=['GEOID','TRACT_NUM','COUNTY'])

#bring in tenancy, cost, and occupancy data and filter for 2010 & 2018
housing_details_raw = pd.read_csv(ROOTBEER + 'data/housing_details.csv', dtype={"TRACT_NUM": str, "GEOID": str, "YEAR":int}) #NOTE: pre-filtered in SQL for King County
housing_details_raw['DATA'] = housing_details_raw['DATA'].astype(str).map(lambda x: x.rstrip('+-'))
housing_details_raw['DATA'] = housing_details_raw['DATA'].astype(float)
housing_details13 = housing_details_raw[(housing_details_raw['YEAR'] == 2013)]
housing_details18 = housing_details_raw[(housing_details_raw['YEAR'] == 2018)]

#sort median_costs_df by census query, creating new column-sorted dfs instead of rows
costs_13f25 = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25057_001E')]
costs_13f25['DATA'] = costs_13f25['DATA'].astype(float)
costs_13f25 = costs_13f25.rename(columns = {'DATA' : 'RENT_25PCTILE_2013'})
costs_13f25 = costs_13f25[['GEOID','RENT_25PCTILE_2013','COUNTY','TRACT_NUM']]
costs_13f50 = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25058_001E')]
costs_13f50 = costs_13f50.rename(columns = {'DATA' : 'RENT_50PCTILE_2013'})
costs_13f50 = costs_13f50[['GEOID','RENT_50PCTILE_2013','COUNTY','TRACT_NUM']]
costs_13f75 = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25059_001E')]
costs_13f75 = costs_13f75.rename(columns = {'DATA' : 'RENT_75PCTILE_2013'})
costs_13f75 = costs_13f75[['GEOID','RENT_75PCTILE_2013','COUNTY','TRACT_NUM']]
costs_13fpct = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25071_001E')]
costs_13fpct['DATA'] = costs_13fpct['DATA'].astype(float)
costs_13fpct = costs_13fpct.rename(columns = {'DATA' : 'RENT_AS_PCT_HOUSEHOLD_INCOME_2013'})
costs_13fpct = costs_13fpct[['GEOID','RENT_AS_PCT_HOUSEHOLD_INCOME_2013','COUNTY','TRACT_NUM']]
costs_13fmedcost = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25105_001E')]
costs_13fmedcost = costs_13fmedcost.rename(columns = {'DATA' : 'MEDIAN_MONTHLY_HOUSING_COST_2013'})
costs_13fmedcost['MEDIAN_MONTHLY_HOUSING_COST_2013'] = costs_13fmedcost['MEDIAN_MONTHLY_HOUSING_COST_2013'].astype(float)
costs_13fmedcost = costs_13fmedcost[['GEOID','MEDIAN_MONTHLY_HOUSING_COST_2013','COUNTY','TRACT_NUM']]
costs_13f = costs_13f25.merge(costs_13f50, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
costs_13f = costs_13f.merge(costs_13f75, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
costs_13f = costs_13f.merge(costs_13fpct, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
costs_13f = costs_13f.merge(costs_13fmedcost, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])

costs_18df25 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25057_001E')]
costs_18df25['DATA'] = costs_18df25['DATA'].astype(float)
costs_18df25 = costs_18df25.rename(columns = {'DATA' : 'RENT_25PCTILE_2018'})
costs_18df25 = costs_18df25[['GEOID','RENT_25PCTILE_2018','COUNTY','TRACT_NUM']]
costs_18df50 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25058_001E')]
costs_18df50 = costs_18df50.rename(columns = {'DATA' : 'RENT_50PCTILE_2018'})
costs_18df50 = costs_18df50[['GEOID','RENT_50PCTILE_2018','COUNTY','TRACT_NUM']]
costs_18df75 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25059_001E')]
costs_18df75 = costs_18df75.rename(columns = {'DATA' : 'RENT_75PCTILE_2018'})
costs_18df75 = costs_18df75[['GEOID','RENT_75PCTILE_2018','COUNTY','TRACT_NUM']]
costs_18dfpct = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25071_001E')]
costs_18dfpct['DATA'] = costs_18dfpct['DATA'].astype(float)
costs_18dfpct = costs_18dfpct.rename(columns = {'DATA' : 'RENT_AS_PCT_HOUSEHOLD_INCOME_2018'})
costs_18dfpct = costs_18dfpct[['GEOID','RENT_AS_PCT_HOUSEHOLD_INCOME_2018','COUNTY','TRACT_NUM']]
costs_18dfmedcost = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25105_001E')]
costs_18dfmedcost = costs_18dfmedcost.rename(columns = {'DATA' : 'MEDIAN_MONTHLY_HOUSING_COST_2018'})
costs_18dfmedcost['MEDIAN_MONTHLY_HOUSING_COST_2018'] = costs_18dfmedcost['MEDIAN_MONTHLY_HOUSING_COST_2018'].astype(float)
costs_18dfmedcost = costs_18dfmedcost[['GEOID','MEDIAN_MONTHLY_HOUSING_COST_2018','COUNTY','TRACT_NUM']]
costs_18df = costs_18df25.merge(costs_18df50, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
costs_18df = costs_18df.merge(costs_18df75, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
costs_18df = costs_18df.merge(costs_18dfpct, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
costs_18df = costs_18df.merge(costs_18dfmedcost, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])

#merge into main df
df = df.merge(housing_df, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
df['sub_600_units_per_capita_2013'] = df['sub_600_per_mo_housing_units_2013']/df['TOT_POP_2013']
df['sub_600_units_per_capita_2018'] = df['sub_600_per_mo_housing_units_2018']/df['TOT_POP_2018']
df['total_housing_units_per_capita_2013'] = df['total_housing_units_2013']/df['TOT_POP_2013']
df['total_housing_units_per_capita_2018'] = df['total_housing_units_2018']/df['TOT_POP_2018']
df['over_600_units_per_capita_2013'] = (df['total_housing_units_per_capita_2013'] - df['sub_600_units_per_capita_2013']) / df['total_housing_units_per_capita_2013']
df['over_600_units_per_capita_2018'] = (df['total_housing_units_per_capita_2018'] - df['sub_600_units_per_capita_2018']) / df['total_housing_units_per_capita_2018']

df = df.merge(costs_13f, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
df = df.merge(costs_18df, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])

#occupancy and housing age data
#occupancydf_units13 = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25002_001E')]
#occupancydf_units13['DATA'] = occupancydf_units13['DATA'].astype(float)
#occupancydf_units13 = occupancydf_units13.rename(columns = {'DATA' : 'housing_units_2013'})
#occupancydf_units13 = occupancydf_units13[['GEOID','housing_units_2013','COUNTY','TRACT_NUM']]
#occupancydf_occupied13 = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25002_002E')]
#occupancydf_occupied13['DATA'] = occupancydf_occupied13['DATA'].astype(float)
#occupancydf_occupied13 = occupancydf_occupied13.rename(columns = {'DATA' : 'housing_occupied_2013'})
#occupancydf_occupied13 = occupancydf_occupied13[['GEOID','housing_occupied_2013','COUNTY','TRACT_NUM']]
#occupancydf_vacant13 = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25002_003E')]
#occupancydf_vacant13['DATA'] = occupancydf_vacant13['DATA'].astype(float)
#occupancydf_vacant13 = occupancydf_vacant13.rename(columns = {'DATA' : 'housing_vacant_2013'})
#occupancydf_vacant13 = occupancydf_vacant13[['GEOID','housing_vacant_2013','COUNTY','TRACT_NUM']]
occupancydf_built13 = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25037_001E')]
occupancydf_built13['DATA'] = occupancydf_built13['DATA'].astype(float)
occupancydf_built13 = occupancydf_built13.rename(columns = {'DATA' : 'housing_yr_built_2013'})
occupancydf_built13 = occupancydf_built13[['GEOID','housing_yr_built_2013','COUNTY','TRACT_NUM']]
#occupancydf_built_owned13 = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25037_002E')]
#occupancydf_built_owned13['DATA'] = occupancydf_built_owned13['DATA'].astype(float)
#occupancydf_built_owned13 = occupancydf_built_owned13.rename(columns = {'DATA' : 'housing_yr_built_owned_2013'})
#occupancydf_built_owned13 = occupancydf_built_owned13[['GEOID','housing_yr_built_owned_2013','COUNTY','TRACT_NUM']]
#occupancydf_built_rented13 = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25037_003E')]
#occupancydf_built_rented13['DATA'] = occupancydf_built_rented13['DATA'].astype(float)
#occupancydf_built_rented13 = occupancydf_built_rented13.rename(columns = {'DATA' : 'housing_yr_built_rented_2013'})
#occupancydf_built_rented13 = occupancydf_built_rented13[['GEOID','housing_yr_built_rented_2013','COUNTY','TRACT_NUM']]
occupancydf_tenure13 = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25039_001E')]
occupancydf_tenure13['DATA'] = occupancydf_tenure13['DATA'].astype(float)
occupancydf_tenure13 = occupancydf_tenure13.rename(columns = {'DATA' : 'housing_yr_movein_2013'})
occupancydf_tenure13 = occupancydf_tenure13[['GEOID','housing_yr_movein_2013','COUNTY','TRACT_NUM']]
#occupancydf_tenure_owned13 = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25039_002E')]
#occupancydf_tenure_owned13['DATA'] = occupancydf_tenure_owned13['DATA'].astype(float)
#occupancydf_tenure_owned13 = occupancydf_tenure_owned13.rename(columns = {'DATA' : 'housing_yr_movein_owned_2013'})
#occupancydf_tenure_owned13 = occupancydf_tenure_owned13[['GEOID','housing_yr_movein_owned_2013','COUNTY','TRACT_NUM']]
#occupancydf_tenure_rented13 = housing_details13[(housing_details13['CENSUS_QUERY'] == 'B25039_003E')]
#occupancydf_tenure_rented13['DATA'] = occupancydf_tenure_rented13['DATA'].astype(float)
#occupancydf_tenure_rented13 = occupancydf_tenure_rented13.rename(columns = {'DATA' : 'housing_yr_movein_rented_2013'})
#occupancydf_tenure_rented13 = occupancydf_tenure_rented13[['GEOID','housing_yr_movein_rented_2013','COUNTY','TRACT_NUM']]
#occupancydf13 = occupancydf_units13.merge(occupancydf_occupied13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#occupancydf13 = occupancydf13.merge(occupancydf_vacant13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#occupancydf13 = occupancydf_units13.merge(occupancydf_built13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#occupancydf13 = occupancydf13.merge(occupancydf_built_owned13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#occupancydf13 = occupancydf13.merge(occupancydf_built_rented13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf13 = occupancydf_built13.merge(occupancydf_tenure13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#occupancydf13 = occupancydf13.merge(occupancydf_tenure_owned13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#occupancydf13 = occupancydf13.merge(occupancydf_tenure_rented13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()

df = df.merge(occupancydf13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#df['occupancy_pct13'] = (df['housing_occupied_2013'] / df['housing_units_2013']) * 100
#df['vacancy_pct13'] = (df['housing_vacant_2013'] / df['housing_units_2013']) * 100
df['housing_age13'] = 2013 - df['housing_yr_built_2013']
#df['housing_age_owned13'] = 2013 - df['housing_yr_built_owned_2013']
#df['housing_age_rented13'] = 2013 - df['housing_yr_built_rented_2013']
df['housing_tenure13'] = 2013 - df['housing_yr_movein_2013']
#df['housing_tenure_owned13'] = 2013 - df['housing_yr_movein_owned_2013']
#df['housing_tenure_rented13'] = 2013 - df['housing_yr_movein_rented_2013']

#occupancydf_units18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25002_001E')]
#occupancydf_units18['DATA'] = occupancydf_units18['DATA'].astype(float)
#occupancydf_units18 = occupancydf_units18.rename(columns = {'DATA' : 'housing_units_2018'})
#occupancydf_units18 = occupancydf_units18[['GEOID','housing_units_2018','COUNTY','TRACT_NUM']]
#occupancydf_occupied18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25002_002E')]
#occupancydf_occupied18['DATA'] = occupancydf_occupied18['DATA'].astype(float)
#occupancydf_occupied18 = occupancydf_occupied18.rename(columns = {'DATA' : 'housing_occupied_2018'})
#occupancydf_occupied18 = occupancydf_occupied18[['GEOID','housing_occupied_2018','COUNTY','TRACT_NUM']]
#occupancydf_vacant18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25002_003E')]
#occupancydf_vacant18['DATA'] = occupancydf_vacant18['DATA'].astype(float)
#occupancydf_vacant18 = occupancydf_vacant18.rename(columns = {'DATA' : 'housing_vacant_2018'})
#occupancydf_vacant18 = occupancydf_vacant18[['GEOID','housing_vacant_2018','COUNTY','TRACT_NUM']]
occupancydf_built18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25037_001E')]
occupancydf_built18['DATA'] = occupancydf_built18['DATA'].astype(float)
occupancydf_built18 = occupancydf_built18.rename(columns = {'DATA' : 'housing_yr_built_2018'})
occupancydf_built18 = occupancydf_built18[['GEOID','housing_yr_built_2018','COUNTY','TRACT_NUM']]
#occupancydf_built_owned18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25037_002E')]
#occupancydf_built_owned18['DATA'] = occupancydf_built_owned18['DATA'].astype(float)
#occupancydf_built_owned18 = occupancydf_built_owned18.rename(columns = {'DATA' : 'housing_yr_built_owned_2018'})
#occupancydf_built_owned18 = occupancydf_built_owned18[['GEOID','housing_yr_built_owned_2018','COUNTY','TRACT_NUM']]
#occupancydf_built_rented18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25037_003E')]
#occupancydf_built_rented18['DATA'] = occupancydf_built_rented18['DATA'].astype(float)
#occupancydf_built_rented18 = occupancydf_built_rented18.rename(columns = {'DATA' : 'housing_yr_built_rented_2018'})
#occupancydf_built_rented18 = occupancydf_built_rented18[['GEOID','housing_yr_built_rented_2018','COUNTY','TRACT_NUM']]
occupancydf_tenure18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25039_001E')]
occupancydf_tenure18['DATA'] = occupancydf_tenure18['DATA'].astype(float)
occupancydf_tenure18 = occupancydf_tenure18.rename(columns = {'DATA' : 'housing_yr_movein_2018'})
occupancydf_tenure18 = occupancydf_tenure18[['GEOID','housing_yr_movein_2018','COUNTY','TRACT_NUM']]
#occupancydf_tenure_owned18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25039_002E')]
#occupancydf_tenure_owned18['DATA'] = occupancydf_tenure_owned18['DATA'].astype(float)
#occupancydf_tenure_owned18 = occupancydf_tenure_owned18.rename(columns = {'DATA' : 'housing_yr_movein_owned_2018'})
#occupancydf_tenure_owned18 = occupancydf_tenure_owned18[['GEOID','housing_yr_movein_owned_2018','COUNTY','TRACT_NUM']]
#occupancydf_tenure_rented18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25039_003E')]
#occupancydf_tenure_rented18['DATA'] = occupancydf_tenure_rented18['DATA'].astype(float)
#occupancydf_tenure_rented18 = occupancydf_tenure_rented18.rename(columns = {'DATA' : 'housing_yr_movein_rented_2018'})
#occupancydf_tenure_rented18 = occupancydf_tenure_rented18[['GEOID','housing_yr_movein_rented_2018','COUNTY','TRACT_NUM']]
#occupancydf18 = occupancydf_units18.merge(occupancydf_occupied18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#occupancydf18 = occupancydf18.merge(occupancydf_vacant18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#occupancydf18 = occupancydf18.merge(occupancydf_built18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#occupancydf18 = occupancydf18.merge(occupancydf_built_owned18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#occupancydf18 = occupancydf18.merge(occupancydf_built_rented18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf18 = occupancydf_built18.merge(occupancydf_tenure18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#occupancydf18 = occupancydf18.merge(occupancydf_tenure_owned18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#occupancydf18 = occupancydf18.merge(occupancydf_tenure_rented18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()

df = df.merge(occupancydf18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
#df['occupancy_pct18'] = (df['housing_occupied_2018'] / df['housing_units_2018']) * 180
#df['vacancy_pct18'] = (df['housing_vacant_2018'] / df['housing_units_2018']) * 180
df['housing_age18'] = 2018 - df['housing_yr_built_2018']
#df['housing_age_owned18'] = 2018 - df['housing_yr_built_owned_2018']
#df['housing_age_rented18'] = 2018 - df['housing_yr_built_rented_2018']
df['housing_tenure18'] = 2018 - df['housing_yr_movein_2018']
#df['housing_tenure_owned18'] = 2018 - df['housing_yr_movein_owned_2018']
#df['housing_tenure_rented18'] = 2018 - df['housing_yr_movein_rented_2018']

#displays missing data on house age as Nan instead of 0, to filter out erroneous results that claim houses were built in year "0"
df.loc[df.housing_age13 > 100, 'housing_age13'] = None
df.loc[df.housing_age18 > 100, 'housing_age18'] = None
#df.loc[df.housing_age_owned10 > 100, 'housing_age_owned10'] = None
#df.loc[df.housing_age_owned18 > 100, 'housing_age_owned18'] = None
#df.loc[df.housing_age_rented10 > 100, 'housing_age_rented10'] = None
#df.loc[df.housing_age_rented18 > 100, 'housing_age_rented18'] = None

rdf = pd.read_csv(ROOTBEER + 'data/race-data.csv', dtype={"TRACT_NUM": str, "YEAR": str})

#filter for King County 2010
rdf13 = rdf[(rdf['COUNTY'] == 'King') & (rdf['YEAR'] == '2013')]

#filter for King County 2018
rdf18 = rdf[(rdf['COUNTY'] == 'King') & (rdf['YEAR'] == '2018')]

#create GEOID
rdf13['GEOID'] = '53033' + rdf13['TRACT_NUM']
rdf18['GEOID'] = '53033' + rdf18['TRACT_NUM']

#racial percentages
white13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B03002_003E')]
white13 = white13[['GEOID','COUNTY','TRACT_NUM','DATA']]
white13 = white13.rename(columns = {'DATA' : 'pop_white_nonhisp_only_2013'})
black13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B02001_003E')]
black13 = black13[['GEOID','COUNTY','TRACT_NUM','DATA']]
black13 = black13.rename(columns = {'DATA' : 'pop_black_only_2013'})
native13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B02001_004E')]
native13 = native13[['GEOID','COUNTY','TRACT_NUM','DATA']]
native13 = native13.rename(columns = {'DATA' : 'pop_native_only_2013'})
asian13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B02001_005E')]
asian13 = asian13[['GEOID','COUNTY','TRACT_NUM','DATA']]
asian13 = asian13.rename(columns = {'DATA' : 'pop_asian_only_2013'})
polynesian13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B02001_006E')]
polynesian13 = polynesian13[['GEOID','COUNTY','TRACT_NUM','DATA']]
polynesian13 = polynesian13.rename(columns = {'DATA' : 'pop_polynesian_only_2013'})
latino13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B03002_012E')]
latino13 = latino13[['GEOID','COUNTY','TRACT_NUM','DATA']]
latino13 = latino13.rename(columns = {'DATA' : 'pop_hispanic_2013'})
other13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B02001_007E')]
other13 = other13[['GEOID','COUNTY','TRACT_NUM','DATA']]
other13 = other13.rename(columns = {'DATA' : 'pop_other_only_2013'})
multiracial13 = rdf13[(rdf13['CENSUS_QUERY'] == 'B02001_008E')]
multiracial13 = multiracial13[['GEOID','COUNTY','TRACT_NUM','DATA']]
multiracial13 = multiracial13.rename(columns = {'DATA' : 'pop_multiracial_2013'})
racial13 = white13.merge(black13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial13 = racial13.merge(native13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial13 = racial13.merge(asian13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial13 = racial13.merge(polynesian13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial13 = racial13.merge(latino13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial13 = racial13.merge(other13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial13 = racial13.merge(multiracial13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
race_data13 = racial13[['GEOID','COUNTY','TRACT_NUM','pop_white_nonhisp_only_2013','pop_black_only_2013','pop_native_only_2013','pop_asian_only_2013','pop_polynesian_only_2013','pop_hispanic_2013','pop_other_only_2013','pop_multiracial_2013']]

df = df.merge(race_data13, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])

white18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B03002_003E')]
white18 = white18[['GEOID','COUNTY','TRACT_NUM','DATA']]
white18 = white18.rename(columns = {'DATA' : 'pop_white_nonhisp_only_2018'})
black18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_003E')]
black18 = black18[['GEOID','COUNTY','TRACT_NUM','DATA']]
black18 = black18.rename(columns = {'DATA' : 'pop_black_only_2018'})
native18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_004E')]
native18 = native18[['GEOID','COUNTY','TRACT_NUM','DATA']]
native18 = native18.rename(columns = {'DATA' : 'pop_native_only_2018'})
asian18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_005E')]
asian18 = asian18[['GEOID','COUNTY','TRACT_NUM','DATA']]
asian18 = asian18.rename(columns = {'DATA' : 'pop_asian_only_2018'})
polynesian18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_006E')]
polynesian18 = polynesian18[['GEOID','COUNTY','TRACT_NUM','DATA']]
polynesian18 = polynesian18.rename(columns = {'DATA' : 'pop_polynesian_only_2018'})
latino18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B03002_012E')]
latino18 = latino18[['GEOID','COUNTY','TRACT_NUM','DATA']]
latino18 = latino18.rename(columns = {'DATA' : 'pop_hispanic_2018'})
other18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_007E')]
other18 = other18[['GEOID','COUNTY','TRACT_NUM','DATA']]
other18 = other18.rename(columns = {'DATA' : 'pop_other_only_2018'})
multiracial18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_008E')]
multiracial18 = multiracial18[['GEOID','COUNTY','TRACT_NUM','DATA']]
multiracial18 = multiracial18.rename(columns = {'DATA' : 'pop_multiracial_2018'})
racial18 = white18.merge(black18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial18 = racial18.merge(native18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial18 = racial18.merge(asian18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial18 = racial18.merge(polynesian18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial18 = racial18.merge(latino18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial18 = racial18.merge(other18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial18 = racial18.merge(multiracial18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
race_data18 = racial18[['GEOID','COUNTY','TRACT_NUM','pop_white_nonhisp_only_2018','pop_black_only_2018','pop_native_only_2018','pop_asian_only_2018','pop_polynesian_only_2018','pop_hispanic_2018','pop_other_only_2018','pop_multiracial_2018']]

df = df.merge(race_data18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])

df['minority_pop_2013'] = df['TOT_POP_2013'] - df['pop_white_nonhisp_only_2013']
df['minority_pop_pct_2013'] = df['minority_pop_2013'] / df['TOT_POP_2013']
df['white_pop_pct_2013'] = df['pop_white_nonhisp_only_2013'] / df['TOT_POP_2013']
df['minority_pop_2018'] = df['TOT_POP_2018'] - df['pop_white_nonhisp_only_2018']
df['minority_pop_pct_2018'] = df['minority_pop_2018'] / df['TOT_POP_2018']
df['white_pop_pct_2018'] = df['pop_white_nonhisp_only_2018'] / df['TOT_POP_2018']

gdf = pd.read_csv(ROOTBEER + 'data/washingtongeo_dist.csv',
                   dtype={"TRACTCE_a": str,"TRACTCE_b": str})

#create GEOID
gdf['GEOID_a'] = '53033' + gdf['TRACTCE_a']
gdf['GEOID_b'] = '53033' + gdf['TRACTCE_b']

df['minority_pop_pct_change'] = (df.minority_pop_pct_2018 - df.minority_pop_pct_2013)
df['white_pop_pct_change'] = (df.white_pop_pct_2018 - df.white_pop_pct_2013)
df['rent_25th_pctile_change'] = (df.RENT_25PCTILE_2018 - df.RENT_25PCTILE_2013)
df['totpop_change'] = (df.TOT_POP_2018 - df.TOT_POP_2013)
df['rent_pct_income_change'] = (df.RENT_AS_PCT_HOUSEHOLD_INCOME_2018 - df.RENT_AS_PCT_HOUSEHOLD_INCOME_2013)
df['monthly_housing_cost_change'] = (df.MEDIAN_MONTHLY_HOUSING_COST_2018 - df.MEDIAN_MONTHLY_HOUSING_COST_2013)
df['market_rate_units_per_cap_change'] = (df.over_600_units_per_capita_2018 - df.over_600_units_per_capita_2013)
df['affordable_units_per_cap_change'] = (df.sub_600_units_per_capita_2018 - df.sub_600_units_per_capita_2013)
df['median_tenancy_change'] = (df.housing_tenure18 - df.housing_tenure13)
df['median_housing_age_change'] = (df.housing_age18 - df.housing_age13)

#CONVERT ALL CHANGES TO Z-SCORE SO YOU CAN COMPARE THEM
df['minority_pop_pct_change'] = (df.minority_pop_pct_change - df.minority_pop_pct_change.mean())/df.minority_pop_pct_change.std()
df['white_pop_pct_change'] = (df.white_pop_pct_change - df.white_pop_pct_change.mean())/df.white_pop_pct_change.std()
df['rent_25th_pctile_change'] = (df.rent_25th_pctile_change - df.rent_25th_pctile_change.mean())/df.rent_25th_pctile_change.std()
df['totpop_change'] = (df.totpop_change - df.totpop_change.mean())/df.totpop_change.std()
df['rent_pct_income_change'] = (df.rent_pct_income_change - df.rent_pct_income_change.mean())/df.rent_pct_income_change.std()
df['monthly_housing_cost_change'] = (df.monthly_housing_cost_change - df.monthly_housing_cost_change.mean())/df.monthly_housing_cost_change.std()
df['affordable_units_per_cap_change'] = (df.affordable_units_per_cap_change - df.affordable_units_per_cap_change.mean())/df.affordable_units_per_cap_change.std()
df['market_rate_units_per_cap_change'] = (df.market_rate_units_per_cap_change - df.market_rate_units_per_cap_change.mean())/df.market_rate_units_per_cap_change.std()
df['median_tenancy_change'] = (df.median_tenancy_change - df.median_tenancy_change.mean())/df.median_tenancy_change.std()
df['median_housing_age_change'] = (df.median_housing_age_change - df.median_housing_age_change.mean())/df.median_housing_age_change.std()

#CONVERT 2013 numbers to z-score for comparison
df['minority_pop_pct_2013z'] = (df.minority_pop_pct_2013 - df.minority_pop_pct_2013.mean())/df.minority_pop_pct_2013.std()
df['white_pop_pct_2013z'] = (df.white_pop_pct_2013 - df.white_pop_pct_2013.mean())/df.white_pop_pct_2013.std()
df['rent_25th_pctile_2013z'] = (df.RENT_25PCTILE_2013 - df.RENT_25PCTILE_2013.mean())/df.RENT_25PCTILE_2013.std()
df['totpop_2013z'] = (df.TOT_POP_2013 - df.TOT_POP_2013.mean())/df.TOT_POP_2013.std()
df['rent_pct_income_2013z'] = (df.RENT_AS_PCT_HOUSEHOLD_INCOME_2013 - df.RENT_AS_PCT_HOUSEHOLD_INCOME_2013.mean())/df.RENT_AS_PCT_HOUSEHOLD_INCOME_2013.std()
df['monthly_housing_cost_2013z'] = (df.MEDIAN_MONTHLY_HOUSING_COST_2013 - df.MEDIAN_MONTHLY_HOUSING_COST_2013.mean())/df.MEDIAN_MONTHLY_HOUSING_COST_2013.std()
df['affordable_units_per_cap_2013z'] = (df.sub_600_units_per_capita_2013 - df.sub_600_units_per_capita_2013.mean())/df.sub_600_units_per_capita_2013.std()
df['market_rate_units_per_cap_2013z'] = (df.over_600_units_per_capita_2013 - df.over_600_units_per_capita_2013.mean())/df.over_600_units_per_capita_2013.std()
df['median_tenancy_2013z'] = (df.housing_tenure13 - df.housing_tenure13.mean())/df.housing_tenure13.std()
df['median_housing_age_2013z'] = (df.housing_age18 - df.housing_age18.mean())/df.housing_age18.std()

#CONVERT 2018 numbers to z-score for comparison
df['minority_pop_pct_2018z'] = (df.minority_pop_pct_2018 - df.minority_pop_pct_2018.mean())/df.minority_pop_pct_2018.std()
df['white_pop_pct_2018z'] = (df.white_pop_pct_2018 - df.white_pop_pct_2018.mean())/df.white_pop_pct_2018.std()
df['rent_25th_pctile_2018z'] = (df.RENT_25PCTILE_2018 - df.RENT_25PCTILE_2018.mean())/df.RENT_25PCTILE_2018.std()
df['totpop_2018z'] = (df.TOT_POP_2018 - df.TOT_POP_2018.mean())/df.TOT_POP_2018.std()
df['rent_pct_income_2018z'] = (df.RENT_AS_PCT_HOUSEHOLD_INCOME_2018 - df.RENT_AS_PCT_HOUSEHOLD_INCOME_2018.mean())/df.RENT_AS_PCT_HOUSEHOLD_INCOME_2018.std()
df['monthly_housing_cost_2018z'] = (df.MEDIAN_MONTHLY_HOUSING_COST_2018 - df.MEDIAN_MONTHLY_HOUSING_COST_2018.mean())/df.MEDIAN_MONTHLY_HOUSING_COST_2018.std()
df['affordable_units_per_cap_2018z'] = (df.sub_600_units_per_capita_2018 - df.sub_600_units_per_capita_2018.mean())/df.sub_600_units_per_capita_2018.std()
df['market_rate_units_per_cap_2018z'] = (df.over_600_units_per_capita_2018 - df.over_600_units_per_capita_2018.mean())/df.over_600_units_per_capita_2018.std()
df['median_tenancy_2018z'] = (df.housing_tenure18 - df.housing_tenure18.mean())/df.housing_tenure18.std()
df['median_housing_age_2018z'] = (df.housing_age18 - df.housing_age18.mean())/df.housing_age18.std()

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

white = df[['GEOID','white_pop_pct_change','white_pop_pct_2013z','white_pop_pct_2018z']]
gdf = gdf.merge(white, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'white_pop_pct_change':'white_pop_pct_change_a'})
gdf = gdf.rename(columns = {'white_pop_pct_2013z':'white_pop_pct_2013z_a'})
gdf = gdf.rename(columns = {'white_pop_pct_2018z':'white_pop_pct_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a']]
gdf = gdf.merge(white, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'white_pop_pct_change':'white_pop_pct_change_b'})
gdf = gdf.rename(columns = {'white_pop_pct_2013z':'white_pop_pct_2013z_b'})
gdf = gdf.rename(columns = {'white_pop_pct_2018z':'white_pop_pct_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b']]

lower_quartile_rent = df[['GEOID','rent_25th_pctile_change','rent_25th_pctile_2013z','rent_25th_pctile_2018z']]
gdf = gdf.merge(lower_quartile_rent, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'rent_25th_pctile_change':'rent_25th_pctile_change_a'})
gdf = gdf.rename(columns = {'rent_25th_pctile_2013z':'rent_25th_pctile_2013z_a'})
gdf = gdf.rename(columns = {'rent_25th_pctile_2018z':'rent_25th_pctile_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b']]
gdf = gdf.merge(lower_quartile_rent, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'rent_25th_pctile_change':'rent_25th_pctile_change_b'})
gdf = gdf.rename(columns = {'rent_25th_pctile_2013z':'rent_25th_pctile_2013z_b'})
gdf = gdf.rename(columns = {'rent_25th_pctile_2018z':'rent_25th_pctile_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b']]

totpop = df[['GEOID','totpop_change','totpop_2013z','totpop_2018z']]
gdf = gdf.merge(totpop, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'totpop_change':'totpop_change_a'})
gdf = gdf.rename(columns = {'totpop_2013z':'totpop_2013z_a'})
gdf = gdf.rename(columns = {'totpop_2018z':'totpop_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b']]
gdf = gdf.merge(totpop, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'totpop_change':'totpop_change_b'})
gdf = gdf.rename(columns = {'totpop_2013z':'totpop_2013z_b'})
gdf = gdf.rename(columns = {'totpop_2018z':'totpop_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b']]

rent_pct_income = df[['GEOID','rent_pct_income_change','rent_pct_income_2013z','rent_pct_income_2018z']]
gdf = gdf.merge(rent_pct_income, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'rent_pct_income_change':'rent_pct_income_change_a'})
gdf = gdf.rename(columns = {'rent_pct_income_2013z':'rent_pct_income_2013z_a'})
gdf = gdf.rename(columns = {'rent_pct_income_2018z':'rent_pct_income_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b']]
gdf = gdf.merge(rent_pct_income, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'rent_pct_income_change':'rent_pct_income_change_b'})
gdf = gdf.rename(columns = {'rent_pct_income_2013z':'rent_pct_income_2013z_b'})
gdf = gdf.rename(columns = {'rent_pct_income_2018z':'rent_pct_income_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b']]

monthly_housing_costs = df[['GEOID','monthly_housing_cost_change','monthly_housing_cost_2013z','monthly_housing_cost_2018z']]
gdf = gdf.merge(monthly_housing_costs, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'monthly_housing_cost_change':'monthly_housing_cost_change_a'})
gdf = gdf.rename(columns = {'monthly_housing_cost_2013z':'monthly_housing_cost_2013z_a'})
gdf = gdf.rename(columns = {'monthly_housing_cost_2018z':'monthly_housing_cost_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','monthly_housing_cost_change_a','monthly_housing_cost_2013z_a','monthly_housing_cost_2018z_a','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b']]
gdf = gdf.merge(monthly_housing_costs, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'monthly_housing_cost_change':'monthly_housing_cost_change_b'})
gdf = gdf.rename(columns = {'monthly_housing_cost_2013z':'monthly_housing_cost_2013z_b'})
gdf = gdf.rename(columns = {'monthly_housing_cost_2018z':'monthly_housing_cost_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','monthly_housing_cost_change_a','monthly_housing_cost_2013z_a','monthly_housing_cost_2018z_a','monthly_housing_cost_change_b','monthly_housing_cost_2013z_b','monthly_housing_cost_2018z_b','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b']]

affordable_units_per_cap = df[['GEOID','affordable_units_per_cap_change','affordable_units_per_cap_2013z','affordable_units_per_cap_2018z']]
gdf = gdf.merge(affordable_units_per_cap, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'affordable_units_per_cap_change':'affordable_units_per_cap_change_a'})
gdf = gdf.rename(columns = {'affordable_units_per_cap_2013z':'affordable_units_per_cap_2013z_a'})
gdf = gdf.rename(columns = {'affordable_units_per_cap_2018z':'affordable_units_per_cap_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','monthly_housing_cost_change_a','monthly_housing_cost_2013z_a','monthly_housing_cost_2018z_a','monthly_housing_cost_change_b','monthly_housing_cost_2013z_b','monthly_housing_cost_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b']]
gdf = gdf.merge(affordable_units_per_cap, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'affordable_units_per_cap_change':'affordable_units_per_cap_change_b'})
gdf = gdf.rename(columns = {'affordable_units_per_cap_2013z':'affordable_units_per_cap_2013z_b'})
gdf = gdf.rename(columns = {'affordable_units_per_cap_2018z':'affordable_units_per_cap_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','monthly_housing_cost_change_a','monthly_housing_cost_2013z_a','monthly_housing_cost_2018z_a','monthly_housing_cost_change_b','monthly_housing_cost_2013z_b','monthly_housing_cost_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a','affordable_units_per_cap_change_b','affordable_units_per_cap_2013z_b','affordable_units_per_cap_2018z_b','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b']]

market_rate_units_per_cap = df[['GEOID','market_rate_units_per_cap_change','market_rate_units_per_cap_2013z','market_rate_units_per_cap_2018z']]
gdf = gdf.merge(market_rate_units_per_cap, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'market_rate_units_per_cap_change':'market_rate_units_per_cap_change_a'})
gdf = gdf.rename(columns = {'market_rate_units_per_cap_2013z':'market_rate_units_per_cap_2013z_a'})
gdf = gdf.rename(columns = {'market_rate_units_per_cap_2018z':'market_rate_units_per_cap_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','monthly_housing_cost_change_a','monthly_housing_cost_2013z_a','monthly_housing_cost_2018z_a','monthly_housing_cost_change_b','monthly_housing_cost_2013z_b','monthly_housing_cost_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a','affordable_units_per_cap_change_b','affordable_units_per_cap_2013z_b','affordable_units_per_cap_2018z_b','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b','market_rate_units_per_cap_change_a','market_rate_units_per_cap_2013z_a','market_rate_units_per_cap_2018z_a']]
gdf = gdf.merge(market_rate_units_per_cap, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'market_rate_units_per_cap_change':'market_rate_units_per_cap_change_b'})
gdf = gdf.rename(columns = {'market_rate_units_per_cap_2013z':'market_rate_units_per_cap_2013z_b'})
gdf = gdf.rename(columns = {'market_rate_units_per_cap_2018z':'market_rate_units_per_cap_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','monthly_housing_cost_change_a','monthly_housing_cost_2013z_a','monthly_housing_cost_2018z_a','monthly_housing_cost_change_b','monthly_housing_cost_2013z_b','monthly_housing_cost_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a','affordable_units_per_cap_change_b','affordable_units_per_cap_2013z_b','affordable_units_per_cap_2018z_b','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b','market_rate_units_per_cap_change_a','market_rate_units_per_cap_2013z_a','market_rate_units_per_cap_2018z_a','market_rate_units_per_cap_change_b','market_rate_units_per_cap_2013z_b','market_rate_units_per_cap_2018z_b']]

tenancy = df[['GEOID','median_tenancy_change','median_tenancy_2013z','median_tenancy_2018z']]
gdf = gdf.merge(tenancy, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'median_tenancy_change':'median_tenancy_change_a'})
gdf = gdf.rename(columns = {'median_tenancy_2013z':'median_tenancy_2013z_a'})
gdf = gdf.rename(columns = {'median_tenancy_2018z':'median_tenancy_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','monthly_housing_cost_change_a','monthly_housing_cost_2013z_a','monthly_housing_cost_2018z_a','monthly_housing_cost_change_b','monthly_housing_cost_2013z_b','monthly_housing_cost_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a','affordable_units_per_cap_change_b','affordable_units_per_cap_2013z_b','affordable_units_per_cap_2018z_b','median_tenancy_change_a','median_tenancy_2013z_a','median_tenancy_2018z_a','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b','market_rate_units_per_cap_change_a','market_rate_units_per_cap_2013z_a','market_rate_units_per_cap_2018z_a','market_rate_units_per_cap_change_b','market_rate_units_per_cap_2013z_b','market_rate_units_per_cap_2018z_b']]
gdf = gdf.merge(tenancy, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'median_tenancy_change':'median_tenancy_change_b'})
gdf = gdf.rename(columns = {'median_tenancy_2013z':'median_tenancy_2013z_b'})
gdf = gdf.rename(columns = {'median_tenancy_2018z':'median_tenancy_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','monthly_housing_cost_change_a','monthly_housing_cost_2013z_a','monthly_housing_cost_2018z_a','monthly_housing_cost_change_b','monthly_housing_cost_2013z_b','monthly_housing_cost_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a','affordable_units_per_cap_change_b','affordable_units_per_cap_2013z_b','affordable_units_per_cap_2018z_b','median_tenancy_change_a','median_tenancy_2013z_a','median_tenancy_2018z_a','median_tenancy_change_b','median_tenancy_2013z_b','median_tenancy_2018z_b','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b','market_rate_units_per_cap_change_a','market_rate_units_per_cap_2013z_a','market_rate_units_per_cap_2018z_a','market_rate_units_per_cap_change_b','market_rate_units_per_cap_2013z_b','market_rate_units_per_cap_2018z_b']]

housing_age = df[['GEOID','median_housing_age_change','median_housing_age_2013z','median_housing_age_2018z']]
gdf = gdf.merge(housing_age, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'median_housing_age_change':'median_housing_age_change_a'})
gdf = gdf.rename(columns = {'median_housing_age_2013z':'median_housing_age_2013z_a'})
gdf = gdf.rename(columns = {'median_housing_age_2018z':'median_housing_age_2018z_a'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','monthly_housing_cost_change_a','monthly_housing_cost_2013z_a','monthly_housing_cost_2018z_a','monthly_housing_cost_change_b','monthly_housing_cost_2013z_b','monthly_housing_cost_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a','affordable_units_per_cap_change_b','affordable_units_per_cap_2013z_b','affordable_units_per_cap_2018z_b','median_tenancy_change_a','median_tenancy_2013z_a','median_tenancy_2018z_a','median_tenancy_change_b','median_tenancy_2013z_b','median_tenancy_2018z_b','median_housing_age_change_a','median_housing_age_2013z_a','median_housing_age_2018z_a','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b','market_rate_units_per_cap_change_a','market_rate_units_per_cap_2013z_a','market_rate_units_per_cap_2018z_a','market_rate_units_per_cap_change_b','market_rate_units_per_cap_2013z_b','market_rate_units_per_cap_2018z_b']]
gdf = gdf.merge(housing_age, how = 'inner', left_on = ['GEOID_b'], right_on = ['GEOID'])
gdf = gdf.rename(columns = {'median_housing_age_change':'median_housing_age_change_b'})
gdf = gdf.rename(columns = {'median_housing_age_2013z':'median_housing_age_2013z_b'})
gdf = gdf.rename(columns = {'median_housing_age_2018z':'median_housing_age_2018z_b'})
gdf = gdf[['GEOID_a','GEOID_b','distance','minority_pop_pct_change_a','minority_pop_pct_change_b','minority_pop_pct_2013z_a','minority_pop_pct_2013z_b','minority_pop_pct_2018z_a','minority_pop_pct_2018z_b','rent_25th_pctile_change_a','rent_25th_pctile_2013z_a','rent_25th_pctile_2018z_a','rent_25th_pctile_change_b','rent_25th_pctile_2013z_b','rent_25th_pctile_2018z_b','totpop_change_a','totpop_2013z_a','totpop_2018z_a','totpop_change_b','totpop_2013z_b','totpop_2018z_b','rent_pct_income_change_a','rent_pct_income_2013z_a','rent_pct_income_2018z_a','rent_pct_income_change_b','rent_pct_income_2013z_b','rent_pct_income_2018z_b','monthly_housing_cost_change_a','monthly_housing_cost_2013z_a','monthly_housing_cost_2018z_a','monthly_housing_cost_change_b','monthly_housing_cost_2013z_b','monthly_housing_cost_2018z_b','affordable_units_per_cap_change_a','affordable_units_per_cap_2013z_a','affordable_units_per_cap_2018z_a','affordable_units_per_cap_change_b','affordable_units_per_cap_2013z_b','affordable_units_per_cap_2018z_b','median_tenancy_change_a','median_tenancy_2013z_a','median_tenancy_2018z_a','median_tenancy_change_b','median_tenancy_2013z_b','median_tenancy_2018z_b','median_housing_age_change_a','median_housing_age_2013z_a','median_housing_age_2018z_a','median_housing_age_change_b','median_housing_age_2013z_b','median_housing_age_2018z_b','white_pop_pct_change_a','white_pop_pct_2013z_a','white_pop_pct_2018z_a','white_pop_pct_change_b','white_pop_pct_2013z_b','white_pop_pct_2018z_b','market_rate_units_per_cap_change_a','market_rate_units_per_cap_2013z_a','market_rate_units_per_cap_2018z_a','market_rate_units_per_cap_change_b','market_rate_units_per_cap_2013z_b','market_rate_units_per_cap_2018z_b']]

omicron = 1/3 #this is the vectored weighting factor of starting point (omicron) vs change (1-omicron)

#calculate diff between the two tracts (and take absolute value since sign is meaningless here) - Delta taking into account starting point (2013) and change.
gdf['minority_pop_pct_change_delta'] = ((((1-omicron) * gdf.minority_pop_pct_change_a) + (omicron * gdf.minority_pop_pct_2013z_a)) - (((1-omicron) * gdf.minority_pop_pct_change_b) + (omicron * gdf.minority_pop_pct_2013z_b))).abs()
gdf['minority_pop_pct_change_delta'] = gdf['minority_pop_pct_change_delta'].fillna(0) #deals with nan in dataframe, which was breaking the network
gdf['white_pop_pct_change_delta'] = ((((1-omicron) * gdf.white_pop_pct_change_a) + (omicron * gdf.white_pop_pct_2013z_a)) - (((1-omicron) * gdf.white_pop_pct_change_b) + (omicron * gdf.white_pop_pct_2013z_b))).abs()
gdf['white_pop_pct_change_delta'] = gdf['white_pop_pct_change_delta'].fillna(0) #deals with nan in dataframe, which was breaking the network
gdf['rent_25th_pctile_change_delta'] = ((((1-omicron) * gdf.rent_25th_pctile_change_a) + (omicron * gdf.rent_25th_pctile_2013z_a)) - (((1-omicron) * gdf.rent_25th_pctile_change_b) + (omicron * gdf.rent_25th_pctile_2013z_b))).abs()
gdf['rent_25th_pctile_change_delta'] = gdf['rent_25th_pctile_change_delta'].fillna(0)
gdf['totpop_change_delta'] = ((((1-omicron) * gdf.totpop_change_a) + (omicron * gdf.totpop_2013z_a)) - (((1-omicron) * gdf.totpop_change_b) + (omicron * gdf.totpop_2013z_b))).abs()
gdf['totpop_change_delta'] = gdf['totpop_change_delta'].fillna(0)
gdf['rent_pct_income_change_delta'] = ((((1-omicron) * gdf.rent_pct_income_change_a) + (omicron * gdf.rent_pct_income_2013z_a)) - (((1-omicron) * gdf.rent_pct_income_change_b) + (omicron * gdf.rent_pct_income_2013z_b))).abs()
gdf['rent_pct_income_change_delta'] = gdf['rent_pct_income_change_delta'].fillna(0)
gdf['monthly_housing_cost_change_delta'] = ((((1-omicron) * gdf.monthly_housing_cost_change_a) + (omicron * gdf.monthly_housing_cost_2013z_a)) - (((1-omicron) * gdf.monthly_housing_cost_change_b) + (omicron * gdf.monthly_housing_cost_2013z_b))).abs()
gdf['monthly_housing_cost_change_delta'] = gdf['monthly_housing_cost_change_delta'].fillna(0)
gdf['affordable_units_per_cap_change_delta'] = ((((1-omicron) * gdf.affordable_units_per_cap_change_a) + (omicron * gdf.affordable_units_per_cap_2013z_a)) - (((1-omicron) * gdf.affordable_units_per_cap_change_b) + (omicron * gdf.affordable_units_per_cap_2013z_b))).abs()
gdf['affordable_units_per_cap_change_delta'] = gdf['affordable_units_per_cap_change_delta'].fillna(0)
gdf['market_rate_units_per_cap_change_delta'] = ((((1-omicron) * gdf.market_rate_units_per_cap_change_a) + (omicron * gdf.market_rate_units_per_cap_2013z_a)) - (((1-omicron) * gdf.market_rate_units_per_cap_change_b) + (omicron * gdf.market_rate_units_per_cap_2013z_b))).abs()
gdf['market_rate_units_per_cap_change_delta'] = gdf['market_rate_units_per_cap_change_delta'].fillna(0)
gdf['median_tenancy_change_delta'] = ((((1-omicron) * gdf.median_tenancy_change_a) + (omicron * gdf.median_tenancy_2013z_a)) - (((1-omicron) * gdf.median_tenancy_change_b) + (omicron * gdf.median_tenancy_2013z_b))).abs()
gdf['median_tenancy_change_delta'] = gdf['median_tenancy_change_delta'].fillna(0)
gdf['median_housing_age_change_delta'] = ((((1-omicron) * gdf.median_housing_age_change_a) + (omicron * gdf.median_housing_age_2013z_a)) - (((1-omicron) * gdf.median_housing_age_change_b) + (omicron * gdf.median_housing_age_2013z_b))).abs()
gdf['median_housing_age_change_delta'] = gdf['median_housing_age_change_delta'].fillna(0)

#Delta in 2013 (without taking into account change)
gdf['minority_pop_pct_change_delta_2013'] = ((gdf.minority_pop_pct_2013z_a) - (gdf.minority_pop_pct_2013z_b)).abs()
gdf['minority_pop_pct_change_delta_2013'] = gdf['minority_pop_pct_change_delta_2013'].fillna(0) #deals with nan in dataframe, which was breaking the network
gdf['white_pop_pct_change_delta_2013'] = ((gdf.white_pop_pct_2013z_a) - (gdf.white_pop_pct_2013z_b)).abs()
gdf['white_pop_pct_change_delta_2013'] = gdf['white_pop_pct_change_delta_2013'].fillna(0) #deals with nan in dataframe, which was breaking the network
gdf['rent_25th_pctile_change_delta_2013'] = ((gdf.rent_25th_pctile_2013z_a) - (gdf.rent_25th_pctile_2013z_b)).abs()
gdf['rent_25th_pctile_change_delta_2013'] = gdf['rent_25th_pctile_change_delta_2013'].fillna(0)
gdf['totpop_change_delta_2013'] = ((gdf.totpop_2013z_a) - (gdf.totpop_2013z_b)).abs()
gdf['totpop_change_delta_2013'] = gdf['totpop_change_delta_2013'].fillna(0)
gdf['rent_pct_income_change_delta_2013'] = ((gdf.rent_pct_income_2013z_a) - (gdf.rent_pct_income_2013z_b)).abs()
gdf['rent_pct_income_change_delta_2013'] = gdf['rent_pct_income_change_delta_2013'].fillna(0)
gdf['monthly_housing_cost_change_delta_2013'] = ((gdf.monthly_housing_cost_2013z_a) - (gdf.monthly_housing_cost_2013z_b)).abs()
gdf['monthly_housing_cost_change_delta_2013'] = gdf['monthly_housing_cost_change_delta_2013'].fillna(0)
gdf['affordable_units_per_cap_change_delta_2013'] = ((gdf.affordable_units_per_cap_2013z_a) - (gdf.affordable_units_per_cap_2013z_b)).abs()
gdf['affordable_units_per_cap_change_delta_2013'] = gdf['affordable_units_per_cap_change_delta_2013'].fillna(0)
gdf['market_rate_units_per_cap_change_delta_2013'] = ((gdf.market_rate_units_per_cap_2013z_a) - (gdf.market_rate_units_per_cap_2013z_b)).abs()
gdf['market_rate_units_per_cap_change_delta_2013'] = gdf['market_rate_units_per_cap_change_delta_2013'].fillna(0)
gdf['median_tenancy_change_delta_2013'] = ((gdf.median_tenancy_2013z_a) - (gdf.median_tenancy_2013z_b)).abs()
gdf['median_tenancy_change_delta_2013'] = gdf['median_tenancy_change_delta_2013'].fillna(0)
gdf['median_housing_age_change_delta_2013'] = ((gdf.median_housing_age_2013z_a) - (gdf.median_housing_age_2013z_b)).abs()
gdf['median_housing_age_change_delta_2013'] = gdf['median_housing_age_change_delta_2013'].fillna(0)

#Delta in 2018 (without taking into account change)
gdf['minority_pop_pct_change_delta_2018'] = ((gdf.minority_pop_pct_2018z_a) - (gdf.minority_pop_pct_2018z_b)).abs()
gdf['minority_pop_pct_change_delta_2018'] = gdf['minority_pop_pct_change_delta_2018'].fillna(0) #deals with nan in dataframe, which was breaking the network
gdf['white_pop_pct_change_delta_2018'] = ((gdf.white_pop_pct_2018z_a) - (gdf.white_pop_pct_2018z_b)).abs()
gdf['white_pop_pct_change_delta_2018'] = gdf['white_pop_pct_change_delta_2018'].fillna(0) #deals with nan in dataframe, which was breaking the network
gdf['rent_25th_pctile_change_delta_2018'] = ((gdf.rent_25th_pctile_2018z_a) - (gdf.rent_25th_pctile_2018z_b)).abs()
gdf['rent_25th_pctile_change_delta_2018'] = gdf['rent_25th_pctile_change_delta_2018'].fillna(0)
gdf['totpop_change_delta_2018'] = ((gdf.totpop_2018z_a) - (gdf.totpop_2018z_b)).abs()
gdf['totpop_change_delta_2018'] = gdf['totpop_change_delta_2018'].fillna(0)
gdf['rent_pct_income_change_delta_2018'] = ((gdf.rent_pct_income_2018z_a) - (gdf.rent_pct_income_2018z_b)).abs()
gdf['rent_pct_income_change_delta_2018'] = gdf['rent_pct_income_change_delta_2018'].fillna(0)
gdf['monthly_housing_cost_change_delta_2018'] = ((gdf.monthly_housing_cost_2018z_a) - (gdf.monthly_housing_cost_2018z_b)).abs()
gdf['monthly_housing_cost_change_delta_2018'] = gdf['monthly_housing_cost_change_delta_2018'].fillna(0)
gdf['affordable_units_per_cap_change_delta_2018'] = ((gdf.affordable_units_per_cap_2018z_a) - (gdf.affordable_units_per_cap_2018z_b)).abs()
gdf['affordable_units_per_cap_change_delta_2018'] = gdf['affordable_units_per_cap_change_delta_2018'].fillna(0)
gdf['market_rate_units_per_cap_change_delta_2018'] = ((gdf.market_rate_units_per_cap_2018z_a) - (gdf.market_rate_units_per_cap_2018z_b)).abs()
gdf['market_rate_units_per_cap_change_delta_2018'] = gdf['market_rate_units_per_cap_change_delta_2018'].fillna(0)
gdf['median_tenancy_change_delta_2018'] = ((gdf.median_tenancy_2018z_a) - (gdf.median_tenancy_2018z_b)).abs()
gdf['median_tenancy_change_delta_2018'] = gdf['median_tenancy_change_delta_2018'].fillna(0)
gdf['median_housing_age_change_delta_2018'] = ((gdf.median_housing_age_2018z_a) - (gdf.median_housing_age_2018z_b)).abs()
gdf['median_housing_age_change_delta_2018'] = gdf['median_housing_age_change_delta_2018'].fillna(0)

#weight the edges
alpha = 1/6.0
bravo = 1/6.0
charlie = 1/6.0
delta = 1/6.0
echo = 1/6.0
foxtrot = 0
golf = 0
hotel = 0

threshold = 0

#TODO - Add in total-units-tract for denominator for affordablehousing and flip sign to get rid of negative
#2013 + change version
gdf['omega'] = (
        (alpha * gdf.white_pop_pct_change_delta) + \
        (bravo * gdf.rent_25th_pctile_change_delta) + \
        (charlie * gdf.totpop_change_delta) + \
        (delta * gdf.rent_pct_income_change_delta) + \
        (echo * gdf.monthly_housing_cost_change_delta) + \
        (foxtrot * gdf.market_rate_units_per_cap_change_delta) + \
        -(golf * gdf.median_tenancy_change_delta) + \
        (hotel * gdf.median_housing_age_change_delta)
)

#gdf.loc[gdf.omega < 0, 'omega'] = None #corrects for the census having "2018" as an answer to some of these
gdf = gdf[(gdf['omega'] >= threshold)]

#2013 only version
gdf['omega13'] = (
        (alpha * gdf.white_pop_pct_change_delta_2013) + \
        (bravo * gdf.rent_25th_pctile_change_delta_2013) + \
        (charlie * gdf.totpop_change_delta_2013) + \
        (delta * gdf.rent_pct_income_change_delta_2013) + \
        (echo * gdf.monthly_housing_cost_change_delta_2018) + \
        (foxtrot * gdf.market_rate_units_per_cap_change_delta_2013) + \
        -(golf * gdf.median_tenancy_change_delta_2013) + \
        (hotel * gdf.median_housing_age_change_delta_2013)
)
gdf = gdf[(gdf['omega13'] >= threshold)]

#2018 only version
gdf['omega18'] = (
        (alpha * gdf.white_pop_pct_change_delta_2018) + \
        (bravo * gdf.rent_25th_pctile_change_delta_2018) + \
        (charlie * gdf.totpop_change_delta_2018) + \
        (delta * gdf.rent_pct_income_change_delta_2018) + \
        (echo * gdf.monthly_housing_cost_change_delta_2018) + \
        (foxtrot * gdf.market_rate_units_per_cap_change_delta_2018) + \
        -(golf * gdf.median_tenancy_change_delta_2018) + \
        (hotel * gdf.median_housing_age_change_delta_2018)
)
gdf = gdf[(gdf['omega18'] >= threshold)]

#tester for bar graph of just geoid_a
gdf['omega_bar'] = (
        (alpha * (((1-omicron) * gdf.white_pop_pct_change_a) + (omicron * gdf.white_pop_pct_2013z_a))) + \
        (bravo * (((1-omicron) * gdf.rent_25th_pctile_change_a) + (omicron * gdf.rent_25th_pctile_2013z_a))) + \
        (charlie * (((1-omicron) * gdf.totpop_change_a) + (omicron * gdf.totpop_2013z_a))) + \
        (delta * (((1-omicron) * gdf.rent_pct_income_change_a) + (omicron * gdf.rent_pct_income_2013z_a))) + \
        (echo * (((1-omicron) * gdf.monthly_housing_cost_change_a) + (omicron * gdf.monthly_housing_cost_2013z_a))) + \
        (foxtrot * (((1-omicron) * gdf.market_rate_units_per_cap_change_a) + (omicron * gdf.market_rate_units_per_cap_2013z_a))) + \
        -(golf * (((1-omicron) * gdf.median_tenancy_change_a) + (omicron * gdf.median_tenancy_2013z_a))) + \
        (hotel * (((1-omicron) * gdf.median_housing_age_change_a) + (omicron * gdf.median_housing_age_2013z_a)))
)
gdf['omega_bar'] = gdf['omega_bar'].fillna(0) #deals with nan in dataframe, which was breaking the network
gdf = gdf[(gdf['omega_bar'] >= threshold)]


#gdf.loc[gdf.omega < 0, 'omega'] = None #corrects for the census having "2018" as an answer to some of these
#gdf = gdf[(gdf['omega'] >= threshold)]
import itertools

#create mtbaker_station_df & mtbaker_station_gdf
mtbaker_station_gdf = gdf[((gdf['GEOID_a'] == '53033010001') & (gdf['distance'] < 1500)) | ((gdf['GEOID_b'] == '53033010001') & (gdf['distance'] < 1500))]
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
othello_station_gdf = gdf[((gdf['GEOID_a'] == '53033011001') & (gdf['distance'] < 5000)) | ((gdf['GEOID_b'] == '53033011001') & (gdf['distance'] < 5000))]
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
rainier_beach_gdf = gdf[((gdf['GEOID_a'] == '53033011700') & (gdf['distance'] < 7000)) | ((gdf['GEOID_b'] == '53033011700') & (gdf['distance'] < 7000))]
#rainier_beach_gdf = gdf[((gdf['GEOID_a'] == '53033001701') | (gdf['GEOID_a'] == '53033010900')) & ((gdf['GEOID_b'] == '53033001701') | (gdf['GEOID_b'] == '53033010900'))]

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
#hacky-ass manual add to the geoids
rainier_beach_missing = ['53033010401', '53033011200','53033011300','53033027200','53033026801']
for tract in rainier_beach_missing:
    rainier_beach_geoids.append(tract)
while '53033024602' in rainier_beach_geoids:
    rainier_beach_geoids.remove('53033024602')
#for testing
#rainier_beach_geoids = ['53033001701','53033010900']
rainier_beach_df = df[df['GEOID'].isin(rainier_beach_geoids)]
rainier_beach_df['neighborhood'] = 'rainier_beach'

#create wallingford_df & wallingford_gdf
wallingford_gdf = gdf[((gdf['GEOID_a'] == '53033004600') & (gdf['distance'] < 4000)) | ((gdf['GEOID_b'] == '53033004600') & (gdf['distance'] < 4000))]
#wallingford_gdf = gdf[((gdf['GEOID_a'] == '53033005000') | (gdf['GEOID_a'] == '53033003500') | (gdf['GEOID_a'] == '53033005200')) & ((gdf['GEOID_b'] == '53033005000') | (gdf['GEOID_b'] == '53033003500')| (gdf['GEOID_b'] == '53033005200'))]

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
#hacky-ass manual add to the geoids
wallingford_missing = ['53033005200']
for tract in wallingford_missing:
    wallingford_geoids.append(tract)
#for testing
#wallingford_geoids = ['53033005000','53033003500']
wallingford_df = df[df['GEOID'].isin(wallingford_geoids)]
wallingford_df['neighborhood'] = 'wallingford'

#combine groupss for a comparison network
combo_geoids = wallingford_geoids + rainier_beach_geoids
combo_gdf = gdf[(gdf['GEOID_a'].isin(combo_geoids)) & (gdf['GEOID_b'].isin(combo_geoids))]

combo_gid_a = list(combo_gdf['GEOID_a'].drop_duplicates())
combo_gid_b = list(combo_gdf['GEOID_b'].drop_duplicates())

combo_pair_data = {
    'GEOID_a': list(),
    'GEOID_b': list()
}

for ga, gb in itertools.product(combo_gid_a + combo_gid_b, combo_gid_a + combo_gid_b):
    combo_pair_data['GEOID_a'].append(ga)
    combo_pair_data['GEOID_b'].append(gb)

combo_pair_df = pd.DataFrame.from_dict(combo_pair_data)
combo_pair_df = combo_pair_df.merge(gdf, how='left', on=['GEOID_a', 'GEOID_b'])
combo_pair_df = combo_pair_df[~combo_pair_df['distance'].isnull()]

combo_gdf = combo_pair_df.drop_duplicates()
combo_df = rainier_beach_df.append(wallingford_df)

def get_df(subset='all'):
    subsets = {
        'all': df,
        'combo':combo_df,
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
        'combo':combo_gdf,
        'mtbaker_station': mtbaker_station_gdf,
        'othello_station': othello_station_gdf,
        'rainier_beach': rainier_beach_gdf,
        'wallingford': wallingford_gdf
    }

    if subset in subsets:
        return subsets[subset]
    else:
        raise ('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))

#DEBUG - CHECK FOR NaNs OR output dfs to csv for exporting
nandf = df[df.isnull().any(axis=1)]
#csv_filename = 'data_prep_tract-nan-check.csv'
csv_filename = 'data_prep_tract-combo_gdf.csv'
combo_gdf.to_csv(csv_filename, index = False,quotechar='"',quoting=csv.QUOTE_ALL)
csv_filename = 'data_prep_tract-combo_df.csv'
combo_df.to_csv(csv_filename, index = False,quotechar='"',quoting=csv.QUOTE_ALL)
print("Exporting csv...")