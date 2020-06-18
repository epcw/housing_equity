import dash
import dash_core_components as dcc
import dash_html_components as html
#from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
#import json
import geopandas as gp
from geopy import distance
from fa2 import ForceAtlas2
import matplotlib
import matplotlib.pyplot as plt
import sklearn
from sklearn.cluster import KMeans
import numpy as np

app = dash.Dash(__name__)
# Beanstalk looks for application by default, if this isn't set you will get a WSGI error.
application = app.server

#this pulls in the header HTML from header.py
from template import Template
grid = Template()
app.index_string = grid
app.title = "Dashboards | EPCW"

df= pd.read_csv('data/housing_prepped.csv', dtype={"GEOID": str,"TRACT_NUM": str})

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

#set a map center (for maps only, obviously)
the_bounty = {"lat": 47.6615392, "lon": -122.3446507}

''' 
#PLOT VERSION 1 (2D circle concept)
#define list of nodes (census tracts in this case)
node_list = list(set(df['GEOID']))
G = nx.Graph()
for i in node_list:
    G.add_node(i)

#define list of edges (distance between the same tract's 2010 and 2018 cost?  This is kind of a guess as might work)
#for i, row in gdf.iterrows():
#    G.add_edges_from([(row['GEOID_a'],row['GEOID_b'])])
for i, row in gdf.iterrows():
    G.add_weighted_edges_from([(row['GEOID_a'],row['GEOID_b'],row['alpha'])])
#    G.add_weighted_edges_from([(row['GEOID_a'],row['GEOID_b'],row['distance'])])
#    G.add_weighted_edges_from([(row['GEOID_a'],row['GEOID_b'],row['distance']) for i, row in gdf.iterrows()])

#set spring layout for position
pos = nx.spring_layout(G, k=.2, iterations=50)
for n, p in pos.items():
    G.nodes[n]['pos'] = p

#plot this bad boy
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1,color='#888'),
    hoverinfo='text',
    mode='lines'
)

for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='RdBu',
        reversescale=True,
        color=[],
        size=15,
        colorbar=dict(
            thickness=10,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)
    )
)

for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
'''

#PLOT 2 (Trying another kind)
node_list = list(set(df['GEOID']))
G = nx.MultiGraph()

forceatlas2 = ForceAtlas2(
                        # Behavior alternatives
                        outboundAttractionDistribution=False,  # Dissuade hubs
                        linLogMode=False,  # NOT IMPLEMENTED
                        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                        edgeWeightInfluence=3.0,

                        # Performance
                        jitterTolerance=1.0,  # Tolerance
                        barnesHutOptimize=True,
                        barnesHutTheta=1.2,
                        multiThreaded=False,  # NOT IMPLEMENTED

                        # Tuning
                        scalingRatio=3.0,
                        strongGravityMode=False,
                        gravity=3.0,

                        # Log
                        verbose=True)

for i in node_list:
    G.add_node(i)

for i, row in gdf.iterrows():
    G.add_weighted_edges_from([(row['GEOID_a'],row['GEOID_b'],row['omega'])])

pos = forceatlas2.forceatlas2_networkx_layout(G,pos=None, iterations=1000)
for n, p in pos.items():
    G.nodes[n]['pos'] = p

#plot this bad boy
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=2,color='#000000'),
    hoverinfo='text',
    mode='lines'
)

for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='RdBu',
        reversescale=True,
        color=[],
        size=15,
        colorbar=dict(
            thickness=10,
            title='network based on Distance & minority population %',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)
    )
)

for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])

node_adjacencies = []

for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    #node_text.append('# of connections: '+str(len(adjacencies[1])))
#node_text = df["COUNTY"] + ' ' + df["TRACT_NUM"] + ' - ' +str(len(adjacencies[1])) + ' connections'
for node in G.nodes():
    node_text = df["TRACT_NUM"] + ' - ' + df['minority_pop_pct'].round(2).astype('str') + '%' + ' City: ' + df['CITYNAME']

node_trace.marker.color = df['labels']
node_trace.text = node_text

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

