import dash #comment out for production deployment
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go #version for networkx
import networkx as nx
from fa2 import ForceAtlas2
from flask_caching import Cache
import plotly.express as px #version for maps
#from sklearn.cluster import KMeans #commented out because hiding Kmeans clusters for now.

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


#TRACT VERSION
import data_prep_tract
df = data_prep_tract.get_df()
gdf = data_prep_tract.get_gdf()
df_wallingford = data_prep_tract.get_df(subset='wallingford')
gdf_wallingford = data_prep_tract.get_gdf(subset='wallingford')
df_rb = data_prep_tract.get_df(subset='rainier_beach')
gdf_rb = data_prep_tract.get_gdf(subset='rainier_beach')
df_combo = data_prep_tract.get_df(subset='combo')
gdf_combo = data_prep_tract.get_gdf(subset='combo')
#df_mtbaker = data_prep_tract.get_df(subset='mtbaker_station')
#gdf_mtbaker = data_prep_tract.get_gdf(subset='mtbaker_station')
#df_othello = data_prep_tract.get_df(subset='othello_station')
#gdf_othello = data_prep_tract.get_gdf(subset='othello_station')
df_rb['GEOID_long'] = df_rb['GEOID']
df_rb['GEOID'] = df_rb['GEOID'].str.replace("53033", "")
gdf_rb['GEOID_long_a'] = gdf_rb['GEOID_a']
gdf_rb['GEOID_long_b'] = gdf_rb['GEOID_b']
gdf_rb['GEOID_a'] = gdf_rb['GEOID_a'].str.replace("53033", "")
gdf_rb['GEOID_b'] = gdf_rb['GEOID_b'].str.replace("53033", "")
#df_mtbaker['GEOID_long'] = df_mtbaker['GEOID']
#df_mtbaker['GEOID'] = df_mtbaker['GEOID'].str.replace("53033", "")
#gdf_mtbaker['GEOID_long_a'] = gdf_mtbaker['GEOID_a']
#gdf_mtbaker['GEOID_long_b'] = gdf_mtbaker['GEOID_b']
#gdf_mtbaker['GEOID_a'] = gdf_mtbaker['GEOID_a'].str.replace("53033", "")
#gdf_mtbaker['GEOID_b'] = gdf_mtbaker['GEOID_b'].str.replace("53033", "")
#df_othello['GEOID_long'] = df_othello['GEOID']
#df_othello['GEOID'] = df_othello['GEOID'].str.replace("53033", "")
#gdf_othello['GEOID_long_a'] = gdf_othello['GEOID_a']
#gdf_othello['GEOID_long_b'] = gdf_othello['GEOID_b']
#gdf_othello['GEOID_a'] = gdf_othello['GEOID_a'].str.replace("53033", "")
#gdf_othello['GEOID_b'] = gdf_othello['GEOID_b'].str.replace("53033", "")
df['GEOID_long'] = df['GEOID']
df['GEOID'] = df['GEOID'].str.replace("53033", "")
gdf['GEOID_long_a'] = gdf['GEOID_a']
gdf['GEOID_long_b'] = gdf['GEOID_b']
gdf['GEOID_a'] = gdf['GEOID_a'].str.replace("53033", "")
gdf['GEOID_b'] = gdf['GEOID_b'].str.replace("53033", "")
df_wallingford['GEOID_long'] = df_wallingford['GEOID']
df_wallingford['GEOID'] = df_wallingford['GEOID'].str.replace("53033", "")
gdf_wallingford['GEOID_long_a'] = gdf_wallingford['GEOID_a']
gdf_wallingford['GEOID_long_b'] = gdf_wallingford['GEOID_b']
gdf_wallingford['GEOID_a'] = gdf_wallingford['GEOID_a'].str.replace("53033", "")
gdf_wallingford['GEOID_b'] = gdf_wallingford['GEOID_b'].str.replace("53033", "")
df_combo['GEOID_long'] = df_combo['GEOID']
df_combo['GEOID'] = df_combo['GEOID'].str.replace("53033", "")
gdf_combo['GEOID_long_a'] = gdf_combo['GEOID_a']
gdf_combo['GEOID_long_b'] = gdf_combo['GEOID_b']
gdf_combo['GEOID_a'] = gdf_combo['GEOID_a'].str.replace("53033", "")
gdf_combo['GEOID_b'] = gdf_combo['GEOID_b'].str.replace("53033", "")

