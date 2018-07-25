import numpy as np
from osgeo import gdal

def write_geotiff(out_file, in_arr, geotran, srs_wkt):
    """
    in_arr must be in channels, rows, cols
    """
    driver = gdal.GetDriverByName('GTiff')
    if len(in_arr.shape) == 3: # if the shape is (bands, rows, columns)
        out = driver.Create(out_file, in_arr.shape[2], in_arr.shape[1], in_arr.shape[0], gdal.GDT_Float64)
        out.SetGeoTransform(geotran) # the origin is the upper left of the input shapefile
        for b in range(in_arr.shape[0]):
            outband = out.GetRasterBand(b+1)
            outband.WriteArray(in_arr[b])
            outband.FlushCache()
    else:
        out = driver.Create(out_file, in_arr.shape[1], in_arr.shape[0], 1, gdal.GDT_Float64)
        out.SetGeoTransform(geotran) # the origin is the upper left of the input shapefile
        outband = out.GetRasterBand(1)
        outband.WriteArray(in_arr)
        outband.FlushCache()
    out.SetProjection(srs_wkt)
    
def read_geotiff(image):
    return NotImplemented