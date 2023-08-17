
def getNDVI(image):
    '''
    Take the image and returns the Normalized difference of the Near-Infrared band and Red Band
    Input -> ee.Image
    Output -> ee.Image
    '''
    nir = image.select('B8')
    red = image.select('B4')
    ndvi = image.normlizedDifference([nir,red])
    return image.addBands(ndvi)