from data_prep_tract import tracts

'''
#BLOCK GROUP VERSION
import data_prep_blockgrp
df = data_prep_blockgrp.get_df()
gdf = data_prep_blockgrp.get_gdf()
df_wallingford = data_prep_blockgrp.get_df(subset='wallingford')
gdf_wallingford = data_prep_blockgrp.get_gdf(subset='wallingford')
df_rb = data_prep_blockgrp.get_df(subset='rainier_beach')
gdf_rb = data_prep_blockgrp.get_gdf(subset='rainier_beach')
df_mtbaker = data_prep_blockgrp.get_df(subset='mtbaker_station')
gdf_mtbaker = data_prep_blockgrp.get_gdf(subset='mtbaker_station')
df_othello = data_prep_blockgrp.get_df(subset='othello_station')
gdf_othello = data_prep_blockgrp.get_gdf(subset='othello_station')
df_rb['GEOID_long'] = df_rb['GEOID']
df_rb['GEOID'] = df_rb['GEOID'].str.replace("53033", "")
gdf_rb['GEOID_long_a'] = gdf_rb['GEOID_a']
gdf_rb['GEOID_long_b'] = gdf_rb['GEOID_b']
gdf_rb['GEOID_a'] = gdf_rb['GEOID_a'].str.replace("53033", "")
gdf_rb['GEOID_b'] = gdf_rb['GEOID_b'].str.replace("53033", "")
df_mtbaker['GEOID_long'] = df_mtbaker['GEOID']
df_mtbaker['GEOID'] = df_mtbaker['GEOID'].str.replace("53033", "")
gdf_mtbaker['GEOID_long_a'] = gdf_mtbaker['GEOID_a']
gdf_mtbaker['GEOID_long_b'] = gdf_mtbaker['GEOID_b']
gdf_mtbaker['GEOID_a'] = gdf_mtbaker['GEOID_a'].str.replace("53033", "")
gdf_mtbaker['GEOID_b'] = gdf_mtbaker['GEOID_b'].str.replace("53033", "")
df_othello['GEOID_long'] = df_othello['GEOID']
df_othello['GEOID'] = df_othello['GEOID'].str.replace("53033", "")
gdf_othello['GEOID_long_a'] = gdf_othello['GEOID_a']
gdf_othello['GEOID_long_b'] = gdf_othello['GEOID_b']
gdf_othello['GEOID_a'] = gdf_othello['GEOID_a'].str.replace("53033", "")
gdf_othello['GEOID_b'] = gdf_othello['GEOID_b'].str.replace("53033", "")
df['GEOID_long'] = df['GEOID']
df['GEOID'] = df['GEOID'].str.replace("53033", "")
gdf['GEOID_long_a'] = gdf['GEOID_a']
gdf['GEOID_long_b'] = gdf['GEOID_b']
gdf['GEOID_a'] = gdf['GEOID_a'].str.replace("53033", "")
gdf['GEOID_b'] = gdf['GEOID_b'].str.replace("53033", "")
df_wallingford['GEOID_long'] = df_wallingford['GEOID']
df_wallingford['GEOID'] = df_wallingford['GEOID'].str.replace("53033", "")
gdf_wallingford['GEOID_long_a'] = gdf_wallingford['GEOID_a']
gdf_wallingford['GEOID_long_b'] = gdf_wallingford['GEOID_b']
gdf_wallingford['GEOID_a'] = gdf_wallingford['GEOID_a'].str.replace("53033", "")
gdf_wallingford['GEOID_b'] = gdf_wallingford['GEOID_b'].str.replace("53033", "")

from data_prep_blockgrp import block_grp_geoids
'''

#set a map center (for maps only, obviously)
the_bounty = {"lat": 47.6615392, "lon": -122.3446507}
pikes_place = {"lat": 47.6145537,"lon": -122.3497373,}

#PLOT
node_list = list(set(df_combo['GEOID']))
#G = nx.Graph()
G2018 = nx.Graph()

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
#    G.add_node(i)
    G2018.add_node(i)

