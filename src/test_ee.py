import ee
import geopandas as gpd
from ee_computation import getNDVI
import pandas as pd

def maskS2clouds(image):
    qa = image.select('QA60')
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11
    mask = qa.bitwiseAnd(cloudBitMask).eq(0) \
        .And(qa.bitwiseAnd(cirrusBitMask).eq(0))
    return image.updateMask(mask)


def read_shapefile(file_path: str, start_date, end_date):
    '''
    Takes the File path to shapefile as an input.
    Returns clipped NDVI of ROI.
    Input -> Shapefile
    Output -> ee.Image
    '''
    # start_date = "2018-01-01"
    # end_date = "2018-12-31"
    if "shp" in file_path:
        # global start_date, end_date
        gdf = gpd.read_file(file_path)
        geom = list(gdf.geometry[0].exterior.coords)
        aoi = ee.Geometry.Polygon(geom)
        image = ee.ImageCollection('COPERNICUS/S2').filterBounds(aoi).filterDate(start_date, end_date)
        ndvi_collection = image.map(maskS2clouds).map(getNDVI).filterDate(start_date, end_date)
        return ndvi_collection

def monthlyNDVI(n):
    global ndvi_collection, aoi, start_date
    date = ee.Date(start_date).advance(n,'month')
    m = date.get("month")
    y = date.get("year")
    dic = ee.Dictionary({
        'Date':date.format('yyyy-MM')
    })
    
    tempNDVI = (ndvi_collection.select('NDVI').filter(ee.Filter.calendarRange(y, y, 'year'))
                .filter(ee.Filter.calendarRange(m, m, 'month'))
                .mean()
                .reduceRegion(
                    reducer = ee.Reducer.mean(),
                    geometry = aoi,
                    scale = 10))
    return dic.combine(tempNDVI)

def getDataframe(file_path, start_date, end_date):
    gdf = gpd.read_file(file_path)
    geom = list(gdf.geometry[0].exterior.coords)
    aoi = ee.Geometry.Polygon(geom)
    start_date = "2018-01-01"
    end_date = "2022-12-31"
    ndvi_collection = read_shapefile(file_path, start_date, end_date).map(maskS2clouds)
    yrMo = ee.List.sequence(0, 12*3-1).map(monthlyNDVI)
    df = pd.DataFrame(yrMo.getInfo())
    return df


if __name__ == "__main__":
    file_path = "E:/upwork/1225/1225.shp"
    ee.Initialize()
    gdf = gpd.read_file(file_path)
    geom = list(gdf.geometry[0].exterior.coords)
    aoi = ee.Geometry.Polygon(geom)
    start_date = "2018-01-01"
    end_date = "2022-12-31"
    ndvi_collection = read_shapefile(file_path, start_date, end_date).map(maskS2clouds)
    yrMo = ee.List.sequence(0, 12*3-1).map(monthlyNDVI)
    df = pd.DataFrame(yrMo.getInfo())