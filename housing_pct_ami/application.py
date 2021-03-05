import dash #comment out for production deployment
import dash_core_components as dcc
import dash_html_components as html
import json
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from flask_caching import Cache

#set root directory for data files
#ROOTBEER = '/home/ubuntu/housing_equity/sandbox-singlepage/' #production
ROOTBEER = '' #local

#from dashbase import app, application #production version
app = dash.Dash(__name__) #local
application = app.server #local

#this pulls in the header HTML from header.py
from template import Template
grid = Template()
app.index_string = grid
app.title = "Dashboards | EPCW"

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache'
})

import os, shutil
folder = 'cache'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

TIMEOUT = 60

@cache.memoize(timeout=TIMEOUT)
def df():
    dataframe = pd.read_csv(ROOTBEER + 'data/df.csv', dtype={"GEOID": str,"TRACT_NUM": str,"YEAR":str})
    return dataframe

#df_debug = pd.read_csv(ROOTBEER + 'data/df.csv', dtype={"GEOID": str,"TRACT_NUM": str,"YEAR":str}) #for debugging df only

#set a map center (for maps only, obviously)
the_bounty = {"lat": 47.6615392, "lon": -122.3446507}

#read in shapefile (needs to be in GeoJSON format)
#with open('/home/ubuntu/dash/data/washingtongeo.json','r') as GeoJSON:
with open('data/washingtongeo.json','r') as GeoJSON:
    tracts = json.load(GeoJSON)

#PLOT
#here we make the graph a function called serve_layout(), which then allows us to have it run every time the page is loaded (unlike the normal which would just be app.layer = GRAPH CONTENT, which would run every time the app was started on the server (aka, once))
def serve_layout():
    return html.Div([
        dcc.Link('Dashboard Home', href='/', id="app_menu"),
        html.Div([
        html.H1(id='housing_title',children='Change in median housing cost as a percentage of area median income in Seattle, 2013-2018'),
        html.H3('Dashboard by Center for Equitable Policy in a Changing World', id='subheading'),
        html.Div(id='data-dropdown', children=[
            html.H4('Data Selection'),
            dcc.Dropdown(
                id='data_selection',
                options=[{'label': i, 'value': i} for i in [
                    'Median Monthly Housing Cost as pct Area Median Monthly Income',
                    'Median Monthly Housing Costs',
                    'Area Median Monthly Income',
                    'Non-white Population'
                ]],
                value='Median Monthly Housing Cost as pct Area Median Monthly Income'
            )]),
        html.P(
            'Data Source: ACS 5 year 2010-2019',
            className='description'),
        dcc.Graph(
                      id='housing_map_change'
                      )
        ], className='container'),
        html.Div([
            html.H1('2013 vs 2018'),
            html.P('These maps compare the change in Seattle from 2013-2018.',
                   className='description graph_title'),
            html.Div([
                html.Div([
                    html.H2(className='graph_title', children='2013'),
                    dcc.Graph(
                              id='housing_2013'
                              )], className='col-6'),
                html.Div([
                    html.H2(className='graph_title', children='2018'),
                    dcc.Graph(
                              id='housing_2018'
                              )], className='col-6')], className='multi-col'),
        ], className='container')
        ], id='housing_maps_page')

# callback for housing_change_map
@app.callback(
    Output('housing_map_change', 'figure'),
    [Input('data_selection', 'value')])

# updates graph based on user input
def update_graph(data_selection):
    return {
        'data': [ go.Choroplethmapbox(
            geojson=tracts,
            locations=df()['GEOID'],
            featureidkey='properties.GEOID',
            zmin=-1 if data_selection == 'Median Monthly Housing Costs'
                else(-1 if data_selection == 'Non-white Population'
                else(-1 if data_selection == 'Area Median Monthly Income'
                else -1)),
            zmax=1 if data_selection == 'Median Monthly Housing Costs'
                else(1 if data_selection == 'Non-white Population'
                else(1 if data_selection == 'Area Median Monthly Income'
                else 1)),
            colorscale='RdYlGn_r' if data_selection == 'Median Monthly Housing Cost'
            else('RdYlGn' if data_selection == 'Area Median Monthly Income'
            else('RdYlGn' if data_selection == 'Non-white Population'
            else 'RdYlGn_r')),
            marker_opacity=0.5,
            marker_line_width=0,
            z=df()['housing_pct_ami_change' if data_selection == 'Median Monthly Housing Cost as pct Area Median Monthly Income'
                else('ami_monthly_change' if data_selection == 'Area Median Monthly Income'
                else('monthly_housing_cost_change' if data_selection == 'Median Monthly Housing Costs'
                else 'minority_pop_pct_change'))])
        ],
        'layout': go.Layout(
            mapbox_style="carto-positron",
            mapbox_zoom=10,
            mapbox_center=the_bounty,
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )
    }

