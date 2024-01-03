from dash import Dash
import dash_bootstrap_components as dbc

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
TEMPLATE_NAME = "LUX"
appplication = Dash(__name__, external_stylesheets=[dbc.themes.LUX, dbc_css])
# bootstrap, Flatly, Journal, Litera, Lumen, Lux, Materia