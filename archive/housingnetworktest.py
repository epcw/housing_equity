import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import json
import geopandas as gp
import gc
import pyarrow

#import dash_dangerously_set_inner_html

#from application import app
from dashbase import app

app.title = "Housing testbed | EPCW"

#read in shapefile (needs to be in GeoJSON format)
with open('data/washingtongeo.json','r') as GeoJSON:
    tracts = json.load(GeoJSON)

#read in the json from covidtracking.  You can also do df=pd.read_csv('CSVFILE') for csvs
df= pd.read_csv('data/housing_test.csv',
                   dtype={"TRACT_NUM": str,"YEAR": str})

#set a map center
the_bounty = {"lat": 47.6615392, "lon": -122.3446507}

#create column called GEOID (a single string id column for matching map data)
df.loc[(df['COUNTY'] == 'King'), 'GEOID'] = '53033' + df['TRACT_NUM']
df.loc[(df['COUNTY'] == 'Pierce'), 'GEOID'] = '53053' + df['TRACT_NUM']
df.loc[(df['COUNTY'] == 'Snohomish'), 'GEOID'] = '53061' + df['TRACT_NUM']

#extract variables of interest
tot_popa = df[(df['CENSUS_QUERY'] == 'B01001_001E')]
born_other_statea = df[(df['CENSUS_QUERY'] == 'B06010_033E')]
born_foreign_75kplusa = df[(df['CENSUS_QUERY'] == 'B06010_055E')]
lowest_quint_household_incomea = df[(df['CENSUS_QUERY'] == 'B19080_001E')]
eighty_pctile_household_incomea = df[(df['CENSUS_QUERY'] == 'B19080_004E')]
del df

#tot_pop = tot_popa.rename(columns = {'DATA' : 'TOT_POP'})
tot_popb = tot_popa[(tot_popa['YEAR'] == '2010')]
tot_pop_compare = tot_popb.rename(columns = {'DATA' : 'TOT_POP_2010'})
tot_popc = tot_popa[(tot_popa['YEAR'] == '2018')]
tot_pop18 = tot_popc.rename(columns = {'DATA' : 'TOT_POP_2018'})
tot_pop_compare = tot_pop_compare.merge(tot_pop18, how = 'inner', on = ['COUNTY','TRACT_NUM','DATASET','GEOID','HUMAN_READABLE','CENSUS_QUERY'])
#clean the dataframe the fuck up
tot_pop_compare.drop(['CENSUS_QUERY','HUMAN_READABLE','YEAR_x','YEAR_y'], axis=1, inplace = True)
del tot_popb, tot_popc, tot_pop18, tot_popa

#born_other_state = born_other_statea.rename(columns = {'DATA' : 'BORN_OTHER_US_STATE'})
born_other_stateb = born_other_statea[(born_other_statea['YEAR'] == '2010')]
born_other_state_compare = born_other_stateb.rename(columns = {'DATA' : 'BORN_OTHER_US_STATE_2010'})
born_other_statec = born_other_statea[(born_other_statea['YEAR'] == '2018')]
born_other_state18 = born_other_statec.rename(columns = {'DATA' : 'BORN_OTHER_US_STATE_2018'})
born_other_state_compare = born_other_state_compare.merge(born_other_state18, how = 'inner', on = ['COUNTY','TRACT_NUM','DATASET','GEOID','HUMAN_READABLE','CENSUS_QUERY'])
born_other_state_compare.drop(['CENSUS_QUERY','HUMAN_READABLE','YEAR_x','YEAR_y'], axis=1, inplace = True)
del born_other_stateb, born_other_statec, born_other_state18, born_other_statea

