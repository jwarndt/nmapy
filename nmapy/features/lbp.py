# local binary pattern
import numpy as np
import skimage
from skimage.feature import local_binary_pattern
from skimage.color import rgb2gray
from osgeo import gdal
from osgeo import osr


from ..utilities.stats import *
from ..utilities.io import *
from .global_vars import * # this gets access to global variables that are used with the features like MAX_SCALE

def lbp_feature(image_name, block, scale, output=None, method='default', radius=[1], n_points=[8], stat=None):
    assert(len(radius) == len(n_points))

    # radius=[4, 4, 8, 8, 16, 16],
    # n_points=[8, 16, 8, 16, 32, 64]

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

    lbps = []
    n = 0
    while n < len(radius):
        lbps.append(local_binary_pattern(image, n_points[n], radius[n], method))
        n+=1
    lbps = np.array(lbps) # an ndarray of shape=(len(radius), image.shape[0], image.shape[1])
    if stat == None:
        if output:
            write_geotiff(output, lbps, geotran, out_srs_wkt)
            return
        else:
            return lbps

    out_image = []
    for i in range(0, image.shape[0], block):
        outrow = []
        if i >= MAX_SCALE and i <= image.shape[0] - MAX_SCALE:
            for j in range(0, image.shape[1], block):
                if j >= MAX_SCALE and j <= image.shape[1] - MAX_SCALE:
                    block_arr = lbps[:,i:i+block,j:j+block]
                    center_i = int(i+block/2)
                    center_j = int(j+block/2)
                    # catch the origin coordinates for writing the output
                    if len(out_image) == 0 and len(outrow) == 0:
                        out_uly = uly + cell_height * (center_i - block)
                        out_ulx = ulx + cell_width * (center_j - block)
                    if block%2 != 0 and scale%2 == 0: # make sure the scale window is the correct size for the block
                        scale_arr = lbps[:, center_i-int(scale/2):center_i+int(scale/2),center_j-int(scale/2):center_j+int(scale/2)]
                    else:
                        scale_arr = lbps[:, center_i-int(scale/2):center_i+int(scale/2)+1,center_j-int(scale/2):center_j+int(scale/2)+1]
                    if stat:
                        out = calc_stat(scale_arr, stat, (1,2)) # out is a 2D array of shape (n_stats, n_lbps)
                    outrow.append(out)
            out_image.append(outrow)
    out_image = np.array(out_image)
    out_image = np.moveaxis(out_image, 0, -1)
    out_image = np.moveaxis(out_image, 0, -1)
    if output:
        out_geotran = (out_ulx, out_cell_width, 0, out_uly, 0, out_cell_height)
        write_geotiff(output, out_image, out_geotran, out_srs_wkt)
    else:
        return np.array(out_image)

#lbp = local_binary_pattern(output, 50, 50, output=None, "n_points"=n_points, "radius"=radius, "method"=lbp_method)

def clbp():
    return NotImplemented