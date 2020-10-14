import dash #comment out for production deployment
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from fa2 import ForceAtlas2
from flask_caching import Cache
import plotly.express as px

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

TIMEOUT = 60

'''
#TRACT VERSION
import data_prep_tract
df = data_prep_tract.get_df(subset='wallingford')
gdf = data_prep_tract.get_gdf(subset='wallingford')
from data_prep_tract import grp0
from data_prep_tract import grp1
from data_prep_tract import grp2
#from data_prep_tract import grp3
'''

#BLOCK GROUP VERSION
import data_prep_blockgrp
df = data_prep_blockgrp.get_df(subset='wallingford')
gdf = data_prep_blockgrp.get_gdf(subset='wallingford')

from data_prep_blockgrp import grp0
from data_prep_blockgrp import grp1
from data_prep_blockgrp import grp2
from data_prep_blockgrp import grp3
grp3_length = str(grp3.shape)

grp0_length = str(grp0.shape)
grp1_length = str(grp1.shape)
grp2_length = str(grp2.shape)

#set a map center (for maps only, obviously)
the_bounty = {"lat": 47.6615392, "lon": -122.3446507}

#PLOT
node_list = list(set(df['GEOID']))
G = nx.Graph()
#G=nx.random_geometric_graph(1422,radius=-0.5)
'''
#normal version (no cache)
forceatlas2 = ForceAtlas2(
                        # Behavior alternatives
                        outboundAttractionDistribution=False,  # Dissuade hubs
                        linLogMode=False,  # NOT IMPLEMENTED
                        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                        edgeWeightInfluence=5.0,

                        # Performance
                        jitterTolerance=1.0,  # Tolerance
                        barnesHutOptimize=True,
                        barnesHutTheta=1.2,
                        multiThreaded=False,  # NOT IMPLEMENTED

                        # Tuning
                        scalingRatio=2,
                        strongGravityMode=True,
                        gravity=20.0,

                        # Log
                        verbose=True)
'''
for i in node_list:
    G.add_node(i)

for i, row in gdf.iterrows():
    G.add_weighted_edges_from([(row['GEOID_a'],row['GEOID_b'],row['omega'])])


#CACHE-USING VERSION
@cache.memoize(timeout=TIMEOUT)
def query_forceatlas2():
    forceatlas2 = ForceAtlas2(
                            # Behavior alternatives
                            outboundAttractionDistribution=False,  # Dissuade hubs
                            linLogMode=False,  # NOT IMPLEMENTED
                            adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                            edgeWeightInfluence=20.0, #was 5, testing if this can change things

                            # Performance
                            jitterTolerance=1.0,  # Tolerance
                            barnesHutOptimize=True,
                            barnesHutTheta=1.2,
                            multiThreaded=False,  # NOT IMPLEMENTED

                            # Tuning
                            scalingRatio=2,
                            strongGravityMode=True,
                            gravity=10.0, #was 20, still seeing a straight line.

                            # Log
                            verbose=True)
    return forceatlas2

def pos():
    return query_forceatlas2().forceatlas2_networkx_layout(G,pos=None, iterations=1000)

for n, p in pos().items():
    G.nodes[n]['pos'] = p
'''

#NON-CACHE-USING VERSION
pos = forceatlas2.forceatlas2_networkx_layout(G,pos=None, iterations=1000)

for n, p in pos.items():
    G.nodes[n]['pos'] = p
'''

#plot this bad boy
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1,color='#c6c6c6'),
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
    mode='markers+text', #make markers+text to show labels
    text=[],
    hoverinfo='text',
    customdata=df['GEOID'],
    marker=dict(
        showscale=False,
        colorscale='Edge',
        reversescale=False,
        color=[],
        size=30,
        opacity=0.8,
        colorbar=dict(
            thickness=10,
            title='COLOR GROUP BY CENSUS TRACT NUMBER',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)
    ),
    showlegend=True,
    marker_line_width=1,
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
    node_label = df["TRACT_NUM"] + ' block group ' + df["BLOCK_GRP"]
    node_text = df["TRACT_NUM"] + ', block group ' + df["BLOCK_GRP"] + '<br>' + 'Minority pop change: ' + (df['minority_pop_pct_change']).round(2).astype('str') + '% <br>' + '25%ile housing: ' + df['rent_25th_pctile_change'].round(2).astype('str') + '%'

df['tract_index'] = df['TRACT_NUM'].astype(int)

node_trace.marker.color = df['tract_index']
#node_trace.text = node_text
node_trace.text = node_label

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

