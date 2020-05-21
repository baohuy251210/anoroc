import dash
import dash_bootstrap_components as dbc

external_css = [
    './assets/stylesheet.css', dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_css)
server = app.server
app.config.suppress_callback_exceptions = True
app.title = 'Anoroc Monitor'