#born_foreign_75kplus = born_foreign_75kplusa.rename(columns = {'DATA' : 'BORN_FOREIGN_75KPLUS'})
born_foreign_75kplusb = born_foreign_75kplusa[(born_foreign_75kplusa['YEAR'] == '2010')]
born_foreign_75kplus_compare = born_foreign_75kplusb.rename(columns = {'DATA' : 'BORN_FOREIGN_75KPLUS_2010'})
born_foreign_75kplusc = born_foreign_75kplusa[(born_foreign_75kplusa['YEAR'] == '2018')]
born_foreign_75kplus18 = born_foreign_75kplusc.rename(columns = {'DATA' : 'BORN_FOREIGN_75KPLUS_2018'})
born_foreign_75kplus_compare = born_foreign_75kplus_compare.merge(born_foreign_75kplus18, how = 'inner', on = ['COUNTY','TRACT_NUM','DATASET','GEOID','HUMAN_READABLE','CENSUS_QUERY'])
born_foreign_75kplus_compare.drop(['CENSUS_QUERY','HUMAN_READABLE','YEAR_x','YEAR_y'], axis=1, inplace = True)
del born_foreign_75kplusb, born_foreign_75kplusc, born_foreign_75kplus18, born_foreign_75kplusa

twenty_pctile_household_incomeb = lowest_quint_household_incomea[(lowest_quint_household_incomea['YEAR'] == '2010')]
twenty_pctile_household_income_compare = twenty_pctile_household_incomeb.rename(columns = {'DATA' : 'TWENTY_PCTILE_2010'})
twenty_pctile_household_incomec = lowest_quint_household_incomea[(lowest_quint_household_incomea['YEAR'] == '2018')]
twenty_pctile_household_income18 = twenty_pctile_household_incomec.rename(columns = {'DATA' : 'TWENTY_PCTILE_2018'})
twenty_pctile_household_income_compare = twenty_pctile_household_income_compare.merge(twenty_pctile_household_income18, how = 'inner', on = ['COUNTY','TRACT_NUM','DATASET','GEOID','HUMAN_READABLE','CENSUS_QUERY'])
twenty_pctile_household_income_compare.drop(['CENSUS_QUERY','HUMAN_READABLE','YEAR_x','YEAR_y'], axis=1, inplace = True)
del twenty_pctile_household_incomeb, twenty_pctile_household_incomec, twenty_pctile_household_income18, lowest_quint_household_incomea

eighty_pctile_household_incomeb = eighty_pctile_household_incomea[(eighty_pctile_household_incomea['YEAR'] == '2010')]
eighty_pctile_household_income_compare = eighty_pctile_household_incomeb.rename(columns = {'DATA' : 'EIGHTY_PCTILE_2010'})
eighty_pctile_household_incomec = eighty_pctile_household_incomea[(eighty_pctile_household_incomea['YEAR'] == '2018')]
eighty_pctile_household_income18 = eighty_pctile_household_incomec.rename(columns = {'DATA' : 'EIGHTY_PCTILE_2018'})
eighty_pctile_household_income_compare = eighty_pctile_household_income_compare.merge(eighty_pctile_household_income18, how = 'inner', on = ['COUNTY','TRACT_NUM','DATASET','GEOID','HUMAN_READABLE','CENSUS_QUERY'])
eighty_pctile_household_income_compare.drop(['CENSUS_QUERY','HUMAN_READABLE','YEAR_x','YEAR_y'], axis=1, inplace = True)
del eighty_pctile_household_incomeb, eighty_pctile_household_incomec, eighty_pctile_household_income18, eighty_pctile_household_incomea

#merge into one dataset with one row per year per tract and different columns for each query
#dataseta = tot_pop.merge(born_other_state, how = 'inner', on = ['COUNTY','TRACT_NUM','YEAR','DATASET','GEOID'])
#datasetb = dataseta.merge(born_foreign_75kplus, how = 'inner', on = ['COUNTY','TRACT_NUM','YEAR','DATASET','GEOID'])
#dataset = datasetb.merge(lowest_quint_household_income, how = 'inner', on = ['COUNTY','TRACT_NUM','YEAR','DATASET','GEOID'])

