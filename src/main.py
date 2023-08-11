import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import glob
import plotly.graph_objs as go
import plotly.express as px
import geemap 
import ee 

## Initialization
Map = geemap.Map()
app = dash.Dash(__name__)

## Layout for the App