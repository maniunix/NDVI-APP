import ee


def getNDVI(image):
    '''
    Take the image and returns the Normalized difference of the Near-Infrared band and Red Band
    Input -> ee.Image
    Output -> ee.Image
    '''
    ndvi = image.normalizedDifference(['B8','B4']).rename('NDVI')
    return image.addBands(ndvi)

def monthlyNDVI(n,collection ,startDate, aoi):
    date = ee.Date(startDate).advance(n,'month')
    m = date.get("month")
    y = date.get("year")
    dic = ee.Dictionary({
        'Date':date.format('yyyy-MM')
        })
    tempNDVI = (collection.filter(ee.Filter.calendarRange(y, y, 'year'))
                .filter(ee.Filter.calendarRange(m, m, 'month'))
                .mean()
                .reduceRegion(
                    reducer = ee.Reducer.mean(),
                    geometry = aoi,
                    scale = 10))
    return dic.combine(tempNDVI)

