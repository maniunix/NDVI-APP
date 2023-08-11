import dash
import dash_core_components as dcc
from dash import html
import plotly.graph_objs as go
import plotly.express as px
import geemap 
# import dash_bootstrap_components as dbc
from datetime import date

## Initialization
Map = geemap.Map()
external_stylesheet = ['/assets/style.css']
app = dash.Dash(__name__, external_stylesheets= external_stylesheet)

## Layout for the App
app.layout = html.Div(
    html.Div(
        [dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date(2015, 1, 1),
            max_date_allowed=date(2023, 7, 31),
            style= {'font-size': '6px','display': 'inline-block', 'border-radius' : '2px', 
                    'border' : '1px solid #ccc', 'color': '#333', 
                    'border-spacing' : '0', 'border-collapse' :'separate'}),
    html.Div([dcc.Upload(id = "upload-file",
                         children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
            ]),
            style={
            'width': '20%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }, multiple= False),
        html.Div(id='output-data-upload')]),

    html.Div(id='output-container-date-picker-range')
]))



### Parse File
@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    dash.dependencies.Input('my-date-picker-range', 'start_date'),
    dash.dependencies.Input('my-date-picker-range', 'end_date'))

def printDate(start_date,end_date):
    return None





if __name__ == '__main__':
    app.run_server(debug=True)
