import numpy as np
from osgeo import gdal
from osgeo import gdal_array

def write_geotiff(out_file, in_arr, geotran, srs_wkt):
    """
    in_arr must be in channels, rows, cols
    """
    driver = gdal.GetDriverByName('GTiff')
    if in_arr.dtype == np.uint64 or in_arr.dtype == np.int64:
        in_arr = in_arr.astype(float)
    type_code = gdal_array.NumericTypeCodeToGDALTypeCode(in_arr.dtype) # get the numpy array data type
    if len(in_arr.shape) == 3: # if the shape is (bands, rows, columns)
        out = driver.Create(out_file, in_arr.shape[2], in_arr.shape[1], in_arr.shape[0], type_code)
        out.SetGeoTransform(geotran) 
        for b in range(in_arr.shape[0]):
            outband = out.GetRasterBand(b+1)
            outband.WriteArray(in_arr[b])
            outband.FlushCache()
    elif len(in_arr.shape) == 4:
        nbands = np.prod([n for n in in_arr.shape[:-2]])
        out = driver.Create(out_file, in_arr.shape[-1], in_arr.shape[-2], int(nbands), type_code)
        out.SetGeoTransform(geotran)
        b = 1
        for b1 in range(in_arr.shape[0]):
            for b2 in range(in_arr.shape[1]):
                outband = out.GetRasterBand(b)
                outband.WriteArray(in_arr[b1,b2,:,:])
                outband.FlushCache()
                b+=1
    else:
        out = driver.Create(out_file, in_arr.shape[1], in_arr.shape[0], 1, type_code)
        out.SetGeoTransform(geotran) # the origin is the upper left of the input shapefile
        outband = out.GetRasterBand(1)
        outband.WriteArray(in_arr)
        outband.FlushCache()
    out.SetProjection(srs_wkt)
    
def read_geotiff(image):
    return NotImplemented