#merge into one dataset to compare 2010 and 2018
comparisona = tot_pop_compare.merge(born_other_state_compare, how = 'inner', on = ['COUNTY','TRACT_NUM','DATASET','GEOID'])
#comparisona.drop(['CENSUS_QUERY','HUMAN_READABLE','YEAR_x','YEAR_y'], axis=1, inplace = True)
del tot_pop_compare,born_other_state_compare
comparisonb = comparisona.merge(born_foreign_75kplus_compare, how = 'inner', on = ['COUNTY','TRACT_NUM','DATASET','GEOID'])
del comparisona, born_foreign_75kplus_compare
comparisonc = comparisonb.merge(twenty_pctile_household_income_compare, how = 'inner', on = ['COUNTY','TRACT_NUM','DATASET','GEOID'])
del comparisonb, twenty_pctile_household_income_compare
comparison = comparisonc.merge(eighty_pctile_household_income_compare, how = 'inner', on = ['COUNTY','TRACT_NUM','DATASET','GEOID'])
del comparisonc, eighty_pctile_household_income_compare
#comparison.drop(['CENSUS_QUERY_x','CENSUS_QUERY_y','HUMAN_READABLE_x','HUMAN_READABLE_y','YEAR_y_x','YEAR_x_y','YEAR_y_y'], axis=1, inplace = True,inplace = True))

#calculated variables
#dataset['BORN_OTHER_US_STATE_PCT'] = dataset.BORN_OTHER_US_STATE / dataset.TOT_POP * 100
#dataset['BORN_FOREIGN_75KPLUS_PCT'] = dataset.BORN_FOREIGN_75KPLUS / dataset.TOT_POP * 100
comparison['BORN_OTHER_US_STATE_PCT_2010'] = comparison.BORN_OTHER_US_STATE_2010 / comparison.TOT_POP_2010 * 100
comparison['BORN_OTHER_US_STATE_PCT_2018'] = comparison.BORN_OTHER_US_STATE_2018 / comparison.TOT_POP_2018 * 100
comparison['BORN_OTHER_US_STATE_PCT_CHANGE'] = (comparison.BORN_OTHER_US_STATE_PCT_2018 - comparison.BORN_OTHER_US_STATE_PCT_2010)
comparison['BORN_FOREIGN_75KPLUS_PCT_2010'] = comparison.BORN_FOREIGN_75KPLUS_2010 / comparison.TOT_POP_2010 * 100
comparison['BORN_FOREIGN_75KPLUS_PCT_2018'] = comparison.BORN_FOREIGN_75KPLUS_2018 / comparison.TOT_POP_2018 * 100
comparison['BORN_FOREIGN_75KPLUS_PCT_CHANGE'] = (comparison.BORN_FOREIGN_75KPLUS_PCT_2018 - comparison.BORN_FOREIGN_75KPLUS_PCT_2010)
comparison['INCOME_GAP_2010'] = (comparison.TWENTY_PCTILE_2010 / comparison.EIGHTY_PCTILE_2010) * 100
comparison['INCOME_GAP_2018'] = (comparison.TWENTY_PCTILE_2018 / comparison.EIGHTY_PCTILE_2018) * 100
comparison['INCOME_GAP_CHANGE'] = (comparison.INCOME_GAP_2018 - comparison.INCOME_GAP_2010)

