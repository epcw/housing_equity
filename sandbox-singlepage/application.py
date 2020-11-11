import dash  #comment out for production deployment
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go  #version for networkx
from flask_caching import Cache
import plotly.express as px  #version for maps
#from sklearn.cluster import KMeans  #commented out because hiding Kmeans clusters for now.
from dash.dependencies import Input, Output

#from dashbase import app, application  #production version
app = dash.Dash(__name__)  #local
application = app.server  #local

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

#set a map center (for maps only, obviously)
the_bounty = {"lat": 47.6615392, "lon": -122.3446507}
pikes_place = {"lat": 47.6145537,"lon": -122.3497373,}

from build_network import tracts

@cache.memoize(timeout=TIMEOUT)
def get_nodes_a1b1c1d1e1f1g1():
    from build_network import get_nodes
    node_trace2018_a1b1c1d1e1f1g1 = get_nodes(subset='a1b1c1d1e1f1g1')
    return node_trace2018_a1b1c1d1e1f1g1

node_trace2018_a1b1c1d1e1f1g1 = get_nodes_a1b1c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_nodes_a1b5c1d1e1f1g1():
    from build_network import get_nodes
    node_trace2018_a1b5c1d1e1f1g1 = get_nodes(subset='a1b5c1d1e1f1g1')
    return node_trace2018_a1b5c1d1e1f1g1

node_trace2018_a1b5c1d1e1f1g1 = get_nodes_a1b5c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_nodes_a1b0c1d1e1f1g1():
    from build_network import get_nodes
    node_trace2018_a1b0c1d1e1f1g1 = get_nodes(subset='a1b0c1d1e1f1g1')
    return node_trace2018_a1b0c1d1e1f1g1

node_trace2018_a1b0c1d1e1f1g1 = get_nodes_a1b0c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_nodes_a5b1c1d1e1f1g1():
    from build_network import get_nodes
    node_trace2018_a5b1c1d1e1f1g1 = get_nodes(subset='a5b1c1d1e1f1g1')
    return node_trace2018_a5b1c1d1e1f1g1

node_trace2018_a5b1c1d1e1f1g1 = get_nodes_a5b1c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_nodes_a5b5c1d1e1f1g1():
    from build_network import get_nodes
    node_trace2018_a5b5c1d1e1f1g1 = get_nodes(subset='a5b5c1d1e1f1g1')
    return node_trace2018_a5b5c1d1e1f1g1

node_trace2018_a5b5c1d1e1f1g1 = get_nodes_a5b5c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_nodes_a5b0c1d1e1f1g1():
    from build_network import get_nodes
    node_trace2018_a5b0c1d1e1f1g1 = get_nodes(subset='a5b0c1d1e1f1g1')
    return node_trace2018_a5b0c1d1e1f1g1

node_trace2018_a5b0c1d1e1f1g1 = get_nodes_a5b0c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_nodes_a0b1c1d1e1f1g1():
    from build_network import get_nodes
    node_trace2018_a0b1c1d1e1f1g1 = get_nodes(subset='a0b1c1d1e1f1g1')
    return node_trace2018_a0b1c1d1e1f1g1

node_trace2018_a0b1c1d1e1f1g1 = get_nodes_a0b1c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_nodes_a0b5c1d1e1f1g1():
    from build_network import get_nodes
    node_trace2018_a0b5c1d1e1f1g1 = get_nodes(subset='a0b5c1d1e1f1g1')
    return node_trace2018_a0b5c1d1e1f1g1

node_trace2018_a0b5c1d1e1f1g1 = get_nodes_a0b5c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_nodes_a0b0c1d1e1f1g1():
    from build_network import get_nodes
    node_trace2018_a0b0c1d1e1f1g1 = get_nodes(subset='a0b0c1d1e1f1g1')
    return node_trace2018_a0b0c1d1e1f1g1

node_trace2018_a0b0c1d1e1f1g1 = get_nodes_a0b0c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_maps():
    from build_network import get_maps
    df_combo = get_maps(subset='one')
    return df_combo

df_combo = get_maps()

