import pandas as pd
import geopandas as gp

path = '../shapefiles/WACensusBlocks2010/tl_2019_53_tabblock10.shp'
gdf = gp.read_file(path)

tracts_df = pd.read_csv('data/seattle_census_tracts.csv', dtype={'TRACT': str})

state = '53'   # WA = 53
county = '033' # King = 033

seattle_gdf = tracts_df.merge(gdf[(gdf['COUNTYFP10'] == county) & (gdf['STATEFP10'] == state)],
                              how='left',
                              left_on='TRACT',
                              right_on='TRACTCE10'
                              )

seattle_gdf = seattle_gdf[['STATEFP10', 'COUNTYFP10', 'TRACTCE10', 'BLOCKCE10', 'GEOID10', 'geometry']]
seattle_gdf['BLOCKGROUP'] = seattle_gdf['BLOCKCE10'].str.slice(0,1)

result_df = seattle_gdf[['TRACTCE10', 'BLOCKGROUP']].drop_duplicates()

result_df.to_csv('data/seattle_census_tract_and_blockgroup.csv', index=False)