#Build the Edge list for the network graph for 2013
for i, row in gdf_combo.iterrows():
#    G.add_weighted_edges_from([(row['GEOID_a'],row['GEOID_b'],row['omega13'])])
    G2018.add_weighted_edges_from([(row['GEOID_a'],row['GEOID_b'],row['omega18'])])

#CACHE-USING VERSION
@cache.memoize(timeout=TIMEOUT)
def query_forceatlas2():
    forceatlas2 = ForceAtlas2(
                            # Behavior alternatives
                            outboundAttractionDistribution=False,  # Dissuade hubs
                            linLogMode=False,  # NOT IMPLEMENTED
                            adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                            edgeWeightInfluence=2, #was 5, testing if this can change things

                            # Performance
                            jitterTolerance=1.0,  # Tolerance
                            barnesHutOptimize=True,
                            barnesHutTheta=8.7,
                            multiThreaded=False,  # NOT IMPLEMENTED

                            # Tuning
                            scalingRatio=12,
                            strongGravityMode=False,
                            gravity=0.00100000, #was 20, still seeing a straight line.

                            # Log
                            verbose=False)
    return forceatlas2

#def pos():
#    return query_forceatlas2().forceatlas2_networkx_layout(G,pos=None, iterations=1000)

def pos2018():
    return query_forceatlas2().forceatlas2_networkx_layout(G2018,pos=None, iterations=1000)

#for n, p in pos().items():
#    G.nodes[n]['pos'] = p

for n, p in pos2018().items():
    G2018.nodes[n]['pos'] = p

'''
#NON-CACHE-USING VERSION
pos = forceatlas2.forceatlas2_networkx_layout(G,pos=None, iterations=1000)

for n, p in pos.items():
    G.nodes[n]['pos'] = p
'''

#plot this bad boy
#edge_trace = go.Scatter(
#    x=[],
#    y=[],
#    line=dict(width=1,color='#c6c6c6'),
#    hoverinfo='text',
#    mode='lines'
#)

edge_trace2018 = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1,color='#c6c6c6'),
    hoverinfo='text',
    mode='lines'
)

#for edge in G.edges():
#    x0, y0 = G.nodes[edge[0]]['pos']
#    x1, y1 = G.nodes[edge[1]]['pos']
#    edge_trace['x'] += tuple([x0, x1, None])
#    edge_trace['y'] += tuple([y0, y1, None])

for edge in G2018.edges():
    x0, y0 = G2018.nodes[edge[0]]['pos']
    x1, y1 = G2018.nodes[edge[1]]['pos']
    edge_trace2018['x'] += tuple([x0, x1, None])
    edge_trace2018['y'] += tuple([y0, y1, None])

#node_trace = go.Scatter(
#    x=[],
#    y=[],
#    mode='markers+text', #make markers+text to show labels
#    text=[],
#    hoverinfo='text',
#    customdata=df_combo['GEOID'],
#    marker=dict(
#        showscale=False,
#        colorscale='Edge',
#        reversescale=False,
#        color=[],
#        size=20,
#        opacity=0.8,
#        colorbar=dict(
#            thickness=10,
#            title='COLOR GROUP BY CENSUS TRACT NUMBER',
#            xanchor='left',
#            titleside='right'
#        ),
#        line=dict(width=0)
#    ),
#    showlegend=True,
#    marker_line_width=1
#)

