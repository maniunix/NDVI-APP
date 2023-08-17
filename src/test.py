import ee
import geemap
import geopandas as gpd
from datetime import date
from dash import html
from ee_computation import getNDVI
from dash import Dash, dcc, html, Input, Output, callback

app = Dash(__name__)


startdate = date(2015, 1, 1)
enddate = date(2023, 7, 31)

app.layout = html.Div([
    html.H4("Select the Date"),
    html.Div([dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2015, 1, 1),
        max_date_allowed=date(2023, 7, 31),
        style={'font-size': '6px', 'display': 'inline-block', 'border-radius': '2px',
               'border': '1px solid #ccc', 'color': '#333',
               'border-spacing': '0', 'border-collapse': 'separate'})
              ]),
    html.Br(),
    html.Div(id='my-output'),
    html.Div([dcc.Upload(id="upload-file",
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
                         }, multiple=False),
              html.Div(id='output-data-upload')]),
    html.Div(id="ndvi-graph")
])


@callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-date-picker-range',
          component_property='start_date'),
    Input(component_id='my-date-picker-range', component_property='end_date')
)
def update_output_div(start_date, end_date):
    global startdate, enddate
    startdate = start_date
    enddate = end_date
    return f'Output: {start_date , end_date}'


@callback(
    Output(component_id= "ndvi-graph", component_property= "children"),
    Input(component_id= "", component_property= "file")
)

def read_shapefile(file_path: str):
    '''
    Takes the File path to shapefile as an input.
    Returns clipped NDVI of ROI.
    Input -> Shapefile
    Output -> ee.Image
    '''
    if "shp" in file_path:
        global start_date, end_date
        gdf = gpd.read_file(file_path)
        geom = list(gdf.geometry[0].exterior.coords)
        aoi = ee.Geometry.Polygon(geom)
        image = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(aoi).filterDate(start_date, end_date).first()
        return getNDVI(image)
    else:
        pass

if __name__ == '__main__':
    app.run(debug=True)