@cache.memoize(timeout=TIMEOUT)
def get_edges_a1b1c1d1e1f1g1():
    from build_network import get_edges
    edge_trace2018_a1b1c1d1e1f1g1 = get_edges(subset='a1b1c1d1e1f1g1')
    return edge_trace2018_a1b1c1d1e1f1g1

edge_trace2018_a1b1c1d1e1f1g1 = get_edges_a1b1c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_edges_a1b5c1d1e1f1g1():
    from build_network import get_edges
    edge_trace2018_a1b5c1d1e1f1g1 = get_edges(subset='a1b5c1d1e1f1g1')
    return edge_trace2018_a1b5c1d1e1f1g1

edge_trace2018_a1b5c1d1e1f1g1 = get_edges_a1b5c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_edges_a1b0c1d1e1f1g1():
    from build_network import get_edges
    edge_trace2018_a1b0c1d1e1f1g1 = get_edges(subset='a1b0c1d1e1f1g1')
    return edge_trace2018_a1b0c1d1e1f1g1

edge_trace2018_a1b0c1d1e1f1g1 = get_edges_a1b0c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_edges_a5b1c1d1e1f1g1():
    from build_network import get_edges
    edge_trace2018_a5b1c1d1e1f1g1 = get_edges(subset='a5b1c1d1e1f1g1')
    return edge_trace2018_a5b1c1d1e1f1g1

edge_trace2018_a5b1c1d1e1f1g1 = get_edges_a5b1c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_edges_a5b5c1d1e1f1g1():
    from build_network import get_edges
    edge_trace2018_a5b5c1d1e1f1g1 = get_edges(subset='a5b5c1d1e1f1g1')
    return edge_trace2018_a5b5c1d1e1f1g1

edge_trace2018_a5b5c1d1e1f1g1 = get_edges_a5b5c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_edges_a5b0c1d1e1f1g1():
    from build_network import get_edges
    edge_trace2018_a5b0c1d1e1f1g1 = get_edges(subset='a5b0c1d1e1f1g1')
    return edge_trace2018_a5b0c1d1e1f1g1

edge_trace2018_a5b0c1d1e1f1g1 = get_edges_a5b0c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_edges_a0b1c1d1e1f1g1():
    from build_network import get_edges
    edge_trace2018_a0b1c1d1e1f1g1 = get_edges(subset='a0b1c1d1e1f1g1')
    return edge_trace2018_a0b1c1d1e1f1g1

edge_trace2018_a0b1c1d1e1f1g1 = get_edges_a0b1c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_edges_a0b5c1d1e1f1g1():
    from build_network import get_edges
    edge_trace2018_a0b5c1d1e1f1g1 = get_edges(subset='a0b5c1d1e1f1g1')
    return edge_trace2018_a0b5c1d1e1f1g1

edge_trace2018_a0b5c1d1e1f1g1 = get_edges_a0b5c1d1e1f1g1()

@cache.memoize(timeout=TIMEOUT)
def get_edges_a0b0c1d1e1f1g1():
    from build_network import get_edges
    edge_trace2018_a0b0c1d1e1f1g1 = get_edges(subset='a0b0c1d1e1f1g1')
    return edge_trace2018_a0b0c1d1e1f1g1

edge_trace2018_a0b0c1d1e1f1g1 = get_edges_a0b0c1d1e1f1g1()

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