node_trace2018 = go.Scatter(
    x=[],
    y=[],
   mode='markers+text', #make markers+text to show labels
    text=[],
    hoverinfo='text',
    customdata=df_combo['GEOID'],
    marker=dict(
        showscale=False,
        colorscale='YlGnBu',
        reversescale=False,
        color=[],
        size=20,
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
    marker_line_width=1
)

#for node in G.nodes():
#    x, y = G.nodes[node]['pos']
#    node_trace['x'] += tuple([x])
#    node_trace['y'] += tuple([y])

for node in G2018.nodes():
    x, y = G2018.nodes[node]['pos']
    node_trace2018['x'] += tuple([x])
    node_trace2018['y'] += tuple([y])

#node_adjacencies = []
node_adjacencies2018 = []

#for node, adjacencies in enumerate(G.adjacency()):
#    node_adjacencies.append(len(adjacencies[1]))

for node, adjacencies in enumerate(G2018.adjacency()):
    node_adjacencies2018.append(len(adjacencies[1]))

#for node in G.nodes():
#    node_label = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"] #tract version

for node in G2018.nodes():
    node_label2018 = df_combo['neighborhood'] + '<br>' + df_combo["TRACT_NUM"] #tract version

df_combo['tract_index'] = df_combo['TRACT_NUM'].astype(int)

#node_trace.marker.color = df_combo['tract_index']
#node_trace.marker.size = node_adjacencies
#node_trace.text = node_label

colorsIndex = {'wallingford':'#ef553b','rainier_beach':'#636efa'} #manually assign colors
colors = df_combo['neighborhood'].map(colorsIndex)
node_trace2018.marker.color = colors
#node_trace2018.marker.color = df_combo['neighborhood_index'].astype(int)
node_trace2018.marker.size = (1.5 + df_combo.omega18) * 20
node_trace2018.text = node_label2018

#fig = go.Figure(data=[edge_trace, node_trace],
#             layout=go.Layout(
#                title='',
#                titlefont=dict(size=16),
#                showlegend=False,
#                hovermode='closest',
#                margin=dict(b=20,l=5,r=5,t=40),
#                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

#fig.update_traces(textfont_size=25)

fig2 = go.Figure(data=[edge_trace2018, node_trace2018],
             layout=go.Layout(
                title='',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

fig2.update_traces(textfont_size=25)

'''
#Kmeans clustering
Y = df_combo[['GEOID','omega18','omega18']]
Y = Y[~Y['omega18'].isnull()]
Y = Y[~Y['omega18'].isnull()]
X = Y[['omega18','omega18']]
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
#re-merge with gdf_combo
df_combo = df_combo.merge(Y, how='left', left_on=['GEOID','omega18','omega18'], right_on=['GEOID','omega18','omega18'])

grp0 = df_combo[(df_combo['labels'] == 0)].drop_duplicates()
grp0 = grp0[['GEOID','omega18','omega18','omega_change','RENT_AS_PCT_HOUSEHOLD_INCOME_2013','RENT_AS_PCT_HOUSEHOLD_INCOME_2018','RENT_25PCTILE_2013','RENT_25PCTILE_2018','TOT_POP_2013','TOT_POP_2018','minority_pop_pct_2013','minority_pop_pct_2018','MEDIAN_MONTHLY_HOUSING_COST_2013','sub_600_units_per_capita_2013','sub_600_units_per_capita_2018','housing_tenure13','housing_tenure18','labels']]
grp0_length = str(grp0.shape)
grp0 = grp0.sort_values('omega_change')

grp1 = df_combo[(df_combo['labels'] == 1)].drop_duplicates()
grp1 = grp1[['GEOID','omega18','omega18','omega_change','RENT_AS_PCT_HOUSEHOLD_INCOME_2013','RENT_AS_PCT_HOUSEHOLD_INCOME_2018','RENT_25PCTILE_2013','RENT_25PCTILE_2018','TOT_POP_2013','TOT_POP_2018','minority_pop_pct_2013','minority_pop_pct_2018','MEDIAN_MONTHLY_HOUSING_COST_2013','sub_600_units_per_capita_2013','sub_600_units_per_capita_2018','housing_tenure13','housing_tenure18','labels']]
grp1 = grp1.sort_values('omega_change')
grp1_length = str(grp1.shape)

grp2 = df_combo[(df_combo['labels'] == 2)].drop_duplicates()
grp2 = grp2[['GEOID','omega18','omega18','omega_change','RENT_AS_PCT_HOUSEHOLD_INCOME_2013','RENT_AS_PCT_HOUSEHOLD_INCOME_2018','RENT_25PCTILE_2013','RENT_25PCTILE_2018','TOT_POP_2013','TOT_POP_2018','minority_pop_pct_2013','minority_pop_pct_2018','MEDIAN_MONTHLY_HOUSING_COST_2013','sub_600_units_per_capita_2013','sub_600_units_per_capita_2018','housing_tenure13','housing_tenure18','labels']]
grp2_length = str(grp2.shape)
grp2 = grp2.sort_values('omega_change')

grp3 = df_combo[(df_combo['labels'] == 3)].drop_duplicates()
grp3 = grp3[['GEOID','omega18','omega18','omega_change','RENT_AS_PCT_HOUSEHOLD_INCOME_2013','RENT_AS_PCT_HOUSEHOLD_INCOME_2018','RENT_25PCTILE_2013','RENT_25PCTILE_2018','TOT_POP_2013','TOT_POP_2018','minority_pop_pct_2013','minority_pop_pct_2018','MEDIAN_MONTHLY_HOUSING_COST_2013','sub_600_units_per_capita_2013','sub_600_units_per_capita_2018','housing_tenure13','housing_tenure18','labels']]
grp3_length = str(grp3.shape)
grp3 = grp3.sort_values('omega_change')
'''

fig3 = px.scatter(df_combo, x="omega13", y="omega18",color='neighborhood',text='GEOID'
)
fig3.update_yaxes(
    range=[-1.5, 1.5]
  )
fig3.update_xaxes(
    range=[-1.5, 1.5]
  )
fig3.update_traces(textposition="middle right")
#can set axis ratios, as well
#fig.update_yaxes(
#    scaleanchor = "x",
#    scaleratio = 1,
#  )
#
fig3.update_traces(marker=dict(size=20))
fig3.add_shape(
        # Line Diagonal so you can see movement btw 2013 and 2018
            type="line",
            x0=-1,
            y0=-1,
            x1=1,
            y1=1,
            line=dict(
                color="MediumPurple",
                width=4,
                dash="dash",
            )
)

fig4 = px.choropleth_mapbox(df_combo,geojson=tracts,locations=df_combo['GEOID_long'],featureidkey='properties.GEOID',color=df_combo['omega_change'],
            opacity=0.7,color_continuous_scale='RdYlGn_r')
fig4.update_layout(mapbox_style="open-street-map",
            mapbox_zoom=10.5,
            mapbox_center=pikes_place)

fig5 = px.choropleth_mapbox(df_combo,geojson=tracts,locations=df_combo['GEOID_long'],featureidkey='properties.GEOID',color=df_combo['omega13'],
            opacity=0.7,color_continuous_scale='RdYlGn_r')
fig5.update_layout(mapbox_style="open-street-map",
            mapbox_zoom=10.5,
            mapbox_center=pikes_place)

fig6 = px.choropleth_mapbox(df_combo,geojson=tracts,locations=df_combo['GEOID_long'],featureidkey='properties.GEOID',color=df_combo['omega18'],
            opacity=0.7,color_continuous_scale='RdYlGn_r')
fig6.update_layout(mapbox_style="open-street-map",
            mapbox_zoom=10.5,
            mapbox_center=pikes_place)

#here we make the graph a function called serve_layout(), which then allows us to have it run every time the page is loaded (unlike the normal which would just be app.layer = GRAPH CONTENT, which would run every time the app was started on the server (aka, once))
def serve_layout():
    return html.Div([
        dcc.Link('Dashboard Home', href='/', id="app_menu"),
        html.Div([
            html.H1('EPCW pilot network model of Displacement Pressure in Seattle'),
            html.P("Our pilot network model compares equitable access to housing and displacement pressure in two Seattle neighborhoods in 2018.  Current evaluation tools, such as the City of Seattle's Displacement Risk Index are statistics computed over geographic regions and presented as map overlays. Geographic regions are related by adjacency. In contrast, the network model defines the strength of relationships between groups of people and revealing communities among these groups. Groups in the network model are related when they share access to resources. The network shows relationships between groups of people, not properties of a geography.", className='description'),
            html.P('In the network model below, tracts that are closer together are more similar than those further apart.  One can best think of this network as a comparison of SIMILARITY.  Nodes closer together have more similar demographic properties than those further apart.', className='description'),
            html.P('Edge weights are determined by racial minority population percentage, by lowest quartile housing cost, housing tenancy, affordable housing stock, and housing cost as a percentage of household income, and median monthly housing cost.', className='description'),
            html.Div([
                dcc.Graph(figure=fig2,
                          id='housing_networkx18',
                          )
            ]),
#            html.Div([
#                html.Div([
#                    html.Div([
#                        html.H2(className='graph_title', children='2013'),
#                        dcc.Graph(figure=fig,
#                                  id='housing_networkx'
#                                  )], className='col-6'),
#                    html.Div([
#                        html.H2(className='graph_title', children='2018'),
#                        dcc.Graph(figure=fig2,
#                                  id='housing_networkx18'
#                                  )], className='col-6')], className='multi-col'),
#            ], className='container'),
            html.Div([
                html.P(['NOTE: these sliders are currently inactive, but when functional will allow a user to tweak the factors used to measure displacement pressure.  Think that the cost of housing is more or less important relative to the availability of low-cost units or the racial breakdown of a neighborhood?  Tweak the weights and see how it affects the model.'
                ]),
                html.Div([
                    html.Div([
                        html.H4('Racial Minority Population Percentage')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='alpha',
                            min=0,
                            max=1,
                            step=0.1,
                            value=1
                        )], className='col-6')], className='multi-col'),
                html.Div([
                    html.Div([
                        html.H4('Rent cost of 25th percentile')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='beta',
                            min=0,
                            max=1,
                            step=0.1,
                            value=1
                        )], className='col-6')], className='multi-col'),
                html.Div([
                    html.Div([
                        html.H4('Total Population')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='charlie',
                            min=0,
                            max=1,
                            step=0.1,
                            value=1
                        )], className='col-6')], className='multi-col'),
                html.Div([
                    html.Div([
                        html.H4('Rent as a percentage of income')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='delta',
                            min=0,
                            max=1,
                            step=0.1,
                            value=1
                        )], className='col-6')], className='multi-col'),
                html.Div([
                    html.Div([
                        html.H4('Monthly housing cost')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='echo',
                            min=0,
                            max=1,
                            step=0.1,
                            value=1
                        )], className='col-6')], className='multi-col'),
                html.Div([
                    html.Div([
                        html.H4('Affordable Housing Units / capita')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='foxtrot',
                            min=0,
                            max=1,
                            step=0.1,
                            value=1
                        )], className='col-6')], className='multi-col'),
                html.Div([
                    html.Div([
                        html.H4('Median Tenure')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='golf',
                            min=0,
                            max=1,
                            step=0.1,
                            value=1
                        )], className='col-6')], className='multi-col'),
            ], className='container'),
