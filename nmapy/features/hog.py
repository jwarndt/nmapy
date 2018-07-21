from skimage.feature import hog
import numpy as np
from osgeo import gdal
from osgeo import osr

from ..utilities.stats import *
from ..utilities.io import *
from .global_vars import * # this gets access to global variables that are used with the features like MAX_SCALE

def hog_feature(image_name, block, scale, output=None, stat=None):
    """
    Parameters:
    ----------
    image_name: str
    block: int
    scale: int
    
    Returns:
    --------
    out_image: 3D ndarray
    """
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
    
    image = np.moveaxis(image, 0, -1) # expects an image in rows, columns, channels
    out_image = []
    for i in range(0, image.shape[0], block):
        outrow = []
        if i >= MAX_SCALE and i <= image.shape[0] - MAX_SCALE:
            for j in range(0, image.shape[1], block):
                if j >= MAX_SCALE and j <= image.shape[1] - MAX_SCALE:
                    block_arr = image[i:i+block,j:j+block]
                    center_i = int(i+block/2)
                    center_j = int(j+block/2)
                    # catch the origin coordinates for writing the output
                    if len(out_image) == 0 and len(outrow) == 0:
                        out_uly = uly + cell_height * (center_i - block)
                        out_ulx = ulx + cell_width * (center_j - block)
                    if block%2 != 0 and scale%2 == 0: # make sure the scale window is the correct size for the block
                        scale_arr = image[center_i-int(scale/2):center_i+int(scale/2),center_j-int(scale/2):center_j+int(scale/2)]
                    else:
                        scale_arr = image[center_i-int(scale/2):center_i+int(scale/2)+1,center_j-int(scale/2):center_j+int(scale/2)+1]      
                    fd = hog(scale_arr, orientations=8, pixels_per_cell=(scale_arr.shape[0], scale_arr.shape[1]), cells_per_block=(1, 1), multichannel=True, feature_vector=False)
                    outrow.append(fd.flatten())
            out_image.append(outrow)
    out_arr = np.moveaxis(out_image, -1, 0)
    
    """for i in range(int(scale/2), image.shape[0] - int(scale/2), block):
        outrow = []
        for j in range(int(scale/2), image.shape[1] - int(scale/2), block):
            block_arr = image[i:i+block,j:j+block]
            center_i = int(i+block/2)
            center_j = int(j+block/2)
            if len(out_image) == 0 and len(outrow) == 0:
                out_uly = uly + cell_height * (center_i - block)
                out_ulx = ulx + cell_width * (center_j - block)
            if block%2 != 0 and scale%2 == 0: # make sure the scale window is the correct size for the block
                scale_arr = image[center_i-int(scale/2):center_i+int(scale/2),center_j-int(scale/2):center_j+int(scale/2)]
            else:
                scale_arr = image[center_i-int(scale/2):center_i+int(scale/2)+1,center_j-int(scale/2):center_j+int(scale/2)+1]      
            fd = hog(scale_arr, orientations=8, pixels_per_cell=(scale_arr.shape[0], scale_arr.shape[1]), cells_per_block=(1, 1), multichannel=True, feature_vector=False)
            outrow.append(fd.flatten())
        out_image.append(outrow)
    out_arr = np.moveaxis(out_image, -1, 0)"""
    
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