import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

app = dash.Dash(__name__)
# Beanstalk looks for application by default, if this isn't set you will get a WSGI error.
application = app.server

df= pd.read_csv('data/coronavirus.csv')

def generate_table(dataframe, max_rows=56):
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

app.layout = html.Div(children=[
    html.H1(children='GOOD MORNINGGGGGGGGG, EPCW!'),

    html.Div(children='''
        This is our EPCW test Dash server running on Elastic Beanstalk.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [ go.Scatter (
                x=df[df['State'] == i]['Date'],
                y=df[df['State'] == i]['Deaths'],

                mode='lines',
                opacity=1,
                name=i)
                for i in df.State.unique()
            ],
            'layout': go.Layout (
                title='US COVID-19 deaths over time',
                yaxis={'type': 'log', 'title': 'Deaths (log)'},
                xaxis={'type': 'date'}
            )
        }
    )
])

if __name__ == '__main__':
    # Beanstalk expects it to be running on 8080.
    application.run(debug=True, port=8080)