'''
#PLOT 3
with open('data/washingtongeo.json','r') as GeoJSON:
    tracts = json.load(GeoJSON)
df['alpha'] = (df['BORN_FOREIGN_75KPLUS_PCT_2010'] + df['BORN_OTHER_US_STATE_PCT_CHANGE']) * 100

data_max = df['alpha'].max()

fig = go.Figure(go.Choroplethmapbox(geojson=tracts, locations=df['GEOID'], z=df['alpha'],featureidkey='properties.GEOID',
                                zmin=0, zmax=data_max,     #colorscale="Viridis",
                                    marker_opacity=0.5, marker_line_width=0))

fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=9, mapbox_center = the_bounty)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
'''

#generate a table if you want this.  Else just comment out  56 rows because states+territories for this dataset If you really need to style this, can add some classes.
def generate_table(dataframe, max_rows=398):
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

#here we make the graph a function called serve_layout(), which then allows us to have it run every time the page is loaded (unlike the normal which would just be app.layer = GRAPH CONTENT, which would run every time the app was started on the server (aka, once))
def serve_layout():
    return html.Div([
        dcc.Link('Dashboard Home', href='/', id="app_menu"),
        html.Div([
            html.H1('Testing NetworkX'),
            html.P('Trying to get this to work', className='description'),
            dcc.Graph(figure=fig,
                      id='housing_networkx'
                      ),
             html.H1('Groupings'),
             html.P('Group 0 - size: ' + str(grp0_length), className='description'),
            generate_table(grp0),
            html.P('Group 1 - size: ' + str(grp1_length), className='description'),
            generate_table(grp1),
            html.P('Group 2 - size: ' + str(grp2_length), className='description'),
            generate_table(grp2),
            html.P('Group 3 - size: ' + str(grp3_length), className='description'),
            generate_table(grp3)
        ], className='container')
    ], id='sandbox')

#this calls the serve_layout function to run on app load.
app.layout = serve_layout

#callbacks for options
#log vs. linear toggler
#@app.callback(
#    Output('covid_19', 'figure'),
#    [Input('yaxis_type', 'value'),Input('data_selection', 'value')])

#updates graph based on user input
'''
def update_graph(yaxis_type,data_selection):
    return {
                'data': [ go.Scatter (
                    x=df[df['state'] == i]['date'],
                    y=df[df['state'] == i][
                    'hospitalized' if data_selection == 'Hospitalizations (Cumulative)'
                    else ('pct_positive' if data_selection == 'Percent of Positive Tests (Cumulative)'
                    else ('total' if data_selection == 'Total Tests (Cumulative)'
                    else ('deathIncrease' if data_selection == 'Deaths (Daily)'
                    else ('hospitalizedIncrease' if data_selection == 'Hospitalizations (Daily)'
                    else ('totalTestResultsIncrease' if data_selection == 'Total Tests (Daily)'
                    else 'death')))))],
                    mode='lines',
                    opacity=1,
                    name=i)
                    for i in df.state.unique()
                ],
                'layout': go.Layout (
                    title='Data source - covidtracking.com, updated 4pm PDT daily',
                    yaxis={'type': 'linear' if yaxis_type == 'Linear' else 'log',
                    'title':
                    'Hospitalizations (Cumulative)' if data_selection == 'Hospitalizations (Cumulative)'
                    else ('Percent of Positive Tests (Cumulative)' if data_selection == 'Percent of Positive Tests (Cumulative)'
                    else ('Total Tests (Cumulative)' if data_selection == 'Total Tests (Cumulative)'
                    else ('Deaths (Daily)' if data_selection == 'Deaths (Daily)'
                    else ('Hospitalizations (Daily)' if data_selection == 'Hospitalizations (Daily)'
                    else ('Total Tests (Daily)' if data_selection == 'Total Tests (Daily)'
                    else 'Deaths (Cumulative)')))))}, #axes options here https://plotly.com/python/axes/
                    xaxis={'type': 'date'}
                )
            }
'''



if __name__ == '__main__':
    # Beanstalk expects it to be running on 8080.
    application.run(debug=True, port=8080)
