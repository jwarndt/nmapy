# local binary pattern
import numpy as np
from skimage.feature import local_binary_pattern
from osgeo import gdal
from osgeo import osr

from ..utilities.stats import *
from ..utilities.io import *
from .global_vars import * # this gets access to global variables that are used with the features like MAX_SCALE

def lbp_feature(image_name, block, scale, output=None, method='default', radius=1, n_points=8):
    ds = gdal.Open(image_name)
    image = ds.ReadAsArray()
    geotran = ds.GetGeoTransform()
    ulx = geotran[0]
    uly = geotran[3]
    cell_width = geotran[1]
    cell_height = geotran[5]
    
    out_srs = osr.SpatialReference()
    out_srs.ImportFromEPSG(4326)
    out_srs_wkt = out_srs.ExportToWkt()
    out_cell_width = block * cell_width
    out_cell_height = block * cell_height
    
    ds = None
    image = np.moveaxis(image, 0, -1)
    image = skimage.img_as_ubyte(rgb2gray(image)) # lbp takes a gray level image

    out_image = []
    for i in range(0, image.shape[0], block):
        outrow = []
        if i >= MAX_SCALE and i <= image.shape[0] - MAX_SCALE:
            for j in range(0, image.shape[1], block):
                if j >= MAX_SCALE and j <= image.shape[1] - MAX_SCALE:
                    print('hi')


    if output:
        if stat:
            out_arr = calc_stat(out_arr, stat, 0)
        out_geotran = (out_ulx, out_cell_width, 0, out_uly, 0, out_cell_height)
        # this should be a standardized write geotiff function
        write_geotiff(output, out_arr, out_geotran, out_srs_wkt)
    else:
        if stat:
            out_arr = calc_stat(out_arr, stat, 0)
        return np.array(out_arr)

#lbp = local_binary_pattern(output, 50, 50, output=None, "n_points"=n_points, "radius"=radius, "method"=lbp_method)