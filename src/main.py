import dash
import dash_core_components as dcc
import ee
import datetime
import io
import base64
import pandas as pd
import geemap
import geopandas as gpd
from datetime import date
from dash import html, dash_table, State
from ee_computation import getDataframe

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
    html.Div([dcc.Upload(id = "upload-data",
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

    html.Div(id='output-container-date-picker-range'),
    html.Div(id = "ndvi-container")
]))



### Parse File
@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    dash.dependencies.Input('my-date-picker-range', 'start_date'),
    dash.dependencies.Input('my-date-picker-range', 'end_date'))

def printDate(start_date,end_date):
    startdate = start_date
    enddate = end_date
    return startdate, enddate


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'shp' in filename:
            df = gpd.read_file(io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(dash.dependencies.Output('output-data-upload', 'children'),
              dash.dependencies.Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    # if list_of_contents is not None:
    #     children = [
    #         parse_contents(c, n, d) for c, n, d in
    #         zip(list_of_contents, list_of_names, list_of_dates)]
    # df = pd.read_csv(list_of_names)
    return list_of_contents

if __name__ == '__main__':
    app.run_server(debug=True)
