import dash

app = dash.Dash(__name__)

application = app.server
app.config.suppress_callback_exceptions = True