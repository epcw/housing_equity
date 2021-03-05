import pandas as pd
import re
#set root directory for data files
ROOTDIR = '/home/ubuntu/housing_equity/interactive-map/' #production
#ROOTDIR = '' #local

df = pd.read_csv(ROOTDIR + 'data/housing_prepped.csv', dtype={"GEOID": str,"TRACT_NUM": str})

#filter for King County
df = df[(df['COUNTY'] == 'King')]

#bring in affordable housing data
housing_df_raw = pd.read_csv(ROOTDIR + 'data/affordable_housing_units.csv', dtype={"TRACT_NUM": str})
median_costs_raw = pd.read_csv(ROOTDIR + 'data/housing_costs_medians.csv', dtype={"TRACT_NUM": str}) #NOTE: pre-filtered in SQL for King County and already has GEOID

#filter for King County
housing_df_raw = housing_df_raw[(housing_df_raw['COUNTY'] == 'King')]

#create geoid
housing_df_raw['GEOID'] = '53033' + housing_df_raw['TRACT_NUM']
housing_df = housing_df_raw[['COUNTY','TRACT_NUM','GEOID']].drop_duplicates()
median_costs_raw['GEOID'] = '53033' + median_costs_raw['TRACT_NUM']
median_costs_df = median_costs_raw[['COUNTY','TRACT_NUM','GEOID','DATA','CENSUS_QUERY']].drop_duplicates()

#Aggregate unit data (rows in original housing_df_raw are counts of units under 100/mo, 200/mo, 300/mo, etc.
housing_data = housing_df_raw.groupby(['GEOID']).sum().reset_index()
housing_df = housing_df.merge(housing_data, how='left', left_on=['GEOID'], right_on=['GEOID'])
housing_df = housing_df[['COUNTY','TRACT_NUM','GEOID','DATA']]
housing_df = housing_df.rename(columns = {'DATA' : 'sub_600_per_mo_housing_units'})

#bring in tenancy, cost, and occupancy data and filter for 2010 & 2018
housing_details_raw = pd.read_csv(ROOTDIR + 'data/housing_details.csv', dtype={"TRACT_NUM": str, "GEOID": str, "YEAR":int}) #NOTE: pre-filtered in SQL for King County
housing_details_raw['DATA'] = housing_details_raw['DATA'].astype(str).map(lambda x: x.rstrip('+-'))
housing_details_raw['DATA'] = housing_details_raw['DATA'].astype(float)
housing_details10 = housing_details_raw[(housing_details_raw['YEAR'] == 2010)]
housing_details18 = housing_details_raw[(housing_details_raw['YEAR'] == 2018)]

