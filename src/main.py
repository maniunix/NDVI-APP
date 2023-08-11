import dash
import dash_core_components as dcc
from dash import html
import pandas as pd
import glob
import plotly.graph_objs as go
import plotly.express as px
import geemap 
import ee 
from datetime import date

## Initialization
Map = geemap.Map()
app = dash.Dash(__name__)

## Layout for the App
app.layout = html.Div(
    html.Div([dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2015, 1, 1),
        max_date_allowed=date(2023, 7, 31),
    ),
    html.Div(id='output-container-date-picker-range')
]))

@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    dash.dependencies.Input('my-date-picker-range', 'start_date'),
    dash.dependencies.Input('my-date-picker-range', 'end_date'))
def printDate(start_date,end_date):
    return None



if __name__ == '__main__':
    app.run_server(debug=True)