#dataset['GEOID'] = '53033' + dataset['TRACT_NUM'].astype(str)
#data_max_quint = dataset['LOWEST_QUINTILE_HOUSEHOLD_INCOME'].max()
#data_max_other = dataset['BORN_OTHER_US_STATE_PCT'].max()
#data_max_foreign = dataset['BORN_FOREIGN_75KPLUS_PCT'].max()
data_max_other10 = comparison['BORN_OTHER_US_STATE_PCT_2010'].max()
data_max_other18 = comparison['BORN_OTHER_US_STATE_PCT_2018'].max()
data_max_otherdelta = comparison['BORN_OTHER_US_STATE_PCT_CHANGE'].max()
#data_min_otherdelta = comparison['BORN_OTHER_US_STATE_PCT_CHANGE'].min()
data_max_foreign10 = comparison['BORN_FOREIGN_75KPLUS_PCT_2010'].max()
data_max_foreign18 = comparison['BORN_FOREIGN_75KPLUS_PCT_2018'].max()
data_max_foreigndelta = comparison['BORN_FOREIGN_75KPLUS_PCT_CHANGE'].max()
#data_min_foreigndelta = comparison['BORN_FOREIGN_75KPLUS_PCT_CHANGE'].min()
data_max_incomegap10 = comparison['INCOME_GAP_2010'].max()
data_max_incomegap18 = comparison['INCOME_GAP_2018'].max()
data_max_incomegapdelta = comparison['INCOME_GAP_CHANGE'].max()

gc.collect()
#alldfs = [var for var in dir() if isinstance(eval(var), pd.core.frame.DataFrame)] #check for all open dfs to see if any temp ones are still opened.
#print(alldfs)

comparison.to_csv('data/housing_prepped.csv', index=False)

#Graph layout for income row (figs 1 # 2)
fig = go.Figure(go.Choroplethmapbox(geojson=tracts, locations=comparison['GEOID'], z=comparison['INCOME_GAP_2010'],featureidkey='properties.GEOID',
                                zmin=0, zmax=data_max_incomegap10,     colorscale="RdYlGn",
                                    marker_opacity=0.5, marker_line_width=0))

fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=8, mapbox_center = the_bounty)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig2 = go.Figure(go.Choroplethmapbox(geojson=tracts, locations=comparison['GEOID'], z=comparison['INCOME_GAP_2018'],featureidkey='properties.GEOID',
                                zmin=0, zmax=data_max_incomegap10,     colorscale="RdYlGn",
                                    marker_opacity=0.5, marker_line_width=0))

fig2.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=8, mapbox_center = the_bounty)
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig2c = go.Figure(go.Choroplethmapbox(geojson=tracts, locations=comparison['GEOID'], z=comparison['INCOME_GAP_CHANGE'],featureidkey='properties.GEOID',
                                zmin=-data_max_incomegapdelta, zmid=0, zmax=data_max_incomegapdelta,     colorscale="RdYlGn",
                                    marker_opacity=0.5, marker_line_width=0))

fig2c.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=8, mapbox_center = the_bounty)
fig2c.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#Graph layout for domestic immigration row (figs 3 & 4)
fig3 = go.Figure(go.Choroplethmapbox(geojson=tracts, locations=comparison['GEOID'], z=comparison['BORN_OTHER_US_STATE_PCT_2010'],featureidkey='properties.GEOID',
                                zmin=0, zmax=data_max_other10,     colorscale="deep",
                                    marker_opacity=0.5, marker_line_width=0))

fig3.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=8, mapbox_center = the_bounty)
fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig4 = go.Figure(go.Choroplethmapbox(geojson=tracts, locations=comparison['GEOID'], z=comparison['BORN_OTHER_US_STATE_PCT_2018'],featureidkey='properties.GEOID',
                                zmin=0, zmax=data_max_other18,     colorscale="deep",
                                    marker_opacity=0.5, marker_line_width=0))

fig4.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=8, mapbox_center = the_bounty)
fig4.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig4c = go.Figure(go.Choroplethmapbox(geojson=tracts, locations=comparison['GEOID'], z=comparison['BORN_OTHER_US_STATE_PCT_CHANGE'],featureidkey='properties.GEOID',
                                zmin=-data_max_otherdelta, zmid=0, zmax=data_max_otherdelta,     colorscale="BrBG",
                                    marker_opacity=0.5, marker_line_width=0))

fig4c.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=8, mapbox_center = the_bounty)
fig4c.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#Graph layout for foreign immigration row (figs 5 & 6)
fig5 = go.Figure(go.Choroplethmapbox(geojson=tracts, locations=comparison['GEOID'], z=comparison['BORN_FOREIGN_75KPLUS_PCT_2010'],featureidkey='properties.GEOID',
                                zmin=0, zmax=data_max_foreign10,     colorscale="dense",
                                    marker_opacity=0.5, marker_line_width=0))

fig5.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=8, mapbox_center = the_bounty)
fig5.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig6 = go.Figure(go.Choroplethmapbox(geojson=tracts, locations=comparison['GEOID'], z=comparison['BORN_FOREIGN_75KPLUS_PCT_2018'],featureidkey='properties.GEOID',
                                zmin=0, zmax=data_max_foreign18,     colorscale="dense",
                                    marker_opacity=0.5, marker_line_width=0))

fig6.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=8, mapbox_center = the_bounty)
fig6.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig6c = go.Figure(go.Choroplethmapbox(geojson=tracts, locations=comparison['GEOID'], z=comparison['BORN_FOREIGN_75KPLUS_PCT_CHANGE'],featureidkey='properties.GEOID',
                                zmin=-data_max_foreigndelta, zmid=0, zmax=data_max_foreigndelta,     colorscale="BrBG",
                                    marker_opacity=0.5, marker_line_width=0))

fig6c.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=8, mapbox_center = the_bounty)
fig6c.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def layout():
    return html.Div([
        dcc.Link('Dashboard Home', href='/',id="app_menu"),
        html.Div([
        html.H1('Tech worker immigration into Seattle'),
        html.P('Foreign born population making more than $75,000/yr',className='description graph_title'),
        html.Div([
        html.Div([
        html.H2(className='graph_title',children='2010'),
        dcc.Graph(figure=fig5,
            id='foreign_immigration_2010'
        )],className='col-4'),
        html.Div([
        html.H2(className='graph_title',children='2018'),
        dcc.Graph(figure=fig6,
            id='foreign_immigration_2018'
        )],className='col-4'),
        html.Div([
        html.H2(className='graph_title',children='%change'),
        dcc.Graph(figure=fig6c,
            id='foreign_immigration_delta'
        )],className='col-4')],className='multi-col'),
        ],className='container'),
        html.Div([
        html.H1('Tech worker immigration into Seattle'),
        html.P('Population born in another US state making more than $75,000/yr',className='description graph_title'),
        html.Div([
        html.Div([
        html.H2(className='graph_title',children='2010'),
        dcc.Graph(figure=fig3,
            id='domestic_immigration_2010'
        )],className='col-4'),
        html.Div([
        html.H2(className='graph_title',children='2018'),
        dcc.Graph(figure=fig4,
            id='domestic_immigration_2018'
        )],className='col-4'),
        html.Div([
        html.H2(className='graph_title',children='%change'),
        dcc.Graph(figure=fig4c,
            id='domestic_immigration_delta'
        )],className='col-4')],className='multi-col'),
        ],className='container'),
        html.Div([
        html.H1('Income gap change, 2010-18'),
        html.P('Percentage of 80th %ile income that a household making the 20th %ile will earn (20th %ile/80th %ile)', className='description graph_title'),
        html.Div([
        html.Div([
        html.H2(className='graph_title',children='2010'),
        dcc.Graph(figure=fig,
            id='income_gap_2010'
        )],className='col-4'),
        html.Div([
        html.H2(className='graph_title',children='2018'),
        dcc.Graph(figure=fig2,
            id='income_gap_2018'
        )],className='col-4'),
        html.Div([
        html.H2(className='graph_title',children='%change'),
        dcc.Graph(figure=fig2c,
            id='income_gap_delta'
        )],className='col-4')],className='multi-col'),
        ],className='container'),
        #html.H1('Testing NetworkX Example'),
        #html.P('Example comparison', className='description'),
        #dcc.Graph(figure=fig5,
#            id='housing_networkx_example'
#        ),
        html.Div([
        generate_table(comparison)
        ],className='container')
    ],id='housingnetworktestpage')