#sort median_costs_df by census query, creating new column-sorted dfs instead of rows
costs_10df25 = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25057_001E')]
costs_10df25['DATA'] = costs_10df25['DATA'].astype(float)
costs_10df25 = costs_10df25.rename(columns = {'DATA' : 'RENT_25PCTILE_2010'})
costs_10df25 = costs_10df25[['GEOID','RENT_25PCTILE_2010','COUNTY','TRACT_NUM']]
costs_10df50 = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25058_001E')]
costs_10df50 = costs_10df50.rename(columns = {'DATA' : 'RENT_50PCTILE_2010'})
costs_10df50 = costs_10df50[['GEOID','RENT_50PCTILE_2010','COUNTY','TRACT_NUM']]
costs_10df75 = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25059_001E')]
costs_10df75 = costs_10df75.rename(columns = {'DATA' : 'RENT_75PCTILE_2010'})
costs_10df75 = costs_10df75[['GEOID','RENT_75PCTILE_2010','COUNTY','TRACT_NUM']]
costs_10dfpct = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25071_001E')]
costs_10dfpct['DATA'] = costs_10dfpct['DATA'].astype(float)
costs_10dfpct = costs_10dfpct.rename(columns = {'DATA' : 'RENT_AS_PCT_HOUSEHOLD_INCOME_2010'})
costs_10dfpct = costs_10dfpct[['GEOID','RENT_AS_PCT_HOUSEHOLD_INCOME_2010','COUNTY','TRACT_NUM']]
costs_10dfmedcost = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25105_001E')]
costs_10dfmedcost = costs_10dfmedcost.rename(columns = {'DATA' : 'MEDIAN_MONTHLY_HOUSING_COST_2010'})
costs_10dfmedcost['MEDIAN_MONTHLY_HOUSING_COST_2010'] = costs_10dfmedcost['MEDIAN_MONTHLY_HOUSING_COST_2010'].astype(float)
costs_10dfmedcost = costs_10dfmedcost[['GEOID','MEDIAN_MONTHLY_HOUSING_COST_2010','COUNTY','TRACT_NUM']]
costs_10df = costs_10df25.merge(costs_10df50, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
costs_10df = costs_10df.merge(costs_10df75, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
costs_10df = costs_10df.merge(costs_10dfpct, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
costs_10df = costs_10df.merge(costs_10dfmedcost, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])

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
df = df.merge(costs_10df, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
df = df.merge(costs_18df, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])

df['twenty_pctile_delta'] = (df['TWENTY_PCTILE_2018'] - df['TWENTY_PCTILE_2010']) / df['TWENTY_PCTILE_2010'] * 100
df['eighty_pctile_delta'] = (df['EIGHTY_PCTILE_2018'] - df['EIGHTY_PCTILE_2010']) / df['TWENTY_PCTILE_2010'] * 100
df['income_gap10'] = (df['EIGHTY_PCTILE_2010'] - df['TWENTY_PCTILE_2010']) / df['TWENTY_PCTILE_2010'] * 100
df['income_gap18'] = (df['EIGHTY_PCTILE_2018'] - df['TWENTY_PCTILE_2018']) / df['TWENTY_PCTILE_2018'] * 100
df['income_gap_delta'] = (df['income_gap18'] - df['income_gap10']) / df['income_gap10'] * 100
df['housing_costs_delta'] = (df['MEDIAN_MONTHLY_HOUSING_COST_2018'] - df['MEDIAN_MONTHLY_HOUSING_COST_2010']) / df['MEDIAN_MONTHLY_HOUSING_COST_2010'] * 100
df['rent_pct_income_delta'] = (df['RENT_AS_PCT_HOUSEHOLD_INCOME_2018'] - df['RENT_AS_PCT_HOUSEHOLD_INCOME_2010']) / df['RENT_AS_PCT_HOUSEHOLD_INCOME_2010'] * 100
df['rent_25pctile_delta'] = (df['RENT_25PCTILE_2018'] - df['RENT_25PCTILE_2010']) / df['RENT_25PCTILE_2010'] * 100

#occupancy and housing age data
occupancydf_units10 = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25002_001E')]
occupancydf_units10['DATA'] = occupancydf_units10['DATA'].astype(float)
occupancydf_units10 = occupancydf_units10.rename(columns = {'DATA' : 'housing_units_2010'})
occupancydf_units10 = occupancydf_units10[['GEOID','housing_units_2010','COUNTY','TRACT_NUM']]
occupancydf_occupied10 = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25002_002E')]
occupancydf_occupied10['DATA'] = occupancydf_occupied10['DATA'].astype(float)
occupancydf_occupied10 = occupancydf_occupied10.rename(columns = {'DATA' : 'housing_occupied_2010'})
occupancydf_occupied10 = occupancydf_occupied10[['GEOID','housing_occupied_2010','COUNTY','TRACT_NUM']]
occupancydf_vacant10 = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25002_003E')]
occupancydf_vacant10['DATA'] = occupancydf_vacant10['DATA'].astype(float)
occupancydf_vacant10 = occupancydf_vacant10.rename(columns = {'DATA' : 'housing_vacant_2010'})
occupancydf_vacant10 = occupancydf_vacant10[['GEOID','housing_vacant_2010','COUNTY','TRACT_NUM']]
occupancydf_built10 = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25037_001E')]
occupancydf_built10['DATA'] = occupancydf_built10['DATA'].astype(float)
occupancydf_built10 = occupancydf_built10.rename(columns = {'DATA' : 'housing_yr_built_2010'})
occupancydf_built10 = occupancydf_built10[['GEOID','housing_yr_built_2010','COUNTY','TRACT_NUM']]
occupancydf_built_owned10 = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25037_002E')]
occupancydf_built_owned10['DATA'] = occupancydf_built_owned10['DATA'].astype(float)
occupancydf_built_owned10 = occupancydf_built_owned10.rename(columns = {'DATA' : 'housing_yr_built_owned_2010'})
occupancydf_built_owned10 = occupancydf_built_owned10[['GEOID','housing_yr_built_owned_2010','COUNTY','TRACT_NUM']]
occupancydf_built_rented10 = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25037_003E')]
occupancydf_built_rented10['DATA'] = occupancydf_built_rented10['DATA'].astype(float)
occupancydf_built_rented10 = occupancydf_built_rented10.rename(columns = {'DATA' : 'housing_yr_built_rented_2010'})
occupancydf_built_rented10 = occupancydf_built_rented10[['GEOID','housing_yr_built_rented_2010','COUNTY','TRACT_NUM']]
occupancydf_tenure10 = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25039_001E')]
occupancydf_tenure10['DATA'] = occupancydf_tenure10['DATA'].astype(float)
occupancydf_tenure10 = occupancydf_tenure10.rename(columns = {'DATA' : 'housing_yr_movein_2010'})
occupancydf_tenure10 = occupancydf_tenure10[['GEOID','housing_yr_movein_2010','COUNTY','TRACT_NUM']]
occupancydf_tenure_owned10 = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25039_002E')]
occupancydf_tenure_owned10['DATA'] = occupancydf_tenure_owned10['DATA'].astype(float)
occupancydf_tenure_owned10 = occupancydf_tenure_owned10.rename(columns = {'DATA' : 'housing_yr_movein_owned_2010'})
occupancydf_tenure_owned10 = occupancydf_tenure_owned10[['GEOID','housing_yr_movein_owned_2010','COUNTY','TRACT_NUM']]
occupancydf_tenure_rented10 = housing_details10[(housing_details10['CENSUS_QUERY'] == 'B25039_003E')]
occupancydf_tenure_rented10['DATA'] = occupancydf_tenure_rented10['DATA'].astype(float)
occupancydf_tenure_rented10 = occupancydf_tenure_rented10.rename(columns = {'DATA' : 'housing_yr_movein_rented_2010'})
occupancydf_tenure_rented10 = occupancydf_tenure_rented10[['GEOID','housing_yr_movein_rented_2010','COUNTY','TRACT_NUM']]
occupancydf10 = occupancydf_units10.merge(occupancydf_occupied10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf10 = occupancydf10.merge(occupancydf_vacant10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf10 = occupancydf10.merge(occupancydf_built10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf10 = occupancydf10.merge(occupancydf_built_owned10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf10 = occupancydf10.merge(occupancydf_built_rented10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf10 = occupancydf10.merge(occupancydf_tenure10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf10 = occupancydf10.merge(occupancydf_tenure_owned10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf10 = occupancydf10.merge(occupancydf_tenure_rented10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()

df = df.merge(occupancydf10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
df['occupancy_pct10'] = (df['housing_occupied_2010'] / df['housing_units_2010']) * 100
df['vacancy_pct10'] = (df['housing_vacant_2010'] / df['housing_units_2010']) * 100
df['housing_age10'] = 2010 - df['housing_yr_built_2010']
df['housing_age_owned10'] = 2010 - df['housing_yr_built_owned_2010']
df['housing_age_rented10'] = 2010 - df['housing_yr_built_rented_2010']
df['housing_tenure10'] = 2010 - df['housing_yr_movein_2010']
df['housing_tenure_owned10'] = 2010 - df['housing_yr_movein_owned_2010']
df['housing_tenure_rented10'] = 2010 - df['housing_yr_movein_rented_2010']

occupancydf_units18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25002_001E')]
occupancydf_units18['DATA'] = occupancydf_units18['DATA'].astype(float)
occupancydf_units18 = occupancydf_units18.rename(columns = {'DATA' : 'housing_units_2018'})
occupancydf_units18 = occupancydf_units18[['GEOID','housing_units_2018','COUNTY','TRACT_NUM']]
occupancydf_occupied18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25002_002E')]
occupancydf_occupied18['DATA'] = occupancydf_occupied18['DATA'].astype(float)
occupancydf_occupied18 = occupancydf_occupied18.rename(columns = {'DATA' : 'housing_occupied_2018'})
occupancydf_occupied18 = occupancydf_occupied18[['GEOID','housing_occupied_2018','COUNTY','TRACT_NUM']]
occupancydf_vacant18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25002_003E')]
occupancydf_vacant18['DATA'] = occupancydf_vacant18['DATA'].astype(float)
occupancydf_vacant18 = occupancydf_vacant18.rename(columns = {'DATA' : 'housing_vacant_2018'})
occupancydf_vacant18 = occupancydf_vacant18[['GEOID','housing_vacant_2018','COUNTY','TRACT_NUM']]
occupancydf_built18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25037_001E')]
occupancydf_built18['DATA'] = occupancydf_built18['DATA'].astype(float)
occupancydf_built18 = occupancydf_built18.rename(columns = {'DATA' : 'housing_yr_built_2018'})
occupancydf_built18 = occupancydf_built18[['GEOID','housing_yr_built_2018','COUNTY','TRACT_NUM']]
occupancydf_built_owned18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25037_002E')]
occupancydf_built_owned18['DATA'] = occupancydf_built_owned18['DATA'].astype(float)
occupancydf_built_owned18 = occupancydf_built_owned18.rename(columns = {'DATA' : 'housing_yr_built_owned_2018'})
occupancydf_built_owned18 = occupancydf_built_owned18[['GEOID','housing_yr_built_owned_2018','COUNTY','TRACT_NUM']]
occupancydf_built_rented18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25037_003E')]
occupancydf_built_rented18['DATA'] = occupancydf_built_rented18['DATA'].astype(float)
occupancydf_built_rented18 = occupancydf_built_rented18.rename(columns = {'DATA' : 'housing_yr_built_rented_2018'})
occupancydf_built_rented18 = occupancydf_built_rented18[['GEOID','housing_yr_built_rented_2018','COUNTY','TRACT_NUM']]
occupancydf_tenure18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25039_001E')]
occupancydf_tenure18['DATA'] = occupancydf_tenure18['DATA'].astype(float)
occupancydf_tenure18 = occupancydf_tenure18.rename(columns = {'DATA' : 'housing_yr_movein_2018'})
occupancydf_tenure18 = occupancydf_tenure18[['GEOID','housing_yr_movein_2018','COUNTY','TRACT_NUM']]
occupancydf_tenure_owned18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25039_002E')]
occupancydf_tenure_owned18['DATA'] = occupancydf_tenure_owned18['DATA'].astype(float)
occupancydf_tenure_owned18 = occupancydf_tenure_owned18.rename(columns = {'DATA' : 'housing_yr_movein_owned_2018'})
occupancydf_tenure_owned18 = occupancydf_tenure_owned18[['GEOID','housing_yr_movein_owned_2018','COUNTY','TRACT_NUM']]
occupancydf_tenure_rented18 = housing_details18[(housing_details18['CENSUS_QUERY'] == 'B25039_003E')]
occupancydf_tenure_rented18['DATA'] = occupancydf_tenure_rented18['DATA'].astype(float)
occupancydf_tenure_rented18 = occupancydf_tenure_rented18.rename(columns = {'DATA' : 'housing_yr_movein_rented_2018'})
occupancydf_tenure_rented18 = occupancydf_tenure_rented18[['GEOID','housing_yr_movein_rented_2018','COUNTY','TRACT_NUM']]
occupancydf18 = occupancydf_units18.merge(occupancydf_occupied18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf18 = occupancydf18.merge(occupancydf_vacant18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf18 = occupancydf18.merge(occupancydf_built18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf18 = occupancydf18.merge(occupancydf_built_owned18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf18 = occupancydf18.merge(occupancydf_built_rented18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf18 = occupancydf18.merge(occupancydf_tenure18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf18 = occupancydf18.merge(occupancydf_tenure_owned18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
occupancydf18 = occupancydf18.merge(occupancydf_tenure_rented18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()

df = df.merge(occupancydf18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM']).drop_duplicates()
df['occupancy_pct18'] = (df['housing_occupied_2018'] / df['housing_units_2018']) * 180
df['vacancy_pct18'] = (df['housing_vacant_2018'] / df['housing_units_2018']) * 180
df['housing_age18'] = 2018 - df['housing_yr_built_2018']
df['housing_age_owned18'] = 2018 - df['housing_yr_built_owned_2018']
df['housing_age_rented18'] = 2018 - df['housing_yr_built_rented_2018']
df['housing_tenure18'] = 2018 - df['housing_yr_movein_2018']
df['housing_tenure_owned18'] = 2018 - df['housing_yr_movein_owned_2018']
df['housing_tenure_rented18'] = 2018 - df['housing_yr_movein_rented_2018']

#displays missing data on house age as Nan instead of 0, to filter out erroneous results that claim houses were built in year "0"
df.loc[df.housing_age10 > 100, 'housing_age10'] = None
df.loc[df.housing_age18 > 100, 'housing_age18'] = None
df.loc[df.housing_age_owned10 > 100, 'housing_age_owned10'] = None
df.loc[df.housing_age_owned18 > 100, 'housing_age_owned18'] = None
df.loc[df.housing_age_rented10 > 100, 'housing_age_rented10'] = None
df.loc[df.housing_age_rented18 > 100, 'housing_age_rented18'] = None

df['occupancy_delta'] = df['occupancy_pct18'] - df['occupancy_pct10']
df['vacancy_delta'] = df['vacancy_pct18'] - df['vacancy_pct10']
df['housing_age_delta'] = df['housing_age18'] - df['housing_age10']
df['housing_age_owned_delta'] = df['housing_age_owned18'] - df['housing_age_owned10']
df['housing_age_rented_delta'] = df['housing_age_rented18'] - df['housing_age_rented10']
df['housing_tenure_delta'] = df['housing_tenure18'] - df['housing_tenure10']
df['housing_tenure_owned_delta'] = df['housing_tenure_owned18'] - df['housing_tenure_owned10']
df['housing_tenure_rented_delta'] = df['housing_tenure_rented18'] - df['housing_tenure_rented10']

rdf = pd.read_csv(ROOTDIR + 'data/race-data.csv', dtype={"TRACT_NUM": str, "YEAR": str})

#filter for King County 2010
rdf10 = rdf[(rdf['COUNTY'] == 'King') & (rdf['YEAR'] == '2010')]

#filter for King County 2018
rdf18 = rdf[(rdf['COUNTY'] == 'King') & (rdf['YEAR'] == '2018')]

#create GEOID
rdf10['GEOID'] = '53033' + rdf10['TRACT_NUM']
rdf18['GEOID'] = '53033' + rdf18['TRACT_NUM']

#racial percentages
white10 = rdf10[(rdf10['CENSUS_QUERY'] == 'B03002_003E')]
white10 = white10[['GEOID','COUNTY','TRACT_NUM','DATA']]
white10 = white10.rename(columns = {'DATA' : 'pop_white_nonhisp_only10'})
black10 = rdf10[(rdf10['CENSUS_QUERY'] == 'B02001_003E')]
black10 = black10[['GEOID','COUNTY','TRACT_NUM','DATA']]
black10 = black10.rename(columns = {'DATA' : 'pop_black_only10'})
native10 = rdf10[(rdf10['CENSUS_QUERY'] == 'B02001_004E')]
native10 = native10[['GEOID','COUNTY','TRACT_NUM','DATA']]
native10 = native10.rename(columns = {'DATA' : 'pop_native_only10'})
asian10 = rdf10[(rdf10['CENSUS_QUERY'] == 'B02001_005E')]
asian10 = asian10[['GEOID','COUNTY','TRACT_NUM','DATA']]
asian10 = asian10.rename(columns = {'DATA' : 'pop_asian_only10'})
polynesian10 = rdf10[(rdf10['CENSUS_QUERY'] == 'B02001_006E')]
polynesian10 = polynesian10[['GEOID','COUNTY','TRACT_NUM','DATA']]
polynesian10 = polynesian10.rename(columns = {'DATA' : 'pop_polynesian_only10'})
latino10 = rdf10[(rdf10['CENSUS_QUERY'] == 'B03002_012E')]
latino10 = latino10[['GEOID','COUNTY','TRACT_NUM','DATA']]
latino10 = latino10.rename(columns = {'DATA' : 'pop_hispanic10'})
other10 = rdf10[(rdf10['CENSUS_QUERY'] == 'B02001_007E')]
other10 = other10[['GEOID','COUNTY','TRACT_NUM','DATA']]
other10 = other10.rename(columns = {'DATA' : 'pop_other_only10'})
multiracial10 = rdf10[(rdf10['CENSUS_QUERY'] == 'B02001_008E')]
multiracial10 = multiracial10[['GEOID','COUNTY','TRACT_NUM','DATA']]
multiracial10 = multiracial10.rename(columns = {'DATA' : 'pop_multiracial10'})
racial10 = white10.merge(black10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial10 = racial10.merge(native10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial10 = racial10.merge(asian10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial10 = racial10.merge(polynesian10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial10 = racial10.merge(latino10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial10 = racial10.merge(other10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial10 = racial10.merge(multiracial10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
race_data10 = racial10[['GEOID','COUNTY','TRACT_NUM','pop_white_nonhisp_only10','pop_black_only10','pop_native_only10','pop_asian_only10','pop_polynesian_only10','pop_hispanic10','pop_other_only10','pop_multiracial10']]

df = df.merge(race_data10, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
df['minority_pop10'] = df['TOT_POP_2010'] - df['pop_white_nonhisp_only10']
df['minority_pop_pct10'] = (df['minority_pop10'] / df['TOT_POP_2010']) * 100
df['white_pct10'] = (df['pop_white_nonhisp_only10'] / df['TOT_POP_2010']) * 100
df['black_pct10'] = (df['pop_black_only10'] / df['TOT_POP_2010']) * 100
df['native_pct10'] = (df['pop_native_only10'] / df['TOT_POP_2010']) * 100
df['asian_pct10'] = (df['pop_asian_only10'] / df['TOT_POP_2010']) * 100
df['polynesian_pct10'] = (df['pop_polynesian_only10'] / df['TOT_POP_2010']) * 100
df['latino_pct10'] = (df['pop_hispanic10'] / df['TOT_POP_2010']) * 100
df['other_pct10'] = (df['pop_other_only10'] / df['TOT_POP_2010']) * 100
df['multiracial_pct10'] = (df['pop_multiracial10'] / df['TOT_POP_2010']) * 100

white18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B03002_003E')]
white18 = white18[['GEOID','COUNTY','TRACT_NUM','DATA']]
white18 = white18.rename(columns = {'DATA' : 'pop_white_nonhisp_only18'})
black18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_003E')]
black18 = black18[['GEOID','COUNTY','TRACT_NUM','DATA']]
black18 = black18.rename(columns = {'DATA' : 'pop_black_only18'})
native18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_004E')]
native18 = native18[['GEOID','COUNTY','TRACT_NUM','DATA']]
native18 = native18.rename(columns = {'DATA' : 'pop_native_only18'})
asian18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_005E')]
asian18 = asian18[['GEOID','COUNTY','TRACT_NUM','DATA']]
asian18 = asian18.rename(columns = {'DATA' : 'pop_asian_only18'})
polynesian18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_006E')]
polynesian18 = polynesian18[['GEOID','COUNTY','TRACT_NUM','DATA']]
polynesian18 = polynesian18.rename(columns = {'DATA' : 'pop_polynesian_only18'})
latino18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B03002_012E')]
latino18 = latino18[['GEOID','COUNTY','TRACT_NUM','DATA']]
latino18 = latino18.rename(columns = {'DATA' : 'pop_hispanic18'})
other18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_007E')]
other18 = other18[['GEOID','COUNTY','TRACT_NUM','DATA']]
other18 = other18.rename(columns = {'DATA' : 'pop_other_only18'})
multiracial18 = rdf18[(rdf18['CENSUS_QUERY'] == 'B02001_008E')]
multiracial18 = multiracial18[['GEOID','COUNTY','TRACT_NUM','DATA']]
multiracial18 = multiracial18.rename(columns = {'DATA' : 'pop_multiracial18'})
racial18 = white18.merge(black18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial18 = racial18.merge(native18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial18 = racial18.merge(asian18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial18 = racial18.merge(polynesian18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial18 = racial18.merge(latino18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial18 = racial18.merge(other18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
racial18 = racial18.merge(multiracial18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
race_data18 = racial18[['GEOID','COUNTY','TRACT_NUM','pop_white_nonhisp_only18','pop_black_only18','pop_native_only18','pop_asian_only18','pop_polynesian_only18','pop_hispanic18','pop_other_only18','pop_multiracial18']]

df = df.merge(race_data18, how = 'inner', left_on = ['GEOID','COUNTY','TRACT_NUM'], right_on = ['GEOID','COUNTY','TRACT_NUM'])
df['minority_pop18'] = df['TOT_POP_2018'] - df['pop_white_nonhisp_only18']
df['minority_pop_pct18'] = (df['minority_pop18'] / df['TOT_POP_2018']) * 100
df['white_pct18'] = (df['pop_white_nonhisp_only18'] / df['TOT_POP_2018']) * 100
df['black_pct18'] = (df['pop_black_only18'] / df['TOT_POP_2018']) * 100
df['native_pct18'] = (df['pop_native_only18'] / df['TOT_POP_2018']) * 100
df['asian_pct18'] = (df['pop_asian_only18'] / df['TOT_POP_2018']) * 100
df['polynesian_pct18'] = (df['pop_polynesian_only18'] / df['TOT_POP_2018']) * 100
df['latino_pct18'] = (df['pop_hispanic18'] / df['TOT_POP_2018']) * 100
df['other_pct18'] = (df['pop_other_only18'] / df['TOT_POP_2018']) * 100
df['multiracial_pct18'] = (df['pop_multiracial18'] / df['TOT_POP_2018']) * 100

df['minority_pop_delta'] = df['minority_pop_pct18'] - df['minority_pop_pct10']
df['white_pop_delta'] = df['white_pct18'] - df['white_pct10']
df['black_pop_delta'] = df['black_pct18'] - df['black_pct10']
df['native_pop_delta'] = df['native_pct18'] - df['native_pct10']
df['asian_pop_delta'] = df['asian_pct18'] - df['asian_pct10']
df['polynesian_pop_delta'] = df['polynesian_pct18'] - df['polynesian_pct10']
df['latino_pop_delta'] = df['latino_pct18'] - df['latino_pct10']
df['other_pop_delta'] = df['minority_pop18'] - df['minority_pop10']
df['minority_pop_delta'] = df['other_pct18'] - df['other_pct10']
df['multiracial_pop_delta'] = df['multiracial_pct18'] - df['multiracial_pct10']

def get_df(subset='all'):
    subsets = {
        'all': df #,
#        'wallingford': wallingford_df
    }

    if subset in subsets:
        return subsets[subset]
    else:
        raise('ERROR - Unrecognized subset. Must be one of {}, bet received: {}'.format(subsets.keys(), subset))