#            dcc.Graph(figure=fig2,
#                      id='housing_bar'
#                      ),
            html.H1('Change in displacement pressure'),
            html.P('This scatterplot compares displacement pressure (what we are calling omega) in the census tract groups in the wealthier northern neighborhoods of Seattle (Wallingford) and the poorer Southeastern neighborhoods (Rainier Beach).  Tracts exactly along the dashed 1:1 line had no change in pressure from 2013-18. Tracts above the line had a higher displacement pressure in 2018; those below had a lower pressure in 2018.', className='description'),
            dcc.Graph(figure=fig3,
                      id='displacement_scatter'
                      ),
            html.Div([
                html.H1('2010 vs 2018'),
                html.P('These maps compare the displacement Pressure (omega) in Seattle from 2010-2018. Red areas have HIGH displacement pressure; green have LOW displacement pressure.',
                       className='description graph_title'),
                html.Div([
                    html.Div([
                        html.H2(className='graph_title', children='2013'),
                        dcc.Graph(figure=fig5,
                            id='displacement_2013'
                        )], className='col-6'),
                    html.Div([
                        html.H2(className='graph_title', children='2018'),
                        dcc.Graph(figure=fig6,
                            id='displacement_2018'
                        )], className='col-6')], className='multi-col'),
            ], className='container'),
            html.H1('Change in displacement pressure map'),
            html.P(
                'This map compares displacement pressure (omega) in each census tract.  Red areas had INCREASING displacement pressure between 2013 and 2018. Green had decreasing.',
                className='description'),
            dcc.Graph(figure=fig4,
                id='block_grp_map'
            ),
#             html.H1('Groupings'),
#             html.H4('Census Tracts', className='description'),
#            html.P('Group 0 - size: ' + str(grp0_length), className='description'),
#            generate_table(grp0),
#            html.P('Group 1 - size: ' + str(grp1_length), className='description'),
#            generate_table(grp1),
#            html.P('Group 2 - size: ' + str(grp2_length), className='description'),
#            generate_table(grp2),
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