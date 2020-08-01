import dash
import dash_core_components as dcc
import dash_html_components as html
import json
import plotly.graph_objects as go
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
# Beanstalk looks for application by default, if this isn't set you will get a WSGI error.
application = app.server

#this pulls in the header HTML from header.py
from template import Template
grid = Template()
app.index_string = grid
app.title = "Dashboards | EPCW"

import data_prep_maps_tract
df = data_prep_maps_tract.get_df()

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
        html.H1(id='housing_title',children='Changing Demographics in Seattle, 2010-2018'),
        html.H3('Dashboard by Center for Equitable Policy in a Changing World', id='subheading'),
        html.Div(id='data-dropdown', children=[
            html.H4('Data Selection'),
            dcc.Dropdown(
                id='data_selection',
                options=[{'label': i, 'value': i} for i in [
                    'White Population',
                    'Non-white Population',
                    'Black Population',
                    'Native Population',
                    'Asian Population',
                    'Polynesian Population',
                    'Latino Population',
                    'Other Race Population',
                    'Multiracial Population',
                    '20th percentile household income',
                    '80th percentile household income',
                    'Median monthly housing costs',
                    '% of household income used for rent',
                    'Affordable housing: 25th percentile rent'
                ]],
                value='Non-white Population'
            )]),
        html.P(
            'This map represents the change in the demographic percentages in Seattle from 2010-2018. Numbers represent percentages (i.e. 10 = +10%, -10 = -10%)',
            className='description'),
        dcc.Graph(
                      id='housing_map_change'
                      )
        ], className='container'),
        html.Div([
            html.H1('2010 vs 2018'),
            html.P('These maps compare the change in the selected demographic group in Seattle from 2010-2018.',
                   className='description graph_title'),
            html.Div([
                html.Div([
                    html.H2(className='graph_title', children='2010'),
                    dcc.Graph(
                              id='housing_2010'
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
            locations=df['GEOID'],
            featureidkey='properties.GEOID',
            zmin=-100 if data_selection == '20th percentile household income'
                else(-50 if data_selection == 'Median monthly housing costs'
                else(-100 if data_selection == '80th percentile household income'
                else -10)),
            zmax=100 if data_selection == '20th percentile household income'
                else(50 if data_selection == 'Median monthly housing costs'
                else(100 if data_selection == '80th percentile household income'
                else(50 if data_selection == 'Affordable housing: 25th percentile rent'
                else 10))),
            colorscale='RdYlGn_r' if data_selection == 'Affordable housing: 25th percentile rent'
            else('RdYlGn_r' if data_selection == 'Median monthly housing costs'
            else('RdYlGn_r' if data_selection == '% of household income used for rent'
            else 'RdYlGn')),
            marker_opacity=0.5,
            marker_line_width=0,
            z=df['white_pop_delta' if data_selection == 'White Population'
                else('black_pop_delta' if data_selection == 'Black Population'
                else('native_pop_delta' if data_selection == 'Native Population'
                else('asian_pop_delta' if data_selection == 'Asian Population'
                else('polynesian_pop_delta' if data_selection == 'Polynesian Population'
                else('latino_pop_delta' if data_selection == 'Latino Population'
                else('other_pop_delta' if data_selection == 'Other Race Population'
                else('multiracial_pop_delta' if data_selection == 'Multiracial Population'
                else('twenty_pctile_delta' if data_selection == '20th percentile household income'
                else('eighty_pctile_delta' if data_selection == '80th percentile household income'
                else('housing_costs_delta' if data_selection == 'Median monthly housing costs'
                else('rent_pct_income_delta' if data_selection == '% of household income used for rent'
                else('rent_25pctile_delta' if data_selection == 'Affordable housing: 25th percentile rent'
                else 'minority_pop_delta'))))))))))))])
        ],
        'layout': go.Layout(
            mapbox_style="carto-positron",
            mapbox_zoom=10,
            mapbox_center=the_bounty,
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )
    }

# callback for housing_2010
@app.callback(
    Output('housing_2010', 'figure'),
    [Input('data_selection', 'value')])

# updates graph based on user input
def update_graph10(data_selection):
    return {
        'data': [ go.Choroplethmapbox(
            geojson=tracts,
            locations=df['GEOID'],
            featureidkey='properties.GEOID',
            zmin=0,
            zmax=30000 if data_selection == '20th percentile household income'
                else(150000 if data_selection == '80th percentile household income'
                else(2500 if data_selection == 'Median monthly housing costs'
                else(1600 if data_selection == 'Affordable housing: 25th percentile rent'
                else(50 if data_selection == '% of household income used for rent'
                else 100)))),
            colorscale='RdYlGn_r' if data_selection == 'Affordable housing: 25th percentile rent'
            else('RdYlGn_r' if data_selection == 'Median monthly housing costs'
            else('RdYlGn_r' if data_selection == '% of household income used for rent'
            else 'tempo')),
            marker_opacity=0.5,
            marker_line_width=0,
            z=df['white_pct10' if data_selection == 'White Population'
                else('black_pct10' if data_selection == 'Black Population'
                else('native_pct10' if data_selection == 'Native Population'
                else('asian_pct10' if data_selection == 'Asian Population'
                else('polynesian_pct10' if data_selection == 'Polynesian Population'
                else('latino_pct10' if data_selection == 'Latino Population'
                else('other_pct10' if data_selection == 'Other Race Population'
                else('multiracial_pct10' if data_selection == 'Multiracial Population'
                else('TWENTY_PCTILE_2010' if data_selection == '20th percentile household income'
                else('EIGHTY_PCTILE_2010' if data_selection == '80th percentile household income'
                else('MEDIAN_MONTHLY_HOUSING_COST_2010' if data_selection == 'Median monthly housing costs'
                else('RENT_AS_PCT_HOUSEHOLD_INCOME_2010' if data_selection == '% of household income used for rent'
                else('RENT_25PCTILE_2010' if data_selection == 'Affordable housing: 25th percentile rent'
                else 'minority_pop_pct10'))))))))))))])
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
            locations=df['GEOID'],
            featureidkey='properties.GEOID',
            zmin=0 if data_selection == 'White Population'
                else 0,
            zmax=30000 if data_selection == '20th percentile household income'
                else(150000 if data_selection == '80th percentile household income'
                else(2500 if data_selection == 'Median monthly housing costs'
                else(1600 if data_selection == 'Affordable housing: 25th percentile rent'
                else(50 if data_selection == '% of household income used for rent'
                else 100)))),
            colorscale='RdYlGn_r' if data_selection == 'Affordable housing: 25th percentile rent'
            else('RdYlGn_r' if data_selection == 'Median monthly housing costs'
            else('RdYlGn_r' if data_selection == '% of household income used for rent'
            else 'tempo')),
            marker_opacity=0.5,
            marker_line_width=0,
            z=df['white_pct18' if data_selection == 'White Population'
                else('black_pct18' if data_selection == 'Black Population'
                else('native_pct18' if data_selection == 'Native Population'
                else('asian_pct18' if data_selection == 'Asian Population'
                else('polynesian_pct18' if data_selection == 'Polynesian Population'
                else('latino_pct18' if data_selection == 'Latino Population'
                else('other_pct18' if data_selection == 'Other Race Population'
                else('multiracial_pct18' if data_selection == 'Multiracial Population'
                else('TWENTY_PCTILE_2018' if data_selection == '20th percentile household income'
                else('EIGHTY_PCTILE_2018' if data_selection == '80th percentile household income'
                else('MEDIAN_MONTHLY_HOUSING_COST_2018' if data_selection == 'Median monthly housing costs'
                else('RENT_AS_PCT_HOUSEHOLD_INCOME_2018' if data_selection == '% of household income used for rent'
                else('RENT_25PCTILE_2018' if data_selection == 'Affordable housing: 25th percentile rent'
                else 'minority_pop_pct18'))))))))))))])
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
    # Beanstalk expects it to be running on 8080.
    application.run(debug=True, port=8080)
