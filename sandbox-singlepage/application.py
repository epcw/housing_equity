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
import data_prep

app = dash.Dash(__name__)
# Beanstalk looks for application by default, if this isn't set you will get a WSGI error.
application = app.server

#this pulls in the header HTML from header.py
from template import Template
grid = Template()
app.index_string = grid
app.title = "Dashboards | EPCW"

df = data_prep.get_df(subset='wallingford')
gdf = data_prep.get_gdf(subset='wallingford')
from data_prep import grp0
from data_prep import grp1
from data_prep import grp2
#from data_prep import grp3

grp0_length = str(grp0.shape)
grp1_length = str(grp1.shape)
grp2_length = str(grp2.shape)
#grp3_length = str(grp3.shape)

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
    mode='markers+text',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='RdBu',
        reversescale=True,
        color=[],
        size=15,
        colorbar=dict(
            thickness=10,
            title='network based on 25%ile rent cost & minority population %',
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

fig.update_traces(textfont_size=25)

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
            generate_table(grp2)#,
#            html.P('Group 3 - size: ' + str(grp3_length), className='description'),
#            generate_table(grp3)
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