#gdff = gdf[['GEOID_a','omega_bar']].drop_duplicates()
gdff = gdf.loc[:, gdf.columns.str.endswith('_a')]
gdfz = gdf[['GEOID_a','omega_bar']]
gdff = gdff.merge(gdfz, how = 'inner', left_on = ['GEOID_a'], right_on = ['GEOID_a'])
gdff['GEOID'] = gdff['GEOID_a'].astype(str)
gdff = gdff.sort_values('omega_bar')

fig2 = px.scatter(gdff, x="rent_25th_pctile_change_a", y="omega_bar",color='GEOID')
fig2.update_traces(marker=dict(size=20))

gdfcombo = gdf.loc[:, gdf.columns.str.endswith('_a')]
gdfcombo['GEOID'] = gdfcombo['GEOID_a'].astype(str)
alpha = 1/6.0
bravo = 1/6.0
charlie = 1/6.0
delta = 1/6.0
echo = 1/6.0
foxtrot = 1/6.0

gdfcombo['omega_13'] = (
        -(alpha * gdfcombo.minority_pop_pct_2013z_a) + \
        (bravo * gdfcombo.rent_25th_pctile_2013z_a) + \
        (charlie * gdfcombo.totpop_2013z_a) + \
        (delta * gdfcombo.rent_pct_income_2013z_a) + \
        -(echo * gdfcombo.affordable_units_per_cap_2013z_a) + \
        -(foxtrot * gdfcombo.median_tenancy_2013z_a) 
)

gdfcombo['omega_18'] = (
        -(alpha * gdfcombo.minority_pop_pct_2018z_a) + \
        (bravo * gdfcombo.rent_25th_pctile_2018z_a) + \
        (charlie * gdfcombo.totpop_2018z_a) + \
        (delta * gdfcombo.rent_pct_income_2018z_a) + \
        -(echo * gdfcombo.affordable_units_per_cap_2018z_a) + \
        -(foxtrot * gdfcombo.median_tenancy_2018z_a) 
)

fig3 = px.scatter(gdfcombo, x="omega_13", y="omega_18",color='GEOID')

#TODO: set up a scatterplot version of this to show change in pressure from 2013-8


#here we make the graph a function called serve_layout(), which then allows us to have it run every time the page is loaded (unlike the normal which would just be app.layer = GRAPH CONTENT, which would run every time the app was started on the server (aka, once))

def serve_layout():
    return html.Div([
        dcc.Link('Dashboard Home', href='/', id="app_menu"),
        html.Div([
            html.H1('Wallingford Urban Village Network'),
            html.P('Pilot network model of census block groups within the urban village of Wallingford (defined as all census block groups within 3km of 5303305002). Block groups that are closer together are more similar than those further apart. Census tracts (which may contain 1 or several block groups) are noted by color.', className='description'),
            html.P('Edge weights are determined by minority population percentage, by lowest quartile housing cost, housing tenancy, affordable housing stock, and housing cost as a percentage of household income (block groups that are closer together are more similar than those further apart).', className='description'),
            html.P('Census tracts (which may contain 1 or several block groups) are noted by color.', className='description'),
            dcc.Graph(figure=fig,
                      id='housing_networkx'
                      ),
            dcc.Graph(figure=fig2,
                      id='housing_bar'
                      ),
            dcc.Graph(figure=fig3,
                      id='displacement_scatter'
                      ),
             html.H1('Groupings'),
             html.P('Census Block Groups', className='description'),
             generate_table(gdff),
#            html.P('Group 1 - size: ' + str(grp1_length), className='description'),
#            generate_table(grp1),
#            html.P('Group 2 - size: ' + str(grp2_length), className='description'),
#            generate_table(grp2)#,
#            html.P('Group 3 - size: ' + str(grp3_length), className='description'),
#            generate_table(grp3)
        ], className='container')
    ], id='sandbox')

def generate_table(dataframe, max_rows=1422):
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

#@app.callback(
#    dash.dependencies.Output(component_id='data_table', component_property='children'),
#    [dash.dependencies.Input(component_id='housing_networkx', component_property='customdata')])
#def update_table(customdata):
    #node_name = clickData['nodes'][0]['customdata']
#    dff = df[(df['GEOID'] == 'customdata')]

#this calls the serve_layout function to run on app load.
app.layout = serve_layout

if __name__ == '__main__':
#    application.run(host='0.0.0.0',port=80)    # production version
    application.run(debug=True, port=8080) #local version