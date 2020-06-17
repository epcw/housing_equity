import dash
import os
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import json
import geopandas as gp

app = dash.Dash(__name__)

application = app.server
#app.config.suppress_callback_exceptions = True

app.title = "Housing Equity in Seattle | EPCW"

#read in shapefile (needs to be in GeoJSON format)
with open('washingtongeo.json','r') as GeoJSON:
    tracts = json.load(GeoJSON)

#this is code to be able to read in a shapefile and print out a json.  You only need to do this once and once you have the json, you're good.
#os.getcwd()
#gdf = gp.read_file('data/cb_2018_53_tract_500k.shp')
#gdf.to_file("washington.geojson", driver='GeoJSON')

#read in the json from covidtracking.  You can also do df=pd.read_csv('CSVFILE') for csvs
df= pd.read_csv('data/housing-expanded.csv',
                   dtype={"GEOID": str})
#data_max = df['Data'].max()
the_bounty = {"lat": 47.6615392, "lon": -122.3446507}
#bob = gdf[gdf['COUNTYFP']=='033'].merge(df, left_on='TRACTCE', right_on='Tract', how='left')

#extract lower quartile of contract rent from df
dataset = df[(df['Query_code'] == 'B25057_001E')]
dataset18 = dataset[(dataset['Year'] == 2018)]
dataset18 = dataset18.rename(columns = {'Data' : 'Data2018'})
dataset10 = dataset[(dataset['Year'] == 2010)]
dataset10 = dataset10.rename(columns = {'Data' : 'Data2010'})
dataset_merged = dataset10.merge(dataset18, left_on='GEOID', right_on='GEOID', how='inner')
print(dataset_merged)
#calc change in cost from 2010 to 2018
dataset_merged['Data_change'] = (dataset_merged.Data2018 - dataset_merged.Data2010) / dataset_merged.Data2010 * 100
data_max = dataset_merged['Data_change'].max()
#print(df.GEOID)
#print(data_max)
fig = go.Figure(go.Choroplethmapbox(geojson=tracts, locations=dataset18['GEOID'], z=dataset_merged['Data_change'],featureidkey='properties.GEOID',
                                zmin=-10, zmax=100,     #colorscale="Viridis",
                                    marker_opacity=0.5, marker_line_width=0))

fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=9, mapbox_center = the_bounty)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


app.layout = html.Div([
#        dcc.Link('Dashboard Home', href='/',id="app_menu"),
        html.H1(id='housing_title',children='Under Construction'),
        html.H3('Dashboard by Center for Equitable Policy in a Changing World', id='subheading'),
        dcc.Graph(figure=fig,
            id='housing'
        )
    ])

'''
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

import plotly.graph_objects as go

fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df.fips, z=df.unemp,
                                    colorscale="Viridis", zmin=0, zmax=12,
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

'''
if __name__ == '__main__':
    # Beanstalk expects it to be running on 8080.
    application.run(debug=True, port=8080)