#here we make the graph a function called serve_layout(), which then allows us to have it run every time the page is loaded (unlike the normal which would just be app.layer = GRAPH CONTENT, which would run every time the app was started on the server (aka, once))
def serve_layout():
    return html.Div([
        dcc.Link('Dashboard Home', href='/', id="app_menu"),
        html.Div([
            html.Div([
                html.H1('Displacement pressure in Seattle, 2010 vs 2018'),
                html.P('These maps compare the displacement Pressure (omega) in Seattle from 2010-2018. Red areas have HIGH displacement pressure; green have LOW displacement pressure.',
                       className='description graph_title'),
                html.Div([
                    html.Div([
                        html.H2(className='graph_title', children='2013'),
                        dcc.Graph(
                            id='displacement_2013'
                        )], className='col-6'),
                    html.Div([
                        html.H2(className='graph_title', children='2018'),
                        dcc.Graph(
                            id='displacement_2018'
                        )], className='col-6')], className='multi-col'),
            ], className='container'),
            html.H1('Network Model of displacement Pressure'),
            html.P("Our pilot network model compares equitable access to housing and displacement pressure in two Seattle neighborhoods in 2018.  Current evaluation tools, such as the City of Seattle's Displacement Risk Index are statistics computed over geographic regions and presented as map overlays. Geographic regions are related by adjacency. In contrast, the network model defines the strength of relationships between groups of people and revealing communities among these groups. Groups in the network model are related when they share access to resources. The network shows relationships between groups of people, not properties of a geography.", className='description'),
            html.P('In the network model below, tracts that are closer together are more similar than those further apart.  One can best think of this network as a comparison of SIMILARITY.  Nodes closer together have more similar demographic properties than those further apart.', className='description'),
            html.P('Edge weights are determined by racial minority population percentage, by lowest quartile housing cost, housing tenancy, affordable housing stock, and housing cost as a percentage of household income, and median monthly housing cost.', className='description'),
            html.Div([
                dcc.Graph(
                          id='housing_networkx18',
                          )
            ]),
            html.Div([
                html.P(['NOTE: ONLY THE RACIAL MINORITY and the 25TH %ILE RENT sliders currently function, but, when integrated, the rest will allow a user to tweak the factors used to measure displacement pressure.  Think that the cost of housing is more or less important relative to the availability of low-cost units or the racial breakdown of a neighborhood?  Tweak the weights and see how it affects the model.'
                ]),
                html.Div([
                    html.Div([
                        html.H4('Racial Minority Population Percentage')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='alpha_slider',
                            min=0,
                            max=1,
                            step=0.5,
                            value=1
                        )], className='col-6')], className='multi-col'),
                html.Div([
                    html.Div([
                        html.H4('Rent cost of 25th percentile')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='beta_slider',
                            min=0,
                            max=1,
                            step=0.5,
                            value=1
                        )], className='col-6')], className='multi-col'),
                html.Div([
                    html.Div([
                        html.H4('Total Population')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='charlie_slider',
                            min=0,
                            max=1,
                            step=0.5,
                            value=1
                        )], className='col-6')], className='multi-col'),
                html.Div([
                    html.Div([
                        html.H4('Rent as a percentage of income')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='delta_slider',
                            min=0,
                            max=1,
                            step=0.5,
                            value=1
                        )], className='col-6')], className='multi-col'),
                html.Div([
                    html.Div([
                        html.H4('Monthly housing cost')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='echo_slider',
                            min=0,
                            max=1,
                            step=0.5,
                            value=1
                        )], className='col-6')], className='multi-col'),
                html.Div([
                    html.Div([
                        html.H4('Affordable Housing Units / capita')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='foxtrot_slider',
                            min=0,
                            max=1,
                            step=0.5,
                            value=1
                        )], className='col-6')], className='multi-col'),
                html.Div([
                    html.Div([
                        html.H4('Median Tenure')], className='col-4'),
                    html.Div([
                        dcc.Slider(
                            id='golf_slider',
                            min=0,
                            max=1,
                            step=0.5,
                            value=1
                        )], className='col-6')], className='multi-col'),
            ], className='container'),
            html.H1('Change in displacement pressure map'),
            html.P(
                'This map compares displacement pressure (omega) in each census tract.  Red areas had INCREASING displacement pressure between 2013 and 2018. Green had decreasing.',
                className='description'),
            dcc.Graph(
                id='block_grp_map'
            ),
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
#            dcc.Graph(figure=fig2,
#                      id='housing_bar'
#                      ),
            html.H1('Change in displacement pressure'),
            html.P('This scatterplot compares displacement pressure (what we are calling omega) in the census tract groups in the wealthier northern neighborhoods of Seattle (Wallingford) and the poorer Southeastern neighborhoods (Rainier Beach).  Tracts exactly along the dashed 1:1 line had no change in pressure from 2013-18. Tracts above the line had a higher displacement pressure in 2018; those below had a lower pressure in 2018.', className='description'),
            dcc.Graph(
                      id='displacement_scatter'
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


# callback for network
@app.callback(
    Output('housing_networkx18', 'figure'),
    [Input('alpha_slider', 'value'),
     Input('beta_slider', 'value')])

# updates graph based on user input
def update_graph(alpha_slider, beta_slider):
    return {
        'data': [
            edge_trace2018_a0b0c1d1e1f1g1 if alpha_slider == 0 and beta_slider == 0
            else (edge_trace2018_a5b0c1d1e1f1g1 if alpha_slider == 0 and beta_slider == 0.5
            else (edge_trace2018_a5b0c1d1e1f1g1 if alpha_slider == 0.5 and beta_slider == 0
            else (edge_trace2018_a5b5c1d1e1f1g1 if alpha_slider == 0.5 and beta_slider == 0.5
            else (edge_trace2018_a1b0c1d1e1f1g1 if alpha_slider == 1 and beta_slider == 0
            else (edge_trace2018_a1b5c1d1e1f1g1 if alpha_slider == 1 and beta_slider == 0.5
            else (edge_trace2018_a1b1c1d1e1f1g1 if alpha_slider == 1 and beta_slider == 1
            else (edge_trace2018_a5b1c1d1e1f1g1 if alpha_slider == 0.5 and beta_slider == 1
            else edge_trace2018_a0b1c1d1e1f1g1))))))),
            node_trace2018_a0b0c1d1e1f1g1 if alpha_slider == 0 and beta_slider == 0
            else (node_trace2018_a5b0c1d1e1f1g1 if alpha_slider == 0 and beta_slider == 0.5
            else (node_trace2018_a5b0c1d1e1f1g1 if alpha_slider == 0.5 and beta_slider == 0
            else (node_trace2018_a5b5c1d1e1f1g1 if alpha_slider == 0.5 and beta_slider == 0.5
            else (node_trace2018_a1b0c1d1e1f1g1 if alpha_slider == 1 and beta_slider == 0
            else (node_trace2018_a1b5c1d1e1f1g1 if alpha_slider == 1 and beta_slider == 0.5
            else (node_trace2018_a1b1c1d1e1f1g1 if alpha_slider == 1 and beta_slider == 1
            else (node_trace2018_a5b1c1d1e1f1g1 if alpha_slider == 0.5 and beta_slider == 1
            else node_trace2018_a0b1c1d1e1f1g1)))))))],
        'layout': go.Layout(
                title='',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    }

@app.callback(
    Output('block_grp_map', 'figure'),
    [Input('alpha_slider', 'value'),
     Input('beta_slider', 'value')])

# updates graph based on user input
def update_change_map(alpha_slider, beta_slider):
    fig4 = px.choropleth_mapbox(df_combo,
                                geojson=tracts,
                                locations=df_combo['GEOID_long'],
                                featureidkey='properties.GEOID',
                                color=df_combo['omegadf_a0b0c1d1e1f1g1' if alpha_slider == 0 and beta_slider == 0
                                else ('omegadf_a0b5c1d1e1f1g1' if alpha_slider == 0 and beta_slider == 0.5
                                else ('omegadf_a5b0c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 0
                                else ('omegadf_a5b5c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 0.5
                                else ('omegadf_a1b0c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 0
                                else ('omegadf_a1b5c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 0.5
                                else ('omegadf_a1b1c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 1
                                else ('omegadf_a5b1c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 1
                                else 'omegadf_a0b1c1d1e1f1g1')))))))],
                                opacity=0.7,
                                color_continuous_scale='RdYlGn_r')
    fig4.update_layout(mapbox_style="open-street-map",
            mapbox_zoom=10.5,
            mapbox_center=pikes_place)
    return fig4

@app.callback(
    Output('displacement_scatter', 'figure'),
    [Input('alpha_slider', 'value'),
     Input('beta_slider','value')])

#updates scatterplot
def update_scatter_plot(alpha_slider, beta_slider):
    fig3 = px.scatter(df_combo,
                      x='omega13df_a0b0c1d1e1f1g1' if alpha_slider == 0 and beta_slider == 0
                      else ('omega13df_a0b5c1d1e1f1g1' if alpha_slider == 0 and beta_slider == 0.5
                      else ('omega13df_a5b0c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 0
                      else ('omega13df_a5b5c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 0.5
                      else ('omega13df_a1b0c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 0
                      else ('omega13df_a1b5c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 0.5
                      else ('omega13df_a1b1c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 1
                      else ('omega13df_a5b1c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 1
                      else 'omega13df_a0b1c1d1e1f1g1'))))))),
                      y='omega18df_a0b0c1d1e1f1g1' if alpha_slider == 0 and beta_slider == 0
                      else ('omega18df_a0b5c1d1e1f1g1' if alpha_slider == 0 and beta_slider == 0.5
                      else ('omega18df_a5b0c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 0
                      else ('omega18df_a5b5c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 0.5
                      else ('omega18df_a1b0c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 0
                      else ('omega18df_a1b5c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 0.5
                      else ('omega18df_a1b1c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 1
                      else ('omega18df_a5b1c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 1
                      else 'omega18df_a0b1c1d1e1f1g1'))))))),
                      color='neighborhood',
                      text='GEOID'
                      )
    fig3.update_yaxes(
        range=[-1.5, 1.5]
    )
    fig3.update_xaxes(
        range=[-1.5, 1.5]
    )
    fig3.update_traces(textposition="middle right")

    # can set axis ratios, as well
    # fig.update_yaxes(
    #    scaleanchor = "x",
    #    scaleratio = 1,
    #  )
    #

    fig3.update_traces(marker=dict(size=20))
    # Add Diagonal Line so you can see movement btw 2013 and 2018
    fig3.add_shape(
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
    return fig3

@app.callback([
    Output('displacement_2013', 'figure'),
    Output('displacement_2018', 'figure')],
    [Input('alpha_slider', 'value'),
     Input('beta_slider','value')])

# updates graph based on user input
def update_displacement_maps(alpha_slider, beta_slider):
    fig5 = px.choropleth_mapbox(df_combo,
                                geojson=tracts,
                                locations=df_combo['GEOID_long'],
                                featureidkey='properties.GEOID',
                                color=df_combo['omega13df_a0b0c1d1e1f1g1' if alpha_slider == 0 and beta_slider == 0
                                else ('omega13df_a0b5c1d1e1f1g1' if alpha_slider == 0 and beta_slider == 0.5
                                else ('omega13df_a5b0c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 0
                                else ('omega13df_a5b5c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 0.5
                                else ('omega13df_a1b0c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 0
                                else ('omega13df_a1b5c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 0.5
                                else ('omega13df_a1b1c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 1
                                else ('omega13df_a5b1c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 1
                                else 'omega13df_a0b1c1d1e1f1g1')))))))],
                                opacity=0.7,
                                color_continuous_scale='RdYlGn_r')
    fig5.update_layout(mapbox_style="open-street-map",
                       mapbox_zoom=10.5,
                       mapbox_center=pikes_place)
    fig6 = px.choropleth_mapbox(df_combo,
                                geojson=tracts,
                                locations=df_combo['GEOID_long'],
                                featureidkey='properties.GEOID',
                                color=df_combo['omega18df_a0b0c1d1e1f1g1' if alpha_slider == 0 and beta_slider == 0
                                else ('omega18df_a0b5c1d1e1f1g1' if alpha_slider == 0 and beta_slider == 0.5
                                else ('omega18df_a5b0c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 0
                                else ('omega18df_a5b5c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 0.5
                                else ('omega18df_a1b0c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 0
                                else ('omega18df_a1b5c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 0.5
                                else ('omega18df_a1b1c1d1e1f1g1' if alpha_slider == 1 and beta_slider == 1
                                else ('omega18df_a5b1c1d1e1f1g1' if alpha_slider == 0.5 and beta_slider == 1
                                else 'omega18df_a0b1c1d1e1f1g1')))))))],
                                opacity=0.7,
                                color_continuous_scale='RdYlGn_r')
    fig6.update_layout(mapbox_style="open-street-map",
                       mapbox_zoom=10.5,
                       mapbox_center=pikes_place)
    return fig5, fig6

#this calls the serve_layout function to run on app load.
app.layout = serve_layout

if __name__ == '__main__':
#    application.run(host='0.0.0.0',port=80)    # production version
    application.run(debug=True, port=8080)  #local version