# callback for housing_2013
@app.callback(
    Output('housing_2013', 'figure'),
    [Input('data_selection', 'value')])

# updates graph based on user input
def update_graph13(data_selection):
    return {
        'data': [ go.Choroplethmapbox(
            geojson=tracts,
            locations=df()['GEOID'],
            featureidkey='properties.GEOID',
            zmin=-50 if data_selection == 'Median Monthly Housing Costs'
                else(0 if data_selection == 'Non-white Population'
                else(10000/12 if data_selection == 'Area Median Monthly Income'
                else .15)),
            zmax=2500 if data_selection == 'Median Monthly Housing Costs'
                else(.7 if data_selection == 'Non-white Population'
                else(60000/12 if data_selection == 'Area Median Monthly Income'
                else .6)),
            colorscale='RdYlGn_r' if data_selection == 'Median Monthly Housing Cost'
            else('RdYlGn' if data_selection == 'Area Median Monthly Income'
            else('RdYlGn' if data_selection == 'Non-white Population'
            else 'RdYlGn_r')),
            marker_opacity=0.5,
            marker_line_width=0,
            z=df()['housing_pct_ami_2013' if data_selection == 'Median Monthly Housing Cost as pct Area Median Monthly Income'
                else('ami_monthly_2013' if data_selection == 'Area Median Monthly Income'
                else('MEDIAN_MONTHLY_HOUSING_COST_2013' if data_selection == 'Median Monthly Housing Costs'
                else 'minority_pop_pct_2013'))])
        ],
        'layout': go.Layout(
            mapbox_style="carto-positron",
            mapbox_zoom=10,
            mapbox_center=the_bounty,
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )
    }


# callback for housing_2018
@app.callback(
    Output('housing_2018', 'figure'),
    [Input('data_selection', 'value')])

# updates graph based on user input
def update_graph18(data_selection):
    return {
        'data': [ go.Choroplethmapbox(
            geojson=tracts,
            locations=df()['GEOID'],
            featureidkey='properties.GEOID',
            zmin=-50 if data_selection == 'Median Monthly Housing Costs'
                else(0 if data_selection == 'Non-white Population'
                else(10000/12 if data_selection == 'Area Median Monthly Income'
                else .15)),
            zmax=2500 if data_selection == 'Median Monthly Housing Costs'
                else(.7 if data_selection == 'Non-white Population'
                else(60000/12 if data_selection == 'Area Median Monthly Income'
                else .60)),
            colorscale='RdYlGn_r' if data_selection == 'Median Monthly Housing Cost'
            else('RdYlGn' if data_selection == 'Area Median Monthly Income'
            else('RdYlGn' if data_selection == 'Non-white Population'
            else 'RdYlGn_r')),
            marker_opacity=0.5,
            marker_line_width=0,
            z=df()['housing_pct_ami_2013' if data_selection == 'Median Monthly Housing Cost as pct Area Median Monthly Income'
                else('ami_monthly_2013' if data_selection == 'Area Median Monthly Income'
                else('MEDIAN_MONTHLY_HOUSING_COST_2018' if data_selection == 'Median Monthly Housing Costs'
                else 'minority_pop_pct_2013'))])
        ],
        'layout': go.Layout(
            mapbox_style="carto-positron",
            mapbox_zoom=10,
            mapbox_center=the_bounty,
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )
    }

#this calls the serve_layout function to run on app load.
app.layout = serve_layout

if __name__ == '__main__':
#     application.run(host='0.0.0.0',port=80)    # production version
    application.run(debug=True, port=8080) #